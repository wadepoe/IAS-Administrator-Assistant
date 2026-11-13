---
name: user-management
description: Step-by-step instructions for looking up users, viewing details, resetting passwords, and unlocking accounts in SAP IAS via MCP tools.
---

# User Management in SAP IAS

## When to Use This Skill

Load this skill when the user asks to:
- Find, look up, or search for a user
- View user details, status, groups, or attributes
- Reset a user's password
- Unlock a locked user account

## Step 1: Search for a User

Use the IAS SCIM MCP tool to search `/scim/Users`.

**Parameters:**
- Provide `filter` parameter using SCIM syntax, e.g.:
  - By email: `filter=emails.value eq "john.doe@company.com"`
  - By display name: `filter=displayName co "John Doe"`
  - By user ID: `filter=id eq "abc123"`

**Present to user:**
- Display name
- Email address
- User ID
- Account status (active/locked/disabled)

If no results are found, inform the user clearly and suggest checking the search term spelling.

## Step 2: View Full User Details

Use the IAS SCIM MCP tool to retrieve a user by ID: `GET /scim/Users/{userId}`.

**Present to user:**
- Display name, email, user ID
- Account status (active, locked, disabled)
- Group memberships (list all group names)
- Key attributes (e.g. userName, phoneNumbers, addresses if present)

## Step 3: Reset User Password

**This is a write operation — confirmation is MANDATORY.**

Flow:
1. Identify the user (run Step 1 first if needed)
2. Present a confirmation summary: "I am about to reset the password for [display name] ([email], ID: [userId]). This will force them to set a new password on next login. Do you confirm?"
3. Wait for explicit confirmation. If user declines, cancel and confirm no action was taken.
4. On confirmation, call the IAS password reset MCP tool: `POST /service/users/{userId}/passwordReset` or equivalent endpoint.
5. Report success or relay the error message verbatim if the call fails.

## Step 4: Unlock a Locked User Account

**This is a write operation — confirmation is MANDATORY.**

Flow:
1. Identify the user (run Step 1 first if needed)
2. Verify the account is actually locked (check status from Step 2)
3. Present a confirmation summary: "I am about to unlock the account for [display name] ([email], ID: [userId]). Do you confirm?"
4. Wait for explicit confirmation. If user declines, cancel.
5. On confirmation, call the IAS unlock MCP tool: `PATCH /scim/Users/{userId}` with `active: true` or the platform's unlock endpoint.
6. Report success or relay the error message verbatim.

## Error Handling

- **User not found**: Inform the user, suggest trying a different search term or checking the tenant.
- **API error**: Relay the error message verbatim. Do not suggest workarounds unless asked.
- **Permission denied**: Inform the user the credentials may lack the required IAS admin scope.
