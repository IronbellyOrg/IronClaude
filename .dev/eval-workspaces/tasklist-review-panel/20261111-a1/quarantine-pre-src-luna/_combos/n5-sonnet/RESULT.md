# n5-sonnet result (Batch 3 row)

Row: t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=gpt-6-luna, t1b-1=claude-sonnet-5-5.
Run 2026-11-12, every reviewer fresh via tools/run-reviewer.sh (2 at once), 1 attempt each, all observed models matched, all findings-v1 blocks present. No reviewer INVALID. No category normalisation needed (merge never refused a round). No scoring.
Earlier outputs moved (not deleted) to `<package>/reviews/combos/n5-sonnet-superseded-20261112`.

Column notes: "Findings" = ledger rows in merged-1.md that include this reviewer (merged rows are clustered, so one row can list several reviewers; "raw" = lines in the reviewer's own findings-v1 block). "Blocking" = those ledger rows marked blocking = yes. Thin = under 1000 output tokens (none).

## TASK-WF-designSpec-20261107-075614
Merged: 11 ledger rows, 0 blocking, merge verdict PASS (decision per merge output). Files: combos/n5-sonnet/TASK-WF-designSpec-20261107-075614/{resolution.json,ledger.json,merged-1.md}

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (raw) | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 113 | 12817 | no | 4 (4) | 0 |
| t3-1 | glm-5.3 | glm-5.3 | 1 | 872 | 39654 | no | 4 (4) | 0 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 34 | 1348 | no | 0 (0) | 0 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 219 | 30281 | no | 5 (6) | 0 |

Total: wall 1238 s (sum of runs), output tokens 84100.

## TASK-WF-makeTheAliasOnly-20261105-051649
Merged: 6 ledger rows, 2 blocking (L2, L5), merge verdict FAIL.
Merge warnings: t2b-1 (1 error) and t3-1 (3 errors): "anchor2 must have at most 200 characters" in their findings blocks, so those entries were not all accepted; their merged counts are below their raw counts. Reports left unedited.
Files: combos/n5-sonnet/TASK-WF-makeTheAliasOnly-20261105-051649/{resolution.json,ledger.json,merged-1.md}

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (raw) | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 111 | 14760 | no (block warning) | 3 (5) | 1 |
| t3-1 | glm-5.3 | glm-5.3 | 1 | 2820 | 133093 | no (block warning) | 1 (5) | 0 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 64 | 2950 | no | 2 (2) | 2 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 185 | 26685 | no | 4 (7) | 1 |

Total: wall 3180 s (sum of runs), output tokens 177488.

## TASK-WF-design-20261108-041415
Merged: 2 ledger rows, 1 blocking (L1), merge verdict FAIL. Files: combos/n5-sonnet/TASK-WF-design-20261108-041415/{resolution.json,ledger.json,merged-1.md}

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (raw) | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 85 | 11013 | no | 1 (6) | 1 |
| t3-1 | glm-5.3 | glm-5.3 | 1 | 1168 | 54667 | no | 2 (4) | 1 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 47 | 2080 | no | 1 (1) | 1 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 223 | 29378 | no | 1 (4) | 1 |

Total: wall 1523 s (sum of runs), output tokens 97138.
