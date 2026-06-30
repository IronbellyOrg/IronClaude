---
cluster: C5
title: Troubleshoot + Reflect Tier-2 tavily-search alignment with tavily-mcp 0.2.x
convergence_score: 0.78
adversarial_status: pass
base_variant: opus:analyzer (troubleshoot) + haiku:backend (reflect)
created: 2026-06-22
---

# C5 Merged Spec — Troubleshoot / Reflect Tier-2 Search

## Convergence summary
3 variants (opus:analyzer, sonnet:qa, haiku:backend). Unanimous: tool id `mcp__tavily__tavily-search` unchanged in 0.2.x; **add no new tools** (no extract/map/crawl — this is rate-limited triage, not deep research); preserve the ≤2-query cap and fail-open/degraded behavior. One real disagreement — `search_depth: advanced` (analyzer) vs inherit `basic` (backend) — adjudicated by **use case**:

- **Troubleshoot Tier-2** fires only after in-repo grounding failed AND the symptom suggests external knowledge → the *hard* cases. The hard ≤2-query cap bounds cost, so `advanced` is justified to maximize hit-rate on obscure stack traces (analyzer wins here).
- **Reflect** Tier-2 is best-practice / spec-literal lookup, not obscure-symptom triage → inherit server-level `basic` default; DRY annotation only (backend wins here).

qa's "capability completion" risk (don't let triage grow into deep research) is honored by both paths.

## Decisions
| # | Decision |
|---|----------|
| D1 | Tool stays `mcp__tavily__tavily-search` only in both skills' allowed-tools — **no** tavily-extract/map/crawl added. |
| D2 | **Troubleshoot:** the focused Tier-2 query uses `search_depth: advanced` (per-call override of the C1 basic default), justified inline by "only hard cases reach Tier-2; the ≤2-query cap bounds cost." Recommend (not mandate) `include_domains: [github.com, stackoverflow.com]` for the error-string query. `topic:news` explicitly excluded (technical). ≤2-query cap unchanged. |
| D3 | **Reflect:** inherit server-level DEFAULT_PARAMETERS (`basic`, 10) — no per-call params; one annotation line "inherits server-level DEFAULT_PARAMETERS (C1)". |
| D4 | Fail-open / degraded behavior on Tavily-down preserved verbatim in both skills. |

## Concrete changes (by file)
### `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- Focused-query block (~line 335): add `search_depth: advanced` + recommended `include_domains` to the rate-limited query instruction, with the cost justification. Do NOT weaken the ≤2-query cap (~335/510/538).
- Capability table (~510) + fallback row (~371): unchanged in meaning; verify tavily-search description stays "Tier 2, rate-limited".

### `src/superclaude/commands/troubleshoot.md`
- Line ~99 bullet: keep "targeted web search (Tier 2, rate-limited)"; optionally note "advanced depth for obscure symptoms" (one clause). No frontmatter change (server-level).

### `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- tavily-search reference: add one annotation "inherits server-level DEFAULT_PARAMETERS (C1)". Keep fail-open line (~1689) intact.

### `src/superclaude/commands/reflect.md`
- Line ~151: unchanged ("targeted web search (Tier 2, rate-limited)"). No frontmatter change.

## Verification / tests (`tests/skills/test_tier2_tavily_consistency.py`)
| Test | Asserts |
|------|---------|
| tool-id parity | all 4 files reference `mcp__tavily__tavily-search`; allowed-tools = prose tools; **no** tavily-extract/map/crawl present |
| rate-cap intact | troubleshoot SKILL still states ≤2 queries (≥1 occurrence) |
| fallback intact | both skills retain fail-open/degraded language for Tavily-down |
| param discipline | only troubleshoot's focused-query block names `search_depth: advanced`; reflect names no per-call params (inherits) |

## Acceptance criteria
- AC1: No new Tavily tools in either skill (search-only).
- AC2: Troubleshoot Tier-2 uses advanced depth + recommended domain filter; ≤2 cap preserved.
- AC3: Reflect inherits the basic default with a one-line annotation; no duplicated params.
- AC4: Fail-open/degraded behavior unchanged; consistency test green.

## Cross-cluster handoffs
- Inherits C1 pin + DEFAULT_PARAMETERS. **Divergence noted:** troubleshoot overrides to `advanced` (the only cluster outside C2 that does) — this is intentional and cost-bounded.
- Shares C4's fallback-fidelity concept (WebSearch fallback loses 0.2.x features).
- The no-new-tools guard + allowed-tools↔prose parity test overlaps C2/C6 parity test — consolidate into one test module if convenient.
