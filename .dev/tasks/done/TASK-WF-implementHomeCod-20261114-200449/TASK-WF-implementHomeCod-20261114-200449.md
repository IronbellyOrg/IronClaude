---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementHomeCod-20261114-200449
version: "1"
priority: Medium
created_date: "2026-11-14"
---

# Build the Sweep Sheet pre-pass, check, launcher and analysis (steps 1 to 13)

Source: ./source.md
Goal: Everything that DESIGN.md steps 1 to 13 of IMPLEMENTATION.md section 2 call for exists under the sweep-sheet folder, and `$T $SW/tests -q -m "not slow and not freeze"`, `ruff check`, `ruff format --check` and the `tests/review` baseline all exit 0, with no model started.

## Constraints

- Names used by every task. `SW` is the folder `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet` (repo-relative). Its three specification files are `SW/DESIGN.md`, `SW/IMPLEMENTATION.md` (section 2 holds the steps) and `SW/TESTING.md` (section 2 fixtures, section 3 requirement map, section 4 constraint tests). Section and row names in a task refer to those files. Test names written `file::function` live under `SW/tests/`. `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`, `RR` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`, `JJ` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/judge-one.sh`, `FND` is `src/superclaude/cli/review/findings.py`, `MRG` is `src/superclaude/cli/review/merge_cmd.py`, `LED` is `src/superclaude/cli/review/ledger.py`.
- Shell variables for every command, run from the repository root: `REPO="$(git rev-parse --show-toplevel)"`, `SW="$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet"`, `T="uv run --frozen --project $REPO pytest -p no:cacheprovider"`, `PYRUN="uv run --frozen --project $REPO python"`, and `export PYTHONDONTWRITEBYTECODE=1`. Python only through `uv run`; never `python -m`, `pip install` or bare `python script.py`.
- Git-write check. `gitcheck() { grep -rnE '\bgit\b[^|;&]*\b(add|commit|tag|push)\b' "$1" | grep -vE 'git -C "\$\{?SB[A-Za-z_]*\}?' | grep -vE ':[0-9]+:[[:space:]]*(#|echo|printf)'; }` prints nothing for a directory when no script in it runs `git add`, `commit`, `tag` or `push` except as `git -C "$SB..."` (a sandbox directory variable), in printed text or in a comment. A script that must read a tag uses `git rev-parse`, `git log` or `git for-each-ref`, never `git tag`. Tasks 8, 27 and 33 run it; Task 27 also shows it prints the probe line for a temporary file that holds `git add -A`, so the check is not vacuous.
- Write scope (DESIGN K1). Every file the build creates lives under `SW`. Scratch goes only to pytest `tmp_path` or `/tmp`; the sandbox root is `/tmp/evalsb-sweep`. `src/`, `tests/`, `.claude/` and every existing folder under `.dev/tasks/` are not touched. Evidence a task produces is written under `SW/results/`, not into this plan's package.
- Git scope. The build stages, commits and pushes nothing, and creates no tag (DESIGN K5). Staging of this plan's package stays with the session that runs `/sc:implement`. The sandbox builder's own `git init`, `git add` and snapshot commit run inside a throwaway sandbox under `/tmp` and are not repository writes; they are spelled `git -C "$SB..."`, which is how the git-write check (`gitcheck`, above) tells them from a write to the real repository.
- No model. No reviewer, judge or spike session is started. Every test that needs `claude` uses the fake `SW/tests/fakes/claude` (TESTING F-FAKE). Scripts that start models in real use (`bin/run-spike.sh`, `bin/run-schedule.sh`, `bin/judge-batch.sh`) are built and tested only against the fake.
- Never open any `ground-truth*.json` or score file. Tests marked `freeze` (the real-ground-truth lint, the recall tests) are written but not run by the build; the build runs `-m "not slow and not freeze"` plus `-m slow` where a task says so.
- Read-only imports. `FND`, `MRG` and `LED` are imported or called, never edited. `FND._check_finding` and `FND._blocks_after` are private; they are reached only through `SW/scaffold/fnd.py` (DESIGN section 2.3).
- Folder names. No folder is named `lib/` (`.gitignore` line 13 ignores it; DESIGN K7). Code folders are `scaffold/`, `sweep/` and `analysis/`.
- Decisions DD-1 to DD-15 of DESIGN section 1.3 hold as written; a conflict between this plan and DESIGN.md is settled by DESIGN.md. Step 0 is done (`SW/results/step0.md`); its sub-steps 0.4, 0.5 and 0.6 were not run, so the task that needs each one runs or reads it first (0.4 in Task 24, 0.5 in Task 26, 0.6 in Tasks 6 and 28). Step 0.3 measured a scope taken from IMPLEMENTATION.md, not the DD-5 scope; Task 23 measures the DD-5 scope.
- Out of scope: steps 14 to 16, Redesign 2, the optional verifier of `MR` 3.0.9, any change under `src/`, and any file under `fixtures/recall/` or `holdout-gt/`.
- Line counts in the design are planning values (unmeasured).

## Phase 1: Foundation and findings adapter

## Task 1: Create the folder layout, lint config, study config and path and model guards

Create under `SW`: `ruff.toml` (one line `extend = "../../../../pyproject.toml"`, four levels from `SW` to the repository root, same idea as `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/ruff.toml`), empty `scaffold/__init__.py`, `sweep/__init__.py`, `analysis/__init__.py`, `config/packages.json`, `config/panels.json` (three panels with caps 8/8/8, 6/9/9 and 6/9/9 as in DESIGN 7.1), `config/values.json` (planning values for `b` per panel and document, `c` per model, `kill_s`, `hang_s` inputs, `K` = 8, `K_single` = 12, `cap` = 12; DESIGN 12.7), and `bin/common.sh` with `sw_assert_writable`, `sw_assert_model`, `sw_assert_nofallback`, the path variables and `sw_py` (`uv run --frozen --project $REPO python`). Model allowlist per DESIGN K2: `muse-ember-1.0`, `gpt-6-luna`, `claude-haiku-5-5`, `claude-sonnet-5-5`; `claude-opus-5-5` only for `bin/judge-one.sh`. Create `tests/test_paths.py`, `tests/test_model_allowlist.py` and `tests/test_layout.py` (TESTING section 4 rows K1, K2, K7). The override guard (`sw_assert_override` in `bin/common.sh`, reused by `tests/conftest.py`) treats each override variable by its kind: the path variables `SW_SB_ROOT` and `SW_SRC_REPO` are refused unless they point under `/tmp/`; `SW_KILL_S` is accepted only as a number from 0.1 to 15 (so `1` passes, `9999` and text are refused); `SW_PREPASS_CMD` is accepted only when its first word is `sleep` or `false` (the stubs of the kill test), anything else is refused.

Acceptance criteria:
- `$T $SW/tests/test_paths.py $SW/tests/test_model_allowlist.py $SW/tests/test_layout.py -q` exits 0.
- `test_paths.py::test_refuses_output_outside_sw` shows a path under `REPO/src` or `REPO/tests` is refused with `E_NOT_WRITABLE`, and `::test_override_must_be_under_tmp` shows `SW_SB_ROOT` set to a path outside `/tmp/` is refused; `::test_kill_s_is_numeric_only` shows `SW_KILL_S=1` is accepted and `9999` and `abc` are refused; `::test_prepass_cmd_stub_only` shows `SW_PREPASS_CMD="sleep 5"` is accepted and `rm -rf x` is refused.
- `test_model_allowlist.py::test_reviewer_models`, `::test_opus_only_in_judge` and `::test_fable_and_tier0_refused` pass: `sw_assert_model` accepts exactly the four reviewer ids and refuses Opus, Fable, Qwen and glm.
- `test_layout.py::test_no_ignored_folder_names` passes: `git check-ignore` flags no folder under `SW` that holds code.
- `$PYRUN -c "import json,sys; [json.load(open(f)) for f in sys.argv[1:]]" $SW/config/packages.json $SW/config/panels.json $SW/config/values.json` exits 0, and the caps in `panels.json` sum to 24 for each panel; `test_layout.py::test_values_selection_constants` shows `values.json` holds `K` = 8, `K_single` = 12 and `cap` = 12.
- `ruff check` and `ruff format --check` on `SW` exit 0. Later tasks depend on `common.sh` (Tasks 8, 23, 27, 28, 32, 33) and on `config/panels.json` (Tasks 20, 26).

## Task 2: Create the pytest conftest, the fake claude and the fake-on-path test

Depends on: Task 1

Create `tests/conftest.py` (puts `SW` on `sys.path` as the r3 precedent's `conftest.py` does; provides the `tmp_roots` fixture, a `PATH` whose first entry is `tests/fakes`, and the override guard of Task 1) and `tests/fakes/claude` (TESTING F-FAKE): a script that reads the brief on stdin, picks a scenario from `FAKE_SCENARIO` (`ok`, `ledger_missing`, `long_anchor`, `api_error`, `wrong_model`, `sleep` using `FAKE_SLEEP_S`, `bad_block`, `exit127`), prints the JSON array of a real `claude -p --output-format json` run, and appends one line per call to `FAKE_CALL_LOG`. Create `tests/test_fake_on_path.py`. Register the markers `slow` and `freeze` in a `SW/pytest.ini`-free way (a `pytest_configure` hook in `conftest.py`, so no ini file outside the folder is needed).

Acceptance criteria:
- `$T $SW/tests/test_fake_on_path.py -q` exits 0 and fails when the first `claude` on `PATH` is not `tests/fakes/claude`.
- Calling the fake with each of the eight scenarios from a test prints valid JSON (or exits 127 for `exit127`) and `FAKE_CALL_LOG` gains one line per call.
- `$T $SW/tests -q -m "not slow and not freeze"` still exits 0 (Task 1 tests keep passing). The integration tests of Tasks 27, 28 and 32 use this fake.

## Task 3: Create the findings adapter and its contract tests

Depends on: Task 2

Create `scaffold/fnd.py`: the single import point for `FND`. It re-exports `parse_block`, `flat`, `locate`, `same_defect` and the private `_check_finding` and `_blocks_after` (signatures in `SW/DESIGN.md` section 2.3 and the grounding note: `_check_finding(obj, seen) -> str | None`, `_blocks_after(text, heading, info) -> tuple`), and adds `lenient_lines(report)`, which returns the raw JSON lines of the findings block even when some lines are invalid. Create `tests/test_fnd_contract.py` with signature pins for the private helpers, `test_merge_accepts_class_probe_src_keys` (REQ-11: runs `MRG.command` through click's `CliRunner` with `--ledger`, `--doc`, `--round 1`, `--report`, `--out` on a report whose findings lines carry `"class"`, `"probe"` and `"src"`, as step 0 check 3 did) and `test_existing_review_suite_passes` (runs `uv run --frozen --project $REPO pytest -p no:cacheprovider $REPO/tests/review -q` in a subprocess, the plan's `$T` form, so no cache folder is written outside `SW`).

Acceptance criteria:
- `$T $SW/tests/test_fnd_contract.py -q` exits 0.
- A rename or signature change of `_check_finding` or `_blocks_after` makes a pin test fail (shown by a test that inspects `inspect.signature`).
- `test_merge_accepts_class_probe_src_keys` shows exit code 0 and that neither the merged report nor the ledger file contains `"class"`, `"probe"` or `"src"` keys, matching `SW/results/step0.md` check 3.
- `$T $REPO/tests/review -q` still passes (126 tests at step 0): `FND` callers `parse_block`, `annotate` and `LED.merge_round` are untouched, and `git diff --stat -- src tests` is empty.

## Task 4: Create the H2 normaliser

Depends on: Task 3

Create `scaffold/normalise.py` (DESIGN 11.2 row H2, REQ-02): for each line of the single `findings-v1` block, cut `anchor` and `anchor2` to their first 200 flattened characters and `claim` to 300 (a prefix of an exact quote stays an exact quote), validate the result with `fnd.parse_block`, keep lines that still fail in `normalised/h2.json` under `unrepaired` (never dropped silently), and be idempotent. Create the F-REPORT fixtures `fixtures/reports/anchor_250.md` and `fixtures/reports/claim_301.md` (invented text) and `tests/test_normalise.py`.

Acceptance criteria:
- `$T $SW/tests/test_normalise.py -q` exits 0 with `test_anchor_250_survives`, `test_prefix_is_exact_quote`, `test_claim_301_cut`, `test_anchor2_cut`, `test_result_parses_ok` and `test_idempotent` present.
- After H2 the 250-character anchor is 200 flattened characters, is a prefix of the original, `fnd.locate` still finds it in the candidate, and `parse_block(...)["ok"]` is true; a second run changes nothing.
- The module imports only from `scaffold/fnd.py` for findings logic. Dependents to be built later that call it: `sweep/cli.py normalise` (Task 22), `bin/run-panel.sh` (Task 27) and the DD-9 order test (Task 27).

## Phase 2: Shared scaffolding: lint, cards, briefs, sandbox

## Task 5: Create the AO-1 leak lint

Depends on: Task 2

Create `scaffold/lint.py` (DESIGN 13.1 row AO-1, REQ-07): it fails on any four-word sequence found in the `description` or `plan_quote` of a ground-truth file, and on any name in the forbidden set (document ids, study and hold-out task titles, path tokens found in ground-truth text); it prints only file, line and a hash of the phrase, never the phrase. It reads ground truth only when a person passes `--gt-glob`. Create `tests/test_lint.py` with `test_seeded_leak_fails`, `test_clean_passes`, `test_forbidden_name_fails` and `test_fixtures_clean` (runs over `SW/fixtures/` and the folders that exist), all on small invented ground-truth and text files built in `tmp_path` by the tests themselves, plus the `freeze`-marked `test_real_files_against_real_gt` which is written and not run.

Acceptance criteria:
- `$T $SW/tests/test_lint.py -q -m "not freeze"` exits 0.
- A seeded leak in a temporary file makes the lint exit non-zero and its output holds the file, the line and a hash but not the phrase.
- No code in `scaffold/lint.py` opens a path unless `--gt-glob` is given; `grep -n "ground-truth" $SW/scaffold/lint.py` shows no hard-coded real path.
- Later tasks that run it over their files: Tasks 6, 7, 9, 10, 11 to 18 (fixtures and words), and `sweep/cli.py lint` (Task 22).

## Task 6: Create the class cards, their schema and the README

Depends on: Task 5

Read sections 2 and 5 of `.dev/brainstorms/20261113-223124-panel-process-redesign/enrichment/investigation-generality.md` (the instance register, `BR/enrichment/` in DESIGN 4.1) first; this is step 0.6. Create `cards/schema.json`, `cards/C1.json` to `cards/C8.json`, `scaffold/cards.py` and `cards/README.md`. Each card holds `id`, `name`, `version`, `definition` (from `MR` section 2, target neutral), `question_template` (the eight questions of `MR` 3.1(a), verbatim; only C3 has the `«value»` placeholder), `extractor`, `route` (C1 read, C2 read, C3 read, C4 search, C5 search, C6 search, C7 read, C8 search), `replicas` (2), `applies_to`, `instances` (at least two citations each from the register), `severity_guidance`, `known_weakness`, `promote_category` (one of the six `FND.CATEGORIES`; DD-11) and an empty `swap_test` record for the second author. `cards.py` exposes `load`, `validate`, `questions`, `routes`, `promote_category` and `definition`. The README holds the REQ-38 re-derive table with rows for block patterns, command dialect, test and root-document paths, severity guidance, location of truth and snapshot, for plan, specification and documentation (DESIGN 13.3). Create `tests/test_cards.py` (`test_schema_valid`, `test_each_card_has_two_instances`, `test_promote_category_valid`, `test_fixture_card_c9_needs_no_dispatcher_change`) and `tests/test_readme.py::test_readme_lists_rederive_rows`.

Acceptance criteria:
- `$T $SW/tests/test_cards.py $SW/tests/test_readme.py $SW/tests/test_lint.py -q -m "not freeze"` exits 0 and `test_fixtures_clean` covers `cards/`.
- Every card validates against `schema.json`, has at least two `instances` entries, and a `promote_category` that is in `FND.CATEGORIES`; no question states an expected outcome.
- A fixture card `C9` added in a test needs no change to `scaffold/cards.py` beyond data (REQ-10).
- Dependents: `scaffold/briefs.py` K paragraph (Task 7), the extractors' `route` and `class` (Tasks 11 to 18), `sweep/render.py` questions (Task 21), `scaffold/ledgerv1.py` promotion category (Task 25).
- The README footer names the second reader as an open manual check (TESTING REQ-38 row M); the `swap_test` records stay empty and are listed as open by Task 33.

## Task 7: Create the briefs and the brief renderer

Depends on: Task 6

Create `briefs/base.txt` (the text of `RR` lines 13-17 with `$CAND_SB` and `$SHA` as placeholders), `briefs/cb1.txt` to `briefs/cb5.txt` (the quoted blocks of `MR` at the lines named in DESIGN 8.1; CB-1 takes `{{SOURCE_ABS}}`), `briefs/ledger-rule.txt` and `briefs/sheet-block.txt` (quoted blocks of `MR`, the second with `{{SHEET_PATH}}`), and `briefs/k-lead.txt` (a draft lead-in, marked as awaiting owner approval, DD-14). Copy the quoted blocks with a one-time script written to `SW/results/` that prints the diff against the extraction used by the test. Create `scaffold/briefs.py` with `render(arm, doc, items, source)` joining the parts of DESIGN 8.1 in the fixed order, the K paragraph generated from the eight card `definition` fields, and a sha256 for every part and every rendered brief. Create `tests/test_briefs.py`.

Acceptance criteria:
- `$T $SW/tests/test_briefs.py -q` exits 0 with `test_cb1_rendered_with_source`, `test_cb1_absent_without_source`, `test_cb_verbatim_against_mr`, `test_arm_part_sets`, `test_base_equals_rr_lines_13_17`, `test_six_categories_unchanged`, `test_empty_sheet_brief_equals_z0_by_hash`, `test_fallback_brief_equals_z0_by_hash` and `test_no_src_path_in_any_brief`.
- The part sets of Z0-raw, Z0, K and SS equal those of DESIGN 8.1 (set equality); no part contains `src/superclaude/`; the first line `/sc:spec-panel @<candidate> --mode critique` is in every arm.
- `scaffold/briefs.py` is called by `sweep/cli.py brief` (Task 22) and `bin/run-panel.sh` (Task 27).

## Task 8: Create the sandbox builder and the test repository builder

Depends on: Task 2

Create `bin/build-sandbox.sh` by reading and adapting `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh` lines 1-59 (copy, do not import): `git archive <base>`, the H4 removals of DESIGN 11.2 plus every `artifacts/` folder, every `progress.md` and every path that contains a document id, `tree:<dir>` bases, `--raw` mode (DD-15), the post-build `grep`, `sandbox.json` with the tree hash, exit 2 `E_SANDBOX_DIRTY` for a modified sandbox, and the `SW_SRC_REPO` override guarded to `/tmp`. Write every git call that changes the sandbox as `git -C "$SBT" init -q`, `git -C "$SBT" add -A -f` and `git -C "$SBT" -c user.name=sw -c user.email=sw@localhost commit -q -m snap` (the precedent's `( cd "$T" && ... )` form is rewritten; `SBT` is the temporary sandbox directory), so that `gitcheck` passes. Create `fixtures/repos/build_repo.py` (TESTING F-REPO: `tests/`, `scripts/`, `docs/`, root files, `CHANGELOG.md`, a mirror copy, `.dev/` noise, `node_modules/` noise, an implementation commit that adds one file and edits another, and a trap file named `ground-truth.json`; returns base and head commits) and `tests/test_sandbox.py`.

Acceptance criteria:
- `$T $SW/tests/test_sandbox.py -q` exits 0 with `test_file_created_by_implementation_absent`, `test_masked_path_equals_base`, `test_tree_snapshot_kind`, `test_dirty_sandbox_refused`, `test_no_reflect_artifacts_progress`, `test_no_doc_id_in_paths_or_contents`, `test_no_ground_truth_file` and `test_raw_mode_removes_only_gt`.
- The trap `ground-truth.json` is absent from every sandbox; `.dev/reflect` is kept in `--raw` mode.
- `build-sandbox.sh` never writes outside `SB` and `/tmp` (`sw_assert_writable`), and `git status --porcelain` in a built sandbox is empty. `gitcheck $SW/bin` prints nothing: every `git add`, `commit`, `tag` and `push` in `bin/build-sandbox.sh` is `git -C "$SBT" ...`.
- The K4 post-run test file `tests/test_sandbox_clean.py` is created in Task 27, which runs the launcher. Dependents: `bin/run-panel.sh` (Task 27), the E2 to E4 `attach` tests (Tasks 12 to 14).

## Phase 3: The pre-pass (reader, extractors, selection, assignment, render, command)

## Task 9: Create the plan reader, format dictionaries, word lists and the two plan fixtures

Depends on: Task 5, Task 3, Task 2

Create `sweep/plan.py` (typed blocks `task`, `criterion`, `constraint`, `dictated_text`, `edit_target`, `gate`, each `{kind, id, text, line_start, line_end, task, phase}`, 1-based lines, anchors cut from the candidate; DESIGN section 3), `sweep/formats.py` (one dictionary each for `plan`, `spec` and `doc`; data only), `sweep/words.py` (set words, limiter words, edit verbs, dictation verbs, ordering verbs and the stop list; DESIGN section 4 describes them by category only, so the actual lists are written here, then linted), `fixtures/plans/p_basic.md` (TESTING F-PLAN-1: an invented report exporter and retention policy, 5 tasks, in the `workflow-plan` format, carrying a trigger for each of E1 to E7) and `fixtures/plans/p_clean.md` (F-PLAN-2: every criterion bounded). All fixture content is invented. Create `tests/test_plan.py` and `tests/test_formats.py::test_new_format_is_data_only`.

Acceptance criteria:
- `$T $SW/tests/test_plan.py $SW/tests/test_formats.py -q -k "not spec_fixture and not doc_fixture"` exits 0: each block kind is recognised in the `plan` format, unknown structure yields zero blocks and no exception, line numbers are right, an anchor cut from the candidate is found by `fnd.locate`, and unreadable bytes raise.
- `test_new_format_is_data_only` shows a format dictionary added in a test needs no change to any function in `sweep/plan.py`.
- `$T $SW/tests/test_lint.py::test_fixtures_clean -q` passes over the new files.
- Dependents: every extractor (Tasks 11 to 18) reads these blocks and word lists; `fixtures/plans/p_basic.md` and `p_clean.md` are the shared fixtures of Tasks 12 to 23 and 27.

## Task 10: Create the set-word plan generator and the specification and documentation fixtures

Depends on: Task 9

Create `fixtures/plans/gen_setwords.py` (TESTING F-PLAN-3: a plan with N set-word sentences, N = 200 for REQ-19, spread over criteria of 12 tasks, with a mix of completeness and universal words), `fixtures/specs/spec1.md` and `fixtures/specs/parent1.md` (F-SPEC: invented `shall` lines, an example block, an "Affects" list, and its parent requirement document) and `fixtures/docs/doc1.md` (F-DOC: a universal claim, a fenced command and a count).

Acceptance criteria:
- `gen_setwords.py` run with N = 200 through `$PYRUN` writes a plan that `sweep/plan.py` reads into at least 200 criterion sentences containing a set word (checked in a test added to `tests/test_plan.py`).
- `$T $SW/tests/test_lint.py::test_fixtures_clean -q` passes over all new files.
- `spec1.md` read with the `spec` dictionary yields `criterion`, `constraint` and `edit_target` blocks; `doc1.md` read with the `doc` dictionary yields `criterion` blocks and a fenced command block (checked in `tests/test_plan.py`).
- Dependents: `test_select.py` (Task 19), `test_formats.py::test_spec_fixture_e1_e2_e5` and `::test_doc_fixture_e4_e1` (Task 16).

## Task 11: Create the extractor core and the repository search helper

Depends on: Task 6, Task 8, Task 9

Create `sweep/extractors.py` with `Candidate` (fields of DESIGN 4.1), `Ctx` (parsed candidate, parsed source or `None`, snapshot root or `None`, scope, seed, constants), the registry `EXTRACTORS = {"E1": (find_e1, attach_e1), ...}` with the seven pairs registered as they are added, and `search(ctx, patterns, scope)`: one `git -C <snapshot> grep -n -I -F --no-color -f <patterns file> -- <pathspecs>` call per extractor with `LC_ALL=C`, at most 3 hits per file and the first 5,000 lines, the matched pattern of each line found by flat substring tests in Python, scope per DD-5 (tracked files under `tests/`, `scripts/`, `docs/`, root-level files, change-log style files, directories of plan-named paths, same-basename mirrors; `.dev/` and dependency folders excluded) kept as the string `Ctx.scope_string` (Task 22 writes it into `prepass.json`), and a raise when the snapshot is not a git repository. Implement the two-phase flow of DD-10 (`find` lexical, `attach` only for the top K candidates per class, every candidate logged with `dropped:pre_rank`): K = 8, or K_single = 12 when only one class has candidates after `find`, both read from `config/values.json` (DESIGN 5.1 step 2). The effect of 12 lookups on the time budget is unmeasured; the one-class attach work is bounded at 12 lookups. Create `tests/test_scope.py` and `tests/test_extractors_common.py`.

Acceptance criteria:
- `$T $SW/tests/test_scope.py $SW/tests/test_extractors_common.py -q` exits 0 with `test_dev_and_dependency_folders_excluded`, `test_named_paths_and_mirrors_included`, `test_scope_string_recorded` (the string is exposed as `Ctx.scope_string`; Task 22 asserts it in `prepass.json`), `test_attach_only_for_top_k`, `test_single_class_attaches_top_12` and `test_all_candidates_logged`.
- With 30 candidates in one class and some in a second class, 8 of the first have `evidence_computed`; with 30 candidates in one class and none in any other, 12 have it; in both cases all 30 appear in the candidate log (DD-10).
- The search helper never reads outside the snapshot root it was given, and a non-git snapshot raises.
- Dependents that register into the table: Tasks 12 to 18; `select.py` (Task 19) consumes `Candidate.status`.

## Task 12: Add extractor E2 (class C4)

Depends on: Task 11

In `sweep/extractors.py` add `find_e2` and `attach_e2` per DESIGN 4.3: backticked commands whose first word is `grep`, `egrep`, `rg`, `git grep`, `pytest` or `test`; ordered strings from task sentences with an ordering verb; the near-miss rule; the literal test (substring, or `re.search` after basic-to-extended conversion, else `pattern_kind = regex_unparsed` with no match line); evidence lines exactly as listed, including the pytest selector count read with `ast`; `pre_priority = 25 + 45*no_match + 20*near_miss`. Create `tests/test_e2.py`.

Acceptance criteria:
- `$T $SW/tests/test_e2.py -q` exits 0 with a positive case, a negative case, a near-miss case (heading `Retry policy` against pattern `retry-policy`, MATCH only after collapsing) and a determinism case on `fixtures/plans/p_basic.md` and `p_clean.md`.
- E2 emits no candidate on `p_clean.md`, and no evidence entry holds a claim, a severity or the word `defect`.
- Dependents: select (Task 19) reads `pre_priority` and `priority`; the printed-tool-output example of DESIGN 4.3 is reproduced by `render.py` (Task 21).

## Task 13: Add extractor E3 (class C8)

Depends on: Task 12

Add `find_e3` and `attach_e3` per DESIGN 4.4: one candidate per existing edit target (present in the snapshot, `creates: false`), features `stem_len` and `has_distinctive`, one batched `git grep -F -f` over the scope for every target path and stem, up to 5 unnamed referencing files with tests first, the `gate names:` line, and `priority = pre_priority + 15*min(unnamed_test_files, 3) + 5*min(unnamed_other_files, 2) + 10*(gate names NONE) - 20*(stem_hits > 40)`. Create `tests/test_e3.py`.

Acceptance criteria:
- `$T $SW/tests/test_e3.py -q` exits 0 with the four case kinds of Task 12, using `fixtures/repos/build_repo.py` (a test that names the edited file's stem and is not named by the plan is found).
- A stem that hits more than 40 files lowers priority by 20; E3 emits nothing on `p_clean.md`.
- Dependents: the same as Task 12.

## Task 14: Add extractor E4 (class C5)

Depends on: Task 13

Add `find_e4` and `attach_e4` per DESIGN 4.5: negative-claim triggers and count-change triggers, `needle` as the search string, one batched `git grep -F -f` over the scope, hits split into plan-named and plan-unnamed files (root documents and change logs first, then mirrors, then the rest, at most 5), the line `hits: <n> in <m> files (<k> named by the plan)`, and the priority formula of the section. Create `tests/test_e4.py`.

Acceptance criteria:
- `$T $SW/tests/test_e4.py -q` exits 0 with the four case kinds, including a count claim that a root document in `build_repo.py` repeats and a plan that names that document (priority bonus absent).
- An item with zero unnamed hits stays low rank and is dropped in a test with a full selection (checked in Task 19's tests).
- Dependents: select (Task 19), `fixtures/docs/doc1.md` test in Task 16.

## Task 15: Add extractor E1 (classes C1 and C6)

Depends on: Task 14

Add `find_e1` and `attach_e1` per DESIGN 4.2: sentence splitting, completeness and universal set words from `sweep/words.py`, `instr_scope` and `sent_scope` token sets (`NONE` when empty), bound types `closed_list`, `glob`, `count`, `none`, the two `find` kinds with their `pre_priority` formulas, and the two `attach` behaviours (side-by-side scopes for `completeness`; up to 3 limiter lines, the enforcing test file and its `def test_` count for `universal`). Items follow card C1 (route read) for `completeness` and card C6 (route search) for `universal`. Create `tests/test_e1.py`.

Acceptance criteria:
- `$T $SW/tests/test_e1.py -q` exits 0 with the four case kinds on `p_basic.md` (an unbounded set word beside a narrower instruction scope; a universal sentence beside a skip rule) and nothing on `p_clean.md`.
- The evidence shows both scopes side by side; a sentence shorter than 12 characters is ignored.
- Dependents: `test_formats.py` spec and doc tests (Task 16), select (Task 19).

## Task 16: Add extractor E5 (class C2) and the specification and documentation tests

Depends on: Task 10, Task 15

Add `find_e5` and `attach_e5` per DESIGN 4.6: runs only when a source exists, otherwise returns nothing and reports C2 as not applicable (`no_source`) through `Ctx` (Task 22 writes that into `prepass.json`); parse the `Source sections:` citations; rule sentences of cited sections; `missing` identifiers not found in the task body or criteria; tasks that cite nothing counted in `tasks_without_citations`; `pre_priority = 30 + 15*min(len(missing), 4)`. Create `tests/test_e5.py` (REQ-01 part `test_no_source_returns_nothing`) and add `test_spec_fixture_e1_e2_e5` and `test_doc_fixture_e4_e1` to `tests/test_formats.py` (REQ-37) over `fixtures/specs/spec1.md` with `parent1.md` and `fixtures/docs/doc1.md`.

Acceptance criteria:
- `$T $SW/tests/test_e5.py $SW/tests/test_formats.py -q` exits 0.
- E5 returns no candidate when the parent is removed from the spec fixture and when no source is given; each listed extractor yields at least one item on its fixture.
- Adding a format dictionary in `test_new_format_is_data_only` still passes with no extractor change.
- Dependents: select (Task 19), `bin/run-panel.sh` `no_source` flag (Task 27).

## Task 17: Add extractor E7 (class C7)

Depends on: Task 16

Add `find_e7` and `attach_e7` per DESIGN 4.8: constraint clauses split at semicolons, " and " and commas (clauses of 4 or more words), distinctive tokens of 4 or more characters not in the stop list and found in exactly one clause, a candidate for each (constraint, dictated block) pair that shares 2 or more distinctive tokens with one clause and none with another, the clause-by-text grid as evidence (at most 5 clauses), `pre_priority = 30 + 15*(zero-overlap clauses, at most 2) + 10*(shared tokens >= 2)`. Create `tests/test_e7.py`.

Acceptance criteria:
- `$T $SW/tests/test_e7.py -q` exits 0 with the four case kinds on `p_basic.md` (a constraint clause the dictated text omits) and nothing on `p_clean.md`.
- Priority range is 55 to 70 as in DESIGN 5.2 for every emitted candidate.
- Dependents: select (Task 19).

## Task 18: Add extractor E6 (class C3, experimental) and the recall test file

Depends on: Task 17

Add `find_e6` and `attach_e6` per DESIGN 4.7: a backticked literal in a read position (keys on, when, ==, is read, returns for, depends on) with no write-position occurrence anywhere in the candidate; `pre_priority = 20 + 5*min(read_count, 3)`; every item carries `experimental: true`. Create `tests/test_e6.py` and `tests/test_recall.py` (TESTING REQ-21, marker `freeze`: `test_recall_per_extractor`, `test_precision_reported`, `test_e6_marked_experimental`), which fails with the message "fixtures/recall missing" and never skips when `fixtures/recall/` is absent. `fixtures/recall/` itself is a step 14 deliverable and is not created.

Acceptance criteria:
- `$T $SW/tests/test_e6.py -q` exits 0 and every E6 item has `experimental: true`.
- `$T $SW/tests/test_recall.py -q -m freeze` is not run by the build; running only its collection (`--collect-only -m freeze`) lists the three tests.
- `$T $SW/tests/test_scope.py $SW/tests/test_extractors_common.py $SW/tests/test_e[1-7].py -q` (the IMPLEMENTATION step 7 command) exits 0 with all seven extractors registered in `EXTRACTORS`.

## Task 19: Create the rank table and the item selection

Depends on: Task 18, Task 10

Create `sweep/rank.py` (the weight table of DESIGN 5.2 as one dict plus its sha256, published as `rank_table_sha256`) and `sweep/select.py` (DESIGN 5.1: top K per class by `pre_priority` (K = 8, or K_single = 12 when only one class has candidates: the rule of Task 11, read from `config/values.json`), with ties by earlier plan line then `sha256(seed + anchor_text)`; pass A top item per class in the fixed class order C4, C8, C5, C2, C1, C6, C7, C3; pass B second item per class; pass C by `priority` with a per-class ceiling `ceil(12 / k)`; class C3 at most 1; `candidates.json` rows with `status` and drop reason; `items.json` rows `S1`, `S2`, ... in descending priority; seed recorded). Create `tests/test_select.py`.

Acceptance criteria:
- `$T $SW/tests/test_select.py -q` exits 0 with `test_200_setword_sentences` (using `fixtures/plans/gen_setwords.py`), `test_single_class_fills_12`, `test_fair_share_ceiling`, `test_class_order_and_ties` and `test_candidate_log_complete`.
- At most 12 items; every triggered class has at least 1; with `k >= 2` no class exceeds `ceil(12/k)`; with `k = 1` (one class has candidates) `attach` ran on that class's top 12 and the sheet holds 12 (1 when that class is C3; `test_single_class_fills_12` runs the two-phase flow of Task 11 on 30 invented candidates of one class); the same input and seed give the same selection; `candidates.json` has an entry for every candidate found (200 or more).
- Dependents: `sweep/assign.py` (Task 20), `sweep/prepass.py` (Task 22), `analysis/g0.py` (Task 31).

## Task 20: Create the item-to-reviewer assignment

Depends on: Task 19

Create `sweep/assign.py` per DESIGN 7: replica targets (1 for an item with empty evidence, otherwise 2; every item 1 when fewer than three reviewers), pass 1 (one reviewer per item in descending priority; search-route items to `S` when allowed and under cap, else the lighter luna), pass 2 (second reviewer, never the same as the first, `replica_dropped` when no one can take it), `dropped:cap_slots`, the haiku restriction (only evidence-bearing items of classes C4, C5, C8), caps read from `config/panels.json`, and per-reviewer order shuffled with `random.Random(f"{seed}:{rid}")`. Create `tests/test_assign.py`.

Acceptance criteria:
- `$T $SW/tests/test_assign.py -q` exits 0 with `test_caps_sum_24_all_panels`, `test_primary_12_items_fills_caps` (7 search and 5 read items end at loads 8, 8, 8), `test_haiku_only_evidence_items`, `test_no_evidence_replica_1`, `test_no_duplicate_reviewer_per_item`, `test_failure_never_raises_survivor_load`, `test_two_reviewers_replica_1` and `test_order_shuffled_per_reviewer_deterministic`.
- No reviewer load exceeds its cap, and every item keeps at least one reviewer or is logged `dropped:cap_slots`.
- Dependents: `sweep/render.py` (Task 21), `sweep/prepass.py` (Task 22), the reviewer-unavailable re-assign in `bin/run-panel.sh` (Task 27).

## Task 21: Create the sheet renderer

Depends on: Task 20

Create `sweep/render.py` per DESIGN 6: the item JSON with the fields and limits of 6.1, the question from the class card, `sheets/<rid>.md` in the shuffled order (header line `Items assigned to you:`, `### S<n>   (class C<n>)`, `Where:`, `Text:`, `Tool output:` with `none` when empty, `Question:`, the reply line), the `experimental` note, the class label only (never an extractor name, kind or priority), the 16,000-character cap that removes evidence entries from the lowest-priority items last entry first and records `sheet_trimmed: true`, and `sheets/<rid>.json`. Create `tests/test_render.py`.

Acceptance criteria:
- `$T $SW/tests/test_render.py -q` exits 0 with `test_sheet_text_in_brief_and_file_equal`, `test_sheet_cap_16000_trims_lowest_priority` (a 20-item overflow fixture) and `test_class_label_only_no_hint`.
- The sheet shows `C4` and never an extractor name, a priority or an expected outcome.
- Dependents: `scaffold/briefs.py` places the same text after `## SWEEP SHEET ITEMS` (Task 7 contract, exercised in Task 27); `sweep/prepass.py` (Task 22).

## Task 22: Create the pre-pass command and the sweep CLI

Depends on: Task 21, Task 7, Task 4

Create `sweep/prepass.py` (parse, find, top-K, attach, select, assign, render; takes exactly three inputs, the candidate, the source and the repository snapshot, plus seed; writes to `prepass.tmp/` and renames to `prepass/` only on success; no clock, no network, sorted lists, `sort_keys=True`, `ensure_ascii=False`, trailing newline, no absolute path inside any JSON; output files `items.json`, `candidates.json`, `assignment.json`, `prepass.json`, `prepass.log`, `sheets/*`; DESIGN 2.4) and `sweep/cli.py` with the subcommands `prepass`, `lint` (delegates to `scaffold/lint.py`), `brief` (delegates to `scaffold/briefs.py`) and `normalise` (delegates to `scaffold/normalise.py`); the `check` subcommand is added in Task 25 and is absent from the parser until then (not stubbed). Create `tests/test_prepass.py` (REQ-18 determinism) and `tests/test_prepass_inputs.py` (K3, REQ-34).

Acceptance criteria:
- `$T $SW/tests/test_prepass.py $SW/tests/test_prepass_inputs.py -q` exits 0 with `test_byte_identical_same_seed`, `test_other_seed_changes_only_order`, `test_no_absolute_paths_in_json`, `test_snapshot_unchanged`, `test_no_network_no_model`, `test_only_three_inputs`, `test_ground_truth_trap_not_read` (a read hook on `open` shows the trap file named like ground truth is never opened), `test_sheets_hold_no_gt_markers` and `test_scope_string_and_no_source_in_prepass_json`.
- Two runs with seed 1 give identical hashes for every file in `prepass/`; seed 2 changes only `assignment.json` and the sheet order, not the ids and statuses in `items.json` or `candidates.json` (TESTING REQ-18). `prepass.json` holds the scope string of Task 11 (REQ-24), and a run with no source file marks class C2 not applicable with `no_source` in `prepass.json` (REQ-01).
- `$PYRUN $SW/sweep/cli.py prepass --help` exits 0.
- Dependents: `bin/run-panel.sh` calls it under `timeout` (Task 27); `bin/time-prepass.sh` (Task 23); `analysis/g0.py` reads its `candidates.json` (Task 31).

## Task 23: Create the pre-pass timing script, kill fallback test and the time checkpoint

Depends on: Task 22

Create `bin/time-prepass.sh` (runs `sweep prepass` on a given snapshot and prints and records the seconds) and `tests/test_prepass_timing.py::test_largest_tree_under_kill_limit` (marker `slow`, REQ-24). The kill-and-fallback tests of REQ-18 need the launcher, so `tests/test_kill_fallback.py` is created in Tasks 26 and 27, not here (a re-split of IMPLEMENTATION step 9). Run the checkpoint of IMPLEMENTATION step 9: `bin/time-prepass.sh` on the repository root and on two smaller snapshots, with the DD-5 scope, and write the seconds into `config/values.json` as `prepass_s` and into `SW/results/prepass-timing.md`.

Acceptance criteria:
- `$T $SW/tests -q -m slow` exits 0 and `bash $SW/bin/time-prepass.sh --help` exits 0.
- `SW/results/prepass-timing.md` holds three measured numbers for S1 and the scope string used; `config/values.json` holds `prepass_s`.
- If S1 on the repository root is over 10 s, this task is reported blocked with the number, DD-5 and DD-10 are named as the items to revisit (IMPLEMENTATION step 9 checkpoint), and later tasks are not started.
- Dependents: the `prepass_s` and kill limit in `scaffold/clock.py` (Task 26) and the fallback path of `bin/run-panel.sh` (Task 27).

## Phase 4: The post-run check

## Task 24: Create the ledger-v1 reader, the four checks, linking and demotion

Depends on: Task 3, Task 6, Task 22

First run step 0.4: with `jq`, list the event types and the `tool_result` shape of one finished `*.attempt1.json` of each reviewer model (luna, haiku, sonnet, ember) under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` `<doc>/reviews/combos/`; open no ground-truth or score file; record the shapes in `SW/results/transcript-shapes.md`. Then create `scaffold/ledgerv1.py` (reader of DESIGN 9.1: heading regexes, one `ledger-v1` block between `## Ledger` and `## Findings block` found through `fnd._blocks_after`, format errors counted with line numbers, case-insensitive verdicts, limits, `unknown_item`, `dup_line`; checks 1 to 4 of 9.2 with the corpora `source`, `candidate`, `sheet`, `transcript` of DD-2; linking by `probe` or by quote; demotion causes `row_unsupported`, `row_unsure`, `no_cb3`, `row_missing` for linked findings only (DD-3, switch `CHECK_SCOPE=linked|all`); the CB-3 sentence rule) and the F-REPORT and F-TRANSCRIPT fixtures listed in TESTING section 2 (`good`, `ledger_missing`, `ledger_after_findings`, `ledger_twice`, `ledger_unclosed`, `findings_unclosed`, `findings_twice`, `bad_json_line`, `quote_wraps_line`, `unknown_item`, `dup_line`, `ok_but_finding`, `unsure_with_blocking`, `blocking_no_cb3`, `blocking_with_cb3_near_id`, `verdict_lowercase`, with minimal `*.attempt1.json` transcripts). Create `tests/test_ledgerv1.py`.

Acceptance criteria:
- `$T $SW/tests/test_ledgerv1.py -q -k "not promotion and not class_key"` exits 0 with `test_misplaced_duplicated_truncated_blocks`, `test_fence_opener_grep_is_not_used`, `test_quote_wrapping_a_plan_line_matches`, `test_unsupported_row_demotes_linked_finding`, `test_unsure_never_blocks`, `test_blocking_needs_cb3_and_two_quotes_or_search`, `test_unlinked_finding_untouched`, `test_check_scope_all_switch_off_by_default` and `test_quote_other_corpora`.
- A plan-versus-plan row whose second quote is from the candidate passes; a quote in none of the four corpora fails; an unlinked blocking finding stays blocking in the default scope.
- `SW/results/transcript-shapes.md` exists and names the `tool_result` shape for each of the four models, or states which model had no finished run on disk.
- Dependents: promotion and telemetry (Task 25), `analysis/analyze.py` act-rate reading (Tasks 29 and 30).

## Task 25: Create promotion, telemetry and the check subcommand

Depends on: Task 24

Extend `scaffold/ledgerv1.py` with promotion (DESIGN 9.3: a `PROBLEM` row with no linked findings line becomes a `MINOR`, non-blocking line with id `P<item>` plus a numeric suffix if used, `category` from the card's `promote_category`, `anchor` = `quote_plan`, `claim` = `problem` unchanged, `refs` empty, telemetry `class`, `probe`, `src: ledger`; validated with `fnd._check_finding`; inserted as the last line inside the one existing block; failures to `check.json: promotion_failures`; `block_unusable` when the block is missing, unclosed or duplicated). Create `scaffold/telemetry.py` (`class`, `probe`, `src`, per-class tables; DD-12: reviewers set only `probe`, the check fills `class` and corrects a wrong one) and add the `check` subcommand to `sweep/cli.py` (raw report in, `check/<rid>.checked.md`, `check/<rid>.ledger.json` and `check/check.json` out, with every field of DESIGN 9.4 including `format_induced_demotions`; any exception is caught by the caller and sets `check_skipped`). Create the four F-REPORT fixtures `fixtures/reports/problem_no_finding.md`, `promote_long_id.md`, `promote_short_anchor.md` and `promote_dup_id.md` (invented text; TESTING section 2), create `tests/test_check_flow.py`, and add the promotion and `test_class_key_added_from_item` tests to `tests/test_ledgerv1.py`.

Acceptance criteria:
- `$T $SW/tests/test_ledgerv1.py $SW/tests/test_check_flow.py -q` exits 0 with `test_promotion_copies_problem_and_anchor`, `test_promotion_validates_with_check_finding` (long id, short anchor, duplicate id), `test_promotion_inside_single_block`, `test_promotion_failure_logged_and_skipped` and `test_class_key_added_from_item`.
- The raw `reviews/<rid>.md` is never edited; promoted findings are counted apart from reviewer findings in `check.json`.
- `$PYRUN $SW/sweep/cli.py check --help` exits 0.
- The four fixtures exist and each promotion test reads its own (`promote_long_id.md`, `promote_short_anchor.md`, `promote_dup_id.md`; `problem_no_finding.md` for `test_promotion_copies_problem_and_anchor`), and `$T $SW/tests/test_lint.py::test_fixtures_clean -q` passes over them.
- Dependents: `bin/run-panel.sh` S5 step with the `check_skipped` catch (Task 27), `analysis/analyze.py` metrics `non-probe findings` and `stages.jsonl` (Tasks 29 and 30).

## Phase 5: The launcher and the clock

## Task 26: Create the clock helper and the clock, hang guard and kill formula tests

Depends on: Task 23

First run step 0.5: time `$PYRUN -c "import superclaude.cli.review.findings"` five times and write the five times and their median into `SW/results/import-time.md` (one earlier run measured 0.28 s; DESIGN 12.1 plans 1 s for S5 including start-up). Then create `scaffold/clock.py` with `kill_s` (`min(15, 0.10 b)`), `hang_s` (`1.5 * (b + expected_overhead)`; overhead 29 s for SS on the ember panel, 37 s haiku, 31 s sonnet, 0 for other arms), `breakeven` (pre-pass 14.0 s and 2.75 s per item for `n = 8` at `b = 100`; about 21.7 s and 3.71 s at `b = 122`), `no_budget` (refuse an SS start when `0.35 b - 13` is under 8 s), and the panel-elapsed arithmetic of DESIGN 11.4 (`t0`; SS: end of S5 minus `t0`; other arms: last reviewer end minus `t0`; H2, merge, judge and verifier outside the clock). Add the launcher inputs (`b`, overhead) to `config/values.json`. Create `tests/test_clock.py` (REQ-29), `tests/test_hang_guard.py::test_formula_per_panel` (REQ-30) and `tests/test_kill_fallback.py` with `test_kill_formula` only (Task 27 adds the rest).

Acceptance criteria:
- `$T $SW/tests/test_clock.py $SW/tests/test_hang_guard.py $SW/tests/test_kill_fallback.py -q` exits 0.
- `kill_s(b)` returns 10.0 for 100, 12.2 for 122 and 15.0 for 200 (`test_kill_formula`).
- The guard is 193.5 s for the primary panel at `b = 100` (1.5 x 129), 385.5 s for haiku at 220, 435 s for sonnet at 259 and 150 s for Z0 at 100.
- `test_panel_elapsed_ss_and_other_arms` and `test_clock_starts_before_prepass` pass with a fake clock; `breakeven(b=100)` returns pre-pass 14.0 and 2.75.
- `SW/results/import-time.md` holds five measured times and their median; if the median is over 1 s the file says so next to the 1 s S5 value (a note, not a block).
- Dependents: `bin/run-panel.sh` (Task 27), `test_report.py::test_breakeven_values` (Task 30), `test_verifier_off_path.py` (Task 30).

## Task 27: Create the reviewer and panel launchers and the fake-claude integration tests

Depends on: Task 26, Task 25, Task 8, Task 7, Task 4

Create `bin/run-reviewer.sh` as the changes against `RR` listed in DESIGN 11.1: writes under `RUN/reviews`, candidate and source from `SB/cand/<doc>/`, brief from a file on stdin, `NOFALLBACK=1` required and one attempt (DD-8; no model ladder, no retry), `cd SB/<doc>/repo`, `timeout <hang guard>`, the same flags as `RR` line 48 (`--no-session-persistence`, `--permission-mode bypassPermissions`, `--disallowedTools Edit Write NotebookEdit`), the model-identity check kept, `BLOCK_OK` from `fnd.parse_block` after H2 on a temporary copy, `meta.json` and `cost.json` with `hang_s`, `killed` and `prompt_sha256`. Create `bin/run-panel.sh` (arms Z0-raw, Z0, K and SS: S0 sandbox check, S1 under `timeout` at `kill_s`, brief render, three reviewers in parallel with the hang guard, S5 under a catch that sets `check_skipped`, H2, the real `superclaude review merge` (`MRG.command` through the `superclaude review merge` command) with `resolution.json`, `run.json`, `timing.json`, the fallback decision taken before any reviewer starts, the `git status --porcelain` before and after every run, the reviewer-unavailable re-assign, and the `VERIFIER` default 0). Create `tests/test_run_panel_fake.py`, `tests/test_sandbox_clean.py` and `tests/test_blindness.py`, and extend `tests/test_kill_fallback.py` (from Task 26) with `test_sleeping_stub_is_killed_and_falls_back` (`SW_PREPASS_CMD=sleep 5`, `SW_KILL_S=1`: the process group is killed after about 1 s, no `prepass/` folder remains, the Z0 brief is used with an equal sha256, `run.json` has `fallback: true` and `reason: kill`) and `test_forced_exception_in_prepass_and_render_falls_back`.

Acceptance criteria:
- `$T $SW/tests/test_run_panel_fake.py $SW/tests/test_sandbox_clean.py $SW/tests/test_kill_fallback.py $SW/tests/test_blindness.py -q` exits 0, and `$T $SW/tests/test_clock.py $SW/tests/test_hang_guard.py -q` still exits 0.
- `test_run_panel_fake.py` has `test_prepass_finishes_before_first_reviewer`, `test_no_trigger_run` (reviewer brief hashes equal the Z0 hash, `no_trigger: true`), `test_sleeping_reviewer_killed`, `test_no_retry_on_failure` (`FAKE_CALL_LOG` shows one call per reviewer), `test_killed_reviewer_absent_from_merge`, `test_forced_exception_in_check_merges_as_written` (`check_skipped: true`, raw text given to the merge), `test_order_s5_then_h2_then_merge` and `test_no_source_run` (a document whose `source` is null: `run.json` has `no_source: true` and no brief holds the CB-1 text), and all pass with the fake `claude`.
- `test_sandbox_clean.py::test_dirty_after_run_is_flagged` shows a fake reviewer that writes a file in the sandbox makes the run `sandbox_dirty`; `test_blindness.py::test_merged_report_has_no_telemetry_keys` shows `merged-1.md` and `merged/ledger.json` contain none of `probe`, `src`, `class` or `ledger-v1`.
- `grep -rn "claude-opus-5-5" $SW/bin $SW/sweep $SW/scaffold` hits only `bin/judge-one.sh` once Task 28 exists (Task 33 re-runs it). `gitcheck $SW/bin` (Constraints) prints nothing over the scripts that exist after this task, `bin/build-sandbox.sh` passing because its writes are `git -C "$SBT" ...`; run over a temporary directory holding a file with the line `git add -A` it prints that line (the probe), and Task 33 re-runs it over the finished `bin/`.
- Dependents: `analysis/analyze.py` reads `run.json` and `timing.json` (Tasks 29 and 30), `bin/run-schedule.sh` and `bin/run-spike.sh` call `bin/run-panel.sh` (Task 32).

## Phase 6: The judge copy, analysis and the offline gate

## Task 28: Create the judge scripts and the anonymiser

Depends on: Task 2, Task 7

Read `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/anon-b11.sh` first (step 0.6) and note its redaction rules in `SW/results/anon-rules.md`. Create `bin/judge-one.sh` (a copy of `JJ` with paths turned into variables `EVAL`, `D`, `GT`, `CAND`; the `BRIEF` text of `JJ` lines 12-23 byte-identical; model `claude-opus-5-5`, the only place it appears), `bin/anon.sh` (random label, reviewer ids replaced by `R1` to `Rn`, paths redacted, per the rules noted), `bin/judge-batch.sh` (anonymise, one blind judge per run, API-error audit, 15% second-judge sample; started only against the fake in tests). Create `tests/test_judge.py` (REQ-43) and `tests/test_anon.py`.

Acceptance criteria:
- `$T $SW/tests/test_judge.py $SW/tests/test_anon.py $SW/tests/test_briefs.py -q` exits 0, with `test_briefs.py::test_judge_brief_sha_equals_jj` added to `tests/test_briefs.py` here, and with `test_judge_brief_sha`, `test_model_is_opus_only_in_judge`, `test_audit_flags_error_with_score_file`, `test_second_judge_sample_15_percent_seeded` (`round(0.15 n)` runs, repeatable for a fixed seed) and `test_audit_counts_match_merged_rows`.
- The sha256 of the `BRIEF` text in `bin/judge-one.sh` equals that of `JJ` lines 12-23.
- No test or script opens a file named `ground-truth*.json` or a real score file; judge tests use synthetic judge folders only.
- Dependents: `analysis/analyze.py audit-judges` and `sample-second-judge` (Task 30).

## Task 29: Create the synthetic run folders and the analysis script core

Depends on: Task 27, Task 25

Create `fixtures/gt/synthetic-gt.json` (TESTING F-GT: invented ground-truth items with `id`, `class`, `blocking_in_implement`, `description` and `plan_quote` for `fixtures/plans/p_basic.md`; invented, not from any study file) and `fixtures/runs/make_runs.py` (TESTING F-RUNS: synthetic run folders for 3 arms, 2 documents and 5 replicates with known found sets, timings, flags and scores; `expected.json` written by hand-written arithmetic, not by calling `analyze.py`) and `analysis/analyze.py` with the per-arm and per-document metrics of DESIGN 14.3: found fraction per run, share of runs finding at least half the items, run-to-run Jaccard, stable-hit rate, wrong blockers per run, found-any against found-blocking, non-probe findings per run (excluding lines with `probe` set and lines with `src: ledger`), elapsed mean and median, tokens, kills, retries, fallbacks, `invalid`, per-class reach with Wilson intervals, consistency (items reached in 60% of runs). Every metric name is defined only in this file. Create `tests/test_analyze.py`.

Acceptance criteria:
- `$T $SW/tests/test_analyze.py -q` exits 0 with `test_metrics_match_expected_json`, `test_one_definition_of_found_fraction` (an AST search over `SW` finds the metric names defined only in `analysis/analyze.py`), `test_d1_uses_medians`, `test_d1_same_block_only`, `test_mean_and_median_reported`, `test_kills_retries_per_arm`, `test_zero_findings_for_killed`, `test_nonprobe_findings_per_run`, `test_promoted_lines_not_counted_as_reviewer_findings`.
- `analysis/analyze.py` reads only run folders, judge outputs and `config/`, and writes `results/metrics.json`; a Z0 run from another block is ignored or raises.
- `$T $SW/tests/test_lint.py::test_fixtures_clean -q` passes over `fixtures/gt/` and `fixtures/runs/`.
- Dependents: gates, shares and reports in Task 30; `analysis/g0.py` reads `fixtures/gt/synthetic-gt.json` (Task 31).

## Task 30: Add the gates, shares, stage rows, preregistration and report to the analysis script

Depends on: Task 29, Task 28, Task 26

Extend `analysis/analyze.py` with the subcommands `all`, `audit-judges`, `compliance`, `prereg` and `sample-second-judge` and the outputs of DESIGN 14.3: gates D1 to D7 with a bootstrap that resamples documents first and then runs, the three shares (`Z0 - Z0raw`, `K - Z0`, `SS - Z0`) as three labelled lines never summed, `stages.jsonl` rows with the five stage fields (extraction, selection, act, merge survival read from `merged/ledger.json` through `(reviewer_id, finding id)`, judge credit), `ok_rate_planted.json`, `judge_audit.json`, the break-even values (planned and measured side by side), the DD-7 count of `## Ledger` headings in Z0 and K reports, the REQ-45 claim sentence, the D6 blocking rule and `prereg --write` with `prereg.json` carrying a band `[lo, hi]` with `0 <= lo < hi <= 1` for each of C1 to C8. Create `tests/test_report.py`, `tests/test_stages.py`, `tests/test_prereg.py` and `tests/test_verifier_off_path.py`.

Acceptance criteria:
- `$T $SW/tests/test_report.py $SW/tests/test_stages.py $SW/tests/test_prereg.py $SW/tests/test_verifier_off_path.py $SW/tests/test_analyze.py -q` exits 0.
- Required tests present: `test_three_shares_separate`, `test_no_summed_headline`, `test_breakeven_values`, `test_report_shows_planned_and_measured`, `test_claim_template_text`, `test_stage_rows_schema`, `test_stage_values_on_fixture`, `test_act_bands_for_all_classes`, `test_d6_failure_blocks_adoption`, `test_no_verifier_step_in_clock`, `test_verifier_default_off` and `test_verifier_time_excluded`.
- `breakeven(b=122)` prints about 21.7 s and 3.71 s; the claim sentence equals the REQ-45 sentence and no other sentence uses "consistent" for another class; a fixture where D2 and D3 pass and D6 fails gives "do not adopt".
- `analysis/analyze.py` never reads a `ground-truth*.json`; `stages.jsonl` takes the ground-truth path as an argument and tests pass only the synthetic one. Dependents: `bin/make-schedule.py` and `bin/check-order.sh` read the `prereg.json` it writes (Tasks 32 and 33).

## Task 31: Create the offline selection-recall gate

Depends on: Task 29, Task 22

Create `analysis/g0.py` per DESIGN 14.1: `covers(item, gt)` (flattened `plan_quote` contains or is contained in the item's `anchor_text`, or line spans within 3 lines via `fnd.locate`, the rule of `FND.same_defect`), extraction recall and selection recall pooled and per class, random baseline (a) with 2,000 seeded draws of 12 candidates, baseline (b) inside the fair-share structure, the floor read from `config/prereg.json` (the recommended 0.45 is an owner decision and is not written by this task), the pass rule (selection recall at or above the floor and the rank beats baseline (a) with at most 10% of draws at or above it), and `--ablate` (leave-one-class-out, pass limit 15 points). Create `tests/test_g0.py`.

Acceptance criteria:
- `$T $SW/tests/test_g0.py -q` exits 0 with `test_recall_definitions`, `test_covers_by_span_within_3`, `test_random_baseline_deterministic`, `test_gate_pass_and_fail` (passes at floor 0.4, fails at 0.99 on the same data) and `test_ablation_report_synthetic`.
- The tests use `fixtures/gt/synthetic-gt.json` and `fixtures/plans/p_basic.md` only; `g0.py` opens a ground-truth file only for a path given on its command line.
- `$PYRUN $SW/analysis/g0.py --help` exits 0. Dependents: the offline gate B3 and B6 commands of TESTING section 5 (run in step 14, not here).

## Phase 7: Schedule, spikes, freeze and order scripts

## Task 32: Create the schedule maker, the schedule runner and the spike script

Depends on: Task 27, Task 30

Create `bin/make-schedule.py` (block-randomised `schedule.tsv`, one block per replicate, recorded seed, the stage and set options of TESTING section 5, 75 panel runs for Stage 1 as designed: 3 arms x 4 documents x 5 plus 15 Z0-raw), `bin/run-schedule.sh` (at most 3 panels at once, `concurrent_panels_at_start` logged, refuses to start without a spike record of 5 runs and a `c_luna` in `config/values.json`; sets 6 items per luna and ember cap 12 when `c_luna > 2.75` at `b = 100`) and `bin/run-spike.sh` (modes `timing` and `compliance`; written for the owner's later go-ahead, run here only against the fake). Create `tests/test_run_schedule.py`.

Acceptance criteria:
- `$T $SW/tests/test_run_schedule.py -q` exits 0 with `test_refuses_without_spike_record` (non-zero exit without a record, starts with one, and applies the 6-item fallback when `c_luna > 2.75`).
- `$PYRUN $SW/bin/make-schedule.py --stage 1 --arms z0,k,ss --docs HO-1,HO-2,HO-3,HO-4 --reps 5 --seed 20261115 --out /tmp/sweep-schedule-check.tsv` writes 60 rows and the Z0-raw append command adds 15, for 75 in all.
- No script in this task starts a real model during the build; the real spikes are step 15.
- Dependents: none inside the build; the commands appear in TESTING section 5 C and D.

## Task 33: Create the freeze, order, sandbox-ground-truth and open-checks scripts, then run the build checkpoint

Depends on: Task 32, Task 31, Task 30

Create `bin/freeze.sh` (hashes of cards, extractors, words, formats, rank table and briefs into `config/freeze.json`; prints the `git tag` command with `echo` or `printf` only; never runs it), `bin/check-order.sh` (`freeze` and `prereg` modes comparing commit times of the freeze tag, the ground-truth commit, `prereg.json` and the first `run.json`, reading the tag with `git rev-parse` or `git log`, never `git tag`), `bin/check-sandbox-gt.sh` (a `grep -r` for ground-truth file names and field names over every `SB/<doc>/repo` and every `RUN/prepass/sheets`) and `bin/open-manual-checks.sh` (lists the M records of TESTING section 3 still open: the `swap_test` records, `fixtures/recall/AUTHORS.md`, attestations, the README second-reader record). Create `tests/test_freeze.py` (K5: `test_freeze_prints_but_never_tags`) and `tests/test_order.py` (REQ-33, REQ-36, REQ-44: `test_freeze_tag_before_gt_commit`, `test_gt_before_tag_fails`, `test_freeze_json_hashes_match_files`, `test_gt_hash_matches_prereg`, `test_every_planted_plan_has_twin`, `test_prereg_commit_before_first_run`). Then run the build checkpoint of IMPLEMENTATION section 2 (after step 13) and save its output.

Acceptance criteria:
- `$T $SW/tests/test_freeze.py $SW/tests/test_order.py -q` exits 0, and `git tag -l` is unchanged after `bin/freeze.sh` runs in the temporary repository of the test.
- `$T $SW/tests -q -m "not slow and not freeze"` exits 0 and its summary line is saved to `SW/results/tests-final.log`; `$T $SW/tests -q -m slow` exits 0.
- `uv run --frozen --project $REPO ruff check $SW` and `uv run --frozen --project $REPO ruff format --check $SW` exit 0; `$T $REPO/tests/review -q` exits 0.
- `git status --porcelain -- src tests .claude` prints nothing, and under `.dev/tasks/` the only entries are this plan's own package folder (plan, source snapshot, contract, grounding note and the executor's ledger); no other `.dev/tasks/` folder changed.
- `bash $SW/bin/open-manual-checks.sh` prints the open manual records, and `SW/results/open-manual-checks.txt` holds that output; the freeze (step 14) has not been done.
- `bash $SW/bin/check-sandbox-gt.sh` exits 0 with no output over the sandboxes the tests built.
- `gitcheck $SW/bin` (Constraints) prints nothing over every script of the finished `bin/`, and `grep -rn "claude-opus-5-5" $SW/bin $SW/sweep $SW/scaffold` hits only `bin/judge-one.sh`; this re-runs the checks that Task 27 first runs.
