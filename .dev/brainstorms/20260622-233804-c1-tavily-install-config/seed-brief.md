---
topic: "C1 Tavily Install/Config/Version-pin upgrade to tavily-mcp 0.2.x"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-06-22T23:38:00Z
---

# Seed Brief: C1 — Tavily Install / Config / Version Pin

## Problem Statement

The project has **two divergent Tavily install paths** that disagree on transport and version, plus a third help-text reference. They must be reconciled into a single source of truth with a coherent version policy, brought up to the current `tavily-mcp@0.2.20` surface, and proven with verification.

## Known Context (verified from files + Tavily docs/npm, 2026-06-22)

- `src/superclaude/cli/install_mcp.py:76-84` — `MCP_SERVERS["tavily"]`: `transport: "stdio"`, `command: "npx -y tavily-mcp@0.1.2"`, `api_key_env: "TAVILY_API_KEY"`. **Pins stale 0.1.2 via local npx.** Installer calls `claude mcp add --transport stdio tavily -e TAVILY_API_KEY=<key> -- npx -y tavily-mcp@0.1.2`.
- `src/superclaude/mcp/configs/tavily.json` — `command: "npx"`, `args: ["-y","mcp-remote","https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}"]`. **Uses the remote hosted MCP endpoint via `mcp-remote`, no version pin.** This is a *different* transport than install_mcp.py.
- `src/superclaude/cli/main.py:235` — help example `superclaude mcp --servers tavily --servers context7` (cosmetic; no version).
- `install_mcp.py` install flow: `claude mcp add --transport <t> [--scope user] <name> [-e KEY=VAL] -- <command>` (server name before `-e`, CLI grammar requirement at lines 591-614).
- npm: `tavily-mcp` `dist-tags.latest = 0.2.20`. 0.2.x tool surface = `tavily-search`, `tavily-extract`, `tavily-map`, `tavily-crawl`.
- 0.2.x adds a `DEFAULT_PARAMETERS` env/header config mechanism (e.g. `{"search_depth":"basic","max_results":10}`) settable for both remote (header) and local (env) installs.
- Tavily's own docs recommend the **remote URL** (`https://mcp.tavily.com/mcp/?tavilyApiKey=...`) as the easiest method; local is `npx -y tavily-mcp@latest`.
- Project convention: `src/superclaude/` is source of truth; `.claude/` is sync-dev output. `configs/tavily.json` is NOT consumed by install_mcp.py (the installer has its own hardcoded registry) — so the two files are independent and the JSON may be dead/aspirational config. This must be confirmed and resolved.

## Constraints

- UV-only Python; no behavior change to the `claude mcp add` grammar already encoded.
- Must not break existing `superclaude mcp --servers tavily` UX.
- API key handling (`TAVILY_API_KEY`) must remain; secret never logged.
- Edits land in `src/superclaude/`; docs/config sync via `make sync-dev` where applicable.
- Tests must run under `uv run pytest` and not require a live network/API key in CI (mock or capability-gate the live call).

## Success Criteria

- Exactly one authoritative version policy for tavily-mcp, applied consistently across install_mcp.py and tavily.json (or one of them is explicitly retired).
- Install path updated off 0.1.2 to the chosen 0.2.x policy.
- DEFAULT_PARAMETERS adoption decision made (adopt with sane defaults, or explicitly defer with rationale).
- A verification plan: unit test asserting the registry command/version, plus an opt-in live smoke (capability-gated) proving `claude mcp add` + a `tavily-search` round-trip on the new version.

## Open Questions

- Is `configs/tavily.json` actually consumed anywhere, or is it dead config? (Grep shows no Python reader.)
- Pin exact `0.2.20` (reproducible, manual bumps) vs `@latest` (auto-fresh, drift risk) vs remote-only (Tavily-managed, no version control)?
- Should remote and local both be offered, or converge on one transport?
- Where do DEFAULT_PARAMETERS belong — installer env injection, config file, or left to the agent call sites (C2/C5)?

## Enrichment Context

**Codebase (primary):** All three C1 files read in full this session. install_mcp.py registry is the live install path; tavily.json is an orphan config with no Python consumer found via grep.

**Research (deep, primary):** npm `tavily-mcp@0.2.20` confirmed latest; 0.2.x exposes search/extract/map/crawl + DEFAULT_PARAMETERS; Tavily docs recommend remote URL, support `npx tavily-mcp@latest` local. Official docs page is itself stale (cites 0.1.3), so npm dist-tags is the authoritative version source.
