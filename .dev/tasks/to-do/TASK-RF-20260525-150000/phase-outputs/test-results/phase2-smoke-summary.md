# Phase 2 Smoke Summary

Command: `uv run pytest tests/roadmap/test_integration_contracts.py tests/roadmap/test_anti_instinct_integration.py -v`

Date: 2026-05-25 16:15

## Result Line (after cycle 1 fix)

```
============================== 51 passed in 0.20s ==============================
```

## Counts

- **Passed:** 51
- **Failed:** 0
- **Skipped:** 0

## Cycle History

- **Cycle 0 (initial Phase 2.1-2.6 edits):** 48 passed, 3 failed — `TestNamedMechanismMatching::test_upper_snake_case_detected`, `TestCliPortifyRegression::test_detects_programmatic_runners_without_wiring`, `TestCliPortifyRegression::test_total_contracts_detected`. Root cause: §2.2's removal of bare `DISPATCH` regressed `CLI_PORTIFY_SPEC` extraction because the fixture's only DISPATCH_PATTERNS-matchable token was "Three-way dispatch:". merged-output.md §4 backward-compat assertion was incorrect (didn't trace through regex semantics — `\bRUNNERS\b` and `\b_RUNNERS\b` don't match inside `PROGRAMMATIC_RUNNERS` due to word boundaries on `_`).
- **Cycle 1 fix (revised Step 2.2):** Added `PROGRAMMATIC_RUNNERS` as an explicit named alternation to `DISPATCH_PATTERNS[0]`, paralleling merged-output.md §2.2's explicit `DISPATCH_TABLE` addition. See `phase-outputs/plans/phase2-smoke-fix-plan.md` for full RCA and rationale. Deviation logged.
- **Cycle 1 result:** 51 passed, 0 failed.

**Smoke verdict: PASS — proceed to Phase 3.**
