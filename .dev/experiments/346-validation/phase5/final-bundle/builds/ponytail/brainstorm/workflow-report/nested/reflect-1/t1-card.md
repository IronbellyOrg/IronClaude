# T1 reflection card (UC-1, pre-execution)

hypothesis_source: inline-orchestrator (UC-1 has no Wave 1C agent at standard depth; the orchestrator also authored the plan, so this card is self-review and is not load-bearing; Tier 2 reviewers re-audit it)
spec: .dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md
tasklist: .dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md
coverage matrix: artifacts/coverage-matrix.yaml (Wave 1B)

## Analyzer section (deviation / root-cause)

- A1. Plan adds a change ./source.md does not list: `tests/recommend/test_routing_refresh.py` line 33 `_POST_REFRESH_ADDITIONS` gains `spec-panel-ponytail` (plan Task 7). Grounded: tests/recommend/test_routing_refresh.py:33 and :647-648 (`shipped - _POST_REFRESH_ADDITIONS == active`). Classification candidate: necessary (a new command file breaks this assertion otherwise).
- A2. Plan omits the `## Unattended mode` section from the variant, against ./source.md section 3.1 row 1 ("Byte copy ... with only these differences"). Grounded: src/superclaude/commands/spec-panel.md:451 (section heading), tests/skills/test_worker_contract.py:830-839 (set equality on commands having that section). Plan Constraints cite an owner ruling. Classification candidate: authorized (owner ruling) / necessary.
- A3. Owner decisions in the plan Constraints override ./source.md section 2.6 ("recorded as minor and closed, not open") with a still-open owner count (plan Task 5). Classification candidate: authorized (coordinator brief owner decision).
- A4. Plan Task 12 copies six S1 briefs and makes no command-name substitution in review briefs; ./source.md section 4 requires T05-T09 byte-identical. Consistent.

## QA section (coverage / acceptance)

- Q1. ./source.md section 3.5 grade-parse bullet requires a test that "`MAJOR (FR-8 GAP)` graded minor counts as protected"; plan Task 2 acceptance criteria list the four formats, non-blocking and unknown/conflicting, but not the FR-8-protected case. Candidate gap.
- Q2. ./source.md section 3.5 hunks bullet names "incidental id mentions"; plan Task 2 AC covers partial words and bare numbers but does not name incidental mentions explicitly. Candidate gap (minor).
- Q3. ./source.md section 2.5 "one smoke dispatch settles it before S1" (plugin skill in a dispatched worker) is carried only as an open precondition line in INSTALL.md (Task 11), not as a task. Out of declared scope (experiment run), candidate advisory.
- Q4. ./source.md section 3.5 static bullet "the canonical cap text and at-cap clause ... are present" is in Task 8. ./source.md section 3.5 "Keep green" list is in Task 8 AC. Covered.
- Q5. Sections 5 and 6 (measurement, replicates, paired fork, blind re-grade, falsifiers F1-F5) are excluded by the plan Constraints per the coordinator scope (sections 3 and 4). Expected unmapped rows.

## Refactorer section (structure / risk)

- S1. Plan Task 12 reads two source paths under /tmp/impl/exp/s1/ that may not survive until /sc:implement runs; the plan says stop and report blocked. Risk: Task 12 blocks.
- S2. Plan Task 8 stages new delivery files with `git add` so tracked-file scans see them; staging inside an /sc:implement run may interact with its private-index snapshots. [INFERRED] no direct evidence of conflict.
- S3. The `verdict` owner count depends on parsing review-3 new-finding labels whose real format is unknown until S1 runs; tests use synthetic fixtures only. Risk carried by fail-closed exit 2.
- S4. Plan has 12 tasks in 5 phases, contiguous numbering, every task has Acceptance criteria (Wave 3 gate of the workflow passed).

## Self-assessed confidence (not used; calibrator re-grades)

0.80
