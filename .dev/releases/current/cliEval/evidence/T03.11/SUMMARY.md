# T03.11 — Evidence summary

**Task:** Implement FR-RPT1 aggregated run report (R-054 / D-0054).
**Date:** 2026-05-20

## Deliverable

- `src/superclaude/cli/eval/run_report.py` — FR-RPT1 writer:
  `write_aggregated_report`, three renderers (`render_summary_markdown`
  / `render_summary_json` / `render_junit_xml`),
  `ReporterContractViolation`, and
  `REPORTER_CONTRACT_VIOLATION_EXIT_CODE = 2`.
- `src/superclaude/cli/eval/__init__.py` — exports the new public
  surface (6 names) added to `__all__`.

## Tests

`tests/cli/eval/test_run_report.py` — **19 tests, all passing**
(see `test-output.txt`). Full eval suite regression in
`pytest-regression.txt`: **886 passed, 1 warning** (pre-existing
deprecation warning unrelated to T03.11).

## Acceptance criteria coverage

| Criterion                                                                                                       | Covered by                                                                              |
|-----------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `write_aggregated_report(summary, output_dir)` writes `summary.md`, `summary.json`, optional `junit.xml`         | `test_writer_emits_markdown_and_json` + `test_writer_emits_junit_when_requested`        |
| Mismatched N'-vs-K raises `ReporterContractViolation`; process exits 2                                          | `test_writer_raises_on_n_prime_vs_k_mismatch` + `test_reporter_contract_violation_exit_code_is_two` + 3 per-renderer guard tests |
| SKIPPED rows included in `evals[]` with `skip_reason` populated                                                 | `test_skipped_rows_present_in_evals_with_skip_reason` + `test_markdown_lists_skipped_with_reason` |
| Spec doc records invariant guard                                                                                | `TASKLIST_ROOT/artifacts/D-0054/spec.md` § Invariant guard                              |
| Byte-stable renderers                                                                                           | `test_render_markdown_is_byte_stable` + `test_render_json_is_byte_stable` + `test_render_junit_is_byte_stable` |
| JSON validates against `summary.schema.json` (DM-012)                                                            | `test_writer_json_validates_against_summary_schema`                                     |
| JUnit XML feature-gated                                                                                         | `test_writer_emits_markdown_and_json` (no junit.xml by default) + `test_writer_emits_junit_when_requested` |
| Markdown design-spec §9 layout                                                                                  | `test_markdown_contains_headline_and_result`                                            |
| Partial summary path (`finished_at=""` for SIGINT)                                                              | `test_writer_handles_partial_summary_with_interrupted_row`                              |

## Invariant guard

```
_check_invariant(summary):
    expected = summary.counts.expanded_n_prime
    actual   = len(summary.evals)
    if expected != actual:
        raise ReporterContractViolation(expected, actual, run_id)
```

Called at the entry of `write_aggregated_report` **before** `mkdir`,
and at the entry of each renderer. SKIPPED rows count toward N' so they
stay in `evals[]`.

## Status mappings

**Markdown failures block / `_FAILURE_STATUSES`:**
`{FAIL, ERRORED, TIMEOUT, INTERRUPTED, XPASS}`.

**JUnit child elements:**
| Status                         | JUnit tag    |
|--------------------------------|--------------|
| `FAIL`, `XPASS`                | `<failure>`  |
| `ERRORED`, `TIMEOUT`, `INTERRUPTED` | `<error>` |
| `SKIPPED`                      | `<skipped>`  |
| `PASS`, `XFAIL`                | (bare)       |

## Artifacts written

- `src/superclaude/cli/eval/run_report.py`
- `src/superclaude/cli/eval/__init__.py` (updated)
- `tests/cli/eval/test_run_report.py`
- `.dev/releases/current/cliEval/artifacts/D-0054/{spec.md, notes.md, evidence.md}`
- `.dev/releases/current/cliEval/evidence/T03.11/{SUMMARY.md, test-output.txt, pytest-regression.txt}`
