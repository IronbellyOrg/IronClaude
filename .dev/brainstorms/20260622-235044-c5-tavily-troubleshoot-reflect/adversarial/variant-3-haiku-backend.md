# Variant 3 — Backend: Tavily Inheritance for Troubleshoot + Reflect Tier-2 Search

**Author**: Backend advocate
**Cluster**: C1 — rate-limited Tier-2 targeted search (tavily-mcp 0.2.x)
**Scope**: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` + `src/superclaude/skills/sc-reflect-protocol/SKILL.md` only. No command-file changes needed.

---

## Decision: Rely on Server-Level DEFAULT_PARAMETERS (No Per-Call Overrides)

**C1 sets** `DEFAULT_PARAMETERS = {"search_depth": "basic", "max_results": 10}` at the **tavily-mcp server level**. Every `mcp__tavily__tavily-search` call that does not pass its own `search_depth` or `max_results` **automatically inherits** these values.

**Decision**: Troubleshoot and Reflect should **NOT** pass per-call parameters. They inherit `search_depth: basic` and `max_results: 10` from the server default with zero plumbing.

### Rationale

**1. Current state — zero per-call params already.**
Neither SKILL.md passes `search_depth`, `max_results`, or any other tavily-search parameter today. Both call `mcp__tavily__tavily-search` with query text only:
- Troubleshoot (Wave 3, step 1): `mcp__tavily__tavily-search` for exact error string + "github issue", or `<library> <version> <symptom>` (capped at 2 queries).
- Reflect: Tavily listed as `allowed-tools` and MCP in the integration table; no call-site parameters; fail-open policy on missing MCPs.

**2. The 2-query cap is the dominant cost limiter, not max_results.**
Both skills already enforce `<= 2 queries` for tavily in Tier 2. That is the hard rate-limit boundary. Per-query, `max_results: 10` at `search_depth: basic` is modest — basic depth returns concise snippets, not full-page extractions. The token budget per query is already bounded by the query cap (2 x basic x 10 results = well within the Tier 2 envelope of +15-60k Claude tokens).

**3. Overriding max_results DOWN (e.g., 5) is not justified for triage.**
The argument for `max_results: 5` would be "keep triage cheap." Counter: basic depth results are already short; 10 results at basic depth is roughly equivalent to 5 at advanced depth in token cost. The 2-query cap already prevents runaway spend. Reducing max_results to 5 would increase the probability that a single query returns zero useful hits, which in a 2-query-budget environment means wasted queries and potentially missing the signal entirely. The cost of a missed hit (escalation to manual research or a degraded report) exceeds the marginal token savings of 5 fewer results.

**4. DRY: do not duplicate DEFAULT_PARAMETERS here.**
The server-level default is the single source of truth. Per-call overrides in the skill files would create a second copy of the same values, which must be kept in sync when the server default changes. If a future tuning calls for different defaults (e.g., `max_results: 5` globally), it is one change in the server config, not N changes across every skill that calls tavily.

**5. Override-if-needed escape hatch.**
If a specific call pattern genuinely needs different params (e.g., a future `search_depth: advanced` for map/crawl — which is deep-research-only and not in scope for this cluster), the call-site should override then. For now, the inheritance path covers both skills.

---

## Changes to Make

### 1. sc-troubleshoot-protocol/SKILL.md — Document the inheritance

**Location**: Wave 3, step 1 (MCP enrichment section, around line 335).

**Add a brief annotation** next to the existing tavily-search bullet:

> `mcp__tavily__tavily-search` — inherits `search_depth: basic` / `max_results: 10` from server-level DEFAULT_PARAMETERS (C1). No per-call params needed. Rate-limited: at most 2 queries in this wave.

No structural change to the call shape — query text only, as today.

### 2. sc-reflect-protocol/SKILL.md — Document the inheritance

**Location**: The MCP integration section (line ~1689 area, "Fail-open on missing MCPs") or the allowed-tools annotation.

**Add a brief note** in the MCP usage section (where tavily is mentioned in the Will/Won't or integration area):

> `mcp__tavily__tavily-search` (Tier 2, rare — when external symptom lookup is needed beyond auggie/serena grounding) — inherits `search_depth: basic` / `max_results: 10` from server-level DEFAULT_PARAMETERS (C1). Fail-open on missing MCP per existing policy.

This is primarily a documentation pass: reflect uses tavily far less than troubleshoot (it is an audit tool, not a debugging tool), but the inheritance principle applies identically.

### 3. No command-file changes

`troubleshoot.md` and `reflect.md` already describe tavily at the conceptual level ("Tier 2 only, rate-limited, used for external lookups"). They do not mention per-call parameters, and they should not — the server-level default is invisible to the command surface.

---

## Verification (d)

1. **Assert no per-call param duplication**: `grep -r 'search_depth\|max_results' src/superclaude/skills/sc-troubleshoot-protocol/ src/superclaude/skills/sc-reflect-protocol/` should return **only** the new inheritance annotation lines (containing "inherits" or "server-level"), not call-site parameter assignments (no `search_depth=` or `max_results=` as invocation arguments).

2. **Assert tavily-search calls remain query-only**: `grep 'mcp__tavily__tavily-search'` in both SKILL.md files should show the tool name referenced in prose/bullet form, not with parameter overrides.

3. **DEFAULT_PARAMETERS documented once**: The server-level default lives in the C1 cluster config (not in this repo). The two SKILL.md files reference it by name ("server-level DEFAULT_PARAMETERS") without restating the values as if they were local config.

---

## Acceptance Criteria

- [ ] Both SKILL.md files contain exactly one sentence documenting that tavily-search inherits server-level DEFAULT_PARAMETERS.
- [ ] No per-call parameter overrides (`search_depth`, `max_results`, etc.) are added to any tavily-search call in either skill.
- [ ] The 2-query rate limit for troubleshoot remains unchanged (already documented).
- [ ] Reflect's fail-open-on-missing-MCPs policy remains unchanged.
- [ ] `make lint` passes on both files.
- [ ] `make verify-sync` passes after `make sync-dev`.

---

## Biggest Risk

**Server default changes silently alter behavior downstream.** If C1's DEFAULT_PARAMETERS are tuned (e.g., `max_results` bumped to 20, or `search_depth` changed to `advanced`), every inheriting call picks up the change without any local diff. Mitigation: the inheritance annotation in each SKILL.md names the source ("server-level DEFAULT_PARAMETERS (C1)") so an operator reading the skill knows where to look for the actual values. If future policy requires pinning per-skill, the annotation marks the exact call site to override.
