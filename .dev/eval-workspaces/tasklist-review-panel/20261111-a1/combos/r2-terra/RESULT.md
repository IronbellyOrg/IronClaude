# r2-terra RESULT (Batch 3, re-run after cooldown 2026-11-11/12)

Row: t4-1=claude-haiku-5-5, t3-1=claude-haiku-5-5, t4-2=grok-4.7, t2b-1=gpt-6.1-terra. All 12 reviewer runs fresh, one at a time. No scoring. Earlier stopped-attempt outputs were moved to reviews/combos/r2-terra/_prior-stopped-attempt/ (not reused).
Flag: thin = under 1000 output tokens. 'category normalised' was not needed (no unpassable-ac in any report). Observed model grok-4.7-build is the script's accepted alias.

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 213 | 48497 | valid | 8 | 1 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 169 | 38013 | valid | 5 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 801 | 53764 | valid | 3 | 1 |
| t2b-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 19 | 407 | THIN (valid block, reported incomplete: candidate's source.md missing) | 0 | 0 |

Total wall (sum of runs, sequential): 1202s. Total output tokens: 140681.
Merged (superclaude review merge, round 1): 6 ledger rows, 2 blocking. File: combos/r2-terra/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 271 | 63535 | valid | 9 | 2 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 200 | 45157 | valid | 9 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 2 | 1460 | 98059 | valid | 5 | 2 |
| t2b-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 20 | 598 | THIN (valid block, reported incomplete: candidate's source.md missing) | 0 | 0 |

Total wall (sum of runs, sequential): 1951s. Total output tokens: 207349.
Merged (superclaude review merge, round 1): 9 ledger rows, 3 blocking. File: combos/r2-terra/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 268 | 57723 | valid | 11 | 2 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 213 | 43939 | valid | 7 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 561 | 37211 | valid | 3 | 1 |
| t2b-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 24 | 539 | THIN (valid block, reported incomplete: candidate's source.md missing) | 0 | 0 |

Total wall (sum of runs, sequential): 1066s. Total output tokens: 139412.
Merged (superclaude review merge, round 1): 3 ledger rows, 2 blocking. File: combos/r2-terra/TASK-WF-design-20261108-041415/merged-1.md

Per-reviewer finding counts are lines in each report's findings-v1 block (before merge); merged rows are after deduplication.
