import streamlit as st
from games.slots_game.slots import play_slots
from games.roulette_game.roulette import play_roulette
from games.blackjack.main import play_blackjack
from games.home import show_home
from games.login import show_login
from games.initialize import set_default_session_vars, reset_to_default

# set session vars
set_default_session_vars()

# set page to "home"
def load_homepage_cb():
    reset_to_default(st.session_state.current_page)
    st.session_state.current_page = "home"

# set page to "login"
def load_login_cb():
    reset_to_default(st.session_state.current_page)
    st.session_state.current_page = "login"

# log out 
def load_logout_cb():
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
else:
    raise Exception("Unknown page request from st.session_state.current_page")
