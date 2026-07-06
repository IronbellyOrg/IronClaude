# Full Sprint Suite Summary (Step 5.1)

**Timestamp:** 2026-06-04 05:18
**Command:** `cd /config/workspace/IronClaude-pr124 && uv run pytest tests/sprint/ -q`
**Raw output:** `pytest-sprint-output.txt`

## Overall result: ✅ PASS (clean)

| Metric | Count |
|---|---|
| Collected | 1154 |
| **Passed** | **1154** |
| Failed | 0 |
| Skipped | 0 |
| Deselected | 0 |
| Errors | 0 |
| Warnings | 20 (DeprecationWarning: `DiagnosticBundle.config=None` — pre-existing, unrelated) |
| Duration | 83.39s |

Summary line (verbatim):
```
================= 1154 passed, 20 warnings in 83.39s (0:01:23) =================
```

## Failing tests

**NONE.** Zero failures.

## Documented baseline note

The research-documented pre-existing baseline failure
`tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` (research 03 §2 — stale
event count after #116 added `checkpoint_manifest`) **now PASSES on the rebased tree.** This is
the "even better" outcome anticipated by research 03 §2 / Step 5.2: master's expected event count
has since been updated, so the suite is fully green with ZERO failures (not even the one allowed
baseline). The new regression test `test_resume_pass_recovered_counts_as_completed` is among the
1154 passing.
