# Variant 1 — Opus / Analyzer Lens

## Cluster: TROUBLESHOOT + REFLECT Tier-2 Tavily upgrade → tavily-mcp 0.2.20

**Lens:** debugging methodology + evidence quality. **Scope:** Tavily as a rate-limited,
targeted Tier-2 web search only. NOT extraction, NOT map/crawl.

## (a) The analyzer call: `search_depth` for triage

The driving question is the cost/quality tradeoff under a **≤2-query hard cap**. The C1 pin
`DEFAULT_PARAMETERS {"search_depth":"basic","max_results":10}` is the *engine* default,
optimized for high-volume deep-research fan-out where many cheap queries beat few expensive
ones. **That economics is inverted here.** When the entire wave's external-evidence budget is
two queries, each query must maximize hit-rate, not minimize unit cost. Basic search returns
shallow snippet matches that frequently miss obscure stack traces and version-specific GitHub
issue threads; `advanced` re-ranks and pulls deeper page content, materially raising recall on
exactly the long-tail symptoms that escalate to Tier 2 in the first place. A Tier-2 escalation
means Tier 1 already failed to ground the bug locally — the symptom is *by definition* obscure.

**Decision: instruct `search_depth: advanced` for these two queries.** The marginal cost (a
few hundred extra tokens / one extra credit per query, ×2 max) is negligible against the ROI of
correctly identifying a root cause. The rate cap is what *makes* `advanced` affordable here: we
are not running 50 advanced searches, we are running ≤2. Basic is the wrong default for a
deliberately rationed, high-stakes lookup.

## (b) `include_domains` for credibility

Tier-2 error lookups have two canonical authoritative sources: **github.com** (issue trackers,
the actual upstream bug) and **stackoverflow.com** (reproductions + accepted fixes). Constraining
to these raises evidence quality (signal over SEO content-farm noise) and tightens the evidence
chain that `evidence-validator` (troubleshoot) / the grounding gate (reflect) later audits.

**Decision: recommend (not mandate) `include_domains: ["github.com","stackoverflow.com"]`** for
the error-string query, with explicit license to drop the filter on the `<library> <version>
<symptom>` query when official docs / release notes are the better source. Mandating it would
suppress legitimate first-party domains (e.g. a project's own docs site). Guidance, not a gate.

## (c) `topic`

These searches are always technical. **Decision: never set `topic: news`** (default `general`
is correct). State this explicitly so no agent reaches for `news` on a "regression since
release" phrasing.

## (d) Out of scope — confirmed excluded

map / crawl / extract are **deep-research** capabilities (C2), wrong tool class for rationed
triage. No edits introduce them. The upgrade to 0.2.20 is otherwise **transparent**: the
`tavily-search` tool signature (query, `search_depth`, `max_results`, `include_domains`,
`exclude_domains`, `topic`) is unchanged across 0.2.x — these are param-guidance edits to
instruction prose, not a tool-surface migration.

## Minimal concrete edits

**`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`** (line ~335, the focused-query
instruction — the load-bearing edit):
> `mcp__tavily__tavily-search` for the exact error string + "github issue", or `<library>
> <version> <symptom>` — **use `search_depth: advanced` (the ≤2-query cap makes the cost
> negligible and Tier-2 symptoms are obscure by definition); prefer
> `include_domains: ["github.com","stackoverflow.com"]` for the error-string query; never set
> `topic: news` (these are technical).** (rate-limited — at most 2 queries in this wave)

**`src/superclaude/commands/troubleshoot.md`** (line ~91 Tavily bullet): append one clause —
"…lookups, using `search_depth: advanced` and GitHub/StackOverflow `include_domains` for
credibility." Lines ~99/~165 ("targeted web search (Tier 2, rate-limited)") unchanged — they
stay description-level and remain consistent.

**`src/superclaude/skills/sc-reflect-protocol/SKILL.md`**: reflect uses tavily far more
incidentally (line ~1689 fail-open only; no focused-query block like troubleshoot's ~335). Add a
**one-line parenthetical** wherever the Tier-2 tavily call is first described in the body
prose, mirroring the troubleshoot wording (`search_depth: advanced`, technical `include_domains`).
Do not invent a new query-budget — reflect has no ≤2 cap; keep its existing usage shape.

**`src/superclaude/commands/reflect.md`** (line ~151): same description bullet, unchanged at the
one-liner level (it already reads "targeted web search (Tier 2, rate-limited)" — keep parity).

**No change** to: capability table rows (~510 troubleshoot: "✓ rate-limited (≤2 queries)" stays),
the "Will Not call tavily without a focused query" guard (~538), or any fallback row.

## (d) Verification

1. **Consistency:** grep `tavily-search` across all four files — every *description-level*
   mention still reads "targeted web search (Tier 2, rate-limited)"; only the *focused-query
   instruction* blocks carry the new param guidance. No description contradicts another.
2. **Rate cap preserved:** troubleshoot ≤2-query language at ~335, ~510, ~538 untouched in
   meaning. New guidance lives *inside* the capped instruction, never relaxing the cap.
3. **No map/crawl/extract:** grep confirms zero occurrences of `tavily-extract`/`map`/`crawl`
   in edited regions.
4. `make sync-dev && make verify-sync` after editing `src/`.

## Acceptance criteria

- [ ] Both skill focused-query blocks specify `search_depth: advanced`, justified by the cap.
- [ ] `include_domains` guidance present as a *recommendation* (github+stackoverflow), not a gate.
- [ ] `topic: news` explicitly excluded.
- [ ] ≤2-query rate cap text byte-identical in meaning across all sites.
- [ ] Zero map/crawl/extract additions; tavily-search description strings agree across 4 files.
- [ ] `make verify-sync` clean.

**Biggest risk:** advancing every Tier-2 search to `advanced` quietly raises per-invocation
Tavily credit burn; mitigated by the hard ≤2 cap, but flag it as the one cost the operator pays.
