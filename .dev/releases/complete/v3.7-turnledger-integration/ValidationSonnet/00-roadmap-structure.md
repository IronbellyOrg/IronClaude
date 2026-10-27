# Roadmap Structure
**Roadmap**: v3.3-TurnLedger-Validation/roadmap.md
**Extraction date**: 2026-03-23

---

## Top-Level Organization

| Phase | Title | Duration | Blocked By | Key Goal |
|-------|-------|----------|------------|----------|
| Phase 1 | Foundation — Audit Trail + Reachability Analyzer | ~3 days (2–4) | — | Build cross-cutting infrastructure |
| Phase 2 | Core E2E Test Suites (FR-1, FR-2, FR-3, FR-6) | ~5 days (3–7) | Phase 1A | Write all E2E tests |
| Phase 3 | Pipeline Fixes + Reachability Gate Integration (FR-4.3, FR-5) | ~2 days (2–4) | Phase 1B + Phase 2 | Ship 3 production changes |
| Phase 4 | Regression Validation + Final Audit (NFR-3, SC-4) | ~1 day (1–2) | All phases | Zero-regression sweep + audit |

---

## Phase 1: Foundation

### 1A: Audit Trail Infrastructure (FR-7)

| Task ID | Requirement | Deliverable |
|---------|-------------|-------------|
| 1A.1 | FR-7.1 | JSONL audit record writer — `tests/audit-trail/audit_writer.py` with 9-field schema |
| 1A.2 | FR-7.3 | `audit_trail` pytest fixture — session-scoped, record() method, auto-flush |
| 1A.3 | FR-7.3 | Summary report at session end: total/passed/failed/wiring coverage |
| 1A.4 | FR-7.2 | Verification test: JSONL meets 4 third-party verifiability properties |

**Integration point**: `audit_trail` fixture registers in `tests/v3.3/conftest.py` and `tests/roadmap/conftest.py`.

### 1B: AST Reachability Analyzer (FR-4)

| Task ID | Requirement | Deliverable |
|---------|-------------|-------------|
| 1B.1 | FR-4.1 | Wiring manifest YAML schema — `entry_points` + `required_reachable` sections |
| 1B.2 | FR-4.2 | AST analyzer module — `src/superclaude/cli/audit/reachability.py` |
| 1B.3 | FR-4.2 | Documented limitations in module docstring |
| 1B.4 | FR-4.1 | Initial wiring manifest YAML — `tests/v3.3/wiring_manifest.yaml` |
| 1B.5 | FR-4.4 | Unit tests for AST analyzer — `tests/v3.3/test_reachability_eval.py` |

**Validation Checkpoint A**: Audit trail fixture produces valid JSONL; AST analyzer resolves cross-module imports; manifest schema committed.

---

## Phase 2: Core E2E Test Suites

### 2A: Wiring Point E2E Tests (FR-1)

**File**: `tests/v3.3/test_wiring_points_e2e.py`

| Task ID | Requirements Covered | Test Count | Description |
|---------|---------------------|------------|-------------|
| 2A.1 | FR-1.1–FR-1.4 | 4 | Construction validation: TurnLedger, ShadowGateMetrics, DeferredRemediationLog, SprintGatePolicy |
| 2A.2 | FR-1.5–FR-1.6 | 2 | Phase delegation: task-inventory vs freeform fallback |
| 2A.3 | FR-1.7 | 2 | Post-phase wiring hook fires on both paths |
| 2A.4 | FR-1.8 | 1 | Anti-instinct hook return type |
| 2A.5 | FR-1.9–FR-1.10 | 2 | Gate result accumulation; failed gate → remediation log |
| 2A.6 | FR-1.11 | 1 | KPI report generation with wiring KPI fields |
| 2A.7 | FR-1.12 | 1 | Wiring mode resolution via _resolve_wiring_mode() |
| 2A.8 | FR-1.13 | 1 | Shadow findings → remediation log with [shadow] prefix |
| 2A.9 | FR-1.14, FR-1.14a–c | 3 | BLOCKING remediation lifecycle |
| 2A.10 | FR-1.15–FR-1.16 | 2 | Convergence registry 3-arg construction; merge_findings() 3-arg call |
| 2A.11 | FR-1.17 | 1 | _run_remediation() dict-to-Finding conversion |
| 2A.12 | FR-1.18 | 1 | TurnLedger budget constant = 61 |

**Subtotal**: ~21 tests covering SC-1.

**NOTE**: FR-1.19 (SHADOW_GRACE_INFINITE), FR-1.20 (post_init derivation), FR-1.21 (check_wiring_report wrapper) do NOT appear in the 2A task table.

### 2B: TurnLedger Lifecycle Tests (FR-2)

**File**: `tests/v3.3/test_turnledger_lifecycle.py`

| Task ID | Requirement | Description |
|---------|-------------|-------------|
| 2B.1 | FR-2.1 | Convergence path E2E — debit/credit/reimburse cycle |
| 2B.2 | FR-2.2 | Sprint per-task path |
| 2B.3 | FR-2.3 | Sprint per-phase path |
| 2B.4 | FR-2.4 | Cross-path coherence |

**Subtotal**: 4 tests covering SC-2.

**NOTE**: FR-2.1a (handle_regression() reachability) does NOT appear in 2B task table.

### 2C: Gate Rollout Mode Matrix (FR-3)

**File**: `tests/v3.3/test_gate_rollout_modes.py`

| Task ID | Requirement | Test Count |
|---------|-------------|------------|
| 2C.1 | FR-3.1a–FR-3.1d | 8 tests (4 modes × 2 paths) |
| 2C.2 | FR-3.2a–FR-3.2d | 4 tests (budget exhaustion) |
| 2C.3 | FR-3.3 | 1 test (interrupted sprint) |

**Subtotal**: 13 tests covering SC-3, SC-6.

### 2D: Remaining QA Gaps (FR-6)

| Task ID | Requirement | File | Test Count |
|---------|-------------|------|------------|
| 2D.1 | FR-6.1 T07 | `tests/roadmap/test_convergence_wiring.py` | 7 tests |
| 2D.2 | FR-6.1 T11 | `tests/roadmap/test_convergence_e2e.py` | 6 tests (SC-1–SC-6) |
| 2D.3 | FR-6.1 T12 | `tests/roadmap/test_convergence_e2e.py` | 1 smoke test |
| 2D.4 | FR-6.1 T14 | `docs/generated/` | Wiring-verification artifact |
| 2D.5 | FR-6.2 T02 | `tests/v3.3/test_wiring_points_e2e.py` | Confirming test |
| 2D.6 | FR-6.2 T17–T22 | `tests/v3.3/test_integration_regression.py` | 6+ tests |

**Subtotal**: ~15 tests covering SC-8.

**Validation Checkpoint B**: All E2E tests pass; SC-1–6, SC-8, SC-12 validated.

---

## Phase 3: Pipeline Fixes

### 3A: Production Code Changes

| Task ID | Requirement | File Modified | Change |
|---------|-------------|---------------|--------|
| 3A.1 | FR-5.1 | `src/superclaude/cli/audit/wiring_gate.py` | 0-files guard |
| 3A.2 | FR-5.2 | New: `src/superclaude/cli/roadmap/fidelity_checker.py` | Impl-vs-spec checker |
| 3A.3 | FR-5.2 | `src/superclaude/cli/roadmap/executor.py` — `_run_checkers()` | Wire fidelity_checker |
| 3A.4 | FR-4.3 | `src/superclaude/cli/audit/reachability.py` | GateCriteria-compatible interface |

### 3B: Validation Tests for Pipeline Fixes

| Task ID | Requirement | Deliverable |
|---------|-------------|-------------|
| 3B.1 | FR-5.1, SC-10 | 0-files-analyzed → FAIL test |
| 3B.2 | FR-4.4, SC-7, SC-9 | Regression test: broken wiring detected |
| 3B.3 | FR-5.2, SC-11 | Fidelity checker synthetic gap test |

**Validation Checkpoint C**: All 3 production fixes shipped; SC-7, SC-9–11 validated.

---

## Phase 4: Regression Validation + Final Audit

| Task ID | Requirement | Deliverable |
|---------|-------------|-------------|
| 4.1 | NFR-3, SC-4 | Full test suite: ≥4894 passed, ≤3 pre-existing, 0 new regressions |
| 4.2 | NFR-1 | Grep-audit: no mock.patch on gate functions |
| 4.3 | FR-7.2, SC-12 | Manual review of JSONL audit trail |
| 4.4 | NFR-5 | Wiring manifest completeness: every wiring point from FR-1 has manifest entry |
| 4.5 | FR-6.1 T14 | Final wiring-verification artifact |
| 4.6 | — | Update docs/memory/solutions_learned.jsonl |

**Validation Checkpoint D (Release Gate)**: Zero regressions; all 12 SC green; audit trail complete.

---

## Gates & Quality Checkpoints

| Gate | Phase | Pass Criteria | Stop Condition |
|------|-------|---------------|----------------|
| Checkpoint A | 1 | Audit trail JSONL valid; AST analyzer resolves cross-module imports; manifest populated | Audit trail fails to produce valid JSONL |
| Checkpoint B | 2 | All E2E tests pass; SC-1–6, SC-8, SC-12 green; audit trail emitted per test | Any SC fails to validate |
| Checkpoint C | 3 | All 3 production fixes shipped; SC-7, SC-9–11 validated | Reachability gate misses broken wiring; fidelity checker has false-positive rate > acceptable threshold |
| Checkpoint D | 4 | Zero regressions; all 12 SC green; evidence package complete | Any SC fails; regressions introduced |

---

## Roadmap Spec References Index

| Roadmap Section | Spec Requirements Covered |
|-----------------|--------------------------|
| 1A (Audit Trail) | FR-7.1, FR-7.2, FR-7.3, SC-12 |
| 1B (AST Analyzer) | FR-4.1, FR-4.2, FR-4.4, NFR-5, NFR-6 |
| 2A (Wiring E2E) | FR-1.1–FR-1.18, SC-1, SC-5 |
| 2B (Lifecycle) | FR-2.1, FR-2.2, FR-2.3, FR-2.4, SC-2 |
| 2C (Gate Modes) | FR-3.1a–d, FR-3.2a–d, FR-3.3, SC-3, SC-6 |
| 2D (QA Gaps) | FR-6.1 T07/T11/T12/T14, FR-6.2 T02/T17-T22, SC-8 |
| 3A/3B (Pipeline) | FR-4.3, FR-5.1, FR-5.2, SC-7, SC-9, SC-10, SC-11 |
| Phase 4 | NFR-1, NFR-3, NFR-5, FR-7.2, SC-4, SC-12 |

---

## New Files Declared

| File | Phase | Purpose |
|------|-------|---------|
| `src/superclaude/cli/audit/reachability.py` | 1B | AST-based reachability analyzer |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | 3 | Impl-vs-spec checker |
| `tests/v3.3/conftest.py` | 1A | Audit trail fixture |
| `tests/v3.3/test_reachability_eval.py` | 1B | Reachability analyzer tests |
| `tests/v3.3/test_wiring_points_e2e.py` | 2A | FR-1 wiring E2E tests |
| `tests/v3.3/test_turnledger_lifecycle.py` | 2B | FR-2 lifecycle tests |
| `tests/v3.3/test_gate_rollout_modes.py` | 2C | FR-3 mode matrix tests |
| `tests/v3.3/test_integration_regression.py` | 2D | FR-6.2 gap closure tests |
| `tests/v3.3/wiring_manifest.yaml` | 1B | Reachability manifest |
| `tests/audit-trail/test_audit_writer.py` | 1A | Audit infrastructure tests |

## Files Modified

| File | Phase | Change |
|------|-------|--------|
| `src/superclaude/cli/audit/wiring_gate.py` | 3 | FR-5.1: 0-files-analyzed assertion |
| `src/superclaude/cli/roadmap/executor.py` | 3 | FR-5.2: wire fidelity_checker |
| `tests/roadmap/test_convergence_wiring.py` | 2D | FR-6.1 T07 |
| `tests/roadmap/test_convergence_e2e.py` | 2D | FR-6.1 T11/T12 |
