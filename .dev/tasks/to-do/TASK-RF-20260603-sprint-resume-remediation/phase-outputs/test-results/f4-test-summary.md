# F-4 Test Summary (Phase 4)

**Command:** `uv run pytest "tests/sprint/test_resume.py::TestResumePlanner" "tests/sprint/test_resume.py::TestInvariants" -v`
**Overall:** ✅ PASS — 10 passed in 0.20s (full output: `cg3-green.txt`)

## Per-test results

| Test | AC / Gap | Result | Note |
|------|----------|--------|------|
| `test_resume_planner_phase_boundary` | AC-1 | ✅ PASS | Unaffected. |
| `test_resume_task_level_recoverable` | AC-2 | ✅ PASS | TASK-granularity boundary unaffected (emit only fires on empty PHASE boundary). |
| `test_resume_hard_crash_phase_level` | AC-3 (reference) | ✅ PASS (**reconciled**) | See "Reference-test reconciliation" below. |
| `test_resume_hard_crash_double_validates_prior_phase_tail` | **CG-3 positive** | ✅ PASS (was RED) | `last_completed` boundary task points at `T02.01`; `report.validated_last is True` (real re-derivation of P2 tail). |
| `test_resume_hard_crash_prior_tail_overclaim_stops` | **CG-3 negative** | ✅ PASS (was RED) | Missing P2 deliverable ⇒ `validated_last is False`, `passed is False` — proves the prior-tail validation can STOP (non-vacuous). |
| `test_planner_performs_no_writes` | invariant | ✅ PASS | Planner stayed **write-free** — the prior-tail emit reads `parse_tasklist_file` (read_text only) and mutates only the in-memory plan. |
| `test_gate_hard_stops_on_last_completed_overclaim` | FR-2.4 | ✅ PASS | Interrupted-phase last-completed validation unaffected (fallback when `lc.phase is None`). |
| `test_boundary_quarantine_nondestructive` | FR-2.5 | ✅ PASS | Non-regressed. |
| `test_boundary_partial_paths_surfaced_in_report` | CG-1 | ✅ PASS | F-2 fix still green. |
| `test_haiku_coherence_advisory_only` | DD-2 | ✅ PASS | Non-regressed. |

## RED→GREEN evidence

- **RED:** `cg3-red.txt` — both CG-3 tests FAILED on `assert lc and lc[0].task_id == "T02.01"` → `assert ([])` (today `boundary_tasks == []`, no `last_completed` emitted, validation vacuous).
- **GREEN:** `cg3-green.txt` — both pass; positive asserts `validated_last is True`, negative asserts `validated_last is False`/`passed is False`.

## Reference-test reconciliation (intentional, per task Open Questions)

`test_resume_hard_crash_phase_level` previously asserted `plan.boundary_tasks == []`. The F-4 fix
makes the PHASE hard-crash path emit ONE prior-tail `last_completed` boundary task, so that exact
assertion no longer holds. Per the task's Open Questions ("F-4 intentionally changes the existing
AC-3 reference test"), the assertion was reconciled to:

```python
assert [bt.role for bt in plan.boundary_tasks] == ["last_completed"]
assert plan.boundary_tasks[0].task_id == "T02.01"
```

This is part of the F-4 landing, NOT a regression — the reference fixture's prior phase (P2) has a
single task `T02.01`, which is now correctly emitted as the prior-tail to double-validate. The test
PASSES with the reconciled assertion. (Note: in that fixture P2 has no transcript/deliverable
written, but the test asserts only plan shape, not the gate verdict, so it is stable.)

## Non-regression confirmation

- **`test_planner_performs_no_writes` PASSES** — confirms the planner remained pure-read after adding `_emit_prior_tail_boundary` (uses `parse_tasklist_file`/`discover_phases`, both read-only; the tasklist read is outside `results/`).
- All TASK-granularity and gate-invariant tests PASS — the emit is gated on `granularity is PHASE and not boundary_tasks`, so it never fires on the TASK path.

All rows reflect the actual pytest output — no fabricated results.
