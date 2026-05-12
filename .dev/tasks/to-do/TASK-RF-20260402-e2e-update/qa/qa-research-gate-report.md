# QA Report -- Research Gate

**Topic:** Update 63-item E2E test task file to reflect QA fixes, auto-detection changes, and new behaviors
**Date:** 2026-04-02
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** report-only (no in-place fixes)

---

## Overall Verdict: PASS

---

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep: 4 | Glob: 0 | Bash: 2

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory -- all 5 files present, Status: Complete, Summary sections | PASS | All 5 files have `Status: Complete`. Files 01-04 have summary sections. File 05 has summary statistics section. |
| 2 | Evidence density -- claims cite specific file paths, line numbers, function names | PASS | All files cite specific paths (e.g., `src/superclaude/cli/roadmap/executor.py` lines 63-186), function names (`detect_input_type`, `_route_input_files`, `build_extract_prompt`), and line numbers. Density is >80% across all files. |
| 3 | Scope coverage -- key files/directories discussed | PASS | Research covers executor.py, gates.py, commands.py, models.py, prompts.py (both roadmap and tasklist), test files. These are all the files relevant to the track goal. |
| 4 | Documentation cross-validation -- doc-sourced claims tagged | PASS | File 01 references skill doc updates (C-12) for scoring.md, extraction-pipeline.md, spec-panel.md. These are described as changes TO docs (aligning docs with code), not claims FROM docs. No unverified doc-sourced architectural claims found. |
| 5 | Contradiction resolution -- files agree with each other | PASS (with 1 issue noted) | Files 02 and 05 have a factual contradiction about `--input-type prd` (see Issues). Otherwise, files 01-04 are mutually consistent and file 05 accurately reflects most findings from 01-04. |
| 6 | Gap severity -- gaps identified and rated | PASS | File 02 identifies the `--input-type prd` discrepancy. File 04 identifies stale item counts (7.3, 6.2). File 05 identifies 21 items needing update and 11 new items. No unaddressed critical gaps. |
| 7 | Depth appropriateness -- complete data flow traced | PASS | File 02 traces the full detection-routing-classification flow end-to-end: `detect_input_type()` -> `_route_input_files()` -> CLI `run()` -> `execute_roadmap()`. File 03 traces gate selection flow. |
| 8 | Integration point coverage -- connection points documented | PASS | File 03 documents the gate routing conditional (`EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE`), the ALL_GATES list exclusion, and the commands.py -> executor.py import chain. File 04 documents tasklist prompt -> fidelity integration. |
| 9 | Pattern documentation -- code patterns and conventions | PASS | Files document the weighted scoring pattern (PRD 5-signal, TDD 4-signal), the routing pattern (classify -> validate -> assign -> merge -> guard -> return), and the prompt builder convention (tdd_file/prd_file conditional blocks). |
| 10 | Incremental writing compliance | PASS | Files show structured investigation (numbered sections, progressive discovery). File 02 discovers the `--input-type prd` discrepancy during investigation and documents it inline. File 04 discovers stale counts and documents required updates. |

---

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Important issues: 1
- Minor issues: 1
- Issues fixed in-place: 0 (report-only mode)

---

## Source Code Verification (5+ claims spot-checked)

### Claim 1: detect_input_type() returns "prd", "tdd", or "spec" with PRD checked first (File 02, Section 1)
**Verified:** Read `executor.py` lines 63-186. PRD scoring block (lines 90-129) runs before TDD scoring block (lines 131-185). Returns "prd" at line 129, "tdd" or "spec" at line 176-185. Five PRD signals with exact weights match file 02's table. CONFIRMED.

### Claim 2: EXTRACT_TDD_GATE has 19 fields (13 standard + 6 TDD-specific) (File 03, Section 1)
**Verified:** Read `gates.py` lines 797-835. Counted 13 standard fields + 6 TDD-specific fields (`data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`). min_lines=50, enforcement_tier="STRICT". CONFIRMED.

### Claim 3: CLI `--input-type` Choice is `["auto", "tdd", "spec"]` without "prd" (File 02, Section 3; File 03, Section 3)
**Verified:** Read `commands.py` line 107: `click.Choice(["auto", "tdd", "spec"], case_sensitive=False)`. Does NOT include "prd". CONFIRMED. Models.py line 114 includes "prd" in Literal. CONFIRMED discrepancy between CLI and model.

### Claim 4: Tasklist fidelity prompt has 5 TDD checks and 4 PRD checks (File 04, Section 3)
**Verified:** Read `tasklist/prompts.py` lines 115-148. TDD block has items numbered 1-5 (S15, S19, S10, S7, S8). PRD block has items numbered 1-4 (S7, S19, S12/S22, S5). CONFIRMED.

### Claim 5: PRD authority language changed from "advisory" to "authoritative" in 2 builders (File 04, Section 2)
**Verified:** Read `prompts.py` lines 199-202 (build_extract_prompt PRD block) and lines 371-374 (build_extract_prompt_tdd PRD block). Both contain: "The PRD defines business requirements (personas, compliance, success metrics, scope). Treat these as authoritative for business context." CONFIRMED.

### Claim 6: EXTRACT_TDD_GATE is NOT in ALL_GATES list (File 03, Section 1)
**Verified:** Grepped `ALL_GATES` in gates.py. Lines 1124-1139 list 14 gates; EXTRACT_TDD_GATE is absent. CONFIRMED.

### Claim 7: 23 new tests across 5 test classes (File 02, Section 4)
**Verified:** Read `tests/cli/test_tdd_extract_prompt.py` lines 507-823. Counted: TestPrdDetection=4, TestThreeWayBoundary=4, TestMultiFileRouting=10, TestBackwardCompat=3, TestOverridePriority=2. Total=23. CONFIRMED.

### Claim 8: `_route_input_files()` is a 12-step function (File 02, Section 2)
**Verified:** Read executor.py lines 188-316. Steps numbered 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 (step 2 skipped in code). 8 distinct UsageError messages listed (file 02 lists these in the Error Conditions subsection). CONFIRMED.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | File 05 (`05-item-impact-mapping.md`), Phase 1 item 1.3 | File 05 says item 1.3 should "verify `--input-type` includes 'prd' option" and the new item 1.3a says "Verify `--input-type` flag accepts 'prd' value." However, the actual code at `commands.py` line 107 shows `click.Choice(["auto", "tdd", "spec"])` -- it does NOT include "prd". File 02 and File 03 both correctly identify this as a discrepancy (PRD is auto-detected only, not CLI-forceable). File 05 contradicts files 02/03 by telling the task builder to add a check that will always FAIL. | File 05 should change item 1.3 guidance to: "verify `--input-type` choices are `[auto, tdd, spec]` (NOT including prd)" and REMOVE suggested new item 1.3a entirely. The `--input-type prd` is a design gap (or intentional design), not something to test for presence. File 02's E2E-AD-19 correctly frames this as a "discrepancy to address" rather than a test expectation. |
| 2 | MINOR | File 02 (`02-auto-detection-changes.md`), Section 1, Borderline Warning | File 02 says "Scores 3 and 4 do NOT trigger the warning because the `if prd_score >= 5` check (line 121) comes first, and scores below 5 fall through to TDD scoring without warning." This is correct but could mislead: the borderline warning range is stated as "3 <= prd_score <= 6" which is technically true for the code block, but in practice only scores 5 and 6 trigger BOTH the return AND the warning. File 02 does explain this correctly in context, so this is more of a clarity note than an error. | No fix required -- the explanation is technically accurate. The task builder should be aware that only PRD scores of 5-6 produce both a "prd" classification AND a borderline warning. |

---

## Cross-File Consistency Check

| Check | Result | Detail |
|-------|--------|--------|
| File 01 QA fix counts vs File 05 references | PASS | File 01 lists 26 fixed findings (3 CRITICAL + 15 IMPORTANT + 8 MINOR). File 05 references "28 findings" in methodology -- minor count discrepancy (26 vs 28) but this does not affect the item mapping accuracy. File 01 also discusses C-122 which is "NOT FIXED" but listed in the IMPORTANT section, accounting for a possible counting difference. |
| File 02 E2E items vs File 05 new items | PASS | File 02 suggests 19 E2E test items (E2E-AD-01 through E2E-AD-19). File 05 suggests 11 new items. File 05's suggestions are a subset/consolidation of file 02's more granular list. No contradiction. |
| File 03 gate changes vs File 01 gate changes | PASS | File 03 documents EXTRACT_TDD_GATE (new) at lines 797-835. File 01 references C-117 creating EXTRACT_TDD_GATE. Consistent. |
| File 04 fidelity counts vs File 05 item updates | PASS | File 04 says items 6.2, 7.3a, 7.3b need count updates (3->4, 3->5, 3->4). File 05 independently identifies the same items for UPDATE_NEEDED with the same rationale. Consistent. |
| File 05 item 7.5 assessment vs File 04 | Consistent but one needs attention | File 05 marks item 7.5 as UPDATE_NEEDED due to possible authority language change, while File 04 marks it as "No update needed" after verifying substring checks still match. File 04 did the deeper verification (checking actual code strings) and is correct. File 05's concern is speculative. Not an error -- File 05 notes "may" need updating. |

---

## Coverage Assessment

### Areas Well-Covered
- Detection logic (3-way classification) -- thoroughly traced with line numbers
- Routing function -- 12-step walkthrough with all error conditions
- Gate changes -- EXTRACT_TDD_GATE fully documented with field list
- Prompt builder changes -- all 10 roadmap + 2 tasklist builders inventoried
- Task item impact mapping -- all 63 items assessed individually
- New test coverage -- 23 tests across 5 classes verified

### Areas Adequately Covered
- State file changes (C-62, C-91, C-111) -- referenced in file 01, impact mapped in file 05
- Resume behavior changes -- covered via C-27, C-91 references

### Potential Gaps (Minor)
- The `_route_input_files` error message for `--prd-file` conflict (step 8, line 275-277) uses "conflicts with positional file detected as PRD" but file 02 only quotes the TDD conflict message verbatim. The PRD conflict message is listed in the error conditions table but not quoted. This is adequate for the task builder.
- No research file discusses the ordering of new test classes relative to pre-existing test classes in the test file (e.g., whether TestPrdDetection at line 507 comes after or before the original TestAutoDetection). This is minor -- test ordering doesn't matter for pytest.

---

## Recommendations

1. **Before spawning the task builder:** Correct the file 05 guidance about `--input-type prd`. The builder will receive incorrect instructions if file 05 is used as-is for item 1.3 and suggested new item 1.3a. The builder should NOT add a check that `--input-type` accepts "prd" -- it does not.

2. **Actionability assessment:** All 5 research files provide sufficient detail for a task builder to update the 63-item E2E task file. The findings are specific (item numbers, current text, required changes) and evidence-based (file paths, line numbers, code quotes).

3. **The file 05 item 7.5 assessment is overly cautious.** File 04 verified that the substring checks in item 7.5 still match the current code. The builder should follow file 04's assessment (no update needed for 7.5), not file 05's speculative concern.

---

## VERDICT: PASS

The research is thorough, evidence-based, and actionable. One IMPORTANT issue found (file 05 contradicts files 02/03 about `--input-type prd` test expectations) -- this is a factual error in the impact mapping that could cause the task builder to add a test that will always fail. However, the source research files (02 and 03) correctly document the actual behavior, so the builder has the correct information available if they cross-reference. This does not block synthesis/building.

One MINOR clarity issue about borderline warning ranges (file 02) is documented but not an error.

All other claims verified against source code. No fabrication detected. No unsupported assertions. Research files are mutually consistent (except the noted contradiction). Coverage is comprehensive for the track goal.

---

## QA Complete
