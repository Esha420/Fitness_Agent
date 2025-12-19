from app.auth import get_current_user
import streamlit as st

def test_get_current_user_creates_id():
    st.session_state.clear()
    user_id, role = get_current_user()
    assert user_id is not None
    assert role == "user"
