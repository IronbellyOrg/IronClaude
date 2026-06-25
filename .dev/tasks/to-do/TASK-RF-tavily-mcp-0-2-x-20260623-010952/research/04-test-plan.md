# Research: Test / verification plan (Tavily 0.2.x)

**Topic type:** Test & Verification
**Status:** Complete
**Date:** 2026-06-23

7 new test files + drift guards. All CI-safe (no live network / API key); live exercises capability-gated → SKIP without key. Reflect fixes H3/H4/M3 folded in (test-scoping + assertions).

## Test files
1. `tests/cli/test_install_mcp_tavily.py` (C1 / M3)
   - `test_tavily_registry_pins_0_2_20`: `MCP_SERVERS["tavily"]["command"] == "npx -y tavily-mcp@0.2.20"`, transport stdio.
   - `test_default_parameters_field`: `MCP_SERVERS["tavily"]["default_parameters"] == {"search_depth":"basic","max_results":10}` (M3a).
   - `test_default_parameters_propagated`: monkeypatch `_run_command`; assert argv contains `-e` then a token `DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}` (compact JSON, M1) AND `tavily-mcp@0.2.20`; no npx spawned.
   - `test_api_key_never_in_logged_command`: echoed "Running:" line excludes the raw key.
   - `test_tavily_json_absent`: `src/superclaude/mcp/configs/tavily.json` does not exist.
   - `test_live_tavily_search_smoke`: `@pytest.mark.skipif(not os.getenv("TAVILY_API_KEY"))`.
2. `tests/agents/test_tavily_tool_parity.py` (C2/C6 + H1) — **glob `src/superclaude/{agents,skills}/**/*.md`** (NOT agents-only) parsing BOTH `tools:` and `allowed-tools:`:
   - every `mcp__tavily__*` in prose ∈ that file's frontmatter list and vice versa (covers deep-research*, 8 rf-*, AND sc-recommend).
   - `test_rf_no_map_crawl`: no rf-* agent references `tavily-map`/`tavily-crawl`.
   - `test_rf_fallback_provenance_present`: each rf-* retains a fallback-provenance form.
3. `tests/core/test_research_config.py` (C2): every Depth Profile names concrete `search_depth`+`extract_depth`+tools; `advanced` only with gating language; `maps`/`crawls` caps + crawl 50-URL truncation present.
4. `tests/commands/test_research_command.py` (C3): research.md has NO concrete params (`search_depth:`/`extract_depth:`/`max_results:`); tier names match RESEARCH_CONFIG.md.
5. `tests/skills/test_brainstorm_protocol.py` (C4): Wave-2A matrix has no Tavily params/tool names.
6. `tests/skills/test_tier2_tavily_consistency.py` (C5 + M3b): all 4 files reference `mcp__tavily__tavily-search`; allowed-tools=prose (no extract/map/crawl); ≤2-query cap present; fail-open present; **troubleshoot SKILL contains `search_depth: advanced`** (M3b); reflect names no per-call params.
7. `tests/docs/test_tavily_doc_alignment.py` (C8 + H3/H4) — **scope to `src/` + `docs/` ONLY, exclude `.dev/`, `.claude/`, `dist/`**:
   - `test_tavily_version_single_pin`: every `tavily-mcp@<ver>` in scope == `0.2.20` (H3).
   - `test_no_stale_mcp_tavily_token`: no `mcp.tavily` in scope EXCEPT the URL `mcp.tavily.com`; run AFTER the C7 docstring fix; word-boundary match, not substring (H4).
   - `test_no_tavily_json_references`: no doc references `configs/tavily.json`.
   - `test_docs_no_default_params_duplication`: docs link to MCP_Tavily.md, don't duplicate DEFAULT_PARAMETERS values.
8. `tests/cli/eval/` (C7/M2): `superclaude eval describe --suite real` parses; `mcp_server.tavily` resolves; new eval SKIPS without key; `test_capabilities_registers_mcp_server_tavily` (M2 mandatory registration).

## Verification commands
- `uv run pytest tests/cli/test_install_mcp_tavily.py tests/agents/test_tavily_tool_parity.py tests/core/test_research_config.py tests/commands/test_research_command.py tests/skills/ tests/docs/test_tavily_doc_alignment.py -v`
- `uv run ruff check src/ tests/` + `uv run ruff format --check src/ tests/`
- `make verify-sync` (after FLAGS.md edit + `make sync-dev`)
- `superclaude eval describe --suite real`
