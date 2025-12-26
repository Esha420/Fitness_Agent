MCP_AUTHZ = {
    "ask_ai": {
        "resource": "agent",
        "action": "call",
        "role": "agent",
        "resource_id": "qa-agent",
    },
    "macro": {
        "resource": "agent",
        "action": "call",
        "role": "agent",
        "resource_id": "macro-agent",
    },
    "profile_update": {
        "resource": "profile",
        "action": "update",
        "role": "user",
    },
    "note_write": {
        "resource": "note",
        "action": "write",
        "role": "user",
    },
    "note_delete": {
        "resource": "note",
        "action": "delete",
        "role": "user",
    },
}
