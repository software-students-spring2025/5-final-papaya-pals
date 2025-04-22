import streamlit as st
from .deck import Deck, Card, Hand


# Initialize player, dealer, deck and game play. Cache these variables
@st.cache_data()
def start_game_cached():
    print('restarting game')
    my_card_list = [
        "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH", 
        "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS", 
        "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC", 
        "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD"
        ]

    game_deck = Deck(my_card_list)
    game_deck.shuffle()
    dealer = Hand()
    player = Hand()
    player.deal(game_deck.deal(), False)
    dealer.deal(game_deck.deal(), False)
    player.deal(game_deck.deal(), False)
    dealer.deal(game_deck.deal(), True)
    return game_deck, dealer, player


def place_bet():
    """Run this start a new game"""

    def callback(bet_amt):
        """callback function to set the game state before the page is reloaded"""
        st.session_state.blackjack = "ongoing"
        st.session_state.bet_amount = bet_amt

    st.subheader("First, place your bet:")
    bet = st.number_input("How much are you putting on the table??", min_value=1, max_value=st.session_state.bankroll)
    
    st.button("Let's Go!", on_click=callback, args=[bet])
    
            
# function to let dealer deal self cards if needed
def dealer_finish(game_deck, dealer, player):
    while dealer.total1 < 17 and (dealer.total2 == 0 or dealer.total2 < 17):
        dealer.deal(game_deck.deal(), False)
    dealer.reveal()

# function to wrap up the game - display results, update bankroll
def finish(result, game_deck, dealer, player):
    result_elements = st.container()
    payout = 0
    if result == "win":
        result_elements.header("You win!!")
        payout = int(st.session_state.bet_amount)
    elif result == "lose":
        result_elements.header("You lose!!")
        payout = int(st.session_state.bet_amount) * -1
    elif result == "tie":
        result_elements.header("It's a tie...")
    else:
        raise ValueError("function not called with 'win' 'lose' or 'tie'")
    
    st.session_state.bankroll += payout
    st.session_state.blackjack = "new"
    st.session_state.hits = 0
    start_game_cached.clear()
    result_elements.button("New Game?")


# function to continue gameplay - show hit/stand options if available
def continue_game(game_deck, dealer, player):
# show buttons for hit or stand - player options

    # bust
    if player.total1 > 21:
        # show (disabled) hit and stand buttons
        col1, col2, extra = st.columns([0.1, 0.2, 0.7])
        with col1:
            hit = st.button("Hit", disabled=True)
        with col2:
            stand = st.button("Stand", disabled=True)
        
        # player loses
        st.write("Bust :( 💥")
        finish("lose", game_deck, dealer, player)
    
    # blackjack
    elif player.total1 == 21 or player.total2 == 21: 
        
        # show (disabled) hit and stand buttons
        col1, col2, extra = st.columns([0.1, 0.2, 0.7])
        with col1:
            hit = st.button("Hit", disabled=True)
        with col2:
            stand = st.button("Stand", disabled=True)
        
        st.write("Blackjack!!! 🎉")

        # allow dealer to finish
        dealer_finish(game_deck, dealer, player)

        # determine winner
        if dealer.total1 == 21 or dealer.total2 == 21:
            finish("tie", game_deck, dealer, player)
        else:
            finish("win", game_deck, dealer, player)
    
    # option to hit or stand
    else: 
        
        # callback functions to change state of app when buttons clicked
        def hit_cb():
            st.session_state.hits += 1
        def stand_cb():
            st.session_state.stood = True

        # display hit and stand buttons
        col1, col2, extra = st.columns([0.1, 0.2, 0.7])
        hit = None
        stand = None
        if st.session_state.stood == False:
            with col1:
                hit = st.button("Hit", on_click=hit_cb)
            with col2:
                stand = st.button("Stand", on_click=stand_cb)
        else:
            with col1:
                hit = st.button("Hit", on_click=hit_cb, disabled=True)
            with col2:
                stand = st.button("Stand", on_click=stand_cb, disabled=True)

        # if stand was pressed last: 
        if stand:
            # allow dealer to finish
            dealer_finish(game_deck, dealer, player)

            # determine winner
            player_result = player.total1
            if player.total2 > player.total1 and player.total2 <= 21:
                player_result = player.total2
            dealer_result = dealer.total1
            if dealer.total2 > dealer.total1 and dealer.total2 <= 21:
                dealer_result = dealer.total2
            
            if dealer_result > 21 or dealer_result < player_result:
                finish("win", game_deck, dealer, player)
            elif dealer_result > player_result:
                finish("lose", game_deck, dealer, player)
            else:
                finish("tie", game_deck, dealer, player)
