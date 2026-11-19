# Task 29: full checks (2026-11-18)

| Check | Result |
|---|---|
| `uv run pytest tests/observe/ -v` | 1176 passed |
| `tests/observe/test_commands.py` gate-constant tests (`QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED`, `release-gates.md`, `Task 18`) | pass (inside the 1176) |
| `make lint` | exit 0 (`ruff check .`: all checks passed) |
| `make test` | exit 2: 25 failed, 16 errors, 28373 passed, 154 skipped, 2 xpassed (1377 s); log `/tmp/t29_test.log` |
| `git diff -- src/superclaude/cli/observe/export.py` | empty |
| paths under the dev mirror directory staged | 0 |
| `git add .dev/tasks` | done, 2707 files staged under `.dev/tasks/` (staging only, nothing committed) |

## The `make test` failures are not in the observer

Every failing or erroring test is outside `tests/observe/`: `tests/audit/` (8 files), `tests/cli/test_verify_sync_hooks.py`, `tests/cli/test_install_keep.py`, `tests/cli/eval/test_claude_process_adapter.py`. Their messages, from a rerun of four of those files:

- `FileNotFoundError` on the dev mirror files that `make sync-dev` creates from `src/superclaude/` (an agent file and a hook file in the worktree's gitignored dev mirror folder); `make verify-sync` reports `MISSING` for the same mirror.
- `No module named ruff` for `.venv/bin/python -m ruff` (two tests that call ruff as a module).

One failure has a different cause and is not about the mirror or ruff: `tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files` fails on its own rerun (13 pass, 1 fails); neither `src/superclaude/cli/install_keep.py` nor that test is touched by this work (the reviewer suspects the `filecmp` signature cache for two same-size files, unconfirmed). `tests/cli/test_verify_sync_hooks.py::test_V7_regression_to_master` belongs to the `make verify-sync` family (it runs the mirror check). Neither is in `tests/observe/` or reads a file this work changed.

This task changed only `src/superclaude/cli/observe/render.py`, `view.py` and `terminal.py` (earlier tasks), `tests/observe/`, and `.dev/` files; none of the failing tests reads them. The cause is the worktree environment: the dev mirror is not synced and ruff is not installed as a module of the venv. `make sync-dev` and `make install` would fix both; they were not run because `make sync-dev` writes the project hook files that this session's own hooks use, which is outside this task's scope.

So the criterion "`make test` passes" is NOT met as written; the cause is outside this change and needs the owner's choice (run `make sync-dev` and `make install`, or accept the 41 environment failures).
