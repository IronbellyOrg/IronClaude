# r2-sol result (Batch 3): t4-1=claude-haiku-5-5, t3-1=claude-haiku-5-5, t4-2=grok-4.7, t2-1=gpt-6.1-sol

No scoring. All 12 reviewer runs are fresh, passed the observed-model check on attempt 1 (grok reports `grok-4.7-build`, which the script accepts), and are valid findings-v1 blocks per the script. Merges: `combos/r2-sol/<package>/merged-1.md` exist for all 3 packages (resolution.json: model per id from the row, tier fields kept from resolution-live7.json; so t3-1 stays tier3 and t2-1 tier2 even though the models differ from the live7 entry).
Runs were done in two sessions (resume): 8 runs for designSpec and alias were already on disk; design t4-1 was started just before resume and completed; the rest of design ran one at a time here. Per-run files: `<package>/reviews/combos/r2-sol/`.

Findings columns: "findings" = rows in the reviewer's own findings-v1 block; "blocking" = rows with blocking true in that block. Merged line = clusters in the merged ledger table, and how many are marked blocking.

## TASK-WF-designSpec-20261107-075614
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 214 | 49204 | ok | 6 | 0 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 252 | 58590 | ok | 12 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 878 | 58558 | ok | 3 | 0 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 32 | 568 | THIN (<1000), review-incomplete report, 0 findings | 0 | 0 |

Total wall (sum of runs) 1376 s; total output tokens 166920. Merged report: 11 clusters, 1 blocking; verdict FAIL / REVISE; merge brief ids L3. Merge: all 4 blocks accepted.

## TASK-WF-makeTheAliasOnly-20261105-051649
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 224 | 49361 | ok | 8 | 1 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 287 | 68456 | block partly invalid (see note) | 10 | 3 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 1273 | 63575 | ok | 7 | 2 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 78 | 1610 | review-incomplete report (says the candidate's `./source.md` was missing), 0 findings; not under 1000 tokens | 0 | 0 |

Total wall 1862 s; total output tokens 183002. Merged report: 7 clusters, 1 blocking; verdict FAIL / REVISE; brief ids L1.
Note (t3-1): the merge reported "block ok false" for t3-1 because finding F1 lists 9 refs (limit 8, "refs must be a list of at most 8 strings"). The round was not refused (3 other blocks were valid) and the merged report still contains t3-1 rows F2, F3, F8 (and others); F1 is the row that did not validate. I did not rerun it: the spec only reruns when the round is refused. Coordinator may decide to rerun t3-1 for this package.

## TASK-WF-design-20261108-041415
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 294 | 63848 | ok | 8 | 1 |
| t3-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 279 | 57681 | ok | 12 | 3 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 720 | 48061 | ok | 2 | 1 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 31 | 740 | THIN (<1000), 0 findings | 0 | 0 |

Total wall 1324 s; total output tokens 170330. Merged report: 5 clusters, 2 blocking; verdict FAIL / REVISE; brief ids L1, L4. Merge: all 4 blocks accepted.

## Notes
- No `unpassable-ac` appeared in any report, so no category normalisation (.catfix.md) was needed.
- gpt-6.1-sol returned a short "review incomplete" report on all 3 packages (0 findings), so the added reviewer contributed no findings to the merges.
- The design t4-1 run was started by the earlier session of this worker; its files are complete and valid (cost.json attempts 1).
