# Base Selection

## Quantitative layer (weight 0.50)

Requirement set for RC: the 23 deduplicated findings D-001..D-023 of the merged card (a variant covers a D item when one of its findings is a source of it).

| Metric (weight) | V1 analyzer | V2 qa | V3 refactorer | Basis |
|---|---|---|---|---|
| RC requirement coverage (0.30) | 13/23 = 0.57 | 9/23 = 0.39 | 9/23 = 0.39 | D source lists in `merged-verdict.yaml` |
| IC internal consistency (0.25) | 1.00 | 1.00 | 1.00 | no finding in any card contradicts another finding in the same card |
| SR specificity (0.15) | 9/12 = 0.75 | 6/9 = 0.67 | 9/9 = 1.00 | findings not tagged `[INFERRED]` / all findings |
| DC dependency completeness (0.15) | 1.00 | 1.00 | 1.00 | every `t1_ref` resolves to an F-NNN in `t1-card.md` |
| SC section coverage (0.15) | 12/12 = 1.00 | 9/12 = 0.75 | 9/12 = 0.75 | findings / max findings |
| quant_score | 0.834 | 0.730 | 0.780 | |

## Qualitative layer (weight 0.50), 30 binary criteria, CEV

| Dimension (5 each) | V1 | V2 | V3 | Key evidence |
|---|---|---|---|---|
| Completeness | 4 | 3 | 3 | V1 covers all 8 analyzer T1 items plus 4 new; V2 and V3 cover their slices plus cross-slice items |
| Correctness | 3 | 4 | 3 | V1: R1-05 fix edits the plan after the first `start` (managed-workspace.md:43); R1-03 fix stops a parked worker (orca-capabilities.md:114, :129); R1-06, R1-11 weak. V2: R2-08 weak; R2-02 blocking is the strongest reading. V3: R3-03 cost claim wrong (qa.md:310 gives FINAL the full plan); R3-08 fix stops on a decision question (orca-capabilities.md:111, :114) |
| Structure | 5 | 5 | 5 | one stance, severity, evidence list and fix per finding |
| Clarity | 4 | 5 | 4 | V2 states each pass/fail reading exactly |
| Risk coverage | 5 | 3 | 5 | V1: staging, hang, resume, retry ladder; V3: false AC-0.4, evidence lost on `--force` removal, retry ladder |
| Invariant and edge cases | 4 | 3 | 4 | all three above the 1/5 floor |
| qual_score | 25/30 = 0.833 | 23/30 = 0.767 | 24/30 = 0.800 | |

Position-bias check: pass 1 in order V1, V2, V3 and pass 2 in order V3, V2, V1 gave the same per-criterion verdicts; no re-evaluation needed.

## Combined

| Variant | quant | qual | combined |
|---|---|---|---|
| V1 analyzer (sonnet) | 0.834 | 0.833 | **0.834** |
| V3 refactorer (opus) | 0.780 | 0.800 | 0.790 |
| V2 qa (haiku/glm) | 0.730 | 0.767 | 0.749 |

Top two differ by 0.044 (5.3% of 0.834), just outside the 5% tiebreak window; had the tiebreak applied, level 1 (debate points won) still picks V1. Debate points won agree (V1 11, V3 9, V2 5).

## Selection

Base: **V1 (reviewer-1, analyzer, sonnet)**. It has the widest correct coverage of the deduplicated findings and the most debate points. Its two weak findings (R1-06, R1-11) and two fixes that conflict with executor or Orca rules (R1-05, R1-03) are corrected from V3 and from the evidence in the refactor plan.
