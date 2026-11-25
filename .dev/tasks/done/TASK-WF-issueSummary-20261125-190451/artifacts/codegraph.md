# codegraph run state (/sc:implement, one readiness check)

- index_state: stale
- access: none (no lookup tool is listed in this session; CLI lookups not used)
- checked_at: 2026-11-25T19:23:07Z
- worktree_root / projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-834
- token: graph:stale
- Note: `pgrep -f 'codegraph\.js (init|index)'` printed a process id in the same command that ran `codegraph status`; the status call was not gated on the pgrep result. The status output also reported an unfinished earlier index run and pending changes. The index may be damaged by that call; this run makes no further codegraph call and uses Grep, Glob and Read for every step.
