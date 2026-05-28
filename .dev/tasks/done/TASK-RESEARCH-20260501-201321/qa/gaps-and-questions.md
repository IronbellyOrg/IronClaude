# Merged Gaps and Questions — Research Completeness Gate

**Date:** 2026-05-01
**Source partition reports:**
- `qa/analyst-completeness-report-1.md` (Partition 1: 01, web-01..web-04)
- `qa/analyst-completeness-report-2.md` (Partition 2: web-05..web-08)
- `qa/qa-research-gate-report-1.md` (Partition 1)
- `qa/qa-research-gate-report-2.md` (Partition 2)

---

## Merged Verdict: **PASS (post-fix)**

Both partition reports returned FAIL on initial pass. The FAIL was gate-driven (Status: In Progress markers on 5 files, plus 2 minor content issues in web-04). All gate-blocking issues were fixed in-place:

| Issue | Files affected | Resolution |
|-------|----------------|------------|
| Status: In Progress not flipped to Complete | web-01, web-03, web-04, web-05, web-08 | All flipped to Status: Complete |
| Helicone OSS license inconsistency ("MIT-style" vs Apache-2.0) | web-04 line 53 | Corrected to "Apache-2.0" — confirmed against the repo |
| Duplicated "Activity signal" line under Phoenix | web-04 lines 74-75 | Merged into single line |

Both QA partition reports explicitly noted that, **with Status fields corrected, remaining minor findings can be deferred to synthesis without re-spawning research**. Substantive content quality is strong across all 9 files (199–330 lines each, real verifiable URLs, comprehensive scope coverage, Deep-tier rigor).

The merge therefore promotes verdict to **PASS** for Phase 5 synthesis to proceed. Remaining minor findings are folded into the gap inventory below for synthesis-time handling.

---

## Critical Gaps — none after fix

(All gate-blocking gaps were resolved. None remain.)

## Important Gaps — deferred to synthesis (Sections 4, 6, 9 of final report)

| # | Gap | Source | Synthesis handling |
|---|-----|--------|-------------------|
| I1 | SpecStory paid-tier pricing not obtained — `/pricing` 404s, Teams page is a Design Partner application | web-01, analyst-1 | Acknowledge in Section 5 (External Findings — SpecStory) and Section 9 (Open Questions) as "Pricing currently unobtainable without Design Partner application; assume free + custom enterprise" |
| I2 | SpecStory RAG-roadmap rests on unreachable beta.specstory.com references; no shipped product to verify | web-01, analyst-1 | Treat RAG-coming-soon as roadmap-only in Section 4 (Gap Analysis); do NOT count it as available capability |
| I3 | web-02 weak-evidence retries on CursorShare, Packmind, G2 alternatives page | web-02, analyst-1 | These are mentioned but not load-bearing — keep as illustrative, not core comparables |
| I4 | web-07 load-bearing claims missing URL citations: Voyage/MongoDB acquisition, Turbopuffer customers (Cursor, Notion AI), Mastra 10x cost reduction | web-07, qa-2 | Synthesis must mark these claims with `[UNVERIFIED]` if they appear in Sections 5, 6, 7, or 8 |
| I5 | web-07 Voyage code-3 uplift wording imprecise ("+13.8% to +16.3% average") | web-07, qa-2 | Use the verified single-value claim "+13.8% over text-embedding-3-large on code retrieval" if cited in Section 6/8 |
| I6 | Open WebUI license clause requiring branding preservation for >50-user deployments sourced to unlinked Reddit thread | web-05, analyst-2 | Include the clause in Section 6 Options Analysis under Open WebUI but mark `[UNVERIFIED — needs verification against actual license text]` |
| I7 | web-04 Phoenix `arize-phoenix-otel` adjacent package license noted as "Elastic-2.0 in some channels — verify per package" | web-04 | Include in Section 9 Open Questions if Phoenix is a recommended option |
| I8 | Some web-files lack standalone `## Gaps and Questions` sections with severity tags | web-01..web-08 (most) | This consolidated file IS the standalone gap repository for synthesis; no additional per-file sections required |
| I9 | web-07 lacks Reliability: tag in per-product entries (file-level reliability implied, but not per-row) | web-07 | Treat all web-07 sources as Official-or-Repo unless otherwise noted; flag in Section 9 if specific source reliability matters |

## Minor Gaps — surfaced for Section 9 Open Questions

| # | Gap | Source | Synthesis handling |
|---|-----|--------|-------------------|
| M1 | Cross-partition deduplication needed: AnythingLLM, Pieces, Cline Memory Bank, MCP-memory servers, Spool, Cursor coverage appears in multiple files | qa-1, qa-2 | Synthesis Section 5 (External Findings) must merge cross-bucket coverage by product, not by bucket |
| M2 | Onyx framing differs between web-05 (chat platform) and web-07 (reference architecture) | analyst-2 | Synthesis must harmonize — Onyx is primarily a self-hosted chat-platform-with-RAG; its appearance in web-07 is as a reference architecture for the BYO-adjacent path |
| M3 | Cursor's "Generate Cursor Rules from chat history" feature — biggest medium-term threat per web-02 | web-02 | Section 4 Gap Analysis and Section 9 Open Questions should track Cursor's roadmap as a potential native solution that could obsolete the unified-context project |
| M4 | Some research files use HIGH/MEDIUM/LOW relevance and others use a different convention | qa-1, qa-2 | Synthesis Section 5 should use a consistent HIGH/MEDIUM/LOW relevance rating across all comparable products |
| M5 | Codex CLI / Copilot CLI / gh-copilot deprecation timeline (gh-copilot deprecated 2025-10-25) | 01-native-storage | Note in Section 2 Current State Analysis that some native storage formats are in flux |
| M6 | Some products' multi-tenant isolation models are described qualitatively rather than with specific feature names | web-03, web-05, web-06 | Acceptable for a research report; if downstream tech-reference is requested, this is one area to deepen |

---

## Cross-Partition Findings (Synthesis Must Reconcile)

These products appear in multiple partition files and need merged treatment in synthesis Section 5:

1. **AnythingLLM** — covered in web-02 (deferred there) AND web-05 (primary self-hosted chat coverage). Synthesis: use web-05 as primary source.
2. **Pieces for Developers** — web-02 + web-08. Synthesis: web-08 has the deeper architectural take (LTM cross-IDE); web-02 acknowledges adjacency.
3. **Cline Memory Bank** — web-02 + web-08. Synthesis: web-08 has the dominant treatment as a "distilled-knowledge" pattern; web-02 mentions the git-native persistence pattern.
4. **MCP memory servers** — web-02 (briefly) + web-08 (deep, with substrate framing) + web-03 (Basic Memory MCP). Synthesis: treat as a substrate category, not a competitor.
5. **Spool** — web-02 (mentioned) + web-07 (extensive cost-comparison precedent). Synthesis: use web-07 as primary (Spool is the closest BYO-vs-buy benchmark).
6. **Cursor coverage** — web-01 (as data source SpecStory captures from), web-02 (its built-in chat history + threat to comparables), web-08 (team features). Synthesis: distinguish "Cursor as a target tool to capture" vs "Cursor's own emerging features as a competitor."
7. **Onyx (Danswer)** — web-05 (primary, chat platform) and web-07 (reference architecture). Synthesis: web-05 is primary.

---

## Phase 5 Synthesis Inputs

Synthesis agents may proceed under the merged PASS verdict. They MUST:

1. Read this `gaps-and-questions.md` before drafting Section 4 (Gap Analysis), Section 5 (External Findings), and Section 9 (Open Questions).
2. Apply the cross-partition reconciliation guidance above when constructing Section 5.
3. Mark all `[UNVERIFIED]` claims explicitly in the report.
4. Carry deferred minor gaps into Section 9 (Open Questions) as appropriate.
5. Surface SpecStory's RAG-roadmap status (not shipping) prominently in Section 4 (Gap Analysis) since the user's stated goal explicitly requires RAG.
