#main.py
import streamlit as st
from ai import ask_ai, get_macros
from profiles import create_profile, get_profile, get_notes
from form_submit import update_personal_info, add_note, delete_note

st.title("Personal Fitness Tool")


def init_session():
    if "profile_id" not in st.session_state:
        profile_id = 1
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)

        st.session_state.profile_id = profile_id
        st.session_state.profile = profile

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)


init_session()


# -------- Personal Data --------
with st.form("personal"):
    g = st.session_state.profile["general"]

    name = st.text_input("Name", g["name"])
    age = st.number_input("Age", 1, 120, g["age"])
    weight = st.number_input("Weight", 0.0, 300.0, float(g["weight"]))
    height = st.number_input("Height", 0.0, 250.0, float(g["height"]))
    gender = st.radio("Gender", ["Male", "Female", "Other"], index=0)
    activity = st.selectbox(
        "Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
    )

    if st.form_submit_button("Save"):
        st.session_state.profile = update_personal_info(
            st.session_state.profile,
            "general",
            name=name,
            age=age,
            weight=weight,
            height=height,
            gender=gender,
            activity_level=activity,
        )
        st.success("Saved")


# -------- Goals --------
with st.form("goals"):
    goals = st.multiselect(
        "Goals", ["Muscle Gain", "Fat Loss", "Stay Active"],
        st.session_state.profile["goals"]
    )

    if st.form_submit_button("Save Goals"):
        st.session_state.profile = update_personal_info(
            st.session_state.profile,
            "goals",
            goals=goals,
        )


# -------- Macros --------
st.subheader("Macros")
if st.button("Generate with AI"):
    result = get_macros(
        st.session_state.profile["general"],
        st.session_state.profile["goals"],
    )
    st.session_state.profile["nutrition"] = result
    st.success("Generated")


# -------- Notes --------
st.subheader("Notes")
for i, note in enumerate(st.session_state.notes):
    if st.button(f"Delete {i}"):
        delete_note(note["_id"])
        st.rerun()

note = st.text_input("New Note")
if st.button("Add Note"):
    st.session_state.notes.append(
        add_note(note, st.session_state.profile_id)
    )
    st.rerun()


# -------- Ask AI --------
st.subheader("Ask AI")
q = st.text_input("Ask a question")
if st.button("Ask"):
    st.write(ask_ai(st.session_state.profile, q))
