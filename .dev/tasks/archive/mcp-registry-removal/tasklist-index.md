---
title: MCP registry removal (sequential-thinking, magic, chrome-devtools)
generated: "2026-09-30"
total_phases: 1
total_tasks: 6
complexity_class: LOW
---

# TASKLIST INDEX — mcp-registry-removal

## Goal

Remove `sequential-thinking`, `magic`, and `chrome-devtools` from the installed MCP list so they no longer appear in `superclaude mcp --list`, install defaults, gateway/plugin MCP catalogs, CLAUDE.md MCP tables, user-guide MCP reference, or tests that assert they are available.

Keep: tavily, context7, serena, playwright, auggie, morphllm-fast-apply, airis-mcp-gateway, mindbase, and any other non-removal server.

No replacements. No commit. SoT = `src/superclaude/`. Never stage `.claude/`.

## Out of scope (other agents)

- Per-command frontmatter that mentions only one of the three
- Already-deleted estimate/select-tool/sc.md
- Reverting catalog edits in help.md / docs/user-guide/commands.md / flags.md unless they still advertise these MCPs as installable

## Phase 1 — Registry, catalogs, tests

| ID | Task | Files |
|---|---|---|
| T01.01 | Drop the three keys from `MCP_SERVERS` | `src/superclaude/cli/install_mcp.py` |
| T01.02 | Drop sequential template pin + sequential.json from registry tests | `tests/cli/test_install_mcp_registry.py` |
| T01.03 | Delete plugin/src MCP config + MCP_*.md for the three | `src/superclaude/mcp/`, `plugins/superclaude/mcp/` |
| T01.04 | Strip MCP tables in CLAUDE.md (repo + core) and persona MCP columns | `CLAUDE.md`, `src/superclaude/core/CLAUDE.md` |
| T01.05 | Strip available-server catalogs in user-guide + core MCP/FLAGS | `docs/user-guide/mcp-installation.md`, `docs/user-guide/mcp-servers.md`, `src/superclaude/core/MCP.md`, `src/superclaude/core/FLAGS.md` (and plugin copies of those catalogs) |
| T01.06 | Verify: pytest registry tests; `superclaude mcp --list` has none of the three; leftover installer/list hits |

## Check

`uv run pytest tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py -q`

Remaining keep-set servers must still be in `MCP_SERVERS`.
