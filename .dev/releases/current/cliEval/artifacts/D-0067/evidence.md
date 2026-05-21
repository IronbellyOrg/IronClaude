# D-0067 — Evidence

## Test run

```
$ uv run pytest tests/cli/eval/test_expect_settings_json.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 21 items

tests/cli/eval/test_expect_settings_json.py::test_relative_path_resolves_against_home_path PASSED
tests/cli/eval/test_expect_settings_json.py::test_absolute_path_is_used_verbatim PASSED
tests/cli/eval/test_expect_settings_json.py::test_resolution_isolated_from_real_home PASSED
tests/cli/eval/test_expect_settings_json.py::test_missing_settings_file_fails PASSED
tests/cli/eval/test_expect_settings_json.py::test_key_path_navigates_nested_dicts PASSED
tests/cli/eval/test_expect_settings_json.py::test_key_path_top_level_key PASSED
tests/cli/eval/test_expect_settings_json.py::test_key_path_short_circuits_on_missing_intermediate PASSED
tests/cli/eval/test_expect_settings_json.py::test_key_path_into_non_mapping_value PASSED
tests/cli/eval/test_expect_settings_json.py::test_exists_true_passes_when_key_present PASSED
tests/cli/eval/test_expect_settings_json.py::test_exists_true_fails_when_key_absent PASSED
tests/cli/eval/test_expect_settings_json.py::test_exists_false_passes_when_key_absent PASSED
tests/cli/eval/test_expect_settings_json.py::test_exists_false_fails_when_key_present PASSED
tests/cli/eval/test_expect_settings_json.py::test_equals_passes_on_scalar_value PASSED
tests/cli/eval/test_expect_settings_json.py::test_equals_fails_on_scalar_mismatch PASSED
tests/cli/eval/test_expect_settings_json.py::test_equals_supports_list_values PASSED
tests/cli/eval/test_expect_settings_json.py::test_equals_supports_dict_values PASSED
tests/cli/eval/test_expect_settings_json.py::test_equals_distinguishes_null_from_unset PASSED
tests/cli/eval/test_expect_settings_json.py::test_equals_fails_when_key_path_missing PASSED
tests/cli/eval/test_expect_settings_json.py::test_exists_true_and_equals_both_evaluated PASSED
tests/cli/eval/test_expect_settings_json.py::test_invalid_json_payload_fails PASSED
tests/cli/eval/test_expect_settings_json.py::test_result_carries_primitive_name_and_timing PASSED

============================== 21 passed in 0.15s ==============================
```

Full output captured at
`.dev/releases/current/cliEval/evidence/T04.04/pytest-output.txt`.

## Acceptance criteria mapping

| AC | Evidence |
|---|---|
| `Expect.settings_json(path, key_path, equals, exists)` returns ExpectCallable producing ExpectResult | `test_result_carries_primitive_name_and_timing` asserts `callable_.__name__ == "settings_json"`, `result.name == "settings_json"`, `result.duration_sec >= 0.0`; every other test asserts the `ExpectResult` shape. |
| `path` resolves against `HomeIsolation.home_path` rather than the real `~/.claude/` | `test_relative_path_resolves_against_home_path` + `test_resolution_isolated_from_real_home` — the latter asserts `result.details["path"].startswith(str(home.home_path))` against a scratch-only marker. |
| `tests/cli/eval/test_expect_settings_json.py` covers key_path navigation + equals + exists | 21 cases across `path` (4), `key_path` (4), `exists` (4), `equals` (6), combined (1), error paths (1), envelope (1). See spec.md test-matrix table. |
| `D-0067/spec.md` documents path resolution and key_path syntax | `.dev/releases/current/cliEval/artifacts/D-0067/spec.md` — §"Path resolution (NFR-ISO1 contract)" + §"`key_path` traversal rules". |

## Manual validation

```python
# Build a fixture settings.json in scratch HOME and invoke
# Expect.settings_json against it. Equivalent to
# test_key_path_navigates_nested_dicts.
import json
from superclaude.cli.eval.expect import Expect
(home.home_path / "settings.json").write_text(json.dumps(
    {"hooks": {"PreToolUse": {"matchers": ["mcp__auggie__*"]}}}
))
ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
result = Expect.settings_json(
    path="settings.json",
    key_path="hooks.PreToolUse.matchers",
    equals=["mcp__auggie__*"],
)(ctx)
assert result.passed
```

The test `test_key_path_navigates_nested_dicts` implements this exact
validation against a real `EvalContext` built from `HomeIsolation` /
`EvalConfig`.

## Files touched

| File | Change |
|---|---|
| `tests/cli/eval/test_expect_settings_json.py` | **created** — 21 tests. |
| `.dev/releases/current/cliEval/artifacts/D-0067/spec.md` | created. |
| `.dev/releases/current/cliEval/artifacts/D-0067/notes.md` | created. |
| `.dev/releases/current/cliEval/artifacts/D-0067/evidence.md` | created (this file). |
| `.dev/releases/current/cliEval/evidence/T04.04/pytest-output.txt` | created — captured pytest -v run. |

`src/superclaude/cli/eval/expect.py` was **not** modified;
`Expect.settings_json` landed in T04.01 (D-0064) and already satisfies
every AC of T04.04.
