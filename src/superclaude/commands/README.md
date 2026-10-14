# SuperClaude Commands

The files in this folder are installed to `~/.claude/commands/sc/` by `superclaude install` and `superclaude update` (this README.md itself is not installed). For the list of installed commands, run `/sc:help`; for which one to use for a job, read the routing guide `src/superclaude/core/HOW-WE-WORK.md` (installed as `~/.claude/HOW-WE-WORK.md`).

When you change a command:

1. Edit it here first (this folder is the source of truth).
2. Run `make sync-dev`, then `make verify-sync`.
3. If you changed `help.md`, `recommend.md`, `workflow.md` or `implement.md`, copy it byte-for-byte to `plugins/superclaude/commands/` (parity tests check these four).
4. If you added a command, add its row to the routing table at the end of `src/superclaude/core/HOW-WE-WORK.md` (or to its "Other commands" table).
