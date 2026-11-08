fdeba1a744a7db65b9ac1ea1e65a8997d57f83b4
# Family probe for review r1-1 (T2)

## family=test-run-not-green

- Defect form: the saved `uv run pytest tests/cli/eval -v` run (AC-named log `artifacts/t2-pytest.log`) is not green: two tests in `tests/cli/eval/test_claude_process_adapter.py` shell out to `.venv/bin/python -m ruff` and fail with "No module named ruff" because the dev extra (pinned `ruff==0.15.20` in `pyproject.toml`) is not installed in the project venv.
- Probe command: `grep -n -F -e 'No module named ruff' -- .dev/tasks/to-do/TASK-WF-refactorAllMcpTo-20261108-150855/artifacts/t2-pytest.log`
- before:
  - 1535: E   AssertionError: adapter module trips its own ban rule: '' '/home/coder/workspaces/worktrees/IronClaude/mcp-litellm-migration/.venv/bin/python: No modul...
  - (summary line of the log: `2 failed, 1499 passed, 4 skipped`)
- Coupled sites: `tests/cli/eval/test_claude_process_adapter.py:417` (`test_ruff_flags_synthetic_anthropic_import_under_cli_eval`) and `test_ruff_passes_on_real_adapter_module` in the same module; `Makefile` `install:` target (`uv pip install -e ".[dev]"`). No product file is coupled; the fix is an environment install plus a rerun that overwrites the AC-named log.
  after: (no hits; summary line now `1501 passed, 4 skipped`, rc=0, new test at log line 185 PASSED)
