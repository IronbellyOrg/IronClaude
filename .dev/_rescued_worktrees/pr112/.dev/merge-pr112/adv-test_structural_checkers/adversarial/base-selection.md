# Base Selection

## Quantitative Scoring (50% weight)
All three variants are functionally identical Python test modules; deterministic metrics are equal by construction.

| Metric | Weight | V1 proposed | V2 ours | V3 theirs |
|--------|--------|-------------|---------|-----------|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | 1.00 |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | 1.00 |
| Specificity ratio (SR) | 0.15 | 1.00 | 1.00 | 1.00 |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **1.00** | **1.00** | **1.00** |

## Qualitative Scoring (50% weight)
Identical code → identical rubric outcomes. Edge-case-coverage floor satisfied (the added MD-family tests explicitly exercise collection/boundary cases for ID canonicalization). All three eligible as base.

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness / Correctness / Structure / Clarity / Risk / Invariant | equal | equal | equal |
| **qual_score** | **equal** | **equal** | **equal** |

## Combined Scoring
- variant_score(V1) == variant_score(V2) == variant_score(V3)
- Three-way tie → tiebreaker protocol invoked.

### Tiebreaker
- **Level 1 (debate performance)**: V1/V2 won C-001 (toward branch-local provenance). V3 conceded no correctness/coverage basis.
- Result: V1 (proposed) selected.

## Selected Base: Variant 1 (proposed)
**Selection rationale**: The proposed resolution is byte-identical to OURS, carries the complete union of test coverage (verified: 66 AST nodes == both sides; the 4 MD-family additions present), has no conflict markers, parses clean, and asserts against the canonical contract `ID_PATTERNS["MD"] = M\d+-D-?\d+`. Because OURS and THEIRS contributed identical test code, the merge cannot drop any side's coverage — the union *is* either side.

**Strengths to preserve**: All 66 test nodes; the 3 MD-family tests + allowlist fixture; the branch-local provenance comment.

**Strengths to incorporate from non-base**: None. THEIRS contributes no unique test node and no divergent assertion. Its only differentiator (the comment label) was adjudicated and not incorporated.
