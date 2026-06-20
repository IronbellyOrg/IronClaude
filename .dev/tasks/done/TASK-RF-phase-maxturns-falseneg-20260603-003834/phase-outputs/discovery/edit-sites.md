# Edit-Site Confirmation (Phase 1, Step 1.5)

Verified verbatim against live source on branch `fix/per-task-error-max-turns-falseneg`
(HEAD `e101951a`) on 2026-06-03. **No line-number drift** from research files 01/04
— every cited anchor is exactly where the research said it would be.

---

## Edit Site 1 — TaskStatus enum (Phase 2)

**File:** `src/superclaude/cli/sprint/models.py`
**Lines:** 39-53

```python
class TaskStatus(Enum):
    """Outcome status for a single task within a phase."""

    PASS = "pass"
    FAIL = "fail"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"

    @property
    def is_success(self) -> bool:
        return self == TaskStatus.PASS

    @property
    def is_failure(self) -> bool:
        return self in (TaskStatus.FAIL, TaskStatus.INCOMPLETE)
```

**Precedent to mirror** — `PhaseStatus.PASS_RECOVERED` at `models.py:219`:

```python
    PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success
```

---

## Edit Site 2 — per-task exit-code switch (Phase 3.2)

**File:** `src/superclaude/cli/sprint/executor.py`
**Lines:** 1014-1020 (inside `execute_phase_tasks`; `config`, `phase`, `task` all in scope)

```python
        # Determine task status from exit code
        if exit_code == 0:
            status = TaskStatus.PASS
        elif exit_code == 124:
            status = TaskStatus.INCOMPLETE
        else:
            status = TaskStatus.FAIL
```

Only the `else:` branch (line 1019-1020) is edited. The `== 0` and `== 124` branches stay UNCHANGED.

---

## Edit Site 3 — phase aggregation (Phase 4.1)

**File:** `src/superclaude/cli/sprint/executor.py`
**Line:** 1278

```python
                all_passed = all(r.status == TaskStatus.PASS for r in task_results)
                status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR
```

Only line 1278's `r.status == TaskStatus.PASS` → `r.status.is_success`. Line 1279 and the
`exit_code = 0 if all_passed else 1` logic stay UNCHANGED.

---

## Edit Site 4 — aggregate_task_results count (Phase 4.2, parallel surface)

**File:** `src/superclaude/cli/sprint/executor.py`
**Line:** 323 (function `aggregate_task_results` @296)

```python
    report.tasks_passed = sum(1 for r in task_results if r.status == TaskStatus.PASS)
```

Only line 323's predicate → `r.status.is_success`. The `tasks_failed`/`tasks_incomplete`/`tasks_skipped` counts stay UNCHANGED.

---

## Supporting anchors

- **`config.task_output_file(phase, task)`** — `models.py:502-503`, returns
  `results_dir / f"phase-{phase.number}-task-{task.task_id}-output.txt"`. Reachable at the switch.
- **`detect_error_max_turns` import** — **YES, already imported** in executor.py at line 37:
  `from .monitor import OutputMonitor, detect_error_max_turns, detect_prompt_too_long`
- **Helper insertion anchor** — `_classify_from_result_file` at `executor.py:1774`;
  `_determine_phase_status` (per-phase recovery precedent) at `executor.py:2067`.

## Drift note

None. Research file 04 cited switch @1014-1020 and aggregation @1278; both are exact.
Research file 01 cited models.py TaskStatus @39-54 and task_output_file @502-503; both exact.
