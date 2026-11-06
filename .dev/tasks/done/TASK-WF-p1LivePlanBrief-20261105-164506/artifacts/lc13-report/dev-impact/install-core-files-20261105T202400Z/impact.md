---
status: success
caller: null
index_state: fresh
checked_at: 2026-11-05T20:23:22Z
advisory: false
degraded: [graph:unresolved]
contract_path: /home/coder/workspaces/worktrees/IronClaude/p1-live-impact/.dev/impact/install-core-files-20261105T202400Z/return-contract.yaml
---

# Impact: install_core_files

## Summary

`install_core_files` (src/superclaude/cli/install_core.py:31-104) has 8 direct callers in the index: 2 production callers (both in `src/superclaude/cli/main.py`: `install` and `update`) and 6 test callers. Nothing further out was found at depth 1. The 2 production call sites were confirmed in the source; the 6 test rows stay at definition line only.

| symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated |
|---|---|---|---|---|---|
| install_core_files | src/superclaude/cli/install_core.py:31-104 | 2/2 | 6/6 | 0 (depth 1) | no |

## How to read this

Rows locate code and are not citations until marked `call-site-verified`. An empty list never proves there are no dependents. While `advisory: true`, nothing here may change a severity, gate or verdict (this run reports `advisory: false`).

## Readiness

| field | value |
|---|---|
| access | mcp |
| index_state | fresh |
| checked_at | 2026-11-05T20:23:22Z |
| cli_version | 1.6.2 |
| pin | 1.6.2 |
| pin_match | true |
| worktree_root | /home/coder/workspaces/worktrees/IronClaude/p1-live-impact |
| project_path | /home/coder/workspaces/worktrees/IronClaude/p1-live-impact |
| worktree_relation | own |

Index status at check: 2166 files, 0 added, 0 modified, 0 removed since index.

## Input

Mode: symbols. Symbols: `install_core_files`. Depth 1, limit 10, tests off.

## Definitions

| name | file:start-end | kind | mapped_by |
|---|---|---|---|
| install_core_files | src/superclaude/cli/install_core.py:31-104 | function | name |

The name matched exactly one definition. Other search hits (`install_hooks`, test-fixture variables under `.dev/tasks/done/`) are different names and were not kept.

## Production dependents

### install_core_files

| caller | file | def_line | call_site_line | resolution | hop | source |
|---|---|---|---|---|---|---|
| install | src/superclaude/cli/main.py | 46 | 178 | call-site-verified | 1 | callers |
| update | src/superclaude/cli/main.py | 340 | 365 | call-site-verified | 1 | callers |

## Test dependents

### install_core_files

| caller | file | def_line | call_site_line | resolution | hop | source |
|---|---|---|---|---|---|---|
| test_core_install_and_listing_include_policy | tests/cli/test_bash_inspection_policy.py | 36 | - | def-line | 1 | callers |
| test_how_we_work_installed_and_listed | tests/cli/test_how_we_work_install.py | 27 | - | def-line | 1 | callers |
| test_install_never_touches_existing_files_without_force | tests/cli/test_how_we_work_install.py | 53 | - | def-line | 1 | callers |
| test_install_never_removes_unshipped_files | tests/cli/test_how_we_work_install.py | 79 | - | def-line | 1 | callers |
| test_body_files_shipped_and_installed_flat | tests/cli/test_issue_body_templates.py | 27 | - | def-line | 1 | callers |
| _install_core | tests/unit/test_cli_install.py | 965 | - | def-line | 1 | callers |

## Limits

- Callers: 8 shown of 8 total (limit 10 not reached; no truncation).
- Transitive (depth 1): the impact answer listed 9 symbols; after dropping the definition itself, all 8 were already in the caller list, so 0 extra rows.
- Call-site budget (5/symbol, 20/run): verified 2, unresolved 6 (test rows, not confirmed), dropped 0.
- Partition is by path markers only (`tests/` prefix); inline test markers were not checked, so the test list is a floor.

## Degraded and fallbacks

- `graph:unresolved`: dependent rows not confirmed at a call site (here the 6 test rows). They are counted, not cited. No fallback was needed: codegraph answered through MCP and Grep was used only to confirm the 2 production call sites.
