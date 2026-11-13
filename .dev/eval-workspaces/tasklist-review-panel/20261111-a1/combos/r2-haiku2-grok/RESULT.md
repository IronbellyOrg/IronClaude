# r2-haiku2-grok result (no scoring)

Row: t4-1=claude-haiku-5-5, t3-1=claude-haiku-5-5, t4-2=grok-4.7. Two independent haiku runs (separate files). All 9 runs valid on attempt 1; no reruns; no category normalisation needed (no `unpassable-ac` in any report). Output tokens = all-model output tokens from <id>.cost.json. Thin = under 1000 output tokens (none). "Findings" = own findings-v1 lines in the reviewer's report; "blocking" = lines with blocking true in that report. "Observed model" `grok-4.7-build` is the accepted form of grok-4.7.

Merged reports: combos/r2-haiku2-grok/<package>/merged-1.md (ledger.json and resolution.json beside it). Raw reports: <package>/reviews/combos/r2-haiku2-grok/.

## TASK-WF-designSpec-20261107-075614
| Reviewer | Model | Observed | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 247 | 51914 | no | 5 | 0 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 202 | 44207 | no | 7 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 957 | 63204 | no | 4 | 0 |

Totals: wall 1406 s (sum of runs; about 957 s elapsed minimum), output tokens 159325. Merge: verdict PASS, 8 merged findings (L1-L8), 0 blocking. merged-1.md written.

## TASK-WF-makeTheAliasOnly-20261105-051649
| Reviewer | Model | Observed | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 213 | 48157 | not thin; merge flagged its findings block invalid (a claim over 300 characters), so some or all of its findings were not counted by the merge | 7 | 2 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 232 | 55036 | no | 8 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 1209 | 87746 | no | 5 | 3 |

Totals: wall 1654 s (sum of runs; about 1209 s elapsed minimum), output tokens 190939. Merge: verdict FAIL, decision REVISE, 5 merged findings (L1-L5), 3 blocking (L1, L2, L4). The round was accepted (not refused), so t4-1 was not rerun; the warning was "t4-1: findings block problem (1 error(s)), first: claim must have at most 300 characters". t4-1 still appears as a reviewer on L1, L2, L3 in the merged table.

## TASK-WF-design-20261108-041415
| Reviewer | Model | Observed | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 240 | 49656 (main 48846) | no | 8 | 3 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 219 | 42880 (main 41988) | no | 7 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 662 | 45257 | no | 2 | 0 |

Totals: wall 1121 s (sum of runs; about 662 s elapsed minimum), output tokens 137793. Merge: verdict FAIL, decision REVISE, 4 merged findings (L1-L4), 1 blocking (L1).

## Notes
- Runs were executed 2 at a time via xargs -P2 over run-reviewer.sh; wall seconds are per run as measured by the script.
- Nothing scored; ground truth and other combos were not opened.
