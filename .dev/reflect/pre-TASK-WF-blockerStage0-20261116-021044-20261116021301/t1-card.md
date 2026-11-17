# T1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/source.md` (21 lines: the stage 0 plan request, one of five requests written for the one-plan-per-stage decision)
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (4 phases, 10 tasks, schema workflow-plan/1.2)
Author of this card: the orchestrator that also authored the plan (self-review; the T2 reviewers exist to break that bias).

## Coverage and acceptance

The source has no labelled requirement ids (parsed_count 0). Step 1B.0 Pass 2 emitted 18 quote-pinned inferred rows (`artifacts/coverage-matrix.yaml`; each quote is a verbatim substring of its cited `source.md` line). The containment rule matched 15 of 18 (`coverage_pct_union` 0.833); the three unmatched-by-task rows (INF-002, INF-016, INF-017) map to the Constraints block, which is the intended home: one package one stage (INF-002), no Jev call (INF-016), the cap of 2 fix cycles (INF-017). Every change the request lists for Tasks 6, 7, 9 and 10 has its text in those tasks.

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

## Self-reported confidence

0.80 (self-review by the plan's own author; the executor-side decisions in Tasks 2, 4 and 6 were not tested).
