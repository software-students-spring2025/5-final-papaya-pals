"""This file contains the main code for the blackjack game"""

import streamlit as st
from .gameplay import start_game_cached, place_bet, continue_game
import db

def play_blackjack():
    """This is the main function that controls blackjack playthrough"""

    # show basic frontend elements
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown(f"**Shame Counter:** {st.session_state.shame_counter}")
        st.markdown(f"**Bankroll:** {st.session_state.bankroll}")
        st.markdown(f"**Current bet:** {st.session_state.blackjack_bet_amount}")
    with col1:
        st.title("Welcome to Blackjack! ♤ ♡ ♧ ♢")

    # get betting amount first
    if st.session_state.blackjack == "new":
        place_bet()

    # begin or continue actual gameplay
    if st.session_state.blackjack == "ongoing":
        # deal, or get cached elements for game continuation
        game_deck, dealer, player = start_game_cached()
        for _i in range(0, st.session_state.blackjack_hits):
            player.deal(game_deck.deal(), False)

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
        dealer_images.image(
            ["./static/images/" + img + ".png" for img in dealer.images], width=80
        )
        if dealer.hidden is True:
            dealer_total.write("Dealer total: ???")
        else:
            # if either total contains blackjack
            if dealer.total2 == 21 or dealer.total1 == 21:
                dealer_total.write("Dealer total: 21")
            # if the totals are the same (no aces)
            elif dealer.total1 == dealer.total2:
                dealer_total.write(f"Dealer total: {str(dealer.total1)}")
            # if the totals are not the same ...
            # if total2 is not bust, show it.
            elif dealer.total2 < 21:
                dealer_total.write(f"Dealer total: {str(dealer.total2)}")
            # else, show total1 (may be bust, but guaranteed smaller than total1)
            else:
                dealer_total.write(f"Dealer total: {str(dealer.total1)}")

        player_images.image(
            ["./static/images/" + img + ".png" for img in player.images], width=80
        )
        # if either total contains blackjack
        if player.total2 == 21 or player.total1 == 21:
            player_total.write("Player total: 21")
        # if the totals are the same (no aces)
        elif player.total1 == player.total2:
            player_total.write(f"Player total: {str(player.total1)}")
        # if the totals are not the same ...
        # if total2 is not bust, show BOTH TOTALS
        elif player.total2 < 21:
            player_total.write(f"Player total: [{player.total1}, {player.total2}]")
        # else, show only total1 (may be bust, but guaranteed smaller than total1)
        else:
            player_total.write(f"Player total: {str(player.total1)}")
