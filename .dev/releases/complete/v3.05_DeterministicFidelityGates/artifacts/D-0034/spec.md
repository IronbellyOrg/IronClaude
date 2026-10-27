# D-0034: Parallel Validation Agents

## Summary
`handle_regression()` in convergence.py spawns 3 agents in isolated temp directories. Each runs independently with copies of spec, roadmap, and registry.

## Behavior
- 3 temp dirs created with `_create_validation_dirs()` (prefix: `fidelity-validation-{i}-`)
- Each agent loads independent registry copy via `DeviationRegistry.load_or_create()`
- Results merged by stable ID; unique findings preserved
- Consolidated report written to `fidelity-regression-validation.md`
- Findings sorted HIGH -> MEDIUM -> LOW
- All 3 agents must succeed; any failure -> validation FAILED

## Verification
- `uv run pytest tests/roadmap/test_convergence.py -v -k "parallel_validation or handle_regression"` — all pass
