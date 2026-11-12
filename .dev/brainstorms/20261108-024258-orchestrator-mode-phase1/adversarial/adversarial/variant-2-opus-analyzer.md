# Orchestrator Mode Phase 1 (#339): `/sc:sweep` Requirements Specification

- Variant: 2
- Model: opus
- Persona: analyzer (root-cause and evidence-based reasoning)
- Date: 2026-11-08
- Status: draft for adversarial debate

Sources read for this variant: the seed brief (all 90 lines); REPORT Section 8 Phase 1 (lines 1216-1333); GAPS lines 118-140; `synthesis/phase7-summary.md`; `enrichment/codebase-context.md`; `src/superclaude/core/WORKER-CONTRACT.md` lines 1-203; `src/superclaude/cli/main.py` lines 550-566; `tests/skills/test_worker_contract.py` lines 440-462 plus a grep for `NEVER_AS_WORKER`; `.gitignore` grep for `.dev`; `pyproject.toml` grep for `yaml`; `git --version` on this host (2.47.3). TASK, REPORT and GAPS are as defined in the seed brief.

## 1. Problem and Root Cause

**Symptom.** A person with many Claude Code sessions across Orca worktrees must open each one to learn whether it is working, waiting on them, stuck, finished or safe to close. Sessions sit on a held message or an unread question (seed brief line 25; 2026-11-05 incident).

**Root cause, two parts.** Each fix alone fails, so both ship:

1. *No observation point.* State is spread over five sources with different freshness: Orca read verbs, each worktree's git state, task-package ledgers, worker return contracts and transcript files (seed brief line 34). Nothing joins them, so the person is the join.
2. *No coordinator duty.* `WORKER-CONTRACT.md` has no rule that the coordinator keeps polling, re-arms an expired wait or sweeps on a schedule. REPORT line 48 records that a grep for poll, re-arm, cron, sweep and expire matches only line 45 (WC-10), a worker liveness rule, not a coordinator loop.

A report without the duty is never run; a duty without the report has nothing to read. `/sc:sweep` fixes part 1; WC-14 fixes part 2.

**Secondary cause the design must not reintroduce.** The obvious implementation of part 1 harms what it observes. A plain `git status` may refresh the index stat cache and take `index.lock`; WC-9 (`WORKER-CONTRACT.md:44`) tells a worker that finds `index.lock` to report `blocked`. A naive sweep would turn healthy workers into blocked ones (GQ-103(1)). The observer effect is the first design constraint, not a detail.

## 2. Scope

Phase 1 adds:

- A Python CLI `superclaude sweep run` in a new package `src/superclaude/cli/sweep/` (option A1, REPORT line 1098).
- A thin command `src/superclaude/commands/sweep.md` and a skill `src/superclaude/skills/sc-sweep-protocol/SKILL.md`.
- The WC-14 "Coordinator loop" rule and `/sc:sweep` on the never-as-worker list in `src/superclaude/core/WORKER-CONTRACT.md`, with contract-test pins.
- Routing registries, `HOW-WE-WORK.md` and its plugin byte copy, user and developer guide rows, a CHANGELOG entry, and `.dev/sweeps/` in `.gitignore`.

Boundary: one coordinator over one worktree tree (a feature worktree and its Orca child worktrees). Constraint order: safety over completeness over convenience (seed brief line 27).

## 3. Out of Scope (Later Phases and Blockers)

Recorded only, not designed. Phase numbers are the REPORT's own (REPORT lines 1324-1332).

| Phase | What | Blocker evidence |
|---|---|---|
| 2 | `/sc:close`: act on safe-to-close REVIEW rows after the person confirms | Section 4 refusals must become executed checks, plus "all commits pushed" and the `.dev/tasks/` rule; removal only through `orca worktree rm`; contract edits after PR #422 (REPORT line 1328) |
| 3 | Resume a stalled (proved) or frozen session as a new Task | WC-6 and WC-10; needs positive stall proof, never `unverifiable` (REPORT line 1329) |
| 4 | Trust layer for messages between sessions | Mode mismatch under `CCSESSION_PERMISSIONS=default`; no design for signed grants; comment-3 research first (REPORT line 1330) |
| 5 | Orchestrator of orchestrators | Version-2 work, after the comment-3 research (REPORT line 1331) |
| 6 | Management-server relay | Owner definition of "management server" (GQ-66); no standing service (REPORT line 1332) |
| Gated, inside the sweep | `check --peek` / `check --all` as question sources | A probe must settle 06 Gaps 1, 2 and 18 first (REPORT line 1302) |

Also out: every action (close, resume, kill, remove, stash, message); any mechanical caller check that stops a worker from running the CLI (coordinator-only is a contract rule, REPORT line 1277); `--include-remote` until its cost is measured (GQ-22); the `gate-list`, `worker-read`, `stash list` and `run-list` reads (Section 8).

## 4. Functional Requirements

Each requirement has one testable acceptance criterion (AC). "Fixture" means a file under `tests/sweep/fixtures/`; every Orca and git response in tests comes through the two seams (Section 8).

**Entry and scope**

- **FR-001 CLI.** `superclaude sweep run [--run <id>]... [--window <N>h|<N>d] [--root <dir>] [--output <dir>]`, registered with a deferred import after `main.add_command(reflect_group, name="reflect")` (`src/superclaude/cli/main.py:561`) and before the `__main__` guard (`:564`). *AC:* `CliRunner` `sweep --help` and `sweep run --help` exit 0 and list every option.
- **FR-002 Run scope (GQ-104).** Runs come from `--run` (repeatable), else from the `run-current` binding. With neither, exit 2 with `no Run bound: pass --run <id>`. No `run-list` fallback. Exception: when Orca is unavailable the CLI cannot ask `run-current`, so it runs a disk-only sweep and exits 0 (FR-020). *AC:* three tests: explicit `--run`; `run-current` returns a binding; `run-current` returns none and exit code is 2 with zero `worker-show` calls recorded.
- **FR-003 Window (GQ-103(2)).** `--window` accepts a positive integer with `h` or `d`; default `6h`; anything else is a Click usage error (exit 2). The parsed `timedelta` is an argument of `classify`, not a module constant. *AC:* the same person-started fixture is `idle` with `--window 1h` and `could not determine` (note "person session, active") with `--window 6h`, and `test_classify` calls `classify` with an explicit window.
- **FR-004 Root and output.** `--root` defaults to the current git top-level and is printed on the Scope line. `--output` defaults to `<root>/.dev/sweeps/`; a resolved path outside `<root>/.dev/` is a usage error. *AC:* `--output /tmp/x` exits 2 and writes nothing.

**Discovery**

- **FR-005 Orca discovery.** For each Run: `worker-list --run <id> --json`, paged on `page.nextCursor`, then one `worker-show --dispatch <id> --json` per row; `task-list --run <id> --json` and `task-list --ready --run <id> --json`; one `worktree ps --json`. The classifier reads only `worker-show` fields, because the populated `worker-list` row schema is uncaptured (GQ-01). *AC:* a 101-row fixture produces exactly 2 list calls and min(N, 50) show calls.
- **FR-006 Disk discovery.** Plain reads of fixed patterns under `--root` and each `worktree ps` root: `.dev/tasks/{to-do,done}/*/progress.md`, `.dev/tasks/{to-do,done}/*/.archiving`, each known `<report-dir>/return-contract.yaml` (parsed with `yaml.safe_load`; `pyyaml>=6.0` is already a dependency, `pyproject.toml:38`), the ccsession tab map, `~/.claude/projects/<key>/topics/*.txt` and transcript tails. No recursive walk; a path whose `resolve()` leaves its root is skipped with `unscanned: outside root`. Never `ccsession --list` (it writes, REPORT line 1247). *AC:* a symlink-out fixture is reported `unscanned: outside root` and its target is never opened.
- **FR-007 Person-started sessions (GQ-108).** A person-started session is a transcript under a scanned root's project key that the tab map joins to no Orca row. Last activity is the transcript mtime. Inside the window it is a session row; older than the window it goes to Historical sessions. *AC:* a fixture with one joined and one unjoined transcript yields one Orca row and one person row; an unjoined transcript older than the window appears only under Historical sessions.

**Classification**

- **FR-008 Precedence.** `classify` applies rules 1-7 and idle in the order of Section 7 and returns the matching rule id with the class. *AC:* one fixture per rule; each asserts both class and rule id; a fixture matching rules 2 and 6 gets rule 2.
- **FR-009 Unknown is its own class.** `unverifiable`, a late heartbeat, stale `evidence.liveStatus`, a missing row, an absent `agentWait` on an unsettled row, or an unreadable source give `could not determine`, never `stalled (proved)` or `idle` (WC-10, `WORKER-CONTRACT.md:45`). *AC:* a property test over every fixture: `stalled (proved)` appears only where the fixture's Orca liveness is `exited` and no `worker_done` and no fenced evidence exist.
- **FR-010 Waiting kinds.** Kind (a) is an explicit question (non-null `agentWait`, or a `blocked` contract meeting rule 1's condition); kind (b) is blocked by policy (frozen plan per `WORKER-CONTRACT.md:133`, or a ready Task, listed with "creator: could not determine"). Policy is computed for every row independently of class (GQ-96). *AC:* a blocked `/sc:implement` contract on a settled row is listed under both (a) and (b).
- **FR-011 Package states (GQ-102, GQ-105).** Each package has exactly one state from Section 7.3, including `conflict` (same id in `to-do/` and `done/`) and `archive-blocked` (in `to-do/` and its `progress.md` has a `FINAL:` line). *AC:* fixtures for all five states; the conflict fixture makes its worktree "removable: no (package conflict: <id>)"; an unfinished ledger without `FINAL:` is `unfinished`, not `archive-blocked`.
- **FR-012 Shared package (GQ-101).** A package counts as "running in a worktree" only when that worktree's own `git status --porcelain` lists a path under `.dev/tasks/{to-do,done}/<id>/` (modified, staged or untracked). Committed folders unchanged in a worktree never count. The same running id in two or more worktrees makes each "removable: no" and prints one Retained-problems line naming every worktree. *AC:* the shared-folders fixture (the same 3 committed packages in 3 worktrees, none changed) flags nothing; a fixture where 3 worktrees each modify one package's `progress.md` prints one line naming all 3.
- **FR-013 Safe-to-close.** Two values per row, each `yes`, `no` or `could not determine`, printed as REVIEW. Phase 1 never prints `yes` for either half: "terminal releasable" needs "result read", which no probe observes, and "worktree removable" needs "report read" and "no open PR", which no allowed read observes (REPORT line 1246). *AC:* a grep of every rendered fixture report finds no `releasable: yes` and no `removable: yes`.
- **FR-014 Worktree git state (GQ-110).** One `git status --porcelain --branch` per worktree, parsed once, answers: uncommitted changes, ahead of upstream or no upstream, unsaved `.dev/tasks/` paths, and running packages (FR-012). Unmerged commits come from one `git log --format=%H --max-count=1 <feature-branch>..HEAD` per child worktree, where `<feature-branch>` is the branch named in the `--root` worktree's own status header; for the root worktree itself unmerged is `could not determine` (its merge target is not observable). *AC:* the recorded `_git` argv list has exactly one `status` call per worktree and at most one `log` call per child.

**Report and output**

- **FR-015 One dated report.** Write `<output>/<YYYYMMDD-HHMMSS>-sweep.md` (UTC) and nothing else. *AC:* the snapshot-diff test of NFR-001.
- **FR-016 People first.** Section order is fixed (Section 9); waiting-on-a-person lists sort oldest first by time since the wait began, ties by id, unknown age in a labelled group, never age 0. *AC:* rendered headings appear in Section 9 order; a three-item fixture sorts as specified.
- **FR-017 JSON on stdout.** Schema version 1 with every key always present (absent values `null`): `schema_version`, `observed_at`, `scope`, `window`, `orca_available`, `sources`, `rows`, `waiting`, `summary`, `report_path`. Each row carries `cls`, `rule`, `evidence`, `notes`, `safe_to_close`. *AC:* `test_cli_contract.py` asserts the key sets and types on one fixture sweep.
- **FR-018 Exit codes.** 0 completed (including rows that are could not determine, a bound reached and Orca unavailable); 1 internal error with a `[sweep ...]` stderr prefix, including an argv outside the allowlist; 2 usage error. *AC:* one test per code.
- **FR-019 Sanitize (GQ-107).** Every untrusted string (contract text, transcript text, Orca body text, titles, paths) passes `sanitize()`: strip ESC/CSI/OSC sequences, C0 and C1 controls (this removes LF, which would otherwise end a table row), carriage returns and bidi controls, then replace `|` with `\|`. *AC:* the injection fixture renders with none of those characters and a `blocked_question` of `a|b` renders as one cell `a\|b`.
- **FR-020 Orca unavailable.** On `runtime_unavailable` or a missing `orca-ide` binary: no further `_orca` call, never `orca open`, banner "Orca unavailable", every Orca source `unscanned: orca unavailable`, disk-only rows, exit 0, `orca_available: false`. *AC:* the first `_orca` call raises; the test records one `_orca` call total and a written report.
- **FR-021 Call bounds.** At most 50 `worker-show` calls and 90 s total wall clock for probe calls per sweep (REPORT line 1247). When a bound is reached no further probe starts; remaining rows are `could not determine (call bound reached)`; the summary counts them; the report is still written. *AC:* a 60-row fixture records 50 show calls and 10 bound rows.
- **FR-022 Recommendations are text.** The report and the skill may print a "what to check next" line per waiting item and may name WC-6 or `WORKER-CONTRACT.md:74` and `:107` actions as proposals; neither performs them (subject to OQ-4). *AC:* the skill's `allowed-tools` contains only Read, Glob, Grep, `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)`.

**Command, contract, registries**

- **FR-023 Command and skill.** `sweep.md` has an Activation block that invokes `sc:sweep-protocol` and names `~/.claude/skills/sc-sweep-protocol/SKILL.md` and the project `.claude/skills/` copy; no `src/superclaude/` path; no `## Unattended mode` section. The skill runs `superclaude sweep run` with a 120000 ms Bash timeout and falls back to `uv run superclaude sweep run` on "command not found". *AC:* `tests/commands/test_sweep_command.py` asserts each item.
- **FR-024 WC-14 and never-as-worker.** Add `### WC-14. Coordinator loop` (Section 10) after the fan-in rule (`WORKER-CONTRACT.md:156`) and before `### Worked example` (`:158`); add `/sc:sweep` to the never-as-worker line (`:23`). Pin both in `tests/skills/test_worker_contract.py` (`RULE_PHRASES` entry; `NEVER_AS_WORKER` at `:245` grows to 9). Gated on PR #422 (OQ-5) and on the owner's GQ-11 answer (REPORT line 1320). *AC:* the parametrized contract tests pass with the new entries and fail when the WC-14 heading is removed.
- **FR-025 Registries and docs.** `"sweep"` in `_POST_REFRESH_ADDITIONS`; `"sc:sweep"` in `_OTHER_COMMANDS`; an "Other commands" row and the "Orca coordination" bullets in `HOW-WE-WORK.md`, byte-copied to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; user guide row; developer guide never-as-worker copy; CHANGELOG entry (REPORT steps 1.20-1.24b). *AC:* `tests/recommend`, `tests/core` and `tests/commands/test_routing_plugin_parity.py` pass.
- **FR-026 Ignore sweep output (GQ-106).** Add `.dev/sweeps/` to `.gitignore`. Today's `.gitignore` lists other `.dev/` subfolders (for example `.dev/pr-monitor/` at line 250) but not `.dev/sweeps/`. The pattern must not match `.dev/tasks/` (always staged). *AC:* `git check-ignore -q .dev/sweeps/x.md` succeeds and `git check-ignore -q .dev/tasks/x/progress.md` fails.

## 5. Non-Functional Requirements

- **NFR-001 Report is the only write.** *AC:* `tests/sweep/test_readonly.py` snapshots (path, size, mtime_ns, sha256) of every file under a fixture root, its fixture worktrees and a fixture `~/.claude/`, runs a sweep, and asserts the only difference is one new file under `<root>/.dev/sweeps/`.
- **NFR-002 Lock-free git by construction (GQ-103(1), first).** `_git` builds `["git", "--no-optional-locks", "-C", str(cwd), *args]` and sets `GIT_OPTIONAL_LOCKS=0` in the child environment; no caller can pass its own argv prefix. *AC (two parts):* (1) every recorded `_git` argv starts with `git --no-optional-locks -C`; (2) a control experiment in `tmp_path` with real git: make the index stat cache stale (touch a tracked file after `git add`), confirm plain `git status` rewrites `.git/index` (mtime changes), reset, then confirm `_git(...,"status","--porcelain","--branch")` leaves `.git/index` mtime and `.git/index.lock` absence unchanged. If the control shows no rewrite, the test is skipped as inconclusive, not passed.
- **NFR-003 Exact argv allowlist.** Each `_orca` and `_git` argv is compared as a tuple against the allowlist in Section 8 (positional ids replaced by a placeholder before comparison). An argv not on the list raises before any subprocess starts. *AC:* every recorded argv across the whole test suite is on the list; a test passes `("orchestration","worker-read",...)` and gets the exception with zero subprocess calls.
- **NFR-004 Mock-testable, no live calls.** All tests patch the two seams; no test spawns `orca`, `orca-ide`, `ccsession` or `claude`. *AC:* a session-scoped fixture patches `subprocess.run` to fail on any `argv[0]` other than `git` (used only by NFR-002's tmp repo).
- **NFR-005 Bounded runtime.** Each probe call has `timeout=10`; 90 s total; 50 `worker-show`; the skill's Bash call has `timeout: 120000`. *AC:* a fake clock test reaches the 90 s bound and still writes the report.
- **NFR-006 Deterministic.** `now` is injected; rows sort by (class order, age, id); the same inputs give a byte-identical report apart from the header timestamp. *AC:* two runs on one fixture with a fixed `now` produce identical files.
- **NFR-007 Installed-path discipline.** No `src/superclaude/` path in the command or skill (CLAUDE.md "Never Hardcode" rule). *AC:* `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol` returns nothing.
- **NFR-008 Repo gates.** `make lint`, `make verify-sync` and `uv run pytest tests/sweep tests/skills/test_worker_contract.py tests/commands tests/recommend tests/core` pass. *AC:* CI on the PR.
- **NFR-009 No new dependency.** Only the standard library, `click`, `rich` (optional) and `pyyaml` (already in `pyproject.toml:38`). *AC:* `pyproject.toml` `dependencies` is unchanged in the diff.

## 6. Architecture and Component Boundaries

The boundary that matters is between code that can touch the outside world and code that cannot. Only `probes.py` runs subprocesses and only `report.py` writes. Everything else is pure, which is what makes K-4 (mock-testable) hold.

| Module (`src/superclaude/cli/sweep/`) | Owns | May import | Must not |
|---|---|---|---|
| `__init__.py` | lazy export of `sweep_group` | `commands` (lazily) | import probes at package import |
| `models.py` | frozen dataclasses (Section 7), class and state enums | stdlib | do I/O |
| `classify.py` | `classify(row, contract, now, window) -> Classification`; package-state and safe-to-close functions | `models` | read files, run subprocesses, read the clock |
| `probes.py` | `_orca`, `_git`, the allowlist, bounds, disk reads, `sanitize()` | `models`, `yaml`, `subprocess` | write any file |
| `report.py` | Markdown render and the one write | `models` | run subprocesses |
| `commands.py` | Click group, option parsing, exit codes, JSON to stdout | all of the above | hold logic beyond wiring |

Data flow: `commands` parses options, then `probes.discover(scope, now)` returns a `Snapshot` (rows, contracts, packages, worktree git states, source coverage), then `classify` maps each row, then `report.render(snapshot, classifications)` returns text, then `report.write(path, text)` writes it, then JSON goes to stdout.

Outside the package:

- `src/superclaude/commands/sweep.md`: thin; Activation invokes the skill.
- `src/superclaude/skills/sc-sweep-protocol/SKILL.md`: runs the CLI, reads the report, summarises people-first in chat, proposes next checks as text only.
- `src/superclaude/core/WORKER-CONTRACT.md`: WC-14 and the never-as-worker line.
- Tests: `tests/sweep/` (new: `test_classify.py`, `test_probes.py`, `test_readonly.py`, `test_cli_contract.py`, `test_report.py`, `fixtures/`), `tests/commands/test_sweep_command.py`, and the pins in `tests/skills/test_worker_contract.py`.

Rejected placements, with the evidence that rules them out: A4, extending `sc-crash-recovery` (allows `Bash(git stash *)` despite "pure read-only", REPORT line 325); a skill-only sweep (no seam to mock, fails K-4, phase7-summary section 3).

## 7. Data Model and Classification States

### 7.1 Records (all frozen dataclasses; GQ-103(3) fields marked)

- `WorkerRow`: `dispatch_id`, `task_id`, `run_id`, `worktree: Path|None`, `liveness: Literal["live","unverifiable","exited"]|None`, `task_status: str|None`, `agent_wait: dict|None` (absent and null are kept apart: `agent_wait_present: bool`), `heartbeat_at: datetime|None`, `consumer_fenced: bool|None`, `worker_done_observed: bool|None` *(GQ-103(3))*, `transcript_readable: bool|None` *(GQ-103(3))*, `gate_policy: str|None` *(GQ-103(3))*, `source: str`.
- `ContractRecord`: `status`, `blocked_question: str|None`, `report_path: Path|None` *(GQ-103(3))*, `artifacts: tuple[Path, ...]` *(GQ-103(3))*, `guard_refused: bool`, `read_ok: bool`.
- `PackageRecord`: `pkg_id`, `worktree`, `state` (7.3), `running_here: bool` (FR-012).
- `WorktreeGit`: `path`, `branch`, `upstream: str|None`, `ahead: int|None`, `dirty: bool|None`, `dev_tasks_unsaved: bool|None`, `unmerged: bool|None`, `error: str|None`.
- `Classification`: `cls`, `rule: str` ("1" to "7" or "idle"), `evidence: tuple[str, ...]` (which field of which source decided it), `notes`, `waiting_kind: Literal["a","b"]|None`, `safe_to_close: tuple[str, str]`.

`rule` and `evidence` are the provenance this variant adds. Root cause it addresses: when a sweep says "stalled", the person needs to know which signal said so before they act on it; a class without its reason recreates the problem of opening the session to find out.

### 7.2 Session classes and precedence

First matching rule wins (REPORT step 1.3 rules, kept in order):

| Rule | Condition | Class |
|---|---|---|
| 1 | contract `blocked`, and the row is settled, or `gate_policy` is `report blocked`, or the Ruling is a halt (`E-HALT-QA`, `E-NO-RULING`); skipped under `ask the coordinator` on a live row | waiting on a person (a) |
| 2 | `liveness == "exited"` and `worker_done_observed is False` and `consumer_fenced is not True` | stalled (proved) |
| 3 | `consumer_fenced is True` | fenced (fixture only; on a live sweep: could not determine, "fenced evidence not readable") |
| 4 | `agent_wait` non-null: waiting (a); a frozen or foreign ready Task: waiting (b) | waiting on a person |
| 5 | `liveness == "live"`, task in progress, `agent_wait_present` and null | working |
| 6 | settled and (contract read, or `guard refused:` seen) | finished (note "partial" when `read_ok` is false) |
| 7 | anything else | could not determine |
| idle | person-started session, no Orca row, last activity older than `window` | idle |

Root-cause note on rule 2: WC-10 makes Orca's `exited` verdict the only stall proof (`WORKER-CONTRACT.md:45`). `worker_done_observed is False` must be a positive observation; `None` falls to rule 7. That is the single place where the "unknown is not stalled" property (FR-009) is enforced, so it is tested exhaustively.

### 7.3 Package states (first match wins)

1. `conflict`: the id exists in both `to-do/` and `done/` (GQ-102).
2. `interrupted archive`: a `.archiving` marker exists.
3. `unfinished`: in `to-do/`, `progress.md` has no `FINAL:` line.
4. `archive-blocked`: in `to-do/`, `progress.md` has a `FINAL:` line (GQ-105; the expected non-Linux outcome per the global CLAUDE.md level-3 row).
5. `archived`: in `done/` only.

States 1 to 4 make the owning worktree "removable: no (<state>: <id>)". No state ever produces advice to delete `.dev/tasks/` content.

## 8. Seams and Argv Allowlist

Two functions in `probes.py` are the only subprocess callers:

```python
def _orca(*args: str) -> dict | list: ...        # argv = ["orca", *args]; check_allowed(("orca", *args)); timeout=10; parse JSON
def _git(cwd: Path, *args: str) -> str: ...      # argv = ["git", "--no-optional-locks", "-C", str(cwd), *args]
                                                 # env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}; timeout=10
```

Why both the flag and the variable: the flag is the documented global option and the variable is its environment form; setting both means a future code path that builds its own `git` call under the seam still inherits the variable. The host has git 2.47.3; the flag exists since git 2.15 (UNVERIFIED against the git release notes in this session). If `git --version` reports an older git, `_git` refuses to run and every git source is `unscanned: git too old for --no-optional-locks` (failure mode F7).

**Orca allowlist (exact shapes; `<id>` is a placeholder for one argument):**

| Argv after `orca` | Used for | Note |
|---|---|---|
| `orchestration run-current` | run scope (FR-002) | JSON flag form UNVERIFIED; capture at step 1.0a |
| `orchestration worker-list --run <id> --json` | rows | cursor flag name for `page.nextCursor` UNVERIFIED; capture at step 1.0a |
| `orchestration worker-show --dispatch <id> --json` | row detail | bounded at 50 |
| `orchestration task-list --run <id> --json` | settled state | |
| `orchestration task-list --ready --run <id> --json` | waiting (b) | |
| `worktree ps --json` | worktree roots | |

Removed from the research allowlist, with reason: `gate-list`, `worker-read` and any stash verb (GQ-109); `run-list` (GQ-104 removes its only use, the no-binding fallback); `inbox` stays forbidden. The smaller the list, the smaller the surface an argv bug can reach, and every removed verb has no consumer in Sections 4 and 7.

**Git allowlist (after the fixed prefix):**

| Args | Count |
|---|---|
| `status --porcelain --branch` | exactly one per worktree (GQ-110) |
| `log --format=%H --max-count=1 <branch>..HEAD` | at most one per child worktree |
| `--version` | once per sweep, with the same prefix (`git --no-optional-locks --version`) |

No other git verb is reachable: no `stash list` (GQ-109), no `fetch`, no `rev-parse`. The `--root` default comes from walking up from the current directory to the first `.git` entry with plain path reads, so it needs no git call.

## 9. Report Format

Path: `<root>/.dev/sweeps/<YYYYMMDD-HHMMSS>-sweep.md`. Layout follows the #409 picks this research chose (header, Attention Ledger, Shift Brief, omission counts, no action controls; REPORT line 328). Sections in fixed order:

1. **Header.** Observed-at (UTC), Scope (root, worktree count, Run ids, window), "Orca: available | unavailable", per-source freshness and coverage table (`scanned` / `unscanned: <reason>` / `bound reached`), "Messages coverage: partial (no non-consuming read of pending questions, GQ-02)".
2. **Waiting on you (Attention Ledger).** Kind (a) then kind (b); columns: age, id, worktree, question or policy (sanitized), evidence (`rule` and source field), what to check next.
3. **Could not determine.** Every such row with its reason. Placed before working rows because an unknown can hide a person-wait.
4. **Stalled (proved).** With the Orca evidence line.
5. **Working, finished, fenced, idle.** One table each; empty tables print "none" rather than being omitted, so absence is visible.
6. **Worktrees.** Path, branch, dirty, unpushed, unmerged, `.dev/tasks` unsaved, packages and states, terminal releasable, worktree removable (both REVIEW, never `yes`).
7. **Retained problems.** Shared running packages (FR-012), conflicts, interrupted archives.
8. **Historical sessions.** Person-started sessions older than the window (GQ-108).
9. **Shift Brief.** Counts per class, per package state, omissions ("N rows not shown: bound reached"), and one line: "This report proposes; it acts on nothing."

Every cell from an untrusted source goes through `sanitize()` (FR-019). There are no links that run anything and no copy-paste commands that mutate state.

## 10. WC-14 Contract Rule Text Proposal

Placement: after the fan-in rule ending at `WORKER-CONTRACT.md:156`, before `### Worked example` at `:158` (REPORT step 1.17). Based on the step 1.17 draft G1 to G7 and its closing sentence, with two analyzer changes: G1 names an observable end condition (so "keep watching" is checkable, not a mood), and G8 states the observer-effect guarantee that makes G3 safe to run on every wake.

```markdown
### WC-14. Coordinator loop

The coordinator keeps watching its Run until every Task it created is settled and admitted, as shown by the Run's own task list; it never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake, the coordinator runs `/sc:sweep` and reads its report before it acts. The sweep's classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine. The coordinator tells the person about each of these and keeps it in its run notes until the person answers: a `failed` or `blocked` result it cannot retry, a `partial` result it has judged unusable, a third brief-guard refusal, a ready Task it did not create, a frozen plan, and a fan-in with fewer than 2 admitted inputs. Person-started sessions appear in the report, observed from their files; they are never messaged. The sweep report is a dated local file; it is never posted. The sweep reads each worktree without taking git's optional locks, so a sweep never causes the `index.lock` case above. The sweep only recommends the stop-and-cancel step for a stalled attempt, worktree removal and a new Task; the coordinator performs them under those rules, and a replacement is always a new Task (WC-6).
```

Checks against the test helpers: the heading line holds both `WC-14` and the first pin phrase, as `_check_rule` requires (REPORT step 1.19 cites `:388-395`); all three pins ("WC-14. Coordinator loop", "On every coordinator wake", "it is never posted") appear verbatim; the text names no setup flag or repo-code span, so `_check_repo_setup_gated` (`test_worker_contract.py:446`) has nothing to flag. If the owner rules against proposals (REPORT row 98b), the last sentence becomes the step 1.17 alternative: "The sweep recommends none of these actions; the coordinator decides and performs them under those rules." `/sc:sweep` stays out of `UNATTENDED_COMMANDS` (REPORT step 1.19).

## 11. Failure Modes and Evidence

Each row: the failure, the evidence that it can happen, the mechanism that contains it, and the test that proves containment.

| # | Failure | Evidence it is real | Containment | Test |
|---|---|---|---|---|
| F1 | Orca absent or down | `runtime_unavailable` is a documented Orca reply (codebase-context section 1 item 2) | FR-020: disk-only sweep, banner, exit 0, never `orca open` | first `_orca` raises; one call recorded |
| F2 | Worktree removed mid-sweep | `worktree ps` and the `git status` call are separate moments; nothing snapshots the filesystem (BASH_INSPECTION_POLICY "separate subshells ... do not provide a filesystem snapshot") | `_git` non-zero or missing path gives `WorktreeGit.error`, row "could not determine (worktree gone)" | fixture deletes the dir between the two seams |
| F3 | Unreadable or partial transcript | transcripts are written live by another process (seed brief Batch 3) | `transcript_readable=False`; rule 7; never idle | truncated-JSONL fixture |
| F4 | Stale list data | `evidence.liveStatus` can lag; the list row schema is uncaptured (GQ-01, REPORT line 1164) | classifier reads only `worker-show` fields; stale gives rule 7 | fixture where list and show disagree; show wins |
| F5 | Slow worker read as dead | WC-10: a late heartbeat is absence (`WORKER-CONTRACT.md:45`) | rule 2 requires `exited`; heartbeat age only adds a note | late-heartbeat live fixture is never `stalled (proved)` |
| F6 | Call bound exhausted | 50-show and 90 s bounds (REPORT line 1247) on a large Run | FR-021: remaining rows "call bound reached", counted in Shift Brief | 60-row fixture |
| F7 | Sweep takes `index.lock`, worker reports `blocked` | WC-9: "A worker that finds `index.lock` in its worktree reports `blocked` with the path" (`WORKER-CONTRACT.md:44`); plain `git status` may refresh the index (GQ-103(1)) | NFR-002 prefix and variable; `git --no-optional-locks --version` failure marks git sources unscanned | NFR-002 control experiment |
| F8 | Untrusted text breaks the report | contract and transcript text are written by workers and people | FR-019 `sanitize()` | injection fixture |
| F9 | Symlink leads outside the root | fixed patterns under user-writable folders | FR-006 `resolve()` check | symlink-out fixture |

F7 is the only failure in which the sweep itself would cause harm to a live worker rather than misreport it, which is why it is solved in the seam and not left to callers.

## 12. Risks and Mitigations

| Risk | Likelihood / impact | Mitigation |
|---|---|---|
| R1 False "waiting on a person" sends the person to a session that needs nothing | medium / low | evidence column names the rule and field; rule 1 needs a settled row or explicit policy |
| R2 False "stalled (proved)" leads the coordinator to cancel a live worker | low / high | rule 2 needs a positive `exited` and a positive `worker_done_observed is False`; property test FR-009; the sweep never acts |
| R3 A real person-wait is missed (no non-consuming question read, GQ-02) | medium / high | header "Messages coverage: partial"; non-null `agentWait` and blocked contracts as stand-ins; could-not-determine listed before working rows |
| R4 Shared-package false positives drown the Retained-problems list | high before GQ-101 fix / medium | FR-012 counts only changed paths in a worktree's own status output |
| R5 Merge conflict with PR #422 on `WORKER-CONTRACT.md` | depends on order / medium | step 1.16a gate; steps 1.17-1.19 land after #422 or move to a follow-up PR (OQ-5) |
| R6 #409 layout drifts after it merges | low / low | cite `495eb96d`; re-diff at step 1.16a |
| R7 Injected text in a contract or transcript misleads the reader | medium / medium | FR-019; text is shown as data inside table cells |
| R8 The report file dirties the worktree and shows up in `git status` | certain without GQ-106 / low | FR-026 ignore line; the next sweep would otherwise flag its own output as uncommitted |
| R9 A worker runs `/sc:sweep` | low / low (read-only) | never-as-worker line and WC-14 make it a contract rule; no mechanical guard (K-1, REPORT step 1.18) |

R8 is worth a root-cause note: without the ignore line the sweep would observe its own previous write as "uncommitted changes" in the root worktree, a feedback loop that makes every second sweep report a problem the sweep created.

## 13. Gap Resolution (GQ-101 to GQ-113)

Gap rows are from GAPS lines 124-136; the "root cause" column is this variant's analysis, not GAPS text. Ordered with the safety item first, as the seed brief requires.

| Gap | Root cause found | Resolution in this spec |
|---|---|---|
| GQ-103(1) | the sweep's own `git status` can refresh the index and take `index.lock`, triggering WC-9 in a live worker | NFR-002: flag plus `GIT_OPTIONAL_LOCKS=0` fixed inside `_git`; argv test plus real-git control experiment; F7 |
| GQ-103(2) | the window was a constant, so tests could not vary it | FR-003: `classify(row, contract, now, window)` |
| GQ-103(3) | precedence rules named fields the model did not have | Section 7.1 adds `gate_policy`, `worker_done_observed`, `transcript_readable`, `report_path`, `artifacts` |
| GQ-101 | presence of a package folder was used as a proxy for "running here"; committed folders exist in every worktree | FR-012: a package runs in a worktree only when that worktree's own status lists a changed path under it |
| GQ-102 | the state machine had no state for an id in both `to-do/` and `done/` | Section 7.3 state 1 `conflict`, blocks removal |
| GQ-104 | a `run-list` fallback guessed scope, which spends the call bound on Runs the person did not ask about | FR-002: exit 2 asking for `--run`; `run-list` removed from the allowlist |
| GQ-105 | archive-blocked was not distinguishable from unfinished | Section 7.3 state 4 from a `FINAL:` line |
| GQ-106 | the output folder was not ignored and not in the rollback table | FR-026 and Section 15 |
| GQ-107 | a pipe character in untrusted text splits a table cell | FR-019 escapes it as `\|` after control stripping |
| GQ-108 | person-started sessions had no join rule and no age rule | FR-007 |
| GQ-109 | the allowlist held verbs with no consumer (`gate-list`, `worker-read`, stash) | Section 8 removes them |
| GQ-110 | several git calls per worktree multiplied lock exposure and runtime | FR-014: one status call answers four questions |
| GQ-111 to GQ-113 | REPORT citations of the gap count predate rows 101-113 | handled without editing REPORT: this spec cites GAPS line 138 (113 rows, 88 open, 25 resolved) and reads REPORT line 1537 ("Every open GQ row is cited") as covering GQ-01 to GQ-100 only |

## 14. Open Questions and Recommended Answers

| # | Question | Recommended answer | Reason |
|---|---|---|---|
| OQ-1 | GQ-01: design for list plus `worker-show`, or capture the row schema first (step 1.0a)? | Design for the list-plus-show worst case now; run step 1.0a as a read-only capture saved to the package `artifacts/`; use it only to confirm the two UNVERIFIED flag forms (Section 8) and to plan a later optimisation | building on an uncaptured schema is the exact failure REPORT line 1541 rates Critical; the worst-case design is correct whatever the capture shows |
| OQ-2 | GQ-02: which signal stands in for pending questions? | Non-null `agentWait` and `blocked` contracts, plus the "Messages coverage: partial" header line | both are reads that consume nothing; saying the coverage gap out loud is cheaper than a false "nobody is waiting" |
| OQ-3 | GQ-04: WC-14 wording | Section 10 text | it names an observable end condition and keeps the three pins |
| OQ-4 | May the sweep print proposals (stop-and-cancel, removal, new Task)? | Yes, as text only, pending the owner (REPORT row 98b) | the person still decides; FR-022's allowed-tools make "text only" mechanical for the skill; the alternative sentence is ready if the owner says no |
| OQ-5 | Sequencing with PR #422 | Ship the new package, command, skill and docs first; land steps 1.17-1.19 after #422 merges, in this PR if it merges first, otherwise a follow-up PR | the CLI does not depend on the contract text, so the gate costs nothing to the code path |
| OQ-6 | #409 layout: copy or cite? | Copy the chosen sections into the design (Section 9) and cite `495eb96d` as their origin | an unmerged commit can move; the design must stand on its own |
| OQ-7 | 6 h or 72 h default window? | 6 h, with older person sessions under Historical sessions | the topic fixes 6 h; 72 h is a crash-recovery horizon, and Historical keeps the older data visible |
| OQ-8 | GQ-11: WC-14 or reuse the unused WC-1 ID? | WC-14 | the next free ID (REPORT line 70); reusing WC-1 risks old references meaning a different rule; owner decision gates FR-024 |

## 15. Rollback

Phase 1 adds code and text and writes only reports, so rollback is deletion and revert; there is no data migration (REPORT rollback table, lines 1304-1320).

| Part | Rollback |
|---|---|
| `src/superclaude/cli/sweep/` and the deferred registration in `cli/main.py` | delete the package; remove the registration lines |
| `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/` | delete; `make sync-dev` removes nothing by itself, so also delete the `.claude/` dev copies and re-run `superclaude install` for installed copies (UNVERIFIED whether install prunes removed files) |
| WC-14, never-as-worker line, contract pins | revert the `WORKER-CONTRACT.md` and `test_worker_contract.py` hunks together, so the pins and the text never disagree |
| Registries, `HOW-WE-WORK.md` and its plugin byte copy, guides, CHANGELOG | revert together; the parity test checks the byte copy |
| `.gitignore` `.dev/sweeps/` line (GQ-106) | remove the line |
| Existing reports under `.dev/sweeps/` | keep; they are local, ignored and harmless; delete by hand only if the person wants |

Rollback check: after the revert, `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_worker_contract.py tests/commands tests/recommend tests/core` pass, and `superclaude sweep --help` exits 2 as an unknown command (UNVERIFIED: Click's exit code for an unknown subcommand is assumed to be 2).
