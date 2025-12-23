# app/db.py
from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

if not ENDPOINT or not TOKEN:
    raise RuntimeError("ASTRA_ENDPOINT or ASTRA_DB_APPLICATION_TOKEN missing")

# -------------------------------------------------
# DB Connection
# -------------------------------------------------
@st.cache_resource
def get_db():
    client = DataAPIClient(TOKEN)
    return client.get_database_by_api_endpoint(ENDPOINT)

db = get_db()

# -------------------------------------------------
# Collection bootstrap (safe + idempotent)
# -------------------------------------------------
REQUIRED_COLLECTIONS = [
    "users",          # 🔐 authentication
    "personal_data",  # 👤 profiles
    "notes",          # 📝 notes
    "mcp_metrics"     # 📊 observability
]

try:
    existing_collections = {
        c["name"] for c in db.list_collections()
    }
except Exception:
    existing_collections = set()

for name in REQUIRED_COLLECTIONS:
    if name not in existing_collections:
        try:
            db.create_collection(name)
        except Exception as e:
            print(f"[WARN] Failed to create collection '{name}': {e}")

# -------------------------------------------------
# Collection handles
# -------------------------------------------------
users_collection = db.get_collection("users")
personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")
mcp_metrics_collection = db.get_collection("mcp_metrics")
