# Variant 2 — Analyzer Spec: Tavily MCP 0.2.x Research Methodology Upgrade

## Position

Upgrade the deep-research engine to tavily-mcp 0.2.20, but treat the new surface as methodology controls, not automatic quality gains. Preserve the cross-cluster pin: version `0.2.20`; default parameters `{"search_depth":"basic","max_results":10}`; allow the research engine to override `search_depth:"advanced"` only for deep/exhaustive or explicit gap-recovery scenarios.

## Methodology Rules

### 1. Search depth must be earned

`search_depth:"basic"` remains the default for quick, standard, planning-only, and first-pass discovery. It is the honest baseline: lower quota burn, less result sprawl, and enough signal for clear or narrow questions.

Use `search_depth:"advanced"` only when one of these conditions is true:

- Depth profile is `deep` or `exhaustive` and the plan requires multi-hop evidence chains.
- Self-reflection finds confidence below target after a basic pass: below `0.8` for deep, below `0.9` for exhaustive, or below the user-specified threshold.
- Replanning triggers fire: contradiction rate over 30%, gaps over 50%, or insufficient high-tier sources.
- The question requires source diversity across domains, time periods, or stakeholder perspectives.

Do not use advanced search just because it exists. It does not improve quality for single-fact lookup, official-doc questions better served by Context7, or already-saturated source sets.

### 2. Tavily parameters map to evidence quality

Add an explicit parameter-to-methodology table:

| Parameter | Methodology use | Quality guardrail |
|---|---|---|
| `topic:"news"` | Current events, active market shifts, policy/regulatory changes, release/news tracking | Require `time_range` or `days`; do not use for stable background facts |
| `topic:"general"` | Default research, technical docs discovery, evergreen analysis | Prefer unless recency is part of the question |
| `time_range` | Recency window for non-news research (`day`, `week`, `month`, `year`) | Record window in methodology; widen only if evidence is sparse |
| `days` | Precise news-window control | Use for event timelines; avoid for evergreen subjects |
| `include_domains` | Credibility targeting: T1 official/academic/government; T2 established media/industry reports | Never use so narrowly that it hides dissenting evidence |
| `exclude_domains` | Filter low-value mirrors, spam, repeated syndication, known irrelevant domains | Do not exclude merely because a source contradicts the hypothesis |
| `include_raw_content` | Quick extraction from search results when snippets are insufficient | Use selectively; prefer `tavily-extract` for cited source text |
| `include_images` | Visual evidence discovery for UI/market/diagram-heavy research | Images support, not replace, textual claims |
| `max_results` | Breadth control; default 10 | Raise only for deep/exhaustive coverage or explicit source-diversity needs |

### 3. Extraction depth follows the depth profile

`extract_depth:"basic"` is the default for quick and standard profiles, simple articles, press releases, static documentation pages, and source triage.

`extract_depth:"advanced"` is reserved for deep/exhaustive profiles when the source is central to a claim, has dense or nested content, contains tables/long reports, or a contradiction must be resolved from primary text. Advanced extraction is not a substitute for source selection; low-credibility pages remain low-credibility even when deeply extracted.

### 4. Crawl and map are completeness tools, not synthesis inputs

Add `tavily-map` and `tavily-crawl` to the Tavily capability model, but gate them tightly:

- `tavily-map`: use to inventory official docs, product documentation, research portals, or source collections before choosing extraction targets.
- `tavily-crawl`: use only for exhaustive profile, bounded official domains, or when completeness matters more than speed.
- Always convert crawl/map output into a curated extraction queue. Do not dump crawl output directly into synthesis.
- Pollution guard: crawl/map results must be deduplicated, tier-scored, and relevance-filtered before they can count toward confidence or completeness.

## Concrete File Edits

### `src/superclaude/agents/deep-research.md`

- Add `mcp__tavily__tavily-map` and `mcp__tavily__tavily-crawl` to the tool list when available.
- Replace the generic Tavily-first bullet with a 0.2.x policy: search defaults to `search_depth:basic,max_results:10`; deep/exhaustive may escalate to advanced after confidence/gap checks.
- Add source table fields: `search_depth`, `extract_depth`, `topic`, `time_window`, `domain_filter`, `backend`, `fallback_reason`.

### `src/superclaude/agents/deep-research-agent.md`

- Extend Tool Orchestration with Search Parameter Selection, Extraction Depth Selection, and Crawl/Map Gating subsections.
- In Self-Reflective Mechanisms, make advanced search a replanning action, not an initial reflex.
- In Evidence Management, require every cited claim to trace to a selected source, not raw crawl bulk.

### `src/superclaude/core/RESEARCH_CONFIG.md`

- Add Tavily config defaults:
  - `version: 0.2.20`
  - `default_parameters: {search_depth: basic, max_results: 10}`
  - `advanced_allowed_for: [deep, exhaustive, replanning_gap_recovery]`
- Expand Depth Profiles:

| Profile | search_depth | extract_depth | Tool set |
|---|---|---|---|
| quick | basic | basic | search + selective extract |
| standard | basic | basic, advanced only for central sources | search + extract |
| deep | basic first, advanced after plan/gap trigger | advanced for central sources | search + extract + optional map |
| exhaustive | advanced allowed after scoped plan | advanced | search + extract + map; crawl only on bounded domains |

- Add the parameter-to-methodology table above under Source Credibility Matrix or a new Tavily Methodology section.

### `src/superclaude/mcp/MCP_Tavily.md`

- Update server surface to tavily-mcp 0.2.20: `tavily-search`, `tavily-extract`, `tavily-map`, `tavily-crawl`, `DEFAULT_PARAMETERS`.
- Replace informal Search Patterns with exact supported parameters and quality intent.
- Add a “Not Quality-Improving By Default” warning for advanced search, raw content, images, crawl, and broad `max_results`.

### `src/superclaude/modes/MODE_DeepResearch.md`

- Add methodology behavior: choose concrete `search_depth`, `extract_depth`, and tool set during planning; record recency and domain filters in the methodology.
- Add skepticism rule: more results are not more evidence unless they improve source diversity, credibility, contradiction resolution, or coverage completeness.

### `src/superclaude/examples/deep_research_workflows.md`

- Update examples so each workflow shows `search_depth`, `extract_depth`, `topic`, and recency/domain filters where relevant.
- Add one negative example: “do not crawl the open web for a narrow official-doc answer; use Context7 or Tavily basic search against official domains.”

## Acceptance Criteria

1. All Tavily docs and agents name tavily-mcp `0.2.20` and the default `{"search_depth":"basic","max_results":10}`.
2. Every Depth Profile names concrete `search_depth`, `extract_depth`, and allowed tool set.
3. Advanced search is gated by depth profile, confidence target, or replanning trigger; no file recommends advanced as a blanket default.
4. Credibility/recency methodology maps to `topic`, `time_range`, `days`, `include_domains`, and `exclude_domains`.
5. Crawl/map are documented as inventory/completeness tools with dedupe, tier scoring, and relevance filtering before synthesis.
6. Citation/source-table guidance records search/extraction parameters and fallback reasons.
7. Examples demonstrate basic-first behavior and at least one advanced escalation after low confidence or gaps.

## Verification

- Run a doc-consistency grep for `0.2.20`, `search_depth`, `extract_depth`, `tavily-map`, and `tavily-crawl` across all six scoped files.
- Run a parity check that no scoped file documents unsupported Tavily parameters or stale names like generic `Recency`/`Extract:true` without mapping to 0.2.x parameters.
- Methodology check: parse the Depth Profiles table and fail if any profile lacks a concrete `search_depth`, `extract_depth`, or tool set.
- Quality check: fail if `advanced` appears without nearby gating language such as confidence, gap, contradiction, deep, exhaustive, or replanning.

## Biggest Risk

The upgrade could create false rigor: bigger searches, raw content, and crawls may look more comprehensive while increasing duplicate, low-credibility, or off-topic evidence. The spec must make curation—not volume—the unit of research quality.
