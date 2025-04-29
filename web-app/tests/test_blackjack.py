"""This is the module to test the streamlit blackjack functionality"""

import pytest  # pylint: disable=unused-import
import streamlit as st  # pylint: disable=unused-import
from streamlit.testing.v1 import AppTest


def setup_game():
    """Helper function to setup a game - use repeatedly when desiring specific conditions"""

    # navigate home
    at = AppTest.from_file("app.py").run()

    # find and press blackjack button
    button = -1
    for i in range(0, len(at.button)):  # pylint: disable=consider-using-enumerate
        if "Blackjack" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    # find the number input and increment the bet
    assert len(at.number_input) > 0, "Number input does not exist on the page"
    for i in range(0, 5):
        at.number_input[0].increment()

    # find and press 'Let's Go!' button
    button = -1
    for i in range(0, len(at.button)):  # pylint: disable=consider-using-enumerate
        if "Let's Go!" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    return at


def test_blackjack_dealt_bust():
    """test when blackjack hand is dealt as bust"""

    # get game that is already bust
    game = None
    brk = False
    while brk is False:
        game = setup_game()
        for md in game.markdown.values:
            if "Player total: 22" in md:
                brk = True

    assert "Bust :( 💥" in game.markdown.values

    # ensure game shows losing screen
    head = -1
    for i in range(0, len(game.header)):  # pylint: disable=consider-using-enumerate
        if game.header[i].value == "You lose!!":
            head = i
    assert head != -1, "You lose!! not in the text as a header"

    # ensure hit and stand buttons are disabled
    for button in game.button:
        if button.value in ("Hit", "Stand"):
            assert button.disabled is True


def test_blackjack_dealt_blackjack_win():
    """test for when player is instantly dealt blackjack"""

    # get game that is already blackjack
    game = None
    brk = False
    while brk is False:
        game = setup_game()
        for md in game.markdown.values:
            if "Dealer total: 21" in md:
                brk = False
                break
            if "Player total: 21" in md:
                brk = True

    print(game.markdown.values)
    assert "Blackjack!!! 🎉" in game.markdown.values

    # ensure game shows winning screen
    head = -1
    for i in range(0, len(game.header)):  # pylint: disable=consider-using-enumerate
        if game.header[i].value == "You win!!":
            head = i
    assert head != -1, "You win!! not in the text as a header"

    # ensure hit and stand buttons are disabled
    for button in game.button:
        if button.value in ("Hit", "Stand"):
            assert button.disabled is True


def test_blackjack_hit():
    """Test that a player can hit"""

    # get game that is able to hit
    game = None
    brk = False
    while brk is False:
        game = setup_game()
        for md in game.markdown.values:
            if "Player total: 15" in md:
                brk = True

    assert "Dealer total: ???" in game.markdown.values

    # ensure hit and stand buttons are NOT disabled
    for button in game.button:
        if button.value in ("Hit", "Stand"):
            assert button.disabled is False

    # find and click hit button
    button = -1
    for i in range(0, len(game.button)):  # pylint: disable=consider-using-enumerate
        if "Hit" in game.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    game.button[button].click().run()


def test_blackjack_tie():
    """test what happens when player and dealer tie"""

    # get game that is able to hit
    game = None
    brk = False
    while brk is False:
        game = setup_game()
        for md in game.markdown.values:
            # find the 'player total' text element
            if "Player total:" not in md:
                continue

            # ensure the player total x is 16 < x < 21
            num = md.split(": ")[1]
            if num[0:1] == "[":
                break
            if int(num) > 21 or int(num) < 16:
                break

            # find and click stand button
            button = -1
            for i in range(
                0, len(game.button)
            ):  # pylint: disable=consider-using-enumerate
                if "Stand" in game.button[i].label:
                    button = i
            assert button != -1, "button does not exist"
            game.button[button].click().run()

            # check dealer total
            for md in game.markdown.values:
                if "Dealer total:" not in md:
                    continue

                # ensure dealer total == player total
                if md == "Dealer total: " + num:
                    brk = True
                    break

    # check if game is tied
    head = -1
    for i in range(0, len(game.header)):  # pylint: disable=consider-using-enumerate
        if game.header[i].value == "It's a tie...":
            head = i
    assert head != -1, "It's a tie... not in the text as a header"
