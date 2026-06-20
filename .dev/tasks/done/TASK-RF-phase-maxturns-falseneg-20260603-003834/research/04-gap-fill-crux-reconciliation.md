# Research (Gap-Fill): CRUX reconciliation — authoritative fix design

**Topic type:** Gap-fill / design reconciliation
**Scope:** Resolves G1 (CRITICAL), G2 (IMPORTANT), G4 (MINOR) from the analyst report; grounded in verified facts from files 01/02/03 + both QA agents.
**Status:** Complete
**Date:** 2026-06-03

---

## Why this file exists

The research-gate analyst FAILED on a cross-file contradiction: research-02's
TL;DR recommended reclassifying the overran task to the **existing**
`TaskStatus.INCOMPLETE` as a "success-like" target, while research-01 proved
that does NOT fix the bug. rf-qa independently confirmed research-01 is
correct against live source. This file is the authoritative tie-breaker the
builder MUST follow. Where this file and any other research file disagree,
**this file wins**.

## Verified ground truth (re-confirmed by rf-qa, 22/22)

- `models.py:48-49` — `TaskStatus.is_success` is **strictly** `== PASS`.
- `models.py:52-54` — `TaskStatus.INCOMPLETE` is included in `is_failure`.
- `executor.py:1278` — phase aggregation is a strict `all(r.status == TaskStatus.PASS for r in task_results)`.
- `executor.py:1016-1020` — per-task switch: `exit 0 → PASS`, `exit 124 → INCOMPLETE`, `else → FAIL`. **`exit 124` (timeout) shares the INCOMPLETE bucket.**
- `models.py:219` — `PhaseStatus.PASS_RECOVERED` already exists, is_success==True, semantics "non-zero exit but evidence of success". **`TaskStatus` has no counterpart.**
- `config.task_output_file(phase, task)` (`models.py:502-503`) → `<release_dir>/results/phase-{n}-task-{task_id}-output.txt`; reachable at the switch (config/phase/task all in scope). No `_run_task_subprocess` signature change needed.
- `detect_error_max_turns(output_path)` (`monitor.py:37`) scans the last non-empty NDJSON line for `"subtype":"error_max_turns"`. Already imported in executor.py.

## DECISION 1 (resolves G1) — introduce a NEW success-valued `TaskStatus.PASS_RECOVERED`; do NOT reuse `INCOMPLETE`

Reusing `INCOMPLETE` is **rejected** for two independent reasons:
1. `INCOMPLETE != PASS` and `INCOMPLETE ∈ is_failure` → the phase still errors. (research-01, confirmed.)
2. `exit 124` (genuine timeout, no completion) **also** maps to `INCOMPLETE` (`executor.py:1018`). If `INCOMPLETE` were made success-valued, genuine timeouts would silently pass the phase — a **regression** that violates REPORT.md's Risk note ("must distinguish overran-after-completing from overran-without-a-result"). So `INCOMPLETE` MUST keep failing the phase.

**Therefore:** add `TaskStatus.PASS_RECOVERED` mirroring the existing
`PhaseStatus.PASS_RECOVERED`. Update `TaskStatus.is_success` to
`self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)` and ensure
`is_failure` does NOT include `PASS_RECOVERED`. This is the minimal,
non-regressive, precedent-aligned choice.

## DECISION 2 (resolves G1) — recovery is GATED on completion evidence

`error_max_turns` alone is NOT sufficient to recover — that would mask a task
that overran *without* finishing. The per-task completion signal available
without new plumbing is the task's own NDJSON output stream: an agent-emitted
successful result / `task_complete` envelope appearing **before** the terminal
`error_max_turns` envelope (exactly the T06.15 shape — its success summary sat
at byte 16K–132K, the `error_max_turns` envelope at EOF).

**Recovery predicate** (per-task, in the `else` branch of the switch):
```
if detect_error_max_turns(task_output_path) and _task_completed_before_overrun(task_output_path):
    status = TaskStatus.PASS_RECOVERED
else:
    status = TaskStatus.FAIL
```
The builder implements a small helper `_task_completed_before_overrun(output_path) -> bool`
that scans the NDJSON for at least one non-error assistant `result`/`task_complete`
prior to the final `error_max_turns` line. If a robust completion scan is not
feasible in scope, the conservative fallback is to recover on `error_max_turns`
alone BUT log a WARNING — documented as the lighter alternative; the gated form
is preferred. Either way `exit 124` is untouched and keeps failing.

## DECISION 3 (resolves G1) — aggregation switches to `is_success`

`executor.py:1278`: change
`all(r.status == TaskStatus.PASS for r in task_results)` →
`all(r.status.is_success for r in task_results)`
so PASS and PASS_RECOVERED both count as passing while FAIL/INCOMPLETE/SKIPPED
still fail. (Confirms with Decision 1's is_success update.) Optionally surface
`PhaseStatus.PASS_RECOVERED` instead of `PhaseStatus.PASS` when any task was
recovered, mirroring the per-phase path — OPTIONAL, not required for the fix.

## DECISION 4 (resolves G2) — test assertions must be `is_success`/phase-level, NOT `!= FAIL`

research-03's drafted positive assertion `results[0].status != TaskStatus.FAIL`
is **too weak** — it passes even under the broken bare-INCOMPLETE fix. Required
assertions:
- **Positive test:** factory returns `(exit=1, turns=101, bytes>0)` AND a fake
  NDJSON output file at `config.task_output_file(phase, task)` whose pre-terminal
  line is a success result and terminal line is `{"subtype":"error_max_turns"}`
  → assert `results[0].status == TaskStatus.PASS_RECOVERED` AND
  `results[0].status.is_success is True` AND the aggregated phase status
  `is_success` / `== PhaseStatus.PASS` (or PASS_RECOVERED).
- **Guard A (genuine failure):** non-zero exit, NO error_max_turns file →
  `status == TaskStatus.FAIL`, phase ERROR.
- **Guard B (genuine timeout, no regression):** `exit == 124` →
  `status == TaskStatus.INCOMPLETE`, phase NOT is_success (still fails).
- **Guard C (overran without completion):** error_max_turns file present but NO
  prior success envelope → `status == TaskStatus.FAIL` (only meaningful if
  Decision 2's gated form is implemented).
- Test location/fixtures: `tests/sprint/test_executor.py::TestPerTaskOrchestration`,
  clone `test_per_task_timeout_produces_incomplete`; MUST
  `out.parent.mkdir(parents=True, exist_ok=True)` before writing the fake file
  (results dir doesn't pre-exist under `release_dir=tmp_path`).

## DECISION 5 (resolves G4) — output-path reconciliation is CLOSED

The fix reads the canonical `config.task_output_file(phase, task)` path
in-caller. It does NOT extend the `_subprocess_factory` tuple. research-03's
UNVERIFIED tension is resolved in favor of research-01. Tests write the fake
NDJSON to that canonical path.

## Files to change (authoritative list for the builder)

1. `src/superclaude/cli/sprint/models.py` — add `TaskStatus.PASS_RECOVERED`; update `is_success` (and confirm `is_failure`).
2. `src/superclaude/cli/sprint/executor.py` — (a) add the recovery branch + `_task_completed_before_overrun` helper in `execute_phase_tasks` per-task switch (@1014-1020); (b) switch aggregation `all_passed` to `.is_success` (@1278).
3. `tests/sprint/test_executor.py` — add the positive + guard tests above.
4. No `.claude/` sync needed (these are `src/` Python + `tests/`, not synced components); `make verify-sync` must still pass unchanged.

## Verification gates
- `uv run pytest tests/sprint/test_executor.py -v` (and full `tests/sprint/`) — new tests pass, no regressions.
- `make lint` (ruff) exit 0; `make format` clean.
- `make verify-sync` passes unchanged.
- Git: feature/`fix/` branch (never main); UV-only.
