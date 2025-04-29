"""This is the module to test the streamlit app functionality"""

import pytest  # pylint: disable=unused-import
import streamlit as st  # pylint: disable=unused-import
from streamlit.testing.v1 import AppTest


# Test functions
def test_sanity_check():
    """Basic test to ensure pytest runs properly"""
    expected = True
    actual = True
    assert actual == expected, "Expected True to be equal to True!"


def test_default_state():
    # navigate home
    at = AppTest.from_file("app.py").run()

    # check default state
    assert at.session_state.current_page == "home"
    assert at.session_state.user == ""



def test_page_navigation():
    # navigate home
    at = AppTest.from_file("app.py").run()

    # find and press blackjack button
    button = -1
    for i in range(0, len(at.button)):
        if "Blackjack" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    assert at.session_state.blackjack == "new"
    assert at.session_state.blackjack_hits == 0
    assert at.session_state.blackjack_stood == False
    assert at.session_state.current_page == "blackjack"

    # find and press home button
    button = -1
    for i in range(0, len(at.button)):
        if "Home" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()
    
    assert at.session_state.current_page == "home"

    # find and press login button
    button = -1
    for i in range(0, len(at.button)):
        if "Login" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    assert at.session_state.current_page == "login"

    """ # find and press register button
    button = -1
    for i in range(0, len(at.button)):
        if "Register" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    assert at.session_state.current_page == "register" """

    # find and press home button
    button = -1
    for i in range(0, len(at.button)):
        if "Home" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    assert at.session_state.current_page == "home"

    # find and press slots button
    button = -1
    for i in range(0, len(at.button)):
        if "Slots" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    assert at.session_state.current_page == "slots"

    # find and press home button
    button = -1
    for i in range(0, len(at.button)):
        if "Home" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    assert at.session_state.current_page == "home"

    # find and press roulette button
    button = -1
    for i in range(0, len(at.button)):
        if "Roulette" in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    assert at.session_state.current_page == "roulette"
