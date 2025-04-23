"""This module contains functionality to display the home page"""

import streamlit as st

def show_home():
    """This function displays the page elements for the home page"""

    # home page title
    titlerow = st.columns([0.3, 0.4, 0.3])
    with titlerow[1]:
        st.title("Let's play!")

    # show all game buttons
    row1 = st.columns([0.2, 0.6, 0.2])
    with row1[0]:
        def cb_slots():
            st.session_state.current_page = "slots"
        st.button("Slots", on_click=cb_slots)
    with row1[2]:
        def cb_blackjack():
            st.session_state.current_page = "blackjack"
        st.button("Blackjack", on_click=cb_blackjack)

    row2 = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])
    with row2[1]:
        def cb_roulette():
            st.session_state.current_page = "roulette"
        st.button("Roulette", on_click=cb_roulette)
    with row2[3]:
        def cb_game1():
            st.session_state.current_page = "unknown_game1"
        st.button("[Game 1]", on_click=cb_game1)

    row3 = st.columns([0.35, 0.2, 0.35])
    with row3[2]:
        def cb_game2():
            st.session_state.current_page = "unknown_game2"
        st.button("[Game 2]", on_click=cb_game2)
