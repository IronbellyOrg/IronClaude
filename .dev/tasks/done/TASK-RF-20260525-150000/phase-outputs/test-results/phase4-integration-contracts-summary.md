# Phase 4 — `test_integration_contracts.py` Summary

Command: `uv run pytest tests/roadmap/test_integration_contracts.py -v`

Date: 2026-05-25 16:20

## Result Line

```
============================== 28 passed in 0.15s ==============================
```

## Counts

- **Total:** 28
- **Passed:** 28
- **Failed:** 0

## Per-Class Breakdown

| Class | Tests | Status |
| --- | --- | --- |
| `TestDispatchPatternDetection` | 8 | PASS |
| `TestWiringCoverage` | 4 | PASS |
| `TestDeduplication` | 2 | PASS |
| `TestNamedMechanismMatching` | 2 | PASS |
| `TestCliPortifyRegression` | 2 | PASS |
| `TestIntegrationAuditResult` | 3 | PASS |
| `TestHubDispatchRegression` (NEW) | 7 | PASS |

**Expected:** 28 (21 existing — task spec said 22 but actual was 21 — plus 7 new). Actual: 28. Match.

## Cycle History

- **Cycle 0 (initial Phase 4):** 27 passed, 1 failed — `test_t7_stem_fallback_without_ident_overlap_uncovers`. Root cause: merged-output.md spec internal inconsistency between Layer 1 (which includes bare `priority` in `dispatch_family` regex) and t7 (which asserts "Implement priority dispatch for logging" should NOT cover the contract). Layer 1 matched and short-circuited before Layer 3's identifier-overlap guard could fire.
- **Cycle 1 fix:** Removed bare `priority` from BOTH `DISPATCH_PATTERNS[0]` (§2.2 extraction) AND Layer 1 `dispatch_family` regex (§2.4 coverage). Keeps `class-priority` and all other named compounds. Honors t7's design intent (Layer 3 identifier-overlap as false-positive defense). See `phase-outputs/plans/phase4-fix-plan.md`. Deviation logged.
- **Cycle 1 result:** 28/28 PASS.

**Phase 4.1 verdict: PASS.**
