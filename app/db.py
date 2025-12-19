# app/db.py
from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")


@st.cache_resource
def get_db():
    client = DataAPIClient(TOKEN)
    return client.get_database_by_api_endpoint(ENDPOINT)


db = get_db()

# List existing collections to avoid errors
try:
    existing_collections = [c["name"] for c in db.list_collections()]
except Exception:
    existing_collections = []

for name in ["personal_data", "notes", "mcp_metrics"]:
    if name not in existing_collections:
        try:
            db.create_collection(name)
        except Exception as e:
            print(f"[WARN] Failed to create collection '{name}': {e}")

personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")
mcp_metrics_collection = db.get_collection("mcp_metrics")
