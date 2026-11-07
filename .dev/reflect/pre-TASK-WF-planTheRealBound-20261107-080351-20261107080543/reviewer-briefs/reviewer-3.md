# Reviewer 3 brief (persona: refactorer; model class: opus)

Mode: UC-1 pre-execution reflection. You are read-only. Do not run commands that change anything. Audit only what is below plus the files you can Read.

Spec (driving request): .dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/source.md
Plan under review: .dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/TASK-WF-planTheRealBound-20261107-080351.md
Design: docs/designs/sc-issue-launch-level-hook.md section 19 (19.1 lines 491-506, 19.7 lines 547-565)

## Your lens (refactorer)
Structure and scope: are the tasks independently reviewable, correctly ordered (`Depends on:`), the right size, free of duplicated work, and faithful to the spec's boundary (observation evidence and a report only; no production change, no real protected push, no global settings change, blocked package untouched)? Does any task quietly exceed that boundary, or does the plan miss a safeguard the spec implies? Also judge whether the binary B-CTX rule in Task 8 matches design section 19.1 and 19.7 (PASS only when every required distinction is observed; the merged design says the earlier plan stays historical).

## Coverage-matrix slice
All 10 inferred rows map (artifacts/coverage-matrix.yaml); look for requirements the matrix missed (anything in the spec the ten rows do not capture).

## Grounding hunks
- T1 card risks R1-R5 are in artifacts/t1-reflection-card.md.
- The plan has 4 phases and 8 tasks; Task 8 depends on Tasks 3, 4, 6 and 7.

## Output (return as text, no file writes)
One card in this shape: `findings:` list; each finding has `id`, `severity` (high|medium|low), `claim`, `citation` (`path:line` you Read yourself), `type` (scope-creep | ordering | missed-requirement | boundary | other), `recommendation`. Then `calibration_self_report: <0-1>`. Tag anything you could not cite as [INFERRED].
