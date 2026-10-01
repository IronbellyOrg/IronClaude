---
status: complete
created: 2026-09-30
owner: agent-3
scope: chrome-devtools-only
---

# chrome-devtools MCP removal

Stop shipping/documenting dedicated Chrome DevTools MCP. Playwright (`--play`) stays.

## Own

Files that mention chrome-devtools / Chrome DevTools MCP and do **not** also mention `sequential-thinking` or `magic`.

- Delete `src/superclaude/mcp/MCP_Chrome-DevTools.md`
- Delete `plugins/superclaude/mcp/MCP_Chrome-DevTools.md`
- Add one test: dedicated chrome-devtools MCP docs gone; Playwright MCP docs/config remain

## Not own (agent 4 / other agents)

CLI installer/registry, CLAUDE.md MCP tables, shared overviews, multi-server files: `install_mcp.py`, `FLAGS.md`, `pm.md`, `mcp-servers.md`, `mcp-installation.md`, `commands.md`, `comprehensive-features.md`, README, PROJECT_INDEX.

## Checklist

- [x] Delete SoT MCP doc
- [x] Delete plugin MCP doc mirror
- [x] Add file-absence test (Playwright still present)
- [x] `uv run pytest` on the new test
- [x] Confirm leftover chrome-devtools hits are only out-of-scope files

## Rules

src/superclaude SoT. Never stage `.claude/`. UV. No commit. No worktrees/.venv. Smallest diff.
