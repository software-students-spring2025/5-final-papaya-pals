"""This is the module to test the streamlit blackjack functionality"""

import pytest  # pylint: disable=unused-import
import streamlit as st  # pylint: disable=unused-import
from streamlit.testing.v1 import AppTest


def test_blackjack_dealt_bust():
    """"""

    def setup_game():
        # navigate home
        at = AppTest.from_file("app.py").run()

        # find and press blackjack button
        button = -1
        for i in range(0, len(at.button)):
            if "Blackjack" in at.button[i].label:
                button = i
        assert button != -1, "button does not exist"
        at.button[button].click().run()

        # find the number input and increment the bet
        try:
            for i in range(0, 5):
                at.number_input[0].increment()
        except Exception as e:
            assert False, "error incrementing number input"

        # find and press 'Let's Go!' button
        button = -1
        for i in range(0, len(at.button)):
            if "Let's Go!" in at.button[i].label:
                button = i
        assert button != -1, "button does not exist"
        at.button[button].click().run()
             

        return at
    
    
    # get game that is already bust
    game = None
    brk = False
    while brk == False:
        game = setup_game()
        for md in game.markdown.values:
            if "Player total: 22" in md:
                brk = True

    assert "Bust :( 💥" in game.markdown.values
    
    # ensure game shows losing screen
    head = -1
    for i in range(0, len(game.header)):
        if game.header[i].value == "You lose!!":
            head = i
    assert head != -1, "You lose!! not in the text as a header"
    


def test_blackjack_dealt_blackjack():
    """"""

    def setup_game():
        # navigate home
        at = AppTest.from_file("app.py").run()

        # find and press blackjack button
        button = -1
        for i in range(0, len(at.button)):
            if "Blackjack" in at.button[i].label:
                button = i
        assert button != -1, "button does not exist"
        at.button[button].click().run()

        # find the number input and increment the bet
        try:
            for i in range(0, 5):
                at.number_input[0].increment()
        except Exception as e:
            assert False, "error incrementing number input"

        # find and press 'Let's Go!' button
        button = -1
        for i in range(0, len(at.button)):
            if "Let's Go!" in at.button[i].label:
                button = i
        assert button != -1, "button does not exist"
        at.button[button].click().run()
             

        return at
    
    
    # get game that is already blackjack
    game = None
    brk = False
    while brk == False:
        game = setup_game()
        for md in game.markdown.values:
            if "Player total: 21" in md:
                brk = True

    print(game.markdown.values)
    assert "Blackjack!!! 🎉" in game.markdown.values
    
    # ensure game shows winning OR TYING screen
    head = -1
    for i in range(0, len(game.header)):
        if game.header[i].value == "You win!!":
            head = i
    assert head != -1, "You win!! not in the text as a header"
    




