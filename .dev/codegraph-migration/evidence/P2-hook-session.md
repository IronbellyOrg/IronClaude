# P2 hook behaviour inside a real Claude Code session (Task 13)

Run on 2026-10-30 with Claude Code 2.1.314 (model alias `haiku`), `claude -p "reply ok" --no-session-persistence --strict-mcp-config` from a fresh `git clone` of this worktree. The real HOME was used only for Claude's login; the SessionStart hook was registered through `--settings` (matcher `startup`, command `sh src/superclaude/hooks/scripts/codegraph-session-start.sh`), the pinned v1.6.2 binary (SHA-256 checked) was put first on `PATH`, and the hook's log went to a temporary `XDG_STATE_HOME`. The real `.mcpServers` hash was identical before and after.

Observed:

- `claude -p` exited 0 and answered, so the hook did not break or delay the session.
- The hook started a background `codegraph init --yes <clone>`; right after the session ended no `codegraph.js init` process was running, `<clone>/.codegraph/codegraph.db` existed and `codegraph status` printed "Index is up to date" (no "never finished").
- The hook itself returns within milliseconds, so the init necessarily kept running after the hook process exited and then finished: it survived the hook's exit.

Not observed (UNVERIFIED): process-group survival after the session's end. The init finished before the session ended, so this run cannot show whether Claude Code would kill a still-running init when the session closes. A repository large enough that init outlasts a short `claude -p` session would be needed to observe that.
