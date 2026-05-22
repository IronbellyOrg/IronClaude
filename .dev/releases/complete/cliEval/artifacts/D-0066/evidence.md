# D-0066 — Evidence

## Test run

```
$ uv run pytest tests/cli/eval/test_expect_jsonl.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 19 items

tests/cli/eval/test_expect_jsonl.py::test_named_path_resolves_via_jsonl_paths PASSED
tests/cli/eval/test_expect_jsonl.py::test_relative_path_resolves_under_home PASSED
tests/cli/eval/test_expect_jsonl.py::test_absolute_path_is_used_verbatim PASSED
tests/cli/eval/test_expect_jsonl.py::test_missing_file_fails_with_existence_payload PASSED
tests/cli/eval/test_expect_jsonl.py::test_line_count_passes_on_exact_match PASSED
tests/cli/eval/test_expect_jsonl.py::test_line_count_fails_on_mismatch PASSED
tests/cli/eval/test_expect_jsonl.py::test_line_count_zero_passes_on_empty_jsonl PASSED
tests/cli/eval/test_expect_jsonl.py::test_line_count_ignores_blank_lines PASSED
tests/cli/eval/test_expect_jsonl.py::test_filter_narrows_rows_before_line_count PASSED
tests/cli/eval/test_expect_jsonl.py::test_filter_to_zero_rows_passes_with_count_zero PASSED
tests/cli/eval/test_expect_jsonl.py::test_assert_each_passes_when_all_rows_match PASSED
tests/cli/eval/test_expect_jsonl.py::test_assert_each_fails_on_first_mismatch PASSED
tests/cli/eval/test_expect_jsonl.py::test_assert_any_passes_when_one_row_matches PASSED
tests/cli/eval/test_expect_jsonl.py::test_assert_any_fails_when_no_row_matches PASSED
tests/cli/eval/test_expect_jsonl.py::test_assert_any_runs_against_filtered_subset PASSED
tests/cli/eval/test_expect_jsonl.py::test_invalid_json_line_fails_with_lineno PASSED
tests/cli/eval/test_expect_jsonl.py::test_no_assertions_passes_when_file_parsable PASSED
tests/cli/eval/test_expect_jsonl.py::test_combined_filter_line_count_assert_each PASSED
tests/cli/eval/test_expect_jsonl.py::test_result_carries_primitive_name_and_timing PASSED

============================== 19 passed in 0.15s ==============================
```

Full output captured at
`.dev/releases/current/cliEval/evidence/T04.03/pytest-output.txt`.

## Acceptance criteria mapping

| AC | Evidence |
|---|---|
| `Expect.jsonl(path, line_count, filter, assert_each, assert_any)` returns an ExpectCallable producing ExpectResult | `test_result_carries_primitive_name_and_timing` + every other test (each asserts `ExpectResult` shape and `result.name == "jsonl"`). |
| `assert_any` returns `passed=True` if at least one filtered line satisfies the predicate | `test_assert_any_passes_when_one_row_matches` — primitive returns `passed=True` when one of the 5 fixture rows matches `matcher == "mcp__airis-mcp-gateway__*"`. Sad-path counterpart: `test_assert_any_fails_when_no_row_matches`. |
| `tests/cli/eval/test_expect_jsonl.py` covers all 5 named-argument combinations with pass/fail cases | 19 cases across `path` (4: named, relative, absolute, missing), `line_count` (4 incl. blank-line tolerance), `filter` (2), `assert_each` (2), `assert_any` (3), parser error (1), combined / envelope (3). See spec.md test-matrix table. |
| `D-0066/spec.md` documents predicate semantics | `.dev/releases/current/cliEval/artifacts/D-0066/spec.md` — §"Argument semantics", §"Predicate signatures", and §"Failure payload by branch". |

## Manual validation

```python
# Manual-validation snippet — exact behaviour exercised by
# test_line_count_passes_on_exact_match against a real EvalContext
# built from HomeIsolation / EvalConfig:
from superclaude.cli.eval.expect import Expect
# (EvalContext / HomeIsolation fixtures omitted; see test_expect_jsonl.py
# `_make_ctx` helper.)
#
# Fixture file at HOME/hooks.jsonl contains 5 JSON rows (hook telemetry).
# Expect.jsonl(path="hooks.jsonl", line_count=5) returns
#   ExpectResult(passed=True, name="jsonl", failure=None,
#                details={"path": "...", "rows_inspected": 5})
```

## Files touched

| File | Change |
|---|---|
| `tests/cli/eval/test_expect_jsonl.py` | **created** — 19 tests. |
| `.dev/releases/current/cliEval/artifacts/D-0066/spec.md` | created. |
| `.dev/releases/current/cliEval/artifacts/D-0066/notes.md` | created. |
| `.dev/releases/current/cliEval/artifacts/D-0066/evidence.md` | created (this file). |
| `.dev/releases/current/cliEval/evidence/T04.03/pytest-output.txt` | created — captured pytest -v run. |

`src/superclaude/cli/eval/expect.py` was **not** modified; `Expect.jsonl`
landed in T04.01 (D-0064) and already satisfies every AC of T04.03.
