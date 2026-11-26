# r3-luna2-grok: result (no scoring)

Row: t4-1=gpt-6-luna, t3-1=gpt-6-luna, t4-2=grok-4.7. Run via tools/run-reviewer.sh, 2 at a time. All attempts first-try; no reviewer rerun; no category normalisation needed (all merges accepted the reports as written).
Thin = under 1000 output tokens. Findings/blocking counted from each reviewer's findings-v1 block (the same ones the merge consumed).

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 26 | 899 | thin | 0 | 0 |
| t3-1 | gpt-6-luna | gpt-6-luna | 1 | 28 | 950 | thin | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 906 | 56648 | ok | 4 | 1 |

Total (sum of runs; ran 2 at a time): wall 960 s, output tokens 58497. Merge: verdict: FAIL
Merged report: combos/r3-luna2-grok/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 77 | 3260 | ok | 1 | 1 |
| t3-1 | gpt-6-luna | gpt-6-luna | 1 | 124 | 6131 | ok | 2 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 1130 | 67470 | ok | 3 | 1 |

Total (sum of runs; ran 2 at a time): wall 1331 s, output tokens 76861. Merge: verdict: FAIL
Merged report: combos/r3-luna2-grok/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 41 | 1713 | ok | 0 | 0 |
| t3-1 | gpt-6-luna | gpt-6-luna | 1 | 33 | 1107 | ok | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 825 | 55484 | ok | 4 | 0 |

Total (sum of runs; ran 2 at a time): wall 899 s, output tokens 58304. Merge: verdict: PASS
Merged report: combos/r3-luna2-grok/TASK-WF-design-20261108-041415/merged-1.md
