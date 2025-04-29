"""This module contains functionality to run the dice game (simplified craps)"""

import random
import streamlit as st  # pylint: disable=import-error


def choose_bet(bet_values):
    """Helper to choose bet value."""
    cols = st.columns(6)
    for i, val in enumerate(bet_values):
        if cols[i].button(f"Bet ${val}", key=f"dice_bet_{val}"):
            if val <= st.session_state.bankroll:
                st.session_state.dice_bet_amount = val
            else:
                st.warning("You don't have enough funds for that bet.")
    return 0


def roll_dice():
    """Roll two dice and return their values"""
    return random.randint(1, 6), random.randint(1, 6)


def display_die(value):
    """Convert a die value to an emoji representation"""
    die_faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
    return die_faces[value]


# pylint: disable=too-many-branches
def evaluate_dice_result(bet_option, hard_way_choice, die1, die2, bet_amount):
    """Evaluates the dice roll result."""
    total = die1 + die2
    winnings = 0
    messages = []

    if bet_option == "Pass Line":
        # Simplified Pass Line bet (win on 7, 11; lose on 2, 3, 12)
        if total in (7, 11):
            winnings += bet_amount
            messages.append(("success", "Pass Line Win!"))
        elif total in (2, 3, 12):
            messages.append(("error", "Pass Line Loss!"))
        else:
            messages.append(("info", f"Point established at {total}. Roll again!"))
            winnings = 0  # Return the bet

    elif bet_option == "Don't Pass Line":
        # Simplified Don't Pass bet (win on 2, 3; lose on 7, 11; push on 12)
        if total in (2, 3):
            winnings += bet_amount
            messages.append(("success", "Don't Pass Win!"))
        elif total in (7, 11):
            messages.append(("error", "Don't Pass Loss!"))
        elif total == 12:
            winnings = bet_amount  # Return the bet on push
            messages.append(("info", "Push on 12!"))
        else:
            messages.append(("info", f"Point established at {total}. Roll again!"))
            winnings = 0  # Return the bet

    elif bet_option == "Any 7":
        # Win only on a 7
        if total == 7:
            winnings += bet_amount * 4
            messages.append(("success", "Any 7 Win!"))
        else:
            messages.append(("error", "Any 7 Loss!"))

    elif bet_option == "Field":
        # Field bet (win on 2, 3, 4, 9, 10, 11, 12; double on 2, 12)
        if total in (2, 12):
            winnings += bet_amount * 2
            messages.append(("success", f"Field Win on {total}! Double payout!"))
        elif total in (3, 4, 9, 10, 11):
            winnings += bet_amount
            messages.append(("success", f"Field Win on {total}!"))
        else:
            messages.append(("error", "Field Loss!"))

    elif bet_option == "Hard Ways":
        return evaluate_hard_way(hard_way_choice, die1, die2, bet_amount)

    return winnings, messages


# pylint: disable=too-many-branches
def evaluate_hard_way(hard_way_bet, die1, die2, bet_amount):
    """Evaluate Hard Way bets"""
    winnings = 0
    messages = []
    total = die1 + die2

    # Check if the dice match the hard way bet
    if hard_way_bet == "Hard 4 (2-2)":
        if die1 == 2 and die2 == 2:
            winnings += bet_amount * 7
            messages.append(("success", "Hard 4 Win!"))
        elif total == 4:
            messages.append(("error", "Easy 4, Hard Way Loss!"))
        elif total == 7:
            messages.append(("error", "Seven Out! Hard Way Loss!"))
        else:
            winnings = 0  # Bet remains active
            messages.append(("info", "Hard Way bet remains active"))

    elif hard_way_bet == "Hard 6 (3-3)":
        if die1 == 3 and die2 == 3:
            winnings += bet_amount * 9
            messages.append(("success", "Hard 6 Win!"))
        elif total == 6:
            messages.append(("error", "Easy 6, Hard Way Loss!"))
        elif total == 7:
            messages.append(("error", "Seven Out! Hard Way Loss!"))
        else:
            winnings = 0  # Bet remains active
            messages.append(("info", "Hard Way bet remains active"))

    elif hard_way_bet == "Hard 8 (4-4)":
        if die1 == 4 and die2 == 4:
            winnings += bet_amount * 9
            messages.append(("success", "Hard 8 Win!"))
        elif total == 8:
            messages.append(("error", "Easy 8, Hard Way Loss!"))
        elif total == 7:
            messages.append(("error", "Seven Out! Hard Way Loss!"))
        else:
            winnings = 0  # Bet remains active
            messages.append(("info", "Hard Way bet remains active"))

    elif hard_way_bet == "Hard 10 (5-5)":
        if die1 == 5 and die2 == 5:
            winnings += bet_amount * 7
            messages.append(("success", "Hard 10 Win!"))
        elif total == 10:
            messages.append(("error", "Easy 10, Hard Way Loss!"))
        elif total == 7:
            messages.append(("error", "Seven Out! Hard Way Loss!"))
        else:
            winnings = 0  # Bet remains active
            messages.append(("info", "Hard Way bet remains active"))

    return winnings, messages


def play_dice():
    """This function runs the dice game (simplified craps)"""

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Dice Casino! 🎲🎲")
    with col2:
        st.markdown(f"**Shame Counter:** {st.session_state.shame_counter}")

    st.write(f"Bankroll: ${st.session_state.bankroll}")

    # Initialize bet amount if not already set
    if "dice_bet_amount" not in st.session_state:
        st.session_state.dice_bet_amount = 10

    st.write(f"Current Bet: ${st.session_state.dice_bet_amount}")

    # Choose bet amount
    st.markdown("#### Choose your bet:")
    bet_values = [1, 5, 10, 50, 100, 1000]
    selected_bet = choose_bet(bet_values)

    # Update bet if a valid amount is selected
    if selected_bet != 0:
        st.session_state.dice_bet_amount = selected_bet
        st.session_state.bankroll -= selected_bet

    # Betting options
    st.markdown("#### Choose your bet type:")
    bet_option = st.radio(
        "Bet on:", ["Pass Line", "Don't Pass Line", "Any 7", "Hard Ways", "Field"]
    )

    # Additional options for Hard Ways
    hard_way_choice = None
    if bet_option == "Hard Ways":
        hard_way_choice = st.selectbox(
            "Select Hard Way bet:",
            ["Hard 4 (2-2)", "Hard 6 (3-3)", "Hard 8 (4-4)", "Hard 10 (5-5)"],
        )

    # Roll the dice button
    if st.button("Roll the Dice! 🎲"):
        dice_bet_amount = st.session_state.dice_bet_amount

        if dice_bet_amount > st.session_state.bankroll:
            st.warning("You don't have enough funds to place this bet.")
            return

        # Deduct bet from bankroll
        st.session_state.bankroll -= dice_bet_amount

        # Roll the dice
        die1, die2 = roll_dice()
        total = die1 + die2

        # Display the dice
        dice_display = "<div style='font-size: 72px; text-align: center;'>"
        dice_display += f"{display_die(die1)} {display_die(die2)}</div>"
        st.markdown(dice_display, unsafe_allow_html=True)

        st.markdown(
            f"<div style='text-align: center; font-size: 24px;'>You rolled: {total}</div>",
            unsafe_allow_html=True,
        )

        # Evaluate the result
        winnings, messages = evaluate_dice_result(
            bet_option, hard_way_choice, die1, die2, dice_bet_amount
        )

        # Display result messages
        for level, msg in messages:
            getattr(st, level)(msg)

        # Update bankroll with winnings
        st.session_state.bankroll += winnings

        if not messages:
            st.error("No result determined. Please try again.")
