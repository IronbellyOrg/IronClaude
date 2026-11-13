# Result: n1-muse-haiku-luna (t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=gpt-6-luna)

All 9 runs: observed model matched, findings block present, 1 attempt each, no category normalisation needed. All 3 merges ran (round 1). No scoring.
Findings = entries in the reviewer's own findings block as submitted; "accepted in merge" = entries the merge ledger took from that reviewer. Blocking = marked blocking in the reviewer's block (ledger blocking count in brackets where it matters). Thin = under 1000 output tokens.

## TASK-WF-designSpec-20261107-075614 (merged: combos/n1-muse-haiku-luna/TASK-WF-designSpec-20261107-075614/merged-1.md; verdict PASS, 0 blocking)
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings (accepted) | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 145 | 16244 | no | 5 (5) | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 169 | 36641 | no | 8 (8) | 0 |
| t4-2 | gpt-6-luna | gpt-6-luna | 1 | 40 | 1505 | not thin by token count, but empty findings block (verdict FAIL, 0 findings) | 0 (0) | 0 |
Total wall (sum of runs): 354 s. Total output tokens: 54390.

## TASK-WF-makeTheAliasOnly-20261105-051649 (merged-1.md; verdict FAIL, 3 blocking ledger items L1-L3)
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings (accepted) | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 155 | 18355 | no | 6 (6) | 2 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 271 | 62741 | no | 10 (10) | 3 |
| t4-2 | gpt-6-luna | gpt-6-luna | 1 | 115 | 5536 | no | 3 (2) | 1 |
Merge warning: t4-2 findings block had 1 entry rejected (anchor over 200 characters); the other 2 were accepted. Report left unedited.
Total wall (sum of runs): 541 s. Total output tokens: 86632.

## TASK-WF-design-20261108-041415 (merged-1.md; verdict FAIL, 1 blocking ledger item L1)
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings (accepted) | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 86 | 11635 | no | 6 (6) | 1 (merged report lists F1, F3, F4 under L1) |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 230 | 42123 | no | 6 (6) | 1 |
| t4-2 | gpt-6-luna | gpt-6-luna | 1 | 44 | 1727 | not thin by token count, but empty findings block (verdict FAIL, 0 findings) | 0 (0) | 0 |
Total wall (sum of runs): 360 s. Total output tokens: 55485.

Files: reviews in <package>/reviews/combos/n1-muse-haiku-luna/, resolution.json, ledger.json, merged-1.md in combos/n1-muse-haiku-luna/<package>/.
