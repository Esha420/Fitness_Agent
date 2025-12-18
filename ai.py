#ai.py
import requests
import uuid
import os
import json
from dotenv import load_dotenv

load_dotenv()

LANGFLOW_ID = os.getenv("LANGFLOW_ID")
ORG_ID = os.getenv("ASTRA_ORG_ID")
TOKEN = os.getenv("LANGFLOW_TOKEN")
REGION = os.getenv("LANGFLOW_REGION")

BASE_URL = f"https://{REGION}.langflow.datastax.com"


def dict_to_string(obj, level=0):
    indent = "  " * level
    if isinstance(obj, dict):
        return ", ".join(
            f"{indent}{k}: {dict_to_string(v, level + 1)}"
            for k, v in obj.items()
        )
    if isinstance(obj, list):
        return ", ".join(dict_to_string(v, level + 1) for v in obj)
    return str(obj)


def _run_langflow(endpoint: str, tweaks: dict):
    url = f"{BASE_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_type": "text",
        "output_type": "text",
        "session_id": str(uuid.uuid4()),
        "tweaks": tweaks,
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "X-DataStax-Current-Org": ORG_ID,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]


def ask_ai(profile: dict, question: str) -> str:
    tweaks = {
        "TextInput-osEzK": {
            "input_value": question
        },
        "TextInput-rDUdT": {
            "input_value": dict_to_string(profile)
        }
    }

    return _run_langflow("runflow", tweaks)


def get_macros(profile: dict, goals: list) -> dict:
    tweaks = {
        "TextInput-V0W1U": {
            "input_value": ", ".join(goals)
        },
        "TextInput-0c1eL": {
            "input_value": dict_to_string(profile)
        }
    }

    result = _run_langflow("macros", tweaks)
    return json.loads(result)
