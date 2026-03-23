# Agent D7: QA Gap Closure — Coverage Validation Report

**Domain**: QA Gap Closure (FR-6.x series + SC-8 + FILE-MOD-3/4)
**Spec**: v3.3-requirements-spec.md
**Roadmap**: roadmap-final.md
**Date**: 2026-03-23
**Agent**: D7
**Assigned Requirements**: 9 primary + 3 cross-cutting

---

## Coverage Assessments

### FR-6.1-T07: v3.05 Gap T07 — tests/roadmap/test_convergence_wiring.py — 7 tests

**Spec Text** (lines 394-396):
> | T07 | `tests/roadmap/test_convergence_wiring.py` — 7 tests | Write tests |

**Roadmap Coverage**:

Phase 2D, Task 2D.1 (line 124):
> | 2D.1 | FR-6.1 T07 | `tests/roadmap/test_convergence_wiring.py` | Extend existing 7 tests (verify already present, add any missing) |

**Existing Code State**: File `tests/roadmap/test_convergence_wiring.py` already exists with 7 test classes:
1. `TestRegistryConstruction` (test 1: registry construction 3-arg call)
2. `TestMergeFindingsStructuralOnly` (test 2: structural merge)
3. `TestMergeFindingsSemanticOnly` (test 3: semantic merge)
4. `TestRemediationDictAccess` (test 4: dict-to-Finding key access)
5. `TestTurnledgerBudgetParams` (test 5: budget constants)
6. `TestEndToEndConvergencePass` (test 6: convergence pass path)
7. `TestEndToEndConvergenceFail` (test 7: convergence fail path)

**Verdict**: COVERED. The roadmap explicitly references FR-6.1 T07 as task 2D.1. The action is "Extend existing 7 tests (verify already present, add any missing)." The 7 tests already exist in the codebase; the roadmap correctly characterizes the work as verification and extension rather than net-new authoring. The roadmap also places this in Phase 2D with a hard dependency on Phase 1A (audit trail), consistent with the spec's requirement that all tests emit JSONL records.

**Risk**: LOW. Tests exist. Roadmap task is to verify and extend if needed.

---

### FR-6.1-T11: v3.05 Gap T11 — tests/roadmap/test_convergence_e2e.py — 6 tests for SC-1 through SC-6

**Spec Text** (lines 394-398):
> | T11 | `tests/roadmap/test_convergence_e2e.py` — 6 tests for SC-1 through SC-6 | Write tests |

**Roadmap Coverage**:

Phase 2D, Task 2D.2 (line 125):
> | 2D.2 | FR-6.1 T11 | `tests/roadmap/test_convergence_e2e.py` | Extend existing SC-1–SC-6 tests |

**Existing Code State**: File `tests/roadmap/test_convergence_e2e.py` already exists with 6 tests in class `TestConvergenceE2E`:
1. `test_sc1_registry_persistence` — SC-1: Registry persistence round-trip
2. `test_sc2_monotonic_progress` — SC-2: Monotonic structural progress
3. `test_sc3_budget_exhaustion` — SC-3: Budget exhaustion halts
4. `test_sc4_regression_handling` — SC-4: Regression handling
5. `test_sc5_convergence_pass` — SC-5: Convergence pass with credit
6. `test_sc6_semantic_fluctuation` — SC-6: Semantic fluctuation warns but does not halt

**Verdict**: COVERED. The roadmap explicitly references FR-6.1 T11 as task 2D.2. All 6 SC-scenario tests exist in the codebase. The roadmap correctly characterizes the action as "Extend existing SC-1–SC-6 tests." Test names map 1:1 to the SC-1 through SC-6 scenarios required by the spec.

**Risk**: LOW. All 6 tests exist and exercise `execute_fidelity_with_convergence()` with controlled checker/remediation callables.

---

### FR-6.1-T12: v3.05 Gap T12 — Smoke test convergence path

**Spec Text** (lines 394-398):
> | T12 | Smoke test convergence path | Write test |

**Roadmap Coverage**:

Phase 2D, Task 2D.3 (line 126):
> | 2D.3 | FR-6.1 T12 | `tests/roadmap/test_convergence_e2e.py` | Add smoke test for convergence path |

**Existing Code State**: File `tests/roadmap/test_convergence_smoke.py` already exists with class `TestConvergenceSmoke` containing 3 smoke tests:
1. `test_smoke_no_runtime_exceptions` — verifies `_run_convergence_spec_fidelity()` completes without TypeError/AttributeError
2. `test_smoke_returns_valid_step_result` — verifies StepResult has PASS status when 0 HIGHs
3. `test_smoke_output_file_written` — verifies output file written to output_dir

**Verdict**: COVERED WITH DISCREPANCY. The roadmap task 2D.3 places the smoke test in `test_convergence_e2e.py`, but the actual smoke tests already exist in a separate file `test_convergence_smoke.py`. This is a minor location discrepancy — the tests exist and cover the requirement. The roadmap should reference the correct file location, or the implementation should move the tests to match the roadmap.

**Risk**: LOW. Functionality is covered. File location is a minor inconsistency.

---

### FR-6.1-T14: v3.05 Gap T14 — Regenerate wiring-verification artifact + validate

**Spec Text** (lines 394-399):
> | T14 | Regenerate wiring-verification artifact | Generate + validate |

**Roadmap Coverage**:

Phase 2D, Task 2D.4 (line 127):
> | 2D.4 | FR-6.1 T14 | `docs/generated/` | Regenerate wiring-verification artifact + validate |

Phase 4, Task 4.5 (line 176):
> | 4.5 | — | Generate final wiring-verification artifact (FR-6.1 T14) |

**Existing Code State**: File `.dev/releases/complete/v3.05_DeterministicFidelityGates/wiring-verification.md` exists with a wiring verification artifact showing 166 files analyzed, 7 major findings (all orphan modules in cli_portify/steps), 0 critical findings, 0 blocking findings.

**Verdict**: COVERED. The roadmap addresses T14 in two locations: task 2D.4 for the initial regeneration and task 4.5 in Phase 4 for the final artifact. The existing wiring-verification artifact provides a baseline. The dual-phase coverage (Phase 2 generation + Phase 4 final validation) is appropriate since the Phase 3 production changes could alter the wiring landscape.

**Risk**: LOW. The regeneration is a pipeline invocation, not new code. The existing artifact provides the expected format.

---

### FR-6.2-T02: v3.2 Gap T02 — run_post_phase_wiring_hook() confirming test

**Spec Text** (lines 405-407):
> | T02 | `run_post_phase_wiring_hook()` call | Already verified WIRED — write confirming test |

**Roadmap Coverage**:

Phase 2D, Task 2D.5 (line 128):
> | 2D.5 | FR-6.2 T02 | `tests/v3.3/test_wiring_points_e2e.py` | Confirming test for `run_post_phase_wiring_hook()` (may overlap 2A.3) |

Phase 2A, Task 2A.3 (line 82):
> | 2A.3 | FR-1.7 | 2 tests: Post-phase wiring hook fires on per-task and per-phase/ClaudeProcess paths |

Roadmap Appendix A.3 (lines 314-320):
> ### A.3: `run_post_phase_wiring_hook()`
> - **Owning Phase**: Phase 2 proves both call sites (FR-1.7); Phase 3 uses FR-4.4 to detect broken reachability
> - **Cross-Reference**: FR-1.7, FR-3.1a–d, FR-4.4, audit expectations, KPI accuracy (FR-1.11)

**Existing Code State**: File `tests/sprint/test_wiring_integration.py` already contains class `TestPostPhaseHookCalledPerPhase` with test `test_post_phase_hook_called_per_phase` that verifies `run_post_phase_wiring_hook` is called once per phase (2 phases = 2 calls, with correct phase numbers verified).

**Verdict**: COVERED. The roadmap addresses FR-6.2-T02 via task 2D.5 and explicitly notes the overlap with task 2A.3 (FR-1.7). The existing test in `test_wiring_integration.py` already confirms the hook is called per-phase. The roadmap's plan to place the confirming test in `test_wiring_points_e2e.py` is valid since the spec asks for a confirming test in the v3.3 test suite alongside the FR-1.7 E2E tests.

**Cross-Cutting Note**: This requirement overlaps with FR-1.7 (assigned to Agent D1). Agent D1 covers the two-path validation (per-task and per-phase/ClaudeProcess). FR-6.2-T02 is the confirming test that the hook is wired at all. The roadmap correctly identifies this overlap: "may overlap 2A.3."

**Risk**: LOW. The hook is already tested. The roadmap plans both a confirming test and the broader FR-1.7 coverage.

---

### FR-6.2-T17-T22: v3.2 Gaps T17-T22 — Integration tests, regression suite, gap closure audit

**Spec Text** (lines 405-408):
> | T17-T22 | Integration tests, regression suite, gap closure audit | Write tests per this spec |

**Roadmap Coverage**:

Phase 2D, Task 2D.6 (line 129):
> | 2D.6 | FR-6.2 T17–T22 | `tests/v3.3/test_integration_regression.py` | Integration + regression suite per spec |

New Files table (line 223):
> | `tests/v3.3/test_integration_regression.py` | 2D | FR-6.2 gap closure tests |

Phase 2D subtotal (line 131):
> **Subtotal**: ~15 tests covering SC-8.

**Existing Code State**: No file `tests/v3.3/test_integration_regression.py` exists yet (it is listed as a new file in the roadmap). However, several related test files already exist:
- `tests/sprint/test_wiring_integration.py` (integration tests for TurnLedger threading)
- `tests/integration/test_sprint_wiring.py` (sprint wiring integration tests)
- `tests/sprint/test_backward_compat_regression.py` (backward compatibility regression)

**Verdict**: COVERED. The roadmap creates a dedicated file `tests/v3.3/test_integration_regression.py` for T17-T22 gap closure. The spec describes these as "Integration tests, regression suite, gap closure audit" — the roadmap correctly plans a new file in Phase 2D with integration and regression tests that close these gaps. The ~15 test count for all of Phase 2D (including T07/T11/T12/T14/T02/T17-T22) is reasonable.

**Risk**: MEDIUM. Unlike T07/T11/T12 which have existing tests, T17-T22 requires net-new test authoring. The roadmap provides the file location and phase but does not decompose T17-T22 into individual test descriptions. The spec itself is also vague — "Integration tests, regression suite, gap closure audit" — which could lead to scope ambiguity during implementation.

---

### SC-8: Remaining QA gaps closed — v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22

**Spec Text** (line 520):
> | SC-8 | Remaining QA gaps closed | v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22 | 2 |

**Roadmap Coverage**:

Success Criteria Validation Matrix (line 255):
> | SC-8 | All QA gap tests passing | FR-6.1 + FR-6.2 tests green | 2 | Yes |

Validation Checkpoint B (line 133):
> **Validation Checkpoint B**: All E2E tests pass. SC-1 through SC-6, SC-8, SC-12 validated. Audit trail JSONL emitted for every test. All runtime-path assertions evidence-backed. QA gaps materially closed.

**Verdict**: COVERED. The roadmap maps SC-8 to Phase 2 and validates it at Checkpoint B. The success criterion is defined as "FR-6.1 + FR-6.2 tests green" which directly traces to tasks 2D.1-2D.6. The automated validation method ("Yes") means this is checked programmatically by test pass/fail. Every component gap (T07, T11, T12, T14, T02, T17-T22) has a corresponding roadmap task.

**Risk**: LOW. SC-8 is a composite criterion that passes if and only if all FR-6.x tasks pass. Coverage of the individual tasks implies coverage of SC-8.

---

### FILE-MOD-3: Modified: tests/roadmap/test_convergence_wiring.py — T07 extend/verify

**Spec reference**: Test File Layout (lines 603):
> `tests/roadmap/test_convergence_wiring.py` — FR-6.1 T07 (7 tests)

**Roadmap Coverage**:

Files Modified table (line 233):
> | `tests/roadmap/test_convergence_wiring.py` | 2D | FR-6.1 T07: extend/verify tests |

Phase 2D, Task 2D.1 (line 124):
> | 2D.1 | FR-6.1 T07 | `tests/roadmap/test_convergence_wiring.py` | Extend existing 7 tests (verify already present, add any missing) |

**Verdict**: COVERED. The roadmap explicitly lists this file in the "Files Modified" table and assigns it to Phase 2D with the correct requirement reference (FR-6.1 T07). The action "extend/verify tests" matches the spec's intent.

**Risk**: LOW.

---

### FILE-MOD-4: Modified: tests/roadmap/test_convergence_e2e.py — T11/T12 extend

**Spec reference**: Test File Layout (lines 604):
> `tests/roadmap/test_convergence_e2e.py` — FR-6.1 T11 (6 tests)

**Roadmap Coverage**:

Files Modified table (line 234):
> | `tests/roadmap/test_convergence_e2e.py` | 2D | FR-6.1 T11/T12: extend tests |

Phase 2D, Tasks 2D.2 and 2D.3 (lines 125-126):
> | 2D.2 | FR-6.1 T11 | `tests/roadmap/test_convergence_e2e.py` | Extend existing SC-1–SC-6 tests |
> | 2D.3 | FR-6.1 T12 | `tests/roadmap/test_convergence_e2e.py` | Add smoke test for convergence path |

**Verdict**: COVERED WITH DISCREPANCY. The roadmap correctly lists this file in "Files Modified" for T11/T12 extension. However, as noted under FR-6.1-T12, the existing smoke test is in `test_convergence_smoke.py`, not `test_convergence_e2e.py`. The roadmap's plan to add a smoke test to `test_convergence_e2e.py` (task 2D.3) may create duplication with the existing smoke test file unless the existing smoke test is migrated or the new test covers different scope.

**Risk**: LOW. The file modification is planned. The location discrepancy for T12 is a minor implementation detail.

---

## Cross-Cutting Requirements

### FR-1.7 (Overlap with FR-6.2-T02)

**Context**: FR-1.7 requires testing `run_post_phase_wiring_hook()` on both per-task and per-phase/ClaudeProcess paths. FR-6.2-T02 requires a confirming test that the hook is wired at all.

**Roadmap Coverage**: The roadmap explicitly identifies this overlap at task 2D.5:
> "Confirming test for `run_post_phase_wiring_hook()` (may overlap 2A.3)"

Task 2A.3 (FR-1.7, assigned to Agent D1) provides the deeper two-path validation. Task 2D.5 (FR-6.2-T02, this domain) provides the confirming test. The existing test in `test_wiring_integration.py::TestPostPhaseHookCalledPerPhase` already covers the basic confirmation.

**Verdict**: COVERED. No gap between domains. The overlap is acknowledged and both tasks are planned.

### NFR-1: No mocking of gate functions or core orchestration logic

**Roadmap Coverage**:

Phase 4, Task 4.2 (line 173):
> | 4.2 | NFR-1 | Grep-audit: confirm no `mock.patch` on gate functions or orchestration logic across all v3.3 test files |

Architectural Priority 1 (line 15):
> 1. **Protect production-path realism** — satisfy NFR-1 by testing real orchestration and gate behavior end-to-end, limiting injection to `_subprocess_factory` only.

**Assessment of Existing QA Gap Tests**: The existing `test_convergence_wiring.py` tests do NOT mock gate functions — they call `execute_fidelity_with_convergence()` directly with controlled `run_checkers` and `run_remediation` callables, which is the accepted injection pattern. The `test_convergence_e2e.py` tests also follow this pattern. The `test_convergence_smoke.py` tests DO use `mock.patch` on `structural_checkers.run_all_checkers`, `semantic_layer.run_semantic_layer`, and `remediate_executor.execute_remediation` — these mock external checkers (analogous to `_subprocess_factory` replacing the external claude binary), not core orchestration logic.

**Verdict**: COVERED. The roadmap includes an explicit Phase 4 grep-audit. Existing QA gap tests follow acceptable injection patterns.

### NFR-4: Every test must emit a JSONL audit record

**Roadmap Coverage**:

Phase 1A establishes the `audit_trail` fixture. Phase 2 hard-depends on Phase 1A (line 72):
> **Hard dependency**: Phase 1A (audit trail fixture must exist).

Validation Checkpoint B (line 133):
> Audit trail JSONL emitted for every test.

**Assessment**: The existing QA gap tests (`test_convergence_wiring.py`, `test_convergence_e2e.py`, `test_convergence_smoke.py`) do NOT currently emit JSONL audit records. The roadmap's plan to extend these files (tasks 2D.1-2D.3) should add audit trail emission. However, the roadmap does not explicitly state that the extension includes adding audit trail calls to existing tests — the "extend" action is ambiguous between "add new tests" and "retrofit audit trail to existing tests."

**Verdict**: PARTIALLY COVERED. The audit trail infrastructure is planned (Phase 1A) and Checkpoint B validates emission. However, the roadmap does not explicitly state that retrofitting audit trail calls into existing `tests/roadmap/` files is part of the 2D.1-2D.3 work. This is an implementation risk — the existing 7+6+3 tests may not emit JSONL records unless explicitly retrofitted.

---

## Summary

| Requirement | Verdict | Risk |
|---|---|---|
| FR-6.1-T07 | COVERED | LOW |
| FR-6.1-T11 | COVERED | LOW |
| FR-6.1-T12 | COVERED (minor location discrepancy) | LOW |
| FR-6.1-T14 | COVERED (dual-phase: 2D + Phase 4) | LOW |
| FR-6.2-T02 | COVERED (overlap with FR-1.7 acknowledged) | LOW |
| FR-6.2-T17-T22 | COVERED (net-new file planned) | MEDIUM |
| SC-8 | COVERED (composite of FR-6.x) | LOW |
| FILE-MOD-3 | COVERED | LOW |
| FILE-MOD-4 | COVERED (minor location discrepancy for T12) | LOW |
| **Cross-cutting: FR-1.7** | COVERED (overlap acknowledged) | LOW |
| **Cross-cutting: NFR-1** | COVERED (Phase 4 grep-audit) | LOW |
| **Cross-cutting: NFR-4** | PARTIALLY COVERED | MEDIUM |

**Overall Domain Verdict**: 11/12 requirements FULLY COVERED, 1/12 PARTIALLY COVERED.

### Gaps Requiring Attention

1. **NFR-4 Retrofit Gap**: The roadmap does not explicitly state that the Phase 2D "extend" tasks (2D.1-2D.3) include adding `audit_trail.record()` calls to the existing tests in `tests/roadmap/test_convergence_wiring.py` and `tests/roadmap/test_convergence_e2e.py`. Without this, the existing ~16 tests may not emit JSONL audit records, violating NFR-4's "every test must emit" constraint.

2. **FR-6.1-T12 Location Discrepancy**: The smoke test exists in `test_convergence_smoke.py` but the roadmap targets `test_convergence_e2e.py`. Minor — either consolidate or reference the correct file.

3. **FR-6.2-T17-T22 Decomposition**: The roadmap provides a file and phase but does not decompose T17-T22 into individual test descriptions. The spec's description ("Integration tests, regression suite, gap closure audit") is broad. Implementation may benefit from more granular task breakdown.
