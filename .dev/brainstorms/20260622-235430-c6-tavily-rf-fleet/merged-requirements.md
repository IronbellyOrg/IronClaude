---
cluster: C6
title: RF agent fleet — Tavily usage under tavily-mcp 0.2.x (verify + parity, no functional change)
convergence_score: 0.90
adversarial_status: pass
base_variant: opus:architect
created: 2026-06-22
---

# C6 Merged Spec — RF Agent Fleet

## Convergence summary
2 variants (opus:architect, sonnet:qa), tight agreement. The fleet's Tavily integration is already mature (Tavily-first + auditable fallback-provenance). The 0.2.x upgrade is **transparent at the agent level** — version is install-level (C1), tool IDs unchanged. **No functional change needed**; this cluster is verify + lock-in via test.

## Decisions
| # | Decision |
|---|----------|
| D1 | **No frontmatter change** for any of the 8 RF agents (rf-qa, rf-qa-qualitative, rf-task-researcher, rf-task-builder, rf-team-lead, rf-analyst, rf-assembler, rf-task-executor). Each already declares exactly `mcp__tavily__tavily-search` + `mcp__tavily__tavily-extract` matching its prose. |
| D2 | **No map/crawl** for any RF agent, including rf-task-researcher. RF research is targeted task-context gathering, not exhaustive web crawl. Adding map/crawl would multiply the fallback-provenance matrix (no WebSearch crawl analogue) and break the auditable two-verb "do not fall back silently" contract for zero role benefit. |
| D3 | **DEFAULT_PARAMETERS auto-inherited** (server-level, C1) — agents call search/extract without per-call params; no prose hardcodes them. No change. |
| D4 | **Fallback-provenance vocab left as-is per agent** (RF uses `tavily-unavailable\|tavily-error\|tavily-rate-limit`; deep-research C2 uses `tavily_missing\|tavily_error\|tavily_rate_limit\|tavily_auth`). Standardize only semantic *classes* in the test, not the literal wire strings — changing them would break existing provenance artifacts. Scope discipline. |

## Concrete changes
- **None to the 8 agent files.** This cluster adds tests only.

## Verification / tests
| Test | Asserts | Location |
|------|---------|----------|
| `test_tavily_tool_parity` (fleet-wide, **shared with C2**) | glob `src/superclaude/agents/*.md`; every `mcp__tavily__*` named in prose ∈ that agent's `tools:` frontmatter, and vice versa | `tests/agents/test_tavily_tool_parity.py` |
| `test_rf_no_map_crawl` | no RF agent references or lists `tavily-map`/`tavily-crawl` (guards "capability completion") | same |
| `test_rf_fallback_provenance_present` | each RF agent that lists tavily tools retains a fallback-provenance mechanism (one of the accepted forms: `Tool engagement:`, `WEB SEARCH PROVENANCE`, `WEB_RESEARCH_FALLBACK`, `web-provenance`) — semantic-class check, not literal-string | same |

## Acceptance criteria
- AC1: All 8 RF agent files unchanged; diff is tests-only.
- AC2: Parity test green fleet-wide; map/crawl guard green.
- AC3: Existing fallback-provenance forms still validate (backward-compat).

## Cross-cluster handoffs
- **Parity test is shared with C2** (and overlaps C5's allowed-tools↔prose check) → consolidate into one `test_tavily_tool_parity.py` covering all agents + skills.
- Inherits C1 pin + DEFAULT_PARAMETERS; nothing agent-local.
