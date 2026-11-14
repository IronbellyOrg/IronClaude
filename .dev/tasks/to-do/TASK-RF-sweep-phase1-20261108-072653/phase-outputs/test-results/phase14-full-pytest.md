# Phase 14 full test run (item 14.4)

Run 2026-11-12 in the background (the run took 16 minutes 40 seconds, longer than the 600 s foreground limit).

Command: `uv run pytest`

Exit code: 1

Counts: 3 failed, 25252 passed, 149 skipped, 2 xpassed, 32 warnings in 1000.47s

Failing test ids:
```text
FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval
FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module
FAILED tests/hooks/test_launch_level_guard.py::test_speed_large_commands[1MB-big]
```

## Were the failures caused by this task?

No. Evidence:

- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval` and `::test_ruff_passes_on_real_adapter_module`: re-run alone, both fail the same way, with the message `.venv/bin/python: No module named ruff`. The tests call `python -m ruff` in the project virtual environment, where `ruff` is not an importable module (`uv run python -c 'import importlib.util ...'` prints `ruff module in venv: False`), while `uv run ruff --version` works (ruff 0.17.3, a system ruff at /usr/local/bin/ruff on PATH; `pyproject.toml:54` pins ruff==0.15.20 as a dev dependency that this venv lacks). This is an environment condition of this checkout. `git diff --stat 5dc29d23 -- src/superclaude/cli/eval tests/cli/eval tests/hooks src/superclaude/hooks` shows no change, and `git status --short` on those paths is empty: this task changed none of the files these tests read or run.
- `tests/hooks/test_launch_level_guard.py::test_speed_large_commands[1MB-big]`: a timing test. It passed when re-run alone (4 passed in the isolated run, which itself took 228 s on this loaded machine while about ten review agents were running). The full run overlapped those agents, so the time budget of the 1 MB case was exceeded. The same paths are unchanged against the base (no diff in `tests/hooks` or `src/superclaude/hooks`), so this task did not cause it.

Result: FAIL by exit code (3 failures), each recorded as pre-existing or environment-caused with its test id and reason in `### Phase 14 Findings`; the item's completion gate allows this ("every remaining failure is logged as pre-existing with evidence").

The full raw output is saved next to this file as `phase14-full-pytest-output.txt`.
