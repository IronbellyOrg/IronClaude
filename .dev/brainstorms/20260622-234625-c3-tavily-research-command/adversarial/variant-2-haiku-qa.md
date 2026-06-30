# QA Spec — /sc:research Tavily Alignment (C3)

**Role**: QA advocate · **Lens**: consistency, non-duplication, anti-drift.

---

## 1. Frontmatter Verdict

**No change.** `mcp-servers: [tavily, ...]` declares the MCP _server_, not individual tools. The Tavily server persists; only its tool surface grew (tavily-map, tavily-crawl). Frontmatter stays as-is.

## 2. Minimal-Edit Recommendation: Generic Over Duplicate

The command's job is to **route the user to the engine**, not re-specify it. Two spots risk drift with C2:

### A. "MCP Integration" — Tavily line (line 95)

**Current**: `**Tavily**: Primary search and extraction engine`
**Risk**: C2 adds map + crawl. Extending the label ("search, extraction, mapping, and crawl") makes this command file a **second source of truth** for Tavily capabilities that will go stale on the next MCP bump.
**Recommendation**: Make it generic and **point to the engine** as the authority:

```
- **Tavily**: Primary research engine (search, extract, map, crawl — see deep-research-agent for tool orchestration)
```

This is a one-line, future-proof annotation. It acknowledges the expanded surface without listing parameters that live elsewhere.

### B. "Adaptive Depth" section (lines 88-91)

**Current** ties `quick|standard|deep|exhaustive` to hop counts ("1 hop", "2-3 hops", etc.). C2's `depth_profile` maps these to `search_depth` and `extract_depth` values, plus tool selection (map for deep/exhaustive, crawl for exhaustive single-domain).

**Recommendation**: **Do NOT duplicate C2's depth table.** Instead, add a single reference sentence after the four bullet items:

```
> Depth profiles map to Tavily tool selection and extraction parameters. The engine
> (deep-research-agent) selects search_depth, extract_depth, map, and crawl per profile.
```

This prevents a second truth source while making the relationship explicit.

### What to Leave Alone

- Examples section: CLI flags (`--depth`) are user-facing; no tool-level detail needed.
- Boundaries: unchanged; Tavily expansion doesn't alter what research "will/won't" do.
- Execute/Smart extraction bullet lines: already generic ("Route by content complexity") — good as-is.

## 3. Should Map/Crawl Be Named Here?

**Barely.** Mention the words once in the MCP Integration line (see 2A) so a reader searching for "map" or "crawl" in this file finds the pointer to the engine. Do **not** describe their semantics (discovery scope, single-domain, etc.) — that is C2 territory.

## 4. Anti-Duplication Consistency Test

Design a lightweight CI or pre-commit test that catches `research.md` vs engine-config contradictions:

```
test_research_command_vs_engine_consistency():
  1. Parse src/superclaude/commands/research.md for:
     - MCP Integration tool descriptions (what Tavily "is" / "does")
     - Adaptive Depth profile names (quick/standard/deep/exhaustive)
     - Depth profile parameter claims (hop counts, search_depth, extract_depth, tool names)
  2. Parse the engine source of truth (deep-research-agent.md + RESEARCH_CONFIG.md or
     the C2 merged-requirements.md) for:
     - Tavily tool list (tavily-search, tavily-extract, tavily-map, tavily-crawl)
     - depth_profile → parameter mapping
  3. Assert:
     a. Every depth profile name in research.md exists in the engine config (no phantom profiles).
     b. No parameter values in research.md contradict engine config values.
     c. The Tavily description contains NO parameterized claims (search_depth values, max_results,
        extract_depth levels) — those belong only in the engine doc. A regex guard:
        research.md must NOT contain "search_depth" | "extract_depth" | "max_results" | "tavily-map"
        followed by a concrete value assignment; only a generic pointer to the engine is permitted.
  4. Fail with: "research.md drifts from engine config at <claim> — update the engine doc,
     then generalize research.md to reference it."
```

This test is **asymmetric**: it allows research.md to be generic/pointing, but forbids concrete parameter claims that could contradict the engine. It catches the exact failure mode this spec guards against.

## 5. Biggest Risk

**Over-editing**: The most likely mistake is expanding research.md into a parallel spec (duplicating C2's depth table, tool defaults, parameter values). Every extra concrete value is a future contradiction. The discipline is: **one generic pointer per section, zero duplicated parameters**.

## 6. Acceptance Criteria

1. Frontmatter unchanged.
2. MCP Integration Tavily line: generic pointer to deep-research-agent, mentions map/crawl by name once.
3. Adaptive Depth section: reference sentence added, zero parameter duplication.
4. No other sections touched.
5. The consistency test design is documented (above, section 4) and implementable as a Python pytest in the repo's test suite.
