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

display_sidebar()

match st.session_state.state:
    case States.HOME:
        st.write("Home page")

    case States.LOGIN:
        with st.form("Login"):
            email_login = st.text_input("Email :")
            password_login = st.text_input("Password :")
            if st.form_submit_button("Login"):
                data = {"email" : email_login, "password": password_login}
                response = requests.post(st.session_state.api_url_auth+"login/", params=data).json()
                st.session_state.api_url_auth+"login/"
                st.session_state.token = response["access_token"]
                st.session_state.current_user = response["user"]
                st.session_state.login = True
                st.session_state.state = States.HOME
                st.rerun()
        


