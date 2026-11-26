# r1-haiku-luna2 RESULT (no scoring)

Row: t4-1=claude-haiku-5-5, t4-2=gpt-6-luna, t3-1=gpt-6-luna. All 9 runs valid on attempt 1 (model matched, findings block present). No category normalising was needed (no `unpassable-ac` in any report). Wall seconds are per run (the 2-at-once overlap makes real elapsed time shorter than the sum). Findings = lines in the reviewer's own findings block / of which blocking. Thin = under 1000 output tokens.

## TASK-WF-designSpec-20261107-075614
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 228 | 52368 | no | 8 | 2 |
| t4-2 | gpt-6-luna | gpt-6-luna | 1 | 30 | 881 | THIN | 0 | 0 |
| t3-1 | gpt-6-luna | gpt-6-luna | 1 | 23 | 768 | THIN | 0 | 0 |

Total: 281 s, 54017 output tokens. Merged (merged-1.md): 7 ledger rows, 2 blocking, verdict FAIL.

## TASK-WF-makeTheAliasOnly-20261105-051649
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 339 | 78838 | no | 12 | 3 |
| t4-2 | gpt-6-luna | gpt-6-luna | 1 | 91 | 4417 | no | 2 | 1 |
| t3-1 | gpt-6-luna | gpt-6-luna | 1 | 155 | 7383 | no (see note) | 6 | 4 |

Total: 585 s, 90638 output tokens. Merged: 6 ledger rows, 3 blocking, verdict FAIL.
Note: the merge reported "t3-1: findings block problem (1 error), anchor must have at most 200 characters" and marked t3-1 "block ok false". The merge still accepted the round, so per SPEC no rerun was done. t3-1's own findings count (6/4) is from its raw block; the merge may not have used all of them.

## TASK-WF-design-20261108-041415
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 195 | 40678 | no | 7 | 2 |
| t4-2 | gpt-6-luna | gpt-6-luna | 1 | 42 | 1692 | no | 0 | 0 |
| t3-1 | gpt-6-luna | gpt-6-luna | 1 | 43 | 1927 | no | 0 | 0 |

Total: 280 s, 44297 output tokens. Merged: 5 ledger rows, 2 blocking, verdict FAIL.

## Files
Per package: combos/r1-haiku-luna2/<package>/{resolution.json,ledger.json,merged-1.md}; raw reviews in <package>/reviews/combos/r1-haiku-luna2/.
