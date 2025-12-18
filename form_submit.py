#form_submit.py
from db import personal_data_collection, notes_collection
from datetime import datetime


def update_personal_info(existing, section, **data):
    existing[section] = data if section != "goals" else data["goals"]

    personal_data_collection.update_one(
        {"_id": existing["_id"]},
        {"$set": {section: existing[section]}},
    )
    return existing


def add_note(text, profile_id):
    note = {
        "user_id": profile_id,
        "text": text,
        "$vectorize": text,
        "metadata": {"ingested": datetime.utcnow().isoformat()},
    }
    result = notes_collection.insert_one(note)
    note["_id"] = result.inserted_id
    return note


def delete_note(_id):
    notes_collection.delete_one({"_id": _id})
