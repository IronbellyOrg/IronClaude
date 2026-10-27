# D-0030: execute_fidelity_with_convergence()

## Summary
Central convergence orchestrator function implementing FR-7. Coordinates up to 3 runs within step 8 with TurnLedger budget accounting and progress tracking.

## Behavior
- Pass condition: `registry.get_active_high_count() == 0`
- Monotonic progress enforced on `structural_high_count` only
- Semantic HIGH fluctuations logged as warnings, not regression triggers
- Budget exhaustion halts with diagnostic report
- Run 1 establishes baseline (no regression detection on first run)
- Regression detection: structural increase on run_idx > 0 triggers `handle_regression()`

## Run Sequence
1. Run 1 (catch): establish baseline findings
2. Remediation between runs
3. Run 2 (verify): check progress
4. Remediation between runs
5. Run 3 (backup): final attempt

## Verification
- `uv run pytest tests/roadmap/test_convergence.py -v -k "convergence_loop"` — all pass
