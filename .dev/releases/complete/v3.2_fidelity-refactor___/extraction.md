---
spec_source: wiring-verification-gate-v1.0-release-spec.md
generated: "2026-03-20T00:00:00Z"
generator: claude-opus-4-6-requirements-extractor
functional_requirements: 15
nonfunctional_requirements: 8
total_requirements: 23
complexity_score: 0.78
complexity_class: HIGH
domains_detected: [backend, static-analysis, pipeline-infrastructure, testing, observability]
risks_identified: 8
dependencies_identified: 9
success_criteria_count: 15
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 145.0, started_at: "2026-03-20T14:28:29.931797+00:00", finished_at: "2026-03-20T14:30:54.951156+00:00"}
---

## Functional Requirements

### FR-T02: Unwired Callable Analysis (`analyze_unwired_callables`)
**Source**: Section 4.2.1, Task T02
**Priority**: P0

Detect constructor parameters typed `Optional[Callable]` (or `Callable | None`) with default `None` that are never explicitly provided at any call site in the codebase.

**Sub-requirements**:
- **FR-T02a**: AST-parse all Python files in target directory and extract `__init__` parameters matching the callable pattern via `re.compile(r'\b(typing\.)?Callable\b|r'\bcollections\.abc\.Callable\b')` with `ast.Constant` None default.
- **FR-T02b**: Search all Python files for call sites constructing matching classes; check if any call site provides the parameter by keyword.
- **FR-T02c**: Emit `WiringFinding(unwired_callable)` for each injectable with zero providing call sites.
- **FR-T02d**: Support whitelist mechanism via `wiring_whitelist.yaml` to exclude intentionally-optional callables. Whitelist entries use `symbol` + `reason` schema. Legacy `class` + `param` split form accepted and normalized.
- **FR-T02e**: Validate whitelist entries on load; skip malformed entries with `WARNING` in Phase 1 shadow mode (must NOT raise `WiringConfigError`).

### FR-T03: Orphan Module Analysis (`analyze_orphan_modules`)
**Source**: Section 4.2.2, Task T03
**Priority**: P0

Detect Python files in provider directories (`steps/`, `handlers/`, `validators/`, `checks/`) whose exported functions are never imported by any consumer module.

**Sub-requirements**:
- **FR-T03a**: Identify provider directories by convention (configurable via `provider_dir_names`).
- **FR-T03b**: AST-parse to extract top-level function definitions excluding `_private` prefix.
- **FR-T03c**: Search all Python files OUTSIDE the provider directory for import statements referencing each exported function.
- **FR-T03d**: Emit `WiringFinding(orphan_module)` for functions with zero importers.
- **FR-T03e**: Exclude `__init__.py`, `conftest.py`, and `test_*.py` files from analysis.

### FR-T04: Unwired Registry Analysis (`analyze_unwired_registries`)
**Source**: Section 4.2.3, Task T04
**Priority**: P0

Detect dictionary constants matching dispatch registry naming patterns whose values reference functions that cannot be resolved via import.

**Sub-requirements**:
- **FR-T04a**: Match module-level assignments where target name matches `DEFAULT_REGISTRY_PATTERNS` regex and value is a Dict literal.
- **FR-T04b**: For Name node values, verify importability in scope. For string values, verify resolution to `module.function` path.
- **FR-T04c**: Emit `WiringFinding(unwired_registry)` for entries with unresolvable values.

### FR-T01: Data Models
**Source**: Section 4.1, Task T01
**Priority**: P0

Implement `WiringFinding` dataclass (with `finding_type`, `file_path`, `symbol_name`, `line_number`, `detail`, `severity` fields and `to_dict()` method) and `WiringReport` dataclass (with `target_dir`, `files_analyzed`, finding lists, and computed properties: `unwired_count`, `orphan_count`, `registry_count`, `total_findings`, `passed`).

### FR-T05: Report Emitter and Gate Definition
**Source**: Sections 4.3, 4.4, Task T05
**Priority**: P0

**Sub-requirements**:
- **FR-T05a**: `emit_report()` writes Markdown file with YAML frontmatter conforming to `WIRING_GATE.required_frontmatter_fields` (12 fields: `gate`, `target_dir`, `files_analyzed`, `files_skipped`, `unwired_count`, `orphan_count`, `registry_count`, `total_findings`, `analysis_complete`, `enforcement_scope`, `resolved_gate_mode`, `whitelist_entries_applied`).
- **FR-T05b**: String-valued frontmatter fields (`target_dir`, `symbol_name`, `detail`) MUST be serialized via `yaml.safe_dump()`, not f-string interpolation.
- **FR-T05c**: `whitelist_entries_applied` field required in every report (0 if no whitelist configured/matched).
- **FR-T05d**: Define `WIRING_GATE = GateCriteria(...)` with 5 semantic checks: `analysis_complete_true`, `zero_unwired_callables`, `zero_orphan_modules`, `zero_unwired_registries`, `total_findings_consistent`.
- **FR-T05e**: Semantic check functions follow `(content: str) -> bool` pattern.
- **FR-T05f**: `check_wiring_report(content: str) -> bool` — SemanticCheck-compatible validation function.

### FR-T07a: TurnLedger Model Extensions
**Source**: Section 4.1.1, Task T07a
**Priority**: P0

**Sub-requirements**:
- **FR-T07a-1**: Add 3 fields to TurnLedger: `wiring_gate_cost: int = 0`, `wiring_gate_credits: int = 0`, `wiring_gate_scope: GateScope = GateScope.TASK`.
- **FR-T07a-2**: `debit_wiring(turns: int)` — unconditionally debit turns before analysis.
- **FR-T07a-3**: `credit_wiring(turns: int, rate: float)` — credit `int(turns * rate)` turns on pass. Must floor to 0 when `turns=1, rate=0.8`.
- **FR-T07a-4**: `can_run_wiring_gate(cost: int) -> bool` — budget availability pre-check.
- **FR-T07a-5**: Add 3 SprintConfig fields: `wiring_gate_enabled: bool = True`, `wiring_gate_scope: GateScope = GateScope.TASK`, `wiring_gate_grace_period: int = 0`. Define `SHADOW_GRACE_INFINITE = 999_999`.
- **FR-T07a-6**: `__post_init__` migration shim for deprecated `wiring_gate_mode` with deprecation warning.

### FR-T07b: Sprint Integration (Wiring Hook)
**Source**: Section 4.5, Task T07b
**Priority**: P0

**Sub-requirements**:
- **FR-T07b-1**: `run_post_task_wiring_hook(task, config, ledger=None) -> WiringReport` — post-task hook at the classification point in `sprint/executor.py`.
- **FR-T07b-2**: Skip analysis entirely when `config.wiring_gate_enabled == False`.
- **FR-T07b-3**: Debit-before-analysis, credit-on-pass budget flow with `ledger is not None` guards.
- **FR-T07b-4**: Resolve enforcement mode via `resolve_gate_mode(scope, grace_period)`.
- **FR-T07b-5**: BLOCKING mode: use `SprintGatePolicy.build_remediation_step()` with callable-based `can_remediate`/`debit` interface.
- **FR-T07b-6**: SHADOW mode: log findings, construct synthetic `TrailingGateResult`, append to `DeferredRemediationLog`.
- **FR-T07b-7**: SOFT mode: warn in TUI without blocking.
- **FR-T07b-8**: When `ledger is None` and BLOCKING failure occurs, issue direct FAIL with no remediation.

### FR-T07b-REMED: Remediation Path
**Source**: Section 4.5.3
**Priority**: P0

- **FR-T07b-REMED-a**: `_format_wiring_failure(report) -> str` — format findings for remediation subprocess input.
- **FR-T07b-REMED-b**: `_recheck_wiring(target_dir, config) -> WiringReport` — re-run analysis after remediation.
- **FR-T07b-REMED-c**: No recursive remediation — recheck FAIL is final.
- **FR-T07b-REMED-d**: Budget exhaustion mid-remediation: skip remediation, direct FAIL, log `WARN: budget-exhausted-skipping-remediation`.
- **FR-T07b-REMED-e**: Subprocess failure: treat as failed remediation, no credit, log exit code.

### FR-T07c: KPI Report Extensions
**Source**: Section 4.5.4, Task T07c
**Priority**: P1

Add 6 fields to `GateKPIReport`: `wiring_total_debits`, `wiring_total_credits`, `wiring_net_cost`, `wiring_analyses_run`, `wiring_findings_total`, `wiring_remediations_attempted`. Update `build_kpi_report()` signature to accept `wiring_ledger: TurnLedger | None`.

### FR-T08: Deviation Count Reconciliation
**Source**: Section 4.6, Task T08
**Priority**: P1

`_deviation_counts_reconciled(content: str) -> bool` added to `SPEC_FIDELITY_GATE.semantic_checks` in `roadmap/gates.py`. Parses frontmatter severity counts, regex-scans body for `DEV-\d{3}` entries, compares counts, fails on mismatch.

### FR-API: Public API Entry Point
**Source**: Section 6.1
**Priority**: P0

`run_wiring_analysis(target_dir: Path, config: WiringConfig | None = None) -> WiringReport` — single entry point orchestrating all three analyzers.

### FR-CONFIG: Configuration Dataclass
**Source**: Section 6.2
**Priority**: P0

`WiringConfig` dataclass with `registry_patterns`, `provider_dir_names` (frozenset default), `whitelist_path`, `exclude_patterns`. `load_wiring_config(path) -> WiringConfig` loader.

### FR-SHADOW-PRECHECK: Pre-Activation Validation
**Source**: Section 8, Phase 1
**Priority**: P0

- **FR-SHADOW-PRECHECK-a**: Validate at least one directory matching `provider_dir_names` exists and contains Python files before shadow mode activation.
- **FR-SHADOW-PRECHECK-b**: If first shadow run produces zero findings across all analyzers on a repo with >50 Python files, emit `WARN: zero-findings-on-first-run` and halt baseline collection.

### FR-GRACEFUL: Graceful AST Parse Failure
**Source**: Section 7 (R2), Section 9.1
**Priority**: P0

When AST parsing fails on a Python file, log warning, skip the file, increment `files_skipped` frontmatter field, do NOT fail the gate.

### FR-GATE-EVAL: Gate Evaluation Compatibility
**Source**: Section 6.3
**Priority**: P0

`WIRING_GATE` constant must be evaluable by existing `gate_passed()` function in `pipeline/gates.py` without any modification to that function.

---

## Non-Functional Requirements

### NFR-001: Analysis Performance
**Source**: Section 7 (R4), SC-009
Analysis must complete in < 5 seconds (p95) for packages up to 50 Python files. AST-only analysis, no subprocess invocation.

### NFR-002: Test Coverage
**Source**: Section 9.3
≥ 90% line coverage on `src/superclaude/cli/audit/wiring_gate.py`. Minimum 14 unit tests across 4 analyzer functions. All `finding_type` values must appear in at least one test assertion.

### NFR-003: Backward Compatibility
**Source**: Sections 4.5.2, 6.2
All TurnLedger extensions use zero-value defaults. `ledger is None` path fully operational. `__post_init__` migration shim for deprecated fields. Cross-release ordering preserved.

### NFR-004: Code Size Budget
**Source**: Section 5
Production code: 410-500 lines. Test code: 400-520 lines. Test fixtures: 50-80 LOC.

### NFR-005: YAML Safety
**Source**: Section 4.3.1
All string frontmatter fields serialized via `yaml.safe_dump()` to prevent malformed output from YAML-special characters in paths/symbols.

### NFR-006: Shadow Mode Non-Interference
**Source**: SC-006, Section 9.2
Shadow mode must not affect task status, must not propagate exceptions, must emit trace logs.

### NFR-007: Zero Existing Infrastructure Changes
**Source**: Section 11
No modifications to `pipeline/models.py`, `pipeline/gates.py` (except consuming), or `pipeline/trailing_gate.py`. Wiring gate is a pure consumer of existing patterns.

### NFR-008: Rollout Safety
**Source**: Section 8
Three-phase rollout (shadow → soft → full) with quantitative transition thresholds. Phase 2 must not activate if FPR cannot be separated from re-export noise floor.

---

## Complexity Assessment

**Score**: 0.78 / 1.0
**Class**: HIGH

**Rationale**:
- **Architectural breadth** (0.85): Touches 7+ files across 3 subsystems (audit, sprint, roadmap). Creates 2 new modules, modifies 4 existing ones.
- **Algorithm complexity** (0.75): Three distinct static analysis algorithms using AST parsing with cross-file reference resolution.
- **Integration depth** (0.80): Must integrate with TurnLedger budget system, SprintGatePolicy remediation, DeferredRemediationLog, TrailingGateRunner, and GateCriteria — all existing subsystems with established contracts.
- **State management** (0.70): Three enforcement modes (shadow/soft/full) with scope-based resolution, budget debit/credit lifecycle, remediation retry logic with edge cases.
- **Testing burden** (0.75): 14+ unit tests, 4 budget integration scenarios, 2 integration tests, test fixtures, plus regression against actual codebase.
- **Edge case density** (0.80): `int()` floor behavior, null ledger paths, budget exhaustion mid-remediation, subprocess failures, recursive remediation prevention, YAML special characters, import alias false positives.

---

## Architectural Constraints

1. **Python-only analysis**: No cross-language support (v1.0 scope).
2. **AST-only static analysis**: No runtime behavioral verification, no dynamic dispatch resolution (`**kwargs`, `getattr`, `importlib`).
3. **Consumer-only integration**: Must NOT modify `GateCriteria`, `SemanticCheck`, `gate_passed()`, `resolve_gate_mode()`, or `TrailingGateRunner` — only consume them.
4. **`SemanticCheck` interface**: All check functions must conform to `(content: str) -> bool` signature.
5. **GateCriteria pattern**: Report format must use YAML frontmatter + Markdown body, validated by `gate_passed()`.
6. **Module location**: New code in `src/superclaude/cli/audit/` (new package) and modifications to `src/superclaude/cli/sprint/` and `src/superclaude/cli/roadmap/`.
7. **TurnLedger extensions**: Wiring-specific fields only; generic `debit_gate()`/`credit_gate()` deferred to v3.3.
8. **Callable-based remediation interface**: Avoid direct `TurnLedger` import in `trailing_gate.py`; use `can_remediate`/`debit` callables.
9. **Shadow mode first**: Initial deployment MUST be shadow mode (`SHADOW_GRACE_INFINITE`). Enforcement activation requires baseline data review.
10. **No `pre_checks` on SemanticCheck**: Interface modification out of scope for v1.0.

---

## Risk Inventory

1. **R1 — False positives from intentional Optional[Callable] hooks** | Severity: **medium** | Mitigation: Whitelist mechanism (`wiring_whitelist.yaml`) with `symbol` + `reason` schema and `whitelist_entries_applied` frontmatter visibility.

2. **R2 — AST parsing fails on complex Python patterns** | Severity: **low** | Mitigation: Graceful degradation — log warning, skip file, increment `files_skipped`, do not fail gate.

3. **R3 — Shadow mode collects insufficient data** | Severity: **medium** | Mitigation: Minimum 2-release shadow period before enforcement decision.

4. **R4 — Performance impact on sprint loop** | Severity: **medium** | Mitigation: AST-only analysis with no subprocesses; < 2s expected for 50-file packages.

5. **R5 — Registry naming heuristics miss new patterns** | Severity: **low** | Mitigation: Configurable `registry_patterns` regex; log when no registries found.

6. **R6 — `provider_dir_names` mismatch with codebase conventions** | Severity: **high** | Mitigation: Pre-activation validation checklist (Section 8 Phase 1); zero-findings sanity check with `WARN: zero-findings-on-first-run`.

7. **R7 — `int(turns * reimbursement_rate)` floors to zero at single-turn** | Severity: **medium** | Mitigation: Explicit test assertions for `wiring_gate_credits == 0`; documented by-design behavior.

8. **R8 — SprintConfig field rename breaks dev branch configs** | Severity: **low** | Mitigation: `__post_init__` migration shim with deprecation warning; v3.2-new code only.

---

## Dependency Inventory

1. **`pipeline/models.py`** — `GateCriteria`, `SemanticCheck` (import, no modification)
2. **`pipeline/gates.py`** — `gate_passed()` function (consume, no modification)
3. **`pipeline/trailing_gate.py`** — `resolve_gate_mode()`, `attempt_remediation()`, `GateScope`, `GateMode`, `TrailingGateResult`, `DeferredRemediationLog` (consume, no modification)
4. **`sprint/executor.py`** — `SprintGatePolicy`, `_classify_from_result_file()`, task execution loop (modify to add hook)
5. **`sprint/models.py`** — `TurnLedger`, `SprintConfig` (modify to add fields/methods)
6. **`sprint/kpi.py`** — `GateKPIReport`, `build_kpi_report()` (modify to add fields)
7. **`roadmap/gates.py`** — `SPEC_FIDELITY_GATE` (modify to add deviation reconciliation check)
8. **Python `ast` module** — Core analysis engine (stdlib)
9. **Python `yaml` module** — Report serialization via `yaml.safe_dump()` (PyYAML dependency)

**Cross-release coordination**:
- Anti-Instincts release (`ANTI_INSTINCT_GATE` on `roadmap/gates.py`)
- Unified Audit Gating (D-03/D-04 `SPEC_FIDELITY_GATE` extensions on `roadmap/gates.py`)

---

## Success Criteria

| ID | Criterion | Acceptance Threshold |
|----|-----------|---------------------|
| SC-001 | Detects `Optional[Callable] = None` never provided at call site | Unit test passes: exactly 1 finding for unmatched callable |
| SC-002 | Detects orphan modules in provider directories | Unit test passes: finding for function with 0 importers |
| SC-003 | Detects unresolvable registry entries | Unit test passes: finding for unresolvable value |
| SC-004 | Report conforms to `GateCriteria` validation pattern | `gate_passed()` returns `(True, None)` for clean report |
| SC-005 | `gate_passed()` evaluates `WIRING_GATE` without modification | Integration test against cli-portify fixture produces expected findings |
| SC-006 | Shadow mode non-interference | Task status unchanged, no exception, trace log emitted |
| SC-007 | Whitelist excludes intentional optionals + records suppression | 0 findings for whitelisted entry AND `whitelist_entries_applied: 1` in frontmatter |
| SC-008 | Deviation count reconciliation catches mismatch | Unit test detects body/frontmatter count inconsistency |
| SC-009 | Analysis performance | < 5 seconds p95 for ≤ 50-file packages |
| SC-010 | Retrospective detection of cli-portify no-op bug | `run_wiring_analysis()` on fixture produces exactly 1 `unwired_callable` finding |
| SC-011 | Provider dir pre-activation validation | Warning emitted and baseline halted when zero provider dirs match |
| SC-012 | TurnLedger debit/credit tracking | `wiring_gate_cost` increments; `wiring_gate_credits` floors correctly |
| SC-013 | `reimbursement_rate` consumed in production | `credit_wiring()` calls `int(turns * reimbursement_rate)` |
| SC-014 | Null ledger operation | No exceptions; analysis runs; no budget calls |
| SC-015 | KPI wiring fields populated | 6 wiring-specific fields present in `GateKPIReport` |

---

## Open Questions

1. **Import alias resolution scope (v1.1)**: The spec acknowledges 30-70% FPR from re-exported classes. Is the v1.1 alias pre-pass (max 3 hops) sufficient, or should the limit be configurable? What is the actual `__init__.py` chain depth in the target codebase?

2. **`WIRING_ANALYSIS_TURNS` and `REMEDIATION_COST` constants**: These are referenced in the budget flow but never defined with concrete values. What are the initial values?

3. **`reimbursement_rate` source**: The spec references `config.reimbursement_rate` in the hook but it is not listed as a `SprintConfig` field in Section 6.2 or T07a. Is this an existing SprintConfig field? If not, it needs to be specified.

4. **`files_skipped` field on WiringReport**: The `WIRING_GATE` requires `files_skipped` in frontmatter (Section 4.4, 6.3), but `WiringReport` dataclass (Section 4.1) does not include a `files_skipped` field. This is a gap between the data model and the gate contract.

5. **`run_wiring_safeguard_checks()` reference**: Section 6.2 migration note mentions this function reads `wiring_gate_mode`, but it is not defined or specified anywhere else in the document.

6. **`sprint/config.py` modification**: Listed in the dependency map (Section 11) but absent from the file manifest (Section 5) and tasklist (Section 12). What changes are needed?

7. **`--skip-wiring-gate` flag**: Mentioned in Phase 2 rollout (Section 8) but not specified in any interface contract or tasklist. Is this a CLI flag on the sprint runner? How does it interact with `wiring_gate_enabled`?

8. **TUI integration**: SOFT mode references `tui.warn()`. What is the TUI interface? Is this an existing function or does it need creation?

9. **Heuristic provider directory detection**: Deferred to v1.1 with "pending algorithm specification and test case definition." Should v1.0 log a warning when `provider_dir_names` matches zero directories (partially addressed by FR-SHADOW-PRECHECK-a, but the warning behavior during normal runs is unspecified)?

10. **`SprintGatePolicy` constructor validation (IE-5)**: The spec notes this is the first production use of `SprintGatePolicy` in the wiring path and its constructor requirements must be validated against `trailing_gate.py`. Has this validation been done?
