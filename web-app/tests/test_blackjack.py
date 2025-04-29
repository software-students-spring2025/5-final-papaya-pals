"""This is the module to test the streamlit blackjack functionality"""

import pytest  # pylint: disable=unused-import
import streamlit as st  # pylint: disable=unused-import
from streamlit.testing.v1 import AppTest


def test_blackjack_basic():
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

        return at
    
    
    # get game that is already bust
    game = setup_game()
    print(game.text)
    print(game.button)
    assert False
    while "Player total: 22" not in game.text:
        game = setup_game()

    
    
    assert "Bust :(" in game.text
    head = -1
    for i in range(0, len(game.header)):
        if game.header[i].value == "You lose!!":
            head = i
    assert head != -1, "You lose!! not in the text as a header"
    




