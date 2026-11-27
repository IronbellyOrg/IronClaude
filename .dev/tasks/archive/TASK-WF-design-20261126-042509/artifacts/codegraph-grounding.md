# Codegraph grounding for TASK-WF-design-20261126-042509

## Run state

- index_state: fresh
- checked_at: 2026-11-26T04:26:25Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
- projectPath passed on every call: /home/coder/workspaces/worktrees/IronClaude/issue-676
- access: mcp (lookup tools listed)
- tokens: none
- Status answer: 3749 files, 0 added, 0 modified, 0 removed since the index.

## Resolved symbols

| Source names | Resolved to | Lines (HEAD 3cf7e2259) |
|---|---|---|
| `install_core_files` | `src/superclaude/cli/install_core.py` | 33 |
| `install_agents` | `src/superclaude/cli/install_agents.py` | 15 |
| `install_templates`, `list_installed_templates`, `list_available_templates`, `_PROTECTED_TARGET_SUBDIRS` | `src/superclaude/cli/install_templates.py` | 30, 145, 131, 27 |
| `backup_if_differs`, `same_content`, `_backup_target` | `src/superclaude/cli/install_keep.py` | 40, 18, 30 |
| `install_commands`, `_copy_tree` (the pattern to copy) | `src/superclaude/cli/install_commands.py`, `src/superclaude/cli/install_user_setup.py` | 16, 87 |
| `install`, `update` | `src/superclaude/cli/main.py` | 46, 356 |
| `_baks`, `_rewrite_keeping_stat` | `tests/cli/test_install_keep.py` | 32, 39 |
| `_stub_installers`, `native_install`, `isolated_home_guard`, `_stub_listings` | `tests/cli/test_update_command.py` | 74, 188, 34, 153 |
| `_INSTALLERS` row table | `tests/unit/test_cli_install.py` | 993 |

Documentation, test and guide files the design names were resolved by Glob and Read (markdown is not indexed).

## Dependents

Caller rows are definition-line leads; the call sites below were confirmed by Read.

| Symbol | Dependents (call sites) |
|---|---|
| `install_core_files` | `main.py:180` (install), `main.py:383` (update); tests: `tests/cli/test_bash_inspection_policy.py:38`, `tests/cli/test_how_we_work_install.py:30,67,90,110,132`, `tests/cli/test_issue_body_templates.py:32`, `tests/cli/test_install_keep.py:72,73,77`, `tests/cli/test_install_failures.py:75` (parametrized), `tests/unit/test_cli_install.py:917` |
| `install_agents` | `main.py:198`, `main.py:396`; tests: `tests/unit/test_cli_install.py:933`, `tests/troubleshoot/test_diagnostic_worker_contract.py:414`, `tests/cli/test_install_failures.py:75` (parametrized) |
| `install_templates` | `main.py:229`, `main.py:417`; tests: `tests/unit/test_cli_install.py:959`, `tests/cli/test_install_failures.py:75` (parametrized) |
| `list_installed_templates` | `main.py:144` (the `install --list` count line, 153-155); stubbed by `_stub_listings` in `tests/cli/test_update_command.py:164` |
| `backup_if_differs` | `install_commands.py:68`, `install_user_setup.py:114`; tests `tests/cli/test_install_keep.py:85,93,94` |
| `install_agents` module | `install_retired_files.py:164` reads only `list_available_agents`; unaffected |

Blast radius of the change: the behaviour reaches users only through `superclaude install --force` and `superclaude update` (the only production callers). Every existing test caller either runs without force or force-installs into an empty target, so none reaches the new backup branch.

## Pre-check

Advisory; the plan was not changed by this section. Checked 2026-11-26 after the gate, with the fresh index and Read, Grep and Glob (no second readiness check).

- Files named by the 20 tasks: 31 of 31 exist (three installers, `install_keep.py`, `install_commands.py`, `install_hooks.py`, `main.py`, `doctor.py`, `install_retired_files.py`, `recommend/prompts.py`, 10 test files, both copies of the routing guide, 7 documentation files, `CHANGELOG.md`, the `archive_workspace.py` plugin script).
- Symbols named by the tasks resolve: `_baks` (test_install_keep.py:32), `_rewrite_keeping_stat` (39), `isolated_home_guard` (test_update_command.py:34), `_stub_installers` (74), `_stub_listings` (153), `native_install` (188), `test_install_force_target_do_not_redirect` (255), `test_update_propagates_hook_install_failure` (118), `_INSTALLERS` (tests/unit/test_cli_install.py:993), `list_installed_templates` (install_templates.py:145), `list_available_templates` (131), `_PROTECTED_TARGET_SUBDIRS` (27); `pyproject.toml` line 7 is `version = "6.1.0"`.
- Dependents named by the tasks are real (Dependents table above). Dependents of the touched symbols that no task named when the gate ran, now handled: `tests/commands/test_worktrees_command.py` (reads both copies of the routing guide; named in Tasks 12, 13, 20) and `tests/pr_submit/test_conflict_sync_protocol.py` (reads `docs/user-guide/flags.md` and `CHANGELOG.md`; named in Tasks 13, 20).
- Unnamed and unaffected: `_stub_listings` stubs `list_installed_templates` (no call reaches the new filter); `install_retired_files.py` reads only `list_available_agents`; `tests/audit/test_full_docs_audit.py` builds its own CHANGELOG fixture.
- Added after the gate: the consumer grep (AC-6) is now an acceptance bullet of Task 6.
- Nothing is empty or unresolved; no `graph:*` token was needed.
