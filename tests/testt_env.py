import os
from dotenv import load_dotenv

load_dotenv()

VARS = [
    "LANGFLOW_TOKEN",
    "ASTRA_ORG_ID",
    "LANGFLOW_ID",
    "LANGFLOW_REGION",
    "ASTRA_DB_APPLICATION_TOKEN",
    "ASTRA_ENDPOINT",
]

for v in VARS:
    value = os.getenv(v)
    print(f"{v}: {'SET' if value else '❌ MISSING'}")
