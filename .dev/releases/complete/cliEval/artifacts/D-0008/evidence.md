# D-0008 — evidence

## Verification command

```
uv run pytest tests/cli/eval/test_capability_dataclass.py -v
```

## Result (2026-05-20)

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
configfile: pyproject.toml
collected 16 items

tests/cli/eval/test_capability_dataclass.py::test_capability_has_required_fields PASSED [  6%]
tests/cli/eval/test_capability_dataclass.py::test_capability_is_frozen PASSED [ 12%]
tests/cli/eval/test_capability_dataclass.py::test_capability_accepts_valid_failure_modes[hard] PASSED [ 18%]
tests/cli/eval/test_capability_dataclass.py::test_capability_accepts_valid_failure_modes[skip] PASSED [ 25%]
tests/cli/eval/test_capability_dataclass.py::test_capability_accepts_valid_failure_modes[xfail] PASSED [ 31%]
tests/cli/eval/test_capability_dataclass.py::test_capability_rejects_invalid_failure_modes[] PASSED [ 37%]
tests/cli/eval/test_capability_dataclass.py::test_capability_rejects_invalid_failure_modes[HARD] PASSED [ 43%]
tests/cli/eval/test_capability_dataclass.py::test_capability_rejects_invalid_failure_modes[hard ] PASSED [ 50%]
tests/cli/eval/test_capability_dataclass.py::test_capability_rejects_invalid_failure_modes[soft] PASSED [ 56%]
tests/cli/eval/test_capability_dataclass.py::test_capability_rejects_invalid_failure_modes[invalid] PASSED [ 62%]
tests/cli/eval/test_capability_dataclass.py::test_capability_rejects_invalid_failure_modes[fail] PASSED [ 68%]
tests/cli/eval/test_capability_dataclass.py::test_capability_rejects_invalid_failure_modes[warn] PASSED [ 75%]
tests/cli/eval/test_capability_dataclass.py::test_capability_optional_fields_default PASSED [ 81%]
tests/cli/eval/test_capability_dataclass.py::test_capability_deterministic_equality PASSED [ 87%]
tests/cli/eval/test_capability_dataclass.py::test_capability_unequal_when_field_differs PASSED [ 93%]
tests/cli/eval/test_capability_dataclass.py::test_capability_check_not_invoked_at_construction PASSED [100%]

============================== 16 passed in 0.11s ==============================
```

Full log: `TASKLIST_ROOT/evidence/T01.09/pytest.log`.

## Acceptance criteria coverage

| AC bullet (T01.09) | Test | Status |
|---|---|---|
| Frozen `Capability` dataclass with 5 named fields. | `test_capability_has_required_fields`, `test_capability_is_frozen` | PASS |
| Invalid `failure_mode` raises `ValueError`. | `test_capability_rejects_invalid_failure_modes[*]` (7 cases) | PASS |
| Valid `failure_mode` values (`hard`/`skip`/`xfail`) accepted. | `test_capability_accepts_valid_failure_modes[*]` (3 cases) | PASS |
| Two instances built from the same arguments compare equal. | `test_capability_deterministic_equality` | PASS |
| Defaults for `skip_flag` (`None`) and `description` (`""`). | `test_capability_optional_fields_default` | PASS |
| `check` callable not invoked at construction time. | `test_capability_check_not_invoked_at_construction` | PASS |
| `spec.md` records the 5-field contract. | `TASKLIST_ROOT/artifacts/D-0008/spec.md` | PRESENT |

## Files produced

- `src/superclaude/cli/eval/capabilities.py`
- `src/superclaude/cli/eval/__init__.py` (re-export added)
- `tests/cli/eval/test_capability_dataclass.py`
- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/notes.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`  (this file)
- `TASKLIST_ROOT/evidence/T01.09/pytest.log`
