# Variant 3 — QA Spec: Tavily 0.2.x Map/Crawl Upgrade (HAiKU)

**CROSS-CLUSTER PIN (C1):** tavily-mcp 0.2.20; defaults `{"search_depth":"basic","max_results":10}`.
**Author:** QA Advocate | **Date:** 2026-06-22

---

## (A) Frontmatter `tools:` Additions

Both agents need the new MCP tool names in their `tools:` allow-list. The tool names use hyphens:

| Agent File | Current Tavily Tools | Add |
|---|---|---|
| `src/superclaude/agents/deep-research.md` | `mcp__tavily__tavily-search`, `mcp__tavily__tavily-extract` | `mcp__tavily__tavily-map`, `mcp__tavily__tavily-crawl` |
| `src/superclaude/agents/deep-research-agent.md` | `mcp__tavily__tavily-search`, `mcp__tavily__tavily-extract` | `mcp__tavily__tavily-map`, `mcp__tavily__tavily-crawl` |

No other tools lists are touched. These two files are the authoritative allow-lists; any routing prose that names a tool not present here will fail at runtime.

## (B) Doc-Frontmatter PARITY Check — Automated Test

**File:** `tests/agents/test_tavily_tool_parity.py`

**Design:** A pytest test that:
1. Parses the YAML frontmatter `tools:` list from both agent `.md` files.
2. Collects every `mcp__tavily__*` identifier referenced in agent/instruction prose (routing tables, workflow steps, Fallback Policy sections) across `src/superclaude/agents/`, `src/superclaude/core/RESEARCH_CONFIG.md`, `src/superclaude/mcp/MCP_Tavily.md`.
3. Asserts bidirectional parity: every `mcp__tavily__*` found in prose is in the tools list, and every `mcp__tavily__*` in the tools list is referenced in at least one routing table or workflow description.

**Pass condition:** zero delta in both directions. **Fail:** lists the mismatched tool names and which file(s) contain them.

## (C) Fallback Policy Extension

Extend the existing "Detecting Tavily unavailable" section in `deep-research.md` to cover map/crawl:

- Add `tavily-map` and `tavily-crawl` to the unavailable-tool detection set. If either tool is missing from the session, fall back to:
  - **map unavailable** -> `WebFetch` on the known seed URL (single-page snapshot only; note in `fallback_reason: map_unavailable`).
  - **crawl unavailable** -> sequential `mcp__tavily__tavily-search` with `include_domains` scoped to the target domain, followed by `mcp__tavily__tavily-extract` on discovered URLs. Note `fallback_reason: crawl_unavailable`.
- Extend `fallback_reason` enum: `tavily_missing | tavily_error | tavily_rate_limit | tavily_auth | map_unavailable | crawl_unavailable`.
- The `mcp__tavily__tavily-map` and `mcp__tavily__tavily-crawl` calls inherit the same transport-level error rules (2 consecutive failures = unavailable).

## (D) Rate-Limit Caps for Map/Crawl

Extend `RESEARCH_CONFIG.md` parallel limits:

```yaml
# Parallel limits: searches=5, extractions=3, analyses=2
maps=2, crawls=1
```

**Rationale:** `tavily-crawl` is the heaviest operation (recursive site traversal); cap at 1 concurrent crawl to avoid hammering a single domain or consuming the API budget. `tavily-map` is lighter but can return large result sets on complex SPAs; cap at 2 concurrent maps.

**Crawl result truncation:** If a crawl returns >50 URLs, take the top 50 by relevance score and note `truncated: true, total_discovered: <N>` in the synthesis. Do not chain a second crawl from the first crawl's output without an explicit user gate.

**Map on single-page site:** If `tavily-map` returns <3 URLs, treat it as a signal the site has no internal link graph and fall back to `tavily-extract` on the seed URL directly. No retry.

## (E) Backward-Compatibility Guard

- `tavily-search` and `tavily-extract` remain unchanged in default params, routing order, and parallel limits.
- The Tavily-first rule still applies: map/crawl use Tavily tools first, with the fallback chain defined in (C).
- No existing workflow is broken — map/crawl are additive capabilities used only when the agent explicitly decides a site-structure investigation is warranted (e.g., "find all pages on domain X" or "map navigation from URL Y").
- Acceptance: run `tests/agents/test_tavily_tool_parity.py` + the existing deep-research test suite. Zero regressions.

## (F) Concrete Edits Per File

1. **`src/superclaude/agents/deep-research.md`**
   - Add `mcp__tavily__tavily-map` and `mcp__tavily__tavily-crawl` to the `tools:` frontmatter list (lines 6-7, after tavily-extract).
   - Extend "Detecting Tavily unavailable" bullet list to include map/crawl tool absence.
   - Add `fallback_reason` enum values: `map_unavailable`, `crawl_unavailable`.
   - Add routing note for when to use map vs crawl vs extract.

2. **`src/superclaude/agents/deep-research-agent.md`**
   - Add `mcp__tavily__tavily-map` and `mcp__tavily__tavily-crawl` to the `tools:` frontmatter list (after line 7, tavily-extract).
   - Extend "Extraction Routing" table to include map (site-structure discovery) and crawl (deep site traversal).

3. **`src/superclaude/core/RESEARCH_CONFIG.md`**
   - Add `maps=2, crawls=1` to parallel limits (line 34).
   - Add map/crawl to the MCP Integration fallback table if needed.

4. **`src/superclaude/mcp/MCP_Tavily.md`**
   - Add sections for `tavily-map` and `tavily-crawl` capabilities with examples.
   - Extend "Error Handling / Fallback Strategies" with map/crawl fallbacks.

5. **`src/superclaude/modes/MODE_DeepResearch.md`**
   - Add "Enables Tavily map and crawl capabilities" to Integration Points.

6. **`src/superclaude/examples/deep_research_workflows.md`**
   - Add one example workflow showing map+crawl usage (e.g., competitive analysis crawling a competitor's site map).

7. **`tests/agents/test_tavily_tool_parity.py`** — NEW FILE (see section B).

## (G) Acceptance Criteria

| Change | Criterion |
|---|---|
| Frontmatter additions | Both agents list all 4 tavily tools; `make test` passes |
| Parity test | `test_tavily_tool_parity.py` detects a deliberate mismatch and passes when synced |
| Fallback extension | Simulated tavily-map absence triggers `map_unavailable` fallback_reason in report |
| Rate limits | Parallel map=2, crawl=1 enforced; crawl >50 URLs triggers truncation note |
| Backward compat | Existing search/extract workflows unchanged; no test regressions |

## (H) Top Risk

**Crawl result explosion:** tavily-crawl on a large domain can return hundreds of URLs, flooding the context window and exhausting the iteration budget. The truncation cap (50) and single-concurrent-crawl limit mitigate this, but a poorly-scoped query ("crawl the entire web") could still trigger over-fetching. The agent must be instructed to scope crawl to specific subdomains or path prefixes.
