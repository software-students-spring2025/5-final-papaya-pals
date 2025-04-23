import streamlit as st
from blackjack.gameplay import start_game_cached

def set_default_session_vars():
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