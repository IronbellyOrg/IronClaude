# Phase 8: Cross-Run Comparison Summary
**Date:** 2026-03-31

## TDD+PRD vs TDD-Only

| Dimension | TDD-Only | TDD+PRD | Delta | Assessment |
|-----------|----------|---------|-------|------------|
| Extraction sections | 14 | 14 | 0 | Same |
| PRD content in extraction (grep -ciE 'prd') | 0 refs | 20 refs | +20 | ENRICHED |
| Roadmap lines | 634 | 593 | -41 | Slightly shorter |
| fingerprint_coverage | 0.76 | 0.69 | -0.07 | **REGRESSION** |

## Spec+PRD vs Spec-Only

| Dimension | Spec-Only | Spec+PRD | Delta | Assessment |
|-----------|-----------|----------|-------|------------|
| Extraction sections | 8 | 8 | 0 | Same (no TDD leak) |
| PRD content in extraction (grep -ciE 'prd') | 1 ref | 38 refs | +37 | ENRICHED |
| Roadmap lines | 494 | 638 | +144 | Significantly richer |
| fingerprint_coverage | 0.72 | 0.78 | +0.06 | IMPROVED |
| TDD content leak | 0 | 0 | 0 | CLEAN |

## Enrichment Assessment

PRD enrichment adds meaningful product context to both paths. The spec path benefits more (+37 PRD refs by grep count, +144 roadmap lines, improved fingerprint). The TDD path shows a fingerprint regression that needs investigation. Note: PRD ref counts use `grep -ciE 'prd'` (case-insensitive line count).
