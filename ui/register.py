import streamlit as st
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import User
from auth.auth_utils import hash_password


def show_register():

    st.subheader("Register")

    name = st.text_input("Name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Select Role",
        [
            "Job Seeker",
            "Recruiter"
        ]
    )

    if st.button("Register"):

        db: Session = SessionLocal()

        existing_user = db.query(User).filter(
            User.email == email
        ).first()

        if existing_user:
            st.error("Email already exists")
            return

        user = User(
            name=name,
            email=email,
            password=hash_password(password),
            role=role
        )

        db.add(user)
        db.commit()

        st.success(
            "Registration Successful"
        )