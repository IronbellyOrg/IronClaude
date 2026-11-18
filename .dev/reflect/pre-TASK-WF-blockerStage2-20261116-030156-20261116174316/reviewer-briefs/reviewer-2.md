# Reviewer brief

Run: pre-TASK-WF-blockerStage2-20261116-030156-20261116174316 (UC-1). Plan and spec paths are in the T1 card header. You are read-only: Read, Grep, Glob and codegraph/search tools only. Audit the supplied hunks and the live files they cite; run nothing.

## T1 card excerpt

### F3 [MEDIUM, grounded] Task 1 entry check is narrower than the Constraints promise
Constraints say Task 1 checks that the stage 1 modules and "the `classify` command exist" (plan:20). Task 1's check imports only `follow_ups`, `safety_route`, `classifier_inputs` (plan:44). `classify_cmd.py`/`classifier.py` (Task 7 runs `superclaude review classify`, plan:126), `refs/scale-map.md` (Tasks 2 and 4 read it, plan:56, 88) and the registry row state `legacy` (Task 6 reads it, plan:113) are not checked. A missing one fails late (Task 4, 6 or 7), after edits.

### F4 [MEDIUM, grounded] `follow-ups write` input format is not defined
Task 2 says `write` "imports the non-blocking rows of reviewer report tables" (plan:56) but names no parser or table format; Task 4 only says "add two fields to the finding row" in five prompt templates (plan:88). Tests use fixture reports (plan:60-62), so nothing ties the real reviewer output to the parser; an unparsable report gives `capture_state: incomplete`, which would make every real run partial.

### F5 [MINOR, grounded] Task 4 body and acceptance disagree on the word "sweep"
Body: "One sentence says this skill makes no sweep call and no offer" (plan:88). Acceptance: added lines contain the word "sweep" 0 times, and "the one sentence that says there is no sweep avoids the word" (plan:92). The body's wording cannot be written as given.

### F7 [MINOR, grounded] source.md base text contradicts Revision 2
source.md:11 still says "the one sweep call and one offer sit in the task skill's Post-Completion Validation" and :12 asks cap-site offers in the task skill and tech-research; Revision 2 (source.md:27-29) drops both. The plan follows Revision 2. The managed executor reads source.md byte-exact, so it sees both.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T17:48:47Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (index covers py/yaml/js/ts, not Markdown: use Read/Grep for the plan, skills and spec)

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md:1-61

````markdown
# Stage 2 plan request: shadow beside the old rule (issue #552)

Third of five plan packages (see `stage-requests/README.md`). Generate it only after the stage 1 package's `./artifacts/stage1-summary-for-owner.md` has been read and the owner has said go in chat; the stage ledger rows for stages 0 and 1 hold their package ids. The old definition still decides every gate outcome in this stage.

## Base text

Reuse Tasks 26 to 30 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 3, stage 2; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 2 parts). Stage 0 and stage 1 evidence is read by package id.

## Changes to apply

- **Constraints.** State this is stage 2: the sweep only records (`promote` off), the classifier has no authority, the one sweep call and one offer sit in the task skill's "Post-Completion Validation (Final Phase Only)", tech-research gets neither. Stage 3 starts only after the owner reads this package's summary and says go; the stage 3 entry also needs at least 5 observed shadow runs, which the owner or operator produces over time and no task here can produce.
- **Cap-site offers (base Tasks 27 and 28).** The halt-offer text goes beside each cap sentence in the task skill and in tech-research only; the two `rf-qa.md` cap sites are not touched here (stage 3). Acceptance quotes the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" and names no line numbers.
- **New task: classifier evaluation on the stage 0 populations (finding F7).** Run the classifier of the stage 1 modules (`classify` command, `classifier_inputs.py` supplier, the question set v1, recorded fixture answers produced by three blind agents that did not write the questions, no Jev) on the three sets built in stage 0: the fresh-findings set, the held-out half of the 318 rows, and the reviewer-called-minor set (read by the stage 0 package's id, its `./artifacts/fresh-findings.md`, `stage0-heldout-ids.json`, `stage0b-sample.md`). Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus, Cohen's kappa, confusion matrix, recall on the panel's blockers, flip rate over three replicates, split by deliverable kind, the count of rows that had each code-supplied input, and the limits. State that it is not an authority test (OD4).
- **New task: shadow summary script and stage 2 exit summary (finding F8).** Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers and prints the stage 2 exit numbers the spec defines (ledger volume per run, share of `consumer-unknown` rows, offers made and answered, shadow agreement, count of runs observed, count of safety misses by the stage 0 definition, capture failures), with a test over fixture ledgers. Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline, the script's output over the shadow runs that exist so far (zero is a valid and stated result), and the sentence that the owner's go for stage 3 is given in chat and not by this file.
- **Acceptance lines inside this package** that a later task of the same package makes false get an end point.

## Not to be done by the plan

No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders or researchers, and no promotion of swept rows to Blocking. Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.

## Revision 2 (2026-11-16)

Edited in place from `stage-requests/revision2-brief.md`. The plan file name, slug and frontmatter are unchanged. The pre-execution review of this stage did not finish; its three reviewer cards were verified against the live files before use, and the claims relayed from one advocate's Round 2 were verified the same way.

### Shared decisions applied

- **Decision 1 (retired carriers).** Every task that edited `src/superclaude/skills/task/SKILL.md` is dropped (old Task 2 and the task-skill half of old Task 5). The Constraints name the task skill, task-builder and `rf-task-builder.md` as not edited. The plan re-pins only the active carrier's part of shared tests (tech-research; the `/sc:implement` protocol).
- **Decision 2 (follow-up carrier).** The sweep call and the printed list moved from the task skill's "Post-Completion Validation (Final Phase Only)" to the final review step of `/sc:implement`: `SKILL.md` "Done" and the archive gate of `refs/managed-workspace.md` (new Task 3). Record and print only: one read-only call, no `--promote`, no `--write`, no question. `refs/qa.md` is not edited (SHA-256 `93e232f5d49207624c24da25bc6f2e9a0686b4f7f7ca99a38e4b95f56edaf004`, source and plugin twin equal, recorded in Task 1 and compared in Tasks 3 and 8). The once-per-run offer question stays with the top-level session through the output style (changed from per loop to per run at stage 3) and with the consent-bound filing path (OD15); the Constraints say so in one sentence.
- **Decision 3.** tech-research keeps its ledger-writing edit (Task 4); no sweep, no offer, and the halt-offer sentences beside its two cap sentences are dropped because no offer exists in this stage.
- **Decision 4 (plugin surface).** No new plugin surface. The one existing hand-kept twin touched is `plugins/superclaude/skills/sc-implement-protocol/` (two files, copied byte for byte in Task 3), because `test_h_implement_protocol_plugin_twins_byte_equal` and the managed-workspace mirror check in `test_reflect_input_snapshot.py` pin it. Registry counts are not touched by this package.
- **Decision 5 (ledger).** `follow-ups.md` stays a separate file; no mapping to `review-ledger/1`; `ledger.py` is not edited.
- **Decision 6.** No `/sc:implement` run, no commit, no push; `.dev/tasks` staged only.

### Review findings

- **R1-1, R3-1 (no command exists for the writer, safety route or sweep): applied.** Verified: `src/superclaude/cli/review/__init__.py` registers nine subcommand modules and none for these. New Task 2 builds `follow_ups_cmd.py` (group `follow-ups`: `write`, `safety`, `sweep`, `summary`) and registers it. Ownership: stage 1 owns `classify_cmd.py`; this package owns `follow_ups_cmd.py` because it builds `sweep.py`. Cross-stage need reported.
- **R1-2, R3-3 (no `--unattended` branch for the offer): applied by removal.** No offer is made in this stage; the sweep asks nothing; the safety route records and does not wait when nobody is reachable. Task 5 adds a test that the unattended commands make no GitHub call and ask no question. The task skill paragraph pinned by `test_task_skill_returns_the_qa_halt_to_an_unattended_caller` is no longer touched. The wording "except the GR12 safety route" was added to the Constraints.
- **R1-3, R2-1 (safety-miss count not computable from ledgers): applied.** Verified: the stage 0 definition needs a later confirmation that no ledger holds. Task 8's script takes `--confirmed-misses <file>` and prints "not computable" without it. The definition is marked proposed in the spec; the Constraints say so.
- **R1-4, R3-2 (no live judge): applied.** Verified: only `FixtureJudge` and `ReviewerJudge` exist (stage 1 Task 9). Live shadow rows read `classifier=unavailable` unless the run owner holds a recorded answers file; Task 8 splits agreement by judge id, prints the `unavailable` count and counts no reviewer-label row.
- **R1-5 (replicate rule per agent): applied** in Task 7 (each agent is its own judge id, median of 3, blind table only, per-agent figures).
- **R1-6, R2-2 (stage 3 entry sentence incomplete): applied.** "zero safety misses and no capture failure" in Task 8 and the Constraints.
- **R1-7, R2-3, R3-4 (Task 6 inputs): applied.** Task 7 names PF `04-historical/master-table.md`, PF `05-scoring/consensus.md`, `stage0b-sample.md`, `fresh-findings.md` and `stage0-heldout-ids.json`, and counts `@E2` rows separately (the supplier runs no subprocess). Task 1 checks that the ledger holds the stage 0 and stage 1 package ids.
- **R1-8 ("Findings Consolidation" ambiguity; no-edit list): partly applied.** The task skill is no longer edited, so the ambiguity is moot (not applied). The request's no-edit list is copied into the Constraints (applied). Advocate claim that the phrase appears at two sites of the task skill: verified, relevant only to the dropped task.
- **R2-4, R3-6 (checks missing for edited text): applied.** Verified: `pytest -k tech_research` selects nothing (95 deselected), because test ids spell `tech-research`. Tasks 3 and 4 now name the test files explicitly, including `test_review_prompt_overrides.py`, `test_worker_contract.py` and the `/sc:implement` pin tests. Task 8 adds the `git diff --stat HEAD` no-edit check.
- **R3-5 (owner go checked after edits): applied.** Task 1 opens with "Before any edit".
- **R3-7 (sweep has no input contract): applied.** Task 1 fixes arguments (ledgers, deliverables, kind) and counts skipped kinds.
- **R3-8 (tech-research halt may show no offer): not applied.** No offer exists in stage 2 by decision 2, so there is nothing to show at a halt.

### Advocate claims

- **WORKER-CONTRACT writes `return-contract.yaml` only under `--unattended`: verified (WC-4).** `/sc:implement` has no unattended section yet (its WC-9 rows are deferred) and tech-research has none. Task 5 names `follow-ups summary` as the producer and Task 8 states the limit that no command emits the keys live yet.
- **Shadow summary must split by judge id, print the `unavailable` count and count only non-reviewer judges: applied** (Task 8).
- **Reviewer brief wording and the tier source: applied** (Task 4: "for every finding you grade non-blocking under your current definition"; the tier comes from `refs/scale-map.md`).

### Existing tests named in the plan

`tests/skills/test_implement_severity_static.py`, `tests/skills/test_review_severity_rule.py`, `tests/skills/test_task_workspace_lifecycle.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/skills/test_workflow_archive.py`, `tests/skills/test_implement_saved_prompt_rule.py`, `tests/skills/test_reflect_input_snapshot.py`, `tests/skills/test_codegraph_adoption.py`, `tests/commands/test_impact_command.py`, `tests/skills/test_worker_contract.py`, `tests/unit/test_cli_install.py`, `tests/skills/test_review_prompt_overrides.py`, `tests/skills/test_review_severity_mapping.py`, `tests/review/test_review_cli.py`.

### Task count

7 before, 8 after (old Task 2 dropped; old Task 1 split into Tasks 1 and 2; Task 3 retargeted; old Tasks 4 to 7 became 5 to 8).
````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:35-50

````markdown
## Phase 1: Build the sweep and the follow-ups commands

## Task 1: Check the entry conditions and build the record-only sweep

Before any edit, run these checks and stop for the owner's Ruling if one fails: the stage ledger `stage-requests/README.md` in PF holds the package ids of stages 0 and 1 and an owner go for stage 2 with a date; the stage 1 modules import; the stage 1 and stage 0 files this package reads exist (read by package id: stage 1 `./artifacts/stage1-summary-for-owner.md`; stage 0 `./artifacts/fresh-findings.md`, `./artifacts/stage0-heldout-ids.json`, `./artifacts/stage0b-sample.md`, `./artifacts/classifier-input-availability.md`). Then record the SHA-256 of `src/superclaude/skills/sc-implement-protocol/refs/qa.md` and of its plugin twin in `./artifacts/qa-md-sha256-before.txt` (two lines, equal today).

Then create `src/superclaude/cli/review/sweep.py` for GR7. Input contract: the ledger paths (read only through the stage 1 reader), one or more deliverable paths, and a deliverable kind: `report`, `spec`, `tasklist`, `code`, `other` or `auto` (a file whose front matter holds `schema: workflow-plan/` is a tasklist; a file with the headings "Options Analysis" and "Recommendation" is a report; a file with requirement and acceptance headings is a spec; anything else is `other`). The decision-basis sections by kind follow spec section 4.3: for a report the sections named "Options Analysis", "Recommendation" and "Implementation Plan" of the tech-research report structure; for a spec its requirements, acceptance criteria, boundary rows and quoted constraints; for a tasklist its acceptance criteria, dependency lines and constraints (reuse the section finders of `classifier_inputs.py` where they already find the same sections). Kinds `code` and `other` have no decision-basis list: the sweep skips them and counts them as skipped, and a deliverable whose decision-basis section is missing is counted as skipped, never an error. A Medium row (Notes are never swept) is flagged when the flawed text or figure from its evidence block still appears verbatim in a decision-basis section of the current deliverable. Switches: `promote` defaults to off and `write` defaults to off. With `promote` off a flagged row is returned as `sweep-flagged` and no grade changes; with `promote` on (used only from the stage 3 package) the same row is returned as Blocking at that gate; with `write` on the flagged state is written through the stage 1 writer, and with `write` off the ledger bytes are never touched. Create `tests/review/test_review_sweep.py` for T16 and for the stage 2 rule.

Acceptance criteria:
- The entry checks above all hold, and `uv run python -c "from superclaude.cli.review import follow_ups, safety_route, classifier_inputs"` succeeds; when any check fails the run stops for the owner's Ruling.
- `./artifacts/qa-md-sha256-before.txt` exists with two equal SHA-256 lines for the source and plugin copies of `refs/qa.md`.
- `uv run pytest tests/review/test_review_sweep.py -v` passes. With `promote` off a Medium row whose flawed figure reaches a decision-basis section uncorrected is returned as `sweep-flagged` and no verdict changes; with `promote` on the same row is returned as Blocking; a corrected row is not flagged either way.
- A test shows kinds `code` and `other` and a deliverable with no decision-basis section are skipped and counted, and `auto` picks `tasklist`, `report` and `spec` for one fixture each.
- The sweep never lowers a grade and never touches a Note row, and with `write` off a test shows the ledger bytes are identical before and after.
- The module opens no ledger file itself: `grep -n "follow-ups.md" src/superclaude/cli/review/sweep.py` prints nothing, and its only file reads are deliverables and the stage 1 reader.
- A test asserts that with the default (`promote` off, `write` off) the result of a gate that includes the sweep equals the result of the same gate without it.
````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:109-118

````markdown
## Task 6: Pin the shadow-stage text

Depends on: Task 3, Task 4

Create `tests/skills/test_review_brief_rests_on.py` for T9: each of the five tech-research reviewer prompt templates of Task 4 (found by heading) must carry the `rests_on` and `why not blocking` fields. Also assert that the legacy definition text of `src/superclaude/output-styles/pragmatic.md` (the sentence "Grade every review finding as blocking or minor" and the bullets around it) is unchanged while the registry row for `output-styles/pragmatic.md` in `src/superclaude/skills/sc-review-severity/refs/registry.yaml` is in state `legacy`; once that row is `v2` the assertion is skipped, so the stage 3 package's pragmatic.md task does not turn the test red. Create `tests/skills/test_implement_follow_up_sweep.py`: the managed-workspace paragraph sits after the step 5 line and before the step 6 line, each file names the sweep call once without `--promote` or `--write`, the `SKILL.md` paragraph holds the sentence "It asks the user nothing" and no question mark, and neither added paragraph holds the words that the static scan of `tests/skills/test_implement_severity_static.py` flags.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_brief_rests_on.py -v` passes and fails when either field is removed from any one of the five prompts.
- A test fails if the legacy definition text of `pragmatic.md` changes while its registry row is `legacy`, and a test shows the assertion is skipped when the row is set to `v2` in a temporary registry copy.
- `uv run pytest tests/skills/test_implement_follow_up_sweep.py -v` passes, and mutated temporary copies fail it: the paragraph moved after the step 6 line, `--promote` added to the call line, and a question added to the paragraph.
````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:120-144

````markdown
## Phase 4: Evaluate the classifier and write the owner summary

## Task 7: Evaluate the classifier on the stage 0 populations

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Run the classifier of the stage 1 modules (`superclaude review classify`, the `classifier_inputs.py` supplier, the question set v1) on the three sets the stage 0 package built, read by package id. Fresh-findings set: `./artifacts/fresh-findings.md` (the blind table and the panel consensus are both in that file). Held-out half of the 318 rows: its ids are in `./artifacts/stage0-heldout-ids.json`; the finding text and cited paths are in PF `04-historical/master-table.md` and the panel consensus is in PF `05-scoring/consensus.md`. Reviewer-called-minor set: its ids are in the same json file, its scores are in the Task 2 sample section of `fresh-findings.md`, and each finding's source file and quote are in `./artifacts/stage0b-sample.md`. Rows whose path starts with `@E2` need `git show` from the branch `origin/ironbelly/eval-tasklist-review-panel`; the supplier reads from disk only and runs no subprocess, so those rows are counted on a separate line as "evidence resolved by hand, not supplied by code", and their evidence input is UNSET for the classifier. The judge answers come from three blind agents that did not write the questions, three replicates each, recorded in fixture files; each agent is its own judge id with the median-of-3 replicate rule, and the figures are reported per agent. The agents see only the blind table (no panel consensus, no old grade, no reviewer label, no scale map), because otherwise agreement is inflated. No Jev and no external service is called, and `ReviewerJudge` is not used for any figure. Report each set separately and never pool them. Write `./artifacts/stage2-classifier-eval.md`: per set and per agent the agreement with the panel consensus, Cohen's kappa, the confusion matrix, recall on the panel's blockers, the flip rate over three replicates, the split by deliverable kind, the count of rows that had each code-supplied input (required-item list, constraint lines, verified evidence excerpt), and the limits. State that this is not an authority test (OD4).

Acceptance criteria:
- `./artifacts/stage2-classifier-eval.md` has one section per set (fresh findings, held-out half, reviewer-called-minor set) with the figures above for each of the three agents, and no pooled figure.
- The three blind agents' ids are recorded and the file states none of them wrote the questions and that they were given the blind table only; the answer files are named and exist under `./artifacts/`.
- The file states that no judge other than the recorded blind agents was used, that no external service was called, and that no classifier authority follows (OD4).
- The file reports the count of rows per code-supplied input for each set and the separate count of `@E2` rows resolved by hand, and each row where an input was not supplied has its answer recorded as UNSET or NA, never N.

## Task 8: Write the shadow summary script and the stage 2 owner summary

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7

Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their follow-up ledgers (`qa/follow-ups.md`, or `follow-ups.md` in a folder with no QA directory), through the stage 1 reader, and prints the stage 2 exit numbers the spec defines in its section 12 stage 2 row (as edited by the stage 0 package): ledger volume per run, the share of rows tagged `consumer-unknown` among non-blocking rows, offers made and answered (read from the Offers table; no stage 2 carrier writes it, because the per-run offer moves to the top-level session at stage 3, so zero is expected and is stated), the shadow agreement figures, the count of runs observed, the count of safety misses by the stage 0 definition, and the count of capture failures. Agreement is split by judge id and version (spec metric M13), prints the count of rows with `classifier=unavailable`, and counts only rows from a judge that is not the reviewer's own label. The safety-miss count takes `--confirmed-misses <file>` (one row id per line that a later review or the owner confirmed as a safety risk); without that file it prints "not computable: N unreviewed rows carry safety vocabulary" and never a bare zero, and with it the count is the confirmed rows that lack the `protected-risk-dispute` tag. Fixture ledgers under `./artifacts/shadow-fixtures/` are generated by the stage 1 writer, not typed by hand, with a test over them. Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline from Task 7, the script's output over the shadow runs that exist so far (zero runs is a valid and stated result), the sweep, command, `/sc:implement` and tech-research wiring results from Tasks 1 to 6, the limits, and the sentence that the owner's go for stage 3 is given in chat and not by this file. The limits include: shadow ledgers come only from tech-research runs now that `/sc:task` is retired; the `/sc:implement` sweep skips code deliverables and so mostly reports skips; the worker-contract keys have a producer and a pinned text but no command emits them live yet; and agreement is empty when only the reviewer's own label ran as judge.

Acceptance criteria:
- `./artifacts/shadow_summary.py` runs with `uv run python ./artifacts/shadow_summary.py --help` and its fixture test passes with `uv run pytest ./artifacts/test_shadow_summary.py -v`, which covers a confirmed unrouted safety miss, a run without a confirmation file (printed as not computable), `unavailable` rows, a capture failure, and a ledger from a reviewer-label judge that adds nothing to agreement (the commands and the pytest output are recorded in the summary).
- `./artifacts/stage2-summary-for-owner.md` names the headline of Tasks 1 to 7 with the file that holds it, states the number of shadow runs observed so far (zero is allowed), and states plainly that the stage 3 entry needs at least 5 observed runs with zero safety misses and no capture failure.
- The summary shows `git diff --stat HEAD -- src/superclaude/output-styles src/superclaude/agents src/superclaude/templates src/superclaude/rules src/superclaude/commands src/superclaude/skills/task src/superclaude/skills/task-builder src/superclaude/skills/sc-implement-protocol/refs/qa.md plugins/superclaude/skills/sc-implement-protocol/refs/qa.md src/superclaude/cli/review/ledger.py` with empty output, and the `refs/qa.md` SHA-256 compared with `./artifacts/qa-md-sha256-before.txt`.
- The summary ends with the sentence that the owner's go for stage 3 is given in chat and not by this file.
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:942-950

````markdown
| Stage | Entry condition | What happens | Exit condition | Rollback |
|---|---|---|---|---|
| 0. Measure (this program, offline) | this spec reviewed | 0a: the scored table and five runs with a fixture or approved judge, only if the table exists. 0b: the retrospective escape test on run 2 (section 8.4). 0c: three blind agents that did not write the rule re-grade the table under the old and the new text, paired, only if the table exists. Inventory freeze: every Grep of section 10 re-run, including the frozen FAIL-trigger Grep (REQ-30), with results stored | a written result: escape estimate with its interval; when the table exists, how many old-blocking rows become non-blocking and the confusion matrix | nothing changed |
| 1. Offline scaffold | stage 0 result written; owner go | the skill folder with registry rows all `legacy` (T1 and T2 accept the legacy text in registered rows); the ledger reader and writer with the codec; ledger adapters; the fixture judge; property tests; crash, reconcile and consent tests; the install check. No carrier is edited | T1 to T4, T6 to T8, T11 to T13 and T17 green offline | delete the new files |
| 2. Shadow beside the old rule | stage 1 exit | the task skill and tech-research gates write the ledger and make the per-run offer (it replaces the output style's "once per loop" ask for that run); reviewers emit `rests_on` while the old definition still decides; the classifier runs in shadow; the safety route GR12 is live; the final-gate sweep GR7 is built; `core/WORKER-CONTRACT.md` gains the three keys (REQ-12) | at least 5 shadow runs observed; ledger volume and `consumer-unknown` share known; offers answered; shadow agreement reported; zero safety misses and no capture failure | stop writing the ledger; restore the old carrier text by the three-step revert (section 9.4) |
| 3. Pilot | 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (section 8.3) met; 0c as well when the table exists; owner go | `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` move to digest v2 together; the stage 3 merge-rule lines of section 10.3 (task skill, rf-qa, rf-qa-qualitative, rf-analyst; L1); L2 fix-pass checks; L6 for rf-qa, and Rule 6 if OD16 chooses (b), with its test re-pinned in the same change; the cadence pins move | one audit window (section 8.2) with no revert trigger tripped; M12 reported | the three-step revert of the pilot rows to `legacy` |
| 4. Propagate | stage 3 exit; owner go | templates, rule prompts, builders and researchers to v2; the stage 4 lines of section 10.3; the spec-panel narrowing; the plugin mirror and parity test; T2 becomes strict (no legacy definition sentence in `src/` or `plugins/`) | drift tests green and strict; a second audit window clear | per-row three-step revert |

Why shadow comes before the pilot: the whole design rests on reviewers being able to name a consumer honestly. Stage 2 measures that while the old definition still decides, so a failure costs nothing.
````

## Coverage slice

| Row | Spec line | Quote | Containment match | By hand |
|---|---|---|---|---|
| INF-001 | source.md:7 | Reuse Tasks 26 to 30 of the revised 46-task plan | none (0.286) | Constraints line 19; whole plan |
| INF-002 | source.md:11 | the sweep only records (`promote` off), the classifier has no authority | Task 4 (0.6) | Task 4 |
| INF-003 | source.md:11 | Stage 3 starts only after the owner reads this package's summary and says go | Task 8 (0.727) | Task 8 |
| INF-004 | source.md:13 | Run the classifier of the stage 1 modules | Task 7 (1.0) | Task 7 |
| INF-005 | source.md:13 | Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus, Cohen's kappa, confusion matrix, recall on the panel's blockers, flip rate over three replicates | Task 7 (1.0) | Task 7 |
| INF-006 | source.md:13 | State that it is not an authority test (OD4). | Task 7 (1.0) | Task 7 |
| INF-007 | source.md:14 | Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers | Task 8 (1.0) | Task 8 |
| INF-008 | source.md:14 | with a test over fixture ledgers | Task 8 (1.0) | Task 8 |
| INF-009 | source.md:14 | Then write `./artifacts/stage2-summary-for-owner.md` | Task 8 (1.0) | Task 8 |
| INF-010 | source.md:15 | Acceptance lines inside this package** that a later task of the same package makes false get an end point. | none (0.538) | Constraints line 30 (end point rule); no task acceptance carries an 'until Task N' |
| INF-011 | source.md:19 | No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders or researchers, and no promotion of swept rows to Blocking. | none (0.286) | Constraints line 26 |
| INF-012 | source.md:19 | Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. | none (0.455) | Constraints line 26 |
| INF-013 | source.md:19 | No Jev call, key or account. | none (0.25) | Constraints line 26 |
| INF-014 | source.md:27 | Every task that edited `src/superclaude/skills/task/SKILL.md` is dropped | none (0.5) | Constraints line 22 |
| INF-015 | source.md:28 | The sweep call and the printed list moved from the task skill's "Post-Completion Validation (Final Phase Only)" to the final review step of `/sc:implement` | Task 3 (0.765) | Task 3 |
| INF-016 | source.md:28 | Record and print only: one read-only call, no `--promote`, no `--write`, no question. | Task 3 (0.857) | Task 3 |
| INF-017 | source.md:28 | `refs/qa.md` is not edited | Task 3 (1.0) | Task 3 |
| INF-018 | source.md:29 | tech-research keeps its ledger-writing edit (Task 4); no sweep, no offer | Task 4 (0.625) | Task 4 |
| INF-019 | source.md:30 | No new plugin surface. | Task 3 (0.667) | Constraints line 23 + Task 3 |
| INF-020 | source.md:30 | copied byte for byte in Task 3 | Task 3 (0.8) | Task 3 |
| INF-021 | source.md:31 | `follow-ups.md` stays a separate file; no mapping to `review-ledger/1`; `ledger.py` is not edited. | none (0.25) | Constraints line 24 |
| INF-022 | source.md:32 | No `/sc:implement` run, no commit, no push; `.dev/tasks` staged only. | none (0.375) | Constraints line 33 (staging); no task runs /sc:implement, commits or pushes |
| INF-023 | source.md:36 | New Task 2 builds `follow_ups_cmd.py` (group `follow-ups`: `write`, `safety`, `sweep`, `summary`) and registers it. | Task 2 (0.769) | Task 2 |
| INF-024 | source.md:37 | Task 5 adds a test that the unattended commands make no GitHub call and ask no question. | Task 3 (0.636) | Task 5 |
| INF-025 | source.md:38 | Task 8's script takes `--confirmed-misses <file>` and prints "not computable" without it. | Task 8 (0.818) | Task 8 |
| INF-026 | source.md:39 | Task 8 splits agreement by judge id, prints the `unavailable` count and counts no reviewer-label row. | Task 8 (0.75) | Task 8 |
| INF-027 | source.md:40 | Task 7 (each agent is its own judge id, median of 3, blind table only, per-agent figures). | Task 7 (0.75) | Task 7 |
| INF-028 | source.md:41 | "zero safety misses and no capture failure" in Task 8 and the Constraints. | Task 8 (0.75) | Task 8 |
| INF-029 | source.md:42 | Task 7 names PF `04-historical/master-table.md`, PF `05-scoring/consensus.md`, `stage0b-sample.md`, `fresh-findings.md` and `stage0-heldout-ids.json`, and counts `@E2` rows separately | Task 7 (0.643) | Task 7 |
| INF-030 | source.md:42 | Task 1 checks that the ledger holds the stage 0 and stage 1 package ids. | Task 1 (0.818) | Task 1 |
| INF-031 | source.md:44 | Tasks 3 and 4 now name the test files explicitly | Task 8 (0.625) | Tasks 3 and 4 |
| INF-032 | source.md:44 | Task 8 adds the `git diff --stat HEAD` no-edit check. | Task 3 (0.667) | Task 8 |
| INF-033 | source.md:45 | Task 1 opens with "Before any edit". | Task 1 (0.8) | Task 1 |
| INF-034 | source.md:46 | Task 1 fixes arguments (ledgers, deliverables, kind) and counts skipped kinds. | Task 3 (0.6) | Task 1 |
| INF-035 | source.md:51 | Task 5 names `follow-ups summary` as the producer and Task 8 states the limit that no command emits the keys live yet. | Task 5 (0.8) | Task 5 |
| INF-036 | source.md:53 | for every finding you grade non-blocking under your current definition | Task 4 (1.0) | Task 4 |
