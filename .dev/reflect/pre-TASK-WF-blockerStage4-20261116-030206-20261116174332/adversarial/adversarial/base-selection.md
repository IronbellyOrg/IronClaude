# Base Selection

Variants: V1 (reviewer 1, analyzer, sonnet class), V2 (reviewer 2, haiku class), V3 (reviewer 3, refactorer, opus class).

## Quantitative Scoring (50% weight)

The "source requirements" for RC are the ten content diff points the debate accepted (C-001 to C-010; C-011 was dropped). A variant covers a point when one of its findings raises it. IC counts contradictions found by the debate (V1: the wrong plan-line citation X-004 and its mislabelled F1 category; V3: the F8 paraphrase X-005, later judged not a factual error but counted here as a contradiction candidate) against the cited claims of the card. SR counts concrete indicators (numbers, file:line, backticked tokens, long quotes) against vague words (the SKILL's list: none found in any card). DC counts broken internal references (V1: one wrong plan line). SC compares the number of top-level sections (all three have Verdict, Findings, Checked, Self-report). Script output is in the audit log row of Wave 4.

| Metric | Weight | V1 | V2 | V3 |
|--------|--------|----|----|----|
| Requirement coverage (RC) | 0.30 | 0.6000 (6 of 10) | 0.3000 (3 of 10) | 0.8000 (8 of 10) |
| Internal consistency (IC) | 0.25 | 0.8462 (2 in 13 claims) | 1.0000 (0 in 17) | 0.9630 (1 in 27) |
| Specificity ratio (SR) | 0.15 | 1.0000 | 1.0000 | 1.0000 |
| Dependency completeness (DC) | 0.15 | 0.9231 | 1.0000 | 1.0000 |
| Section coverage (SC) | 0.15 | 1.0000 | 1.0000 | 1.0000 |
| **quant_score** | | **0.8300** | **0.7900** | **0.9307** |

## Qualitative Scoring (50% weight): additive binary rubric

Two independent passes with CEV evidence (pass 1: opus class, order V1, V2, V3; pass 2: sonnet class, reverse order V3, V2, V1), then one re-evaluation of the three disputed criterion-variant pairs by an opus-class agent whose verdict is final.

| Dimension (5 criteria each) | V1 | V2 | V3 |
|-----------------------------|----|----|----|
| Completeness | 5 | 5 | 4 |
| Correctness | 3 | 4 | 4 |
| Structure | 5 | 5 | 5 |
| Clarity | 4 | 4 | 4 |
| Risk coverage | 3 | 4 | 4 |
| Invariant and edge-case coverage | 5 | 3 | 5 |
| **Total (of 30)** | **25** | **25** | **26** |
| **qual_score** | 0.8333 | 0.8333 | 0.8667 |

Position-bias log: pass 1 totals 25, 25, 25; pass 2 totals 23, 25, 26. Disagreements found: 3 (V1 L5: pass 1 MET, pass 2 NOT MET; V1 R5: MET against NOT MET; V3 K1: NOT MET against MET). Re-evaluation verdicts: V1 L5 MET, V1 R5 MET, V3 K1 MET. Verdicts changed by re-evaluation: 2 of the 3 pass-2 or pass-1 verdicts moved (V1 pass 2 moved up twice to 25; V3 pass 1 moved up once to 26).

### Edge Case Floor Check
All three variants score at least 1 of 5 on invariant and edge-case coverage (V1 5, V2 3, V3 5): all eligible as base.

## Combined Scoring

| | quant (x0.50) | qual (x0.50) | combined |
|---|---------------|--------------|----------|
| V1 | 0.4150 | 0.4167 | 0.8317 |
| V2 | 0.3950 | 0.4167 | 0.8117 |
| V3 | 0.4653 | 0.4333 | **0.8987** |

Margin V3 over V1: 6.7 points (above the 5% tiebreaker band): no tiebreaker applied.

## Selected Base: Variant 3 (reviewer 3, refactorer, opus class)

Selection rationale: widest coverage of the accepted diff points (8 of 10), the cross-stage and retired-carrier checks (U-004), and the best combined score. Its one grade error (F1 blocking) is corrected in the merge; the debate settled it at MEDIUM.

Strengths to preserve: F4 (plugin FR-8 edit rationale), F5 (stale stage 3 text), F6 (doctor tests), F7 (forward reference), the Checked section on retired carriers, plugin decision and cross-stage facts.

Strengths to incorporate from non-base variants: V1's test simulation (U-001), the C-005 and C-006 findings, the cap re-count; V2's G9 to G14 status and the C-002 dissent with the roadmap SKILL.md line 563 evidence; the probe's INV-001 and INV-002 findings, which no card raised.

Judge note: the scorers and the debate orchestrator are all Claude-class models that also served as reviewers (class collision, `judge_class_collision: true`); a disjoint judge class does not exist in this environment.
