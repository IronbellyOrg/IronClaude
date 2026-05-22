# D-0014 — evidence

## Verification command

```
uv run pytest tests/cli/eval/test_expect_failure.py -v
```

## Result (2026-05-20)

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
configfile: pyproject.toml
collected 13 items

tests/cli/eval/test_expect_failure.py::test_expect_failure_has_required_fields PASSED [  7%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_is_frozen PASSED [ 15%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_defaults PASSED [ 23%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_fully_populated PASSED [ 30%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_traceback_captured_on_exception_path PASSED [ 38%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_to_dict_is_json_serialisable PASSED [ 46%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_to_dict_field_order_matches_dm005 PASSED [ 53%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_asdict_matches_to_dict PASSED [ 61%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_deterministic_equality PASSED [ 69%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_unequal_when_field_differs PASSED [ 76%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_round_trips_inside_expect_result PASSED [ 84%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_two_per_eval_pattern PASSED [ 92%]
tests/cli/eval/test_expect_failure.py::test_expect_failure_importable_from_package PASSED [100%]

============================== 13 passed in 0.12s ==============================
```

Full log: `TASKLIST_ROOT/evidence/T01.16/pytest.log`.

## Regression check

```
uv run pytest tests/cli/eval/
```

Result: **236 passed in 0.52s** — no regression in any sibling eval test (config, schema, models, capabilities, loader, doctor, expect_result). Prior phase-1 baseline was 223 passed (post-T01.15); the 13 new tests from T01.16 raise the total to 236.

## Acceptance criteria coverage

| AC bullet (T01.16)                                                                              | Test                                                                                            | Status  |
|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|---------|
| Frozen `ExpectFailure` with the 8 fields named in DM-005.                                       | `test_expect_failure_has_required_fields`, `test_expect_failure_is_frozen`                       | PASS    |
| `to_dict()` output is JSON-serializable per DM-005 implicit serialization requirement.           | `test_expect_failure_to_dict_is_json_serialisable`, `test_expect_failure_to_dict_field_order_matches_dm005`, `test_expect_failure_asdict_matches_to_dict` | PASS |
| Reporter produces exactly one `ExpectFailure` entry per failing Expect (per-failure construction pattern locked here; integration in COMP-008 / T03.13). | `test_expect_failure_two_per_eval_pattern`, `test_expect_failure_round_trips_inside_expect_result` | PASS    |
| `spec.md` documents the 8-field contract.                                                        | `TASKLIST_ROOT/artifacts/D-0014/spec.md`                                                        | PRESENT |
| Deterministic equality.                                                                          | `test_expect_failure_deterministic_equality`, `test_expect_failure_unequal_when_field_differs`  | PASS    |
| Defaults: `message=""`, `artifact_ref=None`, `traceback=None`.                                   | `test_expect_failure_defaults`, `test_expect_failure_fully_populated`, `test_expect_failure_traceback_captured_on_exception_path` | PASS    |
| Package re-export.                                                                               | `test_expect_failure_importable_from_package`                                                   | PASS    |

## Files produced

- `src/superclaude/cli/eval/models.py` (added `ExpectFailure` class + `_EXPECT_FAILURE_FIELDS` tuple + module docstring update; removed now-stale "forward reference" comment from the T01.15 era).
- `src/superclaude/cli/eval/__init__.py` (re-export `ExpectFailure` added to `__all__`).
- `tests/cli/eval/test_expect_failure.py` (13 tests, all PASS).
- `TASKLIST_ROOT/artifacts/D-0014/spec.md`
- `TASKLIST_ROOT/artifacts/D-0014/notes.md`
- `TASKLIST_ROOT/artifacts/D-0014/evidence.md` (this file)
- `TASKLIST_ROOT/evidence/T01.16/pytest.log`

## Cross-link: T01.15 forward-reference resolution

T01.15 (`ExpectResult`) shipped with `failure: Optional["ExpectFailure"]` and a test stand-in. T01.16 lands the concrete class in the same module, so the forward reference now resolves at runtime without any production-code edit in `ExpectResult`. The new test `test_expect_failure_round_trips_inside_expect_result` exercises the real pair end-to-end (`ExpectResult(failure=ExpectFailure(...)).to_dict()["failure"]` is the DM-005 dict). The T01.15 test stand-in remains in place to keep that module's tests isolated from this dependency.
