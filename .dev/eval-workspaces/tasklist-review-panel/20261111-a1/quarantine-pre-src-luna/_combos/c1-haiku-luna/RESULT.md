# RESULT: c1-haiku-luna (t4-1 = claude-haiku-5-5, t4-2 = gpt-6-luna)

No scoring. Wall seconds are the sum of attempts (reviewers ran two at a time, so elapsed time is lower). "Findings" = entries in the reviewer's own findings block (raw), then the merged report's ledger rows (clusters) and how many of those are blocking. Thin = under 1000 output tokens.

## TASK-WF-designSpec-20261107-075614
Merged report: combos/c1-haiku-luna/TASK-WF-designSpec-20261107-075614/merged-1.md (verdict PASS, 0 ledger rows).

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid / thin | Raw findings (blocking) | Merged rows (blocking) |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 303 | 69525 | INVALID block: heading "## Findings block" missing, merge ignored its 15 findings | 15 (0) | 0 (0) |
| t4-2 | gpt-6-luna | gpt-6-luna | 1 | 30 | 991 | THIN (991 < 1000) | 0 (0) | 0 (0) |

Total: 333 s, 70516 output tokens. The merge accepted the round on t4-2 alone (warning for t4-1), so no rerun was triggered.

## TASK-WF-makeTheAliasOnly-20261105-051649
Merged report: INVALID (no merged-1.md). Reason: `superclaude review merge` refused round 1 on both the first run and after the one allowed rerun of both reviewers: "no reviewer produced a valid findings block ... category is not one of the allowed values". Both reviewers used category `unpassable-ac` (the value the run script's brief asks for), but the merge validator (src/superclaude/cli/review/findings.py, CATEGORIES) lists `unpassable-check`. Reviewer output was otherwise well formed; reports are kept unedited.

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid / thin | Raw findings (blocking) | Merged rows (blocking) |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 2 (initial + 1 rerun) | 449 (238 + 211) | 104162 (55386 + 48776) | block rejected by merge (category) | 7 (1) in final run | n/a |
| t4-2 | gpt-6-luna | gpt-6-luna | 2 (initial + 1 rerun) | 295 (156 + 139) | 14093 (7396 + 6697) | block rejected by merge (category) | 3 (3) in final run | n/a |

Total: 744 s, 118255 output tokens. First-run cost files are in combos/c1-haiku-luna/TASK-WF-makeTheAliasOnly-20261105-051649/rerun-backup/ (the script overwrote the per-reviewer cost files on the rerun).

## TASK-WF-design-20261108-041415
Merged report: combos/c1-haiku-luna/TASK-WF-design-20261108-041415/merged-1.md (verdict FAIL, 7 ledger rows, 1 blocking).

| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid / thin | Raw findings (blocking) | Merged rows (blocking) |
|---|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 187 | 42018 | ok | 11 (2) | 7 (1), all from t4-1 |
| t4-2 | gpt-6-luna | gpt-6-luna | 1 | 57 | 2551 | ok (block empty) | 0 (0) | 0 (0) |

Total: 244 s, 44569 output tokens. The merged row counts are for the two reviewers together (the 11 haiku findings were clustered into 7 rows).

## Addendum by the coordinator worker (2026-11-11)
makeTheAliasOnly is no longer INVALID. The refusal was caused by our own brief (tools/run-reviewer.sh listed `unpassable-ac`; the validator wants `unpassable-check`). I merged copies of both reports with that one label changed (`t4-1.catfix.md`, `t4-2.catfix.md`, originals untouched) to combos/c1-haiku-luna/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md (verdict FAIL). The same label problem affects pilot reviews outside this combo; the script is fixed for later runs.
