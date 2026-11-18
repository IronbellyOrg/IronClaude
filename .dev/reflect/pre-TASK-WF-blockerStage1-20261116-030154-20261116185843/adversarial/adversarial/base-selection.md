# Base Selection

Inputs: `debate/quant-scores.json` (script), `debate/scoring-notes.md` (qualitative passes, disagreement resolution and the table below), `debate/convergence-tracking.tsv`.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.962 | 0.885 | 0.962 |
| Internal consistency (IC) | 0.25 | 1.000 | 0.944 | 0.947 |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 | 1.000 |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 | 0.667 |
| Section coverage (SC) | 0.15 | 0.857 | 1.000 | 0.571 |
| **quant_score** | | **0.9671** | **0.9515** | **0.8610** |

Limit: SR saturates (a count of line references, names and numbers over a short vague-word list); RC is keyword presence over 26 review duties. The layer is deterministic, not precise.

## Qualitative Scoring (50% weight): additive binary rubric, two blind passes (sonnet class)

| Dimension (criteria) | V1 final | V2 final | V3 final |
|---|---|---|---|
| Completeness (5) | 3 | 3 | 5 |
| Correctness (5) | 4 | 4 | 4 |
| Structure (5) | 5 | 4 | 5 |
| Clarity (5) | 4 | 5 | 4 |
| Risk coverage (5) | 5 | 3 | 5 |
| Invariant and edge-case coverage (5) | 5 | 4 | 5 |
| Total /30 | 26 | 23 | 28 |
| qual_score | 0.8667 | 0.7667 | 0.9333 |

Key evidence (CEV, abridged): V3 C1-C5 met (checks brief decisions, stage 2 and stage 4, states "Not checked: ... section 9.3 defining files"); V3 K4 not met (it says the `doctor.py` literal makes PLAN:238 fail yet grades it non-blocking); V3 L4 not met (cites T1-F1, T1-F4, T1-F5, undefined in the card). V1 C1 and C5 not met (no brief check, no "not checked" section); V1 K2 not met (`IMPORTANT=Medium` clashes with SPEC:211 and SPEC:744); V1 L1 not met (hedged verdict). V2 K4 not met (blocking yes against its own MEDIUM row); V2 T3 not met (an audit-artifact finding mixed with plan findings); V2 R1, R4 not met (no likelihood, no cross-stage view); V2 E1 not met.

## Position-Bias Mitigation

Pass 1 (forward) totals 26, 22, 28; pass 2 (reverse) totals 25, 22, 28. Disagreements: 7 criterion-variant pairs of 90 (V1 C1, K1, K3; V2 R3, E4; V3 L4, E1); all re-evaluated with both passes' evidence in `debate/scoring-notes.md`; verdicts changed from a pass: 4 (V1 C1 stays 0 as pass 1; V1 K1 and K3 stay 1 as pass 1; V2 R3 and E4 become 1; V3 L4 stays 0 and E1 becomes 1, so changes against at least one pass: 7, against both: 0).
Edge-case floor: all three variants score at least 4 of 5, so all are eligible.

## Combined Scoring

| Variant | quant x 0.50 | qual x 0.50 | final |
|---|---|---|---|
| V1 | 0.4836 | 0.4333 | **0.9169** |
| V3 | 0.4305 | 0.4667 | 0.8972 |
| V2 | 0.4758 | 0.3833 | 0.8591 |

Margin V1 over V3: 2.2 percent, inside the 5 percent band: tiebreaker applied.
Tiebreaker level 1 (debate points won, majority winner per point): V1 8 (S-002, C-001, C-004, C-005, C-006, C-007, X-001, X-004), V3 5 (C-002, C-009, C-010, C-011, X-002), V2 4 (S-003, C-003, C-012, X-003). V1 leads by 3 points; the tiebreaker confirms V1 as the higher-scoring base. Judge class: the scorers are sonnet class, the class of variant 1's reviewer (`judge_class_collision: true`, a limit on the independence of this ranking).

## Selected Base: Variant 1 (reviewer 1, analyzer, sonnet class)

Selection rationale: highest combined score (0.9169) and most debate points; it alone found C-001 and traced it to the stage 2 consumer, and it is the only card that raised the consent-logic gap (C-005) and the NA-for-C consequence (C-004).
Strengths to preserve: finding blocks with `consequence`, `evidence`, `repair`; the earlier-findings check with live lines; the C-001 chain; C-004, C-005, C-006, C-007.
Strengths to incorporate from non-base variants: variant 3's C-009, C-010, C-011 and its "checked and found clean" list and brief-decision check; variant 2's C-002 and C-003 (graded non-blocking after the debate) and its audit-artifact finding C-012; variant 3's stale-quote finding C-008 and its REQ-02 citation (SPEC:211, SPEC:744) for the lens-scale values.
Weaknesses of the base to fix: the `IMPORTANT=Medium` repair (INV-001, INV-002), the hedged verdict, the `R3-Fk` id slip, no brief-decision check, no "not checked" section.
