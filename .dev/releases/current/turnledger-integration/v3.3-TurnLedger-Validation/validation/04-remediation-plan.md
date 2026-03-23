# Remediation Plan — v3.3 TurnLedger Validation

**Date**: 2026-03-23
**Verdict**: NO_GO → targeting CONDITIONAL_GO after R3 fixes

---

## Remediation Phases

### Phase R3: Missing Coverage — HIGH (Add missing tasks)

These are the blocking fixes. All 4 are simple task additions — no restructuring needed.

- [ ] **GAP-H003** (HIGH, SMALL): Add FR-1.19 (SHADOW_GRACE_INFINITE) task to roadmap Phase 2A
  - File: roadmap.md:L88 (after task 2A.12)
  - Action: ADD
  - Change: Add row `| 2A.13 | FR-1.19 | 1 test: SHADOW_GRACE_INFINITE constant value and grace period behavior — when set, shadow mode never exits grace period |`
  - Verification: Search roadmap for "FR-1.19" — should return 1 match
  - Dependencies: []

- [ ] **GAP-H004** (HIGH, SMALL): Add FR-1.20 (__post_init__ derivation) task to roadmap Phase 2A
  - File: roadmap.md:L88 (after task 2A.12)
  - Action: ADD
  - Change: Add row `| 2A.14 | FR-1.20 | 1 test: __post_init__() derives config fields correctly; invalid/missing produce sensible defaults |`
  - Verification: Search roadmap for "FR-1.20" — should return 1 match
  - Dependencies: []

- [ ] **GAP-H005** (HIGH, SMALL): Add FR-1.21 (check_wiring_report wrapper) task to roadmap Phase 2A
  - File: roadmap.md:L88 (after task 2A.12)
  - Action: ADD
  - Change: Add row `| 2A.15 | FR-1.21 | 1 test: check_wiring_report() wrapper called in wiring analysis flow, delegates to analysis, returns valid report |`
  - Verification: Search roadmap for "FR-1.21" — should return 1 match
  - Dependencies: []

- [ ] **GAP-H006** (HIGH, SMALL): Add FR-2.1a (handle_regression) task to roadmap Phase 2B
  - File: roadmap.md:L104 (after task 2B.4)
  - Action: ADD
  - Change: Add row `| 2B.5 | FR-2.1a | 1 test: handle_regression() reachable from _run_convergence_spec_fidelity, called on regression detection, logs event, adjusts budget |`
  - Verification: Search roadmap for "FR-2.1a" — should return 1 match
  - Dependencies: []

- [ ] **GAP-H001** (HIGH, SMALL): Add audit trail retrofit note to tasks 2D.1-2D.3
  - File: roadmap.md:L124-127 (tasks 2D.1-2D.3)
  - Action: EDIT
  - Change: Add note to each task: "Retrofit `audit_trail` fixture usage into existing tests"
  - Verification: Grep "audit_trail" in 2D task descriptions
  - Dependencies: []

- [ ] **GAP-H002** (HIGH, TRIVIAL): Add audit_writer.py to New Files Created table
  - File: roadmap.md:L213-225 (New Files Created table)
  - Action: ADD
  - Change: Add row `| tests/audit-trail/audit_writer.py | 1A | JSONL audit writer module |`
  - Verification: Count rows in table
  - Dependencies: []

### Phase R5: Partial Coverage — MEDIUM (Flesh out vague items)

- [ ] **GAP-M001** (MEDIUM, SMALL): Bind OQ-1 signal mechanism into task 2C.3
  - File: roadmap.md:L116 (task 2C.3)
  - Action: EDIT
  - Change: Append to description: "Signal injection via `os.kill(os.getpid(), signal.SIGINT)` per OQ-1"
  - Dependencies: []

- [ ] **GAP-M002** (MEDIUM, TRIVIAL): Add spec layout divergences note
  - File: roadmap.md (after New Files Created table)
  - Action: ADD
  - Change: Add "Spec Layout Divergences" section listing the 4 filename differences with rationale
  - Dependencies: []

- [ ] **GAP-M003** (MEDIUM, SMALL): Amend task 2A.6 for KPI value correctness
  - File: roadmap.md:L85 (task 2A.6)
  - Action: EDIT
  - Change: Change "wiring KPI fields" to "wiring KPI field VALUES match computed expectations: `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost`"
  - Dependencies: []

- [ ] **GAP-M004** (MEDIUM, SMALL): Document run_post_task_wiring_hook indirect coverage
  - File: roadmap.md (in Integration Point Registry or Phase 2A)
  - Action: ADD
  - Change: Note that `run_post_task_wiring_hook` is exercised through FR-2.2 and FR-3.1 mode tests
  - Dependencies: []

- [ ] **GAP-M005** (MEDIUM, TRIVIAL): Add _parse_phase_tasks return type assertion
  - File: roadmap.md:L82 (task 2A.2)
  - Action: EDIT
  - Change: Append "Assert _parse_phase_tasks() returns list[TaskEntry] | None"
  - Dependencies: []

### Phase R8: Low-Priority Cleanup

- [ ] **GAP-L001** (LOW, TRIVIAL): Enumerate KPI field names in task 2A.6
  - Already addressed by GAP-M003 fix above
  - Dependencies: [GAP-M003]

- [ ] **GAP-L002** (LOW, TRIVIAL): Add budget logging assertion note to task 2B.1
  - File: roadmap.md:L101
  - Action: EDIT
  - Change: Append "; assert budget logging includes consumed/reimbursed/available"
  - Dependencies: []

- [ ] **GAP-L003** (LOW, TRIVIAL): Fix smoke test file reference
  - File: roadmap.md:L126 (task 2D.3)
  - Action: EDIT
  - Change: Reference `test_convergence_smoke.py` or document the merge decision
  - Dependencies: []

- [ ] **GAP-L004** (LOW, TRIVIAL): Document JSONL write contention assumption
  - File: roadmap.md (in Phase 1A section)
  - Action: ADD
  - Change: Note: "Audit trail JSONL assumes sequential test execution or single-writer"
  - Dependencies: []

- [ ] **GAP-L005** (LOW, TRIVIAL): Document can_run_wiring_gate indirect coverage
  - File: roadmap.md (Integration Point Registry)
  - Action: ADD
  - Dependencies: []

### Phase R9: Re-Validate

- [ ] Rerun `/sc:validate-roadmap` after all fixes applied

---

## Remediation Impact

If all R3+R5 remediations are applied:
- **Projected coverage**: 100% (84/84 COVERED)
- **Projected findings**: 0 CRITICAL, 0 HIGH, 0 MEDIUM
- **Projected verdict**: **GO**
- **Estimated effort**: ~30 minutes (all changes are TRIVIAL or SMALL roadmap edits)

### Update to Phase 2A Test Count

After adding tasks 2A.13-2A.15:
- Old subtotal: "~21 tests covering SC-1"
- New subtotal: "~24 tests covering SC-1" (21 + 3)
- SC-1 still satisfied (≥20)

### Update to Phase 2B Test Count

After adding task 2B.5:
- Old subtotal: "4 tests covering SC-2"
- New subtotal: "5 tests covering SC-2"
