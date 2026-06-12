# Regression Diff — baseline vs post-change (sprint suite)

Command (both runs): `uv run pytest tests/sprint/ -q` (UV only), from `/config/workspace/IronClaude`.

| Run | Result |
|---|---|
| Baseline (clean, pre-change) | **1 failed, 1070 passed** |
| Post-change | **1 failed, 1073 passed** (+3 = the new tests) |

## (a) Pre-existing failures in baseline (count = 1)
- `tests/sprint/test_e2e_success.py::TestE2ESuccess::test_jsonl_events_for_each_phase`

NOTE: the BUILD_REQUEST estimated ~18 pre-existing failures; the actual baseline on the
branch base (`master`) is **1**. The zero-NEW-failures proof is computed against this real
baseline, not the estimate.

## (b) Failures post-change (count = 1)
- `tests/sprint/test_e2e_success.py::TestE2ESuccess::test_jsonl_events_for_each_phase`

## (c) NEW failures (post-change minus baseline)
- **NONE.** `comm -13 baseline post` is empty — the only post-change failure also appears in
  the baseline, so it is pre-existing and unrelated to this change.

## (d) New tests — all PASS
- `test_per_task_error_max_turns_tail_verdict_recovers` — PASS
- `test_per_task_error_max_turns_early_verdict_still_fails` — PASS
- `test_task_completed_before_overrun_evidence_classes` — PASS
(Isolated run evidence: `new-tests-result.txt` → `3 passed, 90 deselected`.)

## Verdict
**0 NEW failures; +3 new tests passing.** Zero regression proven.
