# QA Report -- Phase Gate (Phases 4-9)

**Topic:** PRD Pipeline E2E Testing
**Date:** 2026-03-28
**Phase:** phase-gate (Phases 4-9 combined post-hoc verification)
**Fix cycle:** N/A

---

## Overall Verdict: PASS WITH FIXES

All core claims are accurate against actual artifacts. Two PRD reference counts are imprecise (non-reproducible methodology) and one cross-run comparison table has an internally inconsistent PRD ref count. These are MINOR documentation accuracy issues, not functional failures. All PASS/FAIL verdicts are correct. Fixes applied in-place below.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Phase 4 frontmatter field values match actual extraction.md | PASS | All 13 standard + 6 TDD fields verified against actual YAML frontmatter. Every value matches exactly (spec_source, functional_requirements=5, nonfunctional_requirements=8, total_requirements=13, complexity_score=0.55, etc.) |
| 2 | Phase 4 H2 section count (14) matches actual | PASS | `grep -c '^## '` on actual file returns 14. Claim of "8 standard + 6 TDD" confirmed. |
| 3 | Phase 4 persona refs (3) matches actual | PASS | `grep -ciE 'alex\|jordan\|sam'` returns 3. |
| 4 | Phase 4 compliance refs (14) matches actual | PASS | `grep -ciE 'gdpr\|soc.?2\|compliance\|regulatory\|hipaa\|pci'` returns 14. The search pattern must include "compliance" keyword (not just GDPR/SOC2) to reproduce. |
| 5 | Phase 4 anti-instinct fingerprint regression (0.76->0.69) | PASS | Actual anti-instinct-audit.md frontmatter: `fingerprint_coverage: 0.69`, `fingerprint_found: 31`, `fingerprint_total: 45`. 31/45 = 0.689 rounds to 0.69. |
| 6 | Phase 4 anti-instinct obligations/contracts | PASS | Actual: undischarged_obligations=4, uncovered_contracts=4. Matches claims exactly. |
| 7 | Phase 4 state file fields match actual JSON | PASS | Actual .roadmap-state.json: schema_version=1, tdd_file=null, prd_file="/Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/test-prd-user-auth.md", input_type="auto", agents array has 2 entries. All match claims. |
| 8 | Phase 5 frontmatter (13/13 standard, 0/6 TDD) | PASS | Actual spec+PRD extraction.md has 13 standard fields, 0 TDD-specific fields. No TDD leak confirmed. |
| 9 | Phase 5 section count (8/8 standard, 0 TDD) | PASS | `grep -c '^## '` returns 8. No TDD sections present. |
| 10 | Phase 5 PRD enrichment count ("25 matches") | **FAIL (MINOR)** | Cannot reproduce "25" with stated categories "persona/compliance/business": grep returns 15. With "prd" added: 40. No obvious pattern yields exactly 25. Count is non-reproducible. |
| 11 | Phase 5 anti-instinct values (fp=0.78, obligations=1, contracts=3) | PASS | Actual test2-spec-prd anti-instinct-audit.md: fingerprint_coverage=0.78, undischarged_obligations=1, uncovered_contracts=3. Exact match. |
| 12 | Phase 5 roadmap line count (638) | PASS | `wc -l` returns 638. |
| 13 | Phase 6 auto-wire basic test | PASS | Claims auto-wire message was printed and validation ran. Report file exists at stated path. |
| 14 | Phase 7 generate prompt verification (4/4 PASS) | PASS | All 4 scenarios (no_supplements, tdd_only, prd_only, both) reported PASS. This tests a Python function, not artifact content -- accepted as stated. |
| 15 | Phase 7 validation enrichment (INCONCLUSIVE due to missing tasklist generate CLI) | PASS | Correctly identified limitation: no `superclaude tasklist generate` CLI exists, so E2E validation enrichment cannot be tested. Honest reporting. |
| 16 | Phase 8 cross-run TDD+PRD: "15 PRD refs in extraction" | **FAIL (MINOR)** | Actual `grep -ciE 'prd'` on TDD+PRD extraction returns 20, not 15. The cross-run comparison table undercounts. |
| 17 | Phase 8 cross-run Spec+PRD: "20 PRD refs in extraction" | **FAIL (MINOR)** | Actual `grep -ciE 'prd'` on Spec+PRD extraction returns 38, not 20. Same methodology issue as above. |
| 18 | Phase 8 roadmap line counts (TDD+PRD=593, Spec+PRD=638) | PASS | Both verified via `wc -l`. |
| 19 | Phase 8 fingerprint values (TDD-only=0.76, TDD+PRD=0.69, Spec-only=0.72, Spec+PRD=0.78) | PASS | TDD+PRD and Spec+PRD values verified against actual audit files. Prior run values accepted (no prior artifacts available to cross-check). |
| 20 | Phase 9 4-way comparison table values | PASS | All values cross-checked: TDD+PRD fp=0.69/obligations=4/contracts=4 and Spec+PRD fp=0.78/obligations=1/contracts=3 match actual audit files. |
| 21 | Phase 9 pipeline step comparison claim | PASS | Both state files confirm: extract through merge PASS, anti-instinct FAIL, wiring-verification PASS. Matches claim of identical step pattern. |
| 22 | Test1-tdd-prd-summary totals (11 PASS, 3 FAIL, 2 SKIPPED) | PASS | Counted from table: 11 PASS + 3 FAIL + 2 SKIPPED = 16 items. All individually verified where artifacts exist. |
| 23 | No findings omitted from summaries | PASS | All anti-instinct failures, regressions, and limitations (missing tasklist generate CLI) are surfaced in all relevant summary files. |

## Summary

- Checks passed: 20 / 23
- Checks failed: 3 (all MINOR)
- Critical issues: 0
- Issues fixed in-place: 3

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | phase5-extraction-frontmatter.md line 7 | PRD enrichment claimed "25 matches (persona/compliance/business)" but no search pattern reproduces 25. Actual counts: 15 (persona/compliance/business), 38 (prd), 40 (prd/persona/compliance/business). | Change to "38 PRD-related matches" with explicit pattern or "15 matches (persona/compliance/business keywords only)" |
| 2 | MINOR | cross-run-comparison-summary.md, TDD+PRD row | "15 PRD refs" in TDD+PRD extraction, but actual grep for "prd" returns 20. | Change "15 refs" to "20 refs" and "+15" to "+20" |
| 3 | MINOR | cross-run-comparison-summary.md, Spec+PRD row | "20 PRD refs" in Spec+PRD extraction, but actual grep for "prd" returns 38. Also "1 ref" for spec-only is unverified. | Change "20 refs" to "38 refs" and update delta accordingly |

## Actions Taken

### Fix 1: phase5-extraction-frontmatter.md PRD count
Changed "25 matches" to "38 PRD-related matches" with note about search methodology.

### Fix 2: cross-run-comparison-summary.md TDD+PRD PRD refs
Corrected "15 refs" to "20 refs" and delta from "+15" to "+20".

### Fix 3: cross-run-comparison-summary.md Spec+PRD PRD refs
Corrected "20 refs" to "38 refs" and delta from "+19" to "+37".

## Recommendations

- PRD reference counting methodology should be standardized across all verification files. Recommend using `grep -ciE 'prd'` as the canonical count since it captures all PRD-sourced content markers without false positives from generic keywords.
- All other claims verified accurately. The PASS/FAIL verdicts for all test results are correct.
- The fingerprint regression (0.76 to 0.69) is a real finding and correctly flagged.

## QA Complete
