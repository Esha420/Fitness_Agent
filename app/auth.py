# app/auth.py
import streamlit as st
import bcrypt
import uuid
from datetime import datetime
from app.db import users_collection

# ---------------------------
# Helpers
# ---------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------------------
# Signup
# ---------------------------
def signup():
    st.subheader("Sign Up")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pw")
    confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

    if st.button("Create Account"):
        if not email or not password:
            st.error("Email and password required")
            return

        if password != confirm:
            st.error("Passwords do not match")
            return

        if users_collection.find_one({"email": email}):
            st.error("User already exists")
            return

        user = {
            "_id": str(uuid.uuid4()),
            "email": email,
            "password": hash_password(password),
            "role": "user",  # default role
            "created_at": datetime.utcnow().isoformat()
        }

        users_collection.insert_one(user)
        st.success("Account created. Please log in.")
        st.rerun()

# ---------------------------
# Login
# ---------------------------
def login():
    st.subheader("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pw")

    if st.button("Login"):
        user = users_collection.find_one({"email": email})

        if not user or not verify_password(password, user["password"]):
            st.error("Invalid credentials")
            return

        st.session_state.authenticated = True
        st.session_state.user_id = user["_id"]
        st.session_state.role = user["role"]

        st.success("Logged in")
        st.rerun()

# ---------------------------
# Entry Point (BLOCKING)
# ---------------------------
def get_current_user():
    if st.session_state.get("authenticated"):
        return st.session_state.user_id, st.session_state.role

    st.title("Welcome 👋")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        login()

    with tab2:
        signup()

    st.stop()
