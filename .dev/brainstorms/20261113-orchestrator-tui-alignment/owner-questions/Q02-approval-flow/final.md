# Q2 approval flow: final advice

Written 2026-11-14 by the Q2 approval-flow worker. Advice only: nothing here decides anything for the owner, and nothing in the recommended design is built.

**What the owner answered (2026-11-14).** Q2 option 3: keep the claim's default level, so an approved issue gets a worktree `issue-<N>` and a second agent that stops at a plan for a person. Plus a requested approval flow: the plan is posted on the issue, the issue goes to a review state, the assignee is mentioned, and the assignee's move to the next state (or an approval given in Orca, in the coordinator session or the dashboard) authorises the next stage. The owner asked how to stop the two places from causing duplicate work. **Still open:** the owner has not given the written acceptance that the first test sessions run with permission checks off (decision 1 below). The answer above is not that acceptance.

**Terms.**
- *Watcher*: `superclaude issue-watch`, the built issue poller (issue #331). Every 5 minutes, once a schedule is installed, it starts one session that claims an approved issue.
- *Claim*: `/sc:issue --claim <N>`. At the default level it assigns the issue, posts two comments, creates worktree `issue-<N>` and starts the *governed agent*, which writes a plan, prints `Waiting for approval` and waits.
- *Coordinator*: a person-opened Orca session that supervises other agents under the worker contract (`src/superclaude/core/WORKER-CONTRACT.md`).
- *Observer* or *dashboard* (the owner's "TUI panel"): `superclaude observe` (issue #409), a read-only terminal screen. *Decision Desk* is its planned, gated third release (work item OB-09).
- *Plan version*: a SHA-256 hash of the plan's files, so an approval is tied to the exact plan a person read.
- *Approval record*: one row in the coordinator's ledger saying this issue, stage and plan version are approved.
- Work-item ids (WA-01 to WA-07 for the watcher, OB-09, SW-13, XC-01) and owner-question ids (Q2, Q20, Q25, Q26) come from `merged-requirements.md` in the parent brainstorm folder. F1 to F10 are the failure modes in `00-state-machine-and-failure-modes.md` (this folder).

**Files in this folder.** `00-state-machine-and-failure-modes.md` (the flow as stages, what exists today, the ten failure modes); `proposal-A.md`, `proposal-B.md`, `proposal-C.md` (three designs); `adversarial/` (debate record); `merged-proposal.md` (the merged design, full text).

## 1. Debate result and confidence

**Winner: proposal B (one actuator: only the coordinator may tell the agent to proceed), merged with parts of C and A. Confidence 72 percent** (mean of the three advocates' neutral recommendations: 75, 70, 70). All three advocates, including the advocates for A and C, recommended a B-based merge when asked to be neutral. Convergence 95 percent (19 of 20 debate points). One point stayed split: whether work may continue while the coordinator is down (decision 5 below).

- **Proposal A (every channel may start the stage, guarded by one shared lock).** Strength: progress continues with no coordinator running. Weakness: it makes three things able to start work, one of them the permission-free agent itself (which can approve its own plan), and it reverses the owner's recorded watcher decision D2 ("The poller never assigns, comments or moves Project items", `docs/designs/issue-watcher.md` section 2.1). Lost every core point.
- **Proposal B (one actuator).** Strength: it is the owner's "single source" option taken literally, and the watcher stays exactly as built. Weakness found in debate: it overstated that Orca approvals queue while the coordinator is down, and its delivery method collides with the coordinator's own rule "never answer a person prompt" (`WORKER-CONTRACT.md` line 136). Both are fixed in the merge.
- **Proposal C (GitHub is the only authority; Orca approvals are written to GitHub and acted on only after reading them back).** Strength: one public record, and a GitHub-assigned event id that two local copies cannot both claim. Weakness: on this host's single GitHub login, an approval written through by the coordinator and one forged by an agent look identical; with a second login the Orca channel can no longer write through. It contradicts itself on that point.

**fallback_mode: false.** Three advocate sub-agents and one merge sub-agent were spawned. The difference analysis, the scoring and the merge plan were done inline by this worker (one evaluator, so the order-bias check is weaker than the protocol intends). Depth was quick: no rebuttal round and no invariant probe ran.

## 2. Recommended design and the one invariant it rests on

**The invariant.** For each issue, stage and plan version there is at most one approval record; only the coordinator creates it, through a small locked helper, and writes it to disk before it sends any instruction; the agent continues only on a line that names that record and matches the plan's hash.

That is the owner's second option ("the final instructions that trigger anything of consequence can only come from a single source and all others are ignored"), made checkable. Every approval, from GitHub, the coordinator session or later the dashboard, is only an input. The coordinator is the only thing that ever tells the agent to proceed.

**The owner's own scenario under this design.** The person approves in Orca. The coordinator writes the approval record, posts an "approved, starting" comment with a hidden marker on the issue, sends the agent one line (`approved <record-id> plan-sha256=<hash>`), then applies the approval label and moves the Status on GitHub to match. Nothing on GitHub can trigger a second start:
- The watcher never reacts. Today it only acts on issues in the Project's `Backlog` column and treats a claimed issue as finished (`predicates.py` `project_check`; `issue-watcher.md` section 7.3). The design keeps it that way on purpose, so the watcher can never be the second trigger. The owner's picture of "the watcher sees the move and sends the coordinator instructions" describes something that does not exist and should not be built.
- At its next check the coordinator reads GitHub, finds its own record for that issue, stage and plan version, and does nothing.
- If a person also approves on GitHub because GitHub had not caught up yet, the coordinator finds the same record, does nothing, and replies once on the issue: "already approved in Orca at <time>, record <id>".

**Two changes to what the owner described, forced by the code.**
1. *The approval signal on GitHub is a label, with the Status move as the visible sign.* The watcher's code reads who applied a label (account id, login, type) but only reads the current value of the Project Status, never who set it (`github.py` `EVENTS_JQ` and `PROJECT_ITEMS_QUERY`). Without knowing who moved the card, a move by an unauthorised person or by an agent cannot be refused. Whether GitHub can report who moved a Project Status is UNVERIFIED; if it can, the move itself could become the signal (decision 3).
2. *The plain `approved` typed in the agent's own session goes away.* Today the launch prompt says "A human approves by replying `approved` in this session" (`~/.claude/skills/sc-issue-protocol/templates/launch-prompt.md`). Any text in that session, including text the permission-free agent produces after reading issue text anyone can edit, could satisfy it.

The full design text is `merged-proposal.md`.

## 3. Failure modes under the recommended design

| Failure | Scenario | What happens |
|---|---|---|
| F1 Double start | Approved in Orca, then the GitHub side catches up (or a person approves there too) | The coordinator is the only starter; its second look finds the record and does nothing; a duplicate approval gets one reply on the issue |
| F2 Coordinator down | The assignee approves on GitHub at night | Nothing starts. The approval waits on GitHub and is applied once when the coordinator returns. An approval cannot be typed into a coordinator session that is not running. Cost: delay, not duplicate work |
| F3 Same account echo | The coordinator's own label and Status writes look like a person's | Every coordinator write carries the record id; anything on GitHub that matches an existing record is ignored |
| F4 Plan edited after approval | The agent rewrites the plan after approval | The record and the instruction carry the plan hash; the agent recomputes it and refuses a mismatch; a changed plan goes back to review |
| F5 Moved back after work started | The assignee withdraws approval | Removing the approval label (who did it is readable) revokes: one stop message, then the coordinator asks the person. A Status move back alone is reported, not acted on. Nothing restarts by itself |
| F6 Lag and lost events | GitHub shows old state for a while | The coordinator compares states at each check (at most every 5 minutes) instead of reacting to events; lag delays, never duplicates |
| F7 Two approvals at once | Dashboard and coordinator session at the same moment | The helper's lock lets one record through; the second gets "already approved" |
| F8 Someone else, or the agent, approves | A collaborator or a steered agent applies the label | GitHub approvals count only from listed approver accounts that are not this host's own GitHub login. Without such an account the GitHub channel stays off (decision 4) |
| F9 Stale dashboard | The screen still shows "in review" | A dashboard approval carries the versions it showed; a stale one is refused |
| F10 ClickUp | Someone changes a ClickUp status | Never read or written for stages; the claim only sets the ClickUp assignee today (`scripts/clickup_claim.py`) |
| Agent session died while waiting | Host restart during review | The record stays "recorded, not delivered" and the person is told; the agent is never relaunched automatically |

## 4. Safeguards that stay even with a single source

A single actuator removes the race between channels. These still guard against crashes, lag, forgery and stale views:

1. **Write-ahead record.** The record is on disk before any instruction. The helper reuses the watcher's tested lock and sync code (`src/superclaude/cli/issue_watch/record.py`: exclusive non-blocking file lock at line 403, state-directory sync at lines 310 to 313), so the one-record rule is enforced by code, not by asking an AI session to remember it.
2. **Compare states, not events.** At each check the coordinator compares GitHub, its ledger and the agent's state and acts only on a difference.
3. **Echo suppression.** Coordinator writes carry the record id; a match is ignored.
4. **Approval tied to the plan version.** The hash covers a named list of plan files, is printed in the plan reply, and is rechecked by the agent.
5. **Who may approve.** On GitHub: a listed approver account, applying the label after the plan reply, with the plan reply unedited since, and not this host's own login. The watcher's existing edit check cannot be reused as is: it skips comments by the host's own login (`predicates.py` lines 253 to 255), and the coordinator posts the plan reply as that login, so a new check is needed. In Orca: the person at the coordinator's terminal. Whether another session on the same host can type into the coordinator's terminal and pose as the person is UNVERIFIED and stays a residual risk.
6. **Revocation after start.** Label removal revokes; one stop; ask the person; never restart alone. Gap the merge left open and this worker's recommended rule: re-approving the same plan version after a revocation re-opens the same record (its evidence list grows) instead of creating a second one, and the agent resumes only on the person's instruction.
7. **Lost ledger.** A "approved, starting" marker on the issue with no matching record is treated as an existing record, so losing the ledger cannot restart finished work.
8. **Dead session.** Report, never relaunch automatically.
9. **Delivery rule.** The worker contract forbids the coordinator to "answer a person prompt" (`WORKER-CONTRACT.md` line 136), which is what typing the approval line into the waiting agent is. First release: a written, narrow exception for exactly one line per approval record. Lasting fix: start the agent as a supervised worker (work item SW-13), so no person prompt is answered.

## 5. Edits this implies in `merged-requirements.md` (NOT applied)

| Where | Edit |
|---|---|
| Section 3, Q2 row | Record the answer "option 3, plus the approval flow" with its date; keep "written acceptance: open". Under option 3 the acceptance must cover two sessions per test issue (the claim session and the governed agent) |
| WA-01 (claim level) | Take its "If Q2 keeps the default" branch: record the default level as a deliberate choice in #450, list the claim command's ship gates OB-H1 items 1 and 5, OB-H2 and OB-H3 as preconditions of the first live test, and amend design decision D2 in `docs/designs/issue-watcher.md` ("The claim stops at `next-steps.md`") |
| WA-07 (watcher to orchestrator handoff, deferred) | Rewrite as "a coordinator adopts the claimed issue's agent; the watcher stays claim-only and never reacts to later stages" |
| New WA item | Read-only stage-status command in `issue_watch`, reusing the GitHub reads and actor checks, with new stage checks (label after the plan reply; plan reply unedited, including by the host's own login), with tests |
| New item | Approval-record helper (locked, write-ahead, computes the plan version), built on `record.py` |
| New item | Claim template change: the worktree-level launch prompt accepts only `approved <record-id> plan-sha256=<hash>` and answers with an acknowledgement |
| Coordinator protocol (section 6 and `WORKER-CONTRACT.md`) | New issue-pipeline duties: adopt the agent, post the plan reply, mention the assignee, read GitHub at each check, record, post the marker, deliver, revoke; plus the narrow exception to "never answer a person prompt" |
| Section 6.9 (never do) | Add: never tell a governed agent to pass its plan boundary without an approval record; never act on a Status move alone |
| Section 6.8 (grants) | The grant table is written per item and per action (verified). This flow needs a new shape: one grant row per pipeline issue, created at claim time, listing plan reply, marker comment, mention, label and Status writes |
| OB-09 (Decision Desk, deferred) | Add to its gate: an approval from the dashboard is a message to the coordinator only, carrying the plan version and record version it displayed; it needs the write-back boundary change on #409 (the observer today forbids every write verb, `observe/adapter.py` `FORBIDDEN_PREFIXES`) |
| SW-13 (sub-orchestrator design, deferred) | Add: the supervised-worker route is the lasting delivery path for approvals |
| Appendix of owner questions | Add the new decisions 2 to 9 below as Q34 onward |

## 6. Work this adds, in order

1. Owner decisions 1 to 4 and 7 (below). Nothing is built before them.
2. A read-only check, no writes: can GitHub report who moved a Project Status, what the Status values are called, and does applying an already-present label record a second event? (All UNVERIFIED today.) This settles decision 3.
3. The watcher's own first live test (WA-04), unchanged, with its existing preconditions. The approval flow cannot be tried before a claim has ever run live.
4. Approval-record helper, then the read-only stage-status command, each with tests.
5. Claim template change (no plain `approved`).
6. Coordinator protocol duties and the worker-contract exception; the grant shape.
7. One live run of the full flow on a test issue, under its own live-test grant.
8. Later: dashboard approval (OB-09 plus write-back); supervised-worker delivery (SW-13).

## 7. Built today versus not built

| Piece | State |
|---|---|
| Watcher claim trigger, label-actor checks, at-most-once launch store | Built, merged, never run live; schedule not installed |
| Claim at default level: assign, two comments, worktree, governed agent that waits for approval | Built; launch gated by its ship gates, OB-H1 item 5 recorded as not yet run |
| Approval in the agent's own session (plain `approved`) | Built; recommended for removal |
| Plan posted on the issue, review state, mention | Not built |
| Coordinator attached to claimed issues | Not built (WA-07, SW-13 deferred) |
| Approval record, helper, stage-status command | Not built |
| Dashboard approval | Not built; the observer is read-only and its questions panel is switched off (`QUESTION_GATE_PASSED = False`) |
| ClickUp stage status | Not built and not recommended |

## 8. Owner decisions still open

Each can be answered on its own. Reply format: "Decision N: option X".

**Decision 1. Written acceptance for the first test (still open from Q2).** On this host, sessions started by the watcher run with permission checks off and read issue text anyone who can edit the issue controls. With option 3, one approval starts two such sessions (the claim session and the governed agent).
- Option A: accept in writing, for the one test issue only, that both sessions run with permission checks off, covering whatever they do on that issue, not only the intended writes. The test still waits for its other preconditions (the claim's ship gates, a separate live-test grant, Orca running, an owner for the watcher worktree).
- Option B: do not accept; the first live test stays held.
- Recommended: A, and write the test issue's text yourself to shrink the untrusted-input risk.

**Decision 2. Single source or safeguards.** Who may tell the agent to proceed after approval?
- Option A: only the coordinator; every other channel is an input (recommended design).
- Option B: any channel may, behind a shared lock (proposal A). Keeps working without a coordinator, but the agent can approve itself and the watcher must start writing to GitHub.
- Option C: only GitHub counts; Orca approvals are written to GitHub first (proposal C). Breaks on one GitHub login.
- Recommended: A.

**Decision 3. What counts as approval on GitHub.**
- Option A: an approval label applied by the assignee, with the Status move as the visible sign (recommended while no code can tell who moved the Status).
- Option B: the Status move itself, only if the read-only check in section 6 step 2 shows GitHub reports who made the move.
- Recommended: A now; revisit B after that check.

**Decision 4. A second GitHub account for approvers.** Everything on this host acts as one GitHub login, so an agent can apply the approval label as you.
- Option A: approvers use a separate GitHub account that this host's sessions do not hold; approvals from the host's own login are refused.
- Option B: switch the GitHub channel off; approve only in Orca until per-person checks (follow-up FU-6) exist.
- Option C: keep one login and accept in writing that an agent could forge a GitHub approval.
- Recommended: A. If you say nothing: B.

**Decision 5. While the coordinator is not running.**
- Option A: nothing starts; approvals wait and are applied when it returns (delay only).
- Option B: let the watcher start GitHub-approved stages itself (faster, but the watcher becomes a second starter and must write to GitHub, against your recorded design).
- Recommended: A. This was the one point the debate did not settle.

**Decision 6. How the approval reaches the agent.**
- Option A: first release types one approval line into the agent's waiting prompt, under a written, narrow exception to the coordinator rule "never answer a person prompt"; later, move to Option B.
- Option B: first redesign so the coordinator starts the agent as a supervised worker (larger change, deferred item SW-13).
- Recommended: A, then B.

**Decision 7. Which coordinator owns claimed issues.**
- Option A: one person-opened pipeline coordinator for all watcher-claimed issues on this host, with a lock per issue.
- Option B: one coordinator per issue.
- Recommended: A. If you say nothing: no coordinator exists, so the approval flow cannot run and approvals stay in the agent's own session as today.

**Decision 8. Standing permission for the coordinator to write to pipeline issues.** It must post the plan reply, the marker comment, the mention, the label and the Status.
- Option A: one grant row per issue, created when the issue is claimed, listing exactly those writes.
- Option B: you approve each write as it happens.
- Recommended: A.

**Decision 9. Remove approval typed directly in the agent's session.**
- Option A: remove it; approve in Orca or on GitHub only (closes the self-approval hole).
- Option B: keep it (convenient, but text the agent itself produces can approve).
- Recommended: A.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q02-approval-flow/adversarial/` (`diff-analysis.md`, `round1-advocate-V1.md` to `V3.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`).
- fallback_mode: false.
