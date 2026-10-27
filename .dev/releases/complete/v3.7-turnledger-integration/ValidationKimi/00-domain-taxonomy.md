# Domain Taxonomy: v3.3 TurnLedger Validation

**Generated**: 2026-03-23
**Total Domains**: 8
**Total Requirements**: 54

---

## Domain Overview

| Domain ID | Name | Requirements | Description |
|-----------|------|--------------|-------------|
| D1 | E2E Wiring Tests | 21 | FR-1: Wiring point construction, delegation, hooks, lifecycle tests |
| D2 | TurnLedger Lifecycle | 5 | FR-2: Convergence, per-task, per-phase, cross-path coherence |
| D3 | Gate Modes & Budget | 10 | FR-3: Rollout modes, budget exhaustion, interruption handling |
| D4 | Reachability Framework | 4 | FR-4: AST analyzer, wiring manifest, gate integration |
| D5 | Pipeline Fixes | 3 | FR-5: 0-files assertion, fidelity checker, reachability gate |
| D6 | QA Gap Closure | 6 | FR-6: v3.05 and v3.2 remaining test gaps |
| D7 | Audit Trail Infra | 3 | FR-7: JSONL format, properties, runner fixture |
| D8 | Success Criteria | 12 | SC-1 through SC-12: Release validation criteria |

---

## Domain D1: E2E Wiring Tests (FR-1)

**Primary Focus**: Construction validation, phase delegation, wiring hooks, remediation lifecycle

### Requirements Assigned

| ID | Requirement | Cross-Cutting |
|----|-------------|---------------|
| REQ-001 | TurnLedger Construction Validation | No |
| REQ-002 | ShadowGateMetrics Construction | No |
| REQ-003 | DeferredRemediationLog Construction | No |
| REQ-004 | SprintGatePolicy Construction | No |
| REQ-005 | Phase Delegation — Task Inventory Path | No |
| REQ-006 | Phase Delegation — Freeform Fallback Path | No |
| REQ-007 | Post-Phase Wiring Hook — Both Paths | **Yes** |
| REQ-007a | check_wiring_report() Wrapper Call | No |
| REQ-008 | Anti-Instinct Hook Return Type | No |
| REQ-009 | Gate Result Accumulation | No |
| REQ-010 | Failed Gate → Remediation Log | No |
| REQ-011 | KPI Report Generation | **Yes** |
| REQ-012 | Wiring Mode Resolution | No |
| REQ-013 | Shadow Findings → Remediation Log | No |
| REQ-014 | BLOCKING Remediation Lifecycle | **Yes** |
| REQ-015 | Convergence Registry Args | No |
| REQ-016 | Convergence Merge Args | No |
| REQ-017 | Convergence Remediation Dict→Finding | No |
| REQ-018 | Budget Constants | No |
| REQ-019 | SHADOW_GRACE_INFINITE Constant | No |
| REQ-020 | Post-Init Config Derivation | No |

**Cross-Cutting Touch Points**: D2 (TurnLedger), D3 (Gate modes), D7 (Audit trail)

---

## Domain D2: TurnLedger Lifecycle (FR-2)

**Primary Focus**: Debit/credit/reimbursement cycle across all 4 execution paths

### Requirements Assigned

| ID | Requirement | Cross-Cutting |
|----|-------------|---------------|
| REQ-021 | Convergence Path (v3.05) | **Yes** |
| REQ-021a | Regression Handler Reachability | No |
| REQ-022 | Sprint Per-Task Path (v3.1) | **Yes** |
| REQ-023 | Sprint Per-Phase Path (v3.2) | **Yes** |
| REQ-024 | Cross-Path Coherence | **Yes** |

**Cross-Cutting Touch Points**: D1 (Wiring tests), D3 (Budget exhaustion), D7 (Audit trail)

---

## Domain D3: Gate Modes & Budget (FR-3)

**Primary Focus**: Gate rollout mode matrix and budget exhaustion scenarios

### Requirements Assigned

| ID | Requirement | Cross-Cutting |
|----|-------------|---------------|
| REQ-025 | Mode Matrix - off | No |
| REQ-026 | Mode Matrix - shadow | No |
| REQ-027 | Mode Matrix - soft | No |
| REQ-028 | Mode Matrix - full | No |
| REQ-029 | Each mode verification (AC) | No |
| REQ-030 | Budget Exhaustion - before task launch | No |
| REQ-031 | Budget Exhaustion - before wiring analysis | No |
| REQ-032 | Budget Exhaustion - before remediation | No |
| REQ-033 | Budget Exhaustion - mid-convergence | No |
| REQ-034 | Interrupted Sprint | No |

**Cross-Cutting Touch Points**: D1 (Wiring hooks), D2 (TurnLedger budget), D7 (Audit trail)

---

## Domain D4: Reachability Framework (FR-4)

**Primary Focus**: AST-based reachability analysis and gate integration

### Requirements Assigned

| ID | Requirement | Cross-Cutting |
|----|-------------|---------------|
| REQ-035 | Spec-Driven Wiring Manifest | **Yes** |
| REQ-036 | AST Call-Chain Analyzer | **Yes** |
| REQ-037 | Reachability Gate Integration | **Yes** |
| REQ-038 | Regression Test | No |

**Cross-Cutting Touch Points**: ALL domains (reachability validates wiring across all components)

---

## Domain D5: Pipeline Fixes (FR-5)

**Primary Focus**: Production code fixes for pipeline weaknesses

### Requirements Assigned

| ID | Requirement | Cross-Cutting |
|----|-------------|---------------|
| REQ-039 | 0-Files-Analyzed Assertion | No |
| REQ-040 | Impl-vs-Spec Fidelity Check | **Yes** |
| REQ-041 | Reachability Gate (cross-reference) | **Yes** |

**Cross-Cutting Touch Points**: D4 (Reachability), D6 (QA gaps), D7 (Audit trail for verification)

---

## Domain D6: QA Gap Closure (FR-6)

**Primary Focus**: Closing outstanding v3.05 and v3.2 test gaps

### Requirements Assigned

| ID | Requirement | Cross-Cutting |
|----|-------------|---------------|
| REQ-042 | v3.05 Gap T07 — 7 convergence wiring tests | No |
| REQ-043 | v3.05 Gap T11 — 6 E2E tests | No |
| REQ-044 | v3.05 Gap T12 — smoke test | No |
| REQ-045 | v3.05 Gap T14 — regenerate artifact | No |
| REQ-046 | v3.2 Gap T02 — confirming test | No |
| REQ-047 | v3.2 Gap T17-T22 — integration tests | No |

**Cross-Cutting Touch Points**: D1 (Wiring tests), D2 (Lifecycle tests), D7 (Audit trail)

---

## Domain D7: Audit Trail Infrastructure (FR-7)

**Primary Focus**: Structured test output for third-party verification

### Requirements Assigned

| ID | Requirement | Cross-Cutting |
|----|-------------|---------------|
| REQ-048 | Test Output Format (JSONL schema) | **Yes** |
| REQ-049 | Audit Trail Properties (verifiability) | **Yes** |
| REQ-050 | Audit Trail Runner (pytest fixture) | **Yes** |

**Cross-Cutting Touch Points**: ALL domains (audit trail is consumed by all test phases)

---

## Domain D8: Success Criteria (SC-*)

**Primary Focus**: Release validation and acceptance criteria

### Requirements Assigned

| ID | Requirement | Cross-Cutting |
|----|-------------|---------------|
| REQ-SC-001 | SC-1: ≥20 wiring point E2E tests | No |
| REQ-SC-002 | SC-2: TurnLedger lifecycle 4 paths | No |
| REQ-SC-003 | SC-3: Gate rollout modes 8+ scenarios | No |
| REQ-SC-004 | SC-4: Zero regressions baseline | No |
| REQ-SC-005 | SC-5: KPI report accuracy | No |
| REQ-SC-006 | SC-6: Budget exhaustion 4 scenarios | No |
| REQ-SC-007 | SC-7: Eval catches known-bad | No |
| REQ-SC-008 | SC-8: QA gaps closed | No |
| REQ-SC-009 | SC-9: Reachability gate works | No |
| REQ-SC-010 | SC-10: 0-files → FAIL | No |
| REQ-SC-011 | SC-11: Fidelity check exists | No |
| REQ-SC-012 | SC-12: Audit trail verifiable | No |

**Cross-Cutting Touch Points**: ALL domains (success criteria validate all domains)

---

## Cross-Cutting Concern Matrix

| Requirement | Primary | Secondary | Integration Risk |
|-------------|---------|-----------|------------------|
| REQ-007 (Wiring Hook) | D1 | D3, D7 | HIGH |
| REQ-011 (KPI Report) | D1 | D2, D7 | MEDIUM |
| REQ-014 (Remediation) | D1 | D2, D3 | HIGH |
| REQ-021 (Convergence) | D2 | D1, D7 | MEDIUM |
| REQ-022 (Per-Task) | D2 | D1, D3, D7 | HIGH |
| REQ-023 (Per-Phase) | D2 | D1, D3, D7 | HIGH |
| REQ-024 (Cross-Path) | D2 | D1, D3, D7 | HIGH |
| REQ-035 (Manifest) | D4 | ALL | HIGH |
| REQ-036 (AST Analyzer) | D4 | ALL | HIGH |
| REQ-037 (Gate Integration) | D4 | ALL | HIGH |
| REQ-040 (Fidelity Check) | D5 | D4, D7 | MEDIUM |
| REQ-048 (JSONL Format) | D7 | ALL | HIGH |
| REQ-049 (Verifiability) | D7 | ALL | HIGH |
| REQ-050 (Runner) | D7 | ALL | HIGH |

---

## Domain Size Distribution

| Domain | Count | Percentage |
|--------|-------|------------|
| D1 E2E Wiring | 21 | 39% |
| D8 Success Criteria | 12 | 22% |
| D3 Gate Modes | 10 | 19% |
| D6 QA Gaps | 6 | 11% |
| D2 TurnLedger | 5 | 9% |
| D4 Reachability | 4 | 7% |
| D5 Pipeline Fixes | 3 | 6% |
| D7 Audit Trail | 3 | 6% |
| **Total** | **54** | **100%** |

---

## Agent Assignment Summary

Based on the taxonomy, the following agents will be spawned:

| Agent | Domain | Requirements | Type |
|-------|--------|--------------|------|
| D1 | E2E Wiring Tests | 21 | Domain |
| D2 | TurnLedger Lifecycle | 5 | Domain |
| D3 | Gate Modes & Budget | 10 | Domain |
| D4 | Reachability Framework | 4 | Domain |
| D5 | Pipeline Fixes | 3 | Domain |
| D6 | QA Gap Closure | 6 | Domain |
| D7 | Audit Trail Infra | 3 | Domain |
| D8 | Success Criteria | 12 | Domain |
| CC1 | Internal Consistency (Roadmap) | - | Cross-Cutting |
| CC2 | Internal Consistency (Spec) | - | Cross-Cutting |
| CC3 | Dependency & Ordering | - | Cross-Cutting |
| CC4 | Completeness Sweep | - | Cross-Cutting |

**Total Agents**: 12 (8 domain + 4 cross-cutting)
