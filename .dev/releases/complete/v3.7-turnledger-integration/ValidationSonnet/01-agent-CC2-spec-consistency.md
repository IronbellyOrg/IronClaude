# CC2: Internal Consistency Validation Report
## v3.3 Requirements Specification — Spec Document Consistency

**Agent**: CC2 (Internal Consistency Validator)
**Input**: v3.3-requirements-spec.md
**Date**: 2026-03-23
**Scope**: Internal consistency checks — cross-references, counts, ordering, coverage gaps

---

## Findings

### CC2-1: Phase 2 Test Count Mismatch — "FR-1.1–FR-1.18 (20 tests)"

- **Location**: v3.3-requirements-spec.md — Phased Implementation Plan → Phase 2; also Test File Layout
- **Issue**: The spec states "FR-1.1–FR-1.18 (20 tests)" in two places. The range FR-1.1–FR-1.18 contains 18 discrete numbered items. The claim of "20 tests" is internally inconsistent with the stated range. Furthermore, FR-1.19, FR-1.20, and FR-1.21 are all defined in the FR-1 section but are excluded from the range. Including all FR-1 subtests (FR-1.1 through FR-1.21, noting FR-1.21 is out-of-sequence) yields 21 tests, not 20.
- **Evidence**:
  - Statement A (Phase 2): `"FR-1.1–FR-1.18: Wiring point E2E tests (20 tests)"`
  - Statement B (Test File Layout): `"test_wiring_points.py  # FR-1.1–FR-1.18 (20 tests)"`
  - Statement C (FR-1 section): FR-1.1, FR-1.2, FR-1.3, FR-1.4, FR-1.5, FR-1.6, FR-1.7, **FR-1.21** (out-of-sequence, between FR-1.7 and FR-1.8), FR-1.8, FR-1.9, FR-1.10, FR-1.11, FR-1.12, FR-1.13, FR-1.14, FR-1.15, FR-1.16, FR-1.17, FR-1.18, FR-1.19, FR-1.20 — 21 subtests total
  - Statement D (SC-1): `"All 20+ wiring points have ≥1 E2E test | Test count ≥ 20, mapped to FR-1"` — the "20+" phrasing acknowledges there may be more, but the test file comment says exactly "20"
- **Severity**: HIGH
- **Recommended correction**: Update Phase 2 and Test File Layout to read `"FR-1.1–FR-1.21 (21 tests)"`. If FR-1.19, FR-1.20, or FR-1.21 are intentionally excluded from `test_wiring_points.py`, add explicit notes stating which file covers them. SC-1 should be updated to reflect the actual target count (21 rather than "20+").

---

### CC2-2: FR-1.21 Out-of-Sequence Ordering Anomaly

- **Location**: v3.3-requirements-spec.md — FR-1 section, between FR-1.7 and FR-1.8
- **Issue**: FR-1.21 is physically placed between FR-1.7 and FR-1.8 in the document. Numeric ordering places FR-1.21 after FR-1.20. This anomaly is not explained or annotated anywhere in the spec. A reader scanning the spec sequentially will encounter the requirements in the order: FR-1.1, FR-1.2, FR-1.3, FR-1.4, FR-1.5, FR-1.6, FR-1.7, **FR-1.21**, FR-1.8, FR-1.9, ..., FR-1.18, FR-1.19, FR-1.20 — which is disorienting and creates ambiguity about whether FR-1.21 is a late addition inserted between existing items or a sequencing error.
- **Evidence**:
  - Statement A (FR-1.7 header, line 122): `"#### FR-1.7: Post-Phase Wiring Hook — Both Paths"`
  - Statement B (FR-1.21 header, line 129): `"#### FR-1.21: check_wiring_report() Wrapper Call"` — immediately following FR-1.7, before FR-1.8
  - Statement C (FR-1.8 header, line 137): `"#### FR-1.8: Anti-Instinct Hook Return Type"` — follows FR-1.21
- **Severity**: MEDIUM
- **Recommended correction**: Either (a) renumber FR-1.21 to FR-1.7a or move it to the end of the FR-1 section after FR-1.20, or (b) add an inline note explaining the ordering (e.g., "FR-1.21 added post-initial-numbering; placed here due to logical proximity to FR-1.7"). The out-of-sequence placement without explanation is a documentation quality issue that will confuse implementers tracking requirement coverage.

---

### CC2-3: FR-5.3 Cross-Reference Imprecision — "This IS FR-4"

- **Location**: v3.3-requirements-spec.md — FR-5.3
- **Issue**: FR-5.3 states "This IS FR-4. Cross-referenced here for traceability." However, FR-4 is an entire framework comprising four sub-requirements (FR-4.1: Spec-Driven Wiring Manifest, FR-4.2: AST Call-Chain Analyzer, FR-4.3: Reachability Gate Integration, FR-4.4: Regression Test). FR-5.3 is titled "Reachability Gate (Weakness #2)" — which most closely maps to FR-4.3 specifically, not the entire FR-4 workstream. The cross-reference is structurally imprecise: saying "This IS FR-4" when the specific mapping is to FR-4.3 overstates the equivalence and could cause a reader to believe FR-5.3 encompasses the manifest schema, AST analyzer, and regression test.
- **Evidence**:
  - Statement A (FR-5.3): `"FR-5.3: Reachability Gate (Weakness #2) — This IS FR-4. Cross-referenced here for traceability."`
  - Statement B (FR-4 structure): FR-4.1 (Manifest), FR-4.2 (AST Analyzer), FR-4.3 (Gate Integration), FR-4.4 (Regression Test) — four distinct deliverables
  - Statement C (FR-4.3 title): `"FR-4.3: Reachability Gate Integration"` — this is the specific sub-requirement that corresponds to "Reachability Gate (Weakness #2)"
- **Severity**: LOW
- **Recommended correction**: Update FR-5.3 to read: "This is addressed by FR-4 (specifically FR-4.3: Reachability Gate Integration). Cross-referenced here for Weakness #2 traceability." This preserves the traceability intent while being precise about the mapping.

---

### CC2-4: SC-5 Value-Checking Not Specified in FR-1.11

- **Location**: v3.3-requirements-spec.md — Success Criteria (SC-5) vs FR-1.11
- **Issue**: SC-5 explicitly requires that an integration test proves KPI field VALUES are correct (not just present), specifically for `wiring_analyses_run`, `wiring_remediations_attempted`, and `wiring_net_cost`. FR-1.11, which is the requirement that SC-5 references, only requires that the report "includes" those fields — i.e., presence checking, not value correctness. The SC-5 success criterion is more stringent than its supporting requirement FR-1.11. This means FR-1.11 can be satisfied with a test that only asserts field presence, while SC-5 would remain unmet.
- **Evidence**:
  - Statement A (FR-1.11): `"Report content includes wiring KPI fields: wiring_analyses_run, wiring_remediations_attempted, wiring_net_cost"` — uses "includes", implies presence
  - Statement B (SC-5): `"KPI report accuracy validated — integration test proves field VALUES are correct (not just present): wiring_analyses_run, wiring_remediations_attempted, wiring_net_cost match computed expectations from test inputs"` — explicitly requires value equality, not just presence
- **Severity**: HIGH
- **Recommended correction**: Add a value-correctness assertion to FR-1.11. Append: "Assert: `wiring_analyses_run` equals the number of wiring analysis invocations observed during the sprint; `wiring_remediations_attempted` equals the number of remediation cycles triggered; `wiring_net_cost` equals total debited turns minus credited turns. Values must match computed expectations from test inputs, not merely be non-null." This brings FR-1.11 into alignment with SC-5.

---

### CC2-5: Test File Layout Assigns FR-3.2 to Two Files

- **Location**: v3.3-requirements-spec.md — Test File Layout section vs Phased Implementation Plan Phase 2
- **Issue**: FR-3.2 (Budget Exhaustion Scenarios, sub-tests FR-3.2a–FR-3.2d) is listed in two different test files simultaneously. The Test File Layout assigns `test_gate_rollout_modes.py` to cover FR-3.1–FR-3.3 (which includes FR-3.2), AND separately defines `test_budget_exhaustion.py` to cover FR-3.2a–FR-3.2d. This creates an overlap: either FR-3.2 tests live in `test_gate_rollout_modes.py`, or in `test_budget_exhaustion.py`, or duplicated across both. Phase 2 does not resolve this ambiguity — it groups FR-3.1–FR-3.3 together without specifying per-file assignment.
- **Evidence**:
  - Statement A (Test File Layout): `"test_gate_rollout_modes.py  # FR-3.1–FR-3.3 (12+ scenarios)"` — FR-3.2 is within FR-3.1–FR-3.3
  - Statement B (Test File Layout): `"test_budget_exhaustion.py   # FR-3.2a–FR-3.2d"` — FR-3.2 subtests explicitly assigned here
  - Statement C (Phase 2): `"FR-3.1–FR-3.3: Gate rollout mode + budget exhaustion tests (12+ scenarios)"` — no file-level disambiguation
- **Severity**: MEDIUM
- **Recommended correction**: Clarify the Test File Layout comment on `test_gate_rollout_modes.py` to read `"FR-3.1, FR-3.3 (mode matrix + interrupted sprint)"`, explicitly removing FR-3.2 from its scope. Update Phase 2 to acknowledge the split: "FR-3.1, FR-3.3: Gate rollout mode + interrupted sprint → `test_gate_rollout_modes.py`; FR-3.2: Budget exhaustion scenarios → `test_budget_exhaustion.py`."

---

### CC2-6: Wiring Manifest — Three Entries Absent from Verified Constructs Table

- **Location**: v3.3-requirements-spec.md — Wiring Manifest (v3.3) vs Verified Constructs table
- **Issue**: The authoritative 13-entry wiring manifest (Wiring Manifest v3.3 section) declares three convergence-path targets that have no corresponding entry in the Verified Constructs table at the top of the spec: `execute_fidelity_with_convergence`, `reimburse_for_progress`, and `handle_regression`. The Verified Constructs table is the "Code State Snapshot (Verified 2026-03-22)" and is presented as the authoritative record of what is wired in production. If these three functions are in the manifest as MUST-BE-REACHABLE constructs, their absence from the Verified Constructs table means either (a) their wired status has not been verified, or (b) the table is incomplete.

  Additionally: the wiring manifest entry `run_post_task_anti_instinct_hook` (manifest entry #2) has no direct match in the Verified Constructs table. The table lists `run_post_phase_wiring_hook()` (per-task path) and (per-phase path) but not `run_post_task_anti_instinct_hook`.

  Similarly, `run_post_task_wiring_hook` as a standalone function is not listed in the Verified Constructs table (it appears only indirectly via "per-task path" labeling on `run_post_phase_wiring_hook`).
- **Evidence**:
  - Statement A (Verified Constructs, convergence entries): `load_or_create`, `merge_findings`, `budget_snapshot on RunMetadata` — no `execute_fidelity_with_convergence`, `reimburse_for_progress`, or `handle_regression`
  - Statement B (Wiring Manifest v3.3): entries 11–13 are `execute_fidelity_with_convergence`, `reimburse_for_progress`, `handle_regression`, all with `from_entry: _run_convergence_spec_fidelity` and spec_refs `v3.05-FR7`, `v3.05-FR7`, `v3.05-FR8`
  - Statement C (Preamble): `"All v3.05/v3.1/v3.2 architectural constructs are verified present and wired in production code"` — this claim is not substantiated for the three absent convergence functions
- **Severity**: HIGH
- **Recommended correction**: Add the following entries to the Verified Constructs table (with actual line references once verified):
  - `execute_fidelity_with_convergence` | convergence.py:TBD | WIRED
  - `reimburse_for_progress` | convergence.py:TBD | WIRED
  - `handle_regression` | convergence.py:TBD | WIRED
  - `run_post_task_anti_instinct_hook` | executor.py:TBD | WIRED
  - `run_post_task_wiring_hook` | executor.py:TBD | WIRED

  If these cannot be verified as wired, the wiring manifest entries should be flagged as unverified, and the global claim that "All constructs are verified present and wired" should be qualified.

---

### CC2-7: Inconsistent spec_refs Between 9-Entry Example and 13-Entry Authoritative Manifest

- **Location**: v3.3-requirements-spec.md — FR-4.1 (example manifest) vs Wiring Manifest (v3.3) section
- **Issue**: The 9-entry illustrative manifest in FR-4.1 and the 13-entry authoritative manifest at the bottom of the spec use different `spec_ref` values for the same targets. For `_log_shadow_findings_to_remediation_log`, the example uses `"v3.1-T05"` while the authoritative manifest uses `"v3.1-T05/R3"`. For `_format_wiring_failure`, the example uses `"v3.1-T06"` while authoritative uses `"v3.1-T06/R4"`. For `_recheck_wiring`, the example uses `"v3.1-T07"` while authoritative uses `"v3.1-T07/R4"`. Additionally, in the 9-entry example, both `_recheck_wiring` and `build_kpi_report` share the spec_ref `"v3.1-T07"`, which is internally inconsistent (two different functions cannot both map exclusively to the same spec item unless T07 is a multi-function requirement).

  The spec states the FR-4.1 example is "for illustration" and directs readers to the authoritative manifest, but the inconsistency creates confusion about which spec_ref values are correct and whether the `/R3`, `/R4` suffixes represent sub-items or revision markers.
- **Evidence**:
  - Statement A (FR-4.1 example): `"target: ...executor._log_shadow_findings_to_remediation_log ... spec_ref: \"v3.1-T05\""`
  - Statement B (Authoritative manifest): `"target: ...executor._log_shadow_findings_to_remediation_log ... spec_ref: \"v3.1-T05/R3\""`
  - Statement C (FR-4.1 example, duplicate spec_ref): `"target: ...executor._recheck_wiring ... spec_ref: \"v3.1-T07\""` AND `"target: ...kpi.build_kpi_report ... spec_ref: \"v3.1-T07\""` — same spec_ref for two different targets
- **Severity**: LOW
- **Recommended correction**: (a) Add a note to the FR-4.1 example explicitly warning that spec_ref values are simplified for illustration and differ from the authoritative manifest. (b) Resolve the duplicate `v3.1-T07` spec_ref in the example (the authoritative manifest correctly differentiates these: `_recheck_wiring` → `v3.1-T07/R4`, `build_kpi_report` → `v3.1-T07`). (c) Define what the `/R3`, `/R4` suffixes mean (remediation sub-items, revision references, etc.).

---

### CC2-8: "Every Test Must Emit JSONL Record" — Constraint Not Mirrored in FR-7.3

- **Location**: v3.3-requirements-spec.md — Constraints section vs FR-7.3
- **Issue**: The Constraints section states "Audit trail: Every test must emit a JSONL record" — a mandatory, universal requirement. FR-7.3 (Audit Trail Runner) describes a pytest fixture that *provides* a `record()` method, but does not state that every test is *required* to call it. The fixture is opt-in as written; a test that never calls `audit_trail.record(...)` would pass without emitting any JSONL record, satisfying FR-7.3 without satisfying the Constraint. The enforcement mechanism for the universal constraint is absent from the requirements.
- **Evidence**:
  - Statement A (Constraints section): `"Audit trail: Every test must emit a JSONL record"`
  - Statement B (FR-7.3): `"A pytest fixture (audit_trail) that: Opens audit-trail.jsonl in the results directory; Provides record(test_id, spec_ref, assertion_type, inputs, observed, expected, verdict, evidence) method; Auto-flushes after each test; Produces a summary report at session end: total tests, passed, failed, coverage of wiring points"` — describes the fixture's capabilities, does not mandate that each test invokes it
  - Statement C (FR-7.3, absent): No text in FR-7.3 states "all tests in the v3.3 test suite MUST call audit_trail.record()" or describes enforcement (e.g., a pytest plugin hook that fails tests which do not emit a record)
- **Severity**: MEDIUM
- **Recommended correction**: Add an enforcement clause to FR-7.3: "All tests in the `tests/v3.3/` directory MUST declare the `audit_trail` fixture as a parameter. A pytest session-finish hook (in `conftest.py`) must verify that every collected test produced at least one JSONL record; tests missing audit records must be reported as failing the audit trail constraint." Alternatively, implement the `audit_trail` fixture as an autouse fixture for the `tests/v3.3/` scope, making it automatically active without requiring explicit declaration.

---

## Summary

**Total findings: 8**

| Severity | Count | Finding IDs |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 3 | CC2-1, CC2-4, CC2-6 |
| MEDIUM | 3 | CC2-2, CC2-5, CC2-8 |
| LOW | 2 | CC2-3, CC2-7 |

### Key Issues by Priority

**HIGH priority (must fix before implementation):**
1. **CC2-1** — Phase 2 claims "FR-1.1–FR-1.18 (20 tests)" but the range contains 18 items, 3 additional FR-1 subtests exist outside the range, and the total is 21. Implementers will produce the wrong test count.
2. **CC2-4** — FR-1.11 only requires KPI field *presence*; SC-5 requires *value correctness*. FR-1.11 must be strengthened or SC-5 will never be satisfiable from a passing FR-1.11 test alone.
3. **CC2-6** — Three mandatory wiring manifest entries (`execute_fidelity_with_convergence`, `reimburse_for_progress`, `handle_regression`) have no corresponding Verified Constructs table entries, undermining the spec's opening claim that all constructs are verified wired.

**MEDIUM priority (fix before handoff to implementers):**
4. **CC2-2** — FR-1.21 out-of-sequence placement will cause coverage tracking errors.
5. **CC2-5** — FR-3.2 assigned to two test files without resolution guidance.
6. **CC2-8** — "Every test must emit JSONL" is a constraint with no enforcement mechanism in FR-7.3.

**LOW priority (clarifications):**
7. **CC2-3** — FR-5.3 cross-reference says "IS FR-4" when it means "IS FR-4.3."
8. **CC2-7** — Illustrative and authoritative manifests have divergent spec_refs; `/R3`/`/R4` suffixes undefined.
