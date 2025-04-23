import streamlit as st

def show_home():

    # home page title
    titleleft, titlecol, titleright = st.columns([0.3, 0.4, 0.3])
    with titlecol:
        st.title("Let's play!")
    
    # show all game buttons
    row1col1, row1gap, row1col2 = st.columns([0.2, 0.6, 0.2])
    with row1col1:
        def cb():
            st.session_state.current_page = "slots"
        st.button("Slots", on_click=cb)
    with row1col2:
        def cb():
            st.session_state.current_page = "blackjack"
        st.button("Blackjack", on_click=cb)
    
    row2left, row2col1, row2gap, row2col2, row2right = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])
    with row2col1:
        def cb():
            st.session_state.current_page = "roulette"
        st.button("Roulette", on_click=cb)
    with row2col2:
        def cb():
            st.session_state.current_page = "unknown_game1"
        st.button("[Game 1]", on_click=cb)

    row3left, row3col, row3right = st.columns([0.35, 0.2, 0.35])
    with row3col:
        def cb():
            st.session_state.current_page = "unknown_game2"
        st.button("[Game 2]", on_click=cb)

