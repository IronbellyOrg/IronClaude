---
spec_source: wiring-verification-gate-v1.0-release-spec.md
complexity_score: 0.78
adversarial: true
---

# Wiring Verification Gate v1.0 — Final Merged Roadmap

## Executive Summary

This release adds a **static-analysis wiring verification gate** to the SuperClaude audit pipeline, detecting three classes of wiring defects — unwired injectable callables, orphan provider modules, and broken dispatch registries — and integrating them into the sprint execution loop via a phased shadow→soft→blocking enforcement model.

The 0.78 complexity score (HIGH) reflects the multi-system integration surface: the gate touches audit analysis, sprint budget tracking (TurnLedger), KPI reporting, and trailing-gate remediation, while being constrained to zero modifications of existing pipeline infrastructure (`pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py`).

**Architectural decisions**:
- New code lives in `src/superclaude/cli/audit/` (wiring_gate.py, wiring_config.py); modifications to 4 existing files
- Callable-based remediation interface avoids coupling trailing_gate.py to TurnLedger
- Debit-before-analysis budget model with floor-to-zero credit arithmetic
- 3-phase rollout: shadow (log-only) → soft (warn) → blocking (fail + remediate)

**Scope**: 23 requirements (15 functional, 8 non-functional), 15 success criteria, 8 risks to mitigate. Estimated total: ~800-1085 LOC across new code, modifications, and tests.

**Delivery posture**: Ship analysis + shadow-mode integration as the v1.0 target. Promote to soft/blocking only after rollout validation thresholds are met via evidence-driven criteria.

**Implementer assumption**: This roadmap is optimized for a single implementer working on ~800-1100 LOC. The 4-phase core structure (plus rollout validation) maps to natural engineering milestones without artificial coordination overhead.

---

## Phase 1: Core Analysis Engine (Data Models + Analyzers)

**Goal**: Implement the three analysis functions and their supporting data models as self-contained, testable units with zero integration dependencies.

### Milestone 1.1 — Data Models

| Item | Requirement | Deliverable | LOC Est. |
|------|------------|-------------|----------|
| T01 — WiringFinding dataclass | FR: T01 | `audit/wiring_gate.py` (partial) | 30-40 |
| T01 — WiringReport dataclass | FR: T01 | `audit/wiring_gate.py` (partial) | 40-50 |
| T01 — WiringConfig dataclass | FR: T01 | `audit/wiring_config.py` | 40-60 |
| Whitelist schema + loader | FR: Goal-1c, Goal-1d, NFR-008 | `audit/wiring_config.py` | 30-40 |

**Acceptance gates**: WiringFinding.to_dict() round-trips; WiringReport computed properties correct; whitelist loads valid YAML; malformed entries skipped with WARNING (Phase 1 behavior per Goal-1d, NFR-008).

### Milestone 1.2 — Analysis Functions

| Item | Requirement | Deliverable |
|------|------------|-------------|
| `analyze_unwired_callables()` | FR: Goal-1a, Goal-1b | `audit/wiring_gate.py` |
| `analyze_orphan_modules()` | FR: Goal-2a, Goal-2b, Goal-2c, Goal-2d | `audit/wiring_gate.py` |
| `analyze_unwired_registries()` | FR: Goal-3a, Goal-3b | `audit/wiring_gate.py` |

**Key constraints**:
- AST-only analysis using Python `ast` module (Architectural Constraint 1)
- No dynamic dispatch resolution — `**kwargs`, `getattr`, `importlib` excluded (Constraint 2)
- Graceful degradation on parse errors per NFR-002: log warning, skip file, continue. **Degraded analysis state must be treated as an observability event** — emit a structured warning with file path, parse reason, and files-skipped count, not a silent skip. The `analysis_complete` field reflects whether all files parsed successfully; a separate `files_skipped: N` frontmatter field provides visibility into degraded runs.
- Whitelist applied during `analyze_unwired_callables()` per Goal-1c

**Risk mitigation for R1 (false positives)**: Whitelist mechanism is a first-class citizen, not an afterthought. `whitelist_entries_applied` count is surfaced in report frontmatter (Goal-4a) so FPR can be tracked from day one.

**Risk mitigation for R2 (parse errors)**: Each `ast.parse()` call wrapped in try/except; file-level granularity ensures one bad file doesn't poison the entire analysis.

**Risk mitigation for R6 (provider_dir_names mismatch)**: Default `provider_dir_names` set conservatively (`steps/`, `handlers/`, `validators/`, `checks/`). Zero-findings on first run emits explicit warning (SC-011) to prevent silent misconfiguration.

### Milestone 1.3 — Report Emission and Gate Definition

| Item | Requirement | Deliverable |
|------|------------|-------------|
| `emit_report()` | FR: Goal-4a, Goal-4b, Goal-4c, Goal-4d, NFR-005 | `audit/wiring_gate.py` |
| `WIRING_GATE` constant | FR: T05 | `audit/wiring_gate.py` |
| 5 semantic check functions | FR: T05 | `audit/wiring_gate.py` |

**Critical**: All string frontmatter fields serialized via `yaml.safe_dump()` (Goal-4b, NFR-005). The 11 required frontmatter fields must exactly match the `GateCriteria` schema (Goal-4a). Semantic check signatures must follow `(content: str) -> bool` (Constraint 6).

### Milestone 1.4 — Phase 1 Unit Tests

| Item | Requirement | Deliverable | Test Count |
|------|------------|-------------|------------|
| Unwired callable tests | FR: T06 | `tests/audit/test_wiring_gate.py` | 4 |
| Orphan module tests | FR: T06 | `tests/audit/test_wiring_gate.py` | 5 |
| Unwired registry tests | FR: T06 | `tests/audit/test_wiring_gate.py` | 2 |
| Report + gate tests | FR: T06 | `tests/audit/test_wiring_gate.py` | 3 |
| Test fixtures | FR: T06 | `tests/audit/fixtures/` | — |

**Acceptance**: 14+ unit tests passing; all `finding_type` values asserted; ≥90% line coverage on `wiring_gate.py` (NFR-003); SC-001 through SC-005, SC-007 validated.

### Phase 1 Exit Criteria

- All three analyzer fixtures pass with correct finding types
- Parse degradation verified: bad file logged, skipped, analysis continues
- Whitelist behavior stable — suppression count reported
- Gate passes clean report; gate fails invalid report deterministically

---

## Phase 2: Sprint Integration (TurnLedger + Executor Hook)

**Goal**: Wire the analysis engine into the sprint execution loop with budget tracking and enforcement modes.

**Dependency**: Phase 1 complete (analysis functions + gate definition must exist).

### Phase 2 Entry Prerequisites

The following open questions **must be resolved before Phase 2 work begins** (promoted from inline blockers per debate resolution):

| Prerequisite | Open Question | Required Resolution |
|-------------|--------------|-------------------|
| **OQ-2** | `WIRING_ANALYSIS_TURNS` and `REMEDIATION_COST` values | Set conservative defaults (e.g., `WIRING_ANALYSIS_TURNS=1`, `REMEDIATION_COST=2`) with SprintConfig overrides. Document rationale. |
| **OQ-6** | SprintGatePolicy constructor compatibility | Read `trailing_gate.py` source; validate constructor requirements; document interface contract. |

These are explicit entry gates, not inline blockers discovered mid-implementation.

### Milestone 2.1 — TurnLedger Extensions

| Item | Requirement | Deliverable | LOC Est. |
|------|------------|-------------|----------|
| 3 new fields | FR: T07a | `sprint/models.py` MODIFY | 10-15 |
| `debit_wiring()` | FR: T07a | `sprint/models.py` MODIFY | 5 |
| `credit_wiring()` with floor | FR: T07a | `sprint/models.py` MODIFY | 5-8 |
| `can_run_wiring_gate()` | FR: T07a | `sprint/models.py` MODIFY | 3-5 |
| 3 SprintConfig fields | FR: T07a | `sprint/models.py` MODIFY | 10-15 |
| SprintConfig migration shim | NFR-007 | `sprint/models.py` MODIFY | 8-12 |

**Critical behavior**: `credit_wiring(1, 0.8)` MUST return 0 credits (`int(1 * 0.8)` = 0). This is by design (R7) and tests must explicitly assert it. All new fields default to zero (NFR-004).

**Risk mitigation for R7 (floor-to-zero)**: Explicitly documented, tested, and surfaced in KPI reporting so operators understand the economic model.

**Risk mitigation for R8 (config rename)**: `__post_init__` migration shim emits deprecation warning; shim scoped to 1 release then removed (NFR-007).

### Milestone 2.2 — Sprint Executor Hook

| Item | Requirement | Deliverable | LOC Est. |
|------|------------|-------------|----------|
| `run_post_task_wiring_hook()` | FR: T07b | `sprint/executor.py` MODIFY | 50-70 |
| BLOCKING mode path | FR: T07b-b (Goal-5c) | `sprint/executor.py` | — |
| SHADOW mode path | FR: T07b-c (Goal-5a) | `sprint/executor.py` | — |
| SOFT mode path | FR: T07b-d (Goal-5b) | `sprint/executor.py` | — |
| Null-ledger compat | FR: T07b-e, NFR-004 | `sprint/executor.py` | — |
| Helper functions | FR: T07b-f | `sprint/executor.py` | — |

**Architectural note**: Mode resolution via `resolve_gate_mode(scope, grace_period)` replaces string-switch `wiring_gate_mode` (Goal-5d). The callable-based remediation interface (`can_remediate`, `debit`) avoids importing TurnLedger into trailing_gate.py (Constraint 7).

**Critical constraint**: NFR-006 — zero modifications to `pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py`. The hook is a new consumer of these modules only.

### Milestone 2.3 — TurnLedger Unit Tests

| Item | Requirement | Test Count |
|------|------------|------------|
| `debit_wiring`/`credit_wiring` tracking | FR: T06 addendum | 3 |

**Acceptance**: SC-012, SC-013 validated.

### Phase 2 Exit Criteria

- Shadow, soft, and blocking branches are functionally distinct and testable
- `ledger is None` path matches prior behavior exactly
- Budget debit/credit semantics proven with explicit floor-to-zero assertions

---

## Phase 3: KPI and Deviation Reconciliation (P1 Extensions)

**Goal**: Extend reporting and add cross-gate reconciliation.

**Dependency**: Phase 2 complete (TurnLedger extensions must exist for KPI fields).

### Milestone 3.1 — KPI Report Extensions

| Item | Requirement | Deliverable | LOC Est. |
|------|------------|-------------|----------|
| 6 wiring KPI fields | FR: T07c | `sprint/kpi.py` MODIFY | 15-20 |
| `build_kpi_report()` signature update | FR: T07c | `sprint/kpi.py` MODIFY | — |

**Acceptance**: SC-015 validated.

### Milestone 3.2 — Deviation Count Reconciliation

| Item | Requirement | Deliverable | LOC Est. |
|------|------------|-------------|----------|
| `_deviation_counts_reconciled()` | FR: T08 | `roadmap/gates.py` MODIFY | 35-50 |

**Coordination strategy (Constraint 10)**: `roadmap/gates.py` is shared with Anti-Instincts and Unified Audit Gating changes. To mitigate merge conflicts:
1. Implement this milestone last within Phase 3
2. Sequence edits carefully — isolate the new function at file end to minimize diff overlap
3. Rebase onto latest master immediately before merge
4. Coordinate timing with any concurrent PRs touching this file

**Acceptance**: SC-008 validated.

### Phase 3 Exit Criteria

- KPI reporting includes all six wiring metrics
- Deviation count mismatch causes deterministic gate failure
- No merge conflicts or behavioral regressions in existing fidelity gate logic

---

## Phase 4: Integration Testing and Retrospective Validation

**Goal**: End-to-end validation of the full wiring gate pipeline including budget flows and real-codebase retrospective.

**Dependency**: Phases 1-3 complete.

### Milestone 4.1 — Integration Tests

| Item | Requirement | Deliverable | Test Count |
|------|------------|-------------|------------|
| cli-portify fixture | FR: T10 / SC-010 | `tests/audit/test_wiring_integration.py` | 1+ |
| Budget Scenario 5 (credit floor) | FR: T12, SC-012 | `tests/pipeline/test_full_flow.py` | 1 |
| Budget Scenario 6 (BLOCKING remediation) | FR: T12 | `tests/pipeline/test_full_flow.py` | 1 |
| Budget Scenario 7 (null-ledger compat) | FR: T12, SC-014 | `tests/pipeline/test_full_flow.py` | 1 |
| Budget Scenario 8 (shadow deferred log) | FR: T12 | `tests/pipeline/test_full_flow.py` | 1 |

**Non-negotiable**: The cli-portify fixture MUST produce exactly 1 `WiringFinding(unwired_callable)` (SC-010). This is the behavioral contract that validates the gate would have caught the original no-op bug.

### Milestone 4.2 — Retrospective Validation

| Item | Requirement | Deliverable |
|------|------------|-------------|
| Run against actual `cli_portify/` | FR: T11, SC-010 | Validation report |

**Acceptance**: Analysis detects the original `step_runner=None` no-op bug that motivated this entire release.

### Milestone 4.3 — Performance Validation

| Item | Requirement | Threshold |
|------|------------|-----------|
| Benchmark on 50-file package | NFR-001, SC-009 | p95 < 5s |

### Phase 4 Exit Criteria

- Full success-criteria review: SC-001 through SC-015 satisfied or explicitly dispositioned
- Coverage ≥ 90% on `wiring_gate.py` (NFR-003)
- Retrospective detection of the original no-op bug succeeds
- Performance benchmark within threshold
- NFR-006 verified: diff inspection proves protected files unchanged

---

## Phase 5: Rollout Validation

**Goal**: Validate the gate against real repositories before enabling enforcement. This phase addresses R6 (provider_dir_names mismatch) — the highest-severity risk — which can only be fully validated during real-world operation.

**Dependency**: Phase 4 complete (all code merged, tests passing).

**Nature**: Engineering validation milestones, not operational runbook. Each milestone produces measurable evidence that informs promotion decisions.

### Milestone 5.1 — Shadow Mode Baseline

1. Activate `Goal-5a` (shadow/log-only mode)
2. Collect and evaluate:
   - Findings volume per analysis run
   - Whitelist usage and coverage
   - Zero-findings anomalies (SC-011 warnings)
   - p95 runtime under real workloads
3. Validate `provider_dir_names` and registry patterns against real repository conventions
4. **Duration**: Minimum 2-release shadow period (mandated by spec)

### Milestone 5.2 — Soft Mode Readiness

1. Enable `Goal-5b` (warning surfacing)
2. Measure:
   - False-positive burden — is the whitelist adequate?
   - Remediation usefulness — are findings actionable?
3. **Promotion criteria**: FPR manageable through `wiring_whitelist.yaml`; no regression against legacy `ledger is None` paths

### Milestone 5.3 — Blocking Mode Authorization

Enable `Goal-5c` (fail + remediate) **only if all of the following are met**:
- SC-009 stable across shadow period
- SC-010 confirmed detection in real code (not just fixtures)
- Shadow data quality acceptable — no silent misconfiguration artifacts
- Whitelist and provider heuristics calibrated against actual conventions
- Budget constants and recursion protections verified in production path

**Key principle**: Enforcement mode selected by evidence, not by schedule.

---

## Risk Assessment and Mitigation Matrix

| Risk | Severity | Likelihood | Phase Affected | Mitigation Strategy | Residual Risk |
|------|----------|-----------|---------------|---------------------|---------------|
| **R1** — False positives from intentional `Optional[Callable]` hooks | Medium | High | Phase 1 | Whitelist with `reason` field; `whitelist_entries_applied` in frontmatter; shadow-mode calibration before enforcement | Low after whitelist tuning |
| **R2** — AST parse failures on complex patterns | Low | Medium | Phase 1 | Per-file try/except; structured observability event (not silent skip); `files_skipped` frontmatter field | Very low |
| **R3** — Insufficient shadow data | Medium | Low | Phase 5 | Minimum 2-release shadow period; record findings counts, whitelist usage, zero-result anomalies | Low |
| **R4** — Performance impact on sprint loop | Medium | Low | Phase 4 | AST-only (no subprocess); benchmark gate at < 5s p95 | Very low |
| **R5** — Registry pattern misses | Low | Medium | Phase 1 | Configurable `registry_patterns`; log zero-registry warning; validate in retrospective | Low |
| **R6** — Provider dir mismatch | **High** | **High** | Phase 1, 5 | Pre-activation checklist; zero-findings warning (SC-011); Phase 5 real-repository validation | Medium until Phase 5 baseline confirms |
| **R7** — Floor-to-zero credits | Medium | High | Phase 2 | By design; explicit test assertions; documented in KPI; surfaced clearly in output | None (accepted) |
| **R8** — Config field rename breakage | Low | Medium | Phase 2 | `__post_init__` migration shim + deprecation warning; remove after 1 release | Very low |

**Highest-severity risk**: R6 (provider_dir_names mismatch). This is the only risk that can cause **silent corruption of baseline data**. Defense layers: Phase 1 zero-findings warning (SC-011), Phase 4 retrospective validation (T11), and Phase 5 real-repository shadow-mode validation. The third layer — absent from the original base variant — is the critical addition from the debate.

---

## Resource Requirements and Dependencies

### External Dependencies (consumed, not modified)

- `pipeline/models.py` — GateCriteria, SemanticCheck (NFR-006: no modifications)
- `pipeline/gates.py` — gate_passed() (NFR-006: no modifications)
- `pipeline/trailing_gate.py` — resolve_gate_mode(), DeferredRemediationLog, etc. (NFR-006: no modifications)
- Python `ast`, `re`, `yaml` standard library modules

### Files Modified

| File | Phase | Est. LOC Delta | Coordination |
|------|-------|---------------|--------------|
| `audit/wiring_gate.py` | 1 | +200-280 (new) | None |
| `audit/wiring_config.py` | 1 | +80-120 (new) | None |
| `sprint/models.py` | 2 | +30-35 | None |
| `sprint/executor.py` | 2 | +50-70 | None |
| `sprint/kpi.py` | 3 | +15-20 | None |
| `roadmap/gates.py` | 3 | +35-50 | **Anti-Instincts / Unified Audit** — sequence edits carefully, rebase before merge |

### Test Files

| File | Phase | Est. LOC |
|------|-------|----------|
| `tests/audit/test_wiring_gate.py` | 1 | 200-250 |
| `tests/audit/fixtures/` | 1 | 50-80 |
| `tests/audit/test_wiring_integration.py` | 4 | 60-80 |
| `tests/pipeline/test_full_flow.py` | 4 | +80-100 |

### Total Estimated Scope

- **New code**: ~280-400 LOC (wiring_gate.py + wiring_config.py)
- **Modified code**: ~130-175 LOC across 4 files
- **Test code**: ~390-510 LOC across 4 files/directories
- **Total**: ~800-1085 LOC

---

## Success Criteria Validation Map

| SC ID | Description | Phase | Test Type | Gate |
|-------|------------|-------|-----------|------|
| SC-001 | Unwired callable detection | 1.4 | Unit | Milestone 1.4 |
| SC-002 | Orphan module detection | 1.4 | Unit | Milestone 1.4 |
| SC-003 | Unwired registry detection | 1.4 | Unit | Milestone 1.4 |
| SC-004 | Report frontmatter conformance | 1.4 | Unit | Milestone 1.4 |
| SC-005 | Gate evaluation compatibility | 4.1 | Integration | Milestone 4.1 |
| SC-006 | Shadow mode non-interference | 4.1 | Integration | Milestone 4.1 |
| SC-007 | Whitelist suppression + count | 1.4 | Unit | Milestone 1.4 |
| SC-008 | Deviation reconciliation | 3.2 | Unit | Milestone 3.2 |
| SC-009 | p95 < 5s performance | 4.3 | Benchmark | Milestone 4.3 |
| SC-010 | Detect cli-portify no-op bug | 4.1, 4.2 | Integration + Retrospective | Milestones 4.1, 4.2 |
| SC-011 | Zero-findings sanity warning | 4.1 | Integration | Milestone 4.1 |
| SC-012 | Debit/credit correctness | 2.3, 4.1 | Unit + Integration | Milestones 2.3, 4.1 |
| SC-013 | Reimbursement consumed | 4.1 | Integration | Milestone 4.1 |
| SC-014 | Null-ledger compatibility | 4.1 | Integration | Milestone 4.1 |
| SC-015 | KPI field population | 3.1 | Unit | Milestone 3.1 |

All 15 success criteria mapped. Every SC has at least one test-backed verification point.

---

## Open Questions — Resolved Recommendations

These 10 open questions from the specification extraction are resolved with architect recommendations. Items marked **PREREQUISITE** must be resolved before their gated phase begins.

| # | Question | Recommendation | Status |
|---|---------|---------------|--------|
| 1 | Import alias resolution for v1.0 | **Defer to v1.1**. Whitelist mitigates FPR adequately for shadow mode. ~30% Phase 1 scope increase with uncertain payoff. | Approved |
| 2 | `WIRING_ANALYSIS_TURNS` and `REMEDIATION_COST` values | **PREREQUISITE for Phase 2**. Set conservative defaults (`WIRING_ANALYSIS_TURNS=1`, `REMEDIATION_COST=2`) with SprintConfig overrides. | Must resolve before Phase 2 |
| 3 | `analysis_complete` degraded state | `analysis_complete: true` with separate `files_skipped: N` frontmatter field. Degraded analysis is an observability event. Failing the gate on unrelated parse errors would make shadow mode unreliable. | Approved |
| 4 | `sprint/config.py` MODIFY scope | Handled implicitly via `sprint/models.py` where SprintConfig lives. Verify during Phase 2; not a blocker. | Approved |
| 5 | `--skip-wiring-gate` CLI flag | **Defer**. Shadow mode provides non-interference. Flag adds complexity without v1.0 value. | Deferred |
| 6 | SprintGatePolicy constructor validation | **PREREQUISITE for Phase 2**. Read `trailing_gate.py` source; validate constructor requirements; document interface contract before implementing T07b. | Must resolve before Phase 2 |
| 7 | `run_wiring_safeguard_checks()` reference | Likely spec artifact. Verify nonexistence with grep; if absent, ignore. | Approved |
| 8 | Provider directory heuristic ("3+ files with common prefix") | **Exclude from v1.0**. Named directory matching is sufficient and testable. Heuristic algorithm unspecified and untested. | Deferred |
| 9 | Whitelist scope for orphans/registries | **Extend to all three finding types** in v1.0. Cost is ~10 LOC; prevents FPR mitigation gap. | Approved |
| 10 | `check_wiring_report` vs semantic checks | `check_wiring_report` as convenience wrapper calling all 5 semantic checks. Clarify in implementation. | Approved |

---

## Implementation Order Summary

```
Phase 1: Core Analysis Engine
  ├── 1.1  Data Models (T01)
  ├── 1.2  Analysis Functions (Goal-1, Goal-2, Goal-3)
  ├── 1.3  Report + Gate Definition (Goal-4, T05)
  └── 1.4  Unit Tests (T06)
  EXIT: analyzers pass fixtures, parse degradation verified

Phase 2: Sprint Integration
  ├── PREREQUISITES: Resolve OQ-2 (budget constants), OQ-6 (SprintGatePolicy)
  ├── 2.1  TurnLedger Extensions (T07a)
  ├── 2.2  Sprint Executor Hook (T07b)
  └── 2.3  TurnLedger Unit Tests
  EXIT: shadow/soft/blocking distinct, null-ledger compatible

Phase 3: KPI + Deviation Reconciliation
  ├── 3.1  KPI Report Extensions (T07c)
  └── 3.2  Deviation Reconciliation (T08) — coordinate with other gates
  EXIT: KPI complete, deviation mismatch fails gate

Phase 4: Integration + Validation
  ├── 4.1  Integration Tests (T10, T12)
  ├── 4.2  Retrospective Validation (T11)
  └── 4.3  Performance Benchmark (NFR-001)
  EXIT: SC-001–SC-015 satisfied, coverage/perf thresholds met

Phase 5: Rollout Validation (post-merge)
  ├── 5.1  Shadow Mode Baseline (min 2 releases)
  ├── 5.2  Soft Mode Readiness
  └── 5.3  Blocking Mode Authorization (evidence-gated)
```

**Critical path**: Phase 1 → Phase 2 → Phase 4. Phase 3 can run in parallel with Phase 4 (no dependency between KPI extensions and integration tests), though Milestone 3.2 should complete before final merge to avoid `roadmap/gates.py` conflicts. Phase 5 is post-merge and evidence-driven.
