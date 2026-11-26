# Design: Redesign 2, Recipe Ledger (written class recipes and a forced enumerate-then-judge ledger, no pre-pass), implementation and test specification

Grounding: index_state: fresh (`codegraph_status` answered "Changes since index: 0 added, 0 modified, 0 removed" and listed two pending files of the sibling build; checked_at 2026-11-14T22:50:00Z; worktree_root and projectPath `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel`). Only `codegraph_status` was called: this design touches no existing symbol, so no lookup tool was needed. Every file and line cited below was read with Read or a read-only shell command in this session.

Status: design only. Nothing in this document is built, run or measured. No reviewer or judge session was started and no ground-truth file was opened. Every number marked "planning" comes from `MR` and is replaced by a measured value before it is used in a decision (`MR` section 5).

**Path abbreviations.**

| Name | Absolute path |
|---|---|
| `REPO` | `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel` |
| `EVAL` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only) |
| `RL` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger` (this folder: the only place code, fixtures and run output are written) |
| `SW` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet` (the sibling build, Redesign 1; read only, never written) |
| `MR` | `REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (source of truth; "3.2" below means its section 3.2) |
| `RR` | `EVAL/tools/run-reviewer.sh` (87 lines) |
| `JJ` | `EVAL/tools/tmp-scripts/judge-one.sh` (31 lines) |
| `SPEC` | `EVAL/combos/SPEC.md` (procedure and hard limits of the study) |
| `CR` | `EVAL/COMBO-REPORT.md` |
| `FND` | `REPO/src/superclaude/cli/review/findings.py` (findings-v1 parser) |
| `LED` | `REPO/src/superclaude/cli/review/ledger.py` (the merge's finding ledger; not the `ledger-v1` block of this design) |
| `MRG` | `REPO/src/superclaude/cli/review/merge_cmd.py` |
| `SBR` | `/tmp/evalsb-recipe` (sandbox root of this build; the sibling uses `/tmp/evalsb-sweep`, so the two builds never share a sandbox) |
| `SWD` | `SW/DESIGN.md` (the sibling's design; "SWD 9.3" means its section 9.3) |

**Sources read for this design.**
- `MR`: sections 1, 2, 3.0 (3.0.1 to 3.0.10), 3.2 (all of (a) to (i)), 4, 5 (5.1 to 5.9), 6.1, 6.2, 6.4 to 6.8 and "Not checked and unverified". Section 3.1 was read only where 3.2 refers to it (time arithmetic, guard rows).
- Harness: `RR` lines 1-87, `JJ` lines 1-31, `SPEC` lines 1-152, `CR` lines 289-378 (the final-results section: baseline numbers, the 200/300 merge drops, the 156 source skips, luna's 91.4% anchor fidelity).
- Code: `FND` lines 1-60, 84-196 (`_check_finding`, `parse_block`) and 266-304 (`flat`, `locate`); `MRG` lines 1-118.
- Sibling: `SWD` lines 1-824 in full; `SW/IMPLEMENTATION.md` in full; `SW/TESTING.md` sections 1 to 5; `SW/cards/` (README, schema, C1 and C4 in full, the other six cards' `definition`, `route` and `promote_category`), `SW/briefs/` (all nine parts), `SW/bin/common.sh` in full, `SW/bin/build-sandbox.sh` lines 1-60, `SW/scaffold/{briefs,cards,fnd,normalise}.py` and the head of `lint.py` (lines 1-203), `SW/tests/{conftest,helpers}.py`, `SW/tests/fakes/claude` lines 1-80, `SW/config/*.json`, and one plan fixture's first 1,500 characters (`SW/fixtures/plans/p_basic.md`, an invented plan).
- One finished reviewer transcript (`EVAL/<package>/reviews/combos/b4-muse-ember-luna2/t2b-1.attempt1.json`), read through `jq` for event types and key names only, to settle how the `ran` cross-check (REQ-28) can read tool calls (section 7.7).

**Contamination statement.** Two things were read that sit close to the study answers. (1) `CR` lines 289-378 mention ground-truth item ids (GT1, GT3 and so on) and counts per panel, and `MR` section 1 labels the ten missed issues B1-B8 and I1-I7. (2) `SW/config/packages.json` names the three study packages and the files their implementations changed. Nothing from these is used in a recipe, card, lens, brief, regex, fixture or example in this design. Every example below is invented. No `ground-truth*.json` was opened, and the plan text of no study package was read. Section 11.1 turns this into a mechanical check (AO-1 lint over `recipes/`, `config/`, `briefs/`, `cards/` and `fixtures/`).

**How to read.** Section 1 lists where `MR` is silent or pulls two ways and what this design decided. Section 2 gives the run order. Section 3 says which pieces are copied from the sibling and how. Sections 4 to 7 are the parts specific to Recipe Ledger: recipes, lens table, brief change, ledger checks. Section 8 is failure and fallback, 9 the harness, 10 the time budget with numbers, 11 generality, 12 the hooks for the experiment, 13 the open decisions and the unverified list. `TESTING.md` maps every requirement to a test. `IMPLEMENTATION.md` gives the build order.

## 1. Scope, constraints and decisions taken

### 1.1 What is built

Recipe Ledger answers the seed's open question from the instruction side: no script finds the places to check; each reviewer gets a lens of two to four written class recipes, runs them step by step and writes one ledger row per step; the model runs the sweep and the model judges (`MR` 3.2). The parts specific to it:

1. **Recipes file** (`recipes/recipes.json`): the eight class recipes of `MR` 3.2(a), the search-form line and the per-recipe row budgets, as data in one file (REQ-25, REQ-06).
2. **Lens table** (`config/lenses.json`) and the **lens render** (`rl/lens.py`, `rl/render.py`): per panel, per reviewer, which recipes, in which order, under which row cap; the rendered brief for one reviewer.
3. **Row check** (`rl/rowcheck.py`): the post-run check of `MR` 3.2(a) R3, built on the shared ledger rules of `MR` 3.0.4 and 3.0.5. It adds the row-id grammar, recipe coverage, the row budgets and the `NONE FOUND` rule.
4. **Ember re-ask** (`rl/reask.py`): the one repair call `MR` allows, with its clock condition (REQ-27).
5. **Launcher arm RL** (`bin/run-panel.sh`): arms Z0-raw, Z0, K and RL on the same sandbox, judge and clock, with the fallback decision taken before any reviewer starts.
6. **Analysis additions**: the `ran` cross-check (REQ-28), per-recipe stage rows, and the gate bookkeeping for RL (`analysis/`).

Everything that `MR` 3.0 calls shared scaffolding (class cards, briefs with CB-1 to CB-5, the ledger carrier `ledger-v1`, the H2 normaliser, the sandbox, the Z0 and K arms) is copied from the sibling build when it exists (section 3), never invented twice.

Not built here: Redesign 1 (pre-pass, extractors, sheet, assignment, REQ-18 to REQ-24), the optional verifier of 3.0.9 (only the seam test of REQ-46), any production change under `src/`.

### 1.2 Hard constraints (from the task, `SPEC` and `SWD` 1.2)

K1 to K7 are those of `SWD` 1.2 and are enforced by the copied `bin/common.sh` and tests. K8 and K9 are new here.

| Id | Constraint | Enforced by |
|---|---|---|
| K1 | Code, fixtures and run output live under `RL`. Sandboxes live under `SBR`. Nothing is written under `src/`, `tests/`, `.claude/` or `.dev/tasks/`. | `bin/common.sh: sw_assert_writable` (copied; `SW` inside that file resolves to its own folder, which is `RL` after the copy); `test_paths.py` (copied) |
| K2 | Reviewer models: `muse-ember-1.0`, `gpt-6-luna`, `claude-haiku-5-5`, `claude-sonnet-5-5`. The judge is `claude-opus-5-5` and only the judge. Never Fable, Tier 0, Qwen or glm. | `sw_assert_model`; `test_model_allowlist.py` (copied) |
| K3 | The recipes read nothing themselves. No script of this design reads a ground-truth file or a review output except the analysis and judge scripts, after the freeze (AO-6). | `test_ground_truth_not_read.py`: a read hook on `open` while the lens render, brief render and row check run on fixtures that contain a trap file named like a ground-truth file |
| K4 | Reviewers are read-only (`--disallowedTools Edit Write NotebookEdit`, as `RR` line 48). Bash stays open, so the harness checks the sandbox with `git status --porcelain` before and after every run. | `bin/run-panel.sh`; `test_sandbox_clean.py` |
| K5 | No git write by this design's tools. The freeze tag (REQ-33) is created by a person; `bin/freeze.sh` prints the command and never runs it. | `test_freeze.py` |
| K6 | Python only through `uv run` (`uv run --frozen --project REPO python <file>`), never `python -m`. Tests: `uv run --frozen --project REPO pytest`. | every command in `TESTING.md` and `IMPLEMENTATION.md` |
| K7 | No code folder named `lib/` (`.gitignore` line 13 ignores it). | `test_layout_rl.py` runs `git check-ignore` on every code folder |
| K8 | The sibling folder `SW` is read only. The copy script opens it for reading, never writes into it, and never runs a test or script from inside it. | `bin/copy-shared.sh` uses only `sha256sum` and `cp` with `SW` as the source; `test_sibling_readonly.py` greps every script of `RL` for a write target under `SW` and checks the mtime of a canary file in a fake sibling folder |
| K9 | The sandbox root is `SBR` (`SW_SB_ROOT=/tmp/evalsb-recipe`, an override the copied `common.sh` accepts under `/tmp/`). The Recipe Ledger launcher sets it itself, so a run of one build can never reuse or clean the other build's sandbox. | `bin/rl-env.sh` (sourced before `common.sh`); `test_sandbox_root.py` |

### 1.3 Decisions taken where `MR` is silent, ambiguous or pulls two ways

Rows marked **owner** are repeated in section 13.

| Id | Where | The gap | Decision and reason |
|---|---|---|---|
| DR-1 | 3.0.3, REQ-25, REQ-06 | `MR` 3.0.3 puts `recipe_text` on the class card, while REQ-25 says the eight recipes live in one file. The sibling's card schema has `additionalProperties: false` and no `recipe_text`, and its eight cards are shared with Redesign 1. Adding a field would fork them. | The cards are copied unchanged. The recipe text lives in one file, `recipes/recipes.json`, keyed by card id. A test makes the two key sets equal. A new class is one card plus one recipe entry plus a lens placement, with no dispatcher or code change (REQ-10, tested with a fixture class C9). |
| DR-2 | 3.2(a) R2 | "Each gets Z0's brief, its recipe block and the ledger rule." No part order is given. | The RL brief is the Z0 brief text, produced by the copied renderer (`scaffold.briefs.render("Z0", ...)`), followed by the shared ledger rule, the RL block, the reviewer's recipes and, for search reviewers, the search-form line. So every RL brief starts with exactly the Z0 brief of the same document (a prefix test, section 6.2), and the Z0 parts are never re-implemented. |
| DR-3 | 3.2(a) ledger rule | The quoted RL block says "you never write more than 14 rows", but the lens table gives 6 rows to haiku and 8 to sonnet. | The block file holds the placeholder `{{LENS_ROW_CAP}}`. With the value 14 the rendered text equals the `MR` quote byte for byte (tested against `MR`). |
| DR-4 | 3.2(c) fallback, REQ-32 | `MR` fixes the fallback at "12 rows" when the luna cost per row is over 2 s. A measured cost of 2.5 s makes 12 rows cost 30 s against a budget of 29 s at b = 100, so the fixed fallback would still break the cap. | The lens cap is a function: `lens_row_cap(b, c, table_cap) = min(table_cap, floor((0.35 b - 6) / c))`, where 6 is the 1 s render, the 4 s reading and the 1 s check of 3.2(c). It gives 14 for c at most 2.07 and 12 for c up to 2.41 at b = 100, so `MR`'s 12-row fallback is one case of it. The rule is applied per stage with the smallest same-block b of the panel. If the cap falls below the number of recipes in a lens, the harness records `no_budget` and does not run RL on that panel. **owner**: confirm the generalisation. |
| DR-5 | 3.0.4, 3.2(a) | The row id is "the recipe id and a row number". Nothing says how the check knows which ids are legal. | A row id is `C<n>.<k>`. For one reviewer the legal ids are `C<n>.1` to `C<n>.<budget>` for each recipe `C<n>` in its lens. The check feeds that set to the shared reader as the assigned items. `probe` on a findings line is a row id. |
| DR-6 | 3.2(a) R3, REQ-26 | "The check script enforces the budget." Nothing says what happens to a row over budget. | Rows beyond a recipe's budget, or beyond the lens cap, in the order written, are flagged `over_budget`. They stay in the report and in coverage counts, but cannot be promoted and cannot support a blocker. The count is reported per reviewer. Nothing is deleted. |
| DR-7 | 3.0.1 H1, 3.0.7 guard rows, 3.2(e) | With no source file, recipe C2 has nothing to compare with. For documentation targets, 3.2(e) says C2 compares the document to the code, which is not a file a brief can name. | When `packages.json` has `source: null`, the renderer drops recipe C2 from every lens, CB-1 is absent (copied renderer) and `run.json` records `no_source` and `c2_not_applicable`. A lens never becomes empty: every lens of 5.1 keeps at least two recipes after C2 is dropped. For a documentation target the C2 recipe is therefore not applicable until a source path exists. **owner** (low): whether a documentation target may name a code file as its source. |
| DR-8 | 3.2(a) R3, REQ-27, REQ-30 | The ember re-ask has a clock condition but no mechanism. `claude -p` runs with `--no-session-persistence`, so a session cannot be resumed. | A re-ask is one fresh `claude -p` call to the same model with a repair prompt and the reviewer's own final message. It runs only for the ember reviewer, only when `ledger_missing` is the finding, and only if `now + 30 <= 1.35 b`, where `now` is the panel clock. A repaired message replaces the original only if its ledger parses and its findings block equals the original's. Rows of a repaired ledger cannot be promoted. A re-ask is counted as `reask`, never as a retry (REQ-30), and its seconds are inside the panel clock. Haiku and sonnet are not re-asked either (they are on the critical path and `MR` is silent). Section 7.6. |
| DR-9 | 3.0.5 check 2, REQ-16 | `MR` says `quote_other` must be in the source or a printed tool line. RL has no printed tool lines (no sheet), and most defects of C1, C6 and C7 are two plan texts that disagree. | Same decision as `SWD` DD-2 with the corpora of this redesign: `quote_other` is accepted when it is a flattened substring of the source, of the candidate, or of a tool result in the reviewer's own run transcript (`user` events, `tool_result` blocks). The corpus is recorded per row (`source`, `candidate`, `transcript`). "One search result" in REQ-16 means a `transcript` match. Assistant text never counts as a corpus. |
| DR-10 | REQ-28 | "The `ran` field is cross-checked against transcript tool calls in the analysis." The test for it is not defined. | Section 7.7: each row gets `ran_status` of `verified`, `unverified` or `not_a_tool_claim`. It is an analysis metric per class and per reviewer, not a gate and not part of the 1-second post-run check. |
| DR-11 | the task, 3.0 | The sibling is still being built: its cards, briefs, scaffold and sandbox script exist, but its ledger code, clock, launcher, judge copy and analysis do not (checked 2026-11-14 22:50 UTC: all twelve of them absent). | Section 3. Files that exist are copied byte for byte with their sha256 recorded. A file that does not exist when the copy script runs is written locally to the sibling's written contract, in the same file name, and marked `built-local`. Nothing is replaced silently later. |
| DR-12 | 5.3, 5.4 | Z0, K and Z0-raw are common to both redesigns, but the two builds have separate launchers, so each would run its own Z0 and K blocks (75 panel runs for Stage 1 in each build, 150 in total, where `MR` counts 95 runs for both redesigns together). | Each build runs its own same-block Z0 and K (this is what D1 requires: same day, same block). RL writes `run.json` and `timing.json` with the sibling's field names (`SWD` 2.2, 11.4), and the copied brief parts make the Z0 and K briefs byte-identical in both builds. A combined schedule can therefore pool the control arms later. **owner**: run one combined schedule (saves 132 panel runs, 458 against 326, section 12.1) or two separate ones (simpler). |
| DR-13 | 6.6 REQ-35 | The leave-one-class-out ablation changes "reach", which needs model runs, and the run table of 5.4 has no ablation runs. | Runnable here: the brief-level ablation (removing one recipe leaves every other recipe text and every lens position byte for byte unchanged) and the analysis-level report on the real runs. The model-stage ablation (8 extra arms x 4 documents x 3 runs = 96 panel runs) is a labelled manual item for the owner (same as `SWD` DD-13). |
| DR-14 | 3.2(h) | `MR` estimates Redesign 2 at about 310 specific lines and about 760 with the shared scaffolding. That list has no row checks, launcher, re-ask, judge copy or analysis. | `IMPLEMENTATION.md` gives its own list, which is larger (section 2 there). The `MR` figures are not used as a limit. |
| DR-15 | 3.0.2 CB-2 | CB-2 says "including every ledger row you marked PROBLEM". Z0 and K have no ledger. | Adopted from `SWD` DD-7: CB-2 stays verbatim in every non-raw arm (REQ-05), the dangling clause is measured as the number of Z0 and K reports with a `## Ledger` heading. |
| DR-16 | 5.3 arm K | The K paragraph needs a lead-in. | Adopted from `SWD` DD-14: `briefs/k-lead.txt` is copied. Its first line says it is a draft awaiting the owner. It is one shared decision of both builds. |

### 1.4 Decisions adopted from the sibling without change

`SWD` DD-3 (the demotion and CB-3 rule applies to findings linked to a ledger row; unlinked findings pass through unchanged; switch `CHECK_SCOPE=linked|all`, `all` unused), DD-8 (counted runs use one attempt and `NOFALLBACK=1`; a failed reviewer is scored zero findings), DD-9 (order: check on the raw report with a lenient line reader, then H2, then merge), DD-11 (cards carry `promote_category`; a promoted line takes the card's category), DD-12 (reviewers set only `probe`; the check fills `class` and `src`), DD-15 (Z0-raw sandbox is repository HEAD at launch minus ground-truth files and eval-workspace folders; fidelity UNVERIFIED), and the sibling's timing definitions (`SWD` 11.4, 11.5). Where this document says "as `SWD` n.n", the rule is taken over and not restated.

## 2. Architecture and run order

### 2.1 Data flow

```
 R0  harness (no model)        bin/build-sandbox.sh (copied) -> SBR/<doc>/repo   (base commit, no reflect, no reports: H3, H4)
                               candidate.md, source.md copied next to it
                                      |
 R1  lens render (serial, no model, under 1 s)     rl/lens.py + rl/render.py
        config/lenses.json + recipes/recipes.json + packages.json (source or not) + values.json (b, c)
        -> per reviewer: lens (ordered recipes, row cap), briefs/<rid>.txt, lens/<rid>.json
          |  any exception, invalid lens table, no_budget  ->  Z0 briefs, run.json: fallback=true (decided BEFORE any reviewer starts)
                                      |
 R2  three reviewers in parallel, blind, one attempt each (claude -p, NOFALLBACK=1, hang guard)
        final message = ... ## Ledger / ```ledger-v1 ... ``` / ## Findings block / ```findings-v1 ... ```
                                      |
 R3  ledger check (no model, under 1 s; skipped with check_skipped=true on any exception)
        read ledger-v1, id grammar, recipe coverage, budgets, quote tests, demote, promote
        ember only, if ledger_missing and now + 30 <= 1.35 b: one re-ask (rl/reask.py) before the check is rerun
        -> check/<rid>.ledger.json, check/<rid>.checked.md, check/check.json
                                      |
 H2  scaffold/normalise.py (copied)  truncate anchor, anchor2 (200) and claim (300), validate with FND.parse_block
                                      |
 R4  superclaude review merge   (unchanged: MRG)  ->  merged-1.md, ledger.json
                                      |
 JJ  blind Opus judge (brief byte-identical to JJ)  ->  score.json
                                      |
     analysis/analyze.py  (metrics, gates, stage rates, ran cross-check; REQ-28, REQ-39 to REQ-43)
```

Z0, K and Z0-raw run the same R0, R2, H2, R4 and JJ. They skip R1 and R3. Z0-raw also skips H1 to H4 and uses the original brief.

### 2.2 Run order, who runs it, what it writes

| Step | Actor | Reads | Writes (under `RUN/`) | On the critical path |
|---|---|---|---|---|
| R0 | `bin/build-sandbox.sh` | git object store of `REPO`, `config/packages.json` | `SBR/<doc>/repo`, `SBR/<doc>/sandbox.json`, `SBR/cand/<doc>/{candidate.md,source.md}` | no (built once, reused) |
| R1 | `rl/cli.py lens` | `config/lenses.json`, `recipes/recipes.json`, `config/values.json`, `config/packages.json` | `lens/<rid>.json`, `briefs/<rid>.txt`, `briefs/<rid>.sha256` | yes (about 1 s) |
| R2 | `bin/run-reviewer.sh` (one per reviewer) | brief, sandbox | `reviews/<rid>.attempt1.{json,err,md,meta.json}`, `reviews/<rid>.{md,meta.json,cost.json}` | yes |
| R3 | `rl/cli.py check`, and `rl/cli.py reask` for ember | reviews, `lens/<rid>.json`, candidate, source, transcripts | `check/<rid>.ledger.json`, `check/<rid>.checked.md`, `check/check.json`, `reviews/<rid>.reask.{json,md}` | yes (about 1 s; plus up to 30 s for an ember re-ask) |
| H2 | `scaffold/normalise.py` | `check/<rid>.checked.md` (RL) or `reviews/<rid>.md` (other arms) | `normalised/<rid>.md`, `normalised/h2.json` | no (outside the clock in every arm) |
| R4 | `superclaude review merge` | `normalised/*.md`, `resolution.json` | `merged/merged-1.md`, `merged/ledger.json` | no |
| JJ | `bin/judge-one.sh` | anonymised merged report | `scoring/<label>/{merged-anon.md,score.json,judge.json}` | no |

`run.json` (written first, updated at each step) holds: `arm`, `panel`, `doc`, `replicate`, `seed`, `block`, `rl_version`, `recipes_sha256`, `lenses_sha256`, `registry_version`, `freeze_tag`, the sha256 of candidate, source, every brief and the Z0 brief of the same document, the flags `fallback`, `no_source`, `c2_not_applicable`, `no_budget`, `check_skipped`, `reask` (list of reviewer ids), `time_cap_exception` (always false), the lens row cap used per reviewer and the value of `b` and `c` it came from, and `concurrent_panels_at_start`. `timing.json` is as `SWD` 11.4 with the fields of section 9.3.

### 2.3 Folder layout under `RL`

```
RL/
  DESIGN.md  TESTING.md  IMPLEMENTATION.md  SHARED-MANIFEST-DESIGN-TIME.tsv
  ruff.toml                      extends the repo's ruff settings
  scaffold/                      COPIED from SW (Tier A) or built-local (Tier B), section 3
    fnd.py  cards.py  lint.py  normalise.py  briefs.py          (Tier A, copied)
    ledgerv1.py  telemetry.py  clock.py                         (Tier B)
  rl/                            Redesign 2 specific
    recipes.py  lens.py  render.py  rowcheck.py  reask.py  cli.py  ledger_api.py
  recipes/                       recipes.json, rl-block.txt, search-form.txt, README.md (REQ-38), REVIEWS.md (REQ-08 records)
  analysis/                      analyze.py  ran_check.py  g0.py (ledger and time part only)      (analyze: Tier B)
  cards/                         C1.json .. C8.json, schema.json, README.md     (copied, never edited here)
  briefs/                        base.txt, cb1.txt .. cb5.txt, ledger-rule.txt, k-lead.txt, sheet-block.txt   (copied; sheet-block.txt is carried but unused)
  config/                        packages.json, lenses.json (panels, models, lenses), values.json (b, c, overhead, re-ask and cap constants),
                                 shared-list.json, shared-manifest.json, prereg.json (written at freeze), freeze.json
  bin/                           common.sh  build-sandbox.sh                           (copied)
                                 rl-env.sh  copy-shared.sh  run-panel.sh  run-reviewer.sh  judge-one.sh  anon.sh  judge-batch.sh
                                 make-schedule.py  run-schedule.sh  run-spike.sh  freeze.sh  check-order.sh
                                 check-sandbox-gt.sh  check-z0-parity.sh  open-manual-checks.sh
  holdout-gt/                    hold-out ground truth, written by its author after the freeze; never read by the harness before the judge
  fixtures/                      plans/ specs/ docs/ repos/ reports/ transcripts/ lens/ gt/ runs/   (TESTING.md section 2)
  tests/                         conftest.py, helpers.py, fakes/claude, test_*.py
  runs/  scoring/  results/      generated; not committed
```

`scaffold/` and `rl/` are plain packages put on `sys.path` by `tests/conftest.py` (copied) and by `rl/cli.py`. `rl/` imports `scaffold.fnd` for the real parser (`parse_block`, `flat`, `locate`, `_check_finding`, `_blocks_after`); the coupling to the private helpers is pinned by the copied `test_fnd_contract.py`.

### 2.4 Determinism rule

Lens render and brief render are pure functions of (`lenses.json`, `recipes.json`, the panel, `has_source`, the candidate path and sha256, the source path, the `b` and `c` values, `rl_version`). There is no clock, no network, no randomness (a lens has no item order to shuffle: recipe order is the lens table order). Every list is sorted or in table order, JSON is written with `sort_keys=True`, `ensure_ascii=False` and a trailing newline. The same input gives byte-identical briefs (tested). Time enters only as the hang guard, the re-ask condition and the `lens_row_cap` inputs, all of which are recorded in `run.json`.

## 3. What is reused from the Sweep Sheet build, and how it is copied

The task says to reuse the shared pieces of `MR` 3.0 by copying them from the sibling build at build time, with their sha256 recorded. The sibling is being built at the same time (its plan runs in another session), so what exists changes. This section fixes the rule and the list. `SHARED-MANIFEST-DESIGN-TIME.tsv` in this folder records what was there when this design was written (60 rows: 27 Tier A, 1 Tier S, 11 tests (T), 9 fixtures (F) and 12 Tier B rows that were all `ABSENT`; the first three lines of the file are comments).

### 3.1 The three tiers

| Tier | What | Rule at copy time |
|---|---|---|
| A (exists, shared by definition) | `cards/` (C1 to C8, schema, README), `briefs/` (nine parts), `scaffold/{__init__,briefs,cards,fnd,lint,normalise}.py`, `bin/common.sh`, `bin/build-sandbox.sh` | Copy byte for byte with `cp`. Never edit the copy. If a Tier A file is missing in the sibling, the copy script stops: nothing in `RL` may then be rebuilt by hand. |
| S (seed, then owned by RL) | `config/packages.json`: the three study documents with their base commits, candidate and source paths and masked paths | Copy once with `cp` and record the initial sha256. After that the file is RL's: the hold-out documents (`MR` 5.1) are added to it by their author after the freeze, which a byte-identical copy could not allow because `build-sandbox.sh` accepts another packages file only from `/tmp`. `--check` does not compare Tier S files. |
| T (shared tests) | the sibling tests that import nothing from `sweep/`: `conftest.py`, `helpers.py`, `test_briefs.py`, `test_cards.py`, `test_fnd_contract.py`, `test_lint.py`, `test_model_allowlist.py`, `test_normalise.py`, `test_paths.py`, `test_readme.py`, `test_sandbox.py`; fixtures they need: `fixtures/repos/build_repo.py`, `fixtures/reports/{anchor_250,claim_301}.md`, `fixtures/plans/{p_basic,p_clean,source}.md`, `fixtures/specs/{spec1,parent1}.md`, `fixtures/docs/doc1.md` | Copy byte for byte. A copied test that fails in `RL` is a finding about the copy, not a reason to edit the test. |
| B (not built yet at design time) | `scaffold/ledgerv1.py`, `scaffold/telemetry.py`, `scaffold/clock.py`, `bin/run-reviewer.sh`, `bin/judge-one.sh`, `bin/anon.sh`, `bin/judge-batch.sh`, `bin/run-panel.sh`, `bin/make-schedule.py`, `bin/run-schedule.sh`, `analysis/analyze.py`, `analysis/g0.py` | If the sibling file exists when `copy-shared.sh` runs and its content is the same on two reads 60 seconds apart, copy it with its matching sibling tests (when they import nothing from `sweep/`). Otherwise write the file in `RL` under the same name, to the sibling's written contract (the `SWD` section named in 3.3), and record `built-local`. A `built-local` file is never replaced by a later copy without a person reading the diff (`bin/copy-shared.sh --diff`). |

Not copied, and why:
- `sweep/*`, `analysis/__init__.py` of the sibling, and the tests that import `sweep` (`test_e1` to `test_e5`, `test_formats`, `test_extractors_common`, `test_plan`, `test_scope`): extractor code and tests, Redesign 1 only.
- `tests/fakes/claude` and `tests/test_fake_on_path.py`: the sibling's fake writes `S<n>` item rows. RL needs a fake that writes `C<n>.<k>` rows and a repair call (section 3.4), so `RL` has its own `tests/fakes/claude`. The copied `conftest.py` only requires that the first `claude` on `PATH` is `tests/fakes/claude`, so it works with either.
- `tests/test_layout.py`: it asserts the folders `sweep` and `analysis` exist. `RL` has `test_layout_rl.py` with the same K7 check and its own folder set.

`briefs/sheet-block.txt` is carried in the copy because the copied `scaffold/briefs.py` and `test_briefs.py` read it. No RL code renders it.

### 3.2 What `bin/copy-shared.sh` does

| Step | Behaviour |
|---|---|
| 1 | Reads the list of Tier A, T and B paths from `config/shared-list.json` (written at implementation from the three lists above). |
| 2 | For each path: `sha256sum` the sibling file twice, 60 seconds apart for Tier B only (the sibling is writing), and stop on a difference. |
| 3 | `cp` the file into `RL` at the same relative path, then `sha256sum` the copy and compare. |
| 4 | Writes `config/shared-manifest.json`: for every path `{tier, source: "SW/<rel>", sha256, bytes, copied_at, kind: "copied"\|"built-local"}`. A `built-local` entry names the `SWD` section it was written to. |
| 5 | `--check` re-hashes every copy against the manifest (a failure means someone edited a copy) and compares with the sibling's current file (a difference is reported as `drift`, a warning). |
| 6 | `--diff <path>` prints a unified diff between a `built-local` file and the sibling's file of the same name, for a person to read. |

It opens `SW` for reading only (K8). It never runs a script from `SW`. It never writes under `SW`.

### 3.3 What RL needs from each Tier B piece (the contract when it is built locally)

These are the minimum interfaces. They are copied from the sibling's written design, so a later swap of a local file for the sibling's is a drop-in.

| File | Contract (source) | What `rl/` calls |
|---|---|---|
| `scaffold/ledgerv1.py` | the reader of `SWD` 9.1 (heading regexes, fenced block with info string `ledger-v1`, per-line JSON, format errors counted, `dup_line`, `unknown_item`, limits), the checks of 9.2 with the corpora of DR-9, linking and demotion of 9.3, promotion of 9.3 validated by `FND._check_finding` | `rl/ledger_api.py` is the one adapter (at most 40 lines): `read(report, assigned_ids)`, `check(rows, corpora)`, `link_demote(findings, rows)`, `promote(rows, block, cards)`. If the sibling's signatures differ, only this file changes. |
| `scaffold/telemetry.py` | `class`, `probe`, `src` keys and the per-class table of `MR` 3.0.6 | `rl/rowcheck.py` |
| `scaffold/clock.py` | the clock of `SWD` 11.4 and the arithmetic helpers (`kill_s`, `hang_s`, `breakeven`) | `bin/run-panel.sh` through `rl/cli.py` |
| `bin/run-reviewer.sh` | `SWD` 11.1 table (one attempt, `NOFALLBACK=1`, brief from a file on stdin, `cd SBR/<doc>/repo`, hang-guard `timeout`, model-identity check, `BLOCK_OK` by `FND.parse_block` after H2 on a temporary copy, `hang_s`, `killed`, `prompt_sha256` in `meta.json`) | `bin/run-panel.sh` |
| `bin/judge-one.sh`, `bin/anon.sh`, `bin/judge-batch.sh` | `SWD` 11.3: the `BRIEF` text of `JJ` lines 12-23 byte for byte with the paths as variables; anonymisation by random label with reviewer ids replaced and paths redacted; model `claude-opus-5-5` only here | the experiment commands |
| `bin/run-panel.sh` | local by necessity: its arms differ (RL has no sheet). It follows `SWD` 11.4 to 11.7 for clock, hang guard, concurrency and merge, and section 9 below | the experiment commands |
| `bin/make-schedule.py`, `bin/run-schedule.sh` | `SWD` 11.6 and `SW/TESTING.md` section 5: block-randomised schedule with a recorded seed, at most 3 panels at once, refusal without a spike record | the experiment commands |
| `analysis/analyze.py` | `SWD` 14.3 outputs (metrics, consistency, gates D1 to D7, shares, `stages.jsonl`, judge audit) with the arm list `z0raw, z0, k, rl, rlh, rls` and the stage definitions of section 12.2 here | the experiment commands |
| `analysis/g0.py` | only the ledger-and-time half of G0 (`ledger_missing` rate, luna cost per row against its break-even). The selection half belongs to Redesign 1 and is not built. | the experiment commands |

### 3.4 What RL builds even when the sibling has everything

- `tests/fakes/claude`: reads the brief on stdin; finds the recipe ids (`R-C<n>.` headings) in it; writes `C<n>.1 ... C<n>.<budget>` rows for them; scenarios `ok`, `none_found`, `ledger_missing`, `ledger_after_findings`, `over_budget`, `recipe_missing`, `long_anchor`, `bad_block`, `api_error`, `wrong_model`, `sleep`, `exit127` and `repair` (the second call, whose brief starts with the repair sentence of section 7.6, returns the message with a ledger). It appends one line per call to `FAKE_CALL_LOG`. It is a test double; no model is started.
- `rl/*`, `recipes/*`, `config/lenses.json`, `bin/rl-env.sh`, `bin/copy-shared.sh`, `bin/check-z0-parity.sh` and the RL tests.

### 3.5 Z0 and K parity with the sibling

The Z0 and K briefs of the two builds are produced by byte-identical copies of `scaffold/briefs.py` and `briefs/` for byte-identical inputs. `bin/check-z0-parity.sh <doc>` renders the Z0 brief of one document with the copied code and prints its sha256; a person compares it with the `run.json` of any sibling Z0 run of the same document. The unit test (`test_shared_manifest.py::test_briefs_parts_match_manifest`) makes the same claim in code: each copied part equals its recorded hash.

## 4. Recipes (`recipes/recipes.json`)

### 4.1 Format

One file, `recipes/recipes.json`, holds all eight recipes (REQ-25). It has one governing source for each fact: the text is written once; the row budget is read out of the text, never stored a second time.

```json
{
  "schema": "rl-recipes/1",
  "version": 1,
  "recipes": {
    "C1": {"version": 1, "text": "For each acceptance criterion or requirement that says ... Write at most 4 rows."},
    "C2": {"version": 1, "text": "..."}
  }
}
```

Rules, each a test (`test_recipes.py`):
- The key set equals the id set of the cards in `cards/` (DR-1). A card with no recipe, or a recipe with no card, fails.
- Each `text` is at most 120 words (`MR` 3.0.3) and ends with exactly one sentence `Write at most N rows.` where N is an integer from 1 to 14. `recipes.row_budget(id)` parses N from that sentence. Eight budgets as in `MR` 3.2(a): C2 6, every other class 4.
- No `text` contains a path, a task number, a package name or a file name of the study, no `src/superclaude/` path, and no sentence that states an expected outcome (AO-1, AO-8, REQ-09). The lint of `scaffold/lint.py` checks the first part; the second is a word-list test (`expected`, `should find`, `will find`, `you will see`).
- The text equals the `MR` 3.2(a) draft wording byte for byte while `recipes.json` carries no `override` entry. A wording change after the compliance spike is a re-freeze (AO-5), recorded as `"override": {"C4": "<reason, owner approval>"}` and listed in the report.

The printed form of a recipe in a brief is `R-C<n>. <text>` (heading `R-C4.`, then the text without quotes), one paragraph per recipe.

### 4.2 The eight recipes (draft wording of `MR` 3.2(a), taken over unchanged)

Each is a detection procedure, not a "watch for" list. None has been run on any model (`MR`, "Not checked and unverified").

> **R-C1.** For each acceptance criterion or requirement that says every, all, each, complete, exhaustive, found, covers or no remaining: (1) write the finite check that would let a reviewer say yes, with its stopping rule; (2) copy the instruction sentence the criterion checks and write what set each of the two covers; (3) if you cannot write a finite check, or the two sets differ, mark PROBLEM. Write at most 4 rows.
>
> **R-C2.** Split the driving document into rules: one per sentence that contains must, shall, never, only, halts, reports or returns, or per table row. Take up to 10 rules, preferring those that govern a failure, an exit or a special case. For each, quote the candidate sentence that carries it. For the three with the most conditions, trace each failure path through the candidate's tasks to the output the rule governs. No carrying sentence, or a path that ends in a different output, is PROBLEM. Write at most 6 rows.
>
> **R-C3.** List every value, field or state that a task reads, maps or requires as the input to a decision (lookup tables, status mappings, conditions). For each, find the row, task or step that writes it, for every case the reader handles. A value with no writer in some case is PROBLEM. Write at most 4 rows.
>
> **R-C4.** For each criterion that embeds a command, pattern, selector or test name: write the exact text the same task tells the implementer to write or create. Apply the literal pattern to that text, case included (you may run it on a scratch string with Bash). Then ask what the command selects or matches on the current tree. A pattern that cannot match the ordered text, or a selector that picks fewer or other checks than the criterion needs, is PROBLEM. Do not use the current file as proof; it may already contain finished work. Write at most 4 rows.
>
> **R-C5.** For each change that alters a number, name, count, behavior or default that the repository may also state elsewhere: (1) write the old literal; (2) run one search of the whole tree for it, including root-level documents (changelogs, readmes, guides), mirrored copies and comments, not only the files the plan names; (3) list every hit the plan neither edits nor checks. A hit that would be false after the change is PROBLEM. Grade it with the grading check; never drop it. Write at most 4 rows.
>
> **R-C6.** For each sentence the plan states or dictates that says all, only, never, every, no other, or outside X nothing: (1) name the set it covers; (2) run one count or listing command for that set over the tree; (3) compare with the plan's other tasks and with the scope of the test or check said to enforce it (what does that test skip or not read?). A member outside the claim, a task that does the opposite, or a test scope narrower than the claim is PROBLEM. Write at most 4 rows.
>
> **R-C7.** List every constraint, one clause per line (split at semicolons and 'and'). List every piece of text the plan dictates word for word. For each text and each constraint on its topic, tick each clause. A text that omits or contradicts a clause is PROBLEM. Write at most 4 rows.
>
> **R-C8.** For each file the plan edits or creates, search the tests, scripts and docs for its path and distinctive strings: `git grep -l -F '<string>' -- tests scripts docs`. For each referencing file the plan never names, open it and decide whether it pins the text or behavior being changed. If it does and no task updates or runs it, mark PROBLEM. Write at most 4 rows.

Word counts, computed from the `MR` text: C1 71, C2 89, C3 56, C4 99, C5 86, C6 93, C7 50, C8 67 (all at most 120). All eight together are 611 words, which is the "about 800 tokens" of `MR` 3.2(a) at 1.33 tokens per word. The largest lens (ember on the primary panel: C4, C5, C6, C8) is 345 words, about 460 tokens, more than the "about 300 tokens per lens" of `MR`; luna 1 (C1, C2, C3) is 216 words, about 290 tokens.

### 4.3 What each recipe asks for, written for the maintainer (not shown to a reviewer)

This table is the swap-test and review aid (AO-2, REQ-08). It uses only target-neutral words; its examples are invented.

| Class (card route) | Reads (block kinds of `MR` 3.0.3) | A PROBLEM row quotes | `quote_other` expected from | Where it can go wrong (`MR` 3.2(d), 3.2(i)) |
|---|---|---|---|---|
| C1 (read) | `criterion`, `task` | `quote_plan`: the criterion sentence. `quote_other`: the instruction sentence it checks. | `candidate` | Writing a stopping rule is a new move; a model may accept a vague rule. |
| C2 (read) | `task`, `criterion`; the driving document | `quote_plan`: the task sentence nearest the rule, or the sentence that was expected to carry it. `quote_other`: the rule sentence of the driving document. | `source` | Up to 10 rules but 6 rows: a terse model may leave rules unrecorded (known ambiguity, row discipline below). Needs a source file (DR-7). |
| C3 (read) | `task`, `criterion`, `constraint` | `quote_plan`: the sentence that reads the value. `quote_other`: the nearest text that lists the cases or writers the reader handles. | `candidate` | Weak class: no reliable trigger shape; a reader must notice a missing write unaided. |
| C4 (search) | `criterion`, `task`, `dictated_text` | `quote_plan`: the criterion with the command. `quote_other`: the text the task orders, or the line a scratch `printf` test printed. | `candidate` or `transcript` | The model must choose which criteria to take. Must not use the current file as proof. |
| C5 (search) | `task`, `criterion`, `goal` | `quote_plan`: the sentence that changes the literal. `quote_other`: the hit line of the whole-tree search that the plan neither edits nor checks. | `transcript` | The weak step is choosing which changed claim to search for; root-level documents must be in scope. |
| C6 (search) | `criterion`, `dictated_text`, `constraint` | `quote_plan`: the universal sentence. `quote_other`: a member found by the count or listing command, another task's sentence, or a line showing the enforcing check's scope. | `transcript` or `candidate` | The counting search form is the model's to invent; the contradicting task sits elsewhere in the plan. |
| C7 (read) | `constraint`, `dictated_text` | `quote_plan`: the dictated text. `quote_other`: the constraint clause it omits or contradicts. | `candidate` | A clause-by-text matrix over many blocks is hard for a terse model. Only the broad form is claimed (`MR` section 2). |
| C8 (search) | `edit_target`, `gate` | `quote_plan`: the sentence that edits or creates the file. `quote_other`: the first hit line of the search that names a referencing file the plan never names. | `transcript` | Opening an unnamed test file is the step that luna and haiku skip. |

The class definition and the severity guidance of each class are in its card (`cards/C<n>.json`), the single source for them. A PROBLEM row whose class card says blocking only when a builder cannot satisfy the text is graded by the reviewer with the grading check, as in every arm.

### 4.4 Rows, ids and discipline

- **Row id.** `C<n>.<k>`, with `k` counted from 1 within one recipe (`C4.1`, `C4.2`), as the ledger rule of `MR` says. The row id is the ledger `item` and the findings `probe` (DR-5).
- **One row per recipe step that the model ran.** The recipes ask for more steps than their budgets (C2: up to 10 rules, 6 rows). The brief does not say which steps get rows. This design does not change that: which sentences a model ledgers is the self-selection factor `s` of `MR` 3.2(d), and it is measured (section 12.2). The compliance spike reports which rows models write first. If the spike shows that rows go only to the easy steps, a wording change is the owner's decision, recorded as an `override` entry (4.1) and followed by a re-freeze (4.6).
- **`NONE FOUND`.** A recipe that finds nothing to check in the document writes one row: verdict `OK`, empty `quote_plan`, and in `ran` the words `NONE FOUND` and what was searched, at most 15 words in all. The check counts it as coverage of that recipe (section 7.3). A recipe with a `NONE FOUND` row and other rows is flagged `none_found_with_rows`.
- **A recipe row is a question about the text, not a finding.** A finding is written only for a `PROBLEM` or `UNSURE` row, with `probe` set to the row id (ledger rule of `MR` 3.2(a)).

### 4.5 The search-form line

Stored in `recipes/search-form.txt`, added by the renderer to the lens of every search reviewer (ember on the primary panel, haiku and sonnet on the others). Generic placeholders only (AO-8):

> Search forms you may adapt: `grep -rlF '<path>' <test dirs>`; `grep -rlF '<name without extension>' .`; `grep -rnF '<old value>' . --include='*.md'` (include root files); `printf '%s' '<ordered text>' | grep -c '<pattern>'`.

### 4.6 Changing a recipe

A recipe is data in one file plus its card. Editing a recipe before the freeze is a normal commit. After the freeze tag (REQ-33) it is a re-freeze: new tag, new `freeze.json`, and every arm that used the old text is re-run or reported as run under the old tag. The version in `run.json` (`recipes_sha256`) says which text a run saw.

## 5. Lens table and lens render (`config/lenses.json`, `rl/lens.py`)

The lens table is the "small lens table in the launcher" of `MR` 3.2(a). It is data, not code: adding a panel, a model or a class placement is an edit of one JSON file, with no change to the renderer.

### 5.1 The table (`config/lenses.json`)

```json
{
  "schema": "rl-lenses/1",
  "version": 1,
  "panels": {
    "primary": {"label": "ember + 2x luna", "roles": {
      "S":  {"rid": "t2b-1", "model": "muse-ember-1.0", "lens": ["C4", "C5", "C6", "C8"], "table_cap": 14, "search_form": true,  "reask": true},
      "L1": {"rid": "t4-1",  "model": "gpt-6-luna",     "lens": ["C1", "C2", "C3"],       "table_cap": 14, "search_form": false, "reask": false},
      "L2": {"rid": "t3-1",  "model": "gpt-6-luna",     "lens": ["C2", "C4", "C7"],       "table_cap": 14, "search_form": false, "reask": false}}},
    "haiku": {"label": "haiku + 2x luna", "roles": {
      "S":  {"rid": "t2-1",  "model": "claude-haiku-5-5", "lens": ["C5", "C6", "C8"],     "table_cap": 6,  "search_form": true,  "reask": false},
      "L1": {"rid": "t4-1",  "model": "gpt-6-luna",       "lens": ["C1", "C2", "C3"],     "table_cap": 14, "search_form": false, "reask": false},
      "L2": {"rid": "t3-1",  "model": "gpt-6-luna",       "lens": ["C1", "C4", "C7"],     "table_cap": 12, "search_form": false, "reask": false}}},
    "sonnet": {"label": "sonnet + 2x luna", "roles": {
      "S":  {"rid": "t1b-1", "model": "claude-sonnet-5-5", "lens": ["C5", "C6", "C8", "C2"], "table_cap": 8, "search_form": true,  "reask": false},
      "L1": {"rid": "t4-1",  "model": "gpt-6-luna",        "lens": ["C1", "C3", "C7"],       "table_cap": 12, "search_form": false, "reask": false},
      "L2": {"rid": "t3-1",  "model": "gpt-6-luna",        "lens": ["C4", "C7", "C1"],       "table_cap": 12, "search_form": false, "reask": false}}}
  }
}
```

The reviewer ids are those of the sibling's `panels.json` (labels only; the model per id is explicit) so a later combined analysis reads both builds with one id map. Recipe order inside a lens is the order of the list: it is the order the reviewer is told to run them.

Values checked against `MR` 3.2(a) with a scratch script (2026-11-14): each class is in at least one lens of every panel; duplicated classes are C2 and C4 (primary), C1 (haiku), C1 and C7 (sonnet), exactly the REQ-25 sets; the recipe budgets add up to 16, 14 and 14 for the primary lenses (the ember lens is cut to 14), 12, 14 and 12 for the haiku panel (the haiku lens is cut to 6) and 18, 12 and 12 for the sonnet panel (the sonnet lens is cut to 8).

| Panel | Reviewer | Lens (run order) | Budgets sum | Table cap | Reason (`MR` 3.2(b)) |
|---|---|---|---|---|---|
| primary | ember (S) | C4, C5, C6, C8 | 16 | 14 | Search lens. Ember runs greps (78% of runs search recursively) and idles 60-90 s after its 41 s. |
| primary | luna 1 (L1) | C1, C2, C3 | 14 | 14 | Reading lens. Luna reads whole files and rarely searches. |
| primary | luna 2 (L2) | C2, C4, C7 | 14 | 14 | Reading lens. C2 and C4 duplicated for redundancy. |
| haiku | haiku (S) | C5, C6, C8 | 12 | 6 | Search lens; haiku sets the critical path (220-238 s), so its load is capped. |
| haiku | luna 1 | C1, C2, C3 | 14 | 14 | As the primary panel. |
| haiku | luna 2 | C1, C4, C7 | 12 | 12 | Reading lens; C1 duplicated. |
| sonnet | sonnet (S) | C5, C6, C8, C2 | 18 | 8 | Sonnet already opens unnamed files (35% of runs), so it takes the sweeps. |
| sonnet | luna 1 | C1, C3, C7 | 12 | 12 | Reading lens. |
| sonnet | luna 2 | C4, C7, C1 | 12 | 12 | Reading lens; C1 and C7 duplicated. |

Single point of failure per class on the primary panel (`MR` 3.2(i)): C5, C6 and C8 live only in ember; C1 and C3 only in luna 1; C7 only in luna 2; C2 and C4 are in two reviewers. A reviewer that is killed or invalid loses its classes for that run; `check.json` lists `classes_lost`.

### 5.2 Validation of the table (run at every render and in `test_lens.py`)

1. Every class id of `cards/` is in at least one lens of every panel.
2. Every lens holds 2 to 4 recipes, no repeats, every id has a recipe in `recipes.json` (REQ-25: at most 4 per reviewer).
3. `table_cap` is an integer from the number of recipes in the lens up to 14.
4. Every `model` passes `sw_assert_model` (K2). `rid` is unique inside a panel. Exactly one role has `search_form: true` per panel, and exactly one role has `reask: true` on the primary panel and none elsewhere (DR-8).
5. The duplicated-class sets of the three panels equal the REQ-25 sets (constants in the test, taken from `MR`).
6. After dropping C2 (`no_source`, DR-7) every lens keeps at least 2 recipes.

A table that fails any rule is a configuration error: the renderer raises `E_LENS_INVALID`, and the launcher falls back to the Z0 brief with `fallback=true, reason=lens_invalid` and prints the error loudly (section 8, row 3). The test suite fails on the same table, so a bad table never reaches an experiment.

### 5.3 Lens render (R1)

`rl.lens.render(panel, has_source, b_min, c_by_model)` returns, for each role:

| Field | Value |
|---|---|
| `rid`, `model` | from the table |
| `recipes` | the lens list with `C2` removed when `has_source` is false; the printed text of each is `R-C<n>. <text>` |
| `budgets` | `{class: N}` read from each recipe text (4.1) |
| `assigned_ids` | `C<n>.1 ... C<n>.<N>` for every recipe: the set the row check accepts (DR-5) |
| `row_cap` | `min(lens_row_cap(b_min, c_model, table_cap), sum(budgets))` (5.4); the number printed in the ledger rule |
| `search_form` | true for the search role |
| `reask` | true for the primary panel's ember |
| `no_budget` | true when `row_cap` is below the number of recipes (one row per recipe is the least that makes the ledger mean anything) |

The render is under 1 s: it reads three small files and does string joins. The output goes to `lens/<rid>.json`.

### 5.4 The row cap as a function of cost (DR-4)

`lens_row_cap(b, c, table_cap) = min(table_cap, floor((0.35 b - 6) / c))`, with b the smallest same-block Z0 median (seconds) of the panel in the stage, c the cost of one ledger row for the reviewer's model in seconds, and 6 the fixed seconds of 3.2(c) (1 render, 4 reading, 1 check). The cap is the 35% of b that the rule allows less the fixed part, divided by the cost of a row. The values of c are planning stand-ins (`MR` 3.1(c)): luna 2, haiku 4, sonnet 3, ember 0.4 (all UNVERIFIED); the 5-run timing spike replaces luna's (REQ-32).

| b (s) | c (s per row) | `floor((0.35 b - 6) / c)` | Cap used with `table_cap` 14 | Where it comes from |
|---|---|---|---|---|
| 100 | 2.00 | 14 | 14 | planning value; budget exactly used up (29 s, worst case below) |
| 100 | 2.07 | 14 | 14 | break-even at 14 rows |
| 100 | 2.41 | 12 | 12 | the 12-row fallback of `MR` 3.2(c) (break-even 2.42 s) |
| 100 | 2.50 | 11 | 11 | not in `MR`: 12 rows would cost 30 s against 29 s |
| 100 | 3.00 | 9 | 9 | |
| 122 | 2.00 | 18 | 14 | table cap binds |
| 122 | 3.00 | 12 | 12 | |
| 60 | 2.00 | 7 | 7 | below b = 35 not even 3 rows fit (0.35 x 34.3 - 6 = 6 s) |

For the critical-path reviewers of the other panels the table cap always binds at planning costs: haiku (0.35 x 220 - 6) / 4 = 17.75 against a table cap of 6; sonnet (0.35 x 259 - 6) / 3 = 28.2 against 8.

## 6. The brief change (`rl/render.py`, `recipes/`)

### 6.1 Parts and arms

A brief is a join of text parts in a fixed order, as in `SWD` 8.1. The Z0, K and Z0-raw parts are the sibling's, reached through the copied `scaffold/briefs.py`. The RL parts are files under `recipes/`, so the sha256 of each can be frozen (AO-5).

| Part | File | Source |
|---|---|---|
| Base, CB-1 (only with a source), CB-2 to CB-5, K paragraph, ledger rule | `briefs/*` (copied) | `RR` lines 13-17 and `MR` 3.0.2, 3.0.4 (see `SWD` 8.1) |
| RL block | `recipes/rl-block.txt` | `MR` 3.2(a) quoted ledger rule, with `{{LENS_ROW_CAP}}` in place of the number 14 (DR-3) |
| Recipes heading | one line in `rl/render.py`: `## RECIPES ASSIGNED TO YOU` (the only text not in a file; the counterpart of the sibling's `## SWEEP SHEET ITEMS`) | this design |
| Recipes | `recipes/recipes.json` | section 4.2, printed as `R-C<n>. <text>`, one paragraph each, in lens order |
| Search-form line (search role only) | `recipes/search-form.txt` | section 4.5 |

| Arm | Parts, in order |
|---|---|
| Z0-raw | base |
| Z0 | base, CB-1 (if source), CB-2, CB-3, CB-4, CB-5 |
| K | the Z0 parts, K paragraph |
| RL | the Z0 parts, ledger rule, RL block, recipes heading, the reviewer's recipes, search-form line (search role only). On `fallback=true`: the Z0 parts only. |

RL is built as `Z0 text + SEPARATOR + ledger-rule + SEPARATOR + RL block + SEPARATOR + heading + SEPARATOR + recipes (+ SEPARATOR + search-form)`, where the Z0 text comes from `scaffold.briefs.render("Z0", doc, None, source)` and the separator is the copied module's `SEPARATOR` (two newlines). Nothing in `rl/render.py` rebuilds a Z0 part.

### 6.2 Properties of the RL brief (each is a test)

1. **Z0 prefix.** The RL brief of a reviewer starts with exactly the Z0 brief text of the same document and source state, and the next part is the copied ledger rule (REQ-05, DR-2). A `fallback` brief equals the Z0 brief by sha256.
2. **CB-1 only with a source** (REQ-01): the Z0 prefix has it, or not, as the copied renderer decides. With no source the recipe C2 is absent from every reviewer (DR-7), `run.json` has `no_source` and `c2_not_applicable`, and no brief contains the string `Driving document:`.
3. **Recipes verbatim and bounded** (REQ-25): the recipe paragraphs in each reviewer's brief are the `recipes.json` texts, in lens order, at most 4, and the duplicated classes seen across the three briefs of a panel equal the lens table's. Parsing is by the heading `R-C<n>.`.
4. **Row cap rendered**: with `row_cap` 14 the RL block equals the `MR` quote byte for byte; with another value only that number differs.
5. **Search-form line** appears in exactly the search role's brief of each panel (REQ-25 lens text).
6. **No `src/superclaude/` path** in any rendered brief (REQ-09).
7. **No ground truth, package name, task number or file name of the study** in any part (AO-1, K3).
8. **Determinism**: the same inputs give the same bytes (section 2.4).

### 6.3 The RL block (`recipes/rl-block.txt`)

Draft wording of `MR` 3.2(a), taken over with one placeholder. It has not been run on any model. It holds no ground-truth text, no task number and no package name.

> RECIPES AND LEDGER. Before you review freely, run the recipes below that are assigned to you, in order. For each recipe step, write one row in the `ledger-v1` block. The row id is the recipe id and a row number, for example `C4.1`, then `C4.2`. Set `item` to the row id, `verdict` to OK, PROBLEM or UNSURE, and copy each quote exactly. In `ran`, say in at most 15 words what you ran or read. If a recipe finds nothing to check in this document, write one row for it with verdict OK, an empty `quote_plan`, and the words NONE FOUND and what you searched in `ran`. Each recipe has a row limit, and you never write more than {{LENS_ROW_CAP}} rows. A recipe row is a question about the text, not a finding. When you write a findings line for a PROBLEM or UNSURE row, set the findings key `probe` to the row id. Keep at least half of your time for your own review of the plan. The recipes do not replace it. Put the ledger under the heading `## Ledger`, directly above the findings block, in your final message.

The ledger rule that comes before it is the shared one (`briefs/ledger-rule.txt`, `MR` 3.0.4): the final message holds `## Ledger`, one `ledger-v1` block, `## Findings block` and one `findings-v1` block.

### 6.4 What the reviewer's final message looks like

The headings and info strings are exactly those of `MR` 3.0.4. Everything before `## Ledger` is free text. The rows are invented.

````
<report text, including the grading sentences>

## Ledger

```ledger-v1
{"item":"C4.1","verdict":"PROBLEM","quote_plan":"`grep -c 'export-format' docs/usage.md` prints at least 1","quote_other":"add the heading \"Export format\" to docs/usage.md","problem":"The pattern has a hyphen and lower case but the ordered heading has a space and a capital, so grep -c prints 0.","ran":"printf of the ordered heading into grep -c: 0"}
{"item":"C4.2","verdict":"OK","quote_plan":"","quote_other":"","problem":"","ran":"literal pattern matches the ordered text"}
{"item":"C8.1","verdict":"OK","quote_plan":"","quote_other":"","problem":"","ran":"NONE FOUND: git grep of edited paths over tests, scripts, docs"}
```

## Findings block

```findings-v1
{"id":"F1","severity":"MAJOR","blocking":false,"category":"unpassable-check","anchor":"`grep -c 'export-format' docs/usage.md` prints at least 1","refs":[],"claim":"The criterion's pattern cannot match the heading the task orders.","probe":"C4.1"}
```

verdict: FAIL
````

### 6.5 The K arm and the empty case

The K paragraph, the Z0 and K arms and CB-2's dangling clause are the sibling's (DR-15, DR-16). There is no "empty sheet" case in RL: every lens holds at least two recipes after C2 is dropped (5.2 rule 6), so the RL brief always differs from Z0's. `no_trigger` does not exist as an RL flag.

## 7. Ledger format, checks, promotion and the ember re-ask (`rl/rowcheck.py`, `rl/reask.py`)

The ledger carrier, the reader, the quote tests, linking, demotion and promotion are the shared rules of `MR` 3.0.4 and 3.0.5, written out in `SWD` 9.1 to 9.4. They are not restated here. This section gives what Recipe Ledger adds or changes: the row-id grammar, recipe coverage, budgets, the corpora, the re-ask and the `ran` cross-check.

### 7.1 Reading the final message

`RR` keeps only the final result message as the report (`RR` line 50, read) and checks only that a line starts with the `findings-v1` fence opener (`RR` line 57, read). `rl/rowcheck.py` therefore reads `reviews/<rid>.md` with the real parser as `SWD` 9.1 describes: the heading `## Ledger` first, no other heading before `## Findings block`, exactly one `ledger-v1` fenced block between them, every non-empty line parsed as JSON, format errors counted and never skipped, verdict read case-insensitively and counted as `normalised_verdict`. Zero or two blocks, an unclosed block, or a block outside that span is `ledger_missing` for that reviewer. Earlier assistant messages never feed the check (`MR` 3.0.4).

### 7.2 What the check does, in order (R3)

Per reviewer, on the raw report, in under 1 second (no model; the transcript is read only for the corpus of DR-9).

| # | Check | Result recorded |
|---|---|---|
| 1 | Read the ledger (7.1). | `ledger_missing`, `format_errors`, `dup_line`, `normalised_verdict` |
| 2 | **Row-id grammar.** `item` must match `^C[0-9]+\.[0-9]+$` and its class must be in this reviewer's lens. | `unknown_item: [row, ...]`; the row is kept for counting and cannot be linked or promoted |
| 3 | **Recipe coverage.** Every recipe of the lens has at least one accepted row. A `NONE FOUND` row counts (7.3). | `recipe_missing: [C5, ...]`; no re-ask for it |
| 4 | **Budgets.** Per recipe, rows beyond that recipe's budget (the id number is above the budget, or the recipe has more rows than its budget) and rows beyond the lens `row_cap` in the order written are `over_budget`. | `over_budget: [{row, reason: recipe\|lens}]` (DR-6) |
| 5 | `quote_plan` is empty or 12 to 200 flattened characters, and when present is a flattened substring of the candidate (`FND.locate` is non-empty). | `quote_plan_ok` |
| 6 | `quote_other` is a flattened substring of the source, the candidate, or a tool result of the reviewer's own transcript (DR-9). | `quote_other_ok`, `corpus` |
| 7 | Support: `quotes_supported` (both quotes ok and different), `search_supported` (both ok and the corpus is `transcript`), `supported = quotes_supported or search_supported`. | per row |
| 8 | Link each findings line to a row (by `probe`, or when the row's flattened `quote_plan` lies inside the line's flattened `anchor`). | `probe_unknown`, `ok_but_finding` |
| 9 | Demote a linked blocking finding to non-blocking when its row is an unsupported PROBLEM (`row_unsupported`), an UNSURE row (`row_unsure`), has no CB-3 sentence (`no_cb3`), or failed to parse (`row_missing`) (as `SWD` 9.3). A finding that is not linked is left alone (DR-12 adopts `SWD` DD-3). Each cause is counted apart (INV-007). | `demoted.*`, `format_induced_demotions` |
| 10 | Promote a PROBLEM row that has no linked findings line, as `SWD` 9.3, with these RL limits: the row is not `unknown_item`, not `over_budget`, has a `quote_plan` that is present and `quote_plan_ok`, and its ledger was not repaired by a re-ask. The line is validated with `FND._check_finding` and inserted inside the one findings block; on any failure it is logged in `promotion_failures` and skipped. | `promoted`, `promotion_failures` |
| 11 | Fill `class` from the row id prefix and keep the reviewer's `probe` on linked lines; `src: ledger` on promoted lines (DR-12 of `SWD`, `MR` 3.0.6). | telemetry on `check/<rid>.checked.md` |

Check 10 is stricter than `SWD` 9.3 on one point: it requires `quote_plan_ok`, so a promoted line can never anchor to text that is not in the candidate. The sibling's text says only that a row with an empty `quote_plan` is not promoted. If the sibling's implementation promotes a row whose quote is not in the candidate, the two builds differ on that case; `bin/copy-shared.sh --diff` shows it at reconcile time.

### 7.3 `NONE FOUND`

A row counts as `none_found` when its verdict is `OK`, its `quote_plan` is empty, and its `ran` contains `NONE FOUND` (case-insensitive). It covers its recipe (check 3). A recipe with a `none_found` row and other rows is flagged `none_found_with_rows`. A `none_found` row for a search recipe (C5, C6, C8) whose reviewer made no search tool call is reported by the `ran` cross-check as `unverified` (7.7). The rate of `none_found` rows per class is reported, because a model that writes `NONE FOUND` for every recipe is a rubber stamp.

### 7.4 Output of the check

`check/<rid>.ledger.json`: the parsed rows with every result above. `check/<rid>.checked.md`: the report with demotions and promotions applied (the raw `reviews/<rid>.md` is never edited). `check/check.json`:

```
{ "ledger_missing": [rid], "recipe_missing": {rid: [class]}, "unknown_item": n, "over_budget": {rid: n},
  "format_errors": n, "normalised_verdict": n, "dup_line": n, "probe_unknown": n, "none_found": {class: n}, "none_found_with_rows": n,
  "rows": {"OK": n, "PROBLEM": n, "UNSURE": n}, "rows_per_reviewer": {rid: n}, "rows_per_recipe": {class: n},
  "demoted": {"row_unsupported": n, "row_unsure": n, "no_cb3": n, "row_missing": n}, "format_induced_demotions": n,
  "promoted": n, "promotion_failures": [...], "ok_but_finding": n, "block_unusable": [rid],
  "classes_lost": {rid: [class]}, "reask": {rid: {"allowed": bool, "reason": str, "accepted": bool, "seconds": n}} }
```

`format_induced_demotions` counts demotions where the row's `problem` is non-empty, both quotes are present, and a quote test failed or a line did not parse. It is the number that tells whether the 0.914 squared figure of `MR` 3.0.5 shows up in practice (luna's anchors are verbatim 91.4% of the time, `CR` line 294; `MR` 3.2(i) repeats it).

### 7.5 Flags

| Flag | Meaning | Written to |
|---|---|---|
| `fallback=true` | the Z0 brief was run because the lens render failed (invalid table, exception) | `run.json` |
| `no_source=true`, `c2_not_applicable=true` | no source file; CB-1 and recipe C2 not applied (DR-7) | `run.json` |
| `no_budget` | `row_cap` below the number of recipes for some lens: RL is refused on that panel | `run.json`, exit code 3 of `run-panel.sh` |
| `check_skipped=true` | the post-run check raised; demotion and promotion skipped for the whole run and the findings block merged as written | `run.json`, `check/error.log` |
| `ledger_missing`, `recipe_missing`, `reask` | per reviewer, as above | `check.json`, `run.json` |

### 7.6 The ember re-ask (REQ-27)

**Condition.** `reask_allowed(role_reask, ledger_missing, already_asked, now_s, b_s)` is true only when all of these hold: the role has `reask: true` in the lens table (the primary panel's ember only, DR-8); the check found `ledger_missing` for that reviewer; no re-ask has run for it; and `now_s + 30 <= 1.35 * b_s`, where `now_s` is the panel clock (seconds since `t0`, section 9.3) at the moment the reviewer's report was read and `b_s` is the same-block Z0 median of the slowest reviewer for this panel and document (the planning stand-in until measured). The constants 30 and 1.35 live in `config/values.json`. There is no re-ask for luna, whatever the clock says: a luna report ends at about b + 22 s, and b + 22 + 30 = b + 52 is above 1.35 b for every b below 148.6 s (52 / 0.35), which covers the whole planning range of the primary panel (INV-010). Haiku and sonnet are not re-asked (DR-8).

**Mechanism.** One fresh call: `claude -p --model <the ember model> --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit`, in the same sandbox, under `timeout 30`, with the repair prompt below on stdin. The model-identity check of `run-reviewer.sh` applies, and `NOFALLBACK=1` holds. Draft wording, not run on any model:

> Your final message was kept as your review, but it has no valid `ledger-v1` block directly above the `## Findings block` heading, so the checks cannot read it. Your message follows between the lines marked BEGIN and END. Reply with the same message again, with one section added: the heading `## Ledger`, then one fenced block with info string `ledger-v1`, one JSON object per line with the keys item, verdict, quote_plan, quote_other, problem and ran, one line for each recipe row you actually ran. Do not add a row for a step you did not run. Do not change the findings block. Do not run any command.
> BEGIN
> {the original final message}
> END

**Acceptance.** The repaired message replaces the original only if its `ledger-v1` block parses and sits directly above the findings block, and its findings block, parsed as JSON lines in order, equals the original's. Otherwise it is discarded and the run records `ledger_missing`. A repaired ledger is marked `via_reask`: its rows may demote findings but are never promoted (7.2 check 10), because they are written from the model's memory of a run that is over.

**Accounting.** The call is recorded as `reask` in `run.json` and `check.json`, never as a retry (REQ-30 counts retries; a re-asked ember produced a report and is not scored as zero findings). Its seconds are inside the panel clock (`reask_s` in `timing.json`) and its tokens in `cost.json`. The decision function is pure and takes the clock as an argument, so the test uses a fake clock (TESTING REQ-27).

### 7.7 The `ran` cross-check (REQ-28, analysis only)

Run by `analysis/ran_check.py` over a run folder. It reads `reviews/<rid>.attempt1.json`, whose shape was read from one finished ember run: events `system`, `assistant`, `user`, `result`; assistant `message.content` blocks of type `thinking`, `text` and `tool_use` (`name` `Bash` or `Read`, `input.command` or `input.file_path`); `user` events with `tool_result` blocks (`content` a string, `tool_use_id`). Other models' transcripts may differ and are checked at the compliance spike (section 13).

For each ledger row:

| `ran_status` | Rule |
|---|---|
| `not_a_tool_claim` | `ran` names no command word (`grep`, `egrep`, `rg`, `git`, `printf`, `find`, `ls`, `cat`, `sed`, `awk`, `wc`, `head`, `tail`, `pytest`, `jq`) and the recipe is not C5, C6 or C8. Reading the candidate cannot be verified: `claude -p` may attach the `@file` text without a `Read` call. |
| `verified` | `ran` names a command word, and the transcript has a `Bash` call whose command contains that word and (shares a distinctive token of four or more letters with `ran` or `quote_other`, or the call's result contains `quote_other`). |
| `unverified` | `ran` names a command word and no such call exists; or the recipe is C5, C6 or C8 and the transcript has no `Bash` search call at all, whatever `ran` says. A `NONE FOUND` row for a search recipe follows the same rule. |

Reported per reviewer and per class: counts of each status, and the share of search-recipe rows that are `unverified` (the "OK row written without doing the step" signal of `MR` 3.2(i)). It is not a gate. The rule is a heuristic; its agreement with a person's reading is a manual check (TESTING REQ-28, row M), because a heuristic that nobody audited is not evidence.

## 8. Failure and fallback behaviour

The rule behind every row: the decision to fall back is taken before any reviewer starts, so a running reviewer's brief is never changed (INV-012 of `MR`). A failure after the reviewers have finished never discards a reviewer's own findings. The guard rows of `MR` 3.0.7 that concern reviewers (gateway down, judge error, missing source, two reviewers left) apply and are rows 6, 22, 3 and 7 below, in that order.

| # | Condition | Detected by | Action | Recorded | Counted |
|---|---|---|---|---|---|
| 1 | The lens render raises (unreadable `recipes.json`, a recipe with no budget sentence, an exception in `render.py`) | `rl/cli.py lens` exits non-zero | Z0 briefs for all three reviewers; the run continues (REQ-12 a) | `fallback=true, reason=error` and the exception class in `lens/error.json` | the run stays in arm RL (intention to treat); fallback count per arm |
| 2 | The lens table is invalid (section 5.2) | `E_LENS_INVALID` from the renderer | as row 1; the error is printed to stderr and `run.log` | `fallback=true, reason=lens_invalid` | same; the test suite fails on the same table, so this is a configuration bug found early |
| 3 | No source file | `packages.json: source: null` | CB-1 not rendered; recipe C2 dropped from every lens (DR-7) | `no_source`, `c2_not_applicable` | class C2 reported as not applicable for that document; the lens caps are recomputed |
| 4 | `row_cap` below the number of recipes for a lens (`no_budget`) | `rl.lens.render` | the run is refused (`run-panel.sh` exit 3); the schedule excludes RL on that panel | `no_budget` in the stage record | not counted; reported |
| 5 | The sandbox is missing, dirty or contains a masked path | `build-sandbox.sh` exit 2 (copied), `git status --porcelain` before the run | the run is refused, not run in a fallback: the sandbox is the experiment's floor | log line | not counted; must be rebuilt |
| 6 | A reviewer hits the hang guard, fails the model-identity check, returns an API error, or has no usable findings block after H2 | `bin/run-reviewer.sh` (single attempt, `SWD` DD-8 adopted) | the reviewer is dropped from the merge and scored zero findings; survivors keep their lenses | `killed`, `invalid` or `error` in `reviews/<rid>.meta.json`; `classes_lost` in `check.json` | per arm (REQ-30); the classes that lived only in that reviewer (5.1) are listed |
| 7 | Only two reviewers available before launch (a model probe fails) | probe in `run-panel.sh` | the run starts with the reviewers that answered; lenses are not re-assigned in version 1 (a re-assignment would be a different arm) | `reviewers: 2`, `classes_lost` | flagged and counted (intention to treat) |
| 8 | A reviewer wrote no parseable `ledger-v1` block directly above the findings block | `rl/rowcheck.py` | luna: no repair, no demotion, no promotion for that reviewer, findings block merged as written. Ember: the re-ask of 7.6 if `now + 30 <= 1.35 b`, else the same as luna | `ledger_missing`, `reask` | rate per arm; at most 10% in the compliance spike before any arm (REQ-17) |
| 9 | A lens recipe has no row (`recipe_missing`), a row id is unknown, or rows exceed a budget | `rl/rowcheck.py` | recorded; rows kept for counting; over-budget and unknown rows cannot be promoted | `recipe_missing`, `unknown_item`, `over_budget` | per arm and per class |
| 10 | `rl/cli.py check` raises | exception caught in `run-panel.sh` | the whole post-run check is skipped; raw reports go to H2 and the merge (REQ-12 b) | `check_skipped=true`, `check/error.log` | per arm; different from `fallback` |
| 11 | A promoted line fails `FND._check_finding` (long id, short anchor, duplicate id) | `rl/rowcheck.py` | the line is not inserted | `check.json: promotion_failures` | counted apart from reviewer findings |
| 12 | A quote copied inexactly (luna: 91.4% verbatim) | checks 5 and 6 fail on a row whose text is otherwise complete | the linked finding is demoted to non-blocking, never deleted | `format_induced_demotions` | reported with every result (INV-007) |
| 13 | Compliance: a terse luna writes OK rows without doing the steps | the `ran` cross-check (7.7); `ledger_missing` and quote validity in the spike | none at run time | `ran_status` per row | the compliance spike must show `ledger_missing` at most 10% before any arm; if it fails, RL does not run |
| 14 | Prompt length hurts small models | lens validation (at most 4 recipes per reviewer) | none at run time | `recipes` per brief | arm K (plain words) shows whether the recipe wording adds anything (D7) |
| 15 | The row budget forces a choice by salience: the model ledgers the sentences that stand out and skips the true one (T2 again, inside a smaller space) | none at run time | `NONE FOUND` lets a reviewer say a recipe found nothing; budgets sized per class | selection stage rows (section 12.2) | `s` per class is measured, never assumed |
| 16 | Ember's own sweeps give false hits | CB-3; `UNSURE` is non-blocking; a blocker needs `supported` | the demotion rules of 7.2 | `demoted.*` | gate D4 |
| 17 | Wrong blockers grow (earlier 2x ember panels added 2.75 to 3.25) | as row 16 | as row 16 | wrong blockers per run | gate D4: at most Z0 + 1.0 per run; clean twins at most Z0 + 0.7 |
| 18 | Item attention displaces free review | CB-5 (half of the time for free review) | none at run time | non-probe findings per run | gate D6 (blocking) |
| 19 | Time at b = 100, worst case of 14 rows: 134 s against a cap of 135.0 s | `lens_row_cap` (5.4); the 5-run timing spike (REQ-32) | the lens cap falls with the measured cost per row; `no_budget` below the number of recipes | `row_cap`, `b`, `c` per reviewer in `run.json` | the median, not one run, is judged (REQ-29) |
| 20 | A reviewer is killed at the hang guard or the re-ask times out | `timeout` | as row 6; a timed-out re-ask keeps the original report | `killed`, `reask.accepted=false` | per arm |
| 21 | Gateway model identity bleed (a model served as another) | `observed_model` against `expected_model` (copied logic of `RR` lines 51-56) | row 6 | `model_ok=false` | per arm |
| 22 | The judge returns an API error but leaves a score file | `analysis/analyze.py audit-judges` (`CR` line 147 describes one such file) | the score is invalidated and the judge re-run | audit log | REQ-43 |
| 23 | A re-asked ledger holds rows for steps the model did not run | `ran` cross-check; no promotion from a repaired ledger | demotion rules still apply | `via_reask` on every such row | `reask` count per arm; the analysis reports yield with and without re-asked reviewers |
| 24 | A copied shared file is edited, or the sibling's file drifts from the copy | `bin/copy-shared.sh --check`; `test_shared_manifest.py` | an edited copy fails the test; drift is a warning that a person reads | `config/shared-manifest.json` | reported at every freeze |
| 25 | Both builds run on one host and share a sandbox or `/tmp` path | K9 (`SW_SB_ROOT=/tmp/evalsb-recipe`); `test_sandbox_root.py` | the launcher sets the root itself and refuses a root that is the sibling's | log line | never counted |
| 26 | The ledger heading order is wrong (ledger after the findings block, or another heading between) | `rl/rowcheck.py` reading rule 7.1 | `ledger_missing` | per reviewer | rate per arm |
| 27 | A recipe cannot apply to the target (a spec with no tests, a document with no gate) | the model writes `NONE FOUND` | none | `none_found` per class | rate reported; a high rate on one class is a signal to re-derive that recipe for the target (11.3) |

## 9. Harness (`bin/`): arms, clock, hang guard, merge

### 9.1 `bin/run-panel.sh`: one panel, one document

```
bin/run-panel.sh --arm {Z0-raw|Z0|K|RL} --panel {primary|haiku|sonnet} --doc <document id> \
                 --replicate <n> --block <n> --seed <int> --run-id <id> [--b <seconds>] [--dry-run]
```

The arms RLh and RLs of `MR` 5.3 are `--arm RL --panel haiku` and `--panel sonnet`; the analysis derives the label from the pair. Environment: `NOFALLBACK=1` is required (DD-8 adopted); `SW_SB_ROOT` is set by `bin/rl-env.sh` (K9); `PYTHONDONTWRITEBYTECODE=1`. Output goes to `RL/runs/<run-id>/`.

Order of work, one clock (section 9.3):

1. Check the sandbox (`build-sandbox.sh` already ran; `git status --porcelain` empty; K4).
2. Start the panel clock `t0`. Arms Z0-raw, Z0 and K: render the Z0 (or raw, or K) brief for the three reviewers. Arm RL: R1, the lens render (section 5.3) and the RL briefs; on any failure render the Z0 briefs and set `fallback=true`.
3. `--dry-run` stops here: it writes `briefs/`, `lens/` and `run.json`, prints the three `claude` command lines with the brief sha256 of each, and starts no model.
4. Start the three reviewers in parallel with `bin/run-reviewer.sh`, each under `timeout <hang guard>` (9.4). Reviewer ids and models come from `config/lenses.json` for every arm: the roles and models are the same in all arms, only the lens differs (no second panel file exists).
5. When each reviewer ends, record `rev_end[rid]`. Arm RL, for each report: run `rl/cli.py check`; if the ember's check finds `ledger_missing` and `reask_allowed` is true (7.6), run `rl/cli.py reask` and check again. Any exception in the check sets `check_skipped=true` and the raw reports go on.
6. Stop the panel clock. Then, outside the clock: H2 (`scaffold/normalise.py`), the merge (9.6), the sandbox-clean check (K4).
7. Write `run.json` and `timing.json`.

Exit codes: 0 done (including a run with fallback or a killed reviewer); 2 usage error, bad document, or sandbox invalid; 3 `no_budget`; 4 refused (`NOFALLBACK` not set, a model outside the allowlist, or a sandbox root that is the sibling's).

### 9.2 `bin/run-reviewer.sh` against `RR`

As the table of `SWD` 11.1: the brief comes from a file on stdin, `cd SBR/<doc>/repo`, one attempt and no model ladder, the hang guard as `timeout`, the model-identity check kept, `BLOCK_OK` by `FND.parse_block` after H2 on a temporary copy (a missing `ledger-v1` block does not make it false), and `hang_s`, `killed`, `prompt_sha256` in `meta.json`. RL adds only the repair call of 7.6, which the panel script makes with the same flags. `RR` itself is not edited; this is a new script in `RL/bin/`.

### 9.3 The panel clock (REQ-29)

One clock per run in `timing.json`, as `SWD` 11.4, with RL's definitions:

| Field | Definition |
|---|---|
| `t0` | monotonic time immediately before R1 (RL) or before the first brief is rendered (other arms) |
| `render_s` | duration of the lens render and brief render (R1); 0 for other arms |
| `rev_start[rid]`, `rev_end[rid]` | launch and end of each reviewer process |
| `check_s` | duration of R3 for all reviewers, excluding re-asks; 0 for other arms |
| `reask_s` | seconds of the ember re-ask, 0 when none |
| `panel_elapsed_s` | RL: end of R3 minus `t0` (it includes `reask_s`). Other arms: last `rev_end` minus `t0`. H2, the merge, the judge and the optional verifier (REQ-46) are outside the clock in every arm. |
| `slowest_reviewer_s` | max over `rev_end - rev_start` (the quantity b is a median of, for Z0) |

Mean and median per arm per document are reported; gate D1 uses the medians.

### 9.4 Hang guard (REQ-30)

`hang_s = 1.5 * (b + expected_overhead)`, counted from `t0`, with the expected overhead of the arm: RL 28 s on the primary panel (3.2(c): 1 + 4 + 11 rows x 2 + 1) and 30 s on the haiku and sonnet panels (3.2(c)); 0 for Z0, K and Z0-raw. Each reviewer runs under `timeout <hang_s - time already used>`. A killed reviewer is recorded `killed` and scored zero findings. Values at planning b (`SW/config/values.json` lists 100, 120 and 122 for the primary panel):

| Panel, arm | b (s) | `hang_s` (s) |
|---|---|---|
| primary, RL | 100 / 120 / 122 | 192 / 222 / 225 |
| primary, Z0 | 100 / 120 / 122 | 150 / 180 / 183 |
| haiku, RL | 220 / 238 | 375 / 402 |
| sonnet, RL | 259 / 302 | 433.5 / 498 |

The sibling's expected overhead for its own arm is 29, 37 and 31 s (`SWD` 11.5); RL's differ because the work differs.

### 9.5 Schedule and concurrency

As `SWD` 11.6: `bin/make-schedule.py` writes a block-randomised `schedule.tsv` (one block per replicate, recorded seed) and `bin/run-schedule.sh` runs it with `--max-panels N` panels at once. `SPEC` says the gateway is untested above about 10 parallel runs across all sessions, and the sibling's own schedule runs up to 3 panels (9 reviewer sessions) at once. Two builds scheduled at the same time would therefore reach 18. So the default here is `--max-panels 1` (3 sessions, 1 ember), and the owner raises it to 3 only while the sibling's schedule is idle (13.1 item 10). It refuses to start without the timing-spike record of REQ-32. Arms of one block are compared with each other, never with a run from another day.

### 9.6 Merge

As `SWD` 11.7: a per-run `resolution.json` of the reviewers that finished, then

`superclaude review merge --ledger RUN/merged/ledger.json --doc SBR/cand/<doc>/candidate.md --round 1 --report <rid>=RUN/normalised/<rid>.md ... --resolution RUN/resolution.json --out RUN/merged/merged-1.md`

(the options `--ledger`, `--doc`, `--round`, `--report`, `--resolution`, `--out` and `--cap` of `MRG`, read in full). A killed or invalid reviewer is absent from `--report`. If the merge refuses the round it is recorded `merge_refused` and scored zero; it is not re-run. The telemetry keys `class`, `probe` and `src` do not reach `merged-1.md` or the merge ledger (`SWD` 9.3 read `LED.merge_round` and `_check_finding`; REQ-11 confirms it by running the real merge), so the blind judge cannot see which arm a report came from.

### 9.7 Judge

`bin/judge-one.sh` is `JJ` with its paths as variables and the `BRIEF` text of lines 12-23 byte for byte (REQ-05, REQ-43); model `claude-opus-5-5` and only here (K2). It reads a ground-truth file by its package path, which is what scoring is. No other script of this design reads one before the freeze. Anonymisation, the second judge on a 15% sample and the audit of every judge output are as `SWD` 11.3 and 14.3.

## 10. Time budget against the +35% rule

The rule (D1 of `MR` 5.7): the per-package median elapsed time of RL is at most 1.35 times the per-package median of the same-day Z0 in the same randomised block; the 90th percentile at most 1.50 times; kills at most 10%. b is Z0's per-package median of the slowest reviewer. Everything below is arithmetic on planning values from `MR` 3.1(c) and 3.2(c); each value marked "planning" is replaced by a measured one (REQ-29, REQ-31, REQ-32). I re-derived every figure of `MR` 3.2(c) with a scratch script on 2026-11-14 and they all check; the additions are the rows for b = 120 and b = 122 at the break-even, and the cost-driven row cap of 5.4.

### 10.1 Cost model (planning, UNVERIFIED)

A ledger row is about 75-90 output tokens. At 48 tokens per second (derived from one luna run, 4.9k tokens in 102 s) a row costs 1.6-1.9 s. Planning cost per row c: luna 2 s, haiku 4 s, sonnet 3 s, ember about 0.4 s (`MR` 3.1(c)). Fixed parts: lens render and brief render 1 s, reading the recipes 4 s, the post-run check 1 s (it includes a Python start-up; `SWD` 12.1 measured one `uv run` start plus the `findings` import at 0.28 s on this host).

### 10.2 Critical path, primary panel (ember + 2x luna)

Luna sets the critical path: `render + (b + 4 + rows x c) + check`.

| Step | Seconds | Bound |
|---|---|---|
| R1 lens render | 1 | none |
| R2 luna 1 and luna 2, 3 recipes each | `b + 4 + rows x 2`: expected 11 rows = b + 26, worst 14 rows = b + 32 | hang guard; lens row cap |
| R2 ember, 4 recipes (4 searches x 3 s + up to 14 rows x 0.4 s + thinking) | about 81 (41 baseline + 40); off the path until it reaches b + 28 | hang guard |
| R3 ledger check | 1 | none |
| Critical path | expected `1 + b + 4 + 22 + 1 = b + 28`; worst `1 + b + 4 + 28 + 1 = b + 34` | |

| b (s) | Expected (b + 28) | Increase | Worst, 14 rows (b + 34) | Increase | Cap 1.35 b | Slack at worst | Break-even s per row at 14 rows |
|---|---|---|---|---|---|---|---|
| 100 | 128 | +28.0% | 134 | +34.0% | 135.0 | 1.0 | 2.07 |
| 120 | 148 | +23.3% | 154 | +28.3% | 162.0 | 8.0 | 2.57 |
| 122 | 150 | +23.0% | 156 | +27.9% | 164.7 | 8.7 | 2.62 |
| 116 (mean) | 144 | +24.1% | 150 | +29.3% | 156.6 | 6.6 | 2.47 |
| 348 (three-package sum) | 432 | +24.1% | 450 | +29.3% | 469.8 | 19.8 | |

(The 116 and 348 rows are the planning stand-ins of `MR`; the per-package planning values of `SW/config/values.json` are 100, 120 and 122, which sum to 342. The break-even at the mean is `(156.6 - 1 - 116 - 4 - 1) / 14 = 34.6 / 14 = 2.47`.)

The tightest cell is the worst case at b = 100: 134 s against 135.0 s, which is +34.0% with 1 s of slack. This is a planning case: it assumes a luna writes all 14 rows at exactly 2 s. If the timing spike shows more than 2.07 s per row, the cap of 5.4 reduces the rows instead of breaking the rule.

**Break-even at b = 100.** `135 - 1 - 100 - 4 - 1 = 29` s for the rows: 2.07 s per row at 14 rows, 2.42 s at 12 rows. Ember may take up to b + 28 = 128 s (at b = 100) before it, and not luna, sets the path.

**Fallback (REQ-32).** The 5-run luna timing spike measures c. Above 2.07 s at b = 100 the lens cap becomes `floor(29 / c)` (5.4), which is 12 at c = 2.41 (the `MR` fallback) and 11 at c = 2.5. There is no re-ask for luna. The ember re-ask runs only if `now + 30 <= 1.35 b` (7.6); at b = 100 an ember that ended at 81 s may be re-asked (81 + 30 = 111 <= 135) and still ends before luna's b + 28.

### 10.3 Other panels (the lens is adapted, not redesigned)

| Panel | Critical-path reviewer | Arithmetic | Elapsed | Cap |
|---|---|---|---|---|
| haiku + 2x luna | haiku, lens C5, C6, C8 at most 6 rows (luna about 121 s, off the path) | `6 x 4 + 4 + 2 = b + 30` | 250 s (+13.6%) at b = 220; 268 s (+12.6%) at 238 | 297.0 / 321.3 |
| sonnet + 2x luna | sonnet, lens C5, C6, C8, C2 at most 8 rows | `8 x 3 + 4 + 2 = b + 30` | 289 s (+11.6%) at b = 259; 332 s (+9.9%) at 302 | 349.7 / 407.7 |

Luna's own path on these panels is far off the cap: 14 rows x 2 + 4 + 2 = 34 s on top of about 121 s is about 155 s, against haiku's 250 s.

### 10.4 What is enforced and what is only expected

**Enforced by structure.**
- The lens row cap (at most 14, and the cost-driven value of 5.4) and the per-recipe row budget, checked by the script (REQ-26).
- The re-ask condition (REQ-27) and the absence of any luna re-ask.
- The hang guard at 1.5 x (b + expected overhead) from `t0` (9.4). A killed reviewer is scored as zero findings (intention to treat), and kills are reported per arm (REQ-30).
- `no_budget`: RL is refused on a panel whose cap is below the number of recipes in a lens.

**Only expected.** The per-row cost, the number of rows a luna really writes (11 expected), and the median elapsed. They are measured against same-day Z0 (REQ-29). The +35% rule is judged on per-package medians, not on one run, because the natural run-to-run spread of one reviewer is larger than 35% (`MR`). RL has no pre-pass on the critical path, and its expected path (b + 28) is within 1 s of Redesign 1's (b + 29) with a larger worst case (b + 34 against 1 s of slack at b = 100). Its remaining risk is compliance: the models must actually do the steps.

### 10.5 Tokens (planning, unmeasured)

Output: baseline 21.3k per package for ember + 2x luna (63.7k haiku panel, 46.3k sonnet panel); RL adds +5k to +8.5k output (+23% to +40%) on the primary panel and about +6k on the others (`MR` 3.2(g)). Input: the added text per reviewer is the shared ledger rule (80 words), the RL block (191 words), the recipes of the lens and, for the search role, the search-form line (33 words). Counted from the texts: ember 649 words, about 860 tokens; luna 1 487 words, about 650; luna 2 509 words, about 680 (at 1.33 tokens per word). This is more than the "about 300 tokens per lens, about 800 for all eight" of `MR` 3.2(a), which counts the recipes alone (ember's four recipes are 345 words, about 460 tokens). The pre-pass does not exist, so there are no model tokens outside the reviewers. The judge cost is unchanged. All figures are unmeasured.

## 11. How it generalises beyond the three study packages

### 11.1 What ties the design to the study, and what does not

Nothing in a recipe, lens, brief, regex, fixture or example comes from a study package. The recipes mention no document: they speak of "the plan", "the driving document", "criterion", "task", "constraint" and "dictated text" (`MR` 3.2(e): moving to a new plan format needs only a note on where instructions, criteria and constraints live). There is no extractor, so there is no pattern that could be tuned to a package. The mechanical protections (`MR` 3.0.3 AO-1 to AO-8 as 3.2(e) applies them):

| Rule | Mechanism in this design |
|---|---|
| AO-1 | `scaffold/lint.py` (copied) over `recipes/`, `config/`, `briefs/`, `cards/` and `fixtures/`: `uv run --frozen --project REPO python RL/scaffold/lint.py RL/recipes RL/config RL/briefs RL/cards RL/fixtures --gt-glob "<REPO>/.dev/eval-workspaces/**/ground-truth*.json"`. It fails on any 4-word sequence from a ground-truth `description` or `plan_quote` and on any forbidden name, and prints only file, line and a hash. It reads ground truth only when a person runs it. (The copied lint's default target list names `sweep/` files that do not exist in `RL`; `recipes/` and `config/` are given as explicit arguments.) |
| AO-2 | The swap test and a second-author review of each recipe, recorded in `recipes/REVIEWS.md` (reviewer, date, "domain nouns replaced by placeholders, still reads correctly, no issue-specific word"). The cards' own `swap_test` fields belong to the sibling's copies and are not written here. |
| AO-3 | Each card cites at least 2 instances outside the study packages (copied cards, copied `test_cards.py`). There are no extractors. |
| AO-4 | Not applicable (no extractors). The recipes are tested instead by the compliance spike and on the hold-out sets (`MR` 3.2(e)). |
| AO-5 | `bin/freeze.sh` hashes `recipes.json`, `recipes/rl-block.txt`, `recipes/search-form.txt`, `config/lenses.json`, the cards, the briefs and `rl/*.py` into `config/freeze.json` and prints the `git tag` command for a person to run (K5). |
| AO-6 | The recipes read nothing themselves. Ground truth is never in a sandbox (REQ-34), checked by `bin/check-sandbox-gt.sh` (a `grep -r` over every sandbox and every brief). |
| AO-7 | Leave-one-class-out ablation: DR-13. |
| AO-8 | A recipe states no expected outcome and no worked example comes from the study. A word-list test and the second-author review check it. |

### 11.2 A new class, a new target type, a new reviewer model

- **A new class.** One card `cards/C9.json` (all fields of the sibling's schema), one entry in `recipes/recipes.json` with a text of at most 120 words that ends in `Write at most N rows.`, and one placement in `config/lenses.json`. No change to `lens.py`, `render.py`, `rowcheck.py` or the launcher: the class list, the budgets and the lens contents all come from the three files (REQ-10, tested with a fixture class). The table rules of 5.2 refuse a class that is in no lens.
- **A new target type.** The block kinds of `MR` 3.0.3 (`task`, `criterion`, `constraint`, `dictated_text`, `edit_target`, `gate`) are the re-derive checklist. Recipes are target-neutral and need no change; the maintainer fills one column of the table in 11.3 and `recipes/README.md` (REQ-38).
- **A new reviewer model.** Add an entry to `config/lenses.json`. Choose the lens from the model's measured habits: (1) from existing run transcripts, the share of runs with a `Bash` search, the share that open a file the plan never names, and the median wall time; (2) a fast searching model takes the search lens `C4, C5, C6, C8` with a cap up to 14; a slow searching model takes the search lens with a small cap (haiku, 6); a model that already opens unnamed files takes the sweeps plus C2 (sonnet, 8); a model that reads whole files and rarely searches takes a reading lens; (3) run `uv run --frozen --project REPO python RL/rl/cli.py lens --validate`; (4) measure c in the timing spike; (5) re-freeze. The assignment is a hypothesis, and the per-class reach by reviewer id (section 12.2) tests it.

### 11.3 What to re-derive per target type (REQ-38; also written in `recipes/README.md`)

| Re-derive | Plan (done) | Specification | Documentation |
|---|---|---|---|
| Meaning of "edits" | the paths a task orders to be edited or created (`edit_target`) | the items under an "Affects" or "Affected" heading | the sections that the change rewrites |
| Meaning of "tests" and "gate" | files under `tests/`, `scripts/`, `docs/`, root files, and the commands of the last task | the checks that the specification's verification rows name | the commands in the document's fenced blocks, and the code they run |
| Meaning of "source" | the document on the plan's `Source:` line | the parent requirement document | the code the text describes, or the change log; recipe C2 is not applicable until a file path names it (DR-7) |
| Command dialect (recipes and the search-form line) | `grep`, `git grep`, `pytest`, `test` | the dialect of the verification rows | shell inside fenced blocks |
| Test and root-document paths | `tests`, `scripts`, `docs`, root-level files, change logs anywhere | the same, plus the parent folder | the repository paths of the documents and of the code they describe |
| Severity guidance | the card's `severity_guidance`, blocking when a builder cannot satisfy the text | blocking when a `shall` line cannot be met or checked | blocking when a reader who follows the text gets a wrong result |
| Snapshot (H3) | the plan's base commit | the base commit or a recorded working tree | the commit before the fix |
| Lens assignment | `config/lenses.json` as in 5.1 | same table; run the compliance spike on a specification fixture first | same table; recipes C2 and C8 will often answer `NONE FOUND` (row 27 of section 8) |

The fixtures for a specification and a documentation target exist (REQ-37): the copied `fixtures/specs/spec1.md` with its parent and `fixtures/docs/doc1.md`. For Recipe Ledger the REQ-37 test is that a lens renders for both, with recipe C2 present for the specification (it has a parent) and absent for the documentation target (no source), and that every other recipe is present.

### 11.4 What does not generalise without work

- Markdown only. A snapshot that is not a git repository (the sandbox script and recipe C8 use `git`).
- Targets with no tests, no gate or no parent document: the corresponding recipes answer `NONE FOUND`; the share of such rows is reported per class.
- Models that do not write the `ledger-v1` block in their final message (the compliance spike measures this) or that copy quotes inexactly (luna, 91.4%).
- Large trees: the harness has no bound on a reviewer's own search time (Redesign 1's pre-pass is killed at 15 s; a reviewer's `grep` is not). The cost per row c includes that time, so the timing spike must be run on the largest tree of the experiment (the repository itself), not only on a fixture.
- The recipes were written from defect classes of one repository and one plan pipeline (`MR` section 2). They have not been run on any model.

### 11.5 What may be claimed

C2, C4, C5, C6, C8, and C7 in its broad form recur outside the three study packages and are treated as general; C1 and C3 are claimed only in the weaker forms (`MR` section 2). That a class exists is not evidence that cheap panels miss it elsewhere. Generality is shown only by the planted-set, hold-out and documentation-arm results (gate D5). Claims are worded as REQ-45 requires: "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), and only for Redesign 1 at the high end of its range". For Recipe Ledger no class is expected to be consistent (`MR` 3.2(d): the best cell is I4 at 0.24-0.63).

## 12. What the validation experiment needs from the design

The experiment itself is `MR` section 5; its commands are in `TESTING.md` section 5. This section lists what the design provides for it.

### 12.1 Arms and run counts for this build

Arms: Z0-raw, Z0, K and RL on the primary panel; Zh and RLh (haiku panel) and Zs and RLs (sonnet panel) in Stage 2. This build has no SS arm. Stage 1: Z0, K, RL on four hold-out documents with 5 runs each is 60 panel runs, plus Z0-raw on three documents with 5 runs, 15: **75 panel runs** (225 reviewer runs). Stage 2 for Z0 and RL only: planted 36, clean twins 24, specification 10, documentation 48, haiku 24, sonnet 12: **154 panel runs**. Total **229 panel runs**, about 687 reviewer runs. `MR` 5.4 counts 95 + 231 = 326 panel runs for both redesigns together, because Z0 and K are run once. Two separate builds run them twice (75 + 75 + 154 + 154 = 458); a combined schedule saves 132 runs (DR-12).

### 12.2 Reach by stage (REQ-41), as Recipe Ledger defines the stages

| Stage | Definition for RL | Computed from |
|---|---|---|
| Extraction | not applicable (no extractor); logged as null | |
| Selection (`s`) | the reviewer wrote an accepted, within-budget ledger row whose `quote_plan` or `quote_other` covers the hold-out item's trigger text: the flattened `plan_quote` of the item contains or is contained in the quote, or their line spans lie within 3 lines (the rule of `SWD` 14.1, `FND.same_defect`) | `check/<rid>.ledger.json` and the hold-out ground truth, read by the analysis script only |
| Act | the row is a PROBLEM with both quotes and `supported` | the same |
| Merge survival | a finding linked to the row, or a promoted line, is in `merged/ledger.json` (joined by `(reviewer_id, finding id)`) | merge ledger |
| Judge credit | the blind judge credits the item (found-any and found-blocking kept apart) | `score.json` |

Every row of `stages.jsonl` also carries the class and the reviewer id, so the lens hypothesis (a class reaches best in the reviewer it was given to) is a table, not a guess. The per-class act bands to pre-register (REQ-41) default to the act ranges of `MR` 3.2(d): C1 0.10-0.30, C2 0.15-0.35, C3 0.05-0.20, C4 0.40-0.70, C5 0.20-0.45, C6 0.05-0.30, C7 0.10-0.30, C8 0.20-0.45 (the C6 band covers the two C6 rows, 0.05-0.20 and 0.10-0.30). The owner confirms them before the freeze (section 13).

### 12.3 Gates

G0 for RL is the "ledger and time" row of `MR` 5.7: `ledger_missing` at most 10% in the compliance spike, and the measured luna cost per row at or below its break-even (2.07 s at b = 100 and 14 rows, or the cap of 5.4). There is no selection gate. D1 to D7 are `MR` 5.7 as written; D7 compares RL with arm K. Outcomes follow `MR` 5.8: neither passes, keep Z0; K within 0.03 of RL means recipe wording adds nothing over plain words.

### 12.4 Spikes (they need models; none is run here)

| Spike | Runs | Measures | Sets |
|---|---|---|---|
| Timing (REQ-32) | 5 luna runs with an RL brief of the 14-row lens (luna 1) and 5 luna runs with the Z0 brief on the same document and day | `c = (median(RL run) - median(Z0 run) - 4) / mean rows written`; the 4 is the reading time of 3.2(c) | the lens cap through `lens_row_cap` (5.4) |
| Compliance (REQ-17) | 5 RL panel runs on HO-6, the sanity set that is in no decision | `ledger_missing` rate, `recipe_missing`, quote validity (`quote_plan_ok` share), format errors, `none_found` per class, rows per lens, `ran` status counts, re-ask use and acceptance | go or no-go: `ledger_missing` at most 10% |
| Harness share | Z0-raw against Z0 on HO-1 to HO-3 (the first runs of Stage 1) | the measured value that replaces +0.14 | nothing else |

### 12.5 What the analysis script adds for RL (`analysis/analyze.py`, `analysis/ran_check.py`)

All metrics of `SWD` 14.3 for the arms above, and: `ran` status counts per class and per reviewer (7.7); `none_found` share per class; `over_budget`, `recipe_missing`, `unknown_item` per arm; `classes_lost` per arm; re-ask counts and the yield with and without re-asked reviewers; rows per lens; reach per class per reviewer id; the three shares (H share Z0 minus Z0-raw; prompting share K minus Z0; redesign share RL minus Z0), never summed in one line (REQ-40); and the REQ-45 claim sentence.

## 13. Decisions to confirm, and what is not checked

### 13.1 Decisions for the owner (recommended values given)

| # | Decision | Recommended |
|---|---|---|
| 1 | The cost-driven lens row cap `floor((0.35 b - 6) / c)` instead of the fixed 12-row fallback (DR-4) | yes |
| 2 | One combined schedule for Z0, K and Z0-raw across both builds, or two separate schedules (DR-12) | combined, if both launchers write the run folders of `SWD` 2.2; otherwise separate |
| 3 | Re-ask only for ember, and no promotion from a repaired ledger (DR-8) | yes |
| 4 | Whether a documentation target may name a code file as its source so recipe C2 applies (DR-7) | no, for the first run |
| 5 | The K-arm lead-in (`briefs/k-lead.txt`, a draft; shared with the sibling, `SWD` DD-14) | approve when it is written |
| 6 | Whether to reword CB-2 for all arms (shared, `SWD` DD-7) | leave verbatim, measure the `## Ledger` headings in Z0 and K |
| 7 | The per-class act bands to pre-register (12.2) | the defaults of 12.2 |
| 8 | The model-stage leave-one-class-out ablation (96 panel runs, DR-13) | not now |
| 9 | The 5 extra Z0 luna runs in the timing spike (12.4) | yes (needed for c) |
| 10 | Concurrency: default 1 panel at a time (3 sessions); 3 panels (9 sessions) only while the sibling's schedule is idle, because the two builds share one gateway with a limit of about 10 sessions (9.5) | yes |

None of these needs an answer before `IMPLEMENTATION.md` steps 0 to 9. Items 5, 7 and 6 are needed at the freeze.

### 13.2 Not checked and unverified

- Every probability, act range, selection factor, cost per row, the 81 s of ember and the line counts: planning values (`MR`, "Not checked and unverified"). The 48 tokens per second comes from one luna run.
- The recipes, the RL block, the ledger rule and the repair prompt have never been run on any model. Whether ember, luna, haiku and sonnet write the `ledger-v1` block in their final message, with exact quotes and one row per step, is what the compliance spike measures.
- The `claude -p` JSON shape (`assistant` blocks `tool_use` with `input.command` or `input.file_path`; `user` blocks `tool_result` with string `content`) was read from one finished ember run only. Luna, haiku and sonnet transcripts may differ. That `@file` text can reach the model without a `Read` call is an assumption behind `not_a_tool_claim` (7.7) and is UNVERIFIED.
- The `ran` heuristic has not been compared with a person's reading. TESTING REQ-28 row M does that.
- None of the twelve Tier B files of the sibling existed on 2026-11-14 22:50 UTC. Whether the sibling's ledger code, clock, launcher, judge copy and analysis match this document's reading of `SWD` 9, 11 and 14 is unknown until they exist (DR-11). The check-10 difference of 7.2 is one known place where they may differ.
- The copied sibling tests were chosen by their imports (none imports `sweep`) and were not run in `RL`. Step 1 of `IMPLEMENTATION.md` runs them.
- `FND._check_finding` and `FND._blocks_after` are private functions. The copied contract test pins them.
- That unknown keys (`class`, `probe`, `src`) survive the merge (REQ-11) is read from code (`SWD` 9.3) and is not yet tested.
- The re-ask: that a fresh call with the model's own message and a repair prompt returns the same findings block and a valid ledger is untested. The 30 s allowance is `MR`'s number.
- The Z0-raw sandbox (`SWD` DD-15) approximates a checkout that no longer exists.
- That the reviewed plan equals the plan in each package (sha256) is unchecked (`MR` 5.2).
- The 0.914 squared figure comes from one audit of luna anchors. The share of format-induced demotions in this design is known only after the compliance spike.
- The break-even margins are thin: 1 s at b = 100 and 14 rows. The median over the same block decides, not a single run.
- The power of the experiment is low (`MR` 5.9). A pass is evidence, not proof.
- No model was started and no experiment was run. Every statement about results in this document is a plan. The design-time manifest of the sibling's files is a snapshot of a folder that was still changing.
- The codegraph index was used for its status only. No symbol lookup was made, so no caller or impact claim in this document rests on the graph.
