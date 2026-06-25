# Deep Research Configuration

## Default Settings

```yaml
research_defaults:
  planning_strategy: unified
  max_hops: 5
  confidence_threshold: 0.7
  memory_enabled: true
  parallelization: true
  parallel_first: true  # MANDATORY DEFAULT
  sequential_override_requires_justification: true  # NEW
  
# Parallel: See RULES.md §Planning Efficiency. Default PARALLEL. Batch: searches=5, extractions=3, analyses=2.

planning_strategies:
  planning_only: {clarification: false, execution: immediate}
  intent_planning: {clarification: true, max_questions: 3, execution: after_clarification}
  unified: {clarification: optional, plan_presentation: true, execution: after_confirmation}

hop_configuration: {max_depth: 5, timeout: 60s, parallel: true, loop_detection: true}
confidence_scoring: {relevance: 0.5, completeness: 0.5, min: 0.6, target: 0.8}
self_reflection: {frequency: after_each_hop, triggers: [low_confidence, contradictions, 80%_time, user_intervention]}
memory: {case_reasoning: true, pattern_learning: true, session_persistence: true, retention: 30d}
tools: {discovery: tavily, routing: smart, reasoning: sequential, memory: serena, parallel: true}
quality_gates: {planning: [objectives, strategy, criteria], execution: min_confidence=0.6, synthesis: coherence+clarity}
extraction: {strategy: selective, screenshots: contextual, js_rendering: auto, timeout: 15s}
```

## Performance

**Caching**: Tavily 1h, Playwright 24h, Sequential 1h, case patterns always.
**Parallel limits**: searches=5, extractions=3, analysis=2.
**Resource limits**: 10min/research, 10 iterations, 5 hops, 100MB/session.

## Strategy Selection

| Strategy | Indicators |
|----------|-----------|
| planning_only | Clear query, technical docs, well-defined scope |
| intent_planning | Ambiguous terms, broad topic, multiple interpretations |
| unified | Complex multi-faceted, collaboration beneficial, high-stakes |

## Source Credibility Matrix

| Tier | Score | Source Types |
|------|-------|-------------|
| T1 | 0.9-1.0 | Academic journals, government pubs, official docs, peer-reviewed |
| T2 | 0.7-0.9 | Established media, industry reports, expert blogs, tech forums |
| T3 | 0.5-0.7 | Community resources, user docs, verified social, Wikipedia |
| T4 | 0.3-0.5 | User forums, unverified social, personal blogs, comments |

**Domain filters:** Bind Tavily's `include_domains` / `exclude_domains` to the tiers above —
use `include_domains` to bias `search` / `map` / `crawl` toward T1–T2 sources (academic,
official docs, established media) and `exclude_domains` to suppress T4 sources (unverified
social, comment threads).

## Depth Profiles

Tavily MCP version: **0.2.20** (pinned — see the `install_mcp.py` registry and `MCP_Tavily.md`).
The server-level `DEFAULT_PARAMETERS` baseline is injected at install (canonical values live in
`install_mcp.py` / `MCP_Tavily.md` — not duplicated here). Each profile below overrides
`search_depth` / `extract_depth` per tier; per-call tool args override the server default.

| Profile | Sources | Hops | Iterations | Time | Confidence | search_depth | extract_depth | Tools enabled |
|---------|---------|------|------------|------|------------|--------------|---------------|---------------|
| quick | 10 | 1 | 1 | 2min | 0.6 | basic | basic | search |
| standard | 20 | 3 | 2 | 5min | 0.7 | basic | basic | search, extract |
| deep | 40 | 4 | 3 | 8min | 0.8 | advanced | advanced | search, extract, map |
| exhaustive | 50+ | 5 | 5 | 10min | 0.9 | advanced | advanced | search, extract, map, crawl |

`search_depth: advanced` is used ONLY at the **deep** and **exhaustive** tiers; quick and
standard stay `basic`. `tavily-map` is enabled at **deep and above**; `tavily-crawl` is enabled
at the **exhaustive tier only**.

**Discovery caps:** `maps=2` per research run, `crawls=1` per research run; a `tavily-crawl`
result set is truncated to a maximum of **50 URLs**.

## Multi-Hop Patterns

| Pattern | Description | Example | Limit |
|---------|-------------|---------|-------|
| entity_expansion | Explore found entities | Paper → Authors → Works → Collaborators | 3 branches |
| concept_deepening | Drill into concepts | Topic → Subtopics → Details → Examples | depth 4 |
| temporal_progression | Follow chronology | Current → Recent → Historical → Origins | backward |
| causal_chain | Trace cause/effect | Effect → Immediate → Root → Prevention | validated |

## Discovery Routing

| Operation | Tavily tool id | Use | Enabled at |
|-----------|----------------|-----|-----------|
| map | `mcp__tavily__tavily-map` | Site-structure discovery — enumerate a site's URL graph before targeted extraction | deep+ (cap `maps=2`) |
| crawl | `mcp__tavily__tavily-crawl` | Deep domain traversal — follow links across a domain to gather many pages | exhaustive only (cap `crawls=1`, ≤50 URLs) |

Typical flow: `map` a domain to surface candidate URLs, then `extract` the high-value ones;
escalate to `crawl` only at the **exhaustive** tier when broad coverage across a domain is
required. Respect the caps (`maps=2`, `crawls=1`) and the 50-URL crawl truncation.

## Recency Controls

| Param | Use |
|-------|-----|
| `topic: news` | Switch search to the news index for current-events queries (default is `topic: general`) |
| `time_range` | Bound results to a recent window (day / week / month / year) |
| `days` | With `topic: news`, limit results to the last N days |

Apply recency controls only when the query is time-sensitive.

## Extraction Routing

| Tool | Conditions |
|------|-----------|
| tavily | Static HTML, simple articles, public access |
| playwright | JS rendering, dynamic content, auth needed, screenshots |
| context7 | Tech docs, API refs, framework guides |
| native | Local files, simple explanations, code gen |

## Replanning Thresholds

- **Confidence**: critical <0.4, low <0.6, acceptable 0.6-0.7, good >0.7
- **Time**: warning 70%, critical 90% of limit
- **Quality**: sources <3, contradictions >30%, gaps >50%

## Output Formats

- **summary**: 500 words, [key_finding, evidence, sources], simple confidence
- **report**: [exec_summary, methodology, findings, synthesis, conclusions], inline citations
- **academic**: [abstract, intro, methodology, lit_review, findings, discussion, conclusions], academic citations

## Error Handling

See MCP.md §Error Handling & Circuit Breaker for server fallbacks. Research-specific: low_confidence → replan, contradictions → more sources, insufficient_data → expand scope.

## MCP Integration

| Server | Role | Fallback |
|--------|------|----------|
| tavily | primary search | native websearch |
| playwright | complex extraction | tavily extraction |
| sequential | reasoning engine | native reasoning |
| context7 | technical docs | tavily search |
| serena | memory management | session only |
