Roadmap generated. The architect roadmap at `.dev/releases/current/v3.2_fidelity-refactor___/roadmap-haiku-architect.md` has been updated with these key differences from the prior version:

**Key changes in this revision:**
- **Phase 0 is now a gap audit** (not greenfield architecture validation) — the existing ~1400 LOC of implementation must be validated against spec before writing new code
- **Accurately identifies what's MISSING vs EXISTS**: TurnLedger budget extensions (FR-T07a), KPI fields (FR-T07c), and deviation reconciliation (FR-T08) are the primary net-new work; core analyzers and hooks already exist
- **Flags the LOC budget overage**: `wiring_gate.py` at 1048 LOC vs. NFR-004's 410-500 budget — requires explicit disposition in Phase 0
- **All 23 requirement IDs preserved exactly** as extracted (FR-T02, FR-T07a-1, FR-T07b-REMED-d, etc.)
- **All 15 success criteria mapped** to specific phases and test types
- **7 phases** (0-6 engineering + Phase 7 post-merge rollout), estimated 7-10 working days + 3 release cycles for enforcement activation
es on **gap closure, hardening, and spec compliance** rather than greenfield development.

**Key architectural constraint**: The wiring gate is a pure **consumer** of existing pipeline infrastructure (`GateCriteria`, `gate_passed()`, `resolve_gate_mode()`, `TrailingGateResult`, `DeferredRemediationLog`). Zero modifications to those modules are permitted (NFR-007).

---

## Phase 1: Core Analysis Engine & Data Models (Foundation)

**Goal**: Fully spec-compliant analysis engine with correct data models, whitelist support, and report emission.

**Milestone**: All three analyzers produce correct `WiringFinding` instances; `emit_report()` generates gate-compatible Markdown with valid YAML frontmatter.

### Tasks

1. **Audit `WiringFinding` / `WiringReport` against FR-T01**
   - Verify fields: `finding_type`, `file_path`, `symbol_name`, `line_number`, `detail`, `severity`
   - Verify `WiringReport` computed properties: `unwired_count`, `orphan_count`, `registry_count`, `total_findings`, `passed`
   - Add `files_skipped` field to `WiringReport` (Open Question #4 gap)
   - Verify `to_dict()` method on `WiringFinding`

2. **Harden `analyze_unwired_callables()` per FR-T02**
   - FR-T02a: Validate AST extraction regex matches spec pattern for `Optional[Callable]` / `Callable | None`
   - FR-T02b: Cross-file call-site search for keyword provision
   - FR-T02c: Correct `WiringFinding(unwired_callable)` emission
   - FR-T02d: Whitelist support via `wiring_whitelist.yaml` — verify `symbol` + `reason` schema, legacy `class` + `param` normalization
   - FR-T02e: Malformed whitelist entries skip with WARNING (no `WiringConfigError` in Phase 1)

3. **Harden `analyze_orphan_modules()` per FR-T03**
   - FR-T03a: Configurable `provider_dir_names`
   - FR-T03b: Top-level function extraction excluding `_private` prefix
   - FR-T03c: Cross-directory import search
   - FR-T03d: Correct `WiringFinding(orphan_module)` emission
   - FR-T03e: Exclusion of `__init__.py`, `conftest.py`, `test_*.py`

4. **Harden `analyze_unwired_registries()` per FR-T04**
   - FR-T04a: `DEFAULT_REGISTRY_PATTERNS` regex matching
   - FR-T04b: Name/string value importability verification
   - FR-T04c: Correct `WiringFinding(unwired_registry)` emission

5. **Graceful AST parse failure per FR-GRACEFUL**
   - Log warning, skip file, increment `files_skipped` — no gate failure

6. **Report emitter per FR-T05**
   - FR-T05a: 12-field YAML frontmatter including `whitelist_entries_applied`
   - FR-T05b: `yaml.safe_dump()` for all string fields (NFR-005)
   - FR-T05c: `whitelist_entries_applied` always present (0 default)

7. **`WiringConfig` dataclass per FR-CONFIG**
   - `registry_patterns`, `provider_dir_names` (frozenset), `whitelist_path`, `exclude_patterns`
   - `load_wiring_config(path)` loader

8. **Public API per FR-API**
   - `run_wiring_analysis(target_dir, config) -> WiringReport` orchestrating all three analyzers

### Validation
- SC-001: Unit test for unwired callable detection
- SC-002: Unit test for orphan module detection
- SC-003: Unit test for unresolvable registry detection
- SC-007: Whitelist exclusion + `whitelist_entries_applied` frontmatter
- SC-009: Performance < 5s p95 for ≤ 50 files (NFR-001)
- SC-010: Retrospective cli-portify no-op detection

### Files Touched
- `src/superclaude/cli/audit/wiring_gate.py` (modify)
- `src/superclaude/cli/audit/wiring_config.py` (modify)
- `src/superclaude/cli/audit/wiring_analyzer.py` (modify)

---

## Phase 2: Gate Definition & Pipeline Compatibility

**Goal**: `WIRING_GATE` constant passes `gate_passed()` evaluation without any modification to the pipeline infrastructure.

**Milestone**: `gate_passed(wiring_report_content, WIRING_GATE)` returns `(True, None)` for clean reports and correctly identifies each failure mode.

### Tasks

1. **Define `WIRING_GATE = GateCriteria(...)` per FR-T05d**
   - 5 semantic checks: `analysis_complete_true`, `zero_unwired_callables`, `zero_orphan_modules`, `zero_unwired_registries`, `total_findings_consistent`
   - All checks conform to `(content: str) -> bool` signature (FR-T05e)

2. **Implement `check_wiring_report()` per FR-T05f**
   - SemanticCheck-compatible validation wrapper

3. **Gate evaluation compatibility per FR-GATE-EVAL**
   - Integration test: `gate_passed()` evaluates `WIRING_GATE` without modification to `pipeline/gates.py`

4. **Pre-activation validation per FR-SHADOW-PRECHECK**
   - FR-SHADOW-PRECHECK-a: Validate provider directories exist with Python files
   - FR-SHADOW-PRECHECK-b: Zero-findings warning on repos with >50 Python files

### Validation
- SC-004: `gate_passed()` returns `(True, None)` for clean report
- SC-005: Integration test against cli-portify fixture
- SC-011: Provider dir pre-activation warning

### Files Touched
- `src/superclaude/cli/audit/wiring_gate.py` (modify — gate constant + semantic checks)

---

## Phase 3: TurnLedger & Sprint Integration

**Goal**: Wiring gate participates in the sprint budget system with debit-before-analysis, credit-on-pass flow across all three enforcement modes.

**Milestone**: `run_post_task_wiring_hook()` correctly debits/credits the ledger, respects enforcement mode, and routes to remediation or deferred logging as appropriate.

### Tasks

1. **TurnLedger extensions per FR-T07a**
   - FR-T07a-1: Add `wiring_gate_cost`, `wiring_gate_credits`, `wiring_gate_scope` fields
   - FR-T07a-2: `debit_wiring(turns)` method
   - FR-T07a-3: `credit_wiring(turns, rate)` with `int()` floor behavior
   - FR-T07a-4: `can_run_wiring_gate(cost) -> bool`
   - FR-T07a-5: SprintConfig fields: `wiring_gate_enabled`, `wiring_gate_scope`, `wiring_gate_grace_period`, `SHADOW_GRACE_INFINITE`
   - FR-T07a-6: `__post_init__` migration shim for deprecated `wiring_gate_mode`

2. **Sprint hook implementation per FR-T07b**
   - FR-T07b-1: `run_post_task_wiring_hook()` at classification point in executor
   - FR-T07b-2: Skip when `wiring_gate_enabled == False`
   - FR-T07b-3: Debit-before-analysis with `ledger is not None` guards
   - FR-T07b-4: Mode resolution via `resolve_gate_mode(scope, grace_period)`
   - FR-T07b-5: BLOCKING mode with `SprintGatePolicy.build_remediation_step()`
   - FR-T07b-6: SHADOW mode: log, synthetic `TrailingGateResult`, append to `DeferredRemediationLog`
   - FR-T07b-7: SOFT mode: warn without blocking
   - FR-T07b-8: Null ledger + BLOCKING failure: direct FAIL

3. **Remediation path per FR-T07b-REMED**
   - FR-T07b-REMED-a: `_format_wiring_failure()` for subprocess input
   - FR-T07b-REMED-b: `_recheck_wiring()` post-remediation
   - FR-T07b-REMED-c: No recursive remediation
   - FR-T07b-REMED-d: Budget exhaustion handling
   - FR-T07b-REMED-e: Subprocess failure handling

### Validation
- SC-006: Shadow mode non-interference (NFR-006)
- SC-012: TurnLedger debit/credit tracking with floor behavior
- SC-013: `reimbursement_rate` consumed in production
- SC-014: Null ledger operation — no exceptions

### Files Touched
- `src/superclaude/cli/sprint/models.py` (modify — TurnLedger + SprintConfig)
- `src/superclaude/cli/sprint/executor.py` (modify — hook wiring)

---

## Phase 4: KPI Reporting & Deviation Reconciliation

**Goal**: Wiring gate metrics flow into the KPI system; spec fidelity gate gains deviation count reconciliation.

**Milestone**: `GateKPIReport` includes 6 wiring fields; deviation count mismatches are caught.

### Tasks

1. **KPI extensions per FR-T07c**
   - Add 6 fields to `GateKPIReport`: `wiring_total_debits`, `wiring_total_credits`, `wiring_net_cost`, `wiring_analyses_run`, `wiring_findings_total`, `wiring_remediations_attempted`
   - Update `build_kpi_report()` to accept `wiring_ledger: TurnLedger | None`

2. **Deviation count reconciliation per FR-T08**
   - `_deviation_counts_reconciled()` semantic check on `SPEC_FIDELITY_GATE`
   - Parse frontmatter severity counts vs body `DEV-\d{3}` entries

### Validation
- SC-008: Deviation count mismatch detection
- SC-015: 6 wiring-specific KPI fields populated

### Files Touched
- `src/superclaude/cli/sprint/kpi.py` (modify)
- `src/superclaude/cli/roadmap/gates.py` (modify — add check to `SPEC_FIDELITY_GATE`)

---

## Phase 5: Test Suite & Validation

**Goal**: ≥ 90% coverage on wiring gate module; all success criteria verified.

**Milestone**: Full test suite passes with all `finding_type` values exercised.

### Tasks

1. **Unit tests** (minimum 14 per NFR-002)
   - `analyze_unwired_callables`: positive detection, whitelist suppression, no false positive on provided callables
   - `analyze_orphan_modules`: positive detection, exclusion list, `_private` prefix
   - `analyze_unwired_registries`: unresolvable Name, unresolvable string, clean registry
   - `emit_report`: frontmatter field count, `yaml.safe_dump()` safety, `whitelist_entries_applied` presence
   - `WiringFinding`/`WiringReport`: computed properties, `to_dict()`
   - Graceful AST failure: `files_skipped` increment

2. **Budget integration tests** (4 scenarios)
   - Debit + credit on pass
   - Debit + no credit on fail
   - `int()` floor at single turn (R7)
   - Budget exhaustion mid-remediation

3. **Integration tests**
   - `gate_passed()` against `WIRING_GATE` with clean/dirty fixtures
   - cli-portify retrospective fixture (SC-010)

4. **Coverage enforcement**
   - ≥ 90% line coverage on `wiring_gate.py` (NFR-002)
   - All `finding_type` values in at least one assertion

### Code Size Audit (NFR-004)
   - Production: 410-500 LOC
   - Tests: 400-520 LOC
   - Fixtures: 50-80 LOC

### Files Created/Modified
- `tests/cli/audit/test_wiring_gate.py` (create/modify)
- `tests/cli/audit/conftest.py` (fixtures)
- `tests/cli/sprint/test_wiring_integration.py` (create/modify)

---

## Phase 6: Shadow Rollout & Observability

**Goal**: Gate deployed in shadow mode with `SHADOW_GRACE_INFINITE`; baseline data collection begins.

**Milestone**: Shadow mode runs in CI without affecting task status; trace logs emitted for all findings.

### Tasks

1. **Shadow mode activation**
   - Default `wiring_gate_grace_period = SHADOW_GRACE_INFINITE` (999_999)
   - Verify non-interference (NFR-006): no task status changes, no exception propagation
   - Trace logging for all findings

2. **Baseline collection instrumentation**
   - Finding counts per analysis type
   - False positive rate tracking
   - Performance metrics (p50/p95 latency)

3. **Transition threshold documentation**
   - Phase 2 (soft) criteria: FPR measurable and separable from re-export noise
   - Phase 3 (full) criteria: quantitative thresholds from NFR-008

---

## Risk Assessment & Mitigation

| Risk | Severity | Phase | Mitigation |
|------|----------|-------|------------|
| R1: False positives from intentional `Optional[Callable]` | Medium | 1 | Whitelist mechanism (FR-T02d); `whitelist_entries_applied` visibility |
| R2: AST parse failures | Low | 1 | Graceful skip + `files_skipped` counter (FR-GRACEFUL) |
| R3: Insufficient shadow data | Medium | 6 | Minimum 2-release shadow period before enforcement |
| R4: Sprint loop performance | Medium | 3 | AST-only, no subprocesses; p95 < 5s target (NFR-001) |
| R5: Registry naming heuristic gaps | Low | 1 | Configurable `registry_patterns`; log on zero matches |
| R6: Provider dir mismatch | High | 2 | Pre-activation validation (FR-SHADOW-PRECHECK); zero-findings halt |
| R7: `int()` floor on single-turn credit | Medium | 3 | Explicit test assertion; documented by-design |
| R8: Config field rename breakage | Low | 3 | `__post_init__` migration shim with deprecation warning |

### Cross-Release Coordination Risks
- **Anti-Instincts release**: Touches `roadmap/gates.py` — coordinate merge order for `SPEC_FIDELITY_GATE` modifications
- **Unified Audit Gating**: D-03/D-04 extensions also modify `SPEC_FIDELITY_GATE` — ensure additive-only changes

---

## Resource Requirements & Dependencies

### Internal Dependencies (consume only — NFR-007)
| Module | Usage | Modification |
|--------|-------|-------------|
| `pipeline/models.py` | `GateCriteria`, `SemanticCheck` | None |
| `pipeline/gates.py` | `gate_passed()` | None |
| `pipeline/trailing_gate.py` | `resolve_gate_mode()`, `TrailingGateResult`, `DeferredRemediationLog`, `GateScope` | None |

### Internal Dependencies (modify)
| Module | Changes |
|--------|---------|
| `sprint/models.py` | TurnLedger fields/methods, SprintConfig fields |
| `sprint/executor.py` | Hook wiring at classification point |
| `sprint/kpi.py` | 6 KPI fields + signature update |
| `roadmap/gates.py` | Add `_deviation_counts_reconciled` to `SPEC_FIDELITY_GATE` |

### External Dependencies
- Python `ast` module (stdlib)
- PyYAML (`yaml.safe_dump()`) — already a project dependency

---

## Open Questions Requiring Resolution

These open questions from the extraction should be resolved **before or during** the indicated phase:

| # | Question | Blocking Phase | Recommended Resolution |
|---|----------|---------------|----------------------|
| 2 | `WIRING_ANALYSIS_TURNS` and `REMEDIATION_COST` values | Phase 3 | Define as constants in `wiring_gate.py`; start with conservative values (2 turns analysis, 3 turns remediation) |
| 3 | `reimbursement_rate` source | Phase 3 | Verify if existing `SprintConfig` field; if not, add with default 0.8 |
| 4 | `files_skipped` on `WiringReport` | Phase 1 | Add field to dataclass — gap confirmed |
| 5 | `run_wiring_safeguard_checks()` | Phase 3 | Already exists in executor — validate against spec intent |
| 6 | `sprint/config.py` modification | Phase 3 | Audit whether separate from `sprint/models.py` or a spec documentation error |
| 7 | `--skip-wiring-gate` CLI flag | Phase 6 | Implement as CLI flag mapping to `wiring_gate_enabled = False` |
| 8 | TUI `tui.warn()` interface | Phase 3 | Verify existing TUI infrastructure; stub if needed |
| 10 | `SprintGatePolicy` constructor validation | Phase 3 | Validate constructor against `trailing_gate.py` before integration |

---

## Success Criteria Traceability

| Criterion | Phase | Validation Method |
|-----------|-------|------------------|
| SC-001 | 1 | Unit test: exactly 1 finding for unmatched callable |
| SC-002 | 1 | Unit test: finding for function with 0 importers |
| SC-003 | 1 | Unit test: finding for unresolvable registry value |
| SC-004 | 2 | Integration: `gate_passed()` returns `(True, None)` |
| SC-005 | 2 | Integration: cli-portify fixture produces expected findings |
| SC-006 | 6 | Shadow run: task status unchanged, no exception |
| SC-007 | 1 | Unit test: 0 findings + `whitelist_entries_applied: 1` |
| SC-008 | 4 | Unit test: body/frontmatter count mismatch detected |
| SC-009 | 5 | Performance benchmark: < 5s p95 |
| SC-010 | 5 | Integration: fixture produces exactly 1 `unwired_callable` |
| SC-011 | 2 | Unit test: warning emitted, baseline halted |
| SC-012 | 5 | Budget test: cost increments, credits floor correctly |
| SC-013 | 5 | Integration: `credit_wiring()` uses `reimbursement_rate` |
| SC-014 | 5 | Unit test: null ledger, no exceptions |
| SC-015 | 5 | Integration: 6 wiring fields in `GateKPIReport` |

---

## Timeline Estimates

| Phase | Scope | Dependencies |
|-------|-------|-------------|
| Phase 1 | Core analysis engine, data models, report emission | None — can start immediately |
| Phase 2 | Gate definition, pipeline compatibility | Phase 1 complete |
| Phase 3 | TurnLedger integration, sprint hook, remediation | Phases 1-2 complete; open questions #2, #3 resolved |
| Phase 4 | KPI reporting, deviation reconciliation | Phase 3 complete; coordinate with Anti-Instincts merge |
| Phase 5 | Full test suite, coverage enforcement | Phases 1-4 complete |
| Phase 6 | Shadow rollout, baseline collection | Phase 5 complete |

**Critical path**: Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 6

**Parallelizable**: Phase 4 can run in parallel with Phase 3 (after Phase 2), as it touches different files (`kpi.py`, `roadmap/gates.py`).
