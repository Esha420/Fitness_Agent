# tests/test_mcp_load.py
from app.mcp_client import get_mcp_tools

def test_mcp_tools_load():
    tools = get_mcp_tools()
    assert tools, "No MCP tools loaded"
    tool_names = set(tools.keys())
    print("✅ Loaded MCP tools:", tool_names)

    # Check your expected tool names
    assert "ask_ai" in tool_names
    assert "macro" in tool_names
