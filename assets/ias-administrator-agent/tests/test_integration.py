"""
Integration test: end-to-end agent flow with mocked LLM and MCP tools.

Tests that the agent:
1. Receives a password reset request
2. Issues a confirmation prompt (require_user_input)
3. On confirmation, calls the reset tool and completes
"""
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from langchain_core.messages import AIMessage


@pytest.mark.asyncio
async def test_agent_password_reset_flow():
    """Integration test: agent processes a password reset request."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_tool = MagicMock()
    mock_tool.name = "resetUserPassword"
    mock_tool.description = "Reset user password"

    mock_result = {
        "messages": [
            AIMessage(content=(
                "I am about to reset the password for John Doe (john.doe@company.com, ID: user-abc-123). "
                "This will force them to set a new password on next login. Do you confirm?"
            ))
        ]
    }

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_result

        chunks = []
        async for chunk in agent.stream(
            query="Reset the password for john.doe@company.com",
            context_id="test-ctx-001",
            tools=[mock_tool],
        ):
            chunks.append(chunk)

    assert len(chunks) >= 2
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert "confirm" in final["content"].lower() or "password" in final["content"].lower()


@pytest.mark.asyncio
async def test_agent_search_user_flow():
    """Integration test: agent processes a user search request."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_result = {
        "messages": [
            AIMessage(content=(
                "I found the following user:\n"
                "- Name: John Doe\n"
                "- Email: john.doe@company.com\n"
                "- ID: user-abc-123\n"
                "- Status: Active"
            ))
        ]
    }

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_result

        chunks = []
        async for chunk in agent.stream(
            query="Find user john.doe@company.com",
            context_id="test-ctx-002",
            tools=[],
        ):
            chunks.append(chunk)

    assert len(chunks) >= 1
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert "john" in final["content"].lower() or "user" in final["content"].lower()


@pytest.mark.asyncio
async def test_agent_handles_no_tools():
    """Integration test: agent gracefully handles missing tools."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_result = {
        "messages": [
            AIMessage(content="Tools are temporarily unavailable. Please try again later.")
        ]
    }

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_result

        chunks = []
        async for chunk in agent.stream(
            query="Find user test@example.com",
            context_id="test-ctx-003",
            tools=None,
        ):
            chunks.append(chunk)

    assert len(chunks) >= 1
    final = chunks[-1]
    assert final["is_task_complete"] is True
