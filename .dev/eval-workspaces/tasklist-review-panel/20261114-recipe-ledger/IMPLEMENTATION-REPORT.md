# Recipe Ledger: implementation report

Written 2026-11-15 by the build that executed the plan package `.dev/tasks/to-do/TASK-WF-implementRedesig-20261114-231318/` (Tasks 1 to 20) on branch `ironbelly/eval-tasklist-review-panel`, base commit `6225ac3fd`. Nothing is staged, committed or pushed by this build, and the freeze tag (K5) has not been created.

Paths: `RL` is `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger` (this folder), `SW` is the sibling build `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet` (read only), `EVAL` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`, `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`. Design ids (`K1` to `K9`, `DR-1` to `DR-16`, `REQ-nn`) are those of `RL/DESIGN.md` 1.2 and 1.3 and `RL/TESTING.md` 3.

**Where the build stands, in one paragraph.** The no-model build of Recipe Ledger exists and passes its tests on a fake `claude`: of 550 collected tests, 546 pass under the plan's own environment exports (490 fast plus 56 integration), 3 `freeze` tests are collected and were not run, and 1 copied sibling test fails for a cause that is not in this build (547 pass with that one variable unset; section 3). `bin/run-panel.sh` runs the Z0, K, Z0-raw and RL arms end to end on the fake. Nothing in this build shows that Recipe Ledger works: no model, judge or network call was made, so no recipe has been tried on a real reviewer (section 6).

Legend used below. **RUNS**: executed in this build by the tests or the rehearsal, on invented fixtures and the fake `claude`. **WRITTEN, NOT RUN**: complete code that needs a model or the real ground truth, so this build only ran its refusal path or its unit tests. **NOT BUILT**: absent. **STUBBED**: a placeholder standing in for real behaviour; there is none (a search of `rl/`, `analysis/`, `bin/` and `scaffold/` for `NotImplemented`, `TODO`, `FIXME`, `XXX` and `stub` finds only `mktemp` template names and a comment in the copied `bin/common.sh` about the kill test's sleep stubs).

## 1. What was built, per phase

All paths below are under `RL`. About 7,100 lines of code sit in `rl/`, `analysis/`, `scaffold/` and `bin/` (`wc -l`, copied files included); the largest file is `analysis/analyze.py` (1,549 lines).

### Phase 1 (Tasks 1 to 3): preflight, skeleton, shared copy. RUNS

- Preflight (Task 1): `results/step0.md` (four answers: `tests/review` 126 passed; the real merge accepts `class`, `probe` and `src` and keeps them out of the merged report; the sibling's state; the transcript shapes), `results/import-time.md` (five timings and the median).
- Skeleton (Task 2): `ruff.toml`, `rl/__init__.py`, `analysis/__init__.py`, `config/shared-list.json`, `bin/copy-shared.sh` (reads `SW`, never writes there; `--check`, `--diff`), `bin/rl-env.sh` (sandbox root `/tmp/evalsb-recipe`, test hook `RL_FORCE_EXC`, exit 4 on the sibling's root), `fixtures/sibling/make_sibling.py`, `tests/fakes/claude`.
- Shared copy (Task 3): `config/shared-manifest.json` (60 entries, section 2), copies `scaffold/{__init__,briefs,cards,fnd,lint,normalise}.py`, `cards/`, `briefs/`, `bin/common.sh`, `bin/build-sandbox.sh`, `config/packages.json` and nine copied test files with `tests/helpers.py` and `tests/conftest.py`; new tests `tests/test_shared_manifest.py`, `test_sibling_readonly.py`, `test_sandbox_root.py`, `test_layout_rl.py`.

### Phase 2 (Tasks 4 to 6): recipes, lens table, RL brief. RUNS

- Recipes (Task 4): `recipes/recipes.json` (eight recipes C1 to C8, schema `rl-recipes/1`), `recipes/rl-block.txt`, `recipes/search-form.txt`, `recipes/README.md` (re-derive table), `recipes/REVIEWS.md` (eight rows, all OPEN), `rl/recipes.py`, `rl/extract_mr.py`, `fixtures/gt/lint-gt.json`; tests `test_recipes.py`, `test_recipes_readme.py`, `test_recipes_reviews.py`, `test_lint_rl.py`.
- Lens table (Task 5): `config/lenses.json` (three panels, three roles each), `config/values.json` (planning values only; no `spike` record), `rl/lens.py` (six validation rules, `render`, `lens_row_cap`), `fixtures/lens/make_lens.py`; tests `test_lens.py`, `test_model_allowlist_rl.py`.
- Brief renderer (Task 6): `rl/render.py` (the RL brief is the copied renderer's Z0 text plus the ledger rule, the RL block, the heading and the reviewer's recipes; a fallback brief equals Z0), `rl/cli.py` (sub-commands `lens`, `check`, `reask`, `plan`, `briefs`, `prepare-merge`, `record`), `tests/rl_support.py`; tests `test_render.py`, `test_targets.py`, `test_ablation.py`, `test_ground_truth_not_read.py`.

### Phase 3 (Tasks 7 to 10): ledger row check, promotion, ember re-ask. RUNS on fixtures

- Reader and quote checks (Task 7): `scaffold/ledgerv1.py`, `scaffold/telemetry.py` (both built locally, section 2), `fixtures/reports/make_rl_reports.py`, `fixtures/transcripts/make_transcripts.py`; tests in `test_rowcheck.py`, `test_telemetry.py`.
- Link, demote, promote (Task 8): in `scaffold/ledgerv1.py`; tests in `test_rowcheck.py`.
- Row check and adapter (Task 9): `rl/ledger_api.py` (the one adapter), `rl/rowcheck.py`, the `check` sub-command; writes `check/<rid>.ledger.json`, `check/<rid>.checked.md`, `check/check.json`.
- Re-ask (Task 10): `rl/reask.py` (`reask_allowed` takes the clock as an argument; the repair prompt; the acceptance rule), the `reask` sub-command; tests `test_reask.py`.

### Phase 4 (Tasks 11 to 13): fake claude, launcher, clock, hang guard. RUNS

- Fake claude (Task 11): `tests/fakes/claude` with every scenario of the plan (`ok`, `problem`, `none_found`, `ledger_missing`, `ledger_after_findings`, `over_budget`, `recipe_missing`, `long_anchor`, `bad_block`, `api_error`, `wrong_model`, `sleep`, `exit127`, `repair`); `tests/test_fake_claude_rl.py`.
- Clock and reviewer script (Task 12): `scaffold/clock.py` (built locally), `bin/run-reviewer.sh` (built locally; one attempt, `NOFALLBACK=1` required, read-only tools), `tests/test_hang_guard.py`, `test_clock.py`, `test_report.py` (break-even part), `test_run_reviewer.py`.
- Launcher (Task 13): `bin/run-panel.sh` for the arms Z0-raw, Z0, K and RL, with the lens-render fallback, the check-skipped fallback, the ember re-ask and the merge through the real `superclaude review merge`; `tests/panel_support.py`, `test_run_panel_fake.py`, `test_fallback.py`, `test_sandbox_clean.py`, `test_run_json_fields.py`, `test_blindness.py`, `test_verifier_off_path.py`. Rehearsals on the fake over the real sandbox of one study document: `runs/rehearsal-rl`, `-Z0`, `-K`, `-Z0-raw`, `-rl-check-fail`, `-rl-lens-fail`, and in Task 19 `runs/rehearsal-rl-final` and `runs/rehearsal-rl-clean`.

### Phase 5 (Tasks 14 to 16): judge copy, analysis, ran check

- Judge scripts (Task 14): `bin/judge-one.sh`, `bin/anon.sh`, `bin/judge-batch.sh`, `analysis/judge_audit.py`, `fixtures/judge/make_judge.py`; `tests/test_judge.py`. RUNS: anonymisation, the sample, the audit and the `BRIEF` hash check, on synthetic judge folders. WRITTEN, NOT RUN: `bin/judge-one.sh` and the judge call of `bin/judge-batch.sh`, which start the blind Opus judge and refuse without `--go`; no judge was started.
- Analysis (Task 15): `analysis/analyze.py` (sub-commands `all`, `audit-judges`, `compliance`, `prereg`, `sample-second-judge`, `ablate-report`; every metric of `DESIGN.md` 12.5 defined only there; Wilson intervals; bootstrap; gates D1 to D7; the three shares; the REQ-45 claim sentence), `fixtures/gt/synthetic-gt.json`, `fixtures/runs/make_runs.py` and `expected.json` (hand-computed); tests `test_analyze.py`, `test_report.py`, `test_stages.py`, `test_prereg.py`. RUNS on the synthetic runs; it has never run over real runs.
- Ran check (Task 16): `analysis/ran_check.py` (a heuristic, as its header says), `analysis/g0.py` (the ledger-and-time half of G0 only), `fixtures/runs/make_ran_runs.py`; tests `test_ran_check.py`, `test_g0.py`.

### Phase 6 (Tasks 17 and 18): schedule, spikes, freeze and order scripts

- Task 17: `bin/make-schedule.py` (RUNS: 60 rows for Stage 1 plus 15 for the Z0-raw append, seed recorded), `bin/run-schedule.sh` (RUNS against the fake only; refuses without a `spike` record), `bin/run-spike.sh` and `rl/spike.py` (WRITTEN, NOT RUN: both modes need models; only the refusal without `--go` runs), `tests/test_run_schedule.py`.
- Task 18: `bin/freeze.sh` (prints the tag command, never tags), `bin/check-order.sh` (`freeze`, `prereg`, `gt-hash`, `twins`), `bin/check-sandbox-gt.sh`, `bin/check-z0-parity.sh`, `bin/open-manual-checks.sh`, `bin/ran-audit.py`, `tests/order_support.py`; tests `test_freeze.py`, `test_order.py`, `test_check_scripts.py`. RUNS on temporary git repositories and invented sandboxes. The real freeze, the real order checks and the real-sandbox check were not run (they belong to the freeze, section 5).

### Phase 7 (Tasks 19 and 20): full run and this report

- `results/tests-final.log` (every command with its exit code, section 3), an addendum in `results/step0.md`, and this file.

**NOT BUILT** in this build: the model-stage leave-one-class-out ablation (96 panel runs, `DR-13`); the optional verifier (only the seam is tested, `REQ-46`); the selection half of G0 and everything of Redesign 1 (`REQ-18` to `REQ-24`); the real hold-out ground truth, `config/prereg.json`, `config/attestation.md`, `config/freeze.json` and the freeze tag; the spike record in `config/values.json`; any real run, score or report.

## 2. Tier B files: copied or built locally

Source: `config/shared-manifest.json` (written by `bin/copy-shared.sh` in Task 3) and the drift output of `bash bin/copy-shared.sh --check` on 2026-11-15.

**State of the sibling at copy time (Task 3):** all twelve Tier B paths were still absent in `SW`, so none was copied. All 48 other shared files (27 Tier A, 1 Tier S, 20 Tier T) were copied by `sha256sum` then `cp` and match their recorded hashes (`--check`: 59 checked, 0 failed; Tier S is recorded once and not compared).

**Copied: none of the twelve. Built locally: all twelve**, each to the written contract of the sibling's design (`SWD` section in the last column). Their manifest hash is still `ABSENT`: `copy-shared.sh` records a hash only when it runs again with a Tier B file present in `SW`, and it has not been re-run in copy mode.

| Tier B file | Kind | Sibling's design section (`SWD`) |
|---|---|---|
| `scaffold/ledgerv1.py` | built-local | 9.1 to 9.3 (reader, checks, linking, demotion, promotion) |
| `scaffold/telemetry.py` | built-local | 9.2 and DD-12 (`class`, `probe`, `src` keys) |
| `scaffold/clock.py` | built-local | 11.4 (panel clock, `hang_s`, break-even helpers) |
| `bin/run-reviewer.sh` | built-local | 11.1 (one attempt, hang guard, model-identity check) |
| `bin/run-panel.sh` | built-local | 11.4 to 11.7 (clock, hang guard, concurrency, merge) |
| `bin/judge-one.sh` | built-local | 11.3 (blind judge, `claude-opus-5-5` only) |
| `bin/anon.sh` | built-local | 11.3 (anonymisation) |
| `bin/judge-batch.sh` | built-local | 11.3 (judge batch) |
| `bin/make-schedule.py` | built-local | 11.6 (block-randomised schedule) |
| `bin/run-schedule.sh` | built-local | 11.6 (schedule runner) |
| `analysis/analyze.py` | built-local | 14.3 (analysis outputs) |
| `analysis/g0.py` | built-local | 14.1 (ledger-and-time half of gate G0 only) |

**State of the sibling at the end of this build, and what is not reconciled.** The sibling build has kept writing since the copy. `bash bin/copy-shared.sh --check` ends with `59 checked, 15 drift (warning), 0 failed` (exit 0). Twelve drift lines say "built-local, but the sibling now has a file of that name": all twelve files of the table. Nothing was compared with them and nothing was changed to match them. Three more say that a copied file changed in the sibling after the copy (`bin/common.sh`, `tests/test_briefs.py`, `tests/test_paths.py`); our copies still equal the hashes recorded at copy time. `bash bin/copy-shared.sh --diff <path>` shows the difference for each, and a person decides whether to adopt the sibling's version (`DR-11`). Until that is done, the two builds' Tier B files may differ in behaviour, and DR-12 (the two builds read alike) is not shown for them.

## 3. Test counts and summary lines

Source: `results/tests-final.log` (Task 19, 2026-11-15; every line below is copied from it). Commands were run from the repository root with `PYTHONDONTWRITEBYTECODE=1 NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` and `T="uv run --frozen --project $REPO pytest -p no:cacheprovider"`. All tests used the fake `claude`.

| Command | Summary line | Exit |
|---|---|---|
| `$T $RL/tests -q -m "not slow and not freeze"` | `1 failed, 490 passed, 59 deselected in 30.55s` (0 skipped) | 1 |
| the same with `NOFALLBACK` unset | `491 passed, 59 deselected in 29.80s` | 0 |
| `$T $RL/tests -q -m slow` | `56 passed, 494 deselected in 132.80s (0:02:12)` (0 failed, 0 skipped) | 0 |
| `$T $RL/tests -q --collect-only -m freeze` (NOT run) | `3/550 tests collected (547 deselected) in 1.43s` | 0 |
| `uv run --frozen --project $REPO ruff check $RL` | `All checks passed!` | 0 |
| `uv run --frozen --project $REPO ruff format --check $RL` | `166 files already formatted` (179 after the rehearsal added run-folder files) | 0 |
| `$T $REPO/tests/review -q` | `126 passed in 0.97s` (the same count as Task 1) | 0 |
| `bash $RL/bin/copy-shared.sh --check` | `59 checked, 15 drift (warning), 0 failed` | 0 |
| `$PYRUN $RL/rl/cli.py lens --validate` | prints the three panels | 0 |
| rehearsal A7 on the fake (`--run-id rehearsal-rl-clean`) | `arm=RL panel=primary fallback=0 check_skipped=0 merged=3 merge_exit=0`; call log: 3 `review` lines, no `repair` line | 0 |

**Test counts by kind** (from the test files and markers; 550 collected): **U 412** (unit tests written by this build), **I 56** (integration tests, marker `slow`, `bin/run-panel.sh` on the fake `claude`), **C 79** (tests of the nine copied files `test_paths`, `test_model_allowlist`, `test_cards`, `test_briefs`, `test_fnd_contract`, `test_lint`, `test_normalise`, `test_readme`, `test_sandbox`, run unchanged), **F 3** (marker `freeze`, collected and not run). 412 + 56 + 79 + 3 = 550.

**The one failing test, a copied test, cause recorded, copy not edited:** `tests/test_model_allowlist.py::test_nofallback_guard`. The copied `helpers.py` removes only `SW_*` variables from the environment, so the `NOFALLBACK=1` that every command of this plan exports reaches the check "NOFALLBACK unset must fail" and `sw_assert_nofallback` returns 0 where the test expects 1. With `NOFALLBACK` unset that file gives `4 passed` and the whole fast suite gives `491 passed`.

**The three `freeze` tests were collected and NOT run, on purpose:**
- `tests/test_lint.py::test_real_files_against_real_gt` (copied; it needs the real ground-truth glob from a maintainer),
- `tests/test_lint_rl.py::test_real_recipes_against_real_gt` (reads the real ground truth),
- `tests/test_recipes_reviews.py::test_review_record_complete` (needs the second author's rows in `recipes/REVIEWS.md`, `REQ-08`).

They are run at the freeze (`IMPLEMENTATION.md` step 11), by a person who may read the real ground truth.

**A process defect found and corrected during Task 20.** During the Task 18 review a reviewer sub-session ran `bin/freeze.sh` without `--no-write` and left `config/freeze.json`; the Task 19 rehearsal `runs/rehearsal-rl-final/run.json` therefore holds `freeze_tag: "rl-freeze-094c1a314886"` although that tag was never created. The stray file was removed, the rehearsal was rerun on the clean tree as `runs/rehearsal-rl-clean` (`freeze_tag: null`), and `git tag -l` was identical before and after. Details are in the addendum of `results/tests-final.log` section 7. The folder `runs/rehearsal-rl-final/` is kept as written and is not clean evidence.

**Protected paths.** `git status --porcelain -- src tests .claude` prints nothing. No file under `EVAL` or the collab folder is newer than the start of the build. `SW` is untracked as a whole, so git cannot show per-file changes there; this build only reads it (`copy-shared.sh`, canary test `tests/test_sibling_readonly.py`). Under `.dev/tasks/` only this plan package changed.

## 4. Commands to run one panel on each study package (not run against any model by this build)

**These commands were NOT run against any model by this build.** The plan allowed only the fake `claude`. The only run of `bin/run-panel.sh` here is the rehearsal on the fake (section 3); the first real panel is a decision for the owner. They are taken from `RL/TESTING.md` 5.4 and 5.5. One panel is three reviewer sessions: `t2b-1` = `muse-ember-1.0` (the search role), `t4-1` and `t3-1` = `gpt-6-luna`, one attempt each (`NOFALLBACK=1`), run in parallel and blind to each other. Z0 is the control arm (the isolated panel with H1 to H4 and CB-1 to CB-5; no recipes, no ledger rule); RL adds the ledger rule, the RL block and each reviewer's recipes, plus one ember repair call only if its ledger is missing and the clock allows it. Run **one panel at a time**, and the Z0 panel and the RL panel of one document in the **same block**, one after the other on the same day. Planning elapsed time is about b + 28 s for RL and b for Z0 (b about 100 to 122 s; unmeasured). The three study packages are a derivation-set check: reported, never used for an adoption decision.

Environment, once per shell, from the repository root:

```
cd "$(git rev-parse --show-toplevel)"
export REPO=$(git rev-parse --show-toplevel)
export RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
export PYRUN="uv run --frozen --project $REPO python"
export SW_SB_ROOT=/tmp/evalsb-recipe          # bin/rl-env.sh sets it too; the sibling uses /tmp/evalsb-sweep and is refused (exit 4)
export NOFALLBACK=1                           # required: one attempt per reviewer, no fallback model
export PYTHONDONTWRITEBYTECODE=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
```

Before the first arm, `bash $RL/bin/open-manual-checks.sh` shows what is still open, and the plan expects `config/values.json` to hold the timing-spike record before any schedule (a single panel run does not need it).

**Package 1, `TASK-WF-designSpec-20261107-075614`** (the one whose sandbox the rehearsal built, under `/tmp/evalsb-recipe-rehearsal`):

```
bash $RL/bin/build-sandbox.sh TASK-WF-designSpec-20261107-075614
bash $RL/bin/run-panel.sh --arm RL --panel primary --doc TASK-WF-designSpec-20261107-075614 --replicate 1 --block 1 --seed 20261115 --run-id derive-RL-dry-TASK-WF-designSpec-20261107-075614 --dry-run
bash $RL/bin/run-panel.sh --arm Z0 --panel primary --doc TASK-WF-designSpec-20261107-075614 --replicate 1 --block 1 --seed 20261115 --run-id derive-Z0-TASK-WF-designSpec-20261107-075614
bash $RL/bin/run-panel.sh --arm RL --panel primary --doc TASK-WF-designSpec-20261107-075614 --replicate 1 --block 1 --seed 20261115 --run-id derive-RL-TASK-WF-designSpec-20261107-075614
```

**Package 2, `TASK-WF-makeTheAliasOnly-20261105-051649`:**

```
bash $RL/bin/build-sandbox.sh TASK-WF-makeTheAliasOnly-20261105-051649
bash $RL/bin/run-panel.sh --arm RL --panel primary --doc TASK-WF-makeTheAliasOnly-20261105-051649 --replicate 1 --block 1 --seed 20261115 --run-id derive-RL-dry-TASK-WF-makeTheAliasOnly-20261105-051649 --dry-run
bash $RL/bin/run-panel.sh --arm Z0 --panel primary --doc TASK-WF-makeTheAliasOnly-20261105-051649 --replicate 1 --block 1 --seed 20261115 --run-id derive-Z0-TASK-WF-makeTheAliasOnly-20261105-051649
bash $RL/bin/run-panel.sh --arm RL --panel primary --doc TASK-WF-makeTheAliasOnly-20261105-051649 --replicate 1 --block 1 --seed 20261115 --run-id derive-RL-TASK-WF-makeTheAliasOnly-20261105-051649
```

**Package 3, `TASK-WF-design-20261108-041415`:**

```
bash $RL/bin/build-sandbox.sh TASK-WF-design-20261108-041415
bash $RL/bin/run-panel.sh --arm RL --panel primary --doc TASK-WF-design-20261108-041415 --replicate 1 --block 1 --seed 20261115 --run-id derive-RL-dry-TASK-WF-design-20261108-041415 --dry-run
bash $RL/bin/run-panel.sh --arm Z0 --panel primary --doc TASK-WF-design-20261108-041415 --replicate 1 --block 1 --seed 20261115 --run-id derive-Z0-TASK-WF-design-20261108-041415
bash $RL/bin/run-panel.sh --arm RL --panel primary --doc TASK-WF-design-20261108-041415 --replicate 1 --block 1 --seed 20261115 --run-id derive-RL-TASK-WF-design-20261108-041415
```

In each block the second line is the `--dry-run` look: it writes `briefs/`, `lens/` and `run.json` under `$RL/runs/derive-RL-dry-<doc>/`, prints the three `claude` command lines with their brief hashes and starts no model (it needs its own run id, because `run-panel.sh` refuses a run folder that exists). The third and fourth lines are the six panel commands: three documents times the Z0 arm and the RL arm, 18 reviewer sessions in all (plus any ember repair call). The Z0 arm of a document is run before its RL arm. The other two control arms use the same script: `--arm K` (Z0 plus the plain-words paragraph) and `--arm Z0-raw` (it needs `bash $RL/bin/build-sandbox.sh --raw <doc>` first).

What to read afterwards (no model), for one document (`D` is the document id):

```
D=TASK-WF-designSpec-20261107-075614
jq '{arm,panel,fallback,no_source,c2_not_applicable,check_skipped,reask,row_cap}' $RL/runs/derive-RL-$D/run.json
jq . $RL/runs/derive-RL-$D/timing.json                    # panel_elapsed_s, slowest_reviewer_s, reask_s
jq . $RL/runs/derive-RL-$D/check/check.json               # ledger_missing, recipe_missing, over_budget, rows, demoted, promoted
jq -s '.[0].panel_elapsed_s / .[1].panel_elapsed_s' $RL/runs/derive-RL-$D/timing.json $RL/runs/derive-Z0-$D/timing.json   # one-run look at the +35% rule; the gate itself is a median over a block
sed -n 1,80p $RL/runs/derive-RL-$D/merged/merged-1.md     # the merged report
$PYRUN $RL/analysis/ran_check.py $RL/runs/derive-RL-$D    # REQ-28: ran status per row (a heuristic, not yet audited by a person)
```

**Scoring needs the owner's go-ahead, because it starts the blind Opus judge** (`claude-opus-5-5`, the only model name allowed in `bin/judge-one.sh`; it reads the document's real ground truth, which is what scoring is). The script refuses without `--go`:

```
bash $RL/bin/judge-batch.sh --dry --runs derive-Z0-TASK-WF-designSpec-20261107-075614 derive-RL-TASK-WF-designSpec-20261107-075614   # no judge: writes the anonymised reports and prints the plan
bash $RL/bin/judge-batch.sh --go --runs derive-Z0-TASK-WF-designSpec-20261107-075614 derive-RL-TASK-WF-designSpec-20261107-075614   # starts the blind judge: only after the owner says go
```

Use the same two lines with the other two document ids. A single pair of runs shows that the arm runs and what its ledger looks like; it is not evidence for or against adoption.

## 5. Requirements not met or only partly met, and requirements met

Status words: **Met** means every row of `RL/TESTING.md` section 3 for that requirement that this build can run is backed by a passing test (named), and no manual or real-run row remains. **Partly met** means the automated part passes and a manual (M) or real-run (X) row is still open; the open part and the reason are given. **Not met** means the required record or behaviour does not exist. **Not built** means it belongs to Redesign 1 or is out of this build. A "met" here shows the code does what the test says on invented fixtures and the fake `claude`; it does not show that Recipe Ledger raises the found fraction.

### 5.1 Requirements not met or only partly met

| REQ | Status | What is open and why |
|---|---|---|
| REQ-08 | **Not met** | `recipes/REVIEWS.md` has eight rows C1 to C8, all `OPEN` with reviewer and date empty. The second-author review must be written by a person who has not seen the ground truth. The `freeze` test `test_recipes_reviews.py::test_review_record_complete` was collected and not run. |
| REQ-17 | Partly met | The check itself passes (`test_analyze.py::test_compliance_report_on_fixture`). The spike it should be run on (5 compliance runs, `ledger_missing` at most 10%) needs models and was not run. |
| REQ-28 | Partly met | The unit part passes (`test_ran_check.py`, four tests). The 20-row audit by a person (agreement on at least 18 of 20 rows, `results/ran-audit.md`) is open: it needs spike runs. `analysis/ran_check.py` is a heuristic until then. |
| REQ-31 | Partly met | Break-even values and the planned-and-measured report pass (`test_report.py::test_breakeven_values`, `::test_report_shows_planned_and_measured`). A named reader has not yet confirmed the measured values appear next to the planned ones (no measured values exist). |
| REQ-32 | Partly met | `test_run_schedule.py::test_refuses_without_spike_record` and `::test_spike_sets_row_cap` pass. The 5-run luna timing spike (`bin/run-spike.sh timing --go`) needs models and was not run, so `config/values.json` has no `spike` record and `bin/run-schedule.sh` refuses to start on the real file. |
| REQ-29 | Partly met | The clock and the D1 median rules pass (`test_clock.py`, `test_analyze.py::test_d1_uses_medians`). `analysis/analyze.py all --stage N` (`d1.json`) has never run on real run folders. |
| REQ-33 | Partly met | `test_order.py::test_freeze_tag_before_gt_commit`, `::test_gt_before_tag_fails` and `::test_freeze_json_hashes_match_files` pass on temporary git repositories. The real order (`bin/check-order.sh freeze` when the hold-out ground truth is committed, pasted into `results/attestations.md`) is open: no freeze tag exists and none was created (K5). |
| REQ-34 | Partly met | The read-hook and brief tests pass (`test_ground_truth_not_read.py`, `test_render.py::test_briefs_hold_no_gt_markers`, copied `test_sandbox.py`). `bin/check-sandbox-gt.sh` was not run over real sandboxes before and after an arm (no arm was run); it was run only on invented trees. |
| REQ-35 | Partly met | `test_ablation.py` (nine tests) passes. `analysis/analyze.py ablate-report` over Stage 1 runs has no runs to read, and the model-stage ablation (8 arms x 4 documents x 3 runs = 96 panel runs, `DR-13`) was not run: owner decision. |
| REQ-36 | Partly met | `test_order.py::test_gt_hash_matches_prereg` and `::test_every_planted_plan_has_twin` pass on synthetic files. `config/attestation.md` (author, date, hash of the hold-out ground truth) does not exist. |
| REQ-04, REQ-07 | Partly met | The copied sandbox and lint tests pass. The real-sandbox check (REQ-04) and the real lint over the real ground truth (REQ-07, the `freeze` test `test_real_recipes_against_real_gt`) were not run. |
| REQ-38 | Partly met | `test_recipes_readme.py::test_readme_lists_rederive_rows` and the copied `test_readme.py` pass. The dated second-reader line at the foot of `recipes/README.md` does not exist. |
| REQ-40, REQ-45 | Partly met | `test_report.py::test_three_shares_separate`, `::test_no_summed_headline` and `::test_claim_template_text` pass. No real `results/report.md` exists for a person to read, so the headline and claim-wording records (`results/attestations.md`) are open. |
| REQ-41 | Partly met | `test_stages.py` and `test_prereg.py::test_act_bands_for_all_classes` pass. `config/prereg.json` with the owner's real bands does not exist (`DESIGN.md` 13.1 item 7). |
| REQ-43 | Partly met | `test_judge.py` passes on synthetic judge folders. `analysis/analyze.py audit-judges <stage>` on real judge output has not run; no judge was started. |
| REQ-44 | Partly met | `test_order.py::test_prereg_commit_before_first_run` passes. The real order record (`bin/check-order.sh prereg`, pasted into `results/attestations.md`) is open. |
| REQ-18 to REQ-24 | **Not built** | Redesign 1 (`MR` 6.3). `RL/TESTING.md` 3.8 names the nearest Recipe Ledger property for each: `test_render.py::test_byte_identical_same_inputs` and `test_lens.py::test_render_under_one_second` (REQ-18), the row caps of REQ-26 (REQ-19), the lens table of REQ-25 (REQ-20), the fallback brief equal to Z0 by hash (REQ-23). REQ-21 and REQ-22 have no Recipe Ledger counterpart, and REQ-24 is the timing spike on the largest tree (not run). |
| REQ-46 | Met, seam only | `test_verifier_off_path.py` (three tests) passes. The verifier itself is not built; the tests guard the launcher's seam (no verifier step in the clock, default off, time excluded). |

Also not met or open in this build:

- **The `freeze` tests: 3 collected, not run** (section 3), because they read the real ground truth or need a second author's records.
- **Copied tests that failed:** one, `tests/test_model_allowlist.py::test_nofallback_guard`, cause in section 3 (a test that assumes `NOFALLBACK` is not exported); the copy was not edited. With `-m "not freeze"` no other copied test fails.
- **Tier B files built locally and not reconciled with the sibling:** all twelve (section 2). Compare each with `bash bin/copy-shared.sh --diff <path>`.
- **The manual records still open**, as printed by `bash bin/open-manual-checks.sh` (`open: 12 of 12`): REQ-08, REQ-28, REQ-31, REQ-32, REQ-33, REQ-36, REQ-40, REQ-41, REQ-44, REQ-45, REQ-38, REQ-35.
- **Open owner decisions of `DESIGN.md` 13.1 (items 1 to 10).** None needs an answer before the build; items 5, 6 and 7 are needed at the freeze. The build followed the recommended value for the items that shaped code, and none of the ten has been confirmed by the owner:

| # | Decision | What the build did |
|---|---|---|
| 1 | Cost-driven lens row cap `floor((0.35 b - 6) / c)` instead of a fixed 12 (`DR-4`) | Built as recommended (`rl/lens.py`, `lens_row_cap`); unconfirmed. |
| 2 | One combined schedule for Z0, K and Z0-raw across both builds, or two (`DR-12`) | Not decided; `bin/make-schedule.py` writes this build's schedule only, and the two builds' Tier B launchers are not reconciled (section 2). |
| 3 | Re-ask only for ember, and no promotion from a repaired ledger (`DR-8`) | Built as recommended (`rl/reask.py`); unconfirmed. |
| 4 | Whether a documentation target may name a code file as its source so recipe C2 applies (`DR-7`) | Built as recommended (no): a documentation target has no source, so C2 is dropped; unconfirmed. |
| 5 | The K-arm lead-in `briefs/k-lead.txt` (a draft shared with the sibling) | Copied from the sibling as it is; not approved by the owner. |
| 6 | Whether to reword CB-2 for all arms | Left verbatim (the copied briefs); the `## Ledger` headings in Z0 and K are not measured. |
| 7 | The per-class act bands to pre-register | Not set: `config/prereg.json` does not exist. |
| 8 | The model-stage leave-one-class-out ablation (96 panel runs, `DR-13`) | Not run. |
| 9 | The 5 extra Z0 luna runs in the timing spike | Spike not run. |
| 10 | Concurrency: default 1 panel at a time, 3 panels only while the sibling's schedule is idle | Built as recommended (`bin/run-schedule.sh --max-panels`, default 1); unconfirmed. |

### 5.2 Requirements met (each with the test that shows it)

All names are `file::function` under `RL/tests/`; every one passed in the run of section 3 (the 3 `freeze` tests excluded). "(C)" marks a copied sibling test run unchanged.

| REQ | Shown by |
|---|---|
| REQ-01 | `test_render.py::test_cb1_present_with_source`, `::test_cb1_absent_without_source`, `::test_c2_recipe_dropped_without_source`, `::test_no_source_flags_in_run_json`; (C) `test_briefs.py` |
| REQ-02 | (C) `test_normalise.py`; `test_run_panel_fake.py::test_long_anchor_survives_h2_then_merge` |
| REQ-03 | (C) `test_sandbox.py` with `SW_SB_ROOT` under `/tmp` |
| REQ-05 | (C) `test_briefs.py`; `test_render.py::test_rl_brief_starts_with_z0_text`, `::test_fallback_brief_equals_z0_by_hash`, `::test_rl_part_order`, `::test_row_cap_placeholder_equals_mr_at_14`; `test_judge.py::test_judge_brief_sha_equals_jj` |
| REQ-06 | (C) `test_cards.py`; `test_recipes.py::test_recipe_keys_equal_card_ids`, `::test_each_recipe_at_most_120_words`, `::test_budget_sentence_once_and_parsed`, `::test_recipes_equal_mr_quotes` |
| REQ-09 | `test_render.py::test_no_src_path_in_any_brief`; `test_recipes.py::test_no_src_path_in_recipe_files` |
| REQ-10 | `test_lens.py::test_fixture_class_c9_needs_no_code_change` |
| REQ-11 | (C) `test_fnd_contract.py::test_merge_accepts_class_probe_src_keys`, `::test_existing_review_suite_passes` |
| REQ-12 | `test_fallback.py::test_forced_exception_in_lens_render_runs_z0_briefs`, `::test_invalid_lens_table_falls_back`, `::test_fallback_decided_before_first_reviewer_starts`; `test_run_panel_fake.py::test_forced_exception_in_check_merges_as_written` |
| REQ-13 | `test_rowcheck.py::test_misplaced_duplicated_truncated_blocks`, `::test_fence_opener_grep_is_not_used`, `::test_heading_between_ledger_and_findings_is_missing` |
| REQ-14 | `test_rowcheck.py::test_quote_wrapping_a_plan_line_matches`, `::test_quote_plan_not_in_candidate_fails` |
| REQ-15 | `test_rowcheck.py::test_promotion_copies_problem_and_anchor`, `::test_promotion_validates_with_check_finding`, `::test_promotion_inside_single_block`, `::test_promotion_failure_logged_and_skipped`, `::test_promotion_requires_quote_plan_ok`, `::test_no_promotion_for_over_budget_unknown_or_reask_rows`, `::test_class_key_added_from_row_prefix` |
| REQ-16 | `test_rowcheck.py::test_unsupported_row_demotes_linked_finding`, `::test_unsure_never_blocks`, `::test_blocking_needs_cb3_and_two_quotes_or_search`, `::test_unlinked_finding_untouched`, `::test_quote_other_corpora`, `::test_check_scope_all_switch_off_by_default`, `::test_format_induced_demotions_counted` |
| REQ-25 | `test_lens.py::test_generated_briefs_match_lens_table`, `::test_duplicated_classes_equal_req25`, `::test_search_form_only_in_search_role`; `test_recipes.py::test_recipe_text_only_in_one_file` |
| REQ-26 | `test_rowcheck.py::test_row_budget_per_recipe`, `::test_lens_cap_enforced`, `::test_none_found_allowed_and_covers_recipe`, `::test_none_found_with_rows_flagged`, `::test_recipe_missing_flagged`; `test_lens.py::test_row_cap_per_panel`, `::test_row_cap_formula_table`, `::test_no_budget_refuses` |
| REQ-27 | `test_reask.py::test_condition_with_fake_clock`, `::test_boundary_is_inclusive`, `::test_never_for_luna_even_with_large_b`, `::test_only_when_ledger_missing`, `::test_only_once`, `::test_haiku_and_sonnet_never`; `test_run_panel_fake.py::test_ember_reask_runs_once_and_is_accepted`, `::test_reask_rejected_when_findings_differ`, `::test_no_reask_when_clock_too_late`, `::test_luna_ledger_missing_is_not_reasked`, `::test_reask_failure_keeps_original_report`, `::test_reask_not_counted_as_retry` |
| REQ-30 | `test_hang_guard.py::test_formula_per_panel`; `test_run_panel_fake.py::test_sleeping_reviewer_killed`, `::test_no_retry_on_failure`, `::test_killed_reviewer_absent_from_merge`; `test_analyze.py::test_kills_retries_per_arm`, `::test_zero_findings_for_killed`, `::test_reask_counted_apart_from_retries` |
| REQ-37 | `test_targets.py::test_spec_and_doc_fixtures_exist`, `::test_lens_renders_for_spec_fixture`, `::test_lens_renders_for_doc_fixture` |
| REQ-39 | `test_analyze.py::test_metrics_match_expected_json`, `::test_one_definition_of_found_fraction` |
| REQ-42 | `test_analyze.py::test_nonprobe_findings_per_run`, `::test_d6_failure_blocks_adoption`, `::test_promoted_lines_not_counted_as_reviewer_findings` |

The automated halves of the partly met requirements above are shown by: REQ-04 (C) `test_sandbox.py`; REQ-07 (C) `test_lint.py` and `test_lint_rl.py::test_seeded_phrase_in_recipe_fails`, `::test_seeded_name_in_lenses_fails`, `::test_rl_files_clean_on_synthetic_gt`; REQ-17 `test_analyze.py::test_compliance_report_on_fixture`; REQ-28 `test_ran_check.py::test_verified_unverified_and_not_a_tool_claim`, `::test_search_recipe_without_bash_is_unverified`, `::test_none_found_for_search_recipe_without_call_is_unverified`, `::test_report_per_class_and_reviewer`; REQ-29 `test_clock.py::test_panel_elapsed_rl_and_other_arms`, `::test_clock_starts_before_lens_render`, `::test_reask_seconds_inside_the_clock`, `test_analyze.py::test_d1_uses_medians`, `::test_d1_same_block_only`, `::test_mean_and_median_reported`; REQ-31 `test_report.py::test_breakeven_values`, `::test_report_shows_planned_and_measured`; REQ-32 `test_run_schedule.py::test_refuses_without_spike_record`, `::test_spike_sets_row_cap`; REQ-33 and REQ-44 `test_order.py` (names above); REQ-34 `test_ground_truth_not_read.py::test_lens_brief_and_check_never_open_the_trap`, `test_render.py::test_briefs_hold_no_gt_markers`; REQ-35 `test_ablation.py::test_removing_one_recipe_leaves_every_other_part_byte_identical`; REQ-36 `test_order.py::test_gt_hash_matches_prereg`, `::test_every_planted_plan_has_twin`; REQ-38 `test_recipes_readme.py::test_readme_lists_rederive_rows`, (C) `test_readme.py`; REQ-40 `test_report.py::test_three_shares_separate`, `::test_no_summed_headline`; REQ-41 `test_stages.py::test_stage_rows_schema`, `::test_selection_covers_rule`, `::test_stage_values_on_fixture`, `test_prereg.py::test_act_bands_for_all_classes`; REQ-43 `test_judge.py` (`::test_judge_brief_sha_equals_jj`, `::test_model_is_opus_only_in_judge`, `::test_audit_flags_error_with_score_file`, `::test_second_judge_sample_15_percent_seeded`, `::test_audit_counts_match_merged_rows`, `::test_merged_report_has_no_arm_marker`); REQ-45 `test_report.py::test_claim_template_text`; REQ-46 `test_verifier_off_path.py::test_no_verifier_step_in_clock`, `::test_verifier_default_off`, `::test_verifier_time_excluded`.

## 6. What this build does not show

- **No panel reviewer, judge or network call was made by this build.** Every test and rehearsal ran against the fake `claude` at `tests/fakes/claude`, first on `PATH`; the judge and spike scripts that name a model refuse without the explicit arguments (`NOFALLBACK=1`, `--go`), and the only tests that pass `--go` are refusal cases (`NOFALLBACK` unset in `tests/test_judge.py`, an invalid mode in `tests/test_run_schedule.py`), so no judge or spike was started. The call logs of the rehearsals show only fake calls (three `review` lines each). Separately, the executor of this plan used independent QA sub-sessions on `claude-sonnet-5-5` to check each task against its acceptance criteria; they are not panel reviewers or judges and they ran outside the product code.
- **No ground-truth file was opened by the product code or its tests.** Every test that needs ground truth reads the invented files `fixtures/gt/lint-gt.json` and `fixtures/gt/synthetic-gt.json`. `find` over `RL` and over the rehearsal sandbox for a file named `ground*truth*` finds nothing; `bin/check-sandbox-gt.sh` prints nothing on the sandboxes and run folders present; no score file or judge output exists under `RL`. The only code that reads a real ground truth is `bin/judge-one.sh` (scoring), which this build never ran.
- **Recipe Ledger working is not shown by this build.** The tests show that the recipes are rendered into the briefs as designed, that the ledger is parsed and checked as designed, that a missing ember ledger is asked for again at most once and only inside the clock, that a failed lens render or row check falls back to the plain panel, and that the analysis computes the designed metrics on invented runs. They do not show that any real reviewer writes a usable ledger, that the recipes find more defects, that the time stays within +35% of Z0, or that no displacement of the reviewers' own findings occurs. Those are decided only by the timing and compliance spikes and by Stage 1 and Stage 2 of the experiment (`RL/TESTING.md` section 5), whose power is low (`MR` 5.9): a pass there would be evidence, not proof.
- **Next, in order** (`IMPLEMENTATION.md` steps 10 to 13, none done): the owner's go-ahead for the two spikes (`bin/run-spike.sh compliance --go`, then `timing --go`); the second-author review of the recipes (`recipes/REVIEWS.md`); the owner's real act bands (`config/prereg.json`); then the freeze (`bin/freeze.sh`, a person creates the tag), the hold-out ground truth and Stage 1.
