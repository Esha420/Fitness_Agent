#app/form_submit.py
from app.cerbos_client import check_access
from app.db import personal_data_collection, notes_collection
from app.telmetry import trace_span
from datetime import datetime
import uuid

def update_personal_info(profile, section, user_id, role, **data):

    with trace_span(
        "profile.update",
        user_id,
        {"section": section},
    ):
        if not check_access(
            action="update",
            resource_kind="profile",
            resource_id=str(profile["_id"]),
            principal_id=user_id,
            resource_owner_id=profile["user_id"],
            role=role
        ):
            raise PermissionError("Access denied")

        profile[section] = data if section != "goals" else data["goals"]

        personal_data_collection.update_one(
            {"_id": profile["_id"]},
            {"$set": {section: profile[section]}}
        )
        return profile


def add_note(text, profile_id, user_id, role):

    with trace_span(
        "notes.add",
        user_id,
        {"profile_id": profile_id},
    ):
        note_id = str(uuid.uuid4())

        if not check_access(
            action="write",
            resource_kind="note",
            resource_id=note_id,
            principal_id=user_id,
            resource_owner_id=user_id,
            role=role
        ):
            raise PermissionError("Access denied")

        note = {
            "_id": note_id,
            "user_id": user_id,
            "profile_id": profile_id,
            "text": text,
            "$vectorize": text,
            "metadata": {"created": datetime.utcnow().isoformat()}
        }

        notes_collection.insert_one(note)
        return note


def delete_note(note_id, user_id, role):

    with trace_span(
        "notes.delete",
        user_id,
        {"note_id": note_id},
    ):
        note = notes_collection.find_one({"_id": note_id})
        if not note:
            return

        if not check_access(
            action="delete",
            resource_kind="note",
            resource_id=str(note["_id"]),
            principal_id=user_id,
            resource_owner_id=note["user_id"],
            role=role
        ):
            raise PermissionError("Access denied")

        notes_collection.delete_one({"_id": note_id})
