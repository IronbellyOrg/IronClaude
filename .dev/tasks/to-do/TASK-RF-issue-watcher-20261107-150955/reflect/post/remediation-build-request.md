# BUILD_REQUEST: remediation of the POST reflect findings for issue 331 (issue-watch poller)

Status: AUTHORED ONLY. Reflect ran its Wave 6 in the HUMAN-REQUIRED branch (a Regression stands, `needs_human_decision: true`), so no task file was built and nothing here is auto-runnable. An owner decides, then hands this file to `task-builder` (MDTM route, `--remediate --depth deep`) or writes a smaller plan.

Goal: Resolve the blocking Regression R-1 and the non-blocking Regression-class and Drift rows of the report `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/REPORT.md`, without touching any file outside the list below.

## Deviations To Remediate

- Regression R-1 (BLOCKING, LOW): a launch can start after the 120 s cutoff when the durable pending save crosses it. `src/superclaude/cli/issue_watch/cycle.py` lines 1060-1062. Required repair: capture the document before `mark_pending`, re-check `launch_allowed()` after `_save()`, restore and save the captured document and raise `_Skip("budget_exhausted")` if the cutoff passed.
- Regression R-5 (MEDIUM, non-blocking): five skip sites in `tests/issue_watch/test_cli.py` (967, 1070), `test_record.py` (739), `test_cycle.py` (735, 4694). Repair: root-independent checks, stubbed mountinfo.
- Regression R-6 (LOW): `runner.py`/`launch.py` search the operation-unknown marker in stderr already capped at 500 bytes. Repair: detect it before the cap.
- Regression R-2, R-3 (LOW): exit 1 `cycle_crashed` and the 59-name reason table are not in the design or spec. Decision needed: amend the documents (recommended) or remove the additions.
- Regression R-4 (LOW): `record.py` imports `valid_operation_id`. Decision needed: amend the design/task text or use a local copy.
- Regression R-7 (LOW, effectively unreachable): retry list drops an unknown entry whose argv cannot be built.
- Drift D-1..D-4 (LOW): runbook/design exit and platform facts; `cli.py` uses `cycle.format_utc`; duplicated login regex and UTC format in `cycle.py`; wall-clock read in `audit.stderr_fallback`. Decision per item: backfill the design or revert the code.

## Files

- src/superclaude/cli/issue_watch/cycle.py
- src/superclaude/cli/issue_watch/runner.py
- src/superclaude/cli/issue_watch/launch.py
- src/superclaude/cli/issue_watch/record.py
- src/superclaude/cli/issue_watch/cli.py
- src/superclaude/cli/issue_watch/audit.py
- tests/issue_watch/test_cycle.py
- tests/issue_watch/test_cli.py
- tests/issue_watch/test_record.py
- tests/issue_watch/test_launch.py
- tests/issue_watch/test_module_boundaries.py
- docs/designs/issue-watcher.md
- docs/designs/issue-watcher-setup.md

## Acceptance

- `uv run pytest tests/issue_watch -q` passes with 0 skipped, including as uid 0.
- A new test whose clock passes 120 s inside `store.save` asserts no launcher call, the restored document and a `budget_exhausted` decision line.
- `uv run ruff check src/superclaude/cli/issue_watch tests/issue_watch` and `uv run ruff format --check` stay clean.
- `pyproject.toml`, `Makefile` and `.github/` stay unchanged.

## References

- Report: .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/REPORT.md
- Deviation register: .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/adversarial/merged-verdict.yaml
- Grounding gaps: .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/grounding-gaps.yaml
- Handoff key: reflect/handoff-issue-331-github-issue-watcher-20261108T0620Z

## Reflect Verdict State

needs_human_decision: true
regression_count: 7
drift_count: 4
grounding_gaps: see References
(Downstream stages may append findings but must not downgrade a Regression item or clear needs_human_decision.)
