# Variant 2 — QA: Tavily 0.2.x Doc Alignment Spec

## QA thesis
The docs fix is not primarily prose; it is drift prevention. The 0.2.x upgrade creates three recurring drift axes: package version (`0.1.2`, `@latest`, `0.2.20`), eval capability token (`mcp.tavily` vs `mcp_server.tavily`), and parameter duplication outside the canonical Tavily implementation/capability doc. Ship the smallest doc edits plus automated guards that fail before drift reaches users.

## Per-file verdicts

- `src/superclaude/core/FLAGS.md` — **edit lightly**. Keep `--tavily`, but make the behavior generic: enables Tavily MCP web/search-map-crawl capabilities; point readers to `plugins/superclaude/mcp/MCP_Tavily.md` for capability details. Do not list parameter defaults.
- `src/superclaude/core/MODES.md` — **none**. The Deep Research mention is provider-level and does not conflict with 0.2.20.
- `src/superclaude/core/COMMANDS.md` — **none**. The Tavily mentions are command/server participation only.
- `docs/user-guide/mcp-servers.md` — **edit required**. Replace the Tavily example install token `tavily-mcp@latest` with the pinned `tavily-mcp@0.2.20`. Update Tavily requirements from `Node.js 16+` to `Node.js 18+` if installer/runtime has moved to 18+. Add one sentence: Tavily capabilities include search, extract, map, and crawl; details live in `plugins/superclaude/mcp/MCP_Tavily.md`. Avoid copying tool schemas/defaults.
- `docs/user-guide/mcp-installation.md` — **none or single prerequisite alignment only**. It already lists `tavily` and `TAVILY_API_KEY`, and its prerequisites already say `Node.js 18+`. Do not add package/version prose here unless generated from the registry.
- `docs/user-guide/commands.md` — **none**. Mentions Tavily as an MCP used by commands; no version/token drift.
- `docs/user-guide/flags.md` — **none**. High-level `--tavily` row is acceptable; no capability table needed.
- `docs/user-guide/modes.md` — **none**. Tavily orchestration mention is generic.
- `docs/user-guide/agents.md` — **none**. Tavily orchestration mention is generic.
- `docs/reference/comprehensive-features.md` — **edit required**. Remove obsolete `tavily.json` references because orphan configs are deleted. Keep “MCP_Tavily.md” as the capability source of truth, but do not duplicate tool parameters.
- `docs/reference/basic-examples.md` — **none**. Tavily is optional enrichment only.
- `docs/mcp/mcp-integration-policy.md` — **edit lightly** only if it implies fallback-only/optional status inconsistent with Tavily being an installed local stdio server. Keep policy-level routing; point detailed capability semantics to `MCP_Tavily.md`.
- `docs/mcp/mcp-optional-design.md` — **edit lightly** only to prevent “optional/fallback only” from being read as the active install contract. Keep design context; add a note that active installer config is owned by `src/superclaude/cli/install_mcp.py`.
- `docs/eval/retry.md` — **edit required**. Replace `mcp.tavily` with `mcp_server.tavily` in the manifest example and surrounding prose if any.
- `docs/research/**`, `docs/analysis/**` — **exclude** from this pass and from the doc-alignment tests unless a separate archival-cleanup task opts in.

## Automated consistency tests

Add `tests/docs/test_tavily_doc_alignment.py`.

1. **Version drift guard**
   - Import the authoritative package token from `src/superclaude/cli/install_mcp.py` if a constant exists (`TAVILY_MCP_PACKAGE = "tavily-mcp@0.2.20"` preferred); otherwise derive it from `MCP_SERVERS["tavily"]["command"]`.
   - Assert the token is exactly `tavily-mcp@0.2.20`.
   - Scan `src/superclaude/` and `docs/`, excluding `docs/research/**`, `docs/analysis/**`, `.dev/**`, generated caches, and binary files, for `tavily-mcp@...`.
   - Fail if any match is not exactly `tavily-mcp@0.2.20`. This catches current `0.1.2` in installer and `@latest` in docs.

2. **Stale eval capability token guard**
   - Scan `src/superclaude/cli/eval/**`, `tests/cli/eval/**`, and `docs/eval/**` for the literal `mcp.tavily`.
   - Fail on any occurrence.
   - Assert at least one canonical example/reference uses `mcp_server.tavily`, so the test cannot pass by deleting all Tavily eval docs.

3. **Deleted orphan config guard**
   - Assert `src/superclaude/mcp/configs/tavily.json` and any plugin mirror config path do not exist.
   - Scan in-scope docs for `tavily.json` and `mcp.tavily.com`; fail on either. This locks C1 stdio-local and deletion decisions without re-litigating remote transport.

4. **DEFAULT_PARAMETERS duplication guard**
   - Import Tavily `DEFAULT_PARAMETERS` from the implementation module that owns Tavily tool calls.
   - Scan in-scope docs for markdown tables or YAML/JSON snippets that assign those default values to Tavily parameter names outside the implementation module and `MCP_Tavily.md` if it remains canonical.
   - Preferred stricter rule: no docs may contain `DEFAULT_PARAMETERS` value assignments at all; docs can name `tavily-search`, `tavily-extract`, `tavily-map`, and `tavily-crawl`, then link to `MCP_Tavily.md`.

## Node version recommendation
Node 16→18 is in scope only as installer prerequisite alignment. Change user-facing install/requirements docs that currently claim `Node.js 16+` for npm MCP servers or Tavily. Do not make this a Tavily-only rule if the installer requires 18+ generally.

## Acceptance criteria
- All in-scope docs agree on local stdio install, pinned `tavily-mcp@0.2.20`, `TAVILY_API_KEY`, and deleted `tavily.json` configs.
- `docs/eval/retry.md` uses only `mcp_server.tavily`.
- `MCP_Tavily.md` is the only capability detail target and includes search/extract/map/crawl at a high level.
- No in-scope doc duplicates Tavily parameter default tables.
- `uv run pytest tests/docs/test_tavily_doc_alignment.py` fails on the known stale strings and passes after the doc/source edits.
