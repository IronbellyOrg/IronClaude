# c5-glm-haiku result (t3-1 = glm-5.3, t4-1 = claude-haiku-5-5). No scoring.

Source: tools/run-reviewer.sh cost/meta files; merged reports in combos/c5-glm-haiku/<package>/merged-1.md.
Thin = under 1000 output tokens (none were). Wall seconds and tokens are totals over all attempts (from <id>.cost.json). Two reviewers ran at once (one chain per reviewer).

Category normalisation (SPEC Correction): haiku (t4-1) used the category `unpassable-ac` in TASK-WF-designSpec-20261107-075614 (3 findings) and TASK-WF-makeTheAliasOnly-20261105-051649 (2 findings). The first merge accepted the round but warned and dropped those findings. I re-merged those two packages with a `sed` copy (`t4-1.md.catfix.md`, original left unedited) after deleting my own ledger. Both t4-1 rows are marked "category normalised". TASK-WF-design-20261108-041415 needed no fix.

## TASK-WF-designSpec-20261107-075614
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings in merged | Blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 | glm-5.3 | glm-5.3 | 2 | 3437 | 30450 | valid, not thin | 3 (L1,L2,L3) | see package line |
| t4-1 (category normalised) | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 294 | 67734 | valid, not thin | 4 (L1,L4,L5,L6) | see package line |

Merged: 6 findings, 1 blocking (L4, from t4-1). Verdict FAIL / REVISE. Remaining merge warning: one t4-1 finding has a claim over 300 characters ("claim must have at most 300 characters"), so that finding was not counted. Reviewer table counts are per-reviewer contributions to the 6 merged ledger rows (L1 shared).
Total wall 3731 s (sum; ran in parallel with the other reviewer), total output tokens 98184.

## TASK-WF-makeTheAliasOnly-20261105-051649
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings in merged |
|---|---|---|---|---|---|---|---|
| t3-1 | glm-5.3 | glm-5.3 | 1 | 1190 | 87199 | valid, not thin | 3 (L1,L2,L3) |
| t4-1 (category normalised) | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 370 | 88993 | valid, not thin | 6 (L1-L6) |

Merged: 6 findings, 2 blocking (L1, L4). Verdict FAIL / REVISE. No warnings after normalisation.
Total wall 1560 s, total output tokens 176192.

## TASK-WF-design-20261108-041415
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings in merged |
|---|---|---|---|---|---|---|---|
| t3-1 | glm-5.3 | glm-5.3 | 1 | 845 | 65640 | valid, not thin | 2 (L1,L2) |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 324 | 68081 | valid, not thin | 3 (L1,L3,L4) |

Merged: 4 findings, 1 blocking (L1). Verdict FAIL / REVISE. No warnings.
Total wall 1169 s, total output tokens 133721.

## Notes
- glm-5.3 on designSpec needed 2 attempts (3437 s total for both); the cost file reports 30450 output tokens for that package.
- Per-reviewer finding counts count ledger rows the reviewer appears in; the "Blocking" column per reviewer was not split, only per merged package.
