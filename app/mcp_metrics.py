from datetime import datetime
from app.db import db

metrics_collection = db.get_collection("mcp_metrics")

def log_mcp_event(event):
    event["timestamp"] = datetime.utcnow().isoformat()
    metrics_collection.insert_one(event)
