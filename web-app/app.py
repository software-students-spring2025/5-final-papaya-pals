"""This application provides the basis of the web app structure."""

import streamlit as st
from app_pages.games.slots_game.slots import play_slots
from app_pages.games.roulette_game.roulette import play_roulette
from app_pages.games.blackjack.main import play_blackjack
from app_pages.home import show_home
from app_pages.login import show_login
from app_pages.initialize import set_default_session_vars, reset_to_default
from app_pages.reload import show_reload
import db

# set session vars
set_default_session_vars()


# set page to "home"
def load_homepage_cb():
    """This callback function will get called when user presses the home button"""

    ### DB TESTING
    db.get_user(None, None)
    ###
    reset_to_default(st.session_state.current_page)
    st.session_state.current_page = "home"


# set page to "login"
def load_login_cb():
    """This callback function will get called when user presses the login button"""
    reset_to_default(st.session_state.current_page)
    st.session_state.current_page = "login"


# log out
def load_logout_cb():
    """This callback function will get called when user presses the logout button"""
    reset_to_default(st.session_state.current_page)
    st.session_state.user = ""
    st.session_state.current_page = "home"


# show sidebar
with st.sidebar:
    st.title("Casino Menu 🎲")
    st.button("Home", on_click=load_homepage_cb)
    if st.session_state.user == "":
        st.button("Login", on_click=load_login_cb)
    else:
        st.button("Logout", on_click=load_logout_cb)

# if bankroll is zero, redirect to reload page no matter what
if st.session_state.bankroll == 0:
    st.session_state.current_page = "reload"

# load correct page
if st.session_state.current_page == "slots":
    play_slots()
elif st.session_state.current_page == "blackjack":
    play_blackjack()
elif st.session_state.current_page == "home":
    show_home()
elif st.session_state.current_page == "roulette":
    play_roulette()
elif st.session_state.current_page == "unknown_game1":
    st.write("on game page")
elif st.session_state.current_page == "unknown_game2":
    st.write("on game page")
elif st.session_state.current_page == "login":
    show_login()
elif st.session_state.current_page == "reload":
    show_reload()
else:
    raise ValueError("Unknown page request from st.session_state.current_page")
