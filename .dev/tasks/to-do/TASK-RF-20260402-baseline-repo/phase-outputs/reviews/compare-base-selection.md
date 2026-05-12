# Structural Comparison: base-selection.md

**Test 2**: `.dev/test-fixtures/results/test2-spec-modified/base-selection.md`
**Test 3**: `.dev/test-fixtures/results/test3-spec-baseline/base-selection.md`

---

## Frontmatter Field Comparison

| Field Name | Test 2 | Test 3 | Status |
|---|---|---|---|
| base_variant | PRESENT | PRESENT | MATCH |
| variant_scores | PRESENT | PRESENT | MATCH |

**Field Count**: Test 2 = 2, Test 3 = 2 -- MATCH

---

## Body Section Header Comparison

| Structural Element | Test 2 | Test 3 | Status |
|---|---|---|---|
| Scoring Criteria section | PRESENT | PRESENT | MATCH |
| Per-Criterion Scores section | PRESENT | PRESENT | MATCH |
| (Individual criteria subsections) | 6 criteria (C1-C6) | 10 criteria (#1-#10) | DIFF (count) |
| Overall Scores section | PRESENT | PRESENT | MATCH |
| Base Variant Selection Rationale | PRESENT | PRESENT | MATCH |
| Improvements to Incorporate | PRESENT | PRESENT | MATCH |

**Header Count**: Test 2 = 16, Test 3 = 18 -- APPROXIMATE MATCH

---

## Notes

- Both follow the identical base-selection schema: Scoring Criteria -> Per-Criterion Scores -> Overall Scores -> Selection Rationale -> Improvements to merge.
- Test 2 uses 6 weighted criteria (C1-C6); Test 3 uses 10 criteria (#1-#10). This reflects different LLM choices in how many dimensions to score, which depends on the upstream debate content. Expected non-determinism.
- Test 2 selects Variant B (Haiku) as base; Test 3 selects Variant A (Opus) as base. Different base selections are expected because the upstream roadmaps differ between runs. The structural schema for making and justifying the selection is the same.
- Frontmatter is identical in schema (2 fields).
- No TDD-specific content found in either version.

---

## Overall Verdict: MATCH

Structural equivalence confirmed. Identical selection framework schema. The number of scoring criteria and the selected base variant differ due to upstream content differences, which is expected LLM non-determinism.
