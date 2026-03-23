# Adversarial Review — v3.3 TurnLedger Validation

Date: 2026-03-23
Reviewer: Orchestrator (adversarial pass)

---

## Methodology

Fresh re-read of spec and roadmap performed independently of agent reports. Each COVERED assessment from the parallel agents was challenged. Orphan requirements and tasks were searched. Sequencing was re-validated.

---

## Step 4.2: Challenge COVERED Assessments

### Challenged and Upheld (no new findings)

| Requirement | Agent Claim | Challenge | Result |
|-------------|------------|-----------|--------|
| FR-1.1-FR-1.4 | COVERED by 2A.1 (4 tests) | Could a developer write "construction validation" without testing ordering (BEFORE phase loop)? | UPHELD — spec says "construction validation" and the FR text is clear. Implementer must read spec FR-1.1 text. |
| FR-1.7 | COVERED by 2A.3 | Does the roadmap distinguish the two *specific* code paths (executor.py:1199-1204 vs 1407-1412)? | UPHELD — roadmap says "per-task and per-phase/ClaudeProcess paths" which maps exactly. |
| FR-1.14 | COVERED by 2A.9 | 3 tests for 5 sub-items — sufficient? | UPHELD — 2 paths (pass/fail) + format = 3 tests covers all sub-items. |
| FR-2.1 | COVERED by 2B.1 | "budget logging" subsumed — could it be missed? | UPHELD — LOW risk. Spec text is clear; implementer reads spec, not just roadmap. |
| FR-4.2 | COVERED by 1B.2 | Does roadmap capture the 5-step algorithm? | UPHELD — all 5 steps present: ast.parse, call graph, import resolution, BFS/DFS, gap report. |
| All SC-* | COVERED in SC matrix | Does every SC have a test-level enforcement? | UPHELD — SC matrix assigns phase, automation status, and validation method to all 12. |

### Challenged and Downgraded

None. All COVERED assessments survive adversarial challenge. The agent reports were thorough.

---

## Step 4.3: Search for Orphan Requirements

Requirements in the spec not captured by any agent or the requirement universe:

### ADV-1: FR-7.2 Property — "test duration"
- **Type**: MISSED_GAP
- **Severity**: MEDIUM
- **Description**: FR-7.2 PROP1 (spec line 447) says "Timestamp, **test duration**, actual observed values." The 9-field JSONL schema (FR-7.1, spec lines 420-441) has no `duration` field. Neither the requirement universe nor any agent flagged that "test duration" is a verification property but has no schema field to carry it.
- **Spec evidence**: `v3.3-requirements-spec.md:447` — "Were real tests run? — Timestamp, test duration, actual observed values (not static fixtures)"
- **Roadmap evidence**: ABSENT — roadmap task 1A.1 lists 9 fields; none is `duration`. Task 1A.4 checks "real timestamps" but not duration.
- **Impact**: A third party cannot verify test duration from the JSONL record, weakening PROP1's "were real tests run" determination.
- **Recommended correction**: Either add `duration_ms` as a 10th JSONL field (computed by fixture from test start/end) or document that duration is derived from timestamps in consecutive records.

### ADV-2: No Test for `wiring_gate_enabled` / `wiring_gate_grace_period` Config Fields
- **Type**: MISSED_GAP
- **Severity**: LOW
- **Description**: Code State Snapshot line 37 lists `wiring_gate_enabled / wiring_gate_grace_period | models.py:335-336 | WIRED`. These config fields are exercised through the gate mode tests (FR-3.1) but have no dedicated test verifying their default values or that they are correctly read from config.
- **Spec evidence**: `v3.3-requirements-spec.md:37` — verified wiring point
- **Roadmap evidence**: IMPLICIT — exercised through FR-3.1 mode matrix tests
- **Impact**: Low. The mode tests would fail if these fields were broken. No dedicated test needed.
- **Recommended correction**: None — implicit coverage is adequate.

---

## Step 4.4: Search for Orphan Roadmap Tasks

Tasks in the roadmap with no spec traceability:

| Task | Spec Traceability | Status |
|------|------------------|--------|
| 4.5 | "Generate final wiring-verification artifact (FR-6.1 T14)" | TRACED — maps to FR-6.1-T14 |
| 4.6 | "Update docs/memory/solutions_learned.jsonl" | NOT TRACED — housekeeping task, no spec requirement. Not harmful. |
| Appendix A | Integration Point Registry | NOT TRACED — roadmap-generated reference material. Adds value, no spec conflict. |

**No scope creep detected.** Task 4.6 and Appendix A are value-add documentation items that don't conflict with any spec requirement.

---

## Step 4.5: Validate Sequencing and Dependencies

| Check | Result |
|-------|--------|
| Spec phase ordering preserved? | YES — P1→P2→P3→P4 |
| One-way-door operations gated? | YES — production changes only in P3, after P2 baseline |
| Exit criteria before next phase? | YES — Checkpoints A/B/C/D gate correctly |
| Circular dependencies? | NONE |
| OQ-7 investigation sequenced? | WARNING — Not formalized as task (confirmed CC3 finding) |

No new sequencing findings beyond CC3's warnings.

---

## Step 4.6: Check Silent Assumptions

### ADV-3: Roadmap Assumes `_subprocess_factory` Is Stable
- **Type**: SILENT_ASSUMPTION
- **Severity**: LOW
- **Description**: The entire test harness depends on `_subprocess_factory` as the injection point. The roadmap and spec both assume this interface is stable, but no test validates the factory interface itself. If the factory signature changes, all E2E tests would break simultaneously.
- **Impact**: Low — the factory is a simple callable replacement. Breaking it would be immediately obvious.
- **Recommended correction**: None — the factory's stability is verified by usage across all tests.

### ADV-4: Roadmap Assumes `tests/v3.3/` Directory Creation
- **Type**: SILENT_ASSUMPTION
- **Severity**: LOW
- **Description**: The roadmap creates 8+ files under `tests/v3.3/` but no task explicitly creates the directory or its `__init__.py`. This is a trivial implementation detail but could confuse an automated pipeline.
- **Impact**: Negligible. Directory creation is implicit in file creation.
- **Recommended correction**: None.

---

## Step 4.7: Validate Test Coverage Mapping

| Check | Result |
|-------|--------|
| Every spec test case in roadmap with matching scope? | YES — all FR test cases mapped to tasks |
| Test numbering consistent? | YES — FR-1.1→2A.1, etc. |
| Test prerequisites addressed? | YES — Phase 1A (audit trail) is prerequisite for all Phase 2 tests |
| Total test count consistent? | YES — spec says "50+" in summary, roadmap ~53 |
| Spec test file layout vs roadmap? | MINOR MISMATCHES — 4 filename differences (see GAP-L4) |

### ADV-5: FR-3.1 Claims "8 tests" But Spec Requires 16 Assertions
- **Type**: FALSE_COVERAGE (potential)
- **Severity**: LOW
- **Description**: Roadmap task 2C.1 says "8 tests: 4 modes × 2 paths." Each test must verify 4 state items (FR-3.1-AC1 through AC4). That's 32 assertions across 8 tests — 4 assertions per test. This is achievable but the roadmap doesn't confirm that each test checks all 4 state items.
- **Spec evidence**: `v3.3-requirements-spec.md:249-253` — "Each mode test must verify: [4 items]"
- **Roadmap evidence**: `roadmap-final.md:114` — "Each verifies: `TaskStatus`/`GateOutcome`, `TurnLedger` state, `DeferredRemediationLog` entries, `ShadowGateMetrics` recording"
- **Impact**: None — roadmap explicitly lists all 4 verification items with "Each verifies:" prefix.
- **Recommended correction**: None — roadmap is explicit. Finding withdrawn after evidence review.

---

## Step 4.8: Produce Adversarial Findings

### New Finding: ADV-1 (retained)

### ADV-1: FR-7.2 "test duration" — No JSONL Field
- **Type**: MISSED_GAP
- **Severity**: MEDIUM
- **Description**: FR-7.2 PROP1 requires "test duration" as evidence of real test execution, but the 9-field schema has no duration field.
- **Spec evidence**: `v3.3-requirements-spec.md:447` — "Timestamp, test duration, actual observed values"
- **Roadmap evidence**: `roadmap-final.md:47` — 9-field schema lists `timestamp` but not `duration`
- **Impact**: Third-party verification of PROP1 is weakened without duration data.
- **Recommended correction**: Add `duration_ms` field to schema, or document that duration is computed from consecutive timestamps.

---

## Step 4.9: Update to Consolidated Report

### Score Impact

ADV-1 is a new MEDIUM finding. This does not change any requirement's coverage status (FR-7.1 schema is still COVERED as written — the gap is between FR-7.1 and FR-7.2). It is a **spec-internal inconsistency** similar to GAP-H1 (assertion_type).

**Updated finding counts**:
- VALID-CRITICAL: 3 (unchanged)
- VALID-HIGH: 8 (unchanged)
- VALID-MEDIUM: 6 (+1 from ADV-1)
- VALID-LOW: 6 (unchanged)
- NEEDS-SPEC-DECISION: 2 (unchanged)

**Coverage scores unchanged** — ADV-1 does not downgrade any requirement from COVERED.

**Verdict unchanged**: CONDITIONAL_GO

### What the Parallel Agents Missed

| Finding | Why Missed |
|---------|-----------|
| ADV-1 (test duration) | D6 validated FR-7.2 against the roadmap's shorthand "real timestamps" without checking whether all elements of the spec's PROP1 text ("test duration") had schema support. The 9-field schema was validated against FR-7.1, not cross-checked against FR-7.2's prose. |
| ADV-2 (config field defaults) | CC4 flagged SHADOW_GRACE_INFINITE but treated the broader config fields as implicitly covered. Correct assessment — no correction needed. |

---

## Summary

| Category | Count |
|----------|-------|
| COVERED assessments challenged | 6 major |
| COVERED assessments downgraded | 0 |
| Orphan requirements found | 2 (ADV-1 new MEDIUM, ADV-2 LOW) |
| Orphan roadmap tasks found | 2 (4.6 housekeeping, Appendix A reference) |
| Sequencing issues | 0 new (CC3 findings confirmed) |
| Silent assumptions | 2 (both LOW) |
| Test mapping issues | 0 new |
| **Net new findings** | **1 (ADV-1, MEDIUM)** |

The adversarial pass confirms the parallel agents' work was thorough. The roadmap provides strong coverage of all explicitly stated spec requirements. The gaps are concentrated in: (1) spec-level omissions (Code State Snapshot items without FRs), (2) spec-internal inconsistencies (schema vs prose), and (3) minor implementation details (signal mechanism, file naming).
