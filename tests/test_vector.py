from db import notes_collection

doc = {
    "user_id": 1,
    "text": "I have knee pain during squats",
    "$vectorize": "I have knee pain during squats"
}

res = notes_collection.insert_one(doc)
print("Inserted:", res.inserted_id)

docs = list(notes_collection.find({"user_id": 1}))
print("Docs found:", len(docs))
