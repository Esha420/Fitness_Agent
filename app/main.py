# app/main.py
import streamlit as st
import asyncio

from app.auth import get_current_user
from app.ai import ask_ai, get_macros
from app.profiles import create_profile, get_profile, get_notes
from app.form_submit import update_personal_info, add_note, delete_note

# -------------------------------------------------
# Async runner for Streamlit
# -------------------------------------------------
def run_async(coro):
    """
    Safely run async code inside Streamlit.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        return asyncio.run_coroutine_threadsafe(coro, loop).result()
    else:
        return asyncio.run(coro)


st.title("Personal Fitness Tool")

# -------------------------------------------------
# Auth (user identity)
# -------------------------------------------------
user_id, role = get_current_user()

# -------------------------------------------------
# Session Initialization
# -------------------------------------------------
def init_session():
    if "profile_id" not in st.session_state:
        profile_id = f"profile-{user_id}"
        profile = get_profile(profile_id, user_id)

        if not profile:
            profile = create_profile(profile_id, user_id)

        st.session_state.profile_id = profile_id
        st.session_state.profile = profile

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(
            st.session_state.profile_id,
            user_id
        )

init_session()

if st.session_state.profile is None:
    st.error("Profile could not be loaded")
    st.stop()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    if st.button("Logout"):
        for key in ["authenticated", "user_id", "role", "profile", "notes"]:
            st.session_state.pop(key, None)
        st.rerun()

# -------------------------------------------------
# Personal Data
# -------------------------------------------------
st.subheader("Personal Information")

with st.form("personal"):
    g = st.session_state.profile["general"]

    name = st.text_input("Name", g.get("name", ""))
    age = st.number_input("Age", 1, 120, g.get("age", 30))
    weight = st.number_input("Weight", 0.0, 300.0, float(g.get("weight", 60)))
    height = st.number_input("Height", 0.0, 250.0, float(g.get("height", 165)))
    gender = st.radio(
        "Gender",
        ["Male", "Female", "Other"],
        index=["Male", "Female", "Other"].index(g.get("gender", "Male")),
    )
    activity = st.selectbox(
        "Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
        index=[
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
        ].index(g.get("activity_level", "Moderately Active")),
    )

    if st.form_submit_button("Save"):
        try:
            st.session_state.profile = update_personal_info(
                st.session_state.profile,
                section="general",
                user_id=user_id,
                role=role,
                name=name,
                age=age,
                weight=weight,
                height=height,
                gender=gender,
                activity_level=activity,
            )
            st.success("Saved")
        except PermissionError:
            st.error("You are not allowed to update this profile")

# -------------------------------------------------
# Goals
# -------------------------------------------------
st.subheader("Goals")

with st.form("goals"):
    goals = st.multiselect(
        "Goals",
        ["Muscle Gain", "Fat Loss", "Stay Active"],
        st.session_state.profile.get("goals", []),
    )

    if st.form_submit_button("Save Goals"):
        try:
            st.session_state.profile = update_personal_info(
                st.session_state.profile,
                section="goals",
                user_id=user_id,
                role=role,
                goals=goals,
            )
            st.success("Goals updated")
        except PermissionError:
            st.error("You are not allowed to update goals")

# -------------------------------------------------
# Macros (AI via MCP)
# -------------------------------------------------
st.subheader("Macros")

if st.button("Generate with AI"):
    with st.spinner("Generating macros with AI..."):
        try:
            macros = run_async(
                get_macros(
                    st.session_state.profile["general"],
                    st.session_state.profile["goals"],
                    user_id
                )
            )
            st.session_state.profile["nutrition"] = macros
            st.success("Macros generated")
        except Exception as e:
            st.error("Failed to generate macros")
            st.exception(e)

if st.session_state.profile.get("nutrition"):
    st.json(st.session_state.profile["nutrition"])

# -------------------------------------------------
# Notes
# -------------------------------------------------
st.subheader("Notes")

for i, note in enumerate(st.session_state.notes):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(note["text"])
    with col2:
        if st.button("Delete", key=f"delete-{i}"):
            try:
                delete_note(note["_id"], user_id, role)
                st.session_state.notes.pop(i)
                st.rerun()
            except PermissionError:
                st.error("Not allowed to delete this note")

new_note = st.text_input("New Note")
if st.button("Add Note"):
    try:
        note = add_note(
            new_note,
            st.session_state.profile_id,
            user_id,
            role,
        )
        st.session_state.notes.append(note)
        st.rerun()
    except PermissionError:
        st.error("Not allowed to add notes")

# -------------------------------------------------
# Ask AI (MCP + Metrics)
# -------------------------------------------------
st.subheader("Ask AI")

question = st.text_input("Ask a question about fitness or nutrition")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            try:
                answer = run_async(
                    ask_ai(
                        st.session_state.profile,
                        question,
                        user_id,
                    )
                )

                # MCP responses may be text, list, or dict
                if isinstance(answer, list):
                    for msg in answer:
                        st.write(msg.get("text", msg))
                elif isinstance(answer, dict):
                    st.json(answer)
                else:
                    st.write(answer)

            except Exception as e:
                st.error("AI request failed")
                st.exception(e)
