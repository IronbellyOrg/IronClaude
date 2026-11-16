# Testing: Redesign 2, Recipe Ledger

Status: design only. No test exists yet and nothing here was run. This file maps every requirement of `MR` sections 6.1, 6.2 and 6.4 to 6.8 to a runnable test or to a labelled manual check, lists the fixtures, and gives the commands for the validation experiment, including one panel of ember + 2x luna on one package for the RL arm and for the Z0 control arm. `DESIGN.md` has the behaviour; `IMPLEMENTATION.md` has the build order.

Path names are those of `DESIGN.md`: `REPO`, `RL`, `SW`, `MR`, `RR`, `JJ`, `FND`, `LED`, `MRG`, `SBR`, `EVAL`, `SWD`. Decision ids `DR-n` are those of `DESIGN.md` 1.3; constraint ids `K1` to `K9` are those of its 1.2.

Requirements 18 to 24 (`MR` 6.3) belong to Redesign 1 only (pre-pass, sheet, extractors, assignment) and are not tested here. Section 3.8 lists them with the nearest Recipe Ledger property so that nothing is dropped silently.

## 1. Conventions

### 1.1 Kinds of check (the same labels as `SW/TESTING.md`, so the two builds read alike)

| Label | Kind | Needs a model | When it can run |
|---|---|---|---|
| **U** | unit test in `RL/tests/`, pure Python, no process other than `git` | no | any time after the code exists |
| **I** | integration test: the real launcher scripts with the fake `claude` on `PATH` (`tests/fakes/claude`) and the real `superclaude review merge` | no | after step 5 of `IMPLEMENTATION.md` |
| **F** | freeze-time test (pytest marker `freeze`): needs the real ground truth (the lint) or a second author's records. It fails, never skips, when its inputs are missing | no | at the freeze (step 11) |
| **X** | experiment-time check: a script run over real run folders after model runs. Each X check also has a **U** twin on synthetic run folders, so the check itself is tested before it is trusted | the data comes from model runs | during and after the experiment |
| **M** | manual check with a named person, a record file and a pass rule | no | named per row |
| **C** | a copied sibling test, run unchanged in `RL` against the copied code (Tier T of `DESIGN.md` 3.1). It is listed so that a requirement is not shown as covered by a test that does not exist | no | after step 1 |

A requirement is "covered" only when every part of its Test column in `MR` is covered by at least one runnable check; M rows say which part cannot be automated and why.

### 1.2 Commands

```
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"

PYTHONDONTWRITEBYTECODE=1 $T $RL/tests -q -m "not slow and not freeze"     # everything that needs no models and no hand-made records
PYTHONDONTWRITEBYTECODE=1 $T $RL/tests -q -m slow                          # tests that launch a harness script on the fake claude
PYTHONDONTWRITEBYTECODE=1 $T $RL/tests -q -m freeze                        # real-ground-truth lint, review records
PYTHONDONTWRITEBYTECODE=1 $T $RL/tests/test_rowcheck.py -q                 # one file
uv run --frozen --project $REPO ruff check $RL && uv run --frozen --project $REPO ruff format --check $RL
```

The same pytest form as the collaboration designs and the sibling use. The repository's own suite stays the guard for the code this design imports: `uv run --frozen --project $REPO pytest -p no:cacheprovider $REPO/tests/review -q` must pass before and after (`IMPLEMENTATION.md` step 0).

### 1.3 Rules for every test

- Tests write only under a pytest `tmp_path` or `/tmp`. The override variables (`SW_SB_ROOT`, `SW_SRC_REPO`) are refused unless they point under `/tmp/` (copied `common.sh`), so a test can never write into `REPO`.
- Test hooks of this build are named without the `SW_` prefix, because the copied `conftest.py` passes every `SW_*` variable through the copied override guard, which refuses names it does not know. There is one: `RL_FORCE_EXC` (one of `lens`, `check`, `reask`: raise in that component). `bin/rl-env.sh` accepts only those values; anything else exits 2. The value of `b` is passed with the `--b <seconds>` option of `run-panel.sh`, so a test that needs a late clock uses `--b 1`.
- No test starts a real model, a judge or a network call. The fake `claude` is a script on `PATH`; the suite fails if the first `claude` on `PATH` is not the fake (`test_fake_claude_rl.py`, and the copied `conftest.py` helper `assert_fake_first`).
- Timing tests use a fake clock where the requirement is arithmetic, and a real sleeping stub only where the requirement is about killing a process (REQ-30).
- Every fixture is invented. No fixture contains text, names, paths or numbers from a study package or from a ground-truth file. The AO-1 lint runs over `fixtures/` (the copied `test_lint.py::test_fixtures_clean`, which scans `RL/fixtures`).
- A test that depends on a Tier B file (`DESIGN.md` 3.1) names it in its docstring. If that file is `built-local`, the test is the acceptance test of the local build; if it is copied, the same test must pass on the copy.

## 2. Fixtures

All fixtures are built by code where a static copy would be large. Static files are short. The copied ones are Tier T of `DESIGN.md` 3.1.

| Id | Location | What it is | Used by |
|---|---|---|---|
| F-PLAN-1 | `fixtures/plans/p_basic.md` with `source.md` (copied) | an invented plan (a report exporter and a retention policy) in the `workflow-plan` format with a `Source:` line, constraints, tasks, acceptance criteria and a source document | brief and lens render, report fixtures (quotes are cut from it), fake-claude runs |
| F-PLAN-2 | `fixtures/plans/p_clean.md` (copied) | an invented plan with no trigger shape | false-positive checks of the row check; a run whose reviewers write only `OK` rows |
| F-SPEC | `fixtures/specs/spec1.md`, `parent1.md` (copied) | an invented specification and its parent requirement document | REQ-37 |
| F-DOC | `fixtures/docs/doc1.md` (copied) | an invented how-to | REQ-37 |
| F-REPO | `fixtures/repos/build_repo.py` (copied) | builds a small git repository in `tmp_path` with base and head commits, noise folders and a trap file named `ground-truth.json` | sandbox tests, K3, REQ-03, REQ-04, REQ-34 |
| F-LENS | `fixtures/lens/make_lens.py` | builds lens tables in `tmp_path`: a valid copy of `config/lenses.json`, and one invalid variant per rule of `DESIGN.md` 5.2 (a class in no lens, a lens with 5 recipes, a lens with 1 recipe, `table_cap` 15, `table_cap` below the recipe count, an unknown model, two search roles, a re-ask role on the haiku panel, a duplicated-class set that differs from REQ-25); and a class C9 variant (card, recipe, placement) | REQ-10, REQ-25, REQ-26, REQ-35, DR-4 |
| F-REPORT-RL | `fixtures/reports/make_rl_reports.py` | builds reviewer final messages in `tmp_path` from quotes cut out of F-PLAN-1 by regular expression (so a quote is always exact). One per case: `good_ember`, `good_luna1`, `none_found`, `none_found_with_rows`, `ledger_missing`, `ledger_after_findings`, `ledger_twice`, `ledger_unclosed`, `findings_unclosed`, `findings_twice`, `heading_between`, `bad_json_line`, `verdict_lowercase`, `unknown_class`, `over_budget_recipe`, `over_budget_lens`, `recipe_missing`, `dup_row`, `quote_plan_not_in_candidate`, `quote_wraps_line`, `quote_other_in_source`, `quote_other_in_candidate`, `quote_other_in_transcript`, `quote_other_only_in_assistant_text`, `problem_no_finding`, `finding_linked_by_probe`, `finding_linked_by_quote`, `ok_but_finding`, `unsure_with_blocking`, `blocking_no_cb3`, `blocking_with_cb3`, `anchor_250` and `claim_301` (copied), `promote_long_id`, `promote_short_anchor`, `promote_dup_id`, `via_reask` | REQ-02, REQ-13 to REQ-16, REQ-26 |
| F-TRANSCRIPT-RL | `fixtures/transcripts/make_transcripts.py` | minimal run transcripts in the shape of a real `claude -p --output-format json` run (`system`, `assistant` with `message.model` and `tool_use` blocks of `Bash` and `Read`, `user` with `tool_result` blocks, `result` with `result`, `usage`, `modelUsage`), one per report that needs the `transcript` corpus or a `ran` check: a search done, a search claimed and not done, no tool call at all, a `NONE FOUND` with and without a search | REQ-16 corpora, REQ-28 |
| F-FAKE-RL | `tests/fakes/claude` | a script that reads the brief on stdin, finds the `R-C<n>.` headings, picks a scenario from `FAKE_SCENARIO` and prints the JSON array of a real run. Scenarios: `ok` (rows `C<n>.1` to `C<n>.<budget>` for every recipe found, all `OK`), `problem` (one PROBLEM row with exact quotes from the candidate and a linked finding), `none_found`, `ledger_missing`, `ledger_after_findings`, `over_budget`, `recipe_missing`, `long_anchor`, `bad_block`, `api_error`, `wrong_model`, `sleep` (`FAKE_SLEEP_S`), `exit127`, `repair` (used for a second call whose brief starts with the repair sentence of `DESIGN.md` 7.6; it returns the first message with a ledger added). `FAKE_SCENARIO_BY_MODEL` may set a different scenario per requested model. It appends one line per call to `FAKE_CALL_LOG`: `<epoch seconds> TAB <scenario> TAB <requested model> TAB <kind: review or repair>`. | I tests |
| F-GT | `fixtures/gt/synthetic-gt.json` | invented ground truth for F-PLAN-1 (items with `id`, `class`, `blocking_in_implement`, `description`, `plan_quote`), so the stage rows, the lint and the analysis have something to read without any study data | REQ-07, REQ-41 |
| F-RUNS-RL | `fixtures/runs/make_runs.py` | builds synthetic run folders for the arms Z0-raw, Z0, K and RL, 2 documents, 5 replicates, with known found sets, timings, flags (`fallback`, `check_skipped`, `reask`, `killed`), ledgers and scores, and writes `expected.json` by hand-written arithmetic (not by calling `analyze.py`) | REQ-29, REQ-39 to REQ-43 |
| F-SIBLING | `fixtures/sibling/make_sibling.py` | builds a fake sibling folder in `tmp_path` with Tier A, T and B files in chosen states (all present, a Tier A file missing, a Tier B file changing between two reads, a Tier B file absent) and a canary file whose mtime is checked | DR-11, K8 |
| F-LINT-GT | `fixtures/gt/lint-gt.json` | invented ground truth with phrases and a name that are seeded into a temporary copy of a recipe, to prove the lint catches them | REQ-07 |

F-LENS, F-REPORT-RL and F-TRANSCRIPT-RL cases are written by code, not by hand, and the AO-1 lint runs over the generator files as part of `fixtures/`. The hold-out and planted material of `MR` 5.1 is not a fixture of this build: it is written by its author after the freeze (`DESIGN.md` 11.1).

## 3. Requirement map

Test names are `file::function` under `RL/tests/`. "Passes when" is the observable rule. Kind **C** rows name the sibling test file that is copied and run unchanged.

### 3.1 Harness and brief (`MR` 6.1)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-01 | The brief names the source only when a source file exists; otherwise it logs `no_source` and C2 is not applicable | U | `test_render.py::test_cb1_present_with_source`; `::test_cb1_absent_without_source`; `::test_c2_recipe_dropped_without_source`; `::test_no_source_flags_in_run_json` | F-PLAN-1 with and without a source | with a source each of the three RL briefs holds `Driving document: <absolute source path>` once and a C2 recipe where the lens table has one; without a source no brief holds `Driving document:` or the C2 recipe text, and `run.json` has `no_source: true, c2_not_applicable: true` |
| | | C | `test_briefs.py` (CB-1 cases) | | the copied renderer's own CB-1 tests pass in `RL` |
| REQ-02 | The merge input truncates `anchor` and `anchor2` to 200 and `claim` to 300 characters (a prefix of an exact quote) and is validated with the real parser | C | `test_normalise.py` (`anchor_250` survives, prefix is an exact quote, `claim_301` cut, `anchor2` cut, result parses, idempotent) | `fixtures/reports/{anchor_250,claim_301}.md` | the copied H2 tests pass |
| | the whole path | I | `test_run_panel_fake.py::test_long_anchor_survives_h2_then_merge` | F-FAKE-RL `long_anchor` | the finding with a 250-character anchor appears in `merged-1.md` with a 200-character anchor, through the real `superclaude review merge` |
| REQ-03 | The sandbox is built at the plan's base commit, or the recorded working tree for documents without a commit | C | `test_sandbox.py` (file created by the implementation absent, masked path equals base, tree snapshot kind, dirty sandbox refused) | F-REPO | the copied tests pass in `RL` with `SW_SB_ROOT` under `/tmp` |
| REQ-04 | The sandbox holds no `.dev/reflect/`, `artifacts/`, `progress.md`, no report about the package and no ground truth | C | `test_sandbox.py` (no reflect, artifacts or progress; no document id; no ground-truth file; raw mode removes only ground truth) | F-REPO with those files planted | `find` and `grep -r` find none |
| | the real sandboxes | X | `bash $RL/bin/check-sandbox-gt.sh` (a `grep -r` over every sandbox under `SBR` and every `RUN/briefs`) | real sandboxes | prints nothing; run before the first arm and after the last |
| REQ-05 | CB-1 to CB-5 are present verbatim; the grading rule, the six findings categories and the judge are unchanged | C | `test_briefs.py` (CB blocks equal the `MR` quotes byte for byte, arm part sets, base equals `RR` lines 13-17, six categories unchanged) | `MR`, `RR` read as files | the copied tests pass |
| | RL parts | U | `test_render.py::test_rl_brief_starts_with_z0_text`; `::test_fallback_brief_equals_z0_by_hash`; `::test_rl_part_order`; `::test_row_cap_placeholder_equals_mr_at_14` (DR-3) | F-PLAN-1 | the RL brief begins with the exact Z0 brief of the same document, then the copied ledger rule, then the RL block, then the heading, then the recipes; a fallback brief has the sha256 of the Z0 brief; with `row_cap` 14 the RL block equals the `MR` 3.2(a) quote byte for byte |
| | the judge | U | `test_judge.py::test_judge_brief_sha_equals_jj` (Tier B) | `JJ` read as a file | the sha256 of `bin/judge-one.sh`'s `BRIEF` text equals that of `JJ` lines 12-23 |

### 3.2 Registry and ledger (`MR` 6.2)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-06 | The eight cards validate against the schema; each recipe is at most 120 words; each card has at least 2 instances outside the study packages | C | `test_cards.py` (schema valid, two instances each, `promote_category` valid) | `cards/` (copied) | the copied tests pass |
| | recipes | U | `test_recipes.py::test_recipe_keys_equal_card_ids` (DR-1); `::test_each_recipe_at_most_120_words`; `::test_budget_sentence_once_and_parsed` (C2 6, others 4, each 1 to 14); `::test_recipes_equal_mr_quotes` (byte for byte with `MR` 3.2(a) while no `override` entry exists) | `recipes/recipes.json`, `MR` | key sets equal; word counts 71, 89, 56, 99, 86, 93, 50, 67 are all at most 120; each text ends with exactly one `Write at most N rows.`; text equals the `MR` quote |
| REQ-07 | The lint fails on any 4-word sequence from a ground-truth description or plan quote, and on any package, task or file name | C | `test_lint.py` (seeded leak fails, clean passes, forbidden name fails, fixtures clean) | F-LINT-GT | the copied tests pass |
| | RL files | U | `test_lint_rl.py::test_seeded_phrase_in_recipe_fails`; `::test_seeded_name_in_lenses_fails`; `::test_rl_files_clean_on_synthetic_gt` | F-LINT-GT, temporary copies of `recipes/` and `config/` | the lint exits 1 on a seeded recipe and on a seeded name in `lenses.json`, and 0 on the clean files |
| | the real files | F | `test_lint_rl.py::test_real_recipes_against_real_gt` (marker `freeze`) | the real ground truth, read by a maintainer | exit 0 over `recipes/ config/ briefs/ cards/ fixtures/`; the output holds file, line and hash only |
| REQ-08 | The swap test and a second-author review are recorded per card | M | `recipes/REVIEWS.md`: one row per recipe C1 to C8 with reviewer, date and the statement "domain nouns replaced by placeholders, still reads correctly, no issue-specific word"; the cards' `swap_test` records belong to the sibling's copies | | every row filled by a person who has not seen the ground truth, dated before the freeze |
| | the record exists | F | `test_recipes_reviews.py::test_review_record_complete` (marker `freeze`) | `recipes/REVIEWS.md` | 8 rows, none with an empty reviewer or date |
| REQ-09 | Rendered briefs hold no `src/superclaude/` path | U | `test_render.py::test_no_src_path_in_any_brief` (every arm, panel, reviewer, with and without a source); `test_recipes.py::test_no_src_path_in_recipe_files` | F-PLAN-1 | `grep -c 'src/superclaude/'` is 0 on every brief and on `recipes/` |
| REQ-10 | A new class is one card plus an optional extractor, with no dispatcher change | U | `test_lens.py::test_fixture_class_c9_needs_no_code_change` (DR-1) | F-LENS C9 variant | with a card, a recipe entry and a lens placement for C9 and the unchanged modules, the briefs hold `R-C9.`, the legal row ids include `C9.1`, and the table validation passes; with the recipe entry removed it fails |
| REQ-11 | Findings may carry `class`, `probe` and `src`; the existing merge tests pass | C | `test_fnd_contract.py::test_merge_accepts_class_probe_src_keys` (runs `MRG.command` through click's `CliRunner`); `::test_existing_review_suite_passes` (runs `uv run pytest tests/review -q`) | a report with the keys | exit 0, and the merged text does not contain the keys |
| REQ-12 | (a) On failure of the lens render, the harness runs the isolated brief and records `fallback=true`. (b) On failure of the post-run ledger check it merges the findings block as written and records `check_skipped=true` | I | (a) `test_fallback.py::test_forced_exception_in_lens_render_runs_z0_briefs` (`RL_FORCE_EXC=lens`); `::test_invalid_lens_table_falls_back`; `::test_fallback_decided_before_first_reviewer_starts`. (b) `test_run_panel_fake.py::test_forced_exception_in_check_merges_as_written` (`RL_FORCE_EXC=check`) | F-FAKE-RL, F-LENS invalid variants | (a) the three briefs have the sha256 of the Z0 brief, `run.json` has `fallback: true` with the reason, and the first line of `FAKE_CALL_LOG` is later than the `fallback` marker of `run.json`; (b) the text given to the merge equals the raw reviewer text and `check_skipped: true`. The "pre-pass" component of the requirement does not exist in this redesign. |
| REQ-13 | The ledger is a `ledger-v1` JSON-lines block in the final message, directly above the single findings block; both blocks are parsed by a real parser, not by the fence-opener grep | U | `test_rowcheck.py::test_misplaced_duplicated_truncated_blocks`; `::test_fence_opener_grep_is_not_used`; `::test_heading_between_ledger_and_findings_is_missing` | F-REPORT-RL `ledger_missing`, `ledger_after_findings`, `ledger_twice`, `ledger_unclosed`, `findings_unclosed`, `findings_twice`, `heading_between`, `bad_json_line` | each broken case is `ledger_missing` or counts a format error as defined in `DESIGN.md` 7.1; a report that holds the fence opener text only in prose is `ledger_missing`; the good cases parse |
| REQ-14 | Substring checks use the same flattening as `findings.py` | U | `test_rowcheck.py::test_quote_wrapping_a_plan_line_matches`; `::test_quote_plan_not_in_candidate_fails` | F-REPORT-RL `quote_wraps_line`, `quote_plan_not_in_candidate` | a quote that wraps a candidate line passes (`FND.locate` is non-empty); a quote that is not in the candidate has `quote_plan_ok` false |
| REQ-15 | The promotion function copies the reviewer's own `problem`, takes the plan-side anchor, validates with `_check_finding`, inserts inside the single block, tags `src=ledger`, MINOR and non-blocking, and logs and skips on failure | U | `test_rowcheck.py::test_promotion_copies_problem_and_anchor`; `::test_promotion_validates_with_check_finding` (long id, short anchor, duplicate id); `::test_promotion_inside_single_block`; `::test_promotion_failure_logged_and_skipped`; `::test_promotion_requires_quote_plan_ok`; `::test_no_promotion_for_over_budget_unknown_or_reask_rows`; `::test_class_key_added_from_row_prefix` | F-REPORT-RL `problem_no_finding`, `promote_long_id`, `promote_short_anchor`, `promote_dup_id`, `over_budget_recipe`, `unknown_class`, `via_reask` | the promoted line has `claim` equal to the row's `problem`, `anchor` equal to its `quote_plan`, severity MINOR, `blocking` false, `src` `ledger`, `class` from the row id, and sits inside the one findings block; each failing case is in `promotion_failures` and absent from the block; rows of the last three cases are not promoted |
| REQ-16 | Unsupported PROBLEM rows are demoted to non-blocking; blocking needs the grading sentence plus two quotes or a search result | U | `test_rowcheck.py::test_unsupported_row_demotes_linked_finding`; `::test_unsure_never_blocks`; `::test_blocking_needs_cb3_and_two_quotes_or_search`; `::test_unlinked_finding_untouched` (`SWD` DD-3); `::test_quote_other_corpora` (DR-9); `::test_check_scope_all_switch_off_by_default`; `::test_format_induced_demotions_counted` | F-REPORT-RL, F-TRANSCRIPT-RL | a blocking finding linked to an unsupported PROBLEM or an UNSURE row is non-blocking with its severity kept and its cause counted; a plan-versus-plan row with the second quote from the candidate is supported; a `quote_other` found only in a tool result of the transcript is supported as a search result; one found only in assistant text is not; an unlinked blocking finding stays blocking |
| REQ-17 | The `ledger_missing` rate from the compliance spike is at most 10% before any arm | X | `analysis/analyze.py compliance --runs RL/runs/spike-compliance` (section 5.3, step C2) | the 5 spike runs | `ledger_missing` at most 10% of reviewer runs (at most 1 of 15), with quote validity, format errors, `recipe_missing` and `none_found` per class printed |
| | the check itself | U | `test_analyze.py::test_compliance_report_on_fixture` | F-RUNS-RL | the numbers equal the hand-computed ones in `expected.json` |

### 3.3 Redesign 2: Recipe Ledger (`MR` 6.4)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-25 | The eight recipes live in one file and are quoted verbatim by lens; at most 4 per reviewer; the duplicated classes are C2 and C4 on the primary panel, C1 on the haiku panel, and C1 and C7 on the sonnet panel | U | `test_lens.py::test_generated_briefs_match_lens_table[primary]`, `[haiku]`, `[sonnet]`; `::test_duplicated_classes_equal_req25`; `::test_search_form_only_in_search_role`; `test_recipes.py::test_recipe_text_only_in_one_file` | `config/lenses.json`, `recipes/recipes.json`, F-PLAN-1 | for each panel the three rendered briefs are parsed by the heading `R-C<n>.`: each brief's recipe set equals its lens, none has more than 4, each recipe paragraph equals the `recipes.json` text byte for byte, all eight classes appear on the panel, the classes seen in two briefs are exactly {C2, C4} (primary), {C1} (haiku), {C1, C7} (sonnet); the search-form line is in the search role's brief only; no file under `RL` other than `recipes.json` (and the two design documents) holds the first ten words of a recipe |
| REQ-26 | There is a row budget per recipe and at most 14 rows per lens; `NONE FOUND` is allowed | U | `test_rowcheck.py::test_row_budget_per_recipe`; `::test_lens_cap_enforced`; `::test_none_found_allowed_and_covers_recipe`; `::test_none_found_with_rows_flagged`; `::test_recipe_missing_flagged`; `test_lens.py::test_row_cap_per_panel` (14 / 14 / 14, 6 / 14 / 12, 8 / 12 / 12); `::test_row_cap_formula_table` (the table of `DESIGN.md` 5.4); `::test_no_budget_refuses` | F-REPORT-RL `over_budget_recipe`, `over_budget_lens`, `recipe_missing`, `none_found`, `none_found_with_rows`; F-LENS | a fifth row of a 4-row recipe and a fifteenth row of a lens are `over_budget` with reason `recipe` or `lens`; a lone `NONE FOUND` row covers its recipe; a recipe with no row is in `recipe_missing`; the cap function returns the table's values (b = 100: c 2.00 gives 14, 2.07 gives 14, 2.41 gives 12, 2.50 gives 11, 3.00 gives 9; b = 122: c 2.00 gives 14, c 3.00 gives 12; b = 60, c 2.00 gives 7); a cap below the number of recipes exits `run-panel.sh` with code 3 |
| REQ-27 | There is no luna re-ask; an ember re-ask runs only if `now + 30 s <= 1.35 b` | U | `test_reask.py::test_condition_with_fake_clock`; `::test_boundary_is_inclusive`; `::test_never_for_luna_even_with_large_b`; `::test_only_when_ledger_missing`; `::test_only_once`; `::test_haiku_and_sonnet_never` | no files; a fake clock passed as an argument | with b = 100: now 81 allowed (111 <= 135), now 105 allowed (135 <= 135.0), now 105.01 not allowed; with b = 122: now 134.7 allowed, 134.8 not; a role with `reask: false` is never allowed, even at b = 1000; a reviewer with no `ledger_missing` is never allowed; a second request is refused |
| | the whole path | I | `test_run_panel_fake.py::test_ember_reask_runs_once_and_is_accepted`; `::test_reask_rejected_when_findings_differ`; `::test_no_reask_when_clock_too_late` (`--b 1`); `::test_luna_ledger_missing_is_not_reasked`; `::test_reask_failure_keeps_original_report` (`RL_FORCE_EXC=reask`); `::test_reask_not_counted_as_retry` | F-FAKE-RL `ledger_missing` for ember and `repair` | `FAKE_CALL_LOG` shows two ember calls (kinds `review`, `repair`) and one call per luna; the repaired ledger is read, rows are marked `via_reask`, and the run records `reask: [t2b-1]`; a repair whose findings block differs is discarded; with `--b 1` there is no second call; the re-ask is not in the retry count |
| REQ-28 | The `ran` field is cross-checked against transcript tool calls in the analysis | U | `test_ran_check.py::test_verified_unverified_and_not_a_tool_claim`; `::test_search_recipe_without_bash_is_unverified`; `::test_none_found_for_search_recipe_without_call_is_unverified`; `::test_report_per_class_and_reviewer` | F-REPORT-RL, F-TRANSCRIPT-RL | each fixture row gets the `ran_status` of `DESIGN.md` 7.7 and the per-class and per-reviewer counts equal the hand-computed ones |
| | the heuristic against a person | M | read 20 rows of the compliance spike (`bin/open-manual-checks.sh ran-audit` prints them with their transcripts), write `results/ran-audit.md` | the spike runs | a named reader's judgement of "did the reviewer run what `ran` says" agrees with `ran_status` on at least 18 of 20 rows; if not, the rule of `DESIGN.md` 7.7 is revised and the metric is not reported until it is |
| | the real runs | X | `analysis/ran_check.py <run dir>...` | real runs | the per-class table is written to `results/ran.md` |


### 3.4 Time (`MR` 6.5)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-29 | The +35% limit is judged on per-package medians against same-day Z0 in the same randomised block, with one panel clock from before the lens render; mean and median are reported | U | `test_clock.py::test_panel_elapsed_rl_and_other_arms`; `::test_clock_starts_before_lens_render`; `::test_reask_seconds_inside_the_clock`; `test_analyze.py::test_d1_uses_medians`; `::test_d1_same_block_only`; `::test_mean_and_median_reported` | F-RUNS-RL | `panel_elapsed_s` for RL is the end of R3 minus `t0` (it includes `reask_s`); for the other arms the last reviewer end minus `t0`; the D1 ratio is computed from per-document medians; a Z0 run from another block is ignored (or the call raises); the report holds both mean and median |
| | the real timing log | X | `analysis/analyze.py all --stage N` writes `d1.json` | run folders | per-document medians, the 90th percentile and the kills, with pass or fail |
| REQ-30 | The hang guard is 1.5 x (b + expected overhead) from launch; kills and retries are reported per arm; killed or retried reviewers are scored as zero findings | U | `test_hang_guard.py::test_formula_per_panel` | `config/values.json` | primary RL at b = 100, 120, 122: 192, 222, 225 s; primary Z0: 150, 180, 183 s; haiku RL at 220, 238: 375, 402 s; sonnet RL at 259, 302: 433.5, 498 s |
| | | I | `test_run_panel_fake.py::test_sleeping_reviewer_killed`; `::test_no_retry_on_failure`; `::test_killed_reviewer_absent_from_merge` | F-FAKE-RL `sleep`, `api_error`, `wrong_model` | the sleeping reviewer is recorded `killed` after the guard, the others finish, the merge is called without it; `FAKE_CALL_LOG` shows one `review` call per reviewer even after a failure; the merge input has no report from the killed reviewer |
| | | U | `test_analyze.py::test_kills_retries_per_arm`; `::test_zero_findings_for_killed`; `::test_reask_counted_apart_from_retries` | F-RUNS-RL | the per-arm counts equal the fixture's; a killed reviewer contributes zero found items; re-asks are a separate column |
| REQ-31 | The break-even values (row cost 2.07 s) are in the report with the measured values | U | `test_report.py::test_breakeven_values`; `::test_report_shows_planned_and_measured` | `values.json` planned and measured | `breakeven_row_cost(b=100, rows=14)` is 2.07 and `(100, 12)` is 2.42; b = 120 gives 2.57 and b = 122 gives 2.62; b = 116 gives 2.47; the report prints planned and measured side by side. The pre-pass seconds (14 s) and the cost per item (2.75 s) of `MR` REQ-31 belong to Redesign 1 and are not tested here |
| | | M | read `results/report.md` once the first block is analysed | | a named reviewer confirms the measured values appear next to the planned ones |
| REQ-32 | A 5-run luna timing spike precedes every arm and sets the fallbacks (6 items per luna; 12 rows) | I | `test_run_schedule.py::test_refuses_without_spike_record`; `::test_spike_sets_row_cap` | `values.json` without and with a `spike` record | `run-schedule.sh` exits non-zero without a record of 5 runs and a `c_luna`; with a record it starts and passes the cap `lens_row_cap(b_min, c_luna)` into every RL run (c = 2.41 gives 12, c = 2.50 gives 11 at b = 100). The 6 items per luna belong to Redesign 1 |
| | the spike | M | `bin/run-spike.sh timing` (needs models; owner go-ahead) | | the record `config/values.json: spike` exists with `runs: 5` and the 5 baseline runs of `DESIGN.md` 12.4 |

### 3.5 Contamination and overfitting (`MR` 6.6)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-33 | Recipes, cards, extractors and regexes are frozen by git tag before the hold-out ground truth is written | U | `test_order.py::test_freeze_tag_before_gt_commit`; `::test_gt_before_tag_fails`; `::test_freeze_json_hashes_match_files` | a temporary git repository with a tag and a ground-truth commit in both orders | `bin/check-order.sh freeze` exits 0 when the tag's commit time is earlier than the first commit of the ground-truth file and non-zero otherwise; a changed recipe, lens, brief or `rl/*.py` file after the tag makes the hash check fail |
| | the real order | M | run `bin/check-order.sh freeze` when the hold-out ground truth is committed | | exit 0, the output pasted into `results/attestations.md` |
| REQ-34 | Reviewers never receive ground truth; hold-out sandboxes exclude reflect reports | U | `test_ground_truth_not_read.py::test_lens_brief_and_check_never_open_the_trap` (K3); `test_render.py::test_briefs_hold_no_gt_markers`; and the copied `test_sandbox.py` ground-truth cases | F-REPO with the trap | a read hook on `open` shows the lens render, brief render and row check never open the trap; no brief holds a ground-truth file name or a field name such as `plan_quote`; the sandbox has no ground-truth file |
| | the real runs | X | `bash $RL/bin/check-sandbox-gt.sh` | real sandboxes | prints nothing |
| REQ-35 | Leave-one-class-out ablation changes the other classes' reach by at most 15 points | U | `test_ablation.py::test_removing_one_recipe_leaves_every_other_part_byte_identical` (DR-13) | F-LENS | for each class: with its recipe and lens placements removed, every other recipe paragraph in every brief, every Z0 part and every other lens position is byte for byte the same; the lens validation still passes or names the class that is now uncovered |
| | the real report | X | `analysis/analyze.py ablate-report` over the Stage 1 runs | real runs | for each class, the change in the other classes' reach computed from the runs; at most 15 points, else the lens table is revised before the freeze. This is a report on runs that exist, not an ablation run |
| | model-stage ablation | M | not run: it needs 8 extra arms and is outside the run budget of `MR` 5.4 (DR-13); if wanted, 8 arms x 4 documents x 3 runs = 96 panel runs | | owner decision |
| REQ-36 | Hold-out ground truth is written and hashed before the first arm; planted defects are authored by someone who has not seen the recipes or extractors; every planted plan has a clean twin | U | `test_order.py::test_gt_hash_matches_prereg`; `::test_every_planted_plan_has_twin` | synthetic `prereg.json` and planted-set manifest | the sha256 of each ground-truth file equals the value in `prereg.json`; every planted entry names a twin file that exists |
| | | M | `config/attestation.md`: author name, date, "has not seen the recipes or the lens table", hash of the ground-truth files; and the hash times from `check-order.sh prereg` | | signed before the first arm; the hash commit is earlier than the first `run.json` |

### 3.6 Applicability (`MR` 6.7)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-37 | Spec and documentation fixtures exist; the recipes apply to them. (`MR` words the test for Redesign 1's extractors; Recipe Ledger has none, so the test is that a lens renders for both targets.) | U | `test_targets.py::test_spec_and_doc_fixtures_exist`; `::test_lens_renders_for_spec_fixture`; `::test_lens_renders_for_doc_fixture` | F-SPEC with its parent as the source, F-DOC with no source | for the specification every recipe C1 to C8 is present on the primary panel (C2 included, the parent is the source); for the documentation target recipe C2 is absent and the seven others are present, with `no_source` and `c2_not_applicable` in `run.json`; in both cases each lens holds at least 2 recipes |
| REQ-38 | The registry README lists, per target type, what must be re-derived | U | `test_recipes_readme.py::test_readme_lists_rederive_rows` | `recipes/README.md` | for plan, specification and documentation the README has a row for each of: meaning of edits, meaning of tests and gate, meaning of source, command dialect, test and root-document paths, severity guidance, snapshot, lens assignment (the table of `DESIGN.md` 11.3) |
| | the copied README | C | `test_readme.py` | `cards/README.md` (copied) | the sibling's README test passes on the copy; its extractor sentences do not apply to `RL` and `recipes/README.md` says so in its first lines |
| | the content | M | document review by a second reader | | a record at the foot of `recipes/README.md`: reader, date, "each row is specific, not a restatement of the heading" |

### 3.7 Reporting and validation (`MR` 6.8)

| REQ | Requirement (short) | Kind | Test or check | Fixture | Passes when |
|---|---|---|---|---|---|
| REQ-39 | All metrics come from one script over the run folders | U | `test_analyze.py::test_metrics_match_expected_json`; `::test_one_definition_of_found_fraction` | F-RUNS-RL | every metric of `DESIGN.md` 12.5 equals `expected.json`; an AST search over `RL` finds `found_fraction` (and the other metric names) defined only in `analysis/analyze.py` |
| REQ-40 | Gains are reported as H share, prompting share (K minus Z0) and redesign share, never summed in a headline | U | `test_report.py::test_three_shares_separate`; `::test_no_summed_headline` | F-RUNS-RL | the report has three labelled lines with `Z0 - Z0raw`, `K - Z0`, `RL - Z0`; no line holds two share names joined by "+" or "total" |
| | | M | read the headline of `results/report.md` | | no sentence adds two shares |
| REQ-41 | Reach is logged per stage and the per-class act-rate bands are pre-registered | U | `test_stages.py::test_stage_rows_schema` (extraction null for RL, selection, act, merge survival, judge credit, class, reviewer id); `::test_selection_covers_rule`; `::test_stage_values_on_fixture`; `test_prereg.py::test_act_bands_for_all_classes` | F-RUNS-RL, F-GT | each row has the five stage fields; the values equal the hand-computed ones; `prereg.json` has a band `[lo, hi]` with `0 <= lo < hi <= 1` for each of C1 to C8 |
| | the real bands | M | `config/prereg.json` committed with the owner's values (`DESIGN.md` 13.1 item 7) | | committed before the first hold-out run (REQ-44) |
| REQ-42 | Displacement is measured as non-probe findings per run, and D6 is a blocking gate | U | `test_analyze.py::test_nonprobe_findings_per_run`; `::test_d6_failure_blocks_adoption`; `::test_promoted_lines_not_counted_as_reviewer_findings` | F-RUNS-RL | the count excludes lines with `probe` set and lines with `src: ledger`; a fixture where D2 and D3 pass and D6 fails yields "do not adopt" |
| REQ-43 | The judge is a blind Opus with a frozen rubric, a second judge on 15%, and an API-error audit per batch | U | `test_judge.py::test_judge_brief_sha`; `::test_model_is_opus_only_in_judge`; `::test_audit_flags_error_with_score_file`; `::test_second_judge_sample_15_percent_seeded`; `::test_audit_counts_match_merged_rows`; `::test_merged_report_has_no_arm_marker` | synthetic judge folders | the brief hash equals `JJ`'s; no reviewer script names `claude-opus-5-5`; a judge folder with API-error text and a score file is flagged; the sample holds `round(0.15 n)` runs and repeats for a fixed seed; a score whose row counts differ from the merged report is flagged; the anonymised merged report holds none of `probe`, `src`, `class`, `ledger-v1` |
| | the real batch | X | `analysis/analyze.py audit-judges <stage>` | judge outputs | `bad = 0` or each bad item re-judged and logged |
| REQ-44 | Arms, run counts, the consistency definition and the gates are committed before the first hold-out run | U | `test_order.py::test_prereg_commit_before_first_run` | temporary git repository | `bin/check-order.sh prereg` exits 0 when the `prereg.json` commit is earlier than the first `run.json`, and non-zero otherwise |
| | the real order | M | `check-order.sh prereg` output pasted into `results/attestations.md` | | exit 0 |
| REQ-45 | Claims are worded "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), and only for Redesign 1 at the high end of its range" | U | `test_report.py::test_claim_template_text` | the report generator | the generator's claim sentence equals the REQ-45 sentence and no other sentence uses "consistent" for another class |
| | | M | report review | | a named reviewer confirms the final report's claims use that wording |
| REQ-46 | The optional verifier never sits on the critical path, cannot add claims, and its time is excluded | U | `test_verifier_off_path.py::test_no_verifier_step_in_clock`; `::test_verifier_default_off`; `::test_verifier_time_excluded` | `timing.json` fixtures | the launcher has no verifier step; `VERIFIER` defaults to 0; if `verifier_s` is present it is not in `panel_elapsed_s` and no claim is added to a findings block. (The verifier itself is not built; the test guards the seam.) |

### 3.8 Requirements that are not tested here

| REQ | Where it belongs | Nearest Recipe Ledger property and where it is tested |
|---|---|---|
| REQ-18 (pre-pass is a read-only deterministic script, killed at min(15 s, 0.10 b)) | Redesign 1 | the lens and brief render are deterministic and under 1 s (`DESIGN.md` 2.4): `test_render.py::test_byte_identical_same_inputs`; `test_lens.py::test_render_under_one_second` |
| REQ-19 (at most 12 items, quota) | Redesign 1 | the row caps of REQ-26 |
| REQ-20 (assignment over 24 slots) | Redesign 1 | the lens table of REQ-25 |
| REQ-21 (extractor recall) | Redesign 1 | none; AO-4 does not apply (`DESIGN.md` 11.1) |
| REQ-22 (selection-recall gate) | Redesign 1 | none; the ledger-and-time gate G0 is REQ-17 and REQ-31 |
| REQ-23 (empty sheet equals Z0 by hash) | Redesign 1 | the fallback brief equals Z0 by hash (REQ-12 a, REQ-05) |
| REQ-24 (search scope and time on the largest tree) | Redesign 1 | the timing spike on the largest tree (`DESIGN.md` 11.4, 12.4) |

## 4. Tests for the design's own constraints and decisions

| Source | Kind | Test | Passes when |
|---|---|---|---|
| K1 writes stay under `RL`, `SBR`, `/tmp` | C | `test_paths.py` | a path under `REPO/src` or `REPO/tests` is refused with `E_NOT_WRITABLE`; `SW_SB_ROOT=/home/x` is refused |
| K2 model allowlist | C + U | `test_model_allowlist.py` (copied); `test_model_allowlist_rl.py::test_opus_only_in_judge_script`; `::test_lens_models_are_allowed` | `grep -rn claude-opus-5-5 $RL/bin $RL/rl $RL/scaffold` hits only `bin/judge-one.sh`; every `model` in `config/lenses.json` passes `sw_assert_model` |
| K3 the harness reads no ground truth | U | `test_ground_truth_not_read.py` | see REQ-34 |
| K4 sandbox read-only | I | `test_sandbox_clean.py::test_dirty_after_run_is_flagged` | a fake reviewer that writes a file in the sandbox is detected by the post-run `git status --porcelain` and the run is flagged `sandbox_dirty` |
| K5 no git write | U | `test_freeze.py::test_freeze_prints_but_never_tags` | `bin/freeze.sh` prints the `git tag` command and `git tag -l` is unchanged |
| K7 no ignored code folder | U | `test_layout_rl.py::test_no_ignored_folder_names` | `bin`, `tests`, `scaffold`, `rl`, `analysis` exist; none matches a `.gitignore` pattern (`git check-ignore`); there is no `lib/` |
| K8 the sibling is read only | U | `test_sibling_readonly.py::test_copy_script_never_writes_the_sibling`; `::test_no_script_writes_under_sw` | against F-SIBLING, the canary file's mtime and content are unchanged after a copy; a grep of every script of `RL` finds no write target (`>`, `cp`, `mv`, `rm`, `tee`, `mkdir`, `touch`) that resolves under `SW` |
| K9 own sandbox root | U | `test_sandbox_root.py::test_launcher_sets_its_own_root`; `::test_sibling_root_is_refused` | after sourcing `bin/rl-env.sh`, `SW_SB_ROOT` is `/tmp/evalsb-recipe`; `/tmp/evalsb-sweep` is refused with exit 4 |
| DR-1 recipes keyed by card id | U | `test_recipes.py::test_recipe_keys_equal_card_ids` | as REQ-06 |
| DR-2 Z0 prefix | U | `test_render.py::test_rl_brief_starts_with_z0_text` | as REQ-05 |
| DR-3 row-cap placeholder | U | `test_render.py::test_row_cap_placeholder_equals_mr_at_14`; `::test_other_cap_changes_only_the_number` | at 14 the block equals the `MR` quote; at 6 and 8 the only difference is that number |
| DR-4 cost-driven cap | U | `test_lens.py::test_row_cap_formula_table` | as REQ-26 |
| DR-5 row ids | U | `test_rowcheck.py::test_row_id_grammar_and_lens_membership`; `::test_assigned_ids_per_lens` | `C4.1` is accepted for a lens with C4, `C4.1` is `unknown_item` for a lens without it, `C4x` and `4.1` are `unknown_item`; the assigned id set of a lens equals `C<n>.1 ... C<n>.<budget>` per recipe |
| DR-6 over-budget rows | U | `test_rowcheck.py::test_row_budget_per_recipe`; `::test_over_budget_rows_not_promotable` | as REQ-26 and REQ-15 |
| DR-7 no source | U | `test_render.py::test_c2_recipe_dropped_without_source`; `test_lens.py::test_every_lens_keeps_two_recipes_without_c2` | as REQ-01; after dropping C2 every lens of the three panels holds at least 2 recipes |
| DR-8 re-ask scope and rules | U + I | `test_reask.py`; `test_run_panel_fake.py` re-ask tests | as REQ-27; plus `::test_repaired_rows_never_promoted` |
| DR-9 corpora | U | `test_rowcheck.py::test_quote_other_corpora` | as REQ-16 |
| DR-10 `ran` check | U | `test_ran_check.py` | as REQ-28 |
| DR-11 shared copy rule | U | `test_shared_manifest.py::test_manifest_hashes_match_files`; `::test_briefs_parts_match_manifest`; `::test_built_local_entries_name_a_swd_section`; `::test_copy_script_refuses_a_missing_tier_a_file`; `::test_copy_script_refuses_an_unstable_tier_b_file`; `::test_copy_script_marks_absent_tier_b_as_built_local`; `::test_check_reports_drift_as_warning`; `::test_diff_prints_for_built_local` | against F-SIBLING: every copied file equals its recorded hash; an edited copy fails `--check`; a Tier A file missing stops the script; a Tier B file whose hash differs between two reads stops it; an absent Tier B file is recorded `built-local` with a section name; a changed sibling file is `drift`, exit 0 |
| DR-12 run folder fields | U | `test_run_json_fields.py::test_fields_match_sibling_schema` | `run.json` and `timing.json` of an RL run hold every field name of `SWD` 2.2 and 11.4 that applies; the extra RL fields are listed in `DESIGN.md` 2.2 |
| DR-12 Z0 parity | X | `bash $RL/bin/check-z0-parity.sh <doc>` | prints the Z0 brief sha256 for the document; equal to the sibling's `run.json` for a Z0 run of the same document |
| DR-13 ablation | U | REQ-35 test | as REQ-35 |
| DR-15, DR-16 shared brief decisions | C | `test_briefs.py` | the copied tests pass |
| Determinism and render time | U | `test_render.py::test_byte_identical_same_inputs`; `test_lens.py::test_render_under_one_second` | two renders of the same inputs give identical file hashes; the lens render plus the brief render of one panel take under 1 s on the fixture |
| Fake claude is the first on `PATH` | U | `test_fake_claude_rl.py::test_scenarios_and_call_log` | each scenario prints the JSON array of its description; `FAKE_CALL_LOG` gets one line per call; the suite fails if the first `claude` on `PATH` is not the fake |
| Order: check, then H2, then merge | I | `test_run_panel_fake.py::test_order_check_then_h2_then_merge` (`SWD` DD-9) | files appear in `check/`, then `normalised/`, then `merged/`; a long anchor that the check needed for linking is linked before H2 cuts it |
| Blind to the arm | U | `test_blindness.py::test_merged_report_has_no_telemetry_keys` | `merged-1.md` and `merged/ledger.json` contain none of `probe`, `src`, `class`, `ledger-v1` |
| Row check time | U | `test_rowcheck.py::test_check_under_one_second_on_three_reports` | the check of three fixture reports with transcripts takes under 1 s (excluding interpreter start) |
| Concurrency budget (`DESIGN.md` 9.5) | I | `test_run_schedule.py::test_max_panels_default_one`; `::test_max_panels_three_runs_three_at_once` | with the default the fake-claude schedule never has more than 3 reviewer processes alive (read from `FAKE_CALL_LOG` start and end times); with `--max-panels 3` it reaches 9 and never 10 |
| The check scripts of `bin/` | U | `test_check_scripts.py::test_sandbox_gt_check_finds_a_planted_trap_and_is_silent_when_clean`; `::test_z0_parity_prints_a_stable_hash`; `::test_open_manual_checks_lists_open_records` | `check-sandbox-gt.sh` exits non-zero on a sandbox with a planted ground-truth file and prints nothing on a clean one; `check-z0-parity.sh` prints the same sha256 twice for the same document; `open-manual-checks.sh` lists every M record that is still open |
| Tier S file (`config/packages.json`) | U | `test_shared_manifest.py::test_tier_s_file_recorded_once_and_not_checked` | the initial hash is in the manifest; adding a hold-out entry to the file does not fail `--check` |

## 5. Validation experiment commands (written here, not run)

The experiment is `MR` section 5. Nothing below was run for this design. Steps A and B need no model. Steps C onward start reviewer or judge sessions, so each needs the owner's go-ahead; the judge model (`claude-opus-5-5`) is used for scoring only (K2). The helper scripts named here are those of `DESIGN.md` 9 and 12 and `IMPLEMENTATION.md`; options marked `(local)` belong to the version built in `RL`; if a Tier B script was copied from the sibling, its own `--help` is the authority for its options.

```
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
PYRUN="uv run --frozen --project $REPO python"
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
export NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 PYTHONDONTWRITEBYTECODE=1
```

### 5.1 A. No model: copy, build, check and rehearse

```
A1  uv run --frozen --project $REPO pytest -p no:cacheprovider $REPO/tests/review -q     # the code this design imports is healthy
A2  bash $RL/bin/copy-shared.sh && bash $RL/bin/copy-shared.sh --check                     # DR-11: copy Tier A, T and available Tier B; every copy equals its recorded hash
A3  $T $RL/tests -q -m "not slow and not freeze"                                          # unit and fake-claude integration
A4  $T $RL/tests -q -m slow                                                                # tests that launch run-panel.sh on the fake claude
A5  uv run --frozen --project $REPO ruff check $RL && uv run --frozen --project $REPO ruff format --check $RL
A6  $PYRUN $RL/rl/cli.py lens --validate                                                   # the lens table of DESIGN 5.2 against the real cards and recipes
A7  (rehearsal on the fake claude, no model) 
    export SW_SB_ROOT=/tmp/evalsb-recipe-rehearsal
    DOC=TASK-WF-designSpec-20261107-075614
    bash $RL/bin/build-sandbox.sh $DOC             # reads git objects of REPO, writes only under /tmp
    PATH=$RL/tests/fakes:$PATH FAKE_SCENARIO=ok FAKE_CALL_LOG=/tmp/rl-rehearsal-calls.log \
      bash $RL/bin/run-panel.sh --arm RL --panel primary --doc $DOC --replicate 1 --block 1 --seed 1 --run-id rehearsal-rl
    cat /tmp/rl-rehearsal-calls.log                # three review lines, no model was started
```

### 5.2 B. No model: gates and freeze

```
B1  $PYRUN $RL/scaffold/lint.py $RL/recipes $RL/config $RL/briefs $RL/cards $RL/fixtures \
      --gt-glob "$REPO/.dev/eval-workspaces/**/ground-truth*.json"     # AO-1; a maintainer runs it; it prints file, line and a hash, never the phrase
B2  $T $RL/tests -q -m freeze                                          # real-ground-truth lint, review records (REQ-07, REQ-08)
B3  bash $RL/bin/freeze.sh                                             # prints sha256 of recipes, lenses, briefs, cards, rl/*.py and the git tag command; a person runs the tag (K5)
B4  (hold-out author) write $RL/holdout-gt/<doc>/ground-truth.json, commit it   # after B3, never before (REQ-33)
B5  $PYRUN $RL/analysis/analyze.py prereg --write --owner-values $RL/config/owner-values.json   # arms, run counts, consistency definition, gates D1-D7, act bands
B6  bash $RL/bin/check-order.sh freeze && bash $RL/bin/check-order.sh prereg                    # REQ-33, REQ-36, REQ-44
B7  bash $RL/bin/check-sandbox-gt.sh                                   # REQ-34
B8  bash $RL/bin/check-z0-parity.sh $DOC                               # DR-12: the Z0 brief hash, to compare with the sibling's
```

### 5.3 C. Models: the two spikes (owner go-ahead)

```
C1  bash $RL/bin/run-spike.sh timing --panel primary --doc HO-6 --runs 5 --baseline-runs 5     # 5 luna runs with the RL lens of luna 1 and 5 with the Z0 brief, REQ-32
C2  bash $RL/bin/run-spike.sh compliance --panel primary --doc HO-6 --runs 5                    # 5 RL panel runs = 15 reviewer runs, REQ-17
C3  $PYRUN $RL/analysis/analyze.py compliance --runs $RL/runs/spike-compliance                  # ledger_missing, recipe_missing, quote validity, none_found per class
C4  bash $RL/bin/open-manual-checks.sh ran-audit                                                # prints 20 rows with their transcripts for the REQ-28 manual audit
```

Go or no-go: `ledger_missing` at most 10% of the 15 reviewer runs, and the measured c at or below the break-even of the cap. If c is above 2.07 s at b = 100 the cap falls as in `DESIGN.md` 5.4 and is passed into every run by `run-schedule.sh`.

### 5.4 D. One panel, ember + 2x luna, on one package: the RL arm and the Z0 control arm

One panel run is three reviewer sessions: `t2b-1` = `muse-ember-1.0`, `t4-1` and `t3-1` = `gpt-6-luna`, one attempt each (`NOFALLBACK=1`), run in parallel, blind to each other. The control arm Z0 is the isolated panel with H1 to H4 and CB-1 to CB-5 (no recipes, no ledger rule); the RL arm adds the ledger rule, the RL block and each reviewer's recipes. Run them in the same block, one after the other, on the same day. Planning elapsed time is about b + 28 s for RL and b for Z0 (b about 100 to 122 s on these packages; unmeasured).

```
export SW_SB_ROOT=/tmp/evalsb-recipe                # bin/rl-env.sh sets it too; the sibling uses /tmp/evalsb-sweep
DOC=TASK-WF-designSpec-20261107-075614             # one of the three study packages (see section 5.5 for all three); use a hold-out document id for a decision
bash $RL/bin/build-sandbox.sh $DOC                  # S0: base commit, no reflect, no reports (H3, H4); builds $SW_SB_ROOT/$DOC/repo and $SW_SB_ROOT/cand/$DOC/*

# 1. look before running: writes briefs and run.json, prints the three claude command lines with brief hashes, starts no model
bash $RL/bin/run-panel.sh --arm RL --panel primary --doc $DOC --replicate 1 --block 1 --seed 20261115 --run-id one-rl-dry --dry-run

# 2. the Z0 control arm (three model sessions)
bash $RL/bin/run-panel.sh --arm Z0 --panel primary --doc $DOC --replicate 1 --block 1 --seed 20261115 --run-id one-z0

# 3. the RL arm (three model sessions, plus one ember repair call only if its ledger is missing and the clock allows it)
bash $RL/bin/run-panel.sh --arm RL --panel primary --doc $DOC --replicate 1 --block 1 --seed 20261115 --run-id one-rl
```

What to read afterwards (no model):

```
jq '{arm,panel,fallback,no_source,c2_not_applicable,check_skipped,reask,row_cap}' $RL/runs/one-rl/run.json
jq . $RL/runs/one-rl/timing.json                  # panel_elapsed_s, slowest_reviewer_s, reask_s
jq . $RL/runs/one-rl/check/check.json             # ledger_missing, recipe_missing, over_budget, rows, demoted, promoted
jq -s '.[0].panel_elapsed_s / .[1].panel_elapsed_s' $RL/runs/one-rl/timing.json $RL/runs/one-z0/timing.json    # one-run sanity of the +35% rule (the gate itself is a median over a block)
sed -n 1,80p $RL/runs/one-rl/merged/merged-1.md   # the merged report
$PYRUN $RL/analysis/ran_check.py $RL/runs/one-rl  # REQ-28: ran status per row
```

Scoring (Opus, blind; owner go-ahead): `bash $RL/bin/judge-batch.sh --runs one-z0 one-rl` anonymises both merged reports, runs one blind judge each against the document's ground truth, and audits the judge outputs. A single pair of runs shows that the arm runs and what its ledger looks like; it is not evidence for or against adoption.

### 5.5 The three study packages (derivation-set check; reported, never used for a decision)

```
for DOC in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
  bash $RL/bin/build-sandbox.sh $DOC
  for ARM in Z0 RL; do
    bash $RL/bin/run-panel.sh --arm $ARM --panel primary --doc $DOC --replicate 1 --block 1 --seed 20261115 --run-id derive-$ARM-$DOC
  done
done
```

Six panel runs, 18 reviewer sessions, run one panel at a time. The other two control arms of `MR` run the same way: `--arm K` (Z0 plus the plain-words paragraph) and `--arm Z0-raw` (the current harness without the fixes; it needs `bin/build-sandbox.sh --raw $DOC` first).

### 5.6 E. Models: Stage 1 (decision)

```
E1  $PYRUN $RL/bin/make-schedule.py --stage 1 --arms z0,k,rl --docs HO-1,HO-2,HO-3,HO-4 --reps 5 --seed 20261115 --out $RL/runs/schedule-stage1.tsv
E2  $PYRUN $RL/bin/make-schedule.py --stage 1 --arms z0raw --docs HO-1,HO-2,HO-3 --reps 5 --seed 20261115 --append $RL/runs/schedule-stage1.tsv
E3  bash $RL/bin/run-schedule.sh $RL/runs/schedule-stage1.tsv             # at most 3 panels at once; refuses without the spike record (REQ-32)
E4  bash $RL/bin/judge-batch.sh stage1                                     # anonymise, one blind Opus judge per run, API-error audit; second judge on 15%
E5  $PYRUN $RL/analysis/analyze.py audit-judges stage1
E6  $PYRUN $RL/analysis/analyze.py all --stage 1 --out $RL/results/stage1  # metrics, D1-D7, stages.jsonl, shares, ran status, report.md
```

Counts. `MR` 5.4 gives Stage 1 as 95 panel runs for both redesigns (80 for the four arms Z0, K, SS and RL on four documents with 5 runs each, and 15 for Z0-raw). This build has no SS arm, so its schedule has 3 arms x 4 documents x 5 = 60 runs plus 15 Z0-raw = **75 panel runs** (225 reviewer runs), the same count as the sibling's own schedule. The 20 SS runs of `MR` are not part of it (`DESIGN.md` 12.1).

### 5.7 F. Models: Stage 2 (only for an arm that passes D1, D2 or D3 on Stage 1)

```
F1  planted set (6 plans, Z0 and RL, 3 runs):       $PYRUN $RL/bin/make-schedule.py --stage 2 --set planted --arms z0,rl --reps 3 ...        36 runs
F2  clean twins (6 plans, 2 runs):                  ... --set twins --arms z0,rl --reps 2 ...                                               24 runs
F3  specification HO-5 (5 runs):                    ... --set spec --arms z0,rl --reps 5 ...                                                10 runs
F4  documentation arm (8 documents, 3 runs):        ... --set docs --arms z0,rl --reps 3 ...                                                48 runs
F5  haiku panel (4 documents, 3 runs):              ... --set holdout4 --panel haiku --arms z0,rl --reps 3 ...                              24 runs
F6  sonnet panel (3 documents, 2 runs):             ... --set holdout3 --panel sonnet --arms z0,rl --reps 2 ...                             12 runs
F7  then, as E3 to E6 with --stage 2
```

Stage 2 without SS is 36 + 24 + 10 + 48 + 24 + 12 = **154 panel runs** (`MR` gives 231 with both redesigns). With Stage 1 the total is 75 + 154 = **229 panel runs**, about 687 reviewer runs (`MR`: 326 panel runs, about 978 reviewer runs, for both redesigns with one shared Z0 and K).

### 5.8 G. Decision

`analysis/analyze.py all` prints the outcome row of `MR` 5.8 for RL against Z0 and K: neither redesign passes means keep Z0; "RL beats K by at least 0.04" is gate D7; "K within 0.03 of RL" means the recipe wording adds nothing over plain words. A decision across both redesigns needs the sibling's results as well (DR-12). Adoption then follows its own plan (`IMPLEMENTATION.md` step 13).

## 6. Definition of done for the implementation

The implementation is done when all of the following hold, each shown by an output, not by a statement:

1. `$T $RL/tests -q -m "not slow and not freeze"` exits 0 and its summary line is saved to `RL/results/tests-final.log`; the same with `-m slow`.
2. `uv run --frozen --project $REPO ruff check $RL` and `ruff format --check $RL` exit 0.
3. `uv run --frozen --project $REPO pytest -p no:cacheprovider $REPO/tests/review -q` still exits 0.
4. `bash $RL/bin/copy-shared.sh --check` exits 0 and `config/shared-manifest.json` lists every shared file with its kind (`copied` or `built-local`) and sha256.
5. Every row of section 3 is either backed by a passing test or by an M record that exists on disk; the list of M records still open is printed by `bin/open-manual-checks.sh`.
6. `git status` shows no change under `src/`, `tests/`, `.claude/`, `.dev/tasks/` (other than the plan package that `/sc:workflow` created) or `SW` made by the implementation.
7. The rehearsal A7 of section 5.1 ran on the fake claude and its `FAKE_CALL_LOG` shows three review calls and no model.
8. `RL/IMPLEMENTATION-REPORT.md` exists and states what was built, the exact commands of section 5.4 for each of the three study packages for the RL arm and the Z0 arm, the test counts, which Tier B files were copied and which were built locally, and every requirement not met with the reason.
9. The freeze (`IMPLEMENTATION.md` step 11) has not been done before items 1 to 8 hold, and the freeze tests (`-m freeze`) pass.

What "done" does not mean: that Recipe Ledger works. Whether the recipes raise the found fraction is decided only by Stage 1 and Stage 2 (section 5), and the power of that experiment is low (`MR` 5.9): a pass is evidence, not proof.
