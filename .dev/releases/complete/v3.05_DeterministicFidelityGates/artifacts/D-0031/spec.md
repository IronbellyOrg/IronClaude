# D-0031: Legacy/Convergence Dispatch

## Summary
Pipeline executor step 8 dispatch via `convergence_enabled` flag in `RoadmapConfig`.

## Implementation
- When `convergence_enabled=True`: spec-fidelity step gate is set to `None` (convergence handles pass/fail)
- When `convergence_enabled=False`: spec-fidelity step uses `SPEC_FIDELITY_GATE` (legacy behavior)
- Dispatch implemented in `_build_steps()` at line 709 of executor.py

## Mutual Exclusion
- TurnLedger never constructed in legacy mode
- Legacy branch does not import or reference TurnLedger
- `convergence_enabled=False` produces byte-identical output to commit `f4d9035`

## Verification
- `uv run pytest tests/roadmap/test_convergence.py -v -k "dispatch or legacy"` — all pass
