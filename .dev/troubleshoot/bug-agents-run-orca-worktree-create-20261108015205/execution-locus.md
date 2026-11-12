# Execution locus

PRINT-SITE: Orca app terminal tabs (empty plain shells) and ~/.config/orca/logs/daemon.log `startup-command-delivery hasCommand=false` rows, on this host.
RUN-SITE: CLAUDE.md:308 (the worktree rule agents follow) @ local host, Claude Code sessions' Bash tool calls of `orca worktree create` (transcripts under ~/.claude/projects); Orca seeds the tab at IronOrca src/main/runtime/runtime-local-worktree-terminal-startup.ts:202-214 @ local Orca 1.4.245-aidev02 runtime.
SAME-ENV: yes (one host; the creating session, the Orca runtime and the observed tabs are all on this machine)
OBSERVE-VIA: same-shell (read-only: orca --help, orca terminal list, jq over transcripts and daemon.log). re-run permitted: unknown (creating a worktree is a mutation and was not authorized; it stays pending).
