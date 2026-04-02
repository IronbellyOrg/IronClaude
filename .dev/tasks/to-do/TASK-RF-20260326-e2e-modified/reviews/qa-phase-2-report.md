# QA Report -- Phase Gate (Phase 2: Create Test Fixtures)

**Topic:** E2E Pipeline Tests -- TDD and Spec Paths in Modified Repo
**Date:** 2026-03-27
**Phase:** phase-gate
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | TDD fixture: All [bracket] placeholders replaced | PASS | `grep -c '\[FEATURE-ID\]'` returns 0; `grep -c '\[version\]'` returns 0; `grep -nE '\[[A-Z][A-Z_-]+\]'` returns no matches. No bracket placeholders remain. |
| 2 | TDD fixture: feature_id="AUTH-001" | PASS | `grep -c 'feature_id: "AUTH-001"'` returns 1. Frontmatter line 15: `feature_id: "AUTH-001"`. |
| 3 | TDD fixture: Backticked identifiers present | PASS | All 9 required identifiers present with substantial usage: UserProfile(28), AuthToken(19), AuthService(55), TokenManager(38), JwtService(27), PasswordHasher(31), LoginPage(21), RegisterPage(17), AuthProvider(16). |
| 4 | TDD fixture: Sections 5,6,7,8,10,15,19,20,24,25 populated | PASS | Verified each section has substantial content: Sec 5 (Technical Requirements, lines 277-310): 5 FRs + 3 NFRs with tables. Sec 6 (Architecture, lines 313-362): ASCII diagram + design decisions table. Sec 7 (Data Models, lines 365-422): TypeScript interfaces for UserProfile and AuthToken + field tables. Sec 8 (API Specifications, lines 425-568): 4 endpoints with request/response schemas. Sec 10 (Component Inventory, lines 578-608): route table + 3 components. Sec 15 (Testing Strategy, lines 644-684): test pyramid + test cases. Sec 19 (Migration & Rollout, lines 705-737): 3-phase rollout + feature flags + rollback. Sec 20 (Risks & Mitigations, lines 741-748): 3 risks in table. Sec 24 (Release Criteria, lines 792-812): 5-item DoD + release checklist. Sec 25 (Operational Readiness, lines 816-841): 2 runbook scenarios + on-call table + capacity planning. |
| 5 | TDD fixture: Auto-detection score >= 3 | PASS | Signal 1: 67 numbered headings (>= 10) = +3. Signal 2: feature_id (+1), parent_doc (+1), authors (+1), quality_scores (+1), coordinator (+1) = +5. Signal 3: "Data Models" (+1), "API Specifications" (+1), "Component Inventory" (+1), "Testing Strategy" (+1), "Operational Readiness" (+1), "Migration & Rollout" (+1), "State Management" (+1), "Performance Budgets" (+1), "Accessibility Requirements" (+1) = +9. Signal 4: "Technical Design Document" in first 1000 chars = +2. Total: 19. Well above threshold of 3. |
| 6 | Spec fixture: All {{SC_PLACEHOLDER:...}} replaced | PASS | `grep -c '{{SC_PLACEHOLDER:'` returns 0. No sentinels remain. |
| 7 | Spec fixture: FR-AUTH and NFR-AUTH identifiers present | PASS | `grep -c 'FR-AUTH'` returns 20; `grep -c 'NFR-AUTH'` returns 3. Both identifier families present throughout. |
| 8 | Spec fixture: Follows release-spec-template structure | PASS | 12 top-level numbered sections matching the template: Problem Statement, Solution Overview, Functional Requirements, Architecture, Interface Contracts, Non-Functional Requirements, Risk Assessment, Test Plan, Migration & Rollout, Downstream Inputs, Open Items, Brainstorm Gap Analysis. Frontmatter fields match template schema (title, version, status, feature_id, spec_type, complexity_score, complexity_class, target_release, authors, quality_scores). |
| 9 | Spec fixture: NOT TDD structure | PASS | No "Technical Design Document" text (0 occurrences). No TDD-specific sections like "API Specifications", "Component Inventory", "Testing Strategy", "Operational Readiness", "State Management", "Performance Budgets", "Accessibility Requirements". Title is "User Authentication Service" not a TDD title. Frontmatter lacks TDD-specific fields: parent_doc, coordinator. |
| 10 | Spec fixture: Must NOT trigger TDD auto-detection | **FAIL** | Calculated auto-detection score for the spec fixture using `detect_input_type()` algorithm: Signal 1: 12 `## N.` headings >= 10 = +3. Signal 2: feature_id (+1) + authors (+1) + quality_scores (+1) = +3. Signal 3: "Data Models" (+1) + "Migration & Rollout" (+1) = +2. Signal 4: 0. **Total score: 8 (threshold is >= 3 = TDD).** The spec fixture WILL be classified as TDD by the auto-detection algorithm. |
| 11 | TDD sentinel check result file exists and shows PASS | PASS | File at `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/phase-outputs/test-results/phase2-tdd-sentinel-check.md` exists, contains "Result: PASS (after fix)", and all individual checks show PASS. |
| 12 | Spec sentinel check result file exists and shows PASS | PASS | File at `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/phase-outputs/test-results/phase2-spec-sentinel-check.md` exists, contains "Result: PASS", and all individual checks show PASS. |

---

## Summary

- Checks passed: 11 / 12
- Checks failed: 1
- Critical issues: 1
- Issues fixed in-place: 0

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `.dev/test-fixtures/test-spec-user-auth.md` | Spec fixture triggers TDD auto-detection with score 8 (threshold >= 3). Three independent signal sources each contribute enough to exceed the threshold on their own: (a) 12 `## N.` numbered headings = +3, (b) frontmatter fields `feature_id`, `authors`, `quality_scores` = +3, (c) section names "Data Models" and "Migration & Rollout" = +2. Even removing the section name signals (c), the score would be 6, still double the threshold. The root cause is that the release-spec-template shares structural patterns with TDD documents (numbered headings, same frontmatter field names), making it impossible for a faithfully-populated spec to score below 3 with the current detection algorithm. | **Two-part fix required.** Part A (content fix -- can do now): Rename `### 4.5 Data Models` to `### 4.5 Entity Definitions` and rename `## 9. Migration & Rollout` to `## 9. Rollout Strategy` to eliminate Signal 3 matches (-2 points, score drops to 6). Part B (structural note): Even after Part A, score remains 6 due to Signal 1 (numbered headings) and Signal 2 (shared frontmatter fields). The spec fixture cannot score below 3 while following the release-spec-template structure. This is a **detection algorithm design issue** -- the threshold or signals need adjustment in `src/superclaude/cli/roadmap/executor.py:detect_input_type()`. Either: (i) increase threshold from 3 to at minimum 7, (ii) reduce Signal 1 weight for lower heading counts (12 is not the same as 28), or (iii) exclude fields that appear in both templates from Signal 2. **For Phase 2 to pass, Part A should be applied and the detection limitation documented for Phase 3 dry-run verification.** |

---

## Actions Taken

**Fix 1 (Part A -- content-level TDD signal removal):**
- Renamed `### 4.5 Data Models` to `### 4.5 Entity Definitions` in `.dev/test-fixtures/test-spec-user-auth.md`
- Renamed `## 9. Migration & Rollout` to `## 9. Rollout Strategy` in `.dev/test-fixtures/test-spec-user-auth.md`
- Verified: `grep -c 'Data Models' spec` now returns 0; `grep -c 'Migration & Rollout' spec` now returns 0
- **Effect on score:** Signal 3 reduced from +2 to +0. New total: 6 (was 8). Still above threshold of 3.
- **Remaining issue:** Score of 6 is caused by Signal 1 (12 `## N.` headings = +3) and Signal 2 (3 shared frontmatter fields = +3). These are structural features of the release-spec-template itself and cannot be removed without violating criterion 5 (follows release-spec-template structure). **This is a bug in `detect_input_type()` -- the threshold of 3 is too low given that a standard spec template scores 6 on Signals 1+2 alone.**

---

## Recommendations

1. **BLOCKING (for Phase 3):** The spec fixture will be classified as TDD by `detect_input_type()` during the Phase 3 dry-run. Item 3.2 explicitly requires stderr to contain "Auto-detected input type: spec" -- this will fail with the current detection algorithm. Before proceeding to Phase 3, either:
   - (a) Fix `detect_input_type()` in `src/superclaude/cli/roadmap/executor.py` to raise the threshold or adjust signal weights so that a populated release-spec-template does not score >= 3, OR
   - (b) Use the `--input-type spec` CLI flag to override auto-detection for the spec fixture test (if supported), and document the auto-detection bug separately.

2. **Non-blocking:** The section renames ("Entity Definitions", "Rollout Strategy") are reasonable synonyms that preserve meaning. However, they deviate from the literal release-spec-template section names. If exact template fidelity is required for pipeline parsing, these renames may need to be reverted and the detection algorithm fixed instead.

---

## QA Complete
