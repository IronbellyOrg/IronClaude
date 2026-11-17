---
status: success
caller: sc-implement-protocol
index_state: fresh
checked_at: 2026-11-17T20:01:18Z
advisory: false
degraded: [graph:unresolved]
contract_path: /home/coder/workspaces/worktrees/IronClaude/v6-cleanup-audit-runner/.dev/tasks/to-do/TASK-WF-removeTheCleanup-20261117-195340/artifacts/impact/T2/return-contract.yaml
---

## Summary

`cleanup_audit_group` has one production dependent left in the index, the package's own `__init__.py`; `main.py` no longer imports it (Task 1). A word-boundary Grep over tracked files (outside `.dev/` and `.claude/`) also finds the test file `tests/test_cleanup_audit_structure.py` (Task 4) and three lines in `docs/generated/contributor-knowledge-base/cli-api-inventory.md` (Task 13).

| symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated |
|---|---|---|---|---|---|
| cleanup_audit_group | src/superclaude/cli/cleanup_audit/commands.py:19 | 1/1 | 0/0 (graph; Grep finds 1 test file) | 1 | no |

## How to read this

Rows locate code and are not citations until marked `call-site-verified`. An empty list never proves there are no dependents. While `advisory: true`, nothing here may change a severity, gate or verdict.

## Readiness

| field | value |
|---|---|
| access | mcp |
| index_state | fresh |
| checked_at | 2026-11-17T20:01:18Z |
| cli_version / pin | 1.6.2 / 1.6.2 |

## Input

Symbols: `cleanup_audit_group`; depth 1; limit 10.

## Definitions

| name | file:start | kind | mapped_by |
|---|---|---|---|
| cleanup_audit_group | src/superclaude/cli/cleanup_audit/commands.py:19 | function | name |

## Production dependents

| caller | file | def_line | call_site_line | resolution | hop | source |
|---|---|---|---|---|---|---|
| (import and `__all__`) | src/superclaude/cli/cleanup_audit/__init__.py | 1 | 9 | call-site-verified (Grep line 9: `from .commands import cleanup_audit_group`) | 1 | callers |

## Test dependents

| caller | file | def_line | call_site_line | resolution | hop | source |
|---|---|---|---|---|---|---|
| TestCommandRegistration tests | tests/test_cleanup_audit_structure.py | null | 146 | unresolved (Grep only) | 1 | grep |

## Limits

shown/total: callers 1/1. Call-site budget: verified 1, unresolved 1, dropped 0.

## Degraded and fallbacks

`graph:unresolved`: one Grep-only test row counted, not confirmed by CS1 to CS5.
