# D-0017: Anti-Instinct Integration Tests Evidence

## Status: COMPLETE

## Test File

`tests/roadmap/test_anti_instinct_integration.py` — 30 tests across 6 test classes

## Test Results

```
30 passed in 0.12s
```

## Coverage Summary

| Scenario | Tests | Status |
|---|---|---|
| 1. Pipeline wiring (anti-instinct step exists, positioned, metadata) | 5 | PASS |
| 2. SC-001 regression blocking (obligation, contracts, fingerprint, gate, all-three) | 5 | PASS |
| 3. Gate passes on good roadmap (clean audit, frontmatter correct) | 2 | PASS |
| 4. Structural audit warning-only (no raise, missing files, no frontmatter) | 3 | PASS |
| 5. Output format (YAML frontmatter, required fields, sections, lines, types) | 5 | PASS |
| Semantic check unit tests (zero/nonzero/missing/threshold) | 10 | PASS |

## Full Test Suite Regression

```
1277 passed in 2.31s (0 failed, 0 errors)
```

Baseline was 1241 tests. Increase of 36 tests (30 new + 6 parameterized from new gate).
