# Base Selection: D14

All figures are evaluator estimates (two evaluator agents, forward order and reverse order), not measurements. Full tables: `rounds/qual-pass1.md` (order V1 then V2) and `rounds/qual-pass2.md` (order V2 then V1). Scores rate the quality of the OPENING position papers as documents; they do not decide the question (the verdict applies the owner weighting rule on top).

## Quantitative scoring (50 percent weight)

| Metric (weight) | V1 OURS pass 1 | V1 pass 2 | V2 CLAY pass 1 | V2 pass 2 |
|---|---|---|---|---|
| quant score | 0.919 | 0.890 | 0.824 | 0.813 |

Mean quant: V1 0.905, V2 0.819.

## Qualitative scoring (50 percent weight), 30 binary criteria with evidence

| | V1 OURS | V2 CLAY |
|---|---|---|
| MET, pass 1 | 22/30 (0.733) | 15/30 (0.500) |
| MET, pass 2 | 22/30 (0.733) | 15/30 (0.500) |
| Edge-case floor (Invariant and edge-case dimension, minimum 1/5) | 5/5 (pass 1), 5/5 (pass 2) | 1/5 (pass 1), 2/5 (pass 2) |

Both variants clear the floor, so both are eligible as base.

## Position-bias mitigation

The two passes reached identical MET totals for each variant (22 and 15); the quant figures differ by 0.029 (V1) and 0.011 (V2). No pass-level reversal of the winner. The per-criterion disagreement log was not itemised by the evaluators (UNVERIFIED which individual criteria differ), so no re-evaluation prompt was needed.

## Combined scoring

| | V1 OURS | V2 CLAY |
|---|---|---|
| Pass 1 | 0.826 | 0.662 |
| Pass 2 | 0.812 | 0.656 |
| Mean | 0.819 | 0.659 |

Margin 0.160 (about 16 points), well outside the 5 percent tiebreak band. Tiebreak not applied. (Had it been needed: debate points won OURS 12 and 13, CLAY 0, HYBRID 9 and 8, in the two passes.)

## Selected Base: Variant 1 (OURS, position-OURS.md)

Selection rationale: higher on requirement coverage (every one of the nine named items has a disposition in its claim), concrete cited facts, risk and ordering section, and the edge-case dimension (the ordering break, planb collision, ship-gate flag). The weaker CLAY paper scores lower because it names five of nine items, has no stated start conditions, and (found in debate) relies on two premises the verdicts had already retired (the gate dropped; "enabled: false" as an invariant).

Strengths to preserve from the base: revert PR 682 first as a new PR; never merge PR 686 as is; persisted names renamed before any merge; evidence-cited facts.

Strengths to incorporate from the non-base variant (and from the debate rounds): two lanes (independent work does not queue behind the revert); KEEP-ADAPT in place instead of "close the original" (no verdict says CLOSE); PR 690 ends the dangling `/sc:issue --plan` reference in PR 683; `enabled` default needs a pinned test; credit and review history are kept; PR 686 is held as a draft until adapted.

Note on process: the evaluators knew the final debate state when scoring the opening papers, so the two passes are not blind to the debate (UNVERIFIED degree of influence).
