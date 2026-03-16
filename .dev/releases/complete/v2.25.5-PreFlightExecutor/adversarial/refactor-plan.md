# Refactor Plan: pass_no_report Fix via Executor Pre-Write

## Base Solution: Option D (revised) -- Executor Pre-Write

Write a preliminary result file BEFORE `_determine_phase_status()` runs, guarded to exit_code==0 only.

## Implementation Tasks

### Task 1: Add `_write_preliminary_result()` function
**File**: `src/superclaude/cli/sprint/executor.py`
**Location**: After `_write_executor_result_file()` (after L969)
**Risk**: LOW

```python
def _write_preliminary_result(
    config: SprintConfig,
    phase: Phase,
    exit_code: int,
    monitor_state: MonitorState,
    started_at: datetime,
    finished_at: datetime,
) -> None:
    """Write a preliminary result file for _determine_phase_status() to read.

    ONLY called when exit_code == 0. For non-zero exits, the existing
    classification logic in _determine_phase_status() handles context
    exhaustion, checkpoint recovery, and error detection without needing
    a result file.

    This file is overwritten by _write_executor_result_file() after
    status determination, which uses the actual PhaseStatus for richer
    content.
    """
    duration = (finished_at - started_at).total_seconds()
    content = (
        "---\n"
        f"phase: {phase.number}\n"
        "status: PASS\n"
        "---\n"
        "\n"
        f"# Phase {phase.number} -- Preliminary Executor Result\n"
        "\n"
        f"**Source**: executor (preliminary, pre-classification)\n"
        f"**Exit code**: {exit_code}\n"
        f"**Output bytes**: {monitor_state.output_bytes}\n"
        f"**Duration**: {duration:.1f}s\n"
        "\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )
    result_path = config.result_file(phase)
    try:
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(content)
    except OSError:
        pass  # Non-fatal
```

### Task 2: Insert preliminary write call in `execute_sprint()`
**File**: `src/superclaude/cli/sprint/executor.py`
**Location**: Between L694 (shutdown check) and L696 (`_determine_phase_status`)
**Risk**: LOW

Current code (L696-717):
```python
                # Determine phase status
                status = _determine_phase_status(
                    exit_code=exit_code,
                    result_file=config.result_file(phase),
                    ...
                )

                # Write executor result file for downstream consumers.
                # Written AFTER status determination to avoid circularity.
                # Overwrites any agent-written file -- executor is authoritative.
                _write_executor_result_file(
                    config=config,
                    ...
                )
```

New code:
```python
                # Write preliminary result for exit_code==0 so
                # _determine_phase_status finds a result file with
                # EXIT_RECOMMENDATION: CONTINUE instead of falling
                # through to PASS_NO_REPORT.
                # Guard: non-zero exits must NOT get a preliminary file
                # because _determine_phase_status has specialized logic
                # for context exhaustion, checkpoint recovery, etc.
                if exit_code == 0:
                    _write_preliminary_result(
                        config=config,
                        phase=phase,
                        exit_code=exit_code,
                        monitor_state=monitor.state,
                        started_at=started_at,
                        finished_at=finished_at,
                    )

                # Determine phase status
                status = _determine_phase_status(
                    exit_code=exit_code,
                    result_file=config.result_file(phase),
                    ...
                )

                # Write authoritative executor result file.
                # Overwrites the preliminary file with richer content
                # including the actual PhaseStatus.
                _write_executor_result_file(
                    config=config,
                    ...
                )
```

### Task 3: Update comment at L706-708
**File**: `src/superclaude/cli/sprint/executor.py`
**Risk**: NONE

Change:
```python
                # Write executor result file for downstream consumers.
                # Written AFTER status determination to avoid circularity.
                # Overwrites any agent-written file -- executor is authoritative.
```

To:
```python
                # Write authoritative executor result file for downstream consumers.
                # Overwrites the preliminary file (if written) with the actual
                # PhaseStatus. Executor is authoritative for all result files.
```

### Task 4: Add unit test for preliminary write
**File**: `tests/sprint/test_phase8_halt_fix.py` (or new test file)
**Risk**: LOW

Test cases:
1. `exit_code=0, no agent result file` -> `_determine_phase_status` returns `PASS` (not `PASS_NO_REPORT`)
2. `exit_code!=0, no preliminary file written` -> existing behavior unchanged (ERROR, INCOMPLETE, etc.)
3. `exit_code=0, agent also wrote result file` -> preliminary file exists, agent file overwritten, classifier reads preliminary -> PASS
4. `exit_code!=0, detect_prompt_too_long=True` -> no preliminary file, existing INCOMPLETE logic works

### Task 5 (Optional, Defense-in-Depth): Add result-file instruction to agent prompt
**File**: `src/superclaude/cli/sprint/executor.py`, L461-466
**Risk**: LOW

```python
prompt = (
    f"Execute task {task.task_id}: {task.title}\n"
    f"From phase file: {phase.file}\n"
    f"Description: {task.description}\n"
    f"\nWhen all tasks are complete, write: {config.result_file(phase)}\n"
    f"Include: EXIT_RECOMMENDATION: CONTINUE (or HALT if any task failed)\n"
)
```

This is optional and provides defense-in-depth. The executor's preliminary file already ensures PASS classification. If the agent also writes a result file before the executor, `_determine_phase_status` would read the agent's file (which exists at the same path). The executor's post-hoc write overwrites it for downstream consumers.

## Execution Order

| # | Task | Blocked By | Risk |
|---|------|-----------|------|
| 1 | Add `_write_preliminary_result()` | None | LOW |
| 2 | Insert call in `execute_sprint()` | Task 1 | LOW |
| 3 | Update comment | Task 2 | NONE |
| 4 | Add unit tests | Tasks 1-2 | LOW |
| 5 | Optional: prompt injection | None (independent) | LOW |

## Not Implemented

- **Option B**: `execute_phase_tasks()` not wired into main loop. Too large for targeted fix.
- **Option C**: Accepting `pass_no_report` as permanent loses telemetry signal and false-positive detection.
