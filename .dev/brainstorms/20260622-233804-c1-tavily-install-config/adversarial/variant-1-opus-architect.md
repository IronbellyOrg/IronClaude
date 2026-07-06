# Tavily MCP Upgrade — Architect Variant (Option A: pin 0.2.20, single SoT, local stdio)

## Decision summary

- **Version policy: A — pin exact `0.2.20`** via local `npx`. Reproducible, drift is diff-visible, manual bumps are an explicit reviewed event. Reject @latest (non-reproducible CI, silent tool-surface drift) and remote-only (cedes version control to Tavily, adds a network/SSE dependency in the hot path with no rollback handle).
- **SoT resolution: `install_mcp.py` is the ONE authoritative path. DELETE `tavily.json`.** Grep finds zero Python readers of `src/superclaude/mcp/configs/tavily.json` — it is orphan config asserting a *different* transport (remote vs stdio) than the live installer. Two configs that disagree and one is dead = the textbook single-source-of-truth violation. Keeping it "for the future" institutionalizes the drift this variant exists to kill. The remote endpoint stays documented in a comment, not as a competing executable config.
- **DEFAULT_PARAMETERS: ADOPT, with conservative defaults co-located in the registry entry.** 0.2.x exposes the mechanism; declining it leaves call-site token cost uncontrolled. Defaults live next to the command in `MCP_SERVERS["tavily"]` — same SoT, same diff.

## (a) Version policy + SoT

`MCP_SERVERS["tavily"]["command"]` is the only place a version string for Tavily may appear in the repo after this change. Pin is literal `tavily-mcp@0.2.20`. Bumps = one-line PR editing that token, reviewable in isolation.

**Acceptance:** `grep -rn "tavily-mcp@" src/` returns exactly one hit, and it is `@0.2.20`. `grep -rn "mcp.tavily.com" src/` returns zero hits in executable config (comment-only allowed).

## (b) Exact updated registry entry

`src/superclaude/cli/install_mcp.py`, replace the `"tavily"` block (~76–84):

```python
"tavily": {
    "name": "tavily",
    "description": "Web search and real-time information retrieval for deep research",
    "transport": "stdio",
    # Pinned exact for reproducibility; bump deliberately via PR. dist-tags.latest=0.2.20 (2026-06-22).
    # Remote alt (Tavily-managed, no version control): https://mcp.tavily.com/mcp/?tavilyApiKey=<key> — intentionally NOT used.
    "command": "npx -y tavily-mcp@0.2.20",
    "required": False,
    "api_key_env": "TAVILY_API_KEY",
    "api_key_description": "Tavily API key for web search (get from https://app.tavily.com)",
    "default_parameters": {"search_depth": "basic", "max_results": 10},
},
```

The installer must serialize `default_parameters` (if present) into the env injected before the server name, preserving CLI grammar:
`claude mcp add --transport stdio [--scope user] tavily -e TAVILY_API_KEY=<key> -e TAVILY_DEFAULT_PARAMETERS='{"search_depth":"basic","max_results":10}' -- npx -y tavily-mcp@0.2.20`
(JSON compact-dumped; env name verified against 0.2.x before merge — if the package reads `DEFAULT_PARAMETERS` unprefixed, use that exact key. The builder logic: extend the existing `-e KEY=VALUE` emission loop to also emit a `-e <PARAM_ENV>=<json>` pair when `default_parameters` is set. Never log the JSON value or the key.)

**Acceptance:** dry-run install for `tavily` prints a command containing `tavily-mcp@0.2.20`, `--transport stdio`, server name `tavily` positioned before any `-e`, and the `-e TAVILY_API_KEY=` flag. API key value never appears in logs/echo (masked or omitted).

## (c) DEFAULT_PARAMETERS adoption

Adopt. Defaults `{"search_depth":"basic","max_results":10}` minimize per-call token/latency cost as a sane floor; callers override per-request. They live in the registry entry (above) — the single SoT — not in a second file. The builder gates emission on the key's presence so other servers are unaffected.

**Acceptance:** with `default_parameters` present, the built command carries the param env pair; with it removed, no param env pair is emitted (no empty `-e`). Param JSON is compact (`json.dumps(..., separators=(",", ":"))`) and shell-safe.

## (d) Verification / tests

**Unit (CI, no network) — `tests/cli/test_install_mcp_tavily.py`:**
1. `test_tavily_registry_pins_0_2_20` — assert `MCP_SERVERS["tavily"]["command"] == "npx -y tavily-mcp@0.2.20"` and `transport == "stdio"`. Fails the build on any unreviewed bump.
2. `test_tavily_command_grammar` — build the dry-run/arg list for `tavily`; assert order `... tavily -e TAVILY_API_KEY=... [-e <PARAM_ENV>=...] -- npx ...` (server name precedes `-e`; `--` precedes `npx`).
3. `test_tavily_default_parameters_emitted` — assert the param env pair is present and its value parses as JSON equal to `{"search_depth":"basic","max_results":10}`.
4. `test_api_key_never_logged` — capture installer stdout on dry-run with a fake key; assert the fake key substring is absent.
5. `test_no_orphan_tavily_config` — assert `src/superclaude/mcp/configs/tavily.json` does not exist (locks the deletion).

**Live smoke (opt-in, capability-gated) — `tests/integration/test_tavily_live_smoke.py`:**
`@pytest.mark.skipif(not os.getenv("TAVILY_API_KEY"), reason="no TAVILY_API_KEY")` plus `@pytest.mark.live`. Launch `npx -y tavily-mcp@0.2.20` over stdio, perform one MCP `initialize` + a single `tavily-search` round-trip (query "site reliability"), assert a non-empty results payload and that the 0.2.x tool list includes `tavily-search` and `tavily-extract`. Never asserts on key contents; never runs in default CI (`-m "not live"`).

**Top test:** `test_tavily_registry_pins_0_2_20` — it is the executable guardian of the version policy and the SoT.

## Out of scope / cosmetic
`src/superclaude/cli/main.py` ~235 help example needs no change (server name unchanged). Delete `tavily.json`; `make sync-dev` then `make verify-sync` to propagate to `.claude/` (never edit `.claude/` directly).
