import streamlit as st
from typing import cast
from enums import States

def display_sidebar() -> None:
    """
    Display the current game state in the sidebar
    """
    
    with st.sidebar:
        # x = 0        
        # st.divider()
        
        if not st.session_state.login:            
        
            if st.button("login"):
                st.session_state.state = States.LOGIN
                st.rerun()
        
        else:
            st.write(f"Welcome {st.session_state.current_user["username"]}.")
            if st.button("Logout"):
                st.session_state.current_user = {}
                st.session_state.login = False
                st.session_state.token = ""
                st.session_state.state = States.HOME
                st.rerun()
            
       

                    
   