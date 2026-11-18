# Synthesis Accuracy Report 1 (partition A, synthesis-accuracy lens)

**Files reviewed:** synthesis/synth-01-problem-current-state.md, synth-02-overlap-matrix.md, synth-03-target-gaps.md, synth-04-external-findings.md
**Compared against:** research/01-24, web-01 to web-04, gaps-and-questions.md
**Lens:** synthesis accuracy (criteria 1-5), Deep tier
**Grading:** grading-override.md (owner decision A) applied; severity label is information only
**Date:** 2026-11-14
**Status:** Complete (verdict PASS; 0 blocking under the grading override; 10 minor notes)

---

## 0. Method and limits

- Read completely: synth-01 (748 lines), synth-02 (283), synth-03 (405), synth-04 (606). Read the research files each section draws on (R01, R02, R04 to R18 by targeted extraction; web-01 and web-02 in full; web-03 and web-04 by section and by figure; `gaps-and-questions.md` header and row table).
- Verification channels (all read-only): `grep`/`sed` over the research files; `sed -n` against the working tree at HEAD `50d4d2b9d` (confirmed by `git rev-parse`); `git show`, `git ls-tree`, `git log` against the E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`; `wc`/`sed` over the installed E3i files under `~/.claude`. No file under the task folder other than this report was written. Nothing under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `REVIEW-PANEL-UNIFY-RUN2-QUEUED.md` was read.
- Grading: `qa/grading-override.md` applied. Severity label (CRITICAL / IMPORTANT / MINOR) is information only. A finding that the old definition would call blocking but the override makes minor carries the text `(minor under grading override)` in its Finding cell.
- Limit 1: the rule "C8" that synth-03 uses for its Critical rubric and Section 4.2 is defined in the task file, which this item may not read beyond line 338. The rule's wording could not be checked; the way synth-03 applies it (named as shipped, not wired, no on-record deferral) is consistent with the research files it cites. Not graded.
- Limit 2: `[UNVERIFIED]` items that the synthesis labels as such were not re-opened; they were checked only for being labelled and listed (carry-over blocks 2.9.8, 4.6B, and the "Not verified" paragraphs).

## 1. Findings

Columns: # | Severity (information only) | Blocking Y/N | File and location | Finding | Evidence | Proposed fix.

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| SA-01 | IMPORTANT | N | synth-01 line 78 (2.1 table row "Diversity evidence"); line 156 ("Contradictions between research files ... None remain open inside R04, R06, R07 and R15") | (minor under grading override) The table states that engine A computes its diversity fields "from SERVED worker `model_id` values". That is R06 s2.5 / s8(d) and is wrong: `WorkerResult.model_id` is the requested id. The same file says so at lines 522, 532 and 540 ("all three use requested values"), synth-02 RC-1 and synth-03 X-2 correct it, and line 156 then says no R04/R06 contradiction remains open although X-2 is exactly that contradiction. Downstream use: synth-05 lines 567, 594 and 606 repeat the served-id claim as a pro of "engine A only" and a con of "absorb A into B". The recommended composition (Option 4) does not depend on it: the other four lost-capability items in R06 s8(d) (fail-closed exit map, atomic write-back, headless transport, bounded ladder) stand without it, and synth-07 asks for a new served-model record from the transcript. So no decision, number or destination changes. | `src/superclaude/cli/swarm/transports/openai_compat.py:467-470` (`model_id=self._model`; `model_label=self._model`), `:384-388` (the response `model` field is not read); `src/superclaude/cli/reflect/_diversity.py:8-15` (distinct `worker.model_id`); R04 s3.3 and s4.1 (negative Grep); R06 line 287 and line 331 (the claim); synth-01 lines 522, 532, 540; synth-02 RC-1 (line 170); synth-03 X-2 (line 300). | Change the table cell to "from the REQUESTED `model_id` (`openai_compat.py:467-470`); vocabulary `full` / `insufficient`", add the R04-over-R06 side to the contradictions paragraph at line 156, and carry the correction to synth-05 lines 567, 594, 606 (outside this partition). |
| SA-02 | IMPORTANT | N | synth-03 G-01 (line 105), G-99 (line 203), SC-01 (line 47); synth-02 CF-03 (line 113) | (minor under grading override) The mechanism is stated as "a v2 citation-only finding raises `KeyError: 'anchor'` in `findings.annotate`, which `ledger.merge_round` calls". `merge_round` parses each report with the v1 `parse_block`, which already requires `anchor` (12..200), so a citation-only line is rejected at parse time and never reaches `annotate`; the KeyError arises only when a v2-validated finding is passed to `annotate` directly. synth-01 line 442 carries this Gate 1 refinement; G-01, G-99, SC-01 and CF-03 were not updated. The conclusion (a citation-only finding cannot enter the v1 ledger path; location type is a core blocker) is unchanged, so no decision or destination depends on the mechanism wording. SC-01's pass condition ("passes `merge_round` and enters the ledger without KeyError") is still a valid test. | `src/superclaude/cli/review/ledger.py:128-136` (`fnd.parse_block(rv["text"])` then `fnd.annotate(f, doc_text)`), `src/superclaude/cli/review/findings.py:104` (`_check_flat(obj.get("anchor"), "anchor", 12, 200)`), `:349` (`finding["anchor"]`); synth-01 line 442. | Reword G-01, G-99 and CF-03: "a v2 citation-only line fails the v1 parse (anchor required) so it is dropped from the ledger path; `annotate` raises KeyError when called on it directly". |
| SA-03 | IMPORTANT | N | synth-01 line 692; synth-03 SC-32 (line 78), G-146 (line 250), G-147 (line 251) | (minor under grading override) The "148 lines in 56 files" baseline of `src/superclaude` references is stated for "installed primitives" and SC-32 compares `grep -rn 'src/superclaude'` against it. R18 line 138 measured it over `**/*.md` only. The unqualified `grep -rn` over the same six directories at HEAD returns 168 lines in 70 files (168 lines in 66 text files with `-I`); with `--include='*.md'` it returns exactly 148 lines in 56 files. A gate run as SC-32 words it would fail on day one. The number is a baseline for a later check, not an input to the recommendation. | Commands run at HEAD: `grep -rn --include='*.md' 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks,templates}` gives 148 / 56 files; without `--include` gives 168 / 70; R18 line 138 (`**/*.md`) and line 147 (recommends the unqualified grep). | State the baseline as "148 lines in 56 `*.md` files" in synth-01, G-146 and SC-32, or restate SC-32 with `--include='*.md'`. |
| SA-04 | MINOR | N | synth-03 G-40 (line 144) | (minor under grading override) "E2 audit C had to infer source-blind runs (161 of 665, slice-sourced)". The figure is 156 of 665 in synth-01 line 206 and in R08; R05 carries both numbers (line 168 says 161, line 179 says 156, both slice-sourced). The correct figure is discoverable in the sibling file. | R05 lines 168 and 179; R08 ("156"); synth-01 line 206. | Replace 161 by 156. |
| SA-05 | MINOR | N | synth-03 SC-23 (line 69) | (minor under grading override) "the 13 pilot EV-1 failures by class (R06 s6.1-6.2)". 13 is the number of pilot runs counted; the EV-1 failures are 8 (3 unparseable contract, 4 `merged-verdict` absent, 1 empty `reviewer-cards/`), as G-47 and synth-01 lines 107 and 118-122 say. | R06 line 13 (`EV-1 ... shadow 8/13`), line 132 ("5 of 13 pilot EV-1 failures ... and 3 are ..."). | Write "the 8 EV-1 failures among the 13 counted pilot runs". |
| SA-06 | MINOR | N | synth-04 lines 27, 61, 93 and line 23 | (minor under grading override) The handed-in codebase fact "7 multi-reviewer clusters among 216 findings" is repeated three times as `[UNVERIFIED]`, and line 23 says no web file conflicts with a code-verified fact. synth-01 line 139 (from R07 E1-F10) records 216 clusters, 13 with two or more reviewers and 7 of those unchained. The label "findings" in the handed-in text is a unit error against the code-verified figure. No external conclusion depends on it. | R07 lines 50 and 124 ("7 unchained multi-reviewer clusters of 216"); synth-01 line 139; web-01 lines 10, 70, 105. | State "13 of 216 clusters had two or more reviewers (7 unchained)" once in 5.1 and drop the repeated unit. |
| SA-07 | MINOR | N | synth-02 row 15 (line 67) against Table B (lines 90-93) and Table C | (minor under grading override) Row 15 is classed `unique-E2`, but the same row and Table B count E1 and E3 (E3i phase-5 bundle) as having their own harness mechanisms (E3 cell is not in the ABSENT list for row 15). By the stated definition ("only that effort has the mechanism") the capability is not unique; what is unique is ground truth plus the blind judge, which rests on `[UNVERIFIED]` statement OQ-06 (already flagged in 2.9.0, Table C and 2.9.8). The destination of the harness items is set in the value inventory, not by this label. | synth-02 lines 33, 67, 91-93, 203; R01 line 207. | Class the row as "unique per effort (E1 gate scripts, E2 ground truth and judge, E3i bundle)" or keep `unique-E2` and name "ground truth and blind judge" in the Classification cell. |
| SA-08 | MINOR | N | synth-01 lines 412 and 415 (embedded 15-row matrix, rows 1 and 4) | (minor under grading override) The compact matrix copies R01's labels "superset of E3s" for E1 schema and for E1 clustering. synth-02 (RC-2, CF-13, PS-1, PS-2) corrects the clustering label (v2 clusters citation-located findings only; anchor-only findings stay singletons) and calls the schema superset partial. The synth-01 row is attributed to R01 and the correction is discoverable in synth-02. | synth-02 lines 47, 148-149, 171; R01 section 3 takeaway. | Mark the two cells "superset on fields only (partial, see 2.9.6)" or drop the compact matrix in favour of 2.9. |
| SA-09 | MINOR | N | synth-03 4.6C and 4.4/4.5; synth-01 to synth-04 generally | (minor under grading override) Two research items are not surfaced in the Gap Analysis or carry-over: (a) the two `[CODE-CONTRADICTED]` stale-documentation items of R02 (the `findings_v2.py:15-22` line anchor is the import block; the function is `check_finding`, not `_check_finding`) appear only in synth-01 line 479, and 4.6C lists no R02 or R05 cluster; (b) R18 key takeaway 4 of section 3 (an umbrella `ironbelly/review-panel` would not collide with the E2 branch `ironbelly/eval-tasklist-review-panel`, whereas `ironbelly/eval-tasklist-review-panel/<x>` would) is in none of the four files and is not listed in 4.5 as excluded. K-8 states the general rule and synth-01 line 717 names the one existing ref, so the fact is derivable. | R02 "Stale Documentation Found" (lines under that heading); R18 line 113 (key takeaways); synth-03 lines 346, 353, 403-405. | Add one stale-doc row for R02 (and R05's `manifest.md:3-6` item) to 4.6C and one sentence to K-8 or 4.5. |
| SA-10 | MINOR | N | synth-01 line 575 | (minor under grading override) "`/sc:auggie-review` (402 lines)": 402 is the size of `skills/sc-auggie-review-protocol/SKILL.md`; the command file `commands/auggie-review.md` has 178 lines. Wording only. | `wc -l` at HEAD (402 and 178); R13 line 83. | Write "skill 402 lines". |

Blocking findings under the override: 0. All ten findings are notes for the follow-up list. None is fixed in the gate.

## 2. Claim traces (criterion 3 and 4: at least 20 claims per file traced to a research file or to code)

Result codes: OK = matches the source exactly; OK (arith) = also recomputed; FINDING = see section 1.

### 2.1 synth-01 (46 claims traced)

| # | Claim in synth-01 (line) | Traced to | Result |
|---|---|---|---|
| 1 | #519 = `d2d8a2d166c945f556d921b31530a3673f00df89`, 2026-11-12 14:47:10 -0500; 17 RV files (4 modified, 13 added); 22 `tests/review` files (44) | `git log`, `git show --name-status` | OK |
| 2 | #518 = `167184c6ba44...`; 0 RV files, 1 test file `tests/review/test_review_panel_live7.py` (45) | `git show --name-only 167184c6b` | OK |
| 3 | E2 tip commits and times `c2ddeb1b4` 16:17:36, `fd69a006d` 20:25:07, `d561461fa` 04:37:57, `6c0984326` 04:38:11; run-1 commit `4a22d7421` (173) | `git log -1 --format=%ci` | OK |
| 4 | RV layout: 25 tracked files, 16 modules, 5,086 lines with per-file counts; 19 test files (385) | `wc -l`, `git ls-files` | OK (arith: the 16 counts sum to 5,086) |
| 5 | `lint_cmd` and `estimate_cmd` registered, modules absent (385, 126) | `__init__.py:24-25`; file list of the directory | OK |
| 6 | Only cross import between `cli/review` and `cli/reflect` is a test (`test_shadow_skill_contract.py:14`) (47) | `sed -n 14p`; `grep -rn` both directions | OK |
| 7 | Stage 2 exit: 13 of 20; EV-1 8/13 = 0.615 vs 3/39 = 0.077; parity 6/13; lint 9/13; mean 0.704; 352 passed, 1 xpassed (104-114) | R06 line 13 (executed output) | OK |
| 8 | Failure classes: 7 of 28 leaked keys (2 pilot + 5 combo); 6 of 28 recorded parity true / recomputed false (116-124) | R06 lines 250-251 | OK |
| 9 | `reflect_shadow_exit.py:313` `(s_rate or 0.0) > (l_rate or 0.0)`; `:59` card regex; `panel_lint.py:188` card regex (122, 126) | `sed -n` at HEAD | OK |
| 10 | Convergence `>=0.75 PASS, >=0.60 PARTIAL` at `SKILL.md:703`; degrade below 0.80 at `contract.py:321`; incident comment `:309-311`; single-vendor `SKILL.md:839` vs `contract.py:287-288` (89-91) | `sed -n` at HEAD | OK |
| 11 | `ensemble.py:773` count-derived `merge_method`; `:74` version "1.0"; `:817` `citations_dropped: 0`; `runner.py:538-545`, `:480-481`, `:457`; `config.py:318-319`; `commands.py:236-239` (72-96) | `sed -n` at HEAD | OK |
| 12 | 36 tests in `test_verdict_mapping.py` (83) | `grep -c 'def test_'` = 36 | OK |
| 13 | Diversity from SERVED `model_id` (78) | `openai_compat.py:467-470` | FINDING SA-01 |
| 14 | E1 cost: 4,119,747 output tokens, 489.2 min, USD 478.40; orchestrator share median 0.588, range 0.385-0.867 (133-134) | R07 lines 15, 31, 33 | OK |
| 15 | Calibrator without class in 6 of 15 combo runs (A3 3/3, B3 4/4, C1 1/4, C2 1/4, E1 4/4, E2 4/4) (136) | R07 E1-F5 | OK |
| 16 | Zero resolved citations in 7 of 15 combo and 4 of 13 pilot runs; AI label check TP 21 / FP 4 / FN 1 / TN 24; 479/712 vs 495/781 (138-142) | R07 E1-F9, F15, s1 | OK (arith: 21/25 = 0.84, 21/22 = 0.9545) |
| 17 | E2 harness: `run-reviewer.sh` 87 lines, `$MODEL` overwrite at `:76`, `BLOCK_OK` `:57`; `fullpkg()` `final-table.py:15-18`, `BAD_CHECKS` `:20`; `judge-one.sh:4` absolute path (181-189, 217) | `git show 6c0984326:...` | OK |
| 18 | Collaboration packages: 107 / 321 / 130 / 70 / 274 tracked files, 0 `/lib/` paths; `.gitignore:13` is `lib/`, `:79` is `*.log` (266) | `git ls-tree -r --name-only` | OK |
| 19 | `combos/`: 97 entries (96 dirs + `SPEC.md`), 19 `RESULT.md`, 0 `judge.json` / `attempt*.json` tracked (197-198, 215) | `git ls-tree` | OK |
| 20 | Study figures: 306 catches; I7 + I8 = 92; 214 defect-rich; B3 + I2 + B7 = 194 (91%); 71 valid-era rows, distribution 0:3 1:9 2:43 3:12 4:4; 131 of 147 (89%) (201-203) | R08 tables | OK (arith: all sums recomputed) |
| 21 | Merge drops 92 = 56 + 18 + 14 + 3 + 1; 49 blocking = 24 + 14 + 10 + 1; per-model 30+33+14+7+7+1 = 92; 3 flips named (205, 225-226) | R08 lines 70-82 | OK (arith) |
| 22 | Sonnet + 2x luna vs ember + 2x luna: 2.33 / 0.33 / 1.83 / 1.33, 139,113 tokens, 821 s vs 1.83 / 0.17 / 1.83 / 0.83, 63,644, 348 s (208) | R08 lines 60, 97-98 | OK |
| 23 | E3i: scripts 2,668 / 2,050 / 1,740 / 1,131 lines (7,589), `finding-grader.md` 35 lines; `SCHEMA = 1`, `CAP_REVIEWS = 3` (ledger and diffgate); zero `superclaude` references (329-343) | `wc -l`, `grep` under `~/.claude` | OK (arith) |
| 24 | `stoprule.py` `cmd_verify_transcript` returns `EXIT_OK` after printing `mismatch`; `fix_audit.py:877` vs `898-903`; `headline_raw = U3 + W + O` at ledger `SKILL.md:117`; `diffgate.py:796`; `stoprule.py:1189` (341-345) | `sed -n` under `~/.claude` | OK |
| 25 | Tier file 38 lines; `review-tiers.default.json:7-9` tier2 / tier2b / tier3 lists contain `glm-5.3` and `Qwen3.8-max`; `ccsession-models.json` 181 lines; `MODEL-TIERS.md` 227 lines (491, 507-508) | `wc -l`, `sed -n` | OK |
| 26 | `openai_compat.py:384-388` single user message; `:467-470` `model_id=self._model`; `reflect-reviewer.md:5-8, 28` (273, 522) | `sed -n` at HEAD | OK |
| 27 | `panel.py:72-73` `_REFLECT_LAUNCH`, max 3; `:80`, `:137`, `:46`, `:492` `T3Model01`, `:600` `apply_to`; `panel_cmd.py:124` (49, 136, 458) | `sed -n` at HEAD | OK |
| 28 | pr-submit: 6,511 lines; `DEFAULT_MAX_ROUNDS = 2`, `HARD_CAP_MAX_ROUNDS = 5` at `fsm.py:32-33` and `loop_guard.py:19-20`; `is_groundable` `fsm.py:364-372` (574) | `wc -l`, `sed -n` | OK |
| 29 | `rf-qa.md` 551, `rf-qa-qualitative.md` 1154, `rf-analyst.md` 428 lines; `sc-workflow-protocol/SKILL.md` 107; plugins 125 tracked files (564, 576, 596) | `wc -l`, `git ls-files` | OK |
| 30 | `/sc:auggie-review` (402 lines) (575) | `wc -l` | FINDING SA-10 (wording) |
| 31 | `.gitignore:114` `.superclaude/`; `Makefile:549` "6 of 10 checks"; `cli/main.py:568-570` (146, 385, 719) | `sed -n` | OK |
| 32 | 148 lines in 56 files baseline (692) | `grep` with and without `--include='*.md'` | FINDING SA-03 |
| 33 | Defect register: 171 rows (170 distinct); reproduction 64 / 46 / 2 / 59 / 0; buckets sum to 171 (30, 477) | R17 lines 504, 515; arith 75+29+2+2+14+36+2+11 | OK (arith) |
| 34 | Coverage sidecars: 13 files, 2 of 13 with empty `observed`, 11 of 13 with a repeated row; precheck 1,047 / 510 / 472 / 7 / 31; card states 77 / 10 (295) | R10 lines 193 and unit 10 | OK (arith: 510/1047 = 48.7%, 472/510 = 92.5%, 10/87 = 11.5%) |
| 35 | `gaps-and-questions.md`: 555 rows; 243 / 187 / 67 / 58 by tag (32) | recomputed from the Tag column of the table | OK |
| 36 | Plugin `spec-panel.md` differs by 18 changed lines; hard gate extended, not softened (323, 368) | R12 lines 31, 217 | OK |
| 37 | Memory file: 14 tracked `deviation-patterns-*.md`, live file untracked, 100 lines (146) | R15 s6 (not re-read in tree) | OK (as cited) |
| 38 | Phase-5 numbers: 57,763 bytes start; endpoints 63,717 / 70,488 / 70,565; growth 10.31% / 22.03% / 22.16% (360) | R14 lines (hits for 10.31, 22.03, 22.16) | OK |
| 39 | `live7` pooled p = 0.013, second batch 0.168 / recomputed 0.167 over 924 splits (364) | R14 (hits 0.013, 0.168, 0.167, 924) | OK |
| 40 | Install-log base hash `4115f2a97980...` (486-line master) vs PR 427 text `c8d80346a96cb528` (333, 371) | R14 (hits) | OK |
| 41 | Brief defects B-1..B-7, twelve hard-codings, `theory.py` HARD set (462) | R05 unit 7 and unit 5 | OK |
| 42 | D-1, D-2, D-11, D-13 behaviours and the test pins `test_review_ledger.py:193-217, 376-385` (450-460) | R03 s1-s2; `ledger.py:254-258`, `:150-157`, `:363` | OK |
| 43 | `ledger.py:122-134` single warning per reviewer (227) | R02 s5; code read | OK |
| 44 | Severity vocabularies and "Medium" uses; `card_convert.py:81-82` `MINOR_WORDS` includes medium, important, should-fix (582-594) | `sed -n 81,82p card_convert.py`; R12 s2-s3 | OK |
| 45 | `E1 and E2 are one evidence family`: sha256 `044809e3...`; `PLAN.md:96-105` (219) | R16 part 6 (hits 044809e3, a865f397) | OK |
| 46 | Ground truth: 3 packages, 16 items, `ground-truth.json` sha256 values (189) | R16 line 90; `git ls-tree` lists 3 package files plus one r1 test fixture | OK |

### 2.2 synth-02 (34 claims traced)

| # | Claim in synth-02 | Traced to | Result |
|---|---|---|---|
| 1 | The 16 capability rows are the 16 named in the assignment, in order | `research/research-notes.md` line 165 | OK |
| 2 | Table A: 11 conflicting + 1 identical + 0 + 2 + 2 + 0 = 16; row lists match the Classification column | recount of rows 1-16 | OK (arith) |
| 3 | Table B: ABSENT 2 (E1: rows 8, 16) + 6 (E2: 5, 6, 7, 8, 12, 14) + 4 (E3: 10, 12, 14, 16) = 12; 14 + 7 + 12 = 33 own; 3 reuse; 48 cells; 8 rows with and 8 without an ABSENT cell | recount | OK (arith) |
| 4 | Table C: 13 + 3 = 16 | recount | OK (arith) |
| 5 | Row 1: `findings_v2.py:155-162` (blocking forced equal), `:96-97` (`calibrated_confidence`), `findings.py:100-101` | `sed -n` at HEAD | OK |
| 6 | Row 3: v1 fingerprint 16 hex (`findings.py:340-343`); `$MODEL` overwrite; `model.observed` `telemetry.py:49`; `model_observed` only in the view (`:364`) | `sed -n`, `git show` | OK |
| 7 | Row 4: `ensemble.py:773`; legal `merge_method` values `panel_lint.py:184` | `sed -n` | OK |
| 8 | Row 5: `SPAN_TOLERANCE = 3` (`cluster.py:72`), literal 3 at `findings.py:377`, `cluster_agreement` 1.0 rule (`cluster.py:50`), primary citation (`:133-134`) | `sed -n`, `grep` | OK |
| 9 | Row 6: `verify_cmd.py:25` `review-precheck/1`; `ensemble.py:817` | `sed -n` | OK |
| 10 | Row 7: `contract.py:321`; `SKILL.md:703`; 36 tests; `ledger_cmd.py:13` exit map PASS 0 / REVISE 10 / ESCALATE 11; tasklist `:1640, 1646`; `commands.py:181-183`; `return-contract.md:16-21` | `sed -n` | OK |
| 11 | Row 8: `ledger.py:17-19`, `:37-38`; `review_ledger.py:34-35`; `diffgate.py:23`; `fsm.py:32-33`, `loop_guard.py:19-20`; `spec-panel.md:261`; `pragmatic.md:228`; tasklist `:1604` | `sed -n` | OK |
| 12 | Row 9: `panel.py:72, 73, 80, 137, 492`; `panel_cmd.py:124`; tier file lines 7-9; six `reflect-*` templates; `@default` = 4 reviewers | `sed -n`, `ls`, template slots | OK |
| 13 | Row 10: `reflect-reviewer.md:5` tools and `model: sonnet`; `ensemble.py:276` per-model transport; `fallback.py:40, 411`; `openai_compat.py:384-388` | `sed -n` | OK |
| 14 | Row 11: `test_shadow_skill_contract.py:146` three sections; prompts `:62, :70`; `spec-panel.md:258-262` | `sed -n` | OK |
| 15 | Row 13: contract 1.0 with 32 keys, 10 outside, 89 of 110 absent; `panel_lint.py:184-185, 188`; `reviewer_briefs_materialized` at `refs/reviewer-spec.md:51, 57, 78` | R06; `sed -n`; `grep -n` | OK |
| 16 | Row 15: 352 passed / 1 xpassed; 96 directories and 19 `RESULT.md` under `combos/`; py counts r1 27, r2 28, r3 31, r4 17, r5 14 | R06; `git ls-tree` | OK |
| 17 | Row 15 class `unique-E2` | row 15 cells and Table B | FINDING SA-07 |
| 18 | Row 16: 0 `/lib/` paths for r2-r5 (and r1); `.gitignore:13`; claimed vs static test counts; +59% / +55% from 281.567 / 176.9175 and 46,018 / 29,655; `reflect-reviewer.md:28`; `merged-requirements.md:917` quote | `git ls-tree`; R09 line 78; `git show` | OK (arith: 1.59, 1.55) |
| 19 | CF-02 / CF-03: blocking forced equal; KeyError mechanism | `findings_v2.py:155-162`; `ledger.py:128-136` | OK for CF-02; FINDING SA-02 for CF-03 |
| 20 | CF-06: `SKILL.md:703` vs `contract.py:321`; tasklist post gate 0.80 | `sed -n` | OK |
| 21 | CF-07: tier lists still contain both excluded models | `review-tiers.default.json:7-9` | OK |
| 22 | CF-14: `contract_version` 1.0 (`ensemble.py:74, 788`) vs 1.8.0; single vendor `contract.py:287-288` vs `SKILL.md:839`; lint rule B `panel_lint.py:360-365` | `sed -n` | OK |
| 23 | CF-17: `card_convert.py:81-82` maps medium, important, should-fix to MINOR; PR categories `severity_router.py:34-` | `sed -n` | OK |
| 24 | CF-19 / DU-3: pr-submit cap pair defined twice | `fsm.py:32-33`, `loop_guard.py:19-20` | OK |
| 25 | RC-1: R04 over R06 on served vs requested id; `_build_result` stamps `model_id=self._model` | `openai_compat.py:467-470`; R04; R06 line 287 | OK (and confirms SA-01) |
| 26 | RC-3: plugin diff 18 changed lines, not 25 | R12 lines 31, 217 | OK |
| 27 | RC-4: R04 gap 5 is `[UNVERIFIED]`; R06 s4.2 0 matches in `swarm/` | R04 lines 65, 213; R06 line 150 | OK |
| 28 | CC-1: #519 17 RV + 22 test files; #518 0 RV + 1 test file | `git show` | OK |
| 29 | CC-3: `T2bModel01` 18 lines in 11 files; `panel.py:492` reads `T3Model01` only | R04; `sed -n` | OK |
| 30 | CC-4: `observed` in 1 of 15 combo contracts, `requested-pinned` in 14 and in 13 of 13 pilot | R04 s4.2 | OK |
| 31 | CC-8: pilot "no contract" is an unparseable YAML at line 103 | R06 line 359 | OK |
| 32 | OQ-01 to OQ-18: 18 rows, each tied to an `[UNVERIFIED]` cell; E3i sizes and constants re-measured | row count; `wc -l` under `~/.claude` | OK |
| 33 | Key Takeaways: 21 conflicts (CF-01..21), 11 corrections (CC-1..11), 5 contradictions (RC-1..5), 18 open items | recount of ids | OK (arith) |
| 34 | 2.9.9 coverage of the six research files' Summary and Key Takeaway items, each placed or excluded with a reason | sampled R01, R04, R06, R09, R11, R12 takeaways against 2.9.9 rows | OK (see SA-07 only) |

### 2.3 synth-03 (40 claims traced)

| # | Claim in synth-03 | Traced to | Result |
|---|---|---|---|
| 1 | 148 gaps G-01..G-148; 24 Critical, 93 Important, 31 Minor (4.1) | Severity column of lines 105-252, recounted | OK (arith) |
| 2 | The 24 Critical ids in the 4.1 table equal the 24 Critical rows | recount | OK |
| 3 | T-1 / G-147: 16 modules, 5,086 lines, 25 tracked files, `__init__.py:14-36` | `wc -l`, `git ls-files` | OK |
| 4 | G-01 mechanism (KeyError via `merge_round`) | `ledger.py:128-136`, `findings.py:104` | FINDING SA-02 |
| 5 | G-04 fingerprints (`findings.py:340-343`; v2 `cluster.py:119-123`) | `sed -n` | OK |
| 6 | G-12 `ledger.py:254-258`; G-13 `:150-157`; G-15 `:363`; G-35 docstrings `ledger.py:112`, `:351` | `sed -n` | OK |
| 7 | G-17 `contract.py:310, 321`; `SKILL.md:703` | `sed -n` | OK |
| 8 | G-22 / G-137: `findings_v2.py:25, 40, 190`; `manifest.py:176, 402`; `__init__.py:24-25` | `sed -n` | OK |
| 9 | G-23: `telemetry.py:49, 112, 364`; `telemetry_cmd.py:67` | `sed -n` | OK |
| 10 | G-24 / G-26 / G-32: `panel.py:19`; `panel_cmd.py:124`; `panel.py:492` | `sed -n` | OK |
| 11 | G-42 / G-44 / G-45: `ensemble.py:773`; `runner.py:538-545, 480-481`; `config.py:318-319`; `SKILL.md:839`; `contract.py:287-288` | `sed -n` | OK |
| 12 | G-46: `reviewer_briefs_materialized` at `refs/reviewer-spec.md:51, 57, 78` | `grep -n` | OK |
| 13 | G-47: 8/13, 6/13, 9/13, 0.704; 51 of 59 dirs use `-card` | R06 lines 13, 306 | OK |
| 14 | G-48 / G-128: `reflect_shadow_exit.py:313`, `:59`; `panel_lint.py:188` | `sed -n` | OK |
| 15 | G-51: `commands.py:236-239` default True; `runner.py:457` comment | `sed -n` | OK |
| 16 | G-55 / G-77: 7 of 15 and 4 of 13; 373 / 360; 1,047 = 275 + 772, 510 = 110 + 400 | R07 line 49; R10 | OK (arith) |
| 17 | G-56: calibrator class loss per run | R07 E1-F5 | OK |
| 18 | G-57: `cluster_agreement` 1.0 in A2, B1, B3, C3; others 0.143-0.540 | R07 line 50 | OK |
| 19 | G-61: 320/3423 vs 472/4464; 93,616 / 367,381 | R07 lines 27, 42 | OK |
| 20 | G-63: 131 of 147 = 89%; 156-source-blind figures | R08 | OK |
| 21 | G-64: 111 / 109 net vs 92 = 17-19; three named flips | R08 lines 79, 82 | OK |
| 22 | G-40: "161 of 665" | R05 lines 168 vs 179; R08 | FINDING SA-04 |
| 23 | G-70: `lib/` absent for r2-r4 (and r1, r5), claimed vs static test counts, +59% / +55% | `git ls-tree`; R09 | OK |
| 24 | G-76: 13 sidecars, 39 reviewer entries, 0-9 rows, 11 of 13, 2 of 13 | R10 line 193 | OK |
| 25 | G-86: Stage 10.5 `:1640` "non-blocking" and `:1646` "advisory-blocking"; patch loop `:1604` | `sed -n` | OK |
| 26 | G-90 / G-92: `fsm.py:32-33`, `loop_guard.py:19-20`, `pragmatic.md:228` | `sed -n` | OK |
| 27 | G-95 / G-100: `severity_router.py:34`; `is_groundable` `fsm.py:364-372` | `sed -n` | OK |
| 28 | G-102: `reflect-reviewer.md` `permissionMode: plan`, no Write or Bash | `sed -n 5,8p` | OK |
| 29 | G-108: 17 installed files, 7,589 script lines, install-log hash match | `wc -l`; R14 | OK |
| 30 | G-109: `cmd_verify_transcript` `EXIT_OK`; `diffgate.py` `cmd_fixcheck` | `stoprule.py:1790-1816` | OK |
| 31 | G-112 / G-113: plan files and `SNAPSHOT-STATE.txt:3` | R14 (as cited) | OK |
| 32 | G-114..G-122: seven run-record shapes; `manifest.py:348-354`, `:371`, `:53`; `model_scores` fan-out 400 vs 200; memory file facts | R15 lines 70, 80; `sed -n` | OK |
| 33 | G-125 / G-126 / G-127: `judge-one.sh:4`; `final-table.py:15-18, 20`; `run-reviewer.sh:57`; 1,300 flag rows, 257 EXCLUDE | `git show`; R16 | OK |
| 34 | G-132..G-139: parser fragility, union-find chain, `merge_cmd.py:94`, `ledger.py:144` | `sed -n`; R17 | OK |
| 35 | G-142: 25 lines in `sc-reflect-protocol` mention `src/superclaude` | `grep -rn` = 25 | OK |
| 36 | G-146 / SC-32: 148-line baseline | `grep` | FINDING SA-03 |
| 37 | SC-23: "13 pilot EV-1 failures" | R06 line 13 | FINDING SA-05 |
| 38 | K-1 / K-2 / SC-16 / SC-17: 110 and 27 names, 36 tests, 19 fields | `panel_lint.py:33-174` (as cited), `grep -c` = 36 | OK |
| 39 | 4.3 X-2 (served vs requested) resolved for R04 | `openai_compat.py:467-470` | OK |
| 40 | 4.6A decision ids D-1..D-14 and 4.6B U-1..U-18, 4.6C 15 stale clusters | count; each cluster row is a "Stale documentation" row | OK (see SA-09 for two missing items) |

### 2.4 synth-04 (68 external findings; 52 claims and figures traced)

All 68 findings carry `[EXTERNAL]`, Finding, Source, Relevance and Relationship fields (counts: 68 / 68 / 68 / 68 / 68 by `grep -c`; 21 in 5.1, 14 in 5.2, 17 in 5.3, 16 in 5.4).

| # | Claim in synth-04 | Traced to | Result |
|---|---|---|---|
| 1 | A1: position-bias, name bias (Claude-v1), 65.0%, 91.3% / 8.7%, ~10% / ~25% self-enhancement, ">80%" | web-01 A1 | OK |
| 2 | A2, A3 (4.8% vs 2.6%, 97% steering), A4 (12 biases) | web-01 A2-A4 | OK |
| 3 | B1 PoLL: kappa 0.763 / 0.627 / 0.749 / 0.734 / 0.726; Pearson 0.917; 7x cost; limits | web-01 B1 | OK |
| 4 | B2: 350 LLMs, 60% agree when both wrong | web-01 B2 | OK |
| 5 | B3: ~2 effective votes, 8-22 points, phi 0.437 / 0.389 / 0.603, n_eff 1.93, 11% gap, 9.1% | web-01 B3 | OK |
| 6 | C1, C2 (5 agents 60% to 68%, 15 to 79%) | web-01 C1-C2 | OK |
| 7 | D1: 1,000 PRs, ~90% agreement, +43.67%, 21.91% / 30.44% / +118.83%, 36 / 27 overlaps | web-01 D1 | OK |
| 8 | D2: 219 PRs, 187 repos, 19 languages, 96.6%; D3: 59-task, ~30%, 2-of-3 arbiter; D4: 20.1-32.1%, 97 of 234 = 41.5%; D5 | web-01 D2-D5 | OK |
| 9 | AE-1: 541,000 judgments, 33-41 points, 14 positions, 0.95 / 0.10 / 0.011, alpha 0.33 / 0.63 / 0.79 | web-01 AE-1 | OK |
| 10 | AE-2: 70.5% to 77.3%, 14% swap effect | web-01 AE-2 | OK |
| 11 | G1: ~8% flagged, 31 of 32, 97%, 92% passing, 10-50 lines; G2: 10.3%, 20 findings, 16 agreed, 9 real, 7 not (~44%) | web-01 G1-G2 | OK |
| 12 | F1: 15 models, 82 MySQL prompts, Youden's J ~0.52; F2; F3: 26.8%, +12 F1, 8-16% | web-01 F1-F3 | OK |
| 13 | Relevance labels for all 21 web-01 findings (A1 H, A2 H, A3 M, A4 M, B1-B3 H, C1 H, C2 L, D1 H, D2-D4 M, D5 L, AE-1 H, AE-2 M, F1 H, F2 L, F3 M, G1 H, G2 L) | web-01 "Relevance" lines | OK (21 of 21) |
| 14 | Relationship labels (supports / extends / contradicts) match web-01 "Supports / extends / contradicts" (B3 contradicts in part; AE-2 extends and partly contradicts) | web-01 | OK |
| 15 | web-02 s1-s10: PostToolUse success-only, `--bare` drops hooks even via `--settings`, `capabilities` array, 10MB, 2 MiB, `--restricted` v2.1.248, v2.1.193, v2.1.126, `kimi-k3-claude-compatible` | web-02 | OK |
| 16 | Issues 79702 (2026-07-21, v2.1.216), 10373, 37559, 9630, 18311, 22724, 55182 with the stated readings and relevance (H, H, H, M, M) | web-02 s8 | OK |
| 17 | `SubagentStop` fields `last_assistant_message`, `agent_transcript_path`; hooks run inside subagents with `agent_id` / `agent_type` | web-02 s9 | OK |
| 18 | web-03 (17 findings): relevance labels A1 H, B1 H, B2 H, B3 M, B4 M, B5 L, C1 H, D1 H, D2 M, E1 H, E2 L, F1 H, F2 M, F3 M, F4 L, G1 H, G2 M | web-03 relevance lines | OK (17 of 17) |
| 19 | web-03 facts: GA 2026-10-06, same-repo limit, error text, Git 2.39.3, `gh stack` Git 2.36+, Graphite $20 / $40, Ivan Tse / Steinhardt commit, discussion 201439 (Nov 4, 2026), SO 79292495 | web-03 | OK |
| 20 | web-04 (16 findings): relevance labels 1.1 H, 1.2 H, 1.3 M, 1.4 M, 2.1 H, 3.1 H, 3.2 M, 4.1 H, 4.2 H, 4.3 M, 4.4 L, 4.5 H, 5.1-5.4 M | web-04 relevance lines | OK (16 of 16) |
| 21 | web-04 facts: `security-severity` bands 0.1-3.9 / 7.0-8.9, `primaryLocationLineHash` `39fa2ee980eb94b0:1`, `X-GitHub-Api-Version: 2026-03-10`, Codex issue 27691, Greptile 66.2% vs Copilot 56.5%, `PRRT_` ids, `gersmann` action | web-04 | OK |
| 22 | 5.5 coverage table: 9 + 9 (web-01), 9 + 7 (web-02), 8 + 6 (web-03), 7 + 7 (web-04) key findings and recommendations all mapped; none excluded except the web-02 probe text | web-01 lines 215-236; web-02 lines 129-149; web-03, web-04 sections | OK |
| 23 | Precedence statements: codebase facts handed in are not re-verified; web-03 defers to item 2.18; no web file records a code conflict | web-01 line 209; web-02 line 149; web-03 line 2 | OK |
| 24 | "7 multi-reviewer clusters among 216 findings" (27, 61, 93) | R07 lines 50, 124 | FINDING SA-06 |
| 25 | No roadmap, plan or risk register (532, 603) | scan of the file | OK |

## 3. Checklist results (criteria 1 to 5)

| # | Criterion | synth-01 | synth-02 | synth-03 | synth-04 | Evidence |
|---|---|---|---|---|---|---|
| 1 | Section headers match the expected format | PASS (`## 1`, `## 2`, `### 2.1`-`2.8`) | PASS (`## 2.9`, `2.9.0`-`2.9.10`) | PASS (`## Section 3`, `3.1`-`3.5`; `## Section 4`, `4.1`-`4.6`) | PASS (`## 5`, `5.1`-`5.5`) | header listing |
| 2 | Table column structure | PASS (tables carry their own stated columns) | PASS (`# / Capability / E1 / E2 / E3 / Classification / Evidence tag / Notes`) | PASS (`Gap / Current State / Target State / Severity / Notes`; 148 rows, one Severity value each) | PASS (68 blocks with Finding / Source / Relevance / Relationship) | recount |
| 3 | No fabricated content (20+ claims per file traced) | PASS with notes SA-01, SA-03, SA-08, SA-10 | PASS with notes SA-02, SA-07 | PASS with notes SA-02, SA-03, SA-04, SA-05 | PASS with note SA-06 | section 2 |
| 4 | Findings cite real paths and evidence | PASS (every cited path and line that was opened matched, about 120 code cites checked) | PASS | PASS | PASS (every finding carries a URL and a reliability tier) | section 2 |
| 5 | Options with at least two options and pros and cons | not applicable (current state) | not applicable | not applicable (X-9 is a two-sided contradiction, carried to Section 9, not an options analysis) | not applicable (5.1.7 lists rules with effect and evidence; options analysis is synth-05) | scope of each file |

## 4. Gate focus

| Focus | Result |
|---|---|
| Synthesis claims trace to research evidence; no fabrication | PASS. 172 claims traced across the four files; 0 fabricated; 10 notes in section 1. |
| No doc-only claim presented as current | PASS. Every table carries tags; the three tag classes are defined at the head of synth-01 and synth-03; `[UNVERIFIED]` cells are flagged in place (synth-02 uses a dagger on all 16 rows and lists 18 items in 2.9.8). |
| Every `[CODE-CONTRADICTED]` and stale-documentation finding of the research is surfaced in the Gap Analysis or listed for Open Questions | PASS with note SA-09: 15 stale-doc clusters in 4.6C plus the "Corrections" paragraphs in synth-01 and Table E2 (CC-1..CC-11) in synth-02; two R02 items and one R18 takeaway are not carried into 4.6C. |
| Report-only scope (no roadmap, branch plan, PR plan or risk register) | PASS. Scan found no such content; synth-03 states the limit at line 14 and K-8; synth-04 states it at line 532. |
| Every research Key Takeaway is reflected or explicitly excluded with the reason | PASS with note SA-09(b). synth-02 2.9.9 and synth-03 4.4 / 4.5 and synth-01's closing note list inclusions and exclusions per research file; one R18 takeaway is missing. |
| `[PENDING-ADJUDICATION: <slug>]` allowed in synth-07 only | PASS. The marker does not occur in the four assigned files. |
| No synthesis file modified | PASS. This agent wrote only this report; no Edit or Write targeted a reviewed file. |

## 5. Summary

- Files reviewed: 4 (synth-01, synth-02, synth-03, synth-04). Claims traced: 172 (46 + 34 + 40 + 52). Code and git citations re-opened: about 120.
- Findings: 10 (SA-01 to SA-10). Blocking under the grading override: 0. Minor (notes for the follow-up list): 10, each marked `(minor under grading override)`.
- Information labels: IMPORTANT 3 (SA-01, SA-02, SA-03), MINOR 7.
- Most useful follow-up: SA-01 (one wrong table cell in synth-01 that synth-05 repeats three times); SA-03 (restate the 148-line baseline as markdown-only).
- Not graded: the wording of the task rule "C8" (task file outside this item's read range).

**Verdict: PASS** (zero blocking findings under `qa/grading-override.md`).

Status: Complete
