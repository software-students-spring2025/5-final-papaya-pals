# web-app/app_pages/register.py

import streamlit as st
from db import create_user, get_user

def show_register():
    st.title("Register")

    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")

    if st.button("Register"):
        # Check if user already exists
        if get_user(username, password):
            st.warning("User already exists. Try logging in.")
        else:
            new_user = create_user(username, password)
            if new_user:
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Registration failed.")
