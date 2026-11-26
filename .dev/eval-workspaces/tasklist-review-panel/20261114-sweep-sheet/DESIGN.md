# Design: Redesign 1, Sweep Sheet (a script extracts typed items, cheap reviewers judge one item at a time), implementation and test specification

Grounding: index_state: error, token `graph:parse_failed` (`codegraph_status` answered "Changes since index: unknown (measurement timed out or failed)", so the index was not treated as fresh; checked_at 2026-11-14T19:26:27Z; projectPath `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel`). No codegraph lookup tool was used. Every file and line cited below was read with Read or a read-only shell command.

Status: design only. Nothing in this document is built, run or measured. No reviewer or judge session was started and no ground-truth file was opened. Every number marked "planning" comes from `MR` and is replaced by a measured value before it is used in a decision (`MR` section 5).

**Path abbreviations.**

| Name | Absolute path |
|---|---|
| `REPO` | `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel` |
| `EVAL` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only) |
| `SW` | `REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet` (this folder: the only place code, fixtures and run output are written) |
| `MR` | `REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (source of truth; "3.1" below means its section 3.1) |
| `RR` | `EVAL/tools/run-reviewer.sh` (87 lines) |
| `JJ` | `EVAL/tools/tmp-scripts/judge-one.sh` (31 lines) |
| `SPEC` | `EVAL/combos/SPEC.md` (procedure and hard limits) |
| `CR` | `EVAL/COMBO-REPORT.md` |
| `FND` | `REPO/src/superclaude/cli/review/findings.py` (findings-v1 parser) |
| `LED` | `REPO/src/superclaude/cli/review/ledger.py` (the merge's finding ledger; not the `ledger-v1` block of this design) |
| `MRG` | `REPO/src/superclaude/cli/review/merge_cmd.py` |
| `SB` | `/tmp/evalsb-sweep` (sandbox root for this design) |

**Sources read for this design.** `MR` sections 1, 2, 3.0, 3.1, 4, 5 (all subsections), 6.1, 6.3, 6.5 to 6.8 and "Not checked and unverified"; `RR` lines 1-87; `JJ` lines 1-31; `SPEC` lines 1-152; `CR` lines 1-506; `FND` lines 1-457 (`_check_finding` 90-121, `parse_block` 124-196, `flat` 272, `locate` 276-304); `MRG` lines 1-118; `LED` lines 100-220 (`merge_round`); `src/superclaude/rules/prompts/document_review_loop_prompts.md`; `20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh` and `lib/common.sh` (precedent for the sandbox and the folder layout); `20261113-collab/RESULTS-20261114.md`; one finished reviewer run (`.json` shape only).

**Contamination statement.** Two things were read that sit close to the study answers. (1) `CR` lines 401-417 print one-paragraph legends of the study's ground-truth items, because the task required reading `CR`. (2) Lines 1-44 of one study plan's `candidate.md` were read to learn the plan format (front matter, `## Task N:` headings, `Acceptance criteria:` bullets). Nothing from either is used in a rule, card, question, regex, fixture or example in this design. Every example below is invented. Section 13 turns this into a mechanical check (AO-1 lint). No `ground-truth*.json` was opened.

**How to read.** Section 1 lists the places where `MR` is silent or pulls two ways and says what this design decided. Sections 2-9 give behaviour in run order. Section 10 is failure and fallback, 11 the harness changes, 12 the time budget with numbers, 13 generality, 14 the hooks the experiment needs, 15 the open decisions and the unverified list. `TESTING.md` maps every requirement to a test. `IMPLEMENTATION.md` gives the build order.

## 1. Scope, constraints and decisions taken

### 1.1 What is built

1. A **pre-pass** (`sweep prepass`): a stdlib-only, read-only, deterministic script. It reads the candidate plan, the source document if there is one, and the pre-implementation snapshot of the repository. It extracts typed items with extractors E1-E7, keeps at most 12, attaches tool output to each, assigns them to the three reviewers over 24 slots and renders one sheet per reviewer.
2. A **post-run check** (`sweep check`): parses the `ledger-v1` block each reviewer wrote, tests the quotes, demotes unsupported rows, promotes PROBLEM rows that have no findings line, and writes telemetry (`MR` 3.0.4 to 3.0.6).
3. **Shared scaffolding** (`MR` 3.0, built first, shared with Redesign 2): the briefs with CB-1 to CB-5, the H2 anchor and claim normaliser, class cards, the AO-1 lint, the ledger parser, telemetry.
4. A **launcher** that runs arms Z0-raw, Z0, K and SS on the same sandbox and judge, with one panel clock, a hang guard and a fallback decision taken before any reviewer starts.
5. An **analysis script** (one script over the run folders, REQ-39) and an **offline gate script** (G0).

Not built here: Redesign 2 (recipes, lens table, REQ-25 to REQ-28), the optional verifier of 3.0.9, any production change under `src/`.

### 1.2 Hard constraints (from the task and from `SPEC`)

| Id | Constraint | Enforced by |
|---|---|---|
| K1 | Code, fixtures and run output live under `SW`. Sandboxes live under `SB`. Nothing is written under `src/`, `tests/`, `.claude/` or `.dev/tasks/`. | `bin/common.sh: sw_assert_writable` (same idea as the precedent's `r3_assert_writable`); test `test_paths.py` |
| K2 | Reviewer models: `muse-ember-1.0`, `gpt-6-luna`, `claude-haiku-5-5`, `claude-sonnet-5-5`. The judge is `claude-opus-5-5` and only the judge. Never Fable, never a Tier 0 model, never Qwen or glm (`SPEC` lines 35, 98 and 131). Opus is reserved for blind scoring and judging (the header comment of `SW/launch-design.sh`; IronClaude#546 in `PROGRESS-20261114.md`). | `sw_assert_model` allowlist; `test_model_allowlist.py` |
| K3 | The pre-pass reads only the candidate, the source and the snapshot (AO-6). It never opens a ground-truth file or a review output. | the pre-pass takes three explicit paths and no other root; `test_prepass_inputs.py` (a snapshot that contains a trap file named like a ground-truth file; the trap must not be read, checked with a read-hook on `open`) |
| K4 | Reviewers are read-only (`--disallowedTools Edit Write NotebookEdit`, as in `RR` line 48). Bash stays open, so the harness checks the sandbox with `git status --porcelain` before and after every run. | `bin/run-panel.sh`; `test_sandbox_clean.py` |
| K5 | No git write by this design's tools: no stage, no commit, no push. The freeze tag of REQ-33 is created by a person, with a script that only prints the command. | `bin/freeze.sh` prints; it never runs `git tag` |
| K6 | Python only through `uv run` (`uv run --frozen --project REPO python <file>`), never `python -m`. Tests: `uv run --frozen --project REPO pytest`. | every command in `TESTING.md` and `IMPLEMENTATION.md` |
| K7 | Do not name a code folder `lib/`: `.gitignore` line 13 ignores every `lib/` directory, which hid the collaboration designs' code from git until it was force-added (`PROGRESS-20261114.md`, Notes). | folder names in section 2.3 |

### 1.3 Decisions taken where `MR` is silent, ambiguous or pulls two ways

Each row is a decision of this design. Rows marked **owner** are repeated in section 15.

| Id | Where | The gap | Decision and reason |
|---|---|---|---|
| DD-1 | 3.0.2, 3.1(h) | `MR` says the brief edits go into `src/superclaude/rules/prompts/document_review_loop_prompts.md` and `RR`. The study harness does not read that file: `RR` has its own inline brief (lines 13-17). Editing a production rule file before the gates pass is a production change outside this folder. | The study copies live in `SW/briefs/`. The production edit is a listed adoption step (`IMPLEMENTATION.md` step 16), done only after the gates pass. |
| DD-2 | 3.0.5 check 2 | `quote_other` "must be a flattened substring of the source or of a printed tool line". Most plan defects in classes C1, C6 and C7 are two plan texts that disagree, so the second quote is a plan quote. As written, every such true PROBLEM row would fail the check and be demoted. | `quote_other` is accepted when it is a flattened substring of the source, the candidate, a printed tool line of that item, or a tool result in the reviewer's own run transcript (`<rid>.attempt1.json`, `user` events, `tool_result` blocks). The corpus that matched is recorded per row (`corpus: source\|candidate\|sheet\|transcript`). "One search result" in REQ-16 means a match in `sheet` or `transcript`. |
| DD-3 | 3.0.5 item 3 | "A finding is blocking only if it carries the CB-3 sentence and two quotes or one search result" can be read as applying to every blocking finding, including free-review ones. That would make SS differ from Z0 on findings the sheet never touched. | The rule applies to findings linked to a ledger row (by `probe` or by quote) and to promoted lines. Unlinked findings pass through unchanged. A switch `CHECK_SCOPE=linked\|all` exists; `all` is not used in any arm. |
| DD-4 | 3.1(a) S2, 3.0.7 | S2 says "1 to 2 items for each triggered class" and the guard rows say that one triggered class may fill all 12 and that no class may crowd out the rest. | Fair share: pass A takes the top item of every triggered class; pass B takes the second item of every class; pass C fills the rest by rank with a per-class ceiling of `ceil(12 / k)` for `k` triggered classes (`k = 1` gives 12). For `k >= 6` this is the spec's 2 per class; for `k = 1` it is the spec's one-class fill. |
| DD-5 | 3.1(a) E4, REQ-24 | E4 says "whole-tree `git grep -F`", REQ-24 says "tests, root documents and named paths, `.dev/` excluded". | One scope for every search: tracked files under `tests/`, `scripts/`, `docs/`, root-level files, change-log style files anywhere, the directories of plan-named paths, and same-basename copies ("mirrors") of plan-named files; `.dev/` and dependency folders excluded. The scope string is written into `prepass.json`. If the experiment shows a miss caused by scope, widening it is a re-freeze. |
| DD-6 | 3.1(a) S4 | `MR` has the reviewer open `{{SHEET_PATH}}`. 156 of 665 valid runs never opened `source.md` although it was shipped (ember 39%, luna 22%; `CR` line 373). A sheet file may be skipped the same way. | The sheet text is also placed in the brief (after the sheet paragraph) and the file is still written to `{{SHEET_PATH}}` for audit. The brief paragraph is the draft wording of `MR` line 465 with `{{SHEET_PATH}}` filled. Input cost is unchanged (the text enters the context either way). |
| DD-7 | 3.0.2 CB-2, REQ-05, REQ-23 | CB-2 says "including every ledger row you marked PROBLEM". Z0 and K have no ledger. | CB-2 stays verbatim in every non-raw arm (REQ-05 needs verbatim text; REQ-23 needs an empty-sheet brief equal to Z0's by hash). The dangling clause in Z0 and K is a risk, measured as the number of Z0 and K reports that contain a `## Ledger` heading. **owner**: whether to reword CB-2 for all arms before the freeze. |
| DD-8 | REQ-30, `RR` lines 61-83 | `RR` retries once and walks a model ladder. REQ-30 scores a killed or retried reviewer as zero findings. The time arithmetic in 3.1(c) has no room for a retry. | Counted runs use one attempt and `NOFALLBACK=1`. A reviewer whose single attempt fails the model-identity check, has no parseable findings block or hits the hang guard is scored zero findings and counted as `invalid`, `killed` or `error`. The same rule applies to every arm. |
| DD-9 | 3.0.5, 3.1(a) S5 and S6 | `MR` runs the check (S5) and then "H2 normaliser, then merge" (S6), but H2 also truncates anchors that the check needs for linking. | Order: S5 on the raw report with a lenient line reader, then H2, then merge. H2 is the same function in every arm. Promoted lines are built inside the limits, so H2 leaves them unchanged. |
| DD-10 | 3.1(a) S1 | The spec bounds the pre-pass by time only (kill at min(15 s, 0.10 b)). Evidence for hundreds of candidates would take longer than that. | Extractors work in two phases (`find`, `attach`). `find` is lexical and cheap. Only the top K = 8 candidates per class by lexical rank get `attach` (repo and source reads); when only one class has candidates after `find`, that class gets its top K_single = 12 instead, so a one-class sheet can hold 12 items (DD-4). The effect of 12 lookups on the S1 time budget is unmeasured; the attach work for one class is bounded at 12 lookups, and the pre-pass timing checkpoint (`IMPLEMENTATION.md` step 9) measures it. All candidates are still logged, with `dropped: pre_rank` for the rest. A deadline hit aborts the whole pre-pass (fallback), never a partial sheet, so output stays deterministic. |
| DD-11 | 3.0.3 | The card field list has no field for the findings category of a promoted line, but 3.0.5 requires "valid category". | Cards get one extra field, `promote_category` (one of the six categories). |
| DD-12 | 3.0.6 | `MR` says reviewers write `probe`; `class` is a telemetry key. | Reviewers set only `probe`. The check fills `class` from the item and `src` for promoted lines. |
| DD-13 | REQ-35 | Leave-one-class-out ablation changes "reach", which needs model runs, but the 5.4 run table has no ablation runs. | The runnable test is the offline selection ablation (extraction and selection stages). The model-stage ablation is outside the run budget of 5.4 and is listed as an optional extra with its cost. |
| DD-14 | 5.3 arm K | "One paragraph naming the eight checks in plain words" has no wording. | The paragraph is generated from the eight card `definition` fields with a fixed lead-in (`briefs/k-lead.txt`), so there is one governing source for the class wording. **owner**: approve the lead-in. |
| DD-15 | 5.3 arm Z0-raw | The old shared checkout `/tmp/evalsb/repo` no longer exists (`RESULTS-20261114.md`, "Notes and limits"). | Z0-raw's sandbox is "repository HEAD at launch, minus ground-truth files and the eval-workspace folders". Its fidelity to the old checkout is UNVERIFIED and is reported with the arm. |

## 2. Architecture and run order

### 2.1 Data flow

```
 S0  harness (no model)         bin/build-sandbox.sh  ->  SB/<doc>/repo   (base commit, no reflect, no reports: H3, H4)
                                candidate.md, source.md copied next to it
                                       |
 S1  sweep prepass (serial, no model, deterministic, killed at min(15 s, 0.10 b))
        plan.py        candidate -> typed blocks (task, criterion, constraint, dictated_text, edit_target, gate)
        extractors.py  E1..E7 find -> candidates -> top K=8 per class (12 if only one class) -> attach evidence (snapshot, source)
        select.py      quota + fair share -> at most 12 items
        assign.py      24 slots over 3 reviewers (caps by panel), item order shuffled per reviewer with the seed
        render.py      sheets/<rid>.md and .json, briefs/<rid>.txt
          |  error, kill, empty sheet  ->  Z0 briefs, run.json: fallback=true or no_trigger=true
                                       |
 S4  three reviewers in parallel, blind, one attempt each (claude -p, NOFALLBACK=1, hang guard)
        final message = ... ## Ledger / ```ledger-v1 ... ``` / ## Findings block / ```findings-v1 ... ```
                                       |
 S5  sweep check (no model; skipped with check_skipped=true on any exception)
        parse ledger-v1, test quotes, demote unsupported rows, promote PROBLEM rows with no findings line
        -> check/<rid>.checked.md, check/check.json
                                       |
 H2  scaffold/normalise.py  truncate anchor, anchor2 (200) and claim (300), validate with FND.parse_block
                                       |
 S6  superclaude review merge   (unchanged: MRG)  ->  merged-1.md, ledger.json
                                       |
 JJ  blind Opus judge (brief byte-identical to JJ)  ->  score.json
                                       |
     analysis/analyze.py  (all metrics, gates, stage rates; REQ-39)
```

Z0, K and Z0-raw run the same S0, S4, H2, S6 and JJ. They skip S1 and S5. Z0-raw also skips H1, H2, H3 and H4 and uses the original brief (section 8.1).

### 2.2 Run order, who runs it, what it writes

| Step | Actor | Reads | Writes (under `RUN/`) | On the critical path |
|---|---|---|---|---|
| S0 | `bin/build-sandbox.sh` | git object store of `REPO`, `config/packages.json` | `SB/<doc>/repo`, `SB/<doc>/sandbox.json`, `SB/cand/<doc>/{candidate.md,source.md}` | no (built once, reused) |
| S1 | `sweep/cli.py prepass` | candidate, source, `SB/<doc>/repo`, seed | `prepass/{items.json,candidates.json,assignment.json,prepass.json,prepass.log,sheets/*}` | yes |
| S2-S3 | inside `prepass` | | same folder | yes |
| brief render | `bin/run-panel.sh` calling `scaffold/briefs.py` | arm, sheets | `briefs/<rid>.txt`, `briefs/<rid>.sha256` | yes |
| S4 | `bin/run-reviewer.sh` (one per reviewer) | brief, sandbox | `reviews/<rid>.attempt1.{json,err,md,meta.json}`, `reviews/<rid>.{md,meta.json,cost.json}` | yes |
| S5 | `sweep/cli.py check` | reviews, `prepass/items.json`, candidate, source, transcripts | `check/<rid>.ledger.json`, `check/<rid>.checked.md`, `check/check.json` | yes |
| H2 | `scaffold/normalise.py` | `check/<rid>.checked.md` (SS) or `reviews/<rid>.md` (other arms) | `normalised/<rid>.md`, `normalised/h2.json` | no (excluded from the clock in every arm) |
| S6 | `superclaude review merge` | `normalised/*.md`, `resolution.json` | `merged/merged-1.md`, `merged/ledger.json` | no |
| JJ | `bin/judge-one.sh` | anonymised merged report | `scoring/<label>/{merged-anon.md,score.json,judge.json}` | no |

`run.json` (written first, updated at each step) holds: `arm`, `panel`, `doc`, `replicate`, `seed`, `block`, `sweep_version`, `registry_version`, `freeze_tag`, the sha256 of candidate, source, every brief, the flags `fallback`, `no_trigger`, `no_source`, `check_skipped`, `time_cap_exception` (always false), and `concurrent_panels_at_start`. `timing.json` holds the panel clock (section 11.4).

### 2.3 Folder layout under `SW`

```
SW/
  DESIGN.md  TESTING.md  IMPLEMENTATION.md
  ruff.toml                      extends the repo's ruff settings (same idea as the precedent's ruff.toml)
  scaffold/                      shared with Redesign 2 (MR 3.0)
    fnd.py  cards.py  lint.py  ledgerv1.py  normalise.py  briefs.py  telemetry.py
  sweep/                         Redesign 1 specific
    plan.py  formats.py  words.py  extractors.py  rank.py  select.py  assign.py  render.py  prepass.py  cli.py
  analysis/
    analyze.py  g0.py
  cards/                         C1.json .. C8.json, schema.json, README.md (REQ-38)
  briefs/                        base.txt, cb1.txt .. cb5.txt, ledger-rule.txt, sheet-block.txt, k-lead.txt
  config/                        packages.json, panels.json, values.json, prereg.json (written at freeze), freeze.json
  bin/                           common.sh, build-sandbox.sh, run-panel.sh, run-reviewer.sh, judge-one.sh, anon.sh,
                                 judge-batch.sh, make-schedule.py, run-schedule.sh, run-spike.sh, time-prepass.sh,
                                 freeze.sh, check-order.sh, check-sandbox-gt.sh, open-manual-checks.sh
  holdout-gt/                    hold-out ground truth, written by its author after the freeze; never read by the pre-pass
  fixtures/                      plans/ specs/ docs/ repos/ reports/ gt/ runs/ recall/   (TESTING.md section 2)
  tests/                         conftest.py, fakes/claude, test_*.py
  runs/  scoring/  results/      generated; not committed (raw transcripts and run folders stay out of git)
```

`scaffold/` and `sweep/` are plain packages put on `sys.path` by `tests/conftest.py` and by `sweep/cli.py` (same method as the precedent's `conftest.py`). They import `superclaude.cli.review.findings` for the real parser (`parse_block`, `flat`, `locate`) and, through one adapter file `scaffold/fnd.py`, for two private helpers: `_check_finding` (used by REQ-15 promotion) and `_blocks_after` (fence scanning). A contract test (`test_fnd_contract.py`) fails if either is renamed or changes its signature, so the coupling shows up in one place.

### 2.4 Determinism rule

The pre-pass output is a pure function of (candidate bytes, source bytes, snapshot tree, seed, `sweep_version`, `config/values.json` extractor constants). There is no clock, no network, no randomness except `random.Random(f"{seed}:{label}")`, no `os.listdir` order (every list is sorted), no absolute path inside any JSON (paths are repo-relative or `plan:L<line>`), and no dictionary order dependence (JSON written with `sort_keys=True`, `ensure_ascii=False`, trailing newline). `git grep` runs with `LC_ALL=C`. Time only enters as the kill at the process level; a killed pre-pass writes nothing that a later step reads (output goes to `prepass.tmp/` and is renamed to `prepass/` only on success).

## 3. Plan reader (`sweep/plan.py`, `sweep/formats.py`)

The reader turns a document into typed blocks, the six kinds of `MR` 3.0.3. Each block is `{kind, id, text, line_start, line_end, task, phase}`. Line numbers are 1-based lines of the candidate. Anchor quotes are always cut from the candidate text, never rebuilt, so they stay exact quotes.

`formats.py` is data: one dictionary per document format (`plan`, `spec`, `doc`) listing the patterns that recognise each kind. Adding a format is adding one dictionary (REQ-37, REQ-38); no extractor changes.

| Kind | Format `plan` (the workflow-plan format of this repository: front matter with `schema: workflow-plan/...`, a `Source:` line, a `Goal:` line, `## Constraints`, `## Phase N:`, `## Task N: title`, an `Acceptance criteria:` label) | Format `spec` | Format `doc` |
|---|---|---|---|
| `task` | body of a `## Task` section before its `Acceptance criteria:` label; the `Source sections:` sentence is parsed into the task's citations | a numbered section's prose | a section's prose |
| `criterion` | bullets after `Acceptance criteria:` until the next heading; the `Goal:` line (kind `goal`, treated as a criterion) | lines containing `shall`, `must`, `should` | sentences containing a set word (E1) and fenced command blocks (E2) |
| `constraint` | top-level bullets under `## Constraints` | lines that bind other lines ("applies to every ...") | none |
| `dictated_text` | blockquotes, fenced blocks and quoted spans of 25 or more characters in a sentence with a dictation verb (write, state, say, wording, verbatim, exact, must contain) | fenced blocks and lines under "Example" or "Message format" | fenced text blocks in a how-to |
| `edit_target` | path-like tokens (a `/` and an extension, or a trailing `/`) in a task sentence with an edit verb (edit, update, modify, change, rewrite, rename, delete, remove, replace, extend, create); `creates: true` for create/add-new verbs | items under "Affects" or "Affected" | none |
| `gate` | the last task's criteria when its title or body has run, check, verify or sync; a section named Gate or Final checks; any criterion bullet that holds a `pytest` or `make` command | a "Verification" section | none |

The reader never fails on a document it does not understand: unknown structure yields fewer blocks, and the run is logged as `blocks: 0` (an empty sheet, section 10). It does fail (raises) on unreadable bytes, which is a pre-pass error and so a fallback.

## 4. Extractors E1-E7 (`sweep/extractors.py`)

Flat code, one pair of functions per extractor, registered in one table `EXTRACTORS = {"E1": (find_e1, attach_e1), ...}`. No class hierarchy, no adapter layer (`MR` 3.0.3). The word lists live in `sweep/words.py`, the rank weights in `sweep/rank.py`; both are frozen with the extractors (AO-5).

### 4.1 Contract shared by all extractors

```
find_eN(doc: Doc, ctx: Ctx) -> list[Candidate]      lexical only; no repo access; cheap
attach_eN(cands: list[Candidate], ctx: Ctx) -> None  adds evidence from the snapshot or the source; never raises on a missing file
```

`Ctx` holds the parsed candidate, the parsed source (or `None`), the snapshot root (or `None`), the search scope (DD-5), the seed and the constants. `Candidate`:

| Field | Meaning | Limit |
|---|---|---|
| `extractor` | `E1` .. `E7` | |
| `class` | `C1` .. `C8` | one class |
| `kind` | sub-kind inside the extractor (`E1`: `completeness` or `universal`; `E2`: `pattern` or `selector`; and so on) | |
| `anchor_text` | the trigger text, an exact quote from the candidate; if the sentence is longer than 200 characters, its first 200 characters (a prefix of an exact quote is an exact quote) | 12 to 200 characters |
| `location` | `{task, line_start, line_end}` | |
| `evidence` | list of `{path, line, text}`; `path` is a repo-relative path, `source`, or `plan`; `text` is cut to 160 characters; may be empty | at most 5 entries |
| `features` | the named numbers the rank function used | |
| `pre_priority` | rank from `find` only (DD-10) | 0-100 |
| `priority` | final rank (`pre_priority` plus the evidence terms) | 0-100 |
| `route` | `search` or `read`, copied from the class card | |
| `status` | `selected`, `dropped:pre_rank`, `dropped:quota`, `dropped:ceiling`, `dropped:cap12`, `no_evidence_slot` | set by `select.py` |

Evidence entries are facts about text: a count, a match result, a quoted line. No extractor writes a claim, a severity or the word "defect" (`MR` 3.1: "the script never writes a claim").

**Repository search helper** (`sweep/extractors.py: search(ctx, patterns, scope)`): one `git -C <snapshot> grep -n -I -F --no-color -f <patterns file> -- <pathspecs>` call per extractor, with `LC_ALL=C`, at most 3 hits per file and the first 5,000 output lines read. The matched pattern of each line is found by flat substring tests in Python (not by `git grep -o`), so the result is the same on every run. The scope is DD-5. If the snapshot is not a git repository, the helper raises, which is a pre-pass error and so a fallback.

**Instances (AO-3).** Each extractor is justified by the recorded instances outside the study packages that `MR` section 2 counts: C1 3 documents, C2 6 plans, C4 9 documents, C5 9 documents, C6 12 documents, C7 5 plans in the broad form, C8 6 documents. The citations (`BR/enrichment/investigation-generality.md`, sections 2 and 5) are copied into each card's `instances` field in `IMPLEMENTATION.md` step 3; that file was not read for this design. E6 (class C3) is marked "plausible only" and every item it makes is labelled `experimental`.

### 4.2 E1 (classes C1 and C6): set words and their scope

| Part | Behaviour |
|---|---|
| Input blocks | `criterion` (including `goal`), `dictated_text` |
| Sentences | A block is split at sentence ends and at list bullets; a sentence needs at least 12 characters |
| Set words | Completeness (class C1): every, all, each, complete, completely, exhaustive, exhaustively, found, covers, cover, no remaining. Universal (class C6): only, never, no other, outside ... nothing. The lists are in `words.py`; each is matched case-insensitively on word boundaries |
| Named scope | For the task: the path-like and glob-like tokens in the task body before the `Acceptance criteria:` label (`instr_scope`). For the sentence: the same kind of tokens in the sentence (`sent_scope`). A scope is the empty set when no token is found (printed as `NONE`) |
| Bound type of a sentence | `closed_list` (two or more path tokens, no glob), `glob` (a token with `*`), `count` (a number followed by a noun), `none` |
| `find` output (kind `completeness`) | a C1 sentence. Features: `bound_none` (bound type `none` or `glob`), `scope_differs` (`instr_scope` and `sent_scope` both non-empty and not equal), `set_word_count`. `pre_priority = 30 + 25*bound_none + 25*scope_differs + 5*min(set_word_count-1, 2)` |
| `find` output (kind `universal`) | a C6 sentence, with the tokens it names. Features: `names_path` (it names a path, glob or test token), `set_word_count`. `pre_priority = 30 + 20*names_path + 5*min(set_word_count-1, 2)` |
| `attach` for `completeness` | evidence 1: `instruction scope: [<tokens or NONE>]` with the plan line of the instruction sentence; evidence 2: `criterion scope: [<tokens or NONE>], bound: <type>` with the plan line. Both sets are therefore side by side. `priority = pre_priority` |
| `attach` for `universal` | evidence: up to 3 scope-limiting lines elsewhere in the plan, that is, other lines that contain one of the sentence's path or test tokens and a limiter word (skip, ignore, exempt, allow-list, only, except, unless, excluding); the enforcing test the plan names (a token of the form `test_*.py` or a path under `tests/` in the same task's criteria or in the gate) and, when the file exists in the snapshot, up to 3 lines of that file that contain a limiter word plus a count of its `def test_` functions. `priority = pre_priority + 20*(at least one limiter line found) + 20*(enforcing test file found)` |
| Item text | the sentence (`anchor_text`) |
| Routing | `completeness` items follow card C1 (route `read`); `universal` items follow card C6 (route `search`) |
| Blind spot | a set word with no bound that the model must judge as bounded elsewhere; contradicting tasks are not scripted (`MR` 3.1 E1 row) |

### 4.3 E2 (class C4): a literal pattern against the text the plan orders

| Part | Behaviour |
|---|---|
| Input blocks | `criterion` bullets; `task` and `dictated_text` blocks of the same task and of earlier tasks (for the ordered strings) |
| Commands | Backticked spans whose first word is `grep`, `egrep`, `rg`, `git grep`, `pytest` or `test`. `grep`-family: the first non-option argument is the pattern, `-i` makes it case-insensitive, `-F` literal, `-E` extended, `-w` whole word. `pytest`: a `-k` expression, a `-m` marker, or a `path::name` id |
| Ordered strings | Double-quoted strings and backticked headings in task or earlier-task sentences that hold an ordering verb (add, write, create, insert, rename, name, heading, title, section, label). Each carries its plan line |
| Near-miss | An ordered string that equals the pattern after lowercasing and after replacing every hyphen, space and underscore by one space, but not literally |
| `find` output | One candidate per (command, ordered string) pair, or one per command with a selector. Features: `no_match` (the literal test failed), `near_miss`. Literal test: for a pattern with no regular-expression character, or with `-F`, a substring test (case-insensitive with `-i`); for other patterns, `re.search` after converting basic syntax to extended syntax where possible; if the pattern cannot be converted, `pattern_kind = regex_unparsed` and no match line is produced. `pre_priority = 25 + 45*no_match + 20*near_miss` |
| `attach` | Evidence: (1) `pattern '<p>' (<case-sensitive or case-insensitive>) against ordered string '<s>': MATCH or NO MATCH`, with the plan line of the ordered string; (2) when `near_miss`: `after lowercasing and collapsing hyphens, spaces and underscores: MATCH`; (3) for a selector with a named test file: `<n> of <m> test names in <file> match the selector` (test names read with `ast` for Python files, by `def test_` regex otherwise); (4) information only: `base checkout: git grep -c -F -e '<p>' -- <named path>` and its count. Item `priority = pre_priority + 5` when a selector matches 0 of `m` |
| Item text | the criterion bullet (`anchor_text`) |
| Routing | card C4: `search` |
| Blind spot | commands with computed patterns (`MR` 3.1 E2 row); regexes that `re` and POSIX read differently |

Example of the printed tool output (invented content, not from any study package):

```
Text:  "`grep -c 'retry-policy' docs/ops.md` prints at least 1"
Tool output:
  - plan line 85: the task orders the heading "Retry policy"
  - pattern 'retry-policy' (case-sensitive) against ordered string 'Retry policy': NO MATCH
  - after lowercasing and collapsing hyphens, spaces and underscores: MATCH
  - base checkout: git grep -c -F -e 'retry-policy' -- docs/ops.md gives 0
```

### 4.4 E3 (class C8): files that refer to a file the plan edits

| Part | Behaviour |
|---|---|
| Input blocks | `edit_target` |
| `find` output | One candidate per existing edit target (existing means: present in the snapshot, `creates: false`). Features: `stem_len` (length of the file's base name without extension), `has_distinctive` (an identifier in backticks in the same sentence). `pre_priority = 40 + 10*(stem_len >= 8) + 10*has_distinctive` |
| `attach` | One batched `git grep -F -f` over the scope for every target path and every stem. Evidence: up to 5 referencing files the plan never names, tests first, each as `{path, line, text}` (first hit line); then one line `gate names: <referencing files the plan's gate names, or NONE>`. Features added: `unnamed_test_files`, `unnamed_other_files`, `stem_hits` (all files, named or not). `priority = pre_priority + 15*min(unnamed_test_files, 3) + 5*min(unnamed_other_files, 2) + 10*(gate names NONE) - 20*(stem_hits > 40)` (a stem that hits more than 40 files is too common to mean anything) |
| Item text | the sentence with the edit verb |
| Routing | card C8: `search` |
| Blind spot | dependents that refer to the file only by an indirect name (`MR` 3.1 E3 row) |

### 4.5 E4 (class C5): a count or a "no remaining" claim and the places that still carry it

| Part | Behaviour |
|---|---|
| Input blocks | `criterion`, `task`, `goal` |
| Triggers | (a) negative claims: "no remaining", "none", "zero hits", "no matches", "0 matches" next to a backticked phrase; (b) count changes: "N to M", "from N to M", "N-member", "N entries" (a number and a noun) |
| `find` output | One candidate per trigger; the phrase or the number plus noun is the search string `needle`. `pre_priority = 30 + 10*(trigger is a count change) + 10*(needle has 2 or more words or 2 or more digits)` |
| `attach` | One batched `git grep -F -f` over the scope. Evidence: hits split into plan-named files and plan-unnamed files (up to 5 unnamed hits, root-level documents and change logs first, then mirrors, then the rest), then `hits: <n> in <m> files (<k> named by the plan)`. Features added: `unnamed_root_hits`, `unnamed_hits`. `priority = pre_priority + 20*(unnamed_root_hits > 0) + 10*min(unnamed_hits, 3)`; with 0 unnamed hits the item stays a low-rank candidate and is almost always dropped |
| Item text | the sentence containing the trigger |
| Routing | card C5: `search` |
| Blind spot | stale claims that use different wording than the plan (`MR` 3.1 E4 row) |

### 4.6 E5 (class C2): source rules whose identifiers no citing task carries

Runs only when a source file exists (INV-013); otherwise it returns nothing and the run records `no_source` (class C2 is then not applicable).

| Part | Behaviour |
|---|---|
| Input | the candidate's tasks with their citations (the `Source sections:` sentence: section numbers such as `2.3`, decision ids such as `Q4`, and `§` or `section` references); the source document split at its headings |
| Rule sentences | In each cited source section: sentences with a modal or universal verb (must, shall, never, always, only, every, each) or a backticked identifier next to a report, return, halt, set or write verb |
| `find` output | For each task and each rule sentence of a section the task cites: `ids` = backticked identifiers and snake_case or CamelCase tokens of the sentence; `missing` = those not found (case-sensitive, flattened) in the task's body and criteria. A candidate exists when `missing` is not empty. A task that cites nothing yields no candidate and is counted in `prepass.json: tasks_without_citations`. `pre_priority = 30 + 15*min(len(missing), 4)` |
| `attach` | Evidence: the source rule sentence (`source`, line), `missing identifiers: <list>`, and the first 160 characters of the citing task's first sentence. `priority = pre_priority` |
| Item text | the task's first sentence is the `anchor_text` (an exact quote of the candidate); the source rule is in the evidence |
| Routing | card C2: `read` |
| Blind spot | rules carried in words and not in identifiers; high identifier overlap (`MR` 3.1 E5 row) |

### 4.7 E6 (class C3, experimental): a value that is read and never written

| Part | Behaviour |
|---|---|
| Input blocks | `task`, `criterion`, `constraint` |
| Read position | a backticked literal in a sentence with "keys on", "when", "==", "is read", "returns for", "depends on" |
| Write position | the same literal in a sentence with "sets", "=", "gives", "writes", "assigns", "produces", "returns" (without "for") |
| `find` output | a candidate per literal with at least one read occurrence and no write occurrence anywhere in the candidate. `pre_priority = 20 + 5*min(read_count, 3)` |
| `attach` | Evidence: the read-position quote and `write-position occurrences of '<literal>': 0`. `priority = pre_priority` |
| Selection | at most 1 item (the lowest-trust extractor), always labelled `experimental` in the sheet and the log. This sits inside the "1 to 2 per class" quota |
| Routing | card C3: `read` |
| Blind spot | high false-positive rate, low trust, weak class support (`MR` section 2) |

### 4.8 E7 (class C7): clauses of a constraint that dictated text leaves out

| Part | Behaviour |
|---|---|
| Input blocks | `constraint` and `dictated_text` |
| Clauses | A constraint is split at semicolons, " and " and commas, keeping clauses of 4 or more words |
| Distinctive tokens | Words of 4 or more characters that are not in the stop list (`words.py`) and appear in one clause of the constraint and in no other clause of it |
| `find` output | A candidate for each pair (constraint, dictated block) where the block shares 2 or more distinctive tokens with one clause and none with another clause of the same constraint. `pre_priority = 30 + 15*(clauses with zero overlap, at most 2) + 10*(shared tokens >= 2)` |
| `attach` | Evidence: one entry per clause, at most 5: `clause <i>: '<first 100 characters>' - tokens found in the block: <list or none>`. This is the clause-by-text grid of `MR` for the highest-overlap constraint. `priority = pre_priority` |
| Item text | the dictated block's first sentence |
| Routing | card C7: `read` |
| Blind spot | clauses with no distinctive token; only the narrow one-clause form is visible (`MR` 3.1 E7 row) |

## 5. Selection and rank (`sweep/select.py`, `sweep/rank.py`)

### 5.1 Steps

1. Run `find` for every extractor. Group the candidates by class.
2. Keep the top K = 8 candidates of each class by `pre_priority` (ties: earlier plan line, then `sha256(seed + anchor_text)`). If only one class has any candidate after `find`, keep the top K_single = 12 of that class instead, so the one-class sheet of step 4 can hold 12 items. `K` and `K_single` are in `config/values.json`. The rest are logged with `status: dropped:pre_rank` and get no evidence (DD-10). The effect of 12 lookups on the S1 time budget is unmeasured; the one-class attach work is bounded at 12 lookups.
3. Run `attach` for the kept candidates. This sets `priority`.
4. Select at most 12 items (DD-4). Let `k` be the number of classes that still have a candidate with evidence computed.
   - Pass A: the highest-`priority` candidate of every such class, in the class order C4, C8, C5, C2, C1, C6, C7, C3 (a fixed order, so ties between classes never depend on a clock).
   - Pass B: the second candidate of every class, in the same order, while slots remain.
   - Pass C: the rest of the 12 slots by descending `priority`, with a ceiling of `ceil(12 / k)` items per class (for `k = 1` the ceiling is 12, and the sheet reaches 12 when that class is the only one with candidates, because step 2 attached its top 12).
   - Class C3 never exceeds 1 item (E6 is experimental).
5. Write all candidates, selected or not, to `candidates.json` with `status` and, for dropped ones, the reason. Write the selected ones to `items.json` as `S1`, `S2`, ... in descending `priority` (ties as in step 2). The seed is recorded in `prepass.json` and in `candidates.json`.

If no extractor yields a candidate, the sheet is empty (section 10). If only one class triggers, the fill is from that class alone, up to 12 (1 when that class is C3), `attach` having run on its top 12 (step 2), and the reach for that run is reported for that class only (guard rows of `MR` 3.0.7).

### 5.2 The rank function

The numbers are in the extractor sections above and are collected in `sweep/rank.py` as one table. They are planning values chosen from the structure of each signal (a failed literal match is stronger than a set word; an unnamed referencing test is stronger than a stem hit). They are not tuned on any study package. They are frozen with the extractors (AO-5), published in `prepass.json: rank_table_sha256`, and checked only by gate G0 (section 14.1). If G0 fails, the rank function is revised before the freeze, never after.

| Extractor and signal | Weight |
|---|---|
| E1 completeness: base 30, `bound_none` +25, `scope_differs` +25, extra set words up to +10 | 30-90 |
| E1 universal: base 30, names a path or test +20, up to +10 for extra set words, +20 if at least one limiter line is found, +20 if an enforcing test file is found | 30-100 |
| E2: base 25, literal `NO MATCH` +45, near-miss +20, selector with zero matches +5 | 25-95 |
| E3: base 40, long stem +10, distinctive identifier +10, up to +45 for unnamed test files, up to +10 for other files, +10 if the gate names none, -20 for a stem that hits more than 40 files | 20-100 |
| E4: base 30, count change +10, multi-word needle +10, unnamed root-level hit +20, up to +30 for unnamed hits | 30-100 |
| E5: base 30, +15 per missing identifier (at most 4) | 45-90 |
| E6: base 20, +5 per read occurrence (at most 3) | 25-35 |
| E7: base 30, +15 per zero-overlap clause (at most 2), +10 for two or more shared tokens (a candidate exists only with at least one of each, so the range starts at 55) | 55-70 |

All values are clamped to 0-100. Because the classes' ranges differ, cross-class order in pass C is not meaningful by itself; that is why passes A and B guarantee class presence first.

## 6. Sheet format (`sweep/render.py`)

### 6.1 Item (the JSON in `items.json`)

| Field | Content | Limit |
|---|---|---|
| `item_id` | `S<n>` | unique in the run |
| `class` | C1-C8 | one class |
| `anchor_text` | the trigger text, an exact quote of the candidate | at most 200 characters |
| `location` | `{task: "Task 4" or "Constraints" or "Goal", line_start, line_end}` | |
| `evidence` | list of `{path, line, text}` | at most 5 entries, `text` at most 160 characters; may be empty |
| `question` | the printed question of the class card, filled | a string |
| `priority` | the rank value | 0-100 |
| `experimental` | true for E6 items | boolean |
| `replicas` | 1 or 2 (section 7) | |

`items.json` also lists, per item, the `extractor` and `kind`. The reviewer sheet does not show `priority`, `extractor` or `kind`: a reviewer should not read the rank as a verdict.

### 6.2 Questions

The question text is the printed question of `MR` 3.1(a) (eight questions, one per class), stored in `cards/C<n>.json: question_template`. Only the C3 question has a placeholder (`«value»`), filled from the item's `anchor_text` literal. No question states an expected outcome (AO-8), and each passes the swap test (AO-2).

### 6.3 Sheet text, one per reviewer

`sheets/<rid>.md` holds, in the shuffled order of that reviewer (section 7.3), for each assigned item:

```
### S3   (class C4)
Where: Task 4, acceptance criterion 2 (plan lines 87-87)
Text:  "<anchor_text>"
Tool output:
  - [plan L85] ...
  - [tests/test_x.py:12] ...
Question: <question>
Reply with one line in the ledger-v1 block: item S3, verdict OK, PROBLEM or UNSURE.
```

Rules: the class label is a plain id (C4), never a name or a hint of the outcome. An item with no evidence prints `Tool output: none`. An `experimental` item prints `Note: this item comes from a low-trust extractor; most such items are fine.` The sheet starts with one line: `Items assigned to you: S3, S7, ...` in the same order. A sheet may not exceed 16,000 characters (about 4,000 tokens, the worst case of 9 items of 1,600 characters); if it would, `render.py` removes evidence entries from the lowest-priority items, last entry first, until it fits, and records `sheet_trimmed: true`.

`sheets/<rid>.json` holds the same items with all fields for the audit and the analysis.

### 6.4 Where the sheet goes

The brief (section 8) contains the sheet paragraph with `{{SHEET_PATH}}` filled with the absolute path of `sheets/<rid>.md`, followed by a heading `## SWEEP SHEET ITEMS` and the sheet text itself (DD-6). The file is for audit and for a reviewer that wants to re-read it.

## 7. Item-to-reviewer assignment (`sweep/assign.py`)

### 7.1 Inputs and caps

Inputs: the selected items (at most 12), the panel, the set of available reviewers, the seed. Reviewer roles: `S` the search reviewer (ember, haiku or sonnet) and `L1`, `L2` the two lunas. Caps come from `config/panels.json` and sum to 24 (`MR` 3.1(a) S3).

| Panel | S cap | L1 cap | L2 cap | Sum | Items the S reviewer may take |
|---|---|---|---|---|---|
| primary (ember + 2x luna) | 8 | 8 | 8 | 24 | any |
| haiku (haiku + 2x luna) | 6 | 9 | 9 | 24 | only items with attached tool output of classes C4, C5, C8 (extractors E2, E3, E4) |
| sonnet (sonnet + 2x luna) | 6 | 9 | 9 | 24 | any |

Reviewer ids carry no meaning beyond labels: ember `t2b-1`, haiku `t2-1`, sonnet `t1b-1`, lunas `t4-1` and `t3-1` (the ids of batches 8 and 9). `resolution.json` for the merge maps each id to its model.

### 7.2 Algorithm (deterministic)

1. **Replica target.** An item with an empty `evidence` list has `replicas = 1`; every other item has 2. If fewer than three reviewers are available, every item has `replicas = 1` and the caps are not raised.
2. **Pass 1: one reviewer per item.** In descending `priority`: a `search`-route item goes to `S` if `S` is allowed and under its cap, otherwise to the lighter luna; a `read`-route item goes to the lighter luna (ties: `L1`).
3. **Pass 2: the second reviewer.** In descending `priority`, for items with `replicas = 2`: a `search`-route item goes to the lighter luna; a `read`-route item goes to the other luna, and to `S` when the other luna is at its cap and `S` is allowed and under its cap. A second reviewer never equals the first. If no reviewer can take it, the item keeps one reviewer and is listed in `assignment.json: replica_dropped` (the lowest-priority items lose their second replica first, because pass 2 runs in priority order).
4. Every item keeps at least one reviewer. If an item cannot get one (all caps full), it is dropped from the sheet with `status: dropped:cap_slots` and logged.

Worked check for the primary panel with 12 items, 7 of route `search` and 5 of route `read`, all with evidence: pass 1 puts the 7 search items on `S` and spreads the 5 read items over the lunas (3 and 2); pass 2 puts the search items' second replicas on the lighter luna, then the read items' second replicas on the other luna, and the one that no longer fits at the luna's cap of 8 goes to `S` (7 to 8). The end loads are 8, 8, 8 and the sum is 24. The test (`test_assign.py`) asserts the invariants rather than this trace: no load above its cap, the sum equals the number of replica slots, no item has the same reviewer twice, every item has at least one reviewer.

### 7.3 Order and failure

- **Order.** Each reviewer's items are shuffled with `random.Random(f"{seed}:{rid}")` before they are printed (order-bias control, `MR` S3). The shuffled order and the seed are in `assignment.json`.
- **Reviewer fails after launch.** The survivors keep exactly the items they were given; their load never grows (REQ-20). Items that lost a replica are recorded as `lost_replica`; the run is flagged and still counted (intention to treat). Their `ledger-v1` lines are expected only from reviewers that finished.
- **Reviewer unavailable before launch** (a model probe fails): the harness re-runs `assign` with the available set, which gives `replicas = 1` for every item, before any reviewer starts.

## 8. The brief change (`scaffold/briefs.py`, `briefs/`)

### 8.1 Arms and what each brief is made of

A brief is built by joining text parts in a fixed order. Parts are files under `briefs/`; no part is written inside code, so the sha256 of every part can be frozen (AO-5).

| Part | File | Source |
|---|---|---|
| Base brief | `base.txt` | `RR` lines 13-17 byte for byte, with `$CAND_SB` and `$SHA` as placeholders (the category list already says `unpassable-check`, `RR` line 17) |
| CB-1 (only when a source file exists) | `cb1.txt` | `MR` line 205, with `{{SOURCE_ABS}}` filled |
| CB-2, CB-3, CB-4, CB-5 | `cb2.txt` .. `cb5.txt` | `MR` lines 209, 213, 217, 221, verbatim |
| K paragraph | generated: `k-lead.txt` + the eight card `definition` fields | DD-14 |
| Ledger rule | `ledger-rule.txt` | `MR` line 291, verbatim |
| Sheet block | `sheet-block.txt` | `MR` line 465, with `{{SHEET_PATH}}` filled; followed by the heading `## SWEEP SHEET ITEMS` and the sheet text (DD-6) |

| Arm | Parts, in order |
|---|---|
| Z0-raw | base |
| Z0 | base, CB-1 (if source), CB-2, CB-3, CB-4, CB-5 |
| K | Z0 parts, K paragraph |
| SS | Z0 parts, ledger rule, sheet block and items. With an empty sheet or `fallback=true`: Z0 parts only |
| RL (not built here) | reserved |

Consequences, each tested: an empty-sheet SS brief is byte-equal to the Z0 brief of the same document (REQ-23, compared by sha256); CB-1 is absent and `no_source` is logged when there is no source file (REQ-01); no part contains the string `src/superclaude/` (REQ-09); the quoted parts equal the quoted blocks of `MR` (REQ-05); the first line `/sc:spec-panel @<candidate> --mode critique` of `RR` line 13 is kept in every arm.

The text of the ledger rule and the sheet block is draft wording that has not been run on any model (`MR`, "Not checked and unverified"). The compliance spike (section 14.2) is the first run of it.

### 8.2 What the reviewer is told, in one picture

The reviewer's final message must look like this. The headings and info strings are exactly those of `MR` 3.0.4. Everything before `## Ledger` is free text.

````
<report text, including the grading sentences>

## Ledger

```ledger-v1
{"item":"S3","verdict":"PROBLEM","quote_plan":"<12-200 chars from the plan>","quote_other":"<exact text>","problem":"<one sentence, at most 300 chars>","ran":"<at most 15 words>"}
{"item":"S7","verdict":"OK","quote_plan":"","quote_other":"","problem":"","ran":"compared both scopes"}
```

## Findings block

```findings-v1
{"id":"F1","severity":"MAJOR","blocking":false,"category":"other","anchor":"<12-200 chars>","refs":[],"claim":"<one sentence>","probe":"S3"}
```

verdict: FAIL
````

## 9. Ledger, checks and promotion (`scaffold/ledgerv1.py`, `sweep/cli.py check`)

### 9.1 Reading the final message

`RR` keeps only the final result message as the report (`RR` line 50), and checks only that a line starts with the `findings-v1` fence opener (`RR` line 57). The check therefore reads the report file `reviews/<rid>.md` with a real parser:

1. Find the heading `## Ledger` (regex `^#{1,6}\s+Ledger\s*$`, case-insensitive) and the heading `## Findings block` (the same regex `FND` uses). The ledger heading must come first and no other heading may sit between them ("directly above", REQ-13).
2. In the text between the two headings, find fenced blocks with info string `ledger-v1` (`FND._blocks_after`, through the adapter). Zero blocks, two blocks, an unclosed block or a block outside that span means `ledger_missing` for this reviewer.
3. Parse each non-empty line as JSON. A line that is not valid JSON, is not an object, or lacks `item` or `verdict` is a **format error** and is counted (`format_errors`, with the line number). It is never skipped silently.
4. Accepted leniency, counted separately (`normalised_verdict`): the verdict is read case-insensitively and trimmed.
5. Limits: `quote_plan` is empty or 12 to 200 flattened characters; `problem` at most 300; `ran` at most 15 words; `item` must be one of the items assigned to this reviewer, otherwise `unknown_item`. A row that breaks a limit is kept for coverage and flagged `limits_violated`; it cannot be promoted.
6. A second line for the same item is `dup_line`; the first wins.

Earlier assistant messages in the transcript are read for the `transcript` corpus (DD-2) and for diagnosis only. They never feed promotion and never change `ledger_missing` (`MR` 3.0.4).

### 9.2 Checks (per reviewer, per row)

| # | Check | Result recorded |
|---|---|---|
| 1 | Every item assigned to the reviewer has a ledger line | `missing_line: [S5, ...]`. No re-ask (time). |
| 2 | `quote_plan` is a flattened substring of the candidate (`FND.locate` is non-empty) | `quote_plan_ok` |
| 3 | `quote_other` is a flattened substring of the source, the candidate, a printed tool line of this item, or a tool result of the reviewer's own transcript | `quote_other_ok`, `corpus` |
| 4 | Row support. `quotes_supported`: `quote_plan_ok` and `quote_other_ok` and the two flattened quotes differ. `search_supported`: `quote_plan_ok` and `quote_other_ok` and `corpus` is `sheet` or `transcript` | `supported = quotes_supported or search_supported` |

All substring tests use `FND.flat` and `FND.locate`, so a quote that wraps a plan line still matches (REQ-14).

### 9.3 Linking, demotion, promotion

**Link.** A findings line is linked to a ledger row when its `probe` equals the row's `item`, or when the row's flattened `quote_plan` lies inside the finding's flattened `anchor` (`MR` 3.0.5, "Linking"). A `probe` that names an item not assigned to this reviewer is `probe_unknown` and does not link.

**Demotion** (applies to linked findings only, DD-3). A linked finding with `blocking: true` is set to `blocking: false` (severity stays; a `CRITICAL` or `MAJOR` non-blocking line is valid) when any of these holds. Each cause is counted separately, because format-induced demotions must be reported (INV-007):

| Cause | Condition |
|---|---|
| `row_unsupported` | the linked row is `PROBLEM` and `supported` is false |
| `row_unsure` | the linked row is `UNSURE` |
| `no_cb3` | the finding does not carry the CB-3 sentence (below) |
| `row_missing` | the linked row failed to parse (a format error line) |

A linked finding whose row is `OK` is left alone and counted as `ok_but_finding`.

**The CB-3 sentence.** The text `An implementer who follows the stated text as written builds` (compared after flattening, case-insensitive) must appear in the finding's `claim`, or in the report text within 12 lines of a line that mentions the finding's id as a whole word, before the findings block.

**Promotion** (a `PROBLEM` row with no linked findings line; `UNSURE` and `OK` rows are never promoted). The check never writes a claim of its own:

| Field | Value |
|---|---|
| `id` | `P` + the item id (for example `PS3`); a numeric suffix is added if the id is already used in the block |
| `severity`, `blocking` | `MINOR`, `false` |
| `category` | the class card's `promote_category` (DD-11) |
| `anchor` | the row's `quote_plan` (a row with an empty `quote_plan` is not promoted) |
| `claim` | the row's `problem`, copied unchanged |
| `refs` | `[]` |
| telemetry | `"class": "<C1-C8>"`, `"probe": "<item id>"`, `"src": "ledger"` |

The line is built as an object and validated with `_check_finding` (REQ-15) against the ids already in the block; it is inserted as the last line inside the one existing `findings-v1` block, before the closing fence; it is never written as a second block. On any failure the row is logged in `check.json: promotion_failures` and skipped. Promoted findings are counted apart from reviewer findings in every metric.

**Telemetry on reviewer lines.** For every linked line the check adds `"class"` (from the item) and keeps the reviewer's `probe`. `FND` does not reject unknown keys (`_check_finding`, lines 90-121, has no key whitelist), and `LED.merge_round` copies only fixed fields into a ledger row (`row` at lines 184-202; members carry only round, reviewer id, finding id and blocking). So the keys never reach `merged-1.md` or `merged/ledger.json`. Telemetry is therefore read from `check/<rid>.checked.md` and joined to the merged ledger through `(reviewer_id, finding id)`. REQ-11 is a test with the real merge.

**Block repair is out of scope.** If the `findings-v1` block is missing, unclosed or duplicated, the check changes nothing for that reviewer (it cannot insert a promoted line) and records `block_unusable`. The merge then handles the reviewer as it does today (`LED.merge_round` skips a reviewer with an invalid block for clearing but keeps its parsable lines).

### 9.4 Outputs

`check/<rid>.ledger.json`: the parsed rows with every check result. `check/<rid>.checked.md`: the report with demotions and promotions applied (the raw `reviews/<rid>.md` is never edited). `check/check.json`:

```
{ "ledger_missing": [rid, ...], "format_errors": n, "normalised_verdict": n, "dup_line": n, "unknown_item": n,
  "probe_unknown": n, "missing_line": {rid: [item, ...]}, "rows": {"OK": n, "PROBLEM": n, "UNSURE": n},
  "demoted": {"row_unsupported": n, "row_unsure": n, "no_cb3": n, "row_missing": n},
  "format_induced_demotions": n,   // demotions whose row failed only on a quote-match or a parse, not on content
  "promoted": n, "promotion_failures": [...], "ok_but_finding": n, "block_unusable": [rid, ...] }
```

`format_induced_demotions` counts demotions where the row's `problem` text is non-empty and both quotes are present but a quote test failed, or a line failed to parse. It is the number that tells whether the 0.914 squared figure of `MR` 3.0.5 item 4 shows up in practice.

### 9.5 Flags

| Flag | Meaning | Written to |
|---|---|---|
| `fallback=true` | the Z0 brief was run because the pre-pass or the render failed | `run.json` |
| `no_trigger=true` | the sheet was empty; the brief equals Z0's | `run.json` |
| `no_source=true` | no source file; CB-1 and E5 not applied | `run.json` |
| `check_skipped=true` | the post-run check raised; demotion and promotion skipped for the whole run and the findings block merged as written | `run.json`, `check/error.log` |
| `ledger_missing` | per reviewer, in section 9.1 | `check.json` |

## 10. Failure and fallback behaviour

The rule behind every row: the decision to fall back is taken before any reviewer starts, so a running reviewer's brief is never changed (INV-012). A failure after the reviewers have finished never discards a reviewer's own findings.

| # | Condition | Detected by | Action | Recorded | Counted |
|---|---|---|---|---|---|
| 1 | The pre-pass raises (parser, extractor, search helper, render) | `sweep prepass` exits non-zero; `prepass.error.json` names the extractor and exception class | Z0 briefs, run continues | `fallback=true`, reason | the run stays in arm SS (intention to treat); fallback count per arm |
| 2 | The pre-pass runs past `min(15 s, 0.10 b)` | `timeout` in `bin/run-panel.sh` kills the process group; `prepass.tmp/` is removed | same as row 1 | `fallback=true`, `reason: kill` | same |
| 3 | The sheet is empty (no extractor fired, or no candidate with evidence) | `items.json` holds no item | Z0 briefs; no ledger rule | `no_trigger=true` | reported as a no-trigger run; excluded from "per-class reach" but kept in D1 to D6 |
| 4 | One class only triggers, or one class would crowd | `candidates.json`, `classes_triggered` | DD-4 fill; fair-share ceiling | `classes_triggered` | reach reported for that class only; a crowding case with `k >= 2` and one class above `ceil(12/k)` is a test failure (REQ-19) |
| 5 | No source file | `packages.json: source: null` | CB-1 not rendered; E5 returns nothing | `no_source=true` | class C2 reported as not applicable for that document |
| 6 | No base commit (a spec or a document that was never committed) | `packages.json: base: "tree:<dir>"` | the sandbox is built from that recorded working tree | `sandbox.json: kind: tree, tree hash` | REQ-03 |
| 7 | The sandbox is missing, dirty or contains a masked path | `build-sandbox.sh` exit 2 (`E_SANDBOX_DIRTY`), `git status --porcelain` before the run | the run is refused, not run in a fallback: the sandbox is the experiment's floor | log line | not counted; must be rebuilt |
| 8 | A reviewer hits the hang guard, fails the model-identity check, returns an API error, or has no usable findings block after H2 | `bin/run-reviewer.sh` (single attempt, DD-8) | the reviewer is dropped from the merge and scored zero findings; survivors keep their items | `killed`, `invalid` or `error` in `reviews/<rid>.meta.json` | per arm (REQ-30); `lost_replica` items listed |
| 9 | Only two reviewers left before launch | model probe fails | `assign` re-run with `replicas = 1` | `reviewers: 2` | flagged and counted |
| 10 | A reviewer wrote no parseable `ledger-v1` block directly above the findings block | `sweep check` | no demotion and no promotion for that reviewer; its findings block merged as written | `ledger_missing` | rate per arm, must be at most 10% in the compliance spike (REQ-17) |
| 11 | `sweep check` raises | exception caught in `bin/run-panel.sh` | S5 skipped for the whole run; raw reports go to H2 and the merge | `check_skipped=true`, `check/error.log` | per arm; different from `fallback` |
| 12 | A promoted line fails `_check_finding` (long id, short anchor, duplicate id) | `scaffold/ledgerv1.py` | the line is not inserted | `check.json: promotion_failures` | counted apart from reviewer findings |
| 13 | A quote copied inexactly (a luna anchor is verbatim 91.4% of the time, `CR` line 294) | check 2 or 3 fails on a row whose text is otherwise complete | the linked finding is demoted to non-blocking, never deleted | `format_induced_demotions` | reported with every result (INV-007) |
| 14 | Tool lines make wrong blockers more likely | CB-3, `UNSURE` is non-blocking, a blocker needs `supported` | the demotion rules of 9.3 | `demoted.*` | gate D4 |
| 15 | Item attention displaces free review | CB-5 (half the time for free review) | none at run time | non-probe findings per run | gate D6 (blocking) |
| 16 | The model answers OK to every item | none at run time | none | OK-rate on planted items | gate D2 and arm K (D7) |
| 17 | The selection misses the trigger and repeats on every run of that document | none at run time | none | `stages.jsonl` (extraction and selection logged apart from act) | gate G0 before any model arm |
| 18 | An extractor misses a sentence shape, or over-extracts | none at run time | the free review (CB-5) still runs | `candidates.json` shows everything found | REQ-21 recall and precision; a new shape is one new extractor and a re-freeze |
| 19 | The sheet or the sandbox leaks ground truth | `test_prepass_inputs.py`, `bin/build-sandbox.sh` check, REQ-34 grep | the run is refused | log line | study invalid if seen |
| 20 | The judge returns an API error but leaves a score file | `analysis/analyze.py --audit-judges` (as in `CR` line 147: one such file looked real) | the score is invalidated and the judge re-run | audit log | REQ-43 |
| 21 | Gateway model identity bleed (a model served as another) | `observed_model` against `expected_model` in `RR` lines 51-56, kept | row 8 | `model_ok=false` | per arm |
| 22 | The sheet would exceed 16,000 characters | `render.py` | evidence entries removed from the lowest-priority items | `sheet_trimmed=true` | counted |

## 11. Harness changes (`bin/`)

### 11.1 `bin/run-reviewer.sh` against `RR`

| `RR` | What it does today | In `bin/run-reviewer.sh` |
|---|---|---|
| 6-12 | writes under `EVAL/<pkg>/reviews`; copies the candidate and `source.md` into `/tmp/evalsb/cand/<pkg>/` | writes under `RUN/reviews`; the candidate and source come from `SB/cand/<doc>/` made by `build-sandbox.sh` |
| 13-17 | inline `BRIEF` string | the brief is a file from `scaffold/briefs.py`, sent on stdin |
| 19-44, 65-83 | model fallback ladder and a second attempt | removed (DD-8). `NOFALLBACK=1` is required; one attempt |
| 48 | `cd /tmp/evalsb/repo` (a shared checkout; gone), `timeout 3000` | `cd SB/<doc>/repo`; `timeout <hang guard>` from section 11.5; same flags (`--no-session-persistence`, `--permission-mode bypassPermissions`, `--disallowedTools Edit Write NotebookEdit`) |
| 50-56 | keeps only the final result message; model-identity check | same |
| 57 | `BLOCK_OK` is a grep for the fence opener | `BLOCK_OK` is `FND.parse_block` ok after H2 on a temporary copy (REQ-13). A missing `ledger-v1` block does not make `BLOCK_OK` false (section 9.1) |
| 58, 85-87 | writes `meta.json`, `cost.json` | same, plus `hang_s`, `killed`, `prompt_sha256` |

### 11.2 H1 to H4 in this harness

| Fix | Implementation |
|---|---|
| H1 source named | CB-1 with the absolute path `SB/cand/<doc>/source.md`; rendered only if `packages.json: source` is not null |
| H2 normaliser | `scaffold/normalise.py`: for each finding line of the single block, `anchor` and `anchor2` are cut to their first 200 flattened characters and `claim` to 300; a prefix of an exact quote is an exact quote. The result is validated with `FND.parse_block`; lines that still fail are kept in `normalised/h2.json: unrepaired` and are not silently dropped. Idempotent. Used by every arm except Z0-raw |
| H3 base commit | `bin/build-sandbox.sh`, adapted from the precedent `r3-axis-flip-challenge/bin/build-sandbox.sh` lines 1-59: `git archive <base> \| tar -x`, then the removals of H4, then `git init` and one snapshot commit, then `git status --porcelain` must be empty. `config/packages.json` holds `{doc: {kind, set, base, candidate, source, masked_paths[]}}`; `base` is a commit or `tree:<dir>`. `masked_paths` are files the implementation created or changed; each must differ from, or be absent at, the base (REQ-03) |
| H4 no reports | the same script removes `.dev/reflect`, `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research`, every `artifacts/` folder, every `progress.md`, and every path that contains a document id, then checks (REQ-04) with `find` and `grep -r` for ground-truth file names, document ids and `reflect` |
| Z0-raw | `build-sandbox.sh --raw`: repository HEAD at launch with only ground-truth files and the eval-workspace folders removed (DD-15) |

### 11.3 Judge (`bin/judge-one.sh`)

A copy of `JJ` with the paths turned into variables (`EVAL`, `D`, `GT`, `CAND`); the `BRIEF` text of `JJ` lines 12-23 is kept byte for byte and a test compares its sha256 with `JJ`'s (REQ-05, REQ-43). The model stays `claude-opus-5-5` and is used only here (K2). Anonymisation follows the pattern of `EVAL/tools/tmp-scripts/anon-b11.sh` (random label, reviewer ids replaced by R1..Rn, paths redacted); that file was not read for this design, so the exact redaction rules are taken over at implementation. The judge cannot see the arm: the merged report carries no `class`, `probe` or `src` key (section 9.3). A second judge scores a seeded 15% sample; an audit of every judge output follows (section 14.3).

### 11.4 The panel clock

One clock per run (REQ-29), in `timing.json`:

| Field | Definition |
|---|---|
| `t0` | monotonic time immediately before S1 starts (SS), or before the first brief is rendered (other arms) |
| `prepass_s`, `render_s` | durations of S1 and the brief render (0 for other arms) |
| `rev_start[rid]`, `rev_end[rid]` | launch and end of each reviewer process |
| `s5_s` | duration of S5 (0 for other arms) |
| `panel_elapsed_s` | SS: end of S5 minus `t0`. Other arms: last `rev_end` minus `t0`. H2, the merge, the judge and the optional verifier (REQ-46) are outside the clock in every arm |
| `slowest_reviewer_s` | max over `rev_end - rev_start` (this is the quantity `b` is a median of, for Z0) |

Mean and median per arm per document are reported (REQ-29); gate D1 uses the medians.

### 11.5 Hang guard

`hang_s = 1.5 * (b + expected_overhead)` from `t0` (INV-008). `b` comes from `config/values.json` (planning stand-ins until the same-block Z0 medians exist: ember panel 100-122 s by document, haiku 220-238, sonnet 259-302; `MR` 3.1(c)); `expected_overhead` is 29 s for SS on the ember panel (the 8 + 1 + 19 + 1 of section 12), 37 s for haiku, 31 s for sonnet, 0 for the other arms. Each reviewer is run under `timeout <hang_s - (time already used)>`. A reviewer killed by it is recorded `killed` and scored zero findings.

### 11.6 Schedule and concurrency

`bin/make-schedule.py` writes `schedule.tsv` with one line per (stage, block, arm, document, replicate) in block-randomised order (one block per replicate; the shuffle uses a recorded seed). `bin/run-schedule.sh` runs it with at most 3 panels at once, so at most 9 reviewer sessions and at most 3 ember sessions, inside the limits of `SPEC` (10 sessions) and of the precedent (4 ember). `concurrent_panels_at_start` is logged per run. Arms of one block are compared with each other, never with a run from another day (REQ-29).

### 11.7 Merge

As in `SPEC` steps 2 and 3: a per-run `resolution.json` of `{reviewers: [{reviewer_id, model}]}` for the reviewers that finished, then

`superclaude review merge --ledger RUN/merged/ledger.json --doc SB/cand/<doc>/candidate.md --round 1 --report <rid>=RUN/normalised/<rid>.md ... --resolution RUN/resolution.json --out RUN/merged/merged-1.md`

A reviewer that was killed or invalid is simply absent from `--report`. If the merge refuses the round (no valid block in any report), the run is recorded `merge_refused` and scored zero; it is not re-run (intention to treat).

## 12. Time budget against the +35% rule

The rule (D1): per-package median elapsed of SS at most 1.35 x the per-package median of same-day Z0 in the same randomised block; 90th percentile at most 1.50 x; kills at most 10%. `b` is Z0's per-package median of the slowest reviewer. Everything below is arithmetic on planning values from `MR` 3.1(c); each value marked "planning" is replaced by a measured one (REQ-29, REQ-31, REQ-32). I re-derived every figure of `MR` 3.1(c) and they all check; nothing here changes them.

### 12.1 Cost model (planning, UNVERIFIED)

A ledger row is about 75-90 output tokens. At 48 tokens per second (one luna run: 4.9k tokens in 102 s) a row costs 1.6-1.9 s. Planning cost per item `c`: luna 2 s, haiku 4 s, sonnet 3 s, ember 0.4 s. Reading the sheet costs 3 s per reviewer. The pre-pass is 8 s expected, 1 s for selection, assignment and render, and 1 s for the post-run check (which includes Python start-up; one `uv run` start plus the `findings` import took 0.28 s when measured once on this host).

### 12.2 Critical path, primary panel (ember + 2x luna)

Luna sets the critical path: `S1 + S2-S3 + (b + 3 + n*c) + S5` with `n = 8` items and `c = 2 s`.

| Step | Seconds | Bound |
|---|---|---|
| S1 pre-pass | 8 expected | kill at `min(15 s, 0.10 b)` |
| S2-S3 selection, assignment, render | 1 | none |
| S4 luna, 8 items | `b + 3 + 8 x 2 = b + 19` | hang guard |
| S5 check | 1 | none |
| **Critical path** | **b + 29** | |
| S4 ember (off the path) | about 60 (41 baseline + 3 s sheet + 8 items x 2 s, as in `MR`; the 0.4 s per ember item of the cost model would give 47 s, so 60 is the cautious figure) | idle slack of 60-90 s |

| b | Expected `b + 29` | Increase | Pre-pass at its kill limit | Increase | Cap `1.35 b` | Margin to cap (expected / kill limit) |
|---|---|---|---|---|---|---|
| 100 | 129 | +29.0% | 10 + 1 + 119 + 1 = 131 | +31.0% | 135.0 | 6.0 s / 4.0 s |
| 122 | 151 | +23.8% | 12.2 + 1 + 141 + 1 = 155.2 | +27.2% | 164.7 | 13.7 s / 9.5 s |
| 116 (mean) | 145 | +25.0% | | | 156.6 | 11.6 s |
| 348 (three-package sum) | 435 | +25.0% | | | 469.8 | 34.8 s |

The tightest cell is 131 s against 135.0 s: pre-pass at its kill limit and `b = 100`.

### 12.3 Break-even formula

`critical path = S1 + 1 + b + 3 + n*c + 1` (pre-pass, selection and render, the luna's own time, sheet reading, `n` items at `c` seconds, the check), and the cap is `1.35 b`. So the sheet fits when `n * c <= 0.35 b - S1 - 5`. With the planning pre-pass `S1 = 8` s this is `n * c <= 0.35 b - 13`.

| b | Budget for `n*c` | `c` that 8 items may cost | pre-pass that may take (c = 2, n = 8) |
|---|---|---|---|
| 100 | 22.0 s | 2.75 s | 14 s (135 - 1 - 119 - 1) |
| 122 | 29.7 s | 3.71 s | about 21.7 s |

The fallback in `MR` (if the spike measures more than 2.75 s per item): each luna's share drops to `n = 6` and ember takes the rest with its cap raised to 12 (ember then ends at about `41 + 3 + 12 x 2 = 68` s, still below `b`). The critical path becomes `b + 8 + 1 + 3 + 6 x 2 + 1 = b + 25`. For `n = 6` the break-even is `c <= 3.67 s` at `b = 100` and `c <= 4.95 s` at `b = 122`. The largest `n` for a measured `c` at `b = 100` (budget 22 s) is: `c = 2` gives 11 (cap 8 applies), `c = 2.75` gives 8, `c = 3.67` gives 6, `c = 5.5` gives 4. If `b <= 37 s` there is no budget at all (`0.35 b - 13 <= 0`). Luna's fastest recorded runs are 61 s (`SPEC` line 4) and `b` is the slowest reviewer of the panel, so this is not expected; still, the harness refuses to start an SS run when the budget `0.35 b - 13` is under 8 s (room for fewer than 4 items at `c = 2`, which happens below `b = 60 s`) and records `no_budget`.

### 12.4 Other panels (the sheet is adapted, not redesigned)

| Panel | Critical-path reviewer | Arithmetic | Elapsed | Cap |
|---|---|---|---|---|
| haiku + 2x luna | haiku (luna about 121 s, off the path) | `b + 8 + 1 + 3 + 6 x 4 + 1 = b + 37` | 257 s (+16.8%) at `b = 220`; 275 s (+15.5%) at 238 | 297 / 321.3 |
| sonnet + 2x luna | sonnet | `b + 8 + 1 + 3 + 6 x 3 + 1 = b + 31` | 290 s (+12.0%) at 259; 333 s (+10.3%) at 302 | 349.7 / 407.7 |

Pre-pass kill limit for these panels is 15 s (`0.10 b` exceeds 15 s), so the worst case adds 7 s: haiku 264 s (+20.0%) at `b = 220`, sonnet 297 s (+14.7%) at `b = 259`; both are inside the cap.

### 12.5 What the clock excludes and what is measured

Excluded in every arm: S0 (built once and reused), H2, the merge, the judge, the optional verifier (REQ-46). Only expected, never enforced: per-item cost, pre-pass seconds, median elapsed. They are measured against same-day Z0 (REQ-29). The +35% rule is judged on per-package medians, not on one run, because one reviewer's run-to-run spread is larger than 35%.

Measured before any arm: (1) the pre-pass on at least three real snapshots, the largest being the repository itself (no model; `IMPLEMENTATION.md` step 0); (2) the luna timing spike of REQ-32 (section 14.2). If the measured pre-pass exceeds the kill limit on a document, that document runs as `fallback` in every SS run and the document is reported as such.

### 12.6 Tokens (planning, unmeasured)

Output: baseline 21.3k per package for ember + 2x luna (63.7k haiku panel, 46.3k sonnet panel); SS adds +6k to +9k (+28% to +42%) on the primary panel and about +6k on the others. Input: +1.2-2.5k per reviewer for the sheet (worst case 4k with the 16,000-character cap). The pre-pass uses no model tokens. Judge cost is unchanged.

### 12.7 Measured values file

`config/values.json` holds `b` per (panel, document), `c` per model, `prepass_s`, `kill_s`, `hang_s` formula inputs, and the selection constants (`K` = 8 per class, `K_single` = 12 when only one class has candidates, cap 12). Every run copies the values it used into `run.json`, so a later analysis can tell planning values from measured ones.

## 13. How it generalises beyond the three study packages

### 13.1 What ties the design to the study, and what does not

Nothing in the code, cards, questions, regexes, lists or fixtures comes from a study package. The extractors key on sentence shapes (set words, backticked commands, edit verbs, count phrases), on structure (headings, labelled criteria, citations) and on the snapshot (tracked files), not on names. The mechanical protections:

| Rule | Mechanism in this design |
|---|---|
| AO-1 | `scaffold/lint.py` over `cards/`, `sweep/words.py`, `sweep/formats.py`, `sweep/extractors.py`, `briefs/` and `fixtures/`: fails on any 4-word sequence found in a ground-truth `description` or `plan_quote`, and on any name in the forbidden set (document ids, task titles of the study and hold-out plans, path tokens found in ground-truth text). The lint reads ground truth only when a person runs it; it prints the offending file and line and a hash of the phrase, never the phrase |
| AO-2 | each card has a `swap_test` record (a second author, who has not seen ground truth, replaced the domain nouns by placeholders and signed) |
| AO-3 | the `instances` field of every card (at least 2 citations) and the per-extractor counts of section 4.1 |
| AO-4 | REQ-21 fixtures: at least 3 non-study plans with seeded defects, seeded by someone who has not read the extractors (TESTING.md) |
| AO-5 | `bin/freeze.sh`: hashes of cards, extractors, words, formats, rank table, briefs, written to `config/freeze.json`; it prints the `git tag` command for a person to run |
| AO-6 | the pre-pass takes three explicit inputs; `test_prepass_inputs.py`; the sandbox grep of REQ-34 |
| AO-7 | offline selection ablation (`analysis/g0.py --ablate`), DD-13 |
| AO-8 | no card, question or brief states an expected outcome; fixtures use invented domains |

### 13.2 A new class

One card file `cards/C9.json` (all fields of `MR` 3.0.3 plus `promote_category`), and, only if a deterministic trigger exists, one registered extractor pair in `EXTRACTORS`. No change to `select.py`, `assign.py`, `render.py`, `scaffold/ledgerv1.py` or the launcher: the class list for quotas, the question and the route all come from the cards (REQ-10, tested with a fixture card). A new class with no extractor still enters arm K's paragraph.

### 13.3 A new target type

The block kinds of `MR` 3.0.3 are the checklist. For a new type the maintainer adds one dictionary to `sweep/formats.py` and fills the re-derive table in `cards/README.md` (REQ-38):

| Re-derive | Plan (done) | Specification | Documentation |
|---|---|---|---|
| Section map and edited-object detector | `formats.py: plan` | numbered headings; "Affects" lists | headings; fenced command blocks |
| Command dialect | grep, rg, pytest, test | the dialect named in the spec's verification rows | shell commands in fenced blocks |
| Test and root-document paths (the search scope, DD-5) | `tests/`, `scripts/`, `docs/`, root files, change logs | the same, plus the spec's parent folder | the documents' repository paths and the code they describe |
| Severity guidance | in each card | same | same |
| Location of truth | the source document | the parent requirement | the code, or the change log |
| Pre-change snapshot (H3) | base commit | base commit or recorded working tree | the commit before the fix |

Fixtures for a specification and for a documentation target exist (REQ-37): E1, E2 and E5 produce items on the spec fixture; E1 and E4 on the documentation fixture. E5 runs only when a parent document exists.

### 13.4 What does not generalise without work

Markdown only. A snapshot that is not a git repository (the search helper needs `git grep`). Citation styles other than `Source sections:` (E5 yields nothing for a task that cites in another way; `tasks_without_citations` shows it). Test-name reading by `ast` is for Python test files; other test languages need a second small reader. Spec and documentation dictionaries in `formats.py` are drafts until real spec and documentation fixtures exist.

### 13.5 What may be claimed

Class C2, C4, C5, C6, C8 and C7 in its broad form recur outside the three study packages and are treated as general; C1 and C3 are claimed in the weaker forms only (`MR` section 2). That a class exists is not evidence that cheap panels miss it elsewhere. Generality is shown only by the planted-set, hold-out and documentation-arm results (gate D5), and claims are worded as REQ-45 requires.

## 14. What the validation experiment needs from the design

The experiment itself is `MR` section 5 and its commands are in `TESTING.md`. This section lists what the design provides for it.

### 14.1 Gate G0, the offline selection-recall gate (`analysis/g0.py`)

G0 runs before any model arm and uses no model. It needs, per document, the plan, the source, the snapshot and a ground-truth file whose items have `class` and `plan_quote`. For derivation and hold-out documents the file is read by the gate script only, after the freeze; it is never placed in a sandbox and the pre-pass never reads it (AO-6).

| Quantity | Definition |
|---|---|
| covers(item, gt) | the flattened `plan_quote` of the ground-truth item contains, or is contained in, the item's flattened `anchor_text`; or their line spans (found with `FND.locate` on the candidate) come within 3 lines of each other (the same rule as `FND.same_defect`, `findings.py` line 377) |
| extraction recall | share of ground-truth items covered by any candidate (before selection) |
| selection recall | share of ground-truth items covered by a selected item |
| per class | both recalls per class C1-C8 |
| random baseline (a) | 2,000 draws (fixed seed) of 12 candidates uniformly from all candidates of the document: the "blind pick" of `MR` INV-001 |
| random baseline (b) | the same draws kept inside the fair-share structure of section 5 with random order replacing rank |

Pass: selection recall pooled over the decision documents is at or above the pre-registered floor, and the rank function beats random baseline (a) on the three derivation plans (rank recall above the mean of the draws, with at most 10% of draws at or above it). Baseline (b) is reported, not gated. The floor is pre-registered before the first arm (REQ-41, REQ-44). Recommended value: **0.45**. Basis: the mean of the lower ends of the `s` ranges in `MR` 3.1(d) is 0.48 over the ten rows (0.51 without the experimental I1 row); the floor sits just under it. This is a planning value and the owner confirms it (section 15).

`g0.py --ablate` removes one class at a time and reports the change in the selection recall of the other classes (AO-7, DD-13); the pass limit is 15 points.

### 14.2 Spikes (they need models, so they need the owner's go-ahead; none is run here)

| Spike | Runs | Measures | Sets |
|---|---|---|---|
| Timing (REQ-32) | 5 luna runs with an SS brief of 8 fixture items, plus 5 luna runs with the Z0 brief on the same document and day (the extra 5 are needed to get a cost per item; if same-day Z0 luna runs exist in the first block they are reused) | `c = (median(SS run) - median(Z0 run) - 3) / 8` | the item share per luna (8, or 6 under the fallback) |
| Compliance (REQ-17) | 5 SS panel runs on HO-6, the sanity set that is in no decision | `ledger_missing` rate, quote validity (`quote_plan_ok` share), format errors, format-induced demotions | go or no-go: `ledger_missing` at most 10% |
| Pre-pass timing | no model: `sweep prepass` on 3 or more real snapshots, the largest being `REPO` | S1 seconds | the kill limit check; the document-level `fallback` list |
| Harness share | Z0-raw against Z0 on HO-1 to HO-3 (the first runs of Stage 1) | the measured value that replaces +0.14 | nothing else |

### 14.3 Files the analysis script reads and writes (`analysis/analyze.py`, REQ-39)

It reads only the run folders, the judge outputs and `config/`. It writes `results/metrics.json` and `results/report.md`.

| Output | Content |
|---|---|
| per arm, per document | found fraction per run; share of runs that find at least half the items; run-to-run Jaccard of found sets; stable-hit rate; wrong blockers per run; found-any against found-blocking; non-probe findings per run; elapsed (mean and median); tokens; kills, retries, fallbacks, `invalid`; per-class reach with Wilson intervals |
| consistency | items reached in at least 60% of runs (3 of 5), per arm |
| gates | D1 to D7 and G0, pass or fail with the numbers; the bootstrap resamples documents first, then runs |
| shares | H share (Z0 minus Z0-raw), prompting share (K minus Z0), redesign share (SS minus Z0); never added in a headline (REQ-40) |
| `stages.jsonl` | one row per (run, ground-truth item): extraction, selection, act, merge survival, judge credit (REQ-41); `act` is a `PROBLEM` row with both quotes that links to the item (it is not conditional on selection, and the act-band measure of 15.1a is a different quantity); `merge survival` is read from `merged/ledger.json` members through `(reviewer_id, finding id)` |
| `ok_rate_planted.json` | share of `OK` verdicts on planted items (the rubber-stamp measure) |
| `judge_audit.json` | for every judge output: parseable, no API error text, `score.json` row counts equal the merged report's rows, `score.json` not older than the judge's final message (the defect `CR` line 147 describes); a second judge on a seeded 15% sample |

## 15. Decisions to confirm, and what is not checked

### 15.1 Decisions for the owner before the freeze (recommended values given)

| # | Decision | Recommended |
|---|---|---|
| 1 | G0 selection-recall floor (section 14.1) | 0.45 pooled |
| 2 | Per-class act-rate bands to pre-register (REQ-41, INV-004): the eight numbers, the measure they describe, and what a result outside a band may change. The numbers are the act ranges of `MR` 3.1(d). The measure, rule and consequence are in section 15.1a (a debate found that the numbers alone were not a complete registration) | C1 0.10-0.40, C2 0.20-0.45, C3 0.03-0.15, C4 0.50-0.75, C5 0.35-0.60, C6 0.05-0.30, C7 0.15-0.35, C8 0.40-0.65, registered together with the text of 15.1a |
| 3 | Whether to reword CB-2 for all arms so it no longer mentions ledger rows (DD-7) | leave verbatim, measure the `## Ledger` headings in Z0 and K |
| 4 | The K-arm lead-in text (DD-14) | approve `briefs/k-lead.txt` when it is written |
| 5 | The 5 extra Z0 luna runs in the timing spike (14.2) | yes (needed for `c`) |
| 6 | At most 3 panels at once (11.6) | yes |

Nothing else blocks the build. None of these needs an answer before `IMPLEMENTATION.md` steps 0 to 13; items 1 and 2 are needed at the freeze (step 14).

### 15.1a Act-band registration (decision 2)

Status: recommended text, not yet confirmed by the owner. It comes from the debate in `results/debate/1-act-bands/` (verdict FAIL on the numbers-only row; the numbers were not changed).

Why the numbers alone were not a complete registration. The bands are the planning act ranges of `MR` 3.1(d). There "act" is the chance, per run and given that the item is on the sheet, that the item is extracted, the model acts on it and the finding survives (`MR` 539, 357). The stage `act` that `analysis/analyze.py` computes (`stage_rows`) is not conditional on selection (an unselected item is `act` false) and does not include merge survival. A reader who set that stage rate against a band would read selection misses as reviewer misses, which is the confusion the stage split exists to prevent (`MR` 357, 662). The comparison also had no rule: even if every planning midpoint were true, the chance that all eight classes land inside their bands is 0.026 at 10 item-runs per class and 0.092 at 18 (`results/debate/1-act-bands/adversarial/work/band_sim.out`).

Registered text:

1. **Numbers** (planning values, not results): C1 0.10-0.40, C2 0.20-0.45, C3 0.03-0.15, C4 0.50-0.75, C5 0.35-0.60, C6 0.05-0.30, C7 0.15-0.35, C8 0.40-0.65.
2. **Measure.** Per class: among item-runs with `selection` true and `merge_survival` not null, in which at least one reviewer assigned to the item finished with a check ledger, the share with `merge_survival` true. Two ground-truth items covered by the same selected sheet item in the same run count once. Only runs of arm SS on the primary panel (ember + 2x luna) count. `stages.jsonl` has no `panel` or `set` field, so the person applying the rule joins `panel` from `run.json` and the set from `config/packages.json` by hand. Stage 1 and Stage 2 are kept apart, and within Stage 2 each set (planted, HO-5, documentation) is kept apart. The derivation set is excluded. The number of item-runs left out (no merge file, no finished reviewer) is shown.
3. **Rule.** A 95% Wilson interval (`WILSON_Z` 1.96 in `analysis/analyze.py`). Under 10 item-runs the class is "not assessable" and its counts are shown. Otherwise the class is "below" if the whole interval lies under the band, "above" if the whole interval lies over it, and "not contradicted" if the interval overlaps it.
4. **Consequence: report only.** A "below" flag on C4 or C8 adds one sentence beside the unchanged REQ-45 sentence: "the measured share was below its planning band for <class>". A "not assessable" result on C4 or C8 adds "no band check was possible (n = <count>)" there. The REQ-45 sentence itself is not changed (`TESTING.md` 149).
5. **May not:** change a gate result of D1 to D7 or G0, or the outcome of `MR` 5.8; disqualify, re-run or re-rank an arm; move a band after the first hold-out run; pool classes; read "above" or "not contradicted" as confirmation; set a band against the stage `act` rate, `class_reach`, judge credit or any Z0 or K rate. Only "below" is acted on. The measure is probably at or above the planning quantity (it conditions on selection, and the planning act also includes extraction), but that direction is assumed, not shown.

### 15.2 Not checked and unverified

- Every probability, rank weight, act band, selection factor, cost per item and line count: planning values (`MR`, "Not checked and unverified"). The rank weights of section 5.2 are new in this design and have never been run.
- The `ledger-v1` rule and the sheet block have never been run on any model. Whether luna, ember, haiku and sonnet write the block in the final message, with exact quotes, is what the compliance spike measures.
- The `claude -p` JSON shape (`user` events with `tool_result` blocks, `result` event with `result`, `usage`, `modelUsage`) was read from one finished ember run only. Other models' transcripts may differ; the `transcript` corpus (DD-2) must be checked on one run of each model.
- `FND._check_finding` and `FND._blocks_after` are private. The contract test pins them; a rename would need `scaffold/fnd.py` edited.
- That unknown keys survive the merge (REQ-11) is read from the code (`_check_finding` has no key whitelist; `merge_round` builds rows from fixed fields) and is not yet tested.
- The plan format is read from the first 44 lines of one plan (`schema: workflow-plan/1.2`). Other versions are not checked. The spec and documentation dictionaries are drafts.
- The word lists, stop list and verb lists of section 4 are described by category; the actual lists are written in `IMPLEMENTATION.md` step 6 and 7 and linted.
- `BR/enrichment/investigation-generality.md` (the instance register for AO-3) and `EVAL/tools/tmp-scripts/anon-b11.sh` were not read.
- That each ground-truth item's `plan_quote` is its trigger text (G0) is assumed from the field list in `JJ` line 14; the hold-out ground-truth schema must carry it.
- The Z0-raw sandbox (DD-15) is an approximation of a checkout that no longer exists.
- The time cost of `attach` for the top 12 candidates of one class (the single-class case, section 5.1 step 2) is unmeasured; it is bounded at 12 lookups.
- Search cost on the largest tree (`git grep -f` over the DD-5 scope) is unmeasured. It is the first thing `IMPLEMENTATION.md` step 0 measures, because it decides whether 8 s is realistic.
- The "0.914 squared" figure (`MR` 3.0.5 item 4) comes from one audit of luna anchors; the share of format-induced demotions in this design is only known after the compliance spike.
- Act-band measure (15.1a) is not built. No code computes the per-class measure or the flag and no test covers them; `ACT_BANDS` in `analysis/analyze.py` is only range-checked by `prereg`. Until a follow-up change adds both, the rule is applied by hand from `stages.jsonl`, `run.json` and `config/packages.json`, and the report says so. `prereg()` has no field for the 15.1a text and no order check covers this file, so the owner's confirmation of the text is recorded in `results/owner-decisions.md` and committed before the first hold-out run; the follow-up adds the text to `config/owner-values.json`. `bin/open-manual-checks.sh` has no attestation for applying the rule.
- Act-band statistics: the Wilson interval ignores correlation between runs on one item and between items that share evidence, so the false-flag and power figures (`results/debate/1-act-bands/adversarial/work/band_sim.out` and `v3_rule_sim.out`) are optimistic. At 10 to 18 item-runs the "below" flag cannot fire for C1, C3, C6 or C7 (power 0.00 in `v3_rule_sim.out`). The hold-out class mix is unknown, so some classes may be not assessable. The band numbers are unmeasured planning values taken from the three derivation packages; that they transfer to hold-out and planted material is assumed.
- No model was started and no experiment was run. Every statement about results in this document is a plan.
