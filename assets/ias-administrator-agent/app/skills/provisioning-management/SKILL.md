---
name: provisioning-management
description: Instructions for triggering IPS Read and Resync provisioning jobs and retrieving and summarising IPS provisioning logs in plain language.
---

# Provisioning Management in SAP IPS

## When to Use This Skill

Load this skill when the user asks to:
- Trigger a Read or Resync provisioning job
- Check provisioning job status
- View or get a summary of provisioning logs
- Investigate provisioning errors or warnings

## Step 1: Trigger an IPS Read Job

**This is a write operation — confirmation is MANDATORY.**

Flow:
1. Identify the provisioning system name (source system) from the user's request
2. Present a confirmation summary: "I am about to trigger a Read job for the provisioning system '[systemName]'. This will read users from the source system. Do you confirm?"
3. Wait for explicit confirmation. If declined, cancel and confirm no action was taken.
4. On confirmation, call the IPS Job Management MCP tool: `POST /ips/service/systems/{systemName}/jobs/read` or equivalent.
5. Report the returned job ID and initial status.

## Step 2: Trigger an IPS Resync Job

**This is a write operation — confirmation is MANDATORY.**

Flow:
1. Identify the provisioning system name from the user's request
2. Present a confirmation summary: "I am about to trigger a Resync job for the provisioning system '[systemName]'. This will re-synchronise all users between source and target. Do you confirm?"
3. Wait for explicit confirmation. If declined, cancel.
4. On confirmation, call the IPS Job Management MCP tool: `POST /ips/service/systems/{systemName}/jobs/resync` or equivalent.
5. Report the returned job ID and initial status.

## Step 3: Retrieve and Summarise Provisioning Logs

Flow:
1. Optionally filter by system name if the user specified one
2. Call the IPS Job Logs MCP tool to retrieve recent job run logs: `GET /ips/service/systems/{systemName}/logs` or `GET /ips/service/logs`
3. Set limit to 20 (or as requested by user, max 100)
4. Parse the response and produce a plain-language summary:
   - Overall status: How many jobs completed successfully, how many had errors/warnings
   - Highlight any errors: List error messages with affected entity details if available
   - Highlight any warnings: List warning messages
   - Total entities processed, created, updated, deleted (if available in the log)
5. Present the summary first, then offer to show raw details if the user asks.

## Step 4: Read a Transformation (for Debugging)

Flow:
1. Identify the system name and whether it is a source or target system
2. Call the IPS Transformation MCP tool: `GET /ips/service/systems/{systemId}/transformations?systemType=source|target`
3. Present the transformation JSON in a readable, structured format
4. If the user has described a provisioning error, highlight the attribute mapping(s) most likely related to the issue (look for the attribute name in `sourcePath` or `targetPath` entries)
5. Read-only — no confirmation required

## Step 5: Update a Transformation

**This is a write operation — confirmation is MANDATORY.**

Flow:
1. Identify the system name and system type (source or target)
2. Optionally read the current transformation first (Step 4) so the admin can review it
3. Receive the updated transformation JSON from the admin
4. Present a summary of the change: "I am about to replace the [source/target] transformation for system '[systemName]'. The new transformation has [N] user mappings and [M] group mappings. Do you confirm?"
5. Wait for explicit confirmation. If declined, cancel and confirm no action was taken.
6. On confirmation, call the IPS Transformation MCP tool: `PUT /ips/service/systems/{systemId}/transformations?systemType=source|target`
7. Report success or relay the exact error message from IPS (e.g. validation errors are common and contain specific field details)

## Error Handling

- **System not found**: Inform the user the system name may be incorrect. Suggest listing available systems if the API supports it.
- **API unavailable or timeout**: Relay the error verbatim. Inform the user the IPS service may be temporarily unavailable.
- **No logs found**: Inform the user no recent job logs were found for the specified system.
- **Permission denied**: Inform user the credentials may lack the required IPS admin scope.
