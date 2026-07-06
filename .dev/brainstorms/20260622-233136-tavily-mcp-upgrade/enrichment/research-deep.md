---
source: tavily-docs-and-npm
quality_tier: primary
created: 2026-06-22T23:31:36Z
read_coverage: "Read 100% of Tavily search result file lines 0-2539 before use."
---

# Research Context: Tavily MCP Current State

## Verified package state

- `npm view tavily-mcp@latest version` returned `0.2.20`.
- `npm view tavily-mcp versions --json` returned versions `0.1.0` through `0.1.4`, then `0.2.0` through `0.2.20`.
- `npm view tavily-mcp@0.2.20 name version dist-tags --json` returned `name: tavily-mcp`, `version: 0.2.20`, `dist-tags.latest: 0.2.20`.

## Official Tavily MCP guidance observed

- Tavily's current MCP docs lead with remote MCP server usage. For Claude Code, the documented native path is `claude mcp add tavily-remote-mcp --transport http https://mcp.tavily.com/mcp/` and says Claude Code opens an OAuth browser flow; no API key is needed in the URL for OAuth.
- Tavily also documents API-key query usage for remote MCP (`https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>`) and says API-key auth can be used through URL query or Authorization header.
- Tavily documents `mcp-remote` as a compatibility bridge for clients that only support local stdio servers.
- Tavily still documents local installation with `npx -y tavily-mcp@latest` in the default-parameters local config example, while older snippets elsewhere still show `0.1.2` / `0.1.3` examples.
- Official docs list core Tavily web intelligence tools and APIs: search, extract, map, crawl, and research. The user-provided fact says the 0.2.x line added `tavily-map` and `tavily-crawl`; the implementation must verify those tools are present after install.

## Implications for IronClaude

- Remote HTTP-first is now the vendor-preferred Claude Code path and avoids local npx package drift, but it changes auth UX from environment variable prompting to OAuth/browser or URL/header API-key handling.
- Local stdio remains a documented path and fits IronClaude's existing `api_key_env`/`-e` installer abstraction with a minimal registry change from `0.1.2` to `latest` or a known 0.2.x pin.
- `@latest` matches current docs and prevents stale tool surfaces, but it reduces reproducibility. A named constant plus tests can at least ensure docs and installer agree.
- Pinning to `0.2.20` gives reproducible installs today but will recreate docs drift unless docs explicitly say IronClaude intentionally pins a latest-known version.
- Keeping both remote and local paths may be best: default remote HTTP only if installer has a first-class HTTP path and auth messaging; local stdio as deterministic fallback for headless/no-OAuth environments.
