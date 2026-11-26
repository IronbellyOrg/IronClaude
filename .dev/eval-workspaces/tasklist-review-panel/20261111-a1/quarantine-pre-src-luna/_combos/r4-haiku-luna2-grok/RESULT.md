# r4-haiku-luna2-grok result

Row: t3-1=claude-haiku-5-5, t4-1=gpt-6-luna, t3-2=gpt-6-luna, t4-2=grok-4.7. No scoring. No category normalisation was needed (all merges accepted the original reports). Findings/blocking = member findings from that reviewer in the merged ledger (members, not merged rows). Thin = under 1000 output tokens; none below it, but t4-1 and t3-2 on designSpec/design sit at 1036-1577 tokens (low).

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 211 | 47066 | valid | 10 | 0 |
| t3-2 | gpt-6-luna | gpt-6-luna | 1 | 37 | 1170 | valid | 0 | 0 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 30 | 1036 | valid | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 750 | 47304 | valid | 5 | 0 |

Total: summed wall 1028 s (runs were 2 at a time), output tokens 96576. Merged: 7 ledger rows, 0 blocking. Merged report: combos/r4-haiku-luna2-grok/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 185 | 42297 | valid | 5 | 1 |
| t3-2 | gpt-6-luna | gpt-6-luna | 1 | 121 | 5594 | valid | 2 | 1 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 118 | 5181 | valid | 2 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 725 | 45238 | valid | 6 | 2 |

Total: summed wall 1149 s (runs were 2 at a time), output tokens 98310. Merged: 5 ledger rows, 2 blocking. Merged report: combos/r4-haiku-luna2-grok/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 292 | 64447 | valid | 9 | 2 |
| t3-2 | gpt-6-luna | gpt-6-luna | 1 | 33 | 1246 | valid | 0 | 0 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 43 | 1577 | valid | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 591 | 40219 | valid | 1 | 0 |

Total: summed wall 959 s (runs were 2 at a time), output tokens 107489. Merged: 6 ledger rows, 2 blocking. Merged report: combos/r4-haiku-luna2-grok/TASK-WF-design-20261108-041415/merged-1.md
