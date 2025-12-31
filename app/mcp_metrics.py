#mcp_metrics.py
from app.db import mcp_metrics_collection
from datetime import datetime

def log_mcp_event(event: dict):
    """
    Persist telemetry events safely.
    """
    event["timestamp"] = datetime.utcnow().isoformat()

    try:
        mcp_metrics_collection.insert_one(event)
    except Exception as e:
        print(f"[WARN] Failed to log MCP event: {e}")
