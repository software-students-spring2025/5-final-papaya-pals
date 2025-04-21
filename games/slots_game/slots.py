import streamlit as st
import random
from ..initialize import initial_count

icons =["🍒", "🍋", "🔔", "💎", "7️⃣"]

def play_slots():
    print('playing')
    initial_count()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Welcome to Slots! 🎰")
    with col2:
        st.markdown(f"**Shame Counter:** {st.session_state.shame_counter}")

    st.write(f"Bankroll: ${st.session_state.bankroll}")
    bet_amount = st.number_input("Enter your bet amount:", min_value=1, max_value=st.session_state.bankroll)
    
    if bet_amount != st.session_state.bet_amount:
        st.session_state.bet_amount = bet_amount

    if st.button("Spin! 💰"):
        if bet_amount > st.session_state.bankroll:
            st.warning("You don't have enough funds to place this bet.")
        else:
             st.session_state.bankroll -= bet_amount
             i = spin()
             st.write(" ".join(i))
             result, win_amount = payout(i, bet_amount)
             st.write(result)
             st.session_state.bankroll += win_amount

             # Add to shame counter
             if st.session_state.bankroll <= 0:
                st.session_state.shame_counter += 1
                st.write("You're bankrupt! Reloading funds...")
                st.session_state.bankroll = 1000
                
            #st.experimental_rerun()
def spin():
    return [random.choice(icons) for i in range(3)]

def payout(icons, bet_amount):
    if icons[0] == icons[1] == icons[2] == "7️⃣":
        return "Jackpot! Triple 7️⃣!", 100 * bet_amount
    elif icons[0] == icons[1] == icons[2]:
        return "Three of a Kind!", 5 * bet_amount
    elif icons[0] == icons[1] or icons[1] == icons[2] or icons[0] == icons[2]:
        return "Small win!", 2 * bet_amount
    else:
        return "No Wins.", -bet_amount