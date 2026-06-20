# Stage 4 (agent-mail pilot) — Operational Teardown Checklist (L2 stub)

**Status:** STUB — Stage 4 is OUT OF SCOPE for this task (TASK-RF-SPRINTCLI-WIRE-DEAD).
This checklist exists so the out-of-scope Stage-4 work inherits an accurate
operational note: the data rollback is lossless (the `FileHandoffStore` remained
the source of truth throughout the pilot), but the **operational** teardown is NOT
"free" — it requires the four steps below.

## Rollback ≠ teardown

- **Data rollback (lossless):** flip `SprintConfig.handoff_store` from `"mail"` back
  to `"file"`. No handoff records are lost because `MailHandoffStore` runs as a
  shadow/dual-write with the file store as the authoritative oracle the whole pilot.
- **Operational teardown (not free):** the sidecar + MCP wiring + credentials must be
  decommissioned explicitly. The four steps:

## Teardown steps

1. **Stop the sidecar.** Shut down the FastMCP mail sidecar process running in the
   controlled isolation settings dir; confirm it is no longer bound/listening.
2. **Remove per-subprocess MCP config injection.** Strip the mail MCP server entry
   from the per-task `CLAUDE_SETTINGS_DIR` injection so spawned subprocesses no longer
   advertise/attempt the mail transport.
3. **Revoke the token.** Invalidate/rotate the auth token the sidecar + agents used,
   so a stale token cannot reach the mailbox after teardown.
4. **Archive the mailbox repo.** Archive (do not delete) the mailbox/commit-log repo
   for audit/forensics; freeze writes.

## Acceptance

Teardown is complete when: the sidecar is down, no per-subprocess MCP config references
the mail server, the token is revoked, the mailbox repo is archived, and a subsequent
sprint runs cleanly on `handoff_store="file"` with no mail-transport artifacts.
