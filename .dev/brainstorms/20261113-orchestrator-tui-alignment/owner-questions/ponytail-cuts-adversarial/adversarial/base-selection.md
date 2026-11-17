# Base Selection

Condensed for depth quick: quantitative metrics RC, SR and SC are computed from the files (script run 2026-11-16); IC and DC are manual estimates; qualitative CEV is condensed to one evidence note per dimension, not per criterion (shortcut named; upgrade by re-scoring with the full 30-row CEV if this result is contested).

## Quantitative Scoring (50% weight)
| Metric | Weight | V1 | V2 | V3 | How |
|---|---|---|---|---|---|
| RC requirement coverage | 0.30 | 1.00 | 1.00 | 1.00 | All 22 source IDs have a row (grep of `^| Cnn `) |
| IC internal consistency | 0.25 | 0.92 | 0.96 | 0.92 | Manual. V1: C03 "CUT (close)" conflicts with its own risk note. V3: C04, C05 KEEP while its own check (a) and (c) came back TRUE |
| SR specificity | 0.15 | 1.00 | 0.98 | 1.00 | Proxy: file:line, numbers and code names versus vague words (43/0, 57/1, 20/0) |
| DC dependency completeness | 0.15 | 1.00 | 1.00 | 1.00 | Manual: internal references (C21 with C17, C08 with C18) resolve |
| SC section coverage | 0.15 | 1.00 | 1.00 | 1.00 | No H2 headings in any variant (0 of max 0), treated as equal |
| quant_score | | 0.980 | 0.987 | 0.980 | The mechanical metrics barely separate the variants |

## Qualitative Scoring (50% weight): additive binary rubric, condensed
| Dimension (5 criteria each) | V1 | V2 | V3 | Evidence note |
|---|---|---|---|---|
| Completeness | 4 | 4 | 3 | V1, V2 name dependencies and owner-decision limits; V3 gives no dependency or out-of-scope statement |
| Correctness | 3 | 4 | 4 | V1 first said "no caller" for `slo_numbers` and "4,000 lines" without a check; V2's 26-test and file-mode claims are unverified but flagged; V3's checks (a) to (g) held on master |
| Structure | 4 | 4 | 4 | Same table form; V3 adds a claims block; none has a table of contents |
| Clarity | 4 | 4 | 3 | V3's 94 to 99 percent confidences and terse risk cells ("Hides executable-selection differences") are not actionable |
| Risk coverage | 4 | 5 | 3 | V2 names the harm per kept item (gate flip, public repo, pushed commit); V3 repeats the risk of cutting without naming the harm |
| Invariant and edge-case coverage | 2 | 4 | 3 | V2 found the side-branch gate flip and the `validate_approvers` residual; V3 found the probe-runs-candidate and caller-scope cases; V1 found the C21/C17 coupling only |
| Total (of 30) | 21 | 25 | 20 | |
| qual_score | 0.700 | 0.833 | 0.667 | |

Edge-case floor (1 of 5): all three pass.

## Position-Bias Mitigation
First pass in input order (V1, V2, V3); second pass in reverse order (V3, V2, V1) on every dimension, by the same evaluator (the orchestrating session; a single evaluator, not two independent ones). The reverse pass reproduced every dimension total; no verdict was re-evaluated. Limit: one evaluator cannot remove its own bias; the 6.8-point margin below is the real protection.

## Combined Scoring
| Variant | 0.5 x quant | 0.5 x qual | Score |
|---|---|---|---|
| V1 opus:architect | 0.490 | 0.350 | 0.840 |
| V2 sonnet:security | 0.494 | 0.417 | 0.910 |
| V3 haiku:analyzer | 0.490 | 0.333 | 0.823 |

Margin between the top two: 0.07 (7 points), above the 5 percent tiebreaker band, so no tiebreaker applies. For the record, debate performance (points won) also favours V2: advocates picked V2 on 15 of 22 contested points.

## Selected Base: Variant 2 (sonnet:security)
- Rationale: it kept every owner answer and every trust-boundary gate, found the one real hazard in the side checkout (a pushed backup would carry the agent-made gate flip), and named the harm for each KEEP. All three advocates, including V1's and V3's own, moved toward its verdicts.
- Strengths to preserve: C23b hold on the side-branch commits; C01 local-copy-with-hash method; KEEP on C12, C13, C21, C22; DEFER instead of delete on C15, C17, C18.
- Strengths to incorporate: from V1, the C21-with-C17 coupling, the freeze-and-defer spine (C07 to C11, C16, C19, C20) and the explicit owner-decision labels; from V3, the C04 residual line, "backup is not owner approval", the point that a two-output capture does not replace the comparison and message tests (they are deferred, not erased), and that a blanket freeze must not block the requested summaries (C19).
