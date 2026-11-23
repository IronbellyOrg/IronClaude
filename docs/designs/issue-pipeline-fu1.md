# Issue pipeline: first live test (FU-1) runbook for the claim handoff (Decision 6 = B)

Status: runbook only. **No step in this document is run by the agent that wrote it.** The owner runs every step, on a throwaway issue the owner wrote, and fills the record at the end. Nothing here claims, starts, merges or posts anything by itself.

This test is the claim-handoff part of FU-1, the first live test of `docs/designs/issue-watcher-setup.md` section 8.5 (the live-test record) and section 14.1 (the live test). It adds preconditions a to k for design B: a coordinator starts the plan-writing agent as a supervised Orca worker for a watcher-claimed issue. The facts below come from the validation file of the plan package `TASK-WF-planDecision6BFo-20261114-174909` (its section 7 lists a to j); precondition k is new.

## 1. What B does, in four lines

1. The watcher claims the issue with `--pipeline none`: comments, `issue-summary.md` and `next-steps.md`, and no agent.
2. The coordinator runs the existing `orca_worktree.py worktree` step (a worktree `issue-<N>` with no agent for a moment, accepted by the owner on 2026-11-14), then starts the worker with `orca orchestration worker-start --worktree path:<that worktree>`.
3. The worker writes the plan and asks the coordinator for approval through `ask`; the coordinator answers with `reply`.
4. An approval can also arrive as a label or as an `approved` comment on GitHub; both map to one record, so the stage never starts twice.

## 2. Written acceptance the owner must give before the test

Copy this sentence into your own message, replace `<N>`, and send it before precondition a:

> I accept, for test issue #<N> only, that the plan-writing worker runs with permission checks off and with no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement), reading issue text that I wrote myself. This is separate from my 2026-11-14 acceptance of permission checks off.

The test issue text is written by the owner. No other issue runs through this flow until the guard is changed (Plan B Tasks 13 to 15).

## 3. Gates that still apply (none is waived by the acceptance)

- A separate live-test grant row for this one issue.
- A reachable Orca (`orca status` answers) and a coordinator terminal.
- A named owner of the watcher worktree (written in the grant row).
- The claim's own hook check (the claim refuses with `W-ENFORCEMENT-ABSENT` when its checks fail; it is not bypassed).
- Every `gh` call in this runbook is a read-only GET (or the fixed edits GraphQL query) and names `IronbellyOrg/IronClaude`, by `--repo IronbellyOrg/IronClaude` or, for `gh api`, in the path `repos/IronbellyOrg/IronClaude/...`. Nothing is sent to the upstream SuperClaude repository.

## 4. Risk stated once (Decision 4, accepted)

The worker also holds the one GitHub login on this host, so it can apply the approval label or post the approval comment as that same login, and nothing tells the two apart. GitHub approvals (the label and the `approved` comment) stay accepted inputs; the code checks order, author type, edits and the plan hash, not who typed. The guard loss of section 2 means nothing blocks the worker from doing so.

## 5. Preconditions a to k

Run them in this order. For each: the step, the value to record, and what a failure means. Steps marked "throwaway" use the throwaway issue's worktree and a hand-written brief (no brief builder, no worker-approval rule, no coordinator duties).

### a. `worker-start` argv and permission flags

- Step: after one throwaway start, run `ps -o pid,args -p <worker pid>`; read `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` from the worker's environment with `tr '\0' '\n' < /proc/<pid>/environ | grep -E '^(CCSESSION_PERMISSIONS|CC_CLAUDE_FLAGS)='` (values only for these two names).
- Record: the full argv, the two variable values, the permission flag seen.
- Failure means: if permission checks are on, the worker may stall on prompts; if the argv differs from the `ccsession-orca` flags, Decision 1's acceptance does not describe the real worker and the owner must decide again.

### b. `worker-start --worktree path:<existing worktree>` leaves exactly one terminal

- Step: create the worktree with `orca_worktree.py worktree` for the throwaway issue; run `orca terminal list --json` before and after `orca orchestration worker-start --from <coordinator handle> --spec "<brief>" --worktree path:<that worktree> --agent claude --json`.
- Record: terminal count before and after, and the worktree path used.
- Failure means: a second terminal or a second worktree appears, so B1b (script creates, coordinator starts) is not valid and the owner must choose again between the claim levels in the plan's Task 19.

### c. `ask` and `reply` round trip for a worker started with a spec

- Step: the throwaway brief tells the worker to `ask` one question; the coordinator answers with `orca orchestration reply --from <coordinator handle> --id <message id> --body "ok"`; read the worker's result and run `orca orchestration check --terminal <coordinator handle> --json` with and without a narrow `--types` filter.
- Record: the body the worker received, the stored type of the reply (`status` or other), and whether a narrow `--types` filter misses it.
- Failure means: if the reply is not delivered, the coordinator route of Plan B Tasks 9 to 12 cannot work; if a narrow filter misses it, those tasks must read without a type filter.

### d. Launch receipt shape and Dispatch id

- Step: save the full `worker-start --json` reply of step b to a scratch file.
- Record: the field names that hold the Dispatch id, the Task id and the terminal handle (names only; this is the shape that later becomes a test fixture).
- Failure means: Plan B Task 9 cannot parse the receipt and is written after this shape is known.

### e. The plan hash is identical on both sides

- Step: no Orca. In a scratch directory with two plan files, run `uv run superclaude issue-pipeline plan-hash <dir> a.md b.md` as the coordinator and again as the worker (a second shell), then `uv run superclaude issue-pipeline check-approval <dir> a.md b.md --line "approved ap-<N>-plan-<first 12 hex of the hash> plan-sha256=<the 64-hex hash>"` (`plan-hash` prints `plan-sha256: <hash>` with a colon and a space; the line uses `plan-sha256=` with an equals sign and no space; `<N>` is the throwaway issue number).
- Record: both hashes, and the check-approval result word.
- Failure means: any difference is a defect in `src/superclaude/cli/issue_pipeline/plan_hash.py`; stop the test.

### f. Guard interaction under G1

- Step: with G1 (the worker starts with no launch marker), run `ls ~/.claude/state/launch-level/sessions/` before and after the worker starts; then ask the worker to send one `ask` and one `send` to the coordinator.
- Record: whether the sessions folder changed, and whether `ask` and `send` were allowed.
- Failure means: if a guard binds the worker, the worker is blocked and G1 is not what the plan assumes; if `ask` and `send` are blocked, the route needs G2 (Plan B Task 13). The session id lookup for G2 is also recorded here (found or not).

### g. `ask` timeout and resume by message id

- Step: let one `ask` time out (`--timeout-ms 5000` on a throwaway question); then resume it with the message id the timeout printed (the installed `orca orchestration ask --help` lists `--resume <message_id>`; confirm it on the test run).
- Record: the exact text of the timeout, the resume command that worked, and the reply received after it.
- Failure means: without a working resume, a coordinator restart loses the question and Plan B Task 12 must record ids differently.

### h. The worker stays in `ask` while the coordinator is down

- Step: with a worker waiting in `ask`, stop the coordinator's wait (close its wait command, do not close the worker); read `orca orchestration worker-list --run <run id>` after two minutes.
- Record: whether the worker is still listed alive and still waiting.
- Failure means: if the worker exits, "nothing starts for a project while its coordinator is down" is not enough and the approval wait needs a different design.

### i. Worktree reuse when the claim runs twice

- Step: run the claim's worktree step twice for the throwaway issue number; read `orca worktree list`.
- Record: the number of `issue-<N>` worktrees after each run.
- Failure means: two worktrees mean the reuse lookup (marker, record, basename, branch) failed and the coordinator must refuse to start a second worker.

### j. GitHub stage facts

- Step: read-only GETs on the throwaway issue: `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/timeline` and the comments call the plan's Task 5 builds. Then move the issue's Project Status by hand and add and remove the approval label by hand, reading the timeline after each.
- Record: the label event field names, who the actor is shown as, and whether a Project Status move shows as an event or only in the project item.
- Failure means: if a Status move is not readable, it stays the "visible sign only" the plan already assumes; if label events lack the actor, the label channel cannot check who approved and Plan B Task 12 must refuse it.

### k. Web-editor comment round trip and edit time

- Step: post a comment `approved` on the throwaway issue from the GitHub web page (not from `gh`); read it back with `gh api --method GET repos/IronbellyOrg/IronClaude/issues/comments/<comment id>`; then edit it in the web page and read `lastEditedAt` through the fixed edits GraphQL query.
- Record: the body bytes as returned (exactly `approved` or with extra characters), and whether `lastEditedAt` changes on the edit.
- Failure means: if the web editor adds a newline or other characters, the exact-match rule of Task 4 refuses real approvals and the rule needs a decided exception; if `lastEditedAt` does not change, an edited approval cannot be told from an unedited one.

## 6. Record

The agent that runs the test replaces each `PENDING:` line below with `RECORDED: <letter> <measured value>`, adding the Orca build string from `orca-ide --version` and the date inside each value. The owner's go and the written acceptance of section 2 are given in chat; the owner never has to write a file. When the run is done, the agent adds one closing line in the form `RUN BY OWNER: <name>`, with the name the owner gave in chat. Plan B Task 20 checks this section.

RECORDED: a argv `claude --dangerously-skip-permissions --allowedTools=Grep --settings {...}` (permission checks off); `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` not set in the worker's environment; Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17, run by an agent on the owner's direct instruction (throwaway issue 452)
RECORDED: b `worker-start --worktree path:/home/coder/workspaces/worktrees/IronClaude/issue-452` reused the existing worktree and created exactly one terminal (25 before, 26 after); Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RECORDED: c reply body `pong` reached the worker exactly; the stored type of the reply is `status` (so a narrow `--types question` filter would miss it); Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RECORDED: d receipt result keys `dispatchId, effects, launch, mode, mutation, prompt, residualResources, runId, setup, stage, state, taskId, timeoutMs, turnStart, warning`; the terminal handle is in `effects[kind=terminal].id`; state `ready`, turnStart `observed`; Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RECORDED: e hashes identical (coordinator and worker `472a3bed65842388c3f182b0e7792b21e316458a98916aae5d9895cade1381b6`); check-approval `ok`, bare `approved` `refused:bare`; 2026-11-17
RECORDED: f no launch-level session entry was created or changed after the worker started (no entry newer than the start time); the worker's `ask` and `send` were not blocked; the worker's session id lookup for G2 was not attempted; Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RECORDED: g timeout text `ask timeout after 5000ms; question is still pending (messageId: msg_...). Resume waiting; do not ask again:`; resume `orca orchestration ask --from <handle> --resume <message id> --timeout-ms 900000` returned `resumed`; Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RECORDED: h with no coordinator wait for about 100 seconds the worker stayed `workerState=ready`, `terminalState=active` in `worker-list`, then received the reply; the coordinator was not stopped for longer than that; Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RECORDED: i the claim script's worktree step run a second time returned `reused` (match key `marker`), one `issue-452` worktree before and after; Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RECORDED: j a label added and removed on #452 gave `labeled` then `unlabeled` events whose actor is `ironbelly`, id 7361222, type `User` (same login as the host, Decision 4), with `label.name`, `created_at` and keys `actor,commit_id,commit_url,created_at,event,id,intent,label,node_id,performed_via_github_app,url`; the code's projection fields match; moving #452's Project Status Done to Ready and back to Done (with the `project` scope granted by the owner in the browser) gave one `project_v2_item_status_changed` event per move in the issue events, each with actor `ironbelly`, type `User` and the keys of any event, so a Status move by a person is readable with its actor (earlier automatic moves show actor `github-project-automation[bot]`, type `Bot`), and the code's `status_seen` can rely on the event; the Status was restored to Done and the temporary label deleted; Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RECORDED: k a comment typed in the GitHub web editor on #452 came back from the REST comments call with the body exactly `approved` (the edit history of the comment holds `approved` at the creation time 02:55:50Z, so no extra characters or newline were added by the editor); after one edit in the web page (`approved, full stop`) the comment's `lastEditedAt` changed from null to the edit time (02:56:14Z, equal to REST `updated_at`) and the edit history kept the original body, so an edited approval is detectable by `lastEditedAt` and the exact-match rule is safe; author type `User`; Orca 1.4.245-aidev02.9cfecdd30b2a, 2026-11-17
RUN BY OWNER: ironbelly (steps a to j run by an agent on the owner's chat instruction; k posted and edited by the owner in the browser)
