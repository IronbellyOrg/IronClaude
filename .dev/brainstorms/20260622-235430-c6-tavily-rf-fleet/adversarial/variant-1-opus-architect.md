# Change Spec — RF Agent Fleet under tavily-mcp 0.2.x (Architect Variant)

**Lens:** Right-sizing the tool surface per agent role. **Cross-cluster pins consumed:** tavily-mcp 0.2.20 is C1 install-level (NOT agent frontmatter); `DEFAULT_PARAMETERS {"search_depth":"basic","max_results":10}` is C1 server-level; map/crawl adoption (C2) is for the **deep-research engine's exhaustive web crawling**, not RF. Tool IDs `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` are **unchanged** in 0.2.x.

## Core architect position: the fleet is already correctly sized — do not over-adopt

RF research is **targeted, codebase-task context-gathering**, not exhaustive web crawling. The 8 RF agents use the web as a *supplement* to local Read/Grep/Glob (rf-task-researcher's "always check locally first"; rf-analyst/rf-assembler "rare use; usually NOT needed"). `tavily-search` (point lookups) + `tavily-extract` (fetch a known URL) is the exact two-verb surface this workload needs. `tavily-map` (site-structure discovery) and `tavily-crawl` (recursive multi-page harvest) serve breadth-first web exploration — a capability **no RF agent's role calls for**, including the dedicated researcher.

## (1) Does any RF agent need tavily-map / tavily-crawl? — NO (researcher included)

**rf-task-researcher (the dedicated researcher): stay search+extract.** Its "Solution Research" section is explicitly bounded — investigate problem-domain patterns, tool/library comparison, best-practice verification. Every example query (`"PostgreSQL JSONB index best practices"`, `"SVG chart generation without dependencies comparison"`) is a **single-result-set lookup**, satisfied by `tavily-search`, with `tavily-extract` for a named URL. Crawl/map would invite scope creep (recursive harvesting of a vendor site) directly contradicting the agent's own "Do NOT use any web tool for things you can find in the codebase" rule and its evidence-based, per-URL-provenance discipline.

**Adding crawl/map would actively harm the fleet's architecture:** the mature fallback-provenance model (`provider=tavily` default → `provider=WebSearch reason=<tavily-unavailable|tavily-error|tavily-rate-limit>`) is defined for exactly two verbs. Each new tool multiplies the fallback matrix (WebSearch has no crawl analogue — what does a crawl fallback even log?), erodes the auditable "do not fall back silently" contract, and adds an over-powered capability to bypassPermissions agents for zero role benefit. Keep the surface minimal.

## (2) Is the version upgrade transparent at the agent level? — YES

The 0.2.20 pin is install-level (C1). Tool IDs are unchanged. Agents reference tools by stable ID only; none pin a version. **Nothing in any agent body or frontmatter references a tavily-mcp version.** The upgrade is fully transparent to all 8 agents — confirmed by reading rf-task-researcher, rf-qa, rf-analyst, rf-assembler (no version string present).

## (3) Frontmatter changes? — NONE for all 8

Each agent's `tools:` allow-list already contains exactly `mcp__tavily__tavily-search` + `mcp__tavily__tavily-extract`, matching its prose. No tool to add (no map/crawl adopted), none to remove (both still called), no ID to rename (IDs stable). The allow-list ⇔ prose contract already holds.

## (4) Do these inherit DEFAULT_PARAMETERS automatically? — YES

`{"search_depth":"basic","max_results":10}` is enforced server-side (C1). Agents call `tavily-search` without specifying these params, so they inherit the defaults transparently — `basic` depth + 10 results is well-matched to targeted lookups (the fleet does NOT want `advanced`/exhaustive depth). No agent-side change needed; no prose should hardcode these values.

## Per-agent verdict

| Agent | Tavily prose maturity | Verdict |
|---|---|---|
| rf-task-researcher | Heavy (Solution Research + Tavily-first + 3 fallback conds) | **NO-CHANGE** |
| rf-qa | Heavy (Tavily-first external-lookup + auditable fallback) | **NO-CHANGE** |
| rf-analyst | Light (rare; authorized-only) | **NO-CHANGE** |
| rf-assembler | Light (rare; authorized-only) | **NO-CHANGE** |
| rf-task-builder | Inherited Tavily-first pattern | **NO-CHANGE** |
| rf-qa-qualitative | Inherited Tavily-first pattern | **NO-CHANGE** |
| rf-team-lead | Inherited Tavily-first pattern | **NO-CHANGE** |
| rf-task-executor | Inherited Tavily-first pattern | **NO-CHANGE** |

**Net change to the fleet: zero edits.** The correct architect outcome is to *prove* the fleet is already right-sized, not to manufacture churn.

## Verification — fleet-wide parity test (SHARES the C2 parity test)

Add one parity assertion covering both clusters (RF fleet + deep-research engine), since the invariant is identical: **every `mcp__tavily__*` tool ID appearing in any agent's prose body MUST appear in that agent's `tools:` frontmatter, and every `mcp__tavily__*` in frontmatter MUST be exercised by the prose.** This is the C2 parity test extended to glob all `src/superclaude/agents/*.md`.

Implementation sketch (pytest, `tests/agents/test_tavily_tool_parity.py`):
1. Glob `src/superclaude/agents/*.md`; for each, parse YAML frontmatter `tools:` → set of `mcp__tavily__*` IDs.
2. Grep the body (post-frontmatter) for `mcp__tavily__[a-z-]+` → set of prose-referenced IDs.
3. Assert `prose_set ⊆ frontmatter_set` (no prose call to an undeclared tool) **and** `frontmatter_set ⊆ prose_set` (no dead allow-list entry). Report per-agent diffs.
4. **Bonus guard (catches the over-adoption regression this spec rejects):** assert no agent file contains `tavily-map` or `tavily-crawl` in either surface — locks the "RF stays two-verb" decision.

## Acceptance criteria

- AC1: All 8 RF agents retain exactly `mcp__tavily__tavily-search` + `mcp__tavily__tavily-extract`; zero frontmatter edits.
- AC2: No RF agent references `tavily-map`/`tavily-crawl` in prose or frontmatter.
- AC3: Parity test passes fleet-wide (RF + deep-research), proving allow-list ⇔ prose for every tavily ID.
- AC4: No agent body or frontmatter contains a tavily-mcp version string (upgrade transparency held).
- AC5: No agent prose hardcodes `search_depth`/`max_results` (server-side DEFAULT_PARAMETERS inheritance preserved).
- AC6: `make verify-sync` green (src/ ⇔ .claude/) — applies only if any edit lands; with zero edits, sync is trivially preserved.
