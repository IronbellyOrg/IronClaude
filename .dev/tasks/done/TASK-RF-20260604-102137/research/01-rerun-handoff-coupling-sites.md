# File Inventory: PASS_RECOVERED rerun/handoff coupling sites

Status: Complete
Date: 2026-06-04

## Scope and tree checked

Repository root: `/config/workspace/IronClaude`.

I checked the current `master` tree for the requested source files. `git diff --name-only master -- ...` showed `src/superclaude/cli/sprint/rerun_tasks.py` and `src/superclaude/cli/sprint/models.py` do not differ from `master` for this branch, while `handoff.py` and `executor.py` do differ from `master`; for those two files, master-tree line evidence below comes from `git show master:<path>`.

The requested `/config/workspace/IronClaude/src/superclaude/cli/sprint/resume/planner.py` is absent on `master` and in the working tree. Repository-wide search found no `_coerce_task_status` symbol under `/config/workspace/IronClaude/src`; that mirror source is therefore Unverified/absent in this tree.

## 1. `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py`

### Imports

`TaskStatus` is already imported. Current master-tree code at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:40-42`:

```python
from .debug_logger import debug_log
from .models import PhaseResult, SprintConfig, TaskResult, TaskStatus
from .recovery import (
```

### `_rerun_targets_passed(phase_result_json, targets)` full body and read path

Current master-tree full function body at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1165-1177`:

```python
def _rerun_targets_passed(phase_result_json: Path, targets: list[str]) -> bool:
    """True iff every ``targets`` task is recorded PASS in the rerun's result JSON."""
    try:
        data = json.loads(phase_result_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    status_by_id = {}
    for entry in data.get("task_results", []) if isinstance(data, dict) else []:
        task = entry.get("task") if isinstance(entry, dict) else None
        tid = task.get("task_id") if isinstance(task, dict) else None
        if tid:
            status_by_id[tid] = entry.get("status")
    return bool(targets) and all(status_by_id.get(t) == "pass" for t in targets)
```

Critical trace: `status_by_id` contains raw JSON strings, not `TaskStatus` enum members. The read is `json.loads(phase_result_json.read_text(...))` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1168`; each value is assigned directly from `entry.get("status")` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1176`. The persisted writer serializes task results via `tr.to_dict()` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:2671`, and `TaskResult.to_dict()` emits `"status": self.status.value` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:207`. Therefore a recovered-pass rerun persists as raw string `"pass_recovered"`, and the current `== "pass"` predicate rejects it.

Serialization/caller path feeding this file:

- Per-task execution creates `task_results` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1730-1741`.
- The aggregate already counts `PASS_RECOVERED` as success via `r.status.is_success` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:353-355`; comments at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1750-1751` explicitly say `PASS_RECOVERED` is counted as success there.
- The phase JSON writer persists `"task_results": [tr.to_dict() for tr in result.task_results]` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:2671` to `config.phase_result_json(phase)`, whose path is `results_dir / f"phase-{phase.number}-result.json"` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:714-715`.
- `TaskResult.to_dict()` writes string `.value` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:207`; `TaskResult.from_dict()` can deserialize `"pass_recovered"` back to `TaskStatus.PASS_RECOVERED` via `TaskStatus(data["status"])` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:231`.

Caller and consequence: `run_rerun_tasks()` sets `rerun_succeeded = rerun_error is None and _rerun_targets_passed(...)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1369-1372`. The `if rerun_succeeded and merge_back:` block at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1374-1430` re-hashes the source, builds a `RecoveryBundle`, writes the `task-results.json` sidecar from refreshed rerun `task_results`, calls `merge_recovery_bundle(...)`, finalizes source checkboxes, clears restore state, echoes `Rerun merged...`, and sets `exit_code = 0`. If the predicate returns false, the else path sets `exit_code = 1` and echoes `Rerun did not bring all target tasks to PASS; merge skipped.` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1431-1444`; the `finally` path then restores checkboxes if `restore_info` remains set at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1467-1472`. `merge_recovery_bundle()` rewrites canonical `phase-N-result.json` with sidecar task results at `/config/workspace/IronClaude/src/superclaude/cli/sprint/recovery.py:601-669`; skipping merge means canonical results stay stale and the rerun does not finalize.

Severity/blast radius: CRITICAL. This gates merge-back and successful exit for rerun-tasks. A target recorded as `"pass_recovered"` is a success according to `TaskStatus.is_success`, but current code treats it as not passed, skips merge-back, restores source checkboxes, and leaves canonical result JSON unrefreshed.

Recommended fix: fix this site. Because the value is a raw JSON value, coerce before checking success, with a None/invalid-safe helper mirroring the absent `_coerce_task_status` pattern:

```python
def _is_success_task_status(value: object) -> bool:
    try:
        status = value if isinstance(value, TaskStatus) else TaskStatus(value)
    except (TypeError, ValueError):
        return False
    return status.is_success

return bool(targets) and all(_is_success_task_status(status_by_id.get(t)) for t in targets)
```

### `last_pass` tracking in `_print_investigation_summary`

Current master-tree code at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1187-1202`:

```python
view = _load_phase_result_view(phase_result_json)
last_pass = ""
recoverable: list[str] = []
terminal: list[str] = []
for tr in view.task_results:
    if tr.status is TaskStatus.PASS:
        last_pass = tr.task.task_id
    elif tr.status is TaskStatus.FAIL_RECOVERABLE:
        recoverable.append(tr.task.task_id)
    elif tr.status is TaskStatus.FAIL_TERMINAL:
        terminal.append(tr.task.task_id)
click.echo("  investigation pointer (from phase-N-result.json):")
click.echo(f"    last PASS task : {last_pass or '(none recorded)'}")
click.echo(f"    recoverable    : {', '.join(recoverable) or '(none)'}")
click.echo(f"    terminal fails : {', '.join(terminal) or '(none)'}")
click.echo(f"    nominated      : {', '.join(nominated)}")
```

Here `tr.status` is a `TaskStatus` enum, not a raw string. `_print_investigation_summary()` calls `_load_phase_result_view()` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1187`; `_load_phase_result_view()` appends `TaskResult.from_dict(entry)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1155-1159`; `TaskResult.from_dict()` sets `status=TaskStatus(data["status"])` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:231`.

This appears display-only. `_print_investigation_summary()` only emits operator investigation output at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1198-1202`; in `run_rerun_tasks()` it is called from the dry-run branch at `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1317-1325`. It does not gate rerun execution, merge-back, or exit status.

Severity/blast radius: LOW. A `PASS_RECOVERED` task is omitted from the `last PASS task` pointer, which can mislead operator triage but does not change control flow.

Recommended fix: fix for consistency, but it is lower priority than the merge-back gate. Since `tr.status` is already a `TaskStatus`, use the enum property directly:

```python
if tr.status.is_success:
    last_pass = tr.task.task_id
```

If defensive coercion is desired for future malformed views, use the same helper above and call `_is_success_task_status(tr.status)`.

## 2. `/config/workspace/IronClaude/src/superclaude/cli/sprint/handoff.py`

### Imports and current predicate

`TaskStatus` is already imported in the master tree. Current master-tree code at `/config/workspace/IronClaude/src/superclaude/cli/sprint/handoff.py:18-20`:

```python
import json

from .models import GateOutcome, HandoffRecord, SprintConfig, TaskStatus
```

Current master-tree `is_validated_success(record)` body at `/config/workspace/IronClaude/src/superclaude/cli/sprint/handoff.py:23-40`:

```python
def is_validated_success(record: HandoffRecord) -> bool:
    """Resume skip predicate (H5 item 1): a *validated successful* record.

    Returns True ONLY when the task both PASSed and its gate succeeded — i.e.
    ``record.status == TaskStatus.PASS.value`` AND
    ``GateOutcome(record.gate_outcome).is_success``. Mere file existence is
    unsafe: ``FAIL_*``/``INCOMPLETE``/``SKIPPED`` tasks (and PASS-with-gate-fail)
    also leave records behind, and resume must NOT skip those. Per the H4 schema
    fix, ``gate_outcome`` is always the ``GateOutcome`` enum's ``.value`` string
    (never None, never a dict), so there is no None/absent-gate branch to decide.
    """
    if record.status != TaskStatus.PASS.value:
        return False
    try:
        return GateOutcome(record.gate_outcome).is_success
    except ValueError:
        # Defensive: an unrecognized gate_outcome string is not a validated success.
        return False
```

`record.status` is a string here. `HandoffRecord.status` is declared as `str` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:294-298`; `HandoffRecord.to_dict()` writes `"status": self.status` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:313-318`; `HandoffRecord.from_dict()` reloads `status=data.get("status", "")` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:337-342`. `HandoffRecord.from_task_result()` derives it from `result.status.value` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:369-374`, so a recovered task writes and reloads `"pass_recovered"`.

Consumers/callers:

- `executor.py` imports `is_validated_success` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:24-27` in the master tree.
- Parallel task execution reads a handoff record and skips the task only if `_prior is not None and is_validated_success(_prior)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1097-1105`. The skip result is synthesized with `status=TaskStatus.PASS`, `turns_consumed=0`, `exit_code=0`, and `gate_outcome=GateOutcome.PASS` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1105-1115`.
- Sequential task execution has the same resume skip check at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1259-1279` and appends the same PASS/PASS zero-turn result at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1279-1291`.
- Handoff records are written from current task results through `HandoffRecord.from_task_result(...)` and `handoff_store.write(...)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1154-1161` for parallel execution, and the sequential path follows the same store semantics later in `execute_phase_tasks` (not quoted here because researcher-2 owns test fixture coverage).

Severity/blast radius: HIGH. This does not gate rerun merge-back directly, but it is a resume correctness predicate. A validated `PASS_RECOVERED` handoff with gate pass will not be skipped on resume; it will be re-run, consuming budget and potentially causing duplicate side effects. It affects both parallel and sequential resume paths.

Recommended fix: fix this site. Because `record.status` is a serialized string, coerce to `TaskStatus` with None/invalid safety and then use `.is_success`; also catch `TypeError` for None/non-string gate values:

```python
try:
    status = (
        record.status
        if isinstance(record.status, TaskStatus)
        else TaskStatus(record.status)
    )
    gate = GateOutcome(record.gate_outcome)
except (TypeError, ValueError):
    return False
return status.is_success and gate.is_success
```

This accepts both `"pass"` and `"pass_recovered"` while preserving the existing requirement that the gate outcome is successful.

## 3. `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py`

`TaskStatus.is_success` already defines the PASS family. Current code at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:46-58`:

```python
class TaskStatus(Enum):
    """Outcome status for a single task within a phase."""

    PASS = "pass"
    PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success
    FAIL_TERMINAL = "fail"
    FAIL_RECOVERABLE = "fail_recoverable"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"

    @property
    def is_success(self) -> bool:
        return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)
```

`TaskResult` serializes status to a string and deserializes it back to an enum:

- Field type is `status: TaskStatus = TaskStatus.SKIPPED` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:179-180`.
- `to_dict()` emits `"status": self.status.value` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:198-208`.
- `from_dict()` reconstructs `status=TaskStatus(data["status"])` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:219-231`.

Therefore persisted `"pass_recovered"` round-trips as `TaskStatus.PASS_RECOVERED` when code uses `TaskResult.from_dict()`, but remains a raw string when code reads JSON dictionaries directly.

`HandoffRecord.status` is string-typed and string-round-tripped:

- `status: str = ""` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:294-298`.
- `to_dict()` emits `"status": self.status` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:313-318`.
- `from_dict()` reloads `status=data.get("status", "")` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:337-342`.
- `from_task_result()` stores `status=result.status.value` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:369-374`.

No model fix is needed for this task; the model layer already has the desired success taxonomy and serialization semantics. The fix sites should consume that taxonomy instead of comparing to the singleton string/value for PASS only.

## 4. `/config/workspace/IronClaude/src/superclaude/cli/sprint/resume/planner.py`

Unverified/absent. The requested file does not exist on current `master` (`git ls-tree -r --name-only master -- src/superclaude/cli/sprint` lists no `resume/` directory or `planner.py`) and does not exist in the working tree. Repository-wide search under `/config/workspace/IronClaude/src` found no `_coerce_task_status` or `coerce_task_status` symbol. I could not show `_coerce_task_status` from this tree.

Recommended mirror pattern despite absence: use a local helper that accepts either a `TaskStatus` enum or a serialized value, and returns `None`/`False` on `None`, unknown strings, or invalid types instead of raising:

```python
def _coerce_task_status(value: object) -> TaskStatus | None:
    if isinstance(value, TaskStatus):
        return value
    try:
        return TaskStatus(value)
    except (TypeError, ValueError):
        return None
```

Then success predicates should use:

```python
status = _coerce_task_status(value)
return status is not None and status.is_success
```

## Fix-site summary

The task SHOULD fix all three candidate predicate sites:

1. CRITICAL: `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1177` (`status_by_id.get(t) == "pass"`) because it gates rerun merge-back and canonical result refresh.
2. HIGH: `/config/workspace/IronClaude/src/superclaude/cli/sprint/handoff.py:34` (`record.status != TaskStatus.PASS.value`) because it controls validated-success resume skipping for both parallel and sequential task execution.
3. LOW: `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1192` (`tr.status is TaskStatus.PASS`) because it is display-only investigation output, but it should be corrected for consistency and operator accuracy.

Status: Complete

Summary: The main bug is not in `TaskStatus`; it is in consumers that bypass or underuse `TaskStatus.is_success`. `_rerun_targets_passed()` reads raw JSON strings and must coerce before `.is_success`. `is_validated_success()` reads a string `HandoffRecord.status` and must do the same. The investigation summary receives enum statuses via `TaskResult.from_dict()` and can use `tr.status.is_success` directly.
