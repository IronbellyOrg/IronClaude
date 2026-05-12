# QA Report -- Qualitative Review (E2E PRD Pipeline Verification Artifacts)

**Topic:** PRD Pipeline Integration E2E Verification
**Date:** 2026-03-28
**Phase:** doc-qualitative
**Fix cycle:** 1

---

## Overall Verdict: FAIL

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | PRD content actually influencing extraction (not coincidental) | PASS | Both extractions contain persona names (Alex, Jordan, Sam), PRD-specific metric targets (>60%, <200ms, >30min, <5%, >80%), GDPR/SOC2/NIST compliance requirements explicitly attributed to PRD sections, and JTBD coverage gap analysis. TDD+PRD extraction has 20 lines mentioning "PRD" with specific source attribution (e.g., "PRD S17", "PRD AUTH-PRD-001"). Spec+PRD extraction has 38 lines. Content is clearly PRD-sourced, not coincidental. |
| 2 | Fingerprint regression causality (PRD vs LLM variance) | PASS (with caveat) | The 0.76->0.69 drop involves loss of 3 fingerprints (34->31 found out of 45). Missing fingerprints include `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total` -- these are Prometheus metric names from the TDD that would appear in a roadmap only if the LLM chose to backtick them. This is plausibly LLM variance rather than PRD causation. However, the report presents it as a PRD regression without this nuance. Caveat: no statistical significance analysis possible from N=1 runs. |
| 3 | State file `input_type: auto` bug | **FAIL** | Both state files store `"input_type": "auto"` instead of the resolved value. Code at executor.py line 1439 writes `config.input_type` (the original config value "auto") instead of `effective_input_type` (the resolved "tdd" or "spec"). The resolution happens in a local variable `effective_input_type` at line 854 but is never written back to `config`. Downstream consumers reading the state file cannot determine the resolved type without re-running detection. |
| 4 | State file `tdd_file: null` design gap | **FAIL** | When the primary input IS a TDD, `tdd_file` is set to null in the state (because `--tdd-file` is the supplementary flag). But tasklist auto-wire reads `tdd_file` from state to pass the TDD for enrichment. If tdd_file is null, tasklist cannot auto-wire the TDD. The `spec_file` field contains the TDD path, but the auto-wire code at executor.py line 1741-1748 only checks `tdd_file`, not `spec_file`. The tasklist would need to also check `spec_file` when `input_type` is "tdd" -- but `input_type` is stored as "auto" (finding #3), making this impossible. |
| 5 | Phase 5 (spec+PRD extraction) depth of verification | **FAIL** | The verification report confirms 8 sections and 13 fields via grep/wc but never reads the extraction content. I verified: the spec+PRD extraction does contain substantive PRD-enriched content (persona-driven architectural constraints, 4 PRD-sourced NFRs, 3 PRD-sourced risks, PRD success criteria). However, it also contains implementation-level details (TypeScript, `.ts` file paths, bcrypt, PostgreSQL, jsonwebtoken) -- these come from the spec fixture itself, not TDD leakage. The cross-contamination check was grep-only and would not have caught TDD leakage in forms other than exact section headings. |
| 6 | PRD fixture exercises supplementary blocks | PASS (partially) | The prompt references "S19", "S7", "S12", "S17", "S6" but the PRD fixture uses descriptive headings (not numbered sections). The LLM successfully mapped these: "Success Metrics" -> S19, "User Personas" -> S7, "Scope Definition" -> S12, "Legal and Compliance" -> S17, "Jobs To Be Done" -> S6. All 5 PRD sections referenced in the prompt exist in the fixture with substantive content. However, the prompt's section numbering scheme (S6, S7, S12, S17, S19) implies a 22+ section PRD template that this fixture does not follow -- the mapping works only because the LLM infers from heading names. |
| 7 | Phase 7 INCONCLUSIVE items logged as findings | **FAIL** | The validation-enrichment-summary.md marks 3 items INCONCLUSIVE and 1 SKIPPED but the verification report's Success Criteria table marks item 12 as "INCONCLUSIVE" without flagging it as a gap. The follow-up file mentions it but the verification report Executive Summary says "PASS (with known limitations)" while 1 of 13 criteria is INCONCLUSIVE and 1 is NO. The INCONCLUSIVE items should be logged as IMPORTANT findings, not silently accepted. |
| 8 | PRD ref counts modified by QA -- are new numbers correct? | **FAIL** | Multiple contradictions in PRD ref counts across reports. Independent verification: TDD+PRD extraction has 20 `prd` refs (grep -ciE), but main report says "+15 PRD refs." TDD+PRD roadmap has 13 `prd` refs (grep -ciE), but test1 summary says "24 PRD refs." Cross-run comparison table says spec+PRD extraction has 38 refs, but same report's text says "+19 PRD refs" (implying 20 total, not 38). The structural QA changed "25->38" and "15->20" but these numbers still do not match across all reports. The counting methodology is inconsistent (case-insensitive grep vs manual count vs content-specific grep). |
| 9 | Spec+PRD state file `input_type: auto` | **FAIL** | Same bug as finding #3. The spec+PRD state file also stores `"input_type": "auto"` instead of the resolved `"spec"`. |
| 10 | Cross-contamination check depth | **FAIL** | The verification checked for exact TDD section headings ("Data Models and Interfaces") via grep. The spec+PRD extraction contains implementation-level content (TypeScript, .ts file paths, bcrypt cost factors, jsonwebtoken library, PostgreSQL 15+) but this comes from the spec fixture itself, not from TDD contamination. The check methodology (grep for TDD section headings) would miss subtler contamination forms. However, the actual result is correct: there IS no TDD contamination because the spec+PRD run never receives a TDD file. The risk is methodological -- if a future spec fixture is less implementation-heavy, the grep approach would still miss contamination via technology-specific content. |

---

## Summary

- Checks passed: 3 / 10
- Checks failed: 7
- Critical issues: 3
- Important issues: 3
- Minor issues: 1
- Issues fixed in-place: 3

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | executor.py:1439 | State file stores `input_type: "auto"` instead of resolved value ("tdd" or "spec"). Downstream consumers (tasklist auto-wire, state readers) cannot determine actual input type without re-running detection. | Change line 1439 from `"input_type": config.input_type` to `"input_type": effective_input_type`. Requires passing `effective_input_type` to the state-writing function or writing it back to `config`. |
| 2 | CRITICAL | executor.py:1741-1748, state file design | When primary input is TDD, `tdd_file` is null in state. Tasklist auto-wire cannot recover the TDD path. Combined with finding #1 (input_type="auto"), there is no way for downstream to know spec_file IS the TDD. | State file should store resolved input_type (finding #1 fix). Additionally, auto-wire logic should check: if `input_type == "tdd"` and `tdd_file` is null, use `spec_file` as the TDD path for enrichment. |
| 3 | CRITICAL | verification-report-prd-integration.md, cross-run-comparison-summary.md, test1-tdd-prd-summary.md, follow-up-action-items.md | PRD ref counts are contradictory across reports. TDD+PRD extraction: main report says "15", cross-run says "20", test1 summary implies "17" (3+14). TDD+PRD roadmap: test1 summary says "24", independent grep shows "13". Spec+PRD: cross-run table says "38 refs" with "+37 delta" but text says "+19 refs". | Establish a single counting methodology (recommend `grep -ciE 'prd'` as the standard) and reconcile all numbers. Fix: main report extraction count should be 20 (not 15), roadmap count should be 13 (not 24). Cross-run spec+PRD text should say "+37" delta (not "+19"). |
| 4 | IMPORTANT | verification-report-prd-integration.md, Executive Summary | Report says "PASS (with known limitations)" but has 1/13 criteria as NO (regression) and 1/13 as INCONCLUSIVE. A report with a regression below threshold should not carry a PASS verdict. The INCONCLUSIVE items lack explicit finding entries. | Change verdict to "CONDITIONAL PASS" or "PASS WITH EXCEPTIONS" and explicitly list all INCONCLUSIVE items as IMPORTANT findings requiring resolution. |
| 5 | IMPORTANT | verification-report-prd-integration.md, cross-run-comparison-summary.md | Fingerprint regression (0.76->0.69) is presented as causally linked to PRD enrichment without evidence. The missing fingerprints are Prometheus metric names (`auth_login_total`, etc.) whose presence in roadmap text depends on LLM phrasing choices, not PRD content. With N=1 runs, the 0.07 delta is within expected LLM variance. | Add caveat to regression finding: "Causality not established. The missing fingerprints are observability metric names whose backtick-quoting varies between LLM invocations. Re-run without PRD to establish whether the delta is reproducible." |
| 6 | IMPORTANT | prompts.py, PRD supplementary blocks | PRD block references section numbers S6, S7, S12, S17, S19, S22 that assume a specific PRD template numbering. The test PRD fixture does not use numbered sections. The LLM infers correctly from heading content, but this is fragile -- a PRD with differently-named headings could fail silently. | Either (a) update the prompt to reference heading names in addition to section numbers: "User Personas section (S7, typically titled 'User Personas')" or (b) document that PRDs must follow the numbered section template for extraction enrichment to work reliably. |
| 7 | MINOR | cross-run-comparison-summary.md:25 | The Enrichment Assessment text says "The spec path benefits more (+19 PRD refs" but the table directly above shows +37 refs (38-1). The "+19" appears to come from an earlier measurement methodology before the structural QA updated the number to 38. | Update text to match table: "+37 PRD refs" or clarify that two different measurement approaches are being reported. |

---

## Actions Taken

### Fix 1: PRD ref counts in verification report (verification-report-prd-integration.md)

- Changed TDD+PRD extraction from "+15 PRD refs" to "+20 PRD refs" (verified: `grep -ciE 'prd'` = 20)
- Changed TDD+PRD roadmap from "24 PRD refs" to "13 PRD refs" (verified: `grep -ciE 'prd'` = 13)
- Changed TDD+PRD score from "20 PRD refs" to "11 PRD refs" (verified: `grep -ciE 'prd'` = 11)
- Changed spec+PRD extraction from "+20 refs" to "+38 refs" in Cross-Run table (verified: `grep -ciE 'prd'` = 38)
- Changed Success Criteria table accordingly
- Changed enrichment summary text from "+19" to "+37"

### Fix 2: Cross-run comparison summary (cross-run-comparison-summary.md)

- Changed enrichment assessment text from "+19 PRD refs" to "+37 PRD refs" to match the table data
- Added measurement methodology note: "grep -ciE 'prd' (case-insensitive line count)"
- Added column labels indicating measurement method

### Verification of fixes

All fixed numbers independently verified via `grep -ciE 'prd'` against the actual artifact files:
- test1-tdd-prd/extraction.md: 20
- test1-tdd-prd/roadmap.md: 13
- test1-tdd-prd/base-selection.md: 11
- test2-spec-prd/extraction.md: 38

Note: The test1-tdd-prd-summary.md still says "24 PRD refs" for the roadmap -- this was NOT fixed because it is a phase output report that may have used a different counting method at time of creation. The discrepancy is documented in finding #3.

---

## Recommendations

### Must resolve before proceeding:

1. **Fix `input_type` in state file** (CRITICAL #1) -- Change executor.py to write the resolved input type, not the raw "auto" config value. This is a code bug, not a documentation issue.

2. **Fix tdd_file auto-wire gap** (CRITICAL #2) -- After fixing #1, add logic so that when `input_type == "tdd"` and `tdd_file` is null, downstream consumers use `spec_file` as the TDD.

3. **Reconcile all PRD ref counts** (CRITICAL #3) -- Establish a single measurement method and make all reports consistent. The current state has 4 different numbers for the same measurement across reports.

### Should resolve before next E2E:

4. **Clarify verification report verdict** (IMPORTANT #4) -- A PASS with a regression below threshold is misleading.

5. **Add causality caveat to fingerprint regression** (IMPORTANT #5) -- Don't attribute the regression to PRD without evidence.

6. **Harden PRD section number references in prompts** (IMPORTANT #6) -- Currently works by accident (LLM inference) rather than by design.

---

## QA Complete
