# Reviewer brief 1 (persona: analyzer; model class: haiku)

## T1 card excerpt

## Deviation and risk observations

- Phase shape: the plan has four phases because the standard depth requires 4 to 8; they are groupings of a ten-task measurement list (freeze and record; re-grade and split; build new sets; reconcile and summarize), not stages, so a reader may mistake them for stages.
- Reuse risk: the ten task bodies were taken from the revised 46-task plan and edited with exact substitutions; stale cross-references to that plan's numbering (Task 20, Task 31, Phase 2) were replaced, but any remaining mention of a base-plan task number would point at nothing in this package.
- Independence risk: Tasks 4 and 6 require blind agents that did not write the rule, the spec or the findings. The executing session cannot prove authorship; the acceptance lines ask for agent ids and a statement, which is a record, not a check.
- Scope risk: Task 9 edits the spec file, which the stage requests and the 46-task base plan cite, and drafts three definitions marked "proposed, for owner acceptance at the stage 1 go". The spec already says "zero safety misses" in its stage 3 row without a definition, so the draft adds a definition, not a new rule.
- Frame risk: Task 2's retrospective escape test needs a frame of de-duplicated minor findings from the run-2 QA folder (139 files: cycle-control files, analyst reports, fix logs); the plan names the folder but not how minor findings are identified in each file format, and the executor must decide that.
- Sizing risk: Task 7 now requires a stated minimum n per gating class; the sizing arithmetic can show that a "fresh short spec" cannot hold that many planted defects, in which case the task marks the class's pass line advisory, which weakens the stage 3 check.


## Recommendations

- State in Task 2 how a minor finding is recognised in each run-2 QA file type, or say the executor must record the rule it used.
- Add to Task 7 a lower bound on the planted deliverable's size so the advisory fallback is the exception.
- Confirm in Task 10 that the stage ledger file exists before it is cited.


Persona instructions (analyzer): look for acceptance checks that cannot pass as written (a check that needs a file or state nothing earlier in this package produces, or that a task's own edit breaks), tasks that depend on an input the plan does not create, stale cross-references to the 46-task plan's numbering, and instructions that two tasks give differently. Walk the `Depends on:` edges, check that each file a task reads exists today or is created by an earlier task, and check that grep-style acceptance lines would print what the task says given the live files (especially Task 9's spec edits against the spec's real section and line anchors). Test the T1 card's observations against the live files before agreeing or disagreeing.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T02:10:44Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md:1-27
```markdown
1: ---
2: schema: workflow-plan/1.2
3: source: ./source.md
4: strategy: systematic
5: depth: standard
6: slug: TASK-WF-blockerStage0-20261116-021044
7: version: "1"
8: priority: Medium
9: created_date: "2026-11-16"
10: ---
11: 
12: # Stage 0 plan: close the measurement stage for the blocker classification work (issue #552)
13: 
14: Source: ./source.md
15: Goal: The owner can read one file, `./artifacts/stage0-summary-for-owner.md`, and decide whether to say go for stage 1. This package measures, records and drafts definitions; it changes nothing under `src/`, `tests/`, `.claude/` or `plugins/`.
16: 
17: ## Constraints
18: 
19: - One package, one stage. This is stage 0 of five packages (one plan per stage, the owner's decision of 2026-11-16). Stage 1 is generated and run only after the owner has read the stage 0 summary and said go in chat; no task here checks or records that go.
20: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the blocker characteristics in `06-blocker-characteristics.md` and the classifier sketch in `07-classifier/`. The stage ledger and the other four stage requests are in PF `stage-requests/`.
21: - The only file outside `./artifacts/` that a task here edits is the spec file in PF (Task 9). Nothing under `src/`, `tests/`, `.claude/` or `plugins/` is edited.
22: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
23: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, any change to the own-scale primitives, code-assigned severity in `src/superclaude/cli/**/*.py`, the 35 percent score target, and any change to the cap of 2 fix cycles. No task of stages 1 to 4 is in this package.
24: - Classifier facts that bind every task that touches the classifier: the 5-run test of PF `08-test/results.md` used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. Confidence is reported as an ordinal band only, never as a probability.
25: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. Python work uses UV only: `uv run python ...`, never `python -m` or bare `pip`.
26: - Measurement tasks that use blind agents record each agent id, and no agent that wrote the rule, the spec or the findings it grades is used as its own grader.
27: 
```

### .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md:59-83
```markdown
59: ## Phase 2: Re-grade and split the scored table
60: 
61: ## Task 4: Re-grade the scored table under the old and the new rule text (spec stage 0c)
62: 
63: Depends on: Task 1
64: 
65: Use the 318 findings in PF `04-historical/master-table.md` through the blind copies `blind-table-1.md`, `blind-table-2.md` and `blind-table-3.md` in the same folder (columns ID, Category, Description brief, Context only). Spawn three blind agents that did not write the rule or the spec. Each re-grades every finding twice, in a paired design with the order of the two texts alternated: once under today's rule text (the lines of `src/superclaude/output-styles/pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet to the spec-panel scale bullet, today lines 221 to 231) and once under the digest of spec section 4.1 (REQ-01, the block between the quoted lines). Record each agent id and every grade in `./artifacts/stage0c-grades.jsonl` and write `./artifacts/stage0c-regrade.md` with the confusion matrix against the panel consensus in PF `05-scoring/consensus.md` (blocker at mean 4.0 or higher), how many findings graded blocking under the old text become non-blocking under the new text, the spread among the three agents, and the rows that moved from non-blocking to blocking.
66: 
67: Acceptance criteria:
68: - `./artifacts/stage0c-grades.jsonl` has 318 findings times 3 agents times 2 texts, 1908 grades, each with agent id, text version and the order position.
69: - `./artifacts/stage0c-regrade.md` carries the confusion matrix with counts, the old-to-new movement counts and the three-agent spread, and states that the table holds only findings filed as blocking.
70: - The file lists the ids of the agents used and states that none of them wrote the digest or the spec.
71: - Rows the old text and the new text grade differently and that the panel calls a blocker are listed by id, since they are the recall risk.
72: 
73: ## Task 5: Split the scored table into a cluster-aware held-out set
74: 
75: Depends on: Task 2
76: 
77: Split the 318 findings of PF `04-historical/master-table.md` so that no defect cluster has rows on both sides. The clusters are the six keyword clusters of PF `06-blocker-characteristics.md` (the Phase 0 acceptance check that cannot pass, the `--unattended` flag landing before gates convert, the contract status vocabulary, the answer-as-flag and approval-gate rule, the git push classifier, and the missing `target_sha` on the resume path); rows in no cluster are split at random with a recorded seed. Add the stage 0b sample of Task 2 as a separate set of findings that a reviewer called minor. Write `./artifacts/stage0-heldout-split.md` and `./artifacts/stage0-heldout-ids.json`. The fresh findings of Task 6 are a third population and are never placed in either half.
78: 
79: Acceptance criteria:
80: - `./artifacts/stage0-heldout-ids.json` lists the finding ids of the tuning half, the held-out half and the reviewer-called-minor set, with the seed.
81: - No cluster named in PF `06-blocker-characteristics.md` appears in both halves; the split file states each cluster's side.
82: - The two halves differ in size by at most 20 percent unless a cluster is too large to place, and the file says so when it is.
83: 
```

### .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md:117-143
```markdown
117: ## Phase 4: Reconcile the spec and write the owner summary
118: 
119: ## Task 9: Correct the stale statements in the spec
120: 
121: Depends on: Task 4, Task 5, Task 8
122: 
123: Edit PF `02-brainstorm/merged-requirements.md` where the program results made it stale, and write the list of edits to `./artifacts/spec-reconciliation.md`. The edits: the thresholds bullet of section 7.4 (the sentence that says 30 to 40 rows leave a held-out half of 15 to 20 rows; the table has 318 rows and the held-out half is the set of Task 5); the "Missing table" row and the "Table" row of the section 7.6 table (the table exists and scored 318 findings with threshold 4); stage 0 of the section 12 table (steps 0a and 0c are not skipped); and any line of section 17 or Appendix A that says the table is empty or absent (a Grep when the plan was written found none there, so the task re-runs the Grep and records "none found" in `./artifacts/spec-reconciliation.md` when that is still true). Add one sentence to section 7.2 that M, C and E are answerable only with code-supplied inputs, citing PF `08-test/results.md` and `./artifacts/classifier-input-availability.md` (those questions were at chance in the text-only variant). Then draft three further edits, each marked in the spec as "proposed, for owner acceptance at the stage 1 go": (a) in the section 12 table, a definition of "safety miss" for the stage 3 entry count: a finding that a later review or the owner confirms is a security, data-loss or safety-boundary risk that a shadow run recorded as a follow-up or Note and did not route through the GR12 safety route; (b) in the section 12 stage 2 row, the exit numbers made measurable: ledger volume per run, the share of rows tagged `consumer-unknown`, offers made and answered, and the shadow agreement figures of the classifier against the reviewers' labels; (c) in the section 12 stage 3 row, a pointer to the revert triggers RT1 and RT2 of section 13.2 and metric M12 of section 13.1 as the audit-window numbers (quote their existing text; do not redefine them). Also record, in sections 10 and 12 of the spec, three staging decisions: the merge-rule allow-list in `refs/scale-map.md` lists files by path only and the plugin mirror joins it only in stage 4; `agent_template_analysis.md` gets the merge-rule text only and the registry keeps exactly 11 `digest` rows; T3's `src/superclaude` check applies to `digest` and `canonical` rows only and a `pointer-only` row is checked only once its pointer is present.
124: 
125: Acceptance criteria:
126: - The spec no longer says the scored table is empty or that the held-out half is 15 to 20 rows (`grep -n "15 to 20\|was empty"` over the spec returns no stale claim).
127: - `./artifacts/spec-reconciliation.md` lists each edited line with its old and new text.
128: - Section 7.2 of the spec carries the M, C and E sentence with a pointer to `08-test/results.md`.
129: - The spec holds three markers "proposed, for owner acceptance at the stage 1 go" (`grep -c` of that phrase over the spec prints 3 or more), one each for the safety-miss definition, the stage 2 exit numbers and the stage 3 pointer, and the section 12 stage 3 row names RT1, RT2 and M12.
130: - The spec records the three staging decisions (allow-list by path only with the mirror joining in stage 4, analysis template merge-rule text only with exactly 11 digest rows, T3 scope), and `./artifacts/spec-reconciliation.md` lists each of these edits with its old and new text.
131: 
132: ## Task 10: Write the stage 0 results for the owner
133: 
134: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9
135: 
136: Write `./artifacts/stage0-summary-for-owner.md`, the one file the owner reads before saying go for stage 1. For each of Tasks 1 to 9 give its artifact path and its headline result in one or two lines: the inventory differences from the spec (Task 1), the escape estimate with its interval (Task 2), the five-run figures and their limits (Task 3), the old-to-new movement counts and the recall-risk rows (Task 4), the split and the held-out sizes (Task 5), the fresh-findings count and verdicts (Task 6), the seeded-recall set size and its limits (Task 7), the input-availability counts (Task 8) and the spec edits (Task 9). State every limit the tasks recorded (stand-in judge, circular labels, selection bias, the table holds only findings filed as blocking), and list the owner decisions this stage touches (OD3 for any later external judge; OD4 authority none). Add four things for the owner: the drafted definitions of Task 9 (safety miss, stage 2 exit numbers, stage 3 pointer) to accept or change, the three staging decisions, the stage ledger of `stage-requests/README.md` in PF (which stage packages exist and which owner gos are recorded), and the five findings of this stage that matter most for the stage 1 go. End with the sentence that the owner's go for stage 1 is given in chat and not by this file.
137: 
138: Acceptance criteria:
139: - `./artifacts/stage0-summary-for-owner.md` names the artifact path and the headline number or result for each of Tasks 1 to 9, and each path exists.
140: - The file lists the limits of each result and says nowhere that a result proves the classifier works.
141: - The file lists the drafted definitions and the three staging decisions, and names the stage ledger file.
142: - The file ends with the sentence that the owner's go for stage 1 is given in chat and not by this file.
143: 
```


## Coverage slice

| Requirement | Quote (source.md line) | Best task | Ratio | Mechanical match |
|---|---|---|---|---|
| INF-001 | One package, one stage. (13) | 7 | 1.0 | containment-0.6 |
| INF-002 | no task here checks or records that go (13) | 0 | 1.0 | containment-0.6 |
| INF-003 | the second evaluation on this population is run by the stage 2 package's classifier-evalua (14) | 6 | 1.0 | containment-0.6 |
| INF-004 | The sizing must state a minimum n per gating class (safety, decision-bearing, missing) wit (15) | 7 | 1.0 | containment-0.6 |
| INF-005 | State the rule that stage 3 runs each pass with fresh agent spawns and alternated order. (15) | 7 | 0.7 | containment-0.6 |
| INF-006 | Keep the answer key separate. (15) | 7 | 1.0 | containment-0.6 |
| INF-007 | for owner acceptance at the stage 1 go (16) | 7 | 1.0 | containment-0.6 |
| INF-008 | the stage 2 exit numbers (16) | 9 | 1.0 | containment-0.6 |
| INF-009 | the stage 3 audit-window numbers (16) | 9 | 1.0 | containment-0.6 |
| INF-010 | the merge-rule allow-list lists files by path only and the plugin mirror joins it only in  (16) | 9 | 1.0 | containment-0.6 |
| INF-011 | `agent_template_analysis.md` gets the merge-rule text only and the registry keeps exactly  (16) | 9 | 1.0 | containment-0.6 |
| INF-012 | T3's `src/superclaude` check applies to `digest` and `canonical` rows only (16) | 9 | 1.0 | containment-0.6 |
| INF-013 | Each edit is listed in `./artifacts/spec-reconciliation.md` with its old and new text. (16) | 9 | 0.875 | containment-0.6 |
| INF-014 | the stage ledger of `stage-requests/README.md` (17) | 10 | 1.0 | containment-0.6 |
| INF-015 | It still ends with the sentence that the owner's go for stage 1 is given in chat and not b (17) | 10 | 0.875 | containment-0.6 |
| INF-016 | No Jev call, key or account. (21) | 0 | 1.0 | containment-0.6 |
| INF-017 | Do not change the cap of 2 fix cycles (21) | 0 | 1.0 | containment-0.6 |
| INF-018 | the owner can read one file (9) | 7 | 1.0 | containment-0.6 |

---
You are a read-only reviewer (agent type reflect-reviewer). You never edit, write, move or delete anything and you run no shell or git command. Audit ONLY the plan and the evidence named below, using Read, Grep, Glob (and codegraph tools only because index_state=fresh, with the projectPath above). Every claim you make must cite a repo-relative `file:line` that you have Read. A claim you cannot cite is tagged [INFERRED] or dropped.

Mode: UC-1 pre-execution review. Plan under review: `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (4 phases, 10 tasks, 143 lines). Driving source: `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/source.md` (the stage 0 plan request). The plan is stage 0 of five packages, one per stage, for the blocker-classification work (issue #552). Its task bodies come from Tasks 1 to 10 of the 46-task plan `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md`, whose own pre-execution review is `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md` (read its F7, F8, F10 and F11 for context). The program folder is `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/` (spec: `02-brainstorm/merged-requirements.md`, 1,224 lines; read only the parts you need).

Severity rule for this review. Blocking means: the plan, followed literally by `/sc:implement` (one plan file, tasks run in source order, `Depends on` lines ignored, a fresh reviewer checks each task's acceptance lines), leaves (i) an acceptance check or requirement that cannot be met, whose fix needs a decision the plan does not make, or (ii) a silent wrong or missing result. Wording, mechanical coordinate errors with a stated intent, and extra checks the plan forbids are MINOR and non-blocking. Verify claims against the live files before you report them; a plan statement about a live file that you did not check is not a finding.

Return ONE markdown card as your final message, nothing else, under 2800 characters in total (the message channel truncates longer replies), with exactly these sections:
## Verdict
one line: PASS, PASS-with-notes or NEEDS-REVISION, then one sentence why.
## Findings
one block per finding: `F<n>` | severity CRITICAL / MAJOR / MINOR | blocking true/false | category (contradiction, missing-requirement, unpassable-check, data-loss, safety, other) | claim (one or two sentences naming WHO acts and WHAT wrong result they get) | citations (1 to 4 `path:line` refs with a short quote). Report only real defects with evidence. A zero-finding result is valid if you state what you checked. Do not invent findings and do not work to a quota. Use repo-relative paths.
## Checked
a short list (4 bullets at most) of what you verified and found sound (file:line each).
## Self-report
`confidence: <0.00-1.00>` and `reviewer_model_self_report: <the model you run as, one line>`.
