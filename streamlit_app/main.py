import streamlit as st 
import requests
from dotenv import load_dotenv
import os
from enums import States
from streamlit_functions import display_sidebar

if "init" not in st.session_state:
    load_dotenv()
    st.session_state["init"] = True
    st.session_state.api_url = os.getenv("API_URL")
    st.session_state.state = States.HOME
    st.session_state.api_url_users = st.session_state.api_url+"users/"
    st.session_state.api_url_auth = st.session_state.api_url+"auth/"
    st.session_state.api_url_stats = st.session_state.api_url+"stats/"
    st.session_state.token = ""
    st.session_state.login = False
    st.session_state.current_user = {}
    st.session_state.popup_message = ""

display_sidebar()

if st.session_state.popup_message != "":
    st.success(st.session_state.popup_message)
    st.session_state.popup_message = ""

match st.session_state.state:
    case States.HOME:
        st.write("Home page")

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
                except:
                    st.error("Email or password is incorrect.")
    
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

                
                            
            
        


