"""This file loads the page responsible for reloading user funds"""

import streamlit as st

def show_reload():
    """This function displays page elements for reload page"""

    # show page elements
    st.title("You've gone bankrupt!!!")
    st.subheader("Want to continue playing? Go ahead and reload your funds, on us.")
    st.markdown(
        ":red[**WARNING:** This will permanently alter your *shame tally!*] "
        "Click the button below to continue..."
    )

    def cb():
        st.session_state.bankroll = 1000
        st.session_state.shame_counter += 1
        st.session_state.current_page = "home"

    st.button("I suck at gambling", on_click=cb)
