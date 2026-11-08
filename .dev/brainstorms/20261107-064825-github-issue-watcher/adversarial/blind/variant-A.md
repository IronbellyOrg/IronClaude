# Requirements Specification: GitHub Issue Watcher (issue #331), Option A

- Status: Draft variant for adversarial review
- Issue: IronbellyOrg/IronClaude#331
- Inputs: `seed-brief.md`, `enrichment/research-deep.md`, `enrichment/codebase-context.md`
- Convention: a value marked [PROPOSAL] is not fixed by the source; ASSUMPTION marks a premise not verified in the repo.

## 1. Purpose and scope

A watcher runs in each Coder workspace, polls GitHub every 5 minutes with that workspace's own `gh` login, selects eligible issues meant for that login (Section 3), and starts one ordinary top-level Claude session running `/sc:issue --claim <N>` through `orca agent launch`.

In scope: selection rules, the dispatch record, the launch adapter, the security model, a `superclaude issue-watch` CLI group testable with mocked `gh` and `orca`, a design doc and label setup instructions. Out of scope: anything live, the Coder scheduling change, any work after the claim.

Design stance: a pipeline of replaceable stages (discover, filter, route, record, launch, audit) behind narrow interfaces, so each open decision in Section 10 and each documented alternative (B, C, D) replaces one stage, not the cycle.

## 2. Fixed constraints and non-goals

- **D1** Option A, workspace-side poller. No listener, inbound port or address registry. B and C stay documented alternatives; IronbellyOrg/Coder#477 is unnecessary unless B or C is revisited.
- **D2** Claim-only: the watcher's job ends once `/sc:issue --claim <N>` is started; the claim stops at `next-steps.md`.
- **D3** Only a validated positive integer reaches a session prompt.
- Every repository-scoped `gh` call names `IronbellyOrg/IronClaude`; nothing touches SuperClaude-Org. Source of truth is `src/superclaude/`; UV only; no secrets.
- `/sc:issue` is never-as-worker, so the watcher is a plain process, never an Orca worker and never inside a Claude session.

Non-goals: NG-1 no GitHub workflow or Action; NG-2 no listener or webhook receiver; NG-3 no label or Project creation by code; NG-4 no post-claim pipeline; NG-5 no change to the claim; NG-6 no live run or Coder template edit.

## 3. Definitions

Each definition is a predicate over `gh` JSON. The poller reads only `number`, `state`, `labels`, `assignees`, issue events, Project item fields and an integer marker count; never title, body or comment text.

- **Tagged.** `labels[].name` contains the configured trigger label by exact, case-sensitive equality (default `watch:ready` [PROPOSAL]).
- **Approved by a human.** (a) `labels[].name` contains the approval label (default `watch:approved` [PROPOSAL]); (b) the latest `labeled` event for that label has an `actor.login` on the approver allow-list and an actor that is not a bot (`type` `Bot` or login ending `[bot]`); (c) no later `unlabeled` event for that label exists. An empty or missing allow-list approves nothing.
- **In a Project.** The configured Project (owner `IronbellyOrg`, number from config) has an item whose content is issue N of `IronbellyOrg/IronClaude`. If the Project read fails (missing `read:project`, error, or item count equal to the requested limit), the predicate is false for the whole cycle.
- **Backlog.** That item's single-select field (default `Status`) equals the configured value (default `Backlog`) by exact string; missing or null is not Backlog.
- **Intended owner.** For own login L (from `gh api user -q .login`), the configured routing rule returns true; the default `assigned-to-self` requires L in `assignees[].login`. Under every rule, any assignee other than L excludes the issue.
- **Eligible issue.** At evaluation time: `state == "OPEN"`, tagged, approved, in the Project and in Backlog (when Project mode is `required`), intended owner is L, no comment by L carries `<!-- sc:issue:claim -->`, and no dispatch-record entry blocks a launch (Section 7).

## 4. Functional requirements

Every criterion runs with stub `gh` and `orca` executables on PATH or injected runners (style of `tests/pr_submit/test_conflict_e2e.py`). Exit codes are in Section 8.

- **FR-001** Each cycle resolves the own login with `gh api user -q .login` and aborts if it is empty or fails `^[A-Za-z0-9-]{1,39}$`.
  - Given an empty login, when `once` runs, then no launch occurs, exit is 3, audit `outcome=identity_failed`.
- **FR-002** Every repository-scoped `gh` call names `IronbellyOrg/IronClaude` and every `gh api` call passes `--method GET`.
  - Given a recording stub, when a cycle runs, then every `issue` argv has `--repo IronbellyOrg/IronClaude`, every `api` argv has `--method GET`, and none contains `SuperClaude-Org`.
- **FR-003** Discovery runs `gh issue list --repo IronbellyOrg/IronClaude --label <trigger> --state open --json number,labels,assignees,state -L 100`.
  - Given exactly 100 returned items, when the cycle runs, then nothing launches, exit is 4, audit `outcome=truncated`.
- **FR-004** No `gh` call requests `title`, `body` or `comments` fields.
  - Given a recording stub, then no `--json` value names them, and the only `--jq` touching `.body` is the FR-008 count, whose output must parse as a non-negative integer.
- **FR-005** Approval is evaluated from issue events per Section 3.
  - Given a latest `labeled` actor not on the allow-list, then the issue is skipped `not_approved` and no record entry is created.
- **FR-006** In Project mode `required`, membership and Status come from `gh project item-list <number> --owner IronbellyOrg --format json -L 100`.
  - Given the stub exits non-zero with a scope error, then nothing launches, exit is 4, audit `outcome=project_unreadable`.
- **FR-007** Owner routing is one function chosen by config key `routing` from a routing table (default `assigned-to-self`).
  - Given an issue assigned to `alice` and own login `bob`, then it is skipped `other_owner` under every registered rule.
- **FR-008** The poller counts comments by the own login containing `<!-- sc:issue:claim -->`; a non-zero count skips the issue and moves any entry to `claimed`.
  - Given a count of 1, then nothing launches and the entry is `claimed`.
- **FR-009** A `pending` entry is made durable (temp file, `fsync`, `os.replace`) before the launch is invoked.
  - Given a launch stub that reads the record file, then it observes the issue as `pending`.
- **FR-010** Just before launch the poller re-reads `state`, `labels`, `assignees` and re-evaluates eligibility; on failure the entry becomes `abandoned`.
  - Given a second snapshot with another assignee, then the launch stub is not called and the reason is `changed_before_launch`.
- **FR-011** Only `build_claim_prompt(n)` builds the prompt: it accepts an `int` that is not a `bool`, in 1 to 999999999, and returns exactly `"/sc:issue --claim " + str(n)`; otherwise it raises `InvalidIssueNumber`.
  - Given `"12"`, `True`, `0`, `-1`, `12.0`, `1000000000`, then each raises; given `331`, then it returns `/sc:issue --claim 331`.
- **FR-012** The launch is the argv list `["orca","agent","launch","--agent","claude","--worktree","path:<abs>","--surface","terminal","--prompt",<prompt>,"--json"]`, without a shell.
  - Given a recording runner, then it received a list, `shell` was false, and the element after `--prompt` equals the built prompt.
- **FR-013** The configured worktree must be an absolute path to an existing directory, checked before any `gh` call.
  - Given `worktree = "relative/path"`, then exit is 2 and `gh` is never called.
- **FR-014** A success reply moves the entry to `launched`; `agent_session_operation_unknown` stores `operationId` and moves it to `unknown`; any other failure moves it to `failed`.
  - Given each stub reply, then the entry is `launched`, `unknown` with `operation_id`, or `failed`.
- **FR-015** An `unknown` entry is retried only with `orca agent launch --retry-launch <operationId>`.
  - Given an `unknown` entry, when the next cycle runs, then the argv contains `--retry-launch <id>` and no `--prompt`.
- **FR-016** A cycle examines at most `max_candidates` issues, least-recently-examined first by the `considered` map, and launches at most `max_launches`.
  - Given 15 eligible issues and default caps, then exactly 1 launch occurs and the 10 examined are the 10 oldest in `considered` (never-examined first).
- **FR-017** Each cycle appends one JSON audit line (`ts`, `login`, `cycle_id`, `outcome`, `examined`, `skipped`, `launched`, `record_version`, `dry_run`) to the audit log and stdout.
  - Given any cycle, including a failing one, then the audit file grew by exactly one parseable line with every field.
- **FR-018** A non-blocking file lock prevents overlapping cycles; the loser exits 0 with `outcome=locked` without reading GitHub.
  - Given a held lock, then exit is 0 and `gh` is never called.
- **FR-019** `once --dry-run` performs all reads and filters but changes no entry and launches nothing; `status [--json]` prints the record offline.
  - Given an eligible issue, when `once --dry-run` runs, then the launch stub is not called and audit `dry_run=true`; when `status --json` runs, neither stub is called.
- **FR-020** The watcher issues no GitHub write (`gh issue edit`, `gh issue comment`, `gh label`, `gh project item-edit`, non-GET `gh api`).
  - Given a recording stub, when every verb runs, then no argv matches that list.

## 5. Non-functional requirements

- **NFR-001 (security, prompt boundary)** No GitHub-originated byte other than the FR-011 integer appears in any `orca` argv, record or audit line.
  - Given fixtures whose title and body hold a sentinel string, when a cycle launches, then the sentinel appears in no recorded argv, record or audit line.
- **NFR-002 (security, no shell)** No module in `src/superclaude/cli/issue_watch/` uses `shell=True`, `os.system` or `os.popen`.
  - Given an AST scan of the package, then no such call exists.
- **NFR-003 (security, read-only)** Besides FR-020, the GitHub layer rejects any `gh` argv outside the allow-list `api`, `issue list`, `issue view`, `project item-list`.
  - Given `["gh","issue","edit",...]`, then `ForbiddenCommand` is raised before spawning.
- **NFR-004 (at-most-once, idempotency)** Per (login, issue), at most one fresh `--prompt` launch per lease window and at most `max_attempts` in total, whatever step a crash interrupts; an unchanged rerun after a successful launch launches nothing.
  - Given fault injection after record write, after launch call and after reply, when cycles rerun from the persisted record, then fresh launches never exceed these bounds; given a `launched` entry and unchanged stubs, then the launch stub is not called.
- **NFR-005 (rate limits)** A cycle with N candidates makes at most `3 + 3N` `gh` calls.
  - Given 10 candidates, then the stub counts at most 33 calls; 12 cycles an hour is at most 396, under 8 percent of the 5,000 an hour allowance.
- **NFR-006 (rate-limit handling)** A `gh` failure mentioning `rate limit` or HTTP 403/429 ends the cycle with exit 5, `outcome=rate_limited`, and no entry state change.
  - Given `API rate limit exceeded` from the stub, then exit is 5 and no entry changes state.
- **NFR-007 (observability)** Every skip reason comes from a closed enum: `not_open`, `not_tagged`, `not_approved`, `not_in_project`, `not_backlog`, `other_owner`, `not_intended`, `claimed`, `record_blocks`, `cap_reached`, `changed_before_launch`.
  - Given fixtures for each reason, then each audit `skipped` map uses only enum members.
- **NFR-008 (fail closed)** Unreadable, malformed or truncated input yields no launch in the affected scope.
  - Given malformed JSON from any one `gh` call, then no launch depending on it occurs and the audit names the failure.
- **NFR-009 (performance)** Per-call timeout 30 s and cycle timeout 240 s [PROPOSAL], under the 5-minute interval; with instant stubs a 10-candidate cycle takes under 2 s.
  - Given a stub that sleeps past the timeout, then the call is killed, the issue skipped and the audit line still written.
- **NFR-010 (cost)** Each fresh launch starts exactly one session; the watcher makes no model calls.
  - Given one eligible issue, then exactly one `orca agent launch` is recorded and no `claude` executable is invoked.
- **NFR-011 (maintainability)** Stages depend on each other only through typed protocols; no stage imports `cycle`, and no new dependency beyond `click` and the standard library is added.
  - Given an import test and `make verify-deps`, then `cycle.py` imports only stage protocols and public functions, and no dependency is added.

## 6. Security model

Trust boundaries: GitHub content is untrusted (public repository); the workspace `gh` credential and the state directory are trusted to the workspace user; the launched session is trusted for its prompt but reads issue text itself.

| Asset | Threat | Control | Residual risk |
|---|---|---|---|
| Launch prompt | Injection via title, body, labels or comments | FR-004, FR-011, NFR-001: only an in-range `int` is formatted | None for the prompt |
| Launched session | Injection via issue text the claim reads live | Outside the watcher; D2 bounds the session to the claim | Accepted: nothing constrains the session's permission mode (OD-6) |
| Approval gate | Non-approver, bot, or remove-and-re-add | Allow-listed latest `labeled` actor; bots excluded; later `unlabeled` voids; empty list approves nothing | Compromised approver account; post-approval body edit undetected (UNVERIFIED) |
| `gh` token | Writes; leakage | NFR-003 allow-list; tokens never logged or stored | Token scope is set outside this repo |
| Repository target | gh default-repo resolves to upstream | FR-002 literal repo; test asserts no `SuperClaude-Org` | None in code |
| Launch target | Redirected worktree or agent | FR-013 local absolute worktree; agent fixed to `claude` | Local config editor can redirect |
| Dispatch record | Corruption or deletion causing replays | Atomic writes; schema version; unreadable record fails closed (exit 6) | Deletion; FR-008 marker check still blocks after a posted claim |
| Owner routing | Wrong person | Any other assignee excludes; claim refuses foreign assignee | Same-login double claim (R-2) |
| Inbound surface | Remote command execution | None exists (D1, NG-2) | None |

## 7. Dispatch record and at-most-once semantics

The claim has no mutual exclusion (read, check, then additive `--add-assignee @me`), so the watcher writes its own record before every launch. Exactly-once is impossible across a crash between "launch called" and "reply stored"; the guarantee is bounded as in NFR-004.

**Location.** `<state_dir>/<login>/record.json`, default `state_dir = ~/.local/state/superclaude/issue-watch` [PROPOSAL]; keyed by login so a changed login inherits nothing. ASSUMPTION: `$HOME` persists across restarts (else F-1).

**Schema v1.** Top level: `schema_version`, `login`, `repo`, `entries`, `considered` (issue number to last-examined timestamp). Entry: `number`, `state`, `attempts` (fresh launches), `created_at`, `updated_at`, `lease_until`, `operation_id` (nullable), `last_reason`, `history` (last 20 `{ts, from, to, reason}` [PROPOSAL]). Unknown version or unparseable file: exit 6, no launch.

**States.**

| State | Meaning | Blocks a fresh launch? |
|---|---|---|
| `pending` | Record written, launch about to be or being called | Yes, until lease expiry |
| `launched` | Orca confirmed the session started | Yes, always |
| `unknown` | Orca returned `agent_session_operation_unknown` with an `operationId` | Yes; only `--retry-launch` allowed |
| `failed` | Launch definitely did not start | Until lease expiry; then retry if `attempts < max_attempts` |
| `abandoned` | Eligibility lost before launch, or attempts exhausted | Only when `last_reason == max_attempts` |
| `claimed` | Own-login claim marker seen | Yes, always (terminal) |

**Transitions.**

| From | Event | To |
|---|---|---|
| (none) / `failed` (lease expired, attempts left) / `abandoned` (not exhausted) | Eligible and selected | `pending`, `attempts += 1`, `lease_until = now + lease` |
| `pending` | Pre-launch re-read fails | `abandoned` (`changed_before_launch`), `attempts -= 1` |
| `pending` | Success reply | `launched` |
| `pending` | `agent_session_operation_unknown` | `unknown` |
| `pending` | Other failure reply | `failed` |
| `pending` (found at cycle start, lease expired) | No reply was stored (crash) | Claim marker present: `claimed`; else `failed` (`lost_reply`) |
| `unknown` | Retry reply success | `launched` |
| `unknown` | Retry reply definite failure, or lease expired | `failed` |
| `failed` | `attempts >= max_attempts` | `abandoned` (`max_attempts`) |
| any non-terminal or `launched` | Own-login claim marker seen | `claimed` |

A `launched` entry still unclaimed after the lease is audited as `launched_unclaimed` and never relaunched automatically (recovery: F-5).

**Lease and caps.** `lease` 60 min, `max_attempts` 3, `max_launches` 1 per cycle, `max_candidates` 10 per cycle, all [PROPOSAL] from the research plan. Each must be a positive integer and `lease` at least 15 min [PROPOSAL], long enough for a started claim to post its marker; `check-config` rejects other values with exit 2.

**Write discipline.** Every transition is persisted (temp, `fsync`, `os.replace`) before the next external call; the cycle holds `<state_dir>/<login>/cycle.lock` (`fcntl.flock`, non-blocking) throughout.

## 8. Repo-side deliverables (testable with mocks)

**Package `src/superclaude/cli/issue_watch/`**, registered in `src/superclaude/cli/main.py` with `main.add_command(issue_watch_group, name="issue-watch")` after the `reflect` registration. One module per stage; each seam lets a later option replace a module, not the cycle.

| Module | Responsibility | Extension seam |
|---|---|---|
| `runner.py` | `CommandResult`, `Runner`, `run_command(argv, timeout)`; argv list, never a shell | Fake runner in tests |
| `config.py` | Load and validate JSON config (`tomllib` needs Python 3.11; the package supports 3.10) | New keys default safely |
| `github.py` | Read-only layer: login, discovery, snapshot, events, marker count, Project items; allow-list; truncation | `IssueSource`: option D label relay or B/C event feed |
| `predicates.py` | Pure Section 3 predicates returning `(bool, reason)` | None (pure) |
| `routing.py` | Routing table plus shared other-owner predicate | New rules (`person-label`, `project-field`) |
| `approval.py` | `ApproverSource`; default reads config | Repo-hosted list |
| `record.py` | Schema, state machine, atomic persistence, lock | `DispatchStore`: shared ledger on revisit |
| `launch.py` | `build_claim_prompt`, `launch_claim`, `retry_launch`, outcome mapping | `Launcher`: B/C push client |
| `audit.py` | One JSON line per cycle | `AuditSink` |
| `cycle.py`, `commands.py` | Orchestration on protocols only; Click verbs | None |

**Verbs.** `issue-watch once [--config PATH] [--dry-run]` (one cycle, the unit a scheduler runs every 5 minutes); `issue-watch status [--json]` (offline); `issue-watch check-config` (offline, no `gh` call).

**Exit codes.** `0` completed (including nothing eligible and `locked`); `1` internal error; `2` invalid config or worktree; `3` login unresolved; `4` incomplete input (truncated list, unreadable Project); `5` rate limited; `6` record unreadable; `7` completed with at least one `failed` launch.

**Tests `tests/issue_watch/`.** `test_prompt.py`, `test_runner.py`, `test_github.py`, `test_predicates.py`, `test_routing.py`, `test_record.py` (every transition, crash injection, schema failure), `test_launch.py`, `test_cycle.py`, `test_cli.py` (`CliRunner`, exit codes), `test_stub_e2e.py` (stub executables on PATH), `test_no_shell.py`, `test_sentinel.py`.

**Design doc `docs/designs/issue-watcher.md`** in the house format (Status, Issue, Branch, Source of truth, Produced by, numbered sections): D1 to D3, B/C/D with the nine revisit conditions, these definitions, record and threat table, and the note that Coder#477 is unnecessary under A.

**Setup instructions** (design doc section, not executed): `gh label create watch:ready --repo IronbellyOrg/IronClaude`, the same for `watch:approved`, `gh auth refresh -s read:project` per workspace login, an example config, and the scheduler line for the Coder repo.

## 9. Follow-up not built here

- F-1 Coder repo: `coder_script` entry with `cron = "0 */5 * * * *"` running `superclaude issue-watch once`, and a persisted `state_dir` if `$HOME` is not persisted.
- F-2 One owner-run live test: does `--prompt "/sc:issue --claim <N>"` run the slash command; real reply JSON shapes.
- F-3 Decide the launched session's permission mode.
- F-4 Create the two labels and grant `read:project` for real.
- F-5 Operator recovery verb (`issue-watch release <N>`) for `launched_unclaimed` and exhausted entries.
- F-6 Close or repurpose IronbellyOrg/Coder#477 under A.
- F-7 Options B, C, D only on a revisit condition; post-claim pipeline (`--claim --pipeline`) separately.

## 10. Open decisions (recommended defaults)

| ID | Decision | Recommended default | Reason |
|---|---|---|---|
| OD-1 | Owner routing | `assigned-to-self` | The claim already continues on its own login and stops on another; no race between different logins; other candidates are table entries |
| OD-2 | Same login, several workspaces | Config `enabled` defaults `false`; one workspace per login enables it | Records cannot see each other; a shared ledger is a B revisit condition |
| OD-3 | Approver allow-list | Local config list; latest `labeled` actor must be on it | No extra call, testable, fails closed; `ApproverSource` allows a repo-hosted list later |
| OD-4 | Label names | `watch:ready`, `watch:approved` | No clash with the nine defaults; tagging and approval stay separately auditable |
| OD-5 | Project mode | `required`; `off` only by explicit config | The issue requires Project plus Backlog; a missing scope must not widen eligibility |
| OD-6 | Launched session permission mode | `ccsession-orca` default, documented | No launch flag exists; needs the live test (F-2, F-3) |
| OD-7 | Claim's reads of issue text | Accept as residual risk | NG-5; a human approved before launch |
| OD-8 | At-most-once parameters | 60 min, 3, 1, 10 | Research values; one launch per cycle caps a selection bug at one session per 5 minutes |
| OD-9 | Config file | JSON at `~/.config/superclaude/issue-watch.json` [PROPOSAL] | No new dependency on 3.10 |

## 11. Risks

| ID | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R-1 | `/sc:issue` given via `--prompt` does not run as a slash command (UNVERIFIED) | Medium / high | F-2 before rollout; `Launcher` seam allows another submission method |
| R-2 | Same login in two workspaces double-claims | Medium / medium | OD-2; marker check; claim edits its marked comments on re-run |
| R-3 | Token lacks `read:project` | High today / high: nothing launches | Exit 4 makes it visible; F-4; option D fallback |
| R-4 | `gh project item-list` JSON shape differs (UNVERIFIED) | Medium / medium | Defensive parse; fail closed; fixtures updated after F-2 |
| R-5 | Record lost on restart | Unknown / low | FR-008 marker check; F-1 persisted path |
| R-6 | Host Orca ignores `--retry-launch` contract (UNVERIFIED) | Low / medium | `unknown` falls to `failed` after the lease; attempt cap |
| R-7 | Workspace owner differs from `gh` login (UNVERIFIED) | Low / medium | Only the `gh` login is trusted; documented |
| R-8 | Stage interfaces drift as options are added | Medium / medium | NFR-011 import test |

## 12. Traceability

| Requirement | Source fact |
|---|---|
| FR-001, R-7 | Research security model: login read each cycle; Q16 |
| FR-002, FR-020, NFR-003 | Seed: every `gh` call names the repo; research step 4.2: `--method GET`, read-only layer |
| FR-003, FR-006, R-3, R-4 | Verified fact 8: `read:project`, page 30, `-L 100`, fail closed; Q7, Q8 |
| FR-004, FR-011, NFR-001, R-1 | D3; research prompt rule and fields `number,labels,assignees,state`; Q1 |
| FR-005, OD-3, OD-4 | Verified fact 7: no approval label, Triage-or-higher, `labeled` `actor` |
| FR-007, OD-1, OD-2, R-2 | Research intended-owner filter, candidate 1, `claim.md:41-42`; Q14 |
| FR-008 | `claim.md:29`: `<!-- sc:issue:claim -->` on a comment by the current login |
| FR-009, FR-010, FR-016, NFR-004, Section 7, OD-8 | Verified fact 4 (no mutual exclusion); research poll cycle, states, [PROPOSAL] caps, `considered` map; seed success criterion |
| FR-012 to FR-015, R-6 | Verified fact 6: launch argv, existing worktree, `--retry-launch`; Q3 |
| FR-017, NFR-007 | Research: one audit line per cycle |
| FR-018, R-5 | Research Q15: cron overlap, `$HOME` persistence |
| FR-019, Section 8, NFR-002, NFR-011 | Seed: testable with mocks; codebase house patterns, injectable argv runner |
| NFR-005, NFR-006 | Verified fact 9: 5,000 an hour; 0.24 percent cost; Q23 |
| NFR-008, NFR-009 | Research: fail closed on truncation; seed 5-minute interval |
| NFR-010 | D2; one session per issue |
| Section 6 | Verified fact 5 (PUBLIC repo, live reads); Q6; D1 |
| Section 9 | Verified fact 10 (`coder_script` cron); Coder#477 note |



