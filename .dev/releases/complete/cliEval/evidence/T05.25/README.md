# T05.25 Evidence — TEST-013 coverage-gate integration tests

Last refreshed: 2026-05-21 (T05.25 re-verification after the
`_new_run_id` wiring blocker was resolved upstream).

## Files

- `pytest-test-013.log` — `uv run pytest
  tests/cli/eval/test_coverage_gate_integration.py -v` capture.
  Result: `6 passed in 0.20s`, exit 0.

## AC mapping

| Acceptance criterion (phase-5-tasklist.md §T05.25) | Evidence | Status |
|---|---|---|
| File `test_coverage_gate_integration.py` exists with tests for: complete coverage passes; missing matcher fails with exit 2; doctor stderr names the uncovered pattern. | `pytest-test-013.log` cases 1–6; module at `tests/cli/eval/test_coverage_gate_integration.py`. | **MET** — all 6 cases PASS. |
| Test fixtures live under `tests/cli/eval/fixtures/coverage_gate/` for the 4-matcher case. | `suite.yaml`, `settings_complete.json`, `settings_missing.json` (3 covered + 1 uncovered `mcp__auggie__novel_tool_v2`). | **MET** |
| Test asserts a `coverage_missing:<pattern>` artifact file is produced. | `test_run_writes_coverage_missing_artifact_under_output_dir` (case 6) PASS — file `coverage_missing:mcp__auggie__novel_tool_v2` written under `--output-dir`. | **MET** |
| `artifacts/D-0102/spec.md` records the test matrix. | `artifacts/D-0102/spec.md` updated to reflect 6/6 PASS posture. | **MET** |

## Blocker

Cleared. The prior `NameError: name '_new_run_id' is not defined` at
`src/superclaude/cli/eval/commands.py:1418` no longer fires; both
`eval run` cases (5 and 6) reach the top-of-run coverage gate and
exit 2 with the documented artifact written.
