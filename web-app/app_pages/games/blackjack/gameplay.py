"""This module contains helper functions to assist in blackjack gameplay."""

import streamlit as st
from .deck import Deck, Hand
from .cardlist import standard_cardlist


# Initialize player, dealer, deck and game play. Cache these variables
@st.cache_data()
def start_game_cached():
    """
    This function generates a new deck and deals a new hand.
    Because it is cached, it can maintain the state of a deck and of hands when called twice.
    """

    game_deck = Deck(standard_cardlist)
    game_deck.shuffle()
    dealer = Hand()
    player = Hand()
    player.deal(game_deck.deal(), False)
    dealer.deal(game_deck.deal(), False)
    player.deal(game_deck.deal(), False)
    dealer.deal(game_deck.deal(), True)
    return game_deck, dealer, player


def place_bet():
    """Run this to start a new game - allow player to place a bet."""

    def callback(bet_amt):
        """callback function to set the game state before the page is reloaded"""

        st.session_state.blackjack = "ongoing"
        st.session_state.blackjack_bet_amount = bet_amt

    st.subheader("First, place your bet:")
    bet = st.number_input(
        "How much are you putting on the table??",
        min_value=1,
        max_value=st.session_state.bankroll,
    )

    st.button("Let's Go!", on_click=callback, args=[bet])


def dealer_finish(game_deck, dealer):
    """
    This function allows the dealer to deal self cards if desired.
    Dealer is programmed to hit below 17 (must stand on 17).
    """
    # while the first total is still less than 17, and while the second total is between 17 and 21
    while dealer.total1 < 17 and (dealer.total2 < 17 or dealer.total2 > 21):
        dealer.deal(game_deck.deal(), False)
    dealer.reveal()


def finish(result):
    """This function wraps up the game - determine winner, display results, update bankroll"""

    payout = 0
    if result == "win":
        st.header("You win!!")
        payout = int(st.session_state.blackjack_bet_amount)
    elif result == "lose":
        st.header("You lose!!")
        payout = int(st.session_state.blackjack_bet_amount) * -1
    elif result == "tie":
        st.header("It's a tie...")
    else:
        raise ValueError("function not called with 'win' 'lose' or 'tie'")

    st.session_state.bankroll += payout
    st.session_state.blackjack = "new"
    st.session_state.blackjack_hits = 0
    st.session_state.blackjack_stood = False
    st.session_state.blackjack_bet_amount = 0
    start_game_cached.clear()
    st.button("New Game?")


def continue_game(game_deck, dealer, player):
    """
    This function assesses the state of the game and determines what options the player has, if any.
    This function contains the only calls to "finish" which terminates the game.
    """

    # bust
    if player.total1 > 21:
        # show (disabled) hit and stand buttons
        col1, col2, _extra = st.columns([0.1, 0.2, 0.7])
        with col1:
            _hit = st.button("Hit", disabled=True)
        with col2:
            stand = st.button("Stand", disabled=True)

        st.write("Bust :( 💥")
        finish("lose")

    # blackjack
    elif player.total1 == 21 or player.total2 == 21:
        # show (disabled) hit and stand buttons
        col1, col2, _extra = st.columns([0.1, 0.2, 0.7])
        with col1:
            _hit = st.button("Hit", disabled=True)
        with col2:
            stand = st.button("Stand", disabled=True)

        st.write("Blackjack!!! 🎉")

        # allow dealer to finish
        dealer_finish(game_deck, dealer)

        # determine winner
        if dealer.total1 == 21 or dealer.total2 == 21:
            finish("tie")
            return
        finish("win")

    # option to hit or stand
    else:
        # callback functions to change state of app when buttons clicked
        def hit_cb():
            st.session_state.blackjack_hits += 1

        def stand_cb():
            st.session_state.blackjack_stood = True

        # display hit and stand buttons
        col1, col2, _extra = st.columns([0.1, 0.2, 0.7])
        _hit = None
        stand = None
        if st.session_state.blackjack_stood is False:
            with col1:
                _hit = st.button("Hit", on_click=hit_cb)
            with col2:
                stand = st.button("Stand", on_click=stand_cb)
        else:
            with col1:
                _hit = st.button("Hit", on_click=hit_cb, disabled=True)
            with col2:
                stand = st.button("Stand", on_click=stand_cb, disabled=True)

        # if stand was pressed last:
        if stand:
            # allow dealer to finish
            dealer_finish(game_deck, dealer)

            # determine winner
            player_result = player.total1
            if player.total2 > player.total1 and player.total2 <= 21:
                player_result = player.total2
            dealer_result = dealer.total1
            if dealer.total2 > dealer.total1 and dealer.total2 <= 21:
                dealer_result = dealer.total2

            if dealer_result > 21 or dealer_result < player_result:
                finish("win")
            elif dealer_result > player_result:
                finish("lose")
            else:
                finish("tie")
