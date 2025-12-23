#app/ai.py
import requests
import uuid, json
import os
import time
from datetime import datetime
from app.mcp_metrics import log_mcp_event

LANGFLOW_ID = os.getenv("LANGFLOW_ID")
TOKEN = os.getenv("LANGFLOW_TOKEN")
ORG_ID = os.getenv("ASTRA_ORG_ID")
REGION = os.getenv("LANGFLOW_REGION")

BASE_URL = f"https://{REGION}.langflow.datastax.com"

def build_mcp_context(user_id, profile):
    return {
        "user_id": user_id,
        "profile": profile,
        "timestamp": datetime.utcnow().isoformat()
    }

def _run_langflow(endpoint, tweaks):
    url = f"{BASE_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_type": "text",
        "output_type": "text",
        "session_id": str(uuid.uuid4()),
        "tweaks": tweaks
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "X-DataStax-Current-Org": ORG_ID,
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]

def ask_ai(profile, question, user_id):
    start = time.time()
    try:
        response = _run_langflow(
            "runflow",
            {
                "TextInput-osEzK": {"input_value": question},
                "MCPContext": {"context": build_mcp_context(user_id, profile)}
            }
        )
        status = "success"
        return response
    finally:
        log_mcp_event({
            "user_id": user_id,
            "agent": "qa-agent",
            "latency_ms": int((time.time() - start) * 1000),
            "status": status
        })

def get_macros(profile, goals, user_id):
    """
    AI macro generation (secured + MCP logged)
    """
    start = time.time()
    status = "success"

    try:
        result = _run_langflow(
            "macros",
            {
                "TextInput-V0W1U": {"input_value": ", ".join(goals)},
                "MCPContext": {
                    "context": build_mcp_context(user_id, profile)
                }
            }
        )
        return json.loads(result)
    except Exception:
        status = "error"
        raise
    finally:
        log_mcp_event({
            "user_id": user_id,
            "agent": "macro-agent",
            "latency_ms": int((time.time() - start) * 1000),
            "status": status
        })
