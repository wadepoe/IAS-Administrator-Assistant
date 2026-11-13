# Product Requirements Document (PRD)

**Title:** IAS Administrator Assistant
**Date:** 2026-11-13
**Owner:** IAM / IT Operations
**Solution Category:** AI Agent

---

## Product Purpose & Value Proposition

**Elevator Pitch:**
IT helpdesk staff and IAM administrators spend up to 15 minutes per request navigating the SAP IAS admin console to perform routine tasks. A conversational AI agent will handle those tasks through natural language, completing them in seconds — freeing administrators to focus on higher-value work.

**Business Need:**
SAP Identity Authentication Service (IAS) and Identity Provisioning (IPS) require administrators to log into a web console, navigate multiple screens, and execute tasks manually for every user request. This is time-consuming, error-prone, and diverts skilled administrators from strategic work. There is no programmatic, conversational interface for performing these operations today.

**Expected Value:**
Reduction in time-per-admin-task from ~15 minutes to a few seconds. Helpdesk staff can resolve user access issues without deep IAM expertise. IAM admins can trigger provisioning operations and investigate log issues conversationally without switching contexts.

**Product Objectives (Prioritized):**
1. Enable natural language user lookup, detail retrieval, password reset, and account unlock against IAS
2. Enable natural language triggering of IPS Read and Resync jobs and retrieval of provisioning logs
3. Ensure all sensitive operations require explicit confirmation before execution
4. Provide clear setup guidance for IAS/IPS OAuth2 API credentials as part of the solution

---

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to complete a user admin request | ~15 minutes | A few seconds | — | Identity & Access Management | user |

---

## User Profiles & Personas

### Primary Persona: Alex — IT Helpdesk Specialist

Alex is a 31-year-old IT helpdesk specialist who handles 10–20 access-related requests per day, including password resets, locked accounts, and user status checks. Alex is comfortable with IT tooling but is not an IAM expert — navigating the IAS admin console is slow and unfamiliar. Every request requires logging in, finding the right menu, and carefully performing the action without making mistakes. Alex needs a fast, reliable tool that removes the need to learn the IAS console for routine tasks.

**Pain points:** Time lost navigating the IAS UI, risk of making errors in an unfamiliar admin console, context-switching away from ticketing work.

### Secondary Persona: Maria — IAM / IAS Administrator

Maria is a 38-year-old identity and access management administrator responsible for maintaining the health of the IAS and IPS environments. She manages provisioning jobs, investigates sync failures, and ensures users are correctly set up. Maria is technically proficient but spends significant time on operational tasks that could be automated. She needs quick access to job status and log summaries without navigating multiple IPS screens.

**Pain points:** Manually triggering Read/Resync jobs, interpreting raw IPS provisioning logs, time lost on operational tasks instead of architecture and governance work.

---

## User Goals & Tasks

### For Alex (IT Helpdesk Specialist):

**Goals:**
- Resolve user access issues (locked accounts, forgotten passwords) within seconds of receiving a ticket
- Look up user details without needing IAM console access or expertise

**Key Tasks:**
- Search for a user by name, email, or user ID
- View user status, groups, and attributes
- Reset a user's password
- Unlock a locked user account

### For Maria (IAM / IAS Administrator):

**Goals:**
- Monitor and manage IPS provisioning jobs conversationally without navigating the IPS console
- Quickly identify and understand provisioning errors from log output

**Key Tasks:**
- Trigger an IPS Read job for a specific source system
- Trigger an IPS Resync job
- Retrieve and receive a plain-language summary of recent provisioning logs and any issues found

---

## Product Principles

1. **Natural language first:** Every operation must be expressible in plain language — no technical syntax or console knowledge required.
2. **Confirm before you act:** All write operations (password reset, account unlock, job trigger) require explicit user confirmation before execution.
3. **Transparency over magic:** The agent must clearly state what it is about to do, what it has done, and what it could not do — no silent failures.
4. **Least privilege by design:** The agent uses API credentials scoped only to the operations it needs — no broad admin tokens.
5. **Setup simplicity:** Credential configuration must be documented clearly enough that an administrator with no developer background can complete it.

---

## Business Context

**Current State:**
Administrators log into the SAP IAS admin console at `https://<tenant>.accounts.ondemand.com/admin` and manually perform each operation through the UI. For IPS, they navigate to the Identity Provisioning cockpit to manage jobs and view logs. Each task requires authentication, navigation, and manual execution — averaging 15 minutes per request.

**Strategic Alignment:**
This solution supports the organisation's goal of operational efficiency and reduces dependency on specialised IAM knowledge for routine tasks, enabling helpdesk staff to handle first-line identity requests independently.

**Success Criteria:**
See Business Metrics section above.

---

## Goals and Non-Goals

### Goals (In Scope)

- Conversational user lookup in IAS by name, email, or user ID
- Retrieval and display of user details (status, groups, attributes) from IAS
- Password reset for a named user via IAS REST API
- Account unlock for a named user via IAS REST API
- Assigning and removing IAS groups for a named user
- Triggering IPS Read and Resync provisioning jobs
- Retrieval and plain-language summarisation of IPS provisioning logs
- Reading transformations on source and target provisioning systems for debugging
- Updating transformations on source and target provisioning systems
- Confirmation prompt before any write or job-triggering operation
- Setup guidance for IAS/IPS OAuth2 API credentials

### Non-Goals (Out of Scope)

- Creating, deactivating, or deleting users
- Managing corporate identity providers or SSO configurations
- Managing security policies or password policies
- Modifying application configurations in IAS
- Multi-tenant IAS management (single tenant only)

---

## Requirements

### Must-Have Requirements

**R1: User Search**

- **Problem to Solve:** Helpdesk staff need to find a user quickly without navigating the IAS admin console.
- **User Story:** As an IT helpdesk specialist, I need to search for a user by name, email, or user ID so that I can locate the right account in seconds.
- **Acceptance Criteria:**
  - Given I provide a name, email, or user ID, when I ask the agent to find the user, then the agent returns the user's display name, email, user ID, and account status.
  - Given the search returns no results, the agent clearly states that no user was found and suggests checking the search term.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 1

**R2: View User Details**

- **Problem to Solve:** Admins need to see user attributes, group memberships, and status without logging into IAS.
- **User Story:** As an IT helpdesk specialist, I need to view a user's full details — including status, groups, and key attributes — so that I can assess their account state and answer questions accurately.
- **Acceptance Criteria:**
  - Given a valid user is identified, when I ask for their details, then the agent returns status, assigned groups, email, and any relevant attributes.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 2

**R3: Password Reset**

- **Problem to Solve:** Helpdesk staff need to reset a user's password without accessing the IAS console.
- **User Story:** As an IT helpdesk specialist, I need to reset a user's password via the agent so that I can resolve access issues immediately without needing console access.
- **Acceptance Criteria:**
  - Given a user is identified, when I request a password reset, then the agent asks for confirmation before executing.
  - Given confirmation is received, the agent calls the IAS password reset API and confirms success or reports the error.
- **Maps to Objective:** Objectives 1 & 3
- **Priority Rank:** 3

**R4: Unlock User Account**

- **Problem to Solve:** Locked accounts are a frequent helpdesk request that currently requires IAS console access.
- **User Story:** As an IT helpdesk specialist, I need to unlock a locked user account so that the user can regain access without waiting for an IAM admin.
- **Acceptance Criteria:**
  - Given a locked user is identified, when I request an unlock, then the agent asks for confirmation before executing.
  - Given confirmation is received, the agent calls the IAS unlock API and confirms success or reports the error.
- **Maps to Objective:** Objectives 1 & 3
- **Priority Rank:** 4

**R5: Trigger IPS Provisioning Jobs**

- **Problem to Solve:** IAM admins need to trigger Read and Resync jobs without navigating the IPS cockpit.
- **User Story:** As an IAM administrator, I need to trigger an IPS Read or Resync job via the agent so that I can initiate provisioning operations quickly from any interface.
- **Acceptance Criteria:**
  - Given I name a provisioning system, when I ask to trigger a Read or Resync job, then the agent asks for confirmation and then triggers the job via the IPS REST API.
  - The agent reports the job ID and initial status after triggering.
- **Maps to Objective:** Objective 2 & 3
- **Priority Rank:** 5

**R6: Read and Summarise IPS Provisioning Logs**

- **Problem to Solve:** Raw IPS log output is verbose and difficult to interpret quickly; admins need a plain-language summary of errors and warnings.
- **User Story:** As an IAM administrator, I need the agent to retrieve and summarise recent IPS provisioning logs so that I can identify issues without manually parsing raw log data.
- **Acceptance Criteria:**
  - Given I ask for provisioning logs, the agent retrieves recent job logs from the IPS REST API.
  - The agent returns a plain-language summary highlighting errors, warnings, and overall job status.
- **Maps to Objective:** Objective 2
- **Priority Rank:** 6

**R7: Group Assignment — Individual User**

- **Problem to Solve:** Admins need to assign or remove an IAS group for a single user without navigating the IAS admin console.
- **User Story:** As an IAM administrator or IT helpdesk specialist, I need to assign or remove an IAS group from a specific user so that I can manage their access rights conversationally without console access.
- **Acceptance Criteria:**
  - Given a user and group name are provided, when I ask the agent to assign or remove the group, then the agent asks for confirmation before executing.
  - Given confirmation is received, the agent calls the IAS SCIM API to update the user's group membership and confirms the change.
  - Given the group does not exist, the agent clearly states that the group was not found and takes no action.
- **Maps to Objective:** Objectives 1 & 3
- **Priority Rank:** 5

**R7b: Group Assignment — Bulk (List of User IDs)**

- **Problem to Solve:** Admins often need to apply the same group change across multiple users at once, which is extremely time-consuming when done one by one in the IAS console.
- **User Story:** As an IAM administrator, I need to assign or remove an IAS group for a list of user IDs in a single request so that I can make bulk access changes efficiently without repeating the operation per user.
- **Acceptance Criteria:**
  - Given a list of user IDs and a group name are provided, when I ask the agent to assign or remove the group for all of them, then the agent presents a summary (e.g. "Assign group X to 5 users: [list]") and asks for confirmation before executing.
  - Given confirmation is received, the agent processes each user in sequence via the IAS SCIM API and reports a per-user success or failure result.
  - Given one or more users are not found or the operation fails for a subset, the agent reports which succeeded and which failed without stopping the full batch.
  - Given the group does not exist, the agent aborts the entire batch and informs the user before any changes are made.
- **Maps to Objective:** Objectives 1 & 3
- **Priority Rank:** 6

**R9: Read IPS Transformations**

- **Problem to Solve:** When debugging provisioning failures, admins need to inspect the transformation logic applied to source and target systems without navigating the IPS console.
- **User Story:** As an IAM administrator, I need to read the current transformation configuration for a given source or target provisioning system so that I can understand how attributes are mapped and identify the root cause of provisioning errors.
- **Acceptance Criteria:**
  - Given I name a provisioning system and specify source or target, when I ask to view its transformation, then the agent retrieves and displays the transformation JSON from the IPS API.
  - The agent presents the transformation in a readable, structured format and highlights any sections relevant to a reported error if context is available.
  - Read-only — no confirmation required.
- **Maps to Objective:** Objective 2
- **Priority Rank:** 7

**R10: Update IPS Transformations**

- **Problem to Solve:** Admins need to fix or tune transformation logic on source or target provisioning systems without navigating the IPS console.
- **User Story:** As an IAM administrator, I need to update the transformation configuration for a given source or target provisioning system so that I can fix attribute mapping errors or adjust provisioning behaviour conversationally.
- **Acceptance Criteria:**
  - Given I provide a system name, system type (source or target), and the updated transformation JSON, when I ask the agent to apply it, then the agent presents a summary of the change and asks for confirmation.
  - Given confirmation is received, the agent calls the IPS Transformations API to apply the update and confirms success or reports the error.
  - Given the update fails validation, the agent reports the specific error returned by the API without making any partial changes.
- **Maps to Objective:** Objectives 2 & 3
- **Priority Rank:** 8

**R8: Intent Confirmation for Write Operations**

- **Problem to Solve:** Password resets, account unlocks, and job triggers are sensitive operations that must not be performed by accident.
- **User Story:** As any administrator, I need the agent to confirm my intent before performing any write or job-triggering operation so that I do not accidentally execute the wrong action.
- **Acceptance Criteria:**
  - Given any write or trigger operation is requested, the agent presents a clear confirmation prompt stating exactly what it will do before proceeding.
  - Given I decline, the agent cancels the operation and confirms no action was taken.
- **Maps to Objective:** Objective 3
- **Priority Rank:** 1 (cross-cutting, applies to R3, R4, R5, R6, R7)

---

## Solution Architecture

**Architecture Overview:**
A single Python AI agent built on the A2A protocol, deployed on SAP BTP. The agent connects directly to the IAS Identity Directory SCIM API and the IPS Job Management REST API via OAuth2 credentials. No intermediate workflow layer is required — all operations are driven by natural language reasoning within the agent.

**Key Components:**

- **IAS Administrator Agent** — Python-based conversational AI agent (A2A protocol); handles intent recognition, tool selection, confirmation prompts, and response formatting
- **IAS Identity Directory SCIM API** — REST API for user search, attribute retrieval, password reset, and account unlock
- **IPS Job Management REST API** — REST API for triggering Read/Resync jobs and retrieving job logs
- **OAuth2 Credential Store** — Securely holds the IAS/IPS client ID and secret used by the agent

**Integration Points:**

- IAS SCIM API (`/scim/Users`): read user data, reset password, unlock account — read and write
- IPS Jobs API (`/ips/service/jobs`): trigger Read/Resync, retrieve job logs — read and write

**Deployment Environments:**

- Development: connected to IAS/IPS sandbox or dev tenant
- Production: connected to production IAS/IPS tenant with production-scoped OAuth2 credentials

---

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
The agent is designed with clearly separated tool functions, each mapping to a single IAS or IPS operation. This allows new tools (e.g., user creation, group assignment, login method management) to be added without modifying the core agent logic. Extension points are documented in the agent's skill resources.

**Business Step Instrumentation:**
All significant business operations are instrumented with structured log statements following the pattern:
`[MILESTONE_ID].[achieved|missed]: [description]`

This enables observability, debugging, and monitoring in production.

---

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent with human-in-the-loop confirmation for write operations

**Actions the system performs without human approval:**
- Searching for users
- Retrieving user details and attributes
- Retrieving IPS provisioning logs

**Actions that require human review or approval:**
- Password reset
- Account unlock
- Triggering IPS Read or Resync jobs

**Model or engine used:** SAP Generative AI Hub (via SAP BTP AI Core)

**Knowledge & data sources accessed:**
- IAS Identity Directory: user records, account status, group memberships
- IPS Job Management: job definitions, job run history, provisioning logs

**Tools or connectors invoked:**
- `search_user` — searches IAS for a user by name, email, or ID (read-only)
- `get_user_details` — retrieves full user profile from IAS (read-only)
- `reset_user_password` — triggers password reset in IAS (write, confirmation required)
- `unlock_user_account` — unlocks a user account in IAS (write, confirmation required)
- `manage_user_group` — assigns or removes an IAS group from a single user (write, confirmation required)
- `bulk_manage_user_groups` — assigns or removes an IAS group from a list of user IDs in one operation; reports per-user results (write, confirmation required, batch-safe)
- `trigger_ips_job` — triggers a Read or Resync job in IPS (write, confirmation required)
- `get_ips_logs` — retrieves and summarises recent IPS provisioning logs (read-only)
- `get_transformation` — retrieves the transformation JSON for a source or target provisioning system (read-only)
- `update_transformation` — updates the transformation JSON for a source or target provisioning system (write, confirmation required)

**Guardrails & fail-safes:**
- All write operations require explicit user confirmation before execution
- Transformation updates display a clear diff-style summary before confirmation so the admin understands exactly what will change
- The agent never modifies user groups, roles, or application assignments
- On API error, the agent reports the failure clearly and suggests next steps
- The agent does not store or log personally identifiable information beyond what is needed to complete the request
- If the IAS/IPS API is unreachable, the agent informs the user and does not retry silently

---

### Configuration & Data

**Configuration Scope:**
One-time setup of an OAuth2 client in SAP IAS with appropriate admin API scopes, and configuration of the client credentials in the agent's deployment environment. Step-by-step setup documentation is included in the solution.

**Organisational & Master Data:**
No master data migration required. The agent reads live data from IAS/IPS at request time.

---

## Governance, Risk & Compliance

**Data Handling:**
- User data retrieved from IAS is displayed only in the active conversation and is not persisted by the agent
- Credentials (client ID/secret) are stored as environment secrets, never in code or logs
- The agent must not log user email addresses, display names, or other PII in application logs

**Compliance Frameworks:**
- GDPR: user data is not stored; only transient in-session display
- IAS API scopes must follow least-privilege principle

**Approval Flows:**
- Password reset and account unlock require in-session confirmation by the requesting administrator

---

## Milestones

### M1: User Search & Retrieval

- **Description:** The agent can locate a user in IAS by name, email, or user ID and return their basic profile.
- **Achieved when:** A natural language search request returns the correct user record from the IAS SCIM API.
- **Log on achievement:** `M1.achieved: user search completed successfully — user record returned from IAS`
- **Log on miss:** `M1.missed: user search did not return a result or API call failed`

### M2: Password Reset

- **Description:** The agent can reset a user's password in IAS following user confirmation.
- **Achieved when:** A password reset is confirmed by the user and executed successfully via the IAS REST API.
- **Log on achievement:** `M2.achieved: password reset executed successfully for target user`
- **Log on miss:** `M2.missed: password reset was not completed — confirmation declined or API error`

### M3: Account Unlock

- **Description:** The agent can unlock a locked user account in IAS following user confirmation.
- **Achieved when:** An unlock operation is confirmed and executed successfully via the IAS REST API.
- **Log on achievement:** `M3.achieved: user account unlocked successfully`
- **Log on miss:** `M3.missed: account unlock not completed — confirmation declined or API error`

### M4: IPS Job Trigger

- **Description:** The agent can trigger a Read or Resync provisioning job in IPS following user confirmation.
- **Achieved when:** A job trigger request is confirmed and the IPS API returns a job ID with accepted status.
- **Log on achievement:** `M4.achieved: IPS provisioning job triggered successfully — job ID returned`
- **Log on miss:** `M4.missed: IPS job trigger not completed — confirmation declined or API error`

### M5: IPS Log Retrieval & Summarisation

- **Description:** The agent can retrieve IPS provisioning logs and return a plain-language summary of issues.
- **Achieved when:** The agent fetches job logs from the IPS REST API and generates a readable summary.
- **Log on achievement:** `M5.achieved: IPS provisioning logs retrieved and summarised successfully`
- **Log on miss:** `M5.missed: IPS log retrieval failed or no logs returned`

### M6: API Credentials Configured

- **Description:** IAS and IPS OAuth2 credentials are created, scoped, and available to the agent.
- **Achieved when:** The agent successfully authenticates against both IAS and IPS APIs using configured credentials.
- **Log on achievement:** `M6.achieved: IAS and IPS API credentials validated successfully`
- **Log on miss:** `M6.missed: credential validation failed — check client ID, secret, or API scopes`

### M6b: Group Assignment — Individual User

- **Description:** The agent can assign or remove an IAS group from a single user following confirmation.
- **Achieved when:** A group assignment or removal is confirmed and executed successfully via the IAS SCIM API for one user.
- **Log on achievement:** `M6b.achieved: IAS group membership updated successfully for target user`
- **Log on miss:** `M6b.missed: group assignment or removal not completed — confirmation declined, group not found, or API error`

### M6c: Group Assignment — Bulk (List of User IDs)

- **Description:** The agent can assign or remove an IAS group for a list of user IDs in a single operation, reporting per-user outcomes.
- **Achieved when:** A bulk group operation is confirmed and the agent processes all provided user IDs, returning a success/failure report.
- **Log on achievement:** `M6c.achieved: bulk IAS group operation completed — per-user results reported`
- **Log on miss:** `M6c.missed: bulk group operation not completed — confirmation declined, group not found, or all users failed`

### M8: Transformation Read

- **Description:** The agent can retrieve the transformation configuration for a source or target IPS system.
- **Achieved when:** A natural language request returns the transformation JSON from the IPS API.
- **Log on achievement:** `M8.achieved: IPS transformation retrieved successfully for system`
- **Log on miss:** `M8.missed: transformation retrieval failed — system not found or API error`

### M9: Transformation Update

- **Description:** The agent can update the transformation configuration for a source or target IPS system following confirmation.
- **Achieved when:** An update is confirmed and applied successfully via the IPS Transformations API.
- **Log on achievement:** `M9.achieved: IPS transformation updated successfully for system`
- **Log on miss:** `M9.missed: transformation update not completed — confirmation declined, validation error, or API error`

### M7: Agent Deployed and Available

- **Description:** The agent is deployed on SAP BTP and accessible to helpdesk and IAM admin users.
- **Achieved when:** The agent responds to a test query in the production environment.
- **Log on achievement:** `M7.achieved: IAS Administrator Assistant deployed and responding in production`
- **Log on miss:** `M7.missed: deployment failed or agent not reachable in production environment`

---

## Risks, Assumptions, and Dependencies

### Risks

- **IAS API scope misconfiguration:** If the OAuth2 client lacks the required IAS admin scopes, write operations will fail. Mitigation: clear setup documentation with exact scopes required.
- **Sensitive operation misuse:** Password reset and unlock are privileged actions. Without additional access control, any user of the agent could perform them. Mitigation: confirmation prompts; consider restricting agent access to a named admin group in future.
- **IPS API availability:** If the IPS REST API is unavailable or rate-limited, job trigger and log retrieval will fail. Mitigation: graceful error handling and clear user messaging.

### Assumptions

- The organisation has an active SAP Cloud Identity Services (IAS) tenant.
- IAS REST API (SCIM) is enabled and accessible for programmatic access.
- IPS is configured and provisioning jobs are already defined.
- An administrator with IAS admin access is available to create the OAuth2 API client during setup.

### Dependencies

- SAP Identity Authentication Service (IAS) — production tenant
- SAP Identity Provisioning (IPS) — production instance
- SAP BTP AI Core — for LLM inference
- OAuth2 API credentials with appropriate IAS/IPS admin scopes

---

## Appendix

### Glossary

- **IAS** — SAP Identity Authentication Service: the central service for user authentication in SAP Cloud Identity Services
- **IPS** — SAP Identity Provisioning Service: manages automated provisioning and synchronisation of user identities across systems
- **SCIM** — System for Cross-domain Identity Management: the REST API standard used by IAS for user management
- **A2A** — Agent-to-Agent protocol: the communication standard used by SAP AI agents in Joule Studio
- **OAuth2** — Open authorisation framework used to authenticate the agent's API calls to IAS/IPS
- **Read Job** — An IPS job that reads user data from a source system without making changes to the target
- **Resync Job** — An IPS job that re-synchronises all user records between source and target systems

### References

- [SAP Cloud Identity Services — Identity Directory API](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/manage-users)
- [SAP Identity Provisioning REST API](https://help.sap.com/docs/identity-provisioning/identity-provisioning/manage-provisioning-job-via-api)
- [SAP IAS OAuth2 API Authentication](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-oauth-2-0-service-account)
