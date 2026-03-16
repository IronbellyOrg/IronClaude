# D-0012 Evidence — empirical_gate_v1 Classifier

**Task:** T02.02
**Deliverable:** `empirical_gate_v1` function registered in `CLASSIFIERS["empirical_gate_v1"]`
**Status:** COMPLETE

## Implementation
```python
def empirical_gate_v1(exit_code: int, stdout: str, stderr: str) -> str:
    return "pass" if exit_code == 0 else "fail"
```

Registered at module level: `CLASSIFIERS["empirical_gate_v1"] = empirical_gate_v1`

## Validation Results
```
$ uv run python -c "from superclaude.cli.sprint.classifiers import CLASSIFIERS; print(CLASSIFIERS['empirical_gate_v1'](0, 'ok', ''))"
pass

$ uv run python -c "from superclaude.cli.sprint.classifiers import CLASSIFIERS; print(CLASSIFIERS['empirical_gate_v1'](1, '', 'error'))"
fail

$ uv run python -c "from superclaude.cli.sprint.classifiers import CLASSIFIERS; print(CLASSIFIERS['empirical_gate_v1'](127, '', 'command not found'))"
fail
```

## Acceptance Criteria Checklist
- [x] `CLASSIFIERS["empirical_gate_v1"]` resolves to callable
- [x] `empirical_gate_v1(0, ...)` returns `"pass"`
- [x] `empirical_gate_v1(1, ...)` returns `"fail"`
- [x] `empirical_gate_v1(127, ...)` returns `"fail"`
- [x] No external dependencies
