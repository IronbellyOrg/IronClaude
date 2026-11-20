# Base Selection

Method note (disclosure): the metrics below were estimated by reading the two papers, not computed by a script. The qualitative rubric was applied in one pass by the orchestrating session. The dual-pass position-bias check was NOT run, so treat the scores as indicative; the margin is small either way and the merged design takes the strengths of both.

## Quantitative Scoring (50% weight)
| Metric | Weight | V1 | V2 |
|---|---|---|---|
| Requirement coverage (R3, R4, R5, R6, R8, R9 touched) | 0.30 | 0.67 | 0.78 |
| Internal consistency (V1 says "unchanged" yet adds a loop and a rate flag; V2 says "no change to github.py" which is false) | 0.25 | 0.85 | 0.80 |
| Specificity (file:line and numbers) | 0.15 | 0.80 | 0.88 |
| Dependency completeness | 0.15 | 0.80 | 0.85 |
| Section coverage (both 6 sections) | 0.15 | 1.00 | 1.00 |
| **quant_score** | | **0.81** | **0.85** |

## Qualitative Scoring (50% weight)
| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 4/5 | 5/5 |
| Correctness (one false claim each, found by both advocates) | 3/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 |
| Risk coverage | 3/5 | 4/5 |
| Invariant and edge case coverage (floor needs 1/5) | 2/5 | 3/5 |
| **qual_score** (of 30) | 22/30 = 0.73 | 25/30 = 0.83 |

Edge case floor: both pass (2/5 and 3/5).

## Combined Scoring
- V1: 0.5 x 0.81 + 0.5 x 0.73 = **0.77**
- V2: 0.5 x 0.85 + 0.5 x 0.83 = **0.84**
- Margin: 0.07 (about 8%), above the 5% tiebreaker band, so no tiebreaker.

## Selected Base: V2 (one watcher instance per project), as the mechanism
V2 wins the score on evidence and risk coverage. The debate result then merges in the one thing V1 won: the loop lives in the watcher entry point (one verb, one scheduled entry), plus one loop-level account rate wait. V2's advocate accepted both ("effectively V2 with the loop owned by the watcher entry point").

- Strengths to preserve from V2: per-repo config, state_dir, lock, kill switch and day cap; one child process per repo with a kill timer; per-repo `status`.
- Strengths to incorporate from V1: the loop in the `issue-watch` entry point (no outer wrapper); R8 sweep as the same loop; one loop-level account rate wait; global one-launch-per-sweep brake.
