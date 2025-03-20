import streamlit as st
from typing import cast
from enums import States

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
            
            if st.button("Info"):
                st.session_state.state = States.ATHLETE_INFO
                st.rerun()
            
       

                    
   