#db.py
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

for name in ["personal_data", "notes"]:
    try:
        db.create_collection(name)
    except Exception:
        pass

personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")
