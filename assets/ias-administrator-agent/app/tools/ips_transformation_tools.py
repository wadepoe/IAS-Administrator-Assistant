"""
IPS Transformation Tools.

These tools call the IPS Job Management MCP server transformation endpoints.
All SAP API interactions go through MCP tools — no direct HTTP calls.
"""

import logging
from typing import Optional
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def get_transformation(system_id: str, system_type: Optional[str] = "source") -> str:
    """
    Retrieve the current transformation configuration for a provisioning source or target system.

    Useful for debugging provisioning failures — shows exactly how attributes are
    mapped between source and target systems.

    Args:
        system_id: The ID or name of the provisioning system in IPS.
        system_type: Either "source" or "target". Defaults to "source".

    Returns:
        The transformation JSON configuration including attribute mappings,
        conditions, and functions for the specified system.
    """
    return f"Retrieving {system_type} transformation for IPS system: {system_id}"


@tool
def update_transformation(
    system_id: str,
    transformation_json: str,
    system_type: Optional[str] = "source",
) -> str:
    """
    Update the transformation configuration for a provisioning source or target system.

    IMPORTANT: This is a write operation. The agent MUST:
    1. Show the admin a clear summary of the new transformation before confirming.
    2. Obtain explicit user confirmation before calling this tool.

    Args:
        system_id: The ID or name of the provisioning system in IPS.
        transformation_json: The full replacement transformation as a JSON string.
                             Must be a valid IPS transformation with 'user' array
                             and optionally 'group' and 'role' arrays.
        system_type: Either "source" or "target". Defaults to "source".

    Returns:
        Confirmation that the transformation was updated, or an error message
        if the update failed (e.g. validation error from IPS).
    """
    return (
        f"Updating {system_type} transformation for IPS system: {system_id}. "
        f"Transformation length: {len(transformation_json)} chars."
    )
