# n4-sol: muse-wonder-1.0 (t2b-1), glm-5.3 (t3-1), claude-haiku-5-5 (t4-1), gpt-6.1-sol (t2-1)

Driver ran the reviewer jobs earlier; this worker verified model_ok/findings_block per reviewer from the *.meta.json files, built the custom resolution and merged round 1. No scoring.
Findings and blocking counts are parsed-finding counts per reviewer taken from the merge output's clusters (combos/n4-sol/<pkg>/merge.out); 'thin' = under 1000 output tokens.

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | model_ok | attempts | wall s | output tokens | invalid/thin | findings | blocking | block_ok (merge) |
|---|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | true | 1 | 152 | 15959 | ok | 4 | 0 | true |
| t3-1 | glm-5.3 | glm-5.3 | true | 1 | 2414 | 109274 | ok | 5 | 0 | true |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | true | 1 | 164 | 36159 | ok | 9 | 2 | true |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | true | 1 | 24 | 603 | THIN | 0 | 0 | true |

Total (sum over reviewers, final attempts): wall 2754 s, output tokens 161995. Merge: {"verdict":"FAIL","decision":"REVISE","new":["L1","L2","L3","L4","L5","L6","L7","L8","L9","L10"],"brief_ids":["L8","L9"],"warnings":[]}
Merged report: combos/n4-sol/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | model_ok | attempts | wall s | output tokens | invalid/thin | findings | blocking | block_ok (merge) |
|---|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | true | 1 | 88 | 12979 | ok | 2 | 0 | false |
| t3-1 | glm-5.3 | glm-5.3 | true | 1 | 1940 | 90130 | ok | 5 | 2 | true |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | true | 1 | 227 | 50127 | ok | 7 | 1 | true |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | true | 1 | 40 | 947 | THIN | 0 | 0 | true |

Total (sum over reviewers, final attempts): wall 2295 s, output tokens 154183. Merge: {"verdict":"FAIL","decision":"REVISE","new":["L1","L2","L3","L4","L5","L6"],"brief_ids":["L1","L3"],"warnings":["t2b-1: findings block problem (2 error(s)), first: anchor2 must have at most 200 characters"]}
Merged report: combos/n4-sol/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | model_ok | attempts | wall s | output tokens | invalid/thin | findings | blocking | block_ok (merge) |
|---|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | true | 1 | 102 | 13925 | ok | 7 | 2 | true |
| t3-1 | glm-5.3 | glm-5.3 | true | 1 | 2431 | 106952 | ok | 4 | 0 | false |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | true | 1 | 256 | 53471 | ok | 7 | 3 | true |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | true | 1 | 25 | 664 | THIN | 0 | 0 | true |

Total (sum over reviewers, final attempts): wall 2814 s, output tokens 175012. Merge: {"verdict":"FAIL","decision":"REVISE","new":["L1","L2","L3","L4"],"brief_ids":["L1"],"warnings":["t3-1: findings block problem (1 error(s)), first: claim must have at most 300 characters"]}
Merged report: combos/n4-sol/TASK-WF-design-20261108-041415/merged-1.md

## Notes
- All 12 reviewer runs: observed model equals expected model, findings-v1 block present, 1 attempt each (final meta). No reviewer INVALID; no category normalisation (catfix) was needed.
- Stale attempt2 files exist from the quarantined 12-worker run (makeTheAliasOnly t3-1.attempt2, design t2b-1.attempt2, dated 2026-11-11 22:56). They are not part of this run; the t3-1 (makeTheAliasOnly) and t2b-1 (design) cost.json files count them (attempts=2), so cost.json overstates those two rows. The tables above use the final attempt1 meta only.
- gpt-6.1-sol (t2-1) output is thin on all 3 packages (603, 947, 664 tokens).
- Merge warnings (round not refused, valid findings still merged): makeTheAliasOnly t2b-1 "anchor2 must have at most 200 characters" (2 errors); design t3-1 "claim must have at most 300 characters" (1 error). Those reviewers' invalid findings were not counted by the validator.
- resolution.json is built per SPEC from resolution-live7.json (only .model overwritten). The inherited `model_name` labels in live7 do not match the model for some ids (e.g. t2-1 labelled "Muse Spark 1.3"); they are labels only, left as is.
- Pre-existing merge-time quirk: the ledger/merge treat 'model' from the resolution, which is the row's model per id.
