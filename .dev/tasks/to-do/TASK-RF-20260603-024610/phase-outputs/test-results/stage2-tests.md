# Stage 2 — Test & Lint Summary (Step 4.9)

**Captured:** 2026-06-03 20:40
**Raw output:** `stage2-tests.txt`
**Command:** `uv run pytest tests/sprint/test_resume_contract.py tests/sprint/test_handoff_crash_consistency.py tests/sprint/test_resume_backward_compat.py tests/sprint/test_handoff_store.py tests/sprint/test_multi_phase.py tests/sprint/test_backward_compat_regression.py -q`

## Pytest counts (exact)

| Metric | Count |
|--------|-------|
| Passed | 28 |
| Failed | 2 |
| Skipped | 0 |
| Total | 30 |
| Exit code | 1 |

Summary line: `2 failed, 28 passed in 5.67s`

## Lint

`make lint` → **PASS** ("All checks passed!", exit 0).

## Regression analysis vs `pre-change-baseline.md`

**ZERO regressions.** The 2 failures are pre-existing baseline `.stdin`
harness-double failures in `test_multi_phase.py`, both on the Phase-1
already-failing list:

| Failing test | On baseline list? | Signature |
|---|---|---|
| test_multi_phase.py::TestThreePhaseHappyPath::test_three_phase_happy_path | yes | `_PassPopen ... 'stdin'` |
| test_multi_phase.py::TestHaltAtPhaseThree::test_halt_at_phase_three | yes | `_Popen ... 'stdin'` |

## New Stage-2 tests (all PASS)

- `test_resume_contract.py` — 3 passed (validated-success predicate across all
  TaskStatus×GateOutcome states; skip validated-success + re-run failure + no
  budget debit on skip; resume-inactive runs all).
- `test_handoff_crash_consistency.py` — 1 passed (handoff file written, NO
  `task_complete` journal event → resume honors the handoff file and skips).
- `test_resume_backward_compat.py` — 2 passed (no `handoff/` dir → no error, all
  tasks run, phase-granular-equivalent; store `read` on missing dir → None,
  does not create the dir).

## Existing tests held green

- `test_handoff_store.py`, `test_backward_compat_regression.py` — green.

## Verdict

Stage-2 resume contract is green: all new acceptance tests pass (skip predicate,
crash-consistency authority of the handoff file, back-compat degradation), lint
clean, only failures are the 2 pre-existing `.stdin` baseline failures — NOT
regressions.
