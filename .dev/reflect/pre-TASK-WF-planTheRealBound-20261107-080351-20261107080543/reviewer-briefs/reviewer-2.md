# Reviewer 2 brief (persona: qa; model class: haiku)

Mode: UC-1 pre-execution reflection. You are read-only. Do not run commands that change anything. Audit only what is below plus the files you can Read.

Spec (driving request): .dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/source.md
Plan under review: .dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/TASK-WF-planTheRealBound-20261107-080351.md
Gap list the spec points at: .dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/retries/T1/review-2.md (findings F2.1 to F2.6)

## Your lens (qa)
Judge each task's `Acceptance criteria:` as a tester: is each bullet observable, checkable by someone who sees only that task and the plan's Constraints, and impossible to satisfy by writing a report alone? Look for criteria that can pass vacuously, for evidence an executor could fabricate, for a result that can be written as `observed` without a captured selector line, and for contradictions between Constraints and tasks (for example the twelve-run cap versus the cases in Tasks 2-4, or the no-global-settings rule versus a pty-driven interactive session).

## Coverage-matrix slice
All 10 inferred rows (artifacts/coverage-matrix.yaml) map to tasks; test the mapping, not just the count.

## Grounding hunks
- Plan Constraints are the first section of the plan after Goal; acceptance bullets are under each `## Task N:`.
- T1 card risks R1-R5 are in artifacts/t1-reflection-card.md.

## Output (return as text, no file writes)
One card in this shape: `findings:` list; each finding has `id`, `severity` (high|medium|low), `claim`, `citation` (`path:line` you Read yourself), `type` (vacuous-criterion | fabricable-evidence | contradiction | other), `recommendation`. Then `calibration_self_report: <0-1>`. Tag anything you could not cite as [INFERRED].
