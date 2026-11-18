# Reviewer 2 brief (qa, model class haiku)

## T1 card excerpt

Assignment: independent pre-execution review of the plan `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` against its request `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md` (UC-1, advisory, read-only). Lens (qa): coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check every acceptance line of every task: can it pass and can it fail, does it name a file or command that exists or that an earlier task or package creates, does a later task of this plan make it false without an end point, and is the order of tasks valid for an executor that runs them top to bottom.

The T1 points below are UNVERIFIED LEADS written by the orchestrator, not conclusions. Verify each against the files, drop the ones you cannot reproduce, and add defects the card missed. Severity rule (use exactly): BLOCKING = a requirement or check in the plan that cannot be met as written, a wrong or missing result, or data loss; MINOR = wording or format. Say for each finding whether the plan can still be executed correctly by an executor who follows it literally.

Return your findings as your final message (you cannot write files); the orchestrator saves them. For each finding give: id (R2-1, R2-2, ...), grade (blocking or minor), the plan location (PLAN:line), your evidence as file:line with a short quote, what the executor would do wrong, and the smallest fix. At most 8 findings, each under 700 characters. If a T1 lead is wrong, say so in a final section 'Leads dropped' with one line each. Cite only lines you have Read.

Plan = `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` (cited as PLAN:n). Spec = its `source.md` (SRC:n), the stage 2 request. Program spec = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (PSPEC:n). Stage 1 plan = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (S1:n). Stage 0 plan = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (S0:n).

**T1-6 (non-blocking?)** Task 1's gate checks only stage 1 (PLAN:36-37). Task 6 reads stage 0 files (`fresh-findings.md`, `stage0-heldout-ids.json`) with no existence check (PLAN:98), and the ledger row for stage 0 says its review is NEEDS-REVISION (stage-requests README:17). The stage 1 package id is not yet in the ledger (README:19), though PLAN:19 says "the ids are in the stage ledger".

**T1-7 (non-blocking?)** Existing tests that pin the edited skills are not run by Tasks 2 and 3: `tests/skills/test_review_prompt_overrides.py:274-276`, `test_task_builder_merge.py`, `test_review_loop_extension.py` (named in `artifacts/codegraph-grounding.md` "Dependents"). Acceptance runs only the two severity tests (PLAN:58) and `-k "tech_research or review_severity"` (PLAN:67), which selects no tech-research test file (none exists).

**T1-8 (non-blocking?)** Smaller points. (a) Task 1 gives the sweep no input contract: how it finds "decision-basis sections" per deliverable kind (PSPEC:246-252) is left open (PLAN:33). (b) Nothing in the package shows that the request's no-edit list was respected: the stage 1 plan has a `git diff --stat` check (S1:221), this plan has none (PLAN:112-115). (c) PLAN:20 says the old definition "still decides every gate outcome" while Task 2 makes GR12 live, which can stop an attended gate for a person (PSPEC:322). (d) Task 3 forbids the word "sweep" in tech-research (PLAN:65) while also saying in prose that it gets no sweep call (PLAN:62), so the one-offer sentence must avoid the word.

## Items checked and found sound

Cap-sentence count matches: `task/SKILL.md` lines 258, 372, 409 and `tech-research/SKILL.md` lines 490, 555 hold the exact sentence; "highest severity" occurs on 2 lines of `task/SKILL.md` (252, 361); no "sweep" in either skill today; the "Post-Completion Validation (Final Phase Only)" heading exists (`task/SKILL.md:288`); WC-4's key list is `WORKER-CONTRACT.md:33` and "the coordinator opens it" is :39; `pragmatic.md:225` holds the legacy definition sentence; no plugin mirror exists for the task or tech-research skills. Stage 1 creates `follow_ups.py`, `safety_route.py`, `classifier_inputs.py`, the `classify` command, `registry.yaml` and `stage1-summary-for-owner.md` (S1:110, 183, 148, 171, 96, 221). The stage 0 package creates `fresh-findings.md`, `stage0-heldout-ids.json` (S0:82, 96).

## Self-assessed confidence (not used for routing; the blind calibrator re-grades it)

0.72. T1-1 to T1-3 were verified against the files cited; none was reproduced by running anything because the stage 1 modules do not exist yet.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:12:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

`.dev/reflect/pre-TASK-WF-blockerStage2-20261116-030156-20261116030415/artifacts/coverage-matrix.md` holds the coverage matrix (artifact ref).

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md:1-19

```markdown
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
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:29-115

```markdown
## Phase 1: Build the record-only sweep

## Task 1: Build the final-gate sweep in record-only form

Create `src/superclaude/cli/review/sweep.py` for GR7: at the last gate before delivery, every open Medium row is re-tested, and a row whose flawed text or figure appears, uncorrected, in a decision-basis section of the final deliverable is flagged. The function has a `promote` switch that defaults to off. With it off (stage 2) a flagged row is written to the ledger as `sweep-flagged` and no grade changes; with it on (from the stage 3 package) the flagged row becomes Blocking at that gate. Today no final gate reads a ledger (the task skill's "Post-Completion Validation (Final Phase Only)" section runs one final validation and names no ledger; tech-research's Gate 5 enumerates findings and reads no ledger). Create `tests/review/test_review_sweep.py` for T16 and for the stage 2 rule.

Acceptance criteria:
- The stage ledger `stage-requests/README.md` in PF has an owner go for stage 2 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
- `uv run python -c "from superclaude.cli.review import follow_ups, safety_route, classifier_inputs"` succeeds (the stage 1 modules exist) and the stage 1 package's `./artifacts/stage1-summary-for-owner.md` (read by package id) exists.
- `uv run pytest tests/review/test_review_sweep.py -v` passes; with `promote` off a Medium row whose flawed figure reaches the final decision basis uncorrected is returned as `sweep-flagged` and no verdict changes; with `promote` on the same row is returned as Blocking, and a corrected one is not flagged either way.
- The sweep never lowers a grade and never touches a Note row.
- The module reads only the ledger path that the ledger reader returns (no second reader of `follow-ups.md`).
- A test asserts that with the default (`promote` off) the result of a gate that includes the sweep equals the result of the same gate without it.


## Phase 2: Wire the shadow stage into the task skill and tech-research

## Task 2: Make the task skill write the ledger, call the sweep and make the offer in shadow mode

Depends on: Task 1

Edit `src/superclaude/skills/task/SKILL.md`: the reviewer brief at the Phase-Gate QA step asks each reviewer for `rests_on` (the named consumer, or `none`, or `unknown`) and a one-line `why not blocking` for every Medium or Note finding (GR2); the Findings Consolidation step keeps its present merge text in this stage but also writes `qa/follow-ups.md` through the follow-up writer (REQ-07, the run owner is the only writer); the Follow-Up Items bullet in the final-phase notes points at that ledger; the safety route (GR12) is live; the classifier is called in shadow mode and its verdict is recorded and gates nothing. The one sweep call (`promote` off) and the one end-of-run offer (spec section 6.3, replacing the output style's once-per-loop ask for this run only) are placed in the section "Post-Completion Validation (Final Phase Only)", because tech-research runs inside `/task` and shares that final gate. The offer also appears at an escalation halt: at each sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" in this file (today at the Conditional Proceed step, the Escalation item of the fix-cycle list, and the Fidelity Verification step) the text says the end-of-run offer is shown with the halt message. The old definition still decides every gate outcome. Run `make sync-dev` afterwards.

Acceptance criteria:
- The reviewer brief in `src/superclaude/skills/task/SKILL.md` contains `rests_on` and `why not blocking`.
- The skill names `qa/follow-ups.md` as the ledger path and names the run owner as its only writer.
- The sentence "Preserve the highest severity rating when duplicates disagree" still appears in the file (the merge rule is deliberately unchanged in this stage); `grep -c "highest severity" src/superclaude/skills/task/SKILL.md` prints the same count as before the edit.
- The section "Post-Completion Validation (Final Phase Only)" names the sweep call and the offer once each, and `grep -n "sweep" src/superclaude/skills/task/SKILL.md` shows no other call site.
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still appears at each place it appears today, with the halt-offer text beside it.
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py -v` still passes (no pinned text moved).

## Task 3: Make tech-research write the ledger in shadow mode

Edit `src/superclaude/skills/tech-research/SKILL.md`: the same reviewer-brief fields (`rests_on` and `why not blocking`), ledger path `qa/follow-ups.md` next to the consolidated findings, the safety route and the shadow classifier call as Task 2. It gets no sweep call and no offer of its own: it runs inside `/task` (its step "Execution transfers to /task"), which owns the one sweep and the one offer at the end of the run. At each sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" in this file (today two checklist items of the task-file template in section A.7, near lines 490 and 555) add one sentence that the escalation's offer is the task skill's end-of-run offer, so a halt shows one offer and not two. Run `make sync-dev` afterwards.

Acceptance criteria:
- `src/superclaude/skills/tech-research/SKILL.md` names `qa/follow-ups.md` and the reviewer-brief fields, and `grep -n "sweep" src/superclaude/skills/tech-research/SKILL.md` prints nothing.
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still appears at each place it appears today, each with the one-offer sentence beside it.
- `uv run pytest tests/skills -k "tech_research or review_severity" -v` passes.


## Phase 3: Add the worker-contract keys and pin the reviewer briefs

## Task 4: Add the three follow-up keys to the worker contract

Edit `src/superclaude/core/WORKER-CONTRACT.md`: WC-4 (the bullet that enumerates the top-level keys, `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`) gains `follow_up_ledger` (path), `follow_up_counts` with `follow_up`, `note` and `show_user`, and `follow_up_capture_state` (`complete`, or `incomplete` with a reason); the status mapping maps `incomplete` capture to `worker_status: partial`; the coordinator duties (the bullet that says "the coordinator opens it") name the three keys as things to read; follow-ups alone never change `worker_status` from `succeeded`; the ledger is listed in `artifacts` only when it is a tracked path (WC-4 keeps gitignored paths out). Update `tests/skills/test_worker_contract.py` and add T10 cases.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` lists the three new keys in the bullet that enumerates top-level keys.
- `uv run pytest tests/skills/test_worker_contract.py -v` passes and a new test fails when a contract with `follow_up_capture_state: incomplete` is not mapped to `partial`.
- A test asserts an unattended run that records follow-ups makes no GitHub call and asks no question.

## Task 5: Pin the shadow-stage reviewer briefs

Depends on: Task 2, Task 3

Create `tests/skills/test_review_brief_rests_on.py` for T9: the reviewer brief of `src/superclaude/skills/task/SKILL.md` and of `src/superclaude/skills/tech-research/SKILL.md` must carry the `rests_on` and `why not blocking` fields. Also assert that the legacy definition text of `src/superclaude/output-styles/pragmatic.md` (the sentence "Grade every review finding as blocking or minor" and the bullets around it) is unchanged, while the registry row for `output-styles/pragmatic.md` in `src/superclaude/skills/sc-review-severity/refs/registry.yaml` is in state `legacy`; once that row is `v2` the assertion is skipped, so the stage 3 package's pragmatic.md task does not turn the test red.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_brief_rests_on.py -v` passes and fails when either field is removed from either skill.
- A test fails if the legacy definition text of `pragmatic.md` changes while its registry row is `legacy`, and a test shows the assertion is skipped when the row is set to `v2` in a temporary registry copy.


## Phase 4: Evaluate the classifier and write the owner summary

## Task 6: Evaluate the classifier on the stage 0 populations

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5

Run the classifier of the stage 1 modules (`superclaude review classify`, the `classifier_inputs.py` supplier, the question set v1) on the three sets the stage 0 package built, read by package id: the fresh-findings set (`./artifacts/fresh-findings.md`), the held-out half of the 318 rows (`./artifacts/stage0-heldout-ids.json`) and the reviewer-called-minor set (its ids in that file, its scores in `fresh-findings.md`, section for the Task 2 sample). The judge answers come from three blind agents that did not write the questions, three replicates each, recorded in fixture files; no Jev and no external service is called. Report each set separately and never pool them. Write `./artifacts/stage2-classifier-eval.md`: per set the agreement with the panel consensus, Cohen's kappa, the confusion matrix, recall on the panel's blockers, the flip rate over three replicates, the split by deliverable kind, the count of rows that had each code-supplied input (required-item list, constraint lines, verified evidence excerpt), and the limits. State that this is not an authority test (OD4).

Acceptance criteria:
- `./artifacts/stage2-classifier-eval.md` has one section per set (fresh findings, held-out half, reviewer-called-minor set) with the figures above, and no pooled figure.
- The three blind agents' ids are recorded and the file states none of them wrote the questions; the answer files are named and exist under `./artifacts/`.
- The file states that no judge other than the recorded blind agents was used, that no external service was called, and that no classifier authority follows (OD4).
- The file reports the count of rows per code-supplied input for each set, and each row where an input was not supplied has its answer recorded as UNSET or NA, never N.

## Task 7: Write the shadow summary script and the stage 2 owner summary

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers and prints the stage 2 exit numbers the spec defines in its section 12 stage 2 row (as edited by the stage 0 package: ledger volume per run, the share of rows tagged `consumer-unknown`, offers made and answered, the shadow agreement figures, the count of runs observed, the count of safety misses by the stage 0 definition, and the count of capture failures), with a test over fixture ledgers under `./artifacts/`. Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline from Task 6, the script's output over the shadow runs that exist so far (zero runs is a valid and stated result), the sweep and offer wiring results from Tasks 1 to 5, the limits, and the sentence that the owner's go for stage 3 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/shadow_summary.py` runs with `uv run python ./artifacts/shadow_summary.py --help` and its fixture test passes (the command and the pytest or script output are recorded in the summary).
- `./artifacts/stage2-summary-for-owner.md` names the headline of Tasks 1 to 6 with the file that holds it, states the number of shadow runs observed so far (zero is allowed), and states plainly that the stage 3 entry needs at least 5 observed runs with zero safety misses.
- The summary ends with the sentence that the owner's go for stage 3 is given in chat and not by this file.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:13-21

```markdown
## Stage ledger

| Stage | Request file | Base tasks (revised plan) | Package id | Owner go (date, where) |
|---|---|---|---|---|
| 0 Measurement | `stage0-request.md` | 1 to 10 | `TASK-WF-blockerStage0-20261116-021044` (generated 2026-11-16; its pre-execution review says NEEDS-REVISION, 2 blocking findings, so revise before running it) | not needed (no change under `src/`) |
| 1 Offline scaffold | `stage1-request.md` | 11 to 25 | | |
| 2 Shadow | `stage2-request.md` | 26 to 30 | | |
| 3 Pilot | `stage3-request.md` | 31 to 40 | | |
| 4 Propagation | `stage4-request.md` | 41 to 46 | | |
```

### .dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md:39-55

```markdown
| # | Blocking | Finding |
|---|---|---|
| F1 | yes | The three owner gates (four go points in PLAN:20) cannot be enforced: `/sc:implement` has no phase option, no pause path, ignores a plan edited after the first task, and QA anchors a constraint breach only in a diff. |
| F2 | yes | Task 31 only reports the seeded-recall result and Task 33 depends on it finishing, not passing. A stronger `Depends on` line would gate nothing because `/sc:implement` ignores it; only an acceptance line on Task 33 works, and Task 31 cannot move out of Phase 4. |
| F3 | yes | Task 40's allow-list names the plugin mirror of `rule.md` and requires every named file to exist, but Task 46 creates the mirror later; Task 13's allow-list text does not list it. |
| F4 | yes | Task 41 gives `agent_template_analysis.md` a digest and a `v2` registry row, but the registry has exactly 11 digest rows without it and the file has no definition sentence. |
| F5 | yes | Task 25's T3 check fails on `commands/spec-panel.md:220` (and its plugin twin, line 218, and the installed variants). |
| F6 | yes | Later tasks make earlier acceptance lines false (Tasks 16, 25, 27, 13), so the final review cannot pass and the package cannot archive. New, from the probe. |
| F7 | yes | The fresh-findings set and the held-out split are never evaluated by any task. |
| F8 | yes | "Safety miss" is defined nowhere, and the stage 2 and 3 exit numbers have no task that measures them, so the owner has no numbers to read at the gates. New, from the probe. |
| F9 | no | Task 46 copies the skill folder before adding the plugin `canonical` registry row (part of the F3 combined fix). |
| F10 | no | The seeded-recall pass line has no minimum sample size. |
| F11 | no | Task 31 does not alternate pass order or require fresh spawns. |
| F12 | no | T3 may fail a `pointer-only` row before its pointer exists. |
| F13 | no | Wording-dependent scan trips: `scale-map.md` naming the three phrases, `rule.md` quoting the old sentence. |
| F14 | no | Coverage-matrix omissions in the review run. |
| F15 | no | Installed reference files cite package-relative `.dev/` paths. |
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001: Generate it only after the stage 1 package's `./artifacts/stage1-summary-for-owner.md` has | Task 1 | covered | source.md:3 |
| INF-002: The old definition still decides every gate outcome in this stage. | Task 2 | covered | source.md:3 |
| INF-003: Reuse Tasks 26 to 30 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254 | none | covered | PLAN:12-14 header and Constraints PLAN:19-23 |
| INF-004: Stage 0 and stage 1 evidence is read by package id. | Task 6 | covered | source.md:7 |
| INF-005: State this is stage 2: the sweep only records (`promote` off), the classifier has no autho | Task 2 | covered | source.md:11 |
| INF-006: Stage 3 starts only after the owner reads this package's summary and says go; the stage 3  | Task 7 | covered | source.md:11 |
| INF-007: The halt-offer text goes beside each cap sentence in the task skill and in tech-research o | Task 2 | covered | source.md:12 |
| INF-008: Acceptance quotes the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to t | Task 2 | covered | source.md:12 |
| INF-009: Run the classifier of the stage 1 modules (`classify` command, `classifier_inputs.py` supp | Task 6 | covered | source.md:13 |
| INF-010: Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus, Cohen's | Task 6 | covered | source.md:13 |
| INF-011: State that it is not an authority test (OD4). | Task 6 | covered | source.md:13 |
| INF-012: Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shad | Task 7 | covered | source.md:14 |
| INF-013: Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline,  | Task 7 | covered | source.md:14 |
| INF-014: that a later task of the same package makes false get an end point. | none | covered | PLAN:24 (no acceptance line needs an end point today) |
| INF-015: No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, | none | partial | PLAN:22 names part of the list; no task or check covers rf-qa.md, rf-qa-qualitative.md, rf-analyst.md, templates, rule prompts |
| INF-016: Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 f | none | covered | PLAN:22 |
