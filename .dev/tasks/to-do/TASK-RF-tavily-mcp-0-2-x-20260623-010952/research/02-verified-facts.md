# Research: Verified facts + citations (Tavily 0.2.x)

**Topic type:** Integration Points / Facts grounding
**Status:** Complete
**Date:** 2026-06-23

All facts verified this session via npm, Tavily docs/repo, and direct Read/grep of the codebase.

## Tavily package + tool surface
- npm `tavily-mcp` `dist-tags.latest = 0.2.20` (verified `npm view tavily-mcp dist-tags`). **[CODE-VERIFIED]**
- 0.2.x tools: `tavily-search`, `tavily-extract`, `tavily-map`, `tavily-crawl` (tavily-ai/tavily-mcp README). **[CODE-VERIFIED]**
- Config: env var **`DEFAULT_PARAMETERS`** (JSON string) for local `-e`; same-named HTTP header for remote. Example value `{"include_images":true,"search_depth":"basic","max_results":10}`. **[CODE-VERIFIED]** (repo README)
- Tavily search params: `search_depth` (basic|advanced), `max_results`, `topic` (general|news), `include_domains`, `exclude_domains`, `time_range`, `days`, `include_raw_content`, `include_images`. Extract params: `extract_depth` (basic|advanced), `format`.
- B1 DECISION: pin exact `tavily-mcp@0.2.20` (NOT `@latest`, NOT remote-only).

## Codebase citations (verified)
- `install_mcp.py:80` — `"command": "npx -y tavily-mcp@0.1.2"`. **[CODE-VERIFIED]**
- `install_mcp.py` `_run_command` (~L130-142) shlex-quotes each argv token on POSIX; `env_args = ["-e", f"{api_key_env}={api_key}"]` (~L552); argv assembled ~L597-614 (name before `-e`, `--` separator). **[CODE-VERIFIED]**
- `configs/tavily.json` — remote `mcp-remote` endpoint; **zero Python readers** (grep of `src/superclaude/*.py`, `cli/*.py` found none). **[CODE-VERIFIED]**
- `plugins/superclaude/mcp/configs/tavily.json` — exists, identical remote content. **[CODE-VERIFIED]**
- Eval capability format = `mcp_server.<name>`: `capabilities.py` `_DEFAULT_CAPABILITY_SPECS` (~L184-247) lists `mcp_server.auggie`, `mcp_server.auggie-mcp`, `mcp_server.airis-mcp-gateway`; `real.yaml:37-40` declares `mcp_server.{auggie,auggie-mcp,airis-mcp-gateway,serena}` with `gate_flag: "--no-mcp", failure_mode: skip`. **No `mcp_server.tavily` registered yet.** **[CODE-VERIFIED]**
- `mcp.tavily` is STALE: only in `models.py:317,322` docstrings + `docs/eval/retry.md:139` + as substring of URL `mcp.tavily.com` + real test files `tests/cli/eval/test_mcp_retry_once.py`, `test_eval_outcome.py`. **[CODE-VERIFIED]**
- `docs/user-guide/mcp-servers.md:273` — `"args": ["-y", "tavily-mcp@latest"]`; L138 "Node.js 16+" (installer requires 18+ via `check_prerequisites`). **[CODE-VERIFIED]**
- `docs/reference/comprehensive-features.md:98` — `- tavily.json` in a config inventory (dangling after delete); L75/L80 also mention tavily. **[CODE-VERIFIED]**
- `sc-recommend/SKILL.md:4` — `allowed-tools: ..., mcp__tavily__tavily-search, mcp__tavily__tavily-extract, ...`; prose SKILL.md:169 + refs/plugin-ecosystem-sources.md:24. **[CODE-VERIFIED]**
- `tavily-mcp@0.1.2` also in archived `.dev/releases/complete/.../rca-agent-3-environment.md` (test scope must exclude .dev/). **[CODE-VERIFIED]**

## Key External Findings
- Tavily docs page is itself stale (cites 0.1.3); npm dist-tags is the authoritative version source.
