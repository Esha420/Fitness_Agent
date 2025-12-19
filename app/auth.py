import streamlit as st
import uuid

def get_current_user():
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
        st.session_state.role = "user"
    return st.session_state.user_id, st.session_state.role
