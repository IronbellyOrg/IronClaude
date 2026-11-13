# n4-terra (Batch 3) RESULT

Row: t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=claude-haiku-5-5, t2-1=gpt-6.1-terra. Reviewer jobs were run by the driver (not re-run here); model_ok, attempts, wall and tokens are read from each reviewer's meta.json and cost.json. Findings counts are the ledger members per reviewer in the merged report (round 1). Thin = under 1000 output tokens. No scoring. No category normalisation was needed (all merges passed on the original reports).

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | model_ok | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | true | 1 | 163 | 19297 | ok (block=true) | 4 | 0 |
| t3-1 | glm-5.3 | glm-5.3 | true | 1 | 1533 | 67780 | ok (block=true) | 3 | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | true | 1 | 212 | 47859 | ok (block=true) | 7 | 1 |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | true | 1 | 18 | 412 | THIN (block=true) | 0 | 0 |

Merge: ledger rows=7, blocking rows=1; merged report: combos/n4-terra/TASK-WF-designSpec-20261107-075614/merged-1.md. Totals (sum of reviewer wall, sequential): 1926 s, 135348 output tokens.

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | model_ok | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | true | 1 | 128 | 16613 | ok (block=true) | 5 | 1 |
| t3-1 | glm-5.3 | glm-5.3 | true | 1 | 2122 | 100275 | ok (block=true) | 4 | 1 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | true | 1 | 197 | 43578 | ok (block=true) | 8 | 2 |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | true | 1 | 23 | 586 | THIN (block=true) | 0 | 0 |

Merge: ledger rows=6, blocking rows=1; merged report: combos/n4-terra/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md. Totals (sum of reviewer wall, sequential): 2470 s, 161052 output tokens.

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | model_ok | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | true | 1 | 111 | 14935 | ok (block=true) | 7 | 1 |
| t3-1 | glm-5.3 | glm-5.3 | true | 1 | 1338 | 58131 | ok (block=true) | 3 | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | true | 1 | 120 | 26332 | ok (block=true) | 6 | 2 |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | true | 1 | 20 | 527 | THIN (block=true) | 0 | 0 |

Merge: ledger rows=3, blocking rows=2; merged report: combos/n4-terra/TASK-WF-design-20261108-041415/merged-1.md. Totals (sum of reviewer wall, sequential): 1589 s, 99925 output tokens.
