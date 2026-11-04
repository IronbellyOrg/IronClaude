# Task 14: remaining failures

None. No test failed, so no master comparison was needed and no `issue302-master-check` worktree was created.

| Check | Command | Outcome | Log (outcome line) |
|---|---|---|---|
| Targeted suite | `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py` | 1411 passed, rc=0 | `./t14-targeted.log` |
| Full suite | `uv run pytest` | 14830 passed, 136 skipped, 2 xpassed, 0 failed, 0 errors, rc=0 | `./t14-full-pytest.log` |
| Lint | `make lint` | `All checks passed!`, rc=0 | `./t14-lint.log` |
| Sync | `make verify-sync` | `All components in sync.`, rc=0 | `./t14-verify-sync.log` |

Environment notes (not failures):

- `ruff` was not installed in this worktree's `.venv`, so `make lint` could not start it. `make install` (the project's own setup target, `uv pip install -e ".[dev]"`, which pins `ruff==0.15.20`) was run first; its output is in `./t14-make-install.log`. No project file changed.
- The full suite rewrites the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json` with new timing numbers (`tests/cli/eval/test_perf_home_setup.py` writes it; existing behaviour, not part of this feature). The file was unmodified before the run; it was restored with `git restore -- .dev/releases/current/cliEval/evidence/T02.15/perf.json` so the branch carries no unrelated change.
