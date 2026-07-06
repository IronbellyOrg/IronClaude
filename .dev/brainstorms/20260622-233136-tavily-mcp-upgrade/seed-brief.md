---
topic: "Analyze the current Tavily MCP installation pipeline invoked by superclaude mcp and brainstorm the complete set of changes required to move it to tavily-mcp@latest."
domain: code
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: tasklist
created: 2026-06-22T23:31:36Z
---

# Seed Brief: tavily-mcp-upgrade

## Problem Statement

The live `superclaude mcp` installer is lagging behind Tavily's current MCP distribution. It hard-pins local stdio installs to `tavily-mcp@0.1.2`, while user docs already promise `tavily-mcp@latest` and dormant JSON configs point at a remote MCP bridge. This creates stale installed tool surfaces, docs drift, and ambiguous migration behavior for users already configured on the 0.1.x line.

## Known Context

- Live installer source of truth is `src/superclaude/cli/install_mcp.py`, not `src/superclaude/mcp/configs/`.
- Current live Tavily registry entry is local stdio with `npx -y tavily-mcp@0.1.2`, `api_key_env=TAVILY_API_KEY`, and API-key prompting via `-e TAVILY_API_KEY=<value>`.
- User-facing MCP docs already show local `tavily-mcp@latest`, contradicting the installer.
- Dormant Tavily config JSON files use `npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}` but repository search did not find active Python loader references.
- Tavily's current docs prefer remote HTTP/OAuth for Claude Code and still document local `tavily-mcp@latest` as an alternative.
- NPM latest is `0.2.20`; the 0.2.x series exists after the 0.1.x series and must expose map/crawl capabilities per the driving facts.

## Constraints

- Preserve working non-interactive/headless installs; remote OAuth may not be usable everywhere.
- Avoid leaking API keys into logs, dry-run output, or settings files unnecessarily.
- Do not make `src/superclaude/mcp/configs/tavily.json` appear authoritative unless the installer actually loads it.
- Any default transport switch requires installer command-builder support for native HTTP (URL positional argument, no stdio `-- <command>` shape).
- Users already on `tavily` with `0.1.2` must not be silently skipped by the current name-only installed check.
- Tests must use UV for Python execution.

## Success Criteria

- Installer, docs, and any packaged config artifacts converge on one declared Tavily source of truth.
- A fresh `superclaude mcp --servers tavily --dry-run` advertises the intended new Tavily install path.
- Tests fail if the installer regresses to `tavily-mcp@0.1.2` or if docs disagree with the installer policy.
- Verification covers the expected latest tool surface including `tavily-map` and `tavily-crawl`.
- Upgrade/back-compat behavior handles an existing `tavily` install rather than simply skipping it.
- Remote HTTP and local stdio auth behavior are explicit, documented, and accepted by tests.

## Open Questions

- Should IronClaude default to Tavily's vendor-preferred native remote HTTP/OAuth path, or keep local stdio as the default and only update to `tavily-mcp@latest`?
- If remote HTTP is supported, should API-key URL query auth be supported, OAuth-only, or an explicit opt-in mode?
- Should old `mcp/configs` JSON files be removed, generated from installer metadata, or promoted into a loaded registry?
- Should `@latest` float forever, or should IronClaude centralize a latest-known version constant and update it deliberately?
- What exact Claude CLI introspection surface is available to detect an existing Tavily install's command/version for migration?

## Enrichment Context

- `enrichment/codebase-context.md` records live installer, docs/config divergence, command-builder constraints, and test gaps.
- `enrichment/research-deep.md` records npm version verification and current Tavily docs on remote HTTP/OAuth, local stdio, API-key query/header, and expected search/extract/map/crawl capability.
