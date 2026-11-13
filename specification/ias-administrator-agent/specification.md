# Specification: ias-administrator-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [ ] Read `product-requirements-document.md` and `intent.md` at the solution root for full context before starting
- [ ] Bootstrap agent code in `assets/ias-administrator-agent/` using the `sap-agent-bootstrap` skill (invoke from inside `assets/ias-administrator-agent/`, use copy commands — do NOT create files manually)
- [ ] Install dependencies and validate the agent starts and responds at `/.well-known/agent.json`

---

## MCP API Integration

> This agent integrates directly with two SAP Cloud Identity Services REST APIs.
> There are NO pre-existing MCP servers for these APIs — Path A (API spec + `mcp-translation-file` skill) applies.
> All API calls MUST go through generated MCP tools. Direct HTTP calls are strictly forbidden.

### IAS Identity Directory SCIM API

The IAS Identity Directory API is a SCIM-compliant REST API for user management.

**MCP API:** IAS Identity Directory SCIM API
**MCP tool scope:** read-write
**Resources in scope:** Users (search, get, update — password reset, unlock, group membership)

- [ ] Download the IAS Identity Directory SCIM API OpenAPI spec from the SAP Business Accelerator Hub and save it to `specification/ias-administrator-agent/api-specs/ias-identity-directory-api-spec.json`
  - URL: `https://api.sap.com/api/IAS_Identity_Directory/overview` (OpenAPI JSON)
  - If the spec cannot be downloaded automatically, note the manual step for the user in a comment
- [ ] Invoke the `mcp-translation-file` skill on `specification/ias-administrator-agent/api-specs/ias-identity-directory-api-spec.json` to generate the MCP translation card at `specification/ias-administrator-agent/mcps/ias-identity-directory/`
- [ ] Invoke the `setup-solution` skill to register the generated IAS Identity Directory MCP server asset (e.g. `ias-identity-directory-mcp-server`) in `solution.yaml` and create its `asset.yaml`
- [ ] Read the generated `asset.yaml` and copy the exact `ordId` value — use it verbatim in the agent's `asset.yaml` `requires` entry. Never invent or infer the ORD ID.

### IPS Job Management REST API

The IPS Job Management API allows triggering Read/Resync provisioning jobs and retrieving job logs.

**MCP API:** IPS Job Management REST API
**MCP tool scope:** read-write
**Resources in scope:** Jobs (trigger Read, trigger Resync), JobLogs (retrieve, list)

- [ ] Download the IPS Job Management REST API OpenAPI spec from the SAP Business Accelerator Hub and save it to `specification/ias-administrator-agent/api-specs/ips-job-management-api-spec.json`
  - URL: `https://api.sap.com/api/IPS_JobManagement/overview` (OpenAPI JSON)
  - If the spec cannot be downloaded automatically, note the manual step for the user in a comment
- [ ] Invoke the `mcp-translation-file` skill on `specification/ias-administrator-agent/api-specs/ips-job-management-api-spec.json` to generate the MCP translation card at `specification/ias-administrator-agent/mcps/ips-job-management/`
- [ ] Invoke the `setup-solution` skill to register the generated IPS Job Management MCP server asset (e.g. `ips-job-management-mcp-server`) in `solution.yaml` and create its `asset.yaml`
- [ ] Read the generated `asset.yaml` and copy the exact `ordId` value — use it verbatim in the agent's `asset.yaml` `requires` entry. Never invent or infer the ORD ID.

---

## Runtime Skills

> These operations involve sensitive multi-step flows with confirmation gates. Runtime skills are appropriate here.

- [ ] Create `assets/ias-administrator-agent/app/skills/user-management/SKILL.md` with:
  - `name: user-management`
  - `description: Step-by-step instructions for looking up users, viewing details, resetting passwords, and unlocking accounts in SAP IAS`
  - Body covering:
    - How to search for a user (by name, email, or user ID) using the IAS SCIM tool
    - How to retrieve and present user details (status, groups, attributes)
    - Password reset flow: identify user → confirm intent with explicit summary → execute → report result
    - Account unlock flow: identify user → confirm intent → execute → report result
    - Error handling: user not found, API errors, permission denied

- [ ] Create `assets/ias-administrator-agent/app/skills/group-management/SKILL.md` with:
  - `name: group-management`
  - `description: Instructions for assigning or removing IAS groups from individual users or a list of user IDs`
  - Body covering:
    - Single user group assignment: identify user → identify group → confirm intent (show user + group name) → execute → report result
    - Bulk group assignment: receive list of user IDs → validate group exists first → present confirmation summary ("Assign group X to N users: [list]") → on confirm, process each user sequentially → report per-user success/failure
    - Partial failure handling: if one user fails in bulk, continue with remaining users and report all outcomes at the end
    - Group not found: abort entire operation before any changes are made, inform user clearly

- [ ] Create `assets/ias-administrator-agent/app/skills/provisioning-management/SKILL.md` with:
  - `name: provisioning-management`
  - `description: Instructions for triggering IPS Read and Resync jobs and retrieving and summarising provisioning logs`
  - Body covering:
    - Trigger Read job: identify provisioning system → confirm intent → trigger via IPS API → report job ID and status
    - Trigger Resync job: identify provisioning system → confirm intent → trigger via IPS API → report job ID and status
    - Retrieve logs: call IPS job logs API → parse response → summarise in plain language (highlight errors, warnings, overall status, affected users)
    - Error handling: API unavailable, job not found, invalid system name

---

## Project-Specific Tasks

### System Prompt

- [ ] Open `assets/ias-administrator-agent/app/agent.py` and set the system prompt (in `get_system_prompt()` or equivalent) to include:
  - Role: "You are an IAS Administrator Assistant. You help IT helpdesk staff and IAM administrators manage users and provisioning in SAP Cloud Identity Services (IAS) and SAP Identity Provisioning (IPS)."
  - Capabilities: user search, view details, password reset, account unlock, group assignment/removal (individual and bulk), IPS job triggering (Read and Resync), IPS log retrieval and summarisation
  - Confirmation rule: "Before executing any write operation (password reset, account unlock, group assignment or removal, IPS job trigger), you MUST present a clear summary of what you are about to do and ask the user to confirm. Only proceed after receiving explicit confirmation. If the user declines, cancel the operation and confirm no action was taken."
  - Data integrity rule: "IMPORTANT: You MUST use MCP tools to retrieve live data. Never fabricate, guess, or invent user data, group names, job IDs, or log entries. Relay tool errors verbatim."
  - Page size rule: "When calling tools that support pagination, always set the page size parameter to a maximum of 100 items to prevent context overflow."
  - Skill loading: "For user management tasks (search, details, reset, unlock), load the `user-management` skill. For group assignment tasks, load the `group-management` skill. For provisioning job and log tasks, load the `provisioning-management` skill."

### Tool Implementation

- [ ] Implement tool `search_user`: accepts `query` (name, email, or user ID), calls the IAS SCIM MCP tool to search `/scim/Users`, returns display name, email, user ID, and account status
- [ ] Implement tool `get_user_details`: accepts `user_id`, calls the IAS SCIM MCP tool to retrieve full user profile including status, group memberships, and key attributes
- [ ] Implement tool `reset_user_password`: accepts `user_id`, calls the IAS SCIM MCP tool to trigger password reset; requires prior confirmation in the conversation flow (do not call without confirmation)
- [ ] Implement tool `unlock_user_account`: accepts `user_id`, calls the IAS SCIM MCP tool to unlock the account; requires prior confirmation in the conversation flow
- [ ] Implement tool `manage_user_group`: accepts `user_id`, `group_name`, and `action` (`assign` or `remove`), calls the IAS SCIM MCP tool to update group membership; requires prior confirmation
- [ ] Implement tool `bulk_manage_user_groups`: accepts `user_ids` (list of strings), `group_name`, and `action` (`assign` or `remove`); validates group exists first; processes each user sequentially; returns a per-user result report; requires prior confirmation with a summary of all affected users
- [ ] Implement tool `trigger_ips_job`: accepts `system_name` and `job_type` (`read` or `resync`), calls the IPS Job Management MCP tool to trigger the job; returns job ID and initial status; requires prior confirmation
- [ ] Implement tool `get_ips_logs`: accepts optional `system_name` and `limit` (default 20), calls the IPS Job Management MCP tool to retrieve recent job logs; summarises in plain language highlighting errors, warnings, and overall job outcomes

### MCP Tool Wiring

- [ ] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from the `mcp_tools` module (bootstrap-generated indirection layer). Never import directly from `sap_cloud_sdk.agentgateway`. Never create direct HTTP clients for IAS or IPS APIs.
- [ ] Add both MCP server dependencies to `asset.yaml` under `requires`:
  ```yaml
  requires:
    - name: ias-identity-directory-mcp-server
      kind: mcp-server
      ordId: <exact ordId from generated ias-identity-directory-mcp-server asset.yaml>
    - name: ips-job-management-mcp-server
      kind: mcp-server
      ordId: <exact ordId from generated ips-job-management-mcp-server asset.yaml>
  ```
- [ ] After MCP server assets are created and translation files generated, invoke the `mcp-mock-config` skill to generate `mcp-mock.json` at `assets/ias-administrator-agent/`

---

## Business Instrumentation

- [ ] Instrument all 7 milestones from the PRD with structured logging and OpenTelemetry spans in `agent.py`. Extract business logic from `stream()` into a plain async helper (e.g. `_run_agent()`) and instrument that — never use `with tracer.start_as_current_span(...)` inside an async generator.

  | Milestone | Log on achievement | Log on miss |
  |-----------|-------------------|-------------|
  | M1: User Search & Retrieval | `M1.achieved: user search completed successfully — user record returned from IAS` | `M1.missed: user search did not return a result or API call failed` |
  | M2: Password Reset | `M2.achieved: password reset executed successfully for target user` | `M2.missed: password reset was not completed — confirmation declined or API error` |
  | M3: Account Unlock | `M3.achieved: user account unlocked successfully` | `M3.missed: account unlock not completed — confirmation declined or API error` |
  | M4: IPS Job Trigger | `M4.achieved: IPS provisioning job triggered successfully — job ID returned` | `M4.missed: IPS job trigger not completed — confirmation declined or API error` |
  | M5: IPS Log Retrieval | `M5.achieved: IPS provisioning logs retrieved and summarised successfully` | `M5.missed: IPS log retrieval failed or no logs returned` |
  | M6b: Group Assignment (Individual) | `M6b.achieved: IAS group membership updated successfully for target user` | `M6b.missed: group assignment or removal not completed — confirmation declined, group not found, or API error` |
  | M6c: Group Assignment (Bulk) | `M6c.achieved: bulk IAS group operation completed — per-user results reported` | `M6c.missed: bulk group operation not completed — confirmation declined, group not found, or all users failed` |

- [ ] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## Testing

- [ ] Ensure `conftest.py` only sets `IBD_TESTING=true` — the fixture monkey-patches `mcp_tools.get_mcp_tools` using `mcp-mock.json`
- [ ] Write unit tests in `assets/ias-administrator-agent/tests/` — one per tool:
  - `test_search_user.py` — mock IAS SCIM MCP tool, assert correct query and returned fields
  - `test_get_user_details.py` — mock IAS SCIM MCP tool, assert full profile fields returned
  - `test_reset_user_password.py` — mock IAS SCIM MCP tool, assert password reset call is made with correct user ID
  - `test_unlock_user_account.py` — mock IAS SCIM MCP tool, assert unlock call is made with correct user ID
  - `test_manage_user_group.py` — mock IAS SCIM MCP tool, assert assign and remove actions both work correctly
  - `test_bulk_manage_user_groups.py` — mock IAS SCIM MCP tool with partial failure scenario, assert per-user results are reported and processing continues after individual failures
  - `test_trigger_ips_job.py` — mock IPS Job Management MCP tool, assert both `read` and `resync` job types are handled, job ID returned
  - `test_get_ips_logs.py` — mock IPS Job Management MCP tool, assert logs are fetched and a plain-language summary is returned
- [ ] Write one integration test in `assets/ias-administrator-agent/tests/test_integration.py` — end-to-end flow: simulate a user asking to reset a password, mock LLM and MCP tools, assert the confirmation prompt is issued and, on confirmation, the reset tool is called
- [ ] Run `pytest` from `assets/ias-administrator-agent/` (no args) — fix any failures before proceeding
- [ ] Verify coverage ≥ 70%; add targeted tests if below threshold
- [ ] Run `pytest` again (no args) to produce final `test_report.json`
- [ ] Verify `test_report.json` exists in `assets/ias-administrator-agent/`

---

## Validation Checklist

```bash
# Instrumentation
grep -r "M[0-9]\.achieved" assets/ias-administrator-agent/app/     # must return results

# Test report
ls assets/ias-administrator-agent/test_report.json                  # must exist
```
