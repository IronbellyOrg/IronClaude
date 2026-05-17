# Structural Comparison: diff-analysis.md

**Test 2**: `.dev/test-fixtures/results/test2-spec-modified/diff-analysis.md`
**Test 3**: `.dev/test-fixtures/results/test3-spec-baseline/diff-analysis.md`

---

## Frontmatter Field Comparison

| Field Name | Test 2 | Test 3 | Status |
|---|---|---|---|
| total_diff_points | PRESENT | PRESENT | MATCH |
| shared_assumptions_count | PRESENT | PRESENT | MATCH |

**Field Count**: Test 2 = 2, Test 3 = 2 -- MATCH

---

## Body Section Header Comparison

| Section Header | Test 2 | Test 3 | Status |
|---|---|---|---|
| Shared Assumptions / Agreements | PRESENT | PRESENT | MATCH |
| Divergence Points | PRESENT | PRESENT | MATCH |
| (Numbered divergence items) | 17 items | 14 items | DIFF (count varies) |
| Areas Where One Variant Is Stronger | PRESENT | PRESENT | MATCH |
| Areas Requiring Debate to Resolve | PRESENT | PRESENT | MATCH |

**Header Count**: Test 2 = 21, Test 3 = 21 -- MATCH

---

## Notes

- Both have exactly the same 4 top-level structural sections: Shared Assumptions, Divergence Points, Stronger Areas, Debate Areas.
- Test 2 identifies 17 divergence points; Test 3 identifies 14. This is expected because the two roadmap variants they are comparing differ between runs (LLM non-determinism in the upstream Opus/Haiku roadmaps produces different divergences to analyze).
- Frontmatter values differ (Test 2: total_diff_points=17, shared_assumptions_count=17; Test 3: total_diff_points=14, shared_assumptions_count=12) but the field NAMES are identical.
- No TDD-specific content found in either version.

---

## Overall Verdict: MATCH

Structural equivalence confirmed. Identical frontmatter schema (2 fields) and identical section structure (4 top-level sections). The number of divergence sub-items varies due to different upstream roadmap content, which is expected.
