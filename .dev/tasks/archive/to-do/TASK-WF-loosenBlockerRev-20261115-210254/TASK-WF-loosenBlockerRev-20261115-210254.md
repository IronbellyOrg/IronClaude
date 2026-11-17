---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-loosenBlockerRev-20261115-210254
version: "1"
priority: Medium
created_date: "2026-11-15"
---

# Loosen blocker classification across the review loops, revised plan (issue #552)

Source: ./source.md
Goal: Review gates grade each finding by what changes if the flawed text is corrected, record every non-blocking finding in a follow-up ledger with a once-per-run offer to file them, keep security, data-loss and safety findings blocking, and measure a blocker classifier in shadow mode without giving it any authority. This plan revises the first plan after its pre-execution review found 12 blocking defects.

## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the blocker characteristics in `06-blocker-characteristics.md` and the classifier sketch in `07-classifier/`.
- Owner gates. Phase 1 is stage 0 (measurement, no change under `src/`). Phase 2 (stage 1, offline scaffold) starts only after the owner has read the stage 0 results (Task 10 writes them in one file) and said go in chat. Phase 3 (stage 2, shadow) starts only after the stage 1 exit (every Phase 2 acceptance check green) and the owner's say-so. Phase 4 (stage 3, the pilot) starts only after the owner says so; its entry conditions per spec section 12 also need at least 5 observed shadow runs with zero safety misses and no capture failure (the owner or operator runs those shadow runs over time; no task here can produce them), the seeded-recall result of Task 31 and stage 0c (Task 4). Phase 5 (stage 4) starts only after the owner says so after the pilot's audit window. Run `/sc:implement` on one phase at a time and stop at each gate.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
- Classifier facts that bind every classifier task: the 5-run test of PF `08-test/results.md` used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (Task 20 builds the supplier), the "M or C is Y gives BLOCKING" row is never enabled for any gate in this plan, and confidence is reported as an ordinal band, never as a probability.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package.

## Phase 1: Close the measurement stage (stage 0)

## Task 1: Freeze the pattern inventory of spec section 10

Re-run, with plain `grep -rn` (not the Grep tool, which skips gitignored folders and so misses the project `.claude/` copies) over `src/superclaude`, `plugins/superclaude` and the project `.claude/` folder, every pattern the spec lists in section 10: the definition sentence `Grade every review finding as blocking or minor` (spec: 11 files), `Blocking is a real defect` (11), `Minor findings never fail a review` (11), `at most 2 fix cycles \(3 reviews\)` (12), `CRITICAL and IMPORTANT findings are blocking` (7), `follow-up candidates` (3 files, 7 lines), `2 fix cycles` (22 files, 120 lines), the two merge-rule patterns of section 10.3 (13 lines in 10 files), the tasklist pattern `High or Medium` and `Medium (blocking)` in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (7 lines), and the fixed FAIL-trigger patterns of REQ-30 (`= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT`) with one more pattern, `Any CRITICAL or IMPORTANT issue exists` (not in the spec; the review of the first plan found 8 lines in `src/superclaude/agents/rf-qa-qualitative.md` and 1 in `src/superclaude/templates/documents/agent_template_qa.md`), all over `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates` and `src/superclaude/rules`. Write the counts and every hit line to `./artifacts/stage0-inventory-freeze.md`.

Acceptance criteria:
- `./artifacts/stage0-inventory-freeze.md` exists and has one table row per pattern with the columns pattern, scope, spec count, observed count and difference.
- Every fixed FAIL-trigger pattern, including `Any CRITICAL or IMPORTANT issue exists`, has its hit lines (file, line number, text) listed, so later tasks use this list and not a remembered one.
- A section "Differences from the spec" lists each pattern whose observed count differs from the spec count; with no difference it says so in one line.
- The file records the exact commands used so the freeze can be re-run.

## Task 2: Run the retrospective escape test on run 2 (spec section 8.4, stage 0b)

Take a random sample, with a recorded seed, of de-duplicated minor findings from Gates 2 to 5 and the final validation in the run-2 QA folder `TASK-RESEARCH-review-panel-run2-20261114-075454/qa/` (the folder is under the repository's task folder; it holds the cycle-control files and lens reports). For each sampled finding, test by code whether its flawed text or figure appears uncorrected in the run-2 final report `RESEARCH-REPORT-review-panel-unification-run2.md` in the parent folder. Write the check as `./artifacts/stage0b_escape.py` (run with `uv run python`), the sample list as `./artifacts/stage0b-sample.md`, and the result as `./artifacts/stage0b-escape-test.md` with hits over n and a Wilson 95 percent interval. State the limit the spec names: the report was itself produced under the override, so a minor that was corrected anyway cannot be told apart from one that never mattered.

Acceptance criteria:
- `./artifacts/stage0b-escape-test.md` reports hits, n, the seed and a Wilson 95 percent interval computed by `./artifacts/stage0b_escape.py`, and states the limit in one paragraph.
- Re-running `uv run python ./artifacts/stage0b_escape.py` with the recorded seed reproduces the same sample and the same count.
- n is at least 60 or equals the size of the whole frame when the frame is smaller; the file says which.
- `./artifacts/stage0b-sample.md` lists each sampled finding with its source file and the quoted flawed text or figure.

## Task 3: Record stage 0 step 0a (the five runs on file)

Write `./artifacts/stage0a-result.md` from PF `08-test/results.md` and `08-test/evaluate.py`: the five runs of the stand-in LLM judge over the 318 scored rows, and how they were produced (a Claude judge on a text-only variant of the six questions, not Jev, same model family as the three scorers, questions finalised after reading the scored table). Report the figures the spec's section 7.6 asks for: agreement with the panel (58.5 percent by majority of the five runs), Cohen's kappa (0.27), the confusion matrix with counts (76, 126, 6 and 110), recall on the panel's blockers (92.7 percent), the split by deliverable kind (spec 52.6 percent, tasklist 65.3 percent), the flip rate (132 of 318 findings, 41.5 percent), the per-question separation (S, W and D near 0.73 to 0.75, M, C and E near chance) and the stated limits. Re-run `uv run python 08-test/evaluate.py` from PF first and confirm the figures still match the file; if they differ, report the new figures and say so.

Acceptance criteria:
- `./artifacts/stage0a-result.md` contains each figure named above with its source line in PF `08-test/results.md`, or the re-run value and a note that it differs.
- The file states in one paragraph that this is not a Jev run, that the judge shares a model family with the scorers and that the questions were finalised after the table was read, so it measures consistency with the panel and not accuracy on new findings.
- The file states that no classifier authority follows from it (OD4).

## Task 4: Re-grade the scored table under the old and the new rule text (spec stage 0c)

Depends on: Task 1

Use the 318 findings in PF `04-historical/master-table.md` through the blind copies `blind-table-1.md`, `blind-table-2.md` and `blind-table-3.md` in the same folder (columns ID, Category, Description brief, Context only). Spawn three blind agents that did not write the rule or the spec. Each re-grades every finding twice, in a paired design with the order of the two texts alternated: once under today's rule text (the lines of `src/superclaude/output-styles/pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet to the spec-panel scale bullet, today lines 221 to 231) and once under the digest of spec section 4.1 (REQ-01, the block between the quoted lines). Record each agent id and every grade in `./artifacts/stage0c-grades.jsonl` and write `./artifacts/stage0c-regrade.md` with the confusion matrix against the panel consensus in PF `05-scoring/consensus.md` (blocker at mean 4.0 or higher), how many findings graded blocking under the old text become non-blocking under the new text, the spread among the three agents, and the rows that moved from non-blocking to blocking.

Acceptance criteria:
- `./artifacts/stage0c-grades.jsonl` has 318 findings times 3 agents times 2 texts, 1908 grades, each with agent id, text version and the order position.
- `./artifacts/stage0c-regrade.md` carries the confusion matrix with counts, the old-to-new movement counts and the three-agent spread, and states that the table holds only findings filed as blocking.
- The file lists the ids of the agents used and states that none of them wrote the digest or the spec.
- Rows the old text and the new text grade differently and that the panel calls a blocker are listed by id, since they are the recall risk.

## Task 5: Split the scored table into a cluster-aware held-out set

Depends on: Task 2

Split the 318 findings of PF `04-historical/master-table.md` so that no defect cluster has rows on both sides. The clusters are the six keyword clusters of PF `06-blocker-characteristics.md` (the Phase 0 acceptance check that cannot pass, the `--unattended` flag landing before gates convert, the contract status vocabulary, the answer-as-flag and approval-gate rule, the git push classifier, and the missing `target_sha` on the resume path); rows in no cluster are split at random with a recorded seed. Add the stage 0b sample of Task 2 as a separate set of findings that a reviewer called minor. Write `./artifacts/stage0-heldout-split.md` and `./artifacts/stage0-heldout-ids.json`. The fresh findings of Task 6 are a third population and are never placed in either half.

Acceptance criteria:
- `./artifacts/stage0-heldout-ids.json` lists the finding ids of the tuning half, the held-out half and the reviewer-called-minor set, with the seed.
- No cluster named in PF `06-blocker-characteristics.md` appears in both halves; the split file states each cluster's side.
- The two halves differ in size by at most 20 percent unless a cluster is too large to place, and the file says so when it is.

## Task 6: Build the fresh-findings set

Depends on: Task 2, Task 5

Build the population the reconciliation says must be tested apart from the 318 scored rows (spec section 7.6, weaknesses 1 and 2): findings that were not among them. Take the 17 merged findings of the pre-execution review of the first plan from `.dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/adversarial/merged-review-card.md` (each with its verified citations; the validator's two corrections are in `.dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/REPORT.md`) and add the reviewer-called-minor sample of Task 2. Strip every label (severity, blocking flag, reviewer name) into a blind table with the columns ID, Category, Description brief, Context, as PF `04-historical/blind-table-1.md` does, spawn three blind scorer agents that did not write the findings, and have each score every finding from 1 (cosmetic or wording) through 3 (a real weakness the work survives) to 5 (a security, data-loss or safety-boundary risk, or the work cannot be done as written) and propose the lowest blocking score. Write the blind table, the three score files and the consensus (mean 4.0 or higher is a blocker, as in PF `05-scoring/consensus.md`) to `./artifacts/fresh-findings.md`.

Acceptance criteria:
- `./artifacts/fresh-findings.md` lists every finding with its three scores, the mean and the verdict, and states how many came from each source.
- The three scorers' agent ids are recorded and none of them reviewed the first plan.
- The file states that these findings are not among the 318 rows (a check of each ID against PF `04-historical/master-table.md` finds none) and that they are held out from tuning.
- The file states that the second evaluation of the classifier on this population needs the Task 20 supplier and a recorded judge, and is run at stage 2, not here.

## Task 7: Define and size the seeded-defect recall set (spec section 8.3)

Plant known defects in a held-out deliverable so a later task can measure recall under the old and the new rule text. The four classes are a decision-bearing false claim, a missing required section, a safety risk and a cosmetic defect. The held-out deliverable is a fresh short spec written for this purpose under `./artifacts/seeded/` (not a document any rule text was tuned on; the spec notes the 44-defect spec ledger named in the run-2 scope file as a sanity check only, because the whole #346 series was tuned on it). Size the set so a 5-point change in recall is visible: state the arithmetic (with n planted defects per class, the Wilson 95 percent half-width at the expected recall) and choose n per class so the half-width is at most 5 points for the classes that gate (safety, decision-bearing, missing), or state plainly which classes cannot reach it and why. Write the sizing argument and the planted-defect list (class, location, the planted text and the correct text, and the consumer a reviewer should name) to `./artifacts/seeded-recall-set.md`, and keep the answer key separate from what reviewers read.

Acceptance criteria:
- `./artifacts/seeded-recall-set.md` holds the sizing argument with the numbers and the planted-defect list with at least one defect in each of the four classes.
- The planted deliverable exists under `./artifacts/seeded/` and the answer key is in a file reviewers are never given (named in `./artifacts/seeded-recall-set.md`).
- The file states the three spec requirements the run must meet (safety recall equals the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the share of cosmetic items that block falls) and that Task 31 runs the set.

## Task 8: Report which code-supplied classifier inputs the scored rows had

Count, over the 318 findings of PF `04-historical/master-table.md`, how many rows had each of the three inputs the classifier needs for the missing-item (M), constraint (C) and contradiction (E) questions: a required-item list reachable from the row's source deliverable, quoted constraint lines, and an evidence excerpt that re-reads true at its cited line. A row counts for the evidence input only when the cited path and line in its `Evidence` column exist and hold the quoted text; the table carries neither a required-item list nor constraint lines, so those two are expected to be zero (the task confirms this by sampling at least 30 rows and reading their source deliverables). Write the counts, the sampling method and the three suppliers the classifier will need to the file `./artifacts/classifier-input-availability.md`.

Acceptance criteria:
- `./artifacts/classifier-input-availability.md` states three counts out of 318 (required-item list, constraint lines, verified evidence excerpt) and how each was obtained.
- It lists the 30 or more sampled rows and, for each, whether a required-item list and constraint lines could have been supplied by reading its source deliverable.
- It states that, with these counts, the M, C and E questions could not have been asked on the scored table without a supplier, which Task 20 builds.

## Task 9: Correct the stale statements in the spec

Depends on: Task 4, Task 5, Task 8

Edit PF `02-brainstorm/merged-requirements.md` where the program results made it stale, and write the list of edits to `./artifacts/spec-reconciliation.md`. The edits: the thresholds bullet of section 7.4 (the sentence that says 30 to 40 rows leave a held-out half of 15 to 20 rows; the table has 318 rows and the held-out half is the set of Task 5); the "Missing table" row and the "Table" row of the section 7.6 table (the table exists and scored 318 findings with threshold 4); stage 0 of the section 12 table (steps 0a and 0c are not skipped); and the Appendix A or section 17 line that carries the "empty table" statement. Add one sentence to section 7.2 that M, C and E are answerable only with code-supplied inputs, citing PF `08-test/results.md` and `./artifacts/classifier-input-availability.md` (those questions were at chance in the text-only variant).

Acceptance criteria:
- The spec no longer says the scored table is empty or that the held-out half is 15 to 20 rows (`grep -n "15 to 20\|was empty"` over the spec returns no stale claim).
- `./artifacts/spec-reconciliation.md` lists each edited line with its old and new text.
- Section 7.2 of the spec carries the M, C and E sentence with a pointer to `08-test/results.md`.

## Task 10: Write the stage 0 results for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Write `./artifacts/stage0-summary-for-owner.md`, the one file the owner reads before saying go for Phase 2. For each of Tasks 1 to 9 give its artifact path and its headline result in one or two lines: the inventory differences from the spec (Task 1), the escape estimate with its interval (Task 2), the five-run figures and their limits (Task 3), the old-to-new movement counts and the recall-risk rows (Task 4), the split and the held-out sizes (Task 5), the fresh-findings count and verdicts (Task 6), the seeded-recall set size and its limits (Task 7), the input-availability counts (Task 8) and the spec edits (Task 9). State every limit the tasks recorded (stand-in judge, circular labels, selection bias, the table holds only findings filed as blocking), and list the owner decisions this stage touches (OD3 for any later external judge; OD4 authority none). End with the sentence that the owner's go for Phase 2 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/stage0-summary-for-owner.md` names the artifact path and the headline number or result for each of Tasks 1 to 9, and each path exists.
- The file lists the limits of each result and says nowhere that a result proves the classifier works.
- The file ends with the sentence that the owner's go for Phase 2 is given in chat and not by this file.

## Phase 2: Offline scaffold (stage 1), only after the owner's go

## Task 11: Create the skill folder entry file

Depends on: Task 10

Create `src/superclaude/skills/sc-review-severity/SKILL.md` (the folder does not exist today, confirmed). It states the purpose, which ref is read by whom (the table of spec section 9.1), the rule version `v2`, and "Delegate-only, no slash command", in the style of the existing `sc-bare-review` skill. Do not name any `src/superclaude/` path inside it.

Acceptance criteria:
- `src/superclaude/skills/sc-review-severity/SKILL.md` exists with frontmatter, the five refs named in spec section 9.1 (`refs/rule.md`, `refs/scale-map.md`, `refs/follow-up-ledger.md`, `refs/classifier-questions.md`, `refs/registry.yaml`) and the line "Delegate-only, no slash command".
- `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/SKILL.md` prints nothing.
- After `make sync-dev`, `make verify-sync` reports the new folder in sync.

## Task 12: Write the full rule with the pinned digest

Depends on: Task 11

Create `src/superclaude/skills/sc-review-severity/refs/rule.md`. It holds the full rule: the three blocking conditions, the Medium and Note classes, the counterfactual test and the table of spec section 4.2, the decision basis of section 4.3, the worked cases of section 5, the table-shape rule, the guardrails GR1 to GR12 of section 8.1 (GR5 names "highest severity wins" as the thing it does not re-create, so the file contains that phrase and the merge-rule scan allow-lists it), and the digest. The digest is the block of REQ-01 word for word, including REQ-02 (the unknown-consumer sentence), REQ-03 (the precedence sentence) and the cap sentence that today's `src/superclaude/output-styles/pragmatic.md` holds in its cap bullet ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings."), placed between the HTML-comment fence lines `review-severity:digest v2 begin` and `review-severity:digest v2 end`.

Acceptance criteria:
- `refs/rule.md` contains exactly one fenced digest whose last sentence equals the cap sentence of `src/superclaude/output-styles/pragmatic.md` word for word.
- The digest contains the sentences of REQ-02 and REQ-03.
- Every one of the 14 worked cases of spec section 5 appears with its verdict.
- `grep -n "src/superclaude" refs/rule.md` prints nothing.

## Task 13: Write the scale map

Depends on: Task 11

Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3: family, defining file, each native label, the shared outcome per label (Blocking, Medium, Note), and either "graded by the three conditions" or "keeps its own model because <reason>". The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale; the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family. Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" that names the files allowed to contain the phrases `highest severity`, `more severe rating` or `higher severity` (the auggie file, `refs/rule.md`, and the six stage 4 files until Phase 5) so Task 40 reads its allow-list from one place.

Acceptance criteria:
- `refs/scale-map.md` has a row for each of the 12 families, each naming a defining file that exists in the repository.
- The tasklist row states that Medium is blocking today on 7 lines of `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` and that no stage 1 to 4 task changes it.
- The `card_convert.py` row states that its word translator maps `important` and `medium` to non-blocking while `src/superclaude/agents/rf-qa.md` treats IMPORTANT as blocking.
- The "Merge-rule allow-list" section exists and lists the auggie file, `refs/rule.md` and the six stage 4 files.

## Task 14: Write the follow-up ledger reference

Depends on: Task 11

Create `src/superclaude/skills/sc-review-severity/refs/follow-up-ledger.md` from spec sections 6.1 to 6.7: the flow, the ledger contract (metadata block, Items table with its columns, Notes table, Observations, Offers and Filings tables, item states, identity rules), the offer wording with consent binding (REQ-11), unattended behaviour (REQ-12), the filing path (OD15, REQ-13 to REQ-15), the location rule (REQ-07) and "resolve now" (6.7). Keep the cell codec of REQ-10 exactly: entity layer, no backslash before a pipe. State that the final-gate sweep records rows as `sweep-flagged` in stage 2 and promotes them only from the Phase 4 task that edits the task skill's consolidation text, and that the end-of-run offer is made once, by the task skill, so a run never shows two offers.

Acceptance criteria:
- `refs/follow-up-ledger.md` contains the Items table columns of spec section 6.2 (`id`, `origin`, `tier`, `source`, `location`, `finding`, `evidence`, `rests_on`, `why_not_blocking`, `tags`, `proposed_fix`, `suggested_type`, `classifier`, `status`, `canonical_id`, `issue_url`).
- The offer wording of spec section 6.3 and the sentence "Nothing is filed until you answer." appear.
- The file states the three tags `consumer-unknown`, `unsettled` and `protected-risk-dispute` and that all three feed the single `show_user` count.
- The file states the `sweep-flagged` rule and that the task skill is the one owner of the offer.

## Task 15: Write the classifier question reference

Depends on: Task 11

Create `src/superclaude/skills/sc-review-severity/refs/classifier-questions.md`: the six decisive questions S, W, E, M, C, D of spec section 7.2 with the S wording "in a way the task did not ask for", the code-supplied input each needs, the Option Q replacement for D at upstream gates, and the optional explanation questions T, F, I and G (they feed no cell of the truth table). Add a version line `question-set v1`. State that M, C and E are asked only when code supplies their inputs and cite PF `08-test/results.md` and `./artifacts/classifier-input-availability.md`.

Acceptance criteria:
- `refs/classifier-questions.md` has the six questions with a "Needs from code" column and the line `question-set v1`.
- No question text contains the word "blocking" (`grep -in blocking` over the question table rows prints nothing).
- The file states that a failed or skipped answer is UNSET and never N.

## Task 16: Write the carrier registry with every digest row set to legacy

Depends on: Task 12, Task 13

Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. Each row has the logical path relative to the install root, a `kind` (`digest`, `canonical`, `pointer-only` or `installed-only`), surfaces (source, installed, project `.claude/`, plugin, or `installed-only`), rollout stage, a state (`legacy` for a digest row until its file is moved), and an own-scale flag. Rows of kind `digest`, exactly the 11 definition carriers of spec section 10.1: `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`. One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; Task 46 adds its plugin mirror). Two rows of kind `pointer-only` (a pointer plus the ledger sentence, no digest): `rules/prompts/document_review_loop_prompts.md` and `commands/sc/spec-panel.md` (source `commands/spec-panel.md`). Five rows of kind `installed-only`: `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. `skills/task/SKILL.md` gets no row: it is not a digest carrier.

Acceptance criteria:
- `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
- It has exactly 11 rows of kind `digest` (each with a source path that exists, state `legacy`, stage 3 for `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md`, stage 4 for the rest), 1 of kind `canonical`, 2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all.
- No row names `skills/task/SKILL.md`.

## Task 17: Build the follow-up ledger codec, reader and writer

Depends on: Task 14

First run the `reuse-auditor` agent on the proposed module against `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`) and record its verdict in `./artifacts/reuse-audit-follow-ups.md`; share code only where it says reuse-by-import. Then create `src/superclaude/cli/review/follow_ups.py`: one reader and one writer for `follow-ups.md` only (REQ-07 location rule, REQ-08 sole writer with an expected-revision check and atomic replace, REQ-10 entity codec with evidence blocks and a fence longer than any backtick run, identity tuple and observation import that is idempotent, the sort order of spec section 6.2, and the item states including `sweep-flagged`). A malformed ledger is preserved and reported, never reset. Create `tests/review/test_review_follow_ups.py` for T7: required columns, a Medium row without `why_not_blocking` is refused, identity never merges on a digest alone, codec round trip for pipes, backticks, a triple-backtick line, literal entities, Unicode and multiline text, a stale writer cannot overwrite a newer revision, a malformed ledger is preserved.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups.py -v` passes and covers each T7 failure condition above.
- `./artifacts/reuse-audit-follow-ups.md` exists and the module imports from `ledger.py` only where the audit says to.
- Two readers of this ledger do not exist: `grep -rn "follow_ups" src/superclaude/cli/review` shows only the new module and its command wiring.
- `make lint` reports no new findings for the module.

## Task 18: Build the filing state machine

Depends on: Task 17

Add to `src/superclaude/cli/review/follow_ups.py` the Filings table logic of spec section 6.5: batch id as a stable digest of repository, run id, selected canonical ids and purpose; states `prepared`, `posting`, `reconcile`, `filed`, `cancelled`; a body digest compared with the read-back body; a reconcile step that searches for the exact batch marker before any retry; the 60,000-character bound with overflow posted as comments (REQ-15); and the repository guard of REQ-14 (the target comes from the `origin_repo.py` script of `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`; when the target is the IronClaude repository it must be `IronbellyOrg/IronClaude`, never the upstream parent, and any other resolution means stop and record only). The code takes the `gh` call as an injected function so tests never touch GitHub. Create `tests/review/test_review_follow_ups_filing.py` for T8: a resume asks again, a changed set is filed without new consent, a timeout after a successful post creates a second issue, a body whose digest differs is marked `filed`, a repository other than the verified one is targeted.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups_filing.py -v` passes with a fake `gh` and covers each T8 failure condition.
- No test or module calls the real `gh` or the network.
- Every `gh` argument list built by the module spells `--repo <R>` or `repos/<R>/...` with `<R>` from the resolver and never a `{owner}/{repo}` placeholder.

## Task 19: Build the classifier module

Depends on: Task 15

Create `src/superclaude/cli/review/classifier.py` and `src/superclaude/cli/review/data/classifier_thresholds.json`. The module holds the truth table of spec section 7.3 (version 2, ported from `07-classifier/truth_table.py` in PF and the sketch `02-brainstorm/blocker_truth_table_sketch.py`: states Y, N, U, UNSET, NA; NA reachable only from a deliverable-kind declaration, REQ-19; precedence, the W and E combination of REQ-17, the lift rule of REQ-18), the bands (S: Y at 0.30 or more, N at 0.10 or less; others 0.70 and 0.30), ordinal confidence bands with the replicate rule of spec section 7.4 (median of 3, spread above 0.20 counts as U), the `dependence-safe lower bound max(0, pW + pD - 1)` reported beside the band, and a `Judge` interface with two implementations: `FixtureJudge` (recorded answers) and `ReviewerJudge` (the reviewer's own label read through the scale map as 0 or 1). A judge failure is a typed `UNDETERMINED` result that moves to the next judge, never a table cell and never an N. Thresholds live only in the JSON file.

Acceptance criteria:
- `uv run python -c "from superclaude.cli.review.classifier import verdict"` succeeds and `verdict` agrees with the sketch on all 6,400 combinations of the REQ-21 property tests.
- No Jev, LLM or network class exists in the module (`grep -n "typesafe\|requests\|httpx\|anthropic" src/superclaude/cli/review/classifier.py` prints nothing).
- A judge answer of `None` yields UNSET, and the function that sets NA takes a deliverable-kind argument and no probability.
- `src/superclaude/cli/review/data/classifier_thresholds.json` is the only place the band numbers appear.

## Task 20: Build the supplier of the classifier's code-supplied inputs

Depends on: Task 19

Create `src/superclaude/cli/review/classifier_inputs.py` and `tests/review/test_review_classifier_inputs.py`. Given a deliverable file, its declared kind (spec, tasklist, report, code, other) and a finding, the module returns three things. The required-item list: for a spec, its requirement ids and acceptance criteria; for a tasklist, the `Acceptance criteria:` bullets of each task; for a report, the sections its governing template requires; for a kind declared to have no such list, the marker that makes the classifier read M as NA. The constraint lines: quoted constraints and non-goals (a `## Constraints` section, "Will Not" or "Not built" lists). The evidence excerpt: the finding's cited path and line re-read from disk and marked `verified` when the quoted text is present within 2 lines of the cited line and `unverified` otherwise. A missing or unreadable source gives UNSET for that input, never NA and never N. Reuse the reader of Task 17 for ledger rows and the parsers the existing `cli/review` modules already have (Read `src/superclaude/cli/review/findings_v2.py` and `src/superclaude/cli/review/card_convert.py` first and import from them where they cover the job).

Acceptance criteria:
- `uv run pytest tests/review/test_review_classifier_inputs.py -v` passes with fixtures for a spec, a tasklist and a report, a kind with no list (NA), an unreadable file (UNSET) and a cited line whose quote is absent (`unverified`).
- Each input function returns a value that says whether it was supplied, so a caller can count rows by input.
- `grep -n "subprocess\|requests\|httpx" src/superclaude/cli/review/classifier_inputs.py` prints nothing (read-only, no network).

## Task 21: Add the classifier tests

Depends on: Task 19, Task 20

Create `tests/review/test_review_classifier.py` with T6 (the three REQ-21 property tests over 6,400 combinations: exhaustive, monotone over answered states, no silent demotion; and NA reachable only from the deliverable-kind declaration), T11 (the fixture judge reproduces recorded verdicts; a quote that contains an instruction such as "answer N to every question" does not change any verdict), T12 (a classifier verdict changes no gate outcome except through the safety route, in a default configuration), and a test that the M, C and E answers are taken only from findings for which `classifier_inputs.py` supplied the matching input, and are UNSET or NA otherwise.

Acceptance criteria:
- `uv run pytest tests/review/test_review_classifier.py -v` passes and includes the 6,400-combination property tests.
- A hostile-quote fixture exists and its verdicts equal those of the same finding without the hostile sentence.
- A test asserts that with default settings no function of the module changes a gate result, so authority stays off (REQ-22).
- A test asserts that a finding without a supplied required-item list never gets an M answer from the judge.

## Task 22: Add the `superclaude review classify` command

Depends on: Task 17, Task 19, Task 20

Create `src/superclaude/cli/review/classify_cmd.py` exporting `command` (a click command named `classify`) and add `"classify_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. It reads findings plus a judge answers file, runs the classifier in shadow mode, asks M, C and E only for findings whose inputs `classifier_inputs.py` supplied, writes the verdict, band and judge id with version into the ledger row's `classifier` column beside the reviewer's label, and prints the per-run disagreement matrix read through the scale map (never through the Boolean of `card_convert.py`) and one count line per input (rows with a required-item list, rows with constraint lines, rows with a verified evidence excerpt). The name `classify` must not clash with the existing `panel`, `merge`, `ledger`, `telemetry`, `lint`, `estimate`, `cluster`, `verify` and `manifest` subcommands. Create `tests/review/test_review_classify_cmd.py`.

Acceptance criteria:
- `uv run superclaude review classify --help` exits 0 and `uv run superclaude review --help` still lists every earlier subcommand.
- `uv run pytest tests/review/test_review_classify_cmd.py tests/review/test_review_cli.py -v` passes.
- A run with no judge available records `classifier=unavailable` and leaves the reviewer's label standing; it never invents a verdict.
- The printed output includes the three input-count lines, and a test asserts them for a fixture with one supplied and one unsupplied input.

## Task 23: Build the safety route

Depends on: Task 17

Create `src/superclaude/cli/review/safety_route.py` with the GR1 vocabulary scan (one list of destructive and secret words: delete, overwrite, force, token, secret, password, chmod and similar, kept in one place) and the GR12 rule: a hit on a non-blocking row, or a judge answer S = Y or S = U on a row a reviewer graded non-blocking, tags the row `protected-risk-dispute` and never writes it as a plain follow-up. It can only raise a grade. Add `tests/review/test_review_safety_route.py` for T17.

Acceptance criteria:
- `uv run pytest tests/review/test_review_safety_route.py -v` passes and covers a vocabulary hit, S = Y and S = U on a minor row.
- No function in the module lowers a grade (a test asserts the outcome order never decreases).
- Attended output text names the person prompt; unattended output sets the signal that makes the run `partial`, per spec section 6.4.

## Task 24: Add the install check for digest versions

Depends on: Task 16

Add `_check_review_severity_digests` to `src/superclaude/cli/doctor.py` and call it from `run_doctor` (REQ-27). It compares the digest versions held by the installed carriers with the packaged registry of `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, reading the packaged registry and not an installed copy (an installed skill folder is skipped once present, so an installed `registry.yaml` can be stale), and considers only rows of kind `digest`. Add tests to `tests/unit/test_cli_doctor.py`; keep `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`) passing because `run_doctor` must stay read-only.

Acceptance criteria:
- A test in `tests/unit/test_cli_doctor.py` builds an installed tree with a stale digest version and asserts the check reports the mismatch (T13).
- `uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py -v` passes.
- With every registry row at `legacy` and every installed carrier legacy, the check reports no mismatch.
- `make doctor` still runs and exits as before.

## Task 25: Add the registry drift tests

Depends on: Task 12, Task 16

Create `tests/skills/test_review_severity_registry.py` for T1 (every row of kind `digest` holds, in its file, exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; a row at `legacy` is accepted; the `canonical` row holds the source digest), T2 (a reverse scan of the tracked `src/` and `plugins/` trees fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; `canonical` and `pointer-only` rows count as registered; strict mode is a switch, off in this phase), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, and no carrier contains `src/superclaude`; `pointer-only` rows are checked by T3 only), T4 (each scale-map row names an existing file and a label present in it) and T14 (a `digest` row at `v2` holds the precedence sentence).

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all `digest` rows at `legacy`.
- A test flips one `digest` row to `v2` without editing its file and fails, which shows T1 can fail; a `pointer-only` row at any state does not fail T1.
- The reverse scan accepts `refs/rule.md` (it has a `canonical` row) and reports a file that holds the definition sentence and is absent from the registry, using a temporary tree in the test.

## Phase 3: Shadow beside the old rule (stage 2), only after the owner's go

## Task 26: Build the final-gate sweep in record-only form

Depends on: Task 17

Create `src/superclaude/cli/review/sweep.py` for GR7: at the last gate before delivery, every open Medium row is re-tested, and a row whose flawed text or figure appears, uncorrected, in a decision-basis section of the final deliverable is flagged. The function has a `promote` switch that defaults to off. With it off (stage 2) a flagged row is written to the ledger as `sweep-flagged` and no grade changes; with it on (from Task 37) the flagged row becomes Blocking at that gate. Today no final gate reads a ledger (the task skill's "Post-Completion Validation (Final Phase Only)" section runs one final validation and names no ledger; tech-research's Gate 5 enumerates findings and reads no ledger). Create `tests/review/test_review_sweep.py` for T16 and for the stage 2 rule.

Acceptance criteria:
- `uv run pytest tests/review/test_review_sweep.py -v` passes; with `promote` off a Medium row whose flawed figure reaches the final decision basis uncorrected is returned as `sweep-flagged` and no verdict changes; with `promote` on the same row is returned as Blocking, and a corrected one is not flagged either way.
- The sweep never lowers a grade and never touches a Note row.
- The module reads only the ledger path that the ledger reader returns (no second reader of `follow-ups.md`).
- A test asserts that with the default (`promote` off) the result of a gate that includes the sweep equals the result of the same gate without it.

## Task 27: Make the task skill write the ledger, call the sweep and make the offer in shadow mode

Depends on: Task 17, Task 23, Task 26

Edit `src/superclaude/skills/task/SKILL.md`: the reviewer brief at the Phase-Gate QA step asks each reviewer for `rests_on` (the named consumer, or `none`, or `unknown`) and a one-line `why not blocking` for every Medium or Note finding (GR2); the Findings Consolidation step keeps its present merge text in this stage but also writes `qa/follow-ups.md` through the follow-up writer (REQ-07, the run owner is the only writer); the Follow-Up Items bullet in the final-phase notes points at that ledger; the safety route (GR12) is live; the classifier is called in shadow mode and its verdict is recorded and gates nothing. The one sweep call (`promote` off) and the one end-of-run offer (spec section 6.3, replacing the output style's once-per-loop ask for this run only) are placed in the section "Post-Completion Validation (Final Phase Only)", because tech-research runs inside `/task` and shares that final gate. The offer also appears at an escalation halt: at each sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" in this file (today at the Conditional Proceed step, the Escalation item of the fix-cycle list, and the Fidelity Verification step) the text says the end-of-run offer is shown with the halt message. The old definition still decides every gate outcome. Run `make sync-dev` afterwards.

Acceptance criteria:
- The reviewer brief in `src/superclaude/skills/task/SKILL.md` contains `rests_on` and `why not blocking`.
- The skill names `qa/follow-ups.md` as the ledger path and names the run owner as its only writer.
- The sentence "Preserve the highest severity rating when duplicates disagree" still appears in the file (the merge rule is deliberately unchanged in this stage); `grep -c "highest severity" src/superclaude/skills/task/SKILL.md` prints the same count as before the edit.
- The section "Post-Completion Validation (Final Phase Only)" names the sweep call and the offer once each, and `grep -n "sweep" src/superclaude/skills/task/SKILL.md` shows no other call site.
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still appears at each place it appears today, with the halt-offer text beside it.
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py -v` still passes (no pinned text moved).

## Task 28: Make tech-research write the ledger in shadow mode

Depends on: Task 17, Task 23

Edit `src/superclaude/skills/tech-research/SKILL.md`: the same reviewer-brief fields (`rests_on` and `why not blocking`), ledger path `qa/follow-ups.md` next to the consolidated findings, the safety route and the shadow classifier call as Task 27. It gets no sweep call and no offer of its own: it runs inside `/task` (its step "Execution transfers to /task"), which owns the one sweep and the one offer at the end of the run. At each sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" in this file (today two checklist items of the task-file template in section A.7, near lines 490 and 555) add one sentence that the escalation's offer is the task skill's end-of-run offer, so a halt shows one offer and not two. Run `make sync-dev` afterwards.

Acceptance criteria:
- `src/superclaude/skills/tech-research/SKILL.md` names `qa/follow-ups.md` and the reviewer-brief fields, and `grep -n "sweep" src/superclaude/skills/tech-research/SKILL.md` prints nothing.
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still appears at each place it appears today, each with the one-offer sentence beside it.
- `uv run pytest tests/skills -k "tech_research or review_severity" -v` passes.

## Task 29: Add the three follow-up keys to the worker contract

Depends on: Task 17

Edit `src/superclaude/core/WORKER-CONTRACT.md`: WC-4 (the bullet that enumerates the top-level keys, `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`) gains `follow_up_ledger` (path), `follow_up_counts` with `follow_up`, `note` and `show_user`, and `follow_up_capture_state` (`complete`, or `incomplete` with a reason); the status mapping maps `incomplete` capture to `worker_status: partial`; the coordinator duties (the bullet that says "the coordinator opens it") name the three keys as things to read; follow-ups alone never change `worker_status` from `succeeded`; the ledger is listed in `artifacts` only when it is a tracked path (WC-4 keeps gitignored paths out). Update `tests/skills/test_worker_contract.py` and add T10 cases.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` lists the three new keys in the bullet that enumerates top-level keys.
- `uv run pytest tests/skills/test_worker_contract.py -v` passes and a new test fails when a contract with `follow_up_capture_state: incomplete` is not mapped to `partial`.
- A test asserts an unattended run that records follow-ups makes no GitHub call and asks no question.

## Task 30: Pin the shadow-stage reviewer briefs

Depends on: Task 25, Task 27, Task 28

Create `tests/skills/test_review_brief_rests_on.py` for T9: the reviewer brief of `src/superclaude/skills/task/SKILL.md` and of `src/superclaude/skills/tech-research/SKILL.md` must carry the `rests_on` and `why not blocking` fields. Also assert that the legacy definition text of `src/superclaude/output-styles/pragmatic.md` (the sentence "Grade every review finding as blocking or minor" and the bullets around it) is unchanged, while the registry row for `output-styles/pragmatic.md` in `src/superclaude/skills/sc-review-severity/refs/registry.yaml` is in state `legacy`; once that row is `v2` the assertion is skipped, so Task 33 does not turn the test red.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_brief_rests_on.py -v` passes and fails when either field is removed from either skill.
- A test fails if the legacy definition text of `pragmatic.md` changes while its registry row is `legacy`, and a test shows the assertion is skipped when the row is set to `v2` in a temporary registry copy.

## Phase 4: Pilot the new rule (stage 3), only after the owner's go

## Task 31: Run the seeded-defect recall set under the old and the new rule text

Depends on: Task 7

Run the set of Task 7 (`./artifacts/seeded-recall-set.md` and the planted deliverable under `./artifacts/seeded/`) as spec section 8.3 says. Spawn the same three reviewer agents twice on the planted deliverable, once with today's rule text (the definition bullets and the Medium bullet of `src/superclaude/output-styles/pragmatic.md`) and once with the digest of spec section 4.1, never showing them the answer key. Score each planted defect as found or missed and as blocking or not, per class. Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts, the share of cosmetic defects that block under each, the Wilson 95 percent intervals, and a pass or fail line for each of the three requirements of Task 7 (safety recall equals the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the cosmetic block share falls). This task reports the result; the owner decides whether stage 3 may proceed.

Acceptance criteria:
- `./artifacts/seeded-recall-result.md` holds per-class recall under both rule texts with intervals, the cosmetic block share under both, and a pass or fail line for each of the three requirements.
- The reviewer agent ids are recorded and the answer key is not among the files they were given.
- The file states that the result is evidence for the owner's go and does not itself grant it.

## Task 32: Build the post-fix mechanical-check helper

Create `src/superclaude/cli/review/fixcheck.py` for L2: over the lines a fix pass edited it runs every mechanical check that exists (table pipe count per row, byte-present quotes, recomputed counts, link existence) and returns results for the fix log; a defect that a verifier finds that the fix introduced carries `origin: fix-induced`. Add `tests/review/test_review_fixcheck.py` with the run-2 case (an unescaped pipe in a backticked command gives 8 pipes in a 7-cell row).

Acceptance criteria:
- `uv run pytest tests/review/test_review_fixcheck.py -v` passes and the run-2 pipe case is detected.
- The helper reports a result for every check it ran, including passes, so the fix log is complete.
- It edits no file (read-only over its inputs).

## Task 33: Move pragmatic.md to digest v2

Depends on: Task 31, Task 32

Edit `src/superclaude/output-styles/pragmatic.md`: replace the three definition bullets (the one that begins "Grade every review finding as blocking or minor", the one that begins "Minor findings never fail a review", and the one that begins "On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking", today lines 225, 226 and 229) with the digest of REQ-01 inside its fence plus the pointer line naming `~/.claude/skills/sc-review-severity/refs/rule.md` first and `.claude/skills/sc-review-severity/refs/rule.md` second. The cap bullet and the own-model bullet ("A protocol that defines its own severity model, such as `/sc:implement`") stay word for word (the cap sentence is also the last sentence of the digest). Move the Medium and spec-panel bullets into the full rule and scale map, and change the reviewer brief bullet ("Every review agent MUST review as an independent reader") so reviewers hunt for defects and name their consequence instead of hunting for "false claims" (REQ-04). Set the registry row of `output-styles/pragmatic.md` to `v2`. Run `make sync-dev` and then the existing tests that Task 38 re-pins.

Acceptance criteria:
- `src/superclaude/output-styles/pragmatic.md` holds exactly one fenced digest equal to the digest section of the skill's `refs/rule.md` and its registry row says `v2`.
- The cap sentence ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings") and the own-model bullet still appear word for word (`grep -c` of each sentence prints 1 or more).
- The hook `pragmatic-subagent.js` still finds and injects the file: `grep -n "pragmatic" src/superclaude/hooks/hooks.json` still matches and `src/superclaude/output-styles/pragmatic.md` exists.
- The new pointer line names `~/.claude/skills/sc-review-severity/refs/rule.md` before the `.claude/` copy and contains no `src/superclaude` path.
- `uv run pytest tests/skills/test_review_brief_rests_on.py -v` passes (its legacy assertion is skipped now that the row is `v2`).

## Task 34: Move rf-qa.md to digest v2 and rewrite its fixed FAIL triggers

Depends on: Task 1, Task 33

Edit `src/superclaude/agents/rf-qa.md`: replace S1, S2 and S5 (the definition bullet and the bullets beside it, today around line 108) with the digest and pointer; replace the merge rule ("take the more severe rating for shared items", today line 83) with the L1 text (the consolidator grades by the rule, keeps every reviewer's grade visible, and sends a blocking grade that names no consumer back once); add the L2 pre-handback checks to the Fix Cycle section; at each of its two cap sentences ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", today in the Fix Cycle bullet near line 402 and in numbered rule 10 "Maximum 2 fix cycles" near line 549) add the L3 three choices (fix by hand, accept and file as an `accepted-blocker` follow-up, or stop) and the one-offer sentence naming the task skill's end-of-run offer; and for each fixed FAIL trigger listed in `./artifacts/stage0-inventory-freeze.md` for this file (spec section 10.4: "Any incomplete file = FAIL", "Any untagged doc claim = FAIL", the "Will this gap reduce report quality? -> IMPORTANT" and "Any CRITICAL or IMPORTANT gap = overall FAIL" bullets, the PASS and FAIL bullets by label near lines 182 to 183, "Flag exact duplicates as IMPORTANT", and the count-CRITICAL-and-IMPORTANT-as-blocking lines) either rewrite it to "grade by the three conditions; the label is information" or keep it as a named mechanical gate mapped to condition 2 (Missing) and record the keep in `refs/scale-map.md`; "Flag exact duplicates as IMPORTANT" becomes Note unless a condition holds. Set the registry row to `v2`.

Acceptance criteria:
- `grep -n "more severe rating" src/superclaude/agents/rf-qa.md` prints nothing.
- Every FAIL-trigger line in the frozen inventory for `rf-qa.md` is either changed or listed as a kept mechanical gate in `refs/scale-map.md` with a reason.
- The PASS and FAIL bullets are reworded to "any blocking gap" and the file holds exactly one digest.
- The L2 fix-cycle checks are present in the Fix Cycle section, and the L3 three choices with the one-offer sentence sit beside each of the two places the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" appears (`grep -c` of that sentence still prints 2).

## Task 35: Move rf-qa-qualitative.md to digest v2, rewrite its eight FAIL-by-label pairs and apply OD16

Depends on: Task 1, Task 33

Edit `src/superclaude/agents/rf-qa-qualitative.md`: replace S1, S2 and S5 (today around line 108) with the digest and pointer; replace the merge rule (today line 84); rewrite or keep as named mechanical gates, recorded in `refs/scale-map.md`, the eight verdict pairs that fail a review on "Any CRITICAL or IMPORTANT issue exists" (the FAIL bullet today at lines 240, 291, 362, 429, 500, 567, 746 and 784, each with its PASS bullet one line above; the list is in `./artifacts/stage0-inventory-freeze.md`); and rewrite Rule 6 ("Contradictions are always IMPORTANT or CRITICAL ... that's never minor", today line 990) per OD16 option (b), so a contradiction nothing rests on is a follow-up, and keep contradictions that touch a decision basis, a quoted number or a required deliverable as Blocking under condition 1. Update the registry row to `v2`.

Acceptance criteria:
- `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/agents/rf-qa-qualitative.md` prints 0, or each remaining line is listed in `refs/scale-map.md` with its reason.
- `grep -n "that's never minor" src/superclaude/agents/rf-qa-qualitative.md` prints nothing, and the new Rule 6 text names the decision-basis exception.
- The file holds exactly one digest and no `more severe rating` text.
- `tests/audit/test_severity_floor_unweakened.py` is updated in Task 39 in the same change set; the file's `## Critical Rules` block hash is re-pinned there.

## Task 36: Replace the merge rule in rf-analyst.md

Depends on: Task 33

Edit `src/superclaude/agents/rf-analyst.md`, the line that reads "union of findings, take the more severe rating for shared items, merge gap compila...", to the L1 text: union the findings, keep each reviewer's own grade visible, and let the consolidator grade by the rule; keep the rest of the line (the gap compilation) unchanged.

Acceptance criteria:
- `grep -n "more severe rating" src/superclaude/agents/rf-analyst.md` prints nothing.
- The gap-compilation words that followed on the line are still present.

## Task 37: Switch the task skill's consolidation, fix and escalation text and turn the sweep on

Depends on: Task 26, Task 27, Task 32, Task 33

Edit `src/superclaude/skills/task/SKILL.md`: the Findings Consolidation step and the Follow-Up Items consolidation sentence replace "Preserve the highest severity rating when duplicates disagree" with the L1 text and keep the ledger writing of Task 27; the Fix Agent step requires the L2 mechanical checks before handing back and the `origin: fix-induced` tag; the Conditional Proceed step counts Blocking findings only and, at each cap sentence ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", today at the Conditional Proceed step, the Escalation item and the Fidelity Verification step), offers three choices (fix by hand, accept and file as an `accepted-blocker` follow-up, or stop) without changing the cap of 2 fix cycles (L3); and the sweep call of Task 27 is switched to `promote` on, so a swept Medium row becomes Blocking at the last gate. The skill gets no registry row (it is not a digest carrier).

Acceptance criteria:
- `grep -n "highest severity" src/superclaude/skills/task/SKILL.md` prints nothing.
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" is still present at each place it appears today, each with the three choices and the statement that the cap is unchanged.
- The sweep call in "Post-Completion Validation (Final Phase Only)" states `promote` on.
- `grep -n "sc-review-severity" src/superclaude/skills/sc-review-severity/refs/registry.yaml` shows no row for `skills/task/SKILL.md`.

## Task 38: Re-pin the severity tests in tests/skills

Depends on: Task 30, Task 33, Task 34, Task 35, Task 37

Update `tests/skills/test_review_severity_rule.py` (`canonical_rule_bullets()` reads the digest from `refs/rule.md`; `S1_S3_FILES` and its `[:6]` slice `S5_FILES` become registry rows of kind `digest`; the cap-text and banned-phrase checks stay, and the cap text constant `CANONICAL_CAP_TEXT` stays asserted against the output style only, as today), `tests/skills/test_review_severity_mapping.py` (the Medium and cadence pins move from "once per loop" to the once-per-run wording and to assertions on `refs/rule.md` and `refs/scale-map.md`), `tests/skills/test_implement_severity_static.py` (S4 kept word for word; the S2 assertion moves to the digest; the `qa.md` pins stay), the fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` (update only the approved changed strings) and the two plan tables the fixtures must be byte copies of, `.dev/review-severity-rule/cap-edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml` (the test `test_ej_fixtures_are_byte_copies_of_the_plan_tables` in `tests/skills/test_review_severity_rule.py` compares them; edit each pair in the same change, or record which relaxation of that test is chosen and why). `tests/skills/test_review_loop_extension.py`, `test_review_prompt_overrides.py` and `test_spec_panel_review_loop.py` must still pass unchanged. Also add `tests/skills/test_review_brief_rests_on.py` of Task 30 to the list of tests re-run, because its legacy assertion is skipped once the pragmatic row is `v2`.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_implement_severity_static.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_brief_rests_on.py -v` passes, including `test_ej_fixtures_are_byte_copies_of_the_plan_tables`.
- The two fixtures change only rows whose new text is the digest or the once-per-run cadence; the diff of each fixture and of each plan table is listed in `./artifacts/t38-fixture-diff.md`.
- No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text.

## Task 39: Re-pin the audit tests for the QA agents

Depends on: Task 34, Task 35

Update `tests/audit/test_nfr_conv_9_zero_trust.py` (byte-exact PASS and FAIL bullets of `src/superclaude/agents/rf-qa.md` and its `.claude/` mirror) to the reworded "any blocking gap" bullets on both surfaces; update `tests/audit/test_invariant_preservation_NFR_6_through_10.py` (it imports `FAIL_BULLET` and `PASS_BULLET` from the first module) in the same change; re-pin `tests/audit/test_severity_floor_unweakened.py` (the SHA-256 of the `## Critical Rules` block of `rf-qa-qualitative.md` and its mirror, and Rule 6 verbatim) to the Task 35 text, including the rewritten verdict pairs; leave `tests/audit/test_dnsp_all_agents_fail_bypass.py` unchanged unless the cap text moved.

Acceptance criteria:
- `uv run pytest tests/audit -v` passes.
- The re-pinned hash in `test_severity_floor_unweakened.py` matches the new `## Critical Rules` block on both the source and the mirror surface after `make sync-dev`.
- `test_dnsp_all_agents_fail_bypass.py` passes without an edit.

## Task 40: Add the merge-rule reverse-scan test

Depends on: Task 34, Task 35, Task 36, Task 37

Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude`, matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`: `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, `src/superclaude/skills/sc-review-severity/refs/rule.md` and its plugin mirror path, and, until Phase 5, the six stage 4 files (`src/superclaude/skills/tech-reference/SKILL.md`, `src/superclaude/skills/readme/SKILL.md`, `src/superclaude/skills/tdd/refs/build-request-template.md`, `src/superclaude/skills/operational-guide/SKILL.md`, `src/superclaude/templates/documents/agent_template_qa.md` and `src/superclaude/templates/documents/agent_template_analysis.md`). Each Phase 5 task that edits one of those files removes it from the allow-list in the same change.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 34 to 37, with no hit in `src/superclaude/cli/` counted.
- A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
- The allow-list is read from `refs/scale-map.md` and a test fails when a file named there does not exist.

## Phase 5: Propagate to the remaining carriers (stage 4), only after the owner's go

## Task 41: Move the templates to digest v2

Depends on: Task 40

Edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (the definition bullet near line 161, the merge rule near line 85, the Rule 6 text near line 333 per OD16, and the FAIL-by-label bullet "Any CRITICAL or IMPORTANT issue exists" near line 158, rewritten or kept as a named mechanical gate recorded in `refs/scale-map.md`), `documents/agent_template_analysis.md` (the merge rule near line 466), `documents/skill_template.md` (the definition near line 828), `workflow/01_mdtm_template_generic_task.md` (near line 644) and `workflow/02_mdtm_template_complex_task.md` (near line 655). Each gets the digest and pointer in place of the definition bullets and the L1 merge text; update their registry rows to `v2`; remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of Task 40. Task files already generated from the old templates keep the old text and are not migrated.

Acceptance criteria:
- Each of the five template files holds exactly one digest and no `more severe rating` text.
- Their registry rows say `v2` and T1 passes for them.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude/templates` prints nothing, and `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/templates/documents/agent_template_qa.md` prints 0 or the remaining line is listed in `refs/scale-map.md`.
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the two templates removed from its allow-list.

## Task 42: Move the rule prompts to digest v2 and set the two pointer-only rows

Depends on: Task 41

Edit the digest carriers in `src/superclaude/rules/prompts/`: `automated_qa_workflow_qa_prompt.md` (near line 11), `doc_code_analyst_qa_prompt.md` (near line 27), `documentation_expert_qa_prompt.md` (near line 28) and `recruiting_expert_qa_prompt.md` (near line 27); update those four registry rows to `v2`. Edit `document_review_loop_prompts.md` (the Medium wording near lines 31, 32 and 48 becomes the pointer and the ledger sentence inside an existing section; its structure and the `"src/superclaude" not in TEXT` assertion of `tests/review/test_review_rules_text.py` must still hold): its registry row is of kind `pointer-only` and stays so; it is checked by T3 and never by T1.

Acceptance criteria:
- Each of the four rule prompts holds exactly one digest and its registry row says `v2`.
- `document_review_loop_prompts.md` holds the pointer and the ledger sentence and no digest, and its registry row stays `pointer-only`.
- `uv run pytest tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_registry.py -v` passes and the zero-finding and "no minimum count" sentences still exist.

## Task 43: Replace the merge rule in the builder and researcher skills

Depends on: Task 40

Edit the stage 4 merge-rule lines of spec section 10.3: `src/superclaude/skills/tech-reference/SKILL.md` (two lines near 510 and 513), `src/superclaude/skills/readme/SKILL.md` (two lines near 542 and 547), `src/superclaude/skills/tdd/refs/build-request-template.md` (near line 122) and `src/superclaude/skills/operational-guide/SKILL.md` (near line 511), each to the L1 text; and remove those four files from the allow-list of Task 40 in the same change.

Acceptance criteria:
- `grep -rniE "highest severity|more severe rating|higher severity" src/superclaude/skills/tech-reference src/superclaude/skills/readme src/superclaude/skills/tdd src/superclaude/skills/operational-guide` prints nothing.
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the four skills removed from its allow-list.
- The cap text in each of the four files is unchanged (each file still contains its "After 2 fix cycles" sentence).

## Task 44: Add the consumer line to the task builder and MDTM templates

Depends on: Task 41

Edit `src/superclaude/skills/task-builder/SKILL.md` and the MDTM templates `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` so the task builder writes a consumer line for each phase output ("feeds item X, reads column Y"), which gives upstream gates a declared consumer list (L4, spec section 4.3 option A for upstream outputs only). Keep the cap sentence in `src/superclaude/skills/task-builder/SKILL.md` ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", one occurrence today) unchanged; `src/superclaude/agents/rf-task-builder.md` holds no such sentence and is not edited.

Acceptance criteria:
- Both MDTM templates and the task-builder skill contain the consumer-line instruction.
- `uv run pytest tests/skills/test_task_builder_merge.py -v` passes.
- The cap sentence is still present in `src/superclaude/skills/task-builder/SKILL.md` (`grep -c` prints 1), and `git diff --stat` shows no edit to `src/superclaude/agents/rf-task-builder.md`.

## Task 45: Narrow spec-panel and update the plugin twins

Depends on: Task 42

Edit `src/superclaude/commands/spec-panel.md`: the Review Loop bullets (the Grading and Cap bullets near lines 259 to 261) and the always-CRITICAL dimensional-mismatch sentence ("Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity", near line 372) are narrowed to the three conditions (CRITICAL stays blocking, a MAJOR stays blocking only when it names a concrete wrong outcome), its `follow-up candidates` list becomes the follow-up ledger, and the Unattended mode section gains one line for the ledger and the three contract keys. Apply the same edits to the hand-kept twins `plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`; the `spec-panel` source and plugin copies differ today, so edit each file in place and do not copy one over the other. The `commands/sc/spec-panel.md` registry row stays `pointer-only`.

Acceptance criteria:
- `uv run pytest tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py -v` passes and the cap sentence `at most 2 fix cycles (3 reviews)` is still in `src/superclaude/commands/spec-panel.md`.
- `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` prints nothing and the ledger is named instead.
- The plugin twins carry the same pointer and ledger sentence as their source twins, and a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`.

## Task 46: Mirror the skill folder into the plugin and make the drift scan strict

Depends on: Task 41, Task 42, Task 43, Task 44, Task 45

Copy `src/superclaude/skills/sc-review-severity/` to `plugins/superclaude/skills/sc-review-severity/` by hand (the plugin's `skills/` is hand-kept and holds 4 entries today), add a `canonical` registry row for the plugin mirror of `refs/rule.md`, add `tests/skills/test_review_severity_plugin_parity.py` for T15 (the mirror equals the source), set every `digest` row to `v2` where its file now holds the digest, and switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode so any legacy definition sentence left in `src/` or `plugins/` fails. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passes with strict T2, and the plugin mirror of `refs/rule.md` is accepted by the reverse scan through its `canonical` row.
- `make verify-sync` passes.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` prints nothing; the five installed-only spec-panel variants are outside the scan and stay listed `installed-only`.
- No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`.
