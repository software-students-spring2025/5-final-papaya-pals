"""This is the module to test the streamlit app functionality"""
# pylint: disable=duplicate-code,import-error

import pytest  # pylint: disable=unused-import
import streamlit as st  # pylint: disable=unused-import
from streamlit.testing.v1 import AppTest


# helper function to press buttons
def press_button(at, button_value):
    """This function finds a button by value and clicks it"""
    # find and press xxxx button
    button = -1
    for i in range(0, len(at.button)):  # pylint: disable=consider-using-enumerate
        if button_value in at.button[i].label:
            button = i
    assert button != -1, "button does not exist"
    at.button[button].click().run()

    return at


# Test functions
def test_sanity_check():
    """Basic test to ensure pytest runs properly"""
    expected = True
    actual = True
    assert actual == expected, "Expected True to be equal to True!"


def test_default_state():
    """test initial session variables"""

    # navigate home
    at = AppTest.from_file("app.py").run()

    # check default state
    assert at.session_state.current_page == "home"
    assert at.session_state.user == ""


def test_page_navigation():
    """test flow between pages"""

    # navigate home
    at = AppTest.from_file("app.py").run()

    # find and press blackjack button
    at = press_button(at, "Blackjack")
    assert at.session_state.blackjack == "new"
    assert at.session_state.blackjack_hits == 0
    assert at.session_state.blackjack_stood is False
    assert at.session_state.current_page == "blackjack"

    # find and press home button
    at = press_button(at, "Home")
    assert at.session_state.current_page == "home"

    # find and press login button
    at = press_button(at, "Login")
    assert at.session_state.current_page == "login"

    # find and press register button
    at = press_button(at, "Register")
    assert at.session_state.current_page == "register"

    # find and press home button
    at = press_button(at, "Home")
    assert at.session_state.current_page == "home"

    # find and press slots button
    at = press_button(at, "Slots")
    assert at.session_state.current_page == "slots"

    # find and press home button
    at = press_button(at, "Home")
    assert at.session_state.current_page == "home"

    # find and press roulette button
    at = press_button(at, "Roulette")
    assert at.session_state.current_page == "roulette"


def test_fake_login():
    """test that the interface changes when player is logged in"""

    # navigate home
    at = AppTest.from_file("app.py").run()

    # set session user
    at.session_state.user = "random"
    at.run()

    # ensure login/register are not present in buttons; logout is present
    button = -1
    for i in range(0, len(at.button)):  # pylint: disable=consider-using-enumerate
        if "Logout" in at.button[i].label:
            button = i
        assert "Login" not in at.button[i].label
        assert "Register" not in at.button[i].label
    assert button != -1, "button does not exist"
    # press logout button
    at.button[i].click().run()

    assert at.session_state.current_page == "home"
    assert at.session_state.user == ""


def test_unknown_page_request():
    """test when user requests a page that does not exist"""

    # navigate home
    at = AppTest.from_file("app.py").run()

    # set session page to unknown
    at.session_state.current_page = "random"
    at.run()

    assert (
        at.exception[0].message
        == "Unknown page request from st.session_state.current_page"
    )
