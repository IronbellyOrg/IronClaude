# Combo n2-terra (Batch 3): muse-wonder-1.0 + claude-haiku-5-5 + grok-4.7 + gpt-6.1-terra

All 12 runs were fresh (no reuse of earlier batches), via tools/run-reviewer.sh, 2 at a time. No scoring.
Findings / blocking = rows in the reviewer's findings-v1 block as accepted by the merge (blocking = `"blocking": true`). Thin = under 1000 output tokens.

## Key caveats
- **t2b-1 muse-wonder-1.0 is INVALID on all 3 packages.** Both attempts failed the script's observed-model check. Claude Code printed `[claude-code:unrecognized_model] muse-wonder-1.0`. Attempt 1 observed `gpt-6.1-terra,muse-wonder-1.0` (mixed; per-model usage lists only muse-wonder-1.0), attempt 2 observed only `gpt-6.1-terra` (the script's final copy). The muse outputs were therefore not merged and are not part of the merged reports (merged-1.md has t4-1, t4-2, t2-1 only; resolution.json has those three ids). Raw attempt files are kept in the reviews folders.
- **t2-1 gpt-6.1-terra is thin on all 3 packages** (363-631 tokens, 15-19 s, 0 findings; it returned an incomplete report saying a referenced input was missing). Valid model, empty findings block.
- **designSpec / makeTheAliasOnly / design: t4-2 grok-4.7 on makeTheAliasOnly** had its findings block rejected by the merge ("heading" problem), so its 6 findings are NOT in that merged report. Not rerun: the merge accepted the round. Its raw count is shown in parentheses.
- No `unpassable-ac` categories appeared; no `.catfix.md` copies used.

## TASK-WF-designSpec-20261107-075614
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | gpt-6.1-terra (att. 2) | 2 | 103 | 4355 | INVALID (wrong model) | not merged | - |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 139 | 31043 | ok | 5 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 825 | 53752 | ok | 3 | 1 |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 17 | 478 | thin | 0 | 0 |

Total: 1084 s, 89628 output tokens. Merge: verdict FAIL, REVISE; merged-1.md written.

## TASK-WF-makeTheAliasOnly-20261105-051649
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | gpt-6.1-terra (att. 2) | 2 | 35 | 987 | INVALID (wrong model), thin | not merged | - |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 273 | 64537 | ok | 10 | 2 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 628 | 40996 | block rejected by merge | 0 merged (6 raw) | 0 merged (3 raw) |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 19 | 631 | thin | 0 | 0 |

Total: 955 s, 107151 output tokens. Merge: verdict FAIL, REVISE; merged-1.md written.

## TASK-WF-design-20261108-041415
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Flag | Findings | Blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | gpt-6.1-terra (att. 2) | 2 | 42 | 1033 | INVALID (wrong model; att. 1 also had no findings block) | not merged | - |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 200 | 45610 | ok | 6 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 706 | 47102 | ok | 2 | 1 |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 15 | 363 | thin | 0 | 0 |

Total: 963 s, 94108 output tokens. Merge: verdict FAIL, REVISE; merged-1.md written.

Files: combos/n2-terra/<package>/{resolution.json, ledger.json, merged-1.md}; raw reviews in <package>/reviews/combos/n2-terra/.
