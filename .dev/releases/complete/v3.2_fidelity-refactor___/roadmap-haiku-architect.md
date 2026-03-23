---
spec_source: wiring-verification-gate-v1.0-release-spec.md
complexity_score: 0.78
primary_persona: architect
---

# v3.2 Wiring Verification Gate — Architect Roadmap (Revised)

## 1. Executive Summary

This release adds a **static-analysis wiring verification gate** to the SuperClaude sprint pipeline, detecting three classes of structural defects — unwired injectable callables, orphan provider modules, and unresolvable dispatch registries — integrated into the sprint loop via shadow→soft→blocking enforcement with TurnLedger budget tracking.

### Codebase Reality (Architect Assessment)

Critical finding: **substantial implementation already exists**. The prior roadmap assumed greenfield; this revision calibrates against actual code state:

| Module | LOC | State |
|--------|-----|-------|
| `audit/wiring_gate.py` | 1048 | Core analyzers, data models, report emitter, `WIRING_GATE` constant, semantic checks **implemented** |
| `audit/wiring_config.py` | 151 | `WiringConfig`, `WiringConfigError`, whitelist loading **implemented** |
| `audit/wiring_analyzer.py` | 234 | Supplementary analyzer code **implemented** |
| `sprint/executor.py` | 1313 | `run_post_task_wiring_hook()`, `run_wiring_safeguard_checks()` hooks **exist** |
| `sprint/models.py` | 632 | `TurnLedger`, `SprintConfig` exist but **lack wiring budget extensions** (FR-T07a) |
| `sprint/kpi.py` | 151 | `GateKPIReport` exists but **lacks wiring KPI fields** (FR-T07c) |
| `roadmap/gates.py` | 948 | `SPEC_FIDELITY_GATE` exists but **lacks deviation reconciliation** (FR-T08) |

**Implication**: The primary risk is no longer "can we build it?" but "does what's built conform to the spec?" The LOC budget (NFR-004: 410-500 prod) is already exceeded at 1048 LOC in `wiring_gate.py` alone.

### Strategic Priorities (Architect Perspective)

1. **Validate before extending** — Audit existing code against all 23 requirements before writing new code. The gap analysis determines whether Phases 3-5 are net-new or corrective.
2. **Protect existing pipeline contracts** — Preserve consumer-only boundary (NFR-007) with `GateCriteria`, `SemanticCheck`, `gate_passed()`, `resolve_gate_mode()`.
3. **Ship shadow mode with confidence** — Shadow-first activation (Constraint #9) with pre-checks (FR-SHADOW-PRECHECK) and non-interference guarantees (NFR-006).
4. **Evidence-driven enforcement** — No enforcement mode promotion without quantitative data from shadow operation (NFR-008).

### Delivery Outcome

- Public orchestration entry point (FR-API)
- Standards-compliant report emitter and gate definition (FR-T05)
- Sprint post-task enforcement integration (FR-T07b)
- Budget-aware rollout and remediation (FR-T07a, FR-T07b-REMED)
- KPI and roadmap gate extensions (FR-T07c, FR-T08)
- Phased rollout from shadow to soft to full enforcement (NFR-008)

---

## 2. Phased Implementation Plan

### Phase 0 — Gap Audit of Existing Implementation

**Goal**: Validate every extraction requirement against existing code; produce PASS/PARTIAL/MISSING/EXCESS dispositions.

**Rationale**: With ~1400 LOC already implemented, writing more code without understanding conformance risks duplication, contract violations, and further LOC budget exceedance.

#### Key Work Items

1. **Validate FR-T01 (Data Models)** against `wiring_gate.py:44-67`
   - `WiringFinding`: 6 fields (`finding_type`, `file_path`, `symbol_name`, `line_number`, `detail`, `severity`) + `to_dict()`
   - `WiringReport`: `target_dir`, `files_analyzed`, finding lists, computed properties (`unwired_count`, `orphan_count`, `registry_count`, `total_findings`, `passed`)
   - **Critical gap**: Does `WiringReport` include `files_skipped`? (Open Question #4)

2. **Validate FR-T02 (Unwired Callable Analysis)** against `analyze_unwired_callables()` at line 313
   - FR-T02a: AST parsing with callable pattern regex
   - FR-T02b: Call-site keyword argument search
   - FR-T02c: `WiringFinding(unwired_callable)` emission
   - FR-T02d: Whitelist `symbol`+`reason` schema; legacy `class`+`param` normalization
   - FR-T02e: Malformed entry handling — WARNING not `WiringConfigError`

3. **Validate FR-T03 (Orphan Module Analysis)** against `analyze_orphan_modules()` at line 393
   - FR-T03a–e: Provider dirs, public function extraction, cross-file import search, finding emission, file exclusions

4. **Validate FR-T04 (Registry Analysis)** against `analyze_registries()` at line 553
   - FR-T04a–c: `DEFAULT_REGISTRY_PATTERNS` matching, importability verification, finding emission

5. **Validate FR-T05 (Report & Gate)** against `emit_report()` at line 715 and `WIRING_GATE` at line 973
   - FR-T05a: 12-field YAML frontmatter conformance
   - FR-T05b: `yaml.safe_dump()` serialization (NFR-005)
   - FR-T05c: `whitelist_entries_applied` presence
   - FR-T05d: 5 semantic checks
   - FR-T05e–f: `(content: str) -> bool` signature; `check_wiring_report()`

6. **Validate FR-CONFIG** against `wiring_config.py:47`
   - `WiringConfig` fields, `load_wiring_config()` loader

7. **Validate FR-API** against `run_wiring_analysis()` at line 673

8. **Validate FR-GRACEFUL** — AST parse failure handling

9. **Validate FR-GATE-EVAL** — `WIRING_GATE` compatibility with `gate_passed()`

10. **Validate FR-SHADOW-PRECHECK** — provider dir validation and zero-findings halt

11. **Validate sprint hooks** in `executor.py`
    - FR-T07b-1 through FR-T07b-8: Hook signature, skip logic, mode branching, null-ledger path
    - FR-T07b-REMED-a through FR-T07b-REMED-e: Remediation path

12. **LOC budget assessment** (NFR-004): 1048 LOC vs. 410-500 budget — justified or refactoring debt?

#### Deliverable
Gap analysis document with per-requirement disposition:
- **PASS**: Implemented correctly per spec
- **PARTIAL**: Code exists, doesn't fully meet contract
- **MISSING**: No implementation
- **EXCESS**: Code beyond spec

#### Milestone
**M0: Gap analysis complete; implementation scope refined**

#### Timeline Estimate
**0.5-1.0 days**

---

### Phase 1 — Open Question Resolution

**Goal**: Resolve all 10 open questions with concrete decisions before implementation work.

#### Key Work Items

1. **OQ-2** (BLOCKING for Phase 2): Define `WIRING_ANALYSIS_TURNS` and `REMEDIATION_COST` constant values
   - Survey existing TurnLedger budget constants for precedent
   - Propose conservative defaults (e.g., `WIRING_ANALYSIS_TURNS=1`, `REMEDIATION_COST=2`)

2. **OQ-3**: Resolve `reimbursement_rate` source
   - Check `SprintConfig` for existing field; if absent, add to FR-T07a-5 scope with default `0.8`

3. **OQ-4**: Reconcile `files_skipped` gap between FR-T01 and FR-T05a
   - Add `files_skipped: int = 0` to `WiringReport` if missing

4. **OQ-5**: Validate `run_wiring_safeguard_checks()` — already exists in `executor.py`; confirm coverage

5. **OQ-6**: Clarify `sprint/config.py` vs `sprint/models.py` — `SprintConfig` lives in `models.py`

6. **OQ-7**: Disposition `--skip-wiring-gate` CLI flag — defer to v3.2.1 (shadow mode provides non-interference)

7. **OQ-8**: Validate TUI integration — `tui.py` exists; confirm `warn()` or equivalent

8. **OQ-9**: Provider directory zero-match warning during normal runs

9. **OQ-10** (BLOCKING for Phase 2): Validate `SprintGatePolicy` constructor contract against `trailing_gate.py`

10. **OQ-1**: Confirm import alias resolution deferral to v1.1

#### Deliverable
Decision log with rationale per resolution; updated requirement scope

#### Milestone
**M1: All open questions resolved; OQ-2 and OQ-10 unblocked for Phase 2**

#### Timeline Estimate
**0.5-1.0 days**

---

### Phase 2 — TurnLedger Budget Extensions

**Goal**: Implement budget tracking fields and methods; all model extensions unit-tested.

**Prerequisites**: OQ-2 resolved (budget constants), OQ-10 resolved (SprintGatePolicy contract).

**Requirements**: FR-T07a-1 through FR-T07a-6

#### Key Work Items

1. **FR-T07a-1**: Add 3 fields to `TurnLedger` in `sprint/models.py`
   - `wiring_gate_cost: int = 0`
   - `wiring_gate_credits: int = 0`
   - `wiring_gate_scope: GateScope = GateScope.TASK`
   - Zero-value defaults for backward compatibility (NFR-003)

2. **FR-T07a-2**: `debit_wiring(turns: int)` — unconditional debit before analysis

3. **FR-T07a-3**: `credit_wiring(turns: int, rate: float)` — `int(turns * rate)` with floor behavior
   - **R7**: `credit_wiring(1, 0.8)` → 0 credits. By design.

4. **FR-T07a-4**: `can_run_wiring_gate(cost: int) -> bool` — budget pre-check

5. **FR-T07a-5**: Add 3 `SprintConfig` fields + `SHADOW_GRACE_INFINITE = 999_999`

6. **FR-T07a-6**: `__post_init__` migration shim for deprecated `wiring_gate_mode` (R8)

#### Unit Tests

- `test_debit_wiring_increments_cost` — SC-012
- `test_credit_wiring_floors_to_zero` — SC-012, R7
- `test_credit_wiring_normal_rate` — SC-013
- `test_can_run_wiring_gate_budget_check`
- `test_null_ledger_no_exceptions` — SC-014
- `test_migration_shim_deprecation_warning` — R8

#### Architect Notes
- Pure data model changes with no cross-module side effects
- Import `GateScope` from `pipeline/trailing_gate.py` (consume only, NFR-007)
- All defaults zero/False/TASK — existing serialized configs remain valid (NFR-003)

#### Milestone
**M2: Budget tracking operational; floor-to-zero verified; migration shim tested**

#### Timeline Estimate
**1-1.5 days**

---

### Phase 3 — Sprint Hook Hardening & Remediation

**Goal**: Wire budget flow into existing hooks; validate all enforcement modes and remediation.

**Dependency**: Phase 2 (TurnLedger extensions).

**Requirements**: FR-T07b-1 through FR-T07b-8, FR-T07b-REMED-a through FR-T07b-REMED-e

#### Key Work Items

1. **FR-T07b-3**: Wire debit-before-analysis + credit-on-pass into existing `run_post_task_wiring_hook()`
   - All budget calls guarded with `ledger is not None`

2. **Validate/fix FR-T07b-5**: BLOCKING mode — `SprintGatePolicy.build_remediation_step()` with callable-based `can_remediate`/`debit` interface (Constraint #8)

3. **Validate/fix FR-T07b-6**: SHADOW mode — synthetic `TrailingGateResult` + `DeferredRemediationLog.append()`

4. **Validate/fix FR-T07b-7**: SOFT mode — TUI warning without blocking

5. **FR-T07b-8**: Null-ledger BLOCKING path — direct FAIL, no remediation

6. **FR-T07b-REMED-d**: Budget exhaustion mid-remediation — skip, FAIL, log `WARN: budget-exhausted-skipping-remediation`

7. **FR-T07b-REMED-e**: Subprocess failure — no credit, log exit code

8. **FR-T07b-REMED-c**: No recursive remediation — single recheck then final

#### Tests

- `test_shadow_mode_no_interference` — SC-006, NFR-006
- `test_blocking_triggers_remediation` — FR-T07b-5
- `test_null_ledger_blocking_direct_fail` — FR-T07b-8
- `test_budget_exhaustion_skips_remediation` — FR-T07b-REMED-d
- `test_subprocess_failure_no_credit` — FR-T07b-REMED-e
- `test_no_recursive_remediation` — FR-T07b-REMED-c

#### Architect Notes
- Null-ledger is a first-class pathway, not an edge case (NFR-003)
- Callable-based remediation prevents coupling into trailing_gate internals (Constraint #8)
- No modifications to `pipeline/` files (NFR-007)

#### Milestone
**M3: All enforcement modes operational; budget lifecycle proven end-to-end**

#### Timeline Estimate
**2-2.5 days**

---

### Phase 4 — KPI Extensions & Deviation Reconciliation

**Goal**: Complete reporting extensions and cross-gate reconciliation.

**Dependency**: Phase 2 (TurnLedger) for KPI wiring. FR-T08 is independent of sprint changes.

**Requirements**: FR-T07c, FR-T08

#### Key Work Items

1. **FR-T07c**: Add 6 fields to `GateKPIReport` in `sprint/kpi.py`
   - `wiring_total_debits`, `wiring_total_credits`, `wiring_net_cost`
   - `wiring_analyses_run`, `wiring_findings_total`, `wiring_remediations_attempted`
   - Update `build_kpi_report()` signature: `wiring_ledger: TurnLedger | None`

2. **FR-T08**: Add `_deviation_counts_reconciled(content: str) -> bool` to `SPEC_FIDELITY_GATE.semantic_checks` in `roadmap/gates.py`
   - Parse frontmatter severity counts
   - Regex-scan body for `DEV-\d{3}` entries
   - Compare counts; fail on mismatch

#### Cross-Release Coordination
`roadmap/gates.py` is shared with Anti-Instincts (`ANTI_INSTINCT_GATE`) and Unified Audit Gating (D-03/D-04 extensions).
- **Strategy**: Isolate `_deviation_counts_reconciled()` at file end; rebase before merge; coordinate PR timing.

#### Tests

- `test_kpi_wiring_fields_populated` — SC-015
- `test_deviation_counts_match` — SC-008
- `test_deviation_counts_mismatch_fails` — SC-008

#### Milestone
**M4: KPI complete; deviation mismatch triggers deterministic gate failure**

#### Timeline Estimate
**1-1.5 days**

---

### Phase 5 — Test Suite Completion & Coverage

**Goal**: ≥90% line coverage on `wiring_gate.py`; all 15 success criteria validated.

**Requirements**: NFR-002, SC-001 through SC-015

#### Key Work Items

1. **Core analyzer tests** (minimum 14 unit tests per NFR-002)
   - SC-001: Unwired callable — exactly 1 finding for unmatched callable
   - SC-002: Orphan module — finding for function with 0 importers
   - SC-003: Unresolvable registry entry
   - SC-007: Whitelist exclusion + `whitelist_entries_applied: 1`
   - SC-010: cli-portify no-op fixture — exactly 1 `unwired_callable` finding

2. **Gate evaluation tests**
   - SC-004: `gate_passed()` returns `(True, None)` for clean report
   - SC-005: `gate_passed()` evaluates `WIRING_GATE` unmodified (integration)

3. **Pre-activation tests**
   - SC-011: Provider dir validation — warning + baseline halt

4. **Performance test**
   - SC-009: < 5 seconds p95 for ≤ 50-file packages (NFR-001)

5. **Finding-type coverage**: Every value (`unwired_callable`, `orphan_module`, `unwired_registry`) asserted

6. **Coverage**: `uv run pytest --cov=superclaude.cli.audit.wiring_gate` — target ≥90%

#### Test Fixture Budget (NFR-004: 50-80 LOC)
- Synthetic packages with known wiring defects
- Clean packages for gate-pass validation
- Whitelist configs for suppression testing
- cli-portify no-op bug reproduction fixture

#### Milestone
**M5: Coverage ≥90%; all SC-001 through SC-015 validated**

#### Timeline Estimate
**1.5-2 days**

---

### Phase 6 — Integration Validation & Shadow Deployment

**Goal**: End-to-end shadow mode operational on actual codebase.

#### Key Work Items

1. **Integration**: `run_wiring_analysis()` on cli-portify fixture
   - SC-010: Exactly 1 `unwired_callable` finding

2. **FR-SHADOW-PRECHECK validation** on `src/superclaude/` tree
   - Provider dir detection against actual directory structure
   - Non-zero findings or `WARN: zero-findings-on-first-run`

3. **Sprint smoke test**: `wiring_gate_enabled=True`, `wiring_gate_grace_period=SHADOW_GRACE_INFINITE`
   - Analysis runs, findings logged, task status unaffected (NFR-006)
   - `TrailingGateResult` appended to `DeferredRemediationLog`

4. **Performance benchmark**: 50-file package, p95 < 5s (NFR-001)

5. **NFR-007 verification**: Diff inspection — zero changes to `pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py`

6. **LOC audit**: NFR-004 compliance or justified overage

#### Milestone
**M6: Shadow mode operational; all success criteria green; release-candidate ready**

#### Timeline Estimate
**1-1.5 days**

---

### Phase 7 — Rollout & Operationalization (Post-Merge)

**Goal**: Progressive enforcement activation based on evidence.

#### 7.1 Shadow Mode Baseline
- Default to shadow (`SHADOW_GRACE_INFINITE`) per Constraint #9
- Collect minimum 2-release shadow data per R3 mitigation
- Track: findings volume, whitelist usage, zero-findings anomalies, p95 runtime

#### 7.2 Soft Mode Readiness
- Enable warnings only when:
  - Provider-dir mapping validated against real repo conventions
  - False-positive rate characterized
  - FPR separable from re-export noise floor (NFR-008)

#### 7.3 Blocking Mode Authorization
- Enable only when **all** criteria met:
  - SC-009 stable across shadow period
  - SC-010 confirmed on real code
  - Whitelist and provider heuristics calibrated
  - Budget constants verified in production path

**Key principle**: Enforcement selected by evidence, not by schedule.

#### Timeline Estimate
**2 releases minimum (shadow) + 1 release (soft/full transition)**

---

## 3. Risk Assessment and Mitigation

### High-Priority Risks

| Risk | Severity | Phase | Mitigation |
|------|----------|-------|------------|
| **R6** — `provider_dir_names` mismatch | **HIGH** | 0, 6, 7 | FR-SHADOW-PRECHECK-a/b pre-activation checks; Phase 6 real-codebase validation; Phase 7 shadow observation |
| **R1** — False positives from `Optional[Callable]` | Medium | 0, 5 | Whitelist (FR-T02d); `whitelist_entries_applied` visibility; shadow calibration |
| **R4** — Performance impact on sprint | Medium | 6 | AST-only, no subprocesses (NFR-001); benchmark < 5s p95 |
| **R3** — Insufficient shadow data | Medium | 7 | Minimum 2-release shadow; finding quality metrics |
| **R7** — `int()` floor to zero | Medium | 2 | By-design; explicit test; documented behavior |

### Secondary Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **R2** — AST parse failures | Low | FR-GRACEFUL; `files_skipped` counter |
| **R5** — Registry heuristic misses | Low | Configurable `registry_patterns` |
| **R8** — SprintConfig rename | Low | `__post_init__` migration shim (FR-T07a-6) |

### Cross-Release Risk
- **`roadmap/gates.py` contention**: FR-T08 shares file with Anti-Instincts and Unified Audit Gating. Mitigation: isolate function, rebase, coordinate timing.
- **LOC overage**: `wiring_gate.py` at 1048 LOC vs. 410-500 budget. Phase 0 determines if refactoring is needed or budget should be revised.

---

## 4. Resource Requirements and Dependencies

### Consumed Dependencies (NFR-007: no modifications)

| Module | Symbols |
|--------|---------|
| `pipeline/models.py` | `GateCriteria`, `SemanticCheck` |
| `pipeline/gates.py` | `gate_passed()` |
| `pipeline/trailing_gate.py` | `resolve_gate_mode()`, `GateScope`, `GateMode`, `TrailingGateResult`, `DeferredRemediationLog` |
| Python `ast` | AST parsing (stdlib) |
| PyYAML `yaml` | `safe_dump()` report serialization |

### Modified Files

| File | Phase | Changes |
|------|-------|---------|
| `audit/wiring_gate.py` | 0 | Gap fixes from audit |
| `audit/wiring_config.py` | 0 | Gap fixes from audit |
| `sprint/models.py` | 2 | TurnLedger + SprintConfig wiring extensions (FR-T07a) |
| `sprint/executor.py` | 3 | Budget flow wiring in existing hooks (FR-T07b) |
| `sprint/kpi.py` | 4 | 6 KPI fields + signature update (FR-T07c) |
| `roadmap/gates.py` | 4 | Deviation reconciliation check (FR-T08) |

### External/Organizational Dependencies

1. Agreement on rollout thresholds for shadow→soft→blocking
2. Budget constant values (OQ-2)
3. Release coordination with Anti-Instincts and Unified Audit Gating for `roadmap/gates.py`
4. Representative fixture repos for integration testing

---

## 5. Success Criteria Validation Map

| SC | Criterion | Phase | Test Type |
|----|-----------|-------|-----------|
| SC-001 | Unwired callable detection | 5 | Unit |
| SC-002 | Orphan module detection | 5 | Unit |
| SC-003 | Unresolvable registry detection | 5 | Unit |
| SC-004 | Report conforms to GateCriteria | 5 | Unit |
| SC-005 | `gate_passed()` evaluates WIRING_GATE unmodified | 6 | Integration |
| SC-006 | Shadow mode non-interference | 3, 6 | Integration |
| SC-007 | Whitelist exclusion + `whitelist_entries_applied` | 5 | Unit |
| SC-008 | Deviation count reconciliation | 4 | Unit |
| SC-009 | Performance < 5s p95 | 6 | Benchmark |
| SC-010 | cli-portify no-op bug detection | 6 | Integration |
| SC-011 | Provider dir pre-activation validation | 5 | Unit |
| SC-012 | TurnLedger debit/credit tracking | 2 | Unit |
| SC-013 | `reimbursement_rate` consumed | 2 | Unit |
| SC-014 | Null ledger operation | 2, 3 | Unit + Integration |
| SC-015 | KPI wiring fields populated | 4 | Unit |

All 15 success criteria mapped to test-backed verification points.

---

## 6. Timeline Summary

| Phase | Description | Estimate |
|-------|-------------|----------|
| 0 | Gap Audit | 0.5-1.0 days |
| 1 | Open Question Resolution | 0.5-1.0 days |
| 2 | TurnLedger Budget Extensions | 1-1.5 days |
| 3 | Sprint Hook Hardening | 2-2.5 days |
| 4 | KPI + Deviation Reconciliation | 1-1.5 days |
| 5 | Test Suite Completion | 1.5-2 days |
| 6 | Integration Validation | 1-1.5 days |
| **Total engineering** | | **7-10 working days** |
| 7 | Rollout (post-merge) | 2 releases shadow + 1 release soft/full |

### Phase Dependency Graph

```
Phase 0 (Gap Audit) → Phase 1 (OQ Resolution)
                            │
                            ↓
                      Phase 2 (TurnLedger) → Phase 3 (Sprint Hook)
                            │                       │
                            ↓                       ↓
                      Phase 4 (KPI + FR-T08) ←──────┘
                            │
                            ↓
                      Phase 5 (Test Suite) ← all implementation complete
                            │
                            ↓
                      Phase 6 (Integration) → Phase 7 (Rollout)
```

### Critical Path
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 6

Phase 4 is off critical path — FR-T08 can begin after Phase 1; FR-T07c after Phase 2.

### Parallel Opportunities
- Phase 4 FR-T08 (deviation reconciliation) independent of sprint changes
- Test fixture creation during Phases 2-3
- Phase 0 gap audit + Phase 1 OQ research can overlap

---

## 7. Architect Recommendations

1. **Do not skip Phase 0**. The existing 1400+ LOC of implementation must be validated against spec before any new code. The gap analysis shapes all subsequent effort.

2. **Do not begin sprint integration (Phase 3) until M2 is complete**. TurnLedger extensions are the foundation for budget flow. Attempting hook wiring without them creates test debt.

3. **Treat `provider_dir_names` validation as a first-class rollout safeguard** (R6). It is the biggest source of false confidence — a misconfigured provider list produces "clean" reports that miss real defects.

4. **Keep remediation narrow and callable-based** (Constraint #8). Avoid accidental coupling into trailing_gate internals.

5. **Use KPI data, not anecdotal feedback, for enforcement activation** (NFR-008). Especially for R1, R3, and R6.

6. **Address LOC overage explicitly in Phase 0**. Either revise NFR-004 budget with documented rationale, or plan refactoring to bring `wiring_gate.py` within bounds.

7. **Do not collapse rollout phases**. The spec's three-phase rollout exists for safety. NFR-008 depends on measured transition thresholds. Evidence before enforcement.
