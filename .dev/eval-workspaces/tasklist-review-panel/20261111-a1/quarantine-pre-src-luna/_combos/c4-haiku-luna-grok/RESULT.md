# Result: c4-haiku-luna-grok (t3-1=claude-haiku-5-5, t4-1=gpt-6-luna, t4-2=grok-4.7)

No scoring. Findings = ledger rows in merged-1.md that the reviewer contributed to; blocking = those rows marked blocking=yes. Thin = under 1000 output tokens (all-model output tokens).

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 (category normalised) | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 222 | 51835 | ok | 5 | 1 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 28 | 1000 | ok | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 932 | 60489 | ok | 3 | 0 |

Total: wall (sum of reviewers, run 2 at once) 1182s, output tokens 113324. Merge: verdict FAIL, merged-1.md written.

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 (category normalised) | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 268 | 63413 | ok | 5 | 1 |
| t4-1 (category normalised) | gpt-6-luna | gpt-6-luna | 1 | 177 | 8431 | ok | 1 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 709 | 46995 | ok | 2 | 1 |

Total: wall (sum of reviewers, run 2 at once) 1154s, output tokens 118839. Merge: verdict FAIL, merged-1.md written.

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 311 | 63525 | ok | 6 | 1 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 38 | 1531 | ok | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 945 | 59497 | ok | 4 | 1 |

Total: wall (sum of reviewers, run 2 at once) 1294s, output tokens 124553. Merge: verdict FAIL, merged-1.md written.

## Notes
- Merge did not refuse any round; with the original reports it silently dropped findings whose category was unpassable-ac. Per the SPEC correction I re-merged with <report>.catfix.md copies (sed unpassable-ac to unpassable-check) for t3-1 (designSpec, makeTheAliasOnly) and t4-1 (makeTheAliasOnly); the originals are untouched.
- designSpec t4-1 (luna): 1000 output tokens, 28 s, contributed 0 ledger rows.
- grok observed model id is grok-4.7-build (accepted by the script as the expected model).
