"""This file loads the page responsible for allowing user to login"""

import streamlit as st
from db import get_user


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
            st.success(f"Logged in successfully! (user_id: {user_id})")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid username or password.")
