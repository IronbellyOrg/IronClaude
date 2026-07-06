# Variant 2 — QA Change Spec: TROUBLESHOOT + REFLECT Tavily Tier-2 Search Upgrade

## QA position

Upgrade the documented Tavily integration to tavily-mcp 0.2.20 without expanding the Tier-2 triage surface. Official tavily-mcp docs still expose the hyphenated MCP tool name `tavily-search`; Claude Code's namespaced tool id remains `mcp__tavily__tavily-search`. Although tavily-mcp also advertises extract/map/crawl, this cluster is intentionally search-only: targeted web search for rate-limited triage, not deep research.

## Minimal edits

1. In `src/superclaude/commands/troubleshoot.md` and `src/superclaude/commands/reflect.md`, keep `mcp-servers: [auggie, serena, context7, tavily, sequential]` and keep the Tool Coordination entry exactly on `mcp__tavily__tavily-search`. Add only one compact clarification to the Tavily MCP Integration bullet:
   - `Uses tavily-mcp 0.2.20 search only with DEFAULT_PARAMETERS {"search_depth":"basic","max_results":10}; do not use extract/map/crawl in Tier 2.`
2. In `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` and `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, do not add allowed tools. The allowed-tools frontmatter already includes `mcp__tavily__tavily-search` and not `mcp__tavily__tavily-extract`, `mcp__tavily__tavily-map`, or `mcp__tavily__tavily-crawl`.
3. Troubleshoot-specific: preserve every `≤2 queries` / `at most 2 queries` constraint. Any new default-parameter prose must be subordinate to the existing cap: defaults constrain each allowed search call; they do not authorize more calls.
4. Fallback behavior must remain fail-open. Troubleshoot keeps `MCP call fails (context7/tavily) → continue without external docs; note in audit`. Reflect keeps `Fail-open on missing MCPs (auggie, serena, context7, tavily) — fall back to native tools and mark degraded.` If adding Tavily-down wording, use “continue without Tavily results; mark degraded/Grounding Gap,” never STOP.
5. Keep wording aligned across all four files: `mcp__tavily__tavily-search`, `targeted web search`, `Tier 2`, `rate-limited`, `search-only`, `DEFAULT_PARAMETERS {"search_depth":"basic","max_results":10}`.

## Consistency / parity test

Add a focused pytest, e.g. `tests/test_tavily_tier2_search_parity.py`, that reads these four source-of-truth files and asserts:

- Both command files list `tavily` in `mcp-servers` and contain the exact tool id `mcp__tavily__tavily-search`.
- Both skill frontmatter `allowed-tools` contain exactly the Tavily search tool and no Tavily extract/map/crawl tool ids.
- All four files contain `Tier 2` and `rate-limited` near the Tavily search prose.
- Troubleshoot skill contains at least one `≤2 queries` or `at most 2 queries` cap and no added text matching “increase”, “more than 2”, or unbounded “multi-round” Tavily search guidance.
- Fallback/degraded language remains present: troubleshoot has `context7/tavily` + `Continue without external docs`; reflect has `missing MCPs` + `tavily` + `mark degraded`.
- Optional: assert any `DEFAULT_PARAMETERS` prose contains both `search_depth":"basic` and `max_results":10`.

## Acceptance criteria

- tavily-mcp pin is documented as `0.2.20` for this cluster.
- `mcp__tavily__tavily-search` is the only Tavily tool id in both SKILL allowed-tools lists.
- No extract/map/crawl guidance is introduced for troubleshoot or reflect Tier 2.
- Troubleshoot’s ≤2-query cap is unchanged and tested.
- Tavily unavailable paths continue fail-open and surface degraded/Grounding Gap state.
- The parity test fails on any future prose/frontmatter drift across troubleshoot.md, reflect.md, and both SKILL.md files.

## Biggest QA risk

The most likely regression is well-intentioned “0.2.x capability completion” that adds extract/map/crawl to allowed-tools or prose. That would silently convert cheap Tier-2 triage into deep research and bypass the rate-limit contract.
