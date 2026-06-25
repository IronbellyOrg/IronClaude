# Consolidated Tavily 0.2.x Upgrade — Change List (8-cluster brainstorm synthesis)

Synthesizes the 8 per-cluster merged specs (`.dev/brainstorms/2026062*-c{1..8}-*/merged-requirements.md`).
Verified baseline (2026-06-22/23): npm `tavily-mcp` latest = **0.2.20**; 0.2.x tools = `tavily-search`, `tavily-extract`, `tavily-map`, `tavily-crawl`; config via `DEFAULT_PARAMETERS` (JSON env for local `-e`, same-named HTTP header for remote).

---

## Cross-cluster invariants (must stay consistent)

| # | Invariant | Owner | Consumers |
|---|-----------|-------|-----------|
| X1 | **Version pin = `tavily-mcp@0.2.20`** (exact, not `@latest`, not remote-only) | C1 | C7 (eval), C8 (docs + drift test). Was 3-way conflict: install_mcp.py `0.1.2`, tavily.json remote-unpinned, mcp-servers.md `@latest`. |
| X2 | **Single config source of truth = `install_mcp.py` registry**; orphan `configs/tavily.json` DELETED (zero readers + secret-in-URL hazard) | C1 | C8 (remove dangling doc ref) |
| X3 | **`DEFAULT_PARAMETERS` root = `{"search_depth":"basic","max_results":10}`**, injected server-level at install | C1 | C2 overrides `advanced` for deep/exhaustive; C5-troubleshoot overrides `advanced`; C5-reflect + C6 inherit `basic` |
| X4 | **Eval capability token = `mcp_server.tavily`** — `mcp.tavily` is STALE/non-registered (would false-green SKIP) | C7 | C8 (fix docs/eval/retry.md + models.py docstrings) |
| X5 | **map/crawl adopted ONLY in the deep-research engine** (C2); explicitly NOT in RF fleet (C6), troubleshoot/reflect (C5), or brainstorm (C4) | C2 | C4/C5/C6 guards |
| X6 | **Anti-duplication:** commands/docs POINT to `MCP_Tavily.md` + `install_mcp.py`; never duplicate param tables | C3 | C4, C8 |
| X7 | **Frontmatter↔prose parity** for every `mcp__tavily__*` tool id | C2 | C5, C6 (one shared test) |

---

## Changes grouped by file

### Code — install / eval
- **`src/superclaude/cli/install_mcp.py`** (C1): `command` `tavily-mcp@0.1.2` → `@0.2.20`; add `default_parameters` field to the tavily registry entry; in `install_mcp_server()` append `-e DEFAULT_PARAMETERS=<json>` to `env_args` (reuse repeatable-`-e` path, no grammar change).
- **`src/superclaude/mcp/configs/tavily.json`** (C1): **DELETE** (orphan; conflicting remote transport; key-in-URL leak).
- **`src/superclaude/cli/main.py`** (C1): no change (help example is version-agnostic).
- **`src/superclaude/cli/eval/suites/real.yaml`** (C7): add `- { name: mcp_server.tavily, gate_flag: "--no-mcp", failure_mode: skip }` to capability block; add eval `E-tavily-search` (`requires: [mcp_server.tavily]`, `expect_tool_call: mcp__tavily__tavily-search`, exit 0; SKIPs without key).
- **`src/superclaude/cli/eval/capabilities.py`** (C7, optional): add `_CapabilitySpec` row `mcp_server.tavily` (kind `mcp_server`).
- **`src/superclaude/cli/eval/models.py`** (C7): docstring examples (~L317/322) `mcp.tavily` → `mcp_server.tavily`.

### Research engine (C2) — the substantive tool-surface upgrade
- **`src/superclaude/core/RESEARCH_CONFIG.md`**: add Discovery Routing table (map/crawl); make each Depth Profile name concrete `search_depth`+`extract_depth`+tools (quick/standard=basic, deep/exhaustive=advanced; map@deep+, crawl@exhaustive); add caps `maps=2, crawls=1`, crawl truncation 50 URLs; stamp `0.2.20`; bind domain filters to Source Credibility Matrix; add `topic:news`/`days`/`time_range` recency.
- **`src/superclaude/agents/deep-research-agent.md`** + **`deep-research.md`**: add `mcp__tavily__tavily-map` + `mcp__tavily__tavily-crawl` to `tools:` frontmatter; add Discovery Routing block; extend fallback policy + `fallback_reason` enum + backend tagging to map/crawl; add `extract_depth` selection criteria.
- **`src/superclaude/mcp/MCP_Tavily.md`** (canonical capability doc): update to 0.2.x surface (map/crawl, search_depth/extract_depth, topic, time_range/days, domain filters); add DEFAULT_PARAMETERS note; stamp `0.2.20`.
- **`src/superclaude/modes/MODE_DeepResearch.md`**: one-line broaden ("search, extraction, site-mapping, domain-crawl").
- **`src/superclaude/examples/deep_research_workflows.md`**: add one map→extract (deep) + guarded crawl (exhaustive) worked example.

### Commands / skills (consumers — light touch)
- **`src/superclaude/commands/research.md`** (C3): broaden MCP-Integration Tavily line (name map/crawl + pointer); add one Adaptive-Depth engine-pointer sentence. No frontmatter change, no param duplication.
- **`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`** (C4): one Wave-2A inheritance sentence + one fallback-fidelity note (WebSearch fallback loses 0.2.x features). `commands/brainstorm.md`: no change.
- **`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`** (C5): focused Tier-2 query gets `search_depth: advanced` + recommended `include_domains:[github.com,stackoverflow.com]` (justified: only hard cases reach Tier-2; ≤2-query cap bounds cost). ≤2 cap unchanged. `commands/troubleshoot.md`: optional one clause.
- **`src/superclaude/skills/sc-reflect-protocol/SKILL.md`** (C5): one annotation "inherits server-level DEFAULT_PARAMETERS (C1)"; fail-open intact. `commands/reflect.md`: no change.
- **8 RF agents** `rf-{qa,qa-qualitative,task-researcher,task-builder,team-lead,analyst,assembler,task-executor}.md` (C6): **no file change** (tool ids unchanged, version is install-level, defaults auto-inherited, no map/crawl). Tests only.

### Docs (C8) — alignment + drift guards
- **`docs/user-guide/mcp-servers.md`**: L273 `tavily-mcp@latest` → `@0.2.20`; L138 "Node.js 16+" → "18+"; one map/crawl capability line + MCP_Tavily.md pointer.
- **`docs/reference/comprehensive-features.md`**: broaden tavily capability line (pointer); **remove the deleted `tavily.json`** from config inventory.
- **`src/superclaude/core/FLAGS.md`**: broaden `--tavily` Behavior (search→search/extract/map/crawl + pointer); then `make sync-dev` + `make verify-sync`.
- **`docs/eval/retry.md`**: L~138 `mcp.tavily` → `mcp_server.tavily`.
- **Need nothing:** core/MODES.md, core/COMMANDS.md, docs/user-guide/{mcp-installation,commands,flags,modes,agents}.md, docs/mcp/{mcp-integration-policy,mcp-optional-design}.md, docs/reference/basic-examples.md. **Excluded:** docs/research/*, docs/analysis/* (research-output artifacts).

---

## New tests
| Test file | Covers | Clusters |
|-----------|--------|----------|
| `tests/cli/test_install_mcp_tavily.py` | registry pins 0.2.20; DEFAULT_PARAMETERS in argv; key never logged; tavily.json absent; gated live smoke | C1 |
| `tests/agents/test_tavily_tool_parity.py` | frontmatter↔prose parity for all `mcp__tavily__*`; RF map/crawl guard; fallback-provenance present | C2, C6 (shared) |
| `tests/core/test_research_config.py` | depth profiles name concrete params; caps present | C2 |
| `tests/commands/test_research_command.py` | no param duplication; tier names match config | C3 |
| `tests/skills/test_brainstorm_protocol.py` | no Tavily param/tool duplication in Wave 2A | C4 |
| `tests/skills/test_tier2_tavily_consistency.py` | tavily-search-only; ≤2 cap; fail-open; param discipline | C5 |
| `tests/docs/test_tavily_doc_alignment.py` | **version single-pin (0.2.20)** + no stale `mcp.tavily` + no `tavily.json` refs + no DEFAULT_PARAMETERS doc duplication | C7, C8 (shared release guard) |

---

## Suggested implementation order (dependency-respecting)
1. **C1** (install_mcp.py version + DEFAULT_PARAMETERS; delete tavily.json) — establishes X1/X2/X3.
2. **C2** (research engine + MCP_Tavily.md canonical) — establishes X5/X7, the tool surface.
3. **C7** (register `mcp_server.tavily` + verification eval) — establishes X4, the proof vehicle.
4. **C3, C4, C5, C6** (consumers — inherit/point; light edits + tests) — parallelizable.
5. **C8** (docs alignment + drift-guard tests) — consumes all; run `make sync-dev`/`verify-sync` for FLAGS.md.

## Per-cluster convergence
C1 0.92 · C2 0.88 · C3 0.85 · C4 0.90 · C5 0.78 · C6 0.90 · C7 0.80 · C8 0.90 — all PASS (≥0.65). Lowest (C5, C7) reflect genuine adjudicated disagreements (advanced-vs-basic depth; verified capability-token correction), both resolved with evidence.
