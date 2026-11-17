# Change list for the merged requirements (issue watcher claim handoff, Decision 6 = B)

Target file, not edited by this plan: `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` (row ids below are that file's). This list says what each named item must become once design B (a person-opened coordinator starts the plan-writing agent as a supervised Orca worker for a watcher-claimed issue) is built. The owner applies it later; nothing here changes the file.

Written for a person who has not seen the project. Plain words: the *watcher* is the timer job that notices an approved GitHub issue and starts a *claim* session for it; the *coordinator* is a session a person opened, which starts and answers *workers*; design B lets the claim session stop at "claimed, files written, no agent" and lets the coordinator start the agent that writes the plan.

## 1. Item changes (one sentence each)

| Item | Change |
|---|---|
| WA-01 (claim level) | Take the `--pipeline none` branch, now with the coordinator handoff: `launch.PROMPT_PATTERN` and `build_claim_prompt` emit `--pipeline none`, and the claim no longer creates a worktree or an agent (the coordinator does both steps afterwards). |
| WA-02 (#450 edits) | The #450 edits list gains edit B: the issue text states that the watcher claims with `--pipeline none` and a coordinator, not the claim session, starts the plan-writing agent. |
| WA-03 (runbook step) | The runbook step 1.3a also names who runs the coordinator that owns watcher-claimed issues on this host (one person-opened coordinator, one lock per issue) and says nothing starts while it is down. |
| WA-04 (FU-1 record) | The FU-1 record adds preconditions a to k of `docs/designs/issue-pipeline-fu1.md` (a to j from the validation file, k = web-editor comment round trip) and the owner's written guard-loss acceptance for the one test issue. |
| WA-07 | Moves from DEFERRED to live under B, and its "blocked by SW-13" is removed (SW-13 is now the delivery path, see below); its condition (4) is restated to cover the guard loss of the one G1 test issue, and (5) stays: no free text from the issue reaches a prompt. |
| SW-13 | The supervised-worker route (`worker-start` by the coordinator, `ask` and `reply` for plan approval) is now the delivery path of the handoff, no longer a later sub-orchestrator redesign. |
| OB-09 | A dashboard approval is only a message to the coordinator (WC-12): the human answer travels through the coordinator, which records it and tells the worker; the dashboard never approves by itself. |
| Section 6.3 (roles) | Gains a worker row for the plan-writing worker: it writes the plan, asks the coordinator for approval and never pushes, comments, commits or creates worktrees. |
| Section 6.4 rule 10 | Permission mode of every started session is accepted in writing, now including the guard loss: the one G1 test issue runs with permission checks off and no launch-level guard until G2 exists. |
| Section 6.8 (grant table) | Gains a per-pipeline-issue grant row shape: one row per issue holding the plan reply, the marker comment, the mention, and the label and Status writes the coordinator may make. |

## 2. New items, one per plan task

| Task | New item (one sentence) |
|---|---|
| 16 | Remove the plain `approved` release from the launch-level guard and the launch prompt for every worktree-level claim; only a first line starting `/sc:implement`, `/sc:task` or `/task` releases (own branch, own pull request later). |
| 1 | `issue_pipeline` package with `issue-pipeline plan-hash`: a SHA-256 over a named list of plan files (name, length and bytes each), shared by coordinator and worker. |
| 2 | The approval line module and `check-approval`: only `approved` and `approved <record id> plan-sha256=<64 hex>` are accepted, whole text, no trimming. |
| 8 | The first-live-test runbook `docs/designs/issue-pipeline-fu1.md` (document only), with the guard-loss acceptance and eleven `PENDING:` record lines. |
| 3 | A locked, write-ahead approval record helper with an adoption row per (issue, stage) (`reserved`, `started`, `uncertain`) and an approval row per (issue, stage, plan hash), so a start and a continuation happen at most once. |
| 4 | Stage predicates for the approval label and the `approved` comment (order after the plan reply, author type, assignee or approver, edits, plan hash), plus recorded real GitHub responses for the owner's issue. |
| 5 | GitHub reads that turn comment text into booleans and fixed-pattern ids inside jq, under the watcher's call budget. |
| 6 | The read-only `issue-pipeline stage-status` command. |
| 7 | The worker brief builder from fixed templates for the three Feature rows (type `bug` refused), in the layout of `WORKER-CONTRACT.md` section 5. |
| 9 | The brief's `Worktree:` slot changes from the contract's `shared feature worktree` or `child worktree` forms to `path:<existing worktree>`, the worktree the claim script made (Plan B). |
| 15 | The `pending` subcommand of Plan B Task 15 (a new verb that belongs to the guard change G2, Tasks 13 to 15); what it prints is defined in Plan B, which this run did not read, so this row only records that the verb is a new item. |
| 10 | Plan B Task 10: an item of the coordinator route that Plan A says is written after the first live test's launch receipt, together with Task 9 (precondition d); its own wording is in Plan B, which this run did not read. |
| 11 | Plan B Task 11: the code pull request that carries the coordinator route; the documentation amendments of Tasks 17 and 18 wait on it (Q40). |
| 12 | Plan B Task 12: the coordinator's handling of approvals and resumes; per Plan A it refuses the label channel when label events lack the actor (precondition j) and records message ids differently if resume by id does not work (precondition g). |
| 13 | Plan B Task 13: the guard change G2; per Plan A it chooses the release route after the first live test (the worker's session id found or not, Q38) and, being a change to a security hook, gets its own independent review. |
| 14 | Plan B Task 14: the first part of the coordinator-side release of a guarded worker, edited in the same guard file as Task 16 and Task 15, so whichever lands second rebases onto the other. |

## 3. Owner decisions (Q35 to Q41), none open

| Q | Question in plain words | Options | Recommended | Owner's answer |
|---|---|---|---|---|
| Q35 | How does the claim hand over: what does the watcher's claim do before the coordinator takes over? | **B1b**: the watcher claims with `--pipeline none` and the coordinator runs the existing worktree step (no claim code changes, only the watcher prompt and tests). **B2**: a new claim level that creates the worktree and copies files without an agent (about six more test files, and a worktree with no agent until the coordinator starts one). | B1b | **B1b**, 2026-11-15 (first 2026-11-14; the first reply wrote "Q53 b1b" and "2. Approved", read as Q35). |
| Q36 | How fast is approval when no timer re-reads GitHub (decision Q31, no recurring timer)? | **A**: accept the delay and make Orca the fast path (approve in the coordinator session, immediate). **B**: a narrow timed read only for issues waiting for approval (reverses Q31 for that case). **C**: the person types "check now" after approving on GitHub. | A together with C | **Option A**, 2026-11-15 (first 2026-11-14 as "accepted delay"). Option C ("check now") is not selected and not built. |
| Q37 | Where does the worker's plan-approval rule live? | A new rule in `WORKER-CONTRACT.md` next to WC-3 (written once). Only in each brief (no contract edit, every brief repeats it). | In the contract, next to WC-3 | **In `WORKER-CONTRACT.md` next to WC-3**, 2026-11-15 (first 2026-11-14). |
| Q38 | How does a coordinator approval release a guarded worker (the later guard change G2)? | **A**: the coordinator writes the session's release file after recording the approval (needs the worker's session id, UNVERIFIED). **B**: the guard reads a coordinator-signed approval file (more guard code). | A if the first live test shows the session id can be found, else B | **The default until G2**, 2026-11-15 (first 2026-11-14): G2 is not built, so only the one G1 test issue can run; the route is chosen in Task 13 after the first live test. |
| Q39 | How far does removing the plain `approved` release reach? | Remove it for every worktree-level claim (closes the self-approval hole; a person with no coordinator then types `/sc:implement` in the session). Keep it for person-run claims until G2 exists. | Keep for person-run claims (the earlier recommendation, not taken) | **Remove it now for every worktree-level claim**, with no person-run carve-out and no wait for G2 or the live test, 2026-11-15 (Task 16; built on branch `ironbelly/remove-approved-route`). |
| Q40 | In what order do the design documents change? | One follow-up documentation PR for Tasks 17 and 18 (after #548). Fold them into the code PR of Task 11. | One follow-up documentation PR | **One follow-up documentation PR**, 2026-11-15 (first 2026-11-14), opened only after the owner reads the plan; no PR is opened from this plan, and Tasks 17 and 18 wait on Task 11. |
| Q41 | What about the worktree with no agent, for the moment between the claim script and the coordinator's `worker-start`? | **A**: accept it and say so in the claim text (the script closes the plain first tab, nothing runs in the empty worktree, nothing starts while the coordinator is down). **B**: change the script to create the worktree with an agent (more claim code, a second agent instead of the worker). **C**: let `worker-start` create the worktree itself (skips the script's copy step and reuse lookup; rejected in the design session). | A | **A**, 2026-11-14: accept it and say so in the claim text. |

## 4. Facts the first live test must measure (not decisions)

The real `worker-start` argv and permission flags; whether `worker-start` accepts an exact existing worktree that the script created and leaves exactly one terminal; the `ask` and `reply` round trip, including whether the reply is stored as type `status` and a narrow `--types` filter misses it; the launch receipt shape and the Dispatch id; how a worker's session id can be found (it decides the G2 release route in Task 13); `ask` timeout and resume by message id; a worker staying in `ask` while the coordinator is down; worktree reuse when the claim runs twice; the GitHub label event shape; whether a comment typed in the GitHub web editor arrives as exactly `approved`; and what a comment edit does to `lastEditedAt`. Each is a precondition (a to k) of `docs/designs/issue-pipeline-fu1.md`.
