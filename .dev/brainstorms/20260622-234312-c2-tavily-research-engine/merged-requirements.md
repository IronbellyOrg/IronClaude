---
cluster: C2
title: Deep-research engine upgrade to tavily-mcp 0.2.x (search/extract/map/crawl)
convergence_score: 0.88
adversarial_status: pass
base_variant: opus:architect
created: 2026-06-22
---

# C2 Merged Spec — Deep-Research Engine

## Convergence summary
3 variants (opus:architect, sonnet:analyzer, haiku:qa) across 3 vendors. Unanimous on the adoption envelope (map/crawl bounded + opt-in), `search_depth`/`extract_depth` gating by depth profile, and the parity test. Base = architect (routing model); merged in analyzer's param→methodology mappings and qa's parity-test + rate caps + fallback extensions.

**Invariant probe — HIGH resolved:** the silent-failure mode "routing prose tells the agent to call `tavily-map`/`tavily-crawl` but the tools frontmatter omits them" → ADDRESSED by mandating frontmatter additions + an automated parity test (below). MEDIUM (crawl result pollution / cost blowout) guarded by caps + scoping. No HIGH unaddressed.

## Decisions (unanimous)

| # | Decision |
|---|----------|
| D1 | **Adopt `tavily-map`** for the *discovery* phase of **deep + exhaustive** profiles only, on a single known site, to inventory URLs before extraction. NOT for quick/standard, NOT for multi-source open-web. |
| D2 | **Adopt `tavily-crawl`** for **exhaustive** profile only (opt-in within deep), single-domain comprehensive coverage, triggered as a last resort when search recall fails (<3 sources or >50% gap). NOT multi-domain. |
| D3 | **`search_depth` gating:** `basic` for quick/standard; `advanced` for deep/exhaustive, AND on replanning triggers (confidence <0.6, contradictions >30%, gaps). DEFAULT_PARAMETERS root `{"search_depth":"basic","max_results":10}` (C1 pin) is the inheritance baseline; deep/exhaustive override per-call. |
| D4 | **`extract_depth` gating:** `basic` for triage/quick/standard; `advanced` only for central, dense, or contradictory sources, and deep/exhaustive. |
| D5 | **Playwright vs crawl are orthogonal:** crawl = discovery (enumerate domain URLs), Playwright = extraction (render JS/auth pages). Crawl never obviates Playwright except on static-HTML domains. |
| D6 | **Map new search params to existing methodology:** `topic:news` + `days`/`time_range` for current-events/recency; `include_domains`/`exclude_domains` bound to the Source Credibility Matrix tiers + bias guardrails. |

## Concrete changes (by file)

### `src/superclaude/core/RESEARCH_CONFIG.md`
- Add a **Discovery Routing** table (map/crawl) alongside the existing Extraction Routing table — leave the extraction table's tavily/playwright/context7/native rows intact.
- In **Depth Profiles**, make each row name a concrete `search_depth` + `extract_depth` + tool set: quick=`basic`/`basic`/search+extract; standard=`basic`/`basic`/+selective extract; deep=`advanced`/`advanced`/+map(discovery); exhaustive=`advanced`/`advanced`/+map+crawl.
- Add `tools.discovery: [tavily-map, tavily-crawl]`; add parallel caps `maps=2, crawls=1`; crawl result truncation at 50 URLs. Stamp tavily-mcp `0.2.20`.
- Tie `include_domains`/`exclude_domains` to the Source Credibility Matrix; add `topic:news`/`days`/`time_range` to the recency methodology.

### `src/superclaude/agents/deep-research-agent.md` and `deep-research.md`
- **Frontmatter `tools:` add** `mcp__tavily__tavily-map` and `mcp__tavily__tavily-crawl` (deep-research-agent.md gets both; deep-research.md gets them too since its routing prose will reference them — parity required).
- Add a **Discovery Routing** block describing map (deep+) and crawl (exhaustive) conditions; keep the Tavily-first/fallback policy and per-source backend tagging, **extended**: map-unavailable → WebFetch fallback; crawl-unavailable → scoped `tavily-search`+`tavily-extract`; add `fallback_reason` enum values `tavily_map_*`, `tavily_crawl_*`. Tag new backends `tavily-map`/`tavily-crawl` in the sources table.
- Update Extraction Routing prose to add `extract_depth` basic/advanced selection criteria.

### `src/superclaude/mcp/MCP_Tavily.md`
- Update Search Capabilities + Search Patterns to the 0.2.x surface: add `tavily-map`, `tavily-crawl`, `search_depth`/`extract_depth` params, `topic`, `time_range`/`days`, domain filters. Stamp `0.2.20`. Add a "Default Parameters" note pointing at the C1 DEFAULT_PARAMETERS root.

### `src/superclaude/modes/MODE_DeepResearch.md`
- Line ~50 "Enables Tavily search capabilities" → broaden to "search, extraction, site-mapping, and domain-crawl" (one-line edit).

### `src/superclaude/examples/deep_research_workflows.md`
- Add one worked example showing map→extract on a known docs site (deep) and a guarded crawl (exhaustive); keep existing Playwright examples.

## Verification / tests
| Test | Asserts | Location |
|------|---------|----------|
| `test_tavily_tool_parity` | every `mcp__tavily__*` named in any routing table/prose of an agent .md is in that agent's `tools:` frontmatter, and no orphan frontmatter tool | `tests/agents/test_tavily_tool_parity.py` |
| `test_depth_profiles_name_concrete_params` | every Depth Profile row in RESEARCH_CONFIG.md names a `search_depth` + `extract_depth` + tool set; `advanced` only appears with gating language | `tests/core/test_research_config.py` |
| `test_research_config_caps_present` | `maps`/`crawls` caps + crawl truncation present | same |
| live exercise (opt-in, gated) | a real map→extract and a small crawl return non-empty | gated on `TAVILY_API_KEY` |

## Acceptance criteria
- AC1: Parity test green — no frontmatter/prose drift for any tavily tool.
- AC2: All four depth profiles name concrete `search_depth`/`extract_depth`/tools; `advanced` gated.
- AC3: map limited to discovery (deep+), crawl to exhaustive single-domain with the recall trigger + 50-URL cap documented.
- AC4: Fallback policy + `fallback_reason` enum + backend tagging cover map/crawl.
- AC5: Existing tavily-search/tavily-extract usage unchanged (additive-only).

## Cross-cluster handoffs
- Inherits C1 version pin `0.2.20` + DEFAULT_PARAMETERS root.
- The `tools:` frontmatter additions pattern + parity test is **shared with C6** (RF fleet) — same test should cover all agents.
- MCP_Tavily.md surface update is the doc source C8 should reference (avoid re-documenting params in two places).
