# Decomposition Plan: v3.3 TurnLedger Validation

**Generated**: 2026-03-23
**Total Agents**: 12
**Domain Agents**: 8
**Cross-Cutting Agents**: 4

---

## Domain Agent Assignments

### AGENT-D1: E2E Wiring Tests Domain

**Domain**: E2E Wiring Tests (FR-1)
**Requirements**: 21 (REQ-001 through REQ-020, plus REQ-007a)
**Output**: `01-agent-D1-e2e-wiring-tests.md`

**Assigned Requirements**:
- REQ-001: TurnLedger Construction Validation
- REQ-002: ShadowGateMetrics Construction
- REQ-003: DeferredRemediationLog Construction
- REQ-004: SprintGatePolicy Construction
- REQ-005: Phase Delegation — Task Inventory Path
- REQ-006: Phase Delegation — Freeform Fallback Path
- REQ-007: Post-Phase Wiring Hook — Both Paths [CROSS-CUTTING]
- REQ-007a: check_wiring_report() Wrapper Call
- REQ-008: Anti-Instinct Hook Return Type
- REQ-009: Gate Result Accumulation
- REQ-010: Failed Gate → Remediation Log
- REQ-011: KPI Report Generation [CROSS-CUTTING]
- REQ-012: Wiring Mode Resolution
- REQ-013: Shadow Findings → Remediation Log
- REQ-014: BLOCKING Remediation Lifecycle [CROSS-CUTTING]
- REQ-015: Convergence Registry Args
- REQ-016: Convergence Merge Args
- REQ-017: Convergence Remediation Dict→Finding
- REQ-018: Budget Constants
- REQ-019: SHADOW_GRACE_INFINITE Constant
- REQ-020: Post-Init Config Derivation

**Cross-Cutting Requirements to Check**: REQ-007, REQ-011, REQ-014

---

### AGENT-D2: TurnLedger Lifecycle Domain

**Domain**: TurnLedger Lifecycle (FR-2)
**Requirements**: 5 (REQ-021 through REQ-024, REQ-021a)
**Output**: `01-agent-D2-turnledger-lifecycle.md`

**Assigned Requirements**:
- REQ-021: Convergence Path (v3.05) [CROSS-CUTTING]
- REQ-021a: Regression Handler Reachability
- REQ-022: Sprint Per-Task Path (v3.1) [CROSS-CUTTING]
- REQ-023: Sprint Per-Phase Path (v3.2) [CROSS-CUTTING]
- REQ-024: Cross-Path Coherence [CROSS-CUTTING]

**Cross-Cutting Requirements to Check**: REQ-021, REQ-022, REQ-023, REQ-024

---

### AGENT-D3: Gate Modes & Budget Domain

**Domain**: Gate Modes & Budget (FR-3)
**Requirements**: 10 (REQ-025 through REQ-034)
**Output**: `01-agent-D3-gate-modes-budget.md`

**Assigned Requirements**:
- REQ-025: Mode Matrix - off
- REQ-026: Mode Matrix - shadow
- REQ-027: Mode Matrix - soft
- REQ-028: Mode Matrix - full
- REQ-029: Each mode verification (Acceptance Criteria)
- REQ-030: Budget Exhaustion - before task launch
- REQ-031: Budget Exhaustion - before wiring analysis
- REQ-032: Budget Exhaustion - before remediation
- REQ-033: Budget Exhaustion - mid-convergence
- REQ-034: Interrupted Sprint

**Cross-Cutting Requirements to Check**: None

---

### AGENT-D4: Reachability Framework Domain

**Domain**: Reachability Framework (FR-4)
**Requirements**: 4 (REQ-035 through REQ-038)
**Output**: `01-agent-D4-reachability-framework.md`

**Assigned Requirements**:
- REQ-035: Spec-Driven Wiring Manifest [CROSS-CUTTING]
- REQ-036: AST Call-Chain Analyzer [CROSS-CUTTING]
- REQ-037: Reachability Gate Integration [CROSS-CUTTING]
- REQ-038: Regression Test

**Cross-Cutting Requirements to Check**: REQ-035, REQ-036, REQ-037

---

### AGENT-D5: Pipeline Fixes Domain

**Domain**: Pipeline Fixes (FR-5)
**Requirements**: 3 (REQ-039 through REQ-041)
**Output**: `01-agent-D5-pipeline-fixes.md`

**Assigned Requirements**:
- REQ-039: 0-Files-Analyzed Assertion
- REQ-040: Impl-vs-Spec Fidelity Check [CROSS-CUTTING]
- REQ-041: Reachability Gate (cross-reference) [CROSS-CUTTING]

**Cross-Cutting Requirements to Check**: REQ-040, REQ-041

---

### AGENT-D6: QA Gap Closure Domain

**Domain**: QA Gap Closure (FR-6)
**Requirements**: 6 (REQ-042 through REQ-047)
**Output**: `01-agent-D6-qa-gap-closure.md`

**Assigned Requirements**:
- REQ-042: v3.05 Gap T07 — 7 convergence wiring tests
- REQ-043: v3.05 Gap T11 — 6 E2E tests
- REQ-044: v3.05 Gap T12 — smoke test
- REQ-045: v3.05 Gap T14 — regenerate artifact
- REQ-046: v3.2 Gap T02 — confirming test
- REQ-047: v3.2 Gap T17-T22 — integration tests

**Cross-Cutting Requirements to Check**: None

---

### AGENT-D7: Audit Trail Infrastructure Domain

**Domain**: Audit Trail Infrastructure (FR-7)
**Requirements**: 3 (REQ-048 through REQ-050)
**Output**: `01-agent-D7-audit-trail-infra.md`

**Assigned Requirements**:
- REQ-048: Test Output Format (JSONL schema) [CROSS-CUTTING]
- REQ-049: Audit Trail Properties (verifiability) [CROSS-CUTTING]
- REQ-050: Audit Trail Runner (pytest fixture) [CROSS-CUTTING]

**Cross-Cutting Requirements to Check**: REQ-048, REQ-049, REQ-050

---

### AGENT-D8: Success Criteria Domain

**Domain**: Success Criteria (SC-*)
**Requirements**: 12 (REQ-SC-001 through REQ-SC-012)
**Output**: `01-agent-D8-success-criteria.md`

**Assigned Requirements**:
- REQ-SC-001: SC-1 — ≥20 wiring point E2E tests
- REQ-SC-002: SC-2 — TurnLedger lifecycle 4 paths
- REQ-SC-003: SC-3 — Gate rollout modes 8+ scenarios
- REQ-SC-004: SC-4 — Zero regressions baseline
- REQ-SC-005: SC-5 — KPI report accuracy
- REQ-SC-006: SC-6 — Budget exhaustion 4 scenarios
- REQ-SC-007: SC-7 — Eval catches known-bad
- REQ-SC-008: SC-8 — QA gaps closed
- REQ-SC-009: SC-9 — Reachability gate works
- REQ-SC-010: SC-10 — 0-files → FAIL
- REQ-SC-011: SC-11 — Fidelity check exists
- REQ-SC-012: SC-12 — Audit trail verifiable

**Cross-Cutting Requirements to Check**: All SC items verify cross-domain concerns

---

## Cross-Cutting Agent Assignments

### AGENT-CC1: Internal Consistency (Roadmap)

**Scope**: Full roadmap
**Purpose**: ID schema consistency, count consistency, table-to-prose consistency, cross-reference validity
**Output**: `01-agent-CC1-roadmap-consistency.md`

**Checks**:
1. Frontmatter spec_source matches actual spec file
2. Phase task counts match claimed totals
3. Test counts in tables match prose descriptions
4. All file paths referenced are consistent
5. No duplicate task IDs
6. All FR-* references in roadmap exist in spec

---

### AGENT-CC2: Internal Consistency (Spec)

**Scope**: Full spec
**Purpose**: Section cross-references valid, requirement counts match, no contradictory statements
**Output**: `01-agent-CC2-spec-consistency.md`

**Checks**:
1. All spec references (e.g., "executor.py:1127") are consistent
2. FR-1 through FR-7 are complete and non-overlapping
3. SC-1 through SC-12 all trace to at least one FR
4. No contradictory requirements
5. Wiring manifest YAML is valid and complete
6. Phased implementation plan matches FR assignments

---

### AGENT-CC3: Dependency & Ordering

**Scope**: Roadmap + spec
**Purpose**: Spec dependency chains respected in roadmap ordering
**Output**: `01-agent-CC3-dependency-ordering.md`

**Checks**:
1. Phase 1 completes before Phase 2 (audit trail dependency)
2. Phase 1B completes before Phase 3 (AST analyzer dependency)
3. Phase 2 completes before Phase 3 (baseline establishment)
4. All phases complete before Phase 4 (final validation)
5. No circular dependencies in task ordering
6. Infrastructure before features ordering respected

---

### AGENT-CC4: Completeness Sweep

**Scope**: Everything
**Purpose**: Re-scan for requirements missed by extraction, verify complete coverage
**Output**: `01-agent-CC4-completeness-sweep.md`

**Checks**:
1. Re-scan spec for requirements missed in Phase 0
2. Verify every REQ has at least one agent's coverage claim
3. Check for implicit systems required by explicit ones
4. Verify Success Criteria all have validation methods
5. Check for orphaned requirements (no roadmap coverage)
6. Verify integration points have both sides addressed

---

## Cross-Cutting Concern Matrix

| Requirement | Primary Agent | Secondary Agents | Integration Risk |
|-------------|--------------|------------------|------------------|
| REQ-007 | D1 | D3, D7 | HIGH |
| REQ-011 | D1 | D2, D7 | MEDIUM |
| REQ-014 | D1 | D2, D3 | HIGH |
| REQ-021 | D2 | D1, D7 | MEDIUM |
| REQ-022 | D2 | D1, D3, D7 | HIGH |
| REQ-023 | D2 | D1, D3, D7 | HIGH |
| REQ-024 | D2 | D1, D3, D7 | HIGH |
| REQ-035 | D4 | ALL | HIGH |
| REQ-036 | D4 | ALL | HIGH |
| REQ-037 | D4 | ALL | HIGH |
| REQ-040 | D5 | D4, D7 | MEDIUM |
| REQ-041 | D5 | D4 | MEDIUM |
| REQ-048 | D7 | ALL | HIGH |
| REQ-049 | D7 | ALL | HIGH |
| REQ-050 | D7 | ALL | HIGH |

---

## Agent Spawn Order

All 12 agents will be dispatched in parallel:

1. AGENT-D1: E2E Wiring Tests
2. AGENT-D2: TurnLedger Lifecycle
3. AGENT-D3: Gate Modes & Budget
4. AGENT-D4: Reachability Framework
5. AGENT-D5: Pipeline Fixes
6. AGENT-D6: QA Gap Closure
7. AGENT-D7: Audit Trail Infrastructure
8. AGENT-D8: Success Criteria
9. AGENT-CC1: Roadmap Consistency
10. AGENT-CC2: Spec Consistency
11. AGENT-CC3: Dependency Ordering
12. AGENT-CC4: Completeness Sweep
