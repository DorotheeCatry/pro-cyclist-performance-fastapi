import streamlit as st 
import requests
from dotenv import load_dotenv
import os
from enums import States
from streamlit_functions import display_sidebar, fetch_athletes_list, select_athlete_callback
import pandas as pd

# region INIT
if "init" not in st.session_state:
    load_dotenv()
    st.session_state.init = True
    st.session_state.api_url = os.getenv("API_URL")
    st.session_state.state = States.HOME
    st.session_state.api_url_users = st.session_state.api_url+"users/"
    st.session_state.api_url_auth = st.session_state.api_url+"auth/"
    st.session_state.api_url_stats = st.session_state.api_url+"stats/"
    st.session_state.token = ""
    st.session_state.login = False
    st.session_state.current_user = {}
    st.session_state.popup_message = ""
    st.session_state.headers = ""
    st.session_state.athlete_list = []
    st.session_state.current_selected_athlete = ""
    
    st.session_state.force_callback_on_first_dashboard_render = True


# region COMMON UI
display_sidebar()

if st.session_state.popup_message != "":
    st.success(st.session_state.popup_message)
    st.session_state.popup_message = ""

match st.session_state.state:
    # region HOMEPAGE
    case States.HOME:
        st.title(":green[PRO CYCLING TEAM]")
        st.image("streamlit_app/images/home.jpeg", caption="Ultimate datas, ultimate performances!")

    # region LOGIN
    case States.LOGIN:
        with st.form("Login"):
            email_login = st.text_input("Email :")
            password_login = st.text_input("Password :", type="password")
            if st.form_submit_button("Login"):
                data = {"email" : email_login, "password": password_login}
                response = requests.post(st.session_state.api_url_auth+"login/", json=data).json()
                try:
                    st.session_state.token = response["access_token"]
                    st.session_state.current_user = response["user"]
                    st.session_state.login = True
                    st.session_state.state = States.HOME
                    st.session_state.headers = {
                "Authorization": f"Bearer {st.session_state.token}"
                }
                    if response["user"]["role"] == 0:
                        fetch_athletes_list()
                        
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
    
    # region REGISTRATION
    case States.REGISTER:
        with st.form("Register"):
            username_register = st.text_input("Username :", max_chars=16)
            email_register = st.text_input("Email :")
            password_register = st.text_input("Password :", type="password", max_chars=16)
            password_verification_register = st.text_input("Verify password :", type="password", max_chars=16)
            if st.form_submit_button("Submit"):
                if password_register != password_verification_register:
                    st.error("Password does not match verification.")    
                else:
                    data = {"username": username_register, "email": email_register, "password": password_register, "role": 1}
                    response = requests.post(st.session_state.api_url_auth+"register/", json = data).json()
                    if response["status"] == 0:
                        st.error(response["message"])
                    else:
                        st.session_state.popup_message = response["message"]
                        st.session_state.state = States.HOME
                        st.rerun()
    
    # region ATHLETE INFO
    case States.ATHLETE_INFO:
        athlete = requests.post(st.session_state.api_url_users+"get_athlete/", params={"athlete_id":st.session_state.current_user["id"]}).json()
        with st.form("modify_athlete_form"):
            st.write("MODIFY ATHLETE INFOS : ")
            first_name_info = st.text_input("First name :", value=athlete["first_name"])
            last_name_info = st.text_input("Last name :", value=athlete["last_name"])
            sex_info = st.radio("Sex :", ["Female", "Male"],index=athlete["sex"])
            age_info = st.number_input("Age :", min_value=15, max_value=100, value=athlete["age"])
            height_info = st.slider("Height (cm) :", min_value=0, max_value=250, value=athlete["height"], step=1)
            weight_info = st.slider("Weight (kg)", min_value=0.0, max_value=250.0, step=0.1, value=athlete["weight"])
            vo2_max_info = st.slider("VO2 Max :", min_value=0, max_value=100, value=athlete["VO2_max"])
            if st.form_submit_button():
                sex = 0 if sex_info == "Female" else 1
                data = {"sex": sex, "first_name": first_name_info, "last_name": last_name_info, "age": age_info, "height": height_info, \
                    "weight": weight_info, "VO2_max": vo2_max_info}
                response = requests.post(st.session_state.api_url_users+"modify_athlete", \
                    params={"id":st.session_state.current_user["id"]}, json=data, headers=st.session_state.headers).json()
                if response["status"]:
                    st.session_state.popup_message = response["message"]
                    st.session_state.state = States.HOME
                    st.rerun()
                else:
                    st.error(response["message"])
    
    # region ACCOUNT
    case States.ACCOUNT:
        if st.button("Delete account"):
            try:
                response = requests.get(st.session_state.api_url_users+"delete_account", headers=st.session_state.headers).json()
                st.session_state.popup_message = response["message"]
                st.session_state.current_user = {}
                st.session_state.login = False
                st.session_state.token = ""
                st.session_state.state = States.HOME
                st.rerun()
            except Exception as e:
                st.error(str(e))
            
    # region SESSIONS
    case States.SESSIONS:
        
        st.title("MY SESSIONS")
        
        sessions = requests.get(st.session_state.api_url_users+"get_sessions/", headers=st.session_state.headers).json()
        
        fields = ["id", "DATE", 'CADENCE', 'PO', 'HR', 'RF', "VO2", "FTP", "Rating"]
        working_fields=['CADENCE', 'PO', 'HR', 'RF', "VO2", "FTP"]
        
        sessions = pd.DataFrame(sessions)
        sessions.drop("athlete_id", axis=1, inplace=True)
        sessions.columns = fields    
        format_dict = {col: '{:.1f}' for col in sessions.select_dtypes(include=['number']).columns if col != 'id'}
        format_dict['id'] = '{:.0f}'
        sessions_styled = sessions.style.highlight_max(subset=working_fields, color="green").highlight_min(subset=working_fields, color="red").format(format_dict)
        st.write(sessions_styled)
        
        if st.button("Add new session"):
            st.session_state.state = States.SESSION_ADD
            st.rerun()
            
    case States.SESSION_ADD:
        
        with st.form("session_add_form"):
            st.title("New training session :")
            cadence_session = st.number_input("Cadence :", min_value=0.0, step=0.1)
            power_output_session = st.number_input("Power Output :", min_value=0.0, step=0.1)
            heart_rate_session = st.number_input("Heart Rate :", min_value=0.0, step=0.1)
            respiratory_frequency_session = st.number_input("Respiratory Frequency :", min_value=0.0, step=0.1)
            vo2_session = st.number_input("VO2", min_value=0.0, step=0.1)
            FTP_session = st.number_input("FTP", min_value=0.0, step=0.1)
            condition_rating_session = st.number_input("Condition Rating :", min_value=1, max_value=5, step=1)
            
            if st.form_submit_button("Submit"):
                data = {"cadence": cadence_session, "power_output": power_output_session, \
                    "heart_rate": heart_rate_session, "respiratory_frequency": respiratory_frequency_session, "VO2":vo2_session, \
                        "FTP": FTP_session, "condition_rating": condition_rating_session}
                
                response = requests.post(st.session_state.api_url_users+"create_session/", \
                    params={"athlete_id": st.session_state.current_user["id"]}, json=data, headers=st.session_state.headers).json()

                if response["status"]:
                    st.session_state.popup_message = response["message"]
                    st.session_state.state=States.SESSIONS
                    st.rerun()
                else:
                    st.error(response["message"])
            
    case States.DASHBOARD_COACH:
        
        st.selectbox("Select an athlete : ", list(enumerate([(x["first_name"]+" "+x["last_name"]) for x in st.session_state.athlete_list])), \
            format_func=lambda option: option[1], key="athlete_index", on_change=select_athlete_callback)
        
        if  st.session_state.force_callback_on_first_dashboard_render:
            select_athlete_callback()
            st.session_state.force_callback_on_first_dashboard_render = False
        
        st.title(st.session_state.current_selected_athlete["first_name"]+ " " +st.session_state.current_selected_athlete["last_name"])
        
        sessions = requests.get(st.session_state.api_url_users+"get_sessions_coach/", params={"athlete_id": st.session_state.current_selected_athlete["user_id"]}, headers=st.session_state.headers).json()
        
        fields = ["id", "DATE", 'CADENCE', 'PO', 'HR', 'RF', "VO2", "FTP", "Rating"]
        working_fields=['CADENCE', 'PO', 'HR', 'RF', "VO2", "FTP"]
        
        sessions = pd.DataFrame(sessions)
        sessions.drop("athlete_id", axis=1, inplace=True)
        sessions.columns = fields    
        format_dict = {col: '{:.1f}' for col in sessions.select_dtypes(include=['number']).columns if col != 'id'}
        format_dict['id'] = '{:.0f}'
        sessions_styled = sessions.style.highlight_max(subset=working_fields, color="green").highlight_min(subset=working_fields, color="red").format(format_dict)
        st.write(sessions_styled)
        
        
                
            


