# Research: Official MCP releases

**Topic type:** Solution Research
**Scope:** Included MCP release/version and migration verification
**Status:** Complete
**Date:** 2026-09-11

## Verified sources

- **Tavily:** `tavily-mcp@0.2.22` is the verified npm release. Pin command: `npx -y tavily-mcp@0.2.22`. Node 20+ and `TAVILY_API_KEY` remain required. Confidence: high.
- **Sequential Thinking:** `@modelcontextprotocol/server-sequential-thinking@2026.8.31` is the verified npm release. Pin command: `npx -y @modelcontextprotocol/server-sequential-thinking@2026.8.31`. Confidence: high.
- **Serena:** `serena-agent==1.7.0` is the verified PyPI distribution and `--context=claude-code` is the current documented context. First-party docs did not establish an exact version-pinned one-shot `uvx` launch command compatible with that context; treat the final launcher form as a pre-edit verification item. Confidence: high for package/context; unresolved for exact launch command.
- **Auggie:** `@augmentcode/auggie@0.36.0` is the verified npm release. Official Claude Code JSON config uses `auggie --mcp --mcp-auto-workspace`; Node 22+ is safest for this release. Confidence: high.
- **Morph:** `@morph-llm/morph-fast-apply` is deprecated in favor of `@morphllm/morphmcp`; the successor requires `MORPH_API_KEY`. Tool compatibility must be confirmed with a focused config/command test before replacing a server name. Confidence: high for successor; unresolved for drop-in tool-contract compatibility.

## Source URLs
- https://www.npmjs.com/package/tavily-mcp/v/0.2.22
- https://github.com/tavily-ai/tavily-mcp/blob/main/README.md
- https://www.npmjs.com/package/@modelcontextprotocol/server-sequential-thinking/v/2026.8.31
- https://github.com/modelcontextprotocol/servers/blob/main/src/sequentialthinking/README.md
- https://pypi.org/project/serena-agent/1.7.0/
- https://oraios.github.io/serena/02-usage/010_installation.html
- https://oraios.github.io/serena/02-usage/030_clients.html
- https://oraios.github.io/serena/02-usage/050_configuration.html
- https://www.npmjs.com/package/@augmentcode/auggie/v/0.36.0
- https://docs.augmentcode.com/context-services/mcp/quickstart-claude-code
- https://www.npmjs.com/package/@morph-llm/morph-fast-apply
- https://www.npmjs.com/package/@morphllm/morphmcp

## Exclusions
No change to Context7, Playwright, Chrome DevTools, Magic, AIRIS, Markdown Collab, or user-level Codebase Memory because their provenance/version decisions are outside the verified project-owned scope.
