# rf-qa Tavily-first Refactor — Acceptance Review

**Target:** `/config/workspace/IronClaude/src/superclaude/agents/rf-qa.md`
**Proposal:** `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-qa-tavily-refactor.md`
**Phase:** 2 Step 2.9
**Date:** 2026-05-22

---

## Acceptance Criteria (verified via Re-Read of edited file)

- [x] **AC1 — Frontmatter precedence:** `mcp__tavily__tavily-search` (line 13) and `mcp__tavily__tavily-extract` (line 14) appear BEFORE `WebFetch` (line 15) and `WebSearch` (line 16). PRIMARY/FALLBACK inline comments present. **PASS**.

- [x] **AC2 — Fallback tools retained:** `WebFetch` (line 15) and `WebSearch` (line 16) remain in the `tools:` list with `# FALLBACK only` annotations. **PASS**.

- [x] **AC3 — New section exists at governing scope:** `## Web Research Tooling (Tavily-first)` heading inserted at line 101, between Verification Principles (ends line 97) and the first QA Phase (`Research Gate` at line 121). Position governs all downstream phases (Research Gate, Synthesis Gate, Report Validation, Task Integrity, Fix Cycle). **PASS**.

- [x] **AC4 — Three detection conditions enumerated:** Lines 110-113 enumerate exactly the three triggers: (1) tool not present in runtime tool list, (2) structured server error / 5xx / connection refused, (3) rate-limit / quota / HTTP 429. **PASS**.

- [x] **AC5 — Tool Engagement Minimum updated:** Line 473 appends the mandatory reporting requirement `tavily_search: N | tavily_extract: N | web_search_fallback: N | web_fetch_fallback: N` with a one-line reason for any non-zero fallback count when web research was performed. **PASS**.

- [x] **AC6 — Critical Rule 12 codifies Tavily-first + bans silent fallback:** Line 490 adds rule 12 "Tavily-first for any external lookup" — requires attempting `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` before `WebSearch` / `WebFetch`, and explicitly classifies silent fallback as a process violation requiring report disclosure. **PASS**.

- [x] **AC7 — Principle 6 preserved verbatim:** Line 92 reads `6. **Source truth is king**: Verify against actual files, not just agent claims` — unchanged from pre-edit state. The new Web Research Tooling section explicitly reinforces this with a "What this does NOT change" clause referencing Principle 6. **PASS**.

- [x] **AC8 — No existing QA checklist item weakened or removed:** All ten Research Gate items (10), all twelve Synthesis Gate items (12), all nineteen Report Validation items (19), all twenty-eight Task Integrity items (28 incl. TB-Add-1..8), and the Fix Cycle protocol remain intact. Verification Principles (0-9) untouched. Critical Rules 1-11 untouched (rule 12 appended additively). **PASS**.

- [ ] **AC9 — `make verify-sync` passes after sync:** **DEFERRED to Phase 3** per Step 2.9 instructions. Sync execution and verify-sync invocation belong to the sync-and-verify phase, not this content-edit phase.

---

## Anomalies

None. All four edits landed at the proposal-specified anchors with no collateral diff. The `.claude/agents/` mirror was not touched (per instructions — sync is Phase 3).

---

**Overall Verdict:** PASS
