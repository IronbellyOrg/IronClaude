# /sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick (item #808)
Master f2894fc44. Read-only; no source changed.
- F1: no escalate verb, notice sender or Orca unread call exists in issue_pipeline, sweep or observe (grep: only 'unreadable' hits). C27 extends a verb group (escalate, plan stage S15c) that is not on master.
- F2: the cap semantics conflict in the plan (FR-12 'absent or 0 means no cap' vs C27 'no number, no notice') remains open.

Codegraph: index_state=fresh, checked_at=2026-11-24T22:21:17Z; degraded: none
