# Base Selection (refactor cycle 1)

Scored inline by the orchestrator (no separate debate-orchestrator agent; recorded as a degradation).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Computation |
|--------|--------|-----------|-----------|-------------|
| Requirement coverage (RC) | 0.30 | 1.000 | 0.714 | Section-level match over source sections Fix 1, Fix 2, Fix 3, Fix 4, Quality rules, Noticed, Review Feedback. V1 touches all 7; V2 has no Fix 4 or Noticed finding. |
| Internal consistency (IC) | 0.25 | 0.955 | 0.944 | V1: 1 inconsistency in 22 claims (ready_with_notes vs its own mediums). V2: 1 in 18 (R2-1 recommendation drops Task 7 from its own required ancestors). |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 | No vague indicators in either card's claims. |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 | All card_ref values resolve to t1-card claims C1-C7. |
| Section coverage (SC) | 0.15 | 1.000 | 1.000 | Same top-level keys. |
| **quant_score** | | **0.989** | **0.900** | |

## Qualitative Scoring (50% weight) — CEV summary

| Dimension | V1 | V2 | Decisive evidence |
|-----------|----|----|-------------------|
| Completeness | 4/5 | 3/5 | V1 missed R2-5; V2 missed R1-1, R1-2 and the prior-finding audit. |
| Correctness | 3/5 | 3/5 | V1: R1-7 contradicts source:55, R1-8/R1-9 misread source:80/:81. V2: R2-3 rename order reversed (measured bytes), R2-1 recommendation inconsistent. |
| Structure | 5/5 | 5/5 | Both follow the brief schema. |
| Clarity | 4/5 | 4/5 | Both leave abbreviations undefined. |
| Risk coverage | 4/5 | 3/5 | V1 names the heredoc false-fail and fail-closed residue; V2 no external-dependency risk. |
| Invariant & edge case | 5/5 | 3/5 | V1: baseline collection (R1-1), argument guard (R1-2), state across steps (R1-3), rename counts (R1-6), interaction (R1-12). V2: rename (R2-3), guard (R2-5), count (R2-4). |
| **qual_score** | **25/30 = 0.833** | **21/30 = 0.700** | |

Edge-case floor: both eligible. Position-bias: single-evaluator dual pass, 0 disagreements.

## Combined Scoring

| Variant | Quant ×0.5 | Qual ×0.5 | Final |
|---------|-----------|-----------|-------|
| Variant 1 | 0.494 | 0.417 | **0.911** |
| Variant 2 | 0.450 | 0.350 | 0.800 |

Margin 11.1%; no tiebreaker. Debate points won: V1 4, V2 6, tie/accept 3 (V2 won the verdict and dependency points; V1 won the evidence-bearing points).

## Selected Base: Variant 1 (sonnet:analyzer, reviewer-1)
- Preserve: R1-1, R1-2, R1-5, R1-6, R1-10, R1-11; R1-3 as optional hardening; R1-4 as low.
- Incorporate from Variant 2: overall verdict not_ready; R2-1 (with the renumbering); R2-4; R2-5; C3 rejected as a defect (R2-7).
- Drop: R1-7 as a defect (keep only the instruction-wording note), R1-8, R1-9; R2-8 as matrix corrections only.
