# Phase 8 validation (item 8.13)

Run 2026-11-12, in order, after `uv run ruff format tests/sweep/test_readonly.py` fixed the one format failure of the first run (logged in Phase 8 Findings). Each block: the command, its exit code, the last 30 output lines, then one PASS or FAIL line.

## ruff check

Command: `uv run ruff check src/superclaude/cli/sweep tests/sweep`
Exit code: 0

```text
All checks passed!
```

PASS: ruff check

## ruff format --check

Command: `uv run ruff format --check src/superclaude/cli/sweep tests/sweep`
Exit code: 0

```text
9 files already formatted
```

PASS: ruff format --check

## import the three modules

Command: `uv run python -c import superclaude.cli.sweep.classify, superclaude.cli.sweep.probes, superclaude.cli.sweep.report`
Exit code: 0

```text
```

PASS: import the three modules

## pytest tests/sweep -v

Command: `uv run pytest tests/sweep -v`
Exit code: 0

```text
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.venv/bin/python
cachedir: .pytest_cache
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collecting ... collected 4 items

tests/sweep/test_readonly.py::test_git_argv_and_env_are_lock_free PASSED [ 25%]
tests/sweep/test_readonly.py::test_check_git_args_allows_only_the_listed_call PASSED [ 50%]
tests/sweep/test_readonly.py::test_one_git_argv_per_worktree PASSED      [ 75%]
tests/sweep/test_readonly.py::test_real_git_lock_free_status_and_gitignore PASSED [100%]

============================== 4 passed in 0.31s ===============================
```

PASS: pytest tests/sweep -v
