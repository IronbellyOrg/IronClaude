# Requirements Specification: GitHub Issue Watcher (issue #331), Option A

- **Status:** requirements draft (brainstorm variant, analyzer focus: root cause and evidence)
- **Issue:** IronbellyOrg/IronClaude#331
- **Fixed inputs:** D1 option A (workspace-side poller), D2 claim-only, D3 integer-only prompt
- **Sources:** SB `seed-brief.md`; RD `enrichment/research-deep.md` (facts RD-F1..F10); CC `enrichment/codebase-context.md`; RR `RESEARCH-REPORT-issue-watcher.md` (authoritative)
- **Marking:** [PROPOSAL] = no source fixes it; ASSUMPTION = relied on, unverified by any source; [UNVERIFIED] = unverified in the research

## 1. Purpose and scope

### 1.1 Root-cause statement

The manual hand-off (SB) reduces to three missing mechanisms:

| ID | Root cause | Evidence | Design consequence |
|---|---|---|---|
| RC1 | No "ready" signal | Default labels only, no Project code (RD-F7) | Define it and verify who set it |
| RC2 | The claim routes to whoever runs it | Assigns `@me`, refuses other assignees (`refs/claim.md:41-42`) | Start only claims meant for the own login |
| RC3 | No at-most-once start | Check-then-act, issue stays in Backlog (RD-F4) | Own dispatch record plus the claim's marker |

### 1.2 Scope

In scope: `superclaude issue-watch once`, run every 5 minutes in a workspace: read GitHub with the own `gh` login, select eligible issues, record, start one top-level session via `orca agent launch` with prompt `/sc:issue --claim <N>`, audit each decision. All testable with mocked `gh`, `git`, `orca`. Out of scope: live runs, the scheduler entry, the post-claim pipeline, B and C.

## 2. Fixed constraints and non-goals

- C1 (D1): pull only, own `gh` login, no listener, port or registry (SB Q1).
- C2 (D2): the job ends when the claim session starts; the claim stops at `next-steps.md` (RD-F1).
- C3 (D3): the only issue-derived launch text is a validated positive integer (SB Constraints).
- C4: every repository-scoped `gh` call names `IronbellyOrg/IronClaude`, never gh's default repo (SB Constraints).
- C5: the session is top-level, started by a plain process, never an Orca worker (RD-F2, `WORKER-CONTRACT.md:23`).
- C6: nothing deployed, scheduled or launched live; C7: source under `src/superclaude/`, UV only, no secrets.

Non-goals: NG1 no GitHub write by the poller (a second writer without compare-and-set is unsafe, RD-F4); NG2 no post-claim pipeline; NG3 no B or C, so IronbellyOrg/Coder#477 is unnecessary unless they are revisited (SB Q1); NG4 no constraint on the launched session (Section 6); NG5 no wake-up of a stopped workspace.

## 3. Definitions

No definition reads title, body or comment text. "Snapshot" = `gh issue view <N> --repo IronbellyOrg/IronClaude --json number,state,labels,assignees`. "Own login" = `gh api --method GET user -q .login`, read each cycle, accepted only if it matches `^[A-Za-z0-9][A-Za-z0-9-]*$` [PROPOSAL].

| Term | True only if | Fails closed when |
|---|---|---|
| **Tagged** | Snapshot `labels` contains the trigger label (exact match) and `state` is `OPEN` | snapshot unreadable |
| **Approved by a human** | Snapshot has the approval label, AND over the complete REST event list the latest `labeled`/`unlabeled` event for that label is `labeled`, AND its `actor.login` is in the approver allow-list | events truncated (`E-GH-TRUNCATED`), allow-list missing or empty (`E-NO-APPROVERS`), no matching event |
| **In a Project** | The number appears in `gh project item-list <P> --owner <O>` discovery output and the item's content repository is `IronbellyOrg/IronClaude` | repository unreadable |
| **Backlog** | That item's Status equals `Backlog` exactly | status absent |
| **Intended owner** | Snapshot `assignees` is exactly `[own login]` (routing candidate 1) | empty, several, or another login |
| **Eligible issue** | All five above, AND no own-login comment contains `<!-- sc:issue:claim -->` (complete list), AND the dispatch record permits a launch (Section 7), AND a second snapshot just before launch is unchanged | any read fails, truncates, or changes |

Why: any Triage-or-higher account can label (RD-F7), so only the event `actor` proves the approver, and the latest event closes "approved, then removed". Routing lives in one replaceable function, `is_intended_owner` (OD-1).

## 4. Functional requirements

Tests use `FakeRunner` (records argv, exits 99 on an unscripted call) for `gh` and `git`, `FakeOrca`, a `tmp_path` state file and an injected clock.

| ID | Requirement | Given / When / Then |
|---|---|---|
| FR-001 | `superclaude issue-watch once` is registered in `src/superclaude/cli/main.py`. | Given the package, when `CliRunner` runs `--help`, then exit 0 and `issue-watch` is listed. |
| FR-002 | Before any GitHub call, `--worktree-path` must be absolute with `origin` = `IronbellyOrg/IronClaude`. | Given a SuperClaude-Org origin, when `once` runs, then exit 1, `E-WRONG-ORIGIN`, zero `gh` and `orca` calls. |
| FR-003 | The own login is read each cycle, never from configuration. | Given `gh api user` returns `alice` then `bob`, when two cycles run, then cycle 2 compares against `bob`. |
| FR-004 | Discovery is one Project query (`-L 100`, `--jq` projection) keeping only `int` 1..999999999. | Given numbers `[12, "13", 0, 3.0, 1000000000]`, when discovery runs, then candidates are `[12]`, four `dropped`. |
| FR-005 | Discovery fails closed on possible truncation. | Given exactly 100 items, when discovery runs, then exit 2, `E-GH-TRUNCATED`, zero `orca` calls [PROPOSAL]. |
| FR-006 | The five filters run in order and the first failing one is named. | Given five fixtures each failing one filter, when the cycle runs, then each `reason` names it and nothing launches. |
| FR-007 | Approval uses the latest `labeled`/`unlabeled` event of the approval label. | Given labeled(approver), unlabeled, labeled(non-approver), when the cycle runs, then reject `approval-actor-not-allowed`. |
| FR-008 | A full raw page at the page cap rejects the issue. | Given `max_pages` full pages of events, when the cycle runs, then reject `approval-unverifiable`, no launch. |
| FR-009 | An own claim marker comment sets `claimed`, even with no record. | Given an empty state file and an own marker comment, when the cycle runs, then no `orca` call and state `claimed`. |
| FR-010 | The entry is written `pending` before the launch call. | Given an eligible issue, when `FakeOrca` reads the state file, then it holds `pending`, `attempts` 1. |
| FR-011 | A changed second snapshot aborts the launch. | Given a second assignee appears, when the cycle runs, then `changed-before-launch` and no `orca` call. |
| FR-012 | Launch argv is exactly `[<orca>, "agent", "launch", "--agent", "claude", "--worktree", "path:<abs>", "--surface", "terminal", "--prompt", "/sc:issue --claim <N>", "--json"]`. | Given issue 331, when launching, then the recorded argv equals the list and `--prompt` is `/sc:issue --claim 331`. |
| FR-013 | `build_claim_prompt` accepts only an `int` matching `^[1-9][0-9]{0,8}$`. | Given `0, -1, True, 3.0, None, "331", "331; echo x", 1000000000`, then `ValueError`; given `331`, `/sc:issue --claim 331`. |
| FR-014 | Orca is resolved by probing `orca-ide` then `orca` with `skills list --json`, accepting only the `orca-cli` topic. | Given `orca` answers non-JSON and no other candidate, when resolving, then `E-ORCA-NOT-FOUND`, zero launches. |
| FR-015 | Exit 0 maps to `launched`; `agent_session_operation_unknown` to `unknown`+id; timeout to `unknown`+null; anything else to `failed`. | Given `FakeOrca` modes `ok`, `unknown`, `timeout`, `error`, then those four states. |
| FR-016 | `unknown`+id is retried after the lease only with `--retry-launch <id>` from the stored `launch_cwd`. | Given `unknown` id `op-1` past the lease, when the cycle runs, then the only argv is FR-012 plus `--retry-launch op-1`. |
| FR-017 | At most `max_launches` launches and `max_candidates` examined, least-recently-examined first, after local skips. | Given 15 rejected issues and eligible 99, cap 10, when two cycles run, then 99 launches by cycle 2. |
| FR-018 | `--dry-run` reads but writes no record and launches nothing. | Given an eligible issue, when `--dry-run` runs, then `would-launch`, no state file, zero `orca` calls. |
| FR-019 | A held lock exits 0 with no external call. | Given `<state-file>.lock` held, when `once` runs, then exit 0 and an empty call log. |
| FR-020 | Each decision prints one JSON line: `ts`, `mode`, `own_login`, `issue`, `decision`, `reason`, `approver`, `approval_event_id`, `operation_id`, `attempts` [PROPOSAL]. | Given one launch and one rejection, then two objects with exactly those keys plus the summary line, and no fixture title, body or comment string. |
| FR-021 | Exit 0 completed; 1 usage, config, origin or save error; 2 login or discovery failure; 3 any `failed`, `unknown` or `abandoned` [PROPOSAL, RR step 5.3]. | Given each condition, then the matching exit code. |
| FR-022 | `--label-only` replaces discovery with `gh issue list --repo IronbellyOrg/IronClaude --label <trigger> --assignee @me --state open --json number --limit 100`, with `mode: "label-only"`. | Given `--label-only`, then no `project item-list` argv and every line has that mode. |

## 5. Non-functional requirements

| ID | Requirement | Acceptance |
|---|---|---|
| NFR-001 | No built argv contains a GitHub write (`edit`, `comment`, `create`, `-X`, `--add-assignee`, or a `--method` other than `GET`). | A session-scoped assertion over all recorded `gh` argv finds none. |
| NFR-002 | No `gh` read returns title, body or comment text: `--json` lists exclude them and other reads use `--jq` inside `gh`. | A hostile title `"; rm -rf ~ #` appears in no parsed value, audit line or argv. |
| NFR-003 | Every subprocess is an argv list with `shell` false. | Monkeypatched `subprocess.run` asserts this for every call. |
| NFR-004 | Every repo-scoped call carries `--repo IronbellyOrg/IronClaude` or a `repos/IronbellyOrg/IronClaude/` path; `api user` and `project item-list --owner` are exempt. | No argv contains `SuperClaude-Org` or `{owner}`. |
| NFR-005 | Per workspace, an issue launches at most once per lease, at most `max_attempts` in total, never after `claimed` or `abandoned`. | The Section 7 scenarios assert exact `orca` call counts. |
| NFR-006 | Two runs with no GitHub change inside the lease add no launch and leave the record unchanged except `considered`. | Byte comparison with `considered` removed. |
| NFR-007 | A cycle makes at most `2 + 4 × max_candidates + extra pages` `gh` calls, no retry or sleep [PROPOSAL]. | 10 single-page candidates give at most 42 calls. |
| NFR-008 | One audit line per examined issue, one final `{"summary": ...}` line; diagnostics to stderr. | Line count equals examined issues; the last line parses as the summary. |
| NFR-009 | A per-issue read error skips the issue; a login or discovery error gives exit 2; a record-save error aborts with exit 1. | Each scripted failure gives its code and zero `orca` calls. |
| NFR-010 | A corrupt state file loads as empty and is replaced atomically (`os.replace`); the marker still blocks relaunch. | Given `{bad` and a marker, no launch and the new file parses. |
| NFR-011 | A mocked 10-candidate cycle runs in under 2 s [PROPOSAL]. | Timed test. |
| NFR-012 | At the default `max_launches` 1, at most 12 new sessions an hour [PROPOSAL]. | The FR-017 cap test. |
| NFR-013 | Only `commands.py` imports outside the standard library (`click`). | AST import test like `tests/skills/test_issue_repo_resolution.py`. |

## 6. Security model

Option A has no inbound surface; threats enter through read data or the started session.

| # | Threat | Control | Residual |
|---|---|---|---|
| T1 | Issue text injected into the launch prompt | D3 prompt builder; no text read (NFR-002); no shell (NFR-003) | None at the prompt |
| T2 | Non-approver applies the approval label | Latest `labeled` actor on the allow-list | A compromised approver account |
| T3 | Approval read from truncated events | Fail closed at the page cap (FR-008) | Very long histories need manual handling |
| T4 | Body edited after approval to instruct the session; the claim reads text live in a PUBLIC repo (RD-F5) | None here; edit detection is [UNVERIFIED] (Q11) | **Open and material**: the integer protects the prompt, not the session (OD-8, OD-9) |
| T5 | Session runs with permissions skipped; no permission flag exists (RD-F6) | Live check Q6 before the schedule (OD-8) | Open until Q6 |
| T6 | gh default resolves to upstream; same number in another repo | `--repo` pin, item repository check, origin check (FR-002) | None known |
| T7 | `orca` is the GNOME screen reader | `orca-cli` probe (FR-014) | None known |
| T8 | Workspace owner differs from the `gh` login | Login read each cycle; claim uses the same `@me` | Owner-equals-login [UNVERIFIED] (Q16) |
| T9 | Allow-list emptied or edited | Missing or empty is `E-NO-APPROVERS`, exit 1 | Local trust: a home-directory writer can add approvers |
| T10 | Lost record or reply starts a second session | Section 7 | Same login in two workspaces (OD-2) |
| T11 | Secret written to state or audit | Only keys, states, ids, logins, times stored; no token read | None known |

Authorization basis (no existing category, RR step 1.6): the allow-listed approver's label authorizes exactly the claim's own writes; the owner confirms (OD-9).

## 7. Dispatch record and at-most-once semantics

### 7.1 What can and cannot be guaranteed

Assignment has no compare-and-set (RD-F4), so the guarantee is **at most one launch per workspace per issue per lease, at most `max_attempts` in total**, plus best-effort cross-workspace exclusion (owner filter, marker, re-read). The marker is the claim's last write; the local record covers the gap.

### 7.2 Record shape

`--state-file`, default `~/.local/state/superclaude/issue-watch/dispatched.json` [PROPOSAL; `$HOME` persistence [UNVERIFIED], Q15], locked with non-blocking `fcntl.flock` on `<state-file>.lock`. Key `IronbellyOrg/IronClaude#<N>`; fields `state`, `attempts`, `first_at`, `last_at`, `operation_id`, `launch_cwd`, `approver`, `approval_event_id`, `detail`; plus a `considered` map of last-examined times.

### 7.3 States and transitions

| From | Event | To |
|---|---|---|
| (none) | eligible | `pending`, written before the call |
| `pending` | exit 0 / unknown+id / timeout / refusal | `launched` / `unknown`+id / `unknown` / `failed` |
| any | own marker found | `claimed` (terminal) |
| `launched`, `failed` | lease expired (failed: next cycle), no marker, attempts left | new launch, `attempts + 1` |
| `unknown`+id | lease expired, attempts left, same `launch_cwd` | `--retry-launch <id>`; else `abandoned` |
| `unknown`, no id | lease expired | `abandoned` (never a fresh launch) |
| any non-terminal | `attempts >= max_attempts` | `abandoned` (terminal, exit 3) |

A `pending` entry at cycle start is treated as `launched` (the process may have died after the start). A newer approval event is reported `re-approved` and does not reset `attempts` (OD-6).

### 7.4 Parameters

Fixed: poll interval 5 minutes (the issue); discovery `-L 100` (default 30, RD-F8). [PROPOSAL]: lease 60 minutes, `max_attempts` 3, `max_launches` 1, `max_candidates` 10, `max_pages` 5 of 100, fail closed at 100 discovered items, `gh` timeout 60 s, `orca` timeout 120 s.

Lease rationale: the lease must exceed launch-to-marker time so a running claim is not relaunched; 60 minutes exceeding a normal claim run is an ASSUMPTION until the live test measures it.

## 8. Repo-side deliverables (testable with mocks)

### 8.1 Modules (all NEW, package `src/superclaude/cli/issue_watch/`)

| Module | Responsibility |
|---|---|
| `__init__.py` | Lazy export of `issue_watch_group` |
| `runner.py` | Injectable argv-list subprocess seam (`Runner`, `CommandResult`, `CommandError`) |
| `models.py` | `REPO = "IronbellyOrg/IronClaude"`, `MAX_ISSUE_NUMBER`, frozen data types |
| `github.py` | Read-only `gh` layer: `whoami`, `discover_project`, `discover_label_only`, `snapshot`, `label_events`, `own_claim_comment_ids` |
| `selection.py` | Pure filters: `is_intended_owner`, `is_approved`, `load_approvers` |
| `launch.py` | `build_claim_prompt`, `check_worktree_origin`, `resolve_orca`, `launch_claim` |
| `state.py` | `DispatchStore`, atomic save, `poll_lock`, `may_dispatch` |
| `cycle.py` | `run_cycle` |
| `commands.py` | Click group, `once`, exit codes |

Registration: one deferred-import `main.add_command(issue_watch_group, name="issue-watch")` in `src/superclaude/cli/main.py`; no `pyproject.toml` change and no `.claude/` mirror (CLI code is not mirrored).

### 8.2 CLI verb

`superclaude issue-watch once --worktree-path PATH --trigger-label TEXT --approval-label TEXT --approvers-file PATH (--project-owner TEXT --project-number INT | --label-only) [--state-file PATH] [--max-candidates N] [--max-launches N] [--max-attempts N] [--lease-minutes N] [--dry-run]`. No other verb.

### 8.3 Tests (`tests/issue_watch/`)

`conftest.py` (`FakeRunner`; `FakeOrca` modes `ok`, `error`, `unknown`, `timeout`, `not_orca`), `test_runner.py`, `test_launch.py`, `test_selection.py`, `test_github_reads.py`, `test_state.py`, `test_cycle.py`, and `test_cli_once.py` with one PATH-stub end-to-end run like `tests/pr_submit/test_conflict_e2e.py`. Fixtures for `project item-list` and the Orca reply carry `_assumed_shape` naming Q8 or Q2.

### 8.4 Design doc and setup

`docs/designs/issue-watcher.md` in the format of `docs/designs/sc-issue-command.md`, recording D1-D3, the Coder#477 statement, Sections 3, 6 and 7, the UNVERIFIED list and the live-test checklist (written, not run). Setup: `gh label create <name> --repo IronbellyOrg/IronClaude` for both labels; approvers file format (one login per line); `gh auth refresh -s read:project`; a `coder_script` cron example marked as Coder-repo work. Gates: `uv run pytest tests/issue_watch/`, `make lint`, `make test`.

## 9. Follow-up not built here

- F1 (Coder repo, after F3): `coder_script` cron running `superclaude issue-watch once ...` every 5 minutes.
- F2 (Coder repo, if Q15 says `$HOME` is not persisted): a persisted state path.
- F3 (owner, real workspace, before F1): live test of slash-command `--prompt` (Q1), reply shape (Q2), `--retry-launch` (Q3), permission mode (Q6), `read:project` (Q7), `status:Backlog` query (Q8).
- F4 (Coder repo): close or re-scope IronbellyOrg/Coder#477, unnecessary under A unless B or C is revisited.
- F5: options B and C, only on one of the nine revisit conditions (RR Section 6).
- F6: post-claim pipeline (`--claim --pipeline`), a separate decision.
- F7 (Orca or Claude Code configuration): a constraint on the launched session, after Q6.

## 10. Open decisions

| ID | Decision | Recommended default | Reason |
|---|---|---|---|
| OD-1 | Routing rule | Candidate 1: assigned to the own login only; a person assigns before approving | Only rule consistent with the claim's refusal (`refs/claim.md:41-42`); unassigned first-come races |
| OD-2 | Same login in two workspaces | Setup rule: one poller per login; `own_login` in audit | No cross-workspace lock exists under A without a shared store |
| OD-3 | Allow-list location | Local `--approvers-file`, default `~/.config/superclaude/issue-watch/approvers` [PROPOSAL] | A list in the checkout changes with the branch; drift between workspaces is the accepted cost |
| OD-4 | Label names | `watch:claim`, `approved:claim` [PROPOSAL] | Distinct from the 9 defaults; created by a maintainer, since `/sc:issue` never creates labels |
| OD-5 | Label-only fallback | Only with explicit `--label-only`, marked in every line | It drops two definitions; the degradation must stay visible |
| OD-6 | Re-approval resets the record? | No; report `re-approved` | Resetting lets label toggling bypass the attempt cap |
| OD-7 | At-most-once parameters | Section 7.4 values | Conservative; retune after the live test measures claim time |
| OD-8 | Session permission mode | Do not enable F1 before Q6; skipped permissions need written owner acceptance | No flag can set it (RD-F6); it is the largest residual risk |
| OD-9 | Claim's reads of issue text; authorization basis | Accept as residual risk, approver label authorizes the claim's writes only | The claim must read the issue (RD-F5); the approver is the requested human gate |
| OD-10 | State file location | XDG path of Section 7.2 | Loss is survivable because the marker is durable (FR-009) |

## 11. Risks

| ID | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | `/sc:issue` in `--prompt` does not run as a slash command (Q1) | Unknown / high | Live test F3 before F1 |
| R2 | Token lacks `read:project` (RD-F8) | Observed / high | `gh auth refresh -s read:project`; OD-5 |
| R3 | Project JSON differs from the assumed shape (Q8) | Unknown / medium | `_assumed_shape` fixtures; fail closed |
| R4 | Post-approval body edit instructs the session (T4) | Possible / high | OD-8, OD-9 |
| R5 | Same login in two workspaces double-claims | Possible / medium | OD-2 rule |
| R6 | State lost on stop before the marker (Q15) | Possible / medium | F2; the marker bounds the window |
| R7 | Overlapping cycles | Low / low | `flock` |
| R8 | Issues wait while a workspace is stopped | Certain / low | Accepted (NG5) |
| R9 | Rate-limit replies not handled specially | Low / low | The 5-minute cadence is the back-off |

## 12. Traceability

| Requirement | Source fact |
|---|---|
| FR-001, NFR-013 | CC "House patterns"; RR steps 2.4, 2.6 |
| FR-002, FR-003 | RR step 3.3; SB Constraints (claim assigns to the `gh` login) |
| FR-004, FR-005 | RD-F8 (default 30, fail closed) |
| FR-006 to FR-008 | SB "Poll cycle shape"; RD-F7; RR step 4.2 |
| FR-009 to FR-011, FR-017 | SB Enrichment (record before launch, re-read, `considered` map); RR step 5.2 |
| FR-012 to FR-016 | D3; RD-F6; RR steps 3.2, 3.4 |
| FR-018 to FR-022, NFR-008 | RR step 5.3 and algorithm step 13 |
| NFR-001 to NFR-004 | SB Constraints; RD Security model |
| NFR-005, NFR-006, NFR-009, NFR-010 | RD-F4; RR step 5.1 |
| NFR-007, NFR-012 | RD-F9 |
| NFR-011 | [PROPOSAL], no source |
| T4, T5; F1, F2, F4 | RD-F5, RD-F6; SB Q1 and Enrichment |

