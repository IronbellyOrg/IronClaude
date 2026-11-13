# n4-sonnet RESULT (Batch 3 re-run)

Row: t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=claude-haiku-5-5, t1b-1=claude-sonnet-5-5. Every reviewer ran fresh via tools/run-reviewer.sh (driver ran the jobs; I verified outputs, did not rerun). No scoring.

Findings = lines in the reviewer's own findings-v1 block. Own-blocking = those with blocking:true in the reviewer's block. Merged-blocking = that reviewer's findings listed under 'Blocking findings' in merged-1.md. Thin = under 1000 output tokens. Invalid = model_ok false or no findings block.

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | own-blocking | merged-blocking |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 116 | 13873 | ok | 4 | 0 | 1 |
| t3-1 | glm-5.3 | glm-5.3 | 1 | 835 | 46363 | ok | 0 | 0 | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 246 | 55127 | ok | 8 | 1 | 2 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 165 | 21701 | ok | 5 | 0 | 1 |

Total (sum of four runs): wall 1362 s, output tokens 137064. merged-1.md: combos/n4-sonnet/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | own-blocking | merged-blocking |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 114 | 16331 | ok | 5 | 2 | 3 |
| t3-1 | glm-5.3 | glm-5.3 | 1 | 1463 | 82032 | ok | 7 | 1 | 3 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 208 | 47048 | ok | 8 | 3 | 5 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 216 | 30317 | ok | 6 | 0 | 5 |

Total (sum of four runs): wall 2001 s, output tokens 175728. merged-1.md: combos/n4-sonnet/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | own-blocking | merged-blocking |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 98 | 13602 | ok | 6 | 1 | 4 |
| t3-1 | glm-5.3 | glm-5.3 | 1 | 706 | 39453 | ok | 3 | 0 | 2 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 218 | 48026 | ok | 9 | 2 | 7 |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 193 | 21844 | ok | 6 | 0 | 5 |

Total (sum of four runs): wall 1215 s, output tokens 122925. merged-1.md: combos/n4-sonnet/TASK-WF-design-20261108-041415/merged-1.md

## Notes
- No attempt retried (attempts=1 everywhere); no INVALID reviewer; no category normalisation needed (no 'unpassable-ac' in any report).
- makeTheAliasOnly t3-1 (glm-5.3) was rerun by the driver at ~05:11 (first run 1175 s, 67504 tokens, kept in reviews/combos/n4-sonnet/t3-1-firstrun/ and combos/n4-sonnet/<pkg>/firstmerge/). The table and merged-1.md use the rerun (1463 s, 82032 tokens); merged-1.md (05:35:34) was written after the rerun finished (05:35:30).
- resolution.json label quirk: glm-5.3 entries carry model_name 'Qwen 3.8 Max' inherited from resolution-live7.json; the model field is glm-5.3.
- .err files only show claude-code 'unrecognized_model' warnings; observed models matched in all 12 runs.
- designSpec t3-1 (glm-5.3) returned a valid but empty findings-v1 block (verdict PASS, 46363 tokens): 0 findings, not invalid.
