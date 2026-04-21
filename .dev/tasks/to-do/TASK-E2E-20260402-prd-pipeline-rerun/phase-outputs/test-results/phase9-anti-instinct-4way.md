# Phase 9.1 -- 4-Way Anti-Instinct Comparison

Generated: 2026-04-03
Source: anti-instinct-audit.md from all 4 result directories

## 4-Way Comparison Table

| Metric | TDD-only (prior) | TDD+PRD (new) | Spec-only (prior) | Spec+PRD (new) |
|--------|-------------------|----------------|---------------------|-----------------|
| **fingerprint_coverage** | 0.76 | 0.73 | 0.72 | 0.67 |
| **fingerprint_total** | 45 | 45 | 18 | 18 |
| **fingerprint_found** | 34 | 33 | 13 | 12 |
| **undischarged_obligations** | 5 | 1 | 0 | 0 |
| **total_obligations** | 5 | 3 | 0 | 1 |
| **obligations_discharged** | 0 | 2 | 0 | 1 |
| **uncovered_contracts** | 4 | 4 | 3 | 3 |
| **total_contracts** | 8 | 8 | 6 | 6 |
| **contracts_covered** | 4 | 4 | 3 | 3 |
| **Gate PASS/FAIL** | FAIL | FAIL | FAIL | FAIL |

## Analysis: PRD Enrichment Impact on Anti-Instinct Results

### Fingerprint Coverage -- Slight Degradation

- **TDD pipeline**: PRD enrichment decreased fingerprint coverage from 0.76 to 0.73 (-0.03). One additional fingerprint was lost (`RBAC` appeared in the missing list for TDD+PRD but not TDD-only).
- **Spec pipeline**: PRD enrichment decreased fingerprint coverage from 0.72 to 0.67 (-0.05). The new run lost `OWASP` but gained different missing fingerprints (`AUTH_SERVICE_ENABLED`, `RBAC`, `CSRF`), while dropping `UUID` from the missing list.
- **Interpretation**: PRD enrichment slightly reduced fingerprint coverage in both pipelines. The additional PRD context may be causing the roadmap generator to use different terminology or abstractions, leading to fewer exact spec-fingerprint matches.

### Undischarged Obligations -- Significant Improvement (TDD)

- **TDD pipeline**: Obligations dropped from 5 undischarged to 1 undischarged (80% reduction). The PRD-enriched run detected only 3 total obligations (vs 5) and discharged 2 of them. The single remaining undischarged obligation references a `skeleton` in "Phase 0: Design and Foundation" rather than the 5 scattered `skeleton` references in Phase 1/Phase 2 from the prior run.
- **Spec pipeline**: Both runs show 0 undischarged obligations. The PRD run detected 1 obligation total and discharged it, vs 0 detected in the prior run.
- **Interpretation**: PRD enrichment substantially improved obligation handling in the TDD pipeline. The roadmap generator produced fewer skeleton/stub placeholders when given PRD context, suggesting the additional requirements context helps fill in implementation details.

### Integration Contract Coverage -- No Change

- **TDD pipeline**: Both runs show 4 uncovered contracts out of 8. The same 4 contracts (IC-001, IC-002, IC-006, IC-007 -- all `strategy_pattern` type) remain uncovered.
- **Spec pipeline**: Both runs show 3 uncovered contracts out of 6. The same 3 contracts (IC-004, IC-005, IC-006 -- all `middleware_chain` type) remain uncovered.
- **Interpretation**: PRD enrichment had zero effect on integration contract coverage. The uncovered contracts relate to structural patterns (testing strategy references, middleware chain references) that the roadmap generator handles identically regardless of PRD input.

### Gate Outcome -- All FAIL

All 4 runs FAIL the anti-instinct gate. This is expected behavior -- the gate requires zero undischarged obligations AND full contract coverage AND fingerprint coverage above threshold. No run meets all three criteria simultaneously.

### Summary

| Impact Area | TDD Pipeline | Spec Pipeline |
|-------------|-------------|---------------|
| Fingerprint coverage | Slight degradation (-0.03) | Moderate degradation (-0.05) |
| Obligations | Major improvement (5 -> 1) | Neutral (0 -> 0) |
| Contracts | No change (4/8 -> 4/8) | No change (3/6 -> 3/6) |
| Overall gate | FAIL -> FAIL | FAIL -> FAIL |

**Conclusion**: PRD enrichment produces a mixed effect. It significantly improves obligation discharge (fewer skeleton stubs) but slightly degrades fingerprint coverage (different terminology in generated roadmaps). Contract coverage is unaffected. The net effect is ambiguous -- the obligation improvement is meaningful for roadmap quality, but the fingerprint regression indicates some spec-specific terms get diluted when PRD context is added.
