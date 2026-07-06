---
variant: 2
model: sonnet
persona: analyzer
cluster: C4
title: /sc:brainstorm research enrichment Tavily 0.2.x alignment
created: 2026-06-22
---

# Analyzer Variant — Small Change Spec

## Verdict

Keep the current split: `--research light` routes to `/sc:research` with quick depth; `--research deep` routes to `tech-research`. Do **not** add Tavily parameters to brainstorm. Tavily 0.2.x behavior should be inherited from the research engines: C2 owns engine capabilities (`search_depth` basic/advanced, map/crawl), C3 keeps `/sc:research` generic, and brainstorm should remain an orchestration layer.

## Minimal edits

1. In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, add one sentence after the Wave 2A routing matrix or in Quality-tier tracking:
   - Research enrichment delegates all Tavily MCP configuration to `/sc:research` or `tech-research`; brainstorm MUST NOT set Tavily `search_depth`, map/crawl, or default parameter values directly.

2. In the Error Handling Matrix row for research enrichment failure, clarify fallback quality:
   - `WebSearch fallback_1` is a lower-fidelity fallback that preserves enrichment continuity but lacks Tavily MCP 0.2.x engine features such as depth-aware Tavily search and map/crawl-backed discovery.

No edit is required in `src/superclaude/commands/brainstorm.md` unless reviewers want the Related Commands table to say “light research via `/sc:research`” rather than implying direct Tavily usage. No edit is required in `docs/user-guide/brainstorm.md` beyond the same optional wording cleanup.

## Consistency / non-contradiction check

- `src/superclaude/commands/brainstorm.md` frontmatter includes `tavily`, but Wave 2A text delegates enrichment to `/sc:research` and `tech-research`; this is compatible with inherited Tavily behavior.
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` already routes light to `Skill sc-research-protocol --depth quick` and deep to `Skill tech-research`; no stale claim says brainstorm itself performs only basic Tavily search.
- `docs/user-guide/brainstorm.md` says `--research light` is Tavily and `--research deep` is `tech-research`; this is coarse but not contradictory if `tech-research` uses the upgraded engine internally.

## Acceptance criteria

- Brainstorm contains no duplicated Tavily MCP defaults or hardcoded `search_depth` values.
- Deep research enrichment continues to route through `tech-research`, allowing advanced Tavily behavior to be inherited there.
- Fallback documentation explicitly marks WebSearch as lower fidelity than Tavily MCP 0.2.x, while still acceptable for degraded enrichment.
- Command, protocol, and user-guide language remain consistent: brainstorm orchestrates; research engines configure Tavily.
