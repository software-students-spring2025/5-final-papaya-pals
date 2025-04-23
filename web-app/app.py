import streamlit as st
from games.slots_game.slots import play_slots
from games.blackjack.main import play_blackjack
from games.home import show_home

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "user" not in st.session_state:
    st.session_state.user = ""

# set page to "home"
def load_homepage_cb():
    st.session_state.current_page = "home"

# set page to "login"
def load_login_cb():
    st.session_state.current_page = "login"

# log out 
def load_logout_cb():
    st.session_state.user = ""

st.sidebar.title("Casino Menu 🎲")
st.button("Home", onclick=load_homepage_cb)
if st.session_state.user == "":
    st.button("Login", onclick=load_login_cb)
else:
    st.button("Logout", onclick=load_logout_cb)


if st.session_state.current_page == "slots":
    play_slots()
elif st.session_state.current_page == "blackjack":
    play_blackjack()
elif st.session_state.current_page == "home":
    show_home()
