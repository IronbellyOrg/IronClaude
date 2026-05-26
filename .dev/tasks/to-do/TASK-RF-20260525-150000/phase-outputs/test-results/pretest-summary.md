# Pre-refactor Pytest Baseline — Phase 1 Step 1.6

Command: `uv run pytest tests/roadmap/test_integration_contracts.py tests/roadmap/test_anti_instinct_integration.py -v`

Date: 2026-05-25 16:06

## Result Line

```
============================== 51 passed in 0.20s ==============================
```

## Totals

- **Total tests collected:** 51
- **Total passed:** 51
- **Total failed:** 0

## Per-file Counts

- `tests/roadmap/test_integration_contracts.py`: 21 tests (1 fewer than the task spec's "22" — task estimate was off by one, no functional impact)
- `tests/roadmap/test_anti_instinct_integration.py`: 30 tests

## Per-Class Pass Breakdown (test_integration_contracts.py)

| Class | Tests | Status |
| --- | --- | --- |
| `TestDispatchPatternDetection` | 8 | PASS |
| `TestWiringCoverage` | 4 | PASS |
| `TestDeduplication` | 2 | PASS |
| `TestNamedMechanismMatching` | 2 | PASS |
| `TestCliPortifyRegression` | 2 | PASS |
| `TestIntegrationAuditResult` | 3 | PASS |

**Baseline locked: 51/51 tests passing pre-refactor.**
