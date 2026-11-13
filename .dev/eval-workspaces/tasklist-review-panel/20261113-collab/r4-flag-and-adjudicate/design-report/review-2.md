# Review 2 of DESIGN.md (Redesign 4, Flag-and-Adjudicate, F7)

## Scope checked

- `DESIGN.md` read in full (lines 1-571), in pieces of at most 200 lines.
- `review-1.md` read in full (B-1..B-6, M-1..M-15).
- Source of truth `merged-requirements.md` (`REQ`): lines 177-357 (section 2.0), 705-800 (Redesign 4), 922-994 (section 4), 997-1130 (section 5); line 22 for the issue-label to GT-id mapping.
- Code read: `EVAL/tools/run-reviewer.sh` (`RR`) lines 1-87; `EVAL/tools/tmp-scripts/judge-one.sh` (all); `EVAL/analysis/merge-b11.sh:1-40`; `EVAL/analysis/final-table.py` (blocking definitions); `src/superclaude/cli/review/merge_cmd.py` (all); `ledger.py:95-230` (`merge_round`) and the `render_merged_report` output lines; `findings.py:12-24, 88-122` and its function list.
- Host checks (read only): `/usr/local/bin/claude` (a `sh` wrapper); the real binary path; `ps -eo args` for live `claude -p` processes; the three candidates grepped for the anonymiser's forbidden strings, reviewer ids and `origin`; `EVAL/arms/scoring/combos` exists. No ground-truth content was read.
- Recomputed: k at every `test_values.py` vector in integer ms (2, 1, 1/0 at 13.8/13.9, 1/0 at 51.795/51.8, 0, 1); `finish_offset(116, 6.4, 6.4)` = 143.8; hang 174; section 3 thresholds (19.4 s, 51.795 s, 81.3 s); slowdown limits 5.7% / 16.7%, 8.7% / 18.9%, 5.2%; planned ends; flagger 3rd-call times; R-35 deal and form vectors (r = c = 0: C, F, F, C; c = 1: F, C, C, F); the `reach` GT ids against `REQ:22` (B1-B5 = designSpec GT1-5, I1-I5 = GT6-10, B6-B8 and I6 = alias GT1-4, I7 = control GT1) - all correct.
- Cross-references "section X step Y" checked: every one points at the right place.
- Write paths: everything under `R4` or `SBR`, plus `/tmp/jdg.*` (see m-9) and Claude Code's own transcripts.

## Review-1 blocking findings status

| Id | Status | DESIGN.md text that fixes it |
|---|---|---|
| B-1 judge staging in the reviewers' sandbox root | FIXED (a residual exposure is raised as N-2) | Decision 6: "a short-lived staging directory `/tmp/jdg.XXXXXXXX` made by `mktemp -d` ... **not** under `SBR` and is deleted as soon as its results are copied back"; 5.1 step 5.6 "delete `STAGE` with `rm -rf -- "$STAGE"`"; 2.10 audit patterns now include "`ground-truth`, `judge.json`, `score.json`, `/tmp/jdg.`, the absolute `REPO` path". |
| B-2 a reviewer without a block breaks the merge | FIXED | 2.6 step 5: "`<rid>.final.md` is always written. If the last attempt has no findings block, it is a copy of `<rid>.md` (an empty file when the process produced no text)"; 5.1 step 2.5 "still passed to the merge through its always-present `<rid>.final.md`"; fault row "One reviewer without a block". Checked against `merge_cmd.py:84-98` and `ledger.py:127-157`: an empty or blockless file parses as `ok: false` and the merge keeps the others. |
| B-3 refused launch overwrites `run.json` | FIXED | 5.1 step 0: "append ... to `runs/refusals.jsonl`, never creating or touching `runs/<row>/`"; `test_launcher.py`: "the row's files (its `run.json` included) are byte-identical after the refused call". |
| B-4 wrong k test vector | FIXED | 2.7: "computed in integer milliseconds ... `0.35 B` as `B_ms * 35 // 100` ... SL2 gives k = 1 at T_report_p90 = 51.795 s and k = 0 at 51.8 s"; `test_values.py`: "`k_of(273.7, 14, 51.795)` and `51.8`" expecting "1 and 0", plus `pytest.approx`. Recomputed: 95795 - 16000 - 51795 = 28000 / 28000 = 1; 27995 / 28000 = 0. |
| B-5 turn duration misses multi-block output | FIXED | 2.7: "A turn's duration is the **last** entry's `timestamp` in the group minus the `timestamp` of the last entry before the group"; `test_values.py` adds "a final assistant message written as two entries"; S0 records "whether one assistant message is written as several entries". |
| B-6 card references unblind the judge | FIXED | 5.1 step 4: "every other `card cN` (all case-insensitive, `\bcards? c[0-9]+\b`) are deleted ... greps the output ... plus `\bcards? c[0-9]+\b`, `panel card` and `peer reviewer`, and exits 1"; adjudicator brief: "do not mention the card or a peer in it"; `test_anon.py` cases with "Card c1" and "a peer reviewer flagged this". None of the three candidates contains these strings or a reviewer id, so no false hit. |

## New blocking findings

### N-1. The concurrency count can never match a real reviewer process, and S0 then blocks every panel

- **DESIGN.md location:**
  - 5.1 step 0: "count model sessions with `pgrep -fc '^claude -p'` and ember sessions with `pgrep -fc '^claude -p --model muse-ember-1.0'` (anchored at the start of the command line ... S0 confirms that the CLI's command line starts with `claude`)".
  - 6.3 S0 pass condition: "and that the process command line starts with `claude -p` (the concurrency count of 5.1)". If it fails: "F7 cannot run on that model: no panel using it as flagger or adjudicator runs".
- **Evidence:**
  - `/usr/local/bin/claude` is a 10-line `sh` wrapper: `claude_bin="/opt/nvm/versions/node/v24.22.2/bin/claude"` (line 3), then `exec "$claude_bin" "$@"` (line 6) or `exec "$orca" "$@"` (line 8).
  - `ps -eo pid,args` on this host shows a live `-p` session as `278416 timeout 3600 claude -p --model claude-opus-5-5 ...` and its child as `278422 /opt/nvm/versions/node/v24.22.2/bin/claude -p --model claude-opus-5-5 ...`. No process command line starts with `claude -p`.
  - `tests/fake-claude` started through a `#!/usr/bin/env bash` shebang shows as `bash <path>/claude -p ...`, so the offline test cannot match the pattern either.
- **Why it matters:**
  - `pgrep -fc '^claude -p'` returns 0 every time. The `REQ` 4 conduct limits ("at most 10 concurrent runs and at most 4 ember", R-28) are not enforced, although the design says they are.
  - S0 will fail its own command-line item for all four models. The S0 failure action then says no panel may use that model, which stops every F7 arm. An implementer either ships an inert guard or follows the table and runs nothing.
  - This defect was introduced by the fix for review 1's M-7.
- **Suggested fix:**
  - Count launcher-owned state, not command lines. Under the existing `flock SBR/launch.lock`, each `reviewer.sh` writes `SBR/running/<row>.<pkg>.<rid>` holding its PID and model and removes it on exit (trap). The guard counts entries whose PID is alive (`kill -0`) and, for ember, entries whose model is `muse-ember-1.0`.
  - Alternatively, match `pgrep -f '(^|/)claude -p --model '`, which excludes `timeout ...` and `bash reviewer.sh ...` lines.
  - Remove the command-line item from the S0 row whose failure blocks F7, or give it its own failure action ("switch the guard to the PID-file count").

### N-2. Ground truth stays reachable to concurrent reviewers, and the audit only matches literal absolute paths

- **DESIGN.md location:**
  - 2.10, row "Reviewers never see ground truth": "a reviewer tool call is a violation when it names `ground-truth`, `judge.json`, `score.json`, `/tmp/jdg.`, the absolute `REPO` path ..., any `/tmp` path other than its own sandbox ..., or (for a luna) the board directory".
  - 5.1 step 0: "Three panels launched together therefore stay at 9 reviewer sessions, plus any judge sessions"; 5.1 step 5.4: "a second failure marks the package `judge_failed`"; step 5.5 "Fail the package with `judge_wrote_into_eval`"; step 5.6 (the only step that deletes `STAGE`).
  - Risk 1: "enforced by audit ...: transcript scan for those paths".
- **Evidence:**
  - Rows run concurrently. While one row's judge runs (up to 2 x 900 s per package, `judge-one.sh:25`), `/tmp/jdg.*/<pkg>/<L>/` holds `score.json` (GT ids) and, after the first attempt, `judge.attempt1.json` (the judge's Read of `ground-truth.json`, review 1 B-1 evidence). Reviewers of the other rows run with unrestricted Bash and the same uid. `mktemp -d` mode 0700 does not stop the same user.
  - A reviewer's cwd is `/tmp/evalsb-collab-r4/sb/<pkg>/repo`, so `ls ../../../..` is `/tmp`, and `cat ../../../../jdg.Ab12Cd34/...` reaches the staging. That command contains neither `/tmp/jdg.` nor any absolute `/tmp` path. The same holds for `../../../board/...`: a luna reading the other luna's cards or snapshot (`snap/<rid>.jsonl`) does not name "the board directory".
  - `RR:17` already teaches reviewers `~/...` paths. `grep -rn X ~/workspaces` or `grep -rn X /home/coder` reads `EVAL/*/ground-truth.json` and `R4/runs/*/scoring/judge.json` without containing the absolute `REPO` string or `ground-truth`.
  - Step 5.6 runs only on the success path. Steps 5.4 and 5.5 end the package without saying that `STAGE` is deleted, so a failed judge leaves a ground-truth copy in `/tmp` for every later row.
- **Why it matters:**
  - This is a route to ground truth that the harness itself creates (check g). The design's only control is the audit, which misses the relative, `~` and ancestor-directory forms. A contaminated row would then pass AC-13 with `audit_ok: true`.
- **Suggested fix:**
  - Add a content audit that does not depend on path spelling. Flag a reviewer transcript as a violation when any tool **result** contains `"blocking_in_implement"` or `"plan_quote"` (keys found only in ground truth and judge output), any GT `description` string, or (for any reviewer other than the card's recipient after delivery) `"panel-msg/1"`.
  - Before matching names, resolve each path token in a Bash command against that call's `cwd` and expand `~`. Flag any recursive search (`grep -r`, `find`, `rg`, `ls -R`) whose root is `/`, `/tmp`, `/home`, `~`, or an ancestor of `SBR` or `REPO`.
  - Delete `STAGE` from a `trap` on every exit path of `judge.sh`.
  - Optionally, never judge while a reviewer session is live: take `launch.lock` exclusively around the judge, or run all judging after the arm's reviewers have finished.

## Minor findings

### m-1. The "origin" count still disagrees between 2.10 and risk 13

- **Location:** 2.10 last row: "the designSpec candidate itself contains the word "origin" 7 times"; risk 13: "8 times as a substring (2 as a whole word)".
- **Evidence:** `grep -o origin` = 8 and `grep -oiw origin` = 2 on `EVAL/TASK-WF-designSpec-20261107-075614/candidate.md`.
- **Fix:** Change 2.10 to match risk 13.

### m-2. `uv run` without `--frozen` in 5.1

- **Location:** Section 1 says every Python file runs as "`uv run --frozen --project REPO`" ("so `REPO/uv.lock` is never rewritten"). 5.1 step 2.6 ("`uv run --project REPO python R4/lib/collab.py`") and step 6 (`results.py`) omit `--frozen`.
- **Why:** An implementer who copies the 5.1 commands can rewrite `uv.lock` and fail AC-02.
- **Fix:** Add `--frozen` to both commands.

### m-3. `run-panel.sh` interface omits `--block`

- **Location:** 1.2 lists `[--packages] [--seed] [--no-judge]`; 5.1 uses `--block b01` and says it feeds `runs/schedule.jsonl` and `baseline_drift`.
- **Fix:** Add `[--block <id>]` to 1.2.

### m-4. The SLO budget test vector uses a different denominator and baseline from the rule

- **Location:** `test_arm_summary.py`: "2 package-runs of 12 above 1.35 B_A1 ... SLO budget exceeded (2/12 above 1/12)". 2.9 rule: share of package-runs above 1.35 **B_c**. Open question 5: "3 of 36 at 12 runs".
- **Why:** With the file's "12 fixture F7 rows" (36 package-runs), 2 slow package-runs is 2/36 and does not exceed the budget. An implementer may change the rule's denominator to make the test pass.
- **Fix:** State that the fixture has 12 package-runs (4 rows), or use 4 of 36. Use B_c in the fixture text.

### m-5. `arm_summary.py` has no audit-violation check

- **Location:** 2.9 table. `REQ:970` (rule 5) requires "zero audit violations". 5.1 step 3 keeps a contaminated row "scored", with `audit_ok: false`.
- **Fix:** Add an `AUDIT` row: count rows with `audit_ok: false`; any such row fails rule 5. Say whether quarantined rows are excluded from the reach and no-loss tallies.

### m-6. Reviewers killed by the hang guard are not audited

- **Location:** 2.6 step 4 finds the transcript with "`find ~/.claude/projects -name "<session_id>.jsonl"`", and `session_id` comes "from the result object" (step 3). A process killed by `timeout` prints no result object.
- **Why:** For a hung reviewer, `source_md_opened`, timing and the ground-truth transcript scan are all missing, yet the audit reports clean.
- **Fix:** Take the session id from the hook input when collaboration is on. Otherwise find the newest transcript in the cwd's project directory created between `t_start_ms` and `t_end_ms` whose first user message equals the brief. Record `transcript_missing` and treat it as an audit gap, not as clean.

### m-7. `<rid>.md` is never defined

- **Location:** 2.6 steps 3 and 5. Step 3 writes `<rid>.attempt<n>.md` ("exactly as `RR:50-58`"). Step 5 uses `<rid>.md` and `normalize.py <rid>.md`.
- **Evidence:** In `RR`, `<rid>.md` is created at line 85 (`cp ... attempt$attempt.md ... $RID.md`), outside the cited range.
- **Fix:** Add "copy the last attempt's `.md` and `.meta.json` to `<rid>.md` and `<rid>.meta.json` (`RR:85`)".

### m-8. The `post_accepted` sha convention is not stated

- **Location:** 2.2 step 8 ("sha256 of the line") and 2.3 step 7 ("whose sha256 appears in a `post_accepted` event").
- **Why:** The writer appends `printf '%s\n'`. If one side hashes with the newline and the other without, no card is ever delivered. The tests would catch this, but the spec should not leave it open.
- **Fix:** Say "sha256 of the line's bytes without the trailing newline" for both sides.

### m-9. `/tmp/jdg.*` contradicts the isolation rule

- **Location:** Section 0, isolation rule: "Every file this design creates lives under `R4` or `SBR`". Decision 6 and 5.1 step 5 create `/tmp/jdg.XXXXXXXX`.
- **Fix:** List `/tmp/jdg.*` as the one temporary exception in the isolation rule.

### m-10. `allowed_models` includes `grok-4.7`

- **Location:** 1.1 `frozen/panels.json`: `"allowed_models":[..., "grok-4.7"]`. Decision 5 and AC-05 allow only ember, luna, haiku and sonnet.
- **Why:** The launcher would accept a grok reviewer, which AC-05 forbids.
- **Fix:** Remove `grok-4.7`.

### m-11. Turn grouping assumes no interleaved tool-result entries

- **Location:** 2.7, "the last entry before the group".
- **Why:** If the CLI writes a tool result between two entries of one `message.id` (tool execution while streaming), the turn duration includes tool time and T_report_p90 is overstated.
- **Fix:** Add this to the S0 check. If interleaving occurs, define the duration as the sum of the gaps ending at the group's own entries.

### m-12. Normal `/tmp` scratch use quarantines a row

- **Location:** 2.10: "any `/tmp` path other than its own sandbox" is a violation.
- **Why:** Models often write scratch files (`/tmp/check.txt`, `mktemp`). Each such row becomes `audit_ok: false`, and AC-12 fails, for behaviour that is not contamination.
- **Fix:** Classify writes to a new `/tmp` path as `tmp_write` (a sandbox-write finding). Keep reads of `/tmp/jdg.*`, `SBR/board` and other rows' paths as violations.

### m-13. "peer reviewer" in a luna claim drops F7 rows only

- **Location:** 5.1 step 4: the anonymiser exits 1 on `peer reviewer` and the package becomes `anon_failed`, so the row becomes `valid: false`.
- **Why:** Only F7 lunas see the finding-form template text "A peer reviewer flagged". Each echo removes an F7 row, so F7 rows are lost but A1 rows are not, which biases the reach comparison.
- **Fix:** Delete or neutralise the phrase (as for `card cN`) and count `anon_rewrites` per package. Keep the hard failure only for unforeseen residues, or report the anonymisation failure rate per arm.

## Verdict

- All six review-1 blocking findings are fixed (B-1 to B-6).
- Two new blocking findings:
  - N-1: the concurrency guard's `pgrep '^claude -p'` never matches on this host, and the S0 rule built on it would stop every F7 panel.
  - N-2: ground truth in `/tmp/jdg.*` is reachable to concurrent reviewers. The path-literal audit misses relative, `~` and ancestor-directory access, and the staging directory is not removed on judge failure paths.
- Thirteen minor findings (m-1 to m-13).
- The timing arithmetic, the deal and form vectors, the GT reach ids, the cited code lines and the cross-references all check out.

verdict: FAIL
