"""This module contains functionality to display the home page"""

import streamlit as st


def show_home():
    """This function displays the page elements for the home page"""

    # home page title
    titlerow = st.columns([0.1, 2, 0.1])
    with titlerow[1]:
        st.title("Welcome to the Papaya Pals Casino!")

    st.write("")
    st.write("")

    # show all game buttons
    # row 1 - slots / blackjack / roulette
    row1 = st.columns([1, 1, 1])
    with row1[0]:

        def cb_slots():
            st.session_state.current_page = "slots"

        st.button("Slots 🎰", on_click=cb_slots, use_container_width=True)

    with row1[1]:

        def cb_blackjack():
            st.session_state.current_page = "blackjack"

        st.button("Blackjack 🃏", on_click=cb_blackjack, use_container_width=True)

    with row1[2]:

        def cb_roulette():
            st.session_state.current_page = "roulette"

        st.button("Roulette 🎯", on_click=cb_roulette, use_container_width=True)
