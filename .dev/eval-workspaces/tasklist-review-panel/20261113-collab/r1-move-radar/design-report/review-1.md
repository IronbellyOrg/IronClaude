# Review 1 of DESIGN.md (Redesign 1: Move Radar)

Verdict: **FAIL** (4 BLOCKING, 10 MINOR)

Paths: `D` = `r1-move-radar/DESIGN.md`, `SRC` = `merged-requirements.md`, `A1` = `20261111-a1`.

## BLOCKING

**B-1. The Gate 0 rule makes the collab-1 smoke test impossible to run.**
- Where: D:77 and D:412 say `launch.sh` with collab 1 refuses to start unless `gate0.json` lists every gated spike as `pass`.
- S3 is one of those gated spikes (D:421: "S3 | The smoke test below"), and AC-2 requires it (D:441).
- But S3 is itself a collab-1 run through `launch.sh` (D:426: `PANEL_COLLAB=1 bash tools/launch.sh el2 0 …`).
- Result: S3 can never pass, so AC-2, AC-3 and every collab-1 row are blocked.
- Fix: leave S3 out of the precondition (for example, the smoke rep is gated only on G-BASE, G-PINS, S0, S2 and Spike 4), or give the smoke run its own gate.

**B-2. Spike 4 reads session transcripts that launch.sh has already deleted.**
- D:191 says Spike 4 takes turn durations and T_report from "the persisted session transcript of the final attempt".
- `launch.sh` runs `cleanup-sessions.sh <row>` at the end of every row (D:110, D:323). That script deletes exactly those session files (D:64).
- `spikes/spike4.sh` runs `values.py spike4` only after its 3 collab-0 rows have finished (D:422). By then the data is gone, so no values file can be computed and no collab-1 row can start.
- Fix: read the timestamps from `reviews/<rid>.attempt<n>.json`. The `--output-format json` array has a `timestamp` on its assistant messages (checked on `A1/TASK-WF-design-20261108-041415/reviews/combos/b4-muse-ember-luna2/t4-1.attempt1.json`: 33 of 35 entries). Or skip cleanup for Spike 4 rows.

**B-3. The after-run leak check cannot see the text that was actually delivered, and F-4 contradicts the board format.**
- A board line may only have the keys `v,id,run,from,to,t,kind,move` (D:131).
- The `leak` rule compares the *rendered text*, which only the hook passes in, as `{"line","text"}` on stdin (D:134-136).
- The `inject` metrics event does not store the text either (D:168).
- So the after-run pass by `collab_summary.py` over `msgs/radar.jsonl` (D:56, D:136, D:208, D:212) has no text to compare. Its "hard failure → QUARANTINED" on leaks can never fire on what the model received.
- F-4 ("one with altered text", D:398) cannot be built as written: a board line has no text field, and adding a `text` key would be rejected as `bad_key`, not `leak`.
- The source asks for a leak lookup over every injected line, with a hard failure (SRC:433, R-32 verification SRC:1070).
- Fix: log the rendered text (or its sha256) with each inject event or board line, or check the session transcript after the run. Then restate F-4 against that record.

**B-4. collab_summary.py runs before the files it needs exist.**
- `collab_summary.py` runs at step 3, before merge (step 5) and anonymise (step 6) (D:109, D:318-321).
- It must still write `ledger_rows` ("rows in `ledger.json`", D:219) and the `anon_leak` count over `merged-anon.md` into `audit.json` (D:215).
- Neither `ledger.json` nor `merged-anon.md` exists at step 3. So the ledger-row half of the CONVERGENCE alarm (R-25, SRC:1052; D:223) gets no input, and the arm-blinding audit is never computed.
- Fix: run a second summary pass after anonymising. Keep the quarantine decision in the pre-merge pass.

## MINOR

- **M-1. rep 0 contradiction.** D:312 says `<rep>` must be a positive integer, but the smoke test uses rep 0 (D:426, D:433). A strict `launch.sh` would refuse the smoke run.
- **M-2. Spike 5 dropped silently.** R-27 (SRC:1059) lists Spike 5 among the Gate 0 spikes, and D:21 says the design implements R-21..R-30. The Gate 0 table (D:414-422) leaves Spike 5 out without saying so. Either state that it is out of scope (it measures H, not F3) or add it.
- **M-3. collab.json field list incomplete.** The list at D:219 misses R-23's `arm` and `panel_finish_at` (SRC:1050). It also does not say whether `pairwise_task_jaccard` is written as its own key. T-17 asserts "every R-23 key", so an implementer working from D alone would fail that test.
- **M-4. `agent_id` is unverified.** Subagent filtering depends on `agent_id` in the hook's stdin (D:140, D:161), but the S0 pass condition (D:418) never checks that the field exists. If it is missing, subagent tool calls would move the checkpoints.
- **M-5. `hook_ms_p95` has no workable source.** D:172 says Spike 4 derives it "from the metrics timestamps", while D:422 says S0 records it. Tele records only the start time `t`, and metrics logs only checkpoint events, so the time spent in each hook call is never recorded.
- **M-6. Re-ask tokens use a different measure.** Re-ask tokens come from `result.usage.output_tokens` (D:202). Attempts use `modelUsage` `outputTokens`, which includes subagents (`A1/tools/run-reviewer.sh:53`). `total_output_tokens_all` therefore mixes two definitions.
- **M-7. Relative report paths can leak the row id to the judge.** The merge step passes report paths as `runs/<row>/<pkg>/reviews/<rid>.md` (D:320). The merged report prints `- <rid>: report <path>` (`src/superclaude/cli/review/ledger.py:423`), and the anonymiser rule only redacts `report <EVAL>/…` (`A1/tools/tmp-scripts/anon-b11.sh:25`). With relative paths, the row id (which contains `c0`/`c1`) would reach the judge. D:9 says paths are absolute: state that explicitly at step 5.
- **M-8. Block randomisation not addressed.** "Block-randomised order" (R-28, SRC:1060; SRC:938) is neither implemented nor listed as omitted. `alarms.py` computes `baseline_drift` "per block" (D:223), but D never defines a block.
- **M-9. Spike 4 rows can be cut short by the planning hang guard.** Spike 4 collab-0 rows use the planning hang guard 1.5 B (D:300). Historical SL2 maxima (alias 416 s, control 440 s, SRC:278) exceed 410.6 s, so spike rows can be killed. That truncates elapsed times and biases B_f low. This risk is not listed in section 7.
- **M-10. One R-03 check missing from G-BASE.** R-03 also asks to verify that the repaired `refs/merge-guard.md` line is absent in the designSpec sandbox (SRC:1007). That check is not in the G-BASE pass condition (D:416).

## Checked and holds

- **Timing tables (D:262-272, D:186-190, T-12):** all recomputed.
  - el2: 143.8, k=2, ≤6.6 / ≤19.4 s, 109.6, 174, 130.8 / 143.6 s.
  - sl2: 341.5, 65.8/28 → 2, ≤23.8 / ≤51.8 s, A-2 → 2, 266.7, 410.6, 303.7 (+11.0%) / 331.7 (+21.2%).
  - hl2: 275.3, 35.3/46 → 0, ≤12.3 s, A-2 → 2, 152.4, 357, 240 (+0.8%).
  - Q-1: 286 s.
- **Rotation offsets:** recomputed with `sha256sum`: t4-1 → 0, t3-1 → 4, t2b-1 → 1, t1b-1 → 2, t2-1 → 0, and the rotated lists are right.
- **Judge path:** the traversal resolves to `R1/scoring/<opaque>` (`realpath -m`), and `A1/arms/scoring/combos` exists.
- **Judge pin:** `judge-one.sh` sha256 is `a01bd70d…cfcc`, and `judge-one.sh:4-6` matches the design.
- **Base commits:** the base SHAs and squash parents are right (0b8a5801d^1 = 0e486ab8d, 4eb75698d^1 = 38eb3c58a, 54e21668f^1 = 5fa680778). The T1 start SHAs match `progress.md`, and all three bases have only `PreToolUse` hooks in `.claude/settings.json`.
- **Task headings:** `## Task N:` appears in all three candidates (13 / 9 / 12).
- **Tools:** jq 1.7 is at `/usr/bin` (so F-14's PATH works), `flock` is present, and `bats` is absent.
- **Harness citations:**
  - `run-reviewer.sh:13-17` (brief), `:48` (command) and `:50-57` (model checks)
  - `merge-b11.sh:11-12`, `:17-25` and `:34`
  - `final-table.py:31-37`
  - `SPEC.md:79` (degraded panel) and the step-3 rerun rule
  - `manifest.md` (throwaway git repo)
- **Merge interface:** `merge_cmd.py` takes repeated `--report RID=PATH` and `--resolution`.
- **H2 normaliser:** it fits `findings.py` (`parse_block` returns `{ok, errors:[{line,msg}]}`; limits 12-200 / 300, refs ≤ 8, id ≤ 16; `flat` and `locate` exist).
- **Hook output:** the shape `hookSpecificOutput.additionalContext` is the documented PostToolUse form.
- **Constraints:** models only ember, luna, haiku and sonnet, Opus only as judge, no Qwen or glm, `NOFALLBACK=1`, UV, writes only under R1/ and the sandbox. All are respected.
- **Deliverables (1)-(7):** all present, apart from the defects above.
