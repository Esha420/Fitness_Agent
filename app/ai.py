# app/ai.py
import time
import json
from datetime import datetime
from app.mcp_client import get_mcp_tools
from app.cerbos_client import check_access
from app.mcp_authorization import MCP_AUTHZ
from app.mcp_metrics import log_mcp_event

# Load tools once
TOOLS = get_mcp_tools()
FLOW_TOOLS = {tool.name: tool for tool in TOOLS.values()}

def build_mcp_context(user_id, profile):
    return {
        "user_id": user_id,
        "profile": profile,
        "timestamp": datetime.utcnow().isoformat()
    }

# -------------------------------------------------
# Ask AI (QA Flow)
# -------------------------------------------------
async def ask_ai(profile, question, user_id):
    start = time.time()
    status = "success"

    try:
        auth = MCP_AUTHZ["ask_ai"]

        allowed = check_access(
            principal_id=user_id,
            role=auth["role"],
            action=auth["action"],
            resource_kind=auth["resource"],
            resource_id=auth["resource_id"],
        )

        if not allowed:
            raise PermissionError("Cerbos denied ask_ai")

        tool = FLOW_TOOLS["ask_ai"]

        return await tool.arun({
            "question": question,
            "context": build_mcp_context(user_id, profile),
        })

    except Exception:
        status = "error"
        raise

    finally:
        log_mcp_event({
            "user_id": user_id,
            "agent": "qa-agent",
            "latency_ms": int((time.time() - start) * 1000),
            "status": status,
        })



# -------------------------------------------------
# Macro Generation Flow
# -------------------------------------------------
async def get_macros(profile, goals, user_id):
    start = time.time()
    status = "success"

    try:
        auth = MCP_AUTHZ["macro"]

        allowed = check_access(
            principal_id=user_id,
            role=auth["role"],
            action=auth["action"],
            resource_kind=auth["resource"],
            resource_id=auth["resource_id"],
        )

        if not allowed:
            raise PermissionError("Cerbos denied macro")

        tool = FLOW_TOOLS["macro"]

        result = await tool.arun({
            "goals": ", ".join(goals),
            "context": build_mcp_context(user_id, profile),
        })
        if isinstance(result, list):
            for item in result:
                if "text" in item:
                    return item["text"]
            return ""  # fallback if no text found
        elif isinstance(result, dict) and "text" in result:
            return result["text"]
        elif isinstance(result, str):
            return result
        else:
            return ""

    except Exception:
        status = "error"
        raise

    finally:
        log_mcp_event({
            "user_id": user_id,
            "agent": "macro-agent",
            "latency_ms": int((time.time() - start) * 1000),
            "status": status,
        })
