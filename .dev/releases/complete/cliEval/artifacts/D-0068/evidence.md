# D-0068 — Evidence

## Test run

```
$ uv run pytest tests/cli/eval/test_expect_exit_code.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 20 items

tests/cli/eval/test_expect_exit_code.py::test_default_passes_on_zero PASSED
tests/cli/eval/test_expect_exit_code.py::test_default_fails_on_nonzero PASSED
tests/cli/eval/test_expect_exit_code.py::test_equals_explicit_passes_on_match PASSED
tests/cli/eval/test_expect_exit_code.py::test_equals_explicit_fails_on_mismatch PASSED
tests/cli/eval/test_expect_exit_code.py::test_equals_supports_nonzero_default_override PASSED
tests/cli/eval/test_expect_exit_code.py::test_in_set_passes_when_member PASSED
tests/cli/eval/test_expect_exit_code.py::test_in_set_fails_when_not_member PASSED
tests/cli/eval/test_expect_exit_code.py::test_in_set_accepts_list_input PASSED
tests/cli/eval/test_expect_exit_code.py::test_in_set_accepts_tuple_input PASSED
tests/cli/eval/test_expect_exit_code.py::test_in_set_empty_iterable_always_fails PASSED
tests/cli/eval/test_expect_exit_code.py::test_not_equals_passes_when_different PASSED
tests/cli/eval/test_expect_exit_code.py::test_not_equals_fails_when_equal PASSED
tests/cli/eval/test_expect_exit_code.py::test_not_equals_combines_with_in_set PASSED
tests/cli/eval/test_expect_exit_code.py::test_not_equals_combines_with_equals PASSED
tests/cli/eval/test_expect_exit_code.py::test_equals_and_in_set_raises_value_error PASSED
tests/cli/eval/test_expect_exit_code.py::test_default_equals_does_not_collide_with_in_set PASSED
tests/cli/eval/test_expect_exit_code.py::test_from_mapping_threads_in_set PASSED
tests/cli/eval/test_expect_exit_code.py::test_from_mapping_threads_not_equals PASSED
tests/cli/eval/test_expect_exit_code.py::test_result_carries_primitive_name_and_timing PASSED
tests/cli/eval/test_expect_exit_code.py::test_failure_message_includes_in_set_membership PASSED

============================== 20 passed in 0.13s ==============================
```

Full output captured at
`.dev/releases/current/cliEval/evidence/T04.05/pytest-output.txt`.

## Acceptance criteria mapping

| AC (from phase-4-tasklist T04.05) | Evidence |
|---|---|
| `Expect.exit_code(equals, in_set, not_equals)` returns ExpectCallable producing ExpectResult | `test_result_carries_primitive_name_and_timing` asserts `callable_.__name__ == "exit_code"`, `result.name == "exit_code"`, `result.duration_sec >= 0.0`; every other test asserts the `ExpectResult` shape. |
| Default `equals=0` applies when no argument is passed | `test_default_passes_on_zero` (ctx.exit_code=0 → PASS) + `test_default_fails_on_nonzero` (ctx.exit_code=1 → FAIL with `expected=0`, `actual=1`). |
| Specifying both `equals` and `in_set` raises `ValueError` (mutually exclusive) | `test_equals_and_in_set_raises_value_error` — `pytest.raises(ValueError, match="mutually exclusive")` against `Expect.exit_code(equals=0, in_set={0, 1})`. |
| `D-0068/spec.md` documents the contract | `.dev/releases/current/cliEval/artifacts/D-0068/spec.md` — §"Signature", §"Argument semantics", §"Mutual-exclusion guard", §"Evaluation order", §"Failure payload", §"Empty `in_set` behaviour", §"Test matrix". |

## Manual validation (from task validation row)

> Invoke `Expect.exit_code(in_set={0,1})` on an EvalContext with `exit_code=1`.

```python
from superclaude.cli.eval.expect import Expect

# Built via the same _make_ctx fixture used in test_expect_exit_code.py.
ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=1)
result = Expect.exit_code(in_set={0, 1})(ctx)
assert result.passed
assert result.details["actual"] == 1
```

The test `test_in_set_passes_when_member` implements an equivalent
assertion against a real `EvalContext` built from `HomeIsolation` /
`EvalConfig`.

## Files touched

| File | Change |
|---|---|
| `tests/cli/eval/test_expect_exit_code.py` | **created** — 20 tests. |
| `.dev/releases/current/cliEval/artifacts/D-0068/spec.md` | created. |
| `.dev/releases/current/cliEval/artifacts/D-0068/notes.md` | created. |
| `.dev/releases/current/cliEval/artifacts/D-0068/evidence.md` | created (this file). |
| `.dev/releases/current/cliEval/evidence/T04.05/pytest-output.txt` | created — captured `pytest -v` run. |

`src/superclaude/cli/eval/expect.py` was **not** modified;
`Expect.exit_code` landed in T04.01 (D-0064) and already satisfies every
AC of T04.05.
