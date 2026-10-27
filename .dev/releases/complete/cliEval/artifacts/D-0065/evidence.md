# D-0065 — Evidence

## Test run

```
$ uv run pytest tests/cli/eval/test_expect_file.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
rootdir: /config/workspace/IronClaude
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 18 items

tests/cli/eval/test_expect_file.py::test_relative_path_resolves_under_home PASSED
tests/cli/eval/test_expect_file.py::test_absolute_path_is_used_verbatim PASSED
tests/cli/eval/test_expect_file.py::test_exists_true_passes_when_present PASSED
tests/cli/eval/test_expect_file.py::test_exists_true_fails_when_missing PASSED
tests/cli/eval/test_expect_file.py::test_exists_false_passes_when_missing PASSED
tests/cli/eval/test_expect_file.py::test_exists_false_fails_when_present PASSED
tests/cli/eval/test_expect_file.py::test_contains_passes_on_substring_hit PASSED
tests/cli/eval/test_expect_file.py::test_contains_fails_on_substring_miss PASSED
tests/cli/eval/test_expect_file.py::test_contains_supports_utf8 PASSED
tests/cli/eval/test_expect_file.py::test_regex_passes_on_match PASSED
tests/cli/eval/test_expect_file.py::test_regex_fails_on_no_match PASSED
tests/cli/eval/test_expect_file.py::test_regex_matches_across_lines_via_search PASSED
tests/cli/eval/test_expect_file.py::test_equals_passes_on_exact_match PASSED
tests/cli/eval/test_expect_file.py::test_equals_fails_with_unified_diff_in_details PASSED
tests/cli/eval/test_expect_file.py::test_contains_and_regex_both_evaluated PASSED
tests/cli/eval/test_expect_file.py::test_exists_true_with_contains_fails_when_substring_missing PASSED
tests/cli/eval/test_expect_file.py::test_no_assertions_passes_when_file_readable PASSED
tests/cli/eval/test_expect_file.py::test_result_carries_primitive_name_and_timing PASSED

============================== 18 passed in 0.18s ==============================
```

Full output captured at
`.dev/releases/current/cliEval/evidence/T04.02/pytest-output.txt`.

## Acceptance criteria mapping

| AC | Evidence |
|---|---|
| `Expect.file(path, exists, contains, regex, equals)` returns ExpectCallable producing ExpectResult | `test_result_carries_primitive_name_and_timing` + every other test (all assert `ExpectResult` shape). |
| Failure ExpectResult includes a unified diff snippet between expected and actual content | `test_equals_fails_with_unified_diff_in_details` — asserts `result.details["diff"]` starts with `--- expected/`, contains `+++ actual/`, and shows the differing lines. |
| `tests/cli/eval/test_expect_file.py` covers all 5 named-argument combinations with pass/fail cases | 18 cases across `path`, `exists`, `contains`, `regex`, `equals`, plus combined & envelope tests. See spec.md test-matrix table. |
| `D-0065/spec.md` documents the signature and diff format | `.dev/releases/current/cliEval/artifacts/D-0065/spec.md` — §"Signature" + §"Diff format (AC contract)". |

## Manual validation

```python
# python -c snippet captured for manual validation step
from pathlib import Path
import tempfile
from superclaude.cli.eval.expect import Expect
# (EvalContext fixture omitted; see test fixtures)
# Expect.file(path=..., contains="foo") on a fixture file with body "foo bar"
# returns ExpectResult(passed=True, name="file", failure=None).
```

The test `test_contains_passes_on_substring_hit` implements this exact
validation against a real `EvalContext` built from `HomeIsolation` /
`EvalConfig`.

## Files touched

| File | Change |
|---|---|
| `tests/cli/eval/test_expect_file.py` | **created** — 18 tests. |
| `.dev/releases/current/cliEval/artifacts/D-0065/spec.md` | created. |
| `.dev/releases/current/cliEval/artifacts/D-0065/notes.md` | created. |
| `.dev/releases/current/cliEval/artifacts/D-0065/evidence.md` | created (this file). |
| `.dev/releases/current/cliEval/evidence/T04.02/pytest-output.txt` | created — captured pytest -v run. |

`src/superclaude/cli/eval/expect.py` was **not** modified; `Expect.file`
landed in T04.01 (D-0064) and already satisfies every AC of T04.02.
