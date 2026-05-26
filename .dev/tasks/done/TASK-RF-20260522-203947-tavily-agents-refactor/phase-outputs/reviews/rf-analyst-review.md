# rf-analyst Tavily Refactor — Acceptance Review

**Target file:** `/config/workspace/IronClaude/src/superclaude/agents/rf-analyst.md`
**Proposal:** `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-analyst-tavily-refactor.md`
**Reviewer:** Phase 2 Step 2.8 executor (Re-Read verification, re-apply cycle)

## Acceptance Criteria

1. **PASS** — Frontmatter `tools:` contains both `mcp__tavily__tavily-search` (line 13) and `mcp__tavily__tavily-extract` (line 14).
2. **PASS** — Frontmatter still contains `WebSearch` (line 15) and `WebFetch` (line 16) as fallbacks with inline FALLBACK comments.
3. **PASS** — Tavily entries (lines 13-14) appear before WebSearch/WebFetch (lines 15-16) in the frontmatter ordering.
4. **PASS** — New body subsection `## Web Research — Tavily-first Protocol (rare; usually NOT needed)` exists at line 346, placed between "Quality Standards" (ends line 342) and "Completion Protocol" (line 387), separated by a `---` rule at line 344.
5. **PASS** — Subsection states web research requires spawn-prompt authorization ("If — and only if — your spawn prompt explicitly directs you...", line 354) and unauthorized external content is "fabrication-by-import" (line 384, "that is fabrication-by-import and violates Critical Rule 7"). Role-acknowledgement at lines 348-352 links to zero-tolerance-for-fabrication Rule 7.
6. **PASS** — Three Tavily-unavailable conditions defined as numbered list (lines 367-372): (1) tool-not-loaded, (2) server-error-after-retry, (3) rate-limit 429.
7. **PASS** — `[WEB_RESEARCH_FALLBACK: tavily=<reason>; used=<WebSearch|WebFetch>; url=<url>; claim=<claim being verified>]` marker format present at lines 377-378, with `claim=` field present, placed under Methodology/Quality Standards section reference.
8. **PASS** — New Critical Rule 9 (lines 412-418) codifies Tavily-first ("use `mcp__tavily__tavily-search` / `-extract` first; fall back to WebSearch / WebFetch only when Tavily is unavailable") AND links back to Rule 7 ("Treat unauthorized external content as fabrication-by-import (Rule 7).").
9. **PASS** — Existing five analysis types (completeness-verification, cross-validation, synthesis-review, gap-analysis, coverage-audit), Synthetic-DNSP Finding behavior (lines 70-86), Parallel Partitioning (lines 42-69), General Process (lines 90-98), Quality Standards bullets (lines 335-342), and Critical Rules 1-8 (lines 404-411) untouched.
10. **PASS** — Cross-Validation analysis's existing `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tagging preserved unchanged at line 217 (in Process step 3). The refactor reuses `[UNVERIFIED]` for the unauthorized-fetch case (line 382) without altering the original tagging system.

## Deferred Sync/Verify Criterion

- **DEFERRED** — `make sync-dev` + `make verify-sync` to confirm no drift between `src/superclaude/agents/rf-analyst.md` and `.claude/agents/rf-analyst.md`. Per task instructions, `.claude/agents/` was NOT edited; sync/verify is deferred to the Phase 3 batch sync step per project sync discipline.

## Anomalies

None. All edits applied via Edit tool, one Edit per discrete diff anchor (3 edits total: frontmatter tools reorder, new Tavily-first Protocol subsection insertion between Quality Standards and Completion Protocol, new Critical Rule 9 appended). Proposal text reproduced verbatim into target file. Re-apply cycle (post-HEAD-revert) reproduces the same line topology and content as the prior successful application.

**Overall Verdict:** PASS
