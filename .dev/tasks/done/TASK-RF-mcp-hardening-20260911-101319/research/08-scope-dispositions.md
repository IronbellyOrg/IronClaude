# Final gap-fill: evidence dispositions and direct documentation scope

**Status:** Complete
**Date:** 2026-09-11

## Authoritative selected commands

| Registry key and retained client name | Required command | Evidence disposition |
|---|---|---|
| `sequential-thinking` | `npx -y @modelcontextprotocol/server-sequential-thinking@2026.8.31` | **[PRIMARY-VERIFIED]** npm release `2026.8.31` and official MCP servers repository. |
| `serena` | `uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false` | **[PRIMARY-VERIFIED]** PyPI 1.7.0, v1.7.0 source CLI option definitions, and official Serena client documentation. |
| `morphllm-fast-apply` | `npx -y @morphllm/morphmcp` | **[PRIMARY-VERIFIED]** predecessor deprecation metadata and current official Morph package documentation. Retaining the name is a deliberate Claude-client compatibility choice, not a vendor server identity claim. |
| `tavily` | `npx -y tavily-mcp@0.2.22` | **[PRIMARY-VERIFIED]** npm release 0.2.22 and official Tavily MCP documentation. |
| `auggie` installer / `auggie-mcp` root config key | `auggie --mcp --mcp-auto-workspace`; global package `@augmentcode/auggie@0.36.0` | **[PRIMARY-VERIFIED]** official Augment package and Claude Code integration guide. Keeping root key `auggie-mcp` preserves existing project hook/eval namespace. |

Primary sources are recorded in research files `03`, `05`, and `06`; re-check each immediately before implementation as the build request requires.

## Direct documentation disposition

The task MUST update every current project-owned, source/docs surface that presents one of these selected commands or Tavily's pin:
- `docs/user-guide/mcp-installation.md`
- `docs/user-guide/mcp-servers.md`
- `src/superclaude/mcp/MCP_Tavily.md`
- `src/superclaude/mcp/MCP_Auggie.md`

It MUST not broaden into unrelated legacy documentation (`docs/developer-guide/technical-architecture.md`, `docs/reference/mcp-server-guide.md`), packaged template consolidation, plugin config copies, or user/machine configuration. Those are separate technical-debt work.

## Verification baseline policy

Research observed that `make verify-sync` is already non-green before this task due to unrelated mirror drift. The task must capture its pre-change exit/output, run `make sync-dev`, then run `make verify-sync` again. A clean post-change pass is preferred. If it remains failing for byte-identical pre-existing causes, record the baseline and prove no new sync failure attributable to the MCP changes; do not alter unrelated generated `.claude/` files.
