from app.db import personal_data_collection, notes_collection

def default_profile(profile_id, user_id):
    return {
        "_id": profile_id,
        "user_id": user_id,
        "general": {
            "name": "",
            "age": 30,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male"
        },
        "goals": ["Muscle Gain"],
        "nutrition": {}
    }

def create_profile(profile_id, user_id):
    profile = default_profile(profile_id, user_id)

    try:
        personal_data_collection.update_one(
            {"_id": profile_id, "user_id": user_id},
            {"$setOnInsert": profile},  # Only insert if not exists
            upsert=True
        )
    except Exception as e:
        print(f"[WARN] Failed to upsert profile: {e}")

    # Fetch profile from DB
    profile = personal_data_collection.find_one({
        "_id": profile_id,
        "user_id": user_id
    })

    if not profile:
        raise RuntimeError(
            "Failed to create or retrieve profile from DB — check collection schema!"
        )

    return profile





def get_profile(profile_id, user_id):
    return personal_data_collection.find_one({
        "_id": profile_id,
        "user_id": user_id
    })

def get_notes(profile_id, user_id):
    """
    User-scoped notes retrieval
    """
    return list(
        notes_collection.find({
            "profile_id": profile_id,
            "user_id": user_id
        })
    )