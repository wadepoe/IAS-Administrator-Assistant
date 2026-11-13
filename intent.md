# IAS Administrator Assistant

AI-powered conversational assistant to help IT helpdesk staff and IAM administrators manage users and provisioning in SAP Cloud Identity Services (IAS/IPS).

## Business Challenge

IT helpdesk staff and IAM/IAS administrators currently spend approximately 15 minutes per request manually logging into SAP Identity Authentication Service (IAS) and performing user management tasks. The goal is to reduce this to a few seconds by providing a conversational AI assistant that can execute those tasks on the administrator's behalf via natural language.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to complete a user admin request | ~15 minutes | A few seconds | — | Identity & Access Management | user |

## Key Milestones

1. Agent can search and retrieve user details from IAS by name, email, or user ID
2. Agent can reset a user's password via IAS REST API
3. Agent can unlock a locked user account
4. Agent can assign or remove IAS groups for a user
5. Agent can trigger IPS Read and Resync provisioning jobs
6. Agent can read and summarise IPS provisioning logs for issues
7. IAS/IPS API credentials configured and connected to the agent
8. Agent deployed and available to helpdesk and IAM admin users

## Business Architecture (RBA)

### End-to-End Process

Governance (IT Management)

### Process Hierarchy

```
Governance (Level 1)
└── Manage Governance, Risk and Compliance (Level 2)
    └── Manage Identity and Access Governance (BPS-399)
        └── Manage authentication
        └── Manage identity
        └── Manage access governance and authorisations
```

### Summary

The challenge maps to "Manage Identity and Access Governance" (BPS-399) within the Governance E2E, covering identity management, authentication management, and access governance — all core capabilities of SAP Cloud Identity Services (IAS) and Identity Provisioning (IPS).

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|---|---|---|---|---|---|---|---|---|
| Search / look up users by name, email, or ID | SAP Cloud Identity Services (IAS) — Authentication Management (SC1579) | — | — | — | — | — | Yes | IAS Identity Directory REST API required; not pre-connected in catalog, custom integration needed |
| View user details (status, groups, attributes) | SAP Cloud Identity Services (IAS) — Authentication Management (SC1579) | — | — | — | — | — | Yes | IAS Identity Directory REST API; same integration as above |
| Reset user passwords | SAP Cloud Identity Services (IAS) — Authentication Management (SC1579) | — | — | — | — | — | Yes | IAS REST API (password reset endpoint); custom integration needed |
| Unlock user accounts | SAP Cloud Identity Services (IAS) — Authentication Management (SC1579) | — | — | — | — | — | Yes | IAS REST API (unlock endpoint); custom integration needed |
| Assign or remove IAS groups for a user | SAP Cloud Identity Services (IAS) — Authentication Management (SC1579) | — | — | — | — | — | Yes | IAS SCIM API (group membership update); custom integration needed |
| Trigger IPS Read / Resync provisioning jobs | Identity Provisioning (SC1575) | — | — | — | — | — | Yes | IPS REST API; custom integration needed; IPS API credentials required |
| Read and summarise IPS provisioning logs | Identity Provisioning (SC1575) | — | — | — | — | — | Yes | IPS Job Logs REST API; agent will parse and summarise log output |

### Key findings

- SAP Cloud Identity Services (IAS) and Identity Provisioning (IPS) are the standard SAP products covering all identified requirements.
- None of the IAS/IPS REST APIs are available as pre-connected catalog APIs or MCP servers in the current landscape — direct REST integration is required.
- IAS API credentials (client ID/secret via OAuth2) need to be set up as part of the project; guidance will be included in the solution.
- The assistant will use the IAS Identity Directory SCIM API and the IPS Job Management REST API.
- A Python AI agent (A2A protocol) is the right fit for this fully conversational, multi-step, reasoning-based use case.
- No n8n workflow is needed as there is no fixed orchestration — all flows are driven by natural language.

## Recommendations

### IAS / IPS Administrator AI Agent

#### Executive Summary

Conversational Python AI agent integrating directly with IAS and IPS REST APIs.

#### Recommended Solution

Build a Python-based conversational AI agent (A2A protocol) that integrates directly with the SAP Cloud Identity Services REST APIs (IAS Identity Directory API and IPS Job Management API). The agent accepts natural language requests from IT helpdesk staff and IAM admins and translates them into the appropriate API calls — user lookups, password resets, account unlocks, provisioning job triggers, and log retrieval.

#### Problem Statement

Administrators must manually log in to the IAS admin console and navigate multiple screens to perform routine tasks, taking ~15 minutes per request and diverting focus from higher-value work.

#### Affected User Roles

- IT Helpdesk Staff
- IAM / IAS Administrators

#### Important factors

##### Reduces manual effort through automation

The agent handles the full interaction with IAS/IPS APIs so the administrator only needs to describe what they want in plain language.

##### Requires IAS/IPS API credential setup

Since the IAS and IPS APIs are not pre-connected, the project must include guidance on creating an OAuth2 client in IAS and configuring credentials for the agent — a one-time setup step.

#### Potential risks

##### IAS API permissions and scope

The OAuth2 client used by the agent must have the appropriate IAS admin API scopes. Misconfigured permissions could prevent certain operations. Clear setup documentation will mitigate this.

##### Sensitive operations (password reset, unlock)

Password reset and account unlock are sensitive actions. The agent should confirm intent before executing destructive or access-modifying operations.

#### Recommended solution category

AI Agent

#### Intent fit
90%
