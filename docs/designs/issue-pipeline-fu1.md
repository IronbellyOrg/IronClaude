# Issue pipeline: first live test (FU-1) runbook for the claim handoff (Decision 6 = B)

Status: runbook only. **No step in this document is run by the agent that wrote it.** The owner runs every step, on a throwaway issue the owner wrote, and fills the record at the end. Nothing here claims, starts, merges or posts anything by itself.

This test is the claim-handoff part of FU-1, the first live test of `docs/designs/issue-watcher-setup.md` section 8.5 (the live-test record) and section 14.1 (the live test). It adds preconditions a to k for design B: a person-opened coordinator starts the plan-writing agent as a supervised Orca worker for a watcher-claimed issue. The facts below come from the validation file of the plan package `TASK-WF-planDecision6BFo-20261114-174909` (its section 7 lists a to j); precondition k is new.

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
- A reachable Orca (`orca status` answers) and a person-opened coordinator terminal.
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
- Failure means: if the worker exits, "nothing starts while the coordinator is down" is not enough and the approval wait needs a different design.

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

The owner replaces each `PENDING:` line below with `RECORDED: <letter> <measured value>`, adding the Orca build string from `orca-ide --version` and the date inside each value, and, when the run is done, adds one closing line in the form `RUN BY OWNER: <name>` (the owner's name). Plan B Task 20 checks this section.

PENDING: a worker-start argv and permission flags
PENDING: b worker-start on an existing worktree, one terminal
PENDING: c ask and reply round trip
PENDING: d launch receipt and Dispatch id
PENDING: e plan hash identical on both sides
PENDING: f guard interaction under G1
PENDING: g ask timeout and resume by message id
PENDING: h worker stays in ask while the coordinator is down
PENDING: i worktree reuse when the claim runs twice
PENDING: j GitHub stage facts
PENDING: k web-editor comment round trip and edit time
