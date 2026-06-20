# Research: File Inventory

Status: Complete

Scope: `src/superclaude/cli/sprint/` — executor.py, config.py, process.py, logging_.py, checkpoints.py, models.py, rerun_tasks.py, commands.py

Focus: load-bearing symbols the per-task execution + handoff wiring will touch — current signatures, current line numbers (verified by Read), DEAD-or-LIVE status.

## CRITICAL ATTRIBUTION CORRECTION

The task brief attributes several symbols to **config.py** that actually live in **models.py**. Verified by reading both files:

- `SprintConfig` (dataclass + fields) → `models.py:407` (NOT config.py)
- `task_output_file` / `task_error_file` / `output_file` → `models.py:561 / 564 / 555` (NOT config.py)
- `resume_command` → `models.py:677` (method of `SprintResult`, NOT a config symbol)
- `TurnLedger` → `models.py:758` (brief listed it under executor.py; it is defined in models.py, only *constructed* in executor.py)
- `TaskResult` / `TaskResult.to_dict` / `TaskEntry` → `models.py:166 / 184 / 31` (correctly attributed)

`config.py` genuinely owns: `_TASK_HEADING_RE` (line 380), `_DEPENDENCY_RE` (line 385), `parse_tasklist` (line 405), `parse_tasklist_file` (line 501).

## DEAD-or-LIVE headline (the load-bearing finding)

The per-task pipeline is **half-wired**. The runtime fork in `execute_sprint` (executor.py:1264) DOES call `execute_phase_tasks` when a phase has a task inventory — so that path is LIVE. But several supporting symbols built for it are **DEAD in production** (only tests import them):

| Symbol | Defined | Prod caller? | Status |
|---|---|---|---|
| `execute_phase_tasks` | executor.py:928 | execute_sprint:1270 | **LIVE** |
| `_parse_phase_tasks` | executor.py:1121 | execute_sprint:1264 | **LIVE** |
| `_run_task_subprocess` | executor.py:1079 | execute_phase_tasks:1009 | **LIVE** |
| `IsolationLayers` / `setup_isolation` | executor.py:108 / 151 | **none** (live path uses inline `_phase_env_vars`) | **DEAD in prod** |
| `aggregate_task_results` / `AggregatedPhaseReport` | executor.py:297 / 191 | **none** (execute_sprint builds `PhaseResult` inline at 1283) | **DEAD in prod** |
| `build_task_context` | process.py:257 | **none** (never injected into the per-task prompt) | **DEAD in prod** |
| `compress_context_summary` | process.py:347 | only `build_task_context` (itself dead) | **DEAD in prod (transitive)** |
| `get_git_diff_context` | process.py:322 | only `build_task_context` | **DEAD in prod (transitive)** |
| `write_task_rerun_complete` | logging_.py:205 | **none** anywhere in src/ | **DEAD** |
| `write_phase_rerun_start` | logging_.py:190 | **none** in src/ | **DEAD** |
| `write_phase_rerun_complete` | logging_.py:221 | **none** in src/ | **DEAD** |

Caller searches run across `src/` and `tests/` (`grep -rn`). "DEAD in prod" = imported/exercised only by tests, no production call site.

---

## executor.py (2203 lines)

### `IsolationLayers` — dataclass — executor.py:107-148
```python
@dataclass
class IsolationLayers:
    scoped_work_dir: Path
    git_boundary: Path
    plugin_dir: Path
    settings_dir: Path
    @property
    def env_vars(self) -> dict[str, str]   # line 127 — CLAUDE_WORK_DIR, GIT_CEILING_DIRECTORIES, CLAUDE_PLUGIN_DIR, CLAUDE_SETTINGS_DIR
    @property
    def layers_active(self) -> list[str]   # line 137
```
Purpose: 4-layer subprocess isolation config; `env_vars` returns the env-override dict.
**DEAD in prod.** No production caller. Only `tests/sprint/test_executor.py` (752+) and `tests/cli/eval/test_isolation_layers_probe.py`. The LIVE per-phase path uses an inline `_phase_env_vars` dict (executor.py:1327) that sets ONLY `CLAUDE_WORK_DIR` — the other 3 layers are not wired into runtime. **This is the central "wire the dead isolation" seam.**

### `setup_isolation(config: SprintConfig) -> IsolationLayers` — func — executor.py:151-183
Purpose: factory that mkdir's `<results_dir>/.isolation/{plugins,settings}` and returns an `IsolationLayers` (scoped_work_dir=git_boundary=config.release_dir). **DEAD in prod** (tests only).

### `AggregatedPhaseReport` — dataclass — executor.py:191-294
Fields: `phase_number`, `tasks_total/passed/failed/incomplete/skipped/not_attempted`, `budget_remaining`, `total_turns_consumed`, `total_duration_seconds`, `task_results: list[TaskResult]`, `remaining_task_ids: list[str]`. Methods: `status` property (191→214: PASS/FAIL/PARTIAL), `to_yaml()` (224), `to_markdown()` (256, emits `EXIT_RECOMMENDATION: CONTINUE/HALT`).
**DEAD in prod** (tests only). execute_sprint builds a plain `PhaseResult` inline instead (1283).

### `aggregate_task_results(phase_number, task_results, remaining_task_ids=None, budget_remaining=0) -> AggregatedPhaseReport` — func — executor.py:297-336
Purpose: runner-authoritative aggregation of TaskResults into counts/status (does not trust agent self-report). **DEAD in prod** (only `tests/sprint/test_e2e_trailing.py`, `test_executor.py`).

### `execute_phase_tasks(...) -> tuple[list[TaskResult], list[str], list[TrailingGateResult]]` — func — executor.py:928-1076
```python
def execute_phase_tasks(
    tasks: list[TaskEntry], config: SprintConfig, phase,
    ledger: TurnLedger | None = None, *,
    _subprocess_factory=None,
    shadow_metrics: ShadowGateMetrics | None = None,
    remediation_log: DeferredRemediationLog | None = None,
    tui: "SprintTUI | None" = None,
    sprint_result: "SprintResult | None" = None,
) -> tuple[list[TaskResult], list[str], list[TrailingGateResult]]
```
Purpose: per-task subprocess loop. Budget-gates each task via ledger (978 skip-remaining, 992 pre-debit `minimum_allocation`, 1026-1033 reconcile), spawns via `_subprocess_factory` (test) OR `_run_task_subprocess` (prod, 1009), maps exit code → TaskStatus (1016: 0=PASS, 124=INCOMPLETE, transient→FAIL_RECOVERABLE, else FAIL_TERMINAL), runs `run_post_task_wiring_hook` (1046) + `run_post_task_anti_instinct_hook` (1056).
**LIVE.** Called by execute_sprint:1270.
NOTE: `_subprocess_factory` is the **test seam** — production never passes it; it defaults to None and falls through to `_run_task_subprocess`.

### `_run_task_subprocess(task, config, phase) -> tuple[int,int,int]` — func — executor.py:1079-1118
Purpose: real per-task subprocess. Builds an **inline minimal prompt** (1090-1094: `f"Execute task {task.task_id}: {task.title}\nFrom phase file: {phase.file}\nDescription: {task.description}\n"`) — does NOT call `build_prompt` or `build_task_context`. Constructs a `ClaudeProcess` via `__new__` + pipeline base `__init__` (1096-1111), output → `config.task_output_file(phase, task)`. Returns `(exit_code, 0, output_bytes)`.
**LIVE.** Called by execute_phase_tasks:1009.
**Two wiring gaps visible here:** (a) turns_consumed is hard-coded `0` (line 1118, comment "Turn counting is wired separately in T02.06"); (b) no prior-task context injection (build_task_context unused).

### `_parse_phase_tasks(phase: Phase, config: SprintConfig) -> list[TaskEntry] | None` — func — executor.py:1121-1135
Purpose: lazily imports `config.parse_tasklist`, reads phase file, returns task list or None for freeform phases. **LIVE.** Called by execute_sprint:1264.

### `execute_sprint(config: SprintConfig)` — func — executor.py:1138-(through ~1766)
Purpose: main orchestration loop. **The runtime fork is at executor.py:1264-1307:**
```python
tasks = _parse_phase_tasks(phase, config)        # 1264
if tasks:                                         # 1265 — PER-TASK PATH (LIVE)
    task_results, remaining, phase_gate_results = execute_phase_tasks(...)   # 1270
    ... builds PhaseResult inline (1283) ...      # NOT aggregate_task_results
    continue                                      # 1307
# else: SINGLE-CLAUDEPROCESS FALLBACK (1309+)
```
Infrastructure constructed up-front: `TurnLedger(initial_budget=max_turns * len(active_phases), reimbursement_rate=0.8)` (1203), `ShadowGateMetrics()` (1208), `DeferredRemediationLog(persist_path=results_dir/"remediation.json")` (1212), `SprintGatePolicy(config)` (1219, discarded).
**`_phase_env_vars`** is the inline dict at **executor.py:1327-1329** — lives in the *fallback* (single-process) branch, sets ONLY `CLAUDE_WORK_DIR=isolation_dir`; passed to `ClaudeProcess(config, phase, env_vars=_phase_env_vars)` (1330). The per-task branch (execute_phase_tasks) does NOT set any isolation env vars.

### Other relevant executor.py symbols
- `check_budget_guard(ledger) -> str | None` — 339 — pre-launch budget guard. LIVE-adjacent (used by hooks).
- `_is_transient_failure(output_path) -> bool` — 1782 — feeds FAIL_RECOVERABLE classification (used at 1020).
- `_write_phase_result_json(config, phase, result)` — 2053 — persists `phase-<N>-result.json` for rerun-tasks consumption. LIVE, called at 1304 (per-task branch).
- `run_post_task_wiring_hook` (459), `run_post_task_anti_instinct_hook` (804), `run_post_phase_wiring_hook` (749) — LIVE hooks invoked in the per-task loop / branch.

---

## config.py (515 lines) — parsing + regexes only

### `_TASK_HEADING_RE` — module regex — config.py:380-383
```python
_TASK_HEADING_RE = re.compile(r"^###\s+(T\d{2}\.\d{2})\s*(?:--|-—|—)\s*(.+)", re.MULTILINE)
```
Matches `### T<PP>.<TT> -- Title` headings. group(1)=task_id, group(2)=title. **LIVE** (used by parse_tasklist:426).

### `_DEPENDENCY_RE` — module regex — config.py:385-388
```python
_DEPENDENCY_RE = re.compile(r"\*\*Dependencies:\*\*\s*(.*)", re.IGNORECASE)
```
Matches `**Dependencies:** ...` line; group(1) then scanned by `_TASK_ID_REF_RE` (390, `T\d{2}\.\d{2}`). **LIVE** (parse_tasklist:443).
Sibling regexes: `_COMMAND_RE` (393), `_CLASSIFIER_RE` (399).

### `parse_tasklist(content: str, execution_mode: str = "claude") -> list[TaskEntry]` — func — config.py:405-498
Purpose: parse phase markdown into `TaskEntry` list (task_id, title, description-from-Deliverables, dependencies, command, classifier). python-mode tasks without a command raise `click.ClickException` (483). **LIVE** — called by `_parse_phase_tasks` (executor.py:1128, lazy import) and `walk_dependencies` (rerun_tasks.py:407, lazy import).

### `parse_tasklist_file(path: Path, execution_mode="claude") -> list[TaskEntry]` — func — config.py:501
Thin file-reading wrapper around parse_tasklist. LIVE.

(`SprintConfig`, `task_output_file`, etc. are in models.py — see below.)

---

## process.py (385 lines)

### `ClaudeProcess` — class (extends pipeline `ClaudeProcess`) — process.py:88
- `__init__(self, config, phase, *, env_vars: dict[str,str] | None = None)` — 97-121. Stores config/phase/`_extra_env_vars`, builds prompt via `self.build_prompt()` (107), calls pipeline base `super().__init__(...)` with output→`config.output_file(phase)`, lifecycle hooks, `env_vars=env_vars`. **LIVE** (constructed in execute_sprint fallback:1330; also re-used in `_run_task_subprocess` via `__new__`).

### `build_prompt(self) -> str` — method — process.py:123-216
Purpose: builds the **PHASE-LEVEL** `/sc:task` prompt — `f"/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic"` plus Sprint Context / Execution Rules / Checkpoints / Result File sections. **LIVE** for the single-process fallback (called by ClaudeProcess.__init__:107).
IMPORTANT: This is a *whole-phase* prompt. The per-task path (`_run_task_subprocess`) does NOT use it — it hand-rolls a 3-line per-task prompt instead. Wiring per-task prompts to reuse this scaffolding is a likely seam (R3 territory).

### `build_task_context(prior_results, *, start_commit="", compress_threshold=3) -> str` — func — process.py:257-319
Purpose: deterministic markdown context block from prior `TaskResult`s (prior results + gate outcomes + remediation history + optional git diff). Applies progressive summarization when `len > compress_threshold` (289). **DEAD in prod** — only `tests/sprint/test_process.py`. Never injected into any prompt.

### `get_git_diff_context(start_commit: str) -> str` — func — process.py:322-344
`git diff --stat <start_commit>` → markdown section, "" on error. **DEAD in prod** (only called by build_task_context:315).

### `compress_context_summary(results, *, keep_recent=3) -> str` — func — process.py:347-385
Progressive summarization: tasks beyond `keep_recent` window → one-line `to_context_summary(verbose=False)`; recent → verbose. **DEAD in prod (transitive)** — called only by build_task_context:290 (itself dead) + tests.

---

## logging_.py (290 lines)

### `SprintLogger` — class — logging_.py:13
- `__init__(self, config: SprintConfig)` — 23. **LIVE** (instantiated execute_sprint:1164).
- `_jsonl(self, data: dict)` — 265-267 — appends `json.dumps(data, default=str)+"\n"` to `config.execution_log_jsonl`. The single JSONL sink for all events. **LIVE**.

### Event names emitted via `_jsonl` (all from logging_.py)
| Method | line | `"event"` value | LIVE? |
|---|---|---|---|
| `write_header` | 28 | `sprint_start` | LIVE (execute_sprint:1224) |
| `write_phase_start` | 59 | `phase_start` | LIVE |
| `write_phase_interrupt` | 71 | `phase_interrupt` | LIVE |
| `write_phase_result` | 89 | `phase_complete` | LIVE |
| `write_checkpoint_verification` | 159 | `checkpoint_verification` | LIVE (verify path) |
| `write_phase_rerun_start` | 190 | `phase_rerun_start` | **DEAD** (no src caller) |
| `write_task_rerun_complete` | 205 | `task_rerun_complete` | **DEAD** (no src caller) |
| `write_phase_rerun_complete` | 221 | `phase_rerun_complete` | **DEAD** (no src caller) |
| `write_summary` | 245 | `sprint_complete` | LIVE |

### `write_task_rerun_complete(self, phase: int, task_id: str, status: str, turns: int, duration_sec: float) -> None` — logging_.py:205-219
Emits `{"event":"task_rerun_complete","phase","task_id","status","turns","duration_sec","timestamp"}`. **DEAD** — defined for the rerun-tasks flow but `run_rerun_tasks` (rerun_tasks.py) never calls it. Wiring this into the rerun executor is a candidate seam.

---

## checkpoints.py (439 lines)

### `write_manifest(entries: list[CheckpointEntry], output_path: Path) -> None` — func — checkpoints.py:173-210 — **the atomic temp+replace write**
```python
output_path.parent.mkdir(parents=True, exist_ok=True)
tmp = output_path.with_suffix(output_path.suffix + ".tmp")   # 208
tmp.write_text(json.dumps(payload, indent=2) + "\n")          # 209
tmp.replace(output_path)                                       # 210
```
Purpose: serialize checkpoint manifest (summary counts + entries) to JSON atomically (temp file + `Path.replace`). LIVE (verify-checkpoints path). This `with_suffix(".tmp")` + `.replace()` idiom is the canonical atomic-write pattern in this package — also duplicated in rerun_tasks.py (see below). Sibling symbols: `extract_checkpoint_paths` (40), `verify_checkpoint_files` (101), `build_manifest` (138), `recover_missing_checkpoints` (213).

---

## models.py (948 lines)

### `TaskEntry` — dataclass — models.py:30-42
```python
@dataclass
class TaskEntry:
    task_id: str
    title: str
    description: str = ""
    dependencies: list[str] = field(default_factory=list)
    command: str = ""
    classifier: str = ""
```
Purpose: one `### T<PP>.<TT>` block. **LIVE** (produced by parse_tasklist, consumed everywhere).

### `TaskResult` — dataclass — models.py:165-264
```python
@dataclass
class TaskResult:
    task: TaskEntry
    status: TaskStatus = TaskStatus.SKIPPED
    turns_consumed: int = 0
    exit_code: int = 0
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    output_bytes: int = 0
    gate_outcome: GateOutcome = GateOutcome.PENDING
    reimbursement_amount: int = 0
    output_path: str = ""
```
Methods: `to_dict()` (184), `from_dict()` classmethod (212), `duration_seconds` property (236), `to_context_summary(*, verbose=True)` (240). **LIVE** (produced by execute_phase_tasks).

### `TaskResult.to_dict(self) -> dict` — models.py:184-210
Purpose: JSON-safe dict for `phase-N-result.json` (v4.3.0). Enums→`.value`, datetimes→`.isoformat()`, nested `task` serialized as TaskEntry-field dict literal. Round-trips via `from_dict`. **LIVE** (used when persisting phase result JSON).

### `SprintConfig(PipelineConfig)` — dataclass — models.py:406-(through ~572)
Sprint-specific fields (with defaults): `index_path`, `release_dir`, `phases: list[Phase]`, `start_phase=1`, `end_phase=0`, `max_turns=100`, `model=""`, `dry_run=False`, `permission_flag="--dangerously-skip-permissions"`, `tmux_session_name=""`, `debug=False`, `stall_timeout=0`, `startup_stall_timeout=300`, `stall_action="warn"`, `phase_timeout=0`, `shadow_gates=False`, `wiring_gate_mode: Literal["off","shadow","soft","full"]="soft"`, `gate_rollout_mode: Literal[...]="off"`, `wiring_gate_scope="task"`, `wiring_analysis_turns=1`, `remediation_cost=2`, `wiring_gate_enabled=True`, `wiring_gate_grace_period=0`, `checkpoint_gate_mode: Literal[...]="shadow"`, `total_tasks=0`, `state_dir`. `__post_init__` (474) syncs `release_dir`→`work_dir`.
Path methods/properties: `results_dir` property (538), `execution_log_jsonl` property (542), `execution_log_md` property (546), `output_file(phase)` (555), `error_file(phase)` (558), `task_output_file(phase, task)` (561), `task_error_file(phase, task)` (564), `result_file(phase)` (567). **LIVE**.

### `task_output_file(self, phase: Phase, task: TaskEntry) -> Path` — models.py:561-562
Returns `self.results_dir / f"phase-{phase.number}-task-{task.task_id}-output.txt"`. **LIVE** (executor.py:1104, 1115, 1020). `task_error_file` (564) is the parallel `-errors.txt`.

### `resume_command(self) -> str` — method of `SprintResult` — models.py:677-684
```python
def resume_command(self) -> str:
    if self.halt_phase is not None:
        end = self.config.end_phase or max(p.number for p in self.config.phases)
        return f"superclaude sprint run {self.config.index_path} --start {self.halt_phase} --end {end}"
    return ""
```
Purpose: builds the `sprint run --start --end` resume hint on halt. **LIVE** (logging_.py:263, write_summary). NOTE: emits PHASE-granular resume, not task-granular — relevant if per-task handoff wants task-level resume.

### `TurnLedger` — dataclass — models.py:757-841
```python
@dataclass
class TurnLedger:
    initial_budget: int
    consumed: int = 0
    reimbursed: int = 0
    reimbursement_rate: float = 0.8
    minimum_allocation: int = 5
    minimum_remediation_budget: int = 3
    wiring_turns_used: int = 0
    wiring_turns_credited: int = 0
    wiring_budget_exhausted: int = 0
    wiring_analyses_count: int = 0
```
Methods: `available()` (782), `debit(turns)` (786, monotonic), `credit(turns)` (792), `can_launch()` (798, ≥minimum_allocation), `can_remediate()` (802), `debit_wiring(turns=1)` (806), `credit_wiring(turns, rate=None) -> int` (820, `int(turns*rate)` floor), `can_run_wiring_gate()` (837). **LIVE** (constructed execute_sprint:1203; driven by execute_phase_tasks budget logic).
(Note: name-collision with unrelated `TurnLedger` classes in `cli/cli_portify/models.py:681` and `cli/prd/executor.py:145` — distinct definitions.)

Other relevant: `Phase` dataclass (340), `PhaseResult(StepResult)` (585, has `task_results`), `SprintResult` (623), `MonitorState` (687), `ShadowGateMetrics` (901), `build_resume_output(config, halt_task_id, remaining_tasks)` (844 — task-level resume builder, verify callers in R5 scope).

---

## rerun_tasks.py (1482 lines)

### `walk_dependencies(...) -> tuple[list[str], list[str]]` — func — rerun_tasks.py:368-(through ~545)
```python
def walk_dependencies(
    phase_tasklist: Path, target_ids: list[str], *,
    phase_result: Optional[PhaseResult] = None,
    results_dir: Optional[Path] = None,
    include_transitive: bool = False,
    ignore_deps: bool = False,
) -> tuple[list[str], list[str]]   # (resolved_target_ids, warnings)
```
Purpose: resolve+validate the dependency closure for rerun targets. Reads declared deps via lazy `config.parse_tasklist` (407, 420), checks satisfaction against `target_ids` + recorded `phase_result` statuses, cross-phase deps verified via `checkpoints.verify_checkpoint_files` (467, lazy import). Unsatisfied dep → `click.ClickException` unless `ignore_deps`. `include_transitive` auto-includes up to a 50%-of-phase-cost ceiling. **LIVE** — called by `run_rerun_tasks` (1315).

### `_dependencies_of(task_id: str) -> list[str]` — nested func inside walk_dependencies — rerun_tasks.py:438-451
Purpose: order-preserving de-duplicated union of declared deps from the parsed source tasklist (`entry_by_id`) and the persisted result snapshot (`result_by_id`). Closure over walk_dependencies locals. **LIVE** (called at 479). NOT a module-level symbol — only reachable inside walk_dependencies.

### `_atomic_write_text(path: Path, text: str) -> None` — func — rerun_tasks.py:664-668
The rerun-module's own atomic write (`with_suffix(".tmp")` + `tmp.replace(path)`) — same idiom as checkpoints.write_manifest. Also duplicated inline at rerun_tasks.py:187-189 (`extract_phase_subset`) and 333-335 (`build_sub_index`). **LIVE**.

Other rerun symbols (LIVE, context for handoff): `extract_phase_subset` (91), `build_rerun_bundle_dir` (215), `build_sub_index` (269), `select_default_recoverable_tasks(phase_result_json)` (1100), `flip_target_checkboxes` (765), `finalize_checkboxes_on_success` (858), `restore_checkboxes_on_abort` (819), `run_rerun_tasks(...)` (1210 — the rerun-tasks command entrypoint).

---

## commands.py (589 lines)

### `run(...)` click command — commands.py:72-291
`@sprint_group.command()` with `@click.argument("index_path", ...)` (73) and options (param dest in parens):
- `--start` → `start_phase: int = 1` (74-80)
- `--end` → `end_phase: int = 0` (81-87, 0=last discovered)
- `--max-turns` → `max_turns: int = 100` (88)
- `--model` → `model: str = ""` (94)
- `--dry-run` → `dry_run` flag (99)
- `--no-tmux` → `no_tmux` flag (104)
- `--permission-flag` → Choice, default `--dangerously-skip-permissions` (109)
- `--tmux-session-name` → hidden internal (120)
- `--debug` → `debug_mode` flag (126)
- `--stall-timeout` → `stall_timeout: int = 0` (133)
- `--startup-stall-timeout` → `startup_stall_timeout: int = 300` (139)
- `--stall-action` → Choice warn/kill, default warn (147)
- `--shadow-gates` → flag (153)
- `--force-fidelity-fail JUSTIFICATION` / `--force-fidelity` → `force_fidelity_fail: str` (159/170)
- `--release-dir` → `release_dir_override: Path | None` (176)
- `--state-dir` → `state_dir_override: Path | None` (183)

Body (190-291): builds config via `load_sprint_config(...)` (230), applies tmux/release-dir/state-dir overrides, runs `_check_fidelity` (272), and dispatches: `--dry-run`→`_print_dry_run` (284); else `launch_in_tmux(config)` (289) if tmux available else **`execute_sprint(config)`** (291). **LIVE** — this is the CLI entry into the executor. There is NO per-task CLI flag; the per-task vs single-process choice is made at runtime inside execute_sprint based on whether the phase file parses into tasks.

Other commands in file: `attach` (294), `status` (306), `logs` (318), `kill` (343), `verify-checkpoints` (361), `rerun-tasks` (419, with its own --start/etc. — entrypoint `rerun_tasks` at 485 → delegates to `run_rerun_tasks`).

---

## Summary

All 8 files inventoried; every symbol verified by Read with current line numbers.

**Key findings for the wiring task:**

1. **The fork is LIVE but the support cast is DEAD.** `execute_sprint` (executor.py:1264) already branches into `execute_phase_tasks` → `_run_task_subprocess` for task-inventory phases. But `IsolationLayers`/`setup_isolation`, `aggregate_task_results`/`AggregatedPhaseReport`, `build_task_context`/`compress_context_summary`/`get_git_diff_context`, and all three `write_*_rerun_*` logging methods have **no production callers** (tests only). These are the "dead" symbols to wire.

2. **Isolation is the headline gap.** The LIVE per-phase fallback sets ONLY `CLAUDE_WORK_DIR` via an inline `_phase_env_vars` dict (executor.py:1327); the 4-layer `IsolationLayers.env_vars` is never used at runtime, and the per-task branch sets no isolation env at all.

3. **Per-task prompt is a stub.** `_run_task_subprocess` (executor.py:1090) hand-rolls a 3-line prompt and never calls `build_prompt` (the rich phase prompt) or `build_task_context` (prior-result injection) → context-handoff is unwired.

4. **Turn counting is stubbed** — `_run_task_subprocess` returns `turns_consumed=0` (executor.py:1118, "wired separately in T02.06").

5. **Attribution correction:** `SprintConfig`, `task_output_file`/`task_error_file`/`output_file`, `resume_command`, and `TurnLedger` are in **models.py**, NOT config.py as the brief stated. config.py holds only the regexes + `parse_tasklist`.

6. **Atomic write pattern** = `Path.with_suffix(suffix+".tmp")` → write → `tmp.replace(target)`, canonical in `checkpoints.write_manifest` (210) and duplicated as `rerun_tasks._atomic_write_text` (664) + inline at rerun_tasks.py:189, 335.

7. **`run()` has no per-task flag** — `--start`/`--end` are phase-granular (commands.py:74/81); per-task vs single-process is decided at runtime by whether the phase file parses into tasks. `resume_command` (models.py:677) also emits phase-granular resume only.
