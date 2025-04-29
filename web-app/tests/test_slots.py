"""These are the unit tests for Slots"""

import pytest
from app_pages.games.slots_game.slots import play_slots, spin, payout
from streamlit.testing.v1 import AppTest

# Test Functions:

def test_slots_icons_display():
    """Tests icon display"""
    all_icons = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
    result = spin(all_icons)

    assert len(result) == 3
    for icons in result:
        assert icons in all_icons


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

