# Implementation order: Redesign 1, Sweep Sheet

Status: design only. Nothing here was built or run. `DESIGN.md` says what to build, `TESTING.md` says how each requirement is tested. This file gives the order, the files per step, the test command per step and what to run first. Line counts are rough planning values from `MR` 3.1(h) (unmeasured).

Path names as in `DESIGN.md`. Shell variables used in every command:

```
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1
```

## 0. How to execute this

Three rules decide how the work is run.

1. It has far more than five edits and many files, so it goes through a written plan, then an executor: `/sc:workflow "Implement SW/DESIGN.md steps 0 to 13, writing only under SW; tests per SW/TESTING.md" --depth standard --handoff none`, then `/sc:implement <the printed plan path>` once the plan is read (level 3 of the routing guide). Steps 14 to 16 are not part of that plan: they need a second author, the owner's decisions and models.
2. Every file is written under `SW`. The plan must state that `src/`, `tests/`, `.claude/` and `.dev/tasks/` are not touched (K1). Nothing is staged, committed or pushed by the build; staging `.dev/tasks/` stays with the session that runs `/sc:implement`, as the repository rules say.
3. No step starts a model. Steps 0 to 13 need none.

## 1. What to run first

Run these three before any code is written. Each answers a question that could change the design, costs minutes, and needs no model. Write the three results in `SW/results/step0.md`.

| Order | Command | Question it answers | Decision rule |
|---|---|---|---|
| 1 | `uv run --frozen --project $REPO pytest -p no:cacheprovider $REPO/tests/review -q` | Is the code this design imports healthy today? (`findings.py`, `ledger.py`, `merge_cmd.py`) | must pass; if not, stop and fix that first, outside this design |
| 2 | the search-cost spike of step 0.3 below | Can S1 really finish in about 8 s on a full-size tree? It is the largest unmeasured number in the time budget | S1 search part at or under 4 s: go on. Over 4 s: narrow the DD-5 scope or the pattern count before step 7, and re-do the time table in `DESIGN.md` 12 |
| 3 | the merge-keys probe of step 0.2 below | Does the real merge accept `class`, `probe` and `src` on findings lines? (REQ-11, unverified in `MR`) | accepted: go on. Rejected: telemetry moves to a side file keyed by finding id and `DESIGN.md` 9.3 is changed |

## 2. Steps

Each step lists what to create, how to test it, and what "done" means. Test names refer to `TESTING.md`. A step is done only when its test command exits 0.

### Step 0. Preflight (no code in `SW` except the results note)

| Sub-step | What | Where the scratch goes |
|---|---|---|
| 0.1 | the baseline command of section 1, row 1 | none |
| 0.2 | a 20-line scratch script that builds one report whose findings line carries `"class"`, `"probe"` and `"src"`, runs `superclaude.cli.review.merge_cmd.command` through click's `CliRunner` with `--ledger /tmp/x/ledger.json --doc <fixture> --round 1 --report r1=<report> --out /tmp/x/merged.md`, and prints the exit code and whether the merged text contains the keys | `/tmp/sweep-step0/merge_keys.py`, run with `$PYRUN` |
| 0.3 | a scratch script that builds the DD-5 scope of `REPO` at HEAD (tracked files under `tests/`, `scripts/`, `docs/`, root files, change-log style files, minus `.dev/` and dependency folders), writes 40 fixed strings to a pattern file, and times `git -C $REPO grep -n -I -F --no-color -f <file> -- <pathspecs>` three times with `LC_ALL=C` | `/tmp/sweep-step0/search_cost.py` |
| 0.4 | with `jq`, list the event types and the `tool_result` shape of one finished run of each reviewer model already on disk under `EVAL/<doc>/reviews/combos/` (luna, haiku, sonnet, ember; pick any one `*.attempt1.json` each; do not open any ground-truth or score file) | none |
| 0.5 | time `uv run --frozen --project $REPO python -c "import superclaude.cli.review.findings"` five times (one run measured 0.28 s); not run before the build: the plan runs it in step 11 (the clock helper) and writes `SW/results/import-time.md` | none |
| 0.6 | read `EVAL/tools/tmp-scripts/anon-b11.sh` and `BR/enrichment/investigation-generality.md` sections 2 and 5; note the redaction rules and the instance citations for the cards | none |

Done when `SW/results/step0.md` holds the three numbers and the decision taken for each.

### Step 1. Skeleton and test scaffolding (about 120 lines)

| Create | Purpose |
|---|---|
| `SW/ruff.toml` | `extend = "../../../../pyproject.toml"` (four levels up from `SW` to `REPO`), same idea as the precedent's `ruff.toml` |
| `SW/scaffold/__init__.py`, `SW/sweep/__init__.py`, `SW/analysis/__init__.py` | packages (no `lib/` folder anywhere: `.gitignore` line 13) |
| `SW/tests/conftest.py` | puts `SW` on `sys.path` (as the precedent's `conftest.py` does), provides `tmp_roots`, a `PATH` that starts with `tests/fakes`, and the override guard |
| `SW/tests/fakes/claude` | the fake `claude` of TESTING F-FAKE |
| `SW/bin/common.sh` | `sw_assert_writable`, `sw_assert_model`, `sw_assert_nofallback`, path variables, `sw_py` (`uv run --frozen --project $REPO python`) |
| `SW/config/packages.json`, `panels.json`, `values.json` | the three study documents and the three panels with caps (8/8/8, 6/9/9, 6/9/9); planning values for `b`, `c`, `kill_s` |

Tests: `test_paths.py`, `test_model_allowlist.py`, `test_fake_on_path.py`, `test_layout.py`. Command: `$T $SW/tests -q`. Done when they pass.

### Step 2. Findings adapter and H2 (about 90 lines)

Create `scaffold/fnd.py` (imports `parse_block`, `flat`, `locate`, `_check_finding`, `_blocks_after`, and a `lenient_lines(report)` helper that returns the raw JSON lines of the findings block even when some lines are invalid) and `scaffold/normalise.py` (H2: cut anchor and anchor2 to 200 flattened characters, claim to 300, validate with `parse_block`, write `h2.json` with `unrepaired` lines, idempotent).

Tests: `test_fnd_contract.py` (signature pins; REQ-11 `test_merge_accepts_class_probe_src_keys`; the existing review suite), `test_normalise.py` (REQ-02). Command: `$T $SW/tests/test_fnd_contract.py $SW/tests/test_normalise.py -q`.

### Step 3. Class cards, schema, lint, README (about 200 lines of code, 8 JSON files)

Create `cards/schema.json`, `cards/C1.json` to `cards/C8.json`, `scaffold/cards.py` (load, validate, expose `questions`, `routes`, `promote_category`, `definition`), `scaffold/lint.py` (AO-1: 4-word sequences from ground-truth `description` and `plan_quote`; forbidden-name set; prints file, line and a hash only), `cards/README.md` (REQ-38 re-derive table, plan done, specification and documentation drafted).

Card contents: `id`, `name`, `version`, `definition` (from `MR` section 2, target-neutral), `question_template` (the eight questions of `MR` 3.1(a), verbatim), `extractor`, `route` (C1 read, C2 read, C3 read, C4 search, C5 search, C6 search, C7 read, C8 search), `replicas` (2), `applies_to`, `instances` (at least 2 citations each, from the register read in step 0.6), `severity_guidance`, `known_weakness`, `promote_category` (DD-11), and a `swap_test` record (reviewer, date) filled by the second author (M).

Tests: `test_cards.py`, `test_lint.py` (the real-ground-truth test is marker `freeze`), `test_readme.py`. Command: `$T $SW/tests/test_cards.py $SW/tests/test_lint.py $SW/tests/test_readme.py -q -m "not freeze"`.

### Step 4. Briefs (about 80 lines plus the text files)

Create `briefs/base.txt` (copy `RR` lines 13-17 with `$CAND_SB` and `$SHA` as placeholders), `cb1.txt` to `cb5.txt`, `ledger-rule.txt`, `sheet-block.txt` (copied from the quoted blocks of `MR` by a one-time script that prints the diff against the extraction used by the test), `k-lead.txt` (draft, owner approves), and `scaffold/briefs.py` (`render(arm, doc, items, source)`, part order of `DESIGN.md` 8.1, sha256 of every part and of every rendered brief).

Tests: `test_briefs.py` (REQ-01, REQ-05, REQ-09, REQ-23 hash). Command: `$T $SW/tests/test_briefs.py -q`.

### Step 5. Sandbox (about 70 lines of bash)

Create `bin/build-sandbox.sh` by adapting `20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh` lines 1-59 (read it again; copy, do not import: that line of work is closed): `git archive <base>`, the H4 removals of `DESIGN.md` 11.2 plus every `artifacts/` folder, every `progress.md` and every path that holds a document id, `tree:<dir>` bases, `--raw` mode, the post-build `grep`, `sandbox.json` with the tree hash, and the `SW_SRC_REPO` override guarded to `/tmp`. Create `fixtures/repos/build_repo.py`.

Tests: `test_sandbox.py` (REQ-03, REQ-04, REQ-34 sandbox part), `test_sandbox_clean.py` (K4 part waits for step 11). Command: `$T $SW/tests/test_sandbox.py -q`.

### Step 6. Plan reader and its fixtures (about 220 lines)

Create `sweep/plan.py`, `sweep/formats.py` (dictionaries for `plan`, `spec`, `doc`), `sweep/words.py` (set words, limiter words, edit verbs, dictation verbs, ordering verbs, stop list: written here, then linted), and the fixtures `fixtures/plans/p_basic.md`, `p_clean.md`, `gen_setwords.py`, `fixtures/specs/spec1.md`, `parent1.md`, `fixtures/docs/doc1.md`. All content is invented; run the fixture lint (`test_lint.py::test_fixtures_clean`) when each file is added.

Tests: `test_plan.py` (each block kind recognised in each format; unknown structure yields zero blocks and no exception; line numbers right; an anchor cut from the candidate is found by `locate`), `test_formats.py::test_new_format_is_data_only`. Command: `$T $SW/tests/test_plan.py $SW/tests/test_formats.py -q`.

### Step 7. Extractors and the search helper (about 450-600 lines)

Order matters: the mechanical, highest-value extractors first, so a stop after any sub-step leaves a working tool.

| Sub-step | Create or extend | Tests |
|---|---|---|
| 7.1 | `sweep/extractors.py`: `Candidate`, `Ctx`, the registry, `search()` (batched `git grep -F -f`, the scope of DD-5, caps of 3 hits per file and 5,000 lines) | `test_scope.py` (REQ-24), `test_extractors_common.py` (DD-10) |
| 7.2 | E2 (class C4) | `test_e2.py` |
| 7.3 | E3 (class C8) | `test_e3.py` |
| 7.4 | E4 (class C5) | `test_e4.py` |
| 7.5 | E1 (classes C1 and C6) | `test_e1.py` |
| 7.6 | E5 (class C2, needs a source) | `test_e5.py` (REQ-01 part) |
| 7.7 | E7 (class C7) | `test_e7.py` |
| 7.8 | E6 (class C3, experimental) | `test_e6.py` |

Each extractor test has a positive case, a negative case, a near-miss case and a determinism case on `p_basic.md` and `p_clean.md`. Command: `$T $SW/tests/test_scope.py $SW/tests/test_extractors_common.py $SW/tests/test_e[1-7].py -q`.

### Step 8. Rank, selection, assignment (about 150 lines)

Create `sweep/rank.py` (the weight table of `DESIGN.md` 5.2 as one dict, with its sha256), `sweep/select.py` (top-K with K = 8, or 12 when only one class has candidates; passes A, B, C, fair-share ceiling, class order, ties by the seed hash, `candidates.json` rows), `sweep/assign.py` (the two passes of 7.2, caps, the haiku restriction, replica drops, per-reviewer shuffle).

Tests: `test_select.py` (REQ-19), `test_assign.py` (REQ-20). Command: `$T $SW/tests/test_select.py $SW/tests/test_assign.py -q`.

### Step 9. Render and the pre-pass command (about 150 lines)

Create `sweep/render.py` (item JSON, sheet text, the 16,000-character cap, class label only), `sweep/prepass.py` (parse, find, top-K, attach, select, assign, render; writes to `prepass.tmp/`, renames to `prepass/` on success; no clock; sorted lists; no absolute paths), `sweep/cli.py` with subcommands `prepass`, `check`, `lint`, `brief` and `normalise` (only `prepass` is wired now), and `bin/time-prepass.sh`.

Tests: `test_render.py` (DD-6), `test_prepass.py` (REQ-18 determinism), `test_prepass_inputs.py` (K3, REQ-34), `test_kill_fallback.py` (REQ-18 kill, REQ-12a: the forced exception part waits for step 11), `test_prepass_timing.py` (marker `slow`, REQ-24). Command: `$T $SW/tests/test_render.py $SW/tests/test_prepass.py $SW/tests/test_prepass_inputs.py -q`, then `$T $SW/tests -q -m slow`.

Checkpoint: run `bin/time-prepass.sh` on `REPO` and on two smaller snapshots, and write the seconds into `config/values.json`. If S1 on `REPO` is over 10 s, stop and revisit DD-5 and DD-10 before going on.

### Step 10. Ledger parser, checks, promotion (about 300 lines)

Create `scaffold/ledgerv1.py` (section 9.1 reader, the four checks, linking, demotion causes, CB-3 detection, promotion with `_check_finding`, `check.json`), `scaffold/telemetry.py` (`class`, `probe`, `src`, per-class tables), and the `check` subcommand of `sweep/cli.py` (raw report in, `check/<rid>.checked.md` out; any exception caught by the caller sets `check_skipped`). Create the F-REPORT and F-TRANSCRIPT fixtures.

Tests: `test_ledgerv1.py` (REQ-13 to REQ-16, DD-2, DD-3, DD-12), `test_check_flow.py`. Command: `$T $SW/tests/test_ledgerv1.py $SW/tests/test_check_flow.py -q`.

### Step 11. Launcher and fake-claude integration (about 200 lines of bash, 120 of Python)

Create `bin/run-reviewer.sh` (the changes against `RR` in `DESIGN.md` 11.1), `bin/run-panel.sh` (arms Z0-raw, Z0, K, SS; S0 check, S1 under `timeout`, brief render, three reviewers in parallel with the hang guard, S5 with the `check_skipped` catch, H2, the merge, `run.json`, `timing.json`, the clock of 11.4, the sandbox-clean check), `config/values.json` additions (`b`, overhead, `hang_s` inputs), and a helper `scaffold/clock.py` for the arithmetic that the tests call (`kill_s`, `hang_s`, `breakeven`). Before the helper, run step 0.5 (time the `findings` import five times; `SW/results/import-time.md`).

Tests: `test_run_panel_fake.py` (REQ-12, REQ-23 whole run, REQ-30, DD-8, DD-9), `test_clock.py` (REQ-29), `test_hang_guard.py` (REQ-30 formulas), `test_sandbox_clean.py` (K4), `test_kill_fallback.py` (REQ-12a complete). Command: `$T $SW/tests/test_run_panel_fake.py $SW/tests/test_clock.py $SW/tests/test_hang_guard.py $SW/tests/test_sandbox_clean.py $SW/tests/test_kill_fallback.py -q`.

### Step 12. Judge copy, analysis, offline gate (about 350 lines)

Create `bin/judge-one.sh` (a copy of `JJ` with paths as variables; the brief text byte-identical), `bin/anon.sh` (from the rules noted in step 0.6), `bin/judge-batch.sh`, `analysis/analyze.py` (sub-commands `all`, `audit-judges`, `compliance`, `prereg`, `sample-second-judge`; every metric of `DESIGN.md` 14.3; Wilson intervals; the bootstrap that resamples documents first; gates D1 to D7; the three shares; the REQ-45 claim sentence), `analysis/g0.py` (14.1: recalls, random baselines, floor, `--ablate`). Create the fixtures F-GT and F-RUNS.

Tests: `test_analyze.py`, `test_report.py`, `test_stages.py`, `test_prereg.py`, `test_judge.py`, `test_g0.py`, `test_verifier_off_path.py`. Command: `$T $SW/tests/test_analyze.py $SW/tests/test_report.py $SW/tests/test_stages.py $SW/tests/test_prereg.py $SW/tests/test_judge.py $SW/tests/test_g0.py $SW/tests/test_verifier_off_path.py -q`.

### Step 13. Schedule, spikes, freeze and order scripts (about 200 lines)

Create `bin/make-schedule.py` (block-randomised, recorded seed, the stage and set options of `TESTING.md` section 5, 75 lines for Stage 1 as designed), `bin/run-schedule.sh` (at most 3 panels at once; refuses without the spike record), `bin/run-spike.sh` (timing and compliance), `bin/freeze.sh` (hashes, prints the tag command, never tags), `bin/check-order.sh` (`freeze` and `prereg`), `bin/check-sandbox-gt.sh`, `bin/open-manual-checks.sh`.

Tests: `test_run_schedule.py` (REQ-32), `test_freeze.py` (K5), `test_order.py` (REQ-33, REQ-36, REQ-44). Command: `$T $SW/tests/test_run_schedule.py $SW/tests/test_freeze.py $SW/tests/test_order.py -q`.

Checkpoint for steps 1 to 13: `$T $SW/tests -q -m "not slow and not freeze"`, `ruff check` and `ruff format --check`, and the baseline of step 0.1. All must exit 0. This is the point at which the build is "done" in the sense of `TESTING.md` section 6.

## 3. Steps that are not part of the build plan

### Step 14. Freeze (people and decisions; no model)

| Order | Action | Who |
|---|---|---|
| 14.1 | author `fixtures/recall/` (3 or more real non-study, non-hold-out plans with seeded defects) and `AUTHORS.md` | a second author, who has not read the extractors |
| 14.2 | fill the `swap_test` records of the eight cards | a second author |
| 14.3 | decide the open items of `DESIGN.md` 15.1 (G0 floor 0.45 recommended; the act bands; CB-2; the K lead-in) and write `config/owner-values.json` | the owner |
| 14.4 | run `$T $SW/tests -q -m freeze`; B1 and B3 of `TESTING.md` section 5 | the maintainer |
| 14.5 | `bash $SW/bin/freeze.sh`, review its output, run the printed `git tag` command | a person (K5) |
| 14.6 | the hold-out author writes `holdout-gt/` and commits it; then B6 to B9 of `TESTING.md` section 5 | the hold-out author, then the maintainer |

### Step 15. Run the experiment (models; owner go-ahead for each part)

Spikes (C), Stage 1 (D), Stage 2 for arms that pass (E), derivation-set check (F), decision (G): the commands are in `TESTING.md` section 5. The experiment is not part of this design's build.

### Step 16. Adoption (only if the pre-registered gates pass)

Adoption is its own plan. It moves the pre-pass, the scaffold and the briefs into `src/superclaude/cli/review/` (a `sweep` subpackage and a `superclaude review sweep` command), applies CB-1 to CB-5 to `src/superclaude/rules/prompts/document_review_loop_prompts.md` (DD-1), runs `make sync-dev` and `make verify-sync`, adds tests under `tests/review/`, and updates the installed-path rules (no `src/superclaude/` path inside an installed primitive). It needs its own `/sc:workflow` plan and its own review, and it is not specified further here.

## 4. Dependencies between steps

```
0 -> 1 -> 2 -> 10 -> 11 -> 13 -> 14 -> 15 -> 16
          1 -> 3 -> 4 ------^
          1 -> 5 -------------^
          1 -> 6 -> 7 -> 8 -> 9 -> 11
                    2 -> 12 -> 13
```

Steps 3, 4, 5 and 6 can run in parallel after step 1. Step 7 sub-steps run in the order given. Step 11 needs 4, 5, 9 and 10. Step 12 needs 2 and 10.

## 5. Risks to watch while building

| Risk | Where it shows | Response |
|---|---|---|
| The search is slower than 4 s on the full tree | step 0.3, step 9 checkpoint | narrow the scope (DD-5) or the pattern count; the time table of `DESIGN.md` 12 is redone |
| The real merge rejects the telemetry keys | step 0.2 | side file keyed by finding id |
| A model does not copy quotes exactly, so rows are demoted for format only | the compliance spike (TESTING C2) | report `format_induced_demotions`; widen the corpora only with the owner's approval |
| The plan format differs from `workflow-plan/1.2` in a hold-out document | step 6 fixtures; recall fixtures at step 14 | add a dictionary to `formats.py`, re-freeze |
| The hold-out ground truth has no `plan_quote` | G0 | the hold-out author adds it; without it G0 cannot run |
| Anything wants to write outside `SW` | `sw_assert_writable` | stop; it is a defect in the step, not a reason to relax K1 |
