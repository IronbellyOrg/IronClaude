# Refactor Plan

## Overview

- Base variant: Variant 3 — QA
- Incorporated variants: Variant 1 — Architect, Variant 2 — Refactorer
- Risk level: Medium
- Review status: auto-approved

## Planned Changes

1. **Centralize Tavily package policy**
   - Source: Variant 3 with Variant 1 safeguards
   - Target: `src/superclaude/cli/install_mcp.py`
   - Approach: define a single package token such as `TAVILY_MCP_PACKAGE = "tavily-mcp@latest"` and use it in `MCP_SERVERS["tavily"]["command"]`.

2. **Keep default local stdio transport**
   - Source: all variants
   - Target: `src/superclaude/cli/install_mcp.py`, docs
   - Approach: preserve `transport: "stdio"`, `api_key_env: "TAVILY_API_KEY"`, and local `npx` command shape.

3. **Add stale-install reconciliation**
   - Source: all variants
   - Target: `src/superclaude/cli/install_mcp.py`
   - Approach: detect existing exact server name `tavily` using stale package metadata; when stale, remove and re-add or print equivalent dry-run actions.

4. **Redact API key values in echoed commands**
   - Source: Variant 1 and QA invariant probe
   - Target: `src/superclaude/cli/install_mcp.py`
   - Approach: centralize display-string redaction for `-e KEY=value` and URL query forms before printing.

5. **Reconcile docs**
   - Source: all variants
   - Target: `docs/user-guide/mcp-servers.md`
   - Approach: ensure docs show the same `tavily-mcp@latest` policy, stdio default, TAVILY_API_KEY env, expected map/crawl tools, optional remote HTTP future note, and validation command guidance.

6. **Retire dead Tavily configs**
   - Source: Variant 2/3
   - Target: `src/superclaude/mcp/configs/tavily.json`, `plugins/superclaude/mcp/configs/tavily.json`
   - Approach: delete the dormant divergent files unless implementation discovers a packaging dependency; if so, rewrite them to mirror the live installer and mark non-authoritative.

7. **Add unit/regression tests**
   - Source: Variant 3
   - Target: new tests under `tests/cli/` or `tests/mcp/`
   - Approach: mock subprocess/Claude CLI calls; include optional integration smoke for live tool enumeration.

## Changes Not Being Made

- No default switch to remote HTTP/OAuth in this upgrade.
- No API-key query URL default.
- No general MCP registry loader from `src/superclaude/mcp/configs/`.
- No broad migration of every MCP server install check.

## Risk Controls

- Dry-run must remain mutation-free.
- Migration only targets exact server name `tavily`.
- Unit tests must not require a real Claude CLI, Node network install, or Tavily API key.
