# Implementation Workflow: Per-Task OutputMonitor Adaptation (v3.7)

## Metadata

| Field | Value |
|---|---|
| **Date** | 2026-04-03 |
| **Strategy** | Strategy B (Synthetic State) + Append-Mode Fix — per adversarial debate rulings |
| **Source design** | docs/generated/sprint-cli/v3.7-refactor/design-monitor-per-task.md |
| **Debate rulings** | docs/generated/sprint-cli/v3.7-refactor/debates-monitor-adaptation.md |
| **Integration** | Slots into MERGED-REFACTORING-RECOMMENDATION.md wave structure |
| **Total LOC** | ~83 production + ~120 test = ~203 total |
| **Risk** | LOW (no threading changes, no file naming changes, no downstream consumer changes) |

---

## Table of Contents

1. [Strategy Summary](#1-strategy-summary)
2. [Wave Structure Integration](#2-wave-structure-integration)
3. [Wave 0: Prerequisites (PA-04, PA-05, Append-Mode Fix)](#3-wave-0-prerequisites)
4. [Wave 0.5: PhaseAccumulator + Adapter Foundation](#4-wave-05-phaseaccumulator--adapter-foundation)
5. [Wave 1: Executor Integration](#5-wave-1-executor-integration)
6. [Wave 1.5: Invariant Probe Mitigations](#6-wave-15-invariant-probe-mitigations)
7. [Wave 2: Forward-Compatibility Hooks](#7-wave-2-forward-compatibility-hooks)
8. [Test Plan](#8-test-plan)
9. [Dependency Graph](#9-dependency-graph)
10. [Risk Register](#10-risk-register)

---

## 1. Strategy Summary

Per the adversarial debate rulings (3 debates, all converged >87%):

| Ruling | Decision | Source |
|---|---|---|
| Monitor strategy | **Strategy B** (synthetic state population, no live OutputMonitor for Path A) | Debate 1: B wins 6-1-1 |
| Output file fix | **Append mode** (change `"w"` to `"a"` at process.py:114) — 1 LOC | Debate 2: Fix-Now wins 7-1-1 |
| TUI interface | **Shared MonitorState** via PhaseAccumulator.to_monitor_state() adapter | Debate 3: Shared wins 4-2-2 |
| stall_status fix | Adapter sets `last_event_time = monotonic()` to suppress false "STALLED" | Debate 3, INV-005 |
| Invariant: NDJSON boundary | Inject task boundary marker between tasks in append-mode file | INV-001 |
| Invariant: Gate file offset | Record file offset before task, pass to anti-instinct gate | INV-004 |

---

## 2. Wave Structure Integration

This tasklist integrates with the MERGED-REFACTORING-RECOMMENDATION.md unified implementation order:

```
MERGED SPEC Phase 0:  PA-04, PA-05, PA-01
                      ↓
THIS TASKLIST Wave 0:  MA-01 (PA-04), MA-02 (PA-05), MA-03 (append-mode)  ← PARALLEL
                      ↓
THIS TASKLIST Wave 0.5: MA-04 (PhaseAccumulator), MA-05 (task_output_file)  ← PARALLEL
                      ↓
MERGED SPEC Phase 1:  PA-02, PA-03, PA-06, N1-N12, DM-04, DM-05
                      ↓
THIS TASKLIST Wave 1:  MA-06 (executor integration), MA-07 (PA-06 gate default)  ← SEQUENTIAL
                      ↓
THIS TASKLIST Wave 1.5: MA-08 (task boundary), MA-09 (gate offset)  ← PARALLEL
                      ↓
MERGED SPEC Phase 2:  Checkpoint W1, DM-06
                      ↓
THIS TASKLIST Wave 2:  MA-10 (monitor param), MA-11 (forward-compat tests)  ← PARALLEL
                      ↓
MERGED SPEC Phase 3+: TUI v2 F1-F10, Checkpoint W2-W4
```

**Key**: MA = Monitor Adaptation task. Tasks MA-01 through MA-03 ARE PA-04, PA-05 plus the append-mode fix. They execute as the first wave, before any other v3.7 work.

---

## 3. Wave 0: Prerequisites

### MA-01: Fix `turns_consumed` to return actual turn count (= PA-04)

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/executor.py:1091-1092` |
| **LOC** | 2 modified, 1 added (import) |
| **Risk** | Low |
| **Parallelize with** | MA-02, MA-03 |
| **Dependencies** | None |

#### Steps

1. **Read** `executor.py:1089-1092` — current code:
   ```python
   output_bytes = output_path.stat().st_size if output_path.exists() else 0
   # Turn counting is wired separately in T02.06
   return (exit_code if exit_code is not None else -1, 0, output_bytes)
   ```

2. **Add import** at top of executor.py (near other monitor imports):
   ```python
   from superclaude.cli.sprint.monitor import count_turns_from_output
   ```

3. **Replace** lines 1091-1092 with:
   ```python
   turns = count_turns_from_output(output_path) if output_path.exists() else 0
   return (exit_code if exit_code is not None else -1, turns, output_bytes)
   ```

4. **Remove** the stale comment about T02.06.

#### Acceptance Criteria

- [ ] `_run_task_subprocess()` returns actual turn count from NDJSON parsing
- [ ] Turn count is non-zero for tasks that produce assistant-turn output
- [ ] Stale T02.06 comment removed
- [ ] Existing tests pass (budget reconciliation at executor.py:1007-1015 uses actual turns)

#### Verification

```bash
uv run pytest tests/sprint/test_executor.py -v -k "turn"
uv run pytest tests/sprint/test_monitor.py -v -k "count_turns"
```

#### Rollback

Revert to `return (exit_code, 0, output_bytes)`. Budget reconciliation returns to zero-reimbursement behavior.

---

### MA-02: Wire `TaskResult.output_path` (= PA-05)

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/executor.py:1017-1025` |
| **LOC** | 1 modified |
| **Risk** | Negligible |
| **Parallelize with** | MA-01, MA-03 |
| **Dependencies** | None |

#### Steps

1. **Read** `executor.py:1017-1025` — current TaskResult construction:
   ```python
   result = TaskResult(
       task=task,
       status=status,
       turns_consumed=turns_consumed,
       exit_code=exit_code,
       started_at=started_at,
       finished_at=finished_at,
       output_bytes=output_bytes,
   )
   ```

2. **Add** `output_path` field:
   ```python
   result = TaskResult(
       task=task,
       status=status,
       turns_consumed=turns_consumed,
       exit_code=exit_code,
       started_at=started_at,
       finished_at=finished_at,
       output_bytes=output_bytes,
       output_path=str(config.output_file(phase)),
   )
   ```

#### Acceptance Criteria

- [ ] `TaskResult.output_path` contains a valid file path after task execution
- [ ] Anti-instinct gate at executor.py:823-831 evaluates real file content (no longer vacuous pass)
- [ ] `to_context_summary()` includes output path in its output (models.py:207-208)

#### Verification

```bash
uv run pytest tests/sprint/test_executor.py -v -k "output_path or anti_instinct"
```

#### Rollback

Remove `output_path=str(config.output_file(phase))` from TaskResult constructor. Gate reverts to vacuous pass.

---

### MA-03: Fix output file overwrite — change "w" to "a" (append mode)

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/pipeline/process.py:114` |
| **LOC** | 1 modified |
| **Risk** | Low |
| **Parallelize with** | MA-01, MA-02 |
| **Dependencies** | None |

#### Steps

1. **Read** `process.py:114` — current code:
   ```python
   self._stdout_fh = open(self.output_file, "w")
   ```

2. **Replace** with:
   ```python
   self._stdout_fh = open(self.output_file, "a")
   ```

3. **Verify** that Path B is unaffected: Path B calls `monitor.reset(output_path)` at executor.py:1243 before `monitor.start()` at :1244. The monitor resets `_last_read_pos = 0`, so it reads from the beginning regardless of append. However, the phase output file will accumulate across tasks if any consumer creates a new process that writes to the same file. Check that Path B's single-process-per-phase model only opens the file once per phase.

4. **Verify** error file: `process.py:115` also opens error_file with `"w"`. This should ALSO be changed to `"a"` for consistency, but error_file is less critical (it captures stderr which is typically empty for successful tasks).

#### Acceptance Criteria

- [ ] Multi-task phase output file contains all tasks' NDJSON (not just the last task)
- [ ] `count_turns_from_output()` returns total turns across ALL tasks in a phase
- [ ] Path B behavior unchanged (single process per phase, file grows monotonically)
- [ ] Diagnostics at diagnostics.py:118-121 sees complete phase output

#### Verification

```bash
# Run a multi-task sprint in dry-run or test mode and verify output file size
# grows monotonically across tasks (not resets to 0 between tasks)
uv run pytest tests/sprint/ -v -k "output"
```

#### Rollback

Revert to `open(self.output_file, "w")`. Tasks revert to overwrite behavior.

**NOTE**: Also consider changing `process.py:115` (error_file) from `"w"` to `"a"` for consistency.

---

## 4. Wave 0.5: PhaseAccumulator + Adapter Foundation

### MA-04: Add PhaseAccumulator dataclass to models.py

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/models.py` — after MonitorState (line 544) |
| **LOC** | ~48 added |
| **Risk** | Low (additive, no existing code modified) |
| **Parallelize with** | MA-05 |
| **Dependencies** | None (but designed to work with MA-01, MA-02) |

#### Steps

1. **Read** models.py:544 to confirm insertion point (after MonitorState, before TurnLedger at line 546).

2. **Add** the PhaseAccumulator dataclass:

```python
@dataclass
class PhaseAccumulator:
    """Accumulates task metrics across a phase for TUI rendering.

    v3.7: Fed by synthetic post-task data (harvest_synthetic).
    v3.8: Fed by OutputMonitor.state after each task (harvest_monitored).
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

    def harvest_synthetic(
        self, task_id: str, exit_code: int, turns: int, output_bytes: int
    ) -> None:
        """v3.7 path: harvest from subprocess exit data (no monitor)."""
        self.total_output_bytes += output_bytes
        self.total_events += 1
        self.total_turns += turns
        self.tasks_completed += 1
        self._last_task_id = task_id

    def harvest_monitored(
        self, task_id: str, monitor_state: "MonitorState",
        exit_code: int, turns: int
    ) -> None:
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

        Adapter boundary: TUI sees MonitorState regardless of
        whether data came from live monitoring or synthetic population.
        """
        state = MonitorState()
        state.output_bytes = self.total_output_bytes
        state.events_received = self.total_events
        state.files_changed = self.total_files_changed
        state.lines_total = self.total_lines
        state.last_task_id = self._last_task_id
        state.last_tool_used = self._last_tool_used
        # Suppress false stall alarms (Debate 3 ruling, INV-005):
        # Set last_event_time to now so stall_status returns "active"
        state.last_event_time = time.monotonic()
        state.stall_seconds = 0.0
        return state
```

#### Acceptance Criteria

- [ ] `PhaseAccumulator` is importable from `superclaude.cli.sprint.models`
- [ ] `harvest_synthetic()` correctly accumulates output_bytes, events, turns, tasks_completed
- [ ] `to_monitor_state()` returns a valid MonitorState with `stall_status == "active"`
- [ ] `harvest_monitored()` correctly maps OutputMonitor state fields
- [ ] Zero-task edge case: `to_monitor_state()` returns default MonitorState (no crash)

#### Verification

```bash
uv run pytest tests/sprint/test_models.py -v -k "PhaseAccumulator or accumulator"
```

#### Rollback

Delete the PhaseAccumulator class. Executor continues using ad-hoc MonitorState writes.

---

### MA-05: Add `task_output_file()` to SprintConfig (forward-compatibility)

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/models.py:410` — after `output_file()` |
| **LOC** | 3 added |
| **Risk** | Negligible (additive, not called in v3.7) |
| **Parallelize with** | MA-04 |
| **Dependencies** | None |

#### Steps

1. **Read** models.py:409-413 (output_file and error_file methods).

2. **Add** after `output_file()` method (line 410):

```python
def task_output_file(self, phase: Phase, task_id: str) -> Path:
    """Per-task output file for v3.8 monitor lifecycle."""
    return self.results_dir / f"phase-{phase.number}-task-{task_id}-output.txt"
```

#### Acceptance Criteria

- [ ] Method is callable: `config.task_output_file(phase, "T01.03")` returns expected path
- [ ] Path follows pattern: `results/phase-1-task-T01.03-output.txt`
- [ ] NOT called from any production code path in v3.7

#### Verification

```bash
uv run pytest tests/sprint/test_models.py -v -k "task_output"
```

#### Rollback

Delete the method. No runtime impact.

---

## 5. Wave 1: Executor Integration

### MA-06: Replace ad-hoc MonitorState writes with PhaseAccumulator

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/executor.py:912-1050` |
| **LOC** | ~20 added, ~15 modified |
| **Risk** | **Medium** — modifies the core production task loop |
| **Parallelize with** | Nothing (touches critical path) |
| **Dependencies** | MA-01 (turns_consumed), MA-02 (output_path), MA-04 (PhaseAccumulator) |

#### Steps

1. **Add import** at top of executor.py:
   ```python
   from superclaude.cli.sprint.models import PhaseAccumulator
   ```

2. **Add `monitor` parameter** to `execute_phase_tasks()` signature at line 912:
   ```python
   def execute_phase_tasks(
       tasks: list[TaskEntry],
       config: SprintConfig,
       phase,
       ledger: TurnLedger | None = None,
       *,
       _subprocess_factory=None,
       shadow_metrics: ShadowGateMetrics | None = None,
       remediation_log: DeferredRemediationLog | None = None,
       tui: "SprintTUI | None" = None,
       sprint_result: "SprintResult | None" = None,
       monitor: "OutputMonitor | None" = None,  # v3.8 hook point
   ) -> tuple[list[TaskResult], list[str], list[TrailingGateResult]]:
   ```

3. **Initialize accumulator** after line 950 (after `gate_results: list[...] = []`):
   ```python
   accumulator = PhaseAccumulator(tasks_total=len(tasks))
   ```

4. **Replace pre-task TUI update** at lines 978-984:
   ```python
   # BEFORE:
   if tui is not None and sprint_result is not None:
       _tui_state = MonitorState()
       _tui_state.events_received = i
       _tui_state.last_event_time = time.monotonic()
       _tui_state.last_task_id = task.task_id
       tui.update(sprint_result, _tui_state, phase)

   # AFTER:
   if tui is not None and sprint_result is not None:
       pre_state = accumulator.to_monitor_state()
       pre_state.last_task_id = task.task_id
       tui.update(sprint_result, pre_state, phase)
   ```

5. **Add accumulator harvest** after TaskResult construction (after line 1025, before post-task hooks):
   ```python
   # Harvest task metrics into phase accumulator
   accumulator.harvest_synthetic(
       task_id=task.task_id,
       exit_code=exit_code,
       turns=turns_consumed,
       output_bytes=output_bytes,
   )
   ```

6. **Replace post-task TUI update** at lines 1042-1048:
   ```python
   # BEFORE:
   if tui is not None and sprint_result is not None:
       _tui_state = MonitorState()
       _tui_state.events_received = i + 1
       _tui_state.last_event_time = time.monotonic()
       _tui_state.last_task_id = task.task_id
       tui.update(sprint_result, _tui_state, phase)

   # AFTER:
   if tui is not None and sprint_result is not None:
       tui.update(sprint_result, accumulator.to_monitor_state(), phase)
   ```

7. **Pass `monitor=None`** at the fork-point call site (executor.py:1208-1213):
   ```python
   task_results, remaining, phase_gate_results = execute_phase_tasks(
       tasks=tasks, config=config, phase=phase,
       ledger=ledger, shadow_metrics=shadow_metrics,
       remediation_log=remediation_log,
       tui=tui, sprint_result=sprint_result,
       monitor=None,  # v3.7: synthetic. v3.8: pass monitor for live monitoring.
   )
   ```

#### Acceptance Criteria

- [ ] TUI receives MonitorState with accumulated `output_bytes`, `events_received`, `last_task_id`
- [ ] `stall_status` returns `"active"` (not `"STALLED"`) between tasks
- [ ] `output_bytes` grows across tasks (cumulative, not reset)
- [ ] `events_received` equals task index + 1 (not NDJSON line count)
- [ ] All existing executor tests pass
- [ ] `monitor=None` is backward-compatible (no behavior change)

#### Verification

```bash
uv run pytest tests/sprint/test_executor.py -v
uv run pytest tests/sprint/test_tui.py -v
```

#### Rollback

Revert to ad-hoc MonitorState writes at lines 978-984 and 1042-1048. Remove `monitor` parameter. Remove accumulator initialization. TUI reverts to 3-field ad-hoc updates.

---

### MA-07: Change `gate_rollout_mode` default to "shadow" (= PA-06)

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/models.py:329` |
| **LOC** | 1 modified |
| **Risk** | Low-Medium (behavior change: gate now evaluates in shadow mode by default) |
| **Parallelize with** | Nothing (depends on MA-01 + MA-02) |
| **Dependencies** | MA-01 (turns), MA-02 (output_path) — both must be correct before gate evaluates |

#### Steps

1. **Read** models.py:329 — current:
   ```python
   gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"
   ```

2. **Replace** with:
   ```python
   gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
   ```

3. **Verify** that `--gate-mode off` CLI flag still overrides to "off" for users who want to disable.

#### Acceptance Criteria

- [ ] Default mode is "shadow" (evaluate + record metrics, no blocking)
- [ ] `--gate-mode off` override still works
- [ ] Anti-instinct gate produces non-trivial metrics in shadow mode (not all zeros)
- [ ] Gate does NOT block task execution in shadow mode (executor.py:814-816 returns without side effects only in "off" mode)

#### Verification

```bash
uv run pytest tests/sprint/test_executor.py -v -k "gate or anti_instinct"
uv run pytest tests/sprint/test_models.py -v -k "gate_rollout"
```

#### Rollback

Revert default to `"off"`. Gate reverts to no-evaluation behavior.

---

## 6. Wave 1.5: Invariant Probe Mitigations

### MA-08: Inject task boundary markers in append-mode output

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/executor.py` — inside task loop, after subprocess completes (~line 996) |
| **LOC** | 5 added |
| **Risk** | Negligible |
| **Parallelize with** | MA-09 |
| **Dependencies** | MA-03 (append mode must be active) |

#### Steps

1. **Add** after `_run_task_subprocess` returns (after line 995, before `finished_at`):
   ```python
   # Inject NDJSON task boundary for per-task extraction from append-mode file
   _boundary_path = config.output_file(phase)
   if _boundary_path.exists():
       with open(_boundary_path, "a") as _bf:
           import json as _json
           _bf.write(_json.dumps({
               "type": "task_boundary",
               "task_id": task.task_id,
               "exit_code": exit_code,
           }) + "\n")
   ```

2. **Consider** moving the json import to module level if not already imported.

#### Acceptance Criteria

- [ ] Phase output file contains `{"type":"task_boundary","task_id":"T01.XX",...}` between each task's NDJSON
- [ ] Boundary marker is valid NDJSON (parseable by json.loads)
- [ ] `count_turns_from_output()` at monitor.py:114-141 ignores boundary markers (they don't match assistant-turn pattern)
- [ ] Boundary markers enable future per-task extraction from concatenated file

#### Verification

```bash
uv run pytest tests/sprint/ -v -k "boundary or task_boundary"
```

#### Rollback

Remove boundary injection. Concatenated file still works but lacks task delimiters.

---

### MA-09: Record file offset before task for anti-instinct gate

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/executor.py` — inside task loop |
| **LOC** | 5 added, 2 modified |
| **Risk** | Low |
| **Parallelize with** | MA-08 |
| **Dependencies** | MA-02 (output_path must be wired), MA-03 (append mode) |

#### Steps

1. **Record file size** before task launch (before line 986, after budget debit):
   ```python
   # Record file offset for per-task gate evaluation (INV-004)
   _output_path = config.output_file(phase)
   _pre_task_offset = _output_path.stat().st_size if _output_path.exists() else 0
   ```

2. **Pass offset** to TaskResult (modify construction at lines 1017-1025):
   ```python
   result = TaskResult(
       task=task,
       status=status,
       turns_consumed=turns_consumed,
       exit_code=exit_code,
       started_at=started_at,
       finished_at=finished_at,
       output_bytes=output_bytes,
       output_path=str(config.output_file(phase)),
   )
   # Store offset for gate evaluation
   result._output_offset = _pre_task_offset  # private attr for gate use
   ```

3. **Modify anti-instinct gate** to use offset. At executor.py:826-827, the gate reads the full file. Add offset-aware reading:

   **Option A** (minimal): Pass offset as context to the gate:
   ```python
   # In run_post_task_anti_instinct_hook, after resolving output_path:
   offset = getattr(task_result, '_output_offset', 0)
   if output_path is not None and output_path.exists():
       passed, failure_reason = gate_passed(output_path, ANTI_INSTINCT_GATE, offset=offset)
   ```

   **Option B** (if gate_passed doesn't support offset): Slice the file externally and pass a temp path. This is more complex — prefer Option A if the gate API supports it. If not, defer this task to when the gate API is modified.

#### Acceptance Criteria

- [ ] File offset is recorded before each task launch
- [ ] Anti-instinct gate evaluates only the current task's portion of the output file
- [ ] Gate for task 3 does NOT see tasks 1-2's output patterns (no false positives from prior tasks)
- [ ] Offset is 0 for the first task in a phase (correct)

#### Verification

```bash
uv run pytest tests/sprint/test_executor.py -v -k "anti_instinct"
```

#### Rollback

Remove offset recording. Gate reverts to evaluating the full (growing) file — acceptable if gate patterns are task-agnostic.

---

## 7. Wave 2: Forward-Compatibility Hooks

### MA-10: Add `monitor` parameter passthrough at fork point

| Field | Value |
|---|---|
| **Target** | `src/superclaude/cli/sprint/executor.py:1208-1213` |
| **LOC** | 0 (already done in MA-06 step 7) |
| **Risk** | Negligible |
| **Dependencies** | MA-06 |

This is included in MA-06 step 7 for completeness. The `monitor=None` argument at the fork point is the v3.8 hook. Changing it to `monitor=monitor` enables the full per-task monitor lifecycle.

---

### MA-11: Forward-compatibility tests

| Field | Value |
|---|---|
| **Target** | `tests/sprint/test_monitor_adaptation.py` (NEW file) |
| **LOC** | ~60 test code |
| **Risk** | Negligible (test-only) |
| **Parallelize with** | MA-10 |
| **Dependencies** | MA-04, MA-06 |

#### Steps

1. **Create** `tests/sprint/test_monitor_adaptation.py` with tests:

   - `test_phase_accumulator_harvest_synthetic` — verify accumulation of output_bytes, turns, events
   - `test_phase_accumulator_harvest_monitored` — verify mapping from MonitorState fields
   - `test_phase_accumulator_to_monitor_state_stall_fix` — verify `stall_status == "active"`
   - `test_phase_accumulator_zero_tasks` — verify empty accumulator produces valid MonitorState
   - `test_accumulator_to_monitor_state_roundtrip` — verify fields survive the adapter
   - `test_execute_phase_tasks_with_monitor_none` — verify backward compatibility
   - `test_append_mode_preserves_all_tasks_output` — verify multi-task output not overwritten
   - `test_task_boundary_markers_in_output` — verify boundary JSON present between tasks

#### Acceptance Criteria

- [ ] All tests pass
- [ ] Tests cover: accumulation, adapter, stall fix, backward compat, append mode, boundaries

#### Verification

```bash
uv run pytest tests/sprint/test_monitor_adaptation.py -v
```

---

## 8. Test Plan

### Test Matrix

| Test Category | Tasks Covered | Estimated Tests | Priority |
|---|---|---|---|
| Unit: PhaseAccumulator | MA-04 | 5 tests | P0 |
| Unit: to_monitor_state() adapter | MA-04 | 3 tests | P0 |
| Unit: turns_consumed fix | MA-01 | 2 tests | P0 |
| Unit: output_path wiring | MA-02 | 2 tests | P0 |
| Integration: executor task loop | MA-06 | 4 tests | P0 |
| Integration: append-mode output | MA-03 | 3 tests | P0 |
| Integration: task boundary markers | MA-08 | 2 tests | P1 |
| Integration: gate offset | MA-09 | 2 tests | P1 |
| Integration: gate default shadow | MA-07 | 2 tests | P1 |
| Regression: existing executor | MA-06 | existing suite | P0 |
| Forward-compat: monitor=None | MA-06 | 1 test | P1 |
| **Total** | | **~26 new tests** | |

### Verification Commands

```bash
# Full test suite
uv run pytest tests/sprint/ -v

# Targeted test runs
uv run pytest tests/sprint/test_monitor_adaptation.py -v  # New tests
uv run pytest tests/sprint/test_executor.py -v             # Regression
uv run pytest tests/sprint/test_monitor.py -v              # Monitor functions
uv run pytest tests/sprint/test_models.py -v               # Data model
uv run pytest tests/sprint/test_tui.py -v                  # TUI rendering
```

---

## 9. Dependency Graph

```
MA-01 (turns fix) ──────────┐
                             │
MA-02 (output_path) ────────┼──→ MA-07 (gate default)
                             │
MA-03 (append mode) ────────┤
                             │
MA-04 (PhaseAccumulator) ───┤
                             │
MA-05 (task_output_file) ───┘  (independent, forward-compat)
         │
         ↓
MA-06 (executor integration) ←── depends on MA-01, MA-02, MA-04
         │
         ├──→ MA-08 (task boundary) ←── depends on MA-03
         │
         ├──→ MA-09 (gate offset)  ←── depends on MA-02, MA-03
         │
         └──→ MA-11 (forward-compat tests) ←── depends on MA-04, MA-06
```

### Parallelization Summary

| Wave | Tasks | Parallel? | Estimated LOC |
|---|---|---|---|
| **Wave 0** | MA-01, MA-02, MA-03 | **All 3 parallel** | 4 |
| **Wave 0.5** | MA-04, MA-05 | **Both parallel** | 51 |
| **Wave 1** | MA-06, MA-07 | **Sequential** (MA-06 first) | 36 |
| **Wave 1.5** | MA-08, MA-09 | **Both parallel** | 12 |
| **Wave 2** | MA-10, MA-11 | **Both parallel** | 60 (tests) |
| **Total** | 11 tasks | 5 waves | **~83 prod + ~120 test** |

---

## 10. Risk Register

| ID | Risk | Severity | Probability | Mitigation |
|---|---|---|---|---|
| R1 | Append mode causes Path B to accumulate stale data across phases | Medium | Low | Path B calls `monitor.reset()` which doesn't truncate the file. Verify Path B's isolation_dir copy means each phase gets a fresh output file. |
| R2 | Gate evaluation with offset fails on malformed NDJSON | Low | Low | Gate should handle partial JSON gracefully. Add boundary marker before task start, not just after. |
| R3 | PhaseAccumulator.to_monitor_state() drift from MonitorState | Low | Medium | Add test that verifies all 12 MonitorState fields are either explicitly set or at documented defaults. |
| R4 | Existing tests assume turns_consumed == 0 | Medium | Medium | Search for assertions on turns_consumed in test suite. Update mock expectations. |
| R5 | Budget reconciliation changes with non-zero turns | Medium | Low | Budget logic at executor.py:1007-1015 already handles actual > pre_allocated. Verify math with real turn counts. |
| R6 | Shadow-mode gate produces unexpected log noise | Low | Medium | Shadow mode logs via `_anti_instinct_logger.info()` at executor.py:835. Acceptable for v3.7; add log-level control in v3.8 if noisy. |

### Overall Risk Assessment: **LOW**

- No threading changes (debate ruled out Strategy A for v3.7)
- No file naming changes (append mode, not per-task files)
- No downstream consumer changes (phase-N-output.txt preserved)
- No TUI rendering changes (MonitorState adapter is transparent)
- Core changes are 4 LOC in Wave 0 (trivial, independently testable)
- Largest change is MA-06 (~35 LOC) modifying the executor task loop

---

## Summary

This workflow implements the adversarial-debate-validated strategy for v3.7:

1. **Fix the data foundation** (Wave 0): PA-04 turns, PA-05 output_path, append mode — 4 LOC, all parallel
2. **Build the adapter** (Wave 0.5): PhaseAccumulator with both synthetic and monitored harvest methods — 51 LOC, forward-compatible
3. **Wire the executor** (Wave 1): Replace ad-hoc MonitorState with accumulator, enable shadow gate — 36 LOC, medium risk
4. **Close invariant gaps** (Wave 1.5): Task boundaries and gate offset — 12 LOC, low risk
5. **Test forward compatibility** (Wave 2): Verify v3.8 migration path — 60 LOC tests

**Total: ~83 production LOC, ~120 test LOC, 11 tasks across 5 waves.**

The v3.8 migration to full per-task OutputMonitor lifecycle requires only ~23 additional LOC (6 call-site changes in executor.py) with zero TUI changes.

---

*End of implementation workflow.*
