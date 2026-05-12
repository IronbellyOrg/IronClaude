# Sprint CLI — Comprehensive Architecture Reference

This document is the authoritative reference for the `superclaude sprint` CLI subsystem. It covers every module, every data flow, every decision point, and every known design gap — with line-number references to the source code.

**Source tree**: `src/superclaude/cli/sprint/`

---

## Table of Contents

1. [Entry Point & Command Group](#1-entry-point--command-group)
2. [Module Map](#2-module-map)
3. [Configuration Loading](#3-configuration-loading)
4. [Phase Discovery](#4-phase-discovery)
5. [Tasklist Parsing](#5-tasklist-parsing)
6. [Pre-Launch Gates](#6-pre-launch-gates)
7. [Tmux Integration](#7-tmux-integration)
8. [The Main Orchestration Loop](#8-the-main-orchestration-loop)
9. [Execution Modes](#9-execution-modes)
10. [Preflight Executor (Python Mode)](#10-preflight-executor-python-mode)
11. [Per-Task Delegation Path](#11-per-task-delegation-path)
12. [Whole-Phase Execution Path](#12-whole-phase-execution-path)
13. [Subprocess Construction & Isolation](#13-subprocess-construction--isolation)
14. [Prompt Construction & Context Injection](#14-prompt-construction--context-injection)
15. [Budget System (TurnLedger)](#15-budget-system-turnledger)
16. [Wiring Integrity Gate](#16-wiring-integrity-gate)
17. [Anti-Instinct Gate](#17-anti-instinct-gate)
18. [Output Monitoring (Sidecar Thread)](#18-output-monitoring-sidecar-thread)
19. [Phase Status Determination](#19-phase-status-determination)
20. [TUI Dashboard](#20-tui-dashboard)
21. [Logging & Diagnostics](#21-logging--diagnostics)
22. [KPI Report](#22-kpi-report)
23. [Sprint Finalization & Cleanup](#23-sprint-finalization--cleanup)
24. [Results Directory Layout](#24-results-directory-layout)
25. [Data Model Reference](#25-data-model-reference)
26. [Pipeline Inheritance](#26-pipeline-inheritance)
27. [Critical Behavioral Asymmetry](#27-critical-behavioral-asymmetry)
28. [Known Design Gaps](#28-known-design-gaps)
29. [CLI Options Reference](#29-cli-options-reference)
30. [End-to-End Flow Diagram](#30-end-to-end-flow-diagram)

---

## 1. Entry Point & Command Group

The sprint CLI is a Click command group registered in `cli/main.py`:

```python
# main.py:356
from superclaude.cli.sprint import sprint_group
main.add_command(sprint_group, name="sprint")
```

`sprint/__init__.py` is a single re-export:

```python
from .commands import sprint_group
```

The `sprint_group` in `commands.py` defines **5 subcommands**:

| Subcommand | Purpose | Key Implementation |
|---|---|---|
| `sprint run <index>` | Execute a sprint from a tasklist index | `commands.py:run()` → `executor.py:execute_sprint()` |
| `sprint attach` | Attach to a running tmux sprint session | `tmux.py:attach_to_sprint()` |
| `sprint status` | Show current sprint status without attaching | Reads `.sprint-exitcode` sentinel |
| `sprint logs [-n N] [-f]` | Tail the sprint execution log | Reads `execution-log.jsonl` |
| `sprint kill [--force]` | Stop a running sprint | `tmux.py:kill_sprint()` |

The `run` command has **16 CLI options** (see [Section 29](#29-cli-options-reference)).

---

## 2. Module Map

```
sprint/
  __init__.py          # Re-exports sprint_group
  commands.py          # Click command definitions (run, attach, status, logs, kill)
  config.py            # Phase discovery, validation, tasklist parsing
  models.py            # All data models: SprintConfig, Phase, TaskEntry, TurnLedger, etc.
  executor.py          # Core orchestration loop + quality gate hooks (~1850 lines)
  process.py           # ClaudeProcess subprocess wrapper + context injection
  tmux.py              # Tmux session management (launch, attach, kill)
  monitor.py           # Sidecar output monitor (NDJSON parser, liveness tracking)
  tui.py               # Rich-based terminal dashboard
  logging_.py          # Dual-format JSONL + Markdown execution logs
  diagnostics.py       # Post-failure classification + diagnostic bundles
  preflight.py         # Python-mode phase executor (subprocess.run)
  classifiers.py       # Classifier registry for task result classification
  kpi.py               # KPI report for gate/remediation metrics
  debug_logger.py      # Structured debug logging
  notify.py            # Desktop notifications on phase/sprint completion
```

**Dependency flow**: `commands.py` → `config.py` → `models.py` ← `executor.py` ← `process.py`, `monitor.py`, `tui.py`, `diagnostics.py`, `preflight.py`

---

## 3. Configuration Loading

**File**: `config.py` — `load_sprint_config()`

The `run` command calls `load_sprint_config()` which:

1. **Resolves the release directory** — `_resolve_release_dir()` detects if the index lives inside a `tasklist/` subdirectory and resolves up to the grandparent (the true release directory)
2. **Discovers phases** — `discover_phases()` scans the index file and/or its directory
3. **Extracts phase names** — reads the first `# Heading` from each phase file
4. **Validates** — `validate_phases()` checks files exist, warns on gaps in phase numbering
5. **Auto-detects end phase** — if `--end` is not specified, uses the highest phase number
6. **Builds SprintConfig** — populates all fields from CLI options + discovered data

### SprintConfig Construction

`SprintConfig` is a dataclass extending `PipelineConfig` (`models.py:296`). It has 20+ fields:

```python
@dataclass
class SprintConfig(PipelineConfig):
    index_path: Path              # Path to tasklist-index.md
    release_dir: Path             # Root release directory
    phases: list[Phase]           # All discovered phases
    start_phase: int = 1          # --start
    end_phase: int = 0            # --end (0 = auto)
    max_turns: int = 100          # --max-turns
    model: str = ""               # --model
    dry_run: bool = False         # --dry-run
    permission_flag: str = "--dangerously-skip-permissions"
    tmux_session_name: str = ""
    debug: bool = False           # --debug
    stall_timeout: int = 0        # --stall-timeout (0 = disabled)
    stall_action: str = "warn"    # --stall-action: "warn" or "kill"
    phase_timeout: int = 0
    shadow_gates: bool = False
    wiring_gate_mode: Literal["off","shadow","soft","full"] = "soft"
    gate_rollout_mode: Literal["off","shadow","soft","full"] = "off"
    wiring_gate_scope: str = "task"
    wiring_analysis_turns: int = 1
    remediation_cost: int = 2
    wiring_gate_enabled: bool = True
    wiring_gate_grace_period: int = 0
```

**`__post_init__` behavior** (`models.py:338`):

1. Syncs `release_dir` to the inherited `work_dir` field
2. Runs a **migration shim** for deprecated field names (`wiring_budget_turns` → `wiring_analysis_turns`, etc.) — emits `DeprecationWarning`
3. Derives `wiring_gate_mode` from scope-based fields: if `wiring_gate_enabled=False` → mode becomes `"off"`; if `wiring_gate_grace_period >= 999_999` → mode becomes `"shadow"`

---

## 4. Phase Discovery

**File**: `config.py` — `discover_phases()`

Phases are files matching one of **4 canonical filename patterns**:

```python
PHASE_FILE_PATTERN = re.compile(
    r"(?:phase-(\d+)-tasklist\.md"      # phase-1-tasklist.md
    r"|p(\d+)-tasklist\.md"              # p1-tasklist.md
    r"|phase_(\d+)_tasklist\.md"         # phase_1_tasklist.md
    r"|tasklist-p(\d+)\.md)",            # tasklist-p1.md
    re.IGNORECASE,
)
```

**Discovery uses two strategies**:

- **Strategy 1 — Parse index file**: Scans the index markdown for phase file references. Also reads the optional `Execution Mode` column from a markdown pipe-table containing a `File` column.
- **Strategy 2 — Scan directory**: Falls back to directory-level file matching.

**Execution mode column parsing** (`config.py:42-96`): If the index contains a pipe-table with `File` and `Execution Mode` columns, each phase gets tagged with a mode. Unknown modes raise `ClickException`. Allowed values: `claude`, `python`, `skip`.

```markdown
| Phase | File | Execution Mode |
|-------|------|----------------|
| 1 | phase-1-tasklist.md | python |
| 2 | phase-2-tasklist.md | claude |
| 3 | phase-3-tasklist.md | skip |
```

Phases without an explicit mode default to `claude`.

---

## 5. Tasklist Parsing

**File**: `config.py` — `parse_tasklist()`

Parses structured task headings from phase markdown files. Uses these regexes:

```python
_TASK_HEADING_RE = re.compile(r"^###\s+T(\d{2}\.\d{2})\s*(?:--|—)\s*(.*)", re.MULTILINE)
_DEPENDENCY_RE   = re.compile(r"\*\*Dependencies:\*\*\s*(.*)", re.IGNORECASE)
_COMMAND_RE      = re.compile(r"\*\*Command:\*\*\s*`([^`]+)`", re.IGNORECASE)
_CLASSIFIER_RE   = re.compile(r"\|\s*Classifier\s*\|\s*(\w+)\s*\|", re.IGNORECASE)
```

**Expected format in phase files**:

```markdown
### T01.01 -- Implement feature X

**Dependencies:** None
**Command:** `uv run pytest tests/`
**Deliverables:**
- New module with full test coverage

| Classifier | empirical_gate_v1 |
```

**Extracted into `TaskEntry`** (`models.py:26`):
- `task_id`: e.g., `"T01.01"` — phase number + task number
- `title`: text after the `--` separator
- `dependencies`: list of task IDs from `**Dependencies:**`
- `command`: shell command from `**Command:**` (used by python-mode)
- `classifier`: classifier name from the pipe table
- `description`: lines after `**Deliverables:**`

**Return value**: Returns `list[TaskEntry]` if any `### T<PP>.<TT>` headings are found, or `[]` for freeform phases (no structured tasks). This distinction drives the per-task vs. whole-phase execution path decision.

---

## 6. Pre-Launch Gates

### 6.1 Fidelity Check

**File**: `commands.py` — `_check_fidelity()`

Before execution, the runner checks for a `.roadmap-state.json` file in the release directory. If `fidelity_status: "fail"` is found, the sprint is **blocked**:

```
Sprint blocked: spec-fidelity check FAILED.
The tasklist was generated from a spec with unresolved HIGH severity deviations.
```

Override with:
- `--force-fidelity-fail 'justification text'`

This prevents executing sprints generated from specs with unresolved HIGH-severity deviations.

### 6.2 Dry Run

With `--dry-run`, the runner prints discovered phases in a formatted table and exits — no execution, no tmux, no infrastructure.

### 6.3 Claude Binary Check

The first thing `execute_sprint()` does is verify `claude` is in `PATH` (`executor.py:1124`). If missing:

```
Error: 'claude' binary not found in PATH.
Install Claude Code CLI before running sprint.
```

---

## 7. Tmux Integration

**File**: `tmux.py`

### Decision Logic

By default, if tmux is available and the user is not already inside a tmux session (`TMUX` env var not set), the sprint runs inside tmux. With `--no-tmux`, it runs directly in the current terminal.

### Session Lifecycle

`launch_in_tmux()` (`tmux.py:50`):

1. **Deterministic session name**: `sc-sprint-<sha1(release_dir)[:8]>`
2. **Creates detached session**: `tmux new-session -d -s <name> -x 120 -y 40`
3. **Runs the sprint in foreground mode** inside the session — builds a `superclaude sprint run ... --no-tmux` command via `_build_foreground_command()`
4. **Splits the window**: Bottom pane (25% height) tails the output file of the first active phase
5. **Selects top pane**: The TUI runs in pane 0.0
6. **Attaches**: Blocks until user detaches or session ends
7. **Reads exit code**: After detaching, reads `.sprint-exitcode` sentinel file

### Session Management

| Function | Behavior |
|---|---|
| `is_tmux_available()` | Returns `True` if `tmux` binary exists AND `TMUX` env var is not set |
| `session_name(release_dir)` | Deterministic `sc-sprint-<sha1[:8]>` from resolved path |
| `find_running_session()` | Lists tmux sessions, returns first `sc-sprint-*` match |
| `update_tail_pane(session, output_file)` | Sends `C-c` to pane 0.1, then `tail -f <file>` |
| `attach_to_sprint()` | Finds and attaches to running session |
| `kill_sprint(force)` | Graceful: SIGTERM → 10s wait → SIGKILL → kill-session. Force: immediate kill-session |

### Cleanup on Setup Failure

If the `split-window` or `select-pane` commands fail after session creation, the session is killed immediately to prevent stale sessions from blocking future runs (`tmux.py:103-106`).

---

## 8. The Main Orchestration Loop

**File**: `executor.py` — `execute_sprint()` (lines 1112–1553)

This is the core of the sprint runner. Here is the precise execution sequence:

### 8.1 Infrastructure Setup (lines 1123–1168)

```
1. Verify `claude` binary in PATH
2. Install SignalHandler (catches SIGINT/SIGTERM, sets shutdown flag)
3. Set up debug logger
4. Initialize SprintLogger (dual JSONL + Markdown)
5. Initialize SprintTUI (Rich Live display)
6. Initialize OutputMonitor (pointed at /dev/null, reset per phase)
7. Initialize SprintResult (aggregate outcome tracker)
8. Initialize TurnLedger:
     initial_budget = max_turns × len(active_phases)
     reimbursement_rate = 0.8
9. Initialize ShadowGateMetrics (anti-instinct telemetry accumulator)
10. Initialize DeferredRemediationLog (persists to results/remediation.json)
11. Initialize SprintGatePolicy (builds remediation steps from failures)
12. Initialize gate results accumulator: all_gate_results = []
13. Write execution log header
14. Start TUI
15. Orphan cleanup: rm -rf results/.isolation/ (stale from crashed previous runs)
```

### 8.2 Preflight Execution (line 1175)

```python
from .preflight import execute_preflight_phases
preflight_results = execute_preflight_phases(config)
```

All python-mode phases are executed **before** the main loop. This is a single function call that handles all python-mode phases. See [Section 10](#10-preflight-executor-python-mode).

### 8.3 Main Phase Loop (lines 1178–1489)

```python
for phase in config.active_phases:
    # Check 1: Shutdown requested? → INTERRUPTED, break
    # Check 2: Python mode? → already done by preflight, continue
    # Check 3: Skip mode? → record SKIPPED, continue
    # Check 4: Has structured tasks (### T<PP>.<TT>)? → per-task path
    # Else: whole-phase ClaudeProcess path
```

**Branch decision**: `_parse_phase_tasks()` (`executor.py:1095`) reads the phase file and calls `parse_tasklist()`. If it returns a non-empty list → per-task path. If it returns `None` (no `### T<PP>.<TT>` headings) → whole-phase path.

### 8.4 Post-Loop Finalization (lines 1491–1553)

See [Section 23](#23-sprint-finalization--cleanup).

---

## 9. Execution Modes

Each phase has an execution mode (from the index table's `Execution Mode` column):

| Mode | How It Runs | When To Use |
|------|-------------|-------------|
| `claude` (default) | Spawns Claude Code CLI as subprocess | AI-driven task execution |
| `python` | Runs task commands via `subprocess.run()` | Linting, tests, scripts — no AI needed |
| `skip` | Records SKIPPED, no execution | Disabled/deferred phases |

**Ordering**: Python-mode phases run first (preflight), then the main loop processes `claude` and `skip` phases in order.

---

## 10. Preflight Executor (Python Mode)

**File**: `preflight.py` — `execute_preflight_phases()`

Runs **before** the main orchestration loop. Filters `config.active_phases` to those with `execution_mode == "python"`, then for each:

### 10.1 Per-Task Execution

For each task in the phase:
1. **Parse command**: `shlex.split(task.command)` — the `**Command:**` field from the tasklist
2. **Run subprocess**: `subprocess.run(cmd, capture_output=True, timeout=120, cwd=config.work_dir)`
3. **Classify result**: If `task.classifier` is set, calls `run_classifier(classifier_name, exit_code, stdout, stderr)`. If classifier is unknown, falls back to `exit_code == 0 → pass`
4. **Write evidence artifact**: Creates `results/preflight-artifacts/<task_id>/evidence.md` containing:
   - Command executed
   - Exit code, duration, classification
   - Truncated stdout (10KB max) and stderr (2KB max)

### 10.2 Result File

After all tasks, builds an `AggregatedPhaseReport` and writes it to `results/phase-N-result.md` with `source: preflight` injected into YAML frontmatter.

### 10.3 Phase Status

- All tasks passed → `PhaseStatus.PREFLIGHT_PASS`
- Any task failed → `PhaseStatus.HALT`

### 10.4 Classifiers

**File**: `classifiers.py`

Maintains a `CLASSIFIERS` registry dict mapping name → callable. Currently only `empirical_gate_v1` is registered:

```python
def empirical_gate_v1(exit_code, stdout, stderr) -> str:
    return "pass" if exit_code == 0 else "fail"
```

---

## 11. Per-Task Delegation Path

**File**: `executor.py` — `execute_phase_tasks()` (lines 912–1050)

This path is taken when a phase file contains structured `### T<PP>.<TT>` headings. Each task becomes its own subprocess.

### 11.1 The Per-Task Loop

```python
for i, task in enumerate(tasks):
    # 1. Budget guard: can_launch()?
    #    If not → mark this + all remaining as SKIPPED, break
    # 2. Debit minimum_allocation (5 turns) upfront
    # 3. Update TUI with task about to launch
    # 4. Spawn subprocess (_run_task_subprocess or _subprocess_factory)
    # 5. Determine task status from exit code:
    #      0   → PASS
    #      124 → INCOMPLETE
    #      else → FAIL
    # 6. Reconcile budget:
    #      actual = max(turns_consumed, 0)
    #      if actual > pre_allocated: debit(actual - pre_allocated)
    #      if actual < pre_allocated: credit(pre_allocated - actual)
    # 7. Run post-task wiring hook
    # 8. Run post-task anti-instinct hook
    # 9. Update TUI with task completion
```

### 11.2 Budget Guard Detail

`check_budget_guard()` (`executor.py:340`):

```python
def check_budget_guard(ledger):
    if ledger.can_launch():   # available() >= minimum_allocation (5)
        return None            # OK to launch
    return f"Budget exhausted: {ledger.available()} turns remaining, minimum {ledger.minimum_allocation} required"
```

When budget is exhausted, all remaining tasks are marked `SKIPPED` and their IDs are collected in `remaining_task_ids`.

### 11.3 Task Subprocess

`_run_task_subprocess()` (`executor.py:1053–1092`):

```python
def _run_task_subprocess(task, config, phase):
    prompt = f"Execute task {task.task_id}: {task.title}\n..."
    proc = ClaudeProcess.__new__(ClaudeProcess)
    # ... manual init to avoid build_prompt() ...
    proc.start()
    proc.wait()
    exit_code = proc._process.returncode
    output_bytes = output_path.stat().st_size
    return (exit_code, 0, output_bytes)  # turns_consumed hardcoded to 0
```

**Critical**: `turns_consumed` is **hardcoded to 0** (line 1092). The budget system tracks turns but never gets actual consumption data. See [Section 28](#28-known-design-gaps).

### 11.4 Return Value

Returns `(results: list[TaskResult], remaining_task_ids: list[str], gate_results: list[TrailingGateResult])`.

### 11.5 Phase Result Construction

Back in the main loop (`executor.py:1215–1233`), after `execute_phase_tasks()` returns:

```python
all_passed = all(r.status == TaskStatus.PASS for r in task_results)
status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR
phase_result = PhaseResult(phase=phase, status=status, ...)
phase_result = run_post_phase_wiring_hook(phase, config, phase_result, ...)
sprint_result.phase_results.append(phase_result)
continue  # ← DOES NOT halt the sprint
```

**Critical behavioral note**: This path uses `continue` — per-task failures **never** halt the sprint. See [Section 27](#27-critical-behavioral-asymmetry).

---

## 12. Whole-Phase Execution Path

**File**: `executor.py` — lines 1235–1489

This path is taken when a phase file has no structured task headings. The entire file is sent as a single prompt.

### 12.1 Setup

```python
# Create per-phase isolation directory
isolation_dir = config.results_dir / ".isolation" / f"phase-{phase.number}"
isolation_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(phase.file, isolation_dir / phase.file.name)

# Reset monitor for this phase
output_path = config.output_file(phase)
monitor.reset(output_path)
monitor.start()

# Update tmux tail pane if running in tmux
if config.tmux_session_name:
    update_tail_pane(config.tmux_session_name, output_path)

# Launch ClaudeProcess with isolation
proc_manager = ClaudeProcess(config, phase, env_vars={
    "CLAUDE_WORK_DIR": str(isolation_dir),
})
proc_manager.start()
```

### 12.2 Poll Loop

```python
deadline = time.monotonic() + proc_manager.timeout_seconds
while proc_manager._process.poll() is None:
    if signal_handler.shutdown_requested:
        proc_manager.terminate(); break
    if time.monotonic() > deadline:
        _timed_out = True; proc_manager.terminate(); break

    ms = monitor.state

    # Watchdog: stall timeout check
    if (config.stall_timeout > 0
        and ms.stall_seconds > config.stall_timeout
        and ms.events_received > 0
        and not _stall_acted):
        _stall_acted = True
        if config.stall_action == "kill":
            _timed_out = True; proc_manager.terminate(); break
        else:
            # warn action: log and continue

    # Reset watchdog when output resumes
    if _stall_acted and ms.stall_seconds == 0.0:
        _stall_acted = False

    tui.update(sprint_result, monitor.state, phase)
    time.sleep(0.5)  # ~2 Hz TUI update
```

Key details:
- **Timeout enforcement** uses `time.monotonic()` (immune to NTP adjustments)
- **Stall watchdog** is a **single-fire guard** — triggers once, then resets when output resumes
- **TUI errors** are caught and logged, never abort the sprint
- **Poll interval**: 0.5s

### 12.3 Exit Code Determination

```python
raw_rc = proc_manager._process.returncode
if _timed_out:
    exit_code = 124  # timeout convention
else:
    exit_code = raw_rc if raw_rc is not None else -1
```

### 12.4 Preliminary Result Sentinel

For phases that exit 0, `_write_preliminary_result()` (`executor.py:1652`) writes a minimal `EXIT_RECOMMENDATION: CONTINUE\n` sentinel file before `_determine_phase_status()` runs. This ensures phases that produce no agent result file still get classified as `PASS` rather than `PASS_NO_REPORT`.

**Freshness guard**: If a non-empty result file already exists with `st_mtime >= started_at`, the sentinel is not written — the agent-written file is preserved.

### 12.5 Post-Subprocess Processing

```python
# 1. Determine phase status
status = _determine_phase_status(exit_code, result_file, output_file, ...)

# 2. Write executor result file (overwrites agent file — executor is authoritative)
_write_executor_result_file(config, phase, status, exit_code, monitor_state, ...)

# 3. Build PhaseResult
phase_result = PhaseResult(phase, status, exit_code, ...)

# 4. Run post-phase wiring hook
phase_result = run_post_phase_wiring_hook(phase, config, phase_result, ...)

# 5. Record, log, notify
sprint_result.phase_results.append(phase_result)
logger.write_phase_result(phase_result)
notify_phase_complete(phase_result)
tui.update(sprint_result, monitor.state, None)

# 6. Failure handling: HALT and break
if status.is_failure:
    # Collect diagnostics
    collector = DiagnosticCollector(config)
    bundle = collector.collect(phase, phase_result, monitor.state)
    bundle.category = FailureClassifier().classify(bundle)
    ReportGenerator().write(bundle, results_dir / f"phase-{phase.number}-diagnostic.md")

    sprint_result.outcome = SprintOutcome.HALTED
    sprint_result.halt_phase = phase.number
    break  # ← HALTS the sprint
```

### 12.6 Cleanup

The isolation directory is cleaned up in a `finally` block:

```python
finally:
    shutil.rmtree(isolation_dir, ignore_errors=True)
```

---

## 13. Subprocess Construction & Isolation

### 13.1 ClaudeProcess

**File**: `process.py`

`ClaudeProcess` extends `pipeline.process.ClaudeProcess` with sprint-specific behavior:

```python
class ClaudeProcess(_PipelineClaudeProcess):
    def __init__(self, config, phase, *, env_vars=None):
        prompt = self.build_prompt()
        super().__init__(
            prompt=prompt,
            output_file=config.output_file(phase),
            error_file=config.error_file(phase),
            max_turns=config.max_turns,
            model=config.model,
            permission_flag=config.permission_flag,
            timeout_seconds=config.max_turns * 120 + 300,
            output_format="stream-json",
            on_spawn=_make_spawn_hook(phase, config),
            on_signal=_make_signal_hook(phase, config),
            on_exit=_make_exit_hook(phase, config),
            env_vars=env_vars,
        )
```

**Timeout formula**: `max_turns × 120 + 300` seconds. For 100 turns: 12,300s (~3.4 hours).

**Output format**: Always `stream-json` — produces NDJSON for the monitor to parse.

**Lifecycle hooks**: Three factory closures (`_make_spawn_hook`, `_make_signal_hook`, `_make_exit_hook`) inject sprint debug logging without method overrides.

### 13.2 4-Layer Subprocess Isolation

**File**: `executor.py` — `IsolationLayers` dataclass (line 108) + `setup_isolation()` (line 152)

Each subprocess runs with environment-variable-based isolation:

| Layer | Env Var | Value | Purpose |
|-------|---------|-------|--------|
| 1. Scoped work dir | `CLAUDE_WORK_DIR` | Isolation dir or release dir | Restrict filesystem scope |
| 2. Git boundary | `GIT_CEILING_DIRECTORIES` | Release dir | Prevent upward git traversal |
| 3. Empty plugin dir | `CLAUDE_PLUGIN_DIR` | Empty tempdir | No plugins loaded |
| 4. Restricted settings | `CLAUDE_SETTINGS_DIR` | Isolated tempdir | Per-subprocess settings |

Isolation directories live at `results/.isolation/` and are cleaned up per-phase.

**Note**: The whole-phase path only uses layer 1 (`CLAUDE_WORK_DIR`) directly via env_vars. The full 4-layer `setup_isolation()` creates the directories but the whole-phase path passes only the work dir override.

---

## 14. Prompt Construction & Context Injection

**File**: `process.py` — `ClaudeProcess.build_prompt()` (line 123)

The prompt sent to each ClaudeProcess is structured:

```
/sc:task-unified Execute all tasks in @<phase_file> --compliance strict --strategy systematic

## Sprint Context
- Sprint: <release_name>
- Phase: N of M
- Artifact root: <release_dir>/artifacts
- Results directory: <release_dir>/results
- Prior-phase artifact directories: ...
- Prior-phase directories: ...
- All task details are in the phase file. Do not seek additional index files.

## Execution Rules
- Execute tasks in order (T01XX.01, T01XX.02, etc.)
- For STRICT tier tasks: use Sequential MCP for analysis, run quality verification
- For STANDARD tier tasks: run direct test execution per acceptance criteria
- For LIGHT tier tasks: quick sanity check only
- For EXEMPT tier tasks: skip formal verification
- If a STRICT-tier task fails, STOP and report — do not continue to next task
- For all other tier failures, log the failure and continue

## Scope Boundary
- After completing all tasks, STOP immediately.
- Do not read, open, or act on any subsequent phase file.

## Result File
- Write to: <results_dir>/phase-N-result.md
- Content: EXIT_RECOMMENDATION: CONTINUE (or HALT on failure)
```

### Context Injection for Task Chains

**File**: `process.py` — `build_task_context()` (line 245)

When executing a sequence of tasks, each subprocess receives context about prior task results:

```python
def build_task_context(prior_results, *, start_commit="", compress_threshold=3):
    # Older tasks → one-line compressed summary
    # Recent tasks (last 3) → full detail
    # Gate outcomes summary
    # Remediation history (reimbursement amounts)
    # Git diff context (if start_commit provided)
```

**Progressive summarization**: When `len(prior_results) > compress_threshold`, older tasks get compressed to `- **T01.01**: pass | gate: pass` while recent tasks retain full multi-line detail. This bounds context growth for long sprints.

---

## 15. Budget System (TurnLedger)

**File**: `models.py` — `TurnLedger` dataclass (line 547)

The TurnLedger is the economic model for subprocess turn budget tracking.

### 15.1 Initialization

```python
ledger = TurnLedger(
    initial_budget = config.max_turns * len(config.active_phases),
    reimbursement_rate = 0.8,
)
```

**Example**: 100 max_turns × 6 phases = 600 initial budget.

### 15.2 Core API

| Method | Formula / Behavior |
|---|---|
| `available()` | `initial_budget - consumed + reimbursed` |
| `debit(turns)` | `consumed += turns` (enforces non-negative) |
| `credit(turns)` | `reimbursed += turns` (enforces non-negative) |
| `can_launch()` | `available() >= minimum_allocation` (5) |
| `can_remediate()` | `available() >= minimum_remediation_budget` (3) |

### 15.3 Budget Transaction Timeline

For each task in the per-task path:

```
Step 1: Budget guard → can_launch()? (available >= 5)
   NO  → all remaining tasks SKIPPED, loop breaks
   YES ↓

Step 2: Pre-debit → debit(minimum_allocation)  [debit 5]
   consumed += 5

Step 3: Execute subprocess → returns (exit_code, turns_consumed, output_bytes)
   NOTE: turns_consumed is always 0 (hardcoded)

Step 4: Reconcile budget
   actual = max(turns_consumed, 0)  → always 0
   pre_allocated = 5
   Since actual(0) < pre_allocated(5):
     credit(5 - 0) = credit(5)  → reimbursed += 5
   NET EFFECT: consumed=5, reimbursed=5 → net drain = 0

Step 5: Wiring hook (if mode != "off")
   debit_wiring(1)  → consumed += 1, wiring_turns_used += 1
   If non-blocking: credit_wiring(1, 0.8) → int(1*0.8) = 0 credits
   NET EFFECT: net drain from wiring = 1 turn/task

Step 6: Anti-instinct hook (if mode is soft/full)
   On PASS: credit(int(turns_consumed * 0.8)) = credit(int(0 * 0.8)) = credit(0)
   On FAIL: no credit, possibly debit(remediation_cost=2)
   NET EFFECT: 0 (on pass), -2 (on fail)
```

**Net budget drain per task** (typical, wiring=soft, anti-instinct=off): **1 turn** (from wiring analysis only).

### 15.4 Wiring-Specific Budget

| Method | Behavior |
|---|---|
| `debit_wiring(turns)` | Calls `debit(turns)`, increments `wiring_turns_used`, increments `wiring_analyses_count`. Sets `wiring_budget_exhausted = 1` if `available() < minimum_remediation_budget` |
| `credit_wiring(turns, rate)` | Returns `int(turns * rate)`. For `credit_wiring(1, 0.8)` → `int(0.8)` = **0** (floor). Intentional per R7. |
| `can_run_wiring_gate()` | Returns `False` if `wiring_budget_exhausted` (sticky flag, never cleared), otherwise checks `available() >= 3` |

### 15.5 Anti-Instinct Reimbursement

In the anti-instinct hook (`executor.py:860-874`), on PASS:

```python
credit_amount = int(task_result.turns_consumed * ledger.reimbursement_rate)
ledger.credit(credit_amount)
```

Since `turns_consumed` is always 0: `int(0 * 0.8) = 0`. **No reimbursement ever occurs.**

### 15.6 Exhaustion Scenarios

**Budget exhaustion via wiring analysis**: With 600 initial budget and 1 turn/task wiring cost, budget exhaustion would occur at ~595 tasks (allowing for the 5-turn minimum allocation). Practically unreachable for normal sprint sizes.

**`wiring_budget_exhausted` flag**: This is a **sticky one-way flag** — once set to 1, it is never cleared back to 0, even if budget is later credited above the threshold. All subsequent wiring analyses are skipped.

---

## 16. Wiring Integrity Gate

**File**: `executor.py` — `run_post_task_wiring_hook()` (line 450)

### 16.1 Overview

The wiring gate runs **static analysis** on the codebase after each task/phase to detect structural integrity issues. It uses three analyzers from `cli/audit/wiring_gate.py`:

| Analyzer | Code | What It Detects |
|---|---|---|
| G-001: Unwired Callables | `analyze_unwired_callables()` | `Optional[Callable]` parameters that no call site ever provides a value for |
| G-002: Orphan Modules | `analyze_orphan_modules()` | Python files in provider directories (`providers/`, `handlers/`, `strategies/`) with zero inbound imports |
| G-003: Unwired Registries | `analyze_registries()` | Dict/list entries referencing callables that don't exist (broken dispatch tables) |

Findings have two severity levels:
- **critical**: Definite wiring failure (e.g., G-001 with no call sites found at all)
- **major**: Likely wiring gap (e.g., G-002 module present but unreachable)
- **info**: Informational (suppressed entries, edge cases)

### 16.2 Mode Behavior Matrix

| Mode | Analysis Runs? | Findings Logged? | Status Changed? | Budget Debited? | Remediation? |
|------|---------------|-----------------|-----------------|----------------|--------------|
| `off` | No | N/A | No | No | No |
| `shadow` | Yes | Yes (to DeferredRemediationLog) | No | Yes (then fully credited back) | No |
| `soft` | Yes | Yes | No (warning only) | Yes (then fully credited back) | No |
| `full` | Yes | Yes | Yes (FAIL on blocking) | Yes (credited back if non-blocking) | Yes (debit+recheck) |

### 16.3 Detailed Flow (full mode)

```
1. Check can_run_wiring_gate() → budget guard
2. debit_wiring(1) → consume 1 turn
3. Run wiring analysis on release_dir
4. Count blocking findings (critical + major for full mode)
5. If blocking > 0:
   a. Set task_result.status = FAIL, gate_outcome = FAIL
   b. Check can_remediate() (available >= 3)
   c. If can remediate:
      - Format remediation prompt
      - debit(remediation_cost=2)
      - Re-run wiring analysis (_recheck_wiring)
      - If recheck passes: PASS + credit_wiring(1)
      - If recheck fails: FAIL persists
   d. If cannot remediate: BUDGET_EXHAUSTED logged
6. If blocking == 0:
   - credit_wiring(1, 0.8) → 0 credits (floor)
```

### 16.4 Pre-Activation Safeguards

`run_wiring_safeguard_checks()` (`executor.py:356`) runs three checks before the first wiring analysis:

1. **Zero-match warning**: >50 files scanned but 0 findings → suspicious configuration
2. **Whitelist validation**: Parses `wiring_whitelist.yaml`, warns on malformed YAML
3. **Provider directory check**: Verifies configured `provider_dir_names` exist under release dir

Safeguards produce **warnings only** — they never block sprint execution.

### 16.5 Phase-Level Adapter

`run_post_phase_wiring_hook()` (`executor.py:735`) creates a synthetic `TaskEntry` and delegates to the per-task hook, avoiding code duplication:

```python
synthetic_task = TaskEntry(
    task_id=f"phase-{phase.number}",
    title=phase.file.name,
)
# ... map PhaseResult status to TaskStatus ...
updated_result = run_post_task_wiring_hook(synthetic_task, config, synthetic_result, ...)
# ... if wiring changed status to FAIL → set PhaseResult.status = HALT
```

---

## 17. Anti-Instinct Gate

**File**: `executor.py` — `run_post_task_anti_instinct_hook()` (line 787)

The anti-instinct gate evaluates whether a task's output meets quality criteria defined in `ANTI_INSTINCT_GATE` (`cli/roadmap/gates.py`). Unlike wiring analysis, it checks the **output artifact** rather than the codebase structure.

### 17.1 What It Checks

The `ANTI_INSTINCT_GATE` requires three frontmatter fields in the output artifact:

| Check | Field | Passing Condition |
|---|---|---|
| No undischarged obligations | `undischarged_obligations` | Must equal 0 |
| Integration contracts covered | `uncovered_contracts` | Must equal 0 |
| Fingerprint coverage | `fingerprint_coverage` | Must be ≥ 0.7 (70%) |

These fields come from three deterministic modules (no LLM):

1. **Obligation Scanner** (`roadmap/obligation_scanner.py`): Scans for 11 scaffold terms (mock, stub, skeleton, placeholder, etc.) and checks if corresponding discharge terms exist nearby. Per-line exemptions via `# obligation-exempt`.

2. **Integration Contract Checker** (`roadmap/integration_contracts.py`): 7-category dispatch pattern scanner detecting dict dispatch, plugin registries, callback injection, strategy patterns, middleware chains, event systems, and factories.

3. **Fingerprint Coverage** (`roadmap/fingerprint.py`): Extracts backtick identifiers, code block definitions, and ALL_CAPS constants from the spec, then checks what fraction appear in the roadmap text.

### 17.2 Mode Behavior Matrix

| Mode | Gate Evaluated? | Metrics Recorded? | Credit on PASS? | Status Changed on FAIL? |
|------|----------------|-------------------|-----------------|------------------------|
| `off` | No (returns immediately) | No | No | No |
| `shadow` | Yes | Yes (ShadowGateMetrics) | No | No |
| `soft` | Yes | Yes | Yes (via credit) | No (warn only) |
| `full` | Yes | Yes | Yes (via credit) | Yes (TaskStatus.FAIL) |

### 17.3 Detailed Flow (soft/full mode)

```
1. Evaluate gate on output artifact path
2. Record pass/fail + latency in ShadowGateMetrics
3. Build TrailingGateResult
4. If PASS:
   credit_amount = int(turns_consumed * 0.8)  → always 0 (turns_consumed=0)
   ledger.credit(credit_amount)               → credit(0) = no-op
   task_result.gate_outcome = PASS
5. If FAIL:
   Check can_remediate() (available >= 3)
   If cannot: BUDGET_EXHAUSTED + gate_outcome=FAIL
   If can: gate_outcome=FAIL
   If full mode: task_result.status = FAIL
```

### 17.4 ShadowGateMetrics

**File**: `models.py`

Accumulates metrics across all gate evaluations during a sprint:

```python
@dataclass
class ShadowGateMetrics:
    evaluations: int = 0
    passes: int = 0
    failures: int = 0
    latency_ms: list[float]

    def record(self, passed, evaluation_ms):
        self.evaluations += 1
        if passed: self.passes += 1
        else: self.failures += 1
        self.latency_ms.append(evaluation_ms)

    @property
    def pass_rate(self) -> float: ...
    @property
    def p50(self) -> float: ...
    @property
    def p95(self) -> float: ...
```

---

## 18. Output Monitoring (Sidecar Thread)

**File**: `monitor.py` — `OutputMonitor` class (line 144)

A daemon thread that watches the subprocess output file at 0.5s intervals.

### 18.1 Architecture

```
ClaudeProcess → writes NDJSON to output file
    ↓
OutputMonitor thread (0.5s poll)
    → reads incremental bytes
    → splits into lines
    → parses JSON
    → extracts signals
    → updates MonitorState
    ↓
TUI reads MonitorState
```

### 18.2 Incremental Reading

The monitor tracks `_last_read_pos` and reads only new bytes each poll:

```python
def _read_new_chunk(self, current_size):
    with open(self.output_path) as f:
        f.seek(self._last_read_pos)
        chunk = f.read(current_size - self._last_read_pos)
        self._last_read_pos = current_size
        return chunk
```

### 18.3 Line Buffering

Partial lines are buffered across poll cycles via `_line_buffer`. The buffer is prepended to the next chunk and split on `\n`. The last element (possibly partial) is stored back in the buffer.

### 18.4 Signal Extraction

From NDJSON events:
- **Tool use**: `event.get("tool", "")` from `type: "tool_use"` events
- **Task IDs**: Regex `T\d{2}\.\d{2}` (takes last match)
- **Tool names**: Regex `\b(Read|Edit|MultiEdit|Write|Grep|Glob|Bash|TodoWrite|TodoRead|Task)\b`
- **Files changed**: Regex `(?:modified|created|edited|wrote|updated)\s+[`'"]?([^\s`'"]+\.\w+)`

### 18.5 Stall Detection

`MonitorState.stall_status` property (`models.py:522`):

| Condition | Status |
|---|---|
| No events yet, < 120s since phase start | `"waiting..."` |
| No events yet, > 120s since phase start | `"STALLED"` |
| Events received, < 30s since last event | `"active"` |
| Events received, 30–120s since last event | `"thinking..."` |
| Events received, > 120s since last event | `"STALLED"` |

### 18.6 Growth Rate Tracking

Exponential moving average of byte growth:

```python
delta = output_bytes - output_bytes_prev
alpha = 0.3
growth_rate_bps = alpha * (delta / poll_interval) + (1 - alpha) * growth_rate_bps
```

### 18.7 Standalone Detection Functions

| Function | Pattern | Used For |
|---|---|---|
| `detect_error_max_turns(path)` | `"subtype":"error_max_turns"` in last line | Budget exhaustion in subprocess |
| `detect_prompt_too_long(path, error_path)` | `"Prompt is too long"` in last 10 lines | Context window exhaustion |
| `count_turns_from_output(path)` | Counts `"type":"assistant"` lines | Turn consumption counting |

---

## 19. Phase Status Determination

**File**: `executor.py` — `_determine_phase_status()` (line 1765)

After a whole-phase subprocess completes, the runner classifies its outcome through a priority chain:

```
Priority 1: exit_code == 124?
  → TIMEOUT

Priority 2: exit_code != 0?
  2a. Prompt too long? (detect_prompt_too_long)
    → Check for agent result file (_classify_from_result_file)
      → Found: return that status
      → Not found: INCOMPLETE (context exhausted without completing)
  2b. Checkpoint inference? (_check_checkpoint_pass)
    → CP-P<NN>-END.md exists with "STATUS: PASS"?
      → Check contamination (_check_contamination: next-phase task IDs in artifacts?)
      → Not contaminated: PASS_RECOVERED
      → Contaminated: fall through
  2c. Default: ERROR

Priority 3: exit_code == 0 AND result_file exists?
  3a. Has "EXIT_RECOMMENDATION: HALT"? → HALT (wins over CONTINUE if both present)
  3b. Has "EXIT_RECOMMENDATION: CONTINUE"? → PASS
  3c. Has "status: PASS"? → PASS
  3d. Has "status: FAIL/FAILED/FAILURE"? → HALT
  3e. Has "status: PARTIAL"? → HALT
  3f. None of above? → PASS_NO_SIGNAL

Priority 4: exit_code == 0, no result_file?
  4a. Output file exists and non-empty?
    → detect_error_max_turns? → INCOMPLETE (budget exhaustion with exit 0)
    → Else: PASS_NO_REPORT
  4b. No output: ERROR
```

### All 10 PhaseStatus Values

| Status | Category | Meaning |
|---|---|---|
| `PASS` | success | Clean pass with `EXIT_RECOMMENDATION: CONTINUE` |
| `PASS_NO_SIGNAL` | success | Exit 0, result file exists, but no EXIT_RECOMMENDATION or status pattern |
| `PASS_NO_REPORT` | success | Exit 0, output exists, but no result file |
| `PASS_RECOVERED` | success | Non-zero exit but checkpoint evidence proves success |
| `PREFLIGHT_PASS` | success | Python-mode phase completed via preflight |
| `INCOMPLETE` | failure | Timeout (124), context exhaustion, or budget exhaustion detected |
| `HALT` | failure | Agent reported HALT or FAIL/FAILURE status |
| `TIMEOUT` | failure | Process exceeded deadline |
| `ERROR` | failure | Non-zero exit with no recovery evidence |
| `SKIPPED` | non-terminal | Skip-mode phase or budget exhaustion |

### Crash Recovery via Checkpoints

`_check_checkpoint_pass()` (`executor.py:1592`): Reads `checkpoints/CP-P<NN>-END.md` for `STATUS: PASS`. If found, `_check_contamination()` scans `artifacts/` for next-phase task ID patterns — if clean, the phase is reclassified `ERROR → PASS_RECOVERED` and a crash recovery log entry is written.

---

## 20. TUI Dashboard

**File**: `tui.py` — `SprintTUI` class

A Rich `Live` display showing:

- **Phase table**: Phase number, name, status (color-coded), duration, gate state
- **Active phase panel**: Current task ID, tool in use, output size, stall status
- **Progress bar**: Across all phases
- **Gate column**: When trailing gates are enabled

### Status Rendering

| Status | Color | Icon |
|---|---|---|
| PASS / PASS_* | green | ✓ |
| RUNNING | yellow | ▶ |
| HALT | red | ✗ |
| ERROR | red | ✗ |
| TIMEOUT | red | ⏱ |
| INCOMPLETE | yellow | ◐ |
| PREFLIGHT_PASS | cyan | ⚡ |
| SKIPPED | dim | — |
| PENDING | dim | · |

### Gate Display States

7 states with a formal transition FSM (`models.py:107`):

```
NONE → CHECKING → PASS
NONE → CHECKING → FAIL_DEFERRED → REMEDIATING → REMEDIATED
NONE → CHECKING → FAIL_DEFERRED → REMEDIATING → HALT
```

| State | Icon | Color |
|---|---|---|
| NONE | — | dim |
| CHECKING | ⏳ | cyan |
| PASS | ✓ | green |
| FAIL_DEFERRED | ⚠ | yellow |
| REMEDIATING | 🔧 | magenta |
| REMEDIATED | ✓✓ | green |
| HALT | ✗ | red |

---

## 21. Logging & Diagnostics

### 21.1 Dual-Format Execution Logs

**File**: `logging_.py` — `SprintLogger`

- **JSONL** (`execution-log.jsonl`): Machine-readable, every event with timestamps
- **Markdown** (`execution-log.md`): Human-readable, phase-level summary table

Four log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`.

### 21.2 Diagnostic Bundles

**File**: `diagnostics.py`

On failure, a `DiagnosticBundle` is collected:

```python
@dataclass
class DiagnosticBundle:
    phase: Phase
    phase_result: PhaseResult
    category: FailureCategory       # assigned by FailureClassifier
    debug_log_entries: list[str]     # phase-specific debug log lines
    last_events: list[str]           # last 20 debug entries
    output_tail: str                 # last 10 lines of output
    stderr_tail: str                 # last 10 lines of stderr
    monitor_state_snapshot: dict     # output_bytes, events_received, stall_seconds, etc.
    watchdog_triggered: bool
    stall_duration: float
    classification_evidence: list[str]
```

### 21.3 Failure Classification

`FailureClassifier.classify()` uses priority-ordered evidence:

| Priority | Condition | Category |
|---|---|---|
| 1 | Watchdog triggered | `STALL` |
| 2 | Stall duration > 120s | `STALL` |
| 3 | Exit code 124 | `TIMEOUT` |
| 4 | `detect_prompt_too_long()` returns True | `CONTEXT_EXHAUSTION` |
| 5 | Non-zero exit + low stall (< 30s) | `CRASH` |
| 6 | Status is HALT or ERROR | `ERROR` |
| 7 | None of above | `UNKNOWN` |

### 21.4 Diagnostic Report

`ReportGenerator.write()` produces a structured markdown report at `results/phase-N-diagnostic.md` containing:
- Summary (category, status, exit code, duration, stall duration, watchdog status)
- Evidence list
- Monitor state snapshot
- Last 10 debug events
- Output tail (10 lines)
- Stderr tail (10 lines)

---

## 22. KPI Report

**File**: `kpi.py` — `GateKPIReport`, `build_kpi_report()`

Generated at sprint completion and written to `results/gate-kpi-report.md`.

### Metrics Collected

| Category | Metrics |
|---|---|
| Gate Evaluation | Total evaluated, passed, failed, pass rate, latency p50/p95 |
| Remediation | Total, resolved, pending, frequency |
| Conflict Review | Reviews, conflicts found, conflict rate |
| Wiring Gate | Findings total, by type, turns used/credited, net cost, analyses run, remediations attempted, whitelist entries applied, files skipped |

### Source Data

```python
def build_kpi_report(
    gate_results: list[TrailingGateResult],        # from anti-instinct evaluations
    remediation_log: DeferredRemediationLog,       # persisted gate failures
    turn_ledger: TurnLedger,                       # wiring budget data
    wiring_report: WiringReport | None = None,     # last wiring analysis
):
```

---

## 23. Sprint Finalization & Cleanup

**File**: `executor.py` — lines 1491–1553

### 23.1 Result Merging (line 1491)

Preflight results and main-loop results are merged by phase number. Main-loop results take precedence on conflict:

```python
_merged = {r.phase.number: r for r in preflight_results}
for r in sprint_result.phase_results:
    _merged[r.phase.number] = r  # main-loop wins
sprint_result.phase_results = [
    _merged[p.number] for p in config.active_phases if p.number in _merged
]
```

### 23.2 Outcome Verification (line 1502)

If outcome is still `SUCCESS` but not all phases passed → override to `ERROR`:

```python
if sprint_result.outcome == SprintOutcome.SUCCESS:
    if not all(r.status.is_success for r in sprint_result.phase_results):
        sprint_result.outcome = SprintOutcome.ERROR
```

### 23.3 KPI Report (line 1510)

```python
kpi_report = build_kpi_report(
    gate_results=all_gate_results,
    remediation_log=remediation_log,
    turn_ledger=ledger,
)
kpi_path = config.results_dir / "gate-kpi-report.md"
kpi_path.write_text(kpi_report.format_report())
```

### 23.4 Cleanup (line 1523)

In a `finally` block, each cleanup step is independent (one failure doesn't block others):

```python
finally:
    monitor.stop()
    proc_manager.terminate() if proc_manager is not None
    tui.stop()
    signal_handler.uninstall()
```

### 23.5 Exit Sentinel (line 1544)

Writes `.sprint-exitcode` to the release directory so the tmux caller can read the outcome:

```python
_exitcode = 0 if sprint_result.outcome == SprintOutcome.SUCCESS else 1
(config.release_dir / ".sprint-exitcode").write_text(str(_exitcode))
```

If exit code is non-zero, raises `SystemExit(_exitcode)`.

---

## 24. Results Directory Layout

```
results/
  phase-1-output.txt              # Raw subprocess NDJSON output
  phase-1-errors.txt              # Subprocess stderr
  phase-1-result.md               # Phase result (YAML frontmatter + markdown)
  phase-1-diagnostic.md           # Diagnostic report (on failure only)
  phase-2-output.txt
  phase-2-errors.txt
  phase-2-result.md
  ...
  debug.log                       # Structured debug log (when --debug enabled)
  remediation.json                # Persisted DeferredRemediationLog
  gate-kpi-report.md              # KPI metrics from gate evaluations
  crash_recovery_log.md           # Crash recovery entries (PASS_RECOVERED phases)
  preflight-artifacts/            # Python-mode evidence files
    T01.01/evidence.md
    T01.02/evidence.md
  .isolation/                     # Temporary subprocess isolation dirs (cleaned up per-phase)

release-dir/
  execution-log.jsonl             # Machine-readable event log
  execution-log.md                # Human-readable sprint summary
  .sprint-exitcode                # Exit code sentinel for tmux
  .roadmap-state.json             # Fidelity state (read-only by sprint)
  checkpoints/
    CP-P01-END.md                 # End-of-phase checkpoint (agent-written)
```

---

## 25. Data Model Reference

**File**: `models.py`

### Enums

| Enum | Values | Key Properties |
|---|---|---|
| `TaskStatus` | PASS, FAIL, INCOMPLETE, SKIPPED | `.is_success`, `.is_failure` |
| `GateOutcome` | PASS, FAIL, DEFERRED, PENDING | `.is_success` |
| `GateDisplayState` | NONE, CHECKING, PASS, FAIL_DEFERRED, REMEDIATING, REMEDIATED, HALT | `.color`, `.icon`, `.label` |
| `PhaseStatus` | 10 values (see Section 19) | `.is_terminal`, `.is_success`, `.is_failure` |
| `SprintOutcome` | SUCCESS, HALTED, INTERRUPTED, ERROR | — |
| `FailureCategory` | STALL, TIMEOUT, CRASH, ERROR, UNKNOWN, CONTEXT_EXHAUSTION | — |

### Dataclasses

| Class | Key Fields |
|---|---|
| `TaskEntry` | task_id, title, description, dependencies, command, classifier |
| `TaskResult` | task, status, turns_consumed, exit_code, gate_outcome, reimbursement_amount, output_path |
| `Phase` | number, file, name, execution_mode |
| `SprintConfig` | (20+ fields — see Section 3) |
| `PhaseResult` | phase, status, exit_code, started_at, finished_at, output_bytes, error_bytes, last_task_id, files_changed |
| `SprintResult` | config, phase_results, outcome, started_at, finished_at, halt_phase |
| `MonitorState` | output_bytes, events_received, last_task_id, last_tool_used, stall_seconds, growth_rate_bps |
| `TurnLedger` | initial_budget, consumed, reimbursed, reimbursement_rate, minimum_allocation, wiring_turns_used, wiring_budget_exhausted |
| `ShadowGateMetrics` | evaluations, passes, failures, latency_ms |
| `AggregatedPhaseReport` | phase_number, tasks_total, tasks_passed, tasks_failed, tasks_skipped, tasks_not_attempted |
| `DiagnosticBundle` | phase, phase_result, category, debug_log_entries, output_tail, stderr_tail, watchdog_triggered |
| `GateKPIReport` | gate counts, remediation counts, wiring metrics, latency percentiles |
| `IsolationLayers` | scoped_work_dir, git_boundary, plugin_dir, settings_dir |

### Helper Functions

| Function | Location | Purpose |
|---|---|---|
| `aggregate_task_results()` | executor.py:298 | Builds `AggregatedPhaseReport` from `TaskResult[]` |
| `check_budget_guard()` | executor.py:340 | Pre-launch budget check |
| `build_resume_output()` | models.py:633 | Builds actionable HALT output with resume command |
| `build_task_context()` | process.py:245 | Context injection for task chains |
| `compress_context_summary()` | process.py:335 | Progressive summarization of older tasks |
| `get_git_diff_context()` | process.py:310 | Git diff --stat context |

---

## 26. Pipeline Inheritance

The sprint module inherits from a shared pipeline framework (`src/superclaude/cli/pipeline/`):

| Sprint Class | Inherits From | Shared Behavior |
|---|---|---|
| `SprintConfig` | `PipelineConfig` | work_dir, dry_run, max_turns, model, permission_flag, debug |
| `PhaseResult` | `StepResult` | timing fields |
| `SprintStep` | `Step` | id, prompt, output_file, gate, timeout_seconds |
| `ClaudeProcess` | `pipeline.process.ClaudeProcess` | start(), wait(), terminate(), NDJSON output |

Shared infrastructure from `pipeline/`:
- `TrailingGatePolicy` — gate enforcement interface
- `TrailingGateResult` — gate evaluation result (step_id, passed, evaluation_ms, failure_reason)
- `DeferredRemediationLog` — persists failed gate results to JSON
- `GateScope`, `GateMode`, `resolve_gate_mode()` — scope-based mode resolution

---

## 27. Critical Behavioral Asymmetry

The two execution paths handle failures **differently**:

### Per-Task Path (line 1233)
```python
# After execute_phase_tasks() returns, even with failures:
sprint_result.phase_results.append(phase_result)
logger.write_phase_result(phase_result)
continue  # ← Always continues to next phase
```

### Whole-Phase Path (line 1484–1486)
```python
if status.is_failure:
    # Collect diagnostics...
    sprint_result.outcome = SprintOutcome.HALTED
    sprint_result.halt_phase = phase.number
    break  # ← Halts the sprint
```

**Consequence**: A structured phase (per-task) that has all tasks fail will produce `PhaseStatus.ERROR` but the sprint continues to the next phase. A freeform phase (whole-phase) that fails will immediately halt the entire sprint and produce diagnostic output.

This is a **design decision**, not a bug — per-task phases report granular task-level results while whole-phase phases have binary outcomes.

---

## 28. Known Design Gaps

### Gap 1: `turns_consumed` Hardcoded to 0

**Location**: `executor.py:1092` — `_run_task_subprocess()`

```python
return (exit_code, 0, output_bytes)  # turns_consumed always 0
```

The second element (turns consumed) is hardcoded to 0. This means:
- Budget reconciliation always credits back the full pre-allocation
- Anti-instinct reimbursement always computes `int(0 * 0.8) = 0`
- The TurnLedger tracks budget flow but never gets real consumption data
- The `count_turns_from_output()` function exists in `monitor.py` but is not called

**Comment in code**: "Turn counting is wired separately in T02.06" — indicates planned future work.

### Gap 2: `credit_wiring(1, 0.8)` Always Returns 0

**Location**: `models.py:620`

```python
def credit_wiring(self, turns, rate=None):
    effective_rate = rate if rate is not None else self.reimbursement_rate  # 0.8
    credit_amount = int(turns * effective_rate)  # int(1 * 0.8) = int(0.8) = 0
```

With default config (`wiring_analysis_turns=1`, `reimbursement_rate=0.8`), the credit is always 0 due to integer floor. This is **intentional** per R7 (documented in code), but means wiring analysis has a one-way cost of 1 turn/task that is never recouped.

### Gap 3: Sticky `wiring_budget_exhausted` Flag

**Location**: `models.py:606`

Once `wiring_budget_exhausted` is set to 1 (when `available() < minimum_remediation_budget` after a wiring debit), it is never cleared. Even if budget is later credited above the threshold, all subsequent wiring analyses are permanently skipped.

### Gap 4: Anti-Instinct Reimbursement Dead Code

**Location**: `executor.py:867-868`

```python
credit_amount = int(task_result.turns_consumed * ledger.reimbursement_rate)
# Since turns_consumed is always 0: int(0 * 0.8) = 0
ledger.credit(credit_amount)  # credit(0) = no-op
```

The anti-instinct PASS reimbursement path exists but never has any effect.

### Gap 5: Per-Task Path Missing Diagnostic Collection

When the per-task path produces failures, no `DiagnosticBundle` is collected. Diagnostic collection only runs in the whole-phase path (lines 1459–1482). Per-task failures are recorded in the `AggregatedPhaseReport` but without the rich evidence collection (output tails, debug log entries, monitor state snapshots, failure classification).

### Gap 6: No Budget Tracking in Whole-Phase Path

The whole-phase execution path (`executor.py:1235-1489`) does not interact with the `TurnLedger` at all — no debit before launch, no reconciliation after completion. Only the per-task path uses the budget system.

### SPEC-DEVIATION Markers in Code

| ID | Location | Description |
|---|---|---|
| BUG-009/P6 | executor.py:878 | Anti-instinct FAIL should call `attempt_remediation()` for retry-once semantics; uses inline fail logic instead |
| BUG-010 | executor.py:864 | Reimbursement should use upstream merge step turns; uses `turns_consumed` (which is 0) instead |

---

## 29. CLI Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `INDEX_PATH` | argument | (required) | Path to tasklist-index.md |
| `--start N` | int | 1 | Start from phase N |
| `--end N` | int | 0 (auto) | End at phase N (0 = last discovered) |
| `--max-turns N` | int | 100 | Max agent turns per phase |
| `--model` | string | "" | Claude model to use |
| `--dry-run` | flag | false | Show phases without executing |
| `--no-tmux` | flag | false | Run in foreground |
| `--permission-flag` | choice | `--dangerously-skip-permissions` | Permission mode for Claude CLI |
| `--tmux-session-name` | string | "" | Internal: passed when relaunched inside tmux |
| `--debug` | flag | false | Enable structured debug logging |
| `--stall-timeout N` | int | 0 | Stall timeout in seconds (0 = disabled) |
| `--stall-action` | choice | `warn` | Action on stall: `warn` or `kill` |
| `--shadow-gates` | flag | false | Shadow mode for trailing gates |
| `--force-fidelity-fail` | string | (none) | Override fidelity block with justification |
| `--release-dir` | path | (auto) | Explicit release directory |
| `--no-tmux-session-name` | internal | "" | Prevents tmux session name propagation |

---

## 30. End-to-End Flow Diagram

```
superclaude sprint run tasklist-index.md --start 1 --end 6 --max-turns 100
    │
    ▼
┌─────────────────────┐
│  commands.py: run() │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
 Fidelity     load_sprint_config()
  Check       ┌─────────────────┐
    │         │ discover_phases()│ → list[Phase]
    │         │ validate_phases()│
    │         │ extract names    │
    │         └────────┬────────┘
    │                  │
    ▼                  ▼
 Pass?             SprintConfig
    │
    ├─ NO → BLOCKED (unless --force-fidelity-fail)
    │
    ▼
  Dry run?
    │
    ├─ YES → print phases, exit
    │
    ▼
  Tmux available?
    │
    ├─ YES (and not --no-tmux) → launch_in_tmux()
    │   │                          ├── tmux new-session
    │   │                          ├── sprint run ... --no-tmux (inside session)
    │   │                          ├── split-window (tail output)
    │   │                          └── attach-session (blocks)
    │   │
    ├─ NO / --no-tmux
    │
    ▼
┌─────────────────────────────┐
│  executor.py: execute_sprint()  │
├─────────────────────────────┤
│ 1. Verify claude binary        │
│ 2. SignalHandler.install()      │
│ 3. Setup: debug logger, logger, │
│    TUI, monitor, sprint_result  │
│ 4. TurnLedger(max_turns × N)   │
│ 5. ShadowGateMetrics           │
│ 6. DeferredRemediationLog      │
│ 7. SprintGatePolicy            │
│ 8. Orphan cleanup              │
│ 9. execute_preflight_phases()  │
│    └── python-mode phases      │
├─────────────────────────────┤
│ MAIN LOOP: for phase in active │
│                                │
│  ┌─ shutdown? → INTERRUPTED   │
│  ├─ python? → skip (preflight)│
│  ├─ skip? → SKIPPED           │
│  ├─ has tasks? ─────────────┐ │
│  │                          │ │
│  │  PER-TASK PATH           │ │
│  │  ┌──────────────────┐    │ │
│  │  │for task in tasks:│    │ │
│  │  │ budget guard     │    │ │
│  │  │ debit(5)         │    │ │
│  │  │ spawn subprocess │    │ │
│  │  │ classify result  │    │ │
│  │  │ reconcile budget │    │ │
│  │  │ wiring hook      │    │ │
│  │  │ anti-instinct    │    │ │
│  │  └──────────────────┘    │ │
│  │  phase result            │ │
│  │  wiring phase hook       │ │
│  │  continue ←──────────────┘ │
│  │                            │
│  └─ no tasks? ──────────────┐ │
│                             │ │
│     WHOLE-PHASE PATH        │ │
│     ┌──────────────────┐    │ │
│     │ isolation dir     │    │ │
│     │ monitor.reset()   │    │ │
│     │ ClaudeProcess()   │    │ │
│     │ poll loop:        │    │ │
│     │   timeout check   │    │ │
│     │   stall watchdog  │    │ │
│     │   TUI update      │    │ │
│     │ status determine  │    │ │
│     │ executor result   │    │ │
│     │ wiring phase hook │    │ │
│     └──────────────────┘    │ │
│     if failure:             │ │
│       diagnostics           │ │
│       HALTED                │ │
│       break ←───────────────┘ │
│                                │
├─────────────────────────────┤
│ POST-LOOP:                     │
│  Merge preflight + main results│
│  Verify outcome                │
│  Build KPI report              │
│  Write execution logs          │
│  Notify sprint complete        │
├─────────────────────────────┤
│ CLEANUP (finally):             │
│  monitor.stop()                │
│  proc_manager.terminate()      │
│  tui.stop()                    │
│  signal_handler.uninstall()    │
│  Write .sprint-exitcode        │
│  SystemExit if non-zero        │
└─────────────────────────────┘
```

---

*Document generated from source code analysis of `src/superclaude/cli/sprint/` with line-number references to the codebase as of the `feat/tdd-spec-merge` branch.*
