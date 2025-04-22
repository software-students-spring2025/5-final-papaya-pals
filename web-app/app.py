import streamlit as st
from games.slots_game.slots import play_slots

st.sidebar.title("Casino Menu 🎲")
game_choice = st.sidebar.radio("Choose a game:", ["Blackjack","Roulette","Slots"])  
# Add the rest later (just testing slots for now)

if game_choice == "Slots":
    play_slots()