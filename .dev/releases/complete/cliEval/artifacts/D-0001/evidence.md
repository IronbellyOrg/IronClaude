# D-0001 — evidence

## Verification command

```
uv run pytest tests/cli/eval/test_config.py -v
```

## Result (2026-05-20)

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
configfile: pyproject.toml
collected 6 items

tests/cli/eval/test_config.py::test_evalconfig_has_required_fields PASSED [ 16%]
tests/cli/eval/test_config.py::test_evalconfig_is_frozen PASSED          [ 33%]
tests/cli/eval/test_config.py::test_default_allowed_scratch_roots_includes_ac12_paths PASSED [ 50%]
tests/cli/eval/test_config.py::test_allowed_scratch_roots_is_immutable_tuple PASSED [ 66%]
tests/cli/eval/test_config.py::test_deterministic_equality PASSED        [ 83%]
tests/cli/eval/test_config.py::test_default_factories_yield_independent_defaults PASSED [100%]

============================== 6 passed in 0.08s ===============================
```

Full log: `TASKLIST_ROOT/evidence/T01.01/pytest.log`.

## Acceptance criteria coverage

| AC bullet (T01.01) | Test | Status |
|---|---|---|
| Module exports frozen `EvalConfig` with fields `paths,defaults,allowed_scratch_roots`. | `test_evalconfig_has_required_fields` | PASS |
| Frozen / rejects mutation. | `test_evalconfig_is_frozen` | PASS |
| Default `allowed_scratch_roots` contains `/tmp/eval-runs` and `.dev/eval-runs`. | `test_default_allowed_scratch_roots_includes_ac12_paths` | PASS |
| Construction with the same inputs produces equal instances. | `test_deterministic_equality` | PASS |
| `spec.md` records field schema and default list. | `TASKLIST_ROOT/artifacts/D-0001/spec.md` | PRESENT |

## Files produced

- `src/superclaude/cli/eval/__init__.py`
- `src/superclaude/cli/eval/config.py`
- `tests/cli/eval/__init__.py`
- `tests/cli/eval/test_config.py`
- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/notes.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`  (this file)
- `TASKLIST_ROOT/evidence/T01.01/pytest.log`
