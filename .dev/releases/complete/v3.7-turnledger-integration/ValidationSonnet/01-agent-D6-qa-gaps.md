# Agent D6 — QA Gaps Domain Validation Report

**Domain**: qa_gaps
**Agent**: D6
**Spec file**: v3.3-requirements-spec.md
**Roadmap**: roadmap.md
**Date**: 2026-03-23

---

## Assigned Requirements

| REQ ID | Title |
|--------|-------|
| REQ-050 | FR-6.1 T07 — Write 7 tests in tests/roadmap/test_convergence_wiring.py |
| REQ-051 | FR-6.1 T11 — Write 6 tests for v3.3-SC-1 through v3.3-SC-6 in tests/roadmap/test_convergence_e2e.py |
| REQ-052 | FR-6.1 T12 — Write smoke test for convergence path in test_convergence_e2e.py |
| REQ-053 | FR-6.1 T14 — Regenerate wiring-verification artifact + validate |
| REQ-054 | FR-6.2 T02 — run_post_phase_wiring_hook() already wired — write confirming test |
| REQ-055 | FR-6.2 T17-T22 — Integration tests, regression suite, gap closure audit |
| REQ-SC8 | SC-8 — All QA gaps closed: v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22 |

---

## Detailed Findings

### REQ-050: FR-6.1 T07 — Write 7 tests in tests/roadmap/test_convergence_wiring.py

- Spec source: FR-6.1 (v3.05 Gaps table), Test File Layout section
- Spec text: "T07 | `tests/roadmap/test_convergence_wiring.py` — 7 tests | Write tests"
- Status: PARTIAL
- Match quality: WEAK
- Evidence:
  - Roadmap location: Phase 2D, task 2D.1
  - Roadmap text: "2D.1 | FR-6.1 T07 | `tests/roadmap/test_convergence_wiring.py` | Extend existing 7 tests (verify already present, add any missing)"
- Finding:
  - Severity: HIGH
  - Gap description: The spec says "Write tests" — 7 tests must be written in `test_convergence_wiring.py`. The roadmap reframes this as "Extend existing 7 tests (verify already present, add any missing)." This is a semantic substitution: the spec mandates writing 7 specific tests; the roadmap treats it as a possible no-op ("verify already present"). If the tests are already present, the roadmap allows passing without writing anything. The spec does not state that existing tests can satisfy T07 — it identifies T07 as an open gap requiring action. The roadmap also omits any explicit count guarantee: it does not state that after 2D.1, exactly 7 tests exist, only that it will "verify" and "add any missing."
  - Impact: The gap could be declared closed without writing any new tests if prior tests are deemed sufficient. The 7-test count is the spec's enumerated deliverable; a "verify existing" approach does not guarantee that deliverable is met.
  - Recommended correction: Roadmap 2D.1 should state: "Write 7 tests in `tests/roadmap/test_convergence_wiring.py`. If any tests are already present, count them toward the 7 and write remaining tests to reach exactly 7. Deliverable: file contains exactly 7 named test functions covering convergence wiring points."
- Confidence: HIGH

---

### REQ-051: FR-6.1 T11 — Write 6 tests for v3.3-SC-1 through v3.3-SC-6 in tests/roadmap/test_convergence_e2e.py

- Spec source: FR-6.1 (v3.05 Gaps table), Test File Layout section
- Spec text: "T11 | `tests/roadmap/test_convergence_e2e.py` — 6 tests for v3.3-SC-1 through v3.3-SC-6 | Write tests"
- Status: PARTIAL
- Match quality: WEAK
- Evidence:
  - Roadmap location: Phase 2D, task 2D.2
  - Roadmap text: "2D.2 | FR-6.1 T11 | `tests/roadmap/test_convergence_e2e.py` | Extend existing SC-1–SC-6 tests"
- Finding:
  - Severity: HIGH
  - Gap description: Same pattern as REQ-050. The spec mandates writing 6 tests explicitly mapped to v3.3-SC-1 through v3.3-SC-6. The roadmap says "Extend existing SC-1–SC-6 tests," which again allows a pass-through if tests are found to already exist. The roadmap does not confirm: (1) the count of 6 tests, (2) that each SC-1 through SC-6 has exactly one corresponding test, or (3) that these are newly written for v3.3 rather than inherited from prior releases. Additionally, the roadmap references "SC-1–SC-6" without specifying "v3.3-SC-1 through v3.3-SC-6" — the qualifier "v3.3-" in the spec is meaningful because it scopes the success criteria to this release, not to prior success criteria with the same numbering scheme.
  - Impact: The 6-test deliverable for v3.3 success criteria may not be written. Tests inherited from prior releases would not validate the v3.3 spec's success criteria (SC-1 through SC-6 as defined in this spec's Success Criteria section).
  - Recommended correction: Roadmap 2D.2 should state: "Write 6 tests in `tests/roadmap/test_convergence_e2e.py`, one per v3.3 success criterion SC-1 through SC-6. Each test must reference the corresponding SC-ID in its spec_ref. Deliverable: 6 named test functions in the file."
- Confidence: HIGH

---

### REQ-052: FR-6.1 T12 — Write smoke test for convergence path in test_convergence_e2e.py

- Spec source: FR-6.1 (v3.05 Gaps table), Test File Layout section
- Spec text: "T12 | Smoke test convergence path | Write test"
- Status: COVERED
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Phase 2D, task 2D.3
  - Roadmap text: "2D.3 | FR-6.1 T12 | `tests/roadmap/test_convergence_e2e.py` | Add smoke test for convergence path"
- Confidence: HIGH

The roadmap explicitly calls out adding a smoke test for the convergence path in the correct file. The verb "Add" is equivalent to the spec's "Write test" for a single discrete test. The deliverable is unambiguous and the file location matches.

---

### REQ-053: FR-6.1 T14 — Regenerate wiring-verification artifact + validate

- Spec source: FR-6.1 (v3.05 Gaps table)
- Spec text: "T14 | Regenerate wiring-verification artifact | Generate + validate"
- Status: PARTIAL
- Match quality: WEAK
- Evidence:
  - Roadmap location: Phase 2D task 2D.4, and Phase 4 task 4.5
  - Roadmap text (2D.4): "2D.4 | FR-6.1 T14 | `docs/generated/` | Regenerate wiring-verification artifact + validate"
  - Roadmap text (4.5): "4.5 | — | Generate final wiring-verification artifact (FR-6.1 T14)"
- Finding:
  - Severity: MEDIUM
  - Gap description: There are two entries for T14 in the roadmap: 2D.4 (Phase 2) and 4.5 (Phase 4). Task 4.5 has no requirement reference ("—"), which severs the traceability link between the Phase 4 artifact generation and the spec requirement T14. More significantly, there is an internal contradiction: 2D.4 says "Regenerate wiring-verification artifact + validate" (matching the spec exactly), but 4.5 says "Generate final wiring-verification artifact" with no requirement reference. It is unclear whether these are the same task duplicated across phases or distinct steps. If they are the same task, one entry is orphaned from its requirement. If they are distinct steps, the roadmap lacks a clear definition of what "wiring-verification artifact" means, what its schema is, and what "validate" entails. The spec says "Generate + validate" — the validation step is not described in either roadmap entry.
  - Impact: The wiring-verification artifact may be generated without a defined validation step, or validation may be implied but not specified. The duplication creates ambiguity about where the deliverable actually lives in the plan.
  - Recommended correction: Consolidate the two entries. Either: (a) keep 2D.4 as the canonical task with explicit validation criteria, and remove 4.5, or (b) split them clearly — 2D.4 = "Generate draft artifact," 4.5 = "Final validation pass: confirm artifact schema, check all wiring points present" — and ensure 4.5 carries the FR-6.1 T14 requirement reference.
- Confidence: HIGH

---

### REQ-054: FR-6.2 T02 — run_post_phase_wiring_hook() already wired — write confirming test

- Spec source: FR-6.2 (v3.2 Gaps table)
- Spec text: "T02 | `run_post_phase_wiring_hook()` call | Already verified WIRED — write confirming test"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Phase 2D, task 2D.5
  - Roadmap text: "2D.5 | FR-6.2 T02 | `tests/v3.3/test_wiring_points_e2e.py` | Confirming test for `run_post_phase_wiring_hook()` (may overlap 2A.3)"
- Confidence: HIGH

The roadmap exactly captures the spec's intent: write a confirming test for `run_post_phase_wiring_hook()`. The parenthetical note about potential overlap with 2A.3 is an appropriate architectural observation (2A.3 covers FR-1.7 which tests the same hook). The file location (`tests/v3.3/test_wiring_points_e2e.py`) is appropriate — the spec's Test File Layout section shows `tests/roadmap/` only for T07/T11/T12, while T02 has no prescribed file. No overlap concerns are raised as gaps.

---

### REQ-055: FR-6.2 T17-T22 — Integration tests, regression suite, gap closure audit

- Spec source: FR-6.2 (v3.2 Gaps table)
- Spec text: "T17-T22 | Integration tests, regression suite, gap closure audit | Write tests per this spec"
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Phase 2D, task 2D.6
  - Roadmap text: "2D.6 | FR-6.2 T17–T22 | `tests/v3.3/test_integration_regression.py` | Integration + regression suite per spec"
- Finding:
  - Severity: MEDIUM
  - Gap description: The spec's T17-T22 action is "Write tests per this spec" — the phrase "per this spec" signals that the 6 gap IDs (T17, T18, T19, T20, T21, T22) each map to distinct test scenarios defined elsewhere in the spec. However, neither the spec nor the roadmap explicitly enumerates what T17, T18, T19, T20, T21, and T22 individually test. The spec inherits these gap IDs from prior releases (v3.2) without restating their individual descriptions. The roadmap maps the entire T17-T22 range to a single file with no per-ID breakdown. This means: (1) it is unclear what 6 specific tests are required, (2) there is no traceability from T17 through T22 to individual test functions, and (3) the roadmap task could be satisfied by any integration test file without confirming that all 6 gaps are individually addressed. Additionally, the spec says "gap closure audit" as part of the deliverable; the roadmap omits this audit step.
  - Impact: All 6 T17-T22 gaps may not be individually closed. The "gap closure audit" deliverable from the spec is not reflected in the roadmap, meaning there is no planned verification step to confirm that T17-T22 are each satisfied.
  - Recommended correction: (1) The roadmap should enumerate T17 through T22 individually in 2D.6, even if as a table, with a description of what each test covers. (2) Add an explicit "gap closure audit" step — either as a sub-task in 2D.6 or as a separate task 2D.7 — that confirms each of T17-T22 has a passing test and is marked closed.
- Confidence: MEDIUM (The root ambiguity is that T17-T22 descriptions are not in the spec itself — they appear to be inherited from a prior release doc not included in these inputs. The coverage judgment is based on what the roadmap does state.)

---

### REQ-SC8: SC-8 — All QA gaps closed: v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22

- Spec source: Success Criteria table
- Spec text: "SC-8 | Remaining QA gaps closed | v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22 | 2"
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Success Criteria Validation Matrix
  - Roadmap text: "SC-8 | All QA gap tests passing | FR-6.1 + FR-6.2 tests green | 2 | Yes"
- Finding:
  - Severity: HIGH
  - Gap description: The roadmap's validation method for SC-8 is "FR-6.1 + FR-6.2 tests green" — this is a test-passing criterion, not a gap-closure audit. The spec's SC-8 states "v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22" — it requires that each named gap ID is individually closed, not merely that some tests in the FR-6 category pass. The roadmap does not establish an explicit mapping from each gap ID to a specific test function that confirms closure. Given the findings on REQ-050, REQ-051, and REQ-055 above (the "extend existing" framing for T07/T11 and the absence of per-ID breakdown for T17-T22), SC-8 cannot be fully validated by the roadmap as written. Specifically:
    - T07: Roadmap allows a no-op if tests are "already present" — SC-8 could be declared met without writing new tests
    - T11: Same issue — "extend existing SC-1–SC-6 tests" may not produce 6 new v3.3-scoped tests
    - T14: Duplicate entries with ambiguous validation step
    - T17-T22: No per-ID mapping to test functions; no gap closure audit
    - T12 and T02: These are adequately covered
  - The roadmap's success criteria entry for SC-8 uses a binary "all tests green" check without a pre-condition that the correct set of tests has been written. This creates a situation where SC-8 could be declared green on a nearly empty test file if the few existing tests pass.
  - Impact: SC-8 may be declared closed when 4 of the 8 named gaps (T07, T11, T17-T22 individually) are not demonstrably addressed by written tests.
  - Recommended correction: The SC-8 validation method should be: "Each of T07, T11, T12, T14, T02, T17-T22 has a named, passing test function traceable to that gap ID. Gap closure audit confirms all 8 gaps marked closed. Zero gaps in OPEN state."
- Confidence: HIGH

---

## T08/T10 Handling Check

**Spec note**: "Note: T08 (`source_dir` fix) and T10 (budget info in PASS log) are already verified fixed in code state snapshot."

**Roadmap check**: Searching the roadmap for any task targeting T08 or T10...

The roadmap does NOT contain any task targeting T08 or T10. Neither gap ID appears in Phase 2D or anywhere else in the roadmap. The roadmap correctly respects the spec's exclusion of T08 and T10.

**Verdict**: PASS — roadmap correctly omits T08 and T10.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total requirements evaluated | 7 |
| COVERED | 2 (REQ-052, REQ-054) |
| PARTIAL | 4 (REQ-050, REQ-051, REQ-053, REQ-055) |
| MISSING | 0 |
| CONFLICTING | 0 |
| IMPLICIT | 0 |
| PARTIAL sub-classified as SC | 1 (REQ-SC8 — aggregates the partial items above) |

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 3 (REQ-050, REQ-051, REQ-SC8) |
| MEDIUM | 2 (REQ-053, REQ-055) |
| LOW | 0 |

### Coverage Percentage

- Fully covered: 2/7 = **28.6%**
- Partially or fully covered: 6/7 = **85.7%**
- Missing: 0/7 = **0%**

### Key Pattern

The dominant failure mode across this domain is **"extend existing" framing replacing "write" framing**. Where the spec says "Write N tests," the roadmap substitutes "Extend existing / verify already present / add any missing." This framing allows gap closure to be declared without producing the required test artifacts, undermining SC-8's guarantee. The 6-item T17-T22 range is additionally at risk from the absence of per-ID decomposition in either the spec's inherited gap list or the roadmap's task description.

### T08/T10 Guard

Confirmed: roadmap does not target T08 or T10. No spurious tasks for already-fixed items.
