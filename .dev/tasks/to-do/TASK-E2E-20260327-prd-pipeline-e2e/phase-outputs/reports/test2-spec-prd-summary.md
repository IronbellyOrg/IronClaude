# Test 2 (Spec+PRD) — Summary Report
**Date:** 2026-03-31

## Key Results
- **No TDD content leak:** 0 TDD fields, 0 TDD sections in spec extraction
- **PRD enrichment works:** 38 PRD refs in extraction (grep -ciE 'prd')
- **State file correct:** prd_file present, tdd_file=None, input_type=auto
- **Pipeline:** 8/11 steps pass, halts at anti-instinct (pre-existing)
- **fingerprint_coverage:** 0.78 (PASSES ≥0.7, better than TDD+PRD's 0.69)

## Comparison vs Prior Spec-Only Run

| Metric | Spec-only (prior) | Spec+PRD (this) | Delta |
|--------|-------------------|------------------|-------|
| nonfunctional_requirements | 3 | 7 | +4 (PRD added) |
| total_requirements | 8 | 12 | +4 |
| risks_identified | 3 | 7 | +4 |
| fingerprint_coverage | 0.72 | 0.78 | +0.06 (improved) |
| PRD content refs | 0 | 38 | +38 |
| TDD fields | 0 | 0 | 0 (no leak) |
| TDD sections | 0 | 0 | 0 (no leak) |

PRD enrichment improved extraction depth without introducing TDD contamination.
