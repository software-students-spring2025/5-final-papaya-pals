"""This module contains functionality to run the slots game"""

import random
import streamlit as st


def play_slots():
    """This function runs the slots game"""

    all_icons = ["🍒", "🍋", "🔔", "💎", "7️⃣"]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Welcome to Slots! 🎰")
    with col2:
        st.markdown(f"**Shame Counter:** {st.session_state.shame_counter}")

    st.write(f"Bankroll: ${st.session_state.bankroll}")

    _slots_bet = st.number_input(
        "Enter your bet amount:",
        min_value=1,
        max_value=st.session_state.bankroll,
        step=1,
        value=st.session_state.slots_bet_amount,  # This fixed the bet logic
        key="slots_bet_amount",
    )

    # Spin the slot machine
    if st.button("Spin! 💰"):
        slots_bet_amount = st.session_state.slots_bet_amount

        if slots_bet_amount > st.session_state.bankroll:
            st.warning("You don't have enough funds to place this bet.")
        else:
            st.session_state.bankroll -= slots_bet_amount
            chosen_icons = spin(all_icons)
            st.write(" ".join(chosen_icons))
            result, win_amount = payout(chosen_icons, slots_bet_amount)
            st.write(result)
            st.session_state.bankroll += win_amount

            # Add to shame counter
            if st.session_state.bankroll <= 0:
                st.session_state.shame_counter += 1
                st.write("You're bankrupt! Reloading funds...")
                st.session_state.bankroll = 1000


def spin(icons):
    """This function generates a randomly "spun" trio of icons"""

    return [random.choice(icons) for i in range(3)]


def payout(icons, slots_bet_amount):
    """This function calculates the payout"""

    if icons[0] == icons[1] == icons[2] == "7️⃣":
        return "Jackpot! Triple 7️⃣!", 100 * slots_bet_amount
    if icons[0] == icons[1] == icons[2]:
        return "Three of a Kind!", 5 * slots_bet_amount
    if icons[0] == icons[1] or icons[1] == icons[2] or icons[0] == icons[2]:
        return "Small win!", 2 * slots_bet_amount
    return "No Wins.", -slots_bet_amount
