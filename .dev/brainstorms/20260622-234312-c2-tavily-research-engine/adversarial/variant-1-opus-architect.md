# Variant 1 — Architect: tavily-mcp 0.2.20 in the Deep-Research Routing Model

## Lens & thesis

The research engine today runs one loop: **broad search → select URLs → extract**.
`tavily-map` and `tavily-crawl` are not new ways to *extract*; they are a new
**discovery primitive** that sits *upstream* of extraction. The architect call:
adopt both, but only at the bottom two depth profiles (`deep`, `exhaustive`),
and slot them into a new **Discovery Routing** axis distinct from the existing
**Extraction Routing** axis. Do not fold them into extraction tables — that
conflates "find the URLs" with "pull the content" and will cause over-crawling.

## The two-axis routing model (core architectural change)

```
DISCOVERY (find URL inventory)        EXTRACTION (pull content from a URL)
  tavily-search   — query → URLs        tavily-extract — static HTML
  tavily-map      — site → URL graph     playwright     — JS / auth / screenshots
  tavily-crawl    — domain → pages       context7       — library/API docs
                                         native         — local files
```

Search remains the default discovery entry point. Map/crawl are **escalations
within discovery**, gated by depth profile and a single-domain condition.

### Adoption verdicts (where they earn their place)

- **tavily-map — ADOPT for `deep` + `exhaustive`, discovery phase only.**
  Use when the question targets a *known single site* whose structure must be
  inventoried before extracting (e.g. "everything in the Next.js App Router
  docs", a single vendor's pricing/feature tree). Map returns the URL graph
  cheaply; the engine then extracts selectively. **NOT worth it** for
  `quick`/`standard` (one or two URLs — mapping is overhead) or for
  open-web/multi-source questions (no single domain to map).
- **tavily-crawl — ADOPT for `exhaustive` only, plus opt-in on `deep`.**
  Use when comprehensive *coverage of one domain* is the goal and search recall
  is provably insufficient (a hop returns <3 sources, or coverage gap >50% per
  the existing replanning thresholds). Crawl is the heaviest tool — it
  traverses many pages — so it is the **last-resort discovery escalation**, not
  a default. **NOT worth it** for `quick`/`standard`, for multi-domain
  synthesis (crawl is single-domain), or when `tavily-map` + selective extract
  already satisfies coverage.

## search_depth-by-profile rule (honors the C1 cross-cluster pin)

DEFAULT_PARAMETERS inheritance root stays `{"search_depth":"basic","max_results":10}`.
Per-call override by profile:

| Profile     | search_depth | Discovery tools allowed                 | Extraction       |
|-------------|--------------|-----------------------------------------|------------------|
| quick       | basic        | search                                  | tavily_only      |
| standard    | basic        | search                                  | selective        |
| deep        | advanced     | search, **map**, crawl(opt-in)          | comprehensive    |
| exhaustive  | advanced     | search, **map**, **crawl**              | all_sources      |

`basic` for quick/standard; `advanced` for deep/exhaustive — unchanged gate,
now also governing which discovery tools unlock.

## Playwright-vs-crawl boundary (reconciliation)

They do not overlap — they live on different axes. **Crawl is discovery**
(which pages exist on a domain); **Playwright is extraction** (render one JS/
auth page). Crawl never obviates Playwright when target pages are JS-rendered
or login-gated: crawl enumerates the URLs, Playwright still extracts each. The
only case crawl *reduces* Playwright load is static-HTML domains where crawl's
own page text suffices, removing the per-URL extract hop. Rule to encode:
**crawl for the URL set; route each resulting URL through the existing
Extraction Routing table** (static→tavily-extract, JS/auth→playwright).

## Concrete per-file edits

1. **`src/superclaude/core/RESEARCH_CONFIG.md`** *(most important edit)*
   - `tools:` line: add `discovery: tavily` → keep, but add
     `discovery_escalation: [map, crawl]` and `version: 0.2.20`.
   - Depth Profiles table: add a **Discovery** column matching the table above.
   - Add a new **Discovery Routing** table (search/map/crawl + conditions:
     single-domain, profile≥deep, recall<3 or gap>50% for crawl).
   - Leave Extraction Routing table as-is (map/crawl are not extraction).
   - MCP Integration table: add rows `tavily-map → discovery (fallback: search)`
     and `tavily-crawl → domain coverage (fallback: map+search)`.

2. **`src/superclaude/agents/deep-research-agent.md`** *(second most important)*
   - tools frontmatter: add `mcp__tavily__tavily-map`, `mcp__tavily__tavily-crawl`.
   - "Tool Orchestration → Search Strategy": insert step 0 "If single-domain &
     profile≥deep: map before extracting; escalate to crawl on coverage gap."
   - Keep Extraction Routing unchanged; add a sibling "Discovery Routing" block.

3. **`src/superclaude/agents/deep-research.md`**
   - tools frontmatter: add `mcp__tavily__tavily-map`, `mcp__tavily__tavily-crawl`.
   - Tool Selection Policy: add a "Discovery escalation" clause (map/crawl gated
     to deep/exhaustive + single-domain). Add backend tags `tavily-map`,
     `tavily-crawl` to the sources-table backend enum.

4. **`src/superclaude/mcp/MCP_Tavily.md`**
   - Search Capabilities: add **Site Mapping** (map) and **Domain Crawling**
     (crawl) bullets; document DEFAULT_PARAMETERS env/header.
   - Add two Search Patterns: "Site Map (discovery)" and "Domain Crawl
     (coverage)". Note 0.2.20 + the override-to-advanced rule.

5. **`src/superclaude/modes/MODE_DeepResearch.md`** (~line 50)
   - "Enables Tavily search capabilities" → "Enables Tavily search, site-mapping,
     and domain-crawl capabilities (map/crawl gated to deep/exhaustive)."

6. **`src/superclaude/examples/deep_research_workflows.md`**
   - Add one worked example: Example 6 (Next.js docs) gains a map-first
     discovery step; add a short `exhaustive` crawl example for single-domain
     coverage. (Keep edits minimal — examples illustrate, not normative.)

## Acceptance criteria

- AC1: Every depth profile names an allowed discovery tool set; quick/standard
  never reference map/crawl.
- AC2: search_depth = basic for quick/standard, advanced for deep/exhaustive
  (C1 pin intact; DEFAULT_PARAMETERS root unchanged).
- AC3: map/crawl appear only on a Discovery axis; Extraction Routing tables
  remain search-tool-free of map/crawl.
- AC4: Every tavily tool named in any routing table is present in the relevant
  agent's tools frontmatter.

## Verification (doc-consistency, since these are instruction files)

- **Top test — frontmatter↔routing parity (automated):** a pytest doc-check
  that greps every `mcp__tavily__tavily-*` token referenced in routing tables
  across the 6 files and asserts it is declared in the corresponding agent
  frontmatter `tools:` list (and vice-versa: no orphan frontmatter tool). This
  catches the highest-probability drift — a table citing a tool the agent can't
  call.
- **Profile-gate test:** assert `quick`/`standard` rows contain no `map`/`crawl`
  substring; `exhaustive` row contains both.
- **Opt-in live exercise (manual, not CI):** one `deep`-profile run against a
  single doc site exercising map→selective-extract, and one `exhaustive` run
  exercising crawl, logged to confirm the tools resolve and respect
  search_depth:advanced.

## Biggest risk

**Over-adoption / cost blowout:** crawl traverses whole domains; if the gate
(profile≥exhaustive + single-domain + coverage-gap trigger) is stated loosely,
the engine will crawl multi-source open-web questions and burn the API
budget/rate limits the config already warns about. Mitigation: crawl is
last-resort, single-domain, threshold-triggered — never a default discovery
step.
