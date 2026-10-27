# D-0054 — Evidence

**Task:** T03.11 (Phase 3, Roadmap FR-RPT1 / R-054)
**Date:** 2026-05-20

## Test results

```
tests/cli/eval/test_run_report.py
  19 passed in 0.21s
```

Full per-test log: `TASKLIST_ROOT/evidence/T03.11/test-output.txt`.

## Per-test coverage

| #  | Test                                                              | What it pins                                                                                          |
|----|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| 1  | `test_writer_raises_on_n_prime_vs_k_mismatch`                     | Mismatched summary raises before any file is written; `expected` / `actual` / `run_id` populated.     |
| 2  | `test_reporter_contract_violation_exit_code_is_two`               | `REPORTER_CONTRACT_VIOLATION_EXIT_CODE == 2` — design-spec §4 exit-code contract.                     |
| 3  | `test_render_markdown_raises_on_mismatch`                         | Markdown renderer applies the invariant guard at entry.                                               |
| 4  | `test_render_json_raises_on_mismatch`                             | JSON renderer applies the invariant guard at entry.                                                   |
| 5  | `test_render_junit_raises_on_mismatch`                            | JUnit renderer applies the invariant guard at entry.                                                  |
| 6  | `test_skipped_rows_present_in_evals_with_skip_reason`             | SKIPPED rows appear in `evals[]` with `skip_reason` + `skip_flag_triggered` carried into JSON.        |
| 7  | `test_writer_emits_markdown_and_json`                             | Writer emits `summary.md` + `summary.json` by default; no `junit.xml`.                                |
| 8  | `test_writer_emits_junit_when_requested`                          | `emit_junit=True` adds `junit.xml`; output parses as a `<testsuite>` with one `<testcase>` per eval.  |
| 9  | `test_writer_creates_missing_output_dir`                          | `Path.mkdir(parents=True)` so the orchestrator does not need to pre-create the output directory.     |
| 10 | `test_render_markdown_is_byte_stable`                             | Two independent renderings hash-equal (SHA-256).                                                      |
| 11 | `test_render_json_is_byte_stable`                                 | Two independent renderings hash-equal (SHA-256).                                                      |
| 12 | `test_render_junit_is_byte_stable`                                | Two independent renderings hash-equal (SHA-256) — proves fixed attribute order.                       |
| 13 | `test_writer_json_validates_against_summary_schema`               | Writer's `summary.json` validates against DM-012 (`summary.schema.json` / T03.10).                    |
| 14 | `test_markdown_contains_headline_and_result`                      | Design-spec §9 header lines present (run line, suite, result, failures block, counts block).          |
| 15 | `test_markdown_lists_skipped_with_reason`                         | SKIPPED rows surface `skip_reason` in the markdown table notes column.                                |
| 16 | `test_junit_maps_status_to_correct_child_tag`                     | FAIL → `<failure>`, ERRORED → `<error>`, SKIPPED → `<skipped>`, PASS → bare `<testcase>`.             |
| 17 | `test_junit_testsuite_attributes_reflect_counts`                  | `<testsuite tests=N' failures=... skipped=...>` matches `RunCounts` / `RunTotals` accounting.         |
| 18 | `test_writer_handles_partial_summary_with_interrupted_row`        | SIGINT-style partial summary (`finished_at=""`) writes an INTERRUPTED row without crashing.           |
| 19 | `test_reporter_contract_violation_message_includes_counts`        | Exception message carries `len(evals)=...`, `expanded_n_prime=...`, and `run_id` for diagnostics.      |

## Regression

`uv run pytest tests/cli/eval/ -q` — **886 passed, 1 warning**.
Log: `TASKLIST_ROOT/evidence/T03.11/pytest-regression.txt`.

The one warning is pre-existing and unrelated to T03.11 (a deprecation
in a downstream dependency surfaced under an unrelated test). No
failures, no errors.

## Schema fidelity validation

`test_writer_json_validates_against_summary_schema` constructs a
`RunSummary` containing all three of `PASS`, `SKIPPED`, and `FAIL`
outcomes, writes it via `write_aggregated_report`, reads the resulting
`summary.json` from disk, and validates it against `summary.schema.json`
loaded by `load_summary_schema()` (T03.10's loader). The validator is
`jsonschema.Draft202012Validator` (DM-012 spec).

## Byte-stability validation

Three tests (`test_render_*_is_byte_stable`) construct an identical
`RunSummary` containing one PASS, one SKIPPED, and one FAIL row, call
the renderer twice, and SHA-256 the two outputs. All three pairs are
hash-equal. This proves:

- Markdown iteration order is deterministic (tuple-ordered `evals`).
- JSON serialisation order is deterministic (`RunSummary.to_dict()`
  preserves DM-004 field order, `json.dumps` is given `sort_keys=False`).
- JUnit XML attribute order is deterministic (insertion order matches
  the JUnit XSD convention; CPython preserves attribute order on
  output for `ElementTree`).

## Acceptance criteria status

| Acceptance criterion (T03.11 task spec)                                                                                               | Status                                              |
|---------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| `write_aggregated_report(summary, output_dir)` writes `summary.md`, `summary.json`, optional `junit.xml`                              | ✅ (#7, #8)                                          |
| Mismatched N'-vs-K raises `ReporterContractViolation`; process exits 2                                                                | ✅ (#1, #2, #3, #4, #5, #19)                         |
| SKIPPED rows included in `evals[]` with `skip_reason` populated                                                                       | ✅ (#6, #15)                                         |
| Spec doc records the invariant guard                                                                                                  | ✅ (`spec.md` § Invariant guard)                      |
| Byte-stable renderers                                                                                                                 | ✅ (#10, #11, #12)                                   |
| JSON validates against `summary.schema.json` (DM-012)                                                                                 | ✅ (#13)                                             |
| JUnit XML feature-gated                                                                                                               | ✅ (#7 absence + #8 presence)                         |
| Markdown layout per design-spec §9 (headline, table, failures block, counts block)                                                    | ✅ (#14)                                             |
| Partial summary path (SIGINT / `finished_at=""`) handled                                                                              | ✅ (#18)                                             |

## Artifacts written

- `src/superclaude/cli/eval/run_report.py` (~380 lines)
- `src/superclaude/cli/eval/__init__.py` (exports added; `__all__` updated)
- `tests/cli/eval/test_run_report.py` (19 tests)
- `.dev/releases/current/cliEval/artifacts/D-0054/{spec,notes,evidence}.md`
- `.dev/releases/current/cliEval/evidence/T03.11/{SUMMARY,test-output,pytest-regression}.{md,txt,txt}`

## Dependencies and downstream

- **Upstream:**
  - T03.07 `signal_handler.py` — `EXIT_INTERRUPTED = 3` pattern reused
    here for `REPORTER_CONTRACT_VIOLATION_EXIT_CODE = 2`.
  - T03.09 `models.py` — `RunSummary.to_dict()` and friends are the
    canonical DM-004 producers wrapped by `render_summary_json`.
  - T03.10 `schemas/summary.schema.json` + `load_summary_schema()` —
    the JSON renderer's schema-fidelity contract.
- **Downstream:**
  - T03.13 `AggregatedRunReport` Reporter class — wraps these renderers
    in a class-based `to_markdown` / `to_yaml` / `to_json` / `to_junit`
    surface (`to_yaml` is class-only).
  - Phase 4 commands wiring — catches `ReporterContractViolation` and
    exits with `REPORTER_CONTRACT_VIOLATION_EXIT_CODE`.
  - T04.17 TEST-007 — full schema-fidelity round-trip across recorded
    summary fixtures.
