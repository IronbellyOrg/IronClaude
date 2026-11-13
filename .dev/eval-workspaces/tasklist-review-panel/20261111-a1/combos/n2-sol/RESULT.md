# n2-sol RESULT (Batch 3, re-run after cooldown)

Row: t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7, t2-1=gpt-6.1-sol. No scoring.
Run 2026-11-12 03:41-04:51 UTC, one reviewer at a time. A zero-load probe before the run showed muse-wonder-1.0 served by muse-wonder-1.0 (the earlier misrouting to gpt-6.1-terra is gone). Every reviewer passed the observed-model check on attempt 1. The earlier stopped attempt's files are kept as RESULT.stopped-attempt.md and under each package's `reviews/combos/n2-sol/_prior-stopped-attempt`.

Merge: `superclaude review merge --round 1`, custom resolution at `combos/n2-sol/<package>/resolution.json` (the four ids with the models above; tier fields kept from resolution-live7.json). All three merges succeeded: verdict FAIL, decision REVISE. The `unpassable-ac` category fix was not needed.
Findings = findings the merge accepted from that reviewer; blocking = those marked blocking. "thin" = under 1000 output tokens.

## TASK-WF-designSpec-20261107-075614 (merged-1.md present)
| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 157 | 16454 | - | 3 | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 202 | 45210 | - | 7 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 943 | 60707 | - | 4 | 0 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 25 | 579 | thin (empty findings block) | 0 | 0 |
Total: 1327 s wall, 122950 output tokens.

## TASK-WF-makeTheAliasOnly-20261105-051649 (merged-1.md present)
| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 114 | 12385 | merge warning: one finding rejected (anchor2 over 200 chars); 4 in block, 3 accepted | 3 | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 251 | 55772 | - | 8 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 1129 | 53637 | - | 6 | 2 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 29 | 732 | thin (empty findings block) | 0 | 0 |
Total: 1523 s wall, 122526 output tokens.

## TASK-WF-design-20261108-041415 (merged-1.md present)
| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 83 | 11617 | - | 5 | 2 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 190 | 44169 | - | 7 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 981 | 72042 | - | 5 | 0 |
| t2-1 | gpt-6.1-sol | gpt-6.1-sol | 1 | 26 | 814 | thin (empty findings block) | 0 | 0 |
Total: 1280 s wall, 128642 output tokens.

## Caveat: a second writer touched this folder
My run log shows t4-1 and t2-1 of the designSpec package finishing at 03:48 and 04:04, but the files on disk for those two were written at 03:55 and 04:20 (the t4-1 wall of 246 s in my log is 202 s on disk). Another process wrote reviewer outputs into `reviews/combos/n2-sol/` during my run, so my own runs of those files were overwritten and the concurrency may have exceeded one run. Each on-disk set (md, json, meta, cost) was written within about a second, so the files are internally consistent, and every one passed the model check. The tables and the merges use what is on disk. Wall seconds and tokens for t4-1 and t2-1 in this package (and possibly in the other two) may belong to the other writer's run, not mine. I did not investigate who it was. I did not check the other two packages' file times.

## Notes
- gpt-6.1-sol returned a valid but empty findings block with under 1000 tokens on all three packages (the thin flag).
- Grok's observed model is reported as `grok-4.7-build`, which the script accepts as grok-4.7.
- Merged outputs: `combos/n2-sol/<package>/merged-1.md`, plus ledger.json, resolution.json, merge.stdout and merge.stderr.
