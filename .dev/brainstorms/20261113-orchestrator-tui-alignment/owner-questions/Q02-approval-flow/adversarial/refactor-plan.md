# Refactoring Plan

## Overview

- Base: Variant 2 (proposal B)
- Incorporated: Variant 3 (proposal C) changes 1 to 4; Variant 1 (proposal A) change 5; debate findings changes 6 to 12
- Planned changes: 12; rejected: 5
- Overall risk: Low to Medium (additive, plus three corrections of base claims)
- Merged output path: `../merged-proposal.md` (in the Q02-approval-flow folder)

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Read-only stage-status verb for GitHub approvals | C Design item 4, U-008 | Design item 4; build table | insert | C-003 won 3 of 3; checks run as code, not as LLM prose | Low |
| 2 | New stage predicates, not plain reuse | V2 concession 4, V3 concession 3 | Design item 4; GitHub flow step 3 | replace "reusing the watcher's `approval_of` and `unchanged_since` rules" | `unchanged_since` skips own-login comments (`predicates.py` 253 to 255) and the plan reply is posted as that login; `approval_of` orders against a trigger label | Medium |
| 3 | Label removal is the revocation signal; a Status move back is shown, reported, never acted on alone | C F5 row; C-008 | F5 row; Design | replace trigger | C-008 won 2 of 3; Status actor is not read by any code | Low |
| 4 | Label event id stored as evidence; key stays (issue, stage, plan version); public "approved, starting" marker on the issue after the row and before the instruction (non-blocking if GitHub is down; retried at each wake); on start-up a marker without a row is treated as an existing row | C U-004; V3 concessions 4, 5 | Design items 2 and 4; F1, F2 rows | insert | Prevents a lost ledger or a remove-and-reapply from restarting finished work | Medium |
| 5 | Build the helper on the watcher's existing lock and fsync store code (`record.py` file lock, directory fsync) | A Design item 1; V1 strength 1 | Design item 2; build table | insert | Mechanism is built and tested; no new locking code | Low |
| 6 | Correct the coordinator-down claim | V2 concession 2 | F2 row; How an approval flows | replace | An approval typed in the coordinator session cannot be made while it is down; only GitHub approvals (as state) and a future TUI message wait | Low |
| 7 | Delivery to the agent: resolve the "never answer a person prompt" veto | V2 concession 3; A-002 | Design item 3; build table | replace | `WORKER-CONTRACT.md` line 136; first release needs a written, narrow exception for exactly one line per approval row; the durable route is the supervised-worker redesign (SW-13) | Medium |
| 8 | Plan version defined over named files by the helper and printed in the plan reply | A-003 responses | Design item 3 | insert | All three QUALIFY A-003 | Low |
| 9 | Dead or missing agent session: row stays "recorded, not delivered", reported to the person; never relaunched automatically | A-006 responses | New F row note; Design | insert | All three QUALIFY A-006 | Low |
| 10 | Duplicate approval from the other channel gets a short reply on the issue ("already approved in Orca at <time>, row <id>") and no action | Owner's race scenario; C-007 | F1 row | insert | Turns the owner's double-start case into a visible no-op | Low |
| 11 | GitHub channel trust: approvals accepted only from approver account ids that are not the host's `gh` login, else the GitHub channel stays off until FU-6 or until the owner accepts the forgery risk in writing | V2 neutral recommendation; F8 | F8 row; Who may approve | replace | All three concede single-login forgery | Medium |
| 12 | Coordinator scope and grants stated as preconditions (A-001, A-005) and the liveness trade-off (C-005) left to the owner | A-001, A-005, C-005 | What stays unresolved | append | Unanimous "none/owner" | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001 | A: three actuators including the agent | Lost 3 of 3 neutral recommendations; self-approval unsolved |
| X-001 | A: watcher posts comments and types into sessions | Reverses D2 and NG-2 |
| C-004 | A: keep the bare `approved` in the agent session | Self-approval route for a permission-free session |
| C-006, X-002 | C: Orca approvals written through to GitHub and acted on only after read-back | Contradicts C's own account requirement; makes Orca hostage to GitHub lag |
| C-005 | A: watcher starts GitHub-approved stages while the coordinator is down | Requires the watcher to become an actuator; left as an owner decision rather than merged |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 2 | Medium | An edited plan reply goes undetected | The agent's hash check still protects the plan file |
| 4 | Medium | Marker write fails | Row is still the guard; marker retried |
| 7 | Medium | Exception too broad | Narrow to one line per row, logged |
| 11 | Medium | GitHub channel unusable on one login | Orca channel still works |

## Review Status

Auto-approved (non-interactive), 2026-11-14.
