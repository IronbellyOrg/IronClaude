# n3-muse-luna-grok: RESULT (no scoring)

Row: t2b-1=muse-wonder-1.0, t4-1=gpt-6-luna, t4-2=grok-4.7. All 9 runs valid on attempt 1 (model matched, findings-v1 block present). No retries, no overload errors. No "category normalised" case: no report used `unpassable-ac`.
Thin = under 1000 output tokens: none. "Findings" and "blocking" columns count the reviewer's own findings-v1 block; the merged-report totals are listed under each table.

## TASK-WF-designSpec-20261107-075614
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 256 | 22160 | no | 5 | 0 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 51 | 2076 | no | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 1245 | 70166 | no | 4 | 1 |

Total wall 1552 s (sequential sum; runs overlapped 2 at a time), total output tokens 94402. Merged: 5 ledger rows, 1 blocking, verdict FAIL. File: combos/n3-muse-luna-grok/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 147 | 15862 | no | 5 | 1 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 180 | 8615 | no | 2 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 651 | 44775 | no | 5 | 2 |

Total wall 978 s, total output tokens 69252. Merged: 5 ledger rows, 3 blocking, verdict FAIL. File: combos/n3-muse-luna-grok/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

## TASK-WF-design-20261108-041415
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 96 | 11248 | no | 6 | 3 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 31 | 1154 | no | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 848 | 57837 | no | 5 | 1 |

Total wall 975 s, total output tokens 70239. Merged: 1 ledger row, 1 blocking, verdict FAIL. File: combos/n3-muse-luna-grok/TASK-WF-design-20261108-041415/merged-1.md

## Notes
- luna returned an empty findings block on two packages (valid per the script, 0 findings).
- "grok-4.7-build" is the observed id; the script accepts the "-build" suffix.
- Resolution files: combos/n3-muse-luna-grok/<package>/resolution.json (3 reviewers each).
