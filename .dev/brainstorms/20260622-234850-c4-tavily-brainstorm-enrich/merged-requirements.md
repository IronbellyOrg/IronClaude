---
cluster: C4
title: /sc:brainstorm research-enrichment alignment with tavily-mcp 0.2.x
convergence_score: 0.90
adversarial_status: pass
base_variant: opus:architect
created: 2026-06-22
---

# C4 Merged Spec — /sc:brainstorm Research Enrichment

## Convergence summary
2 variants (opus:architect, sonnet:analyzer), tight agreement. Brainstorm enrichment is downstream of /sc:research + tech-research → it **inherits** engine behavior and must not grow its own Tavily config. No stale claims found.

## Decisions
| # | Decision |
|---|----------|
| D1 | **No frontmatter change.** `mcp-servers: [sequential, serena, auggie-mcp, tavily]` is server-level; version/param pins live in the engine (C1/C2). |
| D2 | **`--research light/deep` mapping stated as inheritance, not a duplicated table:** light → `/sc:research` (quick-tier, `search_depth: basic`); deep → `tech-research` (inherits `advanced`). Brainstorm names the route; the engine owns the params. |
| D3 | **Keep "Tavily down → WebSearch" fallback verbatim** (tool-agnostic, substitutes for light single-call enrichment), but add a one-line **fidelity note** to the SKILL error row: WebSearch fallback loses 0.2.x depth/map/crawl features (record in `quality_tier=fallback_1`). |
| D4 | **Brainstorm does NOT name map/crawl** — engine-only concern; leaking them here is scope creep. |

## Concrete changes
### `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- Wave 2A enrichment matrix: add one inheritance sentence ("research depth/params are owned by /sc:research and tech-research — see RESEARCH_CONFIG.md; brainstorm selects the route only").
- Error-handling matrix, "Research enrichment fails (Tavily down)" row: append fidelity note per D3.

### `src/superclaude/commands/brainstorm.md`
- No edits required (example wording "Tavily research enrichment" remains accurate). Listed for completeness.

### `docs/user-guide/brainstorm.md`
- No change needed beyond C8 doc sweep; `--research light (Tavily) / deep (tech-research)` remains accurate.

## Verification / tests
| Test | Asserts | Location |
|------|---------|----------|
| `test_brainstorm_no_tavily_param_duplication` | SKILL.md Wave 2A matrix contains no concrete Tavily params (`search_depth:`, `max_results:`, `tavily-map`, `tavily-crawl`) — enrichment only routes | `tests/skills/test_brainstorm_protocol.py` |

## Acceptance criteria
- AC1: One inheritance sentence + one fallback-fidelity note added; nothing else.
- AC2: No Tavily params or map/crawl names appear in brainstorm command/skill.
- AC3: Non-duplication test green.

## Cross-cluster handoffs
- Downstream of **C2/C3**; inherits the engine's single source of truth.
- Fallback-fidelity note pattern is shared with **C5** (troubleshoot/reflect also fall back to WebSearch).
