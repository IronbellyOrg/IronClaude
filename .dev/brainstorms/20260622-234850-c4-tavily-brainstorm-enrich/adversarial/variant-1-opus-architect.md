# Variant 1 — Architect Lens: Brainstorm Research-Enrichment Tavily Alignment

**Thesis:** Brainstorm enrichment is **downstream** of `/sc:research` and `tech-research`. It must **inherit** the engine's Tavily behavior, never re-specify it. C2 owns the engine (tavily-mcp 0.2.20; map/crawl; depth tiering). C3 kept `/sc:research` generic. Brainstorm's job is routing-by-depth, not parameter ownership. The minimal alignment is three small clarifications plus one consistency assertion — and a deliberate **non-change** to the frontmatter and the fallback row.

## Decision Summary

| Question | Verdict | Rationale |
|----------|---------|-----------|
| (1) Frontmatter `mcp-servers: [...tavily]` | **NO CHANGE** | Server-level declaration. Tavily availability is correct; param/version pins live in the engine (C1/C2), not in a consumer's server list. Bumping it here would duplicate the pin. |
| (2) `--research light/deep` → depth | **State as inheritance** | `light` resolves to `/sc:research` quick-tier (which C2 maps to `search_depth=basic`); `deep` resolves to `tech-research` (which C2 maps to `search_depth=advanced`). Brainstorm names the *route*, not the param. |
| (3) "Tavily down → WebSearch" fallback | **CORRECT, keep** | Already tool-agnostic; confirm wording covers light enrichment that never touches map/crawl. |
| (4) Does brainstorm name map/crawl? | **NO** | map/crawl are engine concerns. Brainstorm light enrichment is a single-query scan; leaking map/crawl here is scope creep. |

## Minimal Edits Per File

### A. `src/superclaude/commands/brainstorm.md` — **NO functional change**

Frontmatter stays `mcp-servers: [sequential, serena, auggie-mcp, tavily]`. The "Tavily research enrichment" example line (≈ L97) is accurate as-is. **One optional clarity edit** to the Related-Commands `/sc:research` row (L171): append *"(inherits Tavily search_depth from the research engine — light = quick-tier basic)"* so the inheritance is explicit without duplicating params. Resist adding a routing table here.

### B. `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` — Wave 2A matrix clarification

In the §Wave 2A enrichment routing matrix (≈ L185–186), append an inheritance note to the two research rows (not a new param column):

- `--research light` row → end with: *"Tavily depth inherited from `/sc:research` quick-tier (search_depth=basic); brainstorm does not set Tavily params directly."*
- `--research deep` row → end with: *"Tavily depth inherited from `tech-research` (search_depth=advanced)."*

Error-handling row (L386) "Research enrichment fails (Tavily down) → WARN, fall back to WebSearch (quality_tier=fallback_1)" — **keep verbatim**. Add a one-clause confirmation it is tool-agnostic: light enrichment is a single search call, so the WebSearch fallback fully substitutes (no map/crawl path to degrade).

### C. `docs/user-guide/brainstorm.md` — depth-label parity

L48 `--research | auto | light (Tavily), deep (tech-research skill), none` → tighten to *`light (Tavily basic via /sc:research), deep (tech-research, Tavily advanced)`*. Keeps docs honest to the engine's depth tiers without re-teaching map/crawl. Do **not** add a Tavily params table.

## (d) Verification — Consistency Check

A doc⇆engine parity assertion (not a code test — these are instruction files):

1. **No-duplication check:** `grep -rn "search_depth\|max_results\|tavily-mcp\|0\.2\.2" src/superclaude/commands/brainstorm.md src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` returns **zero param/version pins** — brainstorm must reference the engine, never restate `{search_depth, max_results, version}`.
2. **No map/crawl leak:** `grep -rin "map\|crawl" <brainstorm command + SKILL>` returns no Tavily-tool references (existing prose uses of "map" unrelated to Tavily are allowed; confirm none are tavily-map/tavily-crawl).
3. **Inheritance non-contradiction:** Brainstorm's only depth claims (`light→basic`, `deep→advanced`) match C2's engine mapping. If C2's tier→depth mapping changes, brainstorm needs no edit (it inherits) — verify by reading the engine's research command and confirming `light`/`deep` resolve there.

## Acceptance Criteria

- [ ] Frontmatter `tavily` server entry unchanged; no version/param pin added to either brainstorm file.
- [ ] Wave 2A research rows state depth as **inherited** from `/sc:research`/`tech-research`, with no duplicated Tavily routing table.
- [ ] Tavily-down → WebSearch fallback row preserved and confirmed tool-agnostic for light (map/crawl-less) enrichment.
- [ ] Brainstorm files contain **no** reference to tavily-map / tavily-crawl.
- [ ] Doc `--research` label reflects light=basic / deep=advanced without re-specifying engine params.
- [ ] Consistency grep checks (1)–(3) pass.
