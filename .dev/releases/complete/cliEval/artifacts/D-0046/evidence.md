# D-0046 — EvalResult evidence

## Test execution

```
$ uv run pytest tests/cli/eval/test_eval_result.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
collected 16 items

tests/cli/eval/test_eval_result.py::test_eval_result_has_required_fields PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_is_frozen PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_defaults PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_artifacts_default_is_independent_per_instance PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_duration_sec_is_computed_from_timestamps PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_duration_sec_caller_value_is_overwritten PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_duration_sec_kept_when_timestamps_missing PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_to_dict_field_order_matches_dm003 PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_to_dict_is_json_serialisable PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_to_dict_unwraps_nested_outcome PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_to_dict_artifacts_is_independent_of_source PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_to_dict_renders_error_as_typed_mapping PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_to_dict_error_none_when_no_error PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_deterministic_equality PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_unequal_when_field_differs PASSED
tests/cli/eval/test_eval_result.py::test_eval_result_reexported_from_package PASSED

============================== 16 passed in 0.14s ==============================
```

## Regression sweep across sibling models

```
$ uv run pytest tests/cli/eval/test_eval_outcome.py tests/cli/eval/test_eval_result.py \
                tests/cli/eval/test_expect_result.py tests/cli/eval/test_expect_failure.py -q
65 passed in 0.17s
```

EvalOutcome (T03.01) / ExpectResult (T01.15) / ExpectFailure (T01.16) all continue to pass; the new wrapper does not regress any sibling model.

## Manual validation (per task Validation step)

> Manual check: build EvalResult with start/end and confirm duration computation.

```python
>>> from superclaude.cli.eval import EvalOutcome, EvalResult
>>> outcome = EvalOutcome(eval_id="E1", title="x", status="PASS", duration_sec=1.0)
>>> r = EvalResult(eval_id="E1", outcome=outcome,
...                start="2026-05-20T11:00:00", end="2026-05-20T11:00:01.500000")
>>> r.duration_sec
1.5
>>> r.to_dict()["error"] is None
True
>>> RuntimeError("boom") and None  # noqa
>>> r2 = EvalResult(eval_id="E1", outcome=outcome,
...                 start="2026-05-20T11:00:00", end="2026-05-20T11:00:00",
...                 error=RuntimeError("boom"))
>>> r2.to_dict()["error"]
{'type': 'builtins.RuntimeError', 'message': 'boom'}
```

The interactive transcript above is the same shape exercised by `test_eval_result_duration_sec_is_computed_from_timestamps` and `test_eval_result_to_dict_renders_error_as_typed_mapping`.

## Artifacts produced

- `src/superclaude/cli/eval/models.py` — `EvalResult` class + `_EVAL_RESULT_FIELDS` + `_render_error()`; `EvalResult` re-exported from `cli/eval/__init__.py`.
- `tests/cli/eval/test_eval_result.py` — 16 new tests covering field schema, frozen contract, duration computation (3 paths), JSON serialisation, error rendering, equality, package re-export.
- `.dev/releases/current/cliEval/artifacts/D-0046/{spec,notes,evidence}.md` — this deliverable.

## Acceptance criteria status

| Criterion (T03.02)                                                                                           | Status | Evidence |
|--------------------------------------------------------------------------------------------------------------|--------|----------|
| `EvalResult` exposes the 9 named fields.                                                                     | PASS   | `test_eval_result_has_required_fields` |
| `EvalResult.to_dict()` returns a deterministic JSON-serialisable mapping.                                    | PASS   | `test_eval_result_to_dict_field_order_matches_dm003`, `test_eval_result_to_dict_is_json_serialisable` |
| `duration_sec` is computed from `end - start` consistently.                                                  | PASS   | `test_eval_result_duration_sec_is_computed_from_timestamps`, `test_eval_result_duration_sec_caller_value_is_overwritten` |
| `TASKLIST_ROOT/artifacts/D-0046/spec.md` records the contract.                                               | PASS   | `artifacts/D-0046/spec.md` (this deliverable) |
