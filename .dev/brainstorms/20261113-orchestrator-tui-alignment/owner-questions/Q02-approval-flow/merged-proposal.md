<!--
Provenance
- Produced by: merge-executor, adversarial pipeline step 5, 2026-11-14
- Base: adversarial/variant-2-original.md (proposal B, one actuator)
- Plan: adversarial/refactor-plan.md (12 planned changes, 5 rejected; none of the rejected changes is included)
- Incorporated sources: adversarial/variant-3-original.md (proposal C, changes 1 to 4), adversarial/variant-1-original.md (proposal A, change 5), adversarial/round1-advocate-V2.md and adversarial/round1-advocate-V3.md (concessions and assumption responses, changes 2, 4, 6 to 12), 00-state-machine-and-failure-modes.md (shared terms and F1 to F10)
- Per-change record: adversarial/merge-log.md
-->

# Merged proposal: one actuator (the coordinator) with GitHub label evidence

Nothing in this proposal is built. It is advice for the owner, written 2026-11-14.

Shared terms, the stage table (S0 to S7) and the failure modes (F1 to F10) are in `00-state-machine-and-failure-modes.md` in this folder.

<!-- Source: Base (V2) Design; item 2 modified by changes 4 and 5 (V3, V1); item 3 modified by changes 7, 8 and 9 (debate); item 4 modified by changes 1, 2, 3 and 4 (V3, debate); invariant updated to name the key, the write-ahead row, the sole creator and the agent's check -->
## Design

Exactly one process may send the instruction that moves the governed agent past the plan boundary or starts any later stage: the coordinator that owns that issue. Every approval, from any channel, is only an input the coordinator validates.

1. **The watcher stays a claim trigger and nothing more.** It keeps its built behaviour (claim-stage at-most-once, `claimed` is terminal) and gains no post-claim logic. It never messages the coordinator or the agent. The coordinator reads GitHub itself at each wake, so the watcher is out of the race entirely.
2. **One approval record, written ahead.** Before it instructs anything, the coordinator writes one row to its ledger: `approval-id | issue | stage | plan sha256 | channel | approver | evidence (label event id, Orca message id or typed line) | state (recorded, instructed, acked, revoked) | time`, through a small CLI helper that takes a per-issue lock and refuses a second row for the same (issue, stage, plan version).
   - **Key and evidence.** For a GitHub approval the label event id is stored in the row as evidence, but the key stays (issue, stage, plan version). A label that is removed and applied again gets a new event id, yet it finds the same row, so it cannot restart finished work.
   - **Built on the watcher's store code.** The helper reuses the watcher's existing lock and fsync code in `src/superclaude/cli/issue_watch/record.py`: its exclusive non-blocking `fcntl.flock` file lock (line 403) and its state-directory fsync (`_fsync_dir`, lines 310 to 313). No new locking code is written. Because the lock is non-blocking, a second concurrent call fails at once rather than waiting.
   - **Lost ledger.** On start-up, an "approved, starting" marker on the issue (item 4) that has no matching row is treated as an existing row, so a lost or fresh ledger does not restart finished work.
3. **The agent obeys only that record.** The launch prompt changes. Today it says "A human approves by replying `approved` in this session or by running the printed implement command." Under this proposal the agent continues only on a line `approved <approval-id> plan-sha256=<hex>`, recomputes the plan version, refuses a mismatch and a bare `approved`, and answers `ack <approval-id> applied|refused`. A person who types in the agent session is told to approve through Orca or GitHub.
   - **Plan version.** The approval-record helper defines the plan version as the SHA-256 over a named list of plan files (one plan file, or the files of a `/sc:workflow` package), in an order the helper fixes. The coordinator prints that file list and the hash in the plan reply, so the reviewer, the coordinator and the agent check the same bytes. The agent recomputes it with the same helper.
   - **Delivery to the agent.** The coordinator delivers the approval line by typing it into the agent's waiting prompt. As written, the worker contract forbids that: its input veto says "never answer a person prompt" (`src/superclaude/core/WORKER-CONTRACT.md` line 136), and the agent's `Waiting for approval` prompt is addressed to a person. There are two routes. First release: a written, narrow exception to that veto that allows exactly one line per approval row (the `approved <approval-id> plan-sha256=<hex>` line), logged. Durable route: the supervised-worker redesign (SW-13), in which the coordinator starts the agent as a supervised worker, so no person prompt is answered.
   - **Dead or missing agent session.** If the agent session is dead or missing, the row stays `recorded` and is shown as "recorded, not delivered". The coordinator reports it to the person and never relaunches the agent by itself.
4. **GitHub is a mirror and an input.** The coordinator posts the plan reply (with the plan version and its file list), moves Status to review and mentions the assignee.
   - **Checks run as code.** The coordinator reads GitHub approvals through a new read-only stage-status verb (for example a stage-status read), so the label and edit checks run as code, not as LLM prose. The verb reuses the watcher's GitHub reads and its actor checks, but it needs new stage predicates rather than plain reuse of `approval_of` and `unchanged_since`: `unchanged_since` skips comments whose author is the watcher's own login (`src/superclaude/cli/issue_watch/predicates.py` lines 253 to 255), and the plan reply is posted as that login, so an edit to the plan reply would not be seen; `approval_of` orders the approval against a trigger label event and the store creation time, not against a plan reply.
   - **Public marker.** After the row is written, from either channel, and before the instruction, the coordinator posts an "approved, starting" comment on the issue with marker `<!-- sc:stage:approved id=<approval-id> stage=<S> plan=<sha256> -->`. If GitHub is down this does not block the instruction (the row is the guard); the comment is retried at each wake. After an Orca approval the coordinator also applies the label and moves Status as a mirror.
   - **No-op on match.** A GitHub change that matches an existing row is a no-op.
   - **Revocation.** Removing the stage approval label (its actor is readable) is the revocation signal. A Status move back is shown and reported to the person, but never acted on alone, because no code reads who moved a Project Status (only its current value).
5. **Reconciliation by level.** At each wake (WC-16 already caps the pass at once every 5 minutes) the coordinator compares GitHub, the ledger and the agent's state and acts only on a difference.

**Invariant.** For each key (issue, stage, plan version) there is at most one approval record; only the coordinator creates it, through the locked helper, and that row is durably written (write-ahead) before any instruction; the agent proceeds only on a line that names that row and matches its plan hash.

<!-- Source: Base (V2) How an approval flows; GitHub step 3 replaced by changes 1, 2, 4 and 11 (V3, debate); Orca step 2 adjusted for change 4; coordinator-down note added by change 6 (debate, V2 concession 2) -->
## How an approval flows

**GitHub channel.**
1. The coordinator posted the plan reply (with the plan version and its file list), moved Status to review and mentioned the assignee.
2. The assignee applies the stage approval label (actor readable) and moves Status (display only; its actor is not read by any code today).
3. At its next wake the coordinator runs the read-only stage-status verb. It reads the label events, checks the actor against the approvers file and that the actor is not the host's `gh` login, and checks with the new stage predicates that the label came after the plan reply and that the plan reply was not edited after the label. The coordinator then writes the row (label event id as evidence), posts the "approved, starting" marker (not blocking if GitHub is down), and types the one approval line into the waiting agent session by the delivery route in Design item 3.
4. The agent checks the hash and acks. The coordinator marks the row `acked`.

**Orca channel (coordinator session now; TUI after the write-back release).**
1. Orca shows the person the plan path and version. The person approves in the coordinator session (or, later, the TUI sends a typed approval message to the coordinator's Run carrying the plan version and record version it displayed).
2. The coordinator writes the row, posts the "approved, starting" marker (not blocking if GitHub is down), delivers the line to the agent, then mirrors the label and Status to GitHub.
3. At its next wake it reads its own marker and mirror on GitHub, finds the row, and does nothing.

**While the coordinator is down.** An approval typed in the coordinator session cannot be made, because that session is not there to take it. Only GitHub approvals wait (as GitHub state), and later a TUI message could wait; whether a TUI message reaches a Run mailbox at all is UNVERIFIED.

<!-- Source: Base (V2) failure table; F1 modified by changes 4 and 10; F2 replaced by change 6 and extended by change 4; F3 adjusted for changes 4 and 11; F5 replaced by change 3 (V3) with change 4; F8 replaced by change 11; dead-session note added by change 9 -->
## What happens in each failure mode

| id | Outcome under the merged proposal |
|---|---|
| F1 Double start | Prevented by structure: only one actor exists, and its second look at the same approval finds the row. The key is (issue, stage, plan version), not the label event id, so a remove-and-reapply of the label finds the same row. A duplicate approval from the other channel gets one short reply on the issue (for example "already approved in Orca at <time>, row <id>") and no action |
| F2 Coordinator down | Nothing starts. GitHub approvals wait as GitHub state. An approval typed in the coordinator session cannot be made while that session is down; only a future TUI message could wait, and whether it reaches a Run mailbox is UNVERIFIED. The coordinator applies waiting approvals once on restart. On start-up, an "approved, starting" marker without a matching row is treated as an existing row, so a lost ledger does not restart finished work. Cost: delay |
| F3 Same-account echo | Irrelevant to duplicates: the coordinator's marker and mirror writes carry its row id, and any GitHub state that matches a row is a no-op. A GitHub approval with no row and no marker for its key is accepted as new, subject to the account rule in F8 |
| F4 Plan edited after approval | Row and instruction carry the plan hash; the agent refuses a mismatch; a changed plan needs a new review |
| F5 Moved backwards after start | Removing the stage approval label is the revocation signal: the coordinator marks the row `revoked`, sends one `stop <approval-id>`, and asks the person. A Status move back alone is shown and reported to the person, never acted on alone. The coordinator never restarts by itself; a later forward move needs a new row. A remove-and-reapply of the label for the same plan version finds the existing row, so it does not restart finished work |
| F6 Lag or lost events | Level reads at each wake; lag delays, never duplicates |
| F7 Two approvals at once | Serialised through one coordinator and the per-issue lock; the second gets "already approved" |
| F8 Someone else, or the agent, moves it | Project Status moves alone never authorise. On a single shared login a permission-free agent can apply the approval label too, so GitHub approvals are accepted only from approver account ids (in the approvers file) that are not the host's `gh` login. Without such an account the GitHub channel stays off until FU-6 (per-actor checks), or until the owner accepts the forgery risk in writing. The in-session path is removed |
| F9 Stale TUI | The TUI message carries the plan version and record version; the coordinator rejects a stale one |
| F10 ClickUp | Never read and never written for stages |

**Note: dead or missing agent session (not one of F1 to F10).** The row stays `recorded` and is shown as "recorded, not delivered"; the coordinator reports it to the person and never relaunches the agent by itself.

<!-- Source: Base (V2) Who is allowed to approve; GitHub bullet replaced by change 11 (debate, V2 neutral recommendation); plan-reply check wording aligned with change 2 -->
## Who is allowed to approve and how that is verified

- GitHub: an account in the approvers file applying the stage approval label after the plan reply, with the plan reply unedited since (checked by the new stage predicates). The approver's account id must not be the host's `gh` login. If no such account exists, the GitHub channel stays off until FU-6, or until the owner accepts the forgery risk in writing.
- Orca: the person at the coordinator's terminal, or the TUI once its write-back release exists. Whether a session on the same host can type into the coordinator's terminal (`orca terminal send`) and impersonate the person is UNVERIFIED and stays a residual risk.

<!-- Source: Base (V2), unchanged -->
## What the TUI and the issue show, and how they stay in step

The ledger row is the truth; the issue and the TUI are views of it. The issue shows the plan reply, the approval comment with the row id and the Status. The TUI would show the row state (recorded, instructed, acked, revoked). They agree within one coordinator wake (at most about 5 minutes); while they disagree, an approval made against the stale view is rejected by version, never doubled.

<!-- Source: Base (V2) build table; first row adjusted and stage-status verb row added by changes 1 and 2 (V3 U-008); helper row extended by changes 5 (V1) and 8; delivery row replaced by change 7 -->
## What it adds to the build

| Change | Watcher | Coordinator protocol | Observer | Claim command |
|---|---|---|---|---|
| None to the claim trigger; the watcher's claim behaviour stays as built (WA-01 to WA-05 unchanged) | none | none | none | none |
| Read-only stage-status verb reusing the watcher's GitHub reads and actor checks, with new stage predicates (approval label after the plan reply; plan reply unedited, including by the host's own login) | code (read-only) | uses it | none | none |
| Approval-record helper (small CLI verb with a per-issue lock), built on the watcher's `record.py` file lock and directory fsync with no new locking code; it also computes the plan version over the named plan files | none (code reused, not changed) | uses it | reads it later | none |
| Issue-pipeline duties: adopt the `issue-<N>` agent, post plan, mention, read GitHub at wake, record, post the marker, deliver, revoke | none | protocol | none | none |
| How the coordinator reaches the agent. First release: type one line into its waiting prompt under a written, narrow exception to the worker contract's "never answer a person prompt" veto, exactly one line per approval row. Durable route: make the agent a supervised worker started by the coordinator (redesign; SW-13) | none | protocol, plus the written exception in `WORKER-CONTRACT.md` | none | possibly |
| Launch prompt: approval-id and hash form only; no bare `approved` | none | none | none | template |
| TUI approval message to the coordinator (OB-09 Decision Desk plus the write-back boundary change) | none | none | code, later | none |

Existing items that change: WA-07 (handoff) becomes "coordinator adopts the claimed agent"; the coordinator needs `issue-write` grant rows (section 6.8) for the plan reply, marker, mention, label and Status.

<!-- Source: Base (V2) Cost and risk; watcher sentence adjusted for change 1 -->
## Cost and risk

Moderate build cost, almost all in the coordinator protocol plus one small helper and one read-only verb. The watcher's claim behaviour and the observer stay untouched until the TUI release; the only new code in the watcher package is the read-only stage-status verb. Progress stops while the coordinator is down. The coordinator is an LLM session, so the helper must enforce the one-row rule mechanically rather than by instruction.

<!-- Source: Base (V2) What stays unresolved; appended by change 12 (A-001, A-005, C-005 responses) -->
## What stays unresolved

Forgery on a single shared account; whether same-host sessions can type into the coordinator terminal; the Project Status value names; how the coordinator discovers a newly claimed issue (it can read `.dev/issues/<N>/worktree.json` or Orca's worktree list; which one is UNVERIFIED as reliable).

Preconditions and owner decisions:

- **Coordinator scope (A-001), a precondition.** No coordinator is attached to watcher or claim sessions today (WA-07 and SW-13 are deferred). Before any of this is built, the owner must decide who opens the coordinator and how many issues one coordinator holds.
- **Grants (A-005), a precondition.** The coordinator needs standing `issue-write` grants for the plan reply, mention, label and Status on every pipeline issue. The per-item grant table shape in `merged-requirements.md` section 6.8 is UNVERIFIED here and will need a pipeline-wide form.
- **Liveness against duplicate risk (C-005), left to the owner.** This proposal stops progress while the coordinator is down, in exchange for having one actuator. Whether that trade is acceptable is the owner's call.
