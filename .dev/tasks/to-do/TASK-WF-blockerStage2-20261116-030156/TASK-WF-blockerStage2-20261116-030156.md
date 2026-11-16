---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-blockerStage2-20261116-030156
version: "1"
priority: Medium
created_date: "2026-11-16"
---

# Stage 2 plan: shadow beside the old rule for the blocker classification work (issue #552)

Source: ./source.md
Goal: Make the task skill and tech-research write the follow-up ledger, call the sweep once and make the once-per-run offer while the old definition still decides every gate outcome; add the worker-contract keys; evaluate the classifier on the stage 0 populations; and give the owner the stage 2 numbers before the stage 3 go.

## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 2 of five packages (one plan per stage). The old definition still decides every gate outcome: the sweep only records (`promote` off), the classifier has no authority, the one sweep call and the one offer sit in the task skill's "Post-Completion Validation (Final Phase Only)" and tech-research gets neither. It runs only after the stage 1 package is done (its modules `follow_ups.py`, `safety_route.py` and `sweep`'s inputs exist; Task 1 checks that) and the owner has said go in chat. Stage 3 starts only after the owner reads this package's summary and says go; its entry also needs at least 5 observed shadow runs, which the owner or operator produces over time and no task here can produce.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.

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
