# Variant 1 — Architect Lens: /sc:research Command Tavily Alignment (tavily-mcp 0.2.x)

**Scope:** `src/superclaude/commands/research.md` ONLY. The command is a thin orchestration
surface that delegates execution to `deep-research-agent`. Tool-surface decisions (search_depth /
extract_depth routing, map/crawl gating) are owned by cluster C2 (the research engine) and live in
`RESEARCH_CONFIG.md`. The command must **reference** that behavior, never duplicate its tables.

## (a) Frontmatter verdict — NO CHANGE

`mcp-servers: [tavily, sequential, playwright, serena]` is a **server-level** registration. tavily-mcp
0.2.20 adds *tools* (`tavily-map`, `tavily-crawl`) under the **same `tavily` server** — no new server.
playwright/sequential/serena roles are unchanged. Touching this line is scope creep. **Leave as-is.**

## (b) Minimal section edits (2 edits)

### Edit 1 — "### Adaptive Depth" (annotate tiers with search_depth, no new table)

The tiers currently name hops/output only. Add a single trailing clause per tier mapping the engine's
search_depth, so the command's described behavior tracks C2 without restating its routing matrix:

```
- **Quick**: Basic search (search_depth: basic), 1 hop, summary output
- **Standard**: Extended search (search_depth: basic), 2-3 hops, structured report
- **Deep**: Comprehensive search (search_depth: advanced) + site discovery, 3-4 hops, detailed analysis
- **Exhaustive**: Maximum depth (search_depth: advanced) + exhaustive crawl on recall gaps, 5 hops, complete investigation
```

This is the minimal touch that (1) introduces the basic→advanced split per C1 default
(`search_depth: basic`) and (2) names discovery (map) at deep and crawl at exhaustive **as orchestration
intent**, not as a parameter spec. Depth-routing detail stays in the engine.

### Edit 2 — "## MCP Integration" → Tavily line (name the expanded tool set, one line)

Current: `- **Tavily**: Primary search and extraction engine`

Replace with:
```
- **Tavily**: Primary search/extraction engine; deep/exhaustive runs also use site mapping (tavily-map) and gated crawl (tavily-crawl). Routing per RESEARCH_CONFIG.md.
```

The trailing pointer makes the reference-not-duplicate contract explicit and keeps the command thin.

### (Optional, only if reviewer insists) Edit 3 — "### 4. Execute" / Smart extraction

`- **Smart extraction**: Route by content complexity` already correctly abstracts extract_depth
(basic vs advanced by source centrality). **Recommend NO edit** — the existing wording is the thin
surface; spelling out extract_depth here would duplicate C2. Hold the line on scope.

## (c) Are map/crawl named at command level? — YES, minimally

Named once in Adaptive Depth (intent: discovery at deep, crawl at exhaustive) and once in MCP
Integration (the tool list). No gating logic, no recall-failure thresholds, no parameters — those are
C2's. This is the floor that keeps the command honest about the upgraded engine.

## (d) Verification — doc-consistency check (non-contradiction, not duplication)

A lightweight grep-based check that the command's tier names + ordering do not contradict
`RESEARCH_CONFIG.md` Depth Profiles:

```bash
# 1. Both files expose the same four tier tokens, in the same order.
grep -oiE 'quick|standard|deep|exhaustive' \
  src/superclaude/commands/research.md src/superclaude/core/RESEARCH_CONFIG.md
# 2. Engine reserves advanced extraction for deep/exhaustive (comprehensive/all_sources rows);
#    command must NOT claim advanced search at quick/standard.
grep -nE 'Quick|Standard' src/superclaude/commands/research.md | grep -i advanced  # expect: no match
```

Pass = identical tier set, quick/standard show `basic`, deep/exhaustive show `advanced`, and the
command introduces NO numeric source/hop value that disagrees with the engine's profile rows
(command stays qualitative; numbers live in RESEARCH_CONFIG.md).

## Acceptance Criteria

1. Frontmatter `mcp-servers` unchanged.
2. Adaptive Depth tiers carry search_depth annotations: basic (quick/standard), advanced (deep/exhaustive).
3. map named at deep, crawl named at exhaustive — as intent only, zero routing tables.
4. MCP Integration Tavily line lists map+crawl and points to RESEARCH_CONFIG.md.
5. No extract_depth/recall-gate/parameter detail duplicated from C2.
6. Consistency check (d) passes; no tier or numeric contradiction with Depth Profiles.

## Biggest risk

**Scope creep into a second routing table.** The strong pull is to restate C2's search_depth/extract_depth
matrix inside the command so it "reads complete." That duplicates the engine, guarantees future drift
(two sources of truth for one routing decision), and violates the thin-orchestration-surface principle.
Mitigation: every depth/tool mention in the command is a *pointer* ("per RESEARCH_CONFIG.md"), never a spec.
