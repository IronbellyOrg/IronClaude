# Requirements Specification: GitHub Issue Watcher (issue #331), Option A

- Status: Draft variant for adversarial review
- Issue: IronbellyOrg/IronClaude#331
- Lens: deployment, observability, runbooks, SLO impact
- Sources: `seed-brief.md` (SB), `enrichment/research-deep.md` (RD), `enrichment/codebase-context.md` (CC)
- Convention: every number not fixed by a source is marked [PROPOSAL]; every assumption about the repo or host is marked ASSUMPTION.

## 1. Purpose and scope

**Purpose.** Replace the manual hand-off of approved issues with a poller that runs inside each person's Coder workspace, polls IronbellyOrg/IronClaude every 5 minutes with that workspace's own `gh` login, and starts one ordinary top-level Claude session per eligible issue with the prompt `/sc:issue --claim <N>` through `orca agent launch` (SB Q1; RD Recommendation).

**Operational framing.** A batch job, not a daemon: each run is one cycle; a `coder_script` cron entry (RD fact 10) gives the cadence; each cycle leaves one audit line and one exit code.

**In scope (mocks only):** package `src/superclaude/cli/issue_watch/`, Click group `superclaude issue-watch` registered after `reflect` in `src/superclaude/cli/main.py`, tests under `tests/issue_watch/`, and design doc `docs/designs/issue-watcher.md` with label setup and an operator runbook. **Out of scope:** anything live; any listener, port, webhook, Action or service; the post-claim pipeline; the Coder template (Section 9).

## 2. Fixed constraints and non-goals

- **D1** Option A, workspace-side pull poller; no listener, inbound port or address registry. IronbellyOrg/Coder#477 is unnecessary under A unless B or C is revisited (SB Q1).
- **D2** Claim-only: the job ends when the session has been asked to run `/sc:issue --claim <N>`; the claim stops at `next-steps.md` (RD fact 1).
- **D3** Only a validated positive integer reaches a session prompt (SB Q2).
- Every repository-scoped `gh` call names IronbellyOrg/IronClaude; `gh` and `orca` run as argv lists, never a shell; the poller is a plain process, never an Orca worker (RD fact 2); no secrets or tokens stored.

**Non-goals:** NG-1 push designs B, C, D (documented alternatives with nine revisit conditions); NG-2 any GitHub write by the poller (GET only; the claim assigns and comments); NG-3 Project writes; NG-4 constraining the launched session (Section 6); NG-5 daemon mode or retry loops inside a cycle.

## 3. Definitions

All are evaluated from projected `gh` JSON; label names default per OD-1.

- **Own login.** Output of `gh api user -q .login` this cycle, matching `^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$`; never cached across cycles.
- **Tagged.** `labels[].name` contains the trigger label by exact, case-sensitive equality.
- **Approved by a human.** (a) the approval label is present; (b) the latest `labeled`/`unlabeled` event for it is `labeled`; (c) its `actor.login` is on the allow-list (OD-2); (d) its `actor.type` is `User`. Only Triage-or-higher accounts can label (RD fact 7).
- **In a Project.** The configured org Project (`--project-owner`, `--project-number`) has an item whose content number equals the issue number and whose repository is `IronbellyOrg/IronClaude`. ASSUMPTION: `gh project item-list --format json` exposes these fields (RD Q8 UNVERIFIED).
- **Backlog.** That item's Status equals the configured name (default `Backlog`) exactly.
- **Intended owner.** Candidate 1 (OD-3): `assignees[].login` contains the own login. Any other assignee excludes the issue (RD shared predicate); unassigned issues are intended for no one.
- **Claimed.** A comment by the own login contains `<!-- sc:issue:claim -->` (`refs/claim.md:29`). A `--jq` projection returns only a boolean; comment bodies never enter the Python process.
- **Eligible issue.** Open AND tagged AND approved AND in the Project AND Backlog AND intended owner AND not claimed AND no dispatch-record state forbids a launch (Section 7).

## 4. Functional requirements

Criteria run with stub `gh` and `orca` recording argv, and a temporary state directory.

- **FR-001** `superclaude issue-watch once` executes exactly one poll cycle and exits.
  *GWT:* Given stubs returning no issues, when `once` runs, then the process exits 0 within the test timeout and the stub `gh` saw exactly one `api user` call.
- **FR-002** The cycle resolves the own login first and makes no other call if it fails.
  *GWT:* Given `gh api user` exits 1, when `once` runs, then exit code is 3, no further `gh` call and no `orca` call is recorded, and the audit line has `result="gh_auth_failed"`.
- **FR-003** Discovery uses `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --json number,labels,assignees,state -L 100`.
  *GWT:* Given any run, then the recorded discovery argv equals that list exactly, and no recorded argv contains `title`, `body` or `comments` as a `--json` field.
- **FR-004** Discovery that returns exactly the limit (100) fails closed.
  *GWT:* Given 100 issues returned, when `once` runs, then exit code is 4, zero launches, audit `result="truncated"`.
- **FR-005** Approval is evaluated from issue events projected to event type, label name, actor login, actor type and time.
  *GWT:* Given the latest approval `labeled` event by a non-listed login, the issue is skipped as `not_approved`; by an allow-listed `User`, it passes.
- **FR-006** Re-labelling moves approval to the latest actor.
  *GWT:* Given approver-labeled, outsider-unlabeled, outsider-labeled, the issue is skipped as `not_approved`.
- **FR-007** Project membership and Backlog status are checked against the configured Project; a Project read failure fails closed for the whole cycle.
  *GWT:* Given `gh project item-list` exits 1 (for example missing `read:project`), then exit code is 3, zero launches, audit `result="project_read_failed"`; given the item has Status `In progress`, then skip reason `not_backlog`.
- **FR-008** The intended-owner filter keeps only issues assigned to the own login.
  *GWT:* Given issue 7 assigned to `other`, issue 8 unassigned, issue 9 assigned to the own login (all otherwise eligible), then only issue 9 is launched; skip reasons `assigned_other` and `unassigned` are recorded.
- **FR-009** An issue already claimed is never launched and its record moves to `claimed`.
  *GWT:* Given a `launched` record for issue 9 and the claim-marker projection returns `true`, then no launch occurs and the record state becomes `claimed`.
- **FR-010** A `pending` record is written and flushed to disk before the launch call.
  *GWT:* Given a stub `orca` that reads `dispatch.json` when invoked, then the stub observes issue 9 in state `pending` with `attempts>=1`.
- **FR-011** A pre-launch re-read (`gh issue view <N> --repo IronbellyOrg/IronClaude --json number,labels,assignees,state`) re-applies the label, state and owner filters; failure removes the `pending` entry without a launch.
  *GWT:* Given discovery shows issue 9 eligible but the re-read shows it closed, then zero launches and audit reason `revalidation_failed`.
- **FR-012** The prompt is built only by `build_claim_prompt(n: int)`, which accepts an `int` (not `bool`) in 1..999999999 and returns `"/sc:issue --claim " + str(n)`.
  *GWT:* Given inputs `9`, `"9"`, `True`, `0`, `-1`, `10**9`, `9.0`, then only `9` returns a string; every other input raises `ValueError` and no launch is recorded.
- **FR-013** The launch argv is `["orca","agent","launch","--agent","claude","--worktree","path:<abs>","--surface","terminal","--prompt",<prompt>,"--json"]`, where `<abs>` is the configured absolute existing directory.
  *GWT:* Given `--worktree /tmp/x` exists, then the recorded argv equals that list with exactly 12 elements; given a relative or missing path, exit code is 2 before any `gh` call.
- **FR-014** Launch outcomes map to record states: success JSON to `launched`; an `agent_session_operation_unknown` reply carrying an `operationId` to `unknown` with the id stored; any other non-zero exit to `failed`.
  *GWT:* For each of the three stub replies, the record holds the expected state and `operation_id` is non-null only for `unknown`.
- **FR-015** An `unknown` record is resolved only with `orca agent launch --retry-launch <operationId> --json`, never a fresh launch.
  *GWT:* Given an `unknown` record with id `op-1`, when the next cycle runs, then the only `orca` argv recorded for that issue contains `--retry-launch op-1` and no `--prompt`.
- **FR-016** Per cycle at most `max_candidates` (10 [PROPOSAL]) issues are examined in least-recently-examined-first order, and at most `max_launches_per_cycle` (1 [PROPOSAL]) launch is made.
  *GWT:* Given 15 eligible issues, then cycle 1 examines 10 and launches 1; cycle 2 examines the 5 unexamined issues first.
- **FR-017** Only one cycle runs at a time per state directory, enforced by a non-blocking `fcntl.flock` on `<state-dir>/lock`.
  *GWT:* Given the lock held by another process, then exit code is 75, no `gh` call, audit `result="lock_held"`.
- **FR-018** A kill switch file `<state-dir>/DISABLED` makes the cycle exit 0 before any external call.
  *GWT:* Given the file exists, then no `gh` or `orca` call is recorded and audit `result="disabled"`.
- **FR-019** `--dry-run` evaluates all filters and writes the audit line but writes no record and makes no launch.
  *GWT:* Given one eligible issue and `--dry-run`, then zero `orca` calls, `dispatch.json` unchanged byte-for-byte, audit `would_launch=[9]`.
- **FR-020** Each cycle appends exactly one JSON line to `<state-dir>/audit.jsonl` (schema in NFR-006), including on every failure exit except a crash.
  *GWT:* For each exit code 0, 3, 4, 6, 75, the file grows by exactly one parseable line whose `exit_code` matches.
- **FR-021** `superclaude issue-watch status` prints the dispatch record and the last audit line, read-only, with `--json` support.
  *GWT:* Given a state directory, then `status` records zero `gh`/`orca` calls, leaves every file's mtime unchanged, and reports `last_cycle_age_seconds`.

## 5. Non-functional requirements

- **NFR-001 Prompt boundary (security).** No byte of issue title, body, comment, label name or login reaches the `--prompt` argument. *Test:* a property test over random `number` values and hostile label/assignee strings asserts every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8}$`.
- **NFR-002 Read-only GitHub (security).** The poller issues only reads. *Test:* every recorded `gh` argv starts with `api user`, `issue list`, `issue view`, `project item-list`, or `api repos/IronbellyOrg/IronClaude/... --method GET`; any other form fails the test.
- **NFR-003 Repo pinning.** Every repository-scoped `gh` argv contains `--repo IronbellyOrg/IronClaude` or the literal path prefix `repos/IronbellyOrg/IronClaude/`; `project item-list` carries `--owner IronbellyOrg`. *Test:* scan of all recorded argv; zero occurrences of `SuperClaude-Org` and of `{owner}`.
- **NFR-004 No shell.** `subprocess.run` is called with a list and `shell=False`. *Test:* the injected runner rejects a `str` argv; a grep test asserts `shell=True` does not appear under `src/superclaude/cli/issue_watch/`.
- **NFR-005 At-most-once.** Per state directory, fresh launches (argv with `--prompt`) per issue never exceed `max_launches` (1 [PROPOSAL]). *Test:* inject a crash after record write, launch call, launch reply and record update in turn; rerun `once` five times; assert at most 1 fresh launch.
- **NFR-006 Observability.** Each audit line holds `ts`, `cycle_id`, `host`, `login`, `exit_code`, `result`, `duration_ms`, `gh_calls`, counts, `skipped` (reason code map), issue-number lists, `rate_remaining`; never issue text. Rotates at 5 MiB [PROPOSAL]. *Test:* schema validation; fixture title `PWNED-TITLE` never appears in `audit.jsonl` or stderr.
- **NFR-007 Fail closed.** Any `gh` failure, timeout, non-JSON reply or truncation before the launch phase yields zero launches. *Test:* table-driven failure injection on each read call.
- **NFR-008 Time budget.** Each subprocess times out at 20 s [PROPOSAL]; no launch starts after 120 s [PROPOSAL] of cycle time, inside the 300 s cadence. *Test:* a sleeping stub yields `result="gh_timeout"`, exit 3.
- **NFR-009 Rate budget.** At most `3 + 3 * max_candidates` calls per cycle (33 [PROPOSAL]), at most 396 an hour, under 8 percent of the 5,000 an hour allowance (RD fact 9); idle cycles make 2 calls. A rate-limit reply ends the cycle with `result="rate_limited"`, exit 3. *Test:* call count with 10 candidates; rate-limit stub.
- **NFR-010 Idempotent cycle.** A second `once` against identical stub state launches nothing. *Test:* direct.
- **NFR-011 Crash-safe state.** Record writes use temp file, `fsync`, `os.replace`; file mode `0600`, directory `0700`. An unparseable record yields exit 5, zero launches, file unchanged; never a silent reset. *Test:* truncated JSON fixture.
- **NFR-012 Footprint.** No new dependency; at most one new session per cycle. *Test:* dependency list unchanged; FR-016.
- **NFR-013 SLO signals [PROPOSAL].** (a) approval-to-`launched` p95 ≤ 10 minutes while the workspace runs; (b) ≥ 99 percent of cycles over 7 days exit 0 or 75; (c) ≥ 95 percent of `launched` records reach `claimed` within the lease. All computable from `audit.jsonl` and `dispatch.json`. *Test:* a helper reduces a fixture log to the three numbers.

## 6. Security model

GitHub content is untrusted; the own login, state directory and configuration are trusted at workspace-user level. The poller holds no token of its own.

| # | Asset | Threat | Control | Residual risk |
|---|---|---|---|---|
| T1 | Launch prompt | Prompt injection from issue text | Fields restricted (FR-003, FR-011); jq projections; `build_claim_prompt` integer-only (FR-012); NFR-001 | The launched claim reads title, body and comments live in a PUBLIC repo (RD fact 5); not solved here |
| T2 | Approval gate | Non-approver applies the approval label | Latest-actor check against allow-list; Triage-or-higher needed to label (FR-005, FR-006) | Compromised approver account; allow-list edited by a writer |
| T3 | Approval gate | Bot or automation applies the label | `actor.type == "User"` required | A human-controlled bot account typed `User` |
| T4 | Approval meaning | Body edited after approval | None in poller (RD Q11 UNVERIFIED) | Approved content can change before claim; claim stays read-and-assign only |
| T5 | Repository target | gh defaults to the upstream parent | Repo pinning (NFR-003) | None known |
| T6 | Host shell | Metacharacters in data | argv lists, `shell=False` (NFR-004) | None known |
| T7 | Issue ownership | Two workspaces of one login both launch | Local record; claim marker | Same-login race (RD Q14); OD-8 |
| T8 | Dispatch record | Tampering or deletion | Mode `0600`; corrupt record fails closed (NFR-011) | Deletion permits a second launch |
| T9 | `gh` token | Scope widened with `read:project` | Poller is GET-only (NFR-002) | Token can still write |
| T10 | Launched session | Broad permissions | None: `orca agent launch` has no permission flag (RD fact 6) | Open (OD-7) |
| T11 | Logs | Issue text leaks into logs | Restricted audit schema (NFR-006); `gh` stderr truncated to 500 bytes [PROPOSAL] | Server messages in truncated stderr |
| T12 | Availability | Flood of tagged issues | Caps (FR-016), truncation fail-closed (FR-004), rate budget (NFR-009) | Legitimate issues delayed |

## 7. Dispatch record and at-most-once semantics

**Why a local record.** The claim has no compare-and-set and leaves the issue in Backlog (RD fact 4); under candidate 1 the issue is already assigned to the own login. Only the record, written before launch, prevents a relaunch before the claim marker appears.

**Location.** `<state-dir>/dispatch.json`, default `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/issue-watch/` [PROPOSAL]. ASSUMPTION: it survives a restart only if the Coder template persists `$HOME` (RD Q15).

**Schema** (`schema_version: 1`, one entry per issue): `issue`; `state` (`pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed`); `login`; `attempts` (launch calls, fresh or retry); `launches` (fresh launches whose outcome was `launched` or `unknown`, so a session may exist); `operation_id` (Orca id, `unknown` only); `created_at`, `updated_at`, `lease_expires_at`, `last_examined_at` (UTC ISO 8601; the last feeds the least-recently-examined order); `last_reason`.

**Parameters** (all [PROPOSAL] from the research plan): `lease_minutes = 60`, `max_attempts = 3`, `max_launches = 1`, `max_candidates = 10`; plus `max_launches_per_cycle = 1` [PROPOSAL, this variant].

**Transitions.**

| From | Event | To | Launch allowed |
|---|---|---|---|
| (none) | eligible, caps allow | `pending` (`attempts += 1`, lease set) | next step |
| `pending` | orca success | `launched` (`launches += 1`) | done |
| `pending` | orca `agent_session_operation_unknown` with id | `unknown` (`launches += 1`) | no |
| `pending` | orca other error | `failed` | no |
| `pending` | found at cycle start (crash between write and reply) | `abandoned`, reason `pending_orphan` | no, never |
| `pending` | pre-launch re-read fails (FR-011) | entry removed | no launch was made |
| `unknown` | `--retry-launch` success | `launched` | no fresh launch |
| `unknown` | `--retry-launch` definite failure | `failed` | no |
| `unknown` | lease expired | `abandoned`, reason `unknown_expired` | no |
| `failed` | next cycle, still eligible, `attempts < max_attempts`, `launches == 0` | `pending` | yes |
| `failed` | `attempts >= max_attempts` | `abandoned`, reason `attempts_exhausted` | no |
| `launched` | claim marker observed | `claimed` | no |
| `launched` | lease expired with no marker | `abandoned`, reason `claim_not_observed` | no |
| any non-terminal | issue closed or no longer intended owner | `abandoned`, reason `ineligible` | no |

`claimed` and `abandoned` are terminal. A fresh launch requires `launches < max_launches`, so at-most-once holds even when Orca's reply is lost; `pending_orphan` prefers a missed dispatch to a double one. Recovering an `abandoned` entry is an operator act: set `DISABLED`, remove the entry, re-enable.

**Scope.** The guarantee is per state directory, not per login. Two workspaces of one login, or a lost directory, can each launch once.

## 8. Repo-side deliverables (testable with mocks)

**Modules** under `src/superclaude/cli/issue_watch/`: `runner.py` (`run_command(argv: list[str], timeout)`, rejects `str` argv); `github.py` (reads, truncation, rate limits); `filters.py` (pure Section 3 predicates; `is_intended_owner()` is the one replaceable routing function); `launch.py`; `state.py` (record, transitions, lock, kill switch); `audit.py`; `cycle.py`; `cli.py`. Registered after `main.add_command(reflect_group, name="reflect")`; no `pyproject.toml` change.

**CLI verb `once`.** Options: `--worktree PATH` (required), `--project-number INT` (required; the sources do not identify the Project), `--project-owner` (default `IronbellyOrg`), `--status-name` (default `Backlog`), `--trigger-label`, `--approval-label`, `--approvers-file`, `--state-dir`, `--dry-run`.

**Exit codes** [PROPOSAL]:

| Code | Meaning | Operator action |
|---|---|---|
| 0 | Cycle complete (any number of launches, including zero, or `disabled`) | None |
| 2 | Usage or configuration error (Click convention) | Fix the scheduler entry |
| 3 | GitHub read failed: auth, scope, timeout, rate limit, non-JSON | Check `gh auth status`, scopes, `result` field |
| 4 | Discovery or Project read truncated | Raise limit or narrow labels; see R3 |
| 5 | Dispatch record unreadable | Inspect and repair the file; never delete blindly |
| 6 | At least one launch ended `failed` | Check Orca runtime and worktree |
| 75 | Lock held by another cycle | None unless repeated; repeated means a hung cycle |

**Tests** under `tests/issue_watch/`: one file per module, `test_cli_e2e.py` (stub executables on PATH, as in `tests/pr_submit/test_conflict_e2e.py`) and `test_security_invariants.py` (NFR-001 to NFR-004). Each FR criterion and each Section 7 row is one test case. **Gates:** `uv run pytest tests/issue_watch/`, `make lint`, `make sync-dev`, `make test`, `make verify-sync`.

**Design doc** `docs/designs/issue-watcher.md` (house format): D1 to D3, options B, C, D with revisit conditions, the Coder#477 statement, and an **operator runbook**:

1. Pre-flight: `gh auth status`; `gh auth refresh -s read:project` if the Project read fails; `orca` on PATH; worktree exists.
2. Label setup (owner-run; `/sc:issue` never creates labels): `gh label create issue-watch:trigger --repo IronbellyOrg/IronClaude` and `gh label create issue-watch:approved --repo IronbellyOrg/IronClaude`.
3. Shadow rollout: run `once --dry-run` on schedule for 24 hours [PROPOSAL]; compare `would_launch` with expectation before removing `--dry-run`.
4. Disable with `touch <state-dir>/DISABLED`; enable by removing it.
5. Exit codes, reason codes, `status --json`; recovering an `abandoned` entry.
6. Staleness: `last_cycle_age_seconds` above 900 [PROPOSAL] means the scheduler is not running.

## 9. Follow-up not built here

- **FU-1 Live slash-command test (blocks enablement).** One owner-run launch on a test issue to confirm a leading `/sc:issue` runs as a slash command (RD Q1, Q2) and to capture real success and `unknown` JSON for the stub fixtures.
- **FU-2 Coder template.** `coder_script` with `cron = "0 */5 * * * *"` running `superclaude issue-watch once` (RD fact 10), plus a persisted state directory if `$HOME` is not.
- **FU-3 Token scope.** Confirm `read:project` (RD Q7) and `--query` (RD Q8).
- **FU-4 Alerting** on staleness or on exit 3, 4, 5 or 6 for three consecutive cycles [PROPOSAL]; sink not chosen.
- **FU-5 SLO measurement** of NFR-013 from two weeks of real logs.
- **FU-6 Session permissions.** Trace whether Orca applies `agentDefaultArgs` (RD Q6); settle OD-7.
- **FU-7 Revisit tracking** against the nine conditions; Coder#477 reopens only if B or C is chosen.

## 10. Open decisions

| ID | Decision | Recommended default | Reason |
|---|---|---|---|
| OD-1 | Label names | `issue-watch:trigger`, `issue-watch:approved` | Namespaced against the nine default labels; anyone may propose, only approvers approve |
| OD-2 | Approver allow-list location | Local login file via `--approvers-file`, shipped with the Coder template; missing or empty means nothing is approved | No extra GitHub read; fails closed. Move to one PR-reviewed repo file if copies drift |
| OD-3 | Intended-owner rule | Candidate 1, already assigned to the own login | Matches the claim's own rule (`claim.md:41-42`); the only race-free candidate; isolated in `is_intended_owner()` |
| OD-4 | Project unreadable | Fail closed; no label-only flag | A silent fallback widens eligibility; Option D is the documented fallback |
| OD-5 | At-most-once parameters | Lease 60 min, 3 attempts, 1 launch, 10 candidates, 1 launch per cycle | Research values; one launch per cycle bounds session bursts and keeps cycles attributable |
| OD-6 | State directory | XDG state path, overridable | Persistence is a Coder template fact (FU-2) |
| OD-7 | Launched-session permission mode | Default interactive mode, never a bypass mode | The session reads untrusted text (T1); prompts keep a human before any write |
| OD-8 | Same login, several workspaces | Scheduler enabled in one workspace per login; `host` in audit | The local record cannot see other workspaces; a shared ledger is a B/C revisit trigger |
| OD-9 | Claim's reads of issue text | Accept as residual under D2 | Same as a manual claim today; changing `/sc:issue` is out of scope |

## 11. Risks

| ID | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | Launch prompt not run as a slash command (RD Q1) | Unknown / nothing works | FU-1 before enablement; `claim_not_observed` surfaces it within one lease |
| R2 | Token lacks `read:project` (RD fact 8) | High today / every cycle exits 3 | Runbook pre-flight; Option D fallback |
| R3 | Project has over 100 items, so `item-list -L 100` always fails closed | Medium / no dispatch | Server-side `--query` if FU-3 confirms it, else limit 500 [PROPOSAL] |
| R4 | Hung cycle overlaps the next | Low / skipped cycles | Lock, timeouts, exit 75 in health SLO |
| R5 | State directory lost on restart | Medium until FU-2 / second launch | `pending_orphan`, claim marker, OD-8 |
| R6 | Scheduler stopped or always failing, unnoticed | Medium / issues wait | `status` staleness, FU-4 |
| R7 | Launched sessions stay open (RD Q21) | Medium / process build-up | One launch per cycle; runbook note |
| R8 | Host Orca ignores the `--retry-launch` rule (RD Q3) | Low / `unknown` never resolves | Lease expiry to `abandoned`, never a fresh launch |
| R9 | Stopped workspace polls nothing (RD fact 10) | Certain / latency | Accepted under D1; B revisit condition |

## 12. Traceability

| Requirement | Source fact |
|---|---|
| FR-001, FR-017, NFR-008, R4 | RD fact 10 (cron); SB Constraints (5 minutes); RD Q15 |
| FR-002, FR-003, NFR-001, T1 | SB D3; RD Security model (own login, fields `number,labels,assignees,state`); RD fact 5 |
| FR-004, FR-007, OD-4, R2, R3 | RD fact 8; RD Q7, Q8 |
| FR-005, FR-006, T2, T3 | RD fact 7; SB Q3 |
| FR-008, OD-3 | RD Intended-owner filter; SB Constraints |
| FR-009 | `refs/claim.md:29` marker |
| FR-010, FR-011, FR-014, FR-016, FR-020, NFR-005, Section 7 | RD fact 4; SB Enrichment (record before launch, re-read, six states, caps, considered map, audit line) |
| FR-012 | RD plan step 3.2; SB D3 |
| FR-013, FR-015, T10, OD-7, R8 | RD fact 6; RD Q6 |
| FR-018, FR-019, FR-021, NFR-006, NFR-007, NFR-012, NFR-013 | Operational additions; SB Success Criteria (observable acceptance) |
| NFR-002, NFR-003, NFR-004, T5, T6 | SB Constraints; CC (injectable runner) |
| NFR-009 | RD fact 9 |
| NFR-010 | SB Success Criteria |
| NFR-011, OD-6, R5, OD-8, T7 | RD Q14, Q15 |
| R1, FU-1, FU-7 | RD Q1; SB Q1 |
