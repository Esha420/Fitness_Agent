# tests/test_cerbos.py
import pytest
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource, ResourceList
from app.ai import ask_ai, get_macros  # assuming these are your async functions

CERBOS_URL = "http://localhost:3592"

def cerbos_response(principal_id, role, action, resource_kind, resource_id, resource_owner_id=None):
    with CerbosClient(CERBOS_URL) as client:
        principal = Principal(
            id=principal_id,
            roles=[role],
        )
        resource = Resource(
            id=resource_id,
            kind=resource_kind,
            attr={"user_id": resource_owner_id} if resource_owner_id else {},
        )
        allowed = client.is_allowed(action, principal, resource)

        # Wrap resource in ResourceList for check_resources
        resource_list = ResourceList([resource])
        response = client.check_resources(principal, resource_list)
        return allowed, response


# ---------------------------
# Cerbos Policy Tests
# ---------------------------
def test_profile_update_allowed():
    allowed, resp = cerbos_response(
        principal_id="user-123",
        role="user",
        action="update",
        resource_kind="profile",
        resource_id="profile-1",
        resource_owner_id="user-123"
    )
    print("=== Profile Update Allowed ===")
    print("Allowed:", allowed)
    print("Full response:", resp)
    assert allowed is True


def test_profile_update_denied():
    allowed, resp = cerbos_response(
        principal_id="user-456",
        role="user",
        action="update",
        resource_kind="profile",
        resource_id="profile-1",
        resource_owner_id="user-123"
    )
    print("=== Profile Update Denied ===")
    print("Allowed:", allowed)
    print("Full response:", resp)
    assert allowed is False


def test_agent_call_allowed():
    allowed, resp = cerbos_response(
        principal_id="qa-agent",
        role="agent",
        action="call",
        resource_kind="agent",
        resource_id="qa-agent"
    )
    print("=== Agent Call Allowed ===")
    print("Allowed:", allowed)
    print("Full response:", resp)
    assert allowed is True


def test_agent_call_denied_wrong_role():
    allowed, resp = cerbos_response(
        principal_id="qa-agent",
        role="user",
        action="call",
        resource_kind="agent",
        resource_id="qa-agent"
    )
    print("=== Agent Call Denied Wrong Role ===")
    print("Allowed:", allowed)
    print("Full response:", resp)
    assert allowed is False


# ---------------------------
# Async MCP Call Tests
# ---------------------------
def test_ask_ai_mcp_call():
    import asyncio

    profile = {"general": {"name": "Test User"}, "goals": ["Muscle Gain"]}
    question = "How much protein should I eat?"
    user_id = "agent-askai"

    # Run the async function safely
    answer = asyncio.run(ask_ai(profile, question, user_id))
    print("=== ask_ai MCP Call ===")
    print("Answer:", answer)
    assert answer is not None


def test_get_macros_mcp_call():
    import asyncio

    profile = {"general": {"name": "Test User"}, "goals": ["Muscle Gain"]}
    goals = ["Muscle Gain", "Stay Active"]
    user_id = "agent-macros"

    macros = asyncio.run(get_macros(profile, goals, user_id))
    print("=== get_macros MCP Call ===")
    print("Macros:", macros)
    assert macros is not None
