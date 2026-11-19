# Reflect report (pre-execution): zero-setup issue watcher plan v2

Mode pre, Tier 2 (rubric rule 4: more than three domains, 23 tasks). Status partial: the evidence check corrected 9 items, the debate ran at quick depth and scores are estimated.
Spec: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-010910/source.md
Plan: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-010910/TASK-WF-requirements-20261119-010910.md
Merged findings (read this): /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/reflect/pre-TASK-WF-requirements-20261119-010910-20261119011330/adversarial/merged-output.md

## Result
FAIL as advice: 4 blocking, 5 medium, 2 notes. Nothing was edited. All 12 earlier findings (M-1 to M-12) were confirmed fixed by all three reviewers.

## Blocking
| Id | Where | What |
|---|---|---|
| P-1 | Tasks 4, 8, 9 | A launched agent running issue-pipeline complete writes the comment and Status from inside Python, past the launch-level guard and the coordinator-only write rule (WORKER-CONTRACT.md:241-243, :300). Owner decision |
| P-2 | Task 10 | Task 10 says tests/issue_watch/test_security_invariants.py still passes; lines 915 and 918 assert the old literal repo and the absence of owner/name variables, so it fails by design |
| P-3 | Task 18 | A child killed after launching prints no launched or attempted line, so the loop can launch a second issue in one sweep (R5, R26) |
| P-4 | Task 5, R25 | Nothing proves who set the Pipeline field or when; approval compares label times only (predicates.py:228-233, :249-258). Owner decision |

## Flags
- tier 2, merge_method adversarial, convergence 0.8125, depth quick, position-bias check not run.
- t2_vendor_diversity single; calibrator classes not disjoint (calibrator_diversity degraded).
- Calibrated card confidence 0.76, 0.69, 0.70.
- Unchecked: Tasks 10 to 22 in depth, tests/hooks bodies, conftest.py.
