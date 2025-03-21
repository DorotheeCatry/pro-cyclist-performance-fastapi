import streamlit as st
from enums import States
import requests

def fetch_athletes_list():
    
    st.session_state.athlete_list = requests.get(st.session_state.api_url_users+"get_athlete_list/", headers=st.session_state.headers).json()

def select_athlete_callback():
    selected_index, selected_name = st.session_state.athlete_index
    st.session_state.current_selected_athlete = st.session_state.athlete_list[selected_index]
    # st.write(f"Currently selected : {st.session_state.current_selected_athlete["first_name"]} {st.session_state.current_selected_athlete["last_name"]}.")

def display_sidebar() -> None:
    """
    Display the navigation sidebar
    """
    
    with st.sidebar:
        
        if st.button("Home"):
            st.session_state.state = States.HOME
            st.rerun()  
        
        st.divider()
        
        if not st.session_state.login:            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login"):
                    st.session_state.state = States.LOGIN
                    st.rerun()
            
            with col2:
                if st.button("Register"):
                    st.session_state.state = States.REGISTER
                    st.rerun()
        
        else:
            st.write(f"Welcome {st.session_state.current_user["username"]}.")
            if st.button("Logout"):
                st.session_state.current_user = {}
                st.session_state.login = False
                st.session_state.token = ""
                st.session_state.state = States.HOME
                st.rerun()
            
            if st.button("Account"):
                st.session_state.state = States.ACCOUNT
                st.rerun()
            
            if st.session_state.current_user["role"] == 1:                
                if st.button("My infos"):
                    st.session_state.state = States.ATHLETE_INFO
                    st.rerun()
            
            if st.session_state.current_user["role"] == 1:
                if st.button("My sessions"):
                    st.session_state.state = States.SESSIONS
                    st.rerun()
            
            if st.session_state.current_user["role"] == 0:
                if st.button("Dashboard"):
                    st.session_state.state = States.DASHBOARD_COACH
                    st.session_state.force_callback_on_first_dashboard_render = True
                    st.rerun()
                
        
            
       

                    
   