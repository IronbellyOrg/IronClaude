# Remediation Plan — v3.3 TurnLedger Validation

Date: 2026-03-23

---

## Remediation Phases (Ordered by Blast Radius)

### Phase R1: Spec-Internal Contradictions

- [ ] **GAP-H1** (HIGH, SMALL): Resolve `assertion_type` missing from FR-7.3 `record()` signature
  - File: `v3.3-requirements-spec.md:456`
  - Action: EDIT
  - Change: Either add `assertion_type` as 8th param to `record()` signature, or document that it is auto-derived from test context (e.g., "behavioral", "structural", "value"). Update FR-7.1 schema documentation accordingly.
  - Verification: FR-7.1 9-field schema and FR-7.3 `record()` params produce the same fields
  - Dependencies: []

- [ ] **GAP-H2** (HIGH, TRIVIAL): Fix FR-5.1-TEST "empty directory" contradiction
  - File: `v3.3-requirements-spec.md:369`
  - Action: EDIT
  - Change: Replace `"Point run_wiring_analysis() at an empty directory"` with `"Point run_wiring_analysis() at a non-empty directory where file collection returns 0 analyzed files (e.g., all files filtered out by extension or path rules)"`
  - Verification: FR-5.1-TEST description is consistent with FR-5.1 guard condition
  - Dependencies: []

- [ ] **ADV-1** (MEDIUM, SMALL): Add `duration_ms` to JSONL schema or document derivation
  - File: `v3.3-requirements-spec.md:420-441`
  - Action: ADD
  - Change: Add `"duration_ms": 1234` to the JSONL example, making it a 10-field schema. Update FR-7.3 `record()` to auto-compute from test start/end (no param needed).
  - Verification: FR-7.2 PROP1 "test duration" has a corresponding schema field
  - Dependencies: [GAP-H1]

### Phase R2: Roadmap-Internal Contradictions

- [ ] **GAP-H8** (HIGH, TRIVIAL): Add missing `audit_writer.py` to New Files table
  - File: `roadmap-final.md:213-225` (New Files Created table)
  - Action: ADD
  - Change: Add row: `"tests/audit-trail/audit_writer.py | 1A | JSONL audit record writer"`
  - Verification: New Files table has entry for every file created by Phase 1A tasks
  - Dependencies: []

- [ ] **GAP-L4** (LOW, TRIVIAL): Reconcile 4 filename mismatches
  - File: `roadmap-final.md` (multiple locations)
  - Action: EDIT
  - Change: Adopt roadmap naming as authoritative (`test_wiring_points_e2e.py`, `audit_writer.py`, consolidate budget into gate modes file). Update spec Test File Layout to match.
  - Verification: Spec and roadmap reference identical file names
  - Dependencies: []

### Phase R3: Missing Coverage (CRITICAL + HIGH)

- [ ] **GAP-C1** (CRITICAL, SMALL): Add FR for `handle_regression` reachability
  - File: `v3.3-requirements-spec.md` (add after FR-2.1) + `roadmap-final.md` (add task to Phase 2B or 1B manifest)
  - Action: ADD
  - Change: Add `"FR-2.1a: Assert handle_regression() is reachable from _run_convergence_spec_fidelity and is called on regression detection"`. Add to wiring manifest in roadmap task 1B.4. Add test to Phase 2B.
  - Verification: `handle_regression` has an FR, a manifest entry, and a test
  - Dependencies: []

- [ ] **GAP-C2** (CRITICAL, SMALL): Add test for `SHADOW_GRACE_INFINITE`
  - File: `v3.3-requirements-spec.md` (add FR-1.19) + `roadmap-final.md` (add to 2A task table)
  - Action: ADD
  - Change: Add `"FR-1.19: Assert SHADOW_GRACE_INFINITE constant value and its effect on shadow mode grace period logic"`. Add task 2A.13 to roadmap.
  - Verification: `SHADOW_GRACE_INFINITE` has an FR and a test
  - Dependencies: []

- [ ] **GAP-C3** (CRITICAL, SMALL): Add test for `__post_init__()` derivation
  - File: `v3.3-requirements-spec.md` (add FR-1.20) + `roadmap-final.md` (add to 2A task table)
  - Action: ADD
  - Change: Add `"FR-1.20: Assert __post_init__() correctly derives sprint config fields from input config"`. Add task 2A.14 to roadmap.
  - Verification: `__post_init__()` derivation logic has an FR and a test
  - Dependencies: []

- [ ] **GAP-H3** (HIGH, TRIVIAL): Add `_parse_phase_tasks()` return type assertion
  - File: `roadmap-final.md` task 2A.2
  - Action: EDIT
  - Change: Amend task 2A.2 to include: "Assert `_parse_phase_tasks()` returns `list[TaskEntry]` for task-inventory phases and `None` for freeform phases"
  - Verification: Return type contract is explicitly tested
  - Dependencies: []

- [ ] **GAP-H4** (HIGH, TRIVIAL): Confirm `can_run_wiring_gate()` coverage
  - File: `roadmap-final.md` task 2C.2
  - Action: EDIT
  - Change: Amend task 2C.2 (FR-3.2b) to explicitly note: "Assert `can_run_wiring_gate()` returns False when budget exhausted, triggering wiring hook skip"
  - Verification: `can_run_wiring_gate()` has explicit assertion in test
  - Dependencies: []

- [ ] **GAP-H5** (HIGH, SMALL): Add test for `check_wiring_report()` wrapper
  - File: `v3.3-requirements-spec.md` + `roadmap-final.md`
  - Action: ADD
  - Change: Add to FR-1.7 or create FR-1.x: "Assert `check_wiring_report()` wrapper (wiring_gate.py:1079) is called within the wiring analysis flow". Add to Phase 2A.
  - Verification: `check_wiring_report()` has a test
  - Dependencies: []

- [ ] **GAP-H6** (HIGH, SMALL): Add explicit E2E test for `run_post_task_wiring_hook`
  - File: `roadmap-final.md` Phase 2A
  - Action: ADD
  - Change: Add task: "2A.13 (or merge into 2A.7): Assert `run_post_task_wiring_hook()` is called per-task with correct mode and ledger context"
  - Verification: Task-level wiring hook has dedicated E2E test alongside phase-level hook
  - Dependencies: []

- [ ] **GAP-H7** (HIGH, SMALL): Sync FR-4.1 manifest with body manifest
  - File: `v3.3-requirements-spec.md:279-325`
  - Action: EDIT
  - Change: Replace FR-4.1 YAML example (9 entries) with the full 13-entry manifest from lines 530-586, or add note: "See Wiring Manifest section (line 528) for the authoritative manifest."
  - Verification: FR-4.1 and body manifest have identical entries
  - Dependencies: []

### Phase R4: Conflicting Coverage (CRITICAL + HIGH)

No CONFLICTING findings. Phase R4 is empty.

### Phase R5: Partial Coverage Gaps (MEDIUM)

- [ ] **GAP-M1/M2** (MEDIUM, TRIVIAL): Bind signal mechanism to task 2C.3
  - File: `roadmap-final.md:116` (task 2C.3)
  - Action: EDIT
  - Change: Amend to: "1 test: Interrupted sprint via `os.kill(os.getpid(), signal.SIGINT)` → KPI report written, remediation log persisted, outcome = INTERRUPTED. Direct flag manipulation is NOT acceptable."
  - Verification: Task 2C.3 specifies signal injection mechanism
  - Dependencies: []

- [ ] **GAP-M3** (MEDIUM, TRIVIAL): Explicit audit trail retrofit note
  - File: `roadmap-final.md:124-126` (tasks 2D.1-2D.3)
  - Action: EDIT
  - Change: Add to each task description: "(includes adding `audit_trail.record()` calls to existing and new tests)"
  - Verification: "extend" scope explicitly includes audit trail retrofit
  - Dependencies: []

- [ ] **GAP-M4** (MEDIUM, SMALL): Decompose FR-6.2-T17-T22
  - File: `roadmap-final.md:129` (task 2D.6)
  - Action: EDIT
  - Change: Break into individual tests: "T17: backward-compat regression, T18: wiring integration smoke, T19: mode interaction, T20: convergence integration, T21: error boundary, T22: gap closure audit"
  - Verification: Each T-ID has a named test
  - Dependencies: []

- [ ] **GAP-M5** (MEDIUM, TRIVIAL): Add timestamped filename to task 1A.2
  - File: `roadmap-final.md:48` (task 1A.2)
  - Action: EDIT
  - Change: Add: "JSONL filename includes run timestamp (e.g., `audit-trail-{timestamp}.jsonl`) per R-4 mitigation"
  - Verification: RISK-4 mitigation has an implementation task
  - Dependencies: []

### Phase R6: Ordering and Dependency Fixes

- [ ] **CC3-W7** (WARNING, TRIVIAL): Document 2D.5 dependency on 2A
  - File: `roadmap-final.md:128` (task 2D.5)
  - Action: EDIT
  - Change: Add note: "Depends on Phase 2A (file `test_wiring_points_e2e.py` must exist)"
  - Verification: Implicit file dependency is documented
  - Dependencies: []

- [ ] **CC3-W10** (WARNING, SMALL): Formalize pre-existing failure investigation
  - File: `roadmap-final.md` (add task to Phase 2 or early Phase 3)
  - Action: ADD
  - Change: Add task: "2.0: Run baseline suite. Capture and document the 3 pre-existing failure identities. Classify as wiring-related or not. This is a hard prerequisite for Phase 3 task 3A.1."
  - Verification: Pre-existing failures documented before production changes
  - Dependencies: []

### Phase R7: Implicit-to-Explicit Promotion

No IMPLICIT findings to promote.

### Phase R8: Low-Priority and Cleanup

- [ ] **GAP-L1** (LOW, TRIVIAL): Enumerate KPI field names in roadmap task 2A.6
- [ ] **GAP-L2** (LOW, TRIVIAL): Clarify SC-5 tests field values, not just presence
- [ ] **GAP-L3** (LOW, TRIVIAL): Reconcile T12 smoke test file location
- [ ] **GAP-L5** (LOW, TRIVIAL): Clarify auto-flush as per-record, not session-end
- [ ] **GAP-L6** (LOW, TRIVIAL): Clarify v3.05-SC vs v3.3-SC in FR-6.1-T11

### Phase R9: Re-Validate

After all fixes are applied, rerun this validation prompt to confirm:
- 0 CRITICAL findings
- 0 HIGH findings
- Weighted coverage ≥ 95%
- Verdict: GO

---

## Remediation Impact Projection

```
If all remediations are applied:
  - Projected coverage: 99.4% (89 → all COVERED except OQ-1 merged into task)
  - Projected findings: 0 CRITICAL, 0 HIGH, 0 MEDIUM (after R1-R8)
  - Projected verdict: GO
  - Estimated effort:
    - R1 (spec fixes): ~30 min
    - R2 (roadmap fixes): ~15 min
    - R3 (add FRs + tasks): ~1 hour
    - R5 (partial fixes): ~30 min
    - R6 (ordering): ~15 min
    - R8 (cleanup): ~30 min
    - Total: ~3 hours of spec/roadmap editing
```

---

## Remediation Checklist Summary

| Phase | Items | Effort | Blocking? |
|-------|-------|--------|-----------|
| R1 | 3 (H1, H2, ADV-1) | SMALL | Yes — spec contradictions |
| R2 | 2 (H8, L4) | TRIVIAL | No |
| R3 | 7 (C1, C2, C3, H3, H4, H5, H6, H7) | SMALL-MEDIUM | Yes — missing coverage |
| R4 | 0 | — | — |
| R5 | 4 (M1/M2, M3, M4, M5) | TRIVIAL | No |
| R6 | 2 (W7, W10) | TRIVIAL-SMALL | Semi — W10 should precede Phase 3 |
| R7 | 0 | — | — |
| R8 | 5 (L1-L3, L5-L6) | TRIVIAL | No |
| **Total** | **23** | **~3 hours** | **R1 + R3 must complete before tasklist** |
