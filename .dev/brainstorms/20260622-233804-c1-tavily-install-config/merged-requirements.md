---
cluster: C1
title: Tavily Install / Config / Version-pin upgrade to tavily-mcp 0.2.x
convergence_score: 0.92
adversarial_status: pass
base_variant: opus:architect
created: 2026-06-22
---

# C1 Merged Spec — Tavily Install / Config / Version Pin

## Convergence summary

3 variants (opus:architect, sonnet:devops, haiku:backend) across 3 vendors. **Unanimous** on every substantive (L3) decision; differences were wording/emphasis (L1/L2). Base = architect (most decisive single-path); incorporated devops's literal argv + CI-mock test mechanics and backend's secret-hygiene rationale.

**Round-2.5 invariant probe — HIGH item resolved:** "exact `DEFAULT_PARAMETERS` env-var name/format unverified" → verified against tavily-mcp repo README: env var is literally `DEFAULT_PARAMETERS`, value is a JSON string (local: `-e DEFAULT_PARAMETERS='{...}'`; remote: a `DEFAULT_PARAMETERS` HTTP header). Status: ADDRESSED. No HIGH invariants remain.

## Decisions (unanimous)

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | **Pin exact `tavily-mcp@0.2.20`** (not `@latest`, not remote-only) | Reproducible CI, drift visible in diff, deliberate manual bumps. `@latest` breaks reproducibility; remote-only surrenders version control + adds network dependency. |
| D2 | **Delete `src/superclaude/mcp/configs/tavily.json`** | Orphan: zero Python readers (grep-confirmed). Asserts a *conflicting* remote transport. Embeds the API key in a URL query string → leak hazard in process listings / proxy logs. install_mcp.py is the sole authoritative install path. |
| D3 | **stdio-local transport** remains the install path | Matches the existing `claude mcp add --transport stdio … -- npx` mechanics; key passed via `-e` (not URL) → better secret hygiene. |
| D4 | **Adopt `DEFAULT_PARAMETERS`** with defaults `{"search_depth":"basic","max_results":10}`, co-located inline in `MCP_SERVERS["tavily"]` | Single source of truth for default search params; `basic` avoids the latency/cost of `advanced`; downstream call-sites (C2/C5) inherit unless they override per-call. |

## Concrete changes (by file)

### `src/superclaude/cli/install_mcp.py`
- Change `MCP_SERVERS["tavily"]["command"]` from `"npx -y tavily-mcp@0.1.2"` → `"npx -y tavily-mcp@0.2.20"`.
- Add to the tavily registry entry a structured field, e.g. `"default_parameters": {"search_depth": "basic", "max_results": 10}`.
- In `install_mcp_server()` env-arg assembly (after the `api_key_env` block, ~line 542-552): if `default_parameters` present, append `-e DEFAULT_PARAMETERS=<json.dumps(default_parameters)>` to `env_args`. Reuse the existing repeatable-`-e` path (no grammar change; server name still precedes `-e`).
- Resulting argv: `claude mcp add --transport stdio --scope user tavily -e TAVILY_API_KEY=<key> -e DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10} -- npx -y tavily-mcp@0.2.20`

### `src/superclaude/mcp/configs/tavily.json`
- **Delete the file.** (If any non-Python consumer is later found, replace — do not resurrect — with a stdio+pinned form mirroring the registry; but grep shows none.)

### `src/superclaude/cli/main.py`
- Help example at ~line 235 unchanged (`--servers tavily` is version-agnostic); no edit required. Listed only for completeness.

## Verification / tests (new: `tests/cli/test_install_mcp_tavily.py`)

| Test | Asserts | CI-safe? |
|------|---------|----------|
| `test_tavily_registry_pins_0_2_20` | `MCP_SERVERS["tavily"]["command"] == "npx -y tavily-mcp@0.2.20"` and transport `stdio` | yes (pure) |
| `test_default_parameters_propagated` | monkeypatch `_run_command`; capture argv; assert it contains `-e DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}` and `tavily-mcp@0.2.20`; **no npx spawned** | yes (mocked) |
| `test_api_key_never_in_logged_command` | the echoed "Running: …" line (install_mcp.py ~622) does not contain the raw key value | yes |
| `test_tavily_json_absent` | `configs/tavily.json` does not exist (guards against resurrection) | yes |
| `test_live_tavily_search_smoke` | gated `@pytest.mark.skipif(not os.getenv("TAVILY_API_KEY"))`: run `claude mcp add` then a `tavily-search`, assert non-empty result | skipped in CI |

## Acceptance criteria
- AC1: `grep -r "tavily-mcp@0.1.2"` returns nothing under `src/`.
- AC2: `configs/tavily.json` deleted; no Python import/Read references it.
- AC3: Installer-built argv contains the pinned version + a syntactically valid `DEFAULT_PARAMETERS` JSON env pair.
- AC4: `uv run pytest tests/cli/test_install_mcp_tavily.py` passes with no network; live smoke skips without a key.
- AC5: API key never appears in any echoed/logged command string.

## Cross-cluster handoffs
- **Version pin `0.2.20` is the shared global** all other clusters must reference (C6 frontmatter, C7 capability, C8 docs).
- **`DEFAULT_PARAMETERS` defaults** set here are the inheritance root for C2 (research engine may override `search_depth: advanced` per-call) and C5 (troubleshoot/reflect keep `basic`, rate-limited).
- **tavily.json deletion** must be reflected in C8 docs (mcp-installation/mcp-servers) that may reference the remote endpoint.
