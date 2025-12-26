# app/mcp_client.py
import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StreamableHttpConnection
from langchain_mcp_adapters.tools import load_mcp_tools

_tools_cache = None

load_dotenv()

# Load environment variables
GEMINI_1_API_KEY = os.environ.get("GEMINI_1_API_KEY")
GEMINI_2_API_KEY = os.environ.get("GEMINI_2_API_KEY")
GEMINI_3_API_KEY = os.environ.get("GEMINI_3_API_KEY")
STRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
APP_TOKEN = os.environ.get("DATASTRAX_APPLICATION_TOKEN")
ORG_ID = os.environ.get("ASTRA_ORG_ID")
MCP_URL = "https://aws-us-east-2.langflow.datastax.com/lf/70e469c4-f68c-4135-a878-25ce31b4deab/api/v1/mcp/project/78cf9c48-14be-4972-8a2f-0c5608c98097/streamable"


async def _load_tools_async():
    client = MultiServerMCPClient(
        connections={
            "lf-starter_project": StreamableHttpConnection(
                url=MCP_URL,
                headers={
                    "Authorization": f"Bearer {APP_TOKEN}",
                    "X-DataStax-Current-Org": ORG_ID,
                },
                transport="http",  # required by MCP adapter
            )
        }
    )

    # Load all tools from the server
    tools = await client.get_tools(server_name="lf-starter_project")
    return {tool.name: tool for tool in tools}


def get_mcp_tools():
    """Synchronous getter with caching for MCP tools."""
    global _tools_cache
    if _tools_cache is None:
        _tools_cache = asyncio.run(_load_tools_async())
    return _tools_cache
