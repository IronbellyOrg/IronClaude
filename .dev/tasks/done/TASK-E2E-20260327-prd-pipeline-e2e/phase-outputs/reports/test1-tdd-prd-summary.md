# Test 1 (TDD+PRD) — Summary Report
**Date:** 2026-03-31

## Pass/Fail Table

| Artifact | Gate | Check | Result | Notes |
|----------|------|-------|--------|-------|
| extraction.md | EXTRACT_GATE | 13 standard fields | PASS | All present |
| extraction.md | — | 6 TDD fields | PASS | All non-zero |
| extraction.md | — | 14 body sections | PASS | 8 standard + 6 TDD |
| extraction.md | — | PRD enrichment | PASS | 3 persona + 14 compliance refs |
| roadmap-opus.md | GENERATE_A | exists, ≥100 lines | PASS | 474 lines |
| roadmap-haiku.md | GENERATE_B | exists, ≥100 lines | PASS | 845 lines |
| diff-analysis.md | DIFF_GATE | fields | PASS | 14 diff pts, 18 shared |
| debate-transcript.md | DEBATE_GATE | fields | PASS | convergence=0.62, rounds=2 |
| base-selection.md | SCORE_GATE | fields + PRD | PASS | A:79 B:73, 20 PRD refs |
| roadmap.md | MERGE_GATE | fields + PRD | PASS | 593 lines, 24 PRD refs |
| anti-instinct | ANTI_INSTINCT | fingerprint ≥0.7 | **FAIL** | 0.69 (REGRESSION from 0.76) |
| anti-instinct | ANTI_INSTINCT | obligations=0 | FAIL | 4 (pre-existing) |
| anti-instinct | ANTI_INSTINCT | contracts=0 | FAIL | 4 (pre-existing) |
| test-strategy.md | TEST_STRATEGY | all fields | SKIPPED | anti-instinct halt |
| spec-fidelity.md | SPEC_FIDELITY | all fields | SKIPPED | anti-instinct halt |
| wiring.md | WIRING_GATE | complete, blocking=0 | PASS | TRAILING mode |
| .roadmap-state.json | — | new PRD fields | PASS | prd_file, input_type present |

## PRD Enrichment Results

| Artifact | PRD Content Expected | PRD Content Found | Assessment |
|----------|---------------------|-------------------|------------|
| extraction.md | Persona refs, compliance, metrics | 3 persona + 14 compliance | ENRICHED |
| base-selection.md | Business value scoring | 20 PRD refs | ENRICHED |
| roadmap.md | Business rationale, compliance milestones | 24 PRD refs | ENRICHED |
| .roadmap-state.json | prd_file field | Present with correct path | ENRICHED |
| test-strategy.md | PRD test dimensions | SKIPPED | — |
| spec-fidelity.md | Dimensions 12-15 | SKIPPED | — |

## REGRESSION: fingerprint_coverage dropped from 0.76 to 0.69

Prior TDD-only run: fingerprint_coverage=0.76 (34/45 found). This TDD+PRD run: 0.69 (31/45 found). The PRD supplementary content may have caused the LLM to generate roadmap text that uses fewer backticked identifiers, or the extraction's increased content diluted the roadmap's identifier density. This is below the 0.7 threshold and would cause anti-instinct to fail even without the obligations/contracts issues.

## Totals: 11 PASS, 3 FAIL (1 regression + 2 pre-existing), 2 SKIPPED
