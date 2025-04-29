"""This file loads the page responsible for allowing user to login"""

import time
import streamlit as st
from db import get_user, get_user_data


def show_login():
    """Display the login page where users can authenticate."""
    st.title("Login")

    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        user_id = get_user(username, password)
        if user_id:
            st.success("Login successful!")
            st.session_state.user = username
            user_data = get_user_data(username)
            if user_data:
                st.session_state.bankroll = user_data["bankroll"]
                st.session_state.shame_counter = user_data["shame_counter"]
            else:
                st.session_state.bankroll = 1000
                st.session_state.shame_counter = 0
            
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid username or password.")
