# Codegraph grounding

## Run state

- index_state: fresh
- access: mcp
- checked_at: 2026-11-18T15:04:00Z (status answer: 0 added, 0 modified, 0 removed; 3838 files)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/ccsession-saved-sessions
- degraded: graph:empty (the graph indexes Python, YAML and a few other languages, not the Bash scripts `ccsession`, `ccsession-orca` and `hooks/session-name.sh`; every Bash symbol below was found with Grep and Read, which is the permanent floor)

## Resolved symbols

| Symbol | File | Line | How found |
|---|---|---|---|
| `session_saved`, `sync_name`, `sync_name_locked`, `lock_list`, `import_claude_names`, `rename_dot_labels`, `migrate_names`, `list_sessions`, `scan_topics`, `retention_warning`, `ask_session_name`, `show_saved`, `orca_tab_reopen`, `auto_name`, `ensure_names_migrated` | `src/superclaude/skills/ccsession-tag/ccsession` | 387, 406, 464, 437, 503, 313, 253, 1712, 1658, 1854, 1869, 1904, 646, 674, 309 | Grep (`^\s*name()`), then Read of each range |
| `read_object`, `managed_value`, `check`, `ensure`, `main` | `src/superclaude/skills/ccsession-tag/retention.py` | 80, 89, 115, 174, 235 | `codegraph_search` and Grep, Read |
| `wire_ccsession` | `src/superclaude/cli/install_ccsession.py` | 11 | `codegraph_node` with `symbolsOnly` |

## Dependents

- `ensure` in `retention.py`: one caller, `main` (line 235), by `codegraph_callers`; `main` is run as a program by `install.sh` line 177 and by `install_ccsession.py` lines 107 to 125 through `subprocess`, which a call graph cannot see (confirmed by Read).
- `sync_name_locked`: called only by `sync_name` (line 406); `sync_name` is called by `rename_dot_labels`, `import_claude_names` and the `--sync-name` dispatch (line 746) and, outside the file, by `hooks/session-name.sh` (confirmed by Read).
- `list_sessions`: called by the `--list` and `--here` dispatch and by `show_saved` inside `ask_session_name` (confirmed by Read).
- Read-only consumers of the data that this plan must not break: `src/superclaude/cli/sweep/probes.py` (Orca tab records), `src/superclaude/cli/sweep/classify.py` line 722, `src/superclaude/cli/doctor.py` `_check_ccsession`.
- `wire_ccsession` is used by `src/superclaude/cli/main.py` and `tests/unit/test_install_ccsession.py` (`codegraph_node`).

## Pre-check

All 12 files named by the tasks exist; the only new file is `tests/unit/test_session_keep.py` (expected) plus the new `session_keep.py`. All 15 shell symbols, 5 Python symbols and 17 test helpers named by the tasks resolve to one definition each, at the line numbers the tasks quote. Dependents of the touched symbols that no task names: none beyond the read-only consumers above.
