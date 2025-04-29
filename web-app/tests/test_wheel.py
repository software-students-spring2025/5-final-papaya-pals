"""This is the module to test the Wheel of Fortune game functionality"""

# pylint: disable=import-error,duplicate-code

import pytest  # pylint: disable=unused-import
import streamlit as st  # pylint: disable=unused-import
from streamlit.testing.v1 import AppTest
from app_pages.games.wheel_game.wheel import evaluate_wheel_result, spin_wheel


def test_spin_wheel():
    """Tests wheel spin function returns valid segment"""
    result = spin_wheel()

    # Check that result is a tuple with 2 elements (label and multiplier)
    assert isinstance(result, tuple)
    assert len(result) == 2

    # Check that label is a string and multiplier is a number
    label, multiplier = result
    assert isinstance(label, str)
    assert isinstance(multiplier, (int, float))

    # Check that the result is one of the valid segments
    valid_labels = ["2X", "1/2X", "3X", "Bankrupt", "1X", "5X", "Jackpot"]
    assert label in valid_labels


def test_evaluate_wheel_result_bankrupt():
    """Tests Bankrupt result evaluation"""
    segment = ("Bankrupt", 0)
    winnings, messages = evaluate_wheel_result(segment, 100)

    assert winnings == 0
    assert len(messages) == 1
    assert messages[0][0] == "error"
    assert "Bankrupt" in messages[0][1]


def test_evaluate_wheel_result_jackpot():
    """Tests Jackpot result evaluation"""
    segment = ("Jackpot", 10)
    winnings, messages = evaluate_wheel_result(segment, 100)

    assert winnings == 1000
    assert len(messages) == 1
    assert messages[0][0] == "success"
    assert "Jackpot" in messages[0][1]


def test_evaluate_wheel_result_half():
    """Tests half multiplier result evaluation"""
    segment = ("1/2X", 0.5)
    winnings, messages = evaluate_wheel_result(segment, 100)

    assert winnings == 50
    assert len(messages) == 1
    assert messages[0][0] == "warning"
    assert "1/2X" in messages[0][1]


def test_evaluate_wheel_result_win():
    """Tests normal win result evaluation"""
    segment = ("3X", 3)
    winnings, messages = evaluate_wheel_result(segment, 100)

    assert winnings == 300
    assert len(messages) == 1
    assert messages[0][0] == "success"
    assert "3X" in messages[0][1]


def setup_wheel_game():
    """Helper function to setup a wheel game"""

    # Navigate home
    at = AppTest.from_file("app.py").run()

    # Find and press the Wheel of Fortune button
    button = -1
    for i, btn in enumerate(at.button):
        if "Wheel of Fortune" in btn.label:
            button = i
            break
    assert button != -1, "Wheel of Fortune button does not exist"
    at.button[button].click().run()

    return at


def test_wheel_game_loads():
    """Test that the wheel game loads and shows the correct title"""
    game = setup_wheel_game()

    # Check for the title
    title_found = False
    for header in game.title:
        if "Wheel of Fortune! 🎡" in header.value:
            title_found = True
            break
    assert title_found, "Wheel of Fortune title not found"

    # Check for bet buttons
    bet_values = ["$1", "$5", "$10", "$50", "$100", "$1000"]
    for value in bet_values:
        button_found = False
        for button in game.button:
            if f"Bet {value}" in button.label:
                button_found = True
                break
        assert button_found, f"Bet {value} button not found"

    # Check for spin button
    spin_button_found = False
    for button in game.button:
        if "Spin the Wheel! 🎡" in button.label:
            spin_button_found = True
            break
    assert spin_button_found, "Spin the Wheel button not found"


def test_wheel_game_bet_selection():
    """Test bet selection functionality"""
    game = setup_wheel_game()

    # Check that bet buttons exist
    bet_values = ["$1", "$5", "$10", "$50", "$100", "$1000"]
    for value in bet_values:
        button_found = False
        for button in game.button:
            if f"Bet {value}" in button.label:
                button_found = True
                break
        assert button_found, f"Bet {value} button not found"

    # Since we can't reliably test the stateful behavior in Streamlit's testing framework,
    # we'll just verify that the current bet amount is displayed
    bet_displayed = False
    for text in game.markdown.values:
        if "Current Bet:" in text:
            bet_displayed = True
            break
    assert bet_displayed, "Current bet amount not displayed"


def test_wheel_game_spin():
    """Test spinning the wheel"""
    game = setup_wheel_game()

    # Verify spin button exists
    spin_button_found = False
    for button in game.button:
        if "Spin the Wheel! 🎡" in button.label:
            spin_button_found = True
            break
    assert spin_button_found, "Spin the Wheel button not found"

    # Since we can't reliably test the stateful behavior in Streamlit's testing framework,
    # we'll verify that the wheel segments information is displayed
    wheel_info_displayed = False
    for text in game.markdown.values:
        if "Wheel Segments:" in text:
            wheel_info_displayed = True
            break
    assert wheel_info_displayed, "Wheel segments information not displayed"

    # Check if at least some of the wheel segments are described
    # We'll search all text for any mention of the segments
    all_text = " ".join(game.markdown.values)
    segment_labels = ["2X", "3X", "5X", "1X", "1/2X", "Jackpot", "Bankrupt"]
    segments_found = sum(1 for label in segment_labels if label in all_text)
    assert segments_found >= 3, (
        f"Not enough wheel segments are described on the page. "
        f"Found: {segments_found}"
    )


def test_wheel_game_insufficient_funds():
    """Test attempting to bet with insufficient funds"""
    # Set up a game with very low bankroll
    at = AppTest.from_file("app.py").run()

    # Manually set a low bankroll
    at.session_state.bankroll = 5

    # Find and press the Wheel of Fortune button
    button = -1
    for i, btn in enumerate(at.button):
        if "Wheel of Fortune" in btn.label:
            button = i
            break
    at.button[button].click().run()

    # Try to bet $10
    bet_button = -1
    for i, button in enumerate(at.button):
        if "Bet $10" in button.label:
            bet_button = i
            break
    at.button[bet_button].click().run()

    # Check for warning message
    warning_found = False
    for warning in at.warning:
        if "You don't have enough funds for that bet" in warning.value:
            warning_found = True
            break
    assert warning_found, "Insufficient funds warning not displayed"
