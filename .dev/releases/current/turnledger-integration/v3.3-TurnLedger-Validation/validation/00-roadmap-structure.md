# v3.3 Roadmap Structure

Parsed from: `roadmap-final.md`
Parse date: 2026-03-23

---

## Sections (Top-Level)

| # | Section | Line Range | Type |
|---|---------|-----------|------|
| 1 | Executive Summary | 9-33 | Overview |
| 2 | Phase 1: Foundation — Audit Trail + Reachability Analyzer | 38-65 | Phase |
| 3 | Phase 2: Core E2E Test Suites (FR-1, FR-2, FR-3, FR-6) | 68-134 | Phase |
| 4 | Phase 3: Pipeline Fixes + Reachability Gate Integration (FR-4.3, FR-5) | 137-161 | Phase |
| 5 | Phase 4: Regression Validation + Final Audit (NFR-3, SC-4) | 164-179 | Phase |
| 6 | Risk Assessment and Mitigation | 183-194 | Risk |
| 7 | Resource Requirements and Dependencies | 197-241 | Resources |
| 8 | Success Criteria Validation Matrix | 244-260 | Validation |
| 9 | Timeline Summary | 263-276 | Timeline |
| 10 | Open Questions (Architect Recommendations) | 279-290 | Decisions |
| 11 | Appendix A: Integration Point Registry | 294-367 | Reference |

---

## Tasks

### Phase 1A: Audit Trail Infrastructure (FR-7)

| Task ID | Description | Requirement | Deliverable | Line Range |
|---------|-------------|-------------|-------------|-----------|
| 1A.1 | JSONL audit record writer | FR-7.1 | `tests/audit-trail/audit_writer.py` with 9-field schema | 47 |
| 1A.2 | `audit_trail` pytest fixture | FR-7.3 | Session-scoped fixture, opens JSONL, provides record() method, auto-flushes | 48 |
| 1A.3 | Summary report generation | FR-7.3 | Total/passed/failed/wiring coverage at session end | 49 |
| 1A.4 | Verification test | FR-7.2 | Confirm JSONL meets 4 third-party verifiability properties | 50 |

### Phase 1B: AST Reachability Analyzer (FR-4)

| Task ID | Description | Requirement | Deliverable | Line Range |
|---------|-------------|-------------|-------------|-----------|
| 1B.1 | Wiring manifest YAML schema | FR-4.1 | entry_points + required_reachable sections | 58 |
| 1B.2 | AST call-chain analyzer module | FR-4.2 | `src/superclaude/cli/audit/reachability.py` | 59 |
| 1B.3 | Documented limitations | FR-4.2 (NFR-6) | Module docstring with dynamic dispatch, TYPE_CHECKING, lazy import notes | 60 |
| 1B.4 | Initial wiring manifest YAML | FR-4.1 | `tests/v3.3/wiring_manifest.yaml` | 61 |
| 1B.5 | Unit tests for AST analyzer | FR-4.4 | `tests/v3.3/test_reachability_eval.py` | 62 |

### Phase 2A: Wiring Point E2E Tests (FR-1)

| Task ID | Description | Requirements | Test Count | Line Range |
|---------|-------------|-------------|-----------|-----------|
| 2A.1 | Construction validation | FR-1.1–FR-1.4 | 4 | 80 |
| 2A.2 | Phase delegation | FR-1.5–FR-1.6 | 2 | 81 |
| 2A.3 | Post-phase wiring hook | FR-1.7 | 2 | 82 |
| 2A.4 | Anti-instinct hook return type | FR-1.8 | 1 | 83 |
| 2A.5 | Gate result accumulation | FR-1.9–FR-1.10 | 2 | 84 |
| 2A.6 | KPI report generation | FR-1.11 | 1 | 85 |
| 2A.7 | Wiring mode resolution | FR-1.12 | 1 | 86 |
| 2A.8 | Shadow findings → remediation log | FR-1.13 | 1 | 87 |
| 2A.9 | BLOCKING remediation lifecycle | FR-1.14, FR-1.14a–c | 3 | 88 |
| 2A.10 | Convergence registry args | FR-1.15–FR-1.16 | 2 | 89 |
| 2A.11 | Dict→Finding conversion | FR-1.17 | 1 | 90 |
| 2A.12 | Budget constants | FR-1.18 | 1 | 91 |

**Subtotal**: ~21 tests covering SC-1

### Phase 2B: TurnLedger Lifecycle Tests (FR-2)

| Task ID | Description | Requirement | Line Range |
|---------|-------------|-------------|-----------|
| 2B.1 | Convergence path (v3.05) | FR-2.1 | 101 |
| 2B.2 | Sprint per-task path (v3.1) | FR-2.2 | 102 |
| 2B.3 | Sprint per-phase path (v3.2) | FR-2.3 | 103 |
| 2B.4 | Cross-path coherence | FR-2.4 | 104 |

**Subtotal**: 4 tests covering SC-2

### Phase 2C: Gate Rollout Mode Matrix (FR-3)

| Task ID | Description | Requirement | Test Count | Line Range |
|---------|-------------|-------------|-----------|-----------|
| 2C.1 | 4 modes × 2 paths | FR-3.1a–FR-3.1d | 8 | 114 |
| 2C.2 | Budget exhaustion scenarios | FR-3.2a–FR-3.2d | 4 | 115 |
| 2C.3 | Interrupted sprint | FR-3.3 | 1 | 116 |

**Subtotal**: 13 tests covering SC-3, SC-6

### Phase 2D: Remaining QA Gaps (FR-6)

| Task ID | Description | Requirement | File | Line Range |
|---------|-------------|-------------|------|-----------|
| 2D.1 | v3.05 T07 convergence wiring | FR-6.1 T07 | test_convergence_wiring.py | 124 |
| 2D.2 | v3.05 T11 SC-1–SC-6 tests | FR-6.1 T11 | test_convergence_e2e.py | 125 |
| 2D.3 | Smoke test convergence | FR-6.1 T12 | test_convergence_e2e.py | 126 |
| 2D.4 | Wiring-verification artifact | FR-6.1 T14 | docs/generated/ | 127 |
| 2D.5 | run_post_phase_wiring_hook test | FR-6.2 T02 | test_wiring_points_e2e.py | 128 |
| 2D.6 | Integration + regression suite | FR-6.2 T17–T22 | test_integration_regression.py | 129 |

**Subtotal**: ~15 tests covering SC-8

### Phase 3A: Production Code Changes

| Task ID | Description | Requirement | File Modified | Line Range |
|---------|-------------|-------------|---------------|-----------|
| 3A.1 | 0-files-analyzed guard | FR-5.1 | wiring_gate.py | 148 |
| 3A.2 | Fidelity checker module | FR-5.2 | New: fidelity_checker.py | 149 |
| 3A.3 | Wire fidelity_checker | FR-5.2 | executor.py → _run_checkers() | 150 |
| 3A.4 | Reachability gate interface | FR-4.3 | reachability.py | 151 |

### Phase 3B: Validation Tests for Pipeline Fixes

| Task ID | Description | Requirement | Line Range |
|---------|-------------|-------------|-----------|
| 3B.1 | 0-files-analyzed → FAIL test | FR-5.1, SC-10 | 156 |
| 3B.2 | Reachability regression test | FR-4.4, SC-7, SC-9 | 157 |
| 3B.3 | Fidelity checker gap test | FR-5.2, SC-11 | 158 |

### Phase 4: Regression + Final Audit

| Task ID | Description | Requirement | Line Range |
|---------|-------------|-------------|-----------|
| 4.1 | Full test suite run | NFR-3, SC-4 | 172 |
| 4.2 | Grep-audit: no mock.patch | NFR-1 | 173 |
| 4.3 | JSONL audit trail review | FR-7.2, SC-12 | 174 |
| 4.4 | Wiring manifest completeness | NFR-5 | 175 |
| 4.5 | Wiring-verification artifact | FR-6.1 T14 | 176 |
| 4.6 | Update solutions_learned.jsonl | — | 177 |

---

## Gates / Validation Checkpoints

| Gate | Phase | Pass Criteria | Line Range |
|------|-------|---------------|-----------|
| Checkpoint A | 1 | Audit trail produces valid JSONL. AST analyzer resolves cross-module imports. Manifest committed. | 64 |
| Checkpoint B | 2 | All E2E tests pass. SC-1–6, SC-8, SC-12 validated. Audit trail emitted for every test. | 133 |
| Checkpoint C | 3 | 3 production fixes shipped. Reachability gate catches broken wiring. Fidelity checker detects missing impls. SC-7, SC-9–11 validated. | 160 |
| Checkpoint D (Release Gate) | 4 | Zero regressions. Audit trail complete. All 12 SC green. Evidence reviewable without tribal knowledge. | 179 |

---

## Integration Points (from Appendix A)

| ID | Type | Components | Phase |
|----|------|-----------|-------|
| A.1 | Dependency injection | `_subprocess_factory` | 1, 2 |
| A.2 | Execution dispatch | Executor phase delegation branch (task-inventory vs freeform) | 2, 3 |
| A.3 | Callback wiring | `run_post_phase_wiring_hook()` | 2, 3 |
| A.4 | Callback wiring | `run_post_task_anti_instinct_hook()` | 2 |
| A.5 | Strategy resolution | `_resolve_wiring_mode()` | 2, 4 |
| A.6 | Checker registry | `_run_checkers()` | 3 |
| A.7 | Findings merge | `registry.merge_findings()` | 2, 3 |
| A.8 | Integration boundary | Convergence registry constructor (3-arg) | 2, 3, 4 |
| A.9 | Logging mechanism | `DeferredRemediationLog` accumulator | 2 |

---

## Risk Mitigations (from roadmap)

| ID | Risk | Severity | Mitigation | Phase |
|----|------|----------|-----------|-------|
| R-1 | AST false negatives on dynamic dispatch | HIGH | Function-scope import extraction first; regression test; allowlist; document limitations per NFR-6 | 1B, 3 |
| R-2 | E2E flakiness from subprocess timing | MEDIUM | All tests use _subprocess_factory; no real subprocess in E2E; capture durations | 2 |
| R-3 | Impl-vs-spec checker false positives | MEDIUM | Exact function-name/class-name matching; fail-open; synthetic tests | 3 |
| R-4 | Audit trail JSONL unbounded | LOW | One file per test run; timestamped; no cross-run accumulation | 1A |
| R-5 | 0-files fix breaks existing tests | LOW | Investigate pre-existing failures first; additive change only | 3 |

---

## Test Assignments by Section

| Roadmap Section | Test File(s) | Test Count |
|-----------------|-------------|-----------|
| Phase 2A | tests/v3.3/test_wiring_points_e2e.py | ~21 |
| Phase 2B | tests/v3.3/test_turnledger_lifecycle.py | 4 |
| Phase 2C | tests/v3.3/test_gate_rollout_modes.py | 13 |
| Phase 2D | tests/roadmap/test_convergence_wiring.py, test_convergence_e2e.py, tests/v3.3/test_integration_regression.py | ~15 |
| Phase 3B | tests/v3.3/test_reachability_eval.py, test_wiring_points_e2e.py, test_pipeline_fixes.py | 3+ |
| Phase 1A | tests/audit-trail/test_audit_writer.py | 1+ |
| Phase 1B | tests/v3.3/test_reachability_eval.py | 1+ |
| **TOTAL** | | **~58+** |
