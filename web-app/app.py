import streamlit as st
from games.slots_game.slots import play_slots
from games.blackjack.main import play_blackjack
from games.roulette_game.roulette import play_roulette

st.sidebar.title("Casino Menu 🎲")
game_choice = st.sidebar.radio("Choose a game:", ["Blackjack","Roulette","Slots"])  
# Add the rest later (just testing slots and roulette for now)

if game_choice == "Slots":
    play_slots()
elif game_choice == "Blackjack":
    play_blackjack()
elif game_choice == "Roulette":
    play_roulette()
