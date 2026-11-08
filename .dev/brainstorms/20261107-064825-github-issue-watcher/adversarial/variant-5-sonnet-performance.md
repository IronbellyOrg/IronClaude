---
title: "Requirements: GitHub issue watcher (issue #331), option A, performance and cost-to-serve emphasis"
status: draft variant
issue: IronbellyOrg/IronClaude#331
decisions_fixed: D1 (option A, workspace poller), D2 (claim-only), D3 (validated integer only reaches a prompt)
tags_used: "[PROPOSAL]" = number or name not fixed by the source; "ASSUMPTION" = not verified in the repo; "UNVERIFIED" = carried from the research
---

# Requirements: GitHub issue watcher (option A)

## 1 Purpose and scope

Issues in `IronbellyOrg/IronClaude` are brought into a session by hand. This document specifies a watcher that removes that hand-off: a plain process in each Coder workspace polls GitHub every 5 minutes with the workspace's own `gh` login, selects issues that are tagged, approved by a human, in a Project, in Backlog and meant for that login, and starts one top-level session per issue with the prompt `/sc:issue --claim <N>`.

This variant stresses cost-to-serve. Every requirement is written so that the steady-state cost of an idle poller is a handful of API calls and zero model calls, and so that the only expensive event (a launched session) is bounded by explicit caps.

In scope: the repo-side poller package, its CLI verb, its dispatch record, tests that use mocked `gh`, `orca` and clock, a design doc and setup instructions. Out of scope: anything run live (section 9).

## 2 Fixed constraints and non-goals

Fixed inputs (not reopened by this document):

- **D1** Option A: each workspace polls; no listener, no inbound port, no address registry. Options B and C stay documented alternatives. IronbellyOrg/Coder#477 is unnecessary under A unless B or C is revisited.
- **D2** Claim-only: the watcher ends at a started `/sc:issue --claim <N>`. The claim stops at `next-steps.md`; the pipeline after it stays manual.
- **D3** Only a validated integer issue number reaches a session prompt. No title, body, comment or label text ever does.

Other constraints: every `gh` call names `--repo IronbellyOrg/IronClaude`; nothing touches `SuperClaude-Org`; no secrets in any file; the poller is a plain process, never a worker Task and never run inside a session (`/sc:issue` is on the never-as-worker list); UV only; edits go to `src/superclaude/` then `make sync-dev`.

Non-goals: running the pipeline after the claim; creating labels from code; any write to GitHub by the poller; a central audit store; reacting to events in less than one poll interval; deploying or running anything live from this task.

## 3 Definitions

All names below are configuration values with the stated defaults; defaults are [PROPOSAL] because no trigger or approval label exists today (nine default labels only).

- **own login**: the output of `gh api user -q .login`, read once per cycle.
- **tagged**: the issue state is `open` and its label set contains, by exact case-sensitive match, the trigger label (default `claim-ready`).
- **approved by a human**: the issue carries the approval label (default `claim-approved`) AND the actor of the most recent `labeled` event for that label has `type == "User"` and a login in the approver allow-list AND no later `unlabeled` event for that label exists. An absent, bot, or non-listed actor means not approved.
- **in a Project**: the issue has a Projects v2 item in the configured project (`project_owner`, `project_number`), obtained from that issue's own `projectItems` (not from a scan of the whole Project).
- **Backlog**: that item's single-select field `Status` has the value `Backlog`, exact match. A missing Status is not Backlog.
- **intended owner** (candidate 1, behind one replaceable function `is_intended_owner(snapshot, own_login) -> bool`): the issue's assignee set equals exactly `{own login}`. Unassigned, other-assignee and multi-assignee issues are not owned by this workspace.
- **eligible issue**: tagged AND approved AND in a Project AND Backlog AND intended owner AND `number` is an integer 1..999999999 AND the dispatch record for it is absent or in a re-dispatchable state (section 7) AND it carries no own claim marker.

## 4 Functional requirements

Test seam: every external effect goes through an injected `Runner` (argv list, never a shell) and an injected clock; tests use a recording fake or a stub `gh`/`orca` on PATH.

- **FR-001** The poller shall read its own login once at the start of each cycle with `gh api user -q .login`. AC: Given a mocked login `alice`, When one cycle runs, Then exactly one `gh api user` call is recorded and `alice` is the login used by every later filter; Given the call fails, Then no launch occurs and the exit code is 3.
- **FR-002** The poller shall discover candidates with one `gh issue list` call restricted to `--repo IronbellyOrg/IronClaude --state open --label <trigger> --json number,labels,assignees,state -L 100`. AC: Given any cycle, Then the recorded argv contains those flags and no `title`, `body` or `comments` field name.
- **FR-003** The poller shall fail closed when discovery returns exactly 100 items. AC: Given a mock returning 100 items, Then no launch occurs, the audit line has `truncated=true` and the exit code is 4.
- **FR-004** The poller shall drop every candidate that is not tagged or not assigned exactly to the own login before making any per-candidate call. AC: Given 50 candidates of which 2 are assigned to `alice`, Then at most 2 per-candidate calls are recorded for each later stage.
- **FR-005** The poller shall order surviving candidates least-recently-examined first using the `considered` map and examine at most `max_candidates` (10, [PROPOSAL]) per cycle. AC: Given 25 survivors and cap 10, Then three consecutive cycles examine all 25 with no candidate examined twice before every other has been examined once.
- **FR-006** The poller shall evaluate approval from the issue's events with one `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events` call per examined candidate. AC: Given a `labeled` event by a listed user followed by an `unlabeled` event, Then the issue is not approved and no launch occurs.
- **FR-007** The poller shall reject approval by an actor that is a bot or not in the allow-list. AC: Given the latest `labeled` actor is `mallory` (not listed) or `type=Bot`, Then no launch occurs and the audit line counts one `rejected_approval`.
- **FR-008** The poller shall test Project membership and Backlog status with one GraphQL call per examined candidate that reads that issue's `projectItems` and its `Status` value. AC: Given an item in Status `Todo`, Then not eligible; given no item in the configured project, Then not eligible; given `Backlog`, Then the stage passes.
- **FR-009** The poller shall treat an unreadable Project (missing `read:project`, GraphQL error) as not eligible and exit 3 at the end of the cycle. AC: Given a mocked scope error, Then zero launches and exit code 3.
- **FR-010** The poller shall skip an issue that already carries an own claim marker, detected with a `--jq` filter that emits only a boolean so comment text is never retained. AC: Given the marker present, Then no launch; the recorded state moves to `claimed` (FR-017).
- **FR-011** The poller shall write the dispatch record in state `pending` and flush it to disk before it calls `orca`. AC: Given a fake `orca` that raises, Then the record file exists with `state=pending` and `attempts=1`.
- **FR-012** The poller shall re-read `number,state,labels,assignees` of the chosen issue immediately before launch and abort if any filter now fails. AC: Given the approval label removed between discovery and re-read, Then no launch occurs and the record is deleted or marked `abandoned` with reason `stale`.
- **FR-013** The poller shall build the prompt only through `build_claim_prompt(number)`, which accepts a Python `int` from 1 to 999999999 and returns `"/sc:issue --claim " + str(number)`. AC: Given `"12; rm -rf"`, `"12"`, `12.0`, `True`, `0`, `-3`, `10**9`, Then each raises `ValueError`; given `412`, Then `/sc:issue --claim 412`.
- **FR-014** The poller shall launch with argv `orca agent launch --agent <agent> --worktree path:<abs> --surface terminal --prompt <prompt> --json` as separate argv elements. AC: Given a recorded launch, Then argv is a list, the prompt is one element and no element is shell-joined.
- **FR-015** The poller shall map the launch result to `launched` (success), `unknown` (error code `agent_session_operation_unknown`, saving `operationId`) or `failed` (any other error). AC: One test per outcome asserts the record state and saved `operationId`.
- **FR-016** The poller shall resolve `unknown` only with `orca agent launch --retry-launch <operationId>` and never with a fresh launch. AC: Given a record `unknown` with id `op-1`, When the next cycle runs, Then argv contains `--retry-launch op-1` and not `--prompt`.
- **FR-017** The poller shall move a `launched` record to `claimed` when a later cycle sees the own login as the issue's assignee and an own claim marker. AC: Given such a snapshot, Then `state=claimed` and the issue is never launched again.
- **FR-018** The poller shall start at most `max_launches` (1, [PROPOSAL]) sessions per cycle and at most `max_launches_per_day` (6, [PROPOSAL]) per day. AC: Given 5 eligible issues, Then one `orca` launch is recorded in the first cycle; Given 6 launches already today, Then zero.
- **FR-019** The poller shall take an exclusive non-blocking file lock for the whole cycle. AC: Given the lock held by another process, Then the run makes zero `gh` calls and exits 5.
- **FR-020** The poller shall write exactly one audit line per cycle containing counts and timings but no issue text (NFR-007). AC: Given any cycle, Then one JSON line is appended with the listed keys.
- **FR-021** The poller shall perform no GitHub write. AC: Given any cycle, Then no recorded `gh` argv contains `--method POST|PATCH|PUT|DELETE`, `edit`, `comment`, `create` or `--add-assignee`.
- **FR-022** The poller shall honor a kill switch: if the file `<state_dir>/DISABLED` exists the cycle makes no launch and exits 0 after writing the audit line. AC: Given the file, Then zero `orca` calls.
- **FR-023** The CLI shall expose `superclaude issue-watch once|status|check-config|reset <N>` with exit codes 0 ok, 2 usage or config error, 3 identity/scope/auth failure, 4 truncation, 5 lock held, 6 record store unwritable, 7 launch failed this cycle, 8 rate limited. AC: One test per code.

## 5 Non-functional requirements

**Call budget (the dominant scaling axis).** Calls per cycle: idle = 2 (login, list); worst = 1 + 1 + 10 candidates x 3 (events, Project, marker) + 1 re-read = 33. At 12 cycles an hour that is 24 calls (0.48 percent of a 5,000 an hour allowance) idle and 396 (7.9 percent) worst case, per workspace. The allowance is per login and shared across that login's tokens, so W workspaces on one login cost W x those figures. The cost grows with the number of examined candidates, never with the size of the repository or the Project, which is why FR-008 queries the issue's own `projectItems` instead of listing the Project (a 100-item `gh project item-list` page would silently stop covering a growing Backlog).

- **NFR-001 Security, no shell.** Every subprocess call shall be an argv list with `shell=False`. AC: a test patches `subprocess.run` and asserts a list argument and `shell` falsy for every recorded call.
- **NFR-002 Security, field minimization.** The poller shall request and retain only `number`, `labels`, `assignees`, `state`, event `actor.login`, `actor.type`, `event`, `created_at`, and Project/Status values. AC: a fixture whose issue text contains a prompt-injection string is run; the string appears in no argv, record, log or audit file.
- **NFR-003 At-most-once.** No issue number shall receive two fresh launches while a non-terminal record exists or after state `launched` or `claimed`. AC: run 50 cycles over a fixed mock with a launch that succeeds; exactly one launch is recorded.
- **NFR-004 Idempotent restart.** A process killed at any point between FR-011 and FR-015 shall, on the next cycle, make no second fresh launch. AC: parametrized fault injection after each step; fresh launches never exceed 1.
- **NFR-005 Call cap.** One cycle shall make at most 35 `gh` calls ([PROPOSAL]) and abort remaining examinations when reached. AC: with 100 mocked candidates, the recorded `gh` call count is at most 35.
- **NFR-006 Rate limits.** On an HTTP 403 or 429 rate-limit signal the cycle shall stop calling GitHub, launch nothing, record `rate_limited=true` and exit 8; the next cycle runs on schedule with no retry storm. AC: mock rate-limit on call 3; exactly 3 calls recorded.
- **NFR-007 Observability.** The audit line shall contain `ts, cycle_id, login, discovered, examined, eligible, launched, rejected_approval, gh_calls, duration_ms, truncated, rate_limited, exit_code` and `status` shall print the last audit line and every non-terminal record. AC: schema test over all exit paths.
- **NFR-008 Failure handling.** Every unparseable `gh` or `orca` output, timeout, or missing executable shall result in no launch for the affected issue (fail closed). AC: one test per failure type.
- **NFR-009 Cycle time.** A cycle shall finish within 120 seconds ([PROPOSAL]); each external call has a 20 second timeout ([PROPOSAL]). AC: a fake clock with a hanging call yields a timeout failure and exit within 120 s of fake time.
- **NFR-010 Latency.** For a running workspace, the time from approval to launch shall not exceed one poll interval plus one cycle time (5 min + 120 s, [PROPOSAL]), except where caps in FR-018 defer it. AC: simulated clock test with approval at an arbitrary offset.
- **NFR-011 Cost, zero model calls.** The poller shall make no model or LLM call; its only paid effect is the launched session. AC: import check that the package imports no model client module; the dependency list is unchanged.
- **NFR-012 Cost, launch bounds.** Launched-session spend shall be bounded by FR-018: at most 1 per cycle and 6 per day per workspace ([PROPOSAL]), so worst-case daily session count equals the daily cap regardless of how many issues are approved. AC: FR-018 tests.
- **NFR-013 State bounds.** Records in a terminal state (`claimed`, `abandoned`) older than 30 days ([PROPOSAL]) shall be pruned, and `considered` shall hold at most 1,000 entries. AC: seeded fixtures, assert counts after one cycle.
- **NFR-014 No secrets in state.** State files and audit lines shall contain no token or environment value. AC: scan of all written files for the fixture token string finds nothing.

## 6 Security model

| Asset | Threat | Control | Residual risk |
|---|---|---|---|
| Session prompt | Issue title or body carries instructions that reach the prompt | D3, FR-013: only `str(int)` is used; text fields are never requested (NFR-002) | None for the prompt |
| Launched session | The claim reads title, body and comments live in a PUBLIC repo, so injected text can steer the session | Poller launches only issues approved by a listed human (FR-007); kill switch (FR-022); caps (FR-018) | Stated, not solved. Integer-only protects the prompt, not the session. Permission mode of the session is not settable by `orca agent launch` (open decision O-6) |
| Approval signal | A non-privileged account or bot adds the approval label | Latest `labeled` actor must be `User` and in the allow-list; Triage is the lowest role that can label | An allow-listed account can be compromised; a body edit after approval is not detected (UNVERIFIED) |
| Approval signal | Label removed after approval, before launch | FR-006 unlabeled check, FR-012 pre-launch re-read | Window between re-read and `orca` call (seconds) |
| Dispatch record | Local tamper or deletion causes a re-launch | File mode 0600 in a private dir; atomic replace; an existing own claim marker (FR-010) and assignee (FR-017) still block a re-claim | A user of the same workspace can already run the claim by hand; tampering gives no new capability |
| GitHub token | Excess scope | Only `read:project` plus the existing `gh` login scopes; poller issues no write (FR-021) | Token scope not verified (O-3) |
| Cost budget | Label spam makes many sessions | Per-cycle and per-day caps; allow-list; the poller itself makes no model call | Up to the daily cap of sessions per workspace |
| Duplicate claim | Two workspaces with one login, or a race between two logins | Intended-owner rule requires exact single assignee; record before launch | Same-login multi-workspace double claims remain possible (UNVERIFIED); race window is the claim's read-check-assign gap |
| Execution context | Poller runs inside a worker | Spec requires a plain process; `status` and `once` print a warning and exit 2 if an Orca worker environment marker is present (ASSUMPTION: such a marker exists; otherwise this requirement is dropped) | Not enforceable in the repo |

## 7 Dispatch record and at-most-once semantics

Storage: one file per issue, `<state_dir>/records/<N>.json`, written by write-to-temp then `os.replace`, mode 0600; plus `considered.json`, `audit.jsonl`, `lock` and the optional `DISABLED`. `state_dir` defaults to `~/.superclaude/issue-watch/` (ASSUMPTION: `$HOME` persists across workspace restarts; if not, the Coder template must provide a persisted path).

Fields: `number`, `state`, `attempts`, `launches`, `operation_id`, `approval_actor`, `created_at`, `updated_at`, `lease_expires_at`, `reason`.

| State | Meaning | Re-dispatchable by the poller |
|---|---|---|
| `pending` | Written before `orca` is called | Only after its lease expires, and then it resolves to `unknown` (the outcome is not known) |
| `launched` | `orca` confirmed the session started | No |
| `unknown` | Launch outcome unconfirmed (`agent_session_operation_unknown`, or a crash after `pending`) | Only via `--retry-launch <operation_id>`; without an id it goes to `abandoned` |
| `failed` | `orca` returned a definite error, no session started | Yes, while `attempts < max_attempts` and backoff elapsed |
| `abandoned` | Attempts exhausted, lease expired with no claim, or stale | No; operator runs `issue-watch reset <N>` |
| `claimed` | Own assignee and own marker seen | No (terminal) |

Transitions: absent to `pending` (FR-011); `pending` to `launched`, `unknown` or `failed` (FR-015); `unknown` to `launched` or `failed` through `--retry-launch` (FR-016); `failed` to `pending` (new attempt); `launched` to `claimed` (FR-017) or, when `lease_expires_at` passes with no claim, to `abandoned` with reason `lease_expired`; any non-terminal state to `abandoned` on cap exhaustion.

Parameters, all [PROPOSAL]: `lease` 60 minutes; `max_attempts` 3; `max_launches` 1 per cycle; `max_launches_per_day` 6; `max_candidates` 10; failed-launch backoff 10 minutes. The source fixes none of them except the 5 minute poll interval.

Cost rationale for the bias: a duplicate launch costs a full session, while a missed launch costs one operator `reset` and a delay, so every ambiguous state resolves toward not launching.

## 8 Repo-side deliverables testable with mocks

Modules under `src/superclaude/cli/issue_watch/` (new package, house pattern of `src/superclaude/pr_submit/`):

- `runner.py`: `CommandResult`, `Runner` protocol, `run_command(argv, timeout)` using `subprocess.run` with an argv list.
- `github.py`: read-only layer (login, list, events, Project/Status, claim-marker boolean), fixed field lists, `--repo IronbellyOrg/IronClaude`, truncation detection.
- `select.py`: pure functions for tagged, approved, Backlog and `is_intended_owner`, plus least-recently-examined ordering.
- `record.py`: record store, atomic write, lease logic, pruning, lock.
- `launch.py`: `build_claim_prompt`, `launch`, `retry_launch`, outcome mapping.
- `cycle.py`: the cycle with call-count budget, caps, audit line.
- `cli.py`: Click group `issue-watch` (`once`, `status`, `check-config`, `reset`), registered in `src/superclaude/cli/main.py` with `main.add_command(issue_watch, name="issue-watch")`.

Tests under `tests/issue_watch/`: `test_prompt.py` (FR-013 fuzz), `test_select.py`, `test_record.py` (state machine, crash injection, NFR-003/004), `test_cycle.py` (FR-001..FR-022 with recording fake runner, call-count NFR-005, fake clock NFR-009/010), `test_cli.py` (exit codes), `test_e2e_stub.py` (stub `gh` and `orca` executables on PATH, as `tests/pr_submit/test_conflict_e2e.py` does), `test_no_text.py` (NFR-002 injection fixture, NFR-014 scan).

Documents: `docs/designs/issue-watcher.md` (house format: Status, Issue, Branch, Source of truth, Produced by, numbered sections; records D1 to D3, B and C as alternatives with revisit conditions, and the section 5 call-budget table). Setup instructions inside it: `gh label create` lines for the trigger and approval labels with `--repo IronbellyOrg/IronClaude`; the `read:project` token scope; the approver allow-list file; a `coder_script` cron line `cron = "0 */5 * * * *"` (six fields, seconds first) for the Coder repo to adopt; one poller per `gh` login.

## 9 Follow-up not built here

Installing the cron entry in the Coder template; persisting `state_dir` in the template; the owner-run live launch test; a permission-mode decision for launched sessions; B or C and Coder#477 only if a revisit condition occurs; post-claim pipeline (`--claim --pipeline`, design only); conditional-request (ETag) support to cut call cost further (UNVERIFIED that `gh api` passes `If-None-Match` and that a 304 is free); a per-actor repository-permission check replacing the static allow-list.

## 10 Open decisions

- **O-1 Label names.** Default `claim-ready` (trigger) and `claim-approved` (approval). Reason: two labels let the trigger be set by anyone with Triage while approval is checked by actor, and they are visible in the default label UI.
- **O-2 Approver allow-list location.** Default: a plain-text file path from config, one login per line. Reason: zero extra API calls per cycle; the alternative (a permission lookup per distinct actor) adds up to 10 calls and is listed as follow-up.
- **O-3 Project read.** Default: per-issue `projectItems` query with `read:project`; fail closed if the scope is missing. Reason: cost scales with candidates, not Project size; the label-only fallback would change the meaning of "Backlog", so use hybrid option D before it.
- **O-4 Intended owner and same-login workspaces.** Default: candidate 1 (exact single assignee), and one poller per login by setup instruction. Reason: the claim already stops on another login; unassigned first-come is the racy one; N pollers on one login multiply API cost by N and widen the double-claim window.
- **O-5 Caps.** Default as in section 7. Reason: they cap spend at 6 sessions a day per workspace; raise only on evidence from the audit lines.
- **O-6 Permission mode of launched sessions.** Default: no override; require one owner-run live test of leading `/sc:issue` before the cron entry is enabled. Reason: `orca agent launch` has no permission flag and the slash-command behaviour is UNVERIFIED.
- **O-7 Backlog drain rate.** Default `max_launches` = 1. Reason: 10 approved issues take about 50 minutes to start, but a burst of 10 sessions is the largest avoidable spend and review load.
- **O-8 Where state lives.** Default `~/.superclaude/issue-watch/`. Reason: ASSUMPTION that `$HOME` persists; if not, a persisted path is required before enabling.

## 11 Risks

- **R-1** Launch does not run `/sc:issue` as a slash command; sessions start and idle (cost without value). Mitigation: O-6 live test; `launched` without claim goes to `abandoned` after the lease.
- **R-2** Shared per-login allowance exhausted by many pollers; NFR-005 and NFR-006 bound it per workspace but not across workspaces.
- **R-3** Stopped workspaces poll nothing; approved issues wait (accepted, D1).
- **R-4** Lost state directory causes a re-launch between launch and claim; bounded by the daily cap and, once claimed, blocked by the marker.
- **R-5** GraphQL field names for `Status` differ from the assumed shape (UNVERIFIED); the stage then fails closed and exits 3.
- **R-6** Started sessions stay open after the claim, so tabs and processes accumulate to at most the daily cap per workspace.
- **R-7** Late research edits F1, F2, B1, B2 are unverified by a further review.

## 12 Traceability

Keys: SB = seed brief (section name); RF-n = verified fact n in `enrichment/research-deep.md`; RQ-n = its UNVERIFIED item n; CC = `enrichment/codebase-context.md`.

| Requirement | Source |
|---|---|
| FR-001, NFR-002 | SB Enrichment (fields read; own login each cycle); research-deep security model |
| FR-002, FR-003, FR-008, FR-009 | RF-8 (`read:project`, default 30 items, `-L 100`, fail closed on truncation); RQ-7, RQ-8 |
| FR-004, FR-005, FR-006, FR-007 | SB Enrichment (five filters, `considered` map); RF-7 (Triage, `labeled` actor) |
| FR-010, FR-017 | SB Enrichment (claim-marker check); RF-4 (claim reads, checks, assigns) |
| FR-011, FR-012, NFR-003, NFR-004, section 7 | SB Enrichment (record before launch, states, [PROPOSAL] values); RF-4 |
| FR-013, NFR-001, NFR-002 | D3; RF-5 (integer check only inside the session) |
| FR-014, FR-015, FR-016 | RF-6 (`orca agent launch` contract, `--retry-launch`); RQ-1, RQ-2, RQ-3 |
| FR-018, NFR-012 | SB Enrichment (caps, [PROPOSAL]); cost emphasis of this variant |
| FR-019, NFR-009 | RF-10 (cron overlap, RQ-15) |
| FR-020, NFR-007 | SB Enrichment ("one audit line") |
| FR-021 | D2; SB Constraints (no write needed; claim does the assign) |
| FR-022, FR-023 | variant addition (operator control); CC (CLI registration pattern in `main.py`) |
| NFR-005, NFR-006, NFR-010 | RF-9 (5,000 an hour per user, shared across tokens); SB Enrichment (0.24 percent per call type) |
| NFR-011 | RF-2 (poller is a plain process), D1 |
| NFR-013, NFR-014 | variant addition; SB Constraints (no secrets) |
| Section 6 rows | RF-2, RF-5, RF-6, RF-7; RQ-6, RQ-11, RQ-14 |
| Section 8 | CC (house patterns, `tests/pr_submit/test_conflict_e2e.py`, `origin_repo.py`); research-deep plan steps 1.1 to 7.1 |
| Section 9, O-6, O-8 | RF-10, RQ-1, RQ-6, RQ-15; D1 note on Coder#477 |

