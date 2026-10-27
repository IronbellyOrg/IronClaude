# Adversarial Review

## Fresh Re-Read Outcome

The adversarial re-read confirmed the main consolidated findings. No previously COVERED requirement was downgraded beyond the gaps already captured during consolidation, but the pattern scan reinforced two hidden-risk areas:

1. **Negation/guard semantics are easy to miss** — especially FR-1.19 shadow-grace behavior and FR-5.1 fail-on-zero-files wording.
2. **Schema/runner precision matters** — audit schema and flush semantics are not safely inferred from general audit-trail language.

## Pattern Scan Results

### Requirement-like statements surfaced
- `v3.3-requirements-spec.md:399` — FAIL report must include `failure_reason: "0 files analyzed from non-empty source directory"`
- `v3.3-requirements-spec.md:490` — `assertion_type` must match FR-7.1 schema field
- `v3.3-requirements-spec.md:652` — every test must emit a JSONL record
- `v3.3-requirements-spec.md:215` — when `wiring_gate_grace_period` is `SHADOW_GRACE_INFINITE`, shadow mode never exits grace period
- `v3.3-requirements-spec.md:405` — current state excludes implementation-vs-spec checking, motivating FR-5.2

### Adversarial findings

#### ADV-001: ORPHAN_REQUIREMENT — FR-1.19 shadow-grace semantics
- Severity: HIGH
- Description: The roadmap covers `_resolve_wiring_mode()` and shadow findings logging, but never plans the sentinel-value semantics for `SHADOW_GRACE_INFINITE`.
- Spec evidence: `v3.3-requirements-spec.md:211-217`
- Roadmap evidence: ABSENT
- Impact: shadow-mode grace behavior may silently remain untested.
- Recommended correction: add an explicit test task under Phase 2A.

#### ADV-002: FALSE_COVERAGE — audit-trail language is insufficient for schema fidelity
- Severity: HIGH
- Description: General audit-trail tasks could look complete, but the roadmap’s explicit 9-field schema and session-end flush wording contradict the spec.
- Spec evidence: `v3.3-requirements-spec.md:450-475`, `487-493`
- Roadmap evidence: `roadmap.md:47-49`
- Impact: third-party verifiability can be claimed while required evidence fields and durability semantics are absent.
- Recommended correction: align roadmap schema and flush behavior exactly with the spec.

#### ADV-003: ORPHAN_REQUIREMENT — per-test JSONL emission requirement
- Severity: MEDIUM
- Description: The spec requires every test to emit a JSONL record. The roadmap implies broad audit use but does not restate this atomic guarantee in every relevant phase or gate.
- Spec evidence: `v3.3-requirements-spec.md:652`
- Roadmap evidence: partial support at `roadmap.md:52`, `133`, `174`
- Impact: implementation could emit partial audit coverage while still appearing compliant.
- Recommended correction: add explicit acceptance text that every v3.3 test writes an audit record.

## Orphan Roadmap Tasks

No major orphan roadmap task was found. Tasks 4.5 and 4.6 are lightly traced but still plausibly justified by FR-6.1 T14 and broader project learning needs.

## Silent Assumptions

No additional silent assumption pattern was found via grep. The roadmap is fairly explicit about dependencies.

## Test Coverage Mapping

The adversarial pass agrees that most test mapping is solid, but the following remain under-specified:
- FR-5.2 positive-case checker test
- FR-6.1 / FR-6.2 per-gap closure details
- FR-1.19 / FR-1.20 / FR-1.21 / FR-2.1a absent from the task matrix

## Final Adversarial Assessment

The consolidated NO_GO verdict stands. Adversarial review increases confidence that the principal blocking issues are real roadmap omissions or contradictions, not validator false positives.
