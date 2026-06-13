import streamlit as st

from database.db import SessionLocal
from database.models import User

from auth.auth_utils import verify_password


def show_login():

    st.subheader("Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        db = SessionLocal()

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            st.error("User not found")
            return

        if not verify_password(
            password,
            user.password
        ):
            st.error("Wrong password")
            return

        st.session_state["logged_in"] = True

        st.session_state["user_name"] = user.name

        st.session_state["role"] = user.role

        st.success("Login Successful")