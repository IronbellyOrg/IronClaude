# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Note |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | Both fill Mode, Type, Issue type, Complexity |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | No internal contradictions |
| Specificity ratio (SR) | 0.15 | 1.00 | 1.00 | No vague indicators in either |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | Only external refs (`refs/labels.md`), excluded |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | Same template sections |
| **quant_score** | | **1.00** | **1.00** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Many rubric criteria (risk, edge cases, navigation) cannot apply to a four-row flags table; with no evidence they score NOT MET for both, as the CEV rule requires.

| Dimension | Variant 1 | Variant 2 | Deciding evidence |
|---|---|---|---|
| Completeness (5) | 1 | 2 | C3 "dependencies named": Variant 2 names `main.py` and `install_skills.py`; Variant 1 names none |
| Correctness (5) | 5 | 5 | Both claims verified (`--type cli` as passed; `install_skills.py:62`, `:76`) |
| Structure (5) | 4 | 4 | No navigation aids (C4) in either |
| Clarity (5) | 3 | 3 | No acronyms defined (C4) and no next steps (C5) in either |
| Risk Coverage (5) | 0 | 0 | None in either |
| Invariant & Edge Case (5) | 0 | 0 | None in either |
| **qual_score** | **13/30 = 0.433** | **14/30 = 0.467** | |

### Edge Case Floor Check

Edge case floor suspended: no variant meets minimum coverage (both 0/5).

## Position-Bias Mitigation

A single native evaluator scored both variants; a separate reverse-order pass was not run (part of the fallback recorded in the debate transcript). The one criterion that differs (Completeness C3) rests on text present or absent in the files, so order cannot change it.

## Combined Scoring

| Variant | Quant × 0.5 | Qual × 0.5 | Score |
|---|---|---|---|
| Variant 1 | 0.500 | 0.217 | 0.717 |
| Variant 2 | 0.500 | 0.233 | 0.733 |

Margin 1.6% < 5%, so the tiebreaker applies. Level 1 (debate points won): Variant 2 won 1 (C-001), Variant 1 won 0. Decided at level 1.

## Selected Base: Variant 2 (issue-worker-t1, `flags-t1.md`)

- **Selection rationale**: code-grounded reasons, won C-001, tiebreaker level 1.
- **Strengths to preserve**: verified code locations in the Type reason.
- **Strengths to incorporate**: Variant 1's point that `cli` also covers `superclaude update`, which shares `install_all_skills` (A-002, `main.py:401-403`), so the merged Type reason is accurate about scope.
