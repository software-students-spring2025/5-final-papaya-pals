import streamlit as st

def show_home():
    st.title("Let's play!")
    row1col1, row1gap, row1col2 = st.columns([0.2, 0.6, 0.2])
    with row1col1:
        def cb():
            st.session_state.current_page = "slots"
        st.button("Slots", onclick=cb)
    with row1col2:
        def cb():
            st.session_state.current_page = "blackjack"
        st.button("Blackjack", onclick=cb)
    
    row2left, row2col1, row2gap, row2col2, row2right = st.columns([0.2, 0.1, 0.4, 0.1, 0.2])
    with row2col1:
        def cb():
            st.session_state.current_page = "roulette"
        st.button("Roulette", onclick=cb)
    with row2col2:
        def cb():
            st.session_state.current_page = "unknown_game1"
        st.button("[Game]", onclick=cb)

    row3left, row3col, row3right = st.columns([0.45, 0.1, 0.45])
    with row3col:
        def cb():
            st.session_state.current_page = "unknown_game2"
        st.button("[Game]", onclick=cb)

