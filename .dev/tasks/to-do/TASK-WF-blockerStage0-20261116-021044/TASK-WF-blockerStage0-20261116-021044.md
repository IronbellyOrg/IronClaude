---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-blockerStage0-20261116-021044
version: "1"
priority: Medium
created_date: "2026-11-16"
---

# Stage 0 plan: close the measurement stage for the blocker classification work (issue #552)

Source: ./source.md
Goal: The owner can read one file, `./artifacts/stage0-summary-for-owner.md`, and decide whether to say go for stage 1. This package measures, records and drafts definitions; it changes nothing under `src/`, `tests/`, `.claude/` or `plugins/`.

## Constraints

- One package, one stage. This is stage 0 of five packages (one plan per stage, the owner's decision of 2026-11-16). Stage 1 is generated and run only after the owner has read the stage 0 summary and said go in chat; no task here checks or records that go.
- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the blocker characteristics in `06-blocker-characteristics.md` and the classifier sketch in `07-classifier/`. The stage ledger and the other four stage requests are in PF `stage-requests/`.
- The only file outside `./artifacts/` that a task here edits is the spec file in PF (Task 9). Nothing under `src/`, `tests/`, `.claude/` or `plugins/` is edited.
- Program-folder files are read-only except the spec (Task 9). No task runs a script that writes beside itself inside PF: `08-test/evaluate.py` rewrites `08-test/results.md` in place (its line 110), so it runs only on a real copy (never a symlink) of `05-scoring/`, `07-classifier/` and `08-test/` made under `./artifacts/`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, any change to the own-scale primitives, code-assigned severity in `src/superclaude/cli/**/*.py`, the 35 percent score target, and any change to the cap of 2 fix cycles. No task of stages 1 to 4 is in this package.
- Classifier facts that bind every task that touches the classifier: the 5-run test of PF `08-test/results.md` used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. Confidence is reported as an ordinal band only, never as a probability.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. Python work uses UV only: `uv run python ...`, never `python -m` or bare `pip`.
- Measurement tasks that use blind agents record each agent id, and no agent that wrote the rule, the spec or the findings it grades is used as its own grader.

## Phase 1: Freeze the inventory and record what is already on file

## Task 1: Freeze the pattern inventory of spec section 10

Re-run, with plain `grep -rn` (not the Grep tool, which skips gitignored folders and so misses the project `.claude/` copies) over `src/superclaude`, `plugins/superclaude` and the project `.claude/` folder, every pattern the spec lists in section 10: the definition sentence `Grade every review finding as blocking or minor` (spec: 11 files), `Blocking is a real defect` (11), `Minor findings never fail a review` (11), `at most 2 fix cycles \(3 reviews\)` (12), `CRITICAL and IMPORTANT findings are blocking` (7), `follow-up candidates` (3 files, 7 lines), `2 fix cycles` (22 files, 120 lines), the two merge-rule patterns of section 10.3 (13 lines in 10 files), the tasklist pattern `High or Medium` and `Medium (blocking)` in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (7 lines), and the fixed FAIL-trigger patterns of REQ-30 (`= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT`) with one more pattern, `Any CRITICAL or IMPORTANT issue exists` (not in the spec; the review of the first plan found 8 lines in `src/superclaude/agents/rf-qa-qualitative.md` and 1 in `src/superclaude/templates/documents/agent_template_qa.md`), all over `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates` and `src/superclaude/rules`. Write the counts and every hit line to `./artifacts/stage0-inventory-freeze.md`.

Acceptance criteria:
- `./artifacts/stage0-inventory-freeze.md` exists and has one table row per pattern with the columns pattern, scope, spec count, observed count and difference.
- Every fixed FAIL-trigger pattern, including `Any CRITICAL or IMPORTANT issue exists`, has its hit lines (file, line number, text) listed, so later tasks use this list and not a remembered one.
- A section "Differences from the spec" lists each pattern whose observed count differs from the spec count; with no difference it says so in one line.
- The file records the exact commands used so the freeze can be re-run.

## Task 2: Run the retrospective escape test on run 2 (spec section 8.4, stage 0b)

Take a random sample, with a recorded seed, of de-duplicated minor findings from Gates 2 to 5 and the final validation in the run-2 QA folder `TASK-RESEARCH-review-panel-run2-20261114-075454/qa/` (the folder is under the repository's task folder; it holds the cycle-control files and lens reports). For each sampled finding, test by code whether its flawed text or figure appears uncorrected in the run-2 final report `RESEARCH-REPORT-review-panel-unification-run2.md` in the parent folder. Write the check as `./artifacts/stage0b_escape.py` (run with `uv run python`), the sample list as `./artifacts/stage0b-sample.md`, and the result as `./artifacts/stage0b-escape-test.md` with hits over n and a Wilson 95 percent interval. State the limit the spec names: the report was itself produced under the override, so a minor that was corrected anyway cannot be told apart from one that never mattered. Record the frame rules in `./artifacts/stage0b-escape-test.md` before the sample is drawn: how a minor finding is recognised in each kind of file in the folder (cycle-control files, analyst reports, fix logs, consolidated findings: name the heading or marker the code looks for in each kind), how duplicates are merged, how many files of each kind were used and how many skipped, and the rule the code uses to decide that a flaw appears uncorrected (the quoted text or figure is still present at its place in the final report).

Acceptance criteria:
- `./artifacts/stage0b-escape-test.md` reports hits, n, the seed and a Wilson 95 percent interval computed by `./artifacts/stage0b_escape.py`, and states the limit in one paragraph.
- Re-running `uv run python ./artifacts/stage0b_escape.py` with the recorded seed reproduces the same sample and the same count.
- n is at least 60 or equals the size of the whole frame when the frame is smaller; the file says which.
- `./artifacts/stage0b-sample.md` lists each sampled finding with its source file and the quoted flawed text or figure.
- `./artifacts/stage0b-escape-test.md` states the frame rules above and the counts of files used and skipped by kind, so the estimate does not rest on a choice nobody recorded.

## Task 3: Record stage 0 step 0a (the five runs on file)

Write `./artifacts/stage0a-result.md` from PF `08-test/results.md` and `08-test/evaluate.py`: the five runs of the stand-in LLM judge over the 318 scored rows, and how they were produced (a Claude judge on a text-only variant of the six questions, not Jev, same model family as the three scorers, questions finalised after reading the scored table). Report the figures the spec's section 7.6 asks for: agreement with the panel (58.5 percent by majority of the five runs), Cohen's kappa (0.27), the confusion matrix with counts (76, 126, 6 and 110), recall on the panel's blockers (92.7 percent), the split by deliverable kind (spec 52.6 percent, tasklist 65.3 percent), the flip rate (132 of 318 findings, 41.5 percent), the per-question separation (S, W and D near 0.73 to 0.75, M, C and E near chance) and the stated limits. Do not run `08-test/evaluate.py` in PF: it rewrites `08-test/results.md` in place (its line 110), and that file holds hand-added lines (the diagnosis from line 54, the kappa and per-kind tables from lines 83 to 89) that no script regenerates. Cite those figures from the file. To check that the generated part still reproduces, copy `05-scoring/`, `07-classifier/` and `08-test/` as real folders under `./artifacts/results-check/`, run `uv run python ./artifacts/results-check/08-test/evaluate.py` there, and compare its printed output with lines 1 to 52 of PF `08-test/results.md`; report any difference. Record the SHA-256 of PF `08-test/results.md` before and after this task, and its git blob id from `git hash-object` (it printed `d9616dd28fbb08daa565b11c69ef75cb7819f274` when this plan was reviewed); a hash detects a change but does not prevent one.

Acceptance criteria:
- `./artifacts/stage0a-result.md` contains each figure named above with its source line in PF `08-test/results.md` (kappa, the per-kind split and the per-question separation are hand-added and are cited from the file), and states whether lines 1 to 52 reproduced on the copy under `./artifacts/results-check/`, with any difference.
- `./artifacts/stage0a-result.md` records the SHA-256 of PF `08-test/results.md` before and after the task and the two are equal, and no `evaluate.py` run took place inside PF.
- The file states in one paragraph that this is not a Jev run, that the judge shares a model family with the scorers and that the questions were finalised after the table was read, so it measures consistency with the panel and not accuracy on new findings.
- The file states that no classifier authority follows from it (OD4).

## Phase 2: Re-grade and split the scored table

## Task 4: Re-grade the scored table under the old and the new rule text (spec stage 0c)

Depends on: Task 1

Use the 318 findings in PF `04-historical/master-table.md` through the blind copies `blind-table-1.md`, `blind-table-2.md` and `blind-table-3.md` in the same folder (columns ID, Category, Description brief, Context only). Spawn three blind agents that did not write the rule or the spec. Each re-grades every finding twice, in a paired design with the order of the two texts alternated: once under today's rule text (the lines of `src/superclaude/output-styles/pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet to the spec-panel scale bullet, today lines 221 to 231) and once under the digest of spec section 4.1 (REQ-01, the block between the quoted lines). Record each agent id and every grade in `./artifacts/stage0c-grades.jsonl` and write `./artifacts/stage0c-regrade.md` with the confusion matrix against the panel consensus in PF `05-scoring/consensus.md` (blocker at mean 4.0 or higher), how many findings graded blocking under the old text become non-blocking under the new text, the spread among the three agents, and the rows that moved from non-blocking to blocking. Every subagent in this session receives the installed output style, which holds the old rule, through the SubagentStart hook `pragmatic-subagent.js` (registered in `src/superclaude/hooks/hooks.json`), so the new-text arm is graded with the old rule still in its context. Tell each grader to apply only the rule text it is given, to quote the sentence it applied for each grade, and to ignore any other review-grading rule in its context; if a way to spawn graders without the injection exists, use it and record how. State the confound in the result file and report the movement counts as a lower bound on the change, because the confound biases them toward no change.

Acceptance criteria:
- `./artifacts/stage0c-grades.jsonl` has 318 findings times 3 agents times 2 texts, 1908 grades, each with agent id, text version and the order position.
- `./artifacts/stage0c-regrade.md` carries the confusion matrix with counts, the old-to-new movement counts and the three-agent spread, and states that the table holds only findings filed as blocking.
- The file lists the ids of the agents used and states that none of them wrote the digest or the spec.
- Rows the old text and the new text grade differently and that the panel calls a blocker are listed by id, since they are the recall risk.
- `./artifacts/stage0c-regrade.md` states the old-rule injection confound, how the graders were instructed, shows the quoted sentence each grader applied for a sample of grades, and reports the movement counts as a lower bound.

## Task 5: Split the scored table into a cluster-aware held-out set

Depends on: Task 2

Split the 318 findings of PF `04-historical/master-table.md` so that no defect cluster has rows on both sides. The clusters are the six keyword clusters of PF `06-blocker-characteristics.md` (the Phase 0 acceptance check that cannot pass, the `--unattended` flag landing before gates convert, the contract status vocabulary, the answer-as-flag and approval-gate rule, the git push classifier, and the missing `target_sha` on the resume path); that file names the clusters but not their keywords, and its keyword pass covered only the 82 blocker descriptions (43 rows). So first write the keywords of each cluster, apply them to all 318 rows, and group exact repeats (rows that cite the same defect: the same source path and the same quoted claim) into one group; each cluster and each group is placed whole on one side; rows in no cluster and no group are split at random with a recorded seed. Record the stage 0b sample of Task 2 (its ids only) as a separate third list, the reviewer-called-minor set; it is in neither half. Write `./artifacts/stage0-heldout-split.md` and `./artifacts/stage0-heldout-ids.json`. The fresh findings of Task 6 are a fourth population and are never placed in either half; Task 6 scores the Task 2 sample in the same blind pass, but the sample is counted once, here.

Acceptance criteria:
- `./artifacts/stage0-heldout-ids.json` lists the finding ids of the tuning half, the held-out half and the reviewer-called-minor set, with the seed.
- No cluster named in PF `06-blocker-characteristics.md` appears in both halves; the split file states each cluster's side.
- The two halves differ in size by at most 20 percent unless a cluster is too large to place, and the file says so when it is.
- The split file lists the keywords of each cluster and the number of rows each cluster and each repeat group holds across all 318 rows, and no repeat group appears in both halves.

## Phase 3: Build the new measurement sets

## Task 6: Build the fresh-findings set

Depends on: Task 2, Task 5

Build the population the reconciliation says must be tested apart from the 318 scored rows (spec section 7.6, weaknesses 1 and 2): findings that were not among them. Take the 17 merged findings of the pre-execution review of the first plan from `.dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/adversarial/merged-review-card.md` (each with its verified citations; the validator's two corrections are in `.dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/REPORT.md`) and score the reviewer-called-minor sample of Task 2 in the same blind pass, in its own section (the sample is listed by Task 5 in `./artifacts/stage0-heldout-ids.json` and is not counted in the fresh set's totals). Strip every label (severity, blocking flag, reviewer name) into a blind table with the columns ID, Category, Description brief, Context, as PF `04-historical/blind-table-1.md` does, spawn three blind scorer agents that did not write the findings, and have each score every finding from 1 (cosmetic or wording) through 3 (a real weakness the work survives) to 5 (a security, data-loss or safety-boundary risk, or the work cannot be done as written) and propose the lowest blocking score. Write the blind table, the three score files and the consensus (mean 4.0 or higher is a blocker, as in PF `05-scoring/consensus.md`) to `./artifacts/fresh-findings.md`.

Acceptance criteria:
- `./artifacts/fresh-findings.md` lists every finding of the fresh set (the 17 findings) and, in a separate section, every finding of the Task 2 sample, each with its three scores, the mean and the verdict, and states the count of each; the sample is not added to the fresh set's totals.
- The three scorers' agent ids are recorded and none of them reviewed the first plan.
- The file states that these findings are not among the 318 rows (a check of each finding's source file against the `Source path and line or heading` column of PF `04-historical/master-table.md` finds none; the ids cannot be compared because the two sets use different id formats) and that they are held out from tuning.
- The file states that the second evaluation of the classifier on this population needs the stage 1 package's classifier-inputs supplier and a recorded judge, that it is run by the stage 2 package's classifier-evaluation task (which reads this file from this package by package id), and that it is not run here.

## Task 7: Define and size the seeded-defect recall set (spec section 8.3)

Plant known defects in a held-out deliverable so a later task can measure recall under the old and the new rule text. The four classes are a decision-bearing false claim, a missing required section, a safety risk and a cosmetic defect. The held-out deliverable is a fresh short spec written for this purpose under `./artifacts/seeded/` (not a document any rule text was tuned on; the spec notes the 44-defect spec ledger named in the run-2 scope file as a sanity check only, because the whole #346 series was tuned on it). Size the set so a 5-point change in recall is visible: state the arithmetic (with n planted defects per class, the Wilson 95 percent half-width at the expected recall) and state a minimum n per gating class (safety, decision-bearing, missing) so the half-width is at most 5 points at the expected recall, and plant at least that many defects of each gating class. Where the deliverable cannot hold that many, state the n reached, the interval that results, and that the recall pass line for that class is advisory for the owner. Compute the n that gives a 5-point Wilson half-width at expected recalls of 0.90 and 0.95 (the review of this plan estimated about 140 and about 83 planted defects) and state whether the deliverable can hold that many; if it cannot, the advisory fallback is the expected outcome and the file says so. State also that the stage 3 package runs each pass (old rule text, new rule text) with freshly spawned agents and alternates the pass order across the three reviewers. Write the sizing argument and the planted-defect list (class, location, the planted text and the correct text, and the consumer a reviewer should name) to `./artifacts/seeded-recall-set.md`, and keep the answer key separate from what reviewers read.

Acceptance criteria:
- `./artifacts/seeded-recall-set.md` holds the sizing argument with the numbers and the planted-defect list with at least one defect in each of the four classes.
- The file states a minimum n for each gating class and the Wilson half-width it gives, or marks that class's pass line advisory and shows the interval the owner will see.
- The planted deliverable exists under `./artifacts/seeded/` and the answer key is in a file reviewers are never given (named in `./artifacts/seeded-recall-set.md`).
- The file states the three spec requirements the run must meet (safety recall equals the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the share of cosmetic items that block falls) and that the stage 3 package runs the set.

## Task 8: Report which code-supplied classifier inputs the scored rows had

Count, over the 318 findings of PF `04-historical/master-table.md`, how many rows had each of the three inputs the classifier needs for the missing-item (M), constraint (C) and contradiction (E) questions: a required-item list reachable from the row's source deliverable, quoted constraint lines, and an evidence excerpt that re-reads true at its cited line. A row counts for the evidence input only when the location its `Source path and line or heading` column cites exists and holds the quote its `Evidence` column gives (the Evidence column holds short quotes, not paths: check what each column holds before applying the rule). Rows whose path starts with `@E2` were read with `git show` from the branch `origin/ironbelly/eval-tasklist-review-panel` and do not exist in this worktree: resolve them as PF `01-historical-inventory.md` explains in its legend for `@E2` and the abbreviated paths, using `git show`, and report separately how many rows were checked that way and how many could not be resolved; the table carries neither a required-item list nor constraint lines, so those two are expected to be zero (the task confirms this by sampling at least 30 rows and reading their source deliverables). Write the counts, the sampling method and the three suppliers the classifier will need to the file `./artifacts/classifier-input-availability.md`.

Acceptance criteria:
- `./artifacts/classifier-input-availability.md` states three counts out of 318 (required-item list, constraint lines, verified evidence excerpt) and how each was obtained.
- It lists the 30 or more sampled rows and, for each, whether a required-item list and constraint lines could have been supplied by reading its source deliverable.
- It reports separately the rows resolved through git (`@E2` rows) and the rows that could not be resolved, and states what the Evidence column holds.
- It states that, with these counts, the M, C and E questions could not have been asked on the scored table without a supplier, which the stage 1 package builds.

## Phase 4: Reconcile the spec and write the owner summary

## Task 9: Correct the stale statements in the spec

Depends on: Task 4, Task 5, Task 8

Edit PF `02-brainstorm/merged-requirements.md` where the program results made it stale, and write the list of edits to `./artifacts/spec-reconciliation.md`. The edits: the thresholds bullet of section 7.4 (the sentence that says 30 to 40 rows leave a held-out half of 15 to 20 rows; the table has 318 rows and the held-out half is the set of Task 5); the "Missing table" row and the "Table" row of the section 7.6 table (the table exists and scored 318 findings with threshold 4); stage 0 of the section 12 table (steps 0a and 0c are not skipped); the section 14 risk RK8 ("Over-fitting the classifier to 30 to 40 rows", spec line 1011) and the section 17.3 line about "a calibration table of 30 or more scored findings" (spec line 1108), both stale because the table exists and has 318 rows; and any other line of section 17 or Appendix A that says the table is empty or absent (a Grep for "empty" found none when this plan was written; the task re-runs it and records what it finds in `./artifacts/spec-reconciliation.md`). Add one sentence to section 7.2 that M, C and E are answerable only with code-supplied inputs, citing PF `08-test/results.md` and `./artifacts/classifier-input-availability.md` (those questions were at chance in the text-only variant). Then draft three further edits, each marked in the spec as "proposed, for owner acceptance at the stage 1 go": (a) in the section 12 table, a definition of "safety miss" for the stage 3 entry count: a finding that a later review or the owner confirms is a security, data-loss or safety-boundary risk that a shadow run recorded as a follow-up or Note and did not route through the GR12 safety route; (b) in the section 12 stage 2 row, the exit numbers made measurable: ledger volume per run, the share of rows tagged `consumer-unknown`, offers made and answered, and the shadow agreement figures of the classifier against the reviewers' labels; (c) in the section 12 stage 3 row, a pointer to the revert triggers RT1 and RT2 of section 13.2 and metric M12 of section 13.1 as the audit-window numbers (quote their existing text; do not redefine them). Also record, in sections 10 and 12 of the spec, three staging decisions: the merge-rule allow-list in `refs/scale-map.md` lists files by path only and the plugin mirror joins it only in stage 4; `agent_template_analysis.md` gets the merge-rule text only and the registry keeps exactly 11 `digest` rows; T3's `src/superclaude` check applies to `digest` and `canonical` rows only and a `pointer-only` row is checked only once its pointer is present.

Acceptance criteria:
- The spec no longer says the scored table is empty, will not exist in time, or has 30 to 40 rows, or that the held-out half is 15 to 20 rows (`grep -n "15 to 20\|was empty\|30 to 40 rows\|30 or more scored"` over the spec returns no stale claim).
- `./artifacts/spec-reconciliation.md` lists each edited line with its old and new text.
- Section 7.2 of the spec carries the M, C and E sentence with a pointer to `08-test/results.md`.
- The spec holds three markers "proposed, for owner acceptance at the stage 1 go" (`grep -c` of that phrase over the spec prints 3 or more), one each for the safety-miss definition, the stage 2 exit numbers and the stage 3 pointer, and the section 12 stage 3 row names RT1, RT2 and M12.
- The spec records the three staging decisions (allow-list by path only with the mirror joining in stage 4, analysis template merge-rule text only with exactly 11 digest rows, T3 scope), and `./artifacts/spec-reconciliation.md` lists each of these edits with its old and new text.

## Task 10: Write the stage 0 results for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Write `./artifacts/stage0-summary-for-owner.md`, the one file the owner reads before saying go for stage 1. For each of Tasks 1 to 9 give its artifact path and its headline result in one or two lines: the inventory differences from the spec (Task 1), the escape estimate with its interval (Task 2), the five-run figures and their limits (Task 3), the old-to-new movement counts and the recall-risk rows (Task 4), the split and the held-out sizes (Task 5), the fresh-findings count and verdicts (Task 6), the seeded-recall set size and its limits (Task 7), the input-availability counts (Task 8) and the spec edits (Task 9). State every limit the tasks recorded (stand-in judge, circular labels, selection bias, the table holds only findings filed as blocking, and the old-rule injection confound of Task 4 next to its movement counts), and list the owner decisions this stage touches (OD3 for any later external judge; OD4 authority none). Add four things for the owner: the drafted definitions of Task 9 (safety miss, stage 2 exit numbers, stage 3 pointer) to accept or change, the three staging decisions, the stage ledger of `stage-requests/README.md` in PF (which stage packages exist and which owner gos are recorded), and the five findings of this stage that matter most for the stage 1 go. End with the sentence that the owner's go for stage 1 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/stage0-summary-for-owner.md` names the artifact path and the headline number or result for each of Tasks 1 to 9, and each path exists.
- The file lists the limits of each result and says nowhere that a result proves the classifier works.
- The file lists the drafted definitions and the three staging decisions, and names the stage ledger file.
- The file lists OD3 and OD4 and the five findings of this stage that matter most for the stage 1 go, and carries the Task 4 confound sentence next to the movement counts.
- The file names this package id `TASK-WF-blockerStage0-20261116-021044` in its ledger section and states the stage 0 row of PF `stage-requests/README.md` as read; the row already names this package id and no task edits that file.
- The file ends with the sentence that the owner's go for stage 1 is given in chat and not by this file.
