# D-0047: Convergence Result to StepResult Mapping

## Summary
ConvergenceResult maps to StepResult for pipeline compatibility. Step 9 receives decorative `spec_fidelity_file`.

## Implementation
- `ConvergenceResult.passed` determines StepResult status
- When `convergence_enabled=True`, `SPEC_FIDELITY_GATE` is NOT invoked
- `DeviationRegistry` is sole pass/fail authority in convergence mode
