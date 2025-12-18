#profiles.py
from db import personal_data_collection, notes_collection


def default_profile(_id):
    return {
        "_id": _id,
        "general": {
            "name": "",
            "age": 30,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male",
        },
        "goals": ["Muscle Gain"],
        "nutrition": {
            "calories": 2000,
            "protein": 140,
            "fat": 20,
            "carbs": 100,
        },
    }


def create_profile(_id):
    profile = default_profile(_id)
    personal_data_collection.insert_one(profile)
    return _id, profile


def get_profile(_id):
    return personal_data_collection.find_one({"_id": _id})


def get_notes(profile_id):
    return list(notes_collection.find({"user_id": profile_id}))
