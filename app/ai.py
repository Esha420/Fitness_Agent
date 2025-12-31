from datetime import datetime
from app.mcp_client import get_mcp_tools
from app.cerbos_client import check_access
from app.mcp_authorization import MCP_AUTHZ
from app.telmetry import trace_span, get_current_trace_id
from app.auth_tokens import verify_token
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

TOOLS = get_mcp_tools()
FLOW_TOOLS = {tool.name: tool for tool in TOOLS.values()}

def build_mcp_context(user_id, role, profile):
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier)

    return {
        "trace_context": carrier,
        "user_id": user_id,
        "role": role,
        "profile": profile,
        "timestamp": datetime.utcnow().isoformat(),
        "trace_id": get_current_trace_id(),
    }

async def ask_ai(profile, question, token):
    with trace_span("ai.ask_ai.total", "anonymous"):
        with trace_span("auth.jwt.verify", "anonymous"):
            auth_ctx = verify_token(token)

        user_id = auth_ctx["sub"]
        role = auth_ctx["role"]

        auth = MCP_AUTHZ["ask_ai"]

        with trace_span("cerbos.ask_ai.check", user_id):
            allowed = check_access(
                principal_id=user_id,
                role=role,
                action=auth["action"],
                resource_kind=auth["resource"],
                resource_id=auth["resource_id"],
            )

        if not allowed:
            raise PermissionError("Cerbos denied ask_ai")

        with trace_span("mcp.ask_ai.invoke", user_id):
            return await FLOW_TOOLS["ask_ai"].arun({
                "question": question,
                "context": build_mcp_context(user_id, role, profile),
            })

async def get_macros(profile, goals, token):
    with trace_span("ai.macro.total", "anonymous"):
        with trace_span("auth.jwt.verify", "anonymous"):
            auth_ctx = verify_token(token)

        user_id = auth_ctx["sub"]
        role = auth_ctx["role"]

        auth = MCP_AUTHZ["macro"]

        with trace_span("cerbos.macro.check", user_id):
            allowed = check_access(
                principal_id=user_id,
                role=role,
                action=auth["action"],
                resource_kind=auth["resource"],
                resource_id=auth["resource_id"],
            )

        if not allowed:
            raise PermissionError("Cerbos denied macro")

        with trace_span("mcp.macro.invoke", user_id):
            result = await FLOW_TOOLS["macro"].arun({
                "goals": ", ".join(goals),
                "context": build_mcp_context(user_id, role, profile),
            })

        return result
