---
name: group-management
description: Instructions for assigning or removing IAS groups from individual users or a list of user IDs, including bulk operations with per-user result reporting.
---

# Group Management in SAP IAS

## When to Use This Skill

Load this skill when the user asks to:
- Assign a group to a user
- Remove a group from a user
- Assign or remove a group for multiple users at once

## Step 1: Validate the Group Exists

Before making any changes, verify the group exists using the IAS SCIM MCP tool:
`GET /scim/Groups?filter=displayName eq "{groupName}"`

- If the group is **not found**: abort the entire operation. Inform the user clearly: "Group '[groupName]' was not found in IAS. No changes were made." Do not proceed.
- If the group is found: note the group ID for use in subsequent calls.

## Step 2a: Single User — Assign or Remove Group

**This is a write operation — confirmation is MANDATORY.**

Flow:
1. Identify the user (search by name/email/ID if not already found)
2. Identify the group (Step 1)
3. Present a confirmation summary:
   - Assign: "I am about to add user [displayName] ([email]) to group [groupName]. Do you confirm?"
   - Remove: "I am about to remove user [displayName] ([email]) from group [groupName]. Do you confirm?"
4. Wait for explicit confirmation. If declined, cancel and confirm no action was taken.
5. On confirmation, use the IAS SCIM MCP tool to update group membership:
   - `PATCH /scim/Groups/{groupId}` with the appropriate member add/remove operation
6. Report success or relay the error message verbatim.

## Step 2b: Bulk — Assign or Remove Group for a List of User IDs

**This is a write operation — confirmation is MANDATORY.**

Flow:
1. Receive the list of user IDs and the group name
2. Validate the group exists (Step 1) — abort if not found, before any changes
3. Look up display names/emails for all user IDs (for the confirmation summary)
4. Present a confirmation summary listing all affected users:
   "I am about to [assign/remove] group [groupName] for the following [N] users:
   - [user1 displayName] ([email1])
   - [user2 displayName] ([email2])
   - ...
   Do you confirm?"
5. Wait for explicit confirmation. If declined, cancel all operations.
6. On confirmation, process each user **sequentially**:
   - For each user ID, call the IAS SCIM MCP tool to update group membership
   - Track each result: success or failure with error message
   - If one user fails, **continue** with the remaining users — do not abort the batch
7. After processing all users, report a full summary:
   - Number succeeded / failed
   - Per-user result (success or specific error)

## Error Handling

- **Group not found**: Abort entire operation before any changes. Inform user.
- **Individual user not found (bulk)**: Record as a failure for that user, continue with others.
- **API error for individual user (bulk)**: Relay error verbatim for that user, continue.
- **Permission denied**: Inform user the credentials may lack the required IAS admin scope for group management.
