# Wave 1.5 Branch A (release docs), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

- release_slug: none (only .dev/releases/backlog/v4.xx-SpawnV2/archive/remediation/major/M5-retry-batch-conflict.md matches "conflict"; unrelated). Controlling artifact: design package TASK-WF-design-20261104-164423.
- artifact_paths: [.dev/tasks/done/TASK-WF-design-20261104-164423/source.md]
- summary (citations are source.md):
  - Time bound: :841 "Whole run under 60 s (`timeout` per command when available); exceeding it: `EVIDENCE_FAIL timeout`." Nothing says what happens when `timeout` is missing; D-9 (:1224) calls the 200 KiB / 60 s bounds testable, but tests E1-E4 (:1392) have no timeout case. The script follows "when available" and breaks "whole run under 60 s": a design gap.
  - --out: :835 --out must be missing or empty, else `EVIDENCE_FAIL out_not_empty`; E4 (:1392) pins it. :844 and :1012 pass `--out <output-dir>/sync/<cycle_id>/<n>/`; any EVIDENCE_FAIL escalates to Tier 3 `sync_tier3` (:844, :1012).
  - Restart: :295 step 3 reuses the open cycle id on a resume restart; rows 5 and 7 (:379, :381) restart under the same cycle_id with `sync_started{resumed: true}`; D-15 (:1230) "`resolution.md` is kept as input". No section clears or versions the old `sync/<cycle_id>/<n>/` folders, so a Tier 2 restart fails `out_not_empty`: a contradiction inside the design.
- confidence: 0.85
