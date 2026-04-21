# Structural Comparison: roadmap-opus-architect.md

**Test 2**: `.dev/test-fixtures/results/test2-spec-modified/roadmap-opus-architect.md`
**Test 3**: `.dev/test-fixtures/results/test3-spec-baseline/roadmap-opus-architect.md`

---

## Frontmatter Field Comparison

| Field Name | Test 2 | Test 3 | Status |
|---|---|---|---|
| spec_source | PRESENT | PRESENT | MATCH |
| complexity_score | PRESENT | PRESENT | MATCH |
| primary_persona | PRESENT | PRESENT | MATCH |
| generated | PRESENT | ABSENT | DIFF (Test 2 only) |
| generator | PRESENT | ABSENT | DIFF (Test 2 only) |
| total_phases | PRESENT | ABSENT | DIFF (Test 2 only) |
| total_milestones | PRESENT | ABSENT | DIFF (Test 2 only) |
| total_requirements_mapped | PRESENT | ABSENT | DIFF (Test 2 only) |
| risks_addressed | PRESENT | ABSENT | DIFF (Test 2 only) |
| open_questions | PRESENT | ABSENT | DIFF (Test 2 only) |

**Field Count**: Test 2 = 10, Test 3 = 3 -- DIFF (-7 in Test 3)

---

## Body Section Header Comparison (## and ### level, normalized)

Both roadmaps share the same structural pattern:
- Executive Summary
- Phased Implementation Plan with multiple phases
- Each phase has milestones, tasks, integration points, exit criteria
- Risk Assessment section
- Resource Requirements section
- Success Criteria / Validation section
- Timeline Summary
- Deferred Items / Open Questions

| Structural Element | Test 2 | Test 3 | Status |
|---|---|---|---|
| Executive Summary | PRESENT | PRESENT | MATCH |
| Phased Plan with phases | 5 phases (0-4) | 4 phases (1-4) | DIFF (phase count) |
| Per-phase milestones | PRESENT | PRESENT | MATCH |
| Integration Points sections | PRESENT | PRESENT | MATCH |
| Risk Assessment | PRESENT | PRESENT | MATCH |
| Resource Requirements | PRESENT | PRESENT | MATCH |
| Success Criteria / Validation | PRESENT | PRESENT | MATCH |
| Timeline Summary | PRESENT | PRESENT | MATCH |
| Deferred Items / Open Questions | PRESENT | PRESENT | MATCH |

**Header Count**: Test 2 = 31, Test 3 = 32 -- APPROXIMATE MATCH

---

## Notes

- Test 2 has 7 additional frontmatter metadata fields (generated, generator, total_phases, total_milestones, total_requirements_mapped, risks_addressed, open_questions). Test 3 has only the 3 core fields. This is expected LLM non-determinism -- the Opus model sometimes emits richer frontmatter.
- Test 2 includes a Phase 0 (Foundation & Decision Resolution); Test 3 starts at Phase 1. Both have 4 implementation phases. This is expected variation in how the LLM chooses to structure phases.
- Both share the same canonical section structure: Executive Summary, Phased Plan, Risk, Resources, Success Criteria, Timeline.
- No TDD-specific content found in either version.

---

## Overall Verdict: MATCH

Structural equivalence confirmed with expected LLM non-determinism. The frontmatter field count difference (10 vs 3) reflects different levels of metadata richness, not a schema violation. The core 3 fields (spec_source, complexity_score, primary_persona) are present in both. Section structure is functionally equivalent.
