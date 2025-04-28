"""These are the unit tests for Slots"""

import pytest
from app_pages.games.slots_game.slots import play_slots, spin, payout

# Test Functions:

def test_slots_icons_display():
    all_icons = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
    result = spin(all_icons)

    assert len(result) == 3
    for i in result:
        assert i in all_icons

def test_jackpot_payout():
    jackpot = ["7️⃣", "7️⃣", "7️⃣"]
    _, winnings = payout(jackpot, 100)
    assert winnings == 10000

def test_lose_payout():
    lose = ["🍒", "🍋", "🔔"]
    _, loss = payout(lose, 100)
    assert loss == -100

def test_three_of_a_kind_payout():
    three = ["🍋", "🍋", "🍋"]
    _, winnings = payout(three, 50)
    assert winnings == 250
