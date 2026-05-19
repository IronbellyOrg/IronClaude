# C4 QA Input Bundle

## Modified production file

**Path:** `src/superclaude/cli/sprint/executor.py` (per-task branch — between former L1264 and L1266; line numbers shifted +1 after insertion)

**Before (per-task branch):**
```python
            tasks = _parse_phase_tasks(phase, config)
            if tasks:
                started_at = datetime.now(timezone.utc)
                # Signal TUI that this phase is now active
                tui.update(sprint_result, MonitorState(), phase)
```

**After:**
```python
            tasks = _parse_phase_tasks(phase, config)
            if tasks:
                started_at = datetime.now(timezone.utc)
                logger.write_phase_start(phase, started_at)
                # Signal TUI that this phase is now active
                tui.update(sprint_result, MonitorState(), phase)
```

## Reference line untouched

`src/superclaude/cli/sprint/executor.py:1328` (per-phase fallback branch, unchanged):
```python
                logger.write_phase_start(phase, started_at)
```
This is the byte-exact pattern the C4 fix mirrors.

## New test function

**Path:** `tests/sprint/test_regression_gaps.py::TestSprintLoggerPhaseStart::test_phase_start_emitted_for_per_task_branch`

**Module-level import added:** `TaskEntry` to the existing `from superclaude.cli.sprint.models import (...)` block.

**Assertions:**
1. At least one event in `config.execution_log_jsonl` has `event == "phase_start"`.
2. The `phase_start` event includes fields `phase`, `phase_name`, `phase_file`, `timestamp` (matching `logging_.py:59-69` schema).
3. `phase_start.phase == 1`.
4. `phase_start` appears in event-order BEFORE `phase_complete` (when phase_complete is present).

Mocks (so no real subprocess spawns):
- `superclaude.cli.sprint.executor._parse_phase_tasks` → `[fake_task]`
- `superclaude.cli.sprint.executor.execute_phase_tasks` → `([], [], [])`
- `superclaude.cli.sprint.executor.run_post_phase_wiring_hook` → passthrough
- `superclaude.cli.sprint.executor.shutil.which` → `/usr/bin/claude`
- `superclaude.cli.sprint.notify._notify` → no-op

## pytest results summary

**Result:** PASSED (4/4, 0.13s)

Raw: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-4-c4-pytest-output.txt`
Summary: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-4-c4-summary.md`

## QA scope

Only C4 scope — items 4.1, 4.2, 4.3. The watchdog block at executor.py:1365-1404, the `_run_task_subprocess` body at executor.py:1086-1115, the dataclass at models.py:369, the C3 reconciliation at executor.py:86, and any `config.py`/`commands.py` lines are NOT in scope. The only production line touched in Phase 4 is the single-line insertion in the per-task branch.

## Test author notes

- The task file's Step 4.2 prompt suggested `TaskEntry(task_id, phase_number, title, description, tier)` but the actual TaskEntry dataclass at `src/superclaude/cli/sprint/models.py:25-37` accepts only `(task_id, title, description, dependencies, command, classifier)`. The test was corrected after first run to use the real fields. This is a research-vs-actual drift (Researcher 1 captured the dataclass correctly; Step 4.2 prompt picked up wrong field names somewhere).
