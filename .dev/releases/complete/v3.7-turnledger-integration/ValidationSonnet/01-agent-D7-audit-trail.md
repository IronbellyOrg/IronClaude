# Agent D7 Validation Report — Domain: audit_trail

**Agent**: D7
**Domain**: audit_trail
**Spec**: v3.3-requirements-spec.md
**Roadmap**: v3.3-TurnLedger-Validation/roadmap.md
**Date**: 2026-03-23
**Validator**: Claude Sonnet 4.6 (1M context)

---

## Scope

Requirements validated in this report:
- REQ-056: FR-7.1 — JSONL audit record with 9-field schema
- REQ-057: FR-7.2 — Third-party verifiability properties
- REQ-058: FR-7.3 — `audit_trail` pytest fixture
- REQ-NFR4: Every test must emit a JSONL audit trail record
- REQ-SC12: SC-12 — audit trail is third-party verifiable

---

## Requirement Validations

### REQ-056: FR-7.1 — JSONL audit record schema
- Spec source: FR-7.1 (section "FR-7: Audit Trail Infrastructure")
- Spec text: "Each test writes a JSONL audit record to `{results_dir}/audit-trail.jsonl`" with a JSON schema example containing the fields: `test_id`, `spec_ref`, `timestamp`, `assertion_type`, `inputs`, `observed`, `expected`, `verdict`, `evidence`, `duration_ms`
- Status: PARTIAL
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Phase 1A, Task 1A.1
  - Roadmap text: "JSONL audit record writer — `tests/audit-trail/audit_writer.py` with 9-field schema: `test_id`, `spec_ref`, `timestamp`, `assertion_type`, `inputs`, `observed`, `expected`, `verdict`, `evidence`"
- Finding:
  - Severity: MEDIUM
  - Gap description: The roadmap's 1A.1 explicitly states "9-field schema" and enumerates 9 fields, omitting `duration_ms`. However, the spec's FR-7.1 JSON schema example includes `duration_ms` as a top-level record field (`"duration_ms": 1234`). The spec's FR-7.3 further clarifies that `duration_ms` is "auto-computed from test start/end timestamps (no parameter needed in `record()`)." This creates an internal spec tension: FR-7.1 shows `duration_ms` in the JSON output, while FR-7.3 implies it is computed rather than a caller-supplied parameter. The roadmap resolves this by labeling the schema as "9-field" and omitting `duration_ms` from the field list, which is consistent with the FR-7.3 framing but conflicts with the FR-7.1 JSON example which renders `duration_ms` as a schema field in the output record. The roadmap does not explicitly address how `duration_ms` appears in the final JSONL output — only that it is not passed as a parameter to `record()`.
  - Impact: Implementation risk that `duration_ms` may be missing from emitted JSONL records, making audit records non-compliant with the FR-7.1 schema example. Third-party reviewers inspecting the JSONL would find a field present in the spec example absent from actual output.
  - Recommended correction: Roadmap 1A.1 should state "9-field schema plus auto-computed `duration_ms`" (10 output fields total) to explicitly acknowledge that `duration_ms` appears in the emitted record even though it is not a `record()` parameter. Alternatively, the field count should be corrected to 10.
- Confidence: HIGH

---

### REQ-057: FR-7.2 — Third-party verifiability properties
- Spec source: FR-7.2 (section "FR-7: Audit Trail Infrastructure")
- Spec text: "A third party with no prior knowledge MUST be able to determine from the audit trail alone: 1. Were real tests run? — Timestamp, test duration, actual observed values (not static fixtures) 2. Were tests run according to spec? — `spec_ref` traces to code location, `inputs` show configuration 3. Are results real? — `observed` contains concrete runtime values, `evidence` describes what was checked 4. Pass/fail determination is sound — `expected` vs `observed` comparison is explicit"
- Status: COVERED
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Phase 1A, Task 1A.4
  - Roadmap text: "Verification test: confirm JSONL output meets 4 third-party verifiability properties (real timestamps, spec-traced, runtime observations, explicit verdict)"
- Finding: None — the roadmap compresses the 4 properties into a single phrase but captures all four semantically: "real timestamps" covers property 1 (real timestamps + duration), "spec-traced" covers property 2 (spec_ref to code), "runtime observations" covers property 3 (concrete observed values + evidence), and "explicit verdict" covers property 4 (expected vs observed). Task 1A.4 delivers an automated verification test rather than just documentation, which is appropriate. The SC-12 entry in the success criteria matrix ("JSONL output review against FR-7.2 properties") provides an additional enforcement point with "Semi — automated check + manual review" validation, aligning with spec intent. Phase 4 task 4.3 adds a manual review step confirming properties.
- Confidence: HIGH

---

### REQ-058: FR-7.3 — `audit_trail` pytest fixture
- Spec source: FR-7.3 (section "FR-7: Audit Trail Infrastructure")
- Spec text: "A pytest fixture (`audit_trail`) that: Opens `audit-trail.jsonl` in the results directory; Provides `record(test_id, spec_ref, assertion_type, inputs, observed, expected, verdict, evidence)` method; `assertion_type` classifies the assertion (e.g., 'behavioral', 'structural', 'value') — must match the FR-7.1 schema field; `duration_ms` is auto-computed from test start/end timestamps (no parameter needed in `record()`); Auto-flushes after each test; Produces a summary report at session end: total tests, passed, failed, coverage of wiring points"
- Status: CONFLICTING
- Match quality: WEAK
- Evidence:
  - Roadmap location: Phase 1A, Tasks 1A.2 and 1A.3
  - Roadmap text (1A.2): "`audit_trail` pytest fixture — session-scoped, opens JSONL in `results_dir`, provides `record()` method, auto-flushes on session end"
  - Roadmap text (1A.3): "Summary report generation at session end: total/passed/failed/wiring coverage"
- Finding:
  - Severity: HIGH
  - Gap description: Three sub-issues identified:

    **Sub-issue 1 (CRITICAL): Flush-semantics conflict.** The spec states the fixture "auto-flushes after each test" (per-test flush). The roadmap 1A.2 states "auto-flushes on session end" (session-level flush). These are semantically opposite. Per-test flushing ensures that if a test session crashes mid-run, all records up to the crash point are persisted to disk. Session-end flushing means a mid-session crash loses all records since the session started. The spec's per-test flush is the more robust behavior for third-party verifiability (a partial audit trail is still useful). The roadmap's session-end flush would silently discard all records on crash, undermining the core audit trail purpose.

    **Sub-issue 2 (MEDIUM): assertion_type requirement not explicitly captured.** The spec's FR-7.3 states that `assertion_type` "must match the FR-7.1 schema field" — i.e., the fixture's `record()` method must accept and validate the `assertion_type` parameter as a schema-defined field, not just a free-text label. The roadmap 1A.2 mentions only that the fixture "provides `record()` method" without specifying `assertion_type` as a named parameter or its schema constraint. This omission risks implementations that treat `assertion_type` as optional or unconstrained.

    **Sub-issue 3 (LOW): duration_ms auto-computation not addressed in 1A.2.** The roadmap 1A.2 does not state that `duration_ms` is auto-computed from test start/end. This is related to the REQ-056 gap. Without explicit instruction that the fixture must measure test start time and compute `duration_ms`, an implementation might omit it or require a caller-supplied value.

  - Impact: The flush conflict is the most serious issue. A session crash produces no audit trail, eliminating the core deliverable. Third-party verifiability (SC-12) would be unachievable for any partial run. The assertion_type omission risks schema non-compliance in fixture output.
  - Recommended correction:
    - Change roadmap 1A.2 to specify "auto-flushes after EACH test (not session end)" to align with the spec.
    - Add explicit statement that `record()` accepts `assertion_type` as a named, required parameter matching the FR-7.1 schema field.
    - Add statement that the fixture records test start time and auto-computes `duration_ms` before writing the record.
    - Task 1A.3 should be updated to explicitly name "wiring points" in the summary (the roadmap uses "wiring coverage" which is close, but the spec says "coverage of wiring points" — this is acceptable as written; no change required for 1A.3).
- Confidence: HIGH

---

### REQ-NFR4: Every test must emit a JSONL audit trail record
- Spec source: Constraints section ("Audit trail: Every test must emit a JSONL record")
- Spec text: "Audit trail: Every test must emit a JSONL record"
- Status: COVERED
- Match quality: SEMANTIC
- Evidence:
  - Roadmap location: Multiple — Executive Summary (paragraph 3), Phase 2 Validation Checkpoint B, Phase 4 task 4.3, Success Criteria matrix SC-12
  - Roadmap text (Executive Summary): "Establish explicit source-of-truth artifacts — wiring manifest for reachability (FR-4.1, NFR-5) and JSONL audit trail for third-party verification (FR-7.1, FR-7.2, FR-7.3, NFR-4)"
  - Roadmap text (Checkpoint B): "Audit trail JSONL emitted for every test."
  - Roadmap text (SC-12 validation matrix): "JSONL output review against FR-7.2 properties"
- Finding: None. The roadmap's Validation Checkpoint B explicitly states "Audit trail JSONL emitted for every test" as a gate condition for Phase 2 completion. The Executive Summary references NFR-4 directly. The enforcement mechanism (the `audit_trail` fixture being session-scoped and required in conftest.py) is covered by 1A.2. The "every test" constraint is architecturally enforced by making the fixture available at all conftest levels. No gaps identified for the coverage requirement itself.
- Confidence: HIGH

---

### REQ-SC12: SC-12 — audit trail is third-party verifiable
- Spec source: Success Criteria table
- Spec text: "SC-12 — audit trail is third-party verifiable, JSONL output with all 4 verification properties" with metric "JSONL output with all 4 verification properties"
- Status: COVERED
- Match quality: EXACT
- Evidence:
  - Roadmap location: Success Criteria Validation Matrix, Phase 1A task 1A.4, Phase 4 task 4.3
  - Roadmap text (SC matrix): "SC-12 | Audit trail third-party verifiable | JSONL output review against FR-7.2 properties | 2 | Semi — automated check + manual review"
  - Roadmap text (4.3): "Manual review of JSONL audit trail: confirm third-party verifiability properties"
- Finding: None. SC-12 is explicitly tracked in the roadmap's success criteria matrix with a validation method (automated + manual review) and a phase assignment (Phase 2 for delivery, Phase 4 for review). Task 1A.4 creates an automated verification test, and task 4.3 adds a manual review step. The roadmap correctly scopes SC-12 validation to FR-7.2 properties.

    Note: The flush-semantics conflict in REQ-058 (FR-7.3) creates an indirect risk to SC-12 — if the fixture flushes on session end rather than per-test, SC-12 may not be achievable for partial runs. However, SC-12 itself is correctly represented in the roadmap; the risk flows from the FR-7.3 gap, not from SC-12's own coverage.
- Confidence: HIGH

---

## Summary Statistics

| Requirement | Status | Match Quality | Severity |
|---|---|---|---|
| REQ-056 (FR-7.1 — 9-field schema) | PARTIAL | SEMANTIC | MEDIUM |
| REQ-057 (FR-7.2 — verifiability properties) | COVERED | SEMANTIC | — |
| REQ-058 (FR-7.3 — audit_trail fixture) | CONFLICTING | WEAK | HIGH |
| REQ-NFR4 (every test emits JSONL) | COVERED | SEMANTIC | — |
| REQ-SC12 (SC-12 third-party verifiable) | COVERED | EXACT | — |

**Totals**:
- Requirements assessed: 5
- COVERED: 3 (60%)
- PARTIAL: 1 (20%)
- MISSING: 0 (0%)
- CONFLICTING: 1 (20%)
- IMPLICIT: 0 (0%)

**Findings requiring action**:
- HIGH: 1 (REQ-058 flush-semantics conflict)
- MEDIUM: 1 (REQ-056 duration_ms schema field omission)
- LOW: 0

**Most critical finding**: The flush-semantics conflict in REQ-058 (FR-7.3). The spec mandates per-test auto-flush; the roadmap specifies session-end flush. This is a behavioral contradiction, not a wording ambiguity. If implemented per the roadmap, a mid-session crash produces zero audit records, directly undermining the core third-party verification deliverable and creating downstream risk for SC-12 and NFR-4.

**Secondary finding**: REQ-056's `duration_ms` field ambiguity. The roadmap calls the schema "9-field" and omits `duration_ms` from its enumeration, but the spec's FR-7.1 JSON example includes `duration_ms` as an output field. Clarification is needed to prevent implementations that compute `duration_ms` but do not emit it in the JSONL record.
