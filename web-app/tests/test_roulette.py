"""These are the unit tests for Roulette"""

import pytest
from app_pages.games.roulette_game.roulette import get_color, evaluate_roulette_result


def test_get_color_green():
    """Tests that get_color returns 'Green' for a green number"""
    assert get_color(0) == "Green"


def test_get_color_red():
    """Tests that get_color returns 'Red' for a red number"""
    assert get_color(1) == "Red"


def test_get_color_black():
    """Tests that get_color returns 'Black' for a black number"""
    assert get_color(2) == "Black"


def test_evaluate_roulette_number_hit():
    """Tests hitting the correct number payout"""
    result = 7
    bet = 10
    number_pick = 7
    color_bet = "None"
    parity_bet = "None"

    winnings, messages = evaluate_roulette_result(
        result, bet, number_pick, color_bet, parity_bet
    )

    assert winnings == 350


def test_evaluate_roulette_color_match():
    """Tests matching color bet"""
    result = 3
    bet = 10
    number_pick = 5
    color_bet = "Red"
    parity_bet = "None"

    winnings, messages = evaluate_roulette_result(
        result, bet, number_pick, color_bet, parity_bet
    )

    assert winnings == 10
    assert any("Color match!" in msg for level, msg in messages)


def test_evaluate_roulette_parity_match():
    """Tests even/odd"""
    result = 8
    bet = 10
    number_pick = 5
    color_bet = "None"
    parity_bet = "Even"

    winnings, messages = evaluate_roulette_result(
        result, bet, number_pick, color_bet, parity_bet
    )

    assert winnings == 10
    assert any("Parity match!" in msg for level, msg in messages)


def test_evaluate_roulette_no_wins():
    result = 9
    bet = 10
    number_pick = 20
    color_bet = "Black"
    parity_bet = "Even"

    winnings, messages = evaluate_roulette_result(
        result, bet, number_pick, color_bet, parity_bet
    )

    assert winnings == 0
    assert any("No wins" not in msg for level, msg in messages)
