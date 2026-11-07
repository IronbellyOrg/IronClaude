# Reviewer 1 brief (persona: analyzer; model class: sonnet)

Mode: UC-1 pre-execution reflection. You are read-only. Do not run commands that change anything. Audit only what is below plus the files you can Read.

Spec (driving request): .dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/source.md
Plan under review: .dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/TASK-WF-planTheRealBound-20261107-080351.md
Gap list the spec points at: .dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/retries/T1/review-2.md (findings F2.1 to F2.6)
Design: docs/designs/sc-issue-launch-level-hook.md section 19 (19.1 at lines 491-506, 19.7 at lines 547-565)

## Your lens (analyzer)
Does every spec requirement land in a task with an observable acceptance criterion, and is every factual claim the plan makes about existing code true? Check with Read/Grep: the plan names src/superclaude/hooks/scripts/launch-job-identity.sh (its `identify` action, release reason, boot and start-tick comparison), tests/hooks/fixtures/launch_level/live_probe.py (its isolated HOME and --settings pattern), and the blocked package's actor-context-probe.sh. Report any claim that is false, any requirement with no task, any task that cannot be executed as written.

## Coverage-matrix slice (all 10 inferred rows map; see artifacts/coverage-matrix.yaml)
INF-003, INF-004, INF-005, INF-006, INF-007 are the ones to test hardest.

## Grounding hunks
- codegraph run state: not used (floor: Grep/Read).
- launch-job-identity.sh:215 `def identify(pid)`; :530 `identify` action in `main`.
- live_probe.py:310-319 lists the unobserved cases; :280 maps a nested-session refusal to `nested_guard_blocked`.
- T1 card risks R1-R5 are in artifacts/t1-reflection-card.md.

## Output (return as text, no file writes)
One card in this shape: `findings:` list; each finding has `id`, `severity` (high|medium|low), `claim` (what is wrong), `citation` (`path:line` you Read yourself), `type` (coverage-gap | false-claim | infeasible-task | other), `recommendation`. Then `calibration_self_report: <0-1>`. Tag anything you could not cite as [INFERRED]. Do not paraphrase from this brief: Read the file and cite its line.
