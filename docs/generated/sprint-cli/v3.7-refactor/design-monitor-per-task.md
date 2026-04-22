# Per-Task OutputMonitor Adaptation for Path A TUI v2

## Design Document

| Field | Value |
|---|---|
| **Author** | Claude (sc:design) |
| **Date** | 2026-04-03 |
| **Status** | DRAFT |
| **Depends on** | chunk-02-sprint-tui-v2.md, chunk-06-path-a-enrichment.md, MERGED-REFACTORING-RECOMMENDATION.md |
| **Target files** | executor.py, monitor.py, models.py, tui.py, config.py |

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Architectural Context](#2-architectural-context)
3. [Strategy A: Per-Task Monitor Lifecycle](#3-strategy-a-per-task-monitor-lifecycle)
4. [Strategy B: Synthetic State Population](#4-strategy-b-synthetic-state-population)
5. [Strategy C: Hybrid (Recommended)](#5-strategy-c-hybrid-recommended)
6. [Comparative Analysis](#6-comparative-analysis)
7. [Recommendation and Migration Path](#7-recommendation-and-migration-path)
8. [Appendix: MonitorState Field Reference](#8-appendix-monitorstate-field-reference)

---

## 1. Problem Statement

The sprint executor has two execution paths that fork at `executor.py:1201-1233`:

- **Path A** (`execute_phase_tasks`): Per-task subprocess loop. One Claude subprocess per task. This is the **production path** — every properly structured tasklist executes here.
- **Path B** (single `ClaudeProcess` via `build_prompt()`): Freeform single subprocess per phase. **Fallback path** for malformed/legacy files.

OutputMonitor is **never started for Path A**. The `monitor.reset()` + `monitor.start()` calls at `executor.py:1242-1244` are inside Path B's branch, after Path A's `continue` at line 1233. This means:

1. **9 of 12 MonitorState fields** remain at defaults under Path A (only `events_received`, `last_event_time`, `last_task_id` are set via ad-hoc writes at `executor.py:978-984` and `1042-1048`).
2. All task subprocesses write to the **same** `phase-N-output.txt` (`executor.py:1078`, opened with `"w"` mode at `process.py:114`), so each task **overwrites** the previous task's NDJSON.
3. The TUI's Active Panel shows **degraded data**: `0 B` output, `+0.0 B/s` growth, `0` files changed, perpetual `"waiting..."` status.
4. The 8 proposed new MonitorState fields (Section 7.1 of v3.7 spec) would all be **dead code** under Path A.

### Design Goal

Make TUI v2 features work for Path A without breaking Path B. Three strategies are analyzed below.

---

## 2. Architectural Context

### Current Data Flow (Path A)

```
execute_sprint()
  │
  ├─ monitor = OutputMonitor(Path("/dev/null"))     # executor.py:1140
  │
  └─ for each phase:
       │
       ├─ tasks = parse_tasklist(phase_file)         # executor.py:1203
       │
       ├─ if tasks:  ─────────── PATH A ───────────
       │   │
       │   ├─ tui.update(result, MonitorState(), phase)   # :1207
       │   │
       │   ├─ execute_phase_tasks(tasks, config, phase, ...)
       │   │   │
       │   │   └─ for each task:
       │   │       │
       │   │       ├─ tui.update(..., ad-hoc MonitorState)  # :978-984
       │   │       │   └─ sets: events_received, last_event_time, last_task_id
       │   │       │
       │   │       ├─ _run_task_subprocess(task, config, phase)
       │   │       │   └─ writes to config.output_file(phase)  # SAME FILE
       │   │       │   └─ returns (exit_code, 0, output_bytes)  # turns=0 ALWAYS
       │   │       │
       │   │       ├─ tui.update(..., ad-hoc MonitorState)  # :1042-1048
       │   │       │
       │   │       └─ run_post_task_anti_instinct_hook(...)
       │   │           └─ output_path="" → vacuous PASS      # BUG PA-05
       │   │
       │   ├─ build PhaseResult from task aggregates  # :1215-1220
       │   │
       │   └─ continue   # :1233 — SKIPS monitor.start()
       │
       └─ else:  ─────────── PATH B (fallback) ───────
           │
           ├─ monitor.reset(output_path)              # :1243
           ├─ monitor.start()                         # :1244
           │   └─ spawns daemon thread → _poll_loop → _poll_once
           │       └─ populates ALL 12 MonitorState fields in real time
           │
           ├─ ClaudeProcess(build_prompt(...))         # full rich prompt
           │
           └─ monitor.stop()                          # :1357
```

### MonitorState Field Status Under Path A

| Field | Default | Path A Status | Set By |
|---|---|---|---|
| `events_received` | `0` | **Partially set** | executor.py:981,1045 (loop index, not real events) |
| `last_event_time` | `monotonic()` | **Partially set** | executor.py:982,1046 (update time, not event time) |
| `last_task_id` | `""` | **Partially set** | executor.py:983,1047 |
| `output_bytes` | `0` | **Dead** | Only monitor.py:204 |
| `output_bytes_prev` | `0` | **Dead** | Only monitor.py:203 |
| `last_growth_time` | `monotonic()` | **Dead** | Only monitor.py:259 |
| `last_tool_used` | `""` | **Dead** | Only monitor.py:285,305 |
| `files_changed` | `0` | **Dead** | Only monitor.py:317 |
| `lines_total` | `0` | **Dead** | Only monitor.py:263 |
| `growth_rate_bps` | `0.0` | **Dead** | Only monitor.py:227 |
| `stall_seconds` | `0.0` | **Dead** | Only monitor.py:213,261 |
| `phase_started_at` | `monotonic()` | **Never written** | No write site outside init |

### TUI Rendering Dependencies (Current)

| TUI Method | MonitorState Fields Read | Path A Impact |
|---|---|---|
| `_build_header` (tui.py:149-152) | None | **OK** |
| `_build_phase_table` (tui.py:154-215) | `stall_seconds` (:193) | **DEGRADED** — shows `0s` |
| `_build_progress` (tui.py:217-228) | None | **OK** |
| `_build_active_panel` (tui.py:230-263) | `stall_status` (:239), `last_task_id` (:252), `last_tool_used` (:253), `output_size_display` (:254), `growth_rate_bps` (:254), `files_changed` (:255) | **DEGRADED** — 4 of 6 fields dead |
| `_build_terminal_panel` (tui.py:264-285) | None | **OK** |

---

## 3. Strategy A: Per-Task Monitor Lifecycle

### 3.1 Concept

Start OutputMonitor before each task subprocess. Let it parse NDJSON in real time from a **per-task output file**. Stop and harvest state after the task exits. Accumulate phase-level stats externally.

### 3.2 File Changes

#### `models.py` — New per-task output path method

**Location**: After `output_file()` at line 410.

```python
# NEW: models.py:411-413
def task_output_file(self, phase: "Phase", task_id: str) -> Path:
    """Per-task output file: phase-N-task-T0101-output.txt"""
    return self.results_dir / f"phase-{phase.number}-task-{task_id}-output.txt"
```

**Also add** aggregated phase output helper:

```python
# NEW: models.py:414-416
def task_output_glob(self, phase: "Phase") -> str:
    """Glob pattern for all task outputs in a phase."""
    return str(self.results_dir / f"phase-{phase.number}-task-*-output.txt")
```

#### `models.py` — PhaseAccumulator dataclass

**Location**: After MonitorState class (after line 544).

```python
# NEW: models.py:546-572
@dataclass
class PhaseAccumulator:
    """Accumulates MonitorState-equivalent fields across tasks in a phase.

    OutputMonitor.reset()/start() creates fresh MonitorState per task.
    This accumulator preserves phase-level totals for TUI rendering.
    """
    total_output_bytes: int = 0
    total_lines: int = 0
    total_events: int = 0
    total_files_changed: int = 0
    total_turns: int = 0
    task_activity_log: list = field(default_factory=list)  # [(ts, task_id, status)]
    task_errors: list = field(default_factory=list)         # [(task_id, source, detail)]
    tasks_completed: int = 0
    tasks_total: int = 0

    def harvest(self, task_id: str, monitor_state: "MonitorState",
                exit_code: int, turns: int) -> None:
        """Harvest per-task monitor state into phase accumulators."""
        self.total_output_bytes += monitor_state.output_bytes
        self.total_lines += monitor_state.lines_total
        self.total_events += monitor_state.events_received
        self.total_files_changed += monitor_state.files_changed
        self.total_turns += turns
        self.tasks_completed += 1
        status = "PASS" if exit_code == 0 else f"FAIL({exit_code})"
        self.task_activity_log.append((time.monotonic(), task_id, status))
        if exit_code != 0:
            self.task_errors.append((task_id, "subprocess", str(exit_code)))

    def to_monitor_state(self) -> "MonitorState":
        """Snapshot accumulator into MonitorState for TUI update."""
        state = MonitorState()
        state.output_bytes = self.total_output_bytes
        state.events_received = self.total_events
        state.files_changed = self.total_files_changed
        state.lines_total = self.total_lines
        return state
```

**LOC added**: ~30

#### `executor.py` — Modified `execute_phase_tasks()` signature

**Location**: Line 912-925.

```python
# MODIFIED: executor.py:912-925
def execute_phase_tasks(
    tasks: list[TaskEntry],
    config: SprintConfig,
    phase,
    ledger: TurnLedger | None = None,
    _subprocess_factory=None,
    shadow_metrics: ShadowGateMetrics | None = None,
    remediation_log: DeferredRemediationLog | None = None,
    tui: SprintTUI | None = None,
    sprint_result: SprintResult | None = None,
    monitor: OutputMonitor | None = None,          # NEW PARAMETER
) -> tuple[list[TaskResult], dict, list]:
```

**LOC modified**: 1 (add parameter)

#### `executor.py` — Per-task monitor lifecycle in task loop

**Location**: Inside the task loop, wrapping `_run_task_subprocess()` call. Replace lines ~975-1050.

```python
# MODIFIED: executor.py, inside execute_phase_tasks() task loop

    accumulator = PhaseAccumulator(tasks_total=len(tasks))

    for i, task in enumerate(tasks):
        # ... existing budget pre-debit ...

        # Per-task output file
        task_output_path = config.task_output_file(phase, task.task_id)

        # Start monitor for this task (if available)
        if monitor:
            monitor.reset(task_output_path)
            monitor.start()

        # Pre-task TUI update with live monitor state
        if tui:
            state = monitor.state if monitor else MonitorState()
            state.last_task_id = task.task_id
            tui.update(sprint_result, state, phase)

        try:
            exit_code, turns_consumed, output_bytes = _run_task_subprocess(
                task, config, phase, output_file=task_output_path  # NEW: pass per-task path
            )
        finally:
            if monitor:
                monitor.stop()

        # Harvest per-task state into accumulator
        if monitor:
            accumulator.harvest(task.task_id, monitor.state, exit_code, turns_consumed)

        # Build TaskResult with output_path (fixes PA-05)
        result = TaskResult(
            task=task.task_id,
            status="pass" if exit_code == 0 else "fail",
            exit_code=exit_code,
            turns_consumed=turns_consumed,
            output_bytes=output_bytes,
            output_path=str(task_output_path),  # FIX: was never set
            # ... remaining fields ...
        )

        # Post-task TUI update with accumulated state
        if tui:
            phase_state = accumulator.to_monitor_state()
            phase_state.last_task_id = task.task_id
            tui.update(sprint_result, phase_state, phase)

        # ... existing anti-instinct hook, gate, remediation ...
```

**LOC added/modified**: ~35

#### `executor.py` — Modified `_run_task_subprocess()` signature

**Location**: Line 1053-1092.

```python
# MODIFIED: executor.py:1053
def _run_task_subprocess(
    task: TaskEntry,
    config: SprintConfig,
    phase,
    output_file: Path | None = None,  # NEW: optional per-task override
) -> tuple[int, int, int]:
```

**Internal change**: Use `output_file or config.output_file(phase)` instead of `config.output_file(phase)` at line 1078.

**LOC modified**: 3

#### `executor.py` — Pass monitor into `execute_phase_tasks()` at fork point

**Location**: Line 1208-1213.

```python
# MODIFIED: executor.py:1208-1213
results, gate_results, remediation_entries = execute_phase_tasks(
    tasks, config, phase,
    ledger=ledger,
    shadow_metrics=shadow_metrics,
    remediation_log=remediation_log,
    tui=tui,
    sprint_result=sprint_result,
    monitor=monitor,          # NEW: pass the existing monitor instance
)
```

**LOC modified**: 1

#### `diagnostics.py` — Adapt to per-task output files

**Location**: Lines 118-121, 195-210.

Post-phase diagnostics currently read `config.output_file(phase)`. Must adapt to scan per-task files and concatenate or read the last task's output.

```python
# MODIFIED: diagnostics.py, adapt output_file resolution
# Use glob to find task output files, fall back to phase output
import glob

task_files = sorted(glob.glob(config.task_output_glob(phase)))
if task_files:
    output_path = Path(task_files[-1])  # last task output for diagnostics
else:
    output_path = config.output_file(phase)  # fallback
```

**LOC modified**: ~8

#### `tmux.py` — Adapt tail pane target

**Location**: Lines 82-97.

The tmux tail pane currently tails `config.output_file(phase)`. For Strategy A, it should tail the current task's per-task output file.

**LOC modified**: ~5

### 3.3 Data Flow Diagram

```
execute_sprint()
  │
  ├─ monitor = OutputMonitor(Path("/dev/null"))
  │
  └─ for each phase:
       │
       └─ PATH A (tasks exist):
            │
            ├─ accumulator = PhaseAccumulator(tasks_total=N)
            │
            └─ for each task:
                 │
                 ├─ task_output = config.task_output_file(phase, task_id)
                 │     └─ results/phase-1-task-T0101-output.txt
                 │
                 ├─ monitor.reset(task_output)    # fresh state + cursor
                 ├─ monitor.start()               # daemon thread → _poll_loop
                 │     │
                 │     ├──┐ _poll_once() every 0.5s
                 │     │  ├─ stat(task_output) for size
                 │     │  ├─ read new bytes → _process_chunk
                 │     │  │   └─ parse NDJSON → _extract_signals
                 │     │  │       └─ populates: output_bytes, lines_total,
                 │     │  │          events_received, last_tool_used,
                 │     │  │          last_task_id, files_changed,
                 │     │  │          growth_rate_bps, stall_seconds
                 │     │  └─ update stall_seconds if no growth
                 │     └──┘
                 │
                 ├─ _run_task_subprocess(task, config, phase,
                 │       output_file=task_output)
                 │     └─ Claude subprocess writes NDJSON to task_output
                 │
                 ├─ monitor.stop()
                 │     └─ state preserved (not cleared)
                 │
                 ├─ accumulator.harvest(task_id, monitor.state, exit_code, turns)
                 │     └─ adds per-task totals to phase accumulators
                 │
                 └─ tui.update(result, accumulator.to_monitor_state(), phase)
                       └─ TUI sees cumulative phase state
```

### 3.4 TUI Feature Support Matrix

| TUI Feature | F# | Support Level | Notes |
|---|---|---|---|
| Activity Stream | F1 | **Full** | Real-time NDJSON parsing per task |
| Enhanced Phase Table | F2 | **Full** | Live turns/output from monitor + accumulator |
| Task-Level Progress | F3 | **Full** | `accumulator.tasks_completed / tasks_total` |
| Error Panel | F4 | **Full** | Real-time error extraction from NDJSON |
| LLM Context Lines | F5 | **Degraded** | Only useful with enriched prompts (PA-01+) |
| Terminal Panels | F6 | **Full** | Aggregated from accumulator |
| Sprint Name | F7 | **Full** | Path-agnostic |
| Post-Phase Summary | F8 | **Full** | Per-task output files available for extraction |
| Tmux Summary | F9 | **Full** | Tail current task output file |
| Retrospective | F10 | **Full** | Aggregate per-task files |

### 3.5 Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Monitor start/stop race condition | Medium | `stop()` + `join(2.0)` before next `start()`. Tests confirm sequential safety. |
| Per-task output file proliferation | Low | 10 tasks × 5 phases = 50 files. Cleanup in sprint finalization. |
| Diagnostics/tmux breakage | Medium | Backward-compatible fallback to phase-level file when no task files exist. |
| `_run_task_subprocess` blocking prevents real-time TUI | **High** | Monitor thread polls file independently of subprocess wait. TUI `update()` called from executor loop, not from monitor. In Path A's current blocking model, TUI updates happen only between tasks unless a separate refresh thread is added. |

**LOC Estimate**: ~85 added, ~18 modified = **~103 total**

---

## 4. Strategy B: Synthetic State Population

### 4.1 Concept

Do **not** start OutputMonitor for Path A. After each task subprocess completes, synthetically populate MonitorState fields from available TaskResult data and subprocess exit info. No output file changes needed.

### 4.2 File Changes

#### `executor.py` — New `_build_synthetic_state()` helper

**Location**: After `_run_task_subprocess()`, around line 1093.

```python
# NEW: executor.py:1093-1120
def _build_synthetic_state(
    task: TaskEntry,
    task_index: int,
    total_tasks: int,
    exit_code: int,
    turns_consumed: int,
    output_bytes: int,
    prior_state: MonitorState | None = None,
) -> MonitorState:
    """Build MonitorState from task subprocess results (no live monitoring).

    Provides between-task TUI updates with accumulated metrics.
    Compatible with Strategy A's PhaseAccumulator.to_monitor_state() interface.
    """
    state = MonitorState()
    now = time.monotonic()

    # Accumulate from prior state
    if prior_state:
        state.output_bytes = prior_state.output_bytes + output_bytes
        state.events_received = prior_state.events_received + 1
        state.files_changed = prior_state.files_changed  # can't know without parsing
        state.lines_total = prior_state.lines_total
    else:
        state.output_bytes = output_bytes
        state.events_received = 1

    # Set current-task fields
    state.last_task_id = task.task_id
    state.last_event_time = now
    state.last_growth_time = now
    state.stall_seconds = 0.0  # just finished, not stalled

    return state
```

**LOC added**: ~28

#### `executor.py` — Replace ad-hoc MonitorState writes in task loop

**Location**: Lines 978-984 and 1042-1048.

```python
# MODIFIED: executor.py:978-984 (pre-task update)
if tui:
    _pre_state = MonitorState()
    _pre_state.last_task_id = task.task_id
    _pre_state.events_received = i
    _pre_state.last_event_time = time.monotonic()
    tui.update(sprint_result, _pre_state, phase)

# MODIFIED: executor.py:1042-1048 (post-task update)
if tui:
    _accumulated_state = _build_synthetic_state(
        task=task,
        task_index=i,
        total_tasks=len(tasks),
        exit_code=exit_code,
        turns_consumed=turns_consumed,
        output_bytes=output_bytes,
        prior_state=_last_synthetic_state,
    )
    _last_synthetic_state = _accumulated_state
    tui.update(sprint_result, _accumulated_state, phase)
```

**LOC modified**: ~12

#### `executor.py` — Wire `TaskResult.output_path` (PA-05 fix, included)

**Location**: Line 1017-1025.

```python
# MODIFIED: executor.py:1024 (inside TaskResult constructor)
output_path=str(config.output_file(phase)),  # FIX PA-05: was ""
```

**LOC modified**: 1

#### `executor.py` — Wire `turns_consumed` (PA-04 fix, included)

**Location**: Line 1091-1092.

```python
# MODIFIED: executor.py:1091-1092
turns = count_turns_from_output(config.output_file(phase))
return (exit_code, turns, output_bytes)
```

**LOC modified**: 2

### 4.3 Data Flow Diagram

```
execute_sprint()
  │
  └─ for each phase:
       │
       └─ PATH A (tasks exist):
            │
            ├─ _last_synthetic_state = None
            │
            └─ for each task:
                 │
                 ├─ tui.update(result, pre_state, phase)
                 │     └─ shows: task_id, "waiting..."
                 │
                 ├─ _run_task_subprocess(task, config, phase)
                 │     └─ writes to phase-N-output.txt (SAME FILE, overwrites)
                 │     └─ returns (exit_code, turns_consumed, output_bytes)
                 │                          ↑ NOW REAL (PA-04 fix)
                 │
                 ├─ _accumulated = _build_synthetic_state(
                 │       task, i, N, exit_code, turns, bytes,
                 │       prior_state=_last_synthetic_state)
                 │     └─ accumulates: output_bytes, events, task_id
                 │
                 ├─ tui.update(result, _accumulated, phase)
                 │     └─ shows: cumulative output, task_id, "active"
                 │     └─ NO real-time data during task execution
                 │
                 └─ _last_synthetic_state = _accumulated
```

### 4.4 TUI Feature Support Matrix

| TUI Feature | F# | Support Level | Notes |
|---|---|---|---|
| Activity Stream | F1 | **Between-task only** | One entry per task completion, no real-time |
| Enhanced Phase Table | F2 | **Between-task only** | Turns/output update after each task |
| Task-Level Progress | F3 | **Full** | Counter increments reliably |
| Error Panel | F4 | **Between-task only** | Exit code, no tool-level errors |
| LLM Context Lines | F5 | **None** | No NDJSON parsing |
| Terminal Panels | F6 | **Between-task only** | Aggregated from synthetic state |
| Sprint Name | F7 | **Full** | Path-agnostic |
| Post-Phase Summary | F8 | **Degraded** | Only last task's output available (overwrite) |
| Tmux Summary | F9 | **Degraded** | Only last task's output in tail |
| Retrospective | F10 | **Degraded** | Incomplete NDJSON history |

### 4.5 Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| No real-time TUI during task execution | **Accepted** | TUI shows "waiting..." then jumps to results. Users see progress between tasks. |
| Output file overwrite loses history | **Accepted** | Known limitation. F8/F9/F10 degraded but functional. |
| `files_changed` always 0 | Low | Synthetic state can't determine file changes without parsing. Show as `"-"` in TUI. |
| `growth_rate_bps` always 0 | Low | No live monitoring = no growth rate. Show as `"-"` in TUI. |

**LOC Estimate**: ~30 added, ~15 modified = **~45 total**

---

## 5. Strategy C: Hybrid (Recommended)

### 5.1 Concept

Ship Strategy B for v3.7 (fast, no output file changes). Design interfaces so Strategy A can be layered in at v3.8 with **zero TUI-side changes**. The key insight: both strategies produce a `MonitorState` that the TUI consumes. The TUI doesn't care whether the state came from live monitoring or synthetic population.

### 5.2 Design Principle: The MonitorState Adapter Interface

Both strategies converge on a single contract:

```
executor task loop → [MonitorState] → tui.update()
```

Strategy B populates `MonitorState` via `_build_synthetic_state()`.
Strategy A populates `MonitorState` via `monitor.state` + `PhaseAccumulator.to_monitor_state()`.
The TUI is agnostic to the source.

### 5.3 File Changes — v3.7 (Strategy B foundation + forward-compatible interfaces)

#### `models.py` — Add `PhaseAccumulator` (forward-compatible)

**Location**: After MonitorState (line 544).

Even though v3.7 uses synthetic state, we introduce `PhaseAccumulator` now because:
1. It provides the `harvest()` + `to_monitor_state()` interface that Strategy A needs.
2. Strategy B's `_build_synthetic_state()` can be reimplemented as `PhaseAccumulator.harvest_synthetic()`.
3. Zero wasted code — every line ships in v3.7.

```python
# NEW: models.py, after line 544
@dataclass
class PhaseAccumulator:
    """Accumulates task metrics across a phase for TUI rendering.

    v3.7: Fed by synthetic post-task data (_build_synthetic_state equivalent).
    v3.8: Fed by OutputMonitor.state after each task (live monitoring).
    TUI consumes .to_monitor_state() in both cases — source-agnostic.
    """
    total_output_bytes: int = 0
    total_lines: int = 0
    total_events: int = 0
    total_files_changed: int = 0
    total_turns: int = 0
    tasks_completed: int = 0
    tasks_total: int = 0
    _last_task_id: str = ""
    _last_tool_used: str = ""
    _phase_start: float = field(default_factory=time.monotonic)

    def harvest_synthetic(self, task_id: str, exit_code: int,
                          turns: int, output_bytes: int) -> None:
        """v3.7 path: harvest from subprocess exit data (no monitor)."""
        self.total_output_bytes += output_bytes
        self.total_events += 1
        self.total_turns += turns
        self.tasks_completed += 1
        self._last_task_id = task_id

    def harvest_monitored(self, task_id: str, monitor_state: "MonitorState",
                          exit_code: int, turns: int) -> None:
        """v3.8 path: harvest from live OutputMonitor state."""
        self.total_output_bytes += monitor_state.output_bytes
        self.total_lines += monitor_state.lines_total
        self.total_events += monitor_state.events_received
        self.total_files_changed += monitor_state.files_changed
        self.total_turns += turns
        self.tasks_completed += 1
        self._last_task_id = task_id
        self._last_tool_used = monitor_state.last_tool_used

    def to_monitor_state(self) -> "MonitorState":
        """Convert accumulator to MonitorState for TUI consumption.

        This is the adapter boundary: TUI sees MonitorState regardless
        of whether data came from live monitoring or synthetic population.
        """
        state = MonitorState()
        state.output_bytes = self.total_output_bytes
        state.events_received = self.total_events
        state.files_changed = self.total_files_changed
        state.lines_total = self.total_lines
        state.last_task_id = self._last_task_id
        state.last_tool_used = self._last_tool_used
        state.last_event_time = time.monotonic()
        state.stall_seconds = 0.0  # just updated, not stalled
        return state
```

**LOC added**: ~48

#### `models.py` — Add `task_output_file()` (forward-compatible, not called in v3.7)

```python
# NEW: models.py:411-413 (after output_file)
def task_output_file(self, phase: "Phase", task_id: str) -> Path:
    """Per-task output file for v3.8 monitor lifecycle."""
    return self.results_dir / f"phase-{phase.number}-task-{task_id}-output.txt"
```

**LOC added**: 3

#### `executor.py` — Modified `execute_phase_tasks()` with accumulator

**Location**: Lines 912-1050.

```python
# MODIFIED: executor.py:912+
def execute_phase_tasks(
    tasks: list[TaskEntry],
    config: SprintConfig,
    phase,
    ledger: TurnLedger | None = None,
    _subprocess_factory=None,
    shadow_metrics: ShadowGateMetrics | None = None,
    remediation_log: DeferredRemediationLog | None = None,
    tui: SprintTUI | None = None,
    sprint_result: SprintResult | None = None,
    monitor: OutputMonitor | None = None,          # NEW: v3.8 hook point
) -> tuple[list[TaskResult], dict, list]:
```

Inside task loop:

```python
    accumulator = PhaseAccumulator(tasks_total=len(tasks))

    for i, task in enumerate(tasks):
        # ... existing budget pre-debit ...

        # === v3.8 HOOK POINT: per-task monitor lifecycle ===
        # When monitor is passed in v3.8:
        #   task_output = config.task_output_file(phase, task.task_id)
        #   monitor.reset(task_output)
        #   monitor.start()
        # v3.7: no monitor, use phase-level output file
        task_output = config.output_file(phase)

        # Pre-task TUI update
        if tui:
            pre_state = accumulator.to_monitor_state()
            pre_state.last_task_id = task.task_id
            tui.update(sprint_result, pre_state, phase)

        try:
            exit_code, turns_consumed, output_bytes = _run_task_subprocess(
                task, config, phase
            )
        finally:
            # === v3.8 HOOK POINT: monitor.stop() here ===
            pass

        # Harvest: v3.7 synthetic, v3.8 monitored
        if monitor:
            accumulator.harvest_monitored(
                task.task_id, monitor.state, exit_code, turns_consumed
            )
        else:
            accumulator.harvest_synthetic(
                task.task_id, exit_code, turns_consumed, output_bytes
            )

        # TaskResult with output_path (PA-05 fix)
        result = TaskResult(
            task=task.task_id,
            status="pass" if exit_code == 0 else "fail",
            exit_code=exit_code,
            turns_consumed=turns_consumed,
            output_bytes=output_bytes,
            output_path=str(task_output),
            # ... remaining fields ...
        )

        # Post-task TUI update with accumulated state
        if tui:
            tui.update(sprint_result, accumulator.to_monitor_state(), phase)

        # ... existing anti-instinct hook ...
```

**LOC added**: ~20, **LOC modified**: ~15

#### `executor.py` — PA-04 fix (turns_consumed)

**Location**: Line 1091-1092.

```python
# MODIFIED: executor.py:1091-1092
turns = count_turns_from_output(config.output_file(phase))
return (exit_code, turns, output_bytes)
```

**LOC modified**: 2

#### `executor.py` — Pass `monitor=None` at fork point (v3.7), `monitor=monitor` (v3.8)

**Location**: Line 1208-1213.

```python
# MODIFIED: executor.py:1208-1213 (v3.7: monitor=None)
results, gate_results, remediation_entries = execute_phase_tasks(
    tasks, config, phase,
    ledger=ledger,
    shadow_metrics=shadow_metrics,
    remediation_log=remediation_log,
    tui=tui,
    sprint_result=sprint_result,
    monitor=None,  # v3.7: synthetic. v3.8: pass `monitor` for live monitoring
)
```

**LOC modified**: 1

### 5.4 Data Flow Diagram — v3.7 (Hybrid, Synthetic)

```
execute_sprint()
  │
  └─ for each phase:
       │
       └─ PATH A:
            │
            ├─ accumulator = PhaseAccumulator(tasks_total=N)
            │
            └─ for each task:
                 │
                 ├─ tui.update(result, accumulator.to_monitor_state(), phase)
                 │     └─ TUI sees accumulated state with current task_id
                 │
                 ├─ _run_task_subprocess(task, config, phase)
                 │     └─ returns (exit_code, turns, output_bytes)
                 │                          ↑ REAL turns (PA-04)
                 │
                 ├─ accumulator.harvest_synthetic(task_id, exit_code, turns, bytes)
                 │     └─ accumulates totals, increments tasks_completed
                 │
                 └─ tui.update(result, accumulator.to_monitor_state(), phase)
                       └─ TUI sees updated cumulative state
```

### 5.5 Data Flow Diagram — v3.8 (Hybrid, Monitored)

```
execute_sprint()
  │
  └─ for each phase:
       │
       └─ PATH A:
            │
            ├─ accumulator = PhaseAccumulator(tasks_total=N)
            │
            └─ for each task:
                 │
                 ├─ task_output = config.task_output_file(phase, task_id)
                 ├─ monitor.reset(task_output)
                 ├─ monitor.start()          # daemon thread
                 │
                 ├─ _run_task_subprocess(task, config, phase,
                 │       output_file=task_output)
                 │     └─ NDJSON → task_output (per-task file)
                 │     └─ monitor._poll_loop reads in real time
                 │
                 ├─ monitor.stop()           # state preserved
                 │
                 ├─ accumulator.harvest_monitored(task_id, monitor.state, ...)
                 │     └─ full fidelity: output_bytes, lines, files, tools
                 │
                 └─ tui.update(result, accumulator.to_monitor_state(), phase)
                       └─ SAME TUI code, richer data
```

### 5.6 TUI Feature Support Matrix (v3.7 → v3.8 progression)

| TUI Feature | F# | v3.7 (Synthetic) | v3.8 (Monitored) |
|---|---|---|---|
| Activity Stream | F1 | **Between-task** | **Full real-time** |
| Enhanced Phase Table | F2 | **Between-task** | **Full real-time** |
| Task-Level Progress | F3 | **Full** | **Full** |
| Error Panel | F4 | **Between-task** (exit code) | **Full** (tool-level) |
| LLM Context Lines | F5 | **None** | **Degraded** |
| Terminal Panels | F6 | **Between-task** | **Full** |
| Sprint Name | F7 | **Full** | **Full** |
| Post-Phase Summary | F8 | **Degraded** (overwrite) | **Full** (per-task files) |
| Tmux Summary | F9 | **Degraded** | **Full** |
| Retrospective | F10 | **Degraded** | **Full** |

### 5.7 Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| PhaseAccumulator interface wrong for v3.8 | Low | `harvest_monitored()` maps directly from MonitorState fields. Conservative design. |
| v3.7 synthetic state misleads users | Low | "Between-task" updates are clearly timestamped. No false real-time claims. |
| `task_output_file()` unused in v3.7 | **Negligible** | 3 LOC, tested, ready for v3.8. |
| PA-04 `count_turns_from_output` reads overwritten file | Medium | In v3.7, only last task's turns are counted (file overwritten). In v3.8, per-task files solve this. Document limitation. |

**LOC Estimate (v3.7)**: ~71 added, ~18 modified = **~89 total**
**LOC Estimate (v3.8 delta)**: ~15 added, ~8 modified = **~23 additional**

---

## 6. Comparative Analysis

### 6.1 Strategy Comparison Matrix

| Dimension | Strategy A | Strategy B | Strategy C (Recommended) |
|---|---|---|---|
| **Real-time TUI** | Full | None (between-task) | v3.7: between-task, v3.8: full |
| **Output files** | Per-task (breaking change) | Unchanged | v3.7: unchanged, v3.8: per-task |
| **LOC** | ~103 | ~45 | v3.7: ~89, v3.8: +23 |
| **Risk** | Medium-High | Low | Low (v3.7), Medium (v3.8) |
| **Path B impact** | None | None | None |
| **TUI code changes** | None | None | None (either version) |
| **PA-04/05/06 included** | Yes | Partial (PA-04,05) | Yes (all three) |
| **Forward compatible** | N/A (final state) | No (rewrite for A) | Yes (B→A seamless) |
| **Diagnostics impact** | Must adapt | None | v3.7: none, v3.8: must adapt |
| **Tmux impact** | Must adapt | None | v3.7: none, v3.8: must adapt |
| **Ship timeline** | v3.8 | v3.7 | v3.7 partial, v3.8 full |

### 6.2 Feature Coverage Comparison

| Feature | Strategy A | Strategy B | Strategy C v3.7 | Strategy C v3.8 |
|---|---|---|---|---|
| F1 Activity | Full | Between-task | Between-task | Full |
| F2 Phase Table | Full | Between-task | Between-task | Full |
| F3 Progress | Full | Full | Full | Full |
| F4 Errors | Full | Between-task | Between-task | Full |
| F5 LLM Context | Degraded | None | None | Degraded |
| F6 Panels | Full | Between-task | Between-task | Full |
| F7 Sprint Name | Full | Full | Full | Full |
| F8 Summary | Full | Degraded | Degraded | Full |
| F9 Tmux | Full | Degraded | Degraded | Full |
| F10 Retro | Full | Degraded | Degraded | Full |
| **Full count** | **8/10** | **2/10** | **2/10** | **8/10** |
| **Functional count** | **10/10** | **7/10** | **7/10** | **10/10** |

---

## 7. Recommendation and Migration Path

### 7.1 Recommendation: Strategy C (Hybrid)

Strategy C is the correct choice because:

1. **Ships v3.7 on time** with meaningful TUI improvements (progress, between-task updates, accumulated metrics) at ~89 LOC.
2. **Zero output file changes** in v3.7 — no diagnostics, tmux, or downstream consumer breakage.
3. **Forward-compatible interfaces** — `PhaseAccumulator` with both `harvest_synthetic()` and `harvest_monitored()` means v3.8 is a ~23 LOC delta, not a rewrite.
4. **TUI is source-agnostic** — `accumulator.to_monitor_state()` produces the same `MonitorState` object regardless of data source. Zero TUI changes between v3.7 and v3.8.
5. **Includes PA-04/05/06 bug fixes** as natural prerequisites, activating the anti-instinct gate system.

### 7.2 Migration Path: v3.7 → v3.8

```
v3.7 (Strategy B via Hybrid)             v3.8 (Strategy A via Hybrid)
─────────────────────────────             ──────────────────────────────

execute_phase_tasks(                      execute_phase_tasks(
    ..., monitor=None)                        ..., monitor=monitor)  ← CHANGE 1

task_output = config.output_file(phase)   task_output = config.task_output_file(
                                              phase, task.task_id)   ← CHANGE 2

# no monitor start/stop                  monitor.reset(task_output)  ← CHANGE 3
                                          monitor.start()
try:                                      try:
    _run_task_subprocess(task, ...)            _run_task_subprocess(task, ...,
                                                  output_file=task_output) ← CHANGE 4
finally:                                  finally:
    pass                                      monitor.stop()         ← CHANGE 5

accumulator.harvest_synthetic(...)        accumulator.harvest_monitored(
                                              ..., monitor.state)    ← CHANGE 6

# TUI code: UNCHANGED                    # TUI code: UNCHANGED
tui.update(result,                        tui.update(result,
    accumulator.to_monitor_state(),           accumulator.to_monitor_state(),
    phase)                                    phase)
```

**Total v3.8 changes**: 6 call-site modifications in `executor.py`, ~23 LOC. No TUI changes. No model changes. No new classes.

### 7.3 Implementation Order (v3.7)

| Order | Task | File | LOC | Depends On |
|---|---|---|---|---|
| 1 | Add `PhaseAccumulator` class | models.py | ~48 | None |
| 2 | Add `task_output_file()` method | models.py | 3 | None |
| 3 | Fix PA-04: `turns_consumed` | executor.py | 2 | None |
| 4 | Fix PA-05: `TaskResult.output_path` | executor.py | 1 | None |
| 5 | Add `monitor` param to `execute_phase_tasks` | executor.py | 1 | None |
| 6 | Replace ad-hoc MonitorState with accumulator | executor.py | ~35 | 1, 3, 4, 5 |
| 7 | Pass `monitor=None` at fork point | executor.py | 1 | 5 |
| 8 | Tests for PhaseAccumulator | tests/ | ~40 | 1 |
| 9 | Tests for synthetic TUI updates | tests/ | ~25 | 6 |
| **Total** | | | **~156** (incl. tests) | |

### 7.4 Prerequisites (from other chunks)

These tasks from chunk-06 should be completed **before or alongside** this work:

- **PA-01** (per-task block extraction): Not required for this design but enriches the prompt that produces the NDJSON that v3.8's monitor will parse.
- **PA-06** (gate default to shadow): Should ship with PA-04/PA-05 to fully activate the anti-instinct system.

---

## 8. Appendix: MonitorState Field Reference

### Current Fields (models.py:508-519)

| Field | Type | Default | Live Source (monitor.py) | Synthetic Source (v3.7) | TUI Consumer (tui.py) |
|---|---|---|---|---|---|
| `output_bytes` | `int` | `0` | `_poll_once:204` | `harvest_synthetic` (from subprocess) | `_build_active_panel:254` via `output_size_display` |
| `output_bytes_prev` | `int` | `0` | `_poll_once:203` | Not populated (internal) | None |
| `last_growth_time` | `float` | `monotonic()` | `_process_chunk:259` | Set to `monotonic()` on harvest | None |
| `last_event_time` | `float` | `monotonic()` | `_process_chunk:260` | Set to `monotonic()` on harvest | `_build_active_panel:239` via `stall_status` |
| `phase_started_at` | `float` | `monotonic()` | Never written | Set at accumulator init | `stall_status` property |
| `events_received` | `int` | `0` | `_process_chunk:262` | Incremented per task | `stall_status` property |
| `last_task_id` | `str` | `""` | `_extract_text:297` | Set to current `task_id` | `_build_active_panel:252` |
| `last_tool_used` | `str` | `""` | `_extract_event:285`, `_extract_text:305` | Not populated (v3.7) | `_build_active_panel:253` |
| `files_changed` | `int` | `0` | `_extract_text:317` | Not populated (v3.7) | `_build_active_panel:255` |
| `lines_total` | `int` | `0` | `_process_chunk:263` | Not populated (v3.7) | None |
| `growth_rate_bps` | `float` | `0.0` | `_poll_once:227` | Not populated (v3.7) | `_build_active_panel:254` |
| `stall_seconds` | `float` | `0.0` | `_poll_once:213`, `_process_chunk:261` | Set to 0 on harvest | `_build_phase_table:193` |

### v3.7 TUI Active Panel Rendering (with Strategy C)

Fields that remain at defaults in v3.7 (`last_tool_used`, `files_changed`, `growth_rate_bps`) render as:
- `last_tool_used = ""` → displays `"-"` (tui.py:253, uses `or '-'`)
- `files_changed = 0` → displays `"0"` (tui.py:255, acceptable — truly unknown)
- `growth_rate_bps = 0.0` → displays `"+0.0 B/s"` (tui.py:254)

**Acceptable tradeoff**: These 3 fields provide low-value information in Path A's between-task update model. They become fully populated in v3.8 with live monitoring.

---

*End of design document.*
