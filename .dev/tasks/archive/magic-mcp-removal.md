---
title: "Remove Magic MCP shipping artifacts"
status: completed
priority: high
complexity: low
owner: agent-2
target_files:
  - src/superclaude/mcp/MCP_Magic.md
  - src/superclaude/mcp/configs/magic.json
  - plugins/superclaude/mcp/MCP_Magic.md
  - plugins/superclaude/mcp/configs/magic.json
  - docs/reference/advanced-patterns.md
verification: "uv run pytest tests/cli/test_install_mcp_registry.py -v"
---

## Problem

Stop shipping/installing/documenting Magic MCP (UI component generation, `--magic` when it only exists to invoke that server).

## Ownership (this agent)

Edit files that mention Magic MCP / `--magic` / mcp-servers magic **and do not** also mention `sequential-thinking` or `chrome-devtools`.

Leave to other agents:

- CLI installer/registry (`src/superclaude/cli/install_mcp.py`)
- CLAUDE.md MCP tables
- Shared MCP overviews
- Files listing more than one of sequential-thinking / magic / chrome-devtools
- `.claude/` (gitignore SoT mirror)
- Historical `.dev/` / `docs/research/` archives

## Checklist

### Phase 1: Delete Magic-only SoT artifacts

- [x] 1.1 Delete `src/superclaude/mcp/MCP_Magic.md`
- [x] 1.2 Delete `src/superclaude/mcp/configs/magic.json`
- [x] 1.3 Delete plugin mirrors `plugins/superclaude/mcp/MCP_Magic.md` and `plugins/superclaude/mcp/configs/magic.json`

### Phase 2: Strip Magic-only docs

- [x] 2.1 `docs/reference/advanced-patterns.md`: drop `--magic` / Magic MCP examples; keep Context7 / native UI wording

### Phase 3: Verify

- [x] 3.1 `uv run pytest tests/cli/test_install_mcp_registry.py -v` (does not require magic.json)
- [x] 3.2 Grep owned files: no leftover Magic MCP / `--magic` / `@21st-dev/magic` in the five target files
