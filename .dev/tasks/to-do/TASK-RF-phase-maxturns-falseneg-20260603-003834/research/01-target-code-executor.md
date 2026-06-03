# Research: Target Code (File Inventory / Production Code to Edit)

- **Topic type:** File Inventory / Target Code
- **Scope:** `/config/workspace/IronClaude/src/superclaude/cli/sprint/{executor.py, models.py, config.py}`
- **Focus:** Exact current state of code that must change to fix a per-task `error_max_turns` false-negative phase failure.
- **Status:** Complete
- **Date:** 2026-06-03

## Context (from REPORT.md)

Phase 6 logged `error`/exit 1 because task T06.15 hit the 100-turn budget
(`num_turns:101`, `subtype:"error_max_turns"`, `is_error:true`) AFTER completing
its work. The per-task classifier maps any non-zero/non-124 exit to
`TaskStatus.FAIL`; phase aggregation then forces `PhaseStatus.ERROR` because
not every task is `PASS`. The per-PHASE path (`_determine_phase_status`) already
has recovery (reclassify `error_max_turns → INCOMPLETE`, checkpoint →
`PASS_RECOVERED`); the per-TASK loop has neither.

---

## 1. `execute_phase_tasks` per-task loop — `executor.py:927-1073`

**Signature** (`executor.py:927-940`):
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
) -> tuple[list[TaskResult], list[str], list[TrailingGateResult]]:
```

**Subprocess dispatch** (`executor.py:1001-1012`) — both branches return the
SAME 3-tuple `(exit_code, turns_consumed, output_bytes)`; no output path is
returned:
```python
        # Spawn subprocess for this task
        if _subprocess_factory is not None:
            exit_code, turns_consumed, output_bytes = _subprocess_factory(
                task, config, phase
            )
        else:
            # Default: delegate to ClaudeProcess (real execution)
            exit_code, turns_consumed, output_bytes = _run_task_subprocess(
                task, config, phase
            )

        finished_at = datetime.now(timezone.utc)
```

**THE PER-TASK STATUS BLOCK — `executor.py:1014-1020`** (verbatim; the exact
edit site). The live code spans 1014-1020 (comment @1014, switch @1015-1020);
REPORT.md cited it as "1013-1020" / "1016-1020" — same block:
```python
        # Determine task status from exit code
        if exit_code == 0:
            status = TaskStatus.PASS
        elif exit_code == 124:
            status = TaskStatus.INCOMPLETE
        else:
            status = TaskStatus.FAIL
```
A pure exit-code switch with NO output-file inspection and NO `error_max_turns`
recovery. The `else` branch (any non-zero, non-124 exit) blanket-maps to
`TaskStatus.FAIL`. T06.15's `error_max_turns` exit lands here.

**Local variables IN SCOPE at line 1014-1020** (from reading loop body 971-1040):
| Variable | Source | Line |
|---|---|---|
| `task` | loop var `for i, task in enumerate(tasks)` | 971 |
| `i` | loop index | 971 |
| `started_at` | `datetime.now(...)` at top of iteration | 972 |
| `exit_code` | unpacked from subprocess call | 1003 / 1008 |
| `turns_consumed` | unpacked from subprocess call | 1003 / 1008 |
| `output_bytes` | unpacked from subprocess call | 1003 / 1008 |
| `finished_at` | `datetime.now(...)` | 1012 |
| `config` | function parameter (`SprintConfig`) | 929 |
| `phase` | function parameter | 930 |
| `ledger` | function parameter | 931 |

**KEY FINDING (answers the open question):** `config`, `phase`, and `task` are
ALL in scope at line 1014-1020. The per-task on-disk output file path is
**fully recoverable INSIDE the classification block WITHOUT changing
`_run_task_subprocess`'s return signature** — just call
`config.task_output_file(phase, task)` (see §3). The path does NOT need to be
threaded through the return tuple. REPORT.md §A speculated the signature might
need to change; that thread-through is NOT required.

**`TaskResult` construction** (`executor.py:1032-1040`) — `TaskResult` has an
`output_path: str = ""` field (models.py:175) that is currently NOT populated
here; a fix could set it for traceability:
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

---

## 2. `_run_task_subprocess` — `executor.py:1076-1115`

**Signature & return type** (`executor.py:1076-1080`):
```python
def _run_task_subprocess(
    task: TaskEntry,
    config: SprintConfig,
    phase,
) -> tuple[int, int, int]:
```
Returns `tuple[int, int, int]` = `(exit_code, turns, output_bytes)`. Turn
counting is stubbed: the middle element is hard-coded `0`
(`# Turn counting is wired separately in T02.06`).

**It DOES know the per-task output path on disk** (`executor.py:1101, 1112`):
```python
        output_file=config.task_output_file(phase, task),   # line 1101
        error_file=config.task_error_file(phase, task),     # line 1102
        ...
    proc.start()
    proc.wait()
    exit_code = proc._process.returncode if proc._process else -1
    output_path = config.task_output_file(phase, task)       # line 1112
    output_bytes = output_path.stat().st_size if output_path.exists() else 0
    # Turn counting is wired separately in T02.06
    return (exit_code if exit_code is not None else -1, 0, output_bytes)   # line 1115
```
The path is computed via `config.task_output_file(phase, task)` (called twice,
1101 and 1112) but the resolved `output_path` is **discarded** — only its byte
size is returned, not the path.

**Recoverability verdict:** The same helper call
`config.task_output_file(phase, task)` is available to the caller
(`execute_phase_tasks`) because `config`, `phase`, `task` are all in caller
scope. **No return-signature change is required.** (Optional heavier
alternative: extend the return tuple to add `output_path` and update both the
real fn and the `_subprocess_factory` test contract @954/@1003 — unnecessary.)

---

## 3. Path helpers — actually on `SprintConfig` in `models.py` (NOT `config.py`)

NOTE: there IS a separate `config.py` (it holds `parse_tasklist`, imported at
`executor.py:1125`), but the path helpers and `max_turns`/`results_dir` live on
`SprintConfig` in **`models.py`**.

**`max_turns`** (`models.py:362`): `max_turns: int = 100` — the budget T06.15
overran (matches REPORT.md `**Max turns**: 100` / `num_turns:101`).

**`results_dir`** (`models.py:478-480`):
```python
    @property
    def results_dir(self) -> Path:
        return self.release_dir / "results"
```

**Per-phase output** (`models.py:496-497`):
```python
    def output_file(self, phase: Phase) -> Path:
        return self.results_dir / f"phase-{phase.number}-output.txt"
```

**PER-TASK output helper (the one the fix needs) — `models.py:502-503`**:
```python
    def task_output_file(self, phase: Phase, task: "TaskEntry") -> Path:
        return self.results_dir / f"phase-{phase.number}-task-{task.task_id}-output.txt"
```
Sibling error file (`models.py:505-506`):
```python
    def task_error_file(self, phase: Phase, task: "TaskEntry") -> Path:
        return self.results_dir / f"phase-{phase.number}-task-{task.task_id}-errors.txt"
```

**Exact on-disk path for T06.15:** with `phase.number == 6` and
`task.task_id == "T06.15"`:
`<release_dir>/results/phase-6-task-T06.15-output.txt`
— exactly matches the path REPORT.md cites at line 49. Confirmed.

**Recovery primitive to call on that path** — `detect_error_max_turns`
(`monitor.py:37`, in researcher-02's scope; cited here because the per-task fix
must invoke it):
```python
def detect_error_max_turns(output_path: Path) -> bool:
    """Check if the last NDJSON line indicates budget exhaustion. ..."""
```
Takes a `Path`, scans the last non-empty NDJSON line for
`"subtype":"error_max_turns"`, returns `bool`. So the fix at 1014-1020 can do:
`detect_error_max_turns(config.task_output_file(phase, task))`.

---

## 4. `models.py` enums

**`TaskStatus` — FULL enum (`models.py:39-53`)**:
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
**FINDING:** `TaskStatus` has **NO `PASS_RECOVERED` equivalent** and no
"completed-but-exited-non-zero" member. Only PASS/FAIL/INCOMPLETE/SKIPPED.
`is_success` is strictly `== PASS`. `is_failure` includes BOTH `FAIL` and
`INCOMPLETE`. Critical implication: today's `INCOMPLETE` (exit 124) is
`is_failure == True` — so reclassifying T06.15 to `INCOMPLETE` would still NOT
make it pass under the current phase aggregation, which checks `== PASS`
directly (see §5). To fix the false negative, the task builder must EITHER
(a) add a new `TaskStatus` member (e.g. `PASS_RECOVERED`/`PASS_MAX_TURNS`) that
`is_success` treats as success, OR (b) change the aggregation to use
`r.status.is_success` AND make the reclassified status report success. A bare
`INCOMPLETE` reclassification alone is insufficient.

**`PhaseStatus` — FULL enum (`models.py:211-269`)**:
```python
class PhaseStatus(Enum):
    """Lifecycle of a single phase."""

    PENDING = "pending"
    RUNNING = "running"
    PASS = "pass"
    PASS_NO_SIGNAL = "pass_no_signal"
    PASS_NO_REPORT = "pass_no_report"
    PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success
    PREFLIGHT_PASS = (
        "preflight_pass"  # completed by preflight execution (python/skip mode)
    )
    PASS_MISSING_CHECKPOINT = "pass_missing_checkpoint"
    INCOMPLETE = "incomplete"
    HALT = "halt"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"

    @property
    def is_terminal(self) -> bool:
        return self in (
            PhaseStatus.PASS, PhaseStatus.PASS_NO_SIGNAL, PhaseStatus.PASS_NO_REPORT,
            PhaseStatus.PASS_RECOVERED, PhaseStatus.PREFLIGHT_PASS,
            PhaseStatus.PASS_MISSING_CHECKPOINT, PhaseStatus.INCOMPLETE,
            PhaseStatus.HALT, PhaseStatus.TIMEOUT, PhaseStatus.ERROR,
            PhaseStatus.SKIPPED,
        )

    @property
    def is_success(self) -> bool:
        return self in (
            PhaseStatus.PASS, PhaseStatus.PASS_NO_SIGNAL, PhaseStatus.PASS_NO_REPORT,
            PhaseStatus.PASS_RECOVERED, PhaseStatus.PREFLIGHT_PASS,
            PhaseStatus.PASS_MISSING_CHECKPOINT,
        )

    @property
    def is_failure(self) -> bool:
        return self in (
            PhaseStatus.INCOMPLETE, PhaseStatus.HALT,
            PhaseStatus.TIMEOUT, PhaseStatus.ERROR,
        )
```
**FINDING:** `PhaseStatus` DOES have `PASS_RECOVERED` (`models.py:219`,
"non-zero exit but evidence of success") and `INCOMPLETE`.
`PhaseStatus.is_success` treats `PASS_RECOVERED` (and 5 other PASS_* variants)
as success; `PhaseStatus.INCOMPLETE` is a FAILURE. The asymmetry: PhaseStatus
has the recovered concept; TaskStatus does not. But the per-task aggregation at
1278-1279 hard-codes `PhaseStatus.PASS`/`ERROR` and never emits `PASS_RECOVERED`
(see §5).

**`TaskResult.output_path`** (`models.py:175`): field exists,
`output_path: str = ""`, currently unset in the per-task loop — available to
populate for evidence trails.

---

## 5. Phase aggregation — `executor.py:1277-1286`

Verbatim (second edit site). REPORT.md cited "1278-1283":
```python
                all_gate_results.extend(phase_gate_results)
                all_passed = all(r.status == TaskStatus.PASS for r in task_results)
                status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR
                phase_result = PhaseResult(
                    phase=phase,
                    status=status,
                    exit_code=0 if all_passed else 1,
                    started_at=started_at,
                    finished_at=datetime.now(timezone.utc),
                )
```

**How `all_passed` is computed (`executor.py:1278`):**
`all_passed = all(r.status == TaskStatus.PASS for r in task_results)` — a strict
identity check against `TaskStatus.PASS`. Any task whose status is anything
other than exactly `PASS` (including `INCOMPLETE`, `FAIL`, `SKIPPED`) makes
`all_passed == False`.

**Consequence (`executor.py:1279, 1283`):** when `all_passed` is False →
`status = PhaseStatus.ERROR` and `exit_code = 1`. No `PASS_RECOVERED` or
`INCOMPLETE` branch at the phase level here — it is binary PASS/ERROR.

**What must change for an "overran-but-completed" task to NOT fail the phase:**
1. Line 1278's `r.status == TaskStatus.PASS` (strict) must become tolerant of a
   recovered status. Two coherent options:
   - **(Option A — new TaskStatus member):** add e.g.
     `TaskStatus.PASS_RECOVERED` whose `is_success` returns True; set it in the
     1014-1020 block when `detect_error_max_turns(...)` is True AND a valid
     result/evidence exists; then change line 1278 to
     `all(r.status.is_success for r in task_results)`.
   - **(Option B — accept set):** change line 1278 to
     `all(r.status in {TaskStatus.PASS, TaskStatus.PASS_RECOVERED} ...)`.
2. The phase `status`/`exit_code` (1279, 1283) only emit `PASS`/`ERROR`. To
   preserve signal (REPORT.md Risk: keep INCOMPLETE→HALT for *genuine* budget
   exhaustion), the fix should map a phase containing recovered tasks to
   `PhaseStatus.PASS_RECOVERED` (success, exit 0) rather than plain `PASS`, while
   keeping genuine `INCOMPLETE`/`FAIL` tasks → `ERROR`.

**Reference symmetry note:** the per-phase recovery primitives to mirror are
`detect_error_max_turns` (monitor.py:37), `_classify_from_result_file`
(executor.py:1774), `_check_checkpoint_pass` (executor.py:1894), and
`_determine_phase_status` (executor.py:2067) — all in researcher-02's scope;
only their existence/signatures are noted here.

---

## Summary

**Edit sites (production code):**
1. **`executor.py:1014-1020`** (`execute_phase_tasks` per-task status switch) —
   the `else: status = TaskStatus.FAIL` branch mis-maps `error_max_turns`.
   Insert recovery here. `config`, `phase`, `task` are all in scope, so
   `config.task_output_file(phase, task)` + `detect_error_max_turns(...)` are
   directly callable. **No signature change to `_run_task_subprocess` is needed**
   (resolves the user's open question — the output path IS reachable in the
   classification block).
2. **`executor.py:1278-1279, 1283`** (phase aggregation) —
   `all_passed = all(r.status == TaskStatus.PASS ...)` is the strict gate that
   forces ERROR. Must be relaxed to treat a recovered status as success and
   ideally emit `PhaseStatus.PASS_RECOVERED`.
3. **`models.py:39-53`** (`TaskStatus`) — has NO recovered/PASS_RECOVERED member;
   a new member (whose `is_success` is True) likely must be added, because
   reclassifying to existing `INCOMPLETE` is still `is_failure == True` and still
   `!= PASS`, so it would NOT fix the false negative on its own.

**Key facts:**
- Exact on-disk path: `<release_dir>/results/phase-6-task-T06.15-output.txt` via
  `SprintConfig.task_output_file(phase, task)` (models.py:502-503).
- `max_turns` default 100 (models.py:362); `results_dir = release_dir/"results"`
  (models.py:478-480).
- `PhaseStatus.PASS_RECOVERED` already exists (models.py:219) and is `is_success`;
  `TaskStatus` has no equivalent — this asymmetry is the crux.
- `_run_task_subprocess` (executor.py:1076-1115) returns
  `(exit_code, turns=0-stub, output_bytes)`; it knows the path internally
  (computes it twice, 1101/1112) but discards it.
- The `_subprocess_factory` test contract (executor.py:954, 1003) also returns
  the 3-tuple — if a builder DID extend the return signature, both the real fn
  and this test factory contract would need updating. The recommended lighter
  approach avoids that by recomputing the path in the caller.

**Status: Complete**
