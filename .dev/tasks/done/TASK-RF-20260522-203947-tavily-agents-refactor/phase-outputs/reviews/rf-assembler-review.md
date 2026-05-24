# rf-assembler Tavily Refactor — Acceptance Review

**Target:** `/config/workspace/IronClaude/src/superclaude/agents/rf-assembler.md`
**Direction Applied:** A (Tavily-first allowlist + body subsection + Critical Rule 10) — Direction B explicitly NOT applied.
**Verification method:** Post-edit Re-Read of target file.

## Acceptance Criteria Checklist

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Frontmatter `tools:` contains both `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract`. | PASS | Lines 13-14 contain both entries with inline `# PRIMARY` comments. |
| 2 | Frontmatter still contains `WebSearch` and `WebFetch` as fallbacks. | PASS | Lines 15-16 retain both with inline `# FALLBACK only — Tavily unavailable` comments. |
| 3 | Tavily entries appear before `WebSearch`/`WebFetch` in frontmatter ordering. | PASS | Order: tavily-search (13), tavily-extract (14), WebSearch (15), WebFetch (16). |
| 4 | New body subsection "Web Research — Tavily-first Protocol (rare; usually NOT needed)" exists. | PASS | Section heading present at line 207, located between "Output Quality Standards" (line 197) and "Completion Protocol" (line 244). |
| 5 | Subsection explicitly states web research requires spawn-prompt authorization. | PASS | Lines 210-212: "Web research violates your 'no fabrication' rule unless explicitly authorized by the spawn prompt or QA fix instruction." Plus lines 214-215 "If — and only if — your spawn prompt or an `ASSEMBLY_FIX` message explicitly directs you…". |
| 6 | Subsection defines the three Tavily-unavailable conditions. | PASS | Lines 226-231: (1) tool not loaded, (2) server error after first attempt AND single retry, (3) 429 rate-limit. |
| 7 | Subsection contains the `[WEB_RESEARCH_FALLBACK: ...]` marker format. | PASS | Lines 235-236: `[WEB_RESEARCH_FALLBACK: tavily=<reason>; used=<WebSearch\|WebFetch>; url=<url>]`. |
| 8 | New "Critical Rules" entry codifies Tavily-first AND no-unauthorized-web-research. | PASS | Line 273 contains rule 10 with both prongs: "Do NOT fetch from the web unless… explicitly authorizes it. If authorized, use `mcp__tavily__tavily-search` / `-extract` first; fall back to WebSearch / WebFetch only when Tavily is unavailable…". |
| 9 | "No fabrication" rule (Output Quality Standards) NOT weakened. | PASS | Line 203 retains original verbatim: "**No fabrication** — You are assembling existing content, not creating new content…". New subsection at line 210 explicitly reinforces it ("Web research violates your 'no fabrication' rule…"). |
| 10 | Assembler core workflow untouched (Steps 1-6, incremental writing, contradiction handling, missing-file handling). | PASS | Assembly Process Steps 1-6 (lines 82-138), Incremental Writing Protocol (lines 142-152), Missing Component Files / Contradictions / Empty Sections (lines 158-179) — all unchanged from baseline. |

## Deferred Sync/Verify Criterion

| # | Criterion | Result | Note |
|---|-----------|--------|------|
| D1 | `make sync-dev` succeeds and `make verify-sync` shows no drift. | DEFERRED | Per task scope, sync-dev is deferred to the consolidated batch step after all agent refactors complete. `.claude/agents/rf-assembler.md` intentionally NOT edited. |

## Anomalies / Notes

- None. All ten in-scope criteria PASS via Re-Read. Edits applied via Edit tool only, one Edit per discrete anchor (frontmatter tools, body subsection insertion, Critical Rule 10 append).
- The new body subsection was placed correctly between "Output Quality Standards" and "Completion Protocol" as specified in the proposal.
- Critical Rule numbering: previous max was 9, new rule lands as rule 10 — freshness report constraint satisfied.

**Overall Verdict:** PASS
