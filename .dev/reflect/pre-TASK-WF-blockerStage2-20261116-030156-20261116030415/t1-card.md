# Tier 1 reflection card (UC-1 pre): TASK-WF-blockerStage2-20261116-030156

Plan = `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` (cited as PLAN:n). Spec = its `source.md` (SRC:n), the stage 2 request. Program spec = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (PSPEC:n). Stage 1 plan = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (S1:n). Stage 0 plan = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (S0:n).

## Coverage (Step 1B.0)

Pass 1 parsed IDs in SRC: 0 (the file labels nothing with R-/REQ-/SPEC-/T-). Pass 2 inferred 16 rows, all quote-pinned (`artifacts/coverage-matrix.md`). Mechanical containment matched 12 of 16 (`coverage_pct_union` 0.75). By a manual read, 15 of 16 are covered by a task or by the Constraints block. INF-015 (SRC:19: no edit of `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders, researchers) is only partly covered: PLAN:22 omits that list and no task checks it. `coverage_degraded: parsed-sparse` (inferred 16 > parsed 0), so a Tier-1 stop is forbidden.

## Findings (candidate defects, self-graded)

**T1-1 (blocking?)** The skill edits call code that has no callable surface. Task 2 makes the task skill "write `qa/follow-ups.md` through the follow-up writer", make "the one sweep call", and run the safety route (PLAN:50). The stage 1 plan builds `follow_ups.py` and `safety_route.py` as modules with tests only (S1:110, S1:183) and its only new command is `classify` (S1:171); stage 2 Task 1 builds `sweep.py` as a module with tests only (PLAN:33). `superclaude review` lists no follow-ups, sweep or safety subcommand (`src/superclaude/cli/review/__init__.py`, ledger_cmd.py pattern). The task skill is Markdown, so the only way to "call" them is prose naming a `uv run python -c` snippet whose signature no task fixes. Task 2's acceptance lines only grep for words (PLAN:53-58).

**T1-2 (blocking?)** `--unattended` is not carried into the offer text. Task 2 adds "the end-of-run offer is shown with the halt message" at each of the three cap sentences (PLAN:50), but `task/SKILL.md:55-57` makes those halts return the open blocking findings to the caller as a question under `--unattended`, WC-2 forbids chat offers there, and PSPEC:430-441 says an unattended run only records (offer state `unattended`). Task 4's check is on the contract text only (PLAN:79). Existing pin: `tests/skills/test_worker_contract.py:1715`.

**T1-3 (blocking?)** "Count of safety misses by the stage 0 definition" cannot be computed from ledgers. The stage 0 definition needs a later review or the owner to confirm a risk on a row that was recorded as a follow-up or Note (S0:130), but the script reads only run folders and `qa/follow-ups.md` (PLAN:110). No confirmation input is specified, so the script can only print 0, and Task 7 then states that stage 3 needs "zero safety misses" (PLAN:114). A silent wrong number goes to the owner.

**T1-4 (non-blocking?)** The judge in live shadow runs is never named. PLAN:50 says "the classifier is called in shadow mode"; OD3 is undecided and no external judge is built (PLAN:21-22); stage 1's judges are `FixtureJudge` and `ReviewerJudge` (S1:136), and PSPEC:586 says that with only the reviewer's label left the row records `classifier=unavailable`. So "shadow agreement" (PLAN:110) is either empty or trivially 1.0, and no task says so.

**T1-5 (non-blocking?)** Task 6 does not say how three blind agents times three replicates become judge verdicts: per agent (three judge ids; PSPEC:586 says results from different judges are not compared) or pooled (PLAN:98). Figures per set depend on it.

**T1-6 (non-blocking?)** Task 1's gate checks only stage 1 (PLAN:36-37). Task 6 reads stage 0 files (`fresh-findings.md`, `stage0-heldout-ids.json`) with no existence check (PLAN:98), and the ledger row for stage 0 says its review is NEEDS-REVISION (stage-requests README:17). The stage 1 package id is not yet in the ledger (README:19), though PLAN:19 says "the ids are in the stage ledger".

**T1-7 (non-blocking?)** Existing tests that pin the edited skills are not run by Tasks 2 and 3: `tests/skills/test_review_prompt_overrides.py:274-276`, `test_task_builder_merge.py`, `test_review_loop_extension.py` (named in `artifacts/codegraph-grounding.md` "Dependents"). Acceptance runs only the two severity tests (PLAN:58) and `-k "tech_research or review_severity"` (PLAN:67), which selects no tech-research test file (none exists).

**T1-8 (non-blocking?)** Smaller points. (a) Task 1 gives the sweep no input contract: how it finds "decision-basis sections" per deliverable kind (PSPEC:246-252) is left open (PLAN:33). (b) Nothing in the package shows that the request's no-edit list was respected: the stage 1 plan has a `git diff --stat` check (S1:221), this plan has none (PLAN:112-115). (c) PLAN:20 says the old definition "still decides every gate outcome" while Task 2 makes GR12 live, which can stop an attended gate for a person (PSPEC:322). (d) Task 3 forbids the word "sweep" in tech-research (PLAN:65) while also saying in prose that it gets no sweep call (PLAN:62), so the one-offer sentence must avoid the word.

## Items checked and found sound

Cap-sentence count matches: `task/SKILL.md` lines 258, 372, 409 and `tech-research/SKILL.md` lines 490, 555 hold the exact sentence; "highest severity" occurs on 2 lines of `task/SKILL.md` (252, 361); no "sweep" in either skill today; the "Post-Completion Validation (Final Phase Only)" heading exists (`task/SKILL.md:288`); WC-4's key list is `WORKER-CONTRACT.md:33` and "the coordinator opens it" is :39; `pragmatic.md:225` holds the legacy definition sentence; no plugin mirror exists for the task or tech-research skills. Stage 1 creates `follow_ups.py`, `safety_route.py`, `classifier_inputs.py`, the `classify` command, `registry.yaml` and `stage1-summary-for-owner.md` (S1:110, 183, 148, 171, 96, 221). The stage 0 package creates `fresh-findings.md`, `stage0-heldout-ids.json` (S0:82, 96).

## Self-assessed confidence (not used for routing; the blind calibrator re-grades it)

0.72. T1-1 to T1-3 were verified against the files cited; none was reproduced by running anything because the stage 1 modules do not exist yet.
