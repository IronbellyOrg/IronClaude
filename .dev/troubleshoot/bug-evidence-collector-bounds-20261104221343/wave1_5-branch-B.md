# Wave 1.5 Branch B (architectural docs), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

| doc_path | currency_verdict | reason |
|---|---|---|
| src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh | unknown | :12-13 "It writes only into --out (which must be missing or empty)"; :25-26 "The whole run is bounded to 60 seconds."; :72-73 "(under `timeout` when it is on PATH)": the header promises 60 s, :73 makes `timeout` optional |
| src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | unknown | :19 `--out <output-dir>/sync/<cycle_id>/<n>/` (keyed by cycle_id and n only); :30 any EVIDENCE_FAIL escalates to Tier 3; :95 "The record and the evidence directories stay in the output dir after an abort." |
| src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | unknown | :71 resolution.md under `<output-dir>/sync/<cycle_id>/`; :99 the validator's `output_dir` is `<output-dir>/sync/<cycle_id>/` |
| src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | unknown | :71 "or the reused open cycle id on a resume restart"; :247 "restart under the same `cycle_id` (`sync_started{resumed: true}`)"; :249 restart as row 5; :252 a c_initial cycle restarts at step 0 |
| src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | unknown | :97 resolution.md and "the evidence directory"; :103 message file and manifest "both under `<output-dir>/sync/<cycle_id>/`" |
| .dev/tasks/done/TASK-WF-design-20261104-164423/source.md | unknown | :835 --out missing or empty else out_not_empty; :841 "Whole run under 60 s (`timeout` per command when available)" |
| .dev/tasks/done/TASK-WF-design-20261104-164423/source.md | unknown | :1224 D-9 the 60 s bound is a testable design requirement |
| .dev/tasks/done/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md | unknown | :212 E4 pins out_not_empty; no restart test |

- No doc defines a per-attempt directory or clears the evidence directory on restart; conflict-intent.md:95 keeps it after an abort, which is the leftover a same-cycle_id restart hits.
- No doc says how the run stays within 60 s without `timeout`.
- src/superclaude/commands/pr-submit.md:49 `--timeout` is the review-wait timeout only; SKILL.md has no collector hits.
