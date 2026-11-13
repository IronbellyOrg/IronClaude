# n5-terra RESULT (Batch 3 row, run 2026-11-12 04:34-07:15 UTC, one reviewer at a time)

Row: t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=gpt-6-luna, t2-1=gpt-6.1-terra. All reviewers ran fresh. Old output folders were moved to `n5-terra-superseded-20261112` (per package under reviews/combos/). No scoring.

Columns "findings / blocking" are rows in the merged ledger that the reviewer appears in (overlapping findings count for each reviewer who raised them). "Own block" is the count in the reviewer's own findings-v1 block, shown where it differs from the merged count. Thin = under 1000 output tokens.

## TASK-WF-designSpec-20261107-075614 (merge: verdict PASS, 6 ledger rows, 0 blocking)
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 176 | 22510 | ok | 5 | 0 |
| t3-1 | glm-5.3 | glm-5.3 | 1 | 2150 | 118121 | ok | 3 | 0 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 47 | 1483 | ok (low, empty findings block) | 0 | 0 |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 17 | 418 | THIN (empty findings block) | 0 | 0 |

Total: wall 2390 s, output tokens 142532.

## TASK-WF-makeTheAliasOnly-20261105-051649 (merge: verdict FAIL, 7 ledger rows, 2 blocking)
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 169 | 17731 | block problem (an anchor2 over 200 chars; own block 8 findings, 2 blocking) | 4 | 2 |
| t3-1 | glm-5.3 | glm-5.3 | 1 | 2347 | 120290 | ok | 5 | 1 |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 113 | 5478 | block problem (an anchor over 200 chars; own block 4 findings, 3 blocking) | 2 | 2 |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 16 | 492 | THIN (empty findings block) | 0 | 0 |

Total: wall 2645 s, output tokens 143991. The merge printed warnings for t2b-1 and t4-1 (anchor too long); it still merged the rest of their findings, so it did not refuse the round and no rerun or catfix copy was needed.

## TASK-WF-design-20261108-041415 (merge: verdict FAIL, decision REVISE, 2 ledger rows, 1 blocking; merged WITHOUT t3-1)
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 94 | 14080 | ok (own block 4, merged 2) | 2 | 1 |
| t3-1 | glm-5.3 | none (no output) | 2 | 3000+ (attempt 1; attempt 2 killed) | 0 | INVALID | - | - |
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 40 | 1342 | ok (low, empty findings block) | 0 | 0 |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 18 | 374 | THIN (empty findings block) | 0 | 0 |

t3-1 INVALID, reason: attempt 1 timed out at the 3000 s limit (exit 124, empty output). Attempt 2 started 06:50 and the runner process was killed (message "Killed") around 07:14 after about 24 min, with an empty output file; the cause of the kill is unknown (not a model failure message). I did not rerun it, as the task says to record INVALID and merge without it. The wall time for this reviewer is therefore a lower bound (over 3000 s plus about 1440 s).

Total (valid reviewers only): wall 152 s, output tokens 15796.

## Notes
- No reviewer failed the observed-model check; muse-wonder-1.0 was observed as muse-wonder-1.0 on all 3 packages.
- No reviewer was "category normalised"; no catfix copies were made.
- Files: per-package resolution, ledger and merged report are under `combos/n5-terra/<package>/` (resolution.json, ledger.json, merged-1.md). For the third package the resolution lists only t2b-1, t4-1 and t2-1.
