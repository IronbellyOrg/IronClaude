# Research: File Inventory

**Topic type:** File Inventory
**Scope:** `docs/designs/orchestrator-mode.md` sections 7, 9, 10, 15 and the repo files they name (new files to create, existing files to modify, line-anchor checks)
**Status:** Complete
**Date:** 2026-11-08

---

## A. Design sections read

| Section | Lines in `docs/designs/orchestrator-mode.md` |
|---|---|
| 7 Interfaces (7.1 signatures, 7.2 data model, 7.3 allowlist, 7.4 JSON v1, 7.5 report layout, 7.6 command/skill) | 351-657 |
| 8 WC-14 and never-as-worker (pins for `test_worker_contract.py`) | 659-686 |
| 9 Routing rows R1-R8 | 688-708 |
| 10 `.gitignore` | 710-722 |
| 11 Test plan per file | 724-747 |
| 15.1 Step 1.0a capture items | 866-898 |
| 15.2 Step table | 900-942 |
| 16 Rollback | 944-961 |
| 17 Open items (23) | 963-993 |

Existence check (Glob + `ls`, 2026-11-08): `src/superclaude/cli/sweep/`, `tests/sweep/`, `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/`, `tests/commands/test_sweep_command.py` do NOT exist. All are true new files.

---

## B. NEW files (create)

Step IDs and gates from design 15.2 (lines 904-940). "Gate" = the step that must be done first (design column "Gate before the step").

### B1. `src/superclaude/cli/sweep/__init__.py` — step 1.1, gate: none

- Purpose: package entry; exposes `sweep_group` lazily so importing the package starts no seam and does not import `commands` (design 7.1 lines 357-361; test in 11 line 741).
- Interface (design line 360):
  ```
  def __getattr__(name: str) -> object        # "sweep_group" only; imports commands lazily
  ```

### B2. `src/superclaude/cli/sweep/models.py` — step 1.2, gate: none

- Purpose: all frozen dataclasses and string constants (design 7.2 line 449).
- Dataclasses (design 7.2 table, lines 451-466): `SweepContext` (`now`, `window`, `window_start = now - window`, `root`, `runs`); `SweepInput` (`orca_rows: tuple[OrcaObservation, ...]`, `contracts`, `transcripts: tuple[TranscriptTail, ...]`, `tab_map: tuple[TabMapEntry, ...]`, `worktrees: tuple[WorktreeState, ...]`, `sources: tuple[SourceCoverage, ...]`, `orca_available: bool`, `orca_binary: str`, `orca_version: str | None`, `truncated: bool`, `collected_start`, `collected_end`); `OrcaObservation` (SPEC line 231 list plus `dispatch: str`, `run: str`, `session_join: str | None`); `ContractRecord` (`path`, `worker_status`, `blocked_question`, `reason`, `report_path`, `artifacts`, `command`); `TranscriptTail` (`path`, `session_id: str | None`, `readable: bool`, `last_record_ts: datetime | None`, `mtime: datetime`, `project_key: str`); `TabMapEntry` (`file_name`, `session_id`, `launch_dir`, `terminal_handle`); `SessionRow` (`id`, `person_started`, `orca`, `contract`, `transcript_path`, `transcript_readable`, `last_activity`, `gate_policy`, `row_id`, the ten #409 dimensions); `StatusParse` (`entries: tuple[tuple[str, str], ...]`, `branch_header: str`, `ahead: int | None`, `has_upstream: bool | None`, `header_note: str | None`); `PackageRecord` (`id`, `location`, `has_final_line`, `archiving_marker`, `active`, `state`); `WorktreeState` (`path`, `status_read`, `uncommitted`, `unpushed: bool | None`, `dev_tasks_unsaved`, `changed_paths`, `packages`, `shared_package_ids`, `frozen`, `upstream_note: str | None`); `Classification` (`class_name` [JSON key `class`], `waiting_kind`, `rule`, `evidence`, `notes`); `SafeToClose` (`terminal`, `worktree`, `reason`); `SourceCoverage` (`name`, `coverage`, `age_seconds`, `unscanned`); `SweepResult` (`rows: tuple[ClassifiedRow, ...]`, `worktrees`, `waiting_a`, `waiting_b`, `summary` [counts per class with zeros, `bound_reached`, `visible`, `historical`, `total`, `total_is_lower_bound`], carried header data).
- Gap: `ClassifiedRow` is named in `SweepResult.rows` (line 466: "row plus `Classification`, policy and `SafeToClose`") but has no row of its own in the 7.2 table. Builder must define it in `models.py`; its field names are Unverified (not in design).
- Gap: the "ten #409 dimensions" of `SessionRow` and the `OrcaObservation` SPEC field list (SPEC line 231) are not copied into the design; they come from the SPEC (Unverified here; researcher 3/4 scope).
- Constants (design line 468): `JSON_SCHEMA_VERSION = 1`; `CLASSES` = (`waiting on a person`, `stalled (proved)`, `fenced`, `working`, `finished`, `idle`, `person session (active)`, `could not determine`); `PACKAGE_STATES` in precedence order (`conflict`, `interrupted-archive`, `archive-blocked`, `unfinished`, `archived`, `unknown`); `SAFE_VALUES` (`yes`, `no`, `could not determine`).

### B3. `src/superclaude/cli/sweep/classify.py` — step 1.3, gate: 1.2 (and open item 22: "the classify step does not start until the owner signs off D9", design line 990)

- Purpose: pure classification; imports none of `subprocess`, `click`, `os`, `shutil` (AST test, design line 739).
- Interfaces (design lines 405-419):
  ```
  @dataclass(frozen=True)
  class Rule:
      name: str
      match: Callable[[SessionRow, SweepContext], Classification | None]

  RULES: tuple[Rule, ...]                      # 9 rules, order in section 7.2
  def classify(row: SessionRow, ctx: SweepContext) -> Classification
  def policy_of(row: SessionRow) -> str | None # "frozen" or None, independent of class (GQ-96)
  def package_state(pkg: PackageRecord) -> str
  def mark_shared_packages(worktrees: tuple[WorktreeState, ...]) -> tuple[WorktreeState, ...]
  def safe_to_close(row: SessionRow, worktree: WorktreeState | None) -> SafeToClose
  def removable(worktree: WorktreeState) -> tuple[str, str]  # ("no", "<first FR-013 condition>") or ("could not determine", reason)
  def classify_all(inp: SweepInput, ctx: SweepContext) -> SweepResult
  ```
- Rule order (design lines 472-482): 1 `blocked_contract`, 2 `orca_exit_proof`, 3 `fenced`, 4 `waiting_signal`, 5 `working`, 6 `finished`, 7 `idle`, 8 `person_active`, 9 `fallback`.
- Fixed readings: rule 1 notes M6 (line 486), rule 5 four conditions SP-24 (line 487), future timestamp SP-26 (line 488); joins path A/B (lines 490-498); observation rules (lines 500-512).

### B4. `src/superclaude/cli/sweep/probes.py` — split across steps 1.4a and 1.4

- **Step 1.4a** (gate 1.2; "The first code commit", design line 911): `_git`, `GitCallFailed`, `ALLOWED_GIT`, `check_git_args`, plus `tests/sweep/test_readonly.py` (B9) and the `.gitignore` lines (C10).
- **Step 1.4** (gates 1.0a for parsers/regexes, and 1.4a; design line 912): `_orca`, `ALLOWED_ORCA`, `Budget`, `OrcaResult`, `bind_run`, `collect`, readers. Live check saved to `.dev/tasks/<pkg>/artifacts/sweep-live-check-1.4.json`; no `--include-remote` timing. Open item 2 (line 970): 1.4 and 1.6 do not start until `RUN_ID_RE`/`DISPATCH_ID_RE` are known from 1.0a item 10.
- Purpose: read side; the only module that starts a subprocess (line 363).
- Interfaces (design lines 365-401):
  ```
  class Budget:
      def __init__(self, shows: int = 50, total_s: float = 90.0, per_call_s: float = 10.0,
                   clock: Callable[[], float] = time.monotonic) -> None
      def share_shows(self, runs: tuple[str, ...]) -> None     # even split, remainder to the first Run
      def take_show(self, run: str) -> bool                    # False: "show cap reached (50)"
      def call_timeout(self) -> float | None                   # min(10, remaining); None below 1 s left
      def cut(self) -> bool                                    # last timeout was cut below 10 s

  @dataclass(frozen=True)
  class OrcaResult:
      kind: str            # "ok" | "no_binding" | "unavailable" | "call_failed"
      data: object | None  # parsed JSON for "ok"
      reason: str | None   # e.g. "binary not found: orca-ide", "unscanned: time budget reached (90 s)"

  class BindingError(Exception)               # carries the exit-2 message; commands maps it to exit 2

  def orca_binary() -> str                                     # $ORCA_CLI_COMMAND, else "orca-ide"
  def check_orca_argv(args: tuple[str, ...]) -> None           # ValueError unless an exact template match
  def check_git_args(args: tuple[str, ...]) -> None            # ValueError unless == ALLOWED_GIT[0]
  def _orca(*args: str, timeout: float) -> OrcaResult
  def _git(cwd: Path, *args: str, timeout: float) -> str       # raises GitCallFailed on nonzero, timeout, > 8 MiB
  class GitCallFailed(Exception)

  def bind_run(budget: Budget) -> str                          # run-current; BindingError on unavailable or no_binding
  def collect(ctx: SweepContext, runs: tuple[str, ...], root: Path, budget: Budget) -> SweepInput

  def read_worktree(path: Path, budget: Budget) -> tuple[WorktreeState, SourceCoverage]
  def parse_status(raw: str) -> StatusParse                    # NUL fields, rename pairs, branch header (M7)
  def read_packages(worktree: Path) -> tuple[PackageRecord, ...]
  def read_ledger(path: Path) -> bool | None                   # has a FINAL: line; head 512 KiB + tail 512 KiB over 1 MiB
  def read_contract(path: Path) -> ContractRecord | None       # None plus "over 1 MiB" coverage when too large
  def read_transcript_tail(path: Path) -> TranscriptTail       # last 256 KiB, first partial line dropped
  def read_tab_map(state_dir: Path) -> tuple[TabMapEntry, ...]
  def read_orca_version(path: Path = ORCA_VERSION_FILE) -> str | None
  ```
- Constants (design 7.3 lines 518-543):
  ```
  ORCA_BINARY_DEFAULT = "orca-ide"
  ALLOWED_ORCA: tuple[tuple[str, ...], ...] = (
      ("orchestration", "run-current"),
      ("orchestration", "worker-list", "--run", "<run>", "--json"),
      ("orchestration", "worker-show", "--dispatch", "<dispatch>", "--json"),
      ("orchestration", "task-list", "--ready", "--run", "<run>", "--json"),
      ("orchestration", "task-list", "--run", "<run>", "--json"),
      ("worktree", "ps", "--json"),
      ("worktree", "list", "--json"),          # pinned, not called in Phase 1
      ("worktree", "current", "--json"),       # pinned, not called in Phase 1
  )                                            # 8 templates, 7 verbs (NFR-014)
  FORBIDDEN_TOKENS = frozenset({"--include-remote", "--agent-wait"})
  ALLOWED_GIT: tuple[tuple[str, ...], ...] = (
      ("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all"),
  )                                            # the seam prepends git --no-optional-locks -C <path>
  ORCA_VERSION_FILE = Path("/opt/Orca/resources/app.asar.unpacked/out/package.json")
  OUTPUT_LIMIT = 8 * 1024 * 1024
  CONTRACT_LIMIT = LEDGER_LIMIT = 1024 * 1024  # hit when size > limit
  LEDGER_SPLIT = 512 * 1024
  TRANSCRIPT_TAIL = 256 * 1024
  WORKER_LIST_PAGE = 100
  ```
  Plus `RUN_ID_RE`, `DISPATCH_ID_RE` (values from step 1.0a item 10; UNVERIFIED today, design line 516, open item 2).
- Constraints: FR-021 forbidden verb list lives in the test, not in `probes.py` (line 546). Child env holds `GIT_OPTIONAL_LOCKS=0` (line 737). Byte limits marked "proposed" in `probes.py` (open item 19, line 987). No `worker-list` cursor template until 1.0a item 3 captures it (line 552).

### B5. `src/superclaude/cli/sweep/report.py` — step 1.5, gate: 1.3

- Purpose: pure rendering of Markdown report and JSON v1; no `write_report` (design line 913).
- Interfaces (design lines 423-431):
  ```
  CHECKED_ORCA_VERSION: str = "1.4.245"
  CELL_MAX: int = 200                          # SP-23 (D4)
  SECTIONS: tuple[Callable[[SweepResult, SweepContext], str], ...]   # order of section 7.5
  def sanitize(text: str) -> str
  def cell(text: str) -> str                   # sanitize, then cut to CELL_MAX ending "..."
  def render(result: SweepResult, ctx: SweepContext) -> str
  def to_json(result: SweepResult, ctx: SweepContext, report_path: str) -> dict[str, object]
  ```
- `SECTIONS` = 12 functions in order: header, source coverage, waiting a, waiting b, could not determine, retained problems, sessions, worktrees, historical, shift brief, what I could not determine, footer (line 632). `render` output ends `Report complete\n` (line 594).
- Holds the fixed `next inspection` map keyed by rule name (line 634).
- JSON v1 key set: design 7.4 lines 558-590. Layout literal: design 7.5 lines 596-628.

### B6. `src/superclaude/cli/sweep/commands.py` — step 1.6, gate: 1.4, 1.5

- Purpose: impure click shell; only module that calls `sys.exit` or raises click exit types (line 445). No `run-list` fallback; `--output` default `<root>/.dev/sweeps/` (line 914).
- Interfaces (design lines 435-443):
  ```
  sweep_group: click.Group                     # "sweep"
  def run(run_ids: tuple[str, ...], window: str, root: str | None, output: str | None) -> None   # "sweep run"
  def _parse_window(text: str) -> timedelta    # FR-003; click.UsageError -> exit 2
  def _find_root(start: Path) -> Path          # FR-004 walk, plain stat only
  def _check_output(output: Path | None, root: Path, inputs: tuple[Path, ...]) -> Path   # FR-004 containment
  def _check_run_ids(values: tuple[str, ...]) -> tuple[str, ...]   # regex from step 1.0a, deduplicated
  def _publish(text: str, output_dir: Path, now: datetime) -> Path  # section 3.2, the one write
  ```
- Exit mapping (line 445): `click.UsageError` and `BindingError` -> exit 2 with message; `ValueError` from allowlist, any other exception, every `_publish` failure -> exit 1 with `[sweep <stage>]` stderr prefix (FR-018).
- `_publish` mechanism is design section 3.2 (lines 99-130; not read here, researcher 4 / R3 scope). CLI options per `sweep.md` argument-hint: `--run <id>` (repeatable), `--window <N>h|<N>d`, `--root <dir>`, `--output <dir>` (line 646).

### B7. `src/superclaude/commands/sweep.md` — step 1.14, gate: 1.7

- Installs to `~/.claude/commands/sc/sweep.md` (line 644).
- Frontmatter (line 646): `name: sweep`, one-line description, `allowed-tools: Skill`, `argument-hint: [--run <id>]... [--window <N>h|<N>d] [--root <dir>] [--output <dir>]`.
- Body (line 647): headings follow `issue.md` (title, Triggers, Usage, Options) plus `## Activation` in the `graph.md` form. Activation invokes `~/.claude/skills/sc-sweep-protocol/SKILL.md` and names project `.claude/skills/sc-sweep-protocol/SKILL.md` as the dual surface.
- Triggers explicit only; no `## Unattended mode`; no `--unattended` (line 648). No `src/superclaude/` substring (line 642, NFR-011).
- Anchor check of cited `graph.md`: line 9 = `allowed-tools: Skill, Bash(codegraph init --yes *), Bash(codegraph init -i)` CONFIRMED; line 41 = `## Activation` CONFIRMED (`src/superclaude/commands/graph.md:9`, `:41`).

### B8. `src/superclaude/skills/sc-sweep-protocol/SKILL.md` — step 1.15, gate: 1.14

- Frontmatter (line 652): `allowed-tools: Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read`.
- Steps (line 653): (1) `superclaude sweep run <args>`, Bash timeout 120000 ms; (2) only on "command not found", `uv run --frozen --no-sync superclaude sweep run <args>`, same timeout; (3) exit 0: parse stdout JSON, take `report_path` and `summary` only, Read the report; (4) print counts and report path; (5) exit 1 or 2: print stderr line and stop.
- Recommends nothing; never edits, stages or deletes a file (line 654). No `src/superclaude/` substring.

### B9. `tests/sweep/test_readonly.py` — created step 1.4a (gate 1.2), extended step 1.11 (gate 1.6)

- 1.4a part (line 737): every recorded `_git` argv has `--no-optional-locks` at index 1 and `-C <path>` after it; child env `GIT_OPTIONAL_LOCKS=0`; one git argv per discovered worktree; one `integration`-marked real-git test in `tmp_path` copying the repo `.gitignore`: control, `git check-ignore .dev/sweeps/x.md` succeeds, `.dev/tasks/to-do/x.md` fails, a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged.
- 1.11 part: snapshot diff (path, size, `st_mtime_ns`, SHA-256) over root, `HOME`, XDG dirs; exactly one added report file (+ output dir when new); no temp file / second name after exit 0 (NFR-001, NFR-013).
- Gap: 1.4a creates this test before `conftest.py` (step 1.8). "one git argv per discovered worktree" also needs worktree discovery, which is `collect` in step 1.4. The design does not say how 1.4a provides the fakes or discovery. Builder must choose (Unverified; flag).

### B10. `tests/sweep/conftest.py` + `tests/sweep/fixtures/` — step 1.8, gate: 1.0a for captured fixtures

- Lines 728-733: `patch_orca`, `patch_git` fakes recording argv (pattern from `tests/cli/reflect/conftest.py`); autouse fixture patching `subprocess.run`, `subprocess.Popen`, `os.system` to raise `AssertionError`, stepping aside only for the `integration` marker; fixed `now`; `tmp_path` layout with `HOME` and `XDG_STATE_HOME` inside it (packages, contracts, transcripts, ccsession `orca-tabs/`). Captured fixtures keep source name; hand-made ones carry `synthetic` in name (line 733).

### B11. `tests/sweep/test_classify.py` — step 1.9, gate: 1.3. Cases: design 11 line 739.

### B12. `tests/sweep/test_probes_allowlist.py` — step 1.10, gate: 1.4. Cases: design 11 line 738 (exact-set pin of 8 templates, negatives, FR-021 list held in the test, budget, byte boundaries, failure modes, `parse_status` M7 cases).

### B13. `tests/sweep/test_report.py` — step 1.12, gate: 1.5. Cases: design 11 line 740.

### B14. `tests/sweep/test_cli_registration.py` — step 1.13, gate: 1.7. Cases (line 741): `superclaude sweep --help` and `sweep run --help` exit 0 under `CliRunner`; importing `superclaude.cli.sweep` records no seam call and does not import `commands` until `sweep_group` is read.

### B15. `tests/sweep/test_cli_contract.py` — step 1.13, gate: 1.7. Cases: design 11 line 742.

### B16. `tests/commands/test_sweep_command.py` — step 1.16, gate: 1.15. Asserts (line 657): both `allowed-tools` literals exactly; installed skill path and dual-surface path in Activation; PATH-first order and "command not found" trigger; `--no-sync` in fallback; timeout 120000; no `## Unattended mode`; no `src/superclaude/` in either file; no stop/retry/release/merge/removal advice in skill.

Count check: 7 new `tests/sweep/*.py` files (`conftest.py`, `test_readonly.py`, `test_probes_allowlist.py`, `test_classify.py`, `test_report.py`, `test_cli_registration.py`, `test_cli_contract.py`), matching design line 726 "Seven new files under `tests/sweep/`". Plus `tests/sweep/fixtures/` (data). Design 11 lists no `tests/sweep/__init__.py`; whether one is needed is a test-convention question (researcher 5 scope).

Non-source step artifacts also created: `.dev/tasks/<pkg>/artifacts/readonly-probe.md` (1.0a, line 876), `owner-decisions.md` (1.0b, line 907), `sweep-live-check-1.4.json` (1.4, line 912), PR #422 results (1.16a, line 925), `sweep-help-pipx.txt` (1.29, line 940).

---

## C. EXISTING files (modify) — anchor checks

All files exist. Every anchor was Read on 2026-11-08 at the current worktree HEAD.

### C1. `src/superclaude/cli/main.py` — step 1.7, gate 1.6 — anchor CONFIRMED

- Design: register `sweep_group` with the deferred-import pattern "after line 561" (design line 915; rollback line 951).
- Actual: `main.py:559` `from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports`; `main.py:561` `main.add_command(reflect_group, name="reflect")`; `main.py:564` `if __name__ == "__main__":`. File is 565 lines.
- Edit: insert after line 561, before the blank lines at 562-563, the pair:
  ```python
  from superclaude.cli.sweep import sweep_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports

  main.add_command(sweep_group, name="sweep")
  ```
  (Pattern copied from `main.py:547-549` `swarm_group` and `:551-553` `recommend_group`, which import from the package `__init__`. `from superclaude.cli.sweep import sweep_group` resolves through B1's `__getattr__`.)

### C2. `src/superclaude/core/WORKER-CONTRACT.md` — steps 1.17 (gate 1.0b GQ-11, 1.16a) and 1.18 (gate 1.17)

- Line 23 — CONFIRMED. `WORKER-CONTRACT.md:23` is the `- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while ...` term line. Step 1.18 replaces it with design line 684 text (inserts `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`; rest unchanged). Must stay one line (`_check_never_as_worker`, C11).
- Line 156 (fan-in paragraph) — CONFIRMED (`WORKER-CONTRACT.md:156` starts "For N input Tasks feeding one merge Task"). Line 158 `### Worked example: gate hit, answer, new Task` — CONFIRMED. Step 1.17 inserts the `### WC-14. Coordinator loop` block (design lines 668-670) between them, i.e. after line 156 / before line 158. Note: line 154 is `### Fan-in rule (several workers, then one merge)`.
- File is 203 lines.

### C3. `src/superclaude/core/HOW-WE-WORK.md` — step 1.21 (R1, R2), gate 1.14

- Lines 318-337 — CONFIRMED. `HOW-WE-WORK.md:318` `<!-- other-commands:v1 -->`, `:320-321` table header, `:337` `<!-- /other-commands -->`.
- Line 333 — CONFIRMED. `HOW-WE-WORK.md:333` is the `/sc:spawn` row. R1 row goes after it, i.e. new line 334, before the blank line and the "One more user-facing skill" paragraph at `:335`. Row text: design line 694.
- Line 396 — CONFIRMED. `HOW-WE-WORK.md:396` `## Orca coordination`.
- Line 403 — CONFIRMED. `HOW-WE-WORK.md:403` `- **Some commands are never workers.** ...`. R2 bullet goes after it, before `:404` `- **Orca creates the worktrees.** ...`. Bullet text: design line 695.
- Note: after R1 lands (+1 line), the R2 anchor shifts to 404; apply R2 first or anchor on content.
- Level table is not touched (design line 706), so no `core/CLAUDE.md` level-table re-copy.

### C4. `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` — step 1.23 (R3), same commit as 1.21

- Exists. `cmp` against `src/superclaude/core/HOW-WE-WORK.md` today: IDENTICAL.
- Edit: byte copy of C3 after R1+R2 (`cp`).
- Checked by `tests/commands/test_routing_plugin_parity.py:38` `assert filecmp.cmp(_GUIDE, _PLUG_SKILL / "refs/HOW-WE-WORK.md", shallow=False)` — CONFIRMED. That test file is unchanged.

### C5. `tests/core/test_how_we_work_routing_table.py` — step 1.22 (R4), gate 1.21 — anchor CONFIRMED

- `test_how_we_work_routing_table.py:27` `_OTHER_COMMANDS = {` (set spans lines 27-40, entries `sc:build` ... `sc:load`, closing `}` at `:40`). Edit: add `"sc:sweep",` inside the set.
- `:24` holds the `<!-- other-commands:v1 -->` markers the test reads.

### C6. `tests/recommend/test_routing_refresh.py` — step 1.20 (R5), gate 1.14 — anchors CONFIRMED

- `test_routing_refresh.py:33` `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}`. Edit: `{"graph", "impact", "issue", "sweep"}`.
- `:648` `assert shipped - _POST_REFRESH_ADDITIONS == active` — CONFIRMED (shipped = every `src/superclaude/commands/*.md` stem except README, `:647`). This is why 1.20 is gated on 1.14 (`sweep.md` existing).
- Optional: comment at `:29-32` lists why each addition exists; a matching comment line for `sweep` (issue #339) keeps it accurate. Not required by the design.

### C7. `docs/user-guide/commands.md` — step 1.24 (R6), gate 1.14 — anchors CONFIRMED

- `commands.md:105` `### 8. UTILITIES`; `:107-108` table header `| Command | Purpose | File | Changes files? |`.
- `commands.md:115` `/sc:issue` row. R6 row goes after it (before `:116` `/sc:recommend`). Row cells per design line 699: `` `/sc:sweep` `` | Read-only snapshot of a Run, its worktrees and person sessions | `sweep.md` | Report only (writes `.dev/sweeps/`).

### C8. `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` — step 1.24a (R7), gate 1.18 — anchor CONFIRMED

- `...Commands-Skills-Agents.md:991` `- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers. ...`
- Edit: insert `/sc:sweep` in the same order as C2 (`/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`).
- Note: `:993` says adding a command is an edit of `WORKER-CONTRACT.md` and `NEVER_AS_WORKER`; no change needed.

### C9. `CHANGELOG.md` — step 1.24b (R8), gate 1.16 — anchor CONFIRMED

- `CHANGELOG.md:5` `## [Unreleased]`. The section's first sub-entry is `:7` `### ccsession: a shim never forwards to another shim`, with `####`-level `Fixed`/`Added` subheadings (`:9`, `:19`).
- Design says one `### Added` entry (line 701), but the current Unreleased section uses `### <topic>` + `#### Added (<topic>)` structure. Builder should follow the file's existing structure, e.g. `### sweep: read-only supervision snapshot (Phase 1)` + `#### Added (sweep)`. Exact heading form is a builder choice (design vs file convention mismatch; flag).
- Content: `superclaude sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-14, `.dev/sweeps/` ignored.

### C10. `.gitignore` — step 1.4a — anchor CONFIRMED

- `.gitignore:254` `.dev/sprint-state/` (comment at `:252-253`). `:255-257` follow with the `e2e-reflect` entry.
- `grep -n sweep .gitignore`: no match — CONFIRMED no existing entry.
- Edit: insert after line 254 (design lines 714-717):
  ```gitignore
  # superclaude sweep reports: dated, operator-local, never posted (WC-14). Never tracked.
  .dev/sweeps/
  ```

### C11. `tests/skills/test_worker_contract.py` — step 1.19, gate 1.18 — anchors CONFIRMED (file is 2265 lines)

| Design anchor | Actual | Edit |
|---|---|---|
| `RULE_PHRASES` dict at line 25 | `:25` `RULE_PHRASES = {`; closes `:237` `}` | add `"WC-14": ("WC-14", ["WC-14. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own"]),` (design line 677) |
| WC-13 at line 155 | `:155` `"WC-13": ("WC-13", ["No Orca fan-out from the worker session"]),` | natural insert point: after `:155`, before `:156` `"heartbeats": (` |
| `NEVER_AS_WORKER` lines 245-254 | `:245` `NEVER_AS_WORKER = (` ... `:252` `"/sc:swarm-wizard",`, `:253` `"/sc:pr-submit",`, `:254` `)` — 8 entries | append `"/sc:sweep",` (design says "append", giving 9). Order does not matter to `_check_never_as_worker` (regex per entry) |
| `_check_never_as_worker` line 398 | `:398-404`: exactly one line containing `**Never-as-worker list**`, each `NEVER_AS_WORKER` entry present in backticks | no edit |
| equality check line 470 | `:470` `assert set(have) == set(UNATTENDED_COMMANDS), (` | no edit (holds because `sweep.md` has no `## Unattended mode`) |
| test at line 545 | `:545` `def test_never_as_worker_list_names_all_seven_commands():` body `:546` `_check_never_as_worker(_contract())` | rename to `test_never_as_worker_list_names_every_listed_command`; body unchanged |
| parametrized removal test line 624 | `:624` `@pytest.mark.parametrize("cmd", NEVER_AS_WORKER)` | no edit; picks up `/sc:sweep` automatically |
| `"load"` assertion line 865 | `:865` `assert "load" not in UNATTENDED_COMMANDS` (in `test_load_usage_line_declares_checkpoint_and_load_is_not_converted`, `:861`) | add `assert "sweep" not in UNATTENDED_COMMANDS` next to it |

`UNATTENDED_COMMANDS` is defined at `:379` `UNATTENDED_COMMANDS: frozenset = frozenset(UNATTENDED_EXPECT)`.

### C12. Files that must pass unchanged

- `tests/commands/test_routing_plugin_parity.py` (C4 check).
- No `pyproject.toml` edit: `integration` marker already registered (design line 731; not re-verified here, researcher 5 scope).

---

## D. Checklist-ready file list in step order

| Step | File | Action |
|---|---|---|
| 1.1 | `src/superclaude/cli/sweep/__init__.py` | create |
| 1.2 | `src/superclaude/cli/sweep/models.py` | create |
| 1.3 | `src/superclaude/cli/sweep/classify.py` | create |
| 1.4a | `src/superclaude/cli/sweep/probes.py` (git half) | create |
| 1.4a | `tests/sweep/test_readonly.py` (1.4a part) | create |
| 1.4a | `.gitignore` after line 254 | modify |
| 1.4 | `src/superclaude/cli/sweep/probes.py` (Orca half, readers, collect) | extend |
| 1.5 | `src/superclaude/cli/sweep/report.py` | create |
| 1.6 | `src/superclaude/cli/sweep/commands.py` | create |
| 1.7 | `src/superclaude/cli/main.py` after line 561 | modify |
| 1.8 | `tests/sweep/conftest.py`, `tests/sweep/fixtures/` | create |
| 1.9 | `tests/sweep/test_classify.py` | create |
| 1.10 | `tests/sweep/test_probes_allowlist.py` | create |
| 1.11 | `tests/sweep/test_readonly.py` (1.11 part) | extend |
| 1.12 | `tests/sweep/test_report.py` | create |
| 1.13 | `tests/sweep/test_cli_registration.py`, `tests/sweep/test_cli_contract.py` | create |
| 1.14 | `src/superclaude/commands/sweep.md` | create |
| 1.15 | `src/superclaude/skills/sc-sweep-protocol/SKILL.md` | create |
| 1.16 | `tests/commands/test_sweep_command.py` | create |
| 1.17 | `src/superclaude/core/WORKER-CONTRACT.md` between lines 156 and 158 | modify |
| 1.18 | `src/superclaude/core/WORKER-CONTRACT.md` line 23 | modify |
| 1.19 | `tests/skills/test_worker_contract.py` lines 155, 254, 545, 865 | modify |
| 1.20 | `tests/recommend/test_routing_refresh.py` line 33 | modify |
| 1.21 | `src/superclaude/core/HOW-WE-WORK.md` after 333 (R1), after 403 (R2) | modify |
| 1.22 | `tests/core/test_how_we_work_routing_table.py` set at 27-40 | modify |
| 1.23 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | byte copy, same commit as 1.21 |
| 1.24 | `docs/user-guide/commands.md` after line 115 | modify |
| 1.24a | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` line 991 | modify |
| 1.24b | `CHANGELOG.md` under line 5 | modify |
| 1.25-1.29 | no file edits (sync, lint, tests, grep, manual pipx check) | verify |

Edit counts per existing file (for the "one item per file" builder): `main.py` 1, `WORKER-CONTRACT.md` 2, `HOW-WE-WORK.md` 2, plugin guide 1 (copy), `test_how_we_work_routing_table.py` 1, `test_routing_refresh.py` 1, `commands.md` 1, developer guide 1, `CHANGELOG.md` 1, `.gitignore` 1, `test_worker_contract.py` 4.

---

## Summary

- 16 new-file entries (6 package modules, `sweep.md`, `SKILL.md`, 7 `tests/sweep/*.py` + fixtures, `tests/commands/test_sweep_command.py`); none exist today. Interfaces copied from design 7.1-7.6 (lines 357-657), step IDs and gates from 15.2 (lines 904-940).
- All 11 existing files exist and every cited line anchor is CONFIRMED; none MOVED. The plugin guide copy is byte-identical to the source guide today.
- Gaps for the builder: `ClassifiedRow` fields undefined in the design (7.2 line 466); the ten #409 `SessionRow` dimensions and SPEC `OrcaObservation` fields are not copied into the design; step 1.4a's `test_readonly.py` precedes `conftest.py` (1.8) and `collect` (1.4), so its fakes/discovery need a decision; CHANGELOG's Unreleased section uses `### <topic>` + `#### Added`, not a bare `### Added`; R2's line anchor shifts by one after R1 lands.
