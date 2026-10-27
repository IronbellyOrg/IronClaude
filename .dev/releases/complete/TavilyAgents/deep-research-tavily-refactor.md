# Refactor: deep-research → Tavily-first

Source file: `/config/workspace/IronClaude/src/superclaude/agents/deep-research.md`

## Current state

The `deep-research` agent is an adaptive research specialist for external knowledge gathering. It explicitly performs web operations.

**Frontmatter** (lines 1-5): minimal — has `name`, `description`, `category` only. **No `tools:` declaration**, so the agent inherits the default tool surface from Claude Code (which includes WebSearch and WebFetch but does not guarantee Tavily MCP tools).

**Workflow references to web tools**:
- Line 14 (Responsibilities): "Execute searches in parallel using approved tools (Tavily, WebFetch, Context7, Sequential)."
- Line 21 (Workflow step 3): "Execute — run searches, capture key facts, and highlight contradictions or gaps."
- Line 22 (Workflow step 4): "Validate — cross-check claims, verify official documentation, and flag remaining uncertainty."

**Observations**:
- Tavily is mentioned but listed in a flat enumeration alongside WebFetch — no precedence rule.
- No explicit MCP tool names (`mcp__tavily__tavily-search`, `mcp__tavily__tavily-extract`) — the agent has no contract that Tavily MCP is actually available.
- No fallback condition defined; agent could silently pick WebFetch first.
- No `tools:` allowlist means the agent cannot signal which tools are intended/required.

**Verdict**: In scope — web search/fetch is core to the agent's mission.

## Proposed refactor

### Frontmatter changes

Add a `tools:` allowlist that puts Tavily MCP tools first and keeps WebSearch/WebFetch only as fallback.

**Before** (lines 1-5):
```yaml
---
name: deep-research
description: Adaptive research specialist for external knowledge gathering
category: analysis
---
```

**After**:
```yaml
---
name: deep-research
description: Adaptive research specialist for external knowledge gathering. Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
category: analysis
tools:
  - mcp__tavily__tavily-search
  - mcp__tavily__tavily-extract
  - WebSearch
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - Read
  - Grep
  - Glob
  - mcp__sequential-thinking__sequentialthinking
---
```

Rationale: Tavily MCP tools listed first signals primary preference; WebSearch/WebFetch retained only as documented fallbacks; Context7 retained for library docs; Sequential retained for multi-step reasoning.

### Body changes

**Replace line 14** (Responsibilities bullet):

Before:
```
- Execute searches in parallel using approved tools (Tavily, WebFetch, Context7, Sequential).
```

After:
```
- Execute web searches using Tavily MCP (`mcp__tavily__tavily-search`) as the primary tool. Use `mcp__tavily__tavily-extract` for page content extraction. Only fall back to WebSearch / WebFetch when Tavily MCP is unavailable (see Fallback Policy below). Use Context7 for official library/framework docs and Sequential for multi-step synthesis.
```

**Insert a new `## Tool Selection Policy` section between current Responsibilities and Workflow**:

```markdown
## Tool Selection Policy

### Tavily-first rule (web search / extraction)
1. **Primary**: `mcp__tavily__tavily-search` for all web search queries; `mcp__tavily__tavily-extract` for fetching specific URLs / page content.
2. **Fallback**: `WebSearch` (search) and `WebFetch` (single-URL fetch) are used **only** when Tavily MCP is unavailable.
3. **Library docs**: `mcp__context7__*` remains primary for library/framework/SDK documentation (not subject to the Tavily-first rule — Context7 is a separate axis).

### Detecting "Tavily unavailable"
Treat Tavily MCP as unavailable, and fall back to WebSearch/WebFetch, when **any** of the following holds:
- The `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` tools are not present in the available tool surface for this session (not loaded / not configured).
- A Tavily call returns a transport-level error (timeout, connection refused, 5xx) **twice in a row** for the same query.
- A Tavily call returns an explicit rate-limit / quota-exceeded error.
- A Tavily call returns an authentication error (missing/invalid API key).

In every fallback event, record in the source citation table: `fallback_reason: <tavily_missing | tavily_error | tavily_rate_limit | tavily_auth>`.

### Never silent fallback
Always state in the report which search backend was used per source. If fallback occurred, note it in the "Open questions / suggested follow-up" section so the operator knows Tavily was not exercised.
```

**Update Workflow step 3** (line 21):

Before:
```
3. **Execute** — run searches, capture key facts, and highlight contradictions or gaps.
```

After:
```
3. **Execute** — run searches via Tavily MCP first (parallel where possible), capture key facts, and highlight contradictions or gaps. Apply the Tool Selection Policy above before issuing any WebSearch/WebFetch call.
```

**Extend the Report block** (lines 24-28) so the sources table includes a `backend` column:

Before:
```
🔗 Sources table (URL, title, credibility score, note)
```

After:
```
🔗 Sources table (URL, title, credibility score, backend [tavily|websearch|webfetch|context7], note)
```

## Acceptance criteria

A reviewer or task-builder should verify the following after the refactor lands:

- [ ] `tools:` block exists in frontmatter and lists `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` **before** `WebSearch` and `WebFetch`.
- [ ] Description in frontmatter mentions Tavily-first behavior explicitly.
- [ ] A `## Tool Selection Policy` section exists in the body and names `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` as primary.
- [ ] The four fallback-trigger conditions (tool missing, transport error 2x, rate limit, auth error) are enumerated in the body.
- [ ] Workflow step 3 explicitly references the Tool Selection Policy.
- [ ] Report template includes a `backend` column in the sources table.
- [ ] No body line still lists Tavily and WebFetch as peers without precedence (i.e., the old line 14 wording is gone).
- [ ] `make sync-dev && make verify-sync` succeed after the edit (proves the source-of-truth edit propagated).
- [ ] Grep `^- WebSearch$` / `^- WebFetch$` appears in `tools:` AFTER the two `mcp__tavily__*` lines.

## Reflection notes

Reflection pass against original intent:

- **Preserves responsibilities?** Yes. The agent still does adaptive research, source tracking, synthesis, and the same Understand→Plan→Execute→Validate→Report workflow. Only the tool selection step is constrained.
- **Actually enforces Tavily-first?** The frontmatter `tools:` ordering is a soft signal, not a hard enforcement. The hard enforcement comes from the body's "Tool Selection Policy" section — that's the prose the agent reads at run time. Tightened: the policy now says "Apply the Tool Selection Policy above before issuing any WebSearch/WebFetch call" inside Workflow step 3, so the rule is invoked at the moment of execution rather than only at the responsibilities level.
- **Fallback unambiguous?** Initial draft only said "unavailable" — too vague. Tightened to four concrete trigger conditions, and added the "twice in a row" qualifier for transient errors so a single blip doesn't cause an unnecessary fallback. Auth-error case added separately because it's permanent, not transient.
- **Observability?** Initial draft didn't require reporting the backend used. Tightened: sources table now has a `backend` column, and `fallback_reason` is required in citations when a fallback occurred. This makes Tavily-first auditable from the report itself.
- **Gap considered then rejected**: We considered making the agent retry Tavily after a backoff before falling back. Rejected for this refactor — single retry is implicit in "twice in a row" check; longer backoff belongs in Tavily MCP server config, not in the agent prose.
- **Context7 handling**: Initial draft conflated Context7 with the Tavily-first rule. Tightened: Context7 is explicitly noted as a separate axis (library docs), unaffected by the Tavily/WebSearch precedence, so the agent doesn't degrade Context7 usage for library lookups.
