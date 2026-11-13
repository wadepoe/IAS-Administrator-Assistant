"""
IPS Job Management Tools.

These tools call the IPS Job Management MCP server.
All SAP API interactions go through MCP tools — no direct HTTP calls.
"""

import logging
from typing import Optional
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def trigger_ips_job(system_name: str, job_type: str) -> str:
    """
    Trigger a provisioning job in SAP Identity Provisioning (IPS).

    IMPORTANT: This is a write operation. The agent MUST obtain explicit user
    confirmation before calling this tool.

    Args:
        system_name: The name of the provisioning source system in IPS.
        job_type: Either "read" to trigger a Read job, or "resync" to trigger a Resync job.

    Returns:
        The job ID and initial status returned by IPS, or an error message.
    """
    return f"Triggering IPS {job_type} job for system: {system_name}"


@tool
def get_ips_logs(system_name: Optional[str] = None, limit: int = 20) -> str:
    """
    Retrieve and summarise recent IPS provisioning job logs.

    Args:
        system_name: Optional. Filter logs for a specific provisioning system.
                     If not provided, retrieves logs across all systems.
        limit: Maximum number of log entries to retrieve (default 20, max 100).

    Returns:
        A plain-language summary of recent provisioning job logs, highlighting
        errors, warnings, and overall job outcomes.
    """
    system_info = f"for system '{system_name}'" if system_name else "across all systems"
    return f"Retrieving up to {limit} IPS provisioning log entries {system_info}"
