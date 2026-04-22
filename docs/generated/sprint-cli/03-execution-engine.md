---
title: Sprint CLI - Execution Engine
generated: 2026-04-03
scope: cli/sprint/executor.py, cli/sprint/process.py, cli/sprint/preflight.py, execution/
---

# Execution Engine

## Core Executor: `execute_sprint()`

**File**: `src/superclaude/cli/sprint/executor.py:1112-1553`

### Initialization Phase (lines 1123-1175)

```
execute_sprint(config: SprintConfig)
  |
  +-> Verify `claude` binary exists in PATH (1123-1128)
  +-> Install SignalHandler (1130-1132)
  +-> Initialize subsystems:
  |     - DebugLogger (1133)
  |     - SprintLogger (1135)
  |     - SprintTUI (1137)
  |     - OutputMonitor (1139)
  |     - TurnLedger (1147-1150)
  |     - ShadowGateMetrics (1152)
  |     - DeferredRemediationLog (1154-1157)
  |     - SprintGatePolicy (1159)
  |
  +-> execute_preflight_phases(config) (1173-1175)
```

### Main Phase Loop (lines 1178-1486)

```python
for phase in config.active_phases:  # line 1178
    if phase.execution_mode == "python":
        # Already handled in preflight (1183-1185)
        continue
    elif phase.execution_mode == "skip":
        # Synthesize SKIPPED PhaseResult (1187-1199)
        continue
    else:
        # Claude-mode execution (see below)
```

### Claude-Mode Path A: Task Inventory (lines 1203-1233)

When phase markdown contains parseable task headings:

```
_parse_phase_tasks(phase) -> TaskEntry[]
  |
  +-> Tasks found?
        |
        YES -> execute_phase_tasks(config, phase, tasks, ...)
        |        |
        |        +-> FOR EACH task (line 956):
        |        |     spawn ClaudeProcess with task-specific prompt
        |        |     monitor NDJSON output stream
        |        |     classify task result (PASS/FAIL/INCOMPLETE)
        |        |     update TurnLedger
        |        |
        |        +-> phase_success = all(task.status == PASS) (1215-1218)
        |        +-> post-phase wiring hook (1223-1227)
        |
        NO  -> Path B (freeform execution)
```

### Claude-Mode Path B: Freeform Phase (lines 1235-1486)

When phase has no task headings, runs as single Claude session:

```
Create isolation dir + copy phase file (1235-1239)
  |
  +-> Start OutputMonitor (1242-1245)
  +-> Spawn ClaudeProcess(config, phase, env_vars=...) (1251-1255)
  |
  +-> Poll loop (1265-1349):
  |     - Update TUI with monitor state
  |     - Check stall timeout (1274-1278)
  |     - Handle stall action (warn/kill) (1297-1323)
  |     - Wait for process exit
  |
  +-> _determine_phase_status(exit_code, ...) (1393-1401)
  +-> _write_executor_result_file(...) (1403-1414)
  +-> On failure: emit diagnostics (1457-1483), halt sprint (1484-1486)
```

### Finalization (lines 1491-1553)

```
Merge preflight + main results (preserving phase order) (1491-1499)
  |
  +-> Compute SprintOutcome (1502-1507)
  +-> build_kpi_report() (1510-1519)
  +-> Cleanup: monitor, process, TUI, signal handler (1524-1542)
  +-> Write .sprint-exitcode (1544-1548)
  +-> sys.exit(1) if failure (1553)
```

## Per-Task Execution: `execute_phase_tasks()`

**File**: `src/superclaude/cli/sprint/executor.py:912`

Iterates tasks in **input order** (line 956). For each task:

1. Build task-specific subprocess via `_run_task_subprocess()` (line 1053)
2. Returns `(exit_code, turns_consumed, output_bytes)` (1091-1092)
3. Classify result into `TaskResult`
4. Update `TurnLedger` with consumption

**Important finding**: Dependencies are parsed into `TaskEntry.dependencies` but are **not used for execution ordering**. Tasks execute in document order.

## Claude Process Spawning

### Base Process (`cli/pipeline/process.py`)

**`build_command()`** (line 71-91) constructs:
```bash
claude --print --verbose \
  [--model <model>] \
  --tools default \
  --max-turns <max_turns> \
  --output-format stream-json \
  [--dangerously-skip-permissions | --allow-hierarchical-permissions] \
  -p "<prompt>"
```

Lifecycle: `start()` (110) -> `wait()` (153) -> `terminate()` (195)

### Sprint Process (`cli/sprint/process.py:88`)

`ClaudeProcess` extends base with:
- Sprint-specific prompt injection (lines 88-121)
- `build_prompt()` (line 123) generates:
  ```
  /sc:task-unified Execute all tasks in @<phase_file> --compliance strict --strategy systematic
  ```
- Includes phase-scope rules and result-file contract (lines 170-204)

## Preflight Execution

**File**: `src/superclaude/cli/sprint/preflight.py:90`

Handles `python`-mode phases before the main loop:

1. Parse task entries from phase markdown (line 116)
2. For each task with `execution_mode == "python"`:
   - Run `subprocess.run(task.command)` directly
   - Capture stdout/stderr
   - Write evidence bundle to `results/preflight-artifacts/<task_id>/evidence.md` (lines 45-73)
3. Aggregate results into `PhaseResult`
4. Write result file with `source: preflight` frontmatter (lines 76-87, 217-221)

## Status Classification

### `_determine_phase_status()` (line 1765)

Decision tree:
```
exit_code == 0?
  YES -> PASS
  |
exit_code == 124?
  YES -> TIMEOUT (1786-1787)
  |
detect_prompt_too_long()?
  YES -> INCOMPLETE (1790-1797)
  |
_check_checkpoint_pass()?
  YES -> contamination_check()?
           clean -> PASS_RECOVERED (1802-1806)
           dirty -> FAIL
  |
_classify_from_result_file()?
  -> parse agent-written result file for status (1555-1590)
  |
DEFAULT -> FAIL
```

### Checkpoint Recovery (lines 1592-1623)

Searches for `checkpoints/CP-P{phase:02d}-END.md` and looks for PASS tokens. If found and contamination check passes, phase is marked `PASS_RECOVERED`.

## Wave-Based Execution Patterns

### Pattern A: Dependency-Wave Batching (`execution/parallel.py`)

**File**: `src/superclaude/execution/parallel.py`

- `ParallelExecutor.plan()` (103-167): Builds dependency-respecting wave groups
- Each wave = all currently-ready tasks (no unmet dependencies)
- Executes via `ThreadPoolExecutor` with `as_completed` (209-217)
- Cycle detection raises `ValueError` (127-130)
- **Not directly wired into sprint executor** (separate subsystem)

### Pattern B: Sprint Phase Checkpoints

- Each phase = one "wave" in the main `execute_sprint` loop
- Checkpoint = `checkpoints/CP-P{N}-END.md` file
- Recovery: non-zero exit + valid checkpoint = `PASS_RECOVERED`

## Error Handling & Recovery

### Timeout Detection
- `exit_code == 124` -> `PhaseStatus.TIMEOUT` (executor.py:1786-1787)

### Context Exhaustion
- `detect_prompt_too_long(output)` in monitor.py:63 -> `INCOMPLETE`

### Stall Detection
- Configurable via `--stall-timeout` and `--stall-action`
- Monitor tracks last activity timestamp
- On stall: warn (TUI update) or kill (process termination)

### Retry Semantics

**Sprint executor**: No task-level or phase-level retry loop exists in `execute_sprint` or `execute_phase_tasks`.

**Pipeline executor** (`pipeline/executor.py`): Generic retry up to `retry_limit + 1` attempts per step (line 192). Gate failures trigger retry; exhausted retries return FAIL.

### Diagnostic Collection
- `DiagnosticCollector` (diagnostics.py:72): Gathers failure evidence
- `FailureClassifier` (diagnostics.py:157): Categorizes failure mode
- `ReportGenerator` (diagnostics.py:235): Writes diagnostic markdown

## Execution Subsystem (`src/superclaude/execution/`)

### Parallel Engine (`parallel.py`)

```python
class ParallelExecutor:
    plan(tasks) -> ExecutionPlan     # Dependency-wave grouping
    execute(plan) -> dict[str, Any]  # ThreadPool execution
```

### Reflection Engine (`reflection.py`)

```python
class ReflectionEngine:
    reflect(context) -> ReflectionResult
    # 3-stage scoring: clarity(0.5) + mistakes(0.3) + context(0.2)
    # Blocks execution if confidence < 0.7
```

### Self-Correction Engine (`self_correction.py`)

```python
class SelfCorrectionEngine:
    detect_failure(error) -> FailureEntry
    analyze_root_cause(entry) -> RootCause
    learn_and_prevent(entry) -> prevention_rules
    # Persists to docs/memory/reflexion.json
```

### Integrator (`__init__.py:41`)

```python
def intelligent_execute(tasks, context):
    # reflection -> parallel planning -> execution -> self-correction
```

**Note**: This execution subsystem is standalone and **not wired into the sprint CLI executor**.
