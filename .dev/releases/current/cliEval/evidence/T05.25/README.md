# T05.25 Evidence — TEST-013 coverage-gate integration tests

Populated retroactively at T05.28 (M5 exit checkpoint).

## Files

- `pytest-test-013.log` — `uv run pytest
  tests/cli/eval/test_coverage_gate_integration.py -v` capture.
  Result: `2 failed, 4 passed in 0.23s`, exit 1.

## AC mapping

| Acceptance criterion (phase-5-tasklist.md §T05.25) | Evidence | Status |
|---|---|---|
| File `test_coverage_gate_integration.py` exists with tests for: complete coverage passes; missing matcher fails with exit 2; doctor stderr names the uncovered pattern. | `pytest-test-013.log` cases 1–6; module at `tests/cli/eval/test_coverage_gate_integration.py`. | **PARTIAL** — 4 doctor cases PASS; 2 `eval run` cases FAIL on the inherited `_new_run_id` blocker. |
| Test fixtures live under `tests/cli/eval/fixtures/coverage_gate/` for the 4-matcher case. | fixtures dir present (see test module imports). | **MET** |
| Test asserts a `coverage_missing:<pattern>` artifact file is produced. | `test_run_writes_coverage_missing_artifact_under_output_dir` case 6 written; gated on runner. | **PARTIAL** — assertion present; not yet exercisable. |
| `artifacts/D-0102/spec.md` records the test matrix. | `artifacts/D-0102/spec.md` populated at T05.28. | **MET** |

## Blocker

`NameError: name '_new_run_id' is not defined` at
`src/superclaude/cli/eval/commands.py:1418`. See
`CP-P05-END.md` § Recommended remediation step 1.
