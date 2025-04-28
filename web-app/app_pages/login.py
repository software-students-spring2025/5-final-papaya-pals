"""This file loads the page responsible for allowing user to login"""

import streamlit as st
from db import get_user

def show_login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_id = get_user(username, password)
        if user_id:
            st.success(f"Logged in successfully! (user_id: {user_id})")
            # You can use Session State to store logged-in status
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid username or password.")