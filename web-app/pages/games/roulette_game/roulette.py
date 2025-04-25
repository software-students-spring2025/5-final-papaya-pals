"""This module provides functionality to run the roulette game"""

import random
import streamlit as st


# Standard European roulette red numbers
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}


def get_color(num):
    """This function returns the color of the chosen number"""

    if num == 0:
        return "Green"
    return "Red" if num in RED_NUMBERS else "Black"


def play_roulette():
    """This function runs the roulette game"""

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Welcome to Roulette! 🎡")
    with col2:
        st.markdown(f"**Shame Counter:** {st.session_state.shame_counter}")

    st.write(f"Bankroll: ${st.session_state.bankroll}")
    st.write(f"Current Bet: ${st.session_state.roulette_bet_amount}")

    # Changed way to choose bets
    st.markdown("#### Choose your bet:")
    cols = st.columns(6)
    bet_values = [1, 5, 10, 50, 100, 1000]
    for i, val in enumerate(bet_values):
        if cols[i].button(f"Bet ${val}"):
            if val <= st.session_state.bankroll:
                st.session_state.roulette_bet_amount = val
                st.session_state.bankroll -= val
            else:
                st.warning("You don't have enough funds for that bet.")


    # Main number pick (optional)
    number_pick = st.number_input(
        "Pick a number (0–36) [Optional]", min_value=0, max_value=36, step=1
    )

    # Red/Black selection
    color_bet = st.radio("Bet on a color:", ["None", "Red", "Black"])

    # Even/Odd selection
    parity_bet = st.radio("Bet on Even or Odd:", ["None", "Even", "Odd"])

    if st.button("Spin the Wheel 🎯"):
        bet = st.session_state.roulette_bet_amount

        if bet > st.session_state.bankroll:
            st.warning("You don't have enough funds to place this bet.")
            return

        # else: if funds are sufficient
        st.session_state.bankroll -= bet
        result = random.randint(0, 36)
        result_color = get_color(result)
        st.write(f"The ball landed on: **{result} ({result_color})**")

        winnings = 0

        # Number bet
        if result == number_pick:
            winnings += 35 * bet
            st.success("You hit your number!")
        else:
            st.info("You did not hit your number.")

        # Color bet
        if color_bet != "None" and result != 0:
            if result_color.lower() == color_bet.lower():
                winnings += bet
                st.success("Color match!")
            else:
                st.info("No match on color.")

        # Even/Odd bet
        if parity_bet != "None" and result != 0:
            if (parity_bet == "Even" and result % 2 == 0) or (
                parity_bet == "Odd" and result % 2 == 1
            ):
                winnings += bet
                st.success("Parity match!")
            else:
                st.info("No match on even/odd.")

        st.session_state.bankroll += winnings

        if winnings == 0:
            st.error("No wins this time!")

        if st.session_state.bankroll <= 0:
            st.session_state.shame_counter += 1
            st.warning("You're bankrupt! Reloading funds...")
            st.session_state.bankroll = 1000
