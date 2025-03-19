import streamlit as st 
import requests
from dotenv import load_dotenv
import os

if "init" not in st.session_state:
    load_dotenv()
    st.session_state["init"] = True
    st.session_state.api_url = os.getenv("API_URL")
    st.session_state.api_url_users = st.session_state.api_url+"users/"
    st.session_state.api_url_auth = st.session_state.api_url+""
    st.session_state.token = ""
    st.session_state.login = False
    st.session_state.current_user = {}
    
# data = requests.post(st.session_state.api_url_users+"get_athlete/", params = {"athlete_id": 1}).json()

if not st.session_state.login:

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
else:      
    st.write(st.session_state.current_user)
        


