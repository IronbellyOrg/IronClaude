# CC4 Completeness Sweep — v3.3 TurnLedger Validation

**Agent**: CC4 (Cross-Cutting Completeness)
**Date**: 2026-03-23
**Inputs**: v3.3-requirements-spec.md, roadmap-final.md, 00-requirement-universe.md

---

## Check 1: Spec Re-Scan for Missed Requirements

### Shall/Must/Will Statements Not Captured

| Line(s) | Statement | Status |
|----------|-----------|--------|
| 78 | "Tests MUST NOT mock gate functions or core orchestration logic" | CAPTURED as FR-1-CONSTRAINT and NFR-1 |
| 366 | "return a FAIL report (not a clean PASS)" | CAPTURED in FR-5.1 |
| 446 | "A third party with no prior knowledge MUST be able to determine..." | CAPTURED in FR-7.2 |
| 613 | "UV only" | CAPTURED as NFR-2 |
| 614 | "No mocks on gate functions" | CAPTURED (duplicate of NFR-1) |
| 617 | "Every test must emit a JSONL record" | CAPTURED as NFR-4 |
| 618 | "Wiring manifest is the source of truth for reachability gate" | CAPTURED as NFR-5 |

**No missed shall/must/will statements.**

### Implicit Requirements in Architecture Decisions

| Finding | Severity | Details |
|---------|----------|---------|
| `_subprocess_factory` stability contract | LOW | Spec line 502 and roadmap Appendix A.1 note this is the "sole allowed injection seam." The requirement universe captures this as NFR-1 and FR-1-CONSTRAINT, but does NOT explicitly require a test that `_subprocess_factory` itself is a stable, functioning injection point. The roadmap task 2A covers usage implicitly. No separate REQ needed — coverage is adequate through usage. |
| `conftest.py` as plugin registration | LOW | Spec line 595 and roadmap 1A.2 both mention `conftest.py` at `tests/v3.3/conftest.py`. The requirement universe captures this in FILE-NEW-3 but does not call out the plugin registration mechanism. This is an implementation detail, not a requirement gap. |

**No CRITICAL or HIGH findings.**

### Requirements Buried in Prose, Footnotes, Examples

| Finding | Severity | Details |
|---------|----------|---------|
| JSONL schema has 9 fields, but FR-7.3 `record()` method lists only 7 params | **HIGH** | Spec line 420-441 defines 9 fields: `test_id`, `spec_ref`, `timestamp`, `assertion_type`, `inputs`, `observed`, `expected`, `verdict`, `evidence`. The FR-7.3 text says the fixture provides `record(test_id, spec_ref, inputs, observed, expected, verdict, evidence)` — only 7 params. `timestamp` is auto-generated (acceptable), but `assertion_type` is missing from the `record()` signature. The requirement universe FR-7.1 captures the 9-field schema, and FR-7.3 captures the 7-param method. The discrepancy is present in the SPEC ITSELF (lines 420 vs 456), not a universe extraction error. **The universe correctly mirrors the spec's inconsistency.** Recommend: roadmap implementer must resolve — either `assertion_type` is auto-derived or added as an 8th param. |
| FR-1.11 requires 3 specific KPI field names | LOW | `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost` — these are captured in FR-1.11 text. No gap. |
| FR-5.1 test description says "empty directory" but requirement says "non-empty" | **HIGH** | Spec line 369: "Point `run_wiring_analysis()` at an empty directory. Assert FAIL, not silent PASS." But line 366 says the FAIL condition is "files_analyzed == 0 AND the source directory is non-empty." The test as described (empty directory) would NOT trigger the new assertion — an empty directory has no `*.py` files, so the guard wouldn't fire. The requirement universe FR-5.1-TEST captures the spec text verbatim ("empty directory"), preserving the spec's own contradiction. **The roadmap task 3B.1 must clarify: the test should use a directory with `.py` files but where the analysis pipeline returns 0 analyzed files (e.g., all files filtered out), not a literally empty directory.** |

### Test Cases Implied but Not Explicitly Listed

| Finding | Severity | Details |
|---------|----------|---------|
| No explicit test for `all_gate_results` accumulator being empty for 0-phase sprint | LOW | Edge case — spec only requires testing N-phase sprints. Not a gap. |
| No explicit test for `DeferredRemediationLog.persist_path` file creation on disk | LOW | FR-1.3 tests construction, FR-3.3 tests persistence on interrupt. Covered indirectly. |
| Phase 4 validation tasks (4.1-4.6) have no test requirements in universe | LOW | These are process validation steps, not code requirements. Correctly excluded from requirement universe. |

### Data Model Details (Schema Fields, Types)

| Finding | Severity | Details |
|---------|----------|---------|
| `budget_snapshot` on `RunMetadata` (spec line 46) | LOW | Referenced in Code State Snapshot table and FR-2.1. Captured in universe FR-2.1 text. No gap. |
| `SHADOW_GRACE_INFINITE` constant (spec line 38) | **CRITICAL** | Present in Code State Snapshot table (line 38) but has NO corresponding FR or test requirement in the universe. This is a verified wiring point in the spec with no test coverage plan. See Check 7 below for full analysis. |
| `__post_init__()` derivation (spec line 39) | **CRITICAL** | Present in Code State Snapshot table (line 39) but has NO corresponding FR or test requirement. The `__post_init__()` method in `models.py:338-384` performs critical derivation logic for sprint config but no FR requires validating it. See Check 7. |
| `source_dir` → `src/superclaude` (spec line 44) | LOW | Marked as already fixed (SCOPE-OUT-1, spec line 64). Correctly excluded. |
| `check_wiring_report()` wrapper (spec line 45) | **HIGH** | Present in Code State Snapshot table (line 45: `wiring_gate.py:1079`) but has NO corresponding FR test requirement. This is a verified wiring point with no planned test. Should have an FR-1.x entry. |

### Config Requirements

No config-specific requirements missed. `wiring_gate_enabled`, `wiring_gate_grace_period` (spec line 37) are referenced through FR-3 gate mode tests.

---

## Check 2: Every REQ Has at Least One Domain Agent Covering It

Checking against domain agent assignments from the decomposition plan.

| REQ ID | Domain Agent | Covered? |
|--------|-------------|----------|
| FR-1.1 through FR-1.18 | D1 (wiring-e2e) | YES |
| FR-1-CONSTRAINT | D1, D5 (cross-cutting) | YES |
| FR-2.1 through FR-2.4 | D2 (turnledger-lifecycle) | YES |
| FR-3.1a through FR-3.3 | D3 (gate-modes) | ASSUMED — D3 agent not yet filed but domain taxonomy assigns it |
| FR-4.1 through FR-4.4 | D4 (reachability) | ASSUMED — D4 agent not yet filed |
| FR-5.1, FR-5.2 | D5 (pipeline-fixes) | ASSUMED — D5 agent not yet filed |
| FR-6.1-T07 through FR-6.2-T17-T22 | D6 (qa-gaps) | ASSUMED — D6 agent not yet filed |
| FR-7.1 through FR-7.3 | D7 (audit-trail) | ASSUMED — D7 agent not yet filed |
| NFR-1 through NFR-6 | Cross-cutting (CC agents) | YES — CC4 (this sweep) |
| SC-1 through SC-12 | Cross-cutting validation | YES — mapped in universe |

**Only D1 and D2 agent reports are filed so far.** D3-D7 are planned but not yet written. No REQ is orphaned from a domain assignment, but execution depends on those agents completing their reports.

---

## Check 3: Implicit Systems Required by Explicit Ones

| Explicit Requirement | Implicit Dependency | Status |
|---------------------|---------------------|--------|
| FR-7.3 (audit_trail fixture) | `tests/v3.3/conftest.py` must exist | CAPTURED in FILE-NEW-3 |
| FR-7.3 (audit_trail fixture) | `results_dir` must be configured/accessible | IMPLICIT — not captured as a separate REQ. The fixture needs a results directory path. Roadmap 1A.2 mentions `results_dir` but doesn't specify how it's configured. **LOW** — implementation detail. |
| FR-4.1 (YAML manifest) | YAML parser dependency | No new dependency — `yaml` or stdlib sufficient. LOW. |
| FR-6.1-T07 (test_convergence_wiring.py) | `tests/roadmap/` directory structure | Already exists per git status. No gap. |
| FR-5.2 (fidelity_checker.py) | `_run_checkers()` must have extensible checker registry | Roadmap 3A.3 covers wiring. Appendix A.6 documents the registry. No gap. |
| All tests (NFR-4) | JSONL writer must handle concurrent test execution | **HIGH** — If tests run in parallel (xdist), the session-scoped JSONL writer could have write contention. The spec and roadmap don't address parallel test execution. Recommend: document that audit trail assumes sequential execution, or add file locking. |

---

## Check 4: Wiring Manifest Entries (Spec Lines 530-586) — All Traceable to Spec FRs?

| Manifest Entry | spec_ref | Traceable FR? | Status |
|---------------|----------|---------------|--------|
| `run_post_task_wiring_hook` → `execute_sprint` | v3.1-T04 | FR-1.7 (partially — FR-1.7 covers `run_post_phase_wiring_hook`, not `run_post_task_wiring_hook`) | **HIGH** — FR-1.7 is about the *phase* hook. The *task* wiring hook has no dedicated FR. It is exercised indirectly through FR-2.2 and FR-3.1 mode tests, but has no explicit wiring-point E2E test like the other FR-1.x items. |
| `run_post_task_anti_instinct_hook` → `execute_sprint` | v3.1-T05 | FR-1.8 | OK |
| `_log_shadow_findings_to_remediation_log` → `execute_sprint` | v3.1-T05/R3 | FR-1.13 | OK |
| `_format_wiring_failure` → `execute_sprint` | v3.1-T06/R4 | FR-1.14 | OK |
| `_recheck_wiring` → `execute_sprint` | v3.1-T07/R4 | FR-1.14 | OK |
| `_resolve_wiring_mode` → `execute_sprint` | v3.2-T09/R5 | FR-1.12 | OK |
| `execute_phase_tasks` → `execute_sprint` | v3.1-T04 | FR-1.5 | OK |
| `build_kpi_report` → `execute_sprint` | v3.1-T07 | FR-1.11 | OK |
| `run_post_phase_wiring_hook` → `execute_sprint` | v3.2-T02 | FR-1.7 | OK |
| `SprintGatePolicy` → `execute_sprint` | v3.2-T06 | FR-1.4 | OK |
| `execute_fidelity_with_convergence` → `_run_convergence_spec_fidelity` | v3.05-FR7 | FR-2.1 | OK |
| `reimburse_for_progress` → `_run_convergence_spec_fidelity` | v3.05-FR7 | FR-2.1 | OK |
| `handle_regression` → `_run_convergence_spec_fidelity` | v3.05-FR8 | **MISSING** | **CRITICAL** — `handle_regression` appears in wiring manifest (line 583-585) but has NO corresponding FR in the spec or requirement universe. There is no test planned for this function's reachability or behavior. |

**Manifest vs. FR-4.1 in spec lines 279-325**: The manifest in lines 530-586 is a superset of the manifest in FR-4.1 (lines 279-325). The earlier FR-4.1 manifest has 9 entries; the full manifest at lines 530-586 has 13 entries. The additional entries are:
- `run_post_task_anti_instinct_hook` (line 546-548)
- `execute_phase_tasks` (line 561-563)
- `SprintGatePolicy` (line 572-574)
- `handle_regression` (line 583-585)

The requirement universe FR-4.1 references lines 277-325 but the full manifest at lines 530-586 contains the authoritative set. **The universe should reference both manifest locations.**

---

## Check 5: Test File Layout (Spec Lines 592-607) — Matches Roadmap File References?

| Spec Layout Entry | Roadmap Reference | Match? |
|------------------|-------------------|--------|
| `tests/v3.3/conftest.py` | 1A.2: "registers as conftest.py plugin at tests/v3.3/conftest.py" | YES |
| `tests/v3.3/test_wiring_points.py` | 2A: `tests/v3.3/test_wiring_points_e2e.py` | **MISMATCH** — Spec says `test_wiring_points.py`, roadmap says `test_wiring_points_e2e.py`. Cosmetic but should be reconciled. |
| `tests/v3.3/test_turnledger_lifecycle.py` | 2B: `tests/v3.3/test_turnledger_lifecycle.py` | YES |
| `tests/v3.3/test_gate_rollout_modes.py` | 2C: `tests/v3.3/test_gate_rollout_modes.py` | YES |
| `tests/v3.3/test_budget_exhaustion.py` | 2C.2: Budget tests in `test_gate_rollout_modes.py` | **MISMATCH** — Spec has a separate `test_budget_exhaustion.py`, roadmap merges budget exhaustion tests into `test_gate_rollout_modes.py` (task 2C.2). The roadmap's approach is reasonable (budget exhaustion is a subset of gate mode behavior), but differs from spec layout. |
| `tests/v3.3/test_reachability_eval.py` | 1B.5: `tests/v3.3/test_reachability_eval.py` | YES |
| `tests/v3.3/test_pipeline_fixes.py` | 3B: Tests split across 3B.1-3B.3 (no single file named) | **MISMATCH** — Spec has `test_pipeline_fixes.py`, roadmap doesn't name a specific file for pipeline fix tests. Roadmap should specify. |
| `tests/roadmap/test_convergence_wiring.py` | 2D.1: `tests/roadmap/test_convergence_wiring.py` | YES |
| `tests/roadmap/test_convergence_e2e.py` | 2D.2-2D.3: `tests/roadmap/test_convergence_e2e.py` | YES |
| `tests/audit-trail/audit_trail.py` | 1A.1: `tests/audit-trail/audit_writer.py` | **MISMATCH** — Spec says `audit_trail.py`, roadmap says `audit_writer.py`. |
| — | 2D.6: `tests/v3.3/test_integration_regression.py` | NOT IN SPEC — Roadmap adds a file not in spec's test layout. This is additive (positive), not a gap. |

**4 filename mismatches** between spec and roadmap. All are LOW severity (cosmetic), but should be reconciled before implementation to avoid confusion.

---

## Check 6: Every SC-* Has at Least One FR Mapping

| SC | Mapped FRs | Adequate? |
|----|-----------|-----------|
| SC-1 | FR-1.1 through FR-1.18 | YES — 18+ FRs |
| SC-2 | FR-2.1, FR-2.2, FR-2.3, FR-2.4 | YES — 4 FRs covering 4 paths |
| SC-3 | FR-3.1a, FR-3.1b, FR-3.1c, FR-3.1d | YES — 4 modes x 2 paths |
| SC-4 | NFR-3 | YES — baseline regression constraint |
| SC-5 | FR-1.11 | YES — KPI report test |
| SC-6 | FR-3.2a, FR-3.2b, FR-3.2c, FR-3.2d | YES — 4 exhaustion scenarios |
| SC-7 | FR-4.4 | YES — regression test |
| SC-8 | FR-6.1-T07, FR-6.1-T11, FR-6.1-T12, FR-6.1-T14, FR-6.2-T02, FR-6.2-T17-T22 | YES — all QA gaps listed |
| SC-9 | FR-4.4 | YES — reachability detection |
| SC-10 | FR-5.1 | YES — 0-files assertion |
| SC-11 | FR-5.2 | YES — fidelity checker |
| SC-12 | FR-7.1, FR-7.2, FR-7.3 | YES — audit trail properties |

**All 12 success criteria have FR mappings. No gaps.**

---

## Check 7: Code State Snapshot Table (Spec Lines 16-47) — All Items Have Test Requirements?

| Snapshot Item | Line | Has FR/Test? | Status |
|--------------|------|-------------|--------|
| TurnLedger constructed | 19 | FR-1.1 | OK |
| ShadowGateMetrics constructed | 20 | FR-1.2 | OK |
| DeferredRemediationLog constructed | 21 | FR-1.3 | OK |
| SprintGatePolicy constructed | 22 | FR-1.4 | OK |
| `all_gate_results` accumulator | 23 | FR-1.9 | OK |
| `execute_phase_tasks()` delegation | 24 | FR-1.5 | OK |
| ClaudeProcess fallback | 25 | FR-1.6 | OK |
| `run_post_phase_wiring_hook()` (per-task) | 26 | FR-1.7 | OK |
| `run_post_phase_wiring_hook()` (per-phase) | 27 | FR-1.7 | OK |
| `build_kpi_report()` | 28 | FR-1.11 | OK |
| `_parse_phase_tasks()` returns `list[TaskEntry] \| None` | 29 | **MISSING** | **HIGH** — No FR tests the return type of `_parse_phase_tasks()`. FR-1.5 tests that task-inventory phases use `execute_phase_tasks()`, but doesn't test the parser's return type contract. This is a verified wiring point with no explicit test. |
| `_resolve_wiring_mode()` called | 30 | FR-1.12 | OK |
| `_log_shadow_findings_to_remediation_log()` | 31 | FR-1.13 | OK |
| `_format_wiring_failure()` | 32 | FR-1.14 | OK |
| `_recheck_wiring()` | 33 | FR-1.14 | OK |
| BLOCKING lifecycle | 34 | FR-1.14 | OK |
| `debit_wiring()` / `credit_wiring()` / `can_run_wiring_gate()` | 35 | FR-2.3 (partial) | **HIGH** — `can_run_wiring_gate()` has no dedicated test. FR-2.3 tests `debit_wiring()` and `credit_wiring()` but `can_run_wiring_gate()` is only exercised implicitly. |
| `wiring_analyses_count` | 36 | FR-2.3 | OK |
| `wiring_gate_enabled` / `wiring_gate_grace_period` | 37 | FR-3.1 (implicit) | OK — tested through mode matrix |
| `SHADOW_GRACE_INFINITE` | 38 | **MISSING** | **CRITICAL** — No FR or test. This constant (models.py:293) is used in shadow mode grace period logic but has no explicit validation. |
| `__post_init__()` derivation | 39 | **MISSING** | **CRITICAL** — No FR or test. The `__post_init__()` method (models.py:338-384) performs critical derivation of sprint config fields. No test validates these derivations. |
| `load_or_create(path, release_id, spec_hash)` | 40 | FR-1.15 | OK |
| `merge_findings(structural, semantic, run_number)` | 41 | FR-1.16 | OK |
| Dict→Finding conversion | 42 | FR-1.17 | OK |
| `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET=61)` | 43 | FR-1.18 | OK |
| `source_dir` → `src/superclaude` | 44 | SCOPE-OUT-1 | OK — out of scope (already fixed) |
| `check_wiring_report()` wrapper | 45 | **MISSING** | **HIGH** — No FR or test. This wrapper (wiring_gate.py:1079) is a verified wiring point with no planned test. |
| `budget_snapshot` on RunMetadata | 46 | FR-2.1 (partial) | OK — tested as part of convergence path |

---

## Check 8: In-Scope Workstreams (Lines 52-61) — All Covered by FRs?

| Workstream | Spec Lines | Covering FRs | Status |
|-----------|------------|-------------|--------|
| WS1: Architectural Validation | 54 | FR-1.1-FR-1.18 | OK |
| WS2: Unit Test Coverage | 55 | FR-1 (wiring points) | OK |
| WS3: Integration Tests | 56 | FR-2.1-FR-2.4 | OK |
| WS4 (partial): Reachability Eval | 57 | FR-4.1-FR-4.4 | OK |
| WS5: Remaining QA Gaps | 58 | FR-6.1, FR-6.2 | OK |
| Pipeline Weaknesses #2, #3, #4 | 59 | FR-5.1, FR-5.2, FR-5.3/FR-4 | OK |
| Audit Trail Infrastructure | 60 | FR-7.1-FR-7.3 | OK |

**All 7 workstreams are covered by FRs. No gaps.**

---

## Check 9: NFR-1 (No mock.patch on Gate Functions) — Roadmap Task Enforcing It?

**YES.** Roadmap Phase 4, Task 4.2: "Grep-audit: confirm no `mock.patch` on gate functions or orchestration logic across all v3.3 test files."

This is a validation-phase check, not a code-level enforcement. There is no automated gate or CI check that prevents mock.patch from being introduced. **Recommendation**: Consider adding a pytest plugin or conftest.py hook that fails tests importing `mock.patch` on protected symbols. This is a LOW-priority enhancement, not a gap in the spec.

---

## Check 10: NFR-2 (UV Only) — Mentioned in Roadmap?

**YES.** Roadmap "Environment Requirements" section: "All Python execution via UV (NFR-2)."

Also captured in requirement universe as NFR-2. The roadmap does not have a specific task to validate this (e.g., grep for `python -m pytest`), but it's stated as a constraint. **LOW** — enforcement is via team convention, not automation.

---

## Check 11: Spec Section Cross-References — Referenced Sections Captured?

| Referencing Req | Referenced Section | Captured? |
|----------------|-------------------|-----------|
| FR-5.3 ("This IS FR-4") | FR-4 | YES — FR-5.3 captured in universe with `related_reqs: ["FR-4.3"]` |
| FR-1.14 references executor.py:554-608 | BLOCKING lifecycle (snapshot line 34) | YES — both captured |
| FR-6.2-T02 references FR-1.7 | FR-1.7 (post-phase wiring hook) | YES — universe has `related_reqs: ["FR-1.7"]` |
| FR-4.1 manifest (lines 279-325) vs. full manifest (lines 530-586) | Each other | **HIGH** — The universe FR-4.1 only references lines 277-325. The authoritative manifest at lines 530-586 has 4 additional entries (see Check 4). The universe should note both locations. |
| Phase 2 depends on Phase 1A | FR-7.3 audit trail fixture | YES — captured in SEQ-2 |
| Phase 3 depends on Phase 1B | FR-4.2 AST analyzer | YES — captured in SEQ-3 |

---

## Summary of Findings

### CRITICAL (Must Fix Before Implementation)

| # | Finding | Check | Recommendation |
|---|---------|-------|----------------|
| C1 | `handle_regression` in wiring manifest (line 583-585) has NO corresponding FR, test, or universe entry | 4 | Add FR for `handle_regression` reachability. Add to requirement universe. Assign to D4 (reachability) domain agent. |
| C2 | `SHADOW_GRACE_INFINITE` constant (models.py:293) — verified wiring point with no test | 7 | Add FR-1.19 or equivalent. The constant's value and usage in shadow grace period logic should be validated. |
| C3 | `__post_init__()` derivation (models.py:338-384) — verified wiring point with no test | 7 | Add FR-1.20 or equivalent. This method derives critical config fields; incorrect derivation would silently break sprint behavior. |

### HIGH (Should Fix Before Implementation)

| # | Finding | Check | Recommendation |
|---|---------|-------|----------------|
| H1 | FR-7.1 defines 9-field JSONL schema but FR-7.3 `record()` has only 7 params — `assertion_type` not in method signature | 1 | Spec inconsistency. Roadmap implementer must resolve: auto-derive or add param. |
| H2 | FR-5.1-TEST describes "empty directory" test but FR-5.1 guard only fires on non-empty directories | 1 | Clarify test: must use a non-empty directory where analysis returns 0 files (e.g., filter mismatch). |
| H3 | `_parse_phase_tasks()` return type contract (models.py, snapshot line 29) — no test | 7 | Add test or document as covered by FR-1.5 indirectly. |
| H4 | `can_run_wiring_gate()` (models.py:595-630) — no dedicated test | 7 | Add test or confirm covered by FR-3.2b (budget exhaustion before wiring). |
| H5 | `check_wiring_report()` wrapper (wiring_gate.py:1079) — no test | 7 | Add FR-1.x entry or confirm covered through FR-1.7/FR-2.3 indirectly. |
| H6 | `run_post_task_wiring_hook` in manifest has no dedicated FR-1.x E2E test | 4 | FR-1.7 covers the *phase* hook, not the *task* hook. Add FR-1.x for task-level wiring hook or confirm FR-2.2 covers it. |
| H7 | FR-4.1 manifest (lines 279-325) vs. full manifest (lines 530-586) — 4 extra entries in full manifest not referenced by universe | 4, 11 | Update universe FR-4.1 to reference both manifest locations. |
| H8 | Parallel test execution and JSONL write contention not addressed | 3 | Document sequential execution assumption or add file locking to audit writer. |

### LOW (Cosmetic / Implementation Details)

| # | Finding | Check | Recommendation |
|---|---------|-------|----------------|
| L1 | 4 filename mismatches between spec test layout and roadmap | 5 | Reconcile before implementation. |
| L2 | NFR-1 has no automated enforcement (only manual grep in Phase 4) | 9 | Consider conftest.py hook. |
| L3 | NFR-2 has no automated enforcement | 10 | Convention-based is acceptable. |
| L4 | `results_dir` configuration for audit fixture not specified | 3 | Implementation detail — fixture can use `tmp_path` or config. |

---

## Coverage Statistics

| Category | Total REQs | Covered by Universe | Gap Count |
|----------|-----------|-------------------|-----------|
| Spec shall/must/will | 7 | 7 | 0 |
| Code State Snapshot items | 29 | 24 | 5 (C2, C3, H3, H4, H5) |
| Wiring manifest entries | 13 | 12 | 1 (C1: handle_regression) |
| Workstreams | 7 | 7 | 0 |
| Success criteria | 12 | 12 | 0 |
| Cross-references | 6 | 5 | 1 (H7: dual manifest) |

**Universe extraction quality**: 89/89 extracted REQs are accurate. 3 CRITICAL and 8 HIGH gaps found, all traceable to items the spec defines but doesn't assign FRs to (Code State Snapshot items without test requirements, and a manifest entry without a spec FR).
