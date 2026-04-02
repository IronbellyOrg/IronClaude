# Phase 6 — Anti-Instinct Comparison (Item 6.2a)

## Side-by-Side Comparison

| Field | Test 1 (TDD) | Test 2 (Spec) | Expected | Notes |
|-------|-------------|---------------|----------|-------|
| fingerprint_coverage | 0.76 | 0.72 | >= 0.7 | Both PASS. TDD has more identifiers (45 total vs 18) |
| fingerprint_total | 45 | 18 | > 0 | TDD fixture has richer backticked content |
| fingerprint_found | 34 | 13 | — | Both have reasonable coverage |
| undischarged_obligations | 5 | 0 | 0 | TDD FAILS, Spec PASSES |
| total_obligations | 5 | 0 | — | TDD roadmap has 5 skeleton-pattern refs |
| uncovered_contracts | 4 | 3 | 0 | Both FAIL — different contract types |
| total_contracts | 8 | 6 | — | TDD has more integration contracts |

## Analysis

Both pipelines fail at anti-instinct, but for different reasons:
- **Test 1 (TDD):** 5 undischarged obligations (skeleton references in roadmap not discharged in later phases) + 4 uncovered contracts
- **Test 2 (Spec):** 0 undischarged obligations but 3 uncovered contracts (middleware_chain integration points)

The fingerprint coverage is similar (0.76 vs 0.72), both above the 0.7 threshold. The TDD fixture generates more fingerprints (45 vs 18) because it has richer backticked content across data models, API specs, and components.

## Verdict: Both fail anti-instinct (pre-existing issue). The failures are structurally similar (roadmap doesn't generate explicit wiring for all contracts) but manifest differently due to different fixture content. Neither failure is caused by our TDD changes.
