# Codegraph grounding

## Run state

index_state: fresh (`codegraph_status`: 3844 files, 0 added, 0 modified, 0 removed)
checked_at: 2026-11-19T01:38Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
access: mcp
tokens: none. Symbol lookups were done with Grep and Read (the targets are two small functions); no graph row is cited.

## Resolved symbols

- `src/superclaude/cli/install_core.py:121-125` `_same_content(a, b)`: private helper, body `filecmp.cmp(a, b, shallow=False)` with `except OSError: return False` (Read).
- `src/superclaude/cli/install_core.py:8` `import filecmp`: the only use of `filecmp` in this file is line 123 (Grep).
- `src/superclaude/cli/install_keep.py:18-26` `same_content(a, b)`: calls `filecmp.clear_cache()` first, same `try` body (Read).

## Dependents

- `src/superclaude/cli/install_core.py:97` is the only caller of `_same_content` in the repo (Grep of `_same_content` over `src` and `tests`, hits only in `install_core.py`). It decides which skipped files are listed as "NOT updated".
- Tests that exercise the caller: `tests/cli/test_how_we_work_install.py:101-114` `test_skip_without_force_names_only_stale_files` (reads `message.split("NOT updated")[1]`), and `tests/cli/test_how_we_work_install.py:66` and `:89` via `install_core.install_core_files`.
- `src/superclaude/cli/install_user_setup.py:90` and `src/superclaude/cli/install_commands.py:61` already use `install_keep.same_content`; unchanged.

## Pre-check

Files named by the plan exist: `src/superclaude/cli/install_core.py`, `src/superclaude/cli/install_keep.py`, `tests/cli/test_how_we_work_install.py`. Symbols resolve. No dependent of `_same_content` is left unnamed by a task. Import check: `install_keep` imports only `filecmp`, `shutil`, `datetime`, `pathlib`, so importing it from `install_core` makes no cycle.
