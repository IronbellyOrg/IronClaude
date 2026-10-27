# D-0054 — FR-RPT1 aggregated run report contract spec

**Task:** T03.11 (Phase 3, Roadmap R-054 / FR-RPT1)
**Module:** `src/superclaude/cli/eval/run_report.py`
**Tests:** `tests/cli/eval/test_run_report.py` (19 tests, all passing)
**Status:** Implemented 2026-05-20

## Purpose

The aggregated run report module is the file-emitting layer behind
COMP-008 Reporter (T03.13). It takes a `RunSummary` (T03.09 / DM-004)
and writes the three canonical artefacts to a caller-supplied output
directory, enforcing the FR-RPT1 N'-vs-K dimensional invariant before
any file is written.

## Public surface

| Symbol                                          | Kind      | Purpose                                                                                                  |
|-------------------------------------------------|-----------|----------------------------------------------------------------------------------------------------------|
| `write_aggregated_report(summary, output_dir, *, emit_junit=False) -> Mapping[str, Path]` | function  | Writes `summary.md`, `summary.json`, and (when `emit_junit=True`) `junit.xml` under `output_dir`.        |
| `render_summary_markdown(summary) -> str`       | function  | Returns the human-readable `summary.md` body.                                                            |
| `render_summary_json(summary) -> str`           | function  | Returns the canonical `summary.json` payload (matches DM-012).                                           |
| `render_junit_xml(summary) -> str`              | function  | Returns the optional JUnit XML payload (only emitted when `emit_junit=True`).                            |
| `ReporterContractViolation`                     | exception | Raised when `len(summary.evals) != summary.counts.expanded_n_prime`. Mapped to exit code 2 by the CLI.   |
| `REPORTER_CONTRACT_VIOLATION_EXIT_CODE`         | constant  | `= 2`. Lives next to the exception so the CLI dispatcher imports a single source of truth.               |

## Invariant guard

Every public function calls `_check_invariant(summary)` before doing
any work:

```
expected = summary.counts.expanded_n_prime
actual   = len(summary.evals)
if expected != actual:
    raise ReporterContractViolation(expected=expected, actual=actual,
                                    run_id=summary.run_id)
```

`write_aggregated_report` calls the guard *before* creating the output
directory or writing any file, so a mismatched summary never leaves a
partial artefact on disk.

The exception carries the three diagnostic fields (`expected`,
`actual`, `run_id`) and a human-readable message identifying which
side disagrees with which.

## Output shapes

### `summary.md`

Layout (design-spec §9):

1. `# Eval Run: <started_at> / <run_id>`
2. `**Suite:** <suite> | **Parallel:** <N> | **Duration:** <Xm Ys>`
3. `## Result: <passed> passed, <failed> failed, ...` (six tallies)
4. `| ID | Title | Status | Duration | Notes |` table — one row per
   `EvalOutcome`, including SKIPPED rows. SKIPPED rows surface
   `skip_reason` in the Notes column; ERRORED rows surface
   `error_class`.
5. `## Failures (<n>)` block — only when at least one row carries a
   failure-class status (`FAIL`, `ERRORED`, `TIMEOUT`, `INTERRUPTED`,
   `XPASS`). Each failure block lists the `expects` lines and the
   artefact map for the failing row.
6. `## Counts` block — the five DM-012 counts sub-fields rendered as
   a bullet list so reviewers can sanity-check the table against the
   N'-vs-K accounting.

Trailing newline so concatenation stays POSIX-clean.

### `summary.json`

Wraps `summary.to_dict()` (the canonical DM-004 producer). Emitted
with `json.dumps(..., indent=2, ensure_ascii=False)` plus a trailing
newline. Validates against `summary.schema.json` (DM-012 / T03.10) for
all representative shapes (PASS-only, SKIPPED, PASS+FAIL+SKIPPED,
INTERRUPTED partial-summary).

### `junit.xml`

Single `<testsuite>` element with one `<testcase>` per
`EvalOutcome`. Status mapping:

| `EvalOutcome.status`            | JUnit child element |
|---------------------------------|---------------------|
| `PASS`                          | (none — bare case) |
| `FAIL`, `XPASS`                 | `<failure>`         |
| `ERRORED`, `TIMEOUT`, `INTERRUPTED` | `<error>`       |
| `SKIPPED`                       | `<skipped>`         |
| `XFAIL`                         | (none — bare case) |

Top-level `<testsuite>` attributes:

| Attribute    | Source                                                                   |
|--------------|--------------------------------------------------------------------------|
| `name`       | `summary.suite`                                                          |
| `tests`      | `summary.counts.expanded_n_prime`                                        |
| `failures`   | `summary.totals.failed + summary.totals.timeout`                         |
| `errors`     | `summary.totals.errored + summary.totals.interrupted`                    |
| `skipped`    | `summary.totals.skipped`                                                 |
| `time`       | `summary.duration_sec` (3 decimal places)                                |
| `timestamp`  | `summary.started_at`                                                     |

XML prologue: `<?xml version="1.0" encoding="UTF-8"?>` plus newline,
matching the canonical JUnit shape.

## Byte-stability

All three renderers are byte-stable for a given `RunSummary` input:

* `RunSummary` is a frozen dataclass with tuple-ordered `evals`.
* Markdown iterates `summary.evals` in tuple order; the failures block
  iterates the same filtered tuple in order.
* JSON uses `RunSummary.to_dict()` which preserves DM-004 field order.
* JUnit XML iterates `summary.evals` in tuple order and emits element
  attributes in a fixed order matching JUnit conventions.

Verified by hashing two independent renderings of the same summary
(see `test_render_*_is_byte_stable`).

## Failure-status classification

Failure-class statuses for the markdown headline and failures block:

```
_FAILURE_STATUSES = frozenset({"FAIL", "ERRORED", "TIMEOUT",
                               "INTERRUPTED", "XPASS"})
```

Matches design-spec §9 "Status taxonomy" table: XPASS is a surprise
success treated as a major signal; XFAIL is the expected-fail path
that does *not* count as failure.

## Exit-code semantics

Per design-spec §4:

| Exit code | Condition                                                                         |
|-----------|-----------------------------------------------------------------------------------|
| 0         | No eval in {FAIL, ERRORED, TIMEOUT, XPASS}                                        |
| 1         | At least one eval in the failure set                                              |
| 2         | Harness contract error (including `ReporterContractViolation` raised by this writer) |
| 3         | SIGINT / SIGTERM during the run (handled by signal_handler.py, T03.07)            |

`REPORTER_CONTRACT_VIOLATION_EXIT_CODE = 2` lives in this module so
the CLI dispatcher and tests have a single source of truth.

## Out-of-scope / forward references

* The Reporter class (`AggregatedRunReport`) with the four emitter
  methods (`to_markdown` / `to_yaml` / `to_json` / `to_junit`) —
  T03.13 / COMP-008. This module provides the file-emitting layer the
  class will sit on top of; `to_yaml` is a Reporter-only concern (this
  task does not emit YAML).
* The CLI dispatcher that maps `ReporterContractViolation` to exit
  code 2 lives in Phase 4 (commands wiring); the writer raises the
  exception, the dispatcher catches it.
* Schema-fidelity round-trip test across recorded runs — TEST-007
  (T04.17). This task only checks fidelity for in-line fixtures.

## Acceptance criteria coverage

| Acceptance criterion                                                                                                                                | Test(s)                                                                          |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| `write_aggregated_report(summary, output_dir)` writes `summary.md`, `summary.json`, and (when enabled) `junit.xml`                                  | `test_writer_emits_markdown_and_json`, `test_writer_emits_junit_when_requested`  |
| Mismatched N'-vs-K raises `ReporterContractViolation`; process exits 2                                                                              | `test_writer_raises_on_n_prime_vs_k_mismatch`, `test_reporter_contract_violation_exit_code_is_two` |
| SKIPPED rows are included in `evals[]` with `skip_reason` populated                                                                                 | `test_skipped_rows_present_in_evals_with_skip_reason`, `test_markdown_lists_skipped_with_reason` |
| Spec doc documents the invariant guard                                                                                                              | This file (§ Invariant guard)                                                    |
| Byte-stable emitter outputs                                                                                                                         | `test_render_markdown_is_byte_stable`, `test_render_json_is_byte_stable`, `test_render_junit_is_byte_stable` |
| JSON output validates against `summary.schema.json` (DM-012)                                                                                        | `test_writer_json_validates_against_summary_schema`                              |
| JUnit XML feature-gated (only when `emit_junit=True`)                                                                                              | `test_writer_emits_markdown_and_json` (no junit.xml by default), `test_writer_emits_junit_when_requested` |
