# Base Selection: structural_checkers.py Resolution

## Quantitative Scoring (50% weight)
Because executable code is identical across all three variants, the metrics that key off runtime behavior (RC, IC, DC) are tied at the maximum. Differentiation is only on comment-carried specificity/documentation.

| Metric | Weight | V1 (ours) | V2 (theirs) | V3 (proposed) | Note |
|--------|--------|-----------|-------------|---------------|------|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | 1.00 | identical code → identical MD/D3 coverage |
| Internal consistency (IC) | 0.25 | 1.00 | 0.97 | 1.00 | V2 has the dead foreign-repo path (an unresolvable internal reference) |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.85 | 0.97 | V3 carries richest concrete provenance (PR# + TASK-RF + design IDs) |
| Dependency completeness (DC) | 0.15 | 1.00 | 0.90 | 1.00 | V2's `/config/workspace/TUIBBS-scp/...` is an unresolvable reference in this repo |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | identical structure |
| **quant_score** | | **0.992** | **0.949** | **0.995** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric (abbreviated for quick mode)
| Dimension (5 crit each) | V1 | V2 | V3 |
|-------------------------|----|----|----|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 5/5 | 4/5 (foreign-path = a false/unresolvable cross-ref) | 5/5 |
| Structure | 5/5 | 4/5 (duplicate-comment risk on auto-merge) | 5/5 |
| Clarity | 5/5 | 4/5 (terse hunk-1 comment invites arch-lint dedup mistake) | 5/5 |
| Risk Coverage | 4/5 | 4/5 | 5/5 (V3 explicitly notes A-001 cross-file dependency + drops the liability) |
| Invariant & Edge Case Coverage | 4/5 | 4/5 | 5/5 (V3 empirically tested: milestone-distinctness + non-MD regression verified) |
| **qual_score** (/30) | 28/30=0.933 | 25/30=0.833 | 30/30=1.000 |

Edge Case Floor (1/5): all variants ≥ 4/5 → all eligible.

## Position-Bias Mitigation
Forward pass (V1,V2,V3) and reverse pass (V3,V2,V1) agree: V3 ranks first in both orders (its content is a strict superset of V1's valuable comments and V2's TASK-RF ref, minus V2's liability). No disagreement to resolve.

## Combined Scoring
| Variant | quant×0.5 | qual×0.5 | **combined** |
|---------|----------|----------|--------------|
| V1 (ours) | 0.496 | 0.467 | **0.963** |
| V2 (theirs) | 0.475 | 0.417 | **0.892** |
| V3 (proposed) | 0.498 | 0.500 | **0.998** |

Margin V3 over V1 = 3.5% (> 5%? no, < 5% would trigger tiebreaker; 0.998-0.963 = 0.035 = 3.5% → within 5%, tiebreaker considered).
- **Tiebreaker L1 (debate performance)**: V3 won 4/4 contested comment points + both unique-contribution calls → V3.

## Selected Base: Variant 3 (proposed-resolution)
- **Selection rationale**: V3 is byte-identical in executable code to the converged port that BOTH branches independently produced (zero regression by construction), AND it carries the strict union of the load-bearing comment content (V1's arch-lint Rule 2 rationale + DISTINCT-forms explanation; V2's TASK-RF design-doc provenance) while excluding V2's only liability (a foreign-repo absolute path that cannot resolve in this tree). It is also free of the duplicate "We also track source family" comment that a naive git auto-merge introduces.
- **Strengths to preserve**: identical MD-family canonicalizer + D3 allowlist branches (empirically verified); single-copy comments.
- **Strengths incorporated from non-base**: TASK-RF-20260531-044100 provenance refs (from V2) merged into hunks 1–3.
- **Rejected**: V2's `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md L665` absolute path (U-001).
