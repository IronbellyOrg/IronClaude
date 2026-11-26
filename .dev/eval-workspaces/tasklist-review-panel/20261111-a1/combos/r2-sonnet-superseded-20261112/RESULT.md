# r2-sonnet RESULT (batch 3; no scoring)

Row: t4-1=claude-haiku-5-5, t3-1=claude-haiku-5-5, t4-2=grok-4.7, t1b-1=claude-sonnet-5-5. All 12 runs fresh, run strictly one at a time, first attempt valid every time (no retries, no category normalisation needed). grok-4.7 is observed as `grok-4.7-build`, which the script accepts as the same model. Findings and blocking counts are taken from each reviewer's findings-v1 block (the same findings the merge ingested); merge refused nothing.

## TASK-WF-designSpec-20261107-075614

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 266 | 60672 | valid | 8 | 0 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 229 | 53138 | valid | 13 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 842 | 53050 | valid | 3 | 1 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 200 | 26446 | valid | 5 | 0 |

Total wall 1537 s, total output tokens 193306. Merged report: combos/r2-sonnet/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 246 | 54638 | valid | 8 | 2 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 181 | 40101 | valid | 7 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 687 | 45595 | valid | 4 | 2 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 132 | 17706 | valid | 3 | 1 |

Total wall 1246 s, total output tokens 158040. Merged report: combos/r2-sonnet/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

## TASK-WF-design-20261108-041415

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 177 | 40701 | valid | 10 | 2 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 182 | 36095 | valid | 9 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 601 | 38601 | valid | 4 | 1 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 176 | 24144 | valid | 6 | 1 |

Total wall 1136 s, total output tokens 139541. Merged report: combos/r2-sonnet/TASK-WF-design-20261108-041415/merged-1.md
