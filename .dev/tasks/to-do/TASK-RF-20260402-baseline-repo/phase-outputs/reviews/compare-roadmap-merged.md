# Structural Comparison: roadmap.md (Merged Final)

**Test 2**: `.dev/test-fixtures/results/test2-spec-modified/roadmap.md`
**Test 3**: `.dev/test-fixtures/results/test3-spec-baseline/roadmap.md`

---

## Frontmatter Field Comparison

| Field Name | Test 2 | Test 3 | Status |
|---|---|---|---|
| spec_source | PRESENT | PRESENT | MATCH |
| complexity_score | PRESENT | PRESENT | MATCH |
| adversarial | PRESENT | PRESENT | MATCH |

**Field Count**: Test 2 = 3, Test 3 = 3 -- MATCH

---

## Body Section Header Comparison

| Structural Element | Test 2 | Test 3 | Status |
|---|---|---|---|
| Executive Summary | PRESENT | PRESENT | MATCH |
| Phased Implementation Plan | PRESENT | PRESENT | MATCH |
| Phase count | 7 (Phase 0-6) | 5 (Phase 1-5) | DIFF (expected) |
| Per-phase tasks/milestones | PRESENT | PRESENT | MATCH |
| Integration Points per phase | PRESENT | PRESENT | MATCH |
| Risk Assessment section | PRESENT | PRESENT | MATCH |
| Resource Requirements section | PRESENT | PRESENT | MATCH |
| Success Criteria / Validation section | PRESENT | PRESENT | MATCH |
| Timeline section | PRESENT | PRESENT | MATCH |
| Deferred Items / Out of Scope | PRESENT | ABSENT | DIFF (Test 2 only) |
| Architecture Decision Log | ABSENT | PRESENT | DIFF (Test 3 only) |
| Architecture Diagram | ABSENT | PRESENT | DIFF (Test 3 only) |
| Open Questions Resolution Plan | ABSENT | PRESENT | DIFF (Test 3 only) |

**Header Count**: Test 2 = 60, Test 3 = 59 -- APPROXIMATE MATCH

---

## Notes

- Both produce a merged adversarial-synthesis roadmap with the same core structure: Executive Summary, Multi-phase plan, Risk Assessment, Resources, Success Criteria, Timeline.
- Test 2 has 7 phases (0-6); Test 3 has 5 phases (1-5). This is expected because the base variant selection differed (Test 2 selected Haiku as base with 7 phases; Test 3 selected Opus as base with fewer phases, adding rollout). The merge strategy cascades from different base selections.
- Test 2 has a consolidated "Items Deferred to v1.1" section (grafted from Opus per merge instructions). Test 3 has an Architecture Decision Log and Architecture Diagram (grafted from Haiku per merge instructions). Both are expected merge artifacts.
- Frontmatter is identical in schema (3 fields).
- No TDD-specific content found in either version.

---

## Overall Verdict: MATCH

Structural equivalence confirmed. Both are valid merged adversarial roadmaps with identical frontmatter and the same core section schema. Differences in phase count and supplementary sections reflect the different base variant selections, which is expected downstream behavior of LLM non-determinism in scoring.
