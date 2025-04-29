"""These are the unit tests for Roulette"""

from unittest import mock
from types import SimpleNamespace
from app_pages.games.roulette_game.roulette import (
    get_color,
    evaluate_roulette_result,
    choose_bet,
    play_roulette,
)


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

    winnings, _ = evaluate_roulette_result(
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
    """Tests when no bets are won"""
    result = 9
    bet = 10
    number_pick = 20
    color_bet = "Black"
    parity_bet = "Even"

    winnings, messages = evaluate_roulette_result(
        result, bet, number_pick, color_bet, parity_bet
    )

    assert winnings == 0
    # Checks that none of the messages are "success"
    for level, _ in messages:
        assert level != "success"


@mock.patch("app_pages.games.roulette_game.roulette.st")
def test_choose_bet_success(mock_st):
    """Test successful bet choice"""
    mock_st.session_state = SimpleNamespace(bankroll=100, roulette_bet_amount=0)
    mock_cols = [mock.MagicMock() for _ in range(6)]

    mock_st.columns.return_value = tuple(mock_cols)
    for i, col in enumerate(mock_cols):
        col.button.return_value = i == 2

    choose_bet([1, 5, 10, 50, 100, 1000])

    assert mock_st.session_state.roulette_bet_amount == 10
    assert mock_st.session_state.bankroll == 90


# Most important to test play_roulette()
# Had to mock this as well to get broader coverage, paths to all funcs that P_R uses


@mock.patch("app_pages.games.roulette_game.roulette.st")
@mock.patch("app_pages.games.roulette_game.roulette.get_color")
@mock.patch("app_pages.games.roulette_game.roulette.evaluate_roulette_result")
@mock.patch("app_pages.games.roulette_game.roulette.random")
def test_play_roulette_spin_win(mock_random, mock_eval, mock_color, mock_st):
    """Light integration test of play_roulette spin flow"""

    # Setup session state
    mock_st.session_state = SimpleNamespace(
        shame_counter=0, bankroll=100, roulette_bet_amount=10
    )

    # Mock layout
    mock_col1 = mock.MagicMock()
    mock_col2 = mock.MagicMock()
    mock_cols_bet = [mock.MagicMock() for _ in range(6)]

    mock_st.columns.side_effect = [(mock_col1, mock_col2), tuple(mock_cols_bet)]
    for col in mock_cols_bet:
        col.button.return_value = False

    # Mock UI inputs
    mock_st.number_input.return_value = 7
    # color, then parity
    mock_st.radio.side_effect = ["Red", "Even"]
    mock_st.button.side_effect = lambda label=None: label == "Spin the Wheel 🎯"

    # Force random result
    mock_random.randint.return_value = 7
    mock_color.return_value = "Red"
    mock_eval.return_value = (10, [("success", "Color match!")])

    # Call play_roulette yayyyy
    play_roulette()

    assert mock_st.session_state.bankroll == 100
