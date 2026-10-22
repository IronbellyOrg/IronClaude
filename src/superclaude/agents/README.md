# SuperClaude Agents

This directory contains agent definition files for specialized AI agents.

## Available Agents

- **deep-research.md** - Autonomous web research agent
- **repo-index.md** - Repository indexing agent
- **self-review.md** - Code review and quality check agent

## Important

These agents are copies from `plugins/superclaude/agents/` for package distribution.

When updating agents:

1. Edit files in `plugins/superclaude/agents/`
2. Copy changes to `src/superclaude/agents/`
3. Both locations must stay in sync

In v5.0, the plugin system will use `plugins/` directly.

## Paths inside agent files

Agents run in other projects after `superclaude install`, where `src/superclaude/` does not exist. Never point an agent at another primitive with a `src/superclaude/...` path; use `~/.claude/skills/<name>/SKILL.md`, `~/.claude/agents/<name>.md` or `~/.claude/commands/sc/<name>.md`. See the "Never Hardcode `src/superclaude/` Paths" rule in the repository `CLAUDE.md`.
