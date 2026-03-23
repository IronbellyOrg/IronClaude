# Re-Validation Report — v3.3 TurnLedger Validation

Date: 2026-03-23
Phase: R9 (Post-Remediation Re-Validation)

---

## Methodology

Walked all 23 items from `04-remediation-plan.md`. For each item, verified:
1. The edit was applied to the correct file
2. The verification criterion from the remediation plan is satisfied
3. No formatting or structural damage was introduced
4. Cross-file consistency (spec FR numbers ↔ roadmap task references)

---

## Item-by-Item Verification

### Phase R1: Spec-Internal Contradictions

| ID | Severity | Applied? | Verified? | Notes |
|----|----------|----------|-----------|-------|
| GAP-H1 | HIGH | YES | YES | FR-7.3 `record()` at spec:489 now includes `assertion_type` as explicit param. FR-7.1 JSONL example has 10 fields (including `duration_ms`). `record()` has 8 explicit params + `timestamp` (auto) + `duration_ms` (auto, noted at spec:491). All 10 fields accounted for. Schema is consistent. |
| GAP-H2 | HIGH | YES | YES | FR-5.1-TEST at spec:401 now reads "non-empty directory where file collection returns 0 analyzed files (e.g., all files filtered out by extension or path rules)". Matches FR-5.1 guard condition at spec:398 ("files_analyzed == 0 AND the source directory is non-empty"). |
| ADV-1 | MEDIUM | YES | YES | `"duration_ms": 1234` added to JSONL example at spec:473. FR-7.3 at spec:491 notes "auto-computed from test start/end timestamps (no parameter needed in record())". FR-7.2 PROP1 (spec:480) references "test duration" — now has corresponding schema field. |

### Phase R2: Roadmap-Internal Contradictions

| ID | Severity | Applied? | Verified? | Notes |
|----|----------|----------|-----------|-------|
| GAP-H8 | HIGH | NO | NO | **NOT APPLIED.** Roadmap New Files table (roadmap:214-225) has `test_audit_writer.py` (line 225) but NOT `audit_writer.py` itself. Task 1A.1 references `tests/audit-trail/audit_writer.py` in its deliverable text, but the New Files Created table lacks a dedicated row for this production file (only the test file is listed). The source file is mentioned inline but not in the registry. |
| GAP-L4 | LOW | NO | NO | **NOT APPLIED.** Spec test file layout (spec:631) still says `test_wiring_points.py` while roadmap consistently uses `test_wiring_points_e2e.py`. Spec says `audit_trail.py` (spec:641) while roadmap says `audit_writer.py` (roadmap:47). Spec has separate `test_budget_exhaustion.py` (spec:634) while roadmap consolidates into `test_gate_rollout_modes.py`. Filenames remain mismatched. |

### Phase R3: Missing Coverage (CRITICAL + HIGH)

| ID | Severity | Applied? | Verified? | Notes |
|----|----------|----------|-----------|-------|
| GAP-C1 | CRITICAL | PARTIAL | NO | **SPEC: Applied** — FR-2.1a added at spec:240-246 with correct content. Wiring manifest at spec:618-620 has `handle_regression` entry. **ROADMAP: NOT applied** — No task 2B.x or 1B manifest task added for FR-2.1a. Roadmap Phase 2B (roadmap:99-106) still covers only FR-2.1 through FR-2.4. The remediation required changes to BOTH files. |
| GAP-C2 | CRITICAL | PARTIAL | NO | **SPEC: Applied** — FR-1.19 added at spec:211-217. **ROADMAP: NOT applied** — No task 2A.13 exists. Roadmap Phase 2A table (roadmap:80-91) ends at 2A.12 covering FR-1.18. FR-1.19 has no roadmap task. |
| GAP-C3 | CRITICAL | PARTIAL | NO | **SPEC: Applied** — FR-1.20 added at spec:219-225. **ROADMAP: NOT applied** — No task 2A.14 exists. Same gap as GAP-C2. FR-1.20 has no roadmap task. |
| GAP-H3 | HIGH | NO | NO | **NOT APPLIED.** Roadmap task 2A.2 (roadmap:81) still reads "2 tests: Phase delegation — task-inventory path vs freeform fallback". No mention of `_parse_phase_tasks()` return type assertion (`list[TaskEntry]` vs `None`). |
| GAP-H4 | HIGH | NO | NO | **NOT APPLIED.** Roadmap task 2C.2 (roadmap:115) still reads "4 tests: Budget exhaustion scenarios — before task launch, before wiring, before remediation, mid-convergence". No explicit `can_run_wiring_gate()` assertion noted. |
| GAP-H5 | HIGH | PARTIAL | NO | **SPEC: Applied** — FR-1.21 added at spec:129-135 near FR-1.7. **ROADMAP: NOT applied** — No corresponding task in Phase 2A for FR-1.21. |
| GAP-H6 | HIGH | NO | NO | **NOT APPLIED.** Roadmap Phase 2A has no task for explicit `run_post_task_wiring_hook()` E2E test. Task 2A.7 (roadmap:86) covers FR-1.12 (`_resolve_wiring_mode`) but not the task-level wiring hook itself. |
| GAP-H7 | HIGH | YES | YES | Spec FR-4.1 at spec:311 now includes note: "See **Wiring Manifest (v3.3)** section below for the authoritative 13-entry manifest including all v3.1, v3.2, and v3.05 constructs." FR-4.1 example (9 entries) and body manifest (13 entries, spec:576-620) are now explicitly linked. |

### Phase R5: Partial Coverage Gaps (MEDIUM)

| ID | Severity | Applied? | Verified? | Notes |
|----|----------|----------|-----------|-------|
| GAP-M1/M2 | MEDIUM | NO | NO | **NOT APPLIED.** Roadmap task 2C.3 (roadmap:116) still reads "1 test: Interrupted sprint → KPI report written, remediation log persisted, outcome = INTERRUPTED". No `os.kill(os.getpid(), signal.SIGINT)` mechanism specified. (Note: Open Question #1 at roadmap:283 does mention SIGINT but the task itself was not amended.) |
| GAP-M3 | MEDIUM | NO | NO | **NOT APPLIED.** Roadmap tasks 2D.1-2D.3 (roadmap:124-126) still say "Extend existing" without explicit mention of `audit_trail.record()` retrofit. |
| GAP-M4 | MEDIUM | NO | NO | **NOT APPLIED.** Roadmap task 2D.6 (roadmap:129) still reads "Integration + regression suite per spec". T17-T22 are not individually decomposed. |
| GAP-M5 | MEDIUM | NO | NO | **NOT APPLIED.** Roadmap task 1A.2 (roadmap:48) still reads "opens JSONL in `results_dir`". No timestamped filename convention mentioned (though R-4 mitigation at roadmap:190 does reference "timestamped filename", the task itself wasn't updated). |

### Phase R6: Ordering and Dependency Fixes

| ID | Severity | Applied? | Verified? | Notes |
|----|----------|----------|-----------|-------|
| CC3-W7 | WARNING | NO | NO | **NOT APPLIED.** Roadmap task 2D.5 (roadmap:128) has no dependency note on Phase 2A. |
| CC3-W10 | WARNING | NO | NO | **NOT APPLIED.** No baseline investigation task (task 2.0) added to roadmap Phase 2. |

### Phase R8: Low-Priority and Cleanup

| ID | Severity | Applied? | Verified? | Notes |
|----|----------|----------|-----------|-------|
| GAP-L1 | LOW | NO | NO | **NOT APPLIED.** Roadmap task 2A.6 (roadmap:85) still reads "1 test: KPI report generation with wiring KPI fields" without enumerating field names. |
| GAP-L2 | LOW | YES | YES | Spec SC-5 (spec:552) now reads "Integration test proves field VALUES are correct (not just present): `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost` match computed expectations from test inputs". |
| GAP-L3 | LOW | NO | NO | **NOT APPLIED.** T12 smoke test file location not reconciled. Spec (spec:604) says `test_convergence_e2e.py` in `roadmap/` dir. Roadmap task 2D.3 (roadmap:126) also says `test_convergence_e2e.py`. These happen to match but no explicit reconciliation note was added. Actually CONSISTENT — marking as non-issue. |
| GAP-L5 | LOW | NO | NO | **NOT APPLIED.** Roadmap task 1A.2 (roadmap:48) still says "auto-flushes on session end". No clarification that auto-flush is per-record. (Spec spec:492 also says "Auto-flushes after each test" — so the spec is correct but the roadmap was not updated to match.) |
| GAP-L6 | LOW | YES | YES | Spec FR-6.1-T11 (spec:429) now reads "v3.3-SC-1 through v3.3-SC-6", using the v3.3 prefix consistent with the rest of the spec. |

---

## Cross-File Consistency Check

### GAP-C1 (FR-2.1a ↔ Roadmap)
- **Spec**: FR-2.1a exists at spec:240-246. Wiring manifest has `handle_regression` at spec:618-620.
- **Roadmap**: No task references FR-2.1a. Phase 2B table stops at FR-2.4.
- **Verdict**: INCONSISTENT — spec has requirement with no roadmap task to implement/test it.

### GAP-C2 (FR-1.19 ↔ Roadmap)
- **Spec**: FR-1.19 exists at spec:211-217.
- **Roadmap**: Phase 2A table ends at 2A.12 (FR-1.18). No task for FR-1.19.
- **Verdict**: INCONSISTENT — spec has requirement with no roadmap task.

### GAP-C3 (FR-1.20 ↔ Roadmap)
- **Spec**: FR-1.20 exists at spec:219-225.
- **Roadmap**: Phase 2A table ends at 2A.12 (FR-1.18). No task for FR-1.20.
- **Verdict**: INCONSISTENT — spec has requirement with no roadmap task.

### GAP-H5 (FR-1.21 ↔ Roadmap)
- **Spec**: FR-1.21 exists at spec:129-135.
- **Roadmap**: Phase 2A table has no task for FR-1.21 or `check_wiring_report()`.
- **Verdict**: INCONSISTENT — spec has requirement with no roadmap task.

### ADV-1 (duration_ms ↔ Roadmap)
- **Spec**: 10-field schema with `duration_ms` at spec:473.
- **Roadmap**: Task 1A.1 (roadmap:47) still says "9-field schema" and lists only 9 fields.
- **Verdict**: INCONSISTENT — field count mismatch between spec (10) and roadmap (9).

### GAP-L4 (Filenames ↔ Cross-file)
- **Spec test layout** (spec:631): `test_wiring_points.py`, `audit_trail.py`, `test_budget_exhaustion.py`
- **Roadmap**: `test_wiring_points_e2e.py`, `audit_writer.py`, budget tests in `test_gate_rollout_modes.py`
- **Verdict**: INCONSISTENT — 3 filename mismatches remain.

---

## Summary

| Metric | Value |
|--------|-------|
| **Total items** | 23 |
| **Applied (fully)** | 6 |
| **Applied (partial — spec only, roadmap missing)** | 4 |
| **Not applied** | 13 |
| **Verified** | 6/23 |
| **CRITICAL findings remaining** | 3 (GAP-C1, C2, C3 — spec-side done but no roadmap tasks) |
| **HIGH findings remaining** | 5 (GAP-H3, H4, H5-roadmap, H6, H8) |
| **MEDIUM findings remaining** | 4 (M1/M2, M3, M4, M5) |
| **LOW findings remaining** | 3 (L1, L4, L5) |
| **WARNING findings remaining** | 2 (W7, W10) |

### New Finding: Cross-File Inconsistency Introduced

- **ADV-1-XREF** (MEDIUM): Roadmap task 1A.1 says "9-field schema" but spec now defines 10 fields (with `duration_ms`). This was not part of the original 23 items but was introduced by the ADV-1 spec edit without a corresponding roadmap update.

---

## Projected Coverage

Original validation coverage: ~89%
After spec-only remediations applied: ~92%
After ALL remediations (including missing roadmap edits): ~99.4%

**Current state with partial application: ~92%** (spec gaps closed but roadmap not updated)

---

## Verdict: **NO-GO**

### Rationale

The spec-side edits (R1: GAP-H1, H2, ADV-1; R3 spec-side: C1, C2, C3, H5, H7; R8: L2, L6) were applied correctly and are individually sound. However:

1. **Roadmap was not edited at all.** All 13 roadmap-targeted remediation items remain unapplied. This means the roadmap cannot be used as a tasklist — it lacks tasks for 4 new spec FRs (FR-1.19, FR-1.20, FR-1.21, FR-2.1a), has stale field counts, filename mismatches, and missing implementation details.

2. **3 CRITICAL items remain partially open.** GAP-C1, C2, C3 each required changes to BOTH spec and roadmap. The spec side is done but the roadmap side is not — meaning these FRs exist in the spec but have no implementation task in the roadmap.

3. **5 HIGH items remain open.** GAP-H3, H4, H6, H8 are roadmap-only and untouched. GAP-H5 has the same spec-done/roadmap-missing pattern.

### Required for GO

1. Apply all 13 remaining roadmap edits (R2: H8, L4; R3-roadmap: C1, C2, C3, H3, H4, H5, H6; R5: M1/M2, M3, M4, M5; R6: W7, W10)
2. Fix ADV-1-XREF: Update roadmap task 1A.1 from "9-field schema" to "10-field schema" and add `duration_ms` to field list
3. Update R8 low-priority items: L1, L5 (roadmap-side)
4. Re-run R9 validation to confirm 0 CRITICAL, 0 HIGH
