# Reviewer brief 2 (persona: qa; model class: opus)

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


Persona instructions (qa): audit the coverage matrix AGAINST the spec body in your grounding hunks (the spec here is the stage 0 request); surface any requirement-bearing span absent from the matrix as a finding. Then check the plan against the request and the program: does every change the request lists have its text in a task, does any task contradict the request, the spec (section numbers, requirement ids) or the staging decisions in PF `stage-requests/README.md`, and do the tasks produce what the owner needs in `./artifacts/stage0-summary-for-owner.md`? Check that no task edits anything under `src/`, `tests/`, `.claude/` or `plugins/`, that the measurement tasks (Tasks 2, 4, 6, 7) are specified well enough for an executor to run them without a design decision the plan does not make, and that the drafted definitions of Task 9 are consistent with the spec's section 12 and 13 text.

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

### .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/source.md:1-21
```markdown
1: # Stage 0 plan request: close the measurement stage for the blocker classification work (issue #552)
2: 
3: This is the first of five plan packages, one per stage (decision of the owner, 2026-11-16; see `stage-requests/README.md` in the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115`, which also lists the decisions that apply to every stage). Generate one plan package for stage 0 only. It changes nothing under `src/`, `tests/`, `.claude/` or `plugins/`; it measures, records and drafts definitions for the owner to read before stage 1.
4: 
5: ## Base text and goal
6: 
7: The revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (found by that folder name under `.dev/tasks/to-do/`) holds the task bodies of stage 0 as its Phase 1, Tasks 1 to 10. Reuse those ten task bodies and acceptance criteria, renumbered 1 to 10 in the new package, with the changes below. The merged spec is `02-brainstorm/merged-requirements.md` in the program folder (called PF in the task bodies); the reconciliation is PF `09-plan-input.md`. Its pre-execution review found 8 blocking defects in the 46-task plan (report `REPORT.md` in the reflect run folder `pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007` under `.dev/reflect/`); the changes below are the ones that touch stage 0.
8: 
9: Goal: the owner can read one file (`./artifacts/stage0-summary-for-owner.md`) and decide whether to say go for stage 1.
10: 
11: ## Changes to apply to the base tasks
12: 
13: - **Constraints.** One package, one stage. State: this package is stage 0; it changes no file under `src/`, `tests/`, `.claude/` or `plugins/` except the spec file in PF (Task 9); stage 1 starts only after the owner reads the stage 0 summary and says go in chat; no task here checks or records that go. Keep the carried-over constraints of the base plan's `## Constraints` that apply to measurement (spec and PF naming, owner-decision defaults OD1 to OD16, the not-built list including no Jev or external judge call and no TypeSafe key, the classifier facts from the 5-run result, UV only, task evidence under `./artifacts/`, `.dev/tasks/` is always staged and never described as "never staged"). Drop the base plan's gate prose about Phases 2 to 5 (it belongs to the later packages).
14: - **Task 6 (fresh-findings set).** Its last acceptance line now says the second evaluation on this population is run by the stage 2 package's classifier-evaluation task, and that the stage 2 package reads `fresh-findings.md` from this package by package id.
15: - **Task 7 (seeded-recall set).** The sizing must state a minimum n per gating class (safety, decision-bearing, missing) with the Wilson arithmetic, or, where the Wilson half-width cannot reach 5 points with a deliverable of the size chosen, say so and write that the recall pass line is advisory for that class, with the interval the owner will see. State the rule that stage 3 runs each pass with fresh agent spawns and alternated order. Keep the answer key separate.
16: - **Task 9 (spec corrections).** Add to the existing spec edits (stale statements about the empty table and the 15 to 20 row held-out half; the M, C, E sentence): draft these definitions into the spec, each marked "proposed, for owner acceptance at the stage 1 go": (a) "safety miss" for the stage 3 entry count, meaning a finding that a later review or the owner confirms is a security, data-loss or safety-boundary risk that a shadow run recorded as a follow-up or Note and did not route through the GR12 safety route; (b) the stage 2 exit numbers: ledger volume per run, share of rows tagged `consumer-unknown`, offers made and answered, and the shadow agreement figures of the classifier against the reviewers' labels; (c) the stage 3 audit-window numbers: the revert triggers and the M12 report the spec names (read the spec's section 12 and its revert-trigger and M12 text and quote their definitions, do not invent them). Also record in the spec these staging decisions of the review: the merge-rule allow-list lists files by path only and the plugin mirror joins it only in stage 4; `agent_template_analysis.md` gets the merge-rule text only and the registry keeps exactly 11 `digest` rows; T3's `src/superclaude` check applies to `digest` and `canonical` rows only and a `pointer-only` row is checked only once its pointer is present. Each edit is listed in `./artifacts/spec-reconciliation.md` with its old and new text.
17: - **Task 10 (owner summary).** The summary also lists the drafted definitions of Task 9 for the owner to accept or change, the staging decisions above, the stage ledger of `stage-requests/README.md` (which stage packages exist), and the five findings of the stage 0 results that matter most for the stage 1 go. It still ends with the sentence that the owner's go for stage 1 is given in chat and not by this file.
18: 
19: ## Not to be done by the plan
20: 
21: Edit nothing under `src/`, `tests/`, `.claude/` or `plugins/` while generating the plan or in any task. Do not change the cap of 2 fix cycles, the own-scale primitives, `sc-implement-protocol/refs/qa.md` or the 35 percent target. No Jev call, key or account. No task for stages 1 to 4.
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
