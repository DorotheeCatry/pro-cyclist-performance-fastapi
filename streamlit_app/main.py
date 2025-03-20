import streamlit as st 
import requests
from dotenv import load_dotenv
import os
from enums import States
from streamlit_functions import display_sidebar

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


# region COMMON UI
display_sidebar()

if st.session_state.popup_message != "":
    st.success(st.session_state.popup_message)
    st.session_state.popup_message = ""

match st.session_state.state:
    # region HOMEPAGE
    case States.HOME:
        st.write("Home page")

    # region LOGIN
    case States.LOGIN:
        with st.form("Login"):
            email_login = st.text_input("Email :")
            password_login = st.text_input("Password :", type="password")
            if st.form_submit_button("Login"):
                data = {"email" : email_login, "password": password_login}
                response = requests.post(st.session_state.api_url_auth+"login/", params=data).json()
                try:
                    st.session_state.token = response["access_token"]
                    st.session_state.current_user = response["user"]
                    st.session_state.login = True
                    st.session_state.state = States.HOME
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
                    data = {"username": username_register, "email": email_register, "password": password_register, "role": 0}
                    response = requests.post(st.session_state.api_url_auth+"register/", params = data).json()
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
                response = requests.post(st.session_state.api_url_users+"modify_athlete", params={"id":st.session_state.current_user["id"]}, json=data).json()
                if response["status"]:
                    st.session_state.popup_message = response["message"]
                    st.session_state.state = States.HOME
                    st.rerun()
                else:
                    st.error(response["message"])
                

                
                            
            
        


