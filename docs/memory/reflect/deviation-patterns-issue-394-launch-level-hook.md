# Reflect deviation patterns: issue-394-launch-level-hook

## pre-TASK-WF-implementTheLaun-20261107-092804 (UC-1, launch-level hook plan review)
- Verdict partial (tier 2, convergence 1.00 blocked by one HIGH invariant, calibrated 0.66): 1 HIGH, 14 MEDIUM, 10 LOW Drift findings; no Regression (nothing ran).
- Recurring plan-defect class: a task that adds a pre-launch check to `orca_worktree.py` (here IR-4 and IR-7 refusals) breaks the shared `launch_scene` fixture (`tests/skills/test_issue_orca_worktree.py:1011` writes a bare `#!/bin/sh`) and about 12 `launched` tests; the plan must migrate the fixture and name every re-baselined test.
- Recurring plan-defect class: an evidence gate written as a document with no downstream task depending on its verdict stops nothing.
- Recurring plan-defect class: a pass case that needs a file the plan never builds (an "owned L2 hook") has no fixture; define the proof or test only the absence.
- Reflect mechanics: a one-sentence prompt spec gives 0 Pass-1 ids, so coverage_degraded parsed-sparse forces tier 2 (same as the claim-pipeline plan review).
