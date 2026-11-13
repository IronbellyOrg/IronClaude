# RESULT: n2-muse-haiku-grok (t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7)

No scoring. Every reviewer passed on attempt 1 (observed model matched, findings-v1 block present). No thin or invalid runs. No `unpassable-ac` appeared in any report, so no catfix copies were needed (no category normalised).
Observed model for grok-4.7 shows as `grok-4.7-build` (the script accepts that suffix).
Runs went 2 at a time via `tools/run-reviewer.sh`. Findings counts come from each report's findings-v1 block; "blocking (reported)" is the reviewer's own flag. Merged ledger rows are the clusters in merged-1.md.

## TASK-WF-designSpec-20261107-075614
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking (reported) |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 149 | 16343 | no | 4 | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 217 | 49892 | no | 9 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 976 | 59565 | no | 4 | 0 |

Total wall (sum of reviewer runs): 1342 s. Total output tokens: 125800.
Merged: merged-1.md written; 7 ledger rows, 0 blocking.

## TASK-WF-makeTheAliasOnly-20261105-051649
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking (reported) |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 179 | 20793 | no | 8 | 3 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 184 | 43904 | no | 8 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 720 | 51347 | no | 6 | 2 |

Total wall (sum of reviewer runs): 1083 s. Total output tokens: 116044.
Merged: merged-1.md written; 7 ledger rows, 3 blocking.
Note: the merge printed `block_ok: false` for t2b-1 on this package, yet it did not refuse the round and t2b-1's findings F1 to F7 appear in the ledger. I parsed t2b-1's findings-v1 block myself: all 8 lines are valid JSON and all anchors are found in the candidate. Cause not investigated (the merge's own source was not read).

## TASK-WF-design-20261108-041415
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking (reported) |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 134 | 12949 | no | 6 | 1 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 242 | 48495 (main 47586) | no | 9 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 622 | 42099 | no | 2 | 0 |

Total wall (sum of reviewer runs): 998 s. Total output tokens: 103543.
Merged: merged-1.md written; 5 ledger rows, 2 blocking.

## Files
- Merged reports: `combos/n2-muse-haiku-grok/<package>/merged-1.md` (with ledger.json and resolution.json beside it).
- Reviewer outputs and cost files: `<package>/reviews/combos/n2-muse-haiku-grok/`.
