# Base Selection

## Quantitative Scoring (50% weight)

Source requirements for RC = the 13 consensus items after Round 2 (12 merged findings plus INV-001). Computed by the orchestrator from the three card texts.

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.46 (6/13) | 0.46 (6/13) | 0.08 (1/13) |
| Internal consistency (IC) | 0.25 | 0.95 | 0.85 | 1.00 |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.90 | 0.70 |
| Dependency completeness (DC) | 0.15 | 0.97 | 0.83 | 1.00 |
| Section coverage (SC) | 0.15 | 1.00 | 0.67 | 0.67 |
| **quant_score** | | **0.806** | **0.710** | **0.629** |

IC notes: V1 F5 overstated (row 4 bypass needs two conditions); V2 F1 over-rated blocking and F2 label inconsistent. DC notes: 8 of V2's 47 citations lost markdown backticks in quotes (pre-check quote-not-found); one HTML-escaped `<` in V1 F6 restored.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Subtotals out of 5 per dimension (orchestrator judgement, evidence = the citation checks of Round 1 and 2 advocates and the pre-check):

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 | 4 | 1 |
| Correctness | 4 | 3 | 4 |
| Structure | 4 | 3 | 3 |
| Clarity | 4 | 4 | 4 |
| Risk Coverage | 3 | 3 | 1 |
| Invariant & Edge Case Coverage | 4 | 3 | 1 |
| **Total / 30** | **22** | **20** | **14** |
| **qual_score** | **0.733** | **0.667** | **0.467** |

### Edge Case Floor Check
All variants score at least 1/5 on Invariant & Edge Case Coverage (V1 4, V2 3, V3 1): all eligible.

## Position-Bias Mitigation
LIMITATION, stated plainly: the dual-pass (forward and reverse order) evaluation was NOT run as two independent evaluations. The qualitative layer is a single orchestrator pass; the order of advocates in Round 1 was parallel and Round 2 followed input order (V1, V2, V3). Position-bias mitigation is therefore degraded (`fallback_mode: true`).

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Final |
|---|---|---|---|
| V1 | 0.403 | 0.367 | **0.770** |
| V2 | 0.355 | 0.333 | 0.689 |
| V3 | 0.315 | 0.233 | 0.548 |

Margin V1 over V2: 8.1 points (above the 5-point tiebreaker band; no tiebreaker applied).

## Selected Base: Variant 1 (reviewer-1, analyzer persona, sonnet class)

- Selection rationale: highest combined score; the only card that audits the spec's decision tables; its findings C-001..C-006 survived Round 1 and Round 2 verification by all advocates.
- Strengths to preserve: the decision-table findings with line citations; honest scope statement.
- Strengths to incorporate: V2's acceptance-criterion gaps (C-007, C-008, C-009, C-010, C-011, C-012), V3's Task 2 grep finding (C-013), the INV-001 probe finding, and the Round 2 blocking rulings.
