import streamlit as st

def initial_count():
    if "bankroll" not in st.session_state:
        st.session_state.bankroll = 1000

    if "shame_counter" not in st.session_state:
        st.session_state.shame_counter = 0

    if "bet_amount" not in st.session_state:
        st.session_state.bet_amount = 1