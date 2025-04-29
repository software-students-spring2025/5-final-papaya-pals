"""Module for user registration page."""

import streamlit as st
from db import create_user, get_user


def show_register():
    """Display the registration page for new users."""
    st.title("Register")

    with st.form("registration_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            # Check if user already exists
            existing_user = get_user(username, password)
            if existing_user:
                st.warning("User already exists.")
            else:
                user = create_user(username, password)
                if user:
                    st.success("Registration successful! You can now log in.")
                else:
                    st.error("Something went wrong during registration.")
