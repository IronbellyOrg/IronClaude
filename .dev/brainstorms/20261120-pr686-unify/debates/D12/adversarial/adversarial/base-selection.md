# Base Selection: D12

## Quantitative Scoring (50% weight)

Source requirements used for RC (taken from the D12 question): R1 disposition of PR 661 plan sections; R2 `--plan`; R3 `--remaining`; R4 issue 689's move of brainstorm and design into create; R5 effect on the owner's claim chain; R6 an explicit keep/adapt/reject verdict; R7 fit with the claim-to-work pipeline. SR is a scripted proxy: concrete = backtick spans plus numbers (V1 163, V2 172), vague = hedging words from the rubric list (0 in both).

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 7/7 = 1.000 | 6/7 = 0.857 (no explicit R6 verdict) |
| Internal consistency (IC) | 0.25 | 1.000 (0 contradictions found) | 1.000 (0 contradictions found) |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 |
| Section coverage (SC) | 0.15 | 7/7 = 1.000 | 6/7 = 0.857 |
| **quant_score** | | **1.0000** | **0.9357** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Two independent evaluator subagents scored the 30 criteria with a Claim-Evidence-Verdict line each (full per-criterion output in the two evaluator hand-backs; summarised here). Pass 1 order V1 then V2; pass 2 reverse order V2 then V1.

| Dimension | V1 pass 1 | V1 pass 2 | V1 final | V2 pass 1 | V2 pass 2 | V2 final |
|---|---|---|---|---|---|---|
| Completeness (5) | 4 | 4 | 4 | 2 | 2 | 2 |
| Correctness (5) | 5 | 5 | 5 | 5 | 5 | 5 |
| Structure (5) | 5 | 5 | 5 | 5 | 5 | 5 |
| Clarity (5) | 4 | 4 | 4 | 3 | 3 | 3 |
| Risk coverage (5) | 2 | 3 | 1 | 4 | 4 | 4 |
| Invariant and edge case (5) | 4 | 4 | 4 | 5 | 5 | 5 |
| **Total (30)** | 24 | 25 | **23** | 24 | 24 | **24** |

Evidence notes (CEV, one line per dimension of what decided it): Completeness V1: R1 to R7 and a KEEP / KEEP-ADAPT / REJECT block (C1 MET); V2: no verdict (C1 NOT) and no out-of-scope statement (C5 NOT); both lack completion criteria (C4 NOT). Correctness: both evaluators spot-checked at least three cited facts per paper and found no hallucination; open note: V1 quotes issue 302's original simple-feature chain which master has since superseded (`chains.md` simple row, 2026-11-18), attributed to issue 302, not to master. Clarity: both leave codes such as B2, B4, K27, T1 undefined (L4 NOT); V2 gives no next steps (L5 NOT). Risk: V1 lists two risks without likelihood or impact; V2 lists five with impact but no mitigation per risk. Edge cases: V1 has no count or range divergence (E4 NOT).

### Edge Case Floor Check
Floor is 1/5 on Invariant and edge-case coverage. V1 4/5 and V2 5/5: both eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Risk V1 (3 risks with likelihood or impact) | V1 | MET | NOT | no | NOT (paper lists two risks, no likelihood or impact) |
| Risk V2 (mitigation per risk) | V1 | NOT | MET | no | NOT (only the `--remaining` risk has a stated mitigation) |
| Risk V5 (validation mechanism) | V1 | NOT | MET | no | NOT (the check that gates the short chain is a rule, not a risk-detection mechanism) |

Disagreements found: 3 criterion-variant pairs, all on V1's risk dimension. Verdicts changed by re-evaluation: 3 (one from each pass in each case, all resolved to NOT MET by the orchestrator re-reading the cited sections). The other 57 of the 60 criterion-variant verdicts agreed between the passes.

## Combined Scoring

| Variant | quant x 0.50 | qual x 0.50 | Final score |
|---|---|---|---|
| Variant 1 (OURS) | 0.5000 | 0.3833 (23/30) | **0.8833** |
| Variant 2 (CLAY) | 0.4679 | 0.4000 (24/30) | **0.8679** |

Margin: 1.5 percent, under the 5 percent tiebreaker trigger.

Tiebreaker applied: Yes, level 1 (debate performance). Points won in the Step 2 scoring matrix: Variant 1 wins 8 (S-002, C-004, C-006, C-007, C-009, C-013, C-014, X-002); Variant 2 wins 1 (C-010); 11 points are HYBRID or tie (S-001, S-003, C-001, C-002, C-003, C-005, C-008, C-011, C-012, X-001, X-003). Variant 1 wins the tiebreak. The brief's weighting rule (a tie goes to OURS) points the same way and was not needed to decide.

## Selected Base: Variant 1 (OURS, `position-OURS.md`)

**Selection rationale.** Highest combined score (0.8833 against 0.8679, margin 1.5 percent) and the tiebreak by points won (8 against 1). The scoring split: V1 wins on requirement coverage and verdict (it ends with a disposition list), V2 on risk coverage and edge cases.

**Strengths to preserve from the base.** The disposition list (KEEP PR 661, KEEP-ADAPT PR 690, REJECT 689's moves); B2 and the claim chain as the owner's recorded design; the claim-reads-the-plan rule as the fix for double planning; the actor and tool-list objection to 689.

**Strengths to incorporate from Variant 2.**
1. `plan_body.py`, plain `--plan` and `--remaining` kept (U-005, C-003): deterministic body write; `--remaining` self-contained.
2. The capability gap for pre-661 and hand-filed issues (U-006) and the design's dependency on `--plan` (U-007).
3. `--mode other` and the GitHub form fields as a separate small change (C-010, U-008).
4. Complex features seeded with the filed plan, a higher tier floor only for medium and complex (C-011), a split refusal guard (C-008).
5. Risk coverage: V2's five risks with impact (stale design, unstated runner, blocked older issues, 690's `--remaining` consumer unbuilt, follow-up issue 665).
6. Open issues from Round 2 that must stay attached: the five HIGH invariant findings.
