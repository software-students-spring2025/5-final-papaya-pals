"""This module contains functionality to run the Wheel of Fortune game"""
# pylint: disable=import-error,duplicate-code,trailing-whitespace,line-too-long

import random
import streamlit as st  # pylint: disable=import-error


def choose_bet(bet_values):
    """Helper to choose bet value."""
    cols = st.columns(6)
    for i, val in enumerate(bet_values):
        if cols[i].button(f"Bet ${val}", key=f"wheel_bet_{val}"):
            if val <= st.session_state.bankroll:
                st.session_state.wheel_bet_amount = val
            else:
                st.warning("You don't have enough funds for that bet.")
    return 0


def spin_wheel():
    """Spin the wheel and return the result"""
    # Wheel segments with associated multipliers
    segments = [
        ("2X", 2),
        ("1/2X", 0.5),
        ("3X", 3),
        ("Bankrupt", 0),
        ("1X", 1),
        ("2X", 2),
        ("5X", 5),
        ("1/2X", 0.5),
        ("1X", 1),
        ("3X", 3),
        ("Jackpot", 10),
        ("Bankrupt", 0),
        ("2X", 2),
        ("1X", 1),
        ("3X", 3),
        ("1/2X", 0.5),
    ]
    return random.choice(segments)


def display_wheel_spin_animation():
    """Display a simple wheel spin animation"""
    # Simple animation placeholder
    spinning = st.empty()
    for i in range(3):
        spinning.markdown(f"**Spinning{'.' * (i + 1)}**")
        st.session_state.wheel_segment = spin_wheel()


def evaluate_wheel_result(segment, bet_amount):
    """Evaluates the wheel spin result."""
    label, multiplier = segment

    if label == "Bankrupt":
        return 0, [("error", "Bankrupt! You lost your bet.")]

    if label == "Jackpot":
        winnings = bet_amount * multiplier
        return winnings, [("success", f"Jackpot! You won ${winnings}!")]

    winnings = int(bet_amount * multiplier)
    if multiplier < 1:
        return winnings, [("warning", f"{label}! You got back ${winnings}.")]

    return winnings, [("success", f"{label}! You won ${winnings}!")]


def play_wheel():
    """This function runs the Wheel of Fortune game"""

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Wheel of Fortune! 🎡")
    with col2:
        st.markdown(f"**Shame Counter:** {st.session_state.shame_counter}")

    st.write(f"Bankroll: ${st.session_state.bankroll}")

    # Initialize bet amount if not already set
    if "wheel_bet_amount" not in st.session_state:
        st.session_state.wheel_bet_amount = 10

    # Initialize wheel segment for state persistence
    if "wheel_segment" not in st.session_state:
        st.session_state.wheel_segment = None

    st.write(f"Current Bet: ${st.session_state.wheel_bet_amount}")

    # Choose bet amount
    st.markdown("#### Choose your bet:")
    bet_values = [1, 5, 10, 50, 100, 1000]
    selected_bet = choose_bet(bet_values)

    # Update bet if a valid amount is selected
    if selected_bet != 0:
        st.session_state.wheel_bet_amount = selected_bet

    # Display wheel segments information
    st.markdown("#### Wheel Segments:")
    st.markdown(
        """
    - **2X** - Double your bet
    - **3X** - Triple your bet
    - **5X** - 5 times your bet
    - **1X** - Get your bet back
    - **1/2X** - Get half your bet back
    - **Jackpot** - 10 times your bet
    - **Bankrupt** - Lose your bet
    """
    )

    # Spin the wheel button
    if st.button("Spin the Wheel! 🎡"):
        wheel_bet_amount = st.session_state.wheel_bet_amount

        if wheel_bet_amount > st.session_state.bankroll:
            st.warning("You don't have enough funds to place this bet.")
            return

        # Deduct bet from bankroll
        st.session_state.bankroll -= wheel_bet_amount

        # Spin animation
        display_wheel_spin_animation()

        # Get result
        segment = st.session_state.wheel_segment

        # Display the result
        st.markdown(
            f"<div style='font-size: 72px; text-align: center;'>{segment[0]}</div>",
            unsafe_allow_html=True,
        )

        # Evaluate the result
        winnings, messages = evaluate_wheel_result(segment, wheel_bet_amount)

        # Display result messages
        for level, msg in messages:
            getattr(st, level)(msg)

        # Update bankroll with winnings
        st.session_state.bankroll += winnings
