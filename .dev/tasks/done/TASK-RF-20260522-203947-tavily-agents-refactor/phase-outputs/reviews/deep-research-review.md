# Review — deep-research Tavily-first Refactor

**Target file:** `/config/workspace/IronClaude/src/superclaude/agents/deep-research.md`
**Proposal:** `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/deep-research-tavily-refactor.md`
**Reviewed:** 2026-05-22 (Phase 2, Step 2.1)
**Method:** Edit tool applied 5 discrete diff anchors; post-edit file Re-Read end-to-end (62 lines) for verification.

## Acceptance Criteria Checklist

- [x] `tools:` block exists in frontmatter and lists `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` **before** `WebSearch` and `WebFetch`. — **PASS** (lines 5-15: `mcp__tavily__tavily-search` at line 6, `mcp__tavily__tavily-extract` at line 7, `WebSearch` at line 8, `WebFetch` at line 9.)
- [x] Description in frontmatter mentions Tavily-first behavior explicitly. — **PASS** (line 3: "Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.")
- [x] A `## Tool Selection Policy` section exists in the body and names `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` as primary. — **PASS** (line 29 heading; line 32 names both MCP tools as Primary.)
- [x] The four fallback-trigger conditions (tool missing, transport error 2x, rate limit, auth error) are enumerated in the body. — **PASS** (lines 38-41 enumerate all four: tools not present in surface; transport error twice in a row; rate-limit/quota-exceeded; authentication error.)
- [x] Workflow step 3 explicitly references the Tool Selection Policy. — **PASS** (line 51: "Apply the Tool Selection Policy above before issuing any WebSearch/WebFetch call.")
- [x] Report template includes a `backend` column in the sources table. — **PASS** (line 57: "Sources table (URL, title, credibility score, backend [tavily|websearch|webfetch|context7], note)".)
- [x] No body line still lists Tavily and WebFetch as peers without precedence (i.e., the old line 14 wording is gone). — **PASS** (old "(Tavily, WebFetch, Context7, Sequential)" enumeration replaced at line 25 with explicit primary/fallback language; no remaining peer-list violation found in lines 18-62.)
- [ ] `make sync-dev && make verify-sync` succeed after the edit (proves the source-of-truth edit propagated). — **deferred to Phase 3**
- [x] Grep `^- WebSearch$` / `^- WebFetch$` appears in `tools:` AFTER the two `mcp__tavily__*` lines. — **PASS** (yaml indented list: `- mcp__tavily__tavily-search` (line 6), `- mcp__tavily__tavily-extract` (line 7), `- WebSearch` (line 8), `- WebFetch` (line 9). The yaml uses 2-space indent on list items; precedence ordering verified.)

## Edit Inventory (5 anchors, 5 Edit calls)

1. **Frontmatter replacement** (lines 1-5 → lines 1-16): added Tavily-first description suffix + `tools:` allowlist with Tavily MCP first.
2. **Responsibilities bullet** (line 14 → line 25): replaced "Execute searches in parallel using approved tools (Tavily, WebFetch, Context7, Sequential)." with explicit Tavily-primary / WebSearch-fallback prose.
3. **New `## Tool Selection Policy` section** inserted between Responsibilities and Workflow (lines 29-46): Tavily-first rule, four detection triggers, never-silent-fallback clause.
4. **Workflow step 3** (line 21 → line 51): appended Tavily-first + "Apply the Tool Selection Policy above" reference.
5. **Sources table backend column** (line 27 → line 57): added `backend [tavily|websearch|webfetch|context7]` between credibility score and note.

## Anomalies

None. All five anchors found verbatim (matching the freshness report's "apply as-written" determination); no drift, no proposal additions invented, no Bash/sed mutation used. Edit tool only.

**Overall Verdict:** PASS
