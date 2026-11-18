# Codegraph grounding

## Run state

- index_state: fresh (MCP `codegraph_status`: 0 added, 0 modified, 0 removed)
- checked_at: 2026-11-17T22:21:36Z
- worktree_root / projectPath: /home/coder/workspaces/worktrees/IronClaude/v6-help-text-fixes
- access: mcp
- tokens: none

## Resolved symbols

| Symbol | File | Resolved by |
|---|---|---|
| `_check_codegraph` | `src/superclaude/cli/doctor.py:146` | Read |
| `run_doctor` | `src/superclaude/cli/doctor.py:17` | codegraph_callers, Read |
| `doctor` (click command) | `src/superclaude/cli/main.py:477` | codegraph_node, Read |
| `recommend_group` | `src/superclaude/cli/recommend/commands.py:35` | codegraph_impact, Read |
| `/sc:help` description read | `src/superclaude/commands/help.md:25,33,58` | Read |

## Dependents

Rows are `resolution: def-line` (caller definition lines; not call sites).

- `_check_codegraph` (10 found, shown 10/10): `run_doctor` (`doctor.py:17`); tests in `tests/unit/test_cli_doctor.py` (lines 259, 267, 276, 282, 290, 313, 320) and `tests/cli/test_update_command.py:381`.
- `run_doctor` (3 found, shown 3/3): `doctor` (`main.py:477`), `tests/unit/test_cli_doctor.py:327`, `tests/cli/test_install_retired_mcp.py:579`.
- `recommend_group` (impact depth 1): `src/superclaude/cli/main.py` registration, `tests/recommend/test_dispatch.py:134`.
- Business-panel, cleanup and PM edits are Markdown (not indexed): dependents found by Grep, listed in `.dev/cleanup/help-text-fixes/dependency-map.md`.

## Pre-check

Checked 2026-11-17 (codegraph fresh, floor Grep/test -f for Markdown):
- All 21 files the five tasks name exist (`test -f`), including the three tracked copy sets.
- Symbols resolve: `_check_codegraph` (`doctor.py:146`), `doctor` (`main.py:477`), `recommend_group` (`commands.py:35`).
- Listed dependents are real: `run_doctor` callers 3 of 3, `_check_codegraph` callers 10 of 10, all named by Task 3 or already covered by its acceptance criteria.
- Dependents no task names: none found.
- Result: 5 tasks checked, 0 problems. Plan not edited.
