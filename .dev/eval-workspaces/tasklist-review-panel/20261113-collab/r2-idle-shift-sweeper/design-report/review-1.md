# Review 1 of DESIGN.md (Redesign 2, Idle-Shift Sweeper)

Reviewer: independent (did not write the design). Date: 2026-11-14.
Document under review: `R2/DESIGN.md` (735 lines, read in full).
Source of truth: `MR` sections 2.0 (177-356), Redesign 2 (483-571), 4 (922-992), 5 (997-1101).
Paths below use the design's abbreviations (`REPO`, `EVAL`, `R2`, `MR`, `RR`, `SBR`).

Grading: blocking = wrong behaviour, false claim, missing required deliverable, security or data-loss risk; minor = wording, style, small gaps an implementer can close without guessing.

## Findings

### B-1 (blocking): the transcript contamination audit fires on clean runs, in every package

- Where: DESIGN.md 2.8 row "No ground truth or other outputs read" (line 387); 2.4 sweeper audit (line 262); AC-6 (line 666).
- Defect: the audit fails a package when a reviewer or sweeper transcript *contains* `ground-truth`, `20261113-collab`, `scoring`, `SBR/board` (and, for the sweeper, `runs/`, `scoring`). Clean runs produce these tokens:
  1. Claude Code writes every hook run into the persisted transcript as a `hook_success` entry that carries the hook `command` string. Checked in `~/.claude/projects/-home-coder-workspaces-worktrees-Coder-dashboard-bmad/a0e92241-....jsonl`: 143 PostToolUse entries each carry `"command":"..."`. The receiver hook command (DESIGN.md:300) contains `R2/bin/hooks/receiver-hook.sh` (a path with `20261113-collab`) and `--board SBR/board/...`. So every F4 receiver transcript fails, and A1 transcripts (no hooks) do not: an arm-asymmetric false violation on every collaboration package.
  2. The sweeper's brief necessarily contains `<POST>` = `SBR/board/<runid>/<pkg>/bin/panel-post` (DESIGN.md:265, 276), and its settings carry the `R2` hook path; 2.8 applies the `SBR/board` and `20261113-collab` tokens to "reviewer or sweeper" transcripts.
  3. Every reviewer runs `/sc:spec-panel` (`RR:13`); the expanded command text is recorded in the transcript (found in `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs/a1c4ed4e-....jsonl`), and `~/.claude/commands/sc/spec-panel.md:36` contains the word "scoring". Every package of both arms fails.
  4. The H3 sandbox trees contain the tokens in ordinary files: `git grep -l ground-truth 0b8a5801d^` (with the H4 directories excluded) lists 82 files and `git grep -l scoring 0b8a5801d^ -- src tests docs` lists 105. A reviewer grep that prints any of them fails the audit.
- Consequence: `audit_ok:false` on (almost) every package, the launch exits 1 (5.1 step 8), and AC-6 can never pass. MR 4 rule 5 (MR:970) asks only that no transcript *opens* `.dev/reflect/` or a ground-truth file.
- Fix: audit only `tool_use` inputs (Read `file_path`, Bash `command`, Grep/Glob `path`/`pattern`) of `assistant` entries, not the whole transcript; match on path patterns (`*/ground-truth.json`, `*/20261111-a1/*`, `*/20261113-collab/*`, `*/.dev/reflect/*`, `SBR/board/*` for receivers only); exclude `hook_success`/attachment entries and the sweeper's own `panel-post` calls. Add a test with a fixture transcript that has a hook entry with the R2 command and a Read of a sandbox file containing "scoring", which must pass.

### B-2 (blocking): the anonymiser self-check refuses legitimate reports that contain the word "origin"

- Where: DESIGN.md 5.2 step 4 (line 530); `test_anon.py` (line 598).
- Defect: the self-check is `grep -cE 'origin|...'`. Step 3 strips only the `"origin":"own"|"peer"` keys, so any other "origin" ("original", "origin/master") survives and the package is refused with exit 4. Evidence: `grep -c origin EVAL/TASK-WF-designSpec-20261107-075614/candidate.md` = 7, and 10 of the 300 existing `EVAL/combos/**/merged-1.md` files contain "origin".
- Consequence: a share of clean packages, mostly designSpec, is never judged and the launch exits 1 in both arms.
- Fix: check for `"origin"[[:space:]]*:` only (the key form), and add a test case where an anchor quoting "original" passes the self-check.

### B-3 (blocking): the H2 re-ask has no hang guard

- Where: DESIGN.md 2.2 "H2 after the final attempt", step 2 (line 197); 6.2 rows "A luna hangs" and "H2 re-ask" (lines 621, 623).
- Defect: the attempt command is wrapped in `timeout <remaining_s>` (line 188) and the sweeper in `timeout` (line 255), but the re-ask command `claude -p --resume <session_id> ...` has no `timeout`. The start check (`deadline - now >= 6 s + turn_p90`) does not bound the run. R-43 (MR:1096) requires every reviewer process still running at T0 + 1.5 B_A1 to be killed and logged `hang_kill`; R-02 counts re-ask time in `elapsed_s`.
- Consequence: a hung re-ask hangs the package and the launch without limit, in both arms. The fault-injection table tests a hang only in the main attempt.
- Fix: run the re-ask under `timeout <deadline - now>` (the same deadline), log `hang_kill` and `slo_breach` on exit 124, and add a 6.2 row "re-ask hangs" for both switches.

### B-4 (blocking): the harvest hook gets its own 2k cap, so the board can hold 4k facts against the source's 2k

- Where: DESIGN.md 2.3 rule 11 (line 243); 2.4 harvest step 6 (line 290); 6.1 `test_harvest_hook` ("the hv cap holds").
- Defect: MR (b) (MR:505-506): "the sweeper posts at most 2k facts ... sweeper: at most 2k sent", and R-18 (MR:1037) verifies it by "Board count". Harvested facts come from the sweeper's own session (MR:487, R-18). The design caps `sw-1` at 2k and `hv-1` at another 2k, so a package can hold 4k facts. Decision table 0.3 does not list this deviation.
- Consequence: the R-18 board-count check fails by design; each luna is dealt up to 2k facts instead of k, which changes which facts reach it (best-rank pick among 2k), and the flood alarm and `not_delivered_cap` are measured against a different cap than the source.
- Fix: one shared cap of 2k over `sw-1` and `hv-1` together, counted under the board lock; or record the change as a decision with its reason and change the R-18 verification. Add a test where 2k mixed posts fill the cap.

### B-5 (blocking): a resumed launch re-merges finished packages and marks them INVALID

- Where: DESIGN.md 5.1 step 0 (idempotent resume, line 503), steps 1, 3, 4 (lines 504-515).
- Defect: on resume, packages with `DONE` are skipped by `run-package.sh`, but step 3 still merges "per valid package" with `--round 1`. `DONE` is written before the merge (2.2 step 6), so after an interruption between merge and judge, `ledger.json` already exists and `ledger.merge_round` raises "round 1 cannot be merged: the ledger expects round 2" (`src/superclaude/cli/review/ledger.py:114-118`). The design marks a refused merge INVALID with no re-run. `merge-b11.sh:16` avoids this by skipping packages that already have `merged-1.md`. Step 1 also writes a new `runid`, and step 4 draws a new `opaque` per launch, so finished packages are anonymised and judged a second time under another key. That breaks R-29's "judged once" (MR:1061).
- Fix: make steps 3 to 5 idempotent per package: skip the merge when `merged-1.md` exists, keep `runid` and `opaque` from the first launch (write each once, read it on resume), and skip judging when `score.json` exists. Add a resume test.

### B-6 (blocking): acceptance criterion AC-2 can never pass

- Where: DESIGN.md 6.5 AC-2 (line 662).
- Defect: AC-2 requires `git status --porcelain -- src EVAL` to be empty after the tests and smoke runs. Today the command prints 3,041 lines for `EVAL` (untracked eval artifacts already present; the session's git status shows them too), before anything in this design runs.
- Fix: take a snapshot before the run (`git status --porcelain` plus a `find EVAL src -newer <stamp>` listing or a sha256 manifest) and require no difference after it.

### B-7 (blocking): the Gate 0 S3 smoke criteria drop the source's "0 dropped findings lines" requirement

- Where: DESIGN.md 6.3 S3 row (line 637) points to 6.4/6.5; AC-4 to AC-10 (lines 664-670).
- Defect: MR Gate 0 S3 (MR:933) requires the full-chain smoke "with 0 dropped findings lines", with stream-json parsed through `jq -s` and the `RR:50-52` filters. R-02's verification (MR:1006) is "S3 smoke shows 0 dropped lines". No acceptance criterion checks `dropped_lines == 0` or the re-ask stream parse.
- Consequence: Gate 0 can pass while H2 still drops lines, which is the T3b defect H2 exists to remove.
- Fix: add an AC: every smoke package has `dropped_lines == 0` in every reviewer meta, and, if a re-ask ran, its `.reask.jsonl` gave `model_ok:true` through `jq -s`.

### B-8 (blocking): the "wrong blockers rise" failure mode and alarm have no test

- Where: DESIGN.md 2.10 row "Wrong blockers" (line 430); 6.1 `test_summarize_arm` (line 596); 6.2 (lines 607-629).
- Defect: the owner asked for one fault-injection test per failure mode. MR (h) lists "Wrong blockers rise (luna grades every fact blocking) -> fail the arm" (MR:569). 6.2 has no row for it, and `test_summarize_arm` lists cases for CONVERGENCE, ECHO, SNAPSHOT, re-run mismatch, SLO budget and planning rows, but none for the wrong-blockers rule. The "Flood" alarm likewise has no `summarize_arm` case.
- Fix: add `test_summarize_arm` cases: wrong-blockers mean at A1 + 1.01 fails the arm, A1 + 1.0 does not; a flood fixture (posts at the cap, uptake below 0.5) is reported and does not stop the arm. Add a 6.2 row where fake luna marks every delivered fact blocking and the arm summary flags it.

### m-1 (minor): the seal is taken at call 6, not immediately before the first delivery

- Where: DESIGN.md 2.5.1 step 6 (line 312).
- Evidence: MR:232 says the hook writes the snapshot "immediately before the first delivery". The design seals at call 6 whether or not a fact is waiting, so when the first fact arrives at call 15 the snapshot misses calls 7-14 of the reviewer's own work. R-19 is still met. AC-4 ("seal_t earlier than first_delivery_t") passes either way.
- Fix: seal inside step 9, just before the first print, and keep fail-closed (no delivery if the seal fails).

### m-2 (minor): the judge's brief names the experiment directory

- Where: D-7 (line 49), 5.2 (lines 535-538).
- Evidence: `judge-one.sh:10,16` puts `$F = $D/merged-anon.md` into the judge brief, so the judge reads `.../combos/../../../../20261113-collab/r2-idle-shift-sweeper/scoring/<opaque>/...`. The self-check of 5.2 step 4 treats `20261113-collab` as a forbidden trace. Both arms of this design share the path, so F4 and A1 stay indistinguishable, but rows from this harness can be told apart from EVAL rows. D-7's path arithmetic itself is correct: `realpath -m EVAL/arms/scoring/combos/../../../../20261113-collab/r2-idle-shift-sweeper/scoring/X/P/L` resolves to `R2/scoring/X/P/L`, and `EVAL/arms/scoring/combos` exists.
- Fix: list this in section 7 as a residual blinding risk; do not compare these rows with EVAL rows as if the judge was blind to the harness.

### m-3 (minor): the row name can reach the judge through the merged report's `report <path>` lines

- Where: 5.1 step 3 (lines 509-511); 5.2 steps 2 and 4.
- Evidence: `ledger.py:423` writes `- <rid>: report <path>` with the path exactly as passed. 5.1 shows relative `runs/<row>/<pkg>/...` paths. The `anon-b11.sh:25` redaction only matches `report <EVAL>/...`, and the self-check does not look for the row name or the runid. With relative paths, a row name such as `smoke-el2-iso` survives.
- Fix: pass absolute paths in the merge, redact every `report \S+` token, and add the row name and runid to the self-check.

### m-4 (minor): the case k = 0 is not specified for the sweeper

- Where: 2.4, 2.7 (line 364).
- Evidence: the cap is 2k = 0, but the design does not say whether the sweeper is started (its brief would read "At most 0 facts").
- Fix: when k = 0, do not start the sweeper and log `sweeper_skipped_k0`.

### m-5 (minor): the concurrency rule is attributed to the source but the source does not state it

- Where: section 3 "Concurrency" (line 470).
- Evidence: MR:953 and R-28 (MR:1060) say "at most 10 concurrent runs and at most 4 ember". The source does not state "at most 2 launches". It follows from the ember cap only for EL2 (2 ember per launch); SL2 and HL2 run 1 ember per launch.
- Fix: present it as this design's derived rule, or allow up to 4 SL2 or HL2 launches.

### m-6 (minor): two test assertions do not match the interfaces

- Where: `test_launch_command_diff.py` (line 601).
- Evidence: `grep -c FALLBACK run-reviewer2.sh` also counts `NOFALLBACK` if the launcher copy guards on it. The test sets `PANEL_COLLAB=0`, but 4 (line 488) says children never read the environment; `run-reviewer2.sh` switches only on `--settings`.
- Fix: grep for `FALLBACK\[` or `fallback.log`, and drive the test with or without `--settings`.

### m-7 (minor): Spike 4's "hang guard off" has no interface

- Where: 2.7 (line 366); 6.3 Spike 4 row.
- Evidence: `launch-panel.sh` has no switch to turn the hang guard off, and `run-package.sh` needs `--values`, a file that Spike 4 is meant to produce.
- Fix: define a `spike4` values file (`hang_s` = 3000, `k` = 0) and say that `spike4-values.sh` passes it.

### m-8 (minor): re-judging after an API error needs the anonymiser to run again

- Where: 5.3 (line 542).
- Evidence: `merged-anon.md` sits in the old label directory, which the operator moves. A fresh label has no input, so `judge-one.sh` would fail at `$F`.
- Fix: the procedure is to move the label directory, run `anon.sh` again (new label), then run `judge.sh`.

### m-9 (minor): the harvest filter ignores files that ember opened on EL2

- Where: 2.5.1 step 3; D-3.
- Evidence: MR:487 harvests paths "that no reviewer has opened". Only receivers are hooked (D-3), so `opened.txt` never holds ember's reads.
- Fix: state this as a consequence of D-3, or fill `opened.txt` from ember's transcript once ember exits.

### m-10 (minor): the tagger can mark retry-isolated attempt-2 lines as `peer`

- Where: 2.6; 2.2 retry row.
- Evidence: tags are computed against "facts delivered to that reviewer", which includes facts delivered in attempt 1, but the final report comes from the fresh attempt 2, which never saw them.
- Fix: when the final report is from attempt 2, tag every line `own` and list the receiver in `isolated_for`.

### m-11 (minor): some facts are counted in no category, and the harvest move signatures overlap

- Where: 2.5.4 (lines 338-339); 2.4 harvest step 3 (line 287).
- Evidence: a fact that is dealt, arrives in time, and is not delivered because a better-ranked fact took the call (k not reached, no later call) is neither `late` nor `not_delivered_cap`. `grep -rl x tests/` matches both M1 and M2, and no precedence is given.
- Fix: add a `not_delivered_other` counter, and state the order of precedence (M1, then M2, then M7).

## Checks performed

- Read DESIGN.md in full, and MR 2.0 (lines 170-369), Redesign 2 (480-574) and sections 4-5 (918-1107).
- Read `RR` in full: the line ranges cited for the brief (13-17), the command (48), extraction (50-58), the retry loop (61-64), the fallback ladder (66-83) and the final copy (85-87) are all correct.
- Read `judge-one.sh`, `anon-b11.sh`, `merge-b11.sh` and `final-table.py:1-40` in full. `merge-b11.sh:11-12, 17-25, 34` and `anon-b11.sh:24-25` are cited correctly. The defect-rich and real-blocking definitions match `final-table.py:4-5, 33-36`. The ground truth gives 10 + 4 items (14), of which 5 + 3 are `blocking_in_implement` (8), and the control package has 2.
- `findings.py`: `_check_finding` 90-121, `parse_block` 124-196, `flat` 272-273 and `locate` 276-304 are correct. Unknown keys such as `origin` are ignored. `merge_cmd.command` 71-118 and `ledger.merge_round` 107-157 (refuses only when no reviewer has a valid block) are correct.
- D-7 path computed by hand and with `realpath -m`: it resolves under `R2/scoring/`, and `EVAL/arms/scoring/combos` exists. The claim is correct.
- H3 squash commits `0b8a5801d`, `4eb75698d` and `54e21668f` are the first commits of each package folder, and their parents exist. All three `source.md` files and `resolution-live7.json` files exist.
- Planning arithmetic recomputed, all correct: 143.8, 131.0, 174, 156.6; k = 2 (25.8/12.8); SL2 341.5 / 328.7 / 369.5 / 410.6; HL2 275.3 / 262.5 / 321.3 / 357; planned luna ends 130.8, 143.6 and 129.6; +12.8% and +23.8%; literal R-42 on HL2 gives k = 0; +45% tokens (MR:905).
- Constraints: models allowlist, Opus as judge only, NOFALLBACK=1 with no fallback ladder, reviewers read-only, no writes into `src/` or `EVAL` by design (the judge output is redirected to R2), UV for Python. No violation found apart from the findings above.
- Owner items (1)-(7) are each present. The gaps are listed above.

verdict: FAIL
