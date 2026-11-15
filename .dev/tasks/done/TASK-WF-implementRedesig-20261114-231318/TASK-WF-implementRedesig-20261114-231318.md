---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementRedesig-20261114-231318
version: "1"
priority: Medium
created_date: "2026-11-14"
---

# Implement Redesign 2 (Recipe Ledger) of the tasklist review panel under the recipe-ledger eval folder

Source: ./source.md
Goal: A tested, no-model build of Recipe Ledger exists under RL: recipes, lens table and render, ledger row check, ember re-ask, launcher with the RL, Z0, K and Z0-raw arms, judge copy, analysis, schedule and freeze scripts, a copy of the shared sibling pieces with recorded hashes, a passing test run, and an IMPLEMENTATION-REPORT.md that states what was built, the exact one-panel commands, test counts and every requirement not met.

## Constraints

Path names used by every task (all repo-relative to the checkout root `REPO`, which is `git rev-parse --show-toplevel`):

- `RL` is `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger`. It holds `DESIGN.md`, `TESTING.md`, `IMPLEMENTATION.md` and `SHARED-MANIFEST-DESIGN-TIME.tsv`, which are the specification and are never edited by the build.
- `SW` is `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`, the sibling build (Redesign 1). It is read only: no task writes, edits, moves or deletes anything under it, and no task runs a script or a test from inside it.
- `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (sections 3.0, 3.2, 5 and 6 are the requirements source; the design documents already map them). `EVAL` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only).
- Design ids: `K1` to `K9` (constraints), `DR-1` to `DR-16` (decisions) and `REQ-nn` (requirements) are those of `RL/DESIGN.md` sections 1.2 and 1.3 and of `RL/TESTING.md` section 3.

Scope rules that hold for every task:

- Create or edit files only under `RL`, plus scratch under `/tmp` (sandboxes under `/tmp/evalsb-recipe`, scratch under `/tmp/rl-*`). Nothing under `src/`, `tests/`, `.claude/`, any existing folder under `.dev/tasks/`, `SW`, `EVAL`, `.dev/eval-workspaces/tasklist-review-panel/20261113-collab` or any other folder is changed.
- No task runs `git commit` or `git push`, and no task runs `git add` for a path under `RL`. The freeze tag (K5) is only printed, never created.
- No task opens, reads, greps the content of or copies any `ground-truth*.json`, score file or judge output of a study package, and no recipe, card, brief, fixture, regex or example uses a study answer. Fixtures are invented. Tests that need ground truth use the synthetic `RL/fixtures/gt/` files only. The tests marked `freeze` (they read the real ground truth or need a second author's records) are never run by this build.
- Python runs only through uv. No `python -m`, no bare `pip`. No code folder is named `lib/` (K7).
- No reviewer or judge session is started and no network call is made. Tests use the fake `claude` at `RL/tests/fakes/claude`. If a task ever needed a model it would use `claude-sonnet-5-5` or `claude-haiku-5-5`; Opus is only the blind judge script's model; never Qwen or glm.
- Files under `RL/scaffold/`, `RL/cards/`, `RL/briefs/`, `RL/bin/common.sh`, `RL/bin/build-sandbox.sh` and the copied tests are copies of sibling files and are never edited after the copy (DESIGN 3.1). A copied test that fails is reported, not edited.
- Shell variables used in task commands:

```
REPO=$(git rev-parse --show-toplevel)
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1 NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
```

## Phase 1: Preflight, skeleton and the shared copy

## Task 1: Run the four preflight checks and write RL/results/step0.md

Follow `RL/IMPLEMENTATION.md` section 1 and step 0 (sub-steps 0.1 to 0.5). Create `RL/results/` and write `RL/results/step0.md` and `RL/results/import-time.md`. Scratch goes to `/tmp/rl-step0/`.

- Run `$T $REPO/tests/review -q`. The code this design imports (`src/superclaude/cli/review/findings.py`, `merge_cmd.py`, `ledger.py`) must be healthy; if it fails, stop and report it, do not fix `src/`.
- Write `/tmp/rl-step0/merge_keys.py` (about 20 lines, run with `$PYRUN`): build one report whose findings line carries `"class"`, `"probe"` and `"src"`, run `superclaude.cli.review.merge_cmd.command` through click's `CliRunner` with `--ledger`, `--doc` (a fixture plan under `/tmp`), `--round 1`, `--report r1=<report>` and `--out` all under `/tmp/rl-step0/`, and print the exit code and whether the merged text contains the three keys. Read `SW/results/step0.md` first (it holds the sibling's answer) and run the probe anyway.
- Run the sibling-state check of 0.3: `cd $SW && sha256sum -c` over the non-ABSENT rows of `RL/SHARED-MANIFEST-DESIGN-TIME.tsv` (read only), `ls -l` of the twelve Tier B paths of that file, and `ls $SW/results $SW/implement-report`.
- Run the transcript-shape check of 0.4 with `jq` on one `*.attempt1.json` per reviewer model (luna, haiku, sonnet, ember) under `EVAL/<document>/reviews/combos/`: list event types, assistant block types and `tool_use` input keys. Open no ground-truth, score or judge file.
- Time `$PYRUN -c "import superclaude.cli.review.findings"` five times and write the five numbers and their median to `RL/results/import-time.md`.

Acceptance criteria:
- `RL/results/step0.md` holds four answers (tests/review result, merge-keys result, sibling-state result, transcript-shape result), each with the decision taken under the decision rules of `RL/IMPLEMENTATION.md` section 1.
- `RL/results/import-time.md` exists with five timings and the median, so the row-check time budget of `RL/DESIGN.md` 10.1 has a measured number.
- The merge-keys answer states whether the real merge accepts `class`, `probe` and `src` and keeps them out of the merged report (REQ-11). If it rejects them, `step0.md` says the telemetry moves to a side file and names `RL/DESIGN.md` 7.2 check 11 as the part to change.
- `git status --porcelain` shows no change under `src/`, `tests/`, `.claude/`, `SW` or `EVAL` caused by this task.

## Task 2: Create the skeleton, the copy script, the environment script and the first fixtures

Depends on: Task 1

Follow `RL/IMPLEMENTATION.md` step 1 (create list) and `RL/DESIGN.md` sections 2.3, 3.1 to 3.4 and K8, K9. Create under `RL`:

- `RL/ruff.toml` with `extend = "../../../../pyproject.toml"`, and empty package files `RL/rl/__init__.py` and `RL/analysis/__init__.py` (`RL/scaffold/__init__.py` arrives by copy).
- `RL/config/shared-list.json` with the Tier A, S, T and B paths of `RL/DESIGN.md` 3.1, one list per tier (Tier A: `cards/` C1 to C8, schema, README; `briefs/` nine parts; `scaffold/{__init__,briefs,cards,fnd,lint,normalise}.py`; `bin/common.sh`; `bin/build-sandbox.sh`. Tier S: `config/packages.json`. Tier T: the eleven shared tests and the fixtures they need. Tier B: the twelve files of 3.1).
- `RL/bin/copy-shared.sh` with the behaviour of `RL/DESIGN.md` 3.2: reads the list, `sha256sum` then `cp` only (never writes under `SW`, K8), two reads 60 seconds apart for Tier B only, stops on a missing Tier A file or an unstable Tier B file, records an absent Tier B file as `built-local` naming its `SWD` section, writes `config/shared-manifest.json` (`tier`, `source`, `sha256`, `bytes`, `copied_at`, `kind`), and supports `--check` (re-hash every copy; a changed sibling file is `drift`, a warning with exit 0) and `--diff <path>`. Tier S is recorded once and not compared by `--check`.
- `RL/bin/rl-env.sh`: sets `SW_SB_ROOT=/tmp/evalsb-recipe`, accepts the one test hook `RL_FORCE_EXC` with values `lens`, `check` or `reask` only (anything else exits 2), exits 4 when the root is the sibling's `/tmp/evalsb-sweep` (K9). Every RL script sources it before `common.sh`.
- `RL/fixtures/sibling/make_sibling.py` (F-SIBLING of `RL/TESTING.md` section 2): builds a fake sibling folder in a temporary directory with Tier A, T and B files in chosen states (all present, a Tier A file missing, a Tier B file changing between two reads, a Tier B file absent) and a canary file whose mtime is checked.
- `RL/tests/fakes/claude`, executable, with only the `ok` scenario for now (reads the brief on stdin, finds `R-C<n>.` recipe headings, writes rows `C<n>.1` to `C<n>.<budget>`, appends one line per call to `FAKE_CALL_LOG`), so the copied `conftest.py` helper finds a fake first on `PATH`.

Acceptance criteria:
- `bash RL/bin/copy-shared.sh --help` or a dry invocation against a fixture sibling from `make_sibling.py` runs without writing under the fixture's sibling folder (canary mtime unchanged).
- `RL/bin/rl-env.sh` sourced with `SW_SB_ROOT=/tmp/evalsb-sweep` exits 4 and with `RL_FORCE_EXC=bogus` exits 2.
- `RL/tests/fakes/claude` is executable and prints a JSON array in the shape of a real `claude -p --output-format json` run for the `ok` scenario.
- `RL/config/shared-list.json` is valid JSON and every path in it appears under `SW` or is listed as Tier B.

## Task 3: Run the shared copy, add the four skeleton tests and run the copied tests

Depends on: Task 2

Run `bash $RL/bin/copy-shared.sh`, then `bash $RL/bin/copy-shared.sh --check`. Then write the tests named in `RL/IMPLEMENTATION.md` step 1 and `RL/TESTING.md` section 4: `RL/tests/test_shared_manifest.py` (manifest hashes match files, briefs parts match manifest, built-local entries name an `SWD` section, missing Tier A refuses, unstable Tier B refuses, absent Tier B is `built-local`, drift is a warning, `--diff` prints for built-local, Tier S recorded once and not checked; DR-11), `RL/tests/test_sibling_readonly.py` (K8: canary file unchanged, no script of `RL` has a write target under `SW`), `RL/tests/test_sandbox_root.py` (K9: root is `/tmp/evalsb-recipe`, the sibling root is refused with exit 4) and `RL/tests/test_layout_rl.py` (K7: `bin`, `tests`, `scaffold`, `rl`, `analysis` exist, none matches a `.gitignore` pattern by `git check-ignore`, no `lib/`).

Run the copied tests unchanged against the copies: `test_paths.py`, `test_model_allowlist.py`, `test_cards.py`, `test_briefs.py`, `test_fnd_contract.py`, `test_lint.py`, `test_normalise.py`, `test_readme.py`, `test_sandbox.py` (REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-11 and K1, K2 coverage by copy). Append a section "Step 1 copied-test findings" to `RL/results/step0.md` with every failure of a copied test and its cause. Record in the same section which of the twelve Tier B files were copied and which are `built-local` (the sibling's Tier B files did not exist at plan time, so the expected outcome is that most are `built-local`).

Acceptance criteria:
- `$T $RL/tests -q` exits 0, or each failing copied test is listed in `RL/results/step0.md` with its cause and no copied file was edited.
- `RL/config/shared-manifest.json` exists, lists every shared file with `kind` `copied` or `built-local` and a sha256, and `bash $RL/bin/copy-shared.sh --check` exits 0.
- `RL/scaffold/{__init__,briefs,cards,fnd,lint,normalise}.py`, `RL/bin/common.sh`, `RL/bin/build-sandbox.sh`, `RL/cards/`, `RL/briefs/` and `RL/config/packages.json` exist and equal the sibling's files by sha256 at copy time.
- `git status --porcelain -- $SW` shows no change made by this task.

## Phase 2: Recipes, lens table and the RL brief

## Task 4: Write the recipes file, the RL block, the search-form line and the recipes README

Depends on: Task 3

Follow `RL/IMPLEMENTATION.md` step 2 and `RL/DESIGN.md` sections 4.1 to 4.6, 6.3 and 11.3. Create `RL/recipes/recipes.json` (schema `rl-recipes/1`, version 1, the eight recipes of `RL/DESIGN.md` 4.2 byte for byte from the quoted text of `MR` 3.2(a), each ending with exactly one sentence `Write at most N rows.`, C2 with 6 and the others with 4), `RL/recipes/rl-block.txt` (the `MR` 3.2(a) ledger rule with `{{LENS_ROW_CAP}}` in place of 14, `RL/DESIGN.md` 6.3), `RL/recipes/search-form.txt` (`RL/DESIGN.md` 4.5), `RL/rl/recipes.py` (load, `row_budget(id)`, validation: key set equals the card ids of `RL/cards/` (DR-1), at most 120 words, one budget sentence with N from 1 to 14, no `src/superclaude/` path, no expected-outcome words `expected`, `should find`, `will find`, `you will see`), `RL/recipes/README.md` (the re-derive table of `RL/DESIGN.md` 11.3 with a row per target type for plan, specification and documentation covering each of: meaning of edits, meaning of tests and gate, meaning of source, command dialect, test and root-document paths, severity guidance, snapshot, lens assignment; its first lines say the sibling's extractor sentences do not apply; REQ-38) and `RL/recipes/REVIEWS.md` (eight rows C1 to C8 with status OPEN, reviewer and date empty; REQ-08). A one-time helper `RL/rl/extract_mr.py` may extract the quoted blocks from `MR` 3.2(a) and prints a diff against the `recipes.json` text.

Write tests with the invented synthetic ground truth `RL/fixtures/gt/lint-gt.json` (F-LINT-GT): `RL/tests/test_recipes.py` (key sets equal card ids, at most 120 words with the counts 71, 89, 56, 99, 86, 93, 50, 67, budget sentence once and parsed, text equals the `MR` quote while no `override` entry exists, no `src/superclaude/` path, recipe text only in one file; REQ-06, REQ-09, REQ-25), `RL/tests/test_recipes_readme.py` (REQ-38), `RL/tests/test_recipes_reviews.py` (the completeness test carries marker `freeze` and is not run by this build), `RL/tests/test_lint_rl.py` (seeded phrase in a recipe fails, seeded name in `lenses.json` fails, clean files pass on the synthetic ground truth; REQ-07). Register the markers `slow` and `freeze` in a `RL/tests/conftest.py` addition only if the copied `conftest.py` does not already define them; otherwise use a new `RL/pytest.ini`.

Acceptance criteria:
- `$T $RL/tests/test_recipes.py $RL/tests/test_recipes_readme.py $RL/tests/test_recipes_reviews.py $RL/tests/test_lint_rl.py -q -m "not freeze"` exits 0.
- `RL/recipes/recipes.json` has exactly the key set C1 to C8, equal to the ids in `RL/cards/`, and the word counts are all at most 120.
- The RL block rendered with 14 in place of `{{LENS_ROW_CAP}}` equals the `MR` 3.2(a) quote byte for byte (checked later by Task 6, the placeholder is present now).
- `RL/recipes/REVIEWS.md` has 8 rows with status OPEN: the second-author review (REQ-08) is a manual record left open for a person who has not seen the ground truth, and is listed in Task 20.
- No file under `RL/recipes/` contains a package name, task number, file name of a study package or a 4-word sequence from a ground-truth file (the real lint is not run by this build).

## Task 5: Write the lens table, the values file, the lens render and the cost-driven row cap

Depends on: Task 4

Follow `RL/IMPLEMENTATION.md` step 3 (lens part) and `RL/DESIGN.md` sections 5.1 to 5.4 and DR-3, DR-4, DR-7. Create `RL/config/lenses.json` exactly as `RL/DESIGN.md` 5.1 (three panels `primary`, `haiku`, `sonnet`, three roles each with `rid`, `model`, `lens`, `table_cap`, `search_form`, `reask`), `RL/config/values.json` (planning `b` per panel and document: primary 100, 120, 122; haiku 220, 238, 226; sonnet 259, 302, 269; `c` per model: ember 0.4, luna 2, haiku 4, sonnet 3; fixed 6 s, share 0.35, hard cap 14; overhead 28 s for the primary panel and 30 s for haiku and sonnet; re-ask constants 30 and 1.35; every value marked planning), `RL/rl/lens.py` (load, the six validation rules of 5.2 raising `E_LENS_INVALID`, `render(panel, has_source, b_min, c_by_model)` returning per role `rid`, `model`, `recipes`, `budgets`, `assigned_ids`, `row_cap`, `search_form`, `reask`, `no_budget`, `lens_row_cap(b, c, table_cap) = min(table_cap, floor((0.35 b - 6) / c))`, `assigned_ids`; C2 dropped from every lens when `has_source` is false) and `RL/fixtures/lens/make_lens.py` (F-LENS: a valid table plus one invalid variant per rule of 5.2, and a C9 variant with card, recipe and placement). Model names pass `sw_assert_model` (K2).

Write `RL/tests/test_lens.py`: `test_duplicated_classes_equal_req25` (primary {C2, C4}, haiku {C1}, sonnet {C1, C7}), `test_search_form_only_in_search_role`, `test_row_cap_per_panel` (14/14/14, 6/14/12, 8/12/12), `test_row_cap_formula_table` (b=100: c 2.00 gives 14, 2.07 gives 14, 2.41 gives 12, 2.50 gives 11, 3.00 gives 9; b=122: c 2.00 gives 14, c 3.00 gives 12; b=60, c 2.00 gives 7), `test_no_budget_refuses`, `test_every_lens_keeps_two_recipes_without_c2` (DR-7), `test_fixture_class_c9_needs_no_code_change` (REQ-10), one test per invalid-table variant, `test_render_under_one_second`, and `RL/tests/test_model_allowlist_rl.py` (K2: every `model` in `lenses.json` passes `sw_assert_model`; `claude-opus-5-5` appears under `RL/bin`, `RL/rl`, `RL/scaffold` only in `bin/judge-one.sh`, which Task 14 creates, so the Opus half of this test is written in Task 14).

Acceptance criteria:
- `$T $RL/tests/test_lens.py -q` exits 0 and covers REQ-10, REQ-25 (lens part), REQ-26 (cap part), DR-4 and DR-7.
- `RL/config/lenses.json` validates by the six rules of `RL/DESIGN.md` 5.2, each class is in at least one lens of every panel, and every lens holds 2 to 4 recipes.
- `lens_row_cap` returns the table values of `RL/DESIGN.md` 5.4 for all eight rows, and a cap below the number of recipes in a lens sets `no_budget`.
- Rendering one panel plus one brief takes under 1 second on the fixture.

## Task 6: Write the brief renderer, the lens subcommand and the render, target and ablation tests

Depends on: Task 5

Follow `RL/IMPLEMENTATION.md` step 3 (render part) and `RL/DESIGN.md` sections 2.4, 6.1 to 6.5, 11.3 and DR-2, DR-3, DR-7. Create `RL/rl/render.py`: the RL brief is the copied renderer's Z0 text (`scaffold.briefs.render("Z0", doc, None, source)`, never re-implemented) then the copied ledger rule, then `recipes/rl-block.txt` with `{{LENS_ROW_CAP}}` filled, then the line `## RECIPES ASSIGNED TO YOU`, then the reviewer's recipes printed as `R-C<n>. <text>` one paragraph each in lens order, then (search role only) the search-form line, joined by the copied module's `SEPARATOR`; on `fallback` the Z0 text only. Create `RL/rl/cli.py` with the subcommand `lens` (`--validate`, `--panel`, `--doc`, `--out`) writing `lens/<rid>.json`, `briefs/<rid>.txt`, `briefs/<rid>.sha256` and the `run.json` fields of `RL/DESIGN.md` 2.2 (`no_source`, `c2_not_applicable`, `no_budget`, `fallback`, `recipes_sha256`, `lenses_sha256`, row cap, `b` and `c` used); JSON is written with `sort_keys=True`, `ensure_ascii=False` and a trailing newline.

Write `RL/tests/test_render.py` (REQ-01: CB-1 present with a source and absent without, C2 recipe dropped without a source, `no_source` flags; REQ-05 RL parts: brief starts with the exact Z0 text, fallback brief equals Z0 by sha256, part order, row-cap placeholder equals the `MR` quote at 14 and only the number changes at 6 and 8 (DR-3); REQ-09: no `src/superclaude/` path in any brief of any arm, panel, reviewer, with and without a source; REQ-25: generated briefs match the lens table for each of the three panels, recipe paragraphs equal `recipes.json` byte for byte, at most 4 per brief, parsed by the heading `R-C<n>.`; byte-identical same inputs), `RL/tests/test_targets.py` (REQ-37: spec fixture with its parent as source has all eight recipes, documentation fixture has no C2 and seven others, with `no_source` and `c2_not_applicable`, every lens at least 2 recipes), `RL/tests/test_ablation.py` (REQ-35, DR-13: removing one recipe leaves every other recipe paragraph, Z0 part and lens position byte for byte unchanged) and the render part of `RL/tests/test_ground_truth_not_read.py` (K3, REQ-34: a read hook on `open` shows the lens and brief render never open a trap file named like a ground-truth file in the F-REPO fixture).

Acceptance criteria:
- `$T $RL/tests/test_lens.py $RL/tests/test_render.py $RL/tests/test_targets.py $RL/tests/test_ablation.py $RL/tests/test_ground_truth_not_read.py -q` exits 0.
- `$PYRUN $RL/rl/cli.py lens --validate` prints the three panels and exits 0 (checkpoint of step 3).
- Every rendered RL brief begins with the Z0 brief of the same document and source state, and the three briefs of a panel hold the recipe sets of the lens table.
- A bad lens table makes the `lens` subcommand exit non-zero with `E_LENS_INVALID`, which Task 13 turns into a Z0 fallback.

## Phase 3: Ledger row check, promotion and the ember re-ask

## Task 7: Provide the ledger reader and quote checks with report and transcript fixtures

Depends on: Task 3

Follow `RL/IMPLEMENTATION.md` sub-step 4.1 and `RL/DESIGN.md` sections 3.3, 7.1, 7.2 checks 1 and 5 to 7, and DR-9. If `RL/config/shared-manifest.json` records `scaffold/ledgerv1.py` and `scaffold/telemetry.py` as `copied`, nothing is written for them; if `built-local`, write them to the written contract of `SW/DESIGN.md` sections 9.1 and 9.2 (read only) and `MR` 3.0.4 to 3.0.6: heading `## Ledger` first, no other heading before `## Findings block`, exactly one `ledger-v1` fenced block between them, every non-empty line parsed as JSON with format errors counted never skipped, verdict read case-insensitively (`normalised_verdict`), `dup_line`, `unknown_item`, limits, quote tests on flattened text using `scaffold.fnd.locate`/`flat` (REQ-14), corpora `source`, `candidate`, `transcript` (tool results of the reviewer's own run, never assistant text; DR-9). Create the fixture generators `RL/fixtures/reports/make_rl_reports.py` (every case listed under F-REPORT-RL in `RL/TESTING.md` section 2, quotes cut from `RL/fixtures/plans/p_basic.md` by regular expression so they are exact) and `RL/fixtures/transcripts/make_transcripts.py` (F-TRANSCRIPT-RL: a search done, a search claimed and not done, no tool call, a `NONE FOUND` with and without a search, in the shape of a real `claude -p --output-format json` run).

Write the reader part of `RL/tests/test_rowcheck.py`: `test_misplaced_duplicated_truncated_blocks`, `test_fence_opener_grep_is_not_used`, `test_heading_between_ledger_and_findings_is_missing` (REQ-13), `test_quote_wrapping_a_plan_line_matches`, `test_quote_plan_not_in_candidate_fails` (REQ-14).

Acceptance criteria:
- `$T $RL/tests/test_rowcheck.py -q -k "blocks or fence or heading or wrapping or not_in_candidate"` exits 0.
- A report that holds the fence opener text only in prose is `ledger_missing`; a quote that wraps a candidate line passes; a quote not in the candidate has `quote_plan_ok` false.
- Every case of F-REPORT-RL listed in `RL/TESTING.md` section 2 can be built by the generator, and the AO-1 lint (`RL/scaffold/lint.py`) finds no study text in `RL/fixtures/`.

## Task 8: Implement linking, demotion and promotion of ledger rows

Depends on: Task 7

Follow `RL/IMPLEMENTATION.md` sub-steps 4.2 and 4.3 and `RL/DESIGN.md` sections 7.2 checks 7 to 11, 1.4 (`SWD` DD-3, DD-11, DD-12) and 7.4. Write the link, demote and promote logic in `RL/scaffold/ledgerv1.py` (if `built-local`; otherwise in the RL adapter of Task 9 without editing the copy): link each findings line to a row by `probe` or by the row's flattened `quote_plan` lying inside the line's flattened `anchor`; demote a linked blocking finding to non-blocking when its row is an unsupported PROBLEM (`row_unsupported`), an UNSURE row (`row_unsure`), has no CB-3 sentence (`no_cb3`) or failed to parse (`row_missing`), keeping its severity; leave unlinked findings untouched (switch `CHECK_SCOPE=linked|all`, `all` unused); count `format_induced_demotions`; promote a PROBLEM row with no linked line using the row's own `problem` as `claim` and `quote_plan` as `anchor`, validated with `FND._check_finding`, inserted inside the single findings block, severity MINOR, `blocking` false, `src` `ledger`, `class` from the row id prefix, and only when the row is not `unknown_item`, not `over_budget`, has a present `quote_plan_ok` `quote_plan`, and its ledger was not repaired by a re-ask (check 10). Failures are logged in `promotion_failures` and skipped.

Write the REQ-15 and REQ-16 tests in `RL/tests/test_rowcheck.py`: `test_promotion_copies_problem_and_anchor`, `test_promotion_validates_with_check_finding` (long id, short anchor, duplicate id), `test_promotion_inside_single_block`, `test_promotion_failure_logged_and_skipped`, `test_promotion_requires_quote_plan_ok`, `test_no_promotion_for_over_budget_unknown_or_reask_rows`, `test_class_key_added_from_row_prefix`, `test_unsupported_row_demotes_linked_finding`, `test_unsure_never_blocks`, `test_blocking_needs_cb3_and_two_quotes_or_search`, `test_unlinked_finding_untouched`, `test_quote_other_corpora`, `test_check_scope_all_switch_off_by_default`, `test_format_induced_demotions_counted`.

Acceptance criteria:
- `$T $RL/tests/test_rowcheck.py -q -k "promotion or demotes or unsure or blocking or unlinked or corpora or scope or format_induced"` exits 0.
- A `quote_other` found only in a tool result of the transcript is supported as a search result, one found only in assistant text is not, and an unlinked blocking finding stays blocking (REQ-16, DR-9).
- The raw `reviews/<rid>.md` is never edited by any function; checked output goes to a separate `checked.md`.

## Task 9: Write the RL adapter, the row check and the check subcommand

Depends on: Task 8

Follow `RL/IMPLEMENTATION.md` sub-step 4.4 and `RL/DESIGN.md` sections 3.3, 4.4, 7.2 to 7.5 and DR-5, DR-6. Create `RL/rl/ledger_api.py` (the one adapter, at most 40 lines: `read`, `check`, `link_demote`, `promote`, so a later swap of a local Tier B file for the sibling's changes only this file) and `RL/rl/rowcheck.py`: row-id grammar `^C[0-9]+\.[0-9]+$` with the class in the reviewer's lens (`unknown_item`), recipe coverage (`recipe_missing`, with a lone `NONE FOUND` row covering its recipe and `none_found_with_rows` flagged), budgets (rows beyond a recipe's budget or beyond the lens `row_cap` are `over_budget` with reason `recipe` or `lens`, kept for counting, never promotable; DR-6), `check/<rid>.ledger.json`, `check/<rid>.checked.md`, `check/check.json` with the keys of `RL/DESIGN.md` 7.4 and `classes_lost`, and the `check` subcommand of `RL/rl/cli.py`. The check must raise on error so the launcher can set `check_skipped`.

Write the REQ-26 and DR-5 tests in `RL/tests/test_rowcheck.py`: `test_row_budget_per_recipe`, `test_lens_cap_enforced`, `test_none_found_allowed_and_covers_recipe`, `test_none_found_with_rows_flagged`, `test_recipe_missing_flagged`, `test_row_id_grammar_and_lens_membership`, `test_assigned_ids_per_lens`, `test_over_budget_rows_not_promotable`, `test_check_under_one_second_on_three_reports`, and `RL/tests/test_blindness.py::test_merged_report_has_no_telemetry_keys` is deferred to Task 13. Extend `RL/tests/test_ground_truth_not_read.py` with the row-check part (K3).

Acceptance criteria:
- `$T $RL/tests/test_rowcheck.py $RL/tests/test_ground_truth_not_read.py -q` exits 0.
- `C4.1` is accepted for a lens with C4, `unknown_item` for a lens without it; `C4x` and `4.1` are `unknown_item`; a fifth row of a 4-row recipe and a fifteenth row of a lens are `over_budget`.
- The check of three fixture reports with transcripts takes under 1 second excluding interpreter start.

## Task 10: Write the ember re-ask and its tests

Depends on: Task 9

Follow `RL/IMPLEMENTATION.md` sub-step 4.5 and `RL/DESIGN.md` sections 7.6, 8 (rows 8, 20, 23) and DR-8. Create `RL/rl/reask.py`: a pure `reask_allowed(role_reask, ledger_missing, already_asked, now_s, b_s)` true only when the role has `reask: true`, the reviewer is `ledger_missing`, no re-ask has run, and `now_s + 30 <= 1.35 * b_s` with `math.isclose` tolerance 1e-9 at the boundary (constants read from `config/values.json`); the repair prompt of 7.6 verbatim; the fresh call `claude -p --model <ember model> --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit` under `timeout 30` in the same sandbox with the model-identity check; the acceptance rule (the repaired message replaces the original only if its `ledger-v1` block parses directly above the findings block and its findings block parsed as JSON lines in order equals the original's; rows are marked `via_reask`); the `reask` subcommand of `RL/rl/cli.py`. A re-ask is recorded as `reask`, never as a retry, and its seconds are reported as `reask_s`.

Write `RL/tests/test_reask.py`: `test_condition_with_fake_clock` (b=100: now 81 allowed, now 105 allowed, now 105.01 not allowed; b=122: now 134.7 allowed, 134.8 not), `test_boundary_is_inclusive`, `test_never_for_luna_even_with_large_b` (b=1000), `test_only_when_ledger_missing`, `test_only_once`, `test_haiku_and_sonnet_never`; the whole-path tests that call the launcher are written in Task 13.

Acceptance criteria:
- `$T $RL/tests/test_reask.py -q` exits 0 (REQ-27 condition part).
- `reask_allowed` takes the clock as an argument and reads no wall clock, so the tests use a fake clock.
- The repair prompt text equals the `RL/DESIGN.md` 7.6 quote, and rows of a repaired ledger are never promoted (check 10 of Task 8 is exercised by a `via_reask` fixture).

## Phase 4: Fake claude, launcher, clock and hang guard

## Task 11: Complete the fake claude and test it

Depends on: Task 10

Follow `RL/IMPLEMENTATION.md` step 5 (first sentence) and `RL/DESIGN.md` 3.4. Extend `RL/tests/fakes/claude` with every scenario: `ok`, `problem` (one PROBLEM row with exact quotes from the candidate and a linked finding), `none_found`, `ledger_missing`, `ledger_after_findings`, `over_budget`, `recipe_missing`, `long_anchor`, `bad_block`, `api_error`, `wrong_model`, `sleep` (`FAKE_SLEEP_S`), `exit127` and `repair` (a second call whose brief starts with the repair sentence of `RL/DESIGN.md` 7.6 returns the first message with a ledger added). `FAKE_SCENARIO_BY_MODEL` may set a scenario per requested model. Each call appends `<epoch seconds> TAB <scenario> TAB <requested model> TAB <review or repair>` to `FAKE_CALL_LOG`. Write `RL/tests/test_fake_claude_rl.py::test_scenarios_and_call_log` (each scenario prints the JSON array of its description, one log line per call, the suite fails if the first `claude` on `PATH` is not the fake).

Acceptance criteria:
- `$T $RL/tests/test_fake_claude_rl.py -q` exits 0.
- No scenario starts a model or makes a network call.
- The `repair` scenario is selected by the brief starting with the repair sentence and returns a message whose findings block equals the first message's.

## Task 12: Write the clock, the reviewer script and the hang guard

Depends on: Task 11

Follow `RL/IMPLEMENTATION.md` step 5 and `RL/DESIGN.md` sections 3.3, 9.2 to 9.4 and 10.2. Check that `RL/results/import-time.md` from Task 1 exists first. If `scaffold/clock.py` and `bin/run-reviewer.sh` are `built-local`, write them to the contract of `SW/DESIGN.md` 11.1 and 11.4 (read only): `scaffold/clock.py` with `hang_s`, `breakeven_row_cost` and `lens_row_cap` imported from `rl/lens.py`; `bin/run-reviewer.sh` with one attempt, `NOFALLBACK=1` required, brief from a file on stdin, `cd /tmp/evalsb-recipe/<doc>/repo`, hang-guard `timeout`, the model-identity check, `BLOCK_OK` by `FND.parse_block` after H2 on a temporary copy (a missing `ledger-v1` block does not make it false), `hang_s`, `killed` and `prompt_sha256` in `meta.json`, read-only tools (`--disallowedTools Edit Write NotebookEdit`, K4).

Write `RL/tests/test_hang_guard.py::test_formula_per_panel` (primary RL at b 100/120/122: 192/222/225 s; primary Z0: 150/180/183; haiku RL at 220/238: 375/402; sonnet RL at 259/302: 433.5/498), `RL/tests/test_clock.py` (`test_panel_elapsed_rl_and_other_arms`, `test_clock_starts_before_lens_render`, `test_reask_seconds_inside_the_clock`; REQ-29) and `RL/tests/test_report.py::test_breakeven_values` (`breakeven_row_cost(100, 14)` is 2.07, `(100, 12)` is 2.42, 120 gives 2.57, 122 gives 2.62, 116 gives 2.47; REQ-31 breakeven part).

Acceptance criteria:
- `$T $RL/tests/test_hang_guard.py $RL/tests/test_clock.py $RL/tests/test_report.py -q -k "formula or panel_elapsed or clock or breakeven"` exits 0.
- `bin/run-reviewer.sh` refuses (exit 4) when `NOFALLBACK` is not set or the model is outside the allowlist.
- No reviewer script names `claude-opus-5-5` (K2).

## Task 13: Write the panel launcher, the fallback logic and the integration tests

Depends on: Task 12

Follow `RL/IMPLEMENTATION.md` step 5 (launcher) and `RL/DESIGN.md` sections 2.1, 2.2, 7.5, 8 and 9.1, 9.6, 10, REQ-12, REQ-27, REQ-30, REQ-46. Create `RL/bin/run-panel.sh --arm {Z0-raw|Z0|K|RL} --panel {primary|haiku|sonnet} --doc <id> --replicate <n> --block <n> --seed <int> --run-id <id> [--b <seconds>] [--dry-run]` writing to `RL/runs/<run-id>/`: check the sandbox is clean (`git status --porcelain`, K4), start the panel clock before the lens render, render briefs (RL arm: lens render with fallback to the Z0 briefs and `fallback=true` decided before any reviewer starts; no source drops C2), `--dry-run` writes `briefs/`, `lens/`, `run.json`, prints the three `claude` command lines with brief sha256 and starts nothing, start three reviewers in parallel under the hang guard, record `rev_end`, run `rl/cli.py check` and (ember only, `ledger_missing`, `reask_allowed`) `rl/cli.py reask` and a re-check, set `check_skipped=true` on any exception and merge the raw reports, stop the clock, then outside the clock run `scaffold/normalise.py` (order: check, then H2, then merge), build `resolution.json`, call `superclaude review merge --ledger ... --doc ... --round 1 --report <rid>=... --resolution ... --out ...` (a killed or invalid reviewer is absent; `merge_refused` is recorded, not re-run), run the sandbox-clean check, write `run.json` and `timing.json` (fields of `RL/DESIGN.md` 2.2 and 9.3 including `reask_s`, `panel_elapsed_s`, `slowest_reviewer_s`, row cap, `b`, `c`, `concurrent_panels_at_start`). Exit codes: 0 done, 2 usage or sandbox invalid, 3 `no_budget`, 4 refused. No verifier step exists and `VERIFIER` defaults to 0.

Write the integration tests (marker `slow`) in `RL/tests/test_run_panel_fake.py` (`test_long_anchor_survives_h2_then_merge`, `test_forced_exception_in_check_merges_as_written`, `test_ember_reask_runs_once_and_is_accepted`, `test_reask_rejected_when_findings_differ`, `test_no_reask_when_clock_too_late` with `--b 1`, `test_luna_ledger_missing_is_not_reasked`, `test_reask_failure_keeps_original_report`, `test_reask_not_counted_as_retry`, `test_repaired_rows_never_promoted`, `test_sleeping_reviewer_killed`, `test_no_retry_on_failure`, `test_killed_reviewer_absent_from_merge`, `test_order_check_then_h2_then_merge`), `RL/tests/test_fallback.py` (`test_forced_exception_in_lens_render_runs_z0_briefs`, `test_invalid_lens_table_falls_back`, `test_fallback_decided_before_first_reviewer_starts`), `RL/tests/test_sandbox_clean.py::test_dirty_after_run_is_flagged` (K4), `RL/tests/test_run_json_fields.py::test_fields_match_sibling_schema` (DR-12), `RL/tests/test_blindness.py::test_merged_report_has_no_telemetry_keys`, `RL/tests/test_verifier_off_path.py` (REQ-46: `test_no_verifier_step_in_clock`, `test_verifier_default_off`, `test_verifier_time_excluded`) and the REQ-26 test `no_budget` exit code 3. Then run rehearsal A7 of `RL/TESTING.md` section 5.1 on the fake claude over the real sandbox of one study document: `export SW_SB_ROOT=/tmp/evalsb-recipe-rehearsal`, `bash $RL/bin/build-sandbox.sh TASK-WF-designSpec-20261107-075614`, then `PATH=$RL/tests/fakes:$PATH FAKE_SCENARIO=ok FAKE_CALL_LOG=/tmp/rl-rehearsal-calls.log bash $RL/bin/run-panel.sh --arm RL --panel primary --doc TASK-WF-designSpec-20261107-075614 --replicate 1 --block 1 --seed 1 --run-id rehearsal-rl`. Do not open any ground-truth file in the sandbox or the repository.

Acceptance criteria:
- `$T $RL/tests/test_fake_claude_rl.py $RL/tests/test_clock.py $RL/tests/test_hang_guard.py $RL/tests/test_fallback.py $RL/tests/test_run_panel_fake.py $RL/tests/test_sandbox_clean.py $RL/tests/test_run_json_fields.py $RL/tests/test_blindness.py $RL/tests/test_verifier_off_path.py -q` exits 0 (REQ-02 whole path, REQ-12, REQ-27 whole path, REQ-30, REQ-46).
- The rehearsal log `/tmp/rl-rehearsal-calls.log` shows exactly three review lines and no model was started; the run folder holds `run.json`, `timing.json`, `check/check.json`, `merged/merged-1.md` and a merged report with none of `probe`, `src`, `class`, `ledger-v1`.
- A forced `RL_FORCE_EXC=lens` run uses Z0 briefs with `fallback: true` before the first fake call; `RL_FORCE_EXC=check` merges the raw reports with `check_skipped: true`.
- The Z0, K and Z0-raw arms render and run through the same script (K adds only the copied K paragraph; Z0-raw uses the base brief and the raw sandbox built by `bin/build-sandbox.sh --raw`).

## Phase 5: Judge copy and analysis

## Task 14: Write the judge scripts and the judge tests

Depends on: Task 13

Follow `RL/IMPLEMENTATION.md` step 6 (judge part) and `RL/DESIGN.md` sections 3.3, 9.7 and REQ-43. If `bin/judge-one.sh`, `bin/anon.sh`, `bin/judge-batch.sh` are `built-local`, create them from `EVAL/tools/tmp-scripts/judge-one.sh` (read only, lines 12 to 23 hold the `BRIEF` text, kept byte for byte with the paths as variables), anonymisation by random label with reviewer ids replaced and paths redacted, a batch script with the API-error audit, and the second judge on a 15% seeded sample. `claude-opus-5-5` appears only in `bin/judge-one.sh` (K2) and the script is never run by this build. Create synthetic judge folders under `RL/fixtures/` for the tests. Write `RL/tests/test_judge.py` (`test_judge_brief_sha_equals_jj`, `test_model_is_opus_only_in_judge`, `test_audit_flags_error_with_score_file`, `test_second_judge_sample_15_percent_seeded`, `test_audit_counts_match_merged_rows`, `test_merged_report_has_no_arm_marker`) and `RL/tests/test_model_allowlist_rl.py::test_opus_only_in_judge_script`.

Acceptance criteria:
- `$T $RL/tests/test_judge.py $RL/tests/test_model_allowlist_rl.py -q` exits 0 (REQ-05 judge, REQ-43, K2).
- The sha256 of the `BRIEF` text in `bin/judge-one.sh` equals that of the cited lines of the `EVAL` script.
- `grep -rn claude-opus-5-5 $RL/bin $RL/rl $RL/scaffold` hits only `bin/judge-one.sh`.
- The sample holds `round(0.15 n)` runs and repeats for a fixed seed.

## Task 15: Write the analysis script, the synthetic ground truth and the run-folder fixtures

Depends on: Task 14

Follow `RL/IMPLEMENTATION.md` step 6 (analysis part) and `RL/DESIGN.md` sections 9.3, 12.2 to 12.5 and REQ-17, REQ-29, REQ-31, REQ-39 to REQ-45. Create `RL/fixtures/gt/synthetic-gt.json` (F-GT, invented items for the fixture plan) and `RL/fixtures/runs/make_runs.py` (F-RUNS-RL: synthetic run folders for arms Z0-raw, Z0, K, RL, 2 documents, 5 replicates, known found sets, timings, flags, ledgers and scores, and `expected.json` written by hand-written arithmetic, not by calling `analyze.py`). Create `RL/analysis/analyze.py` with subcommands `all`, `audit-judges`, `compliance`, `prereg`, `sample-second-judge`, `ablate-report`: every metric of `RL/DESIGN.md` 12.5 defined only in this file (`found_fraction` and the other metric names), Wilson intervals, a bootstrap that resamples documents then runs, gates D1 to D7 (D1 on per-document medians, same block only, mean and median both reported; D6 blocking), the three labelled shares `Z0 - Z0raw`, `K - Z0`, `RL - Z0` never summed, per-stage rows `stages.jsonl` (extraction null, selection, act, merge survival, judge credit, class, reviewer id), kills and retries per arm with re-asks apart, non-probe findings per run excluding `probe` lines and `src: ledger` lines, the REQ-45 claim sentence, and `analysis/g0.py` is written in Task 16. The analysis reads real ground truth only when a person runs it on real runs after the freeze; no test or build step does.

Write `RL/tests/test_analyze.py`, `RL/tests/test_report.py` (the REQ-31 `test_report_shows_planned_and_measured`, REQ-40 `test_three_shares_separate` and `test_no_summed_headline`, REQ-45 `test_claim_template_text`), `RL/tests/test_stages.py` (REQ-41), `RL/tests/test_prereg.py::test_act_bands_for_all_classes`, and the analysis-side tests of REQ-29, REQ-30, REQ-39, REQ-42 and REQ-43 listed in `RL/TESTING.md` sections 3.4 and 3.7.

Acceptance criteria:
- `$T $RL/tests/test_analyze.py $RL/tests/test_report.py $RL/tests/test_stages.py $RL/tests/test_prereg.py -q` exits 0.
- Every metric on the F-RUNS-RL fixture equals `expected.json`, and an AST search of `RL` finds `found_fraction` defined only in `analysis/analyze.py`.
- A fixture where D2 and D3 pass and D6 fails yields "do not adopt"; the report has no line that adds two share names.
- `analyze.py compliance` on the fixture reports `ledger_missing`, `recipe_missing`, quote validity, format errors and `none_found` per class equal to the hand-computed values (REQ-17 check itself).

## Task 16: Write the ran cross-check and the ledger-and-time gate script

Depends on: Task 15

Follow `RL/DESIGN.md` sections 7.7, 3.3 (`analysis/g0.py` row) and 12.3 and `RL/TESTING.md` REQ-28. Create `RL/analysis/ran_check.py <run dir>...`: for every ledger row a `ran_status` of `not_a_tool_claim`, `verified` or `unverified` by the rules of 7.7 (command words `grep`, `egrep`, `rg`, `git`, `printf`, `find`, `ls`, `cat`, `sed`, `awk`, `wc`, `head`, `tail`, `pytest`, `jq`; a `Bash` call containing the word and sharing a distinctive token of four or more letters, or a result containing `quote_other`; recipes C5, C6, C8 with no `Bash` search call at all are `unverified`, as is a `NONE FOUND` row for them), counts per reviewer and per class, share of unverified search-recipe rows, output `results/ran.md`; it reads `reviews/<rid>.attempt1.json` and accepts the transcript shapes found in Task 1 (`RL/results/step0.md`). Create `RL/analysis/g0.py` (ledger-and-time half only: `ledger_missing` rate and luna cost per row against its break-even). Write `RL/tests/test_ran_check.py` (`test_verified_unverified_and_not_a_tool_claim`, `test_search_recipe_without_bash_is_unverified`, `test_none_found_for_search_recipe_without_call_is_unverified`, `test_report_per_class_and_reviewer`).

Acceptance criteria:
- `$T $RL/tests/test_ran_check.py -q` exits 0 (REQ-28 unit part).
- `analysis/ran_check.py` run on the synthetic F-TRANSCRIPT-RL runs writes `ran.md` with the hand-computed per-class counts.
- The manual audit of 20 spike rows (REQ-28 manual part) is not done here and is listed as open in Task 20.

## Phase 6: Schedule, spikes, freeze and order scripts

## Task 17: Write the schedule maker, the schedule runner and the spike script

Depends on: Task 16

Follow `RL/IMPLEMENTATION.md` step 7 (first three scripts), `RL/DESIGN.md` sections 9.5, 12.1, 12.4 and `RL/TESTING.md` sections 5.3 and 5.6 to 5.7. Create `RL/bin/make-schedule.py` (block-randomised `schedule.tsv`, one block per replicate, recorded seed, options `--stage`, `--arms`, `--docs`, `--reps`, `--set`, `--panel`, `--out`, `--append`; Stage 1 with arms z0, k, rl on four documents with 5 runs plus z0raw on three documents with 5 runs gives 75 rows), `RL/bin/run-schedule.sh` (`--max-panels N`, default 1, at most 3 reviewer processes alive by default; refuses to start without a `spike` record in `config/values.json` with `runs: 5` and a `c_luna`; passes `lens_row_cap(b_min, c_luna)` into every RL run; the script is only ever run against the fake claude by this build) and `RL/bin/run-spike.sh` (`timing` and `compliance` modes, each documented, each refusing to run without an explicit `--go` argument because it needs models; never run by this build). Write `RL/tests/test_run_schedule.py` (`test_refuses_without_spike_record`, `test_spike_sets_row_cap` with c=2.41 giving 12 and c=2.50 giving 11 at b=100, `test_max_panels_default_one`, `test_max_panels_three_runs_three_at_once`: with the default the fake schedule never has more than 3 reviewer processes alive, with `--max-panels 3` it reaches 9 and never 10).

Acceptance criteria:
- `$T $RL/tests/test_run_schedule.py -q` exits 0 (REQ-32 automatable part, concurrency budget).
- `make-schedule.py --stage 1 --arms z0,k,rl --docs HO-1,HO-2,HO-3,HO-4 --reps 5 --seed 20261115` writes 60 rows and the `z0raw` append adds 15 (75 total), with the seed recorded.
- `run-spike.sh` without `--go` prints that it needs models and exits non-zero without starting anything.

## Task 18: Write the freeze, order, sandbox-check, parity and open-checks scripts

Depends on: Task 17

Follow `RL/IMPLEMENTATION.md` step 7 (last five scripts), `RL/DESIGN.md` sections 11.1, 3.5 and K5, and `RL/TESTING.md` REQ-33, REQ-34, REQ-36, REQ-44 and section 4. Create `RL/bin/freeze.sh` (hashes `recipes/recipes.json`, `recipes/rl-block.txt`, `recipes/search-form.txt`, `config/lenses.json`, the cards, the briefs and `rl/*.py` into `config/freeze.json`, prints the `git tag` command and never runs it; K5), `RL/bin/check-order.sh` (`freeze`: tag commit time earlier than the first commit of a ground-truth file, and the hash check; `prereg`: `prereg.json` commit earlier than the first `run.json`), `RL/bin/check-sandbox-gt.sh` (`grep -r` for ground-truth file names and field names over every sandbox under `/tmp/evalsb-recipe` and every `RUN/briefs`, prints nothing when clean, exits non-zero on a hit, never prints file content), `RL/bin/check-z0-parity.sh <doc>` (renders the Z0 brief with the copied code and prints its sha256), `RL/bin/open-manual-checks.sh` (lists the manual records still open, plus `ran-audit` printing 20 spike rows with their transcripts). Write `RL/tests/test_freeze.py::test_freeze_prints_but_never_tags`, `RL/tests/test_order.py` (`test_freeze_tag_before_gt_commit`, `test_gt_before_tag_fails`, `test_freeze_json_hashes_match_files`, `test_gt_hash_matches_prereg`, `test_every_planted_plan_has_twin`, `test_prereg_commit_before_first_run`, using a temporary git repository and synthetic files only) and `RL/tests/test_check_scripts.py` (`test_sandbox_gt_check_finds_a_planted_trap_and_is_silent_when_clean`, `test_z0_parity_prints_a_stable_hash`, `test_open_manual_checks_lists_open_records`).

Acceptance criteria:
- `$T $RL/tests/test_freeze.py $RL/tests/test_order.py $RL/tests/test_check_scripts.py -q` exits 0.
- `git tag -l` is unchanged after running `bin/freeze.sh`.
- `bin/check-order.sh freeze` exits 0 only when the tag commit is earlier than the first ground-truth commit in the temporary repository.
- `bin/open-manual-checks.sh` lists the open M records (REQ-08 recipe reviews, REQ-28 ran audit, REQ-31 report read, REQ-32 timing spike, REQ-33, REQ-36, REQ-40, REQ-41 bands, REQ-44, REQ-45, REQ-38 content review, REQ-35 model-stage ablation).

## Phase 7: Full test run and the implementation report

## Task 19: Run every test and every build check and save the logs

Depends on: Task 18

Follow `RL/IMPLEMENTATION.md` step 8 and `RL/TESTING.md` section 6 items 1 to 7. Create `RL/results/` outputs by running, from `REPO`:

- `$T $RL/tests -q -m "not slow and not freeze"` and save its summary line and the counts of passed, failed, skipped and deselected tests to `RL/results/tests-final.log`.
- `$T $RL/tests -q -m slow` and append its summary line and counts to the same log.
- `$T $RL/tests -q --collect-only -m freeze` to list the tests with marker `freeze` and append the list and their count to the log; do not run them (they read the real ground truth or need a second author's records) and record that they were not run and why.
- `uv run --frozen --project $REPO ruff check $RL` and `uv run --frozen --project $REPO ruff format --check $RL`.
- `$T $REPO/tests/review -q` again (the baseline of Task 1 must still hold).
- `bash $RL/bin/copy-shared.sh --check` and `$PYRUN $RL/rl/cli.py lens --validate`.
- The rehearsal of Task 13 once more, and `git status --porcelain` over `src/`, `tests/`, `.claude/`, `.dev/tasks/` (other than this plan package), `SW` and `EVAL`, which must show no change made by the build.
- Per-kind counts: the number of tests per kind U, I, C (copied), F (freeze, not run), taken from the test files and markers, for the report.

If any command fails, fix the cause in the file that owns it (never a copied file) and rerun that command and the full run until it passes, or, if the cause is a copied test or a missing sibling piece, record it with its reason in `RL/results/tests-final.log` and `RL/results/step0.md` for the report.

Acceptance criteria:
- `RL/results/tests-final.log` holds the three summary lines (not slow and not freeze, slow, freeze collected-only), the ruff results, the `tests/review` result and the `copy-shared.sh --check` result, each with its exit code.
- Every non-freeze test passes, or each remaining failure is a copied test with a recorded cause; no copied file was edited.
- No path under `src/`, `tests/`, `.claude/`, `SW`, `EVAL` or an existing `.dev/tasks/` folder changed (shown by the `git status` output saved in the log).
- No ground-truth file was opened (the build used only `RL/fixtures/gt/` synthetic files).

## Task 20: Write RL/IMPLEMENTATION-REPORT.md

Depends on: Task 19

Follow `RL/IMPLEMENTATION.md` step 9 and `RL/TESTING.md` section 6 item 8 and section 5.4 and 5.5. Write `RL/IMPLEMENTATION-REPORT.md` from the files on disk (`RL/config/shared-manifest.json`, `RL/results/step0.md`, `RL/results/tests-final.log`, the file tree of `RL`) with sections, filled section by section:

- What was built, per phase of this plan, with file lists (recipes, lens table and render, row check, re-ask, launcher and arms, judge copy, analysis, schedule, spike, freeze and check scripts) and which parts RUN, which are STUBBED and which are NOT BUILT.
- Which Tier B files were copied and which were built locally (from `shared-manifest.json`, with the sibling's state at copy time).
- Test counts per kind (U, I, C, F) and the summary lines of `tests-final.log`, including the freeze tests collected and not run.
- The exact commands to run one panel of ember (`t2b-1`, `muse-ember-1.0`) plus two luna reviewers (`t4-1` and `t3-1`, `gpt-6-luna`) on each of the three study packages `TASK-WF-designSpec-20261107-075614`, `TASK-WF-makeTheAliasOnly-20261105-051649` and `TASK-WF-design-20261108-041415`, for the Z0 control arm and for the RL arm, taken from `RL/TESTING.md` 5.4 and 5.5: the environment lines (`REPO`, `RL`, `SW_SB_ROOT=/tmp/evalsb-recipe`, `NOFALLBACK=1`), `bash $RL/bin/build-sandbox.sh <doc>`, the `--dry-run` look, then `bash $RL/bin/run-panel.sh --arm Z0 --panel primary --doc <doc> --replicate 1 --block 1 --seed 20261115 --run-id derive-Z0-<doc>` and the same with `--arm RL --run-id derive-RL-<doc>`, run one panel at a time and in the same block, the `jq` lines to read the result, and the scoring command `bash $RL/bin/judge-batch.sh --runs <z0 run> <rl run>` flagged as needing the owner's go-ahead because it starts the blind Opus judge. State that these commands were not run against any model by this build.
- Every requirement not met or only partly met, with the reason: REQ-08 (second-author record open), REQ-28 manual audit, REQ-17, REQ-32 and the spike (need models), REQ-31 and REQ-33 and REQ-36 and REQ-41 bands and REQ-44 and REQ-45 manual records, REQ-35 model-stage ablation (96 runs, owner decision, DR-13), the `freeze` tests not run, REQ-18 to REQ-24 (Redesign 1 only, not built), every copied test that failed with its cause, every Tier B file built locally and not yet reconciled with the sibling (`copy-shared.sh --diff`), and the open owner decisions of `RL/DESIGN.md` 13.1 (items 1 to 10).
- A statement that no model, judge or network call was made, no ground-truth file was opened, and that Recipe Ledger working is not shown by this build (the experiment decides it).

After the file exists, check each claim in it against disk (counts against `tests-final.log`, file lists against `ls`, commands against `RL/TESTING.md` 5.4 and 5.5).

Acceptance criteria:
- `RL/IMPLEMENTATION-REPORT.md` exists and contains the six sections above, with the six exact commands (3 packages x 2 arms) written out in full and the `NOFALLBACK=1` and `SW_SB_ROOT` settings.
- The test counts in the report equal the numbers in `RL/results/tests-final.log`.
- Every requirement of `RL/TESTING.md` section 3 appears in the report either as met (with the test name that shows it) or as not met with a reason.
- The report does not call any piece "done" or "working" that is stubbed, not built or only shown by a fake claude.
