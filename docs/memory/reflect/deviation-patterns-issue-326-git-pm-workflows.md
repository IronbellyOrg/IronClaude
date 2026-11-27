# Reflect deviation patterns: issue-326-git-pm-workflows

## pre-TASK-WF-design-20261126-162939-20261126164050 (UC-1, /sc:git + implement commit step plan review)
- Verdict partial (tier 2, convergence 1.00 blocked by one HIGH invariant, calibrated 0.82): 11 Blocking, 14 Medium, 10 Note findings on a 38-task plan; nothing ran, so no Regression.
- Recurring plan-defect class: a plan Constraint that bans a token ("no code or text uses `--no-verify`") while a task must write that token into a deny-list; `/sc:implement` QA quotes Constraints, so the plan halts itself.
- Recurring plan-defect class: a task that edits a primitive under `src/superclaude/` leaves its `plugins/superclaude/` twin to a last task, while existing byte-parity tests run in the tasks in between.
- Recurring plan-defect class: a new reason, halt line or Ruling line added to the implement protocol hits an existing static test that pins the old set (`_TRANSIENT` in `test_task_workspace_lifecycle.py`, `_ALLOW` in `test_implement_severity_static.py`); check every test that scans the files a task edits.
- Recurring plan-defect class: an acceptance check that cannot pass as written (a repo-wide "only file that does X" scan, `git ls-files` after a plain delete, a routing test run before the file it resolves exists).
- Reflect mechanics: a design whose ids are FR/NFR/DD/AC (not R/REQ/SPEC) gives only T-nn Pass-1 ids, so coverage_degraded parsed-sparse forces tier 2; expand the plan's own "FR-110 to FR-118" ranges before counting unmapped ids (the first count was 0.66, the corrected one 0.85).
