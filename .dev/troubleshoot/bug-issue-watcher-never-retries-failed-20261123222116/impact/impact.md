---
status: partial
caller: sc-troubleshoot-protocol
index_state: stale
checked_at: 2026-11-23T23:35:34Z
advisory: true
degraded: [graph:stale, graph:unresolved]
---
# Impact: run_sweep, first_run (abridged run)

Rows locate code and are not citations until call-site-verified. An empty list never proves no dependents. While advisory is true, nothing here changes a gate or verdict.

| symbol | prod callers | test callers |
|---|---|---|
| run_sweep (dispatch.py:348) | run_all_command, src/superclaude/cli/issue_watch/cli.py:470 (grep: cli.py:508, 511) | sweep, tests/issue_watch/test_dispatch.py:141 (grep: :152) |
| first_run (first_run.py:125) | run_sweep, dispatch.py:348 (call at dispatch.py:427) | test_first_run.py:125, :347 |

Limits: codegraph index was stale (107407 pending references), call sites were not run through the full CS1-CS5 confirmation; depth-2 transitive dependents were not listed. The change adds a branch inside run_sweep and a read-only helper in first_run.py, so the signature of both functions stays unchanged.
