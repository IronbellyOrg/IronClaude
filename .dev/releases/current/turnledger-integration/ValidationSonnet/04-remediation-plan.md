# Remediation Plan
**Date**: 2026-03-23
**Verdict**: NO_GO → target: CONDITIONAL_GO or GO

---

## Remediation Overview

All gaps can be resolved with **targeted roadmap edits only** — no spec changes, no production code changes required. The dominant issues are:

1. **Three missing tasks** (FR-1.19, FR-1.20, FR-1.21) — add 3 tasks to Phase 2A
2. **One missing behavioral test task** (FR-2.1a) — add 1 task to Phase 2B
3. **One CONFLICTING clause** (FR-7.3 flush semantics) — correct one sentence in 1A.2
4. **Weak language** in QA gap tasks — strengthen wording in 2D.1 and 2D.2
5. **Several medium/low precision gaps** — targeted wording clarifications

**Projected post-remediation verdict**: GO (if all R1-R8 applied) or CONDITIONAL_GO (if R1-R3 applied, R4-R8 optional)

---

## Phase R1: Spec-Internal Contradictions

*Fix source of truth first.*

No spec-internal contradictions require roadmap changes. The spec has self-consistency issues (CC2 findings) but those are spec-level fixes. The roadmap cannot resolve spec contradictions — flagging for spec owner:

- **NEEDS-SPEC-DECISION**: FR-1.11 (KPI fields present) vs SC-5 (KPI field VALUES correct) — spec should align FR-1.11 to match SC-5 wording.
- **NEEDS-SPEC-DECISION**: FR-3.2a-d appears assigned to both test_gate_rollout_modes.py and test_budget_exhaustion.py — spec should clarify canonical file.
- **NEEDS-SPEC-DECISION**: FR-5.3 says "this IS FR-4" but actually maps to FR-4.3 only — spec should say "this IS FR-4.3."

---

## Phase R2: Roadmap-Internal Contradictions

*Fix self-consistency.*

### R2.1 — Fix flush-semantics conflict
- **Gap**: GAP-H005
- **File**: roadmap.md
- **Task**: 1A.2
- **Action**: EDIT
- **Change**: Current: "auto-flushes on session end" → Correct to: "auto-flushes after each test"
- **Verification**: Both spec FR-7.3 and roadmap 1A.2 now say "after each test"
- **Dependencies**: None
- **Effort**: TRIVIAL

### R2.2 — Fix critical path statement
- **Gap**: GAP-L002
- **File**: roadmap.md
- **Task**: Timeline Summary footer
- **Action**: EDIT
- **Change**: "Critical path: Phase 1A → Phase 2 → Phase 4" → "Critical path: Phase 1A → Phase 2 → Phase 3 → Phase 4"
- **Verification**: Matches Phase 4 dependency ("All previous phases complete")
- **Dependencies**: None
- **Effort**: TRIVIAL

---

## Phase R3: Missing Coverage — HIGH (add missing tasks)

### R3.1 — Add task for FR-1.21 (check_wiring_report() wrapper)
- **Gap**: GAP-H001
- **File**: roadmap.md
- **Section**: Phase 2A task table (after 2A.12)
- **Action**: ADD
- **Change**:
```
| 2A.13 | FR-1.21 | 1 test: Assert check_wiring_report() wrapper (wiring_gate.py:1079) is called within wiring analysis flow; wrapper delegates to underlying analysis; returns valid report structure |
```
- **Verification**: 2A task table now covers FR-1.21; "~21 tests" subtotal increases to "~22 tests"
- **Dependencies**: None
- **Effort**: SMALL

### R3.2 — Add task for FR-1.19 (SHADOW_GRACE_INFINITE)
- **Gap**: GAP-H002
- **File**: roadmap.md
- **Section**: Phase 2A task table (after 2A.13)
- **Action**: ADD
- **Change**:
```
| 2A.14 | FR-1.19 | 1 test: Assert SHADOW_GRACE_INFINITE defined in models.py:293 with expected sentinel value; assert shadow mode with wiring_gate_grace_period=SHADOW_GRACE_INFINITE never exits grace period (wiring gate always credits back) |
```
- **Verification**: 2A task table now covers FR-1.19
- **Dependencies**: None
- **Effort**: SMALL

### R3.3 — Add task for FR-1.20 (__post_init__ derivation)
- **Gap**: GAP-H003
- **File**: roadmap.md
- **Section**: Phase 2A task table (after 2A.14)
- **Action**: ADD
- **Change**:
```
| 2A.15 | FR-1.20 | 1 test: Assert __post_init__() derives wiring_gate_enabled, wiring_gate_grace_period, wiring_analyses_count from base config values (models.py:338-384); assert invalid/missing base config → sensible defaults |
```
- **Verification**: 2A task table now covers FR-1.20
- **Dependencies**: None
- **Effort**: SMALL

### R3.4 — Add task for FR-2.1a (handle_regression() behavioral test)
- **Gap**: GAP-H004
- **File**: roadmap.md
- **Section**: Phase 2B task table (after 2B.1)
- **Action**: ADD
- **Change**:
```
| 2B.1a | FR-2.1a | Behavioral test: inject regression condition (convergence score decreases between runs); assert handle_regression() is invoked; assert log entry created with regression event; assert budget adjusted accordingly (convergence.py, spec_ref: v3.05-FR8) |
```
- **Verification**: 2B.1a addresses runtime behavioral requirement; complement to static reachability in manifest
- **Dependencies**: None
- **Effort**: SMALL

### R3.5 — Strengthen FR-5.2 test to include positive case
- **Gap**: GAP-H... (from GAP-M001 → HIGH due to ADV-003 cascade)
- **File**: roadmap.md
- **Task**: 3B.3
- **Action**: EDIT
- **Change**: Current: "Test: impl-vs-spec checker finds gap in synthetic test with missing implementation" → Correct to: "Test (positive): checker finds existing function → no gap flagged; Test (negative): remove function → checker flags gap; both cases required to validate R-3 exit criteria"
- **Verification**: Both test cases specified; R-3 exit criteria confirmable at Checkpoint C
- **Dependencies**: None
- **Effort**: TRIVIAL

---

## Phase R4: Conflicting Coverage — HIGH

All CONFLICTING requirements addressed in R2.1 above.

---

## Phase R5: Partial Coverage Gaps — MEDIUM

### R5.1 — Add failure_reason literal to 3A.1
- **Gap**: GAP-M002
- **File**: roadmap.md
- **Task**: 3A.1
- **Action**: EDIT
- **Change**: Add to 3A.1 description: "failure_reason must be exactly: '0 files analyzed from non-empty source directory'"
- **Dependencies**: None
- **Effort**: TRIVIAL

### R5.2 — Expand manifest scope in 1B.4
- **Gap**: GAP-M003
- **File**: roadmap.md
- **Task**: 1B.4
- **Action**: EDIT
- **Change**: "executor.py entry points" → "both entry points (execute_sprint + _run_convergence_spec_fidelity) and all 13 required_reachable entries from spec wiring manifest (v3.3-requirements-spec.md bottom section)"
- **Dependencies**: None
- **Effort**: TRIVIAL

### R5.3 — Add duration_ms to 1A.1 schema field list
- **Gap**: GAP-M004
- **File**: roadmap.md
- **Task**: 1A.1
- **Action**: EDIT
- **Change**: "9-field schema: test_id, spec_ref, timestamp, assertion_type, inputs, observed, expected, verdict, evidence" → "10-field schema: test_id, spec_ref, timestamp, assertion_type, inputs, observed, expected, verdict, evidence, duration_ms (auto-computed from test start/end timestamps)"
- **Dependencies**: None
- **Effort**: TRIVIAL

### R5.4 — Consolidate T14 duplicate tasks
- **Gap**: GAP-M005
- **File**: roadmap.md
- **Tasks**: 2D.4 and 4.5
- **Action**: REMOVE 2D.4; EDIT 4.5
- **Change 4.5**: "Generate final wiring-verification artifact (FR-6.1 T14) AND validate against current codebase state (confirms artifact is current, not stale)"
- **Change 2D.4**: Remove entirely or mark as "see Phase 4 task 4.5"
- **Dependencies**: None
- **Effort**: TRIVIAL

---

## Phase R6: Ordering and Dependency Fixes

### R6.1 — Strengthen QA gap language in 2D.1
- **Gap**: GAP-H006
- **File**: roadmap.md
- **Task**: 2D.1
- **Action**: EDIT
- **Change**: "Extend existing 7 tests (verify already present, add any missing)" → "Verify test_convergence_wiring.py contains tests covering all 7 T07 scope items (from spec FR-6.1); for each of the 7 missing, write the test; do not count pre-v3.3 tests toward this total unless they explicitly cover T07 scenarios"
- **Dependencies**: None
- **Effort**: TRIVIAL

### R6.2 — Strengthen QA gap language in 2D.2
- **Gap**: GAP-H007
- **File**: roadmap.md
- **Task**: 2D.2
- **Action**: EDIT
- **Change**: "Extend existing SC-1–SC-6 tests" → "Verify test_convergence_e2e.py contains 6 tests covering v3.3-SC-1 through v3.3-SC-6 convergence scenarios; write any missing v3.3-scoped tests; v3.3 scoping means the tests validate convergence behavior as described in this spec, not prior release behavior"
- **Dependencies**: None
- **Effort**: TRIVIAL

---

## Phase R7: Implicit-to-Explicit Promotion

### R7.1 — Make audit trail explicit for Phase 2D and 3B
- **Gap**: CC4-10 (cross-cutting)
- **File**: roadmap.md
- **Sections**: Phase 2D preamble, Phase 3B preamble
- **Action**: ADD sentence
- **Change**: Add to end of Phase 2D intro: "All tests in this section must emit JSONL audit records via the audit_trail fixture (NFR-4)."
- **Change**: Add to end of Phase 3B intro: "All tests in this section must emit JSONL audit records via the audit_trail fixture (NFR-4)."
- **Dependencies**: R3.1–R3.4 (audit trail fixture defined)
- **Effort**: TRIVIAL

---

## Phase R8: Low-Priority and Cleanup

### R8.1 — Clarify NFR-5 scope in task 4.4
- **Gap**: GAP-L001
- **File**: roadmap.md
- **Task**: 4.4
- **Action**: EDIT
- **Change**: "every known wiring point from FR-1 has a manifest entry" → "all 13 required_reachable entries from spec wiring manifest are present in tests/v3.3/wiring_manifest.yaml"
- **Dependencies**: R5.2 (manifest scope clarified)
- **Effort**: TRIVIAL

### R8.2 — Fix audit trail module name inconsistency
- **Gap**: CC1-5
- **File**: roadmap.md
- **Action**: EDIT
- **Change**: Standardize to `tests/audit-trail/audit_writer.py` throughout (matches roadmap task body name); update New Files table entry `test_audit_writer.py` → `audit_writer.py`
- **Dependencies**: None
- **Effort**: TRIVIAL

---

## Phase R9: Re-Validate

After applying all remediations:
1. Run `/sc:validate-roadmap` again with same inputs
2. Expected result: 0 CRITICAL, 0–1 HIGH, weighted ≥ 92% → CONDITIONAL_GO or GO

---

## Remediation Impact Computation

| Remediation Phase | Gaps Closed | New Coverage Status |
|------------------|-------------|---------------------|
| R2: Internal contradictions | GAP-H005, GAP-L002 | 1 CONFLICTING → COVERED, 1 LOW closed |
| R3: Missing tasks | GAP-H001, H002, H003, H004 + GAP-M001 | 3 MISSING → COVERED, 1 PARTIAL → COVERED |
| R5: Medium partial | GAP-M002, M003, M004, M005 | 4 PARTIAL → COVERED |
| R6: Ordering/language | GAP-H006, H007 | 2 PARTIAL → COVERED |
| R7: Implicit-to-explicit | CC4-10 | Cross-cutting gap closed |
| R8: Cleanup | GAP-L001, CC1-5 | 2 LOW closed |

**Projected post-remediation scores**:
- Covered: 50 + 12 = 62
- Partial: 17 − 12 = 5 (remaining minor items)
- Missing: 3 − 3 = 0
- Conflicting: 1 − 1 = 0
- **Projected weighted coverage**: (62 + 0.5×5) / 71 = 64.5/71 = **90.8%**
- **Projected HIGH findings**: 10 → 0
- **Projected verdict**: **GO** (0 CRITICAL, 0 HIGH, weighted ≥ 90%)

**Effort summary**:
- 4 ADD tasks (R3.1–R3.4): SMALL each
- 10 EDIT operations (R2.1, R2.2, R3.5, R5.1–R5.4, R6.1, R6.2, R7.1, R8.1, R8.2): TRIVIAL each
- 1 REMOVE (R5.4 duplicate 2D.4): TRIVIAL
- **Total estimated effort**: ~2-3 hours of roadmap editing

---

## Patch Checklist

- [ ] **GAP-H001** (HIGH, SMALL): Add task 2A.13 for FR-1.21 (check_wiring_report() wrapper)
  - File: roadmap.md:Phase 2A task table
  - Action: ADD row after 2A.12
  - Verification: 2A table lists FR-1.21; subtotal updated

- [ ] **GAP-H002** (HIGH, SMALL): Add task 2A.14 for FR-1.19 (SHADOW_GRACE_INFINITE)
  - File: roadmap.md:Phase 2A task table
  - Action: ADD row after 2A.13
  - Verification: 2A table lists FR-1.19; models.py:293 covered

- [ ] **GAP-H003** (HIGH, SMALL): Add task 2A.15 for FR-1.20 (__post_init__ derivation)
  - File: roadmap.md:Phase 2A task table
  - Action: ADD row after 2A.14
  - Verification: 2A table lists FR-1.20; models.py:338-384 covered

- [ ] **GAP-H004** (HIGH, SMALL): Add task 2B.1a for FR-2.1a (handle_regression() behavioral)
  - File: roadmap.md:Phase 2B task table
  - Action: ADD row after 2B.1
  - Verification: 2B.1a covers runtime behavioral test; complements manifest entry

- [ ] **GAP-H005** (HIGH, TRIVIAL): Fix flush semantics in 1A.2
  - File: roadmap.md:1A.2
  - Action: EDIT "on session end" → "after each test"
  - Verification: roadmap matches spec FR-7.3 exactly

- [ ] **GAP-H006** (HIGH, TRIVIAL): Strengthen 2D.1 language
  - File: roadmap.md:2D.1
  - Action: EDIT as specified in R6.1
  - Verification: language guarantees T07-scoped tests written

- [ ] **GAP-H007** (HIGH, TRIVIAL): Strengthen 2D.2 language
  - File: roadmap.md:2D.2
  - Action: EDIT as specified in R6.2
  - Verification: language guarantees v3.3-scoped SC-1–SC-6 tests

- [ ] **ADV-003** (HIGH, TRIVIAL): No separate fix needed — resolved by R3.1–R3.3 (Checkpoint B becomes achievable once FR-1.19/1.20/1.21 tasks exist)
  - Verification: After adding 2A.13–2A.15, SC-1 ≥20 tests achievable, Checkpoint B valid

- [ ] **GAP-M001** (HIGH, TRIVIAL): Add positive test case to 3B.3
  - File: roadmap.md:3B.3
  - Action: EDIT as specified in R3.5
  - Verification: both positive and negative cases specified

- [ ] **GAP-L002** (LOW, TRIVIAL): Fix critical path label
  - File: roadmap.md:Timeline Summary
  - Action: EDIT as specified in R2.2
  - Verification: Phase 3 included in critical path

- [ ] **GAP-M002** (MEDIUM, TRIVIAL): Add failure_reason literal to 3A.1
  - File: roadmap.md:3A.1
  - Action: EDIT as specified in R5.1

- [ ] **GAP-M003** (MEDIUM, TRIVIAL): Expand manifest scope in 1B.4
  - File: roadmap.md:1B.4
  - Action: EDIT as specified in R5.2

- [ ] **GAP-M004** (MEDIUM, TRIVIAL): Add duration_ms to 1A.1 schema
  - File: roadmap.md:1A.1
  - Action: EDIT as specified in R5.3

- [ ] **GAP-M005** (MEDIUM, TRIVIAL): Consolidate T14 tasks
  - File: roadmap.md:2D.4 and 4.5
  - Action: REMOVE 2D.4; EDIT 4.5 as specified in R5.4

- [ ] **GAP-L001** (LOW, TRIVIAL): Clarify NFR-5 scope in task 4.4
  - File: roadmap.md:4.4
  - Action: EDIT as specified in R8.1

- [ ] **CC4-10** (MEDIUM, TRIVIAL): Add explicit audit trail mandate to 2D and 3B
  - File: roadmap.md:Phase 2D preamble and Phase 3B preamble
  - Action: ADD sentence as specified in R7.1

- [ ] **CC1-5** (LOW, TRIVIAL): Fix module name inconsistency
  - File: roadmap.md:New Files table
  - Action: EDIT as specified in R8.2
