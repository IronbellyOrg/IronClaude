# Reflect report (pre-execution): zero-setup issue watcher plan

Mode pre, Tier 2 (rubric rule 4: three domains, 20 tasks). Status partial: the evidence check dropped or corrected 4 items, and the debate ran at quick depth.
Spec: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261118-233559/source.md
Plan: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261118-233559/TASK-WF-requirements-20261118-233559.md
Merged findings (read this): /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/reflect/pre-TASK-WF-requirements-20261118-233559-20261118234500/adversarial/merged-output.md

## Result
Verdict FAIL as advice: 4 blocking, 8 medium, 1 note group. Nothing was edited; the plan is unchanged.

## Coverage (UC-1)
- Parsed requirement rows: 23 (R1 to R23). Fully mapped: 22. Weak: R20 (a Coder row; the plan records the open question, which is the right handling, only its acceptance wording is wrong).
- coverage_pct 0.957 (parsed), coverage_pct_union 0.917 (one inferred row, source.md:62, lock and restart tests, unmapped).
- Details: .../artifacts/coverage-matrix.md

## Blocking findings
| Id | Where | What |
|---|---|---|
| M-1 | Tasks 14-15 | After an unknown launch outcome (cycle.py:1106-1109) no `launched:` line prints, so a second repo can launch in the same sweep |
| M-2 | Task 5 | Prompt is built (cycle.py:1054) before the revalidation reread; a Status or Pipeline changed in between would launch the old command |
| M-3 | Task 13 | R18 names the lock test and restart test; the first-run check omits them |
| M-5 | Tasks 4, 6 | "Create the approval record from approver id and event id" fits only a plan-hash approval row (approval_record.py:132-153), which must come from the worker's ask (WORKER-CONTRACT.md:298), not a claim-time label |

## Flags
- tier 2, merge_method adversarial, convergence 0.857, depth quick, position-bias check not run, scores estimated.
- t2_vendor_diversity single (all Anthropic), calibrator classes not disjoint (all three classes were reviewers): calibrator_diversity degraded.
- citations dropped or corrected by the evidence validator: 4 (record.py header cite, "R18 is later", "R23 rows stale" as file facts, M-7 Task 18 claim).
- Unchecked: record.py:381, conftest beyond 244-248, tests/hooks, tests/skills, tests/commands.
