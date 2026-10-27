# Agent D5 — Domain Validation Report: pipeline_fixes

**Agent**: D5
**Domain**: pipeline_fixes
**Date**: 2026-03-23
**Spec**: v3.3-requirements-spec.md
**Roadmap**: v3.3-TurnLedger-Validation/roadmap.md
**Output dir**: ValidationSonnet/

---

## Scope

Requirements validated: REQ-044, REQ-045, REQ-046, REQ-047, REQ-048, REQ-049, REQ-SC10, REQ-SC11, REQ-RISK3

---

## Requirement Evaluations

### REQ-044: FR-5.1 production change — 0-files-analyzed guard with specific condition and failure_reason field

- Spec source: FR-5.1 (Pipeline Fixes section)
- Spec text: "In `run_wiring_analysis()` (wiring_gate.py:673+), after file collection: If `files_analyzed == 0` AND the source directory is non-empty (contains *.py files): return a FAIL report (not a clean PASS). The FAIL report must include: `failure_reason: \"0 files analyzed from non-empty source directory\"`"
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Phase 3A, Task 3A.1
  - Roadmap text: "Add assertion: if `files_analyzed == 0` AND source dir non-empty → return FAIL with `failure_reason`"
- Finding:
  - Severity: MEDIUM
  - Gap description: The roadmap captures the logical condition (`files_analyzed == 0` AND source dir non-empty → return FAIL) and references the `failure_reason` field generically. However, the roadmap does not quote the required literal string value `"0 files analyzed from non-empty source directory"`. The spec prescribes the exact field name AND its exact string value — both are load-bearing for any automated assertion or contract test downstream. The roadmap says "return FAIL with `failure_reason`" without specifying the string, leaving implementation latitude that could produce a different message string and still satisfy the roadmap's description.
  - Impact: An implementer reading only the roadmap could produce a `failure_reason` of any arbitrary string (e.g., `"no files collected"` or `"source_dir empty scan result"`). Any test that asserts the specific string from the spec would fail. Third-party audits comparing output to spec would flag the mismatch.
  - Recommended correction: Amend roadmap 3A.1 to include the exact required string: "return FAIL with `failure_reason: \"0 files analyzed from non-empty source directory\"`" matching the spec verbatim.
- Confidence: HIGH

---

### REQ-045: FR-5.1 test — non-empty dir where collection returns 0 files; assert FAIL not silent PASS

- Spec source: FR-5.1 test paragraph
- Spec text: "Point `run_wiring_analysis()` at a non-empty directory where file collection returns 0 analyzed files (e.g., all files filtered out by extension or path rules). Assert FAIL, not silent PASS."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 3B, Task 3B.1
  - Roadmap text: "Test: 0-files-analyzed on non-empty dir → FAIL, not silent PASS"
- Finding: None
- Confidence: HIGH

---

### REQ-046: FR-5.2 production change — new check phase reads spec FR-* items, searches codebase for implementation evidence, reports gaps

- Spec source: FR-5.2 (Impl-vs-Spec Fidelity Check)
- Spec text: "A new check phase that: 1. Reads the spec's declared functional requirements (FR-* items) 2. For each FR, searches the implementation codebase for evidence of implementation (function names, class names, docstring references) 3. Reports FRs with no implementation evidence as gaps"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 3A, Task 3A.2
  - Roadmap text: "New: `src/superclaude/cli/roadmap/fidelity_checker.py` — Impl-vs-spec fidelity checker: reads spec FRs, searches codebase for function/class name evidence, reports gaps"
- Finding: None
- Confidence: HIGH

---

### REQ-047: FR-5.2 integration point — runs as additional checker in _run_checkers() alongside structural and semantic layers

- Spec source: FR-5.2 integration point paragraph
- Spec text: "Integration point: Runs as an additional checker in `_run_checkers()` alongside structural and semantic layers."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 3A, Task 3A.3; also Appendix A.6
  - Roadmap text (3A.3): "`src/superclaude/cli/roadmap/executor.py` — `_run_checkers()` checker registry — Wire `fidelity_checker` into `_run_checkers()` alongside structural and semantic layers"
  - Roadmap text (A.6): "Phase 3 adds impl-vs-spec fidelity checker (FR-5.2)" and "additions must preserve ordering, output shape, and failure aggregation"
- Finding: None
- Confidence: HIGH

---

### REQ-048: FR-5.2 test — positive case (checker finds function) AND negative case (checker flags gap after removal)

- Spec source: FR-5.2 test paragraph
- Spec text: "Create a spec with an FR that references a function. Assert the checker finds it. Remove the function. Assert the checker flags the gap."
- Status: PARTIAL
- Match quality: WEAK
- Evidence:
  - Roadmap location: Phase 3B, Task 3B.3
  - Roadmap text: "Test: impl-vs-spec checker finds gap in synthetic test with missing implementation"
- Finding:
  - Severity: HIGH
  - Gap description: The spec mandates a two-part test scenario: (a) a positive case — checker FINDS the function when it exists — AND (b) a negative case — checker FLAGS the gap after the function is removed. The roadmap task 3B.3 describes only the negative case: "finds gap in synthetic test with missing implementation." The positive case (confirming the checker correctly identifies existing implementations and does not false-positive on a valid codebase) is absent from the roadmap description. Without the positive case, the test would not verify that the checker can distinguish between present and absent implementations.
  - Impact: If only the negative case is implemented, the checker could be trivially implemented as "always flag everything" and the test would pass. The positive case is required to validate that the checker does not have an unacceptably high false-positive rate (which also links to REQ-RISK3). An auditor reviewing SC-11 ("impl-vs-spec fidelity check exists, finds and flags missing implementations") could accept a test that only demonstrates flagging but never demonstrates correct detection.
  - Recommended correction: Amend roadmap 3B.3 to read: "Tests: (1) positive — spec FR references existing function; assert checker finds evidence, no gap flagged; (2) negative — remove function; assert checker flags gap. Both cases required to satisfy FR-5.2 test requirement."
- Confidence: HIGH

---

### REQ-049: FR-5.3 = FR-4 cross-reference for traceability

- Spec source: FR-5.3
- Spec text: "This IS FR-4. Cross-referenced here for traceability."
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Executive Summary paragraph 1; Phase 3 overview; Phase 3A Task 3A.4
  - Roadmap text (Executive Summary): "three targeted production code changes: a 0-files-analyzed assertion fix (FR-5.1), an impl-vs-spec fidelity checker (FR-5.2), and a new AST-based reachability eval framework (FR-4)"
  - Roadmap text (3A.4): "`src/superclaude/cli/audit/reachability.py` — Add `GateCriteria`-compatible interface: reads manifest, runs AST analysis, produces structured PASS/FAIL report"
- Finding: None — the cross-reference between FR-5.3 and FR-4 is implicit throughout the roadmap by treating them as the same work item. FR-4 is covered in Phase 1B (analyzer), Phase 3 (gate integration), and the roadmap correctly treats them as one deliverable.
- Confidence: HIGH

---

### REQ-SC10: SC-10 — 0-files assertion added, test proves it

- Spec source: Success Criteria table, SC-10
- Spec text: "SC-10 | 0-files-analyzed produces FAIL | Assertion added, test proves it | 3"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Success Criteria Validation Matrix, SC-10; Phase 3B Task 3B.1; Phase 3 Validation Checkpoint C
  - Roadmap text (matrix): "SC-10 | 0-files → FAIL | FR-5.1 assertion test | 3 | Yes"
  - Roadmap text (checkpoint): "SC-7, SC-9, SC-10, SC-11 validated"
- Finding: None
- Confidence: HIGH

---

### REQ-SC11: SC-11 — impl-vs-spec fidelity check exists, finds and flags missing implementations

- Spec source: Success Criteria table, SC-11
- Spec text: "SC-11 | Impl-vs-spec fidelity check exists | New checker finds and flags missing implementations | 3"
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Success Criteria Validation Matrix, SC-11; Phase 3B Task 3B.3; Phase 3 Validation Checkpoint C
  - Roadmap text (matrix): "SC-11 | Fidelity checker finds gap | FR-5.2 synthetic test | 3 | Yes"
  - Roadmap text (checkpoint): "Fidelity checker detects missing implementations."
- Finding:
  - Severity: MEDIUM
  - Gap description: SC-11 requires that the checker "finds AND flags missing implementations" — the spec formulation implies both detection capability (finding) and reporting capability (flagging). The roadmap's validation description collapses this to "finds gap" (3B.3) and "detects missing implementations" (checkpoint C). This is semantically close but inherits the gap noted in REQ-048: the roadmap's test description omits the positive-case validation. SC-11 cannot be considered fully validated if only the negative case is tested, since there is no proof that "finds" (i.e., correctly identifies present implementations) is working.
  - Impact: SC-11 reads as a release gate. If it is accepted based solely on the negative test, the release may ship a fidelity checker with an undetected false-positive problem.
  - Recommended correction: Tie SC-11 validation explicitly to the two-part test from 3B.3 once that task is corrected per REQ-048's recommendation. Update the SC-11 matrix row to: "Validation Method: positive + negative synthetic test (FR-5.2 two-part test)."
- Confidence: HIGH

---

### REQ-RISK3: R-3 — impl-vs-spec checker false positives: exact matching only, fail-open on ambiguous, synthetic positive and negative tests

- Spec source: Risk Assessment table, R-3
- Spec text: "Impl-vs-spec checker has high false-positive rate | MEDIUM | Start with exact function-name matching; iterate on NLP matching in v3.4"
- Spec (full mitigations from task prompt): "start with exact function-name/class-name matching; no NLP/fuzzy; fail-open on ambiguous; synthetic positive and negative tests"
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Risk Assessment table, R-3; Open Questions section, item 2; Appendix A.6
  - Roadmap text (R-3): "Start with exact function-name + class-name matching only; no NLP/fuzzy matching; fail-open on ambiguous matches (log warning, don't block); add synthetic positive and negative tests before enabling broad assertions"
  - Roadmap text (exit criteria for R-3): "Checker passes known-good synthetic cases and flags known-bad synthetic cases with low ambiguity"
  - Roadmap text (Open Questions #2): "Require exact function-name or class-name match as minimum evidence. Docstring FR-ID citations are bonus evidence, not required. This minimizes R-3 false positives."
- Finding:
  - Severity: LOW
  - Gap description: The roadmap R-3 mitigation text is substantively correct and covers all three mandated mitigations: exact matching, fail-open, and synthetic tests. The gap is execution-level: task 3B.3 (the only test task for the fidelity checker) does not mention the positive synthetic test case (see REQ-048). The R-3 exit criteria states "passes known-good synthetic cases AND flags known-bad synthetic cases" — but if 3B.3 is only written as a negative test, the exit criterion cannot be confirmed at checkpoint C. The risk mitigation is well-specified in the risk table but the corresponding test task does not yet enforce it.
  - Impact: R-3 exit criteria may be declared met at Checkpoint C without the positive test existing, creating a documentation-reality mismatch. Low severity because the risk table itself is correct — this is a cross-reference gap, not a missing mitigation concept.
  - Recommended correction: Explicitly cross-reference 3B.3 from the R-3 exit criteria row and from Open Questions #2. Ensure 3B.3 is corrected per REQ-048's recommendation (two-part test), so R-3 exit criteria can be mechanically verified at Checkpoint C.
- Confidence: HIGH

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total requirements evaluated | 9 |
| COVERED | 5 |
| PARTIAL | 4 |
| MISSING | 0 |
| CONFLICTING | 0 |
| IMPLICIT | 0 |

| Severity distribution (findings only) |  |
|----------------------------------------|--|
| CRITICAL | 0 |
| HIGH | 1 (REQ-048) |
| MEDIUM | 2 (REQ-044, REQ-SC11) |
| LOW | 1 (REQ-RISK3) |

| Match quality distribution |  |
|---------------------------|--|
| EXACT | 4 |
| SEMANTIC | 3 |
| WEAK | 1 |
| NONE | 0 |

---

## Key Findings Summary

1. **REQ-044 / MEDIUM**: Roadmap 3A.1 captures the logical condition for the 0-files guard but omits the required literal `failure_reason` string value. Implementer has latitude to produce any string.

2. **REQ-048 / HIGH**: Roadmap 3B.3 covers only the negative test case (missing implementation flagged). The spec explicitly requires BOTH a positive case (checker finds existing function) and a negative case (checker flags removed function). This is the most significant gap in the domain.

3. **REQ-SC11 / MEDIUM**: Inherits the 3B.3 gap. SC-11 as a release gate cannot be fully validated with only a one-sided test.

4. **REQ-RISK3 / LOW**: R-3 mitigation is correctly specified in the risk table and open questions. The gap is that task 3B.3 does not yet enforce the R-3 exit criteria for the positive test case. Correcting 3B.3 (per REQ-048) resolves this finding as well.

---

## Confidence Assessment

All evaluations are rated HIGH confidence. Both source documents were read in full. The spec language for FR-5.1 through FR-5.3, SC-10, SC-11, and R-3 is unambiguous. The roadmap language for 3A.1–3A.4 and 3B.1–3B.3 is explicit enough to evaluate against spec requirements without inference chains longer than one step.
