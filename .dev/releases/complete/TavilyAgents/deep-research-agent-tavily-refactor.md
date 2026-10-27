# Refactor: deep-research-agent → Tavily-first

Source file: `/config/workspace/IronClaude/src/superclaude/agents/deep-research-agent.md`

## Current state

The `deep-research-agent` is the `/sc:research` command's underlying specialist for comprehensive research with adaptive strategies. It is heavily web-oriented.

**Frontmatter** (lines 1-5): minimal — `name`, `description`, `category` only. **No `tools:` allowlist** — agent inherits default tool surface.

**Workflow references to web tools**:
- Line 98 (Tool Orchestration → Search Strategy step 1): "Broad initial searches (Tavily)"
- Line 99: "Identify key sources"
- Line 100: "Deep extraction as needed"
- Line 101: "Follow interesting leads"
- Line 104 (Extraction Routing): "Static HTML → Tavily extraction"
- Line 105: "JavaScript content → Playwright"
- Line 106: "Technical docs → Context7"
- Line 107: "Local context → Native tools"

**Observations**:
- Tavily is mentioned in two places (`Search Strategy` step 1 and `Extraction Routing` for static HTML), implying it IS preferred — but the language is descriptive ("Broad initial searches (Tavily)"), not prescriptive (no "must use Tavily first"). An LLM reading "approved tools" or seeing WebSearch in its default tool surface could still pick WebSearch.
- No explicit fallback rule. No detection of "Tavily unavailable."
- No mention of WebSearch / WebFetch at all in the body — yet those are available by default and the agent could silently use them.
- No `tools:` allowlist means no machine-readable contract about which tools are required vs fallback.
- The "Extraction Routing" matrix uses "Tavily extraction" without naming `mcp__tavily__tavily-extract`.

**Verdict**: In scope — web search/extraction is central to the agent's mission and is the area most at risk for non-Tavily drift.

## Proposed refactor

### Frontmatter changes

**Before** (lines 1-5):
```yaml
---
name: deep-research-agent
description: Specialist for comprehensive research with adaptive strategies and intelligent exploration
category: analysis
---
```

**After**:
```yaml
---
name: deep-research-agent
description: Specialist for comprehensive research with adaptive strategies and intelligent exploration. Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
category: analysis
tools:
  - mcp__tavily__tavily-search
  - mcp__tavily__tavily-extract
  - WebSearch
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_evaluate
  - mcp__sequential-thinking__sequentialthinking
  - Read
  - Grep
  - Glob
---
```

Rationale: Tavily MCP tools listed first; WebSearch/WebFetch retained only as documented fallbacks. Playwright retained for JS-rendered content per existing Extraction Routing matrix. Context7 retained for library docs. Sequential retained for multi-step synthesis.

### Body changes

**Replace the `### Tool Orchestration` block** (lines 95-114 area). Specifically:

Before:
```markdown
### Tool Orchestration

**Search Strategy**
1. Broad initial searches (Tavily)
2. Identify key sources
3. Deep extraction as needed
4. Follow interesting leads

**Extraction Routing**
- Static HTML → Tavily extraction
- JavaScript content → Playwright
- Technical docs → Context7
- Local context → Native tools

**Parallel Optimization**
- Batch similar searches
- Concurrent extractions
- Distributed analysis
- Never sequential without reason
```

After:
```markdown
### Tool Orchestration

**Tavily-First Rule (mandatory)**

All web search and HTML extraction MUST be attempted via Tavily MCP first:
- Search → `mcp__tavily__tavily-search`
- Page extraction → `mcp__tavily__tavily-extract`

`WebSearch` and `WebFetch` are **fallback tools only**. They are used solely when Tavily MCP is unavailable (see Fallback Policy below). Do not invoke `WebSearch` or `WebFetch` while Tavily MCP is operational.

**Search Strategy**
1. Broad initial searches via `mcp__tavily__tavily-search` (Tavily MCP)
2. Identify key sources
3. Deep extraction via `mcp__tavily__tavily-extract` as needed
4. Follow interesting leads (re-issuing Tavily searches with refined queries)

**Extraction Routing**
- Static HTML → `mcp__tavily__tavily-extract` (Tavily MCP, primary)
- JavaScript-rendered content → Playwright (`mcp__playwright__*`) — independent axis, not subject to Tavily-first
- Technical / official library docs → Context7 (`mcp__context7__*`) — independent axis, not subject to Tavily-first
- Local context → Native tools (Read/Grep/Glob)
- Tavily MCP unavailable → `WebSearch` (search) / `WebFetch` (single-URL fetch) — fallback only

**Fallback Policy — when to fall back to WebSearch/WebFetch**

Treat Tavily MCP as unavailable, and fall back, when **any** of the following holds:
1. `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` are not present in the available tool surface for the session (not loaded / not configured).
2. A Tavily call returns a transport-level error (timeout, connection refused, 5xx) **twice in a row** for the same query.
3. A Tavily call returns an explicit rate-limit / quota-exceeded error.
4. A Tavily call returns an authentication error (missing/invalid API key).

Always record the backend used per source. If fallback occurred, label the source with `backend: websearch` or `backend: webfetch` and add a `fallback_reason` field (`tavily_missing | tavily_error | tavily_rate_limit | tavily_auth`). Never fall back silently.

**Parallel Optimization**
- Batch similar Tavily searches concurrently
- Concurrent Tavily extractions
- Distributed analysis
- Never sequential without reason
```

**Update the Citation Requirements block** (around line 90-93):

Before:
```markdown
**Citation Requirements**
- Provide sources when available
- Use inline citations for clarity
- Note when information is uncertain
```

After:
```markdown
**Citation Requirements**
- Provide sources when available
- Use inline citations for clarity
- Note when information is uncertain
- Tag each source with the backend used: `tavily`, `websearch`, `webfetch`, `playwright`, `context7`
- If a `websearch` or `webfetch` source appears, include `fallback_reason` per the Fallback Policy
```

## Acceptance criteria

- [ ] `tools:` block exists in frontmatter; `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` are listed **before** `WebSearch` and `WebFetch`.
- [ ] Description in frontmatter mentions Tavily-first behavior explicitly.
- [ ] `### Tool Orchestration` contains a `**Tavily-First Rule (mandatory)**` subsection naming both `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract`.
- [ ] `### Tool Orchestration` contains a `**Fallback Policy**` subsection enumerating the four fallback-trigger conditions (tool missing, transport error 2x, rate limit, auth error).
- [ ] `Extraction Routing` includes a "Tavily MCP unavailable → WebSearch / WebFetch — fallback only" line.
- [ ] `Citation Requirements` requires per-source `backend` tagging and `fallback_reason` on fallback sources.
- [ ] No body line still describes Tavily without naming the actual MCP tool IDs (the old "(Tavily)" wording in step 1 is replaced with `mcp__tavily__tavily-search`).
- [ ] Playwright and Context7 are explicitly marked as "independent axis, not subject to Tavily-first" so they aren't accidentally degraded.
- [ ] `make sync-dev && make verify-sync` succeed after the edit.

## Reflection notes

Reflection pass against original intent:

- **Preserves responsibilities?** Yes. All four phases (Discovery / Investigation / Synthesis / Reporting), all four planning strategies, all multi-hop reasoning patterns, self-reflective mechanisms, evidence management, learning integration, quality standards, performance optimization, and boundaries are untouched. Only Tool Orchestration is rewritten.
- **Actually enforces Tavily-first?** The original already implied Tavily preference but used parenthetical / descriptive phrasing ("Broad initial searches (Tavily)") which is too easy for an LLM to override under context pressure. Tightened: the new "Tavily-First Rule (mandatory)" subsection uses MUST language and names the exact MCP tool IDs, and the Extraction Routing matrix names `mcp__tavily__tavily-extract` explicitly. The frontmatter `tools:` ordering reinforces it at the contract level.
- **Fallback unambiguous?** Initial draft just said "when Tavily fails." Tightened to the same four-condition list as the deep-research refactor for cross-agent consistency, including the "twice in a row" qualifier for transient errors and a separate auth-error case.
- **Risk of over-constraining Playwright / Context7?** Yes — initial draft put Playwright and Context7 in the same fallback flow as WebSearch, which would degrade JS-content and library-docs paths. Tightened: both are now explicitly labeled "independent axis, not subject to Tavily-first" so the agent keeps using them for their original purposes (JS rendering, official library docs) without confusion.
- **Observability?** Original agent had no per-source backend tagging. Tightened: Citation Requirements now mandates `backend` tagging per source and `fallback_reason` whenever a non-Tavily web tool is used. This makes the Tavily-first rule auditable from the report alone.
- **Parallel Optimization preserved?** Original said "Batch similar searches / Concurrent extractions." Tightened to "Batch similar Tavily searches concurrently / Concurrent Tavily extractions" so parallelism explicitly applies to Tavily MCP calls (which is where most operations happen).
- **Cross-agent consistency**: The fallback policy here is intentionally identical to the `deep-research` agent refactor. Both agents now share the same four-condition contract, which makes downstream auditing simpler and avoids ambiguity if both agents are active in the same session.
