# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Computation notes |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.50 | 1.00 | 13 plan AC: V2 cites each one by row; V1 states "13 audited, 13 adherent" with per-AC evidence only for T3/T4 code |
| Internal consistency (IC) | 0.25 | 0.96 | 0.96 | one false claim each in ~25 scorable claims (V1: R1-F7 "no 262 figure"; V2: "no artifact documents the guard") |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.90 | both cite file:line almost everywhere |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | internal references (finding IDs, gap IDs) resolve |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 4 top-level sections each |
| **quant_score** | | **0.825** | **0.975** | (RC×0.30)+(IC×0.25)+(SR×0.15)+(DC×0.15)+(SC×0.15) |

## Qualitative Scoring (50% weight) — additive binary rubric (CEV, summarized)

| Dimension (5 each) | V1 | V2 | Decisive evidence |
|---|---|---|---|
| Completeness | 3 | 4 | V2 per-AC table (variant-2 AC audit); V1 no AC rows; both note out-of-scope items |
| Correctness | 3 | 3 | V1: R1-F7 false (verify-logs:17), R1-F4 misclassified; V2: R2-F1 "no artifact" false, R2-F1/F2 misclassified (calibrations) |
| Structure | 4 | 4 | both follow the reflect card shape |
| Clarity | 3 | 4 | V2 concrete rewording for CHANGELOG:11; V1 "accepted, weakly" not a taxonomy value |
| Risk coverage | 4 | 3 | V1: None stderr, macOS getsid, subreaper, pkill width; V2: process-group regression check, provenance gaps |
| Invariant & edge-case coverage | 4 | 2 | V1 covers guard edge, platform boundary, subreaper interaction, pid-reuse/regex; V2 covers untested branch, group-signal regression |
| **Total / 30** | **21 (0.700)** | **20 (0.667)** | |

Edge-case floor (≥ 1/5): both eligible.

## Position-Bias Mitigation

Pass 1 (V1, V2) and pass 2 (V2, V1) agreed on every dimension total above, except Clarity (pass 1 V1 = 4, pass 2 V1 = 3). Re-evaluation with both pieces of evidence: "accepted, weakly" is not a taxonomy value, and the CHANGELOG remark has no concrete wording, so V1 = 3 is final. Disagreements found: 1; verdicts changed: 1.

## Combined Scoring

| Variant | quant × 0.5 | qual × 0.5 | Combined |
|---|---|---|---|
| Variant 1 (sonnet, analyzer) | 0.4125 | 0.3500 | **0.763** |
| Variant 2 (haiku = glm-5.3, qa) | 0.4875 | 0.3333 | **0.821** |

Margin 0.058 (> 0.05): no tiebreaker. Debate points won: V1 6 (C-001, C-002, C-007, C-009, X-002, X-003), V2 5 (S-002, C-004, C-008, C-011, X-001); 5 ties; A-001 shared.

## Selected Base: Variant 2 (reviewer 2, qa)

- Rationale: its per-AC table makes the audit re-derivable, it holds the correct verification figure, it records the process-group regression check, and it is explicit about which results come only from the implement-leg logs.
- Strengths to preserve: the AC audit table; the R2-F4 `make sync-dev` record; the provenance notes (G1, G2); the regression sweep; the CHANGELOG:11 rewording.
- Strengths to incorporate from Variant 1: the guard classification (necessary, LOW) and the dead-pty reason; the necessary class for the T1 extra assertions; the None-stderr advisory (with the calibrator's correction that the old code already failed per request); macOS getsid portability; the subreaper caveat; the `pkill -f` regex width; the invariant-probe residuals (INV-001, INV-002 residual, INV-006).
