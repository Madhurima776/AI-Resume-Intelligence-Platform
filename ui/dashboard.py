import streamlit as st


def show_dashboard():

    st.title("Dashboard")

    st.write(
        f"Welcome {st.session_state['user_name']}"
    )

    st.write(
        f"Role: {st.session_state['role']}"
    )