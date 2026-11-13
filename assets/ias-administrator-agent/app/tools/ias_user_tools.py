"""
IAS User Management Tools.

These tools call the IAS Identity Directory SCIM MCP server.
All SAP API interactions go through MCP tools — no direct HTTP calls.
"""

import logging
from typing import Optional
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def search_user(query: str) -> str:
    """
    Search for a user in SAP IAS by name, email address, or user ID.

    Args:
        query: The search term — can be a display name, email address, or user ID.

    Returns:
        A summary of matching users including display name, email, user ID, and account status.
        Returns a not-found message if no users match the query.
    """
    # This tool is a descriptor for the agent.
    # At runtime the agent uses the IAS SCIM MCP tool to search /scim/Users.
    # The MCP tool is loaded dynamically via get_mcp_tools() and the agent
    # selects the appropriate tool by capability.
    return f"Searching IAS for user: {query}"


@tool
def get_user_details(user_id: str) -> str:
    """
    Retrieve full details for a specific user from SAP IAS by their user ID.

    Args:
        user_id: The IAS user ID (SCIM ID) of the user.

    Returns:
        Full user profile including status, group memberships, email, and key attributes.
    """
    return f"Retrieving full details for user ID: {user_id}"


@tool
def reset_user_password(user_id: str) -> str:
    """
    Reset the password for a specific user in SAP IAS.

    IMPORTANT: This is a write operation. The agent MUST obtain explicit user
    confirmation before calling this tool.

    Args:
        user_id: The IAS user ID (SCIM ID) of the user whose password will be reset.

    Returns:
        Confirmation that the password reset was triggered, or an error message.
    """
    return f"Triggering password reset for user ID: {user_id}"


@tool
def unlock_user_account(user_id: str) -> str:
    """
    Unlock a locked user account in SAP IAS.

    IMPORTANT: This is a write operation. The agent MUST obtain explicit user
    confirmation before calling this tool.

    Args:
        user_id: The IAS user ID (SCIM ID) of the locked user account.

    Returns:
        Confirmation that the account was unlocked, or an error message.
    """
    return f"Unlocking account for user ID: {user_id}"
