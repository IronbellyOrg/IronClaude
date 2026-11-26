# Implementation order: Redesign 2, Recipe Ledger

Status: design only. Nothing here was built or run. `DESIGN.md` says what to build, `TESTING.md` says how each requirement is tested. This file gives the order, the files per step, the test command per step and what to run first. Line counts are rough planning values (unmeasured). Redesign 2 is much smaller than Redesign 1 in its own code, but it still needs a launcher, a row check, a re-ask, a judge copy and an analysis script, which `MR` 3.2(h) does not count (DR-14); the estimate is in section 2.1.

Shell variables used in every command:

```
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet     # read only
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1
```

## 0. How to execute this

Three rules decide how the work is run.

1. It has far more than five edits and many files, so it goes through a written plan, then an executor: `/sc:workflow "Implement RL/DESIGN.md steps 0 to 9, writing only under RL; tests per RL/TESTING.md" --depth standard --handoff none`, then `/sc:implement <the printed plan path>` once the plan is read (level 3 of the routing guide). Steps 10 to 13 are not part of that plan: they need a second author, the owner's decisions, models and a production change.
2. Every file is written under `RL`. The plan must state that `src/`, `tests/`, `.claude/`, every existing folder under `.dev/tasks/` and the sibling folder `SW` are not touched (K1, K8). Nothing is staged, committed or pushed by the build; staging `.dev/tasks/` stays with the session that runs `/sc:implement`, as the repository rules say.
3. No step starts a model. Steps 0 to 9 need none. The tests use the fake claude (`tests/fakes/claude`).

## 1. What to run first

Run these four before any code is written. Each answers a question that could change the design, costs minutes, and needs no model. Write the four results in `RL/results/step0.md`.

| Order | Command | Question it answers | Decision rule |
|---|---|---|---|
| 1 | `uv run --frozen --project $REPO pytest -p no:cacheprovider $REPO/tests/review -q` | Is the code this design imports healthy today? (`findings.py`, `ledger.py`, `merge_cmd.py`) | must pass; if not, stop and fix that first, outside this design |
| 2 | the merge-keys probe of step 0.2 below | Does the real merge accept `class`, `probe` and `src` on findings lines, and keep them out of the merged report? (REQ-11, unverified in `MR`) | accepted: go on. Rejected: telemetry moves to a side file keyed by finding id and `DESIGN.md` 7.2 check 11 is changed. The sibling's `SW/results/step0.md` may already hold this answer: read it first, run the probe anyway (it is 20 lines) |
| 3 | the sibling-state check of step 0.3 below | Which files of the copy list exist now, and have the Tier A files changed since `SHARED-MANIFEST-DESIGN-TIME.tsv` was written? | a changed Tier A file is copied as it is now and its new hash recorded; a Tier B file that exists is a candidate for copying (`DESIGN.md` 3.1); the result decides which Tier B files step 4 and step 6 write locally |
| 4 | the transcript-shape check of step 0.4 below | Do luna, haiku and sonnet transcripts have the event and block shapes that `analysis/ran_check.py` and the `transcript` corpus assume (read from one ember run only)? | same shape: go on. Different: write the differences into `DESIGN.md` 7.7 and make the reader accept both shapes before step 4 |

## 2. Steps

### 2.1 Effort estimate (planning, unmeasured, DR-14)

| Step | New code in `RL` (lines, rough) | Tests (lines, rough) | Data and text |
|---|---|---|---|
| 1 skeleton and copy | 220 | 200 | `shared-list.json` 40 |
| 2 recipes | 110 | 150 | `recipes.json`, `rl-block.txt`, `search-form.txt`, README: about 200 |
| 3 lens table, render | 290 | 250 | `lenses.json` 40 |
| 4 ledger check, re-ask | 330, plus about 360 if `ledgerv1.py` and `telemetry.py` are built locally | 350 | |
| 5 launcher, clock, fake claude | 560 | 300 | |
| 6 judge copy, analysis | 700 (about 580 if the judge scripts are copied) | 350 | |
| 7 schedule, spikes, freeze scripts | 450 | 200 | |
| **Total** | **about 2,300 (all Tier B copied) to 3,000 (all built locally)** | **about 1,800** | **about 280** |

`MR` 3.2(h) gives about 310 specific lines and about 760 with the shared scaffolding. Its list is the recipe text (120), the lens table (70), the brief additions (40) and the tests (80), plus 450 shared lines. It has no row check beyond the shared 3.0.5, no launcher or clock, no re-ask, no judge copy and no analysis. Those are needed to run the experiment, so they are counted here. Neither figure is a limit.

### 2.2 Steps

Each step lists what to create, how to test it, and what "done" means. Test names refer to `TESTING.md`. A step is done only when its test command exits 0. If a copied test fails, the failure is reported in `results/step0.md` and in the final report; the copy is never edited to make it pass (`DESIGN.md` 3.1).

#### Step 0. Preflight (no code in `RL` except the results note)

| Sub-step | What | Where the scratch goes |
|---|---|---|
| 0.1 | the command of section 1 row 1 | none |
| 0.2 | a 20-line scratch script that builds one report whose findings line carries `"class"`, `"probe"` and `"src"`, runs `superclaude.cli.review.merge_cmd.command` through click's `CliRunner` with `--ledger /tmp/rl-step0/ledger.json --doc <a fixture plan> --round 1 --report r1=<report> --out /tmp/rl-step0/merged.md`, and prints the exit code and whether the merged text contains the keys | `/tmp/rl-step0/merge_keys.py`, run with `$PYRUN` |
| 0.3 | `cd $SW && sha256sum -c <(awk -F'\t' '!/^#/ && $3 != "ABSENT" {print $4"  "$2}' $RL/SHARED-MANIFEST-DESIGN-TIME.tsv)` (read-only on `SW`), then `ls -l` of the twelve Tier B paths of that file, then `ls $SW/results $SW/implement-report` to see whether the sibling has written its own step-0 note and report | none |
| 0.4 | with `jq`, list the event types, the assistant block types and the `tool_use` input keys of one finished run of each reviewer model already on disk under `EVAL/<doc>/reviews/combos/` (luna, haiku, sonnet, ember; pick one `*.attempt1.json` each; do not open any ground-truth or score file); the ember shape is already recorded in `DESIGN.md` 7.7 | none |
| 0.5 | time `uv run --frozen --project $REPO python -c "import superclaude.cli.review.findings"` five times and write `RL/results/import-time.md` (the sibling measured 0.28 s once); the number goes into the row-check time budget of `DESIGN.md` 10.1 | none |

Done when `RL/results/step0.md` holds the four answers and the decision taken for each.

#### Step 1. Skeleton, shared copy and the copied tests (about 220 lines of new code)

| Create | Purpose |
|---|---|
| `RL/ruff.toml` | `extend = "../../../../pyproject.toml"` (four levels up from `RL` to `REPO`) |
| `RL/scaffold/__init__.py` is copied; create `RL/rl/__init__.py` and `RL/analysis/__init__.py` | packages (no `lib/` folder anywhere: `.gitignore` line 13) |
| `RL/config/shared-list.json` | the Tier A, S, T and B paths of `DESIGN.md` 3.1, one list per tier |
| `RL/bin/copy-shared.sh` | the behaviour of `DESIGN.md` 3.2: `--check`, `--diff <path>`, two reads 60 s apart for Tier B, `cp` only, `config/shared-manifest.json` |
| `RL/bin/rl-env.sh` | sets `SW_SB_ROOT=/tmp/evalsb-recipe`, accepts the one test hook `RL_FORCE_EXC`, exits 4 on the sibling's root; sourced by every RL script before `common.sh` |
| `RL/fixtures/sibling/make_sibling.py` | F-SIBLING |
| `RL/tests/fakes/claude` | the RL fake of `DESIGN.md` 3.4 (scenarios are added in step 5; step 1 needs only the file and the `ok` scenario so the copied `conftest.py` helper finds it) |

Then run `bash $RL/bin/copy-shared.sh`. It copies Tier A, S, T and whichever Tier B files exist and are stable, and writes the manifest. The copied `scaffold/lint.py`, `scaffold/briefs.py`, `scaffold/cards.py`, `scaffold/fnd.py`, `scaffold/normalise.py`, `bin/common.sh` and `bin/build-sandbox.sh` are not touched afterwards.

Tests: `test_shared_manifest.py`, `test_sibling_readonly.py`, `test_sandbox_root.py`, `test_layout_rl.py`, and the copied `test_paths.py`, `test_model_allowlist.py`, `test_cards.py`, `test_briefs.py`, `test_fnd_contract.py`, `test_lint.py`, `test_normalise.py`, `test_readme.py`, `test_sandbox.py`. Command: `$T $RL/tests -q`. Done when they pass, or each failure of a copied test is written up as a finding with its cause.

#### Step 2. Recipes (about 110 lines of code, about 200 of data and text)

Create `recipes/recipes.json` and `recipes/rl-block.txt` and `recipes/search-form.txt` (extracted from the quoted blocks of `MR` 3.2(a) by a one-time script `rl/extract_mr.py` that prints a diff against the extraction used by `test_recipes_equal_mr_quotes`; the `rl-block.txt` placeholder `{{LENS_ROW_CAP}}` replaces the number 14), `rl/recipes.py` (load, `row_budget(id)`, validate: key set equals card ids, at most 120 words, one budget sentence, no `src/superclaude/` path, no expected-outcome words), `recipes/README.md` (the table of `DESIGN.md` 11.3, REQ-38) and `recipes/REVIEWS.md` (eight rows, status OPEN).

Tests: `test_recipes.py`, `test_recipes_readme.py`, `test_recipes_reviews.py` (the completeness test has marker `freeze`), `test_lint_rl.py` with F-LINT-GT. Command: `$T $RL/tests/test_recipes.py $RL/tests/test_recipes_readme.py $RL/tests/test_recipes_reviews.py $RL/tests/test_lint_rl.py -q -m "not freeze"`. Done when they pass.

#### Step 3. Lens table, lens render and the RL brief (about 290 lines)

Create `config/lenses.json` (`DESIGN.md` 5.1), `config/values.json` (planning `b` per panel and document: 100, 120, 122 for the primary panel, 220, 238, 226 for haiku, 259, 302, 269 for sonnet, as the sibling's file lists them; `c` per model: ember 0.4, luna 2, haiku 4, sonnet 3; the fixed 6 s, the 0.35 share and the hard cap 14 of `lens_row_cap`; the overhead 28, 30, 30; the re-ask constants 30 and 1.35; every value marked planning), `rl/lens.py` (load, validate by the six rules of 5.2, `render`, `lens_row_cap`, `assigned_ids`, `E_LENS_INVALID`), `rl/render.py` (brief assembly of 6.1 on top of `scaffold.briefs.render("Z0", ...)`, the heading, the search-form line, `run.json` fields), `rl/cli.py` with subcommands `lens` (`--validate`, `--panel`, `--doc`, `--out`) and later `check`, `reask`. Create `fixtures/lens/make_lens.py`.

Tests: `test_lens.py`, `test_render.py`, `test_targets.py`, `test_ablation.py`, `test_ground_truth_not_read.py` (render part). Command: `$T $RL/tests/test_lens.py $RL/tests/test_render.py $RL/tests/test_targets.py $RL/tests/test_ablation.py $RL/tests/test_ground_truth_not_read.py -q`. Done when they pass. Checkpoint: `$PYRUN $RL/rl/cli.py lens --validate` prints the three panels and exits 0.

#### Step 4. Ledger check, promotion and the re-ask (about 330 lines, plus about 360 if Tier B is built locally)

Order inside the step, so a stop after any sub-step leaves working code:

| Sub-step | Create or extend | Tests |
|---|---|---|
| 4.1 | `scaffold/ledgerv1.py` if it is not a copy (the reader of `SWD` 9.1 and the quote checks of 9.2 with the corpora of DR-9) and `scaffold/telemetry.py`; the fixtures `fixtures/reports/make_rl_reports.py` and `fixtures/transcripts/make_transcripts.py` | `test_rowcheck.py` (REQ-13, REQ-14) |
| 4.2 | linking, demotion and the CB-3 sentence (`SWD` 9.3) | `test_rowcheck.py` (REQ-16) |
| 4.3 | promotion with `FND._check_finding` and the RL limits of `DESIGN.md` 7.2 check 10 | `test_rowcheck.py` (REQ-15) |
| 4.4 | `rl/ledger_api.py` (the adapter, at most 40 lines) and `rl/rowcheck.py`: id grammar, recipe coverage, budgets, `NONE FOUND`, `check.json`, `classes_lost`, the `check` subcommand of `rl/cli.py` | `test_rowcheck.py` (REQ-26, DR-5, DR-6) |
| 4.5 | `rl/reask.py` (`reask_allowed` with the clock as an argument and `math.isclose` tolerance 1e-9 on the boundary, the repair prompt, the acceptance rule, the `reask` subcommand) | `test_reask.py` (REQ-27) |

Tests command: `$T $RL/tests/test_rowcheck.py $RL/tests/test_reask.py -q`. Done when they pass and the check of three fixture reports takes under 1 s.

#### Step 5. Fake claude, launcher, clock, hang guard (about 560 lines)

Create the remaining scenarios of `tests/fakes/claude` (`DESIGN.md` 3.4), `scaffold/clock.py` if it is not a copy (the arithmetic of 9.3 and 9.4: `kill_s` is not needed; `hang_s`, `breakeven_row_cost`, `lens_row_cap` imported from `rl/lens.py`), `bin/run-reviewer.sh` (the `SWD` 11.1 table, if it is not a copy), `bin/run-panel.sh` (section 9.1: arms Z0-raw, Z0, K, RL; sandbox check; clock; lens render with fallback; three reviewers with the hang guard; check and re-ask; H2; merge; `run.json`, `timing.json`; sandbox-clean check; `--dry-run`; exit codes). Copy-in of `config/packages.json` is already done by step 1 (Tier S).

Before writing `clock.py`, finish sub-step 0.5 (`results/import-time.md`).

Tests: `test_fake_claude_rl.py`, `test_clock.py`, `test_hang_guard.py`, `test_fallback.py`, `test_run_panel_fake.py`, `test_sandbox_clean.py`, `test_run_json_fields.py`, `test_blindness.py`, `test_verifier_off_path.py`. Command: `$T $RL/tests/test_fake_claude_rl.py $RL/tests/test_clock.py $RL/tests/test_hang_guard.py $RL/tests/test_fallback.py $RL/tests/test_run_panel_fake.py $RL/tests/test_sandbox_clean.py $RL/tests/test_run_json_fields.py $RL/tests/test_blindness.py $RL/tests/test_verifier_off_path.py -q`. Done when they pass.

Checkpoint: the rehearsal A7 of `TESTING.md` 5.1 (RL arm on the fake claude over the real sandbox of one study document).

#### Step 6. Judge copy, analysis, ran check (about 700 lines)

Create or copy `bin/judge-one.sh` (a copy of `JJ` with its paths as variables and the `BRIEF` text byte for byte), `bin/anon.sh`, `bin/judge-batch.sh`; `analysis/analyze.py` (sub-commands `all`, `audit-judges`, `compliance`, `prereg`, `sample-second-judge`, `ablate-report`; every metric of `DESIGN.md` 12.5; Wilson intervals; a bootstrap that resamples documents first and then runs; gates D1 to D7; the three shares; the REQ-45 claim sentence); `analysis/ran_check.py` (7.7); `analysis/g0.py` (the ledger-and-time half only). Create fixtures F-GT and F-RUNS-RL.

Tests: `test_analyze.py`, `test_report.py`, `test_stages.py`, `test_prereg.py`, `test_judge.py`, `test_ran_check.py`. Command: `$T $RL/tests/test_analyze.py $RL/tests/test_report.py $RL/tests/test_stages.py $RL/tests/test_prereg.py $RL/tests/test_judge.py $RL/tests/test_ran_check.py -q`. Done when they pass.

#### Step 7. Schedule, spikes, freeze and order scripts (about 450 lines)

Create `bin/make-schedule.py` (block-randomised, recorded seed, the stage and set options of `TESTING.md` 5; 75 lines for Stage 1 as designed), `bin/run-schedule.sh` (`--max-panels`, default 1; refuses without the spike record), `bin/run-spike.sh` (timing and compliance), `bin/freeze.sh` (hashes, prints the tag command, never tags), `bin/check-order.sh` (`freeze` and `prereg`), `bin/check-sandbox-gt.sh`, `bin/check-z0-parity.sh`, `bin/open-manual-checks.sh`.

Tests: `test_run_schedule.py`, `test_freeze.py`, `test_order.py`, `test_check_scripts.py`. Command: `$T $RL/tests/test_run_schedule.py $RL/tests/test_freeze.py $RL/tests/test_order.py $RL/tests/test_check_scripts.py -q`. Done when they pass.

#### Step 8. Build checkpoint

`$T $RL/tests -q -m "not slow and not freeze"`, then `$T $RL/tests -q -m slow`, `uv run --frozen --project $REPO ruff check $RL` and `ruff format --check $RL`, the baseline of step 0.1, `bash $RL/bin/copy-shared.sh --check`, and the rehearsal A7. All must exit 0. Save the summary lines to `RL/results/tests-final.log`. This is the point at which the build is "done" in the sense of `TESTING.md` section 6.

#### Step 9. `RL/IMPLEMENTATION-REPORT.md`

Write the report that the build plan's last step requires. It states: what was built (per step, with file lists); which Tier B files were copied and which were built locally (from `config/shared-manifest.json`); the test counts per kind (U, I, C, F) and the summary lines; the exact commands of `TESTING.md` 5.4 for each of the three study packages (`designSpec`, `makeTheAliasOnly`, `design`) for the RL arm and for the Z0 arm; every requirement not met or only partly met, with the reason (including the M records still open from `bin/open-manual-checks.sh`); the findings about copied tests that failed; and the list of decisions of `DESIGN.md` 13.1 that are still open.

## 3. Steps that are not part of the build plan

### Step 10. Inputs to the freeze (people and decisions; no model)

| Order | Action | Who |
|---|---|---|
| 10.1 | fill `recipes/REVIEWS.md`: the swap test and a read for issue-specific words, one row per recipe | a second author, who has not seen the ground truth |
| 10.2 | read `recipes/README.md` and sign its footer (REQ-38) | a second reader |
| 10.3 | decide the open items of `DESIGN.md` 13.1 (items 5, 6 and 7 are needed at the freeze) and write `config/owner-values.json` | the owner |
| 10.4 | decide whether the Z0, K and Z0-raw blocks are shared with the sibling (DR-12) | the owner |
| 10.5 | author the planted set, the clean twins and the hold-out ground truth in a place that is not inside `RL` before the freeze, by someone who has not seen the recipes or the lens table (REQ-36) | the hold-out author |

### Step 11. Freeze (no model)

| Order | Action | Who |
|---|---|---|
| 11.1 | `$T $RL/tests -q -m freeze`; B1 of `TESTING.md` 5.2 (the lint over the real ground truth) | the maintainer |
| 11.2 | `bash $RL/bin/freeze.sh`, review its output, run the printed `git tag` command | a person (K5) |
| 11.3 | the hold-out author commits `holdout-gt/`; then B5 to B8 of `TESTING.md` 5.2 | the hold-out author, then the maintainer |

### Step 12. Run the experiment (models; owner go-ahead for each part)

Spikes (C), one panel per arm (D), Stage 1 (E), Stage 2 for the arms that pass (F), derivation-set check (5.5) and decision (G): the commands are in `TESTING.md` section 5. The experiment is not part of this design's build.

### Step 13. Adoption (only if the pre-registered gates pass)

Adoption is its own plan. It moves the recipes, the lens table and the row check into `src/superclaude/cli/review/` (a `recipes` subpackage and a `superclaude review` option), applies CB-1 to CB-5 to `src/superclaude/rules/prompts/document_review_loop_prompts.md` (`SWD` DD-1; one edit shared by both redesigns), runs `make sync-dev` and `make verify-sync`, adds tests under `tests/review/`, and updates the installed-path rules (no `src/superclaude/` path inside an installed primitive). It needs its own `/sc:workflow` plan and its own review, and is not specified further here.

## 4. Dependencies between steps

```
0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12 -> 13
          1 -> 4.1 (the Tier B ledger code, if it is not a copy, can start as soon as step 1 is done)
               4 -> 6 -> 8
          5 -> 6   (the analysis tests use run folders that the launcher writes)
```

Steps 2 and 4.1 can run in parallel after step 1. Step 3 needs step 2 (the lens renders recipes). Step 4 needs step 3 (the assigned row ids come from the lens). Step 5 needs steps 3 and 4. Step 6 needs steps 4 and 5. Step 7 needs step 5. Step 8 needs 5, 6 and 7.

When the sibling's Tier B files appear after step 1 has run, do not re-copy in the middle of a step: finish the step, then run `bin/copy-shared.sh --diff <path>` for each Tier B file that RL built locally, read the diff, and record the outcome in `results/step0.md`. A local file is replaced only by a person's decision.

## 5. Risks to watch while building

| Risk | Where it shows | Response |
|---|---|---|
| The sibling's Tier B files appear or change while this build runs | step 0.3, `copy-shared.sh --check` | the rule of `DESIGN.md` 3.1: copy if stable, else build locally; never replace silently; `--diff` before any swap |
| A copied test fails in `RL` because of a path or layout assumption | step 1 | report it with its cause; do not edit the copy; if the copy is wrong for `RL`, say so in the report and write an RL test with a different name |
| The sibling edits a Tier A file after the copy (a card, a brief part) | `copy-shared.sh --check` | `drift` is a warning: decide with the owner whether to recopy; a recopy is a re-freeze if it happens after step 11 |
| The real merge rejects the telemetry keys | step 0.2 | side file keyed by finding id; `DESIGN.md` 7.2 check 11 and the blindness test change |
| Luna, haiku or sonnet transcripts differ from the ember shape | step 0.4 | the `transcript` corpus and `ran_check.py` accept both shapes before step 4 |
| A model does not copy quotes exactly, so rows are demoted for format only | the compliance spike (`TESTING.md` 5.3) | report `format_induced_demotions`; widen the corpora only with the owner's approval |
| A model writes the ledger before the final message, so it is lost | the compliance spike | `ledger_missing` rate; the ember re-ask covers ember only (DR-8) |
| `@file` text reaches the model without a `Read` call, so reading rows have no tool call to check | step 0.4, the `ran` manual audit | `not_a_tool_claim` stays as defined; the audit decides whether the heuristic is reported |
| The time margin is 1 s at b = 100 with 14 rows | the timing spike | `lens_row_cap` lowers the cap; `no_budget` refuses a panel that cannot hold one row per recipe |
| Two builds share one gateway | `run-schedule.sh --max-panels` | default 1; raise only while the sibling is idle (DR-12, 13.1 item 10) |
| The hold-out documents need `packages.json` entries | step 11 | Tier S: the hold-out author appends them to `RL/config/packages.json`; `--check` ignores that file |
| The two builds' Z0 or K arms drift apart (a recopy of a brief part in one build only) | `bin/check-z0-parity.sh` | compare the Z0 brief hash with the sibling's before every block |
| Anything wants to write outside `RL` | `sw_assert_writable` (copied) | stop; it is a defect in the step, not a reason to relax K1 |
| A recipe wording change after the compliance spike | spike results | `override` entry, owner approval, re-freeze (`DESIGN.md` 4.1, 4.6) |
