# SuperClaude Commands

The files in this folder are installed to `~/.claude/commands/sc/` by `superclaude install` and `superclaude update` (this README.md itself is not installed). For the list of installed commands, run `/sc:help`; for which one to use for a job, read the routing guide `src/superclaude/core/HOW-WE-WORK.md` (installed as `~/.claude/HOW-WE-WORK.md`).

When you change a command:

1. Edit it here first (this folder is the source of truth).
2. Run `make sync-dev`, then `make verify-sync`.
3. If you changed `help.md`, `recommend.md`, `workflow.md` or `implement.md`, copy it byte-for-byte to `plugins/superclaude/commands/` (parity tests check these four).
4. If you added a command, add its row to the routing table at the end of `src/superclaude/core/HOW-WE-WORK.md` (or to its "Other commands" table).
5. The routing guide's canonical copy is `src/superclaude/core/HOW-WE-WORK.md`. When you change it, recopy its level-table block into `src/superclaude/core/CLAUDE.md` and copy the whole file byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (tests check both). The routing and recommendation tests are static text and cache checks: they pin the written contract, not which route a model actually picks. When routing behavior changes, check it with a separate recorded model-generation evaluation and report those results apart from the static tests.
6. Inside a command, never point at another primitive with a `src/superclaude/...` path. The installed copy is what runs in other projects, so name `~/.claude/skills/<name>/SKILL.md`, `~/.claude/agents/<name>.md` or `~/.claude/commands/sc/<name>.md` (and accept the project `.claude/` copy where a lookup needs it). See the "Never Hardcode `src/superclaude/` Paths" rule in the repository `CLAUDE.md`.
