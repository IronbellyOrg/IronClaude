---
status: partial
caller: sc-reflect-protocol
index_state: stale
checked_at: 2026-11-08T04:21:00Z
advisory: false
degraded: [graph:stale, graph:unresolved]
contract_path: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/artifacts/impact/return-contract.yaml
---

# Impact report: diff against e8db2fe660d9 (issue-watch poller)

## Summary

The commit adds the whole `superclaude.cli.issue_watch` package (every symbol is new, so each symbol of a changed file overlaps a hunk). Only 30 candidate symbols could be mapped (protocol cap D4); they were picked for cross-module use. All counts are depth 1. 20 production call sites are confirmed; 43 production rows stay unresolved by the call-site budget.

| symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated |
|---|---|---|---|---|---|
| REASON_TABLE | audit.py:26-102 | 2/2 | 1/1 | 0 | no |
| cycle_line | audit.py:292-319 | 1/1 | 8/8 | 0 | no |
| decision_line | audit.py:322-351 | 2/2 | 9/9 | 0 | no |
| warning_line | audit.py:354-378 | 2/2 | 17/17 | 0 | no |
| stderr_fallback | audit.py:381-404 | 5/5 | 6/6 | 0 | no |
| AuditLog | audit.py:123-156 | 3/3 | 15/15 | 4 | no |
| exit_for | cycle.py:461-463 | 1/1 | 6/6 | 0 | no |
| resolve_exit | cycle.py:447-458 | 1/1 | 12/12 | 0 | no |
| run_cycle | cycle.py:1177-1185 | 1/1 | 12/12 | 0 | no |
| Deadline | cycle.py:383-412 | 1/1 | 2/2 | 23 | no |
| Config | cycle.py:97 | 1/1 | 3/3 | 0 | no |
| Deps | cycle.py:416-426 | 1/1 | 1/1 | 0 | no |
| load_config | cycle.py:195 | 1/1 | 27/27 | 0 | no |
| status_report | cycle.py:1233-1298 | 1/1 | 0/0 | 0 | no |
| slo_numbers | cycle.py:1322-1369 | 0/0 | 5/5 | 0 | no |
| build_deps | cli.py:62-74 | 1/1 | 2/2 | 0 | no |
| format_utc | predicates.py:42-49 | 11/11 | 15/15 | 0 | no |
| parse_utc | predicates.py:27-39 | 6/6 | 7/7 | 0 | no |
| approval_of | predicates.py:185-234 | 2/2 | 5/5 | 0 | no |
| marker_in_window | predicates.py:279-296 | 1/1 | 2/2 | 0 | no |
| FileStore | record.py:334 | 5/5 | 21/21 | 10 | no |
| StoreDoc | record.py:92 | 3/3 | 5/5 | 0 | no |
| Entry | record.py:69 | 3/3 | 6/6 | 0 | no |
| mark_pending | record.py:538-568 | 1/1 | 14/14 | 0 | no |
| mark_launched | record.py:580-596 | 1/1 | 6/6 | 0 | no |
| mark_claimed | record.py:654-686 | 1/1 | 9/9 | 0 | no |
| fail | record.py:503 | 1/1 | 7/7 | 0 | no |
| sweep | record.py:627 | 1/1 | 10/10 | 0 | no |
| OrcaLauncher | launch.py:337-355 | 2/2 | 11/11 | 2 | no |
| check_origin | launch.py:218-236 | 1/1 | 13/13 | 0 | no |

## How to read this

Rows locate code and are not citations until marked `call-site-verified`. An empty list never proves there are no dependents. While `advisory: true`, nothing here may change a severity, gate or verdict (this run reports `advisory: false`, E-1 outcome A, MCP access).

## Readiness

| field | value |
|---|---|
| access | mcp |
| index_state | stale (one pending file, `.dev/.../reflect/post/verify-logs/invocations.yaml`, not source) |
| checked_at | 2026-11-08T04:21:00Z |
| cli_version / pin / pin_match | 1.6.2 / 1.6.2 / true |
| worktree_root / project_path | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher |
| worktree_relation | own |

## Input

Diff mode, base e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b, 379 changed files (266 md, 41 txt, 31 py, 21 json, 18 yaml, 2 other). Indexed source files outlined (D3): the 10 `src/superclaude/cli/issue_watch/*.py` files and `src/superclaude/cli/main.py`. Changed symbols table: see `symbols[]` in the contract (every row `mapped_by: hunk`, the hunk being the whole new file).

## Definitions

Listed in the Summary table; no ambiguity (`file` was passed on every lookup).

## Production dependents

Confirmed rows (CS1-CS4, hop 1, 20 of the 20-per-run budget) are in the contract `dependents[]`. The remaining 43 production rows (including 14 file-level import rows) were counted from `codegraph_callers` and not confirmed.

## Test dependents

Counts per symbol are in the Summary table. Test rows come from `codegraph_callers`; the tests are under `tests/issue_watch/`.

## Unmapped files

| file | reason |
|---|---|
| src/superclaude/cli/main.py | no_span_match (module-level hunk at 563-566, no symbol) |
| src/superclaude/cli/issue_watch/__init__.py | no_span_match (empty file) |
| docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md | not_indexed |
| tests/issue_watch/*.py (31 files) | cap |
| .dev/** (327 files) | not_indexed |

## Limits

Candidate cap: 30 of roughly 400 new symbols mapped. Call-site budget: verified 20, unresolved 43, dropped 0. No list truncated (the largest total is 28, `load_config`). `transitive.count` is derived: impact rows minus the queried definition minus rows already in the caller list.

## Degraded and fallbacks

- `graph:stale`: codegraph_status listed one pending non-source file; rows are leads.
- `graph:unresolved`: 43 production rows are over the call-site budget; they are counted, not cited.
- Nine of 30 CLI span queries (`codegraph query --json | jq`) failed to parse (control characters in the JSON); start lines were taken from the file outline and some end lines are null.
