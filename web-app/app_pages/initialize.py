"""This module provides functionality to handle setting and manipulating session variables"""

import streamlit as st
from .games.blackjack.gameplay import start_game_cached


def set_default_session_vars():
    """
    This function checks that every necessary session variable has been set to
        at least the default value.
    It will not change any session variables that already exist.
    """

    # global
    if "bankroll" not in st.session_state:
        st.session_state.bankroll = 1000
    if "shame_counter" not in st.session_state:
        st.session_state.shame_counter = 0
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    if "user" not in st.session_state:
        st.session_state.user = ""
    # slots
    if "slots_bet_amount" not in st.session_state:
        st.session_state.slots_bet_amount = 1
    # roulette
    if "roulette_bet_amount" not in st.session_state:
        st.session_state.roulette_bet_amount = 1
    # blackjack
    if "blackjack" not in st.session_state:
        st.session_state.blackjack = "new"
        start_game_cached.clear()
    if "blackjack_bet_amount" not in st.session_state:
        st.session_state.blackjack_bet_amount = 0
    if "blackjack_hits" not in st.session_state:
        st.session_state.blackjack_hits = 0
    if "blackjack_stood" not in st.session_state:
        st.session_state.blackjack_stood = False


def reset_to_default(old_page):
    """
    This function resets any session vars to their default values.
    This means you can navigate to the homepage from the blackjack page;
        when you later return to the blackjack page, the session variables
        for blackjack will be reset to a new game.
    """

    if old_page == "blackjack":
        st.session_state.blackjack = "new"
        start_game_cached.clear()
        st.session_state.blackjack_hits = 0
        st.session_state.blackjack_stood = False
        st.session_state.blackjack_bet_amount = 0
