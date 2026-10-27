# D-0028 Evidence — T04.06: Regression Test for All-Claude Tasklist Behavior

## Summary

3 regression tests added to `tests/sprint/test_preflight.py` in class
`TestAllClaudeRegression`, confirming zero behavioral change for all-Claude sprints.

## Test Inventory

| Test | Assertion | Pass |
|---|---|---|
| `test_all_claude_preflight_returns_empty` | execute_preflight_phases returns [] for 3-phase all-Claude config | ✓ |
| `test_all_claude_no_subprocess_called_by_preflight` | subprocess.run never called by preflight for all-Claude config | ✓ |
| `test_existing_tests_still_pass` | All prior-phase symbols import and behave correctly (canary) | ✓ |

## Behavioral Invariants Confirmed

- `execute_preflight_phases(config)` returns `[]` when no `execution_mode == "python"` phases exist
- No subprocess is invoked by the preflight executor for an all-Claude tasklist
- `PhaseStatus` enum values and their `is_success`/`is_failure` properties are unchanged
- `CLASSIFIERS["empirical_gate_v1"]` is still registered

## Verification

```
uv run pytest tests/sprint/test_preflight.py -v -k "AllClaude"
# 3 passed in 0.05s

uv run pytest tests/sprint/ -v
# 696 passed, 0 failed
```

The full sprint test suite (696 tests) passes without modification, confirming
the preflight feature has zero impact on existing all-Claude workflows.
