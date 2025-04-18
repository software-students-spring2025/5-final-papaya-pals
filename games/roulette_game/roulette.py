import streamlit as st
import random
from ..initialize import initial_count

colors = ["🔴", "⚫️"]

def play_roulette():
    initial_count()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Welcome to Roulette! 🔴⚫️ ")
    with col2:
        st.markdown(f"**Shame Counter:** {st.session_state.shame_counter}")
        st.write(f"Bankroll: ${st.session_state.bankroll}")
    bet_amount = st.number_input("Enter your bet amount:", min_value=1, max_value=st.session_state.bankroll)
    
    if bet_amount != st.session_state.bet_amount:
        st.session_state.bet_amount = bet_amount

    