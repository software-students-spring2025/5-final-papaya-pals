"""These are the unit tests for Slots"""

import pytest
from unittest import mock
from types import SimpleNamespace
from app_pages.games.slots_game.slots import play_slots, spin, payout

# Test Functions


def test_slots_icons_display():
    """Tests icon display"""
    all_icons = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
    result = spin(all_icons)

    assert len(result) == 3
    for icon in result:
        assert icon in all_icons


def test_jackpot_payout():
    """Tests Jackpot"""
    jackpot = ["7️⃣", "7️⃣", "7️⃣"]
    _, winnings = payout(jackpot, 100)
    assert winnings == 10000


def test_lose_payout():
    """Tests when you lose"""
    lose = ["🍒", "🍋", "🔔"]
    _, loss = payout(lose, 100)
    assert loss == -100


def test_three_of_a_kind_payout():
    """Tests three of a kind"""
    three = ["🍋", "🍋", "🍋"]
    _, winnings = payout(three, 50)
    assert winnings == 250


# Mocked play_slots tests bc of the way the game is structured, couldn't do same module as blackjack
# Streamlit specific issue, their website said this is okay to do

## These tests cover play_slots() functionalities


@mock.patch("app_pages.games.slots_game.slots.st")
def test_play_slots_displays_bankroll_and_bet(mock_st):
    """Test that bankroll and bet are displayed"""
    mock_st.session_state = SimpleNamespace(
        shame_counter=0, bankroll=100, slots_bet_amount=5
    )
    mock_col1 = mock.MagicMock()
    mock_col2 = mock.MagicMock()
    mock_cols_bet = [mock.MagicMock() for _ in range(6)]

    mock_st.columns.side_effect = [(mock_col1, mock_col2), tuple(mock_cols_bet)]

    for col in mock_cols_bet:
        col.button.return_value = False
    mock_col1.button.return_value = False
    mock_col2.button.return_value = False
    # No Spin
    mock_st.button.return_value = False

    play_slots()

    mock_st.write.assert_any_call("Bankroll: $100")
    mock_st.write.assert_any_call("Current Bet: $5")


@mock.patch("app_pages.games.slots_game.slots.st")
def test_play_slots_bet_more_than_bankroll(mock_st):
    """Test trying to bet too much"""
    mock_st.session_state = SimpleNamespace(
        shame_counter=0, bankroll=10, slots_bet_amount=5
    )
    mock_col1 = mock.MagicMock()
    mock_col2 = mock.MagicMock()
    mock_cols_bet = [mock.MagicMock() for _ in range(6)]

    mock_st.columns.side_effect = [(mock_col1, mock_col2), tuple(mock_cols_bet)]

    # simulate pressing $50 bet button
    for i, col in enumerate(mock_cols_bet):
        # $50 is index 3
        col.button.return_value = i == 3

    # No spin
    mock_st.button.return_value = False

    play_slots()

    mock_st.warning.assert_called_with("You don't have enough funds for that bet.")


@mock.patch("app_pages.games.slots_game.slots.st")
def test_play_slots_spin_win(mock_st):
    """Test spinning and winning"""
    mock_st.session_state = SimpleNamespace(
        shame_counter=0, bankroll=50, slots_bet_amount=5
    )
    mock_col1 = mock.MagicMock()
    mock_col2 = mock.MagicMock()
    mock_cols_bet = [mock.MagicMock() for _ in range(6)]

    # Mock columns return
    mock_st.columns.side_effect = [(mock_col1, mock_col2), tuple(mock_cols_bet)]

    # None of the bet buttons are pressed
    for col in mock_cols_bet:
        col.button.return_value = False

    # No header buttons pressed either
    mock_col1.button.return_value = False
    mock_col2.button.return_value = False

    # "Spin!" button pressed
    mock_st.button.side_effect = lambda label=None: label == "Spin! 💰"

    with mock.patch(
        "app_pages.games.slots_game.slots.spin", return_value=["🍒", "🍒", "🍒"]
    ), mock.patch(
        "app_pages.games.slots_game.slots.payout", return_value=("Three of a Kind!", 25)
    ):
        play_slots()

    # Now bankroll should have updated
    # 50-5+25
    assert mock_st.session_state.bankroll == 70


@mock.patch("app_pages.games.slots_game.slots.st")
def test_play_slots_spin_too_broke(mock_st):
    """Test spinning without enough bankroll"""
    mock_st.session_state = SimpleNamespace(
        shame_counter=0, bankroll=2, slots_bet_amount=5
    )
    mock_col1 = mock.MagicMock()
    mock_col2 = mock.MagicMock()
    mock_cols_bet = [mock.MagicMock() for _ in range(6)]

    mock_st.columns.side_effect = [(mock_col1, mock_col2), tuple(mock_cols_bet)]

    for col in mock_cols_bet:
        col.button.return_value = False

    mock_col1.button.return_value = False
    mock_col2.button.return_value = False

    mock_st.button.side_effect = lambda label=None: label == "Spin! 💰"

    mock_st.warning = mock.MagicMock()

    play_slots()

    mock_st.warning.assert_any_call("You don't have enough funds to place this bet.")
