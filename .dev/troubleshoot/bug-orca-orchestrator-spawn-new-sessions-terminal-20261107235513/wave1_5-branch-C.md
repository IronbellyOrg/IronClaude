# Wave 1.5 Branch C (semantic-restriction extraction), returned by troubleshoot-analyst, persisted by parent
(`applies_to` text condensed by the parent; `quoted_text` and `file_line` as returned. Line numbers are re-checked in Wave 5.)

Repo root = /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test

| source_file (repo-relative) | file_line | quoted_text | applies_to |
|---|---|---|---|
| CLAUDE.md | 307 | **ABSOLUTE RULE — every project worktree is created through Orca and lives at Orca's default worktree location.** | every project worktree must go through Orca |
| CLAUDE.md | 308 | Create it with `orca worktree create --name <name>`, adding `--repo <selector>`, `--base-branch <ref>`, and | worktree creation command shape; flags listed (308-309) do not include `--agent`; no instruction on launching a Claude session |
| CLAUDE.md | 312 | - Never create a project worktree with raw `git worktree add`, under the retired `.dev/worktrees/` location, or under `.claude/worktrees/`. | prohibited creation methods |
| CLAUDE.md | 313 | - Do **not** use the `EnterWorktree` tool: it hardcodes `.claude/worktrees/`, which is gitignored sync-dev territory. | EnterWorktree prohibited |
| CLAUDE.md | 314 | - Never pass Orca link flags (`--issue`, `--pr`) for this repo; ... | link flags |
| src/superclaude/core/CLAUDE.md | 47 | For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**. | launching a ccsession-backed Claude session (the "Orca session launches" paragraph; installs to ~/.claude/CLAUDE.md) |
| src/superclaude/core/CLAUDE.md | 48 | Load the version-matched `orca-cli` guide before choosing commands. Use `agent launch` in an existing worktree or `worktree create --agent` for a new checkout; request `--surface terminal` when a CLI session is required. `terminal create` is for shells, not agent sessions. The Claude command must be configured as `ccsession-orca` to use ccsession. | command choice for Claude sessions (lines 48-51) |
| src/superclaude/core/CLAUDE.md | 52 | For supervised workers, keep `worker-start` and the dispatch preamble authoritative; this rule does not replace supervised dispatch or commands' internal Agent-tool subagents. | scope limit |
| src/superclaude/skills/ccsession-tag/README.md | 230 | For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**. | same rule in the README |
| src/superclaude/skills/ccsession-tag/README.md | 231 | Load the version-matched `orca-cli` guide ... `terminal create` is for shells, not agent sessions. This requires the `ccsession-orca` Claude command configuration above ... | same (231-235) |
| src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py | 27 | ``orca worktree create`` (no link flag, no agent flag), | `/sc:issue --claim` script creates the worktree with no `--agent` (code at 594-610 matches) |
| src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py | 42 | ``orca agent launch --surface terminal`` with a prompt that starts with | the script then launches Claude in that worktree in a second call (code at 951-952 adds `--agent claude --worktree path:<wt>`) |
| src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py | 708 | "this agent is NOT behind the ccsession shim, or could not be verified; " "close it. Orca's Claude command must be the ccsession-orca wrapper" | warning W-LAUNCH-NOT-CCSESSION remedy |

conflict-check (returned): No two quoted constraints disagree about whether a new worktree gets `--agent`. Gap, not contradiction: repo-root CLAUDE.md's ABSOLUTE RULE never mentions `--agent`, and the core/README rule does not say whether `worktree create` without `--agent` is acceptable when a Claude session is also wanted. The `/sc:issue --claim` script creates the worktree without `--agent` and launches the agent in a second step.

Worker notes (returned):
- src/superclaude/cli/install_user_setup.py has no constraint on worktree/session/terminal creation.
- /home/coder/.claude/CLAUDE.md has no Orca or session-launch language (0 matches): the installed copy does not carry the "Orca session launches" paragraph.
- "choose Claude (CLI), never New Terminal" reads as guidance for a human choosing in the Orca UI; it has no MUST/SHALL wording tied to `worktree create --agent`.
