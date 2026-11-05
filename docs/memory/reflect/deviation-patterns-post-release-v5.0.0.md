# Reflect deviation patterns — post-release-v5.0.0

## pre-workflowSource-20261102234109 (UC-1, /sc:workflow plan for /sc:post-release v5.0.0)
- Recurring pattern: a spec "verification" constraint (smoke pytest + final `make test`) is dropped by the plan because the workflow template forbids verification-only tasks (quality-gates.md:22) and `/sc:implement` treats tests as extras (implement.md:11). Net effect: nothing runs the suite. Remedy: put the check in the last real task's AC with a recorded baseline and a saved log, or have the orchestrator run it.
- Recurring pattern: reviewers recommend editing the plan, but workflow's Wave 4 reflect is advisory and may not edit `<id>.md`; route remedies to the executor or orchestrator.
- Recurring pattern: removal-grep ACs ("grep X returns nothing") contradict items that tell the writer to state "X does not exist / is planned".
- Fresh worktrees fail ~43 mirror/ruff tests until `make install` and `make sync-dev` run; record a baseline after both.
