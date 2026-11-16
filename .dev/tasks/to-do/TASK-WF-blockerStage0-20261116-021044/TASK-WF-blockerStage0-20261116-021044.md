---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-blockerStage0-20261116-021044
version: "1"
priority: Medium
created_date: "2026-11-16"
---

# Stage 0 plan: freeze the inventory, re-grade the scored table and correct the spec for the blocker classification work (issue #552)

Source: ./source.md
Goal: The owner can read one file, `./artifacts/stage0c-regrade.md`, and decide whether to say go for the next stage. This package freezes the pattern inventory, re-grades the scored table under the old and the new rule text, and writes a short errata note for the spec. It changes nothing under `src/`, `tests/`, `.claude/` or `plugins/`; the one file outside `./artifacts/` it edits is the spec.

## Constraints

- One package, one stage. This is stage 0 of the four packages that remain after the cuts debate of 2026-11-16 (the stage 2 package was merged into stage 1; the authoritative list is `cuts-debate/final-cuts.md` in the program folder). Stage 1 is generated and run only after the owner has read `./artifacts/stage0c-regrade.md` and said go in chat; no task here checks or records that go.
- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md` and the stage ledger and stage requests in `stage-requests/`.
- The only file outside `./artifacts/` that a task here edits is the spec file in PF (Task 3). Nothing under `src/`, `tests/`, `.claude/` or `plugins/` is edited.
- Program-folder files are read-only except the spec (Task 3). No task runs a script that writes beside itself inside PF: `08-test/evaluate.py` rewrites `08-test/results.md` in place (its line 110), so it is never run inside PF and runs only on a real copy (never a symlink) made under `./artifacts/`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says otherwise. Staging is not committing.
- Owner decisions use the spec's recommendations unless the owner changes them (they are recommendations pending the owner, not owner answers): OD1 no new skill folder; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files; OD12 yes; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD16 option (b) at stage 3. OD3 (finding text leaving the machine) stays open and is not decided here; OD5 to OD8, OD10, OD13, OD15 and OD17 are not decided here either, and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, any change to the own-scale primitives, code-assigned severity in `src/superclaude/cli/**/*.py`, the 35 percent score target, and any change to the cap of 2 fix cycles. No task of stages 1 to 4 is in this package.
- Figures the tasks may cite, from `08-test/results.md` and `05-scoring/consensus.md`: 82 of the 318 scored findings are panel blockers, the stand-in judge of the 5-run test agreed with the panel on 58.5 percent (Cohen's kappa 0.27), and the questions S, W and D separated at an area under the curve of 0.73 to 0.75. Nothing here reports a classifier probability or claims that a result proves a classifier works.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. Python work uses UV only: `uv run python ...`, never `python -m` or bare `pip`.
- Measurement tasks that use blind agents record each agent id, and no agent that wrote the rule, the spec or the findings it grades is used as its own grader.

## Phase 1: Freeze the inventory

## Task 1: Freeze the pattern inventory of spec section 10

Re-run, with plain `grep -rn` (not the Grep tool, which skips gitignored folders and so misses the project `.claude/` copies) over `src/superclaude`, `plugins/superclaude` and the project `.claude/` folder, every pattern the spec lists in section 10: the definition sentence `Grade every review finding as blocking or minor` (spec: 11 files), `Blocking is a real defect` (11), `Minor findings never fail a review` (11), `at most 2 fix cycles \(3 reviews\)` (12), `CRITICAL and IMPORTANT findings are blocking` (7), `follow-up candidates` (3 files, 7 lines), `2 fix cycles` (22 files, 120 lines), the two merge-rule patterns of section 10.3 (13 lines in 10 files), the tasklist pattern `High or Medium` and `Medium (blocking)` in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (7 lines), and the fixed FAIL-trigger patterns of REQ-30 (`= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT`) with one more pattern, `Any CRITICAL or IMPORTANT issue exists` (not in the spec; the review of the first plan found 8 lines in `src/superclaude/agents/rf-qa-qualitative.md` and 1 in `src/superclaude/templates/documents/agent_template_qa.md`), all over `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates` and `src/superclaude/rules`. Write the counts and every hit line to `./artifacts/stage0-inventory-freeze.md`.

Acceptance criteria:
- `./artifacts/stage0-inventory-freeze.md` exists and has one table row per pattern with the columns pattern, scope, spec count, observed count and difference.
- Every fixed FAIL-trigger pattern, including `Any CRITICAL or IMPORTANT issue exists`, has its hit lines (file, line number, text) listed, so later tasks use this list and not a remembered one.
- A section "Differences from the spec" lists each pattern whose observed count differs from the spec count; with no difference it says so in one line.
- The file records the exact commands used so the freeze can be re-run.

## Phase 2: Re-grade the scored table and write the owner-readable result

## Task 2: Re-grade the scored table under the old and the new rule text (spec stage 0c)

Depends on: Task 1

Use the 318 findings in PF `04-historical/master-table.md` through the blind copies `blind-table-1.md`, `blind-table-2.md` and `blind-table-3.md` in the same folder (columns ID, Category, Description brief, Context only). Spawn three blind agents that did not write the rule or the spec. Each re-grades every finding twice, in a paired design with the order of the two texts alternated: once under today's rule text (the lines of `src/superclaude/output-styles/pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet to the spec-panel scale bullet, today lines 221 to 231) and once under the digest of spec section 4.1 (REQ-01, the block between the quoted lines). Record each agent id and every grade in `./artifacts/stage0c-grades.jsonl` and write `./artifacts/stage0c-regrade.md` with the confusion matrix against the panel consensus in PF `05-scoring/consensus.md` (blocker at mean 4.0 or higher), how many findings graded blocking under the old text become non-blocking under the new text, the spread among the three agents, and the rows that moved from non-blocking to blocking. Every subagent in this session receives the installed output style, which holds the old rule, through the SubagentStart hook `pragmatic-subagent.js` (registered in `src/superclaude/hooks/hooks.json`), so the new-text arm is graded with the old rule still in its context. Tell each grader to apply only the rule text it is given, to quote the sentence it applied for each grade, and to ignore any other review-grading rule in its context; if a way to spawn graders without the injection exists, use it and record how. State the confound in the result file and report the movement counts as a lower bound on the change, because the confound biases them toward no change.

`./artifacts/stage0c-regrade.md` is also the owner-readable result of this package. Besides the matrix and the counts it holds: the limits of the result (the stand-in judge of the 5-run test, circular labels, selection bias, and that the table holds only findings filed as blocking); the old-rule injection confound stated next to the movement counts; a statement that the regrade is a lower bound and cannot measure discovery, because it grades findings that were supplied and cannot tell whether a reviewer would have found a defect, and that RT1 (spec section 13.2), the owner's read of the first five runs' Medium lists and one small planted-defect check run as part of the live RT1 audit after the switch cover what it cannot; and the owner decisions it touches (OD3, finding text leaving the machine for any later external judge, still open; OD4, no classifier authority in version 1). It ends with the sentence that the owner's go for the next stage is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/stage0c-grades.jsonl` has 318 findings times 3 agents times 2 texts, 1908 grades, each with agent id, text version and the order position.
- `./artifacts/stage0c-regrade.md` carries the confusion matrix with counts, the old-to-new movement counts and the three-agent spread, and states that the table holds only findings filed as blocking.
- The file lists the ids of the agents used and states that none of them wrote the digest or the spec.
- Rows the old text and the new text grade differently and that the panel calls a blocker are listed by id, since they are the recall risk.
- `./artifacts/stage0c-regrade.md` states the old-rule injection confound, how the graders were instructed, shows the quoted sentence each grader applied for a sample of grades, and reports the movement counts as a lower bound.
- The file states that the regrade is a lower bound and cannot measure discovery, and names RT1, the read of the first five runs' Medium lists and the small planted-defect check as what covers the rest.
- The file lists the limits of the result (stand-in judge, circular labels, selection bias, the table holds only findings filed as blocking), carries the old-rule injection confound next to the movement counts, lists OD3 and OD4, and says nowhere that a result proves a classifier works.
- The file ends with the sentence that the owner's go for the next stage is given in chat and not by this file.

## Phase 3: Correct the stale statements in the spec

## Task 3: Write the spec errata note

Depends on: Task 1, Task 2

Edit PF `02-brainstorm/merged-requirements.md` only where the program results made it stale, and write the list of edits to `./artifacts/spec-reconciliation.md` with the old and the new text of each edited line. The edits:

- The thresholds bullet of section 7.4 (the sentence that says 30 to 40 rows leave a held-out half of 15 to 20 rows): reword it without a held-out set; the table has 318 rows.
- The "Missing table" row and the "Table" row of the section 7.6 table (the table exists and scored 318 findings with threshold 4).
- Stage 0 of the section 12 table (steps 0a and 0c are not conditional on the table existing; it exists).
- The section 14 risk RK8 ("Over-fitting the classifier to 30 to 40 rows", spec line 1011) and the section 17.3 line about "a calibration table of 30 or more scored findings" (spec line 1108), both stale because the table exists and has 318 rows; and any other line of section 17 or Appendix A that says the table is empty or absent (a Grep for "empty" found none when this plan was written; the task re-runs it and records what it finds, or "none found", in `./artifacts/spec-reconciliation.md`).
- One sentence in section 7.2 that M, C and E are answerable only with code-supplied inputs, citing PF `08-test/results.md` only (those questions were at chance in the text-only variant).
- The RT1 row of section 13.2 (spec line 985) reworded to "any real blocker found in a Medium list": a single event that needs no sample size, replacing the wording that names the seeded set and a plain follow-up.
- The RK15 mitigation at spec line 1018: drop `M10b` from the list that ends the mitigation text.
- The section 12 stage 3 row: its exit condition names RT1 and no longer names M12 ("M12 reported" is dropped from that cell); RT2 is not named.
- One line directly under the `Date:` line near the top of the spec: "Version 1 scope: see cuts-debate/final-cuts.md in this folder".

No other line of the spec is edited and no definition, exit number or staging decision is drafted into it; the spec sections that describe cut machinery stay as written and the scope line points the reader to the cuts list.

Acceptance criteria:
- The spec no longer says the scored table is empty, will not exist in time, or has 30 to 40 rows, or that the held-out half is 15 to 20 rows (`grep -n "15 to 20\|was empty\|30 to 40 rows\|30 or more scored"` over the spec returns no stale claim).
- `./artifacts/spec-reconciliation.md` lists each edited line with its old and new text, and records the result of the re-run Grep over section 17 and Appendix A.
- Section 7.2 of the spec carries the M, C and E sentence with a pointer to `08-test/results.md` and no pointer to a file of this package.
- The RT1 row of section 13.2 reads "any real blocker found in a Medium list", the RK15 mitigation no longer contains `M10b`, and the section 12 stage 3 row names RT1 and does not name RT2 or M12.
- The spec carries the one line "Version 1 scope: see cuts-debate/final-cuts.md in this folder" once, directly under the `Date:` line, and the file `cuts-debate/final-cuts.md` exists in PF.
