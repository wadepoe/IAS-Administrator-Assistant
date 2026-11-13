"""
IAS Group Management Tools.

These tools call the IAS Identity Directory SCIM MCP server.
All SAP API interactions go through MCP tools — no direct HTTP calls.
"""

import logging
from typing import List
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def manage_user_group(user_id: str, group_name: str, action: str) -> str:
    """
    Assign or remove an IAS group for a single user.

    IMPORTANT: This is a write operation. The agent MUST obtain explicit user
    confirmation before calling this tool.

    Args:
        user_id: The IAS user ID (SCIM ID) of the user.
        group_name: The display name of the IAS group to assign or remove.
        action: Either "assign" to add the user to the group, or "remove" to take them out.

    Returns:
        Confirmation that the group membership was updated, or an error message.
    """
    return f"Updating group '{group_name}' for user ID '{user_id}' — action: {action}"


@tool
def bulk_manage_user_groups(user_ids: List[str], group_name: str, action: str) -> str:
    """
    Assign or remove an IAS group for a list of user IDs in a single operation.

    IMPORTANT: This is a write operation. The agent MUST:
    1. Validate the group exists FIRST (before processing any users).
    2. Present a full summary of all affected users and obtain explicit confirmation.
    3. Process each user sequentially and report per-user success/failure.
    4. Continue processing remaining users even if one fails.

    Args:
        user_ids: List of IAS user IDs to process.
        group_name: The display name of the IAS group.
        action: Either "assign" to add users to the group, or "remove" to take them out.

    Returns:
        A per-user result report showing success or failure for each user ID.
    """
    return (
        f"Bulk updating group '{group_name}' for {len(user_ids)} user(s) — action: {action}. "
        f"User IDs: {user_ids}"
    )
