# Base Selection (Step 3)

Evaluators: pass 1 (opus class, order V1, V2, V3) wrote `debate/scoring-pass1.md`; pass 2 (sonnet class, order V3, V2, V1) wrote `debate/scoring-pass2.md`. They did not read each other's file. Both applied `refs/scoring-protocol.md`: five quantitative metrics (RC against 12 review-coverage items, IC, SR, DC, SC) and the 30-criterion binary rubric with a Claim-Evidence-Verdict line per criterion. Correctness was judged against the debate's settled findings, not the cards' own claims.

## Quantitative Scoring (50% weight)

| Variant | Pass 1 quant | Pass 2 quant | Mean quant |
|---|---|---|---|
| V1 (analyzer, sonnet) | 0.808 | 0.838 | 0.823 |
| V2 (qa, haiku) | 0.890 | 0.945 | 0.918 |
| V3 (refactorer, opus) | 0.782 | 0.860 | 0.821 |

## Qualitative Scoring (50% weight) - additive binary rubric

| Variant | Pass 1 qual (met/30) | Pass 2 qual (met/30) | Mean qual |
|---|---|---|---|
| V1 | 0.733 (22) | 0.767 (23) | 0.750 |
| V2 | 0.600 (18) | 0.567 (17) | 0.583 |
| V3 | 0.833 (25) | 0.833 (25) | 0.833 |

## Edge Case Floor Check
All three variants scored at least 1 of 5 on the invariant and edge case dimension in both passes; no variant is ineligible.

## Position-Bias Mitigation
The two passes agree on rank (V3 first, V1 second, V2 third) and on eligibility. They differ in magnitude by at most 0.055 on a combined score (V2 quant 0.890 against 0.945 is the widest gap; pass 1 flagged the undefined-key scores and V1 completeness 4 as the likely sources). Protocol deviation, stated plainly: no per-criterion third evaluation was run for the individual criterion pairs that differ; the two combined scores per variant were averaged instead, because the base choice is decided by the tiebreaker below and not by any one criterion.

## Combined Scoring

| Variant | Pass 1 combined | Pass 2 combined | Mean combined |
|---|---|---|---|
| V1 | 0.770 | 0.802 | 0.786 |
| V2 | 0.745 | 0.756 | 0.751 |
| V3 | 0.808 | 0.846 | 0.827 |

Margin V3 over V1: 0.041 (4.1 percent), inside the 5 percent tiebreaker band.

## Tiebreaker (level 1: debate performance)
Points whose final grade follows a variant's own position and were contributed by that variant (final grades, Round 2): V1: C-002 (blocking, confirmed by all three advocates), C-003 (shared with V3), C-004, C-005, C-006, C-007, C-008, C-009 = 8 points. V3: C-003 (shared), C-013, C-014 = 3 points (C-015 and X-001/X-002 as separate points were dropped or folded). V2: C-011 = 1 point (C-010, C-012 dropped; S-002 dropped). Level 1 winner: V1 (8 against 3 and 1). Level 2 would also favour V1 (correctness criteria 5 of 5 in pass 1 against 4 for V3).

## Selected Base: Variant 1 (analyzer, sonnet class, `model: claude-gw-tier1b`)

- **Selection rationale.** V3 leads on the mean combined score by 4.1 percent, so the tiebreaker applies and V1 wins it on debate performance. V1 alone found the one defect that all three advocates graded blocking besides the stage 3 conflict (C-002: the mapping test pins what Task 5 removes) and holds the largest set of surviving findings in the format the brief asks for.
- **Strengths to preserve.** The F-line format; C-001 and C-002 with exact citations; the seven minor findings with citations that held on re-read (calibrator: 16 of 16 hold); the Checked section.
- **Strengths to incorporate.** From V3: the step-by-step walk of Task 6, the tracked-files-only scan consequence (C-013), the registry row model point (C-014) and the allow-list end-state check. From V2: the check of each earlier-review finding (F3, F4, F5, F6, F9, F12, F13) against the plan, the Tasks 1 to 6 against base Tasks 41 to 46 comparison, and the Task 2 cap-pin gap (C-011). From the invariant probe (Round 2.5): INV-006, INV-007, INV-008 (raises C-006), INV-012, INV-017 (raises C-008), INV-005, INV-010, INV-013, INV-014 and INV-015. From the debate: the dropped points and the reasons.
