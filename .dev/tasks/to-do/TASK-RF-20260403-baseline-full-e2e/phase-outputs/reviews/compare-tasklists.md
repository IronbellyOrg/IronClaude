# Tasklist Comparison: Baseline vs Enriched

**Date**: 2026-04-02
**Phase**: 6.4

## Status: SKIPPED

**No enriched tasklist artifacts exist yet.**

Neither enriched pipeline run produced tasklist artifacts:

| Artifact | Baseline (test3-spec-baseline) | TDD+PRD (test1-tdd-prd) | Spec+PRD (test2-spec-prd) |
|----------|-------------------------------|-------------------------|---------------------------|
| tasklist-index.md | YES (2,763 bytes) | NO | NO |
| phase-1-tasklist.md | YES (20,480 bytes) | NO | NO |
| phase-2-tasklist.md | YES (22,236 bytes) | NO | NO |
| phase-3-tasklist.md | YES (20,946 bytes) | NO | NO |
| phase-4-tasklist.md | YES (24,819 bytes) | NO | NO |
| phase-5-tasklist.md | YES (17,623 bytes) | NO | NO |

## Reason

The enriched pipeline runs (test1-tdd-prd and test2-spec-prd) completed through the roadmap generation stage (extraction, diff-analysis, debate-transcript, base-selection, roadmap variants, merged roadmap, anti-instinct-audit, wiring-verification) but did not execute the tasklist generation step. Both runs' `.roadmap-state.json` and `wiring-verification.md` files confirm the pipeline terminated after roadmap generation.

The baseline run (test3-spec-baseline) is the only run that completed the full pipeline including tasklist generation.

## Impact on Comparison

The following comparisons cannot be performed:
- Task counts (baseline has 87 tasks across 5 phases)
- Data model task coverage (does enriched produce schema-specific tasks from TDD data models?)
- API endpoint task coverage (does enriched produce endpoint-specific tasks from TDD API specs?)
- Persona references in task descriptions (does enriched reference Alex/Jordan/Sam in acceptance criteria?)
- Effort distribution comparison

## Recommendation

To complete this comparison, run the tasklist pipeline against both enriched roadmaps:
1. `superclaude tasklist run .dev/test-fixtures/results/test1-tdd-prd/roadmap.md`
2. `superclaude tasklist run .dev/test-fixtures/results/test2-spec-prd/roadmap.md`
