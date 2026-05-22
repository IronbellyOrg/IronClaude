# T01.26 evidence — execution log

Date: 2026-05-20
Task: T01.26 — Register `superclaude eval` Click group without breaking existing commands (FR-G3)
Deliverable: D-0022

## Pytest

```
$ uv run pytest tests/cli/test_cli_registration.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
collected 5 items

tests/cli/test_cli_registration.py::test_top_level_help_lists_eval_group PASSED [ 20%]
tests/cli/test_cli_registration.py::test_top_level_command_roster_unchanged PASSED [ 40%]
tests/cli/test_cli_registration.py::test_eval_group_help_lists_m1_subcommands PASSED [ 60%]
tests/cli/test_cli_registration.py::test_eval_group_registers_m1_subcommands_in_click PASSED [ 80%]
tests/cli/test_cli_registration.py::test_pre_existing_command_help_still_invokable PASSED [100%]

============================== 5 passed in 0.14s ===============================
```

All five regression tests pass on 2026-05-20.

## CLI smoke — `superclaude --help` (AC1)

```
$ uv run superclaude --help
Usage: superclaude [OPTIONS] COMMAND [ARGS]...

  SuperClaude - AI-enhanced development framework for Claude Code

  A pytest plugin providing PM Agent capabilities and optional skills system.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  cleanup-audit  Multi-pass read-only repository audit with...
  cli-portify    Port inference-based SuperClaude workflows into...
  doctor         Check SuperClaude installation health
  eval           Run and inspect the cliEval real-eval harness.
  install        Install SuperClaude to Claude Code
  install-skill  Install a SuperClaude skill to Claude Code
  mcp            Install and manage MCP servers for Claude Code
  prd            Generate Product Requirements Documents via multi-step...
  roadmap        Generate project roadmaps from specification files.
  sprint         Orchestrate multi-phase Claude Code sprint execution.
  tasklist       Tasklist validation commands.
  update         Update SuperClaude to latest version
  version        Show SuperClaude version
```

`eval` listed alongside the 12 pre-existing top-level commands.

## CLI smoke — `superclaude eval --help` (AC2)

```
$ uv run superclaude eval --help
Usage: superclaude eval [OPTIONS] COMMAND [ARGS]...

  Run and inspect the cliEval real-eval harness.

Options:
  --help  Show this message and exit.

Commands:
  describe  Print a validated, post-parameterize-expansion manifest.
  doctor    Verify host preconditions for ``superclaude eval run``.
  list      Enumerate suite manifests under ``cli/eval/suites/``.
```

The three M1 subcommands (`describe`, `doctor`, `list`) are listed.
`run` (FR-CLI1, M4) is intentionally absent and lands in its own task.

## Regression — pre-existing command unchanged

The frozen `EXPECTED_TOP_LEVEL_COMMANDS` set in
`tests/cli/test_cli_registration.py` matches the observed `main.commands`
keys exactly; the `test_pre_existing_command_help_still_invokable` test
additionally invokes `--help` on every pre-existing command and asserts
exit 0. Both passed.

## Entry-point pointer

Registration site: `src/superclaude/cli/main.py:393-395`.

```python
from superclaude.cli.eval.commands import eval_group

main.add_command(eval_group, name="eval")
```

The wire-up was placed during earlier M1 tasks (T01.13/T01.21/T01.22) so
each subcommand could be smoke-tested via the live CLI; T01.26 validates
and pins the additive contract via `tests/cli/test_cli_registration.py`.
