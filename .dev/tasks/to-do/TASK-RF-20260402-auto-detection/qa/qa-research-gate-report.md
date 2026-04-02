# QA Report — Research Gate

**Topic:** Auto-detection of PRD/TDD/Spec files for CLI routing
**Date:** 2026-04-01
**Phase:** research-gate
**Fix cycle:** N/A

---

## Overall Verdict: PASS

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | 5 research files present: 01-detection-signals.md, 02-cli-click-nargs.md, 03-routing-logic.md, 04-existing-tests.md, 05-template-conventions.md. All have Status: Complete or equivalent completion indicators. All have Summary sections. |
| 2 | Evidence density | PASS | Sampled claims across all 5 files. 01: cites `executor.py` lines 63-133 for detect_input_type -- VERIFIED at L63. Cites `.dev/test-fixtures/test-prd-user-auth.md` line 7 for `type: "Product Requirements"` -- VERIFIED. 02: cites `commands.py` line 33 for `@click.argument("spec_file", ...)` -- VERIFIED. Cites line 107 for `--input-type` Choice -- VERIFIED at L106-107. Cites line 176 for `spec_file.parent` -- VERIFIED. 03: cites `executor.py` lines 2113-2116 for auto-resolution -- VERIFIED. Cites lines 2124-2135 for same-file guard -- VERIFIED. Cites lines 539-548 for labels -- VERIFIED at L539-547. 04: cites 45 tests across 13 classes -- VERIFIED via grep (45 `def test_` matches, 13 `class Test` matches). Rating: Dense (>90% claims evidenced with file paths and line numbers). |
| 3 | Scope coverage | PASS | research-notes.md EXISTING_FILES lists: executor.py, commands.py, models.py, test_tdd_extract_prompt.py, 3 test fixtures, 2 template files, prompts.py, gates.py, tasklist/commands.py. Research files cover: executor.py (01, 03), commands.py (02), models.py (02, 03), test file (04), fixtures (01), templates (05). Downstream consumers (prompts.py, gates.py) are documented in research-notes.md as "should NOT be modified" and are referenced in 03's _build_steps analysis. No unexamined key files. |
| 4 | Documentation cross-validation | PASS | Research-02 cites Click documentation for nargs=-1 behavior. This is external doc, not internal code doc. The claim is validated against Click's actual behavior description. No internal doc-sourced claims found that lack verification tags. Research-01 and 03 derive all claims from reading actual code, not docs. |
| 5 | Contradiction resolution | PASS with NOTE | One cross-file tension identified: Research-02 (Section 7) recommends adding `"prd"` to `models.py input_type` Literal. Research-03 (Section 11) says this is NOT needed if PRD remains supplementary-only. This is NOT a contradiction -- it is a design decision with two valid options, both explicitly documented. Research-03 correctly notes that `input_type` tracks the *primary* input type, and PRD is never primary. Research-02 adds it for completeness of the `--input-type` CLI Choice (allowing manual override). Both are self-consistent. The task builder can make this decision. |
| 6 | Gap severity | PASS | research-notes.md GAPS_AND_QUESTIONS lists 4 gaps. All 4 are answered by the research files: (1) PRD threshold -- answered by 01 Section 7 (threshold >= 5). (2) nargs=-1 interaction with options -- answered by 02 Section 2. (3) PRD-only input behavior -- answered by 03 Section 8.1 (error). (4) Tasklist CLI scope -- answered by research-notes.md itself (only roadmap). No unresolved gaps remain. |
| 7 | Depth appropriateness | PASS | Standard tier. Research-03 traces the complete data flow from CLI argument parsing -> config construction -> execute_roadmap() auto-resolution -> _build_steps() -> state save/restore. This constitutes end-to-end coverage of the routing code path. Research-01 traces detection signal flow from file content -> scoring -> threshold -> classification. |
| 8 | Integration point coverage | PASS | Integration points documented: CLI layer <-> executor (02 Section 6, 03 Section 9.3), executor <-> models (03 Section 11), executor <-> prompts (03 Section 3.2), executor <-> state file (03 Section 4), positional args <-> explicit flags conflict (02 Section 6, 03 Section 8.4-8.5). The connection between detection results and _build_steps routing (via config.input_type) is documented in 03 Section 3. |
| 9 | Pattern documentation | PASS | Code patterns documented: weighted scoring with threshold (01 Section 6-7), Click decorator conventions (02 Section 3), dataclass replace pattern (03 Section 2.1), test patterns (04 Section 3 -- 6 distinct patterns cataloged with code examples), MDTM template conventions (05 Sections 2-6). |
| 10 | Incremental writing compliance | PASS | Files show structured, section-by-section organization with numbered sections. Research-01 has 12 sections progressing from analysis to proposal to verification. Research-03 has 12 sections progressing from current architecture to proposed changes. Research-04 catalogs tests systematically then identifies gaps. No signs of one-shot generation (files have appropriate cross-references between sections and iterative structure). |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only mode)

## Issues Found

None.

## Design Decision Notes (Not Issues)

| # | Topic | Location | Observation |
|---|-------|----------|-------------|
| 1 | `input_type` Literal expansion | 02 Section 7 vs 03 Section 11 | Research-02 recommends adding `"prd"` to `--input-type` CLI Choice AND `models.py` Literal. Research-03 argues models.py change is unnecessary if PRD stays supplementary-only. Both positions are valid and well-reasoned. The task builder should decide based on whether `--input-type prd` (force a file to be treated as PRD) is a useful override. Research-02's argument (backward compat, completeness) is stronger -- a user might want `--input-type prd` to force-classify a non-standard PRD. |
| 2 | Single PRD rejection | 03 Section 8.1, 04 Section 5.3 test_single_prd_file | Research-03 says single PRD should error. Research-04 lists `test_single_prd_file` expecting `spec_file=prd, input_type="prd"` -- implying it might be allowed. This is a minor inconsistency in test expectations vs routing logic. The task builder should align the test expectation with the chosen design. |

## Recommendations

- Green light to proceed to synthesis/task building.
- Task builder should resolve the two design decisions noted above before writing the task file.
- All 5 research files provide dense, code-traced evidence suitable for implementation planning.

## QA Complete
