# Evidence: settings.json `env` reaches hook subprocesses

Collected by the orchestrator on 2026-11-04 to resolve the shared assumption that all three variants marked UNVERIFIED (variant 1 V-1, variant 2 AC-M1, variant 3 manual check).

1. Claude Code settings docs (`content/en/docs/claude-code/settings.md`, via Context7 `/pjbrito/claude-code-docs`): "`env` — Environment variables applied to every session and to subprocesses Claude Code spawns from it."
2. Claude Code hooks docs (`content/en/docs/claude-code/hooks.md`, same source): "Handlers run in the current directory with Claude Code's environment."
3. Live observation in this session: `~/.claude/settings.json` `env` sets `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` and `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION=5000`; a Bash-tool subprocess prints `AGENT_TEAMS=1 MAX_WEB=5000`.

Conclusion: documented and observed for spawned subprocesses. Plugin hooks are command hooks spawned the same way, so `env.PONYTAIL_DEFAULT_MODE` reaches `ponytail-activate.js`. A plugin-hook-specific live run was not performed (no plugin may be installed in this workspace); a throwaway-HOME session check remains optional confirmation, not a merge gate.
