# D-0036: FR-7.1 Interface Contract Evidence

## Contract Verification
1. `handle_regression()` signature: `(registry: DeviationRegistry, spec_path: Path, roadmap_path: Path) -> RegressionResult`
2. `RegressionResult` contains: `validated_findings`, `debate_verdicts`, `agents_succeeded`, `consolidated_report_path`
3. Regression validation + remediation counts as one budget unit (REGRESSION_VALIDATION_COST=15, no separate REMEDIATION_COST)
4. FR-7 does not spawn agents directly (delegates to handle_regression / FR-8)
5. FR-8 (handle_regression) does not evaluate convergence (no ledger ops)

## Test Evidence
- `TestInterfaceContract::test_handle_regression_signature` — PASS
- `TestInterfaceContract::test_regression_result_fields` — PASS
- `TestInterfaceContract::test_convergence_result_fields` — PASS
