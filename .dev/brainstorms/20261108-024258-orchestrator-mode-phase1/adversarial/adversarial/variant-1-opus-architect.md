# Spec: Orchestrator Mode Phase 1, read-only `/sc:sweep` and WC-14 (#339)

| Field | Value |
|---|---|
| Variant | 1 |
| Model | opus |
| Persona | architect |
| Emphasis | maintainability and extension scaffolding |
| Date | 2026-11-08 |
| Status | draft for adversarial debate |

Sources read for this spec: `seed-brief.md` (whole); REPORT Section 8 Phase 1 (lines 1216-1340); GAPS lines 118-140; `synthesis/phase7-summary.md`; `enrichment/codebase-context.md`; `src/superclaude/core/WORKER-CONTRACT.md` lines 20-79 and 104-159; a grep of `.gitignore`. REPORT = the research report, GAPS = `gaps-and-questions.md`, both in `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`. Anything not traced to those reads is marked UNVERIFIED.

## 1. Problem and scope

**Problem.** A person running many Claude Code sessions across Orca worktrees must open each one to learn whether it is working, waiting for them, stuck, finished or safe to close. The worker contract has no rule that the coordinator keeps polling, re-arms an expired wait or sweeps on a schedule (seed brief line 17; `WORKER-CONTRACT.md:45` is the only match for those words, REPORT line 48 via phase7 summary).

**Goal of Phase 1.** One coordinator-only, read-only command that observes one worktree tree, classifies every Orca worker and every person-started Claude session over a 6 h activity window, and writes one dated Markdown report; plus the WC-14 coordinator-loop rule in the worker contract.

**Success metric.** The person answers "who needs me, and what is safe to close" from one report, without opening a child session (seed brief line 47).

**Scope.**

- One worktree tree: a feature worktree and its Orca child worktrees (seed brief line 26).
- Inputs: Orca read verbs, one `git status` per worktree, task-package ledgers and contracts on disk, ccsession tab map and transcript files. No new store.
- Output: one dated report file under `<root>/.dev/sweeps/` and JSON on stdout. That file is the only write.
- Deliverables: package `src/superclaude/cli/sweep/`, command `src/superclaude/commands/sweep.md`, skill `src/superclaude/skills/sc-sweep-protocol/`, tests under `tests/sweep/`, WC-14 and the never-as-worker addition, routing registries and docs (REPORT steps 1.1 to 1.29).

**Architectural stance of this variant.** Phase 1 is the first of six phases. Its code must be the stable read model the later phases build on, so this spec fixes four extension points now and keeps everything else minimal: the ordered rule table in `classify.py`, the exact read allowlist table in `probes.py`, the versioned JSON output, and a hard split between read code (this package) and any future write code (a separate package with its own seam). Nothing speculative is built; the points are shapes, not features.

## 2. Out of scope (later phases, recorded with blockers)

Phase numbers are the REPORT's, not a source's (REPORT line 1324). None is designed here.

| Phase | What | Blocker before it can start | Extension point it will use |
|---|---|---|---|
| 2 `/sc:close` | Act on safe-to-close REVIEW rows after the person confirms | Section 4 refusals turned into executed checks, "all commits pushed" and the `.dev/tasks/` rule; removal only through `orca worktree rm`; named instruction plus confirmation at the moment of action; contract edits after PR #422 (REPORT line 1328) | Reads sweep JSON schema v1 as a hint only, re-probes before acting; own package and own write allowlist (FR-021) |
| 3 Resume | Resume a stalled (proved) or frozen session as a new Task | WC-6 and WC-10; needs positive stall proof, never `unverifiable` (REPORT line 1329) | New rows in the classify rule table, never a reorder |
| 4 Trust layer | One permission mode, fixed message types, signed narrow grants | `CCSESSION_PERMISSIONS=default` mode mismatch; no Macaroon or Biscuit design; comment-3 research and debate first (REPORT line 1330) | None in the sweep package |
| 5 Orchestrator of orchestrators | Sweep several coordinators' Runs | Version-2 work after the comment-3 research (REPORT line 1331) | Repeatable `--run`; `scope` field in JSON |
| 6 Management-server relay | Relay results through a management server | Owner must define "management server" (GQ-66); no standing service (REPORT line 1332) | JSON schema v1 |

Also out of Phase 1: `check --peek` and `check --all` (gated on a probe of 06 Gaps 1, 2 and 18, REPORT line 1302); `--include-remote` until its cost is measured (GQ-22); any `gh` call; `gate-list`, `worker-read`, `run-list`, `git stash list`, `git log`, `git branch` (GQ-104, GQ-109, GQ-110, this spec section 7).

## 3. Functional requirements

Each acceptance criterion (AC) is checked with the two seams mocked (section 7) unless it says "live".

| ID | Requirement | Acceptance criterion |
|---|---|---|
| FR-001 | `superclaude sweep run [--run <id>]... [--window <N>h\|<N>d] [--root <dir>] [--output <dir>]` exists, registered with the deferred-import pattern in `cli/main.py` (REPORT step 1.7). | `superclaude sweep --help` and `sweep run --help` exit 0 under `CliRunner` (step 1.13). |
| FR-002 | Run selection: `--run` is repeatable; with none given the sweep uses the `run-current` binding; with no binding it exits 2 with `no Run bound: pass --run <id>`. No `run-list` fallback (GQ-104). | Fixture with `run-current` empty gives exit 2 and that text; no `worker-list` or `worker-show` argv is recorded. |
| FR-003 | `--window` default `6h`; anything other than a positive integer plus `h` or `d` is a usage error (exit 2). | Parser cases `6h`, `3d` pass; `0h`, `6`, `6m`, `-1h` exit 2. |
| FR-004 | `--output` default `<root>/.dev/sweeps/`; a resolved path outside `<root>/.dev/` is a usage error. | `--output /tmp/x` exits 2 and writes nothing. |
| FR-005 | The sweep lists every Orca Task/Dispatch row of the selected Runs, every worktree under the tree, and every person-started session (FR-010). | Fixture with 3 workers, 2 worktrees, 1 person session yields 6 rows in JSON and in the report; `<shown>/<total>` equal. |
| FR-006 | Each session row gets exactly one class from section 6, chosen by the ordered rule table. | Parametrized test: one case per section 6 rule (REPORT rules 1-7 plus idle); each class name is reached at least once. |
| FR-007 | `classify` receives a `SweepContext` holding `now`, `window` and `window_start` (GQ-103(2)). | A row with transcript mtime 5 h old is idle-eligible only when window is under 5 h; same row, window 6 h, is not idle. |
| FR-008 | "Could not determine" is its own class, never folded into stalled or idle; `unverifiable`, a late heartbeat, a stale `liveStatus` or a missing row give it (WC-10, `WORKER-CONTRACT.md:45`). | Fixtures for each of the four inputs give `could not determine`, never `stalled (proved)`. |
| FR-009 | Stalled (proved) only from Orca's own exit proof with no `worker_done` and no fencing evidence; with fencing evidence unreadable it is could not determine with note "fenced evidence not readable" (REPORT step 1.3 rules 2, 3; GQ-84). | Synthetic `exited` fixture without `worker_done` and with unreadable transcript gives could not determine plus that note. |
| FR-010 | A person-started session is a transcript under a scanned root's project key that the ccsession tab map joins to no Orca row; one with no activity inside the window goes to Historical sessions (GQ-108). | Fixture: 2 transcripts, one mapped to an Orca row, one not; only the unmapped one is person-started; an 8 h old unmapped one is listed under Historical. |
| FR-011 | Waiting on a person comes first in the report, split into (a) explicit questions, oldest first, tie-break by ID, unknown age in its own group, and (b) blocked by policy, never with question text (REPORT step 1.5). | Rendered heading order test; sort test with 3 ages plus one unknown. |
| FR-012 | Safe-to-close is a separate two-part REVIEW value (terminal, worktree), each `yes`, `no` or `could not determine`. Phase 1 never prints `worktree removable: yes`. | Over all fixtures, no row has `safe_to_close.worktree == "yes"`. |
| FR-013 | A worktree is `removable: no` with the condition named when status shows uncommitted changes, an unpushed branch (ahead or no upstream), an unsaved path under `.dev/tasks/`, a frozen plan, a package in state unfinished, interrupted-archive or conflict, or an active package shared with another worktree. | One fixture per condition; each prints `no` plus its named reason. |
| FR-014 | Package states are read per package folder: `unfinished`, `archive-blocked`, `interrupted-archive`, `conflict`, `archived`, `unknown` (section 6; GQ-102, GQ-105). | Fixture per state, including one package id in both `to-do/` and `done/` giving `conflict`. |
| FR-015 | One package id is "shared" only when it is active in two or more worktrees; active means that worktree's single `git status` shows a changed or untracked path inside that package folder (GQ-101). | Shared-folders fixture: 3 worktrees with the same 44 committed, unchanged folders give no shared flag; one folder modified in 3 worktrees gives one line naming all 3. |
| FR-016 | Every untrusted string passes `sanitize()`, which strips ESC/CSI/OSC, C0/C1 controls, carriage returns and bidi controls, folds newlines to a space, and escapes the pipe character with a backslash (REPORT step 1.5; GQ-107). | Injection fixture includes `a\|b`, an ANSI sequence and a bidi override; the rendered table keeps its column count. |
| FR-017 | The report is written to `<output>/<YYYYMMDD-HHMMSS>-sweep.md`; JSON schema v1 is printed to stdout with every key always present (REPORT step 1.6). | Key-set and type test on stdout; file exists at the dated path. |
| FR-018 | Exit codes: 0 sweep completed (including could-not-determine rows and Orca down); 1 internal error with `[sweep ...]` stderr prefix, including an argv outside the allowlist; 2 usage error. | One test per code. |
| FR-019 | Orca unavailable (`runtime_unavailable`): banner "Orca unavailable", no further `_orca` call, discovery from `--root` fixed patterns only, every Orca source `unscanned: orca unavailable`. | Fixture raising on first `_orca`; exactly one `_orca` argv recorded; report still written; exit 0. |
| FR-020 | Per-sweep bounds: at most 50 `worker-show` calls, 10 s per call, 90 s total probe budget; once reached, no new probe starts and remaining rows print could not determine with `unscanned: call bound reached` (REPORT step 1.4). | Fixture with 60 rows: exactly 50 `worker-show` argv recorded, 10 rows bound-reached, `summary.bound_reached == 10`. |
| FR-021 | Read and write code never share a seam or a table: the sweep package holds no write verb, and no later phase adds one to it. | Static test: `probes.ALLOWED_ORCA` holds no verb from a fixed forbidden list (`check`, `ask`, `reply`, `send`, `inbox`, `open`, `worker-start`, `task-create`, `task-update`, `dispatch`, `stop`, `rm`). |
| FR-022 | `/sc:sweep` command and `sc-sweep-protocol` skill: the command's Activation block invokes the skill by installed path `~/.claude/skills/sc-sweep-protocol/SKILL.md` with the project `.claude/` copy as dual surface; the skill calls `superclaude sweep run` from PATH first, `uv run superclaude sweep run` on "command not found"; no `## Unattended mode` section (REPORT steps 1.14-1.16). | `tests/commands/test_sweep_command.py` asserts each of these and both `allowed-tools` literals. |
| FR-023 | WC-14 "Coordinator loop" is added to `WORKER-CONTRACT.md` (section 9) and `/sc:sweep` joins the never-as-worker list; both pinned in `tests/skills/test_worker_contract.py` (REPORT steps 1.17-1.19). | `RULE_PHRASES["WC-14"]` and the 9-entry `NEVER_AS_WORKER` pass; `sweep` absent from `UNATTENDED_COMMANDS`. |
| FR-024 | Routing registries and docs: `_POST_REFRESH_ADDITIONS`, `HOW-WE-WORK.md` "Other commands" row and "Orca coordination" bullet, its plugin byte copy, `_OTHER_COMMANDS`, user guide row, developer-guide never-as-worker copy, CHANGELOG (REPORT steps 1.20-1.24b). | `tests/recommend`, `tests/core`, `tests/commands/test_routing_plugin_parity.py` pass. |
| FR-025 | `.dev/sweeps/` is added to `.gitignore` (GQ-106). A grep on 2026-11-08 found no `sweeps` entry today. | `git check-ignore .dev/sweeps/x.md` succeeds in a test checkout; a sweep leaves `git status --porcelain` unchanged. |

## 4. Non-functional requirements

| ID | Requirement | Acceptance criterion |
|---|---|---|
| NFR-001 | Read-only: the report file and its directory are the only filesystem change (REPORT step 1.11). | Snapshot-diff test with `HOME` and `XDG_STATE_HOME` inside the isolated root: exactly one added file (plus the `--output` dir if new); `subprocess.run`, `Popen`, `os.system` patched to raise. |
| NFR-002 | Lock-free git: every `_git` argv starts `git --no-optional-locks -C <path>` and the seam sets `GIT_OPTIONAL_LOCKS=0` in the child environment (GQ-103(1); section 7). | Recorded-argv test: every argv has `--no-optional-locks` at index 1; env test on the seam. |
| NFR-003 | Exact allowlist: every recorded `_orca` argv equals one allowlisted template after placeholder substitution, never a prefix match (REPORT step 1.10). | Full-sweep recording test plus negative cases (`check`, `inbox`, `worker-read`, `gate-list`, extra flag) that raise `ValueError`. |
| NFR-004 | Pure core: `classify.py` and `report.render` import no `subprocess`, `click`, `os` or `shutil`, and do no I/O. | AST import test over both modules. |
| NFR-005 | Determinism: same `SweepInput` and same `SweepContext` give a byte-identical report and JSON. | Render twice from one fixture; assert equal bytes. |
| NFR-006 | No import-time side effects: `sweep/__init__.py` exports `sweep_group` lazily (REPORT step 1.1). | Importing `superclaude.cli.sweep` records no seam call. |
| NFR-007 | Bounded runtime: total probe time 90 s or less; the skill runs the Bash call with timeout 120000 ms. | FR-020 test; static check of the skill text. |
| NFR-008 | Safety over completeness over convenience (seed brief line 27): a lost or unscanned source never resolves a question, fails a session, lifts a freeze or yields a recommendation. | Source-loss fixture: affected rows are could not determine with the `unscanned:` reason. |
| NFR-009 | Schema stability: JSON carries `schema_version: 1`; a key is never removed or renamed within v1; additions only. | Golden key-set test; a change to the key set fails unless `schema_version` changes. |
| NFR-010 | Rule-order stability: the class precedence is the order of `classify.RULES`, pinned by name. | Test asserts `[r.name for r in RULES]` equals the section 6 list. |
| NFR-011 | Installed primitives use `~/.claude/...` paths only; no `src/superclaude/` path in the command or skill (CLAUDE.md rule). | `tests/commands/test_sweep_command.py` path assertion; step 1.28 grep. |
| NFR-012 | Repo gates: `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check src/ tests/` and the affected tests pass; `.claude/` never staged except `settings.json`. | CI and local run of REPORT steps 1.25-1.27. |
| NFR-013 | No live Orca, ccsession or Claude launch in tests. | Tests run with the seams patched and real subprocess entry points patched to raise (NFR-001). |

## 5. Architecture and component boundaries (A1 layout)

Option A1 (REPORT line 1098): a Python CLI with a pure classifier and one probe module, called by a thin command and a protocol skill. A4 (extend `sc-crash-recovery`) is rejected because that skill allows `git stash` and has scanner bugs (REPORT line 325); a skill-only sweep is rejected because it cannot be mock-tested (K-4).

**Package layout** (six modules, matching REPORT steps 1.1 to 1.6; no seventh module):

| Module | Role | May import | Must not import |
|---|---|---|---|
| `__init__.py` | Lazy `__getattr__` export of `sweep_group`, as `cli/recommend/__init__.py:12-20` (REPORT step 1.1) | `commands` (lazily) | anything at import time |
| `models.py` | Frozen dataclasses, class-name `str` constants, `SweepContext`, `SweepInput`, `SweepResult`, `JSON_SCHEMA_VERSION = 1` | stdlib `dataclasses`, `datetime`, `pathlib` (types only) | every other sweep module |
| `classify.py` | Pure: `RULES`, `classify`, `policy_of`, `package_state`, `mark_shared_packages`, `safe_to_close`, `classify_all(SweepInput, SweepContext) -> SweepResult` | `models` | `probes`, `report`, `commands`, `subprocess`, `click`, `os` |
| `probes.py` | The two seams, `ALLOWED_ORCA`, `ALLOWED_GIT`, the call `Budget`, disk readers, `collect(ctx, runs, root) -> SweepInput` | `models`, `subprocess`, `os`, `json` | `classify`, `report`, `click` |
| `report.py` | `sanitize`, pure `render(SweepResult, SweepContext) -> str`, and `write_report(text, output_dir, now) -> Path`, the package's only write | `models` | `probes`, `classify`, `subprocess`, `click` |
| `commands.py` | Click group `sweep`, subcommand `run`: parse options, build `SweepContext`, call `collect`, `classify_all`, `render`, `write_report`, echo JSON | all of the above, `click`, `json` | nothing extra |

**Data flow.** `commands` builds `SweepContext(now, window, window_start, root, runs)` once. `probes.collect` returns a `SweepInput`: raw observations only, no derived class. `classify.classify_all` turns it into a `SweepResult` (rows with class, policy and safe-to-close; worktrees with package states and shared flags). `report.render` and the JSON builder both read only `SweepResult`. This three-stage split is the maintainability core: every behaviour except the seams is a pure function of two frozen values, so every test in `tests/sweep/` except the seam and read-only tests builds a `SweepInput` directly from fixtures.

**Boundary rules (pinned by tests).**

- B1. Dependency direction is one way: `commands -> {probes, classify, report} -> models`. An AST import test fails on any other edge (extends NFR-004).
- B2. `classify` and `render` never see a `Path` they could open: paths are data only.
- B3. The read allowlist lives only in `probes.py`. A later phase that writes (Phase 2 `/sc:close`) gets its own package, its own write seam and its own allowlist; it may import `sweep.models`, `sweep.classify` and `sweep.probes.collect`, and must re-collect before any action rather than trust a stored report or JSON (FR-021).
- B4. Command and skill are thin: all logic sits in the CLI; the skill only runs the CLI, reads the report path from JSON and summarises it. No classification text is duplicated in Markdown primitives.
- B5. `superclaude.contracts` names are not re-declared under `src/superclaude/cli/` (lint Check 11, REPORT line 1227).

**Extension points fixed now (shape only, no extra code).**

| Point | Where | How a later phase extends it |
|---|---|---|
| Rule table | `classify.RULES: tuple[Rule, ...]` | Insert a named rule at a stated position; NFR-010 makes the reorder visible in review |
| Read allowlist | `probes.ALLOWED_ORCA: tuple[ArgvTemplate, ...]` | Add one template after a recorded read-only probe (REPORT step 1.0a method); never a write verb (FR-021) |
| Sources | `SourceCoverage` rows built by `collect` | A new source adds one coverage row; the report header lists it with no renderer change |
| Machine output | JSON `schema_version: 1` | Additive keys only; Phase 2, 5 and 6 consume it |

## 6. Data model and classification states

All types are frozen dataclasses in `models.py`. Class and state names are plain `str` constants (printed as they are), collected in tuples, as REPORT step 1.2 decides. Fields added by this spec for GQ-103(3) are marked (new).

- `SweepContext`: `now: datetime` (UTC, injected), `window: timedelta`, `window_start: datetime`, `root: Path`, `runs: tuple[str, ...]`.
- `OrcaObservation`: `liveness_verdict` (`live`, `unverifiable`, `exited` or None), `status`, `outcome`, `agent_wait: object | None`, `agent_wait_present: bool` (null versus absent, GQ-58), `parent`, `worktree_path`, `body_text`, `unsupervised: bool | None`, `terminal_state`, `next_action`, `worker_done_seen: bool | None` (new), `fenced_evidence: str` (new; `present`, `absent` or `unreadable`; always `unreadable` on live rows in Phase 1, REPORT step 1.3 rule 3), `task_spec_text: str | None` (new; source of the gate policy line).
- `ContractRecord`: `path`, `worker_status`, `blocked_question`, `reason`, `report_path: Path | None` (new), `artifacts: tuple[Path, ...]` (new), `command: str | None` (new).
- `SessionRow`: `id`, `person_started: bool`, `orca: OrcaObservation | None`, `contract: ContractRecord | None`, `transcript_path`, `transcript_readable: bool | None` (new), `last_activity: datetime | None`, `gate_policy: str | None` (new; `report blocked`, `ask the coordinator`, or None when the spec cannot be read), and the ten #409 dimensions defaulting to `unknown` (REPORT step 1.2).
- `PackageRecord` (new): `id`, `location` (`to-do`, `done`, `both`), `has_final_line: bool | None`, `archiving_marker: bool`, `active: bool | None`, `state: str` (set by `classify.package_state`).
- `WorktreeState`: `path`, `status_read: bool`, `uncommitted`, `unpushed`, `dev_tasks_unsaved` (each `bool | None`, all parsed from the one status call), `changed_paths: tuple[str, ...]`, `packages: tuple[PackageRecord, ...]`, `shared_package_ids: tuple[str, ...]`, `frozen: bool | None`.
- `Classification`: `cls`, `waiting_kind` (`a`, `b` or None), `rule: str` (new; name of the rule that matched, printed in JSON for audit), `evidence`, `notes`.
- `SafeToClose`: `terminal`, `worktree` (each `yes`, `no`, `could not determine`), `reason`.
- `SourceCoverage`: `name`, `coverage`, `age_seconds`, `unscanned`.

**Session classes and precedence.** `classify` walks `RULES` in order; the first rule that returns a value wins. Policy (frozen or not) is computed separately by `policy_of` for every row (GQ-96: dimensions are independent).

| Order | Rule name | Class | Condition (REPORT step 1.3) |
|---|---|---|---|
| 1 | `blocked_contract` | waiting on a person (a) | Contract `worker_status: blocked` and rule 1's condition: Orca row settled, or `gate_policy == "report blocked"`, or a Ruling halt (`E-HALT-QA`, `E-NO-RULING`). Under `ask the coordinator` on a live unsettled row the rule declines and adds note "blocked contract under ask the coordinator; may be re-running"; with `gate_policy` None on a live row it returns could not determine with that note |
| 2 | `orca_exit_proof` | stalled (proved) | `liveness_verdict == "exited"`, `worker_done_seen is False`, `fenced_evidence == "absent"`. With `fenced_evidence == "unreadable"` or `transcript_readable is False`: could not determine, note "fenced evidence not readable" (GQ-84) |
| 3 | `fenced` | fenced | `fenced_evidence == "present"` (synthetic fixtures only in Phase 1) |
| 4 | `waiting_signal` | waiting on a person (a) or (b) | (a) non-null `agent_wait`; (b) frozen plan from a `failed` contract with a STOP code other than `E-RESUME-NEEDED`, or a ready Task (creator: could not determine) |
| 5 | `working` | working | `live`, `in_progress`, `agent_wait_present` and null |
| 6 | `finished` | finished | Settled outcome and a parsed contract (`succeeded`, `partial` with note "partial: usable not yet judged", `failed`), or a `guard refused:` body |
| 7 | `idle` | idle | `person_started` and `last_activity < window_start` within Historical rules; never for an Orca row, never for a just-dispatched worker |
| 8 | `fallback` | could not determine | Everything else, including `unverifiable`, absent `agentWait` on an unsettled row, a context-only Dispatch, an active person session (note "person session, active") |

The REPORT numbers idle outside 1-7; this spec places it as rule 7 and the fallback as rule 8 so the table is total and ordered. Cross-cutting notes: non-null `parent` adds "WC-13 violation, review" (GQ-40). Never inputs to the class: `projection.stage.activity` and `resource.terminalState` (REPORT step 1.3).

**Package states** (precedence top to bottom, first match wins; read by `package_state`):

| State | Condition | Blocks worktree removal |
|---|---|---|
| `conflict` | Same id in `to-do/` and `done/` (GQ-102) | yes |
| `interrupted-archive` | `.archiving` marker present (checked with `os.stat`, never cleared) | yes, listed under Retained problems |
| `archive-blocked` | In `to-do/` and `progress.md` has a `FINAL:` line (GQ-105) | no by itself, printed in Package state column |
| `unfinished` | In `to-do/`, ledger read, no `FINAL:` line | yes (refusal condition 4, `WORKER-CONTRACT.md:108`) |
| `archived` | In `done/` only | no |
| `unknown` | Ledger unreadable | prints could not determine |

**Safe-to-close.** Terminal releasable needs `terminal_state == "reclaimable"`, `next_action == "release"` and the result already read; the read is not observable, so Phase 1 prints `could not determine (result read not observable)` plus the Orca values; `retained` is never releasable. Worktree removable prints `no` with the first observed condition from FR-013, else `could not determine (report read, open PR and unmerged commits not observable)`.

## 7. Probe seams and argv allowlist

**Seams** (REPORT step 1.4). Both live in `probes.py`; nothing else in the package calls `subprocess`.

- `_orca(*args) -> str` runs `["orca-ide", *args]`.
- `_git(cwd, *args) -> str` builds `["git", "--no-optional-locks", "-C", str(cwd), *args]` itself and passes `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. A caller passes only the subcommand, so no call site can omit the flag. This is the first item built and the first test written (GQ-103(1)).
- Both use `subprocess.run(argv, capture_output=True, check=True, text=True, timeout=10)`, check the argv against the allowlist before running, and raise. An argv outside the allowlist raises `ValueError` (exit 1, a bug, not a source loss). Probe functions catch `(OSError, subprocess.SubprocessError)` and record the source as `unscanned: <reason>`.
- A `Budget` object (50 `worker-show`, 90 s total) is passed into `collect`, never global, so tests set it per case.

Why lock-free git: WC-9 at `WORKER-CONTRACT.md:44` says a worker that finds `index.lock` in its worktree reports `blocked` with the path. A plain `git status` may refresh the index and take that lock, so an unflagged sweep could block a live worker. `--no-optional-locks` is in REPORT step 1.4 via GQ-103(1); the `GIT_OPTIONAL_LOCKS` variable is from git's own documentation, not from a repo file (UNVERIFIED here), and is kept as belt and braces.

**Orca allowlist** (exact templates; `<run>` and `<dispatch>` must match an id regex fixed after the step 1.0a capture, UNVERIFIED shape today):

| Template | Purpose |
|---|---|
| `orchestration run-current` | Default Run binding (FR-002) |
| `orchestration worker-list --run <run> --json` | Rows, 100 per page; the cursor flag name is UNVERIFIED until step 1.0a and is added as one extra template then |
| `orchestration worker-show --dispatch <dispatch> --json` | Per-row detail, bounded at 50 (GQ-01) |
| `orchestration task-list --ready --run <run> --json` | Foreign ready Task, rule 4 (b) (`WORKER-CONTRACT.md:129`) |
| `orchestration task-list --run <run> --json` | Task spec text for the gate policy line (GQ-103(3)) |
| `worktree ps --json` | Worktree discovery and `agentWait` (no `--agent-wait` filter) |

Removed from the research allowlist by GQ-109: `gate-list`, `worker-read` (it consumes messages), and any `git stash` form. `run-list` is removed by GQ-104. `--include-remote` and `gh` are Phase 2 or later. Whether every template above takes `--json` exactly as written is UNVERIFIED and is the first thing the step 1.0a capture checks; a template that fails the capture is dropped, and its rows print could not determine.

**Git allowlist** (subcommand part only; the seam adds the prefix):

| Template | Purpose |
|---|---|
| `status --porcelain --branch` | One call per worktree answers uncommitted, untracked, ahead/no-upstream, `.dev/tasks/` unsaved and active-package paths (GQ-110, GQ-101) |
| `rev-parse --show-toplevel` | Default `--root` only, once per sweep |

No `git log`, `git branch`, `git stash list` or `git worktree list`. Unmerged commits and open PRs are not observed in Phase 1; that is acceptable because worktree removable is never `yes` (FR-012).

**Disk reads** (no seam needed, `os.stat` and open-for-read only): package `progress.md` and `.archiving` markers under `<worktree>/.dev/tasks/{to-do,done}/`, worker contract records named by the Orca row, transcripts under the scanned project keys, and the ccsession tab map. Each reader records a `SourceCoverage` row and never raises past `collect`.

## 8. Report format

The layout copies the sections this research chose from #409 at `495eb96d` (header, Attention Ledger, Shift Brief; REPORT line 328) into the design, citing the commit, because #409 is unmerged. The renderer is one pure function per section, called in a fixed order from a tuple `SECTIONS`, so a later phase adds a section by appending one function (the same table pattern as `RULES`).

**File:** `<output>/<YYYYMMDD-HHMMSS>-sweep.md`, UTC timestamp from `SweepContext.now`.

**Header block:**

```text
READ ONLY . observed <UTC ISO time>
Scope: Runs <ids> . worktrees <n> . sessions <shown>/<total> . window <6h>
Sources: <name> <coverage> (age <s>s) . ...   [one entry per SourceCoverage]
Messages coverage: partial
```

"Messages coverage: partial" is fixed text in Phase 1, because there is no non-consuming read of pending questions (GQ-02).

**Sections, in order:**

1. `## Waiting on a person (a)`: table `| ID | Age | Question | Requested by | Decision owner | Affected | Evidence |`, oldest first, then "unknown age". Under it: "Seen is not resolved" and "Answered: could not determine".
2. `## Waiting on a person (b)`: blocked by policy (frozen plan, foreign ready Task); no question text, the policy reason and evidence only.
3. `## Retained problems`: interrupted archives, conflict packages, shared active packages, WC-13 violations, call bound reached.
4. `## Sessions (<shown>/<total>)`: one row per session with the ten #409 dimensions, class, rule name, safe-to-close (terminal, worktree) and notes.
5. `## Worktrees`: path, uncommitted, unpushed, `.dev/tasks/` unsaved, Package state column, removable with reason.
6. `## Historical sessions`: person-started sessions with no activity inside the window (GQ-108).

**Fixed strings:** an empty section prints "No matching records. This is not an all-clear."; any count over sessions prints "Distinct affected sessions: <N> (set union, not a sum)". The footer is "Inspection only." followed by the source list. The report holds no action controls, commands to paste, or advice to delete anything under `.dev/tasks/` (seed brief constraint).

**Stdout JSON (schema v1):** `schema_version`, `observed_at`, `scope`, `window`, `orca_available`, `sources`, `rows`, `waiting` (`a`, `b`), `summary` (count per class, `bound_reached`, `total`), `report_path`. Each row carries `class` and `rule`. Every key is always present (null or empty when unknown). The skill reads only `report_path` and `summary`; Phases 2, 5 and 6 read `rows`.

## 9. WC-14 contract rule text (proposal)

Placement: a new subsection after the fan-in rule at `WORKER-CONTRACT.md:156` and before `### Worked example` at `:158`. WC-14 is the next free ID (REPORT line 70). This text adapts the REPORT step 1.17 draft (G1 to G7) and is a proposal for GQ-04; the owner's GQ-11 answer is a hard gate before steps 1.17 to 1.19 are written.

> **WC-14. Coordinator loop.** The coordinator keeps watching its Run until every Task it created has settled and been admitted; it never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake, the coordinator runs `/sc:sweep` and reads its report before it acts. The sweep's classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine. The coordinator escalates to the person, and does not act alone, on: a failed or blocked result it cannot retry under WC-6, a partial result it judges unusable, a third brief-guard refusal, a foreign ready Task, a frozen plan, and a fan-in with fewer than 2 admitted inputs. Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged. The sweep report is a dated local file; it is never posted. The sweep recommends none of these actions; the coordinator decides and performs them under those rules.

Choices in this text:

- The closing sentence takes the "recommends none" alternative (open owner decision 98b). It keeps the read/write split of section 5 in the contract itself: the classifier never becomes an actor, so Phase 2 cannot grow a "recommended action" column that a worker would read as an instruction.
- "On every coordinator wake" ties the sweep to events the contract already has, not to a timer. A scheduled sweep (the owner memory mentions a cron sweep) is allowed by this text but not required; see section 13.
- `/sc:sweep` joins the never-as-worker list (9 entries); the sweep stays out of `UNATTENDED_COMMANDS`.

**Pins** (`tests/skills/test_worker_contract.py`): `RULE_PHRASES["WC-14"] = ("WC-14", ["WC-14. Coordinator loop", "On every coordinator wake", "it is never posted"])`; `NEVER_AS_WORKER` grows to 9; rename `test_never_as_worker_list_names_all_seven_commands` to `test_never_as_worker_list_names_every_listed_command` so the next addition does not need a rename. Sequencing: PR #422 lands, or this branch rebases on it, before the contract edit (step 1.16a).

## 10. Failure modes

Each mode has a fixture in `tests/sweep/`. "CND" means could not determine.

| Mode | Detection | Behaviour | Exit |
|---|---|---|---|
| Orca absent or `runtime_unavailable` | First `_orca` raises or returns that code | Banner, no more `_orca`, disk-only discovery, Orca sources unscanned (FR-019) | 0 |
| No Run bound | `run-current` empty and no `--run` | Usage message (FR-002) | 2 |
| Worktree removed mid-sweep | `_git` raises `CalledProcessError` or path gone at `os.stat` | That worktree row CND, `unscanned: worktree not readable`; others continue | 0 |
| Live worker holds `index.lock` | Not detected; avoided | `--no-optional-locks` means the sweep never takes it (NFR-002) | 0 |
| Unreadable transcript or contract | `OSError` on open | `transcript_readable False`; rules 2 and 1 decline; row CND with note | 0 |
| Stale list data | `liveStatus` stale, or a row in the list missing from `worker-show` | CND (WC-10); never stalled | 0 |
| Slow worker | Late heartbeat only | CND, never stalled (WC-10, `WORKER-CONTRACT.md:45`) | 0 |
| Call bound or time budget reached | `Budget` exhausted | Remaining rows CND, `unscanned: call bound reached` (FR-020) | 0 |
| Unknown row schema field | Key missing in JSON | Field stays `unknown`; no exception | 0 |
| Allowlist miss | `ValueError` from the seam | `[sweep ...]` stderr, no report written | 1 |
| Output dir not writable | `OSError` in `write_report` | `[sweep ...]` stderr; JSON not printed | 1 |
| Malicious text in a field | Control or pipe characters | `sanitize()` (FR-016) | 0 |

## 11. Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| R1. The real `worker-list` and `worker-show` schema differs from the fixtures (GQ-01) | High | Step 1.0a capture before step 1.2; models keep every field optional; unknown stays unknown; fixtures regenerated from the capture |
| R2. "Waiting on a person" missed because questions cannot be read without consuming them (GQ-02) | High | `blocked_question` plus non-null `agentWait` as stand-ins; fixed "Messages coverage: partial" header so the gap is visible |
| R3. A sweep disturbs a live worker | Low after NFR-002 | Seam-built `--no-optional-locks`, exact allowlist, forbidden-verb test, snapshot-diff test |
| R4. Rule precedence drifts as later phases add rules | Medium | Named `RULES` tuple pinned by NFR-010; each rule has its own test; insertion position must be justified in the PR |
| R5. Phase 2 reuses the read seam to write | Medium | B3 plus FR-021: write verbs live in another package with its own seam; static test on `ALLOWED_ORCA` |
| R6. Consumers break on JSON changes | Medium | `schema_version` and the golden key-set test (NFR-009) |
| R7. The coordinator reads "finished" as "safe to delete" | Medium | Safe-to-close is a separate field; worktree never `yes`; no deletion advice for `.dev/tasks/` |
| R8. Contract wording conflicts with PR #422 | Medium | Step 1.16a sequencing; new-file PR first if needed (section 13) |
| R9. Six modules grow into one large classifier file | Medium | One function per rule and per report section; the dependency test (B1) keeps them apart |

## 12. Resolution of GQ-101 to GQ-110, handling of GQ-111 to GQ-113

Source: GAPS lines 124-136. GQ-103(1) is built first, before any other probe code.

| GQ | Resolution in this spec | Where |
|---|---|---|
| GQ-103(1) | Every `_git` argv built by the seam as `git --no-optional-locks -C <path>`, plus `GIT_OPTIONAL_LOCKS=0`; first commit and first test | NFR-002, section 7 |
| GQ-101 | Count only packages active in a worktree (changed or untracked path inside the package folder, from the one status call); committed unchanged folders shared by every worktree are never flagged | FR-015, section 6 |
| GQ-102 | `conflict` is a package state (id in both `to-do/` and `done/`); it blocks removal and lists under Retained problems | FR-014, section 6 |
| GQ-103(2) | `SweepContext` with the window is a parameter of `classify_all` | FR-007 |
| GQ-103(3) | New fields: `gate_policy` (from the Task spec), `worker_done_seen`, `transcript_readable`, `ContractRecord.report_path` and `artifacts` | section 6 |
| GQ-104 | No `run-list` fallback; no binding and no `--run` exits 2 | FR-002 |
| GQ-105 | `archive-blocked` = package in `to-do/` whose `progress.md` has a `FINAL:` line | FR-014 |
| GQ-106 | `.dev/sweeps/` in `.gitignore` and in the rollback table | FR-025, section 14 |
| GQ-107 | `sanitize()` escapes the pipe character | FR-016 |
| GQ-108 | Person-started = transcript joined to no Orca row; outside the window goes to Historical | FR-010 |
| GQ-109 | `gate-list`, `worker-read` and stash removed from the allowlist | section 7, NFR-003 |
| GQ-110 | One `git status --porcelain --branch` per worktree; a recorded-argv test counts them | section 7 |

GQ-111 to GQ-113 are stale citations inside the REPORT. They are carried, not fixed: the design does not edit the REPORT. Where the design needs a count it cites GAPS line 138 (113 rows, 88 open, 25 resolved), and it reads REPORT line 1537 ("Every open GQ row is cited") as covering GQ-01 to GQ-100 only.

## 13. Open questions with recommended answers

| Question | Recommended answer | Why (architecture view) |
|---|---|---|
| GQ-01: design for list plus `worker-show`, or capture the row schema first? | Both: design the models for list plus `worker-show` now, and run the step 1.0a capture before step 1.2 fixes fixtures | Optional fields cost nothing; the capture then only removes calls, it never changes a class rule |
| GQ-02: what stands in for a non-consuming question read? | `blocked_question` from the contract plus non-null `agentWait`; header says "Messages coverage: partial" | No consuming verb ever enters the allowlist; the gap is shown, not hidden |
| GQ-04: WC-14 wording | The section 9 text | Short, testable phrases for the pins |
| #409 layout: copy or cite? | Copy the chosen sections into the design and cite `495eb96d` | An unmerged commit is not a stable dependency |
| 6 h or 72 h window? | 6 h default, `--window` override; older person sessions go to Historical | Matches the issue; 72 h belongs to `sc-crash-recovery`, a different job |
| PR #422 sequencing | New files first (package, tests, command, skill, `.gitignore`); contract and registry edits after #422 lands | New files cannot conflict; the contract edit is the only shared surface |
| Sweep cadence: wake only, or also scheduled? | WC-14 requires a sweep on every wake; a cron sweep stays an operator choice outside the contract | The contract stays event-driven; a timer adds no new rule |
| Closing sentence of WC-14 (decision 98b) | "The sweep recommends none of these actions" | Keeps the read/write split in the contract |
| Package name `sc-sweep-protocol` with `name: sc:sweep-protocol` | Keep | Matches existing skill folders such as `sc-implement-protocol` (cited in `synthesis/phase7-summary.md`) |

## 14. Rollback

Phase 1 is additive, and its only runtime write is the report file, so rollback is one revert of the branch's commits as one unit (REPORT lines 1304-1320). No data migration.

| Item | Rollback |
|---|---|
| `src/superclaude/cli/sweep/` and `tests/sweep/` | Delete |
| `cli/main.py` deferred import and `add_command` lines | Remove |
| `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/`, `tests/commands/test_sweep_command.py` | Delete; run `make sync-dev` (whether it removes the `.claude/` copies is UNVERIFIED; check and delete them by hand if not, never stage them) |
| WC-14 in `WORKER-CONTRACT.md`, never-as-worker entry, `RULE_PHRASES`, `NEVER_AS_WORKER`, the test rename | Revert |
| `_POST_REFRESH_ADDITIONS` (`tests/recommend/test_routing_refresh.py:33`), `HOW-WE-WORK.md` "Other commands" row and "Orca coordination" bullet, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `_OTHER_COMMANDS` (`tests/core/test_how_we_work_routing_table.py`) | Revert together, so the byte copy stays equal |
| `docs/user-guide/commands.md`, developer guide never-as-worker copy, CHANGELOG | Revert; add a CHANGELOG revert entry |
| `.gitignore` `.dev/sweeps/` line | Keep until existing reports are dealt with, then remove (GQ-106) |
| Reports already written under `.dev/sweeps/` | Stay; they are ignored local files and the owner decides |

Rollback check: `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_worker_contract.py tests/recommend tests/core tests/commands` pass on the reverted tree.
