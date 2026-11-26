# /sc:analyze report: src/superclaude/cli/issue_watch (architecture, quick)

Target: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/issue_watch` (the watcher dispatch and store). Checked against issue #772 on worktree HEAD a7ae3dd30; origin/master is f2894fc44 and differs from HEAD in this area only in `dispatch.py` and `first_run.py` (git diff --stat), neither of which holds the cited rules.

Codegraph: index_state=fresh, checked_at=2026-11-24T20:43:22Z; degraded: none (lookups were not needed beyond Grep/Read at quick depth)

## Architecture findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| A1 | Medium | A `claimed` or `pending` store entry is skipped as `already_dispatched`, so a second stage run through the watcher cannot start. | `src/superclaude/cli/issue_watch/cycle.py:982` |
| A2 | Medium | Only `abandoned` and `unknown` entries can be reset. `claimed` has no reset path. | `src/superclaude/cli/issue_watch/record.py:448` (`_RESETTABLE`), `:714` (check in `reset_entry`) |
| A3 | Info | Governed levels (anything above None) are switched off by a module constant; such an issue ends `level_gated`. | `src/superclaude/cli/issue_watch/launch.py:48`, `cycle.py:1029-1036` |
| A4 | Info | All four stage pipelines end at In review (one named table). | `src/superclaude/cli/issue_pipeline/complete.py:55-60` |
| A5 | Medium | Four passages say a relaunch needs the Status moved back; by A1 and A2 that is necessary at most, never sufficient for a claimed issue. | `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt:17`, `src/superclaude/core/WORKER-CONTRACT.md:297`, `docs/designs/issue-watcher-status-pipelines.md:65`, `:79` |

## Recommendations

1. Owner answers the four questions in #772 before any behaviour change.
2. Text fixes for A5 and the launch-prompt conflict can follow the answers; no code change is needed for them.

Read-only run: no source file was modified.
