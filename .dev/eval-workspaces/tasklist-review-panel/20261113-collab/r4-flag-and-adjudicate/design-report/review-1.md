# Review 1 of DESIGN.md (Redesign 4, Flag-and-Adjudicate, F7)

## Scope checked

- `DESIGN.md` read in full (lines 1-557).
- Source of truth `merged-requirements.md` (called `REQ` below) read in pieces: lines 1-380 (sections 1, 2.0, 2.1), 700-800 (Redesign 4), 896-995 (sections 3 and 4), 996-1130 (section 5, all of 5.1-5.10).
- Code read: `EVAL/tools/run-reviewer.sh` (`RR`), `EVAL/tools/tmp-scripts/judge-one.sh`, `EVAL/tools/tmp-scripts/anon-b11.sh`, `EVAL/analysis/merge-b11.sh`, `EVAL/analysis/final-table.py:1-80`, `EVAL/combos/SPEC.md:95-152`, `src/superclaude/cli/review/merge_cmd.py`, `findings.py:1-200, 272-304`, `ledger.py:100-227`.
- Checked on disk: sha256 of `judge-one.sh`, `findings.py`, `ledger.py` (all three match AC-03); the three base sha values (all are git tree objects; none is the tree of any commit in this clone); `progress.md` header lines; `EVAL/arms/scoring/combos` exists; ground-truth keys (`jq '.items[0]|keys'` only: `blocking_in_implement, class, cost, description, evidence, id, plan_quote`); `## Task N:` headings (13 / 9 / 12); `b4-muse-ember-luna2` resolution ids (t2b-1 ember, t4-1 and t3-1 luna); structure of an existing `judge.json` (a JSON array with `user` tool-result messages; `grep -c plan_quote` = 1; content not read).
- Arithmetic recomputed in Python floats: k, PANEL_FINISH_AT, hang guard, planned ends, slowdown limits, k >= 1 thresholds, the R-42 / section 3 test vectors, and the three Fisher p-values.
  - Correct: k = 2 / 2 / 0 (EL2 / SL2 / HL2); PANEL_FINISH_AT - T0 = 143.8 / 341.5 / 275.3 s; finish bound 156.6 / 369.5 / 321.3 s; hang 174 / 410.6 / 357 s; planned ends 130.8 / 143.6, 303.7 / 331.7, 286 s; slowdown limits 5.7% / 16.7%, 8.7% / 18.9%, 5.2%; Fisher p = 0.047, 0.034, 0.045.
  - Wrong: one test vector (B-4).
- The seven required items, the model and path constraints, and requirements R-01..R-10, R-21..R-30, R-34..R-37 and R-41..R-47 were checked against the design.

## Blocking findings

### B-1. Judge staging puts complete ground-truth copies in the reviewers' shared sandbox root, and the audit does not watch that path

- **DESIGN.md location:** section 0, decision 6 ("steered outside `EVAL` ... into a random staging directory under `SBR/jdg/`"); section 1.5 (`jdg/<random>/<pkg>/<label>/  judge staging`); section 5.1 step 5.6 ("The staging directory is kept"); section 2.10, row "Reviewers never see ground truth" (audit patterns `ground-truth`, `EVAL`, `R4/runs`, `/.dev/reflect`, board).
- **Evidence:**
  - `judge-one.sh:25-27` writes `claude -p --output-format json` output to `$D/judge.json`. That output is the whole message array: an existing `EVAL/arms/scoring/combos/j1-sonnet-luna2-r1/TASK-WF-design-20261108-041415/U/judge.json` is an array of `assistant:6 result:1 system:3 user:4` messages, and the user tool results contain `plan_quote` (the judge's Read of `ground-truth.json`).
  - `score.json` also holds GT ids and notes (`judge-one.sh:21`).
  - Every reviewer runs with unrestricted Bash in `SBR/sb/<pkg>/repo` (`DESIGN.md` 1.5, risk 1). The design's own audit is the only control.
- **Why it matters:**
  - After the first judged row, `/tmp/evalsb-collab-r4/jdg/*/<pkg>/<L>/judge.json` holds the full ground truth, two directories above every later reviewer's cwd (and next to `SBR/cand`, which each brief names).
  - A reviewer of a later or concurrent row that runs `ls /tmp/evalsb-collab-r4` or `grep -r ... /tmp/evalsb-collab-r4` reads ground truth. None of the audit patterns matches (`jdg`, `judge.json`, `score.json`, the SBR root), so `audit_ok` stays true and AC-13 passes on a contaminated row.
  - This is a harness-created route to ground truth (check g).
- **Suggested fix:**
  - Stage the judge outside the sandbox root (for example `R4/jdg-stage/` or a separate `/tmp/evalsb-collab-r4-judge/`), never under `SBR`.
  - Move or delete the staging copy right after step 5.6. The kept copy lives in `runs/<row>/<pkg>/scoring/`.
  - Add the staging root, `judge.json` and `score.json` to the transcript audit patterns, and add the absolute `R4` path (not the literal `R4/runs`).

### B-2. A reviewer without a findings block breaks the whole package's merge

- **DESIGN.md location:**
  - 2.6 step 3: "a reviewer that fails both attempts is recorded invalid (`final_ok: false`) and the merge proceeds with the others".
  - 2.6 step 5: "If the last attempt has a findings block: `normalize.py <rid>.md <rid>.final.md ...`".
  - 2.6 end: "The merge input is `<rid>.final.md`".
  - 5.1 step 2.5: `--report <rid>=<pkgdir>/reviews/<rid>.final.md (x3)`.
- **Evidence:** `merge_cmd.py:84-98` reads every `--report` path through `_read`, and `merge_cmd.py:13-18` raises `ClickException("cannot read ...")` for a missing file. `<rid>.final.md` is only written when a block exists (2.6 step 5).
- **Why it matters:** One reviewer with no block, or one killed by the hang guard, makes `<rid>.final.md` absent. The merge then exits non-zero, the package becomes `merge_refused`, and it is not judged, so `valid: false`. That contradicts the stated "merge proceeds with the others". It also differs from `merge_round`, which keeps a panel with at least one valid block (`ledger.py:150-157`). No test covers the one-missing-block case; the fault table only has "three fake reports without blocks".
- **Suggested fix:** Always write `<rid>.final.md`. When there is no block, copy `<rid>.md`, or an empty report when the process was killed, so the parser marks it invalid and `merge_round` keeps the others. Alternatively, omit that reviewer's `--report` and record it. Add a fault test: one reviewer without a block, and the package still merges.

### B-3. A refused launch on an existing row overwrites that row's `run.json`

- **DESIGN.md location:** 5.1 step 0: "Exit 2 ... and write `runs/<row>/run.json` with `"status":"refused","reason":...` when: ... `runs/<row>/` already exists". `test_launcher.py`: "each refusal ... writes `run.json` with the reason", including "existing row".
- **Evidence:** 5.1 step 1 and step 7 store the row's panel, seed, values sha256, pins result and `"status":"done"` in that same `runs/<row>/run.json`, and 5.2 says `results.py` takes `schema`, `seed`, `values_sha256`, `pins_ok`, `started` and `finished` "from `run.json`".
- **Why it matters:** Re-running a command with an existing row id, which is exactly the case the refusal is for, destroys the scored row's metadata. A later `results.py` re-run then loses the seed and pins, and the row reads as refused. This is data loss, and the test plan enforces it.
- **Suggested fix:** For the "row exists" refusal, write nothing inside the existing row. Print to stderr, or append to a launcher-level `runs/refusals.jsonl`. Change the `test_launcher` expectation to "existing `run.json` byte-identical after the refused call".

### B-4. A `test_values.py` vector gives the wrong answer for the design's own k formula

- **DESIGN.md location:** 6.1 `test_values.py`: cases "`k_of(273.7, 14, 51.8)` and `51.9`" with expected "1 and 0".
- **Evidence:**
  - Formula at 2.7 and `REQ:285`: `(0.35 x 273.7 - 2 - 14 - 51.8) / 28 = 27.995 / 28 = 0.99982`, so the floor is 0, not 1.
  - The exact threshold is T_report_p90 <= 51.795 s. `REQ:293` and `REQ:1095` print it rounded as 51.8, and the design copies the rounded value into a strict floor test.
  - Recomputed in Python: `k_of(273.7,14,51.8) = 0`.
  - The other vectors are right: `k_of(100,6.4,13.8) = 1` (exactly 1.0 in float), `k_of(238,20.3,20.3) = 1`.
- **Why it matters:** A correct `values.py` fails AC-01, and an implementer who trusts the test will alter the formula, for example with a tolerance or rounding. The k formula is the design's main time guard.
- **Suggested fix:** Use 51.79 for "1" and 51.80 for "0". Alternatively, state the vector as "k = 1 for T_report_p90 <= 51.795". Also say that `finish_offset` and `hang_s` are compared with `pytest.approx` (`1.35*116-12.8` is `143.79999999999998` in float).

### B-5. The turn-duration definition misses the output time of multi-block messages, so T_report_p90 and k come out wrong

- **DESIGN.md location:** 2.7, row "turn_p90, T_report_p90": "A turn is one assistant message (entries grouped by `message.id` ...); its duration is the first entry's `timestamp` minus the `timestamp` of the entry before it. T_report is the last turn's duration."
- **Evidence:** `REQ:67` defines T_report_p90 as the duration of "the last turn, the one that writes the final report", and `REQ:295` stresses that it is luna's "output-heavy final turn". The design itself groups several entries under one `message.id`, which means the transcript writes one entry per content block, each stamped when that block completes.
- **Why it matters:** For a final message made of [thinking, text] or [text, tool_use], the first entry's timestamp marks the end of the first block. The time spent generating the long report text is excluded. T_report_p90, and to a lesser degree turn_p90, are then underestimated, k comes out too high, and PANEL_FINISH_AT too late. That is the bound REQ timing rule 2 relies on: "the planned end ... is at or under PANEL_FINISH_AT by construction". The implementer builds exactly this definition and gets wrong values without any error.
- **Suggested fix:** Define the duration as the **last** entry's timestamp of the message group minus the timestamp of the last entry before the group. Add a fixture with a two-block final message to `test_values.py`, and add a check to S0 that records whether the gateway models emit multi-block messages.

### B-6. The anonymiser leaves card references in reviewers' claims, so the judge can tell the F7 arm

- **DESIGN.md location:** 5.1 step 4: "`[panel card cN]`, `panel card cN` and `card cN: passed` are deleted"; 2.10 last row: forbidden-string grep for `"origin":`, `panel card`, `evalsb-collab`, `r4-flag`, `20261113-collab` and the ids; "The judge cannot tell the arm".
- **Evidence:**
  - `REQ:953` and R-29 (`REQ:1061`) require "origin keys and board references stripped ... so the judge cannot tell which arm a report came from".
  - The adjudicator brief (2.4) tells each luna to report a card's defect as a finding, and the delivered text begins "[panel card c<i>]". A luna claim such as "Card c1 asks for ...", "per card c0" or "a peer reviewer flagged this sentence" matches none of the deletion rules or forbidden strings.
  - Claims reach the judge: the merged report carries them (`ledger.py:199`).
- **Why it matters:** Only F7 reports can contain these phrases, so they unblind the judge for the treatment arm. Both the rule set and the post-check let them through, and `test_anon.py` does not test them.
- **Suggested fix:**
  - Delete or neutralise every case-insensitive `\bcard c[0-9]+\b` and `peer reviewer flagged`.
  - Add `\bcard c[0-9]+\b`, `panel card` and `\bpeer reviewer\b` to the forbidden grep, which fails the package as `anon_failed`.
  - Add a `test_anon.py` case with a claim that says "card c1".
  - Alternatively, tell the lunas in their brief never to mention the card id in a finding. The coverage line "card <id>: passed" is not merged.

## Minor findings

### M-1. The base sha values are tree objects, not commits; H3's wording is not met as stated

- **DESIGN.md location:** fact table line 32: "each package's `progress.md` starts with `T1: start sha=<tree>` ... `progress.md` line 2".
- **Evidence:**
  - `REPO/.dev/tasks/done/<pkg>/progress.md`: the `T1: start sha=` line is line 3; line 1 is the ledger header and line 2 the `PLAN:` line.
  - `git cat-file -t` gives `tree` for all three, and `git log --all --format='%H %T'` finds no commit with any of these trees.
  - `REQ:317` and R-03 (`REQ:1007`) ask for "the commit the plan was written against (the parent of its first implementing commit)" and "3 base SHAs".
- **Why it matters:** The line citation is wrong. The substitution of a working-tree snapshot for a commit is not declared as a deviation, and nothing confirms that the snapshot equals the parent of the first implementing commit.
- **Suggested fix:** Correct the citation to line 3. Add a deviation D-3 saying the base is the T1 start tree, a snapshot that is not a commit. Record in `manifest.json`, where it can be found, the parent commit of the first implementing commit and whether its tree differs.

### M-2. The "origin" count for the designSpec candidate is wrong

- **DESIGN.md location:** 2.10 and risk 13: "the designSpec candidate itself contains the word "origin" 7 times".
- **Evidence:** `grep -o origin` on `EVAL/TASK-WF-designSpec-20261107-075614/candidate.md` gives 8; `grep -oiw origin` gives 2.
- **Why it matters:** It is a factual claim the risk entry rests on. The conclusion, that a bare-word check fails, still holds.
- **Suggested fix:** Say "8 times as a substring, 2 as a whole word".

### M-3. `planning.json` has no `.sha256` file, so the launcher refuses Spike 4 and the smoke test

- **DESIGN.md location:** 1.4 (`values/planning.json` "Written by `values.py planning`", with no sha file listed); 5.1 step 0 (refuse when "the values file's sha256 differs from `<values>.sha256`"); 6.4 ("Before Spike 4 has run, the smoke uses `values/planning.json`", while the command shown passes `--values R4/values/EL2.json`).
- **Evidence:** `DESIGN.md` 1.4 rows for `values/<P>.json` versus `planning.json`; 6.3 Spike 4 row; 6.4 command.
- **Why it matters:** As written, Spike 4 and the pre-Spike-4 smoke are refused. The shape of `planning.json`, which covers three panels, also differs from the per-panel, per-package `values/<P>.json` the launcher reads, and neither shape is specified.
- **Suggested fix:** Have `values.py planning` write `values/planning-<P>.json` plus a `.sha256` in the same per-package shape as `values/<P>.json`. Fix the 6.4 command so it matches its text.

### M-4. `values/<P>.json` is described as written once and pinned, but it is also updated after the slowdown runs

- **DESIGN.md location:** 1.4: "Written once by `values.py build`, then pinned", and in the same row "after the slowdown runs `s` and `budget_fail`"; `values/<P>-srun.json` is "a copy of `values/<P>.json`".
- **Evidence:** `DESIGN.md` 1.4. R-30 (`REQ:1062`) requires the values file to be committed with its sha before the first arm.
- **Why it matters:** The pinning point is ambiguous. The sha in `collab.json` of an srun row will not match the final values file.
- **Suggested fix:** State the order: build, then srun copy, then slowdown, then write `s` and `budget_fail`, then pin once. Alternatively, keep `s` in a separate pinned `values/<P>-slowdown.json`.

### M-5. The flagger brief's `{MOVES}` placeholder is missing from the file table

- **DESIGN.md location:** 1.1 `frozen/brief-flagger.txt`: "Placeholders `{HELPER}`, `{CAP}`"; 2.4 uses `{MOVES}` as well.
- **Why it matters:** This is an internal inconsistency.
- **Suggested fix:** List `{MOVES}` in 1.1.

### M-6. `build-sandbox.sh` reads environment variables its interface does not list, and its test would overwrite the real manifest

- **DESIGN.md location:** 1.2 (`build-sandbox.sh` "Writes `R4/manifest.json`"; the column header says "no environment variable is read except where stated"); 6.1 `test_build_sandbox.py`: "build into a `tmp_path` `R4_SBR`".
- **Why it matters:** The interface does not list `R4_SBR` or `R4_OUT`, so the test cannot redirect the build. If it is redirected only partly, the test overwrites the real `R4/manifest.json`.
- **Suggested fix:** State that `build-sandbox.sh` honours `R4_SBR` and `R4_OUT`, the same as the launcher.

### M-7. The concurrency guard counts each session two or three times and races between launchers

- **DESIGN.md location:** 5.1 step 0: "`pgrep -fc 'claude -p'` is above 7 or, for EL2, `pgrep -fc 'muse-ember-1.0'` is above 3. Three panels launched together therefore stay at 9 reviewer sessions."
- **Evidence:** 2.6 step 2 launches `timeout --kill-after=5 "$TMO" claude -p --model "$MODEL" ...`. The `timeout` process's command line also contains `claude -p`, so each reviewer matches twice. `reviewer.sh <pkgdir> <rid> <model> ...` also contains `muse-ember-1.0`, so each ember reviewer matches three times. Judge sessions (`judge-one.sh:25`) also match.
- **Why it matters:** The stated "9 sessions" is wrong: effectively at most 2 panels run, and ember is capped near 1-2. Two launchers polling at the same moment can both start.
- **Suggested fix:** Count `pgrep -xc claude` (process name) or count the `reviewer.sh` processes. Take an `flock` around the check-and-start. Add a guard test.

### M-8. The re-ask block reuses a stale timeout and does not state its working directory

- **DESIGN.md location:** 2.6 step 6: `timeout --kill-after=5 "$TMO" claude -p --resume "$SID" ...`; the condition is `hang_ms - now >= 1 s`.
- **Why it matters:** `TMO` was computed before the attempts (step 2). Reused, it lets the re-ask run past T0 + 1.5 B_A1, which breaks R-43. `--resume` looks up the session under the cwd's project directory, so a re-ask run from `<pkgdir>` fails to find it.
- **Suggested fix:** Recompute `TMO` immediately before the re-ask, and state cwd `SBR/sb/<pkg>/repo`.

### M-9. `collab.json` field names differ from R-23

- **DESIGN.md location:** 2.8 slot field `form`; 2.8 end "`collab.json` carries every R-23 field ... so the same schema check applies to every arm".
- **Evidence:** R-23 (`REQ:1050`) names the per-slot fields `card_form`, `deal_r`, `deal_c` and `slot_type`. The design puts `deal_r` and `deal_c` at panel level and `slot_type` as a top-level null.
- **Why it matters:** A schema check written from R-23 fails.
- **Suggested fix:** Name the slot field `card_form`, and repeat `deal_r`, `deal_c` and `slot_type` (null) per slot.

### M-10. The forged-line fault test expects a result the hook does not produce

- **DESIGN.md location:** 6.2 "Forged board line": "not delivered (`from` is not the flagger, or no matching `post_accepted`)"; 2.1: "a line that did not come through the writer fails the audit instead".
- **Why it matters:** The hook (2.3 step 6) checks only `card.jq` and the 600-byte cap. A forged line with `from` set to the flagger id is therefore delivered. The expected outcome holds only for the `from`-mismatch variant.
- **Suggested fix:** Split the test into two cases. A forged line with a wrong `from` is not delivered; a forged line with a correct `from` is delivered but counted in `board_lines_invalid`. Alternatively, have the hook check the line's sha against `post_accepted`.

### M-11. The rendered-card audit cannot run, and contradicts open question 3

- **DESIGN.md location:** 5.1 step 3: "every harness-authored text (`frozen/*`, every rendered card and finish text in the board metrics) must contain no `plan_quote` substring"; open question 3: "rendered cards apart from the anchor".
- **Evidence:** The delivery event logs only `{"ev":"delivery","card":...,"form":...}` (2.3 step 9), not the rendered text.
- **Why it matters:** The audit has nothing to scan. The two passages also disagree on whether the anchor is in scope.
- **Suggested fix:** Log the rendered text minus the anchor, or re-render from the board in `audit.py`, and state the anchor exclusion in one place.

### M-12. The zero-overlap check reaches the unchangeable baseline brief and has no remedy if it fails

- **DESIGN.md location:** 5.1 step 3 and `test_pins.py` apply the zero-tolerance `plan_quote` check to all of `frozen/*`, including `brief-a1.txt`, which must stay byte-identical to `RR:13-17`.
- **Evidence:** R-07 (`REQ:1016`) applies the check to the catalogue, and rule 5 (`REQ:970`) to board messages.
- **Why it matters:** If an `RR` sentence shares 12 characters with a `plan_quote`, both arms fail the audit and the design says nothing about what happens next.
- **Suggested fix:** Limit the check to the moves, templates and role paragraphs, and record `brief-a1.txt` overlap as descriptive only.

### M-13. Some audit inputs are missing or too strict

- **DESIGN.md location:** 2.10 and 5.1 step 3.
- **Gaps:**
  - The audit does not scan for the absolute `REPO` path. `REPO/.dev/tasks/done/<pkg>/` holds the post-implementation package and is reachable by absolute path.
  - `git status --porcelain --ignored` flags any cache a reviewer's test run creates (`__pycache__`, `.pytest_cache`), and a sandbox shared by concurrently running rows gets another row's write blamed on it.
  - R-01's verification (source.md opened per transcript) is not computed anywhere.
- **Suggested fix:** Add the `REPO` prefix to the transcript patterns. Report ignored-only files separately from tracked or untracked changes, and record which rows overlapped in time. Add `source_md_opened` per reviewer.

### M-14. Gate and pre-registration items from section 5 are not covered

- **Evidence:**
  - R-27 (`REQ:1059`) requires Spike 5 before any arm runs; the design sets it aside without marking that as a deviation.
  - R-30 (`REQ:1062`) requires the analysis script (`arm_summary.py`) and the decision rule to be committed with sha256 before the first arm; `pins.sha256` covers only `frozen/*`, `judge-one.sh`, `findings.py` and `ledger.py`.
  - R-28 asks for a scheduler log of block order; R-45 asks for `baseline_drift` per randomised block; R-47 asks for measured act rates listed beside the planning factors. The design describes none of these as outputs.
- **Suggested fix:** Pin `lib/arm_summary.py`, `lib/results.py` and a decision-rule file. Add a block log and per-block drift to `arm_summary.py`, and an act-rate table fed from the REQ-S3 spike output. Mark Spike 5 as an explicit deviation.

### M-15. Smaller gaps an implementer would have to fill in

- The percentile method for p90 over 4 samples (nearest-rank or interpolation) is not given, yet `test_values.py` expects "hand-computed values".
- `finish_would_fire` uses "some reviewer" (2.8), while R-41 (`REQ:1094`) says "a luna".
- The SLO budget row in 2.9 does not say whether B_A1 means B_f or B_c (R-24 uses B_c after the fact).
- `grep -qF` needs `--` because anchors that start with "- " are common in acceptance criteria.
- `uv run --project REPO` may rewrite `REPO/uv.lock`; use `--frozen`, otherwise AC-02 can fail.
- R-26's "quarantined in place on contamination" step is not described.
- Subagent (Task) tool calls also fire PostToolUse. A card could be delivered into a subagent context of the `/sc:spec-panel` skill, and the call counter would include sidechain calls. This should be an S0 check or an open question.
- PostToolUse may not fire for a failed tool call (a refused `panel-post` exits 1), which would undercount `calls`. S0 should record this.

## Verdict

Six blocking findings:

- B-1: a ground-truth exposure route created by the judge staging.
- B-2: a merge that fails when one reviewer lacks a block.
- B-3: an existing row's `run.json` is overwritten.
- B-4: a wrong k test vector.
- B-5: a wrong turn-duration definition that skews k.
- B-6: an anonymiser gap that unblinds the judge.

Fifteen minor findings. The timing arithmetic otherwise checks out, as do the deal and form vectors, the Fisher p-values, the pins and the cited code facts. Every write path stays under `R4` or `SBR`, apart from Claude Code's own session transcripts under `~/.claude/projects`, which `REQ` requires, and the `uv.lock` risk in M-15.

verdict: FAIL
