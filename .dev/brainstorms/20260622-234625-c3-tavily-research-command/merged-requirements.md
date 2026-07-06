---
cluster: C3
title: /sc:research command alignment with tavily-mcp 0.2.x engine
convergence_score: 0.85
adversarial_status: pass
base_variant: haiku:qa
created: 2026-06-22
---

# C3 Merged Spec — /sc:research Command

## Convergence summary
2 variants (opus:architect, haiku:qa). Agreement: no frontmatter change; minimal edits; command must reference the engine, not duplicate C2. Sole tension — annotate `search_depth` per depth tier (architect) vs keep generic pointers (qa) — resolved toward **qa's anti-duplication discipline** (avoid a second source of truth that drifts on the next tavily bump), keeping the architect's "name map/crawl for discoverability" point.

## Decisions
| # | Decision |
|---|----------|
| D1 | **No frontmatter change.** `mcp-servers: [tavily, …]` is server-level; tavily-map/crawl are new tools under the unchanged `tavily` server. Editing it is scope creep. |
| D2 | **`## MCP Integration` Tavily line:** broaden "Primary search and extraction engine" → "Primary search, extraction, site-mapping (`tavily-map`) and domain-crawl (`tavily-crawl`) engine — see deep-research-agent / RESEARCH_CONFIG.md for routing." One generic pointer; no semantics duplicated. |
| D3 | **`### Adaptive Depth`:** add ONE pointer sentence ("Per-tier `search_depth`/`extract_depth` and map/crawl selection are defined by the research engine — see RESEARCH_CONFIG.md Depth Profiles."). Do **not** annotate each tier with concrete params (that would duplicate the C2 single source of truth). |
| D4 | **"Smart extraction" bullet:** no change — already a correct thin abstraction of `extract_depth` routing. |

## Concrete changes (file: `src/superclaude/commands/research.md`)
- MCP Integration → edit the Tavily line per D2.
- Adaptive Depth → append the single pointer sentence per D3.
- No other edits; no frontmatter edit.

## Verification / tests
| Test | Asserts | Location |
|------|---------|----------|
| `test_research_command_no_param_duplication` | research.md contains **no** concrete param claims (`search_depth:`, `extract_depth:`, `max_results:`, numeric tool defaults) — it may only be generic/point to the engine | `tests/commands/test_research_command.py` |
| `test_research_tiers_match_config` | the four depth tiers in research.md (quick/standard/deep/exhaustive) match RESEARCH_CONFIG.md Depth Profiles names+order, and quick/standard never claim `advanced` | same |

## Acceptance criteria
- AC1: research.md names map/crawl exactly once (MCP Integration) + one engine-pointer in Adaptive Depth; no routing tables.
- AC2: Anti-duplication test green (zero concrete params in the command file).
- AC3: Tier names consistent with RESEARCH_CONFIG.md; no contradiction.

## Cross-cluster handoffs
- Entirely downstream of **C2** — RESEARCH_CONFIG.md / deep-research-agent.md remain the single source of truth for params; C3 only points at them.
- The anti-duplication test pattern is reusable for C8 docs (docs should also point, not duplicate).
