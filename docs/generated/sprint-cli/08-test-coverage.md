---
title: Sprint CLI - Test Suite & Coverage Analysis
generated: 2026-04-03
scope: tests/sprint/, tests/pipeline/, tests/roadmap/, tests/integration/
---

# Test Suite & Coverage Analysis

## Test File Inventory

### Sprint Tests (39 files + 8 diagnostic)

**Core executor/orchestration**:
| File | Purpose |
|------|---------|
| `tests/sprint/test_executor.py` | Executor unit tests |
| `tests/sprint/test_execute_sprint_integration.py` | E2E `execute_sprint()` with mocked process |
| `tests/sprint/test_e2e_success.py` | Multi-phase success scenarios |
| `tests/sprint/test_e2e_halt.py` | Multi-phase halt scenarios |
| `tests/sprint/test_e2e_trailing.py` | Trailing gate E2E acceptance |
| `tests/sprint/test_multi_phase.py` | Multi-phase execution flow |
| `tests/sprint/test_integration_halt.py` | Integration halt behavior |
| `tests/sprint/test_integration_lifecycle.py` | Full lifecycle integration |
| `tests/sprint/test_integration_signal.py` | Signal handling integration |

**Configuration & parsing**:
| File | Purpose |
|------|---------|
| `tests/sprint/test_config.py` | Config loading and phase discovery |
| `tests/sprint/test_cli_contract.py` | CLI argument parsing contract |
| `tests/sprint/test_resolve_release_dir.py` | Release directory resolution |
| `tests/sprint/test_resume_semantics.py` | Resume skip/rerun semantics |
| `tests/sprint/test_backward_compat_regression.py` | Backward compatibility |

**Models & status**:
| File | Purpose |
|------|---------|
| `tests/sprint/test_models.py` | Model dataclass contracts |
| `tests/sprint/test_gate_display_state.py` | Gate display state transitions |
| `tests/sprint/test_shadow_mode.py` | Shadow gate mode behavior |

**Process & monitoring**:
| File | Purpose |
|------|---------|
| `tests/sprint/test_process.py` | ClaudeProcess subprocess handling |
| `tests/sprint/test_monitor.py` | Output monitor NDJSON parsing |
| `tests/sprint/test_watchdog.py` | Stall detection watchdog |

**TUI**:
| File | Purpose |
|------|---------|
| `tests/sprint/test_tui.py` | TUI lifecycle |
| `tests/sprint/test_tui_gate_column.py` | Gate column display |
| `tests/sprint/test_tui_monitor.py` | TUI monitor integration |
| `tests/sprint/test_tui_task_updates.py` | Task status TUI updates |

**Gates & wiring**:
| File | Purpose |
|------|---------|
| `tests/sprint/test_wiring_integration.py` | Wiring gate integration |
| `tests/sprint/test_wiring_budget_scenarios.py` | Wiring budget accounting |
| `tests/sprint/test_wiring_mode_resolution.py` | Wiring mode derivation |
| `tests/sprint/test_wiring_performance.py` | Wiring gate performance |
| `tests/sprint/test_anti_instinct_sprint.py` | Anti-instinct integration |

**Quality & diagnostics**:
| File | Purpose |
|------|---------|
| `tests/sprint/test_diagnostics.py` | Diagnostic collector/classifier |
| `tests/sprint/test_kpi_contract.py` | KPI report contract |
| `tests/sprint/test_kpi_report.py` | KPI report formatting |
| `tests/sprint/test_preflight.py` | Python-mode preflight |
| `tests/sprint/test_context_injection.py` | Context injection behavior |
| `tests/sprint/test_nfr_benchmarks.py` | Non-functional requirement benchmarks |
| `tests/sprint/test_property_based.py` | Property-based tests (globally ignored) |
| `tests/sprint/test_regression_gaps.py` | Regression gap detection |
| `tests/sprint/test_phase5_negative_validation.py` | Phase 5 negative cases |
| `tests/sprint/test_phase8_halt_fix.py` | Phase 8 halt fix |

**Diagnostic sub-suite** (`tests/sprint/diagnostic/`):
| File | Purpose |
|------|---------|
| `test_debug_logger.py` | Debug logger output |
| `test_diagnostics.py` | Diagnostic system |
| `test_instrumentation.py` | Instrumentation hooks |
| `test_level_0.py` through `test_level_3.py` | Diagnostic depth levels |
| `test_negative.py` | Negative diagnostic cases |

### Pipeline Tests (33 files)

| File | Purpose |
|------|---------|
| `test_executor.py` | Pipeline executor retry/gate logic |
| `test_gates.py` | Gate evaluation function |
| `test_models.py` | Pipeline model contracts |
| `test_process.py` | Base process subprocess |
| `test_process_hooks.py` | Process hook wiring |
| `test_trailing_gate.py` | Trailing gate async evaluation |
| `test_full_flow.py` | Compound pass/remediate/halt scenarios |
| `test_parallel.py` | Parallel step execution |
| `test_thread_safety.py` | Thread safety invariants |
| `test_gate_performance.py` | Gate evaluation performance |
| `test_behavioral.py` | Behavioral contracts |
| `test_deliverable.py` | Deliverable serialization |
| `test_conflict_detector.py` | Conflict detection |
| `test_conflict_review.py` | Conflict review |
| `test_contract_extractor.py` | Contract extraction |
| `test_dataflow_graph.py` | Dataflow graph construction |
| `test_dataflow_pass.py` | Dataflow pass execution |
| `test_decompose.py` | Task decomposition |
| `test_diagnostic_chain.py` | Diagnostic chain |
| `test_fmea_classifier.py` | FMEA classification |
| `test_fmea_domains.py` | FMEA domain coverage |
| `test_fmea_promotion.py` | FMEA promotion logic |
| `test_guard_analyzer.py` | Guard analysis |
| `test_guard_pass.py` | Guard pass execution |
| `test_guard_resolution.py` | Guard resolution |
| `test_integration_decompose.py` | Integration decomposition |
| `test_invariant_pass.py` | Invariant pass execution |
| `test_invariants.py` | Invariant validation |
| `test_mutation_inventory.py` | Mutation inventory |
| `test_release_gate_validation.py` | Release gate validation |
| `test_state_detector.py` | State detection |
| `test_verification_emitter.py` | Verification emission |
| `test_combined_m2_pass.py` | Combined M2 pass |

### Roadmap Tests (48 files)

Key files requested:

**`test_convergence_wiring.py`**: Integration-heavy convergence wiring tests
- Registry construction, structural vs semantic merge tagging
- Remediation dict contract, constants sanity
- Pass/fail E2E scenarios
- Markers: `integration`
- Fixtures: `audit_trail`, `tmp_path`

**`test_gates_data.py`**: Exhaustive gate criteria validation
- All gate definitions, strictness levels
- Frontmatter/line/semantic requirements
- Fixtures: `tmp_path`

**`test_spec_fidelity.py`**: Spec fidelity pipeline/state/report coverage
- Severity definitions, quoting requirements
- YAML frontmatter contract, step timeout/retry/output
- Fidelity status derivation
- Fixtures: `tmp_path`

**`test_validate_defects.py`**: Known-defect detection
- Duplicate headings, missing frontmatter/schema defects
- Strict gate rejection paths

### Integration Tests (3 files)

| File | Purpose |
|------|---------|
| `tests/integration/test_sprint_wiring.py` | Sprint wiring integration |
| `tests/integration/test_wiring_pipeline.py` | Wiring pipeline flow |
| `tests/integration/test_wiring_e2e_shadow.py` | E2E shadow mode wiring |

### PM Agent Tests (scattered)

No dedicated `tests/pm_agent/` directory. Tests found in:
- `tests/unit/test_confidence.py` — ConfidenceChecker
- `tests/unit/test_reflexion.py` — ReflexionPattern
- `tests/unit/test_self_check.py` — SelfCheckProtocol
- `tests/unit/test_token_budget.py` — Token budget
- `tests/integration/test_pytest_plugin.py` — Plugin fixture validation

## Test Fixtures

### Global (`tests/conftest.py`)

| Fixture | Purpose |
|---------|---------|
| `sample_context` | PM context with all checks passing |
| `low_confidence_context` | PM context with low confidence |
| `sample_implementation` | Passing implementation dict |
| `failing_implementation` | Failing implementation dict |
| `temp_memory_dir` | Temp dir for PM Agent tests |

Also: `collect_ignore = ["sprint/test_property_based.py"]`

### Pipeline (`tests/pipeline/conftest.py`)

| Fixture | Purpose |
|---------|---------|
| `tmp_dir` | Temporary directory |
| `make_file` | Helper to create test files |

### Roadmap (`tests/roadmap/conftest.py`)

| Fixture | Purpose |
|---------|---------|
| `audit_trail` (session) | Shared audit trail for integration tests |
| `results_dir` | Results directory |

Writes summary JSON/JSONL at teardown.

### Sprint Diagnostic (`tests/sprint/diagnostic/conftest.py`)

| Fixture | Purpose |
|---------|---------|
| `harness` | `DiagnosticTestHarness` |
| `multi_phase_harness` | Multi-phase diagnostic harness |
| `log_reader_factory` | `DebugLogReader` factory |

## Test Markers

| Marker | Used In | Purpose |
|--------|---------|---------|
| `integration` | roadmap, sprint | Integration-level tests |
| `e2e_trailing` | sprint | Trailing gate E2E |
| `unit` | auto-applied | Unit tests (by path) |
| `parametrize` | many | Parameterized test cases |
| `nfr_benchmark` | sprint | Non-functional benchmarks |
| `context_injection_test` | sprint | Context injection tests |
| `property_based` | sprint | Property-based (ignored) |
| `backward_compat` | sprint | Backward compatibility |
| `performance` | sprint, pipeline | Performance tests |
| `slow` | various | Slow-running tests |
| `gate_performance` | pipeline | Gate performance |
| `thread_safety` | pipeline | Thread safety |
| `confidence_check` | PM tests | Confidence gating |
| `self_check` | PM tests | Self-check validation |
| `reflexion` | PM tests | Error learning |

## Coverage Analysis

### Well-Tested Areas

- Sprint orchestration + status transitions + halt/resume semantics
- TurnLedger budget debit/credit accounting and gating
- Trailing gates: queueing, retries, remediation, thread safety
- Roadmap step graph ordering and gate datasets
- Convergence engine behavior and invariants
- Prompt builders and report formatting contracts
- State persistence (`.roadmap-state.json`) and backward compatibility
- Multiple E2E scenario files across sprint/roadmap

### Coverage Gaps

| Area | Issue |
|------|-------|
| PM Agent tests | Scattered across `unit/`, no dedicated package |
| True external E2E | Most "integration" tests mock subprocess boundary |
| Property-based tests | Present but globally ignored |
| Cross-pipeline E2E | No single test spanning roadmap -> tasklist -> sprint |
| Shadow gates runtime | Config exists but no executor branches use it |
| Per-task turn counting | Returns `0` with comment "wired separately" |
| Task dependency ordering | Parsed but not used for execution ordering |
