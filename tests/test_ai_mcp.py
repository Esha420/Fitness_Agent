import pytest
import logging
import asyncio

from app.ai import ask_ai, get_macros
from app.mcp_client import get_mcp_tools

# -------------------------------------------------
# Logging config (FULL LOGS)
# -------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


# -------------------------------------------------
# MCP Tool Load Test
# -------------------------------------------------
def test_mcp_tools_loaded():
    """
    Verifies MCP tools load correctly from LangFlow.
    """
    tools = get_mcp_tools()
    logger.info(f"Loaded MCP tools: {list(tools.keys())}")

    assert isinstance(tools, dict)
    assert "ask_ai" in tools
    assert "macro" in tools


# -------------------------------------------------
# Ask AI Test
# -------------------------------------------------
@pytest.mark.asyncio
async def test_ask_ai():
    profile = {
        "general": {
            "name": "Isha",
            "age": 25,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active"
        },
        "goals": ["Fat Loss"]
    }

    user_id = "test-user-ask-ai"
    question = "How much protein should I eat daily?"

    logger.info("Calling ask_ai MCP tool...")

    response = await ask_ai(profile, question, user_id)

    logger.info("ask_ai response received:")
    logger.info(response)

    # Basic validation
    assert response is not None
    assert isinstance(response, (str, list, dict))


# -------------------------------------------------
# Get Macros Test
# -------------------------------------------------
@pytest.mark.asyncio
async def test_get_macros():
    profile = {
        "name": "Isha",
        "age": 25,
        "weight": 60,
        "height": 165,
        "activity_level": "Moderately Active"
    }

    goals = ["Fat Loss", "Muscle Gain"]
    user_id = "test-user-macros"

    logger.info("Calling get_macros MCP tool...")

    macros = await get_macros(profile, goals, user_id)

    logger.info("get_macros response received:")
    logger.info(macros)

    # Validation
    assert macros is not None
    assert isinstance(macros, (dict, list))

    if isinstance(macros, dict):
        assert "protein" in macros
        assert "calories" in macros
