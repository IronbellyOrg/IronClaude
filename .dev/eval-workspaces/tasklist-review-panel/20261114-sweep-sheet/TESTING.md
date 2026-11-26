# Testing: Redesign 1, Sweep Sheet

Status: design only. No test exists yet and nothing here was run. This file maps every requirement of `MR` sections 6.1, 6.3, 6.5, 6.6, 6.7 and 6.8 to a runnable test or to a labelled manual check, lists the fixtures, and gives the validation-experiment commands. `DESIGN.md` has the behaviour; `IMPLEMENTATION.md` has the build order.

Path names are those of `DESIGN.md`: `REPO`, `SW`, `MR`, `RR`, `JJ`, `FND`, `LED`, `MRG`, `SB`, `EVAL`.

## 1. Conventions

### 1.1 Kinds of check

| Label | Kind | Needs a model | When it can run |
|---|---|---|---|
| **U** | unit test in `SW/tests/`, pure Python, no process other than `git` | no | any time after the code exists |
| **I** | integration test: the real launcher scripts with a fake `claude` on `PATH` (`tests/fakes/claude`) and the real `superclaude review merge` | no | any time after step 11 of `IMPLEMENTATION.md` |
| **F** | freeze-time test (pytest marker `freeze`): needs hand-made fixtures that only a second author can write (REQ-21) or the real ground truth (the lint). It fails, never skips, when its fixtures are missing | no | at the freeze (step 14) |
| **X** | experiment-time check: a script run over real run folders after model runs. Each X check also has a **U** twin on synthetic run folders, so the check itself is tested before it is trusted | the data comes from model runs | during and after the experiment |
| **M** | manual check with a named person, a record file and a pass rule | no | named per row |

A requirement is "covered" only when every part of its Test column in `MR` is covered by at least one runnable check; M rows say which part cannot be automated and why.

### 1.2 Commands

```
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"

PYTHONDONTWRITEBYTECODE=1 $T $SW/tests -q -m "not slow and not freeze"     # everything that needs no models and no hand-made fixtures
PYTHONDONTWRITEBYTECODE=1 $T $SW/tests -q -m slow                          # timing tests on the largest tree
PYTHONDONTWRITEBYTECODE=1 $T $SW/tests -q -m freeze                        # REQ-21 recall, real-ground-truth lint
PYTHONDONTWRITEBYTECODE=1 $T $SW/tests/test_prepass.py -q                  # one file
uv run --frozen --project $REPO ruff check $SW && uv run --frozen --project $REPO ruff format --check $SW
```

This is the same pytest form that the collaboration designs used (`r3-axis-flip-challenge/IMPLEMENTATION.md`, line 73). The repository's own suite stays the guard for the code this design imports: `uv run pytest tests/review -q` must pass before and after (`IMPLEMENTATION.md` step 0).

### 1.3 Rules for every test

- Tests write only under a pytest `tmp_path` or `/tmp`; the path override variables (`SW_SB_ROOT`, `SW_SRC_REPO`) are refused unless they point under `/tmp/` (the precedent's rule), so a test can never write into `REPO`; `SW_KILL_S` is accepted only as a number from 0.1 to 15 (so `1` passes and `9999` is refused) and `SW_PREPASS_CMD` only when its first word is `sleep` or `false` (the stubs of the kill test).
- No test starts a real model, a judge or a network call. The fake `claude` is a script on `PATH`; the suite fails if the first `claude` on `PATH` is not the fake (`test_fake_on_path.py`).
- Timing tests use a fake clock where the requirement is about arithmetic, and a real sleeping stub only where the requirement is about killing a process (REQ-18, REQ-30).
- Every fixture is invented. No fixture contains text, names, paths or numbers from a study package or from a ground-truth file. The AO-1 lint runs over `fixtures/` (`test_lint.py::test_fixtures_clean`).

## 2. Fixtures

All fixtures are built by code where a static copy would be large. Static files are short.

| Id | Location | What it is | Used by |
|---|---|---|---|
| F-PLAN-1 | `fixtures/plans/p_basic.md` | an invented plan (a report exporter and a retention policy, 5 tasks) in the `workflow-plan` format with a front matter, `Source:`, `Goal:`, `## Constraints`, `## Phase`, `## Task N:`, `Acceptance criteria:` and `Source sections:` citations. It carries at least one mechanical trigger for every extractor E1 to E7 (a criterion with an unbounded set word beside a narrower instruction scope; a universal sentence next to a skip rule; a command whose literal pattern misses the heading the task orders; an edited file that an unnamed test refers to; a count claim that another document repeats; a cited source rule whose identifiers the task lacks; a read-only value; a constraint clause the dictated text omits) | E1 to E7 unit tests, select, assign, render |
| F-PLAN-2 | `fixtures/plans/p_clean.md` | an invented plan with every criterion bounded and no trigger shape | no-trigger run, REQ-23, false-positive checks |
| F-PLAN-3 | `fixtures/plans/gen_setwords.py` | a generator for a plan with N set-word sentences (N = 200 for REQ-19) spread over criteria of 12 tasks, with a mix of completeness and universal words | REQ-19 |
| F-REPO | `fixtures/repos/build_repo.py` | builds a small git repository in `tmp_path`: `tests/` (with a test that names the edited file's stem), `scripts/`, `docs/` (with a heading and a count claim), root files, `CHANGELOG.md`, a mirror copy of a plan-named file, `.dev/` noise that repeats every search string, `node_modules/` noise, an "implementation" commit that adds a file and edits another, and a trap file named `ground-truth.json`. Returns the base and head commits | sandbox, E2 to E4 `attach`, scope, REQ-03, REQ-04, REQ-24, REQ-34 |
| F-SPEC | `fixtures/specs/spec1.md`, `parent1.md` | an invented specification with `shall` lines, an example block, an "Affects" list, and its parent requirement document | REQ-37 |
| F-DOC | `fixtures/docs/doc1.md` | an invented how-to with a universal claim, a fenced command and a count | REQ-37 |
| F-REPORT | `fixtures/reports/*.md` | reviewer final messages, one per case: `good`, `ledger_missing`, `ledger_after_findings`, `ledger_twice`, `ledger_unclosed`, `findings_unclosed`, `findings_twice`, `bad_json_line`, `anchor_250`, `claim_301`, `quote_wraps_line`, `unknown_item`, `dup_line`, `ok_but_finding`, `unsure_with_blocking`, `blocking_no_cb3`, `blocking_with_cb3_near_id`, `problem_no_finding`, `promote_long_id`, `promote_short_anchor`, `promote_dup_id`, `verdict_lowercase` | REQ-02, REQ-13 to REQ-16 and the design's check rules |
| F-TRANSCRIPT | `fixtures/reports/*.attempt1.json` | minimal run transcripts in the shape of a real `claude -p --output-format json` run (`system`, `assistant` with `message.model`, `user` with a `tool_result` block, `result` with `result`, `usage`, `modelUsage`), one per report that needs the `transcript` corpus | DD-2 tests |
| F-GT | `fixtures/gt/synthetic-gt.json` | invented ground truth (items with `id`, `class`, `blocking_in_implement`, `description`, `plan_quote`) for `F-PLAN-1`, so G0, stages and the lint have something to read without any study data | REQ-07, REQ-22, REQ-35, REQ-41 |
| F-RUNS | `fixtures/runs/make_runs.py` | builds synthetic run folders for 3 arms x 2 documents x 5 replicates with known found sets, timings, flags and scores, and writes `expected.json` by hand-written arithmetic (not by calling `analyze.py`) | REQ-29, REQ-39 to REQ-43 |
| F-FAKE | `tests/fakes/claude` | a script that reads the brief on stdin, picks a scenario from `FAKE_SCENARIO`, and prints the JSON array of a real run: `ok` (valid ledger and findings), `ledger_missing`, `long_anchor`, `api_error`, `wrong_model`, `sleep` (sleeps `FAKE_SLEEP_S`), `bad_block`, `exit127`; it appends one line per call to `FAKE_CALL_LOG` | I tests |
| F-RECALL | `fixtures/recall/<plan-id>/` | at least 3 real plans from the repository that are not a study package, not a hold-out document and not a planted-set plan, each with a copy in which a second author seeded defects of classes C1, C2, C4, C5, C6, C7, C8 and a `seeds.json` of exact quotes; plus `AUTHORS.md` (who seeded, that they had not read the extractors) | REQ-21 (marker `freeze`) |

F-RECALL cannot be written by the author of the extractors (AO-4). Until it exists the `freeze` tests fail with the message "fixtures/recall missing"; they are never skipped, so the freeze script cannot pass without them.

## 3. Requirement map

Test names are `file::function` under `SW/tests/`. "Passes when" is the observable rule.

### 3.1 Harness and brief (MR 6.1)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-01 | The brief names the source only when a source file exists; otherwise `no_source` is logged and C2 is not applicable | U | `test_briefs.py::test_cb1_rendered_with_source`; `::test_cb1_absent_without_source`; `test_e5.py::test_no_source_returns_nothing` | F-PLAN-1 with and without a source | the Z0 brief contains the CB-1 text with the absolute source path only in the first case; `run.json` has `no_source: true` in the second; E5 returns no candidate and `prepass.json` marks C2 not applicable |
| REQ-02 | The merge input truncates `anchor` and `anchor2` to 200 and `claim` to 300 characters (a prefix of an exact quote) and is validated with the real parser | U | `test_normalise.py::test_anchor_250_survives`; `::test_prefix_is_exact_quote`; `::test_claim_301_cut`; `::test_anchor2_cut`; `::test_result_parses_ok`; `::test_idempotent` | F-REPORT `anchor_250`, `claim_301` | after H2 the 250-character anchor is 200 flattened characters, is a prefix of the original, is still found by `FND.locate` in the candidate, and `FND.parse_block(...)["ok"]` is true; a second run of H2 changes nothing |
| REQ-03 | The sandbox is built at the plan's base commit, or the recorded working tree for documents without a commit | I | `test_sandbox.py::test_file_created_by_implementation_absent`; `::test_masked_path_equals_base`; `::test_tree_snapshot_kind`; `::test_dirty_sandbox_refused` | F-REPO (base and head commits) | a file that the head commit adds is absent from `SB/<doc>/repo`; a file that the head commit edits equals its base version; for `base: tree:<dir>` the sandbox equals that directory and `sandbox.json` records `kind: tree` and the tree hash; a modified sandbox makes `build-sandbox.sh` exit 2 |
| REQ-04 | The sandbox holds no `.dev/reflect/`, `artifacts/`, `progress.md`, no report about the package and no ground truth | I | `test_sandbox.py::test_no_reflect_artifacts_progress`; `::test_no_doc_id_in_paths_or_contents`; `::test_no_ground_truth_file`; `::test_raw_mode_removes_only_gt` (DD-15) | F-REPO with those files planted | `find` finds no `reflect`, `artifacts` or `progress.md`; `grep -r -l <doc id>` and `find -path '*<doc id>*'` print nothing; the planted `ground-truth.json` trap is absent; in `--raw` mode `.dev/reflect` is kept and the trap is still removed |
| REQ-05 | CB-1 to CB-5 are present verbatim; the grading rule, the six findings categories and the judge are unchanged | U | `test_briefs.py::test_cb_verbatim_against_mr`; `::test_arm_part_sets`; `::test_base_equals_rr_lines_13_17`; `::test_six_categories_unchanged`; `::test_judge_brief_sha_equals_jj` | `MR`, `RR`, `JJ` read as files | each `briefs/cb*.txt` equals the matching quoted block of `MR` byte for byte (found by its opening words); the part sets of Z0-raw, Z0, K and SS are exactly those of `DESIGN.md` 8.1 (set equality); `briefs/base.txt` equals `RR` lines 13-17 and still lists exactly the six categories and the Medium grading rule; the sha256 of `bin/judge-one.sh`'s `BRIEF` text equals that of `JJ` lines 12-23 |

### 3.2 Redesign 1: Sweep Sheet (MR 6.3)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-18 | The pre-pass is a non-model, read-only script, byte-identical for the same input and seed, run serially, and killed at min(15 s, 0.10 b) with fallback | U | `test_prepass.py::test_byte_identical_same_seed`; `::test_other_seed_changes_only_order`; `::test_no_absolute_paths_in_json`; `::test_snapshot_unchanged`; `::test_no_network_no_model` | F-PLAN-1, F-REPO | two runs with seed 1 give identical file hashes for every file in `prepass/`; seed 2 changes only `assignment.json` and `sheets/` order, not `items.json` or `candidates.json` ids and statuses; no JSON holds a path starting with `/`; `git status` and the tree hash of the sandbox are unchanged; a monkeypatched `socket` and an environment without API keys do not break it |
| | | I | `test_kill_fallback.py::test_sleeping_stub_is_killed_and_falls_back`; `::test_kill_formula` | F-FAKE, `SW_PREPASS_CMD=sleep 5`, `SW_KILL_S=1` | the process group is killed after about 1 s, no `prepass/` folder remains, the run uses the Z0 brief (sha256 equal) and `run.json` has `fallback: true, reason: kill`; `kill_s(b)` returns 10.0 for 100, 12.2 for 122 and 15.0 for 200 |
| | serial | I | `test_run_panel_fake.py::test_prepass_finishes_before_first_reviewer` | F-FAKE with a call log | the first line of `FAKE_CALL_LOG` is later than the end timestamp of `prepass.json` in `timing.json` |
| REQ-19 | At most 12 items; quota 1-2 per triggered class with ranked fill; all candidates and dropped items logged with the seed | U | `test_select.py::test_200_setword_sentences`; `::test_single_class_fills_12`; `::test_fair_share_ceiling`; `::test_class_order_and_ties`; `::test_candidate_log_complete` | F-PLAN-3 (N = 200) | at most 12 items; every triggered class has at least 1; with `k >= 2` no class exceeds `ceil(12/k)`; with `k = 1` (one class has candidates) `attach` ran on that class's top 12 and the sheet holds 12 (1 when that class is C3); `candidates.json` has one entry per candidate found (at least 200), each with `status` and, when dropped, the reason, and carries the seed; the same input and seed give the same selection |
| REQ-20 | Assignment over 24 slots with caps summing to 24, replica 1 for items without attached tool output, no growth in the survivors' load on failure, order shuffled per reviewer | U | `test_assign.py::test_caps_sum_24_all_panels`; `::test_primary_12_items_fills_caps`; `::test_haiku_only_evidence_items`; `::test_no_evidence_replica_1`; `::test_no_duplicate_reviewer_per_item`; `::test_failure_never_raises_survivor_load`; `::test_two_reviewers_replica_1`; `::test_order_shuffled_per_reviewer_deterministic` | synthetic item lists built in the test | for each panel the caps in `config/panels.json` sum to 24; with 12 items (7 search, 5 read) the primary panel ends at loads 8, 8, 8; the haiku reviewer receives only items of classes C4, C5, C8 that have evidence; an item with an empty evidence list has one reviewer; after a simulated failure the surviving loads are equal to their loads before it; with two reviewers every item has one reviewer and no cap rises; two reviewers see the same items in different orders, and the same seed gives the same orders |
| REQ-21 | Extractors E1-E4 and E7 reach recall 0.8 or more on at least 3 non-study plans with seeded defects, precision reported; E6 labelled experimental | F | `test_recall.py::test_recall_per_extractor`; `::test_precision_reported`; `::test_e6_marked_experimental` | F-RECALL | recall is 0.8 or more for each of E1, E2, E3, E4, E7 pooled over at least 3 plans, precision is printed, every E6 item has `experimental: true` |
| | mechanics of each extractor | U | `test_e1.py` to `test_e7.py` (each: a positive case, a negative case, a near-miss case, a determinism case) | F-PLAN-1, F-REPO | the extractor emits the expected candidates with the expected evidence lines and priorities, and nothing on `p_clean.md` |
| | seeding authorship | M | `fixtures/recall/AUTHORS.md` | | signed by a person who did not write or read the extractors, dated before the extractors are frozen |
| REQ-22 | The offline selection-recall gate is met and the rank function beats a random pick on the derivation plans | U | `test_g0.py::test_recall_definitions`; `::test_covers_by_span_within_3`; `::test_random_baseline_deterministic`; `::test_gate_pass_and_fail` | F-GT with F-PLAN-1 | with known coverage the extraction and selection recall equal hand-computed values; a quote that sits within 3 lines counts; the random baseline repeats for a fixed seed; the gate passes at floor 0.4 and fails at floor 0.99 on the same data |
| | the real gate | X | `analysis/g0.py --docs derivation` then `--docs holdout` (section 5, step B3) | derivation ground truth (read by the script), hold-out ground truth (after the freeze) | selection recall at or above the pre-registered floor, and the rank beats the random baseline with at most 10% of draws at or above it; otherwise SS does not run |
| REQ-23 | An empty sheet leaves the brief equal to Z0's | U | `test_briefs.py::test_empty_sheet_brief_equals_z0_by_hash`; `::test_fallback_brief_equals_z0_by_hash` | F-PLAN-1 | sha256 of the SS brief with no items equals the sha256 of the Z0 brief for the same document |
| | the whole run | I | `test_run_panel_fake.py::test_no_trigger_run` | F-PLAN-2, F-FAKE | `run.json` has `no_trigger: true`, every reviewer brief hash equals the Z0 hash, no ledger is required and `ledger_missing` is not counted |
| REQ-24 | Search scope is tests, root documents and named paths, `.dev/` excluded, with a time bound | U | `test_scope.py::test_dev_and_dependency_folders_excluded`; `::test_named_paths_and_mirrors_included`; `::test_scope_string_recorded` | F-REPO | no hit from `.dev/` or `node_modules/` appears in any evidence; a hit in a root document, in `tests/`, in a plan-named directory and in a same-basename mirror does appear; `prepass.json` holds the scope string |
| | time on the largest tree | X | `test_prepass_timing.py::test_largest_tree_under_kill_limit` (marker `slow`) and `bin/time-prepass.sh` | `REPO` at HEAD, `F-PLAN-1` | S1 finishes in under 10 s (the kill limit at `b = 100`); the measured seconds go into `config/values.json` |

### 3.3 Time (MR 6.5)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-29 | The +35% limit is judged on per-package medians against same-day Z0 in the same randomised block, with one panel clock from before the pre-pass; mean and median reported | U | `test_clock.py::test_panel_elapsed_ss_and_other_arms`; `::test_clock_starts_before_prepass`; `test_analyze.py::test_d1_uses_medians`; `::test_d1_same_block_only`; `::test_mean_and_median_reported` | F-RUNS | `panel_elapsed_s` for SS is the end of S5 minus `t0`, for other arms the last reviewer end minus `t0`; the D1 ratio is computed from per-document medians; a Z0 run from another block is ignored (or the call raises); the report holds both mean and median |
| | the real timing log | X | `analysis/analyze.py all --stage N` writes `d1.json` | run folders | `d1.json` lists per-document medians, the 90th percentile and the kills, with pass or fail |
| REQ-30 | The hang guard is 1.5 x (b + expected overhead) from launch; kills and retries reported per arm; killed or retried reviewers are scored as zero findings | U | `test_hang_guard.py::test_formula_per_panel` | `values.json` | for the primary panel at `b = 100` the guard is 193.5 s (1.5 x 129); haiku at 220: 385.5 s; sonnet at 259: 435 s; Z0 at 100: 150 s |
| | | I | `test_run_panel_fake.py::test_sleeping_reviewer_killed`; `::test_no_retry_on_failure`; `::test_killed_reviewer_absent_from_merge` | F-FAKE `sleep`, `api_error`, `wrong_model` | the sleeping reviewer is recorded `killed` after the guard, the others finish, the merge is called without it; `FAKE_CALL_LOG` shows one call per reviewer even after a failure; the merged input has no report from the killed reviewer |
| | | U | `test_analyze.py::test_kills_retries_per_arm`; `::test_zero_findings_for_killed` | F-RUNS | the per-arm counts equal the counts in the fixture; a killed reviewer contributes zero found items |
| REQ-31 | The break-even values (pre-pass 14 s and 2.75 s per item at b = 100) are in the report with the measured values | U | `test_report.py::test_breakeven_values`; `::test_report_shows_planned_and_measured` | `values.json` planned and measured | `breakeven(b=100)` returns pre-pass 14.0 and 2.75 s per item for `n = 8`; `b = 122` returns about 21.7 s and 3.71 s; the report prints planned and measured side by side. The row cost 2.07 s of `MR` belongs to Redesign 2 and is not tested here |
| | | M | read `results/report.md` once the first block is analysed | | a named reviewer confirms the measured values appear next to the planned ones |
| REQ-32 | A 5-run luna timing spike precedes every arm and sets the fallbacks (6 items per luna; 12 rows) | I | `test_run_schedule.py::test_refuses_without_spike_record` | `values.json` without and with a `spike` record | `run-schedule.sh` exits non-zero without a record of 5 runs and a `c_luna`; with a record it starts; if `c_luna > 2.75` at `b = 100` it sets 6 items per luna and raises ember's cap to 12 in `panels.json` for the run (the 12 rows of Redesign 2 are not tested here) |
| | the spike | M | `bin/run-spike.sh timing` (needs models; owner go-ahead) | | the record `config/values.json: spike` exists with `runs: 5` (plus the 5 baseline runs, `DESIGN.md` 14.2) |

### 3.4 Contamination and overfitting (MR 6.6)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-33 | Recipes, cards, extractors and regexes are frozen by git tag before the hold-out ground truth is written | U | `test_order.py::test_freeze_tag_before_gt_commit`; `::test_gt_before_tag_fails`; `::test_freeze_json_hashes_match_files` | a temporary git repository with a tag and a ground-truth commit in both orders | `bin/check-order.sh freeze` exits 0 when the tag's commit time is earlier than the first commit of the ground-truth file and exits non-zero otherwise; a changed extractor file after the tag makes the hash check fail |
| | the real order | M | run `bin/check-order.sh freeze` when the hold-out ground truth is committed | | exit 0, the output pasted into `results/attestations.md` |
| REQ-34 | Reviewers never receive ground truth; hold-out sandboxes exclude reflect reports | U | `test_prepass_inputs.py::test_ground_truth_trap_not_read`; `::test_sheets_hold_no_gt_markers`; `test_sandbox.py::test_no_ground_truth_file` | F-REPO with the trap | a read hook on `open` shows the pre-pass never opens the trap; no sheet or brief contains a ground-truth file name or a field name such as `plan_quote`; the sandbox has no ground-truth file |
| | the real runs | X | `bash bin/check-sandbox-gt.sh` (a `grep -r` over every `SB/<doc>/repo` and every `RUN/prepass/sheets`) | real sandboxes | prints nothing; run before the first arm and after the last |
| REQ-35 | Leave-one-class-out ablation changes the other classes' reach by at most 15 points | U | `test_g0.py::test_ablation_report_synthetic` | F-GT, F-PLAN-1 | with a class removed, each other class's selection recall changes by at most 0.15 on the fixture, and the report names each class with its change |
| | the real report | X | `analysis/g0.py --ablate` on the decision documents | | every change is at most 15 points, else the quota is revised before the freeze |
| | model-stage ablation | M | not run: it needs 8 extra arms and is outside the run budget of `MR` 5.4 (DD-13); if wanted, 8 arms x 4 documents x 3 runs = 96 panel runs | | owner decision |
| REQ-36 | Hold-out ground truth is written and hashed before the first arm; planted defects are authored by someone who has not seen the recipes or extractors; every planted plan has a clean twin | U | `test_order.py::test_gt_hash_matches_prereg`; `::test_every_planted_plan_has_twin` | synthetic `prereg.json` and planted-set manifest | the sha256 of each ground-truth file equals the value in `prereg.json`; every planted entry names a twin file that exists |
| | | M | `config/attestation.md`: author name, date, "has not seen the recipes, cards or extractors", hash of the ground-truth files; and the hash times from `check-order.sh prereg` | | signed before the first arm; the hash commit is earlier than the first `run.json` |

### 3.5 Applicability (MR 6.7)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-37 | Spec and documentation fixtures exist: E1, E2 and E5 produce items on a spec fixture; E4 and E1 on a documentation fixture | U | `test_formats.py::test_spec_fixture_e1_e2_e5`; `::test_doc_fixture_e4_e1`; `::test_new_format_is_data_only` | F-SPEC with its parent, F-DOC with F-REPO | each listed extractor yields at least one item on its fixture; E5 yields nothing on the spec fixture when the parent is removed; adding a format dictionary in the test needs no change to any extractor function |
| REQ-38 | The registry README lists, per target type, what must be re-derived | U | `test_readme.py::test_readme_lists_rederive_rows` | `cards/README.md` | for plan, specification and documentation the README has a row for each of: block patterns, command dialect, test and root-document paths, severity guidance, location of truth, snapshot |
| | the content | M | document review by a second reader | | a record in `cards/README.md` footer: reader, date, "each row is specific, not a restatement of the heading" |

### 3.6 Reporting and validation (MR 6.8)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-39 | All metrics come from one script over the run folders | U | `test_analyze.py::test_metrics_match_expected_json`; `::test_one_definition_of_found_fraction` | F-RUNS | every metric of `DESIGN.md` 14.3 equals `expected.json`; an AST search over `SW` finds `found_fraction` (and the other metric names) defined only in `analysis/analyze.py` |
| REQ-40 | Gains are reported as H share, prompting share (K minus Z0) and redesign share, never summed | U | `test_report.py::test_three_shares_separate`; `::test_no_summed_headline` | F-RUNS | the report has three labelled lines with the values `Z0 - Z0raw`, `K - Z0`, `SS - Z0`; no line contains two share names joined by "+" or "total" |
| | | M | read the headline of `results/report.md` | | no sentence adds two shares |
| REQ-41 | Reach is logged per stage and the per-class act-rate bands are pre-registered | U | `test_stages.py::test_stage_rows_schema`; `::test_stage_values_on_fixture`; `test_prereg.py::test_act_bands_for_all_classes` | F-RUNS, F-GT | each row of `stages.jsonl` has the five stage fields; the values equal the hand-computed ones; `prereg.json` has a band `[lo, hi]` with `0 <= lo < hi <= 1` for each of C1-C8 |
| | the real bands | M | `config/prereg.json` committed with the owner's values (`DESIGN.md` 15.1) | | committed before the first hold-out run (REQ-44) |
| REQ-42 | Displacement is measured as non-probe findings per run, and D6 is a blocking gate | U | `test_analyze.py::test_nonprobe_findings_per_run`; `::test_d6_failure_blocks_adoption`; `::test_promoted_lines_not_counted_as_reviewer_findings` | F-RUNS | the count excludes lines with `probe` set and lines with `src: ledger`; a fixture where D2 and D3 pass and D6 fails yields an overall result of "do not adopt" |
| REQ-43 | The judge is a blind Opus with a frozen rubric, a second judge on 15%, and an API-error audit per batch | U | `test_judge.py::test_judge_brief_sha`; `::test_model_is_opus_only_in_judge`; `::test_audit_flags_error_with_score_file`; `::test_second_judge_sample_15_percent_seeded`; `::test_audit_counts_match_merged_rows` | synthetic judge folders | the brief hash equals `JJ`'s; no reviewer script names `claude-opus-5-5`; a judge folder with API-error text and a score file is flagged; the sample holds `round(0.15 n)` runs and repeats for a fixed seed; a score whose row counts differ from the merged report is flagged |
| | the real batch | X | `analysis/analyze.py audit-judges <stage>` | judge outputs | `bad = 0` or each bad item re-judged and logged |
| REQ-44 | Arms, run counts, the consistency definition and the gates are committed before the first hold-out run | U | `test_order.py::test_prereg_commit_before_first_run` | temporary git repository | `bin/check-order.sh prereg` exits 0 when the `prereg.json` commit is earlier than the first `run.json`, and non-zero otherwise |
| | the real order | M | `check-order.sh prereg` output pasted into `results/attestations.md` | | exit 0 |
| REQ-45 | Claims are worded "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), and only for Redesign 1 at the high end of its range" | U | `test_report.py::test_claim_template_text` | the report generator | the generator's claim sentence equals the REQ-45 sentence and no other sentence uses "consistent" for another class |
| | | M | report review | | a named reviewer confirms the final report's claims use that wording |
| REQ-46 | The optional verifier never sits on the critical path, cannot add claims, and its time is excluded | U | `test_verifier_off_path.py::test_no_verifier_step_in_clock`; `::test_verifier_default_off`; `::test_verifier_time_excluded` | `timing.json` fixtures | the launcher has no verifier step; `VERIFIER` defaults to 0; if `verifier_s` is present it is not in `panel_elapsed_s` and no claim is added to a findings block. (The verifier itself is not built; the test guards the seam.) |

### 3.7 Also needed by this design (not on the requested list)

These requirements of `MR` 6.2 are part of how the sheet works, so they have tests too. REQ-06, REQ-08 and REQ-10 concern the shared cards; REQ-25 to REQ-28 (Redesign 2) are out of scope.

| REQ | Kind | Test |
|---|---|---|
| REQ-06 (cards) | U | `test_cards.py::test_schema_valid`, `::test_each_card_has_two_instances`, `::test_promote_category_valid` (the 120-word recipe limit belongs to Redesign 2) |
| REQ-07 (lint) | U + F | `test_lint.py::test_seeded_leak_fails`, `::test_clean_passes`, `::test_forbidden_name_fails`, `::test_fixtures_clean`; F: `test_lint.py::test_real_files_against_real_gt` (reads real ground truth, run by a maintainer) |
| REQ-08 (swap test and second-author review) | M | `cards/*.json: swap_test` records with reviewer and date |
| REQ-09 (no `src/superclaude/` in briefs) | U | `test_briefs.py::test_no_src_path_in_any_brief` |
| REQ-10 (new class = one card) | U | `test_cards.py::test_fixture_card_c9_needs_no_dispatcher_change` |
| REQ-11 (extra keys) | U | `test_fnd_contract.py::test_merge_accepts_class_probe_src_keys` (runs `MRG.command` through click's `CliRunner` on a report with the keys); `::test_existing_review_suite_passes` runs `uv run pytest tests/review -q` |
| REQ-12 (a)(b) | I | (a) `test_kill_fallback.py::test_forced_exception_in_prepass_and_render_falls_back`; (b) `test_run_panel_fake.py::test_forced_exception_in_check_merges_as_written` (the report text given to the merge equals the raw reviewer text; `check_skipped: true`) |
| REQ-13 | U | `test_ledgerv1.py::test_misplaced_duplicated_truncated_blocks` over F-REPORT; `::test_fence_opener_grep_is_not_used` |
| REQ-14 | U | `test_ledgerv1.py::test_quote_wrapping_a_plan_line_matches` |
| REQ-15 | U | `test_ledgerv1.py::test_promotion_copies_problem_and_anchor`, `::test_promotion_validates_with_check_finding` (long id, short anchor, duplicate id), `::test_promotion_inside_single_block`, `::test_promotion_failure_logged_and_skipped` |
| REQ-16 | U | `test_ledgerv1.py::test_unsupported_row_demotes_linked_finding`, `::test_unsure_never_blocks`, `::test_blocking_needs_cb3_and_two_quotes_or_search`, `::test_unlinked_finding_untouched` (DD-3), `::test_quote_other_corpora` (DD-2: source, candidate, sheet, transcript) |
| REQ-17 | X | `analysis/analyze.py compliance` over the 5 compliance-spike runs: `ledger_missing` at most 10% |

## 4. Tests for the design's own constraints and decisions

| Source | Kind | Test | Passes when |
|---|---|---|---|
| K1 writes stay under `SW`, `SB`, `/tmp` | U | `test_paths.py::test_refuses_output_outside_sw`, `::test_override_must_be_under_tmp`, `::test_kill_s_is_numeric_only`, `::test_prepass_cmd_stub_only` | a path under `REPO/src` or `REPO/tests` is refused with `E_NOT_WRITABLE`; `SW_SB_ROOT=/home/x` is refused; `SW_KILL_S=1` is accepted and `9999` refused; `SW_PREPASS_CMD=sleep 5` is accepted and `rm -rf x` refused |
| K2 model allowlist | U | `test_model_allowlist.py::test_reviewer_models`, `::test_opus_only_in_judge`, `::test_fable_and_tier0_refused` | `sw_assert_model` accepts the four reviewer models and refuses every other id, including Opus, Fable, Qwen and glm; `grep -rn claude-opus-5-5 $SW/bin $SW/sweep $SW/scaffold` hits only `bin/judge-one.sh` |
| K3 pre-pass inputs | U | `test_prepass_inputs.py::test_only_three_inputs` | the pre-pass entry point has exactly the arguments candidate, source and repo, and opens no other root |
| K4 sandbox read-only | I | `test_sandbox_clean.py::test_dirty_after_run_is_flagged` | a fake reviewer that writes a file in the sandbox is detected by the post-run `git status --porcelain` and the run is flagged `sandbox_dirty` |
| K5 no git write | U | `test_freeze.py::test_freeze_prints_but_never_tags` | `bin/freeze.sh` prints the `git tag` command and `git tag -l` is unchanged |
| K7 no `lib/` folder | U | `test_layout.py::test_no_ignored_folder_names` | no folder under `SW` matches a `.gitignore` pattern (checked with `git check-ignore` on each code folder) |
| DD-2 `quote_other` corpora | U | covered by REQ-16 `test_quote_other_corpora` | a plan-vs-plan row with the second quote from the candidate passes; a quote that is in none of the four corpora fails |
| DD-3 linked findings only | U | `test_ledgerv1.py::test_unlinked_finding_untouched`, `::test_check_scope_all_switch_off_by_default` | an unlinked blocking finding stays blocking in the default scope |
| DD-4 fair share | U | REQ-19 tests | as in 3.2 |
| DD-5 one scope | U | REQ-24 tests | as in 3.2 |
| DD-6 sheet in the brief | U | `test_render.py::test_sheet_text_in_brief_and_file_equal`, `::test_sheet_cap_16000_trims_lowest_priority`, `::test_class_label_only_no_hint` | the items text in the brief equals the file; a 20-item overflow fixture is trimmed from the lowest-priority items and flagged `sheet_trimmed`; the sheet shows `C4`, never an extractor name or a priority |
| DD-7 dangling CB-2 clause | X | `analysis/analyze.py all` counts reports in Z0 and K that contain a `## Ledger` heading | the count is reported per arm; an owner decision if it is above 0 |
| DD-8 one attempt | I | REQ-30 `test_no_retry_on_failure` | as in 3.3 |
| DD-9 order S5, H2, merge | I | `test_run_panel_fake.py::test_order_s5_then_h2_then_merge` | the files appear in `check/`, then `normalised/`, then `merged/`, and a long anchor that the check needed for linking is linked before H2 cuts it |
| DD-10 two-phase extractors | U | `test_extractors_common.py::test_attach_only_for_top_k`, `::test_single_class_attaches_top_12`, `::test_all_candidates_logged` | with 30 candidates in one class and some in a second class, 8 of the first have `evidence_computed`; with 30 in one class and none elsewhere, 12 do; all 30 are in `candidates.json` in both cases |
| DD-12 `class` filled by the check | U | `test_ledgerv1.py::test_class_key_added_from_item` | a linked line without `class` gets it; a line with a wrong `class` is corrected and counted |
| Sheet and brief are blind to the arm | U | `test_blindness.py::test_merged_report_has_no_telemetry_keys` | `merged-1.md` and `merged/ledger.json` contain none of `probe`, `src`, `class`, `ledger-v1` |

## 5. Validation experiment commands (written here, not run)

The experiment is `MR` section 5. Nothing below was run for this design. Steps A and B need no model. Steps C onward start reviewer or judge sessions, so each needs the owner's go-ahead; the judge model (`claude-opus-5-5`) is used for scoring only (K2).

```
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
PYRUN="uv run --frozen --project $REPO python"
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
export NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 PYTHONDONTWRITEBYTECODE=1
```

### A. No model: build and check

```
A1  uv run --frozen --project $REPO pytest -p no:cacheprovider $REPO/tests/review -q        # the code this design imports is healthy
A2  $T $SW/tests -q -m "not slow and not freeze"                                          # unit and fake-claude integration
A3  $T $SW/tests -q -m slow                                                                # prepass seconds on the largest tree
A4  bash $SW/bin/time-prepass.sh --doc <doc>                                              # S1 seconds on each real snapshot; writes config/values.json: prepass_s
A5  uv run --frozen --project $REPO ruff check $SW && uv run --frozen --project $REPO ruff format --check $SW
```

### B. No model: gates and freeze

```
B1  $PYRUN $SW/sweep/cli.py lint --all --gt-glob "$REPO/.dev/eval-workspaces/**/ground-truth*.json"   # AO-1 over frozen files; a maintainer runs it, it reads ground truth and prints only file, line and a hash
B2  $T $SW/tests -q -m freeze                                                              # REQ-21 recall on fixtures/recall, real-ground-truth lint
B3  $PYRUN $SW/analysis/g0.py --docs derivation --seeds 1,2,3,4,5 --floor-from $SW/config/prereg.json
    $PYRUN $SW/analysis/g0.py --docs derivation --ablate --seeds 1,2,3,4,5                 # REQ-35, DD-13
B4  bash $SW/bin/freeze.sh                                                                 # prints sha256 of cards, extractors, words, formats, rank table, briefs and the git tag command; a person runs the tag
B5  (hold-out author) write hold-out ground truth to $SW/holdout-gt/<doc>/ground-truth.json, commit it
B6  $PYRUN $SW/analysis/g0.py --docs holdout --seeds 1,2,3,4,5 --floor-from $SW/config/prereg.json   # decision gate G0
B7  $PYRUN $SW/analysis/analyze.py prereg --write --owner-values $SW/config/owner-values.json        # arms, run counts, consistency definition, gates D1-D7, floor, act bands
B8  bash $SW/bin/check-order.sh freeze && bash $SW/bin/check-order.sh prereg                # REQ-33, REQ-36, REQ-44
B9  bash $SW/bin/check-sandbox-gt.sh                                                       # REQ-34: grep for ground truth in every sandbox
```

If B6 fails, SS does not run (`MR` 3.1, selection-recall gate).

### C. Models: the two spikes (owner go-ahead)

```
C1  bash $SW/bin/run-spike.sh timing --panel ember --doc HO-6 --item-count 8 --runs 5 --baseline-runs 5     # 10 luna runs, REQ-32
C2  bash $SW/bin/run-spike.sh compliance --panel ember --doc HO-6 --runs 5                                  # 5 SS panel runs = 15 reviewer runs, REQ-17
C3  $PYRUN $SW/analysis/analyze.py compliance --runs $SW/runs/spike-compliance                              # ledger_missing at most 10%, quote validity, format errors
```

Go or no-go: `ledger_missing` at most 10%, and the measured `c_luna` at or below the break-even (`DESIGN.md` 12.3), otherwise the fallback share of 6 items per luna is set in `config/panels.json`.

### D. Models: Stage 1 (decision)

```
D1  $PYRUN $SW/bin/make-schedule.py --stage 1 --arms z0,k,ss --docs HO-1,HO-2,HO-3,HO-4 --reps 5 --seed 20261115 --out $SW/runs/schedule-stage1.tsv
D2  $PYRUN $SW/bin/make-schedule.py --stage 1 --arms z0raw --docs HO-1,HO-2,HO-3 --reps 5 --seed 20261115 --append $SW/runs/schedule-stage1.tsv
D3  bash $SW/bin/run-schedule.sh $SW/runs/schedule-stage1.tsv              # at most 3 panels at once; refuses without the spike record (REQ-32)
D4  bash $SW/bin/judge-batch.sh stage1                                     # anonymise, one blind Opus judge per run, API-error audit; 15% second judge
D5  $PYRUN $SW/analysis/analyze.py audit-judges stage1
D6  $PYRUN $SW/analysis/analyze.py all --stage 1 --out $SW/results/stage1  # metrics, D1-D7, stages.jsonl, shares, report.md
```

Counts. `MR` 5.4 gives Stage 1 as 95 panel runs: 80 for the four arms Z0, K, SS and RL on four documents with 5 runs each, and 15 for Z0-raw on three documents. This design builds no RL arm, so the Stage 1 schedule above has 3 arms x 4 documents x 5 = 60 runs plus 15 Z0-raw = **75 panel runs** (225 reviewer runs). The 20 RL runs of `MR` are not part of this schedule.

### E. Models: Stage 2 (only for an arm that passes D1, D2 or D3 on Stage 1)

```
E1  planted set (6 plans, Z0 and SS, 3 runs):      $PYRUN $SW/bin/make-schedule.py --stage 2 --set planted --arms z0,ss --reps 3 ...      36 runs
E2  clean twins (6 plans, 2 runs):                 ... --set twins --arms z0,ss --reps 2 ...                                               24 runs
E3  spec HO-5 (5 runs):                            ... --set spec --arms z0,ss --reps 5 ...                                                10 runs
E4  documentation arm (8 documents, 3 runs):       ... --set docs --arms z0,ss --reps 3 ...                                                48 runs
E5  haiku panel (4 documents, 3 runs):             ... --set holdout4 --panel haiku --arms z0,ss --reps 3 ...                              24 runs
E6  sonnet panel (3 documents, 2 runs):            ... --set holdout3 --panel sonnet --arms z0,ss --reps 2 ...                             12 runs
E7  then, as in D3 to D6 with --stage 2
```

Stage 2 without RL is 36 + 24 + 10 + 48 + 24 + 12 = **154 panel runs** (`MR` gives 231 with RL). With Stage 1 the total is 75 + 154 = **229 panel runs**, about 687 reviewer runs (`MR`: 326 panel runs, about 978 reviewer runs, with both redesigns).

### F. Derivation-set check (reported, never used for a decision)

```
F1  run Z0 and SS once on the three study packages (derivation set):  $PYRUN $SW/bin/make-schedule.py --stage d --set derivation --arms z0,ss --reps 1 ...
F2  $PYRUN $SW/analysis/analyze.py all --stage d --out $SW/results/derivation --label derivation-only
```

### G. Decision

`analysis/analyze.py all` prints the outcome row of `MR` 5.8 for SS against Z0 and K: neither redesign passes means keep Z0; SS passing alone adopts SS; "SS beats K by at least 0.04" is gate D7. Adoption then follows `IMPLEMENTATION.md` step 16.

## 6. Definition of done for the implementation

The implementation is done when all of the following hold, each shown by an output, not by a statement:

1. `$T $SW/tests -q -m "not slow and not freeze"` exits 0 and its summary line is saved to `SW/results/tests-final.log`.
2. `uv run --frozen --project $REPO ruff check $SW` and `ruff format --check $SW` exit 0.
3. `uv run --frozen --project $REPO pytest -p no:cacheprovider $REPO/tests/review -q` still exits 0.
4. Every row of section 3 is either backed by a passing test or by an M record that exists on disk; the list of M records still open is printed by `bin/open-manual-checks.sh`.
5. `git status` shows no change under `src/`, `tests/`, `.claude/` or `.dev/tasks/` made by the implementation.
6. The freeze (`IMPLEMENTATION.md` step 14) has not been done before items 1 to 5 hold, and the freeze tests (`-m freeze`) pass.

What "done" does not mean: that SS works. Whether the sheet raises the found fraction is decided only by Stage 1 and Stage 2 (section 5), and the power of that experiment is low (`MR` 5.9): a pass is evidence, not proof.
