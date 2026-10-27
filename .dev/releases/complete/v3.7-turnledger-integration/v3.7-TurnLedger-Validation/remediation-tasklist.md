# v3.3 TurnLedger Validation — Remediation Tasklist

**Source**: `validation-comparison/merged-consolidated-report.md` (adversarial-merged)
**Current Verdict**: NO_GO (10 HIGH, 84.6% weighted coverage)
**Target Verdict**: GO (≤3 HIGH, ≥90% weighted coverage)
**Execution**: `/sc:task-unified` per task

---

## Phase 0: Roadmap Remediation (Pre-Implementation)

These tasks modify the roadmap itself to close gaps identified by validation. They must be completed before implementation begins, as implementation tasks reference roadmap text.

---

### TASK-R01: Add `duration_ms` to audit schema (GAP-H007)
- **Priority**: HIGH
- **Type**: Roadmap text correction
- **Gap**: GAP-H007 — FR-7.1 schema lists 9 fields; spec shows 10 including `duration_ms`
- **Action**: Update roadmap task 1A.1 (L47) to list 10-field schema: `test_id`, `spec_ref`, `timestamp`, `assertion_type`, `inputs`, `observed`, `expected`, `verdict`, `evidence`, `duration_ms`
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Line**: ~47
- **Acceptance**: Task 1A.1 schema field count = 10, includes `duration_ms (auto-computed from test start/end)`
- **Closes**: GAP-H007

### TASK-R02: Fix flush semantics — session-end → per-test (GAP-H008)
- **Priority**: HIGH
- **Type**: Roadmap text correction
- **Gap**: GAP-H008 — Roadmap task 1A.2 says "auto-flushes on session end"; spec FR-7.3 says "auto-flushes after each test"
- **Action**: Change roadmap task 1A.2 (L48) to: "`audit_trail` pytest fixture — session-scoped, opens JSONL in `results_dir`, provides `record()` method, auto-flushes after each test; produces summary at session end"
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Line**: ~48
- **Acceptance**: Task 1A.2 says "auto-flushes after each test", not "on session end"
- **Closes**: GAP-H008

### TASK-R03: Add task 2A.13 — FR-1.19 SHADOW_GRACE_INFINITE (GAP-H003)
- **Priority**: HIGH
- **Type**: Roadmap task addition
- **Gap**: GAP-H003 — FR-1.19 MISSING from roadmap
- **Action**: Add row to Phase 2A table after task 2A.12:
  - `2A.13 | FR-1.19 | 1 test: SHADOW_GRACE_INFINITE constant value and grace period behavior under shadow mode`
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Location**: Phase 2A table, after 2A.12
- **Acceptance**: Task 2A.13 exists referencing FR-1.19; subtotal updated to ~22 tests
- **Closes**: GAP-H003

### TASK-R04: Add task 2A.14 — FR-1.20 `__post_init__` config derivation (GAP-H004)
- **Priority**: HIGH
- **Type**: Roadmap task addition
- **Gap**: GAP-H004 — FR-1.20 MISSING from roadmap
- **Action**: Add row to Phase 2A table:
  - `2A.14 | FR-1.20 | 1 test: __post_init__() config field derivation and defaults validation`
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Location**: Phase 2A table, after 2A.13
- **Acceptance**: Task 2A.14 exists referencing FR-1.20; subtotal updated
- **Closes**: GAP-H004

### TASK-R05: Add task 2A.15 — FR-1.21 `check_wiring_report` wrapper (GAP-H005)
- **Priority**: HIGH
- **Type**: Roadmap task addition
- **Gap**: GAP-H005 — FR-1.21 MISSING from roadmap
- **Action**: Add row to Phase 2A table:
  - `2A.15 | FR-1.21 | 1 test: check_wiring_report() wrapper is called, delegates, returns valid report`
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Location**: Phase 2A table, after 2A.14
- **Acceptance**: Task 2A.15 exists referencing FR-1.21; subtotal updated to ~24 tests
- **Closes**: GAP-H005

### TASK-R06: Add task 2B.5 — FR-2.1a `handle_regression()` (GAP-H006)
- **Priority**: HIGH
- **Type**: Roadmap task addition
- **Gap**: GAP-H006 — FR-2.1a MISSING from roadmap (task 2B.1 covers FR-2.1 but not FR-2.1a)
- **Action**: Add row to Phase 2B table:
  - `2B.5 | FR-2.1a | 1 test: handle_regression() — reachability, regression detection, logging, budget adjustment`
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Location**: Phase 2B table, after 2B.4
- **Acceptance**: Task 2B.5 exists referencing FR-2.1a; subtotal updated to 5 tests
- **Closes**: GAP-H006

### TASK-R07: Add `audit_writer.py` to resource table (GAP-H002)
- **Priority**: HIGH
- **Type**: Roadmap table correction
- **Gap**: GAP-H002 — `tests/audit-trail/audit_writer.py` absent from "New Files Created" table
- **Action**: Add row to "New Files Created" table (L213-225):
  - `tests/audit-trail/audit_writer.py | 1A | JSONL audit record writer`
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Location**: New Files Created table
- **Acceptance**: File listed in resource table
- **Closes**: GAP-H002

### TASK-R08: Add audit trail retrofit note to tasks 2D.1-2D.3 (GAP-H001)
- **Priority**: HIGH
- **Type**: Roadmap text amendment
- **Gap**: GAP-H001 — Existing tests extended in tasks 2D.1-2D.3 may not emit JSONL records
- **Action**: Add note after Phase 2D task table: "**Note**: Tasks 2D.1-2D.3 must retrofit `audit_trail` fixture usage into all existing tests being extended, per constraint REQ-078."
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Location**: After Phase 2D task table
- **Acceptance**: Explicit retrofit instruction present
- **Closes**: GAP-H001

---

## Phase 0M: Medium-Priority Roadmap Fixes

These close MEDIUM findings that won't block GO verdict but improve roadmap quality.

---

### TASK-R09: Bind signal mechanism to task 2C.3 (GAP-M001)
- **Priority**: MEDIUM
- **Type**: Roadmap text amendment
- **Gap**: GAP-M001 — FR-3.3 signal mechanism unspecified in task 2C.3
- **Action**: Amend task 2C.3 description to include: "Use `os.kill(os.getpid(), signal.SIGINT)` per OQ-1 recommendation"
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Acceptance**: Task 2C.3 specifies signal approach
- **Closes**: GAP-M001

### TASK-R10: Add spec layout divergences note (GAP-M002)
- **Priority**: MEDIUM
- **Type**: Roadmap section addition
- **Gap**: GAP-M002 — Test file naming diverges from spec without explanation
- **Action**: Add a "Spec Layout Divergences" note section explaining:
  1. `test_wiring_points.py` → `test_wiring_points_e2e.py` (clarity)
  2. separate `test_budget_exhaustion.py` → merged into `test_gate_rollout_modes.py` (co-located with mode matrix)
  3. `test_pipeline_fixes.py` → distributed across Phase 3 tests
  4. `audit_trail.py` → `audit_writer.py` (name specificity)
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Acceptance**: Section exists, all 4 divergences documented
- **Closes**: GAP-M002

### TASK-R11: Amend task 2A.6 for value-correctness assertions (GAP-M003)
- **Priority**: MEDIUM
- **Type**: Roadmap text amendment
- **Gap**: GAP-M003 — SC-5 requires value matching, not just presence
- **Action**: Amend task 2A.6 to: "1 test: KPI report generation with wiring KPI fields — assert field VALUES match computed expectations from test inputs (not just presence)"
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Acceptance**: Task 2A.6 explicitly requires value-correctness
- **Closes**: GAP-M003

### TASK-R12: Add return type assertion to task 2A.2 (GAP-M005)
- **Priority**: MEDIUM
- **Type**: Roadmap text amendment
- **Gap**: GAP-M005 — `_parse_phase_tasks()` return type untested
- **Action**: Amend task 2A.2 to include: "Assert `_parse_phase_tasks()` return type is `list[PhaseTask]`"
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Acceptance**: Return type assertion specified in task 2A.2
- **Closes**: GAP-M005

### TASK-R13: Add positive-case test to task 3B.3 (GAP-M006)
- **Priority**: MEDIUM
- **Type**: Roadmap text amendment
- **Gap**: GAP-M006 — FR-5.2 positive case absent
- **Action**: Amend task 3B.3 to: "Test: impl-vs-spec checker — (a) positive case: finds existing implementation; (b) negative case: flags gap in synthetic test with missing implementation"
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Acceptance**: Task 3B.3 describes both positive and negative cases
- **Closes**: GAP-M006

### TASK-R14: Correct requirement count in timeline (GAP-M007)
- **Priority**: MEDIUM
- **Type**: Roadmap text correction
- **Gap**: GAP-M007 — L271 claims "13 requirements" vs actual 47 FRs / 65 total
- **Action**: Change L271 from "13 requirements, 12 success criteria" to "47 functional requirements (7 FR groups), 12 success criteria, 6 constraints — 65 total obligations"
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Line**: ~271
- **Acceptance**: Timeline summary reflects accurate requirement count
- **Closes**: GAP-M007

### TASK-R15: Document `run_post_task_wiring_hook` coverage (GAP-M004)
- **Priority**: MEDIUM
- **Type**: Roadmap note addition
- **Gap**: GAP-M004 — No dedicated E2E test for task-level wiring hook
- **Action**: Add note to Phase 2A section: "Note: `run_post_task_wiring_hook` (spec:L578-580) is exercised indirectly through FR-2.2 and FR-3.1 mode tests. Dedicated wiring point E2E test deferred — indirect coverage deemed sufficient per architect review."
- **File**: `v3.3-TurnLedger-Validation/roadmap.md`
- **Acceptance**: Coverage decision documented
- **Closes**: GAP-M004

---

## Phase 0L: Low-Priority Roadmap Improvements

Non-blocking quality improvements. Execute if time permits.

---

### TASK-R16: Enumerate KPI field names in task 2A.6 (GAP-L001)
- **Priority**: LOW
- **Type**: Roadmap text enrichment
- **Gap**: GAP-L001 — FR-1.11 KPI field names not listed
- **Action**: Amend task 2A.6 to list fields: `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost`
- **Closes**: GAP-L001

### TASK-R17: Add budget logging assertion to task 2B.1 (GAP-L002)
- **Priority**: LOW
- **Type**: Roadmap text enrichment
- **Gap**: GAP-L002 — FR-2.1 budget logging detail implicit
- **Action**: Amend task 2B.1 to include: "Assert budget logging includes consumed/reimbursed/available"
- **Closes**: GAP-L002

### TASK-R18: Clarify smoke test file location (GAP-L003)
- **Priority**: LOW
- **Type**: Roadmap text correction
- **Gap**: GAP-L003 — Task 2D.3 references `test_convergence_e2e.py` but smoke test is in `test_convergence_smoke.py`
- **Action**: Verify correct location and update task 2D.3 accordingly
- **Closes**: GAP-L003

### TASK-R19: Document JSONL write contention assumption (GAP-L004)
- **Priority**: LOW
- **Type**: Roadmap note addition
- **Gap**: GAP-L004 — Parallel test JSONL interleave risk
- **Action**: Add note to Phase 1A: "Design assumption: tests run sequentially within a session. If parallel execution is introduced, JSONL write locking must be added to `audit_writer.py`."
- **Closes**: GAP-L004

### TASK-R20: Document `can_run_wiring_gate()` indirect coverage (GAP-L005)
- **Priority**: LOW
- **Type**: Roadmap note addition
- **Gap**: GAP-L005 — No dedicated test for `can_run_wiring_gate()`
- **Action**: Add note: "Indirectly covered by FR-3.2b budget exhaustion test."
- **Closes**: GAP-L005

### TASK-R21: Strengthen FR-6.1/6.2 task descriptions (GAP-L006)
- **Priority**: LOW
- **Type**: Roadmap text enrichment
- **Gap**: GAP-L006 — Tasks 2D.1, 2D.2, 2D.6 use vague language
- **Action**: Add specific assertion counts or acceptance bullets to each task
- **Closes**: GAP-L006

---

## Phase 0X: Cross-Cutting Fixes

### TASK-R22: Update `_run_checkers()` integration status
- **Priority**: MEDIUM
- **Type**: Roadmap correction
- **Gap**: Change #7 — Integration Wiring Audit shows implicit FULLY_WIRED
- **Action**: Update Appendix A.6 to note PARTIALLY_WIRED status pending FR-5.2 positive-case gap closure
- **Closes**: Integration wiring inconsistency

---

## Post-Remediation Validation

### TASK-V01: Re-run validation against remediated roadmap
- **Priority**: CRITICAL
- **Type**: Validation
- **Depends**: All TASK-R01 through TASK-R08 (HIGH priority)
- **Action**: Run `/sc:validate-roadmap` against the updated roadmap to confirm:
  1. All 10 HIGH findings are resolved
  2. Weighted coverage ≥ 90%
  3. Verdict flips to GO or CONDITIONAL_GO
- **Acceptance**: New validation report shows ≤3 HIGH findings and weighted coverage ≥ 90%

### TASK-V02: Resolve NSD-001 (spec decision needed) — COMPLETE
- **Priority**: HIGH
- **Type**: Spec clarification
- **Gap**: NSD-001 — FR-7.1 vs FR-7.3 `assertion_type` ambiguity in method signature
- **Resolution**: Spec L489 already resolves this — `assertion_type` is an explicit 3rd positional param of `record()`. 8 explicit params + 2 auto-computed (`timestamp`, `duration_ms`) = 10 schema fields. No spec or roadmap change needed.
- **Status**: RESOLVED 2026-03-23

---

## Execution Summary

| Priority | Count | Status |
|----------|-------|--------|
| HIGH (roadmap fixes) | 8 | COMPLETE |
| MEDIUM (quality fixes) | 7 | COMPLETE |
| LOW (enrichments) | 6 | COMPLETE (R16 folded into R11) |
| Cross-cutting | 1 | COMPLETE |
| Validation | 2 | PENDING — TASK-V01 (re-validate) and TASK-V02 (NSD-001 spec decision) |
| **Total** | **24** | **22 applied, 2 pending validation** |

### Execution Order

```
┌─────────────────────────────────────────────────┐
│ Phase 0: HIGH priority (TASK-R01 → R08)         │
│   Can execute in parallel — all are independent  │
│   roadmap text edits                             │
├─────────────────────────────────────────────────┤
│ Phase 0M: MEDIUM priority (TASK-R09 → R15)      │
│   Can execute in parallel after Phase 0          │
├─────────────────────────────────────────────────┤
│ Phase 0L: LOW priority (TASK-R16 → R21)         │
│   Optional, execute if time permits              │
├─────────────────────────────────────────────────┤
│ Phase 0X: Cross-cutting (TASK-R22)              │
│   Execute alongside Phase 0M                     │
├─────────────────────────────────────────────────┤
│ TASK-V02: Spec decision (can run anytime)        │
├─────────────────────────────────────────────────┤
│ TASK-V01: Re-validate (after all HIGH complete)  │
└─────────────────────────────────────────────────┘
```

### `/sc:task-unified` Execution Hint

All Phase 0 tasks (R01–R08) are **Tier 1** (single-file text edits, no code, no tests). They can be batched:

```
/sc:task-unified Execute TASK-R01 through TASK-R08 from remediation-tasklist.md —
all are roadmap text corrections in v3.3-TurnLedger-Validation/roadmap.md.
Apply all 8 HIGH-priority changes, then run /sc:validate-roadmap to confirm
HIGH findings resolved and coverage ≥ 90%.
```
