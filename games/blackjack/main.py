"""This file contains the main code for the blackjack game"""

import streamlit as st
from .deck import Card, Deck, Hand
from .gameplay import start_game_cached, place_bet, continue_game


def play_blackjack():

    # session variables
    if "blackjack" not in st.session_state:
        st.session_state.blackjack = "new"
        start_game_cached.clear()
    if "bankroll" not in st.session_state:
        st.session_state.bankroll = 1000
    if "shame_counter" not in st.session_state:
        st.session_state.shame_counter = 0
    if "bet_amount" not in st.session_state:
        st.session_state.bet_amount = 0

    # show basic frontend elements
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown(f"**Shame Counter:** {st.session_state.shame_counter}")
        st.markdown(f"**Bankroll:** {st.session_state.bankroll}")
        st.markdown(f"**Current bet:** {st.session_state.bet_amount}")
    with col1:
        st.title("Welcome to Blackjack! ♤ ♡ ♧ ♢")

    # get betting amount first
    if st.session_state.blackjack == "new":
        place_bet()
            
    # begin or continue actual gameplay
    if st.session_state.blackjack == "ongoing":
        # deal, or get cached elements for game continuation
        game_deck, dealer, player = start_game_cached()

        # empty elements
        st.write("Dealer:")
        dealer_images = st.empty()
        dealer_total = st.empty()
        st.divider()
        st.write("Player:")
        player_images = st.empty()
        player_total = st.empty()

        # allow player to hit or stand if available - continue game if not
        continue_game(game_deck, dealer, player)
        
        # fill in page elements
        dealer_images.image(["./static/images/" + img + ".png" for img in dealer.images], width=80)
        if dealer.hidden == True:
            dealer_total.write("Dealer total: ???")
        else:
            if dealer.total2 == 21 or dealer.total1 == 21:
                dealer_total.write(f"Dealer total: 21")
            elif dealer.total2 > dealer.total1 and dealer.total2 < 21:
                dealer_total.write(f"Dealer total: {str(dealer.total2)}")
            else:
                dealer_total.write(f"Dealer total: {str(dealer.total1)}")

        player_images.image(["./static/images/" + img + ".png" for img in player.images], width=80)
        if player.total2 == 21 or player.total1 == 21:
            player_total.write(f"Player total: 21")
        elif player.total2 > player.total1 and player.total2 < 21:
            player_total.write(f"Player total: {str(player.total2)}")
        else:
            player_total.write(f"Player total: {str(player.total1)}")


