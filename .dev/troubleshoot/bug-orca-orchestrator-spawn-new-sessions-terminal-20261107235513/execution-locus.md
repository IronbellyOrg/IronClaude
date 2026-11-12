# Execution locus card

PRINT-SITE: Orca UI as described by the user: new tabs that are empty plain terminals, with the orchestrator waiting. Copied from the issue text; no log line was supplied.
RUN-SITE: unresolved candidate set (all four surviving producers of producers.md): P1 CLAUDE.md:308 @ the orchestrator's Claude Code session (the command text it runs); P2 `orca terminal create` (CLI help, tier1-observation.md O1; no file:line) @ the orca CLI process on the Orca host; P3 /home/coder/workspaces/IronOrca/src/shared/keybindings/definitions-core-2.ts:69 @ the Orca desktop renderer (a human keypress); P4 `orca orchestration worker-start` / `orca agent launch` (CLI help, O1; no file:line) @ the Orca main process on the Orca host. No unique run site is claimed.
SAME-ENV: unknown
OBSERVE-VIA: artifact-file
re-run permitted: unknown

Notes:
- The thing that decides "terminal or Claude session" is an LLM orchestrator choosing an `orca` command. Its Bash tool calls are recorded in Claude transcripts under ~/.claude/projects/, which is the only captured record of that choice.
- Orca's own record of what a tab started is ~/.config/orca/logs/daemon.log (`startup-command-delivery`: hasCommand true/false). It does not say who asked.
- Read-only `orca terminal list` / `orca orchestration worker-list` can show live tabs; they do not show how a tab was requested.
