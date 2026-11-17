# Base selection (hybrid scoring)

Two independent scorer passes ran in parallel: pass 1 in input order V1, V2, V3 (sonnet class), pass 2 in reverse order V3, V2, V1 (opus class). Both applied the same 8-item review assignment (R1 to R8), the 5 quantitative metrics and the 30-criterion binary rubric with a claim-evidence-verdict line per criterion. The orchestrator reconciled disagreements by re-reading the live files where a verdict turned on a fact.

## Quantitative scoring (50% weight)

| Metric (weight) | V1 pass 1 / pass 2 | V2 pass 1 / pass 2 | V3 pass 1 / pass 2 |
|---|---|---|---|
| Requirement coverage RC (0.30) | 7/8 / 7/8 | 4/8 / 3/8 | 6/8 / 6/8 |
| Internal consistency IC (0.25) | 1.00 / 0.94 | 1.00 / 1.00 | 1.00 / 1.00 |
| Specificity SR (0.15) | 0.94 / 0.94 | 0.88 / 0.80 | 0.93 / 0.94 |
| Dependency completeness DC (0.15) | 0.57 / 0.57 | 0.29 / 0.00 | 0.67 / 0.80 |
| Section coverage SC (0.15) | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| quant score | 0.89 / 0.88 | 0.73 / 0.63 | 0.87 / 0.89 |
| quant used (mean of the two passes) | 0.885 | 0.68 | 0.88 |

The DC losses come from key abbreviations (V1 and V3 reuse the keys "S1" and "S3" for spec bullets; V2's header keys are unused). The card header lines of V2 that read "as in the other cards" were written by the orchestrator when saving the card; they are not charged to V2 here.

## Qualitative scoring (50% weight), additive binary rubric

Subtotals per dimension (Completeness / Correctness / Structure / Clarity / Risk / Invariant and edge case), final after reconciliation:

| Variant | Pass 1 | Pass 2 | Disagreements and resolution | Final |
|---|---|---|---|---|
| V1 | 3/4/5/5/5/5 = 27 | 3/2/5/4/5/5 = 24 | Correctness 1: V1 says "Every test path in the Task 5 run list exists (checked by Glob)"; `test_review_severity_registry.py`, `test_review_merge_rule_scan.py` and `test_review_brief_rests_on.py` do not exist (re-checked with `test -e`): NOT MET (pass 2 right). Correctness 4: Verdict "H1 to H5 fixed" against Checked "H2 is recorded as an exclusion" is loose wording, not a contradiction: MET (pass 1 right). Clarity 4: "lead T1-1" is not defined in the card: NOT MET (pass 2 right). | 3/3/5/4/5/5 = 25 |
| V2 | 3/4/3/4/4/2 = 20 | 4/4/5/4/4/3 = 24 | Completeness 3: "earlier-stage generated files remain future deliverables" cites cross-stage prerequisites: MET. Structure 4 and 5: the "SRC4" key line was added by the orchestrator, F-ids and the fixed fields are present: MET. Invariant 5: no interaction-effects analysis: NOT MET. | 4/4/5/4/4/2 = 23 |
| V3 | 4/4/4/4/5/5 = 26 | 4/4/5/4/5/5 = 27 | Structure 5: categories written as "other (stale cross-reference)" keep the fixed field: MET. | 4/4/5/4/5/5 = 27 |

Edge-case floor (Invariant and edge-case dimension, 1/5 required): V1 5/5, V2 2/5, V3 5/5. All three are eligible.

## Position-bias mitigation

Disagreements between the two passes: V1 Correctness 1 and 4, V1 Clarity 4, V2 Completeness 3, V2 Structure 4 and 5, V2 Invariant 5, V3 Structure 5 (9 criterion-variant pairs). Re-evaluated with both evidence lines; verdicts changed from pass 1 in 3 pairs (V1 Correctness 1, V1 Clarity 4, V2 Invariant 5) and from pass 2 in 3 pairs (V1 Correctness 4, V2 Structure 4 and 5 counted as one resolution each).

## Combined scoring

| Variant | quant (0.50) | qual (0.50) | combined |
|---|---|---|---|
| V1 (analyzer, sonnet) | 0.885 | 25/30 = 0.833 | 0.859 |
| V2 (qa, haiku) | 0.68 | 23/30 = 0.767 | 0.723 |
| V3 (refactorer, opus) | 0.88 | 27/30 = 0.900 | 0.890 |

Margin between the top two: 0.031, below 5 percent, so the tiebreaker protocol applies.

## Tiebreaker

Level 1, debate performance (points won in Step 2, by the majority of the three Round 1 "superior" fields, reading the Round 2 updates): V1 won 7 points (S-001, C-001, C-006, C-007, C-008, C-009, X-002), V3 won 3 (C-003, C-004, X-003), V2 won 2 (C-011, X-001); C-002, C-005 and C-010 were ties. V1 has the most points: the tiebreaker is decided at level 1 for V1. Tiebreaker applied: yes (level 1); margin 3.1 percent.

## Selected Base: Variant 1 (analyzer, sonnet)

Selection rationale: V1's verdict and grading are the ones the debate settled on (PASS with Medium findings, no blocking finding): after Round 2 every advocate agreed with it. V3 scores higher on the rubric but its one blocking finding (cap count) was graded Medium by its own advocate, so using V3 as base would require rewriting its verdict and its first finding. V2's three blocking findings were withdrawn or lowered by its own advocate.

Strengths to preserve from V1: the status of each earlier finding H1 to H13 with live recounts; the sibling doubt lines (C-008); the live-file counts.

Strengths to incorporate: from V3, the Rule 6 heading dependency (C-004), the digest-only positive greps (C-003, shared with V2), the quoted Task 1 and Task 2 acceptance lines and the exact fix for the cap count (state whether the bullet is folded, set the expected count to match); from V2, the plugin and pointer items as recorded decisions (C-006, C-007) and the matrix-completeness note (C-011). Corrections to V1: remove the false "every test path exists (checked by Glob)" statement (three test files are created by earlier stages) and raise C-004, C-007, C-008 and C-009 to the debate's settled grades.
