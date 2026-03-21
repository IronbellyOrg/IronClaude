# D-0044: SC-2, SC-3, SC-5 End-to-End Evidence

## SC-2: Convergence Budget (<=3 runs, TurnLedger never negative)

### Tests Passed
- `test_convergence_loop_early_pass` — convergence passes in 1 run when 0 HIGHs
- `test_convergence_loop_three_runs` — terminates within 3 runs max
- `test_convergence_loop_budget_exhaustion` — halts with diagnostic when budget exhausted
- `test_budget_guard_halts_on_exhaustion` — TurnLedger guard prevents negative budget

### Implementation Guarantees
- `execute_fidelity_with_convergence()` max_runs=3 (default)
- Budget guard checks `ledger.can_launch()` before each run
- Budget guard checks `ledger.can_remediate()` before remediation
- Halt includes diagnostic: available turns, consumed turns, initial budget

## SC-3: Edit Preservation (FIXED findings remain FIXED)

### Tests Passed
- `test_fixed_findings_not_reported_as_new` — FIXED findings not re-reported in subsequent runs
- `test_active_to_fixed_when_absent` — findings absent in subsequent run transition to FIXED
- `test_remediation_with_all_fixed` — all-FIXED scenario handled correctly
- `test_fixed_findings_not_re_reported` — semantic layer respects FIXED status
- `test_remediation_status_overlay_fixed` — parser correctly overlays FIXED status

### Implementation Guarantees
- `DeviationRegistry.merge_findings()` tracks first_seen/last_seen
- FIXED findings excluded from active HIGH count
- Registry persists across runs via JSON serialization

## SC-5: Legacy Backward Compatibility

### Tests Passed
- `test_backward_compatibility` suite (5 tests) — pre-v3.05 registry loads correctly
- `test_pre_v305_registry_loads_with_default_source_layer`
- `test_registry_serialization_preserves_fields`
- `test_turnledger_conditional_import` — TurnLedger import is conditional
- 26 backward compat tests pass, 1 pre-existing failure (`test_turnledger_not_in_legacy_path`)

### Implementation Guarantees
- `convergence_enabled=false` (default): spec-fidelity runs as LLM step with SPEC_FIDELITY_GATE
- `convergence_enabled=true`: spec-fidelity runs via convergence engine
- Steps 1-7 and step 9 unaffected by convergence flag (NFR-7)

## Combined Test Results
```
uv run pytest tests/roadmap/ -k "sc2 or sc3 or sc5 or legacy_compat or convergence_loop or budget_guard or fixed" → 29 passed
uv run pytest tests/roadmap/ -k "legacy or backward_compat or convergence_enabled" → 26 passed, 1 pre-existing failure
```
