# Review 2 of DESIGN.md (Redesign 1: Move Radar)

Verdict: **FAIL**. B-1 to B-4 are all FIXED. One new blocking defect: N-1, in the B-2 fix itself.

Paths: `D` = `r1-move-radar/DESIGN.md`, `SRC` = `merged-requirements.md`, `A1` = `20261111-a1`.

## Status of the review-1 blocking findings

**B-1 (Gate 0 made the smoke test impossible): FIXED.**
- D:412 now splits the gate:
  - collab-0 rows need G-BASE and G-PINS;
  - the collab-1 smoke row (`rep` 0) needs G-BASE, G-PINS, S0, S2 and Spike 4;
  - collab-1 rows with `rep` ≥ 1 also need S3.
- AC-2 (D:441) matches this.
- D:312 allows `rep` 0, which also clears M-1.
- The smoke run's collab-0 half (D:426) needs only G-BASE and G-PINS, so nothing depends on itself.

**B-2 (Spike 4 read deleted transcripts): FIXED.**
- D:191 now reads timestamps from `reviews/<rid>.attempt<n>.json`, which is kept (D:89), not from the session file that `cleanup-sessions.sh` deletes.
- I spot-checked `A1/TASK-WF-design-20261108-041415/reviews/combos/b4-muse-ember-luna2/t4-1.attempt1.json` with jq. It has 35 entries: 20 `assistant`, 13 `user`, 1 `system`, 1 `result`.
- All 33 `assistant` and `user` entries have `timestamp`. Only `system` and `result` lack it, so the "33 of 35" claim is correct.
- The data source is therefore sound. The way turns are counted from it is not: see N-1.

**B-3 (the after-run leak check had no text to compare): FIXED.**
- D:136 and D:168: the `inject` metrics event now stores `text` and `text_sha256`, joined to the board line by `id`.
- `collab_summary.py pre` re-runs the validator over every (board line, logged text) pair. It also flags an `inject` event with no board line, and a board line with no `inject` event.
- F-4 (D:398) can now be built. It has three fixtures, each of which leads to exit 3 and `QUARANTINED`:
  - an `anchor` key, rejected by the `bad_key` rule;
  - logged text that differs from the catalogue text, caught by the `leak` rule;
  - an orphan board line.

**B-4 (the summary ran before its inputs existed): FIXED.**
- The order pre → merge → anonymise → post → judge is the same in all three places:
  - section 1.2 (D:60): `pre` before the merge, `post` after the anonymiser;
  - section 2.1 (D:109);
  - section 5.2 (D:318 step 3, D:320 step 5, D:321 step 6).
- T-17 (D:387) tests that `pre` works without `ledger.json` and `merged-anon.md`, and that `post` adds `ledger_rows` and `anon_leak`.

## New blocking defect

**N-1. Spike 4 measures gaps between content blocks, not turns, so `turn_p90` is wrong.**
- Where: D:191 defines turn durations as "differences between consecutive assistant-message `timestamp` fields".
- `SRC:66` defines `turn_p90` as the 90th percentile duration of one turn. It feeds `finish_offset`, `k` and the guard (D:186-189), and the values file is frozen (R-30).
- Problem: in the `--output-format json` array, each content block of one model response (thinking, every parallel `tool_use`, text) is a separate `assistant` entry with the same `message.id`.
- Measured on the spot-check file above:
  - There are 19 consecutive gaps between `assistant` entries.
  - 10 of them are 0.001-0.087 s. These are parallel `tool_use` and thinking blocks of one response; for example, `resp_04008f…` has 7 entries within 12 ms.
  - The two largest gaps (21.1 s and 10.6 s), which set the p90, are between thinking blocks *inside the final report response* (`resp_05b831…`). That time belongs to `T_report`, not to a tool turn.
  - The real tool turns in this file (previous `tool_result` to the end of the next response) are about 3.5, 4.5 and 8.6 s.
- Result: the computed `turn_p90` is a mix of near-zero block gaps and pieces of the report turn. That changes `k` and PANEL_FINISH_AT for every collab-1 row, and the value is never recomputed.
- Fix:
  - Group `assistant` entries by `message.id`, and exclude entries with a non-null `parent_tool_use_id`.
  - Define one turn as the time from the previous `tool_result` (or from the start of the session) to the last entry of that response.
  - Leave the final response out of `turn_p90`; it is already `T_report`, defined correctly at D:191.

## Changed passages checked, with no new blocking defect

- **Section 2.2, last paragraph (D:136):** consistent with step 10 (D:168) and F-4.
- **Section 2.4 step 10 and the Cost paragraph (D:168, D:172):** an `{"ev":"t"}` metrics line on every exit gives `hook_ms_p95` a source, which clears M-5. This agrees with S0 (D:422) and the collab.json field list (D:219).
- **Section 2.7 Outputs (D:202):** checked `A1/tools/run-reviewer.sh:53`. It is `TOKALL = sum of modelUsage[].outputTokens` of the `result` event, as cited, and line 48 is the attempt command. This clears M-6.
- **Section 2.9 (D:219):**
  - The field list is checked against R-23 (SRC:1050). Every key is present, including `arm`, `panel_finish_at`, `pairwise_task_jaccard` and the values sha256.
  - The block definition (D:223) is internally consistent, and section 7.1 (D:464) lists it as a design choice.
- **Section 4, "Values for collab 0" (D:300):**
  - The 2.0 × planning B guards are right: 232, 547.4 and 476 s.
  - 1.5 × 273.7 = 410.6 s is below the cited historical maxima of 416 s and 440 s.
  - Collab 1 without a values file is refused.
  - This agrees with D:293 and D:464.
- **Section 5.2 step 5 (D:320):** checked `src/superclaude/cli/review/ledger.py:423`. It prints `- {reviewer_id}: report {report}`. `A1/tools/tmp-scripts/anon-b11.sh:25` redacts only `report <EVAL>/…`, and `A1/analysis/merge-b11.sh:34` is the cited merge call. The requirement for absolute paths is therefore correct and needed.
- **Section 6.3 intro (D:412):** consistent, as under B-1. Spike 5 is now out of scope with a reason, which clears M-2.
- **G-BASE row (D:416):**
  - `git show --stat 0b8a5801d` shows `merge-guard.md | 196 ++`.
  - Its parent is `0e486ab8d…`.
  - `git cat-file -e 0e486ab8d:…/merge-guard.md` fails, so the file is absent at the base and the check holds.
- **S0 row (D:418):** now checks `agent_id` on subagent calls and fails closed, which clears M-4.
- **F-4 and T-17:** see B-3 and B-4.
- **AC-2 (D:441):** consistent with D:412.
- **Section 7.1, design-choices paragraph (D:464):** consistent with D:223, D:300 and D:412.

Not blocking, noted only:
- AC-2 says the S3 gate refusal is "tested in T-10", but T-10's checks (D:380) do not list it.
- `post` records `anon_leak`, but no step says what happens when it is above 0. The judge still runs at step 7.
