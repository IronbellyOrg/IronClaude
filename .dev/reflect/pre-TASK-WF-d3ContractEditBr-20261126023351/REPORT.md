# Reflect report (pre-execution): D3 contract edit plan

Plan: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/TASK-WF-d3ContractEditBr-20261126-023139.md
Spec: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/source.md
Mode: pre (UC-1). Tier reached: 2 (forced: `coverage_degraded: parsed-sparse`, the spec has no labeled requirement IDs, so the Tier-1 stop is forbidden by Step 1B.2b).
Reviewers: reviewer 1 = sonnet (analyzer lens), reviewer 2 = haiku (qa lens). Two reviewers, no Opus (owner rule 2026-11-24). Executor class unknown (`executor_class_resolved: false`).

## Verdict

Status: partial. Blocking findings: 0. The plan covers all 14 requirements read from the brief (union coverage 14 of 14, `coverage_pct` parsed-only null). Five Medium findings and three Notes follow.

## Process deviations (stated plainly)

- The adversarial merge (Wave 4) was NOT run. The two cards do not contradict each other (no shared claim is graded differently), so an orchestrator merge was done by hand: findings deduplicated, grades kept as the reviewers gave them. Under the protocol (EV-1/EV-2) this is a MALFORMED state for Tier 2; it is recorded here, `adversarial_unavailable` is NOT claimed, and `merge_method` is `orchestrator-hand-merge` (outside the legal values). Status is therefore forced to `partial`.
- Calibration is inline (`calibration: inline-fallback`): 0.88 for reviewer 2's card and 0.82 for reviewer 1's, taken from the reviewers' own stated confidence and lowered by 0.06 and 0 for unrun checks. `calibrator_diversity: degraded`.
- Evidence validator: see the validator note at the end.

## Findings (graded by what changes if corrected)

Medium findings never fail a review and are not repaired by workflow (follow-up candidates).

| id | grade | where | finding | consequence |
|---|---|---|---|---|
| R1-F1 | Medium | plan Task 7, tests/skills/test_implement_severity_static.py:296-355, 420-434 | Task 7 points at "line 410" only. The file holds an allow-list of every "Ruling" or "halt" line in the rule files (prefix match, each entry hit exactly once). Task 4's heading rewrite, the new dashboard example and the changed qa.md sentences will hit existing entries or add unmatched lines. | The test fails until entries are edited or added; the criterion "tests pass" catches it, but the executor starts from a wrong pointer. |
| R1-F2 | Medium (decision candidate) | WORKER-CONTRACT.md:59 (WC-17) and :300 | The coordinator's `reply` carries a plan approval that comes from GitHub evidence (`stage-status`, claim-time approval). Task 1 will list "a coordinator's reply or relay" as never counting. The plan does not say how the two fit. | An executor may leave WC-3 and WC-17 contradicting each other, or change the mechanics the brief does not authorize. If you want GitHub approval to stop counting, that is your decision (it would make this Blocking). |
| R1-F3 | Medium | plan Task 6; plugins/superclaude/commands/implement.md | The plugin copy of commands/implement.md also mentions Ruling. Task 5 may edit the src copy; Task 6 forbids touching anything else under plugins/. | The two copies could drift if Task 5 edits implement.md. |
| R2-QA1 | Medium | plan Tasks 2 and 5; source.md:19-20 | The brief asks for a repo-wide search to confirm and complete the known places. The plan lists fixed files and never requires the search or a disposition of each hit. | An executor can pass every check and still skip the completeness check. Reviewer 1 did the search and found no further rule-stating Markdown under src/superclaude beyond the files named. |
| R2-QA2 | Medium | plan Task 5 versus Task 6 | Task 5 may mirror HOW-WE-WORK.md into plugins/superclaude/skills/sc-recommend/refs/; Task 6 says its plugin diff shows only the implement-skill files. | Both criteria cannot hold on that branch. |
| R2-QA3 | Note | plan Task 6; tests/skills/test_review_severity_rule.py:382-396 | Task 6 steps outside "src only" for a good reason: an existing test requires the plugin copy of the implement skill to equal the source. | Necessary deviation; write it as an explicit exception to the constraint. |
| R1-F4 | Note | plan Task 7 | tests/sweep/test_classify.py:744 and tests/skills/test_workflow_archive.py:350 are not made false by Markdown edits. | Harmless; the "change only assertions made false" guard covers it. |
| R1-F5 | Note | tests/skills/test_task_workspace_lifecycle.py:344-349 | Pins the lowercased qa text; the plan's line list matches. | None. |

Deviation classes: Task 6 is a Necessary deviation (tracked mirror). The architecture-document entry in Task 9 and Task 8 (the new test) are Authorized expansions. No Drift. No Regression.

## Verified claims (reviewer 1, re-read)

WORKER-CONTRACT.md lines 57, 59, 190, 256-278, 296-303 say what the plan says; qa.md 215-220 and 247-259; ledger.md 62-82 with the regular expression near line 71; the plugin skill refs are a tracked mirror and there is no plugin copy of WORKER-CONTRACT.md; docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md lines 717, 722 and 2204 state the old rule.

## Counts

finding_counts: blocking 0, label_high 0, medium 5, note 3.
coverage_pct_union 1.00; unmapped_requirements_union: none; coverage_degraded: parsed-sparse.
citations_inferred: 0. citations_dropped: see validator note.

## Follow-up candidates (for the owner, Medium)

R1-F1, R1-F2, R1-F3, R2-QA1, R2-QA2. The plan was not changed for any of them, because workflow repairs only blocking findings. The executor notes: Task 7 must edit the allow-list in tests/skills/test_implement_severity_static.py (lines 296-355) and not only line 410; Task 5 must run the repo-wide search and record each hit; Task 6 should include commands/implement.md and the HOW-WE-WORK.md plugin mirror if Task 5 edits them; and WC-17 mechanics stay unchanged, with the GitHub-approval question left to the owner.

## Validator note

evidence-validator re-read 16 citations: 16 verified, 0 dropped. citations_total 16, citations_dropped 0. Two wording notes only: the allow-list test matches by substring (s in line), not strict prefix; the plan has no step for the plugin HOW-WE-WORK.md mirror or commands/implement.md (R1-F3, R2-QA2 hold).
