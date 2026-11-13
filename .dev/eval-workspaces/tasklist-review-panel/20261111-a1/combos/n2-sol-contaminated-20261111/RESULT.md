# n2-sol RESULT (muse-wonder-1.0, claude-haiku-5-5, grok-4.7, gpt-6.1-sol); no scoring

Notes: muse-wonder-1.0 (t2b-1) is INVALID on all 3 packages: the gateway answered as gpt-6.1-terra (attempt 1 reported 'gpt-6.1-terra,muse-wonder-1.0'), both attempts failed the observed-model check. It is excluded from the resolution and the merge. No category normalisation was needed. grok observed as 'grok-4.7-build' (accepted by the script). Findings/blocking counted from each reviewer's findings-v1 block (merged report counts: see merged-1.md).

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | gpt-6.1-terra | 2 | 47 | 1236 | INVALID (wrong observed model) | n/a (excluded) | n/a |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 2 | 202 | 44213 |  | 5 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 879 | 54648 |  | 3 | 0 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 29 | 590 | thin | 0 | 0 |

Total (all four incl. invalid muse): wall 1157 s (sum), output tokens 100687. Merged: combos/n2-sol/TASK-WF-designSpec-20261107-075614/merged-1.md (verdict FAIL per merge output; reviewers merged: t4-1, t4-2, t2-1).

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | gpt-6.1-terra | 2 | 115 | 4237 | INVALID (wrong observed model) | n/a (excluded) | n/a |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 191 | 44177 |  | 6 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 748 | 48890 |  | 4 | 2 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 128 | 4241 |  | 3 | 2 |

Total (all four incl. invalid muse): wall 1182 s (sum), output tokens 101545. Merged: combos/n2-sol/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md (verdict FAIL per merge output; reviewers merged: t4-1, t4-2, t2-1).

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | gpt-6.1-terra | 2 | 38 | 1000 | INVALID (wrong observed model) | n/a (excluded) | n/a |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 204 | 44490 |  | 6 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 1225 | 57332 |  | 4 | 0 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 22 | 602 | thin | 0 | 0 |

Total (all four incl. invalid muse): wall 1489 s (sum), output tokens 103424. Merged: combos/n2-sol/TASK-WF-design-20261108-041415/merged-1.md (verdict FAIL per merge output; reviewers merged: t4-1, t4-2, t2-1).
