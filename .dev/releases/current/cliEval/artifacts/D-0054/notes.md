# D-0054 — Implementation notes

## Design decisions

### Invariant guard at every public renderer, not just the writer

`_check_invariant(summary)` is called at the top of
`write_aggregated_report`, `render_summary_markdown`,
`render_summary_json`, and `render_junit_xml`. A naive design would
only enforce it inside the writer, on the assumption that the renderers
are private helpers. But the renderers are *exported* (Reporter T03.13
will call them directly for `to_markdown` / `to_json`), so a misbuilt
RunSummary that bypasses the writer could otherwise leak through to a
caller via `Reporter.to_markdown()` without ever triggering the contract
violation. Putting the guard at every entry point makes the invariant
load-bearing for the whole `run_report` public surface, not just one
function.

The cost (an extra `int == int` comparison per render) is negligible
relative to file IO.

### Writer checks invariant *before* `mkdir`

The writer does `_check_invariant(summary)` *before* it calls
`Path(output_dir).mkdir(parents=True, exist_ok=True)`. This is
intentional: a mismatched summary should not even create the output
directory, because doing so would leave an empty dir as a side-effect of
a failed run. The current order means:

1. Invariant fails → exception raised → no fs side effects.
2. Invariant passes → mkdir → write md → write json → (optional) write
   junit.

Each renderer also re-checks the invariant before doing work; this is
defence-in-depth, not duplication. If the writer is bypassed and a
caller composes its own write sequence around the renderers, every
renderer still aborts cleanly.

### `REPORTER_CONTRACT_VIOLATION_EXIT_CODE` lives in `run_report.py`, not in a shared exit-codes module

T03.07 (`signal_handler.py`) defined `EXIT_INTERRUPTED = 3` next to the
SIGINT handler that emits it. Following that pattern, the reporter
contract exit code lives next to the exception class that raises it.
Two upsides:

1. Tests for the writer can import both the exception and its exit code
   from one module.
2. There is no central `exit_codes.py` to grow into an unrelated
   grab-bag.

Future CLI dispatcher work (Phase 4) will import the constant from
`run_report` directly; the README and design-spec already cross-reference
this convention.

### Failure-class membership: XPASS in, XFAIL out

`_FAILURE_STATUSES = {"FAIL", "ERRORED", "TIMEOUT", "INTERRUPTED", "XPASS"}`.

The design-spec §9 status taxonomy table distinguishes:

- **XFAIL** — expected fail; *not* a failure (expected-failure path
  worked as intended).
- **XPASS** — surprise success; *is* a failure (the eval was expected
  to fail but didn't, suggesting the expectation drifted).

The markdown "Failures (N)" block and the JUnit `<failure>` mapping both
honour this asymmetry. The JSON output is just the verbatim
`RunSummary.to_dict()` — status is a string, no classification is baked
in — so consumers can re-classify if they prefer a different convention.

### Markdown layout: counts block goes *last*

Design-spec §9 shows the counts block at the end of `summary.md`, after
the per-eval table and the failures block. This is intentional — a
reviewer scrolling top-to-bottom sees the result headline, then the
table (where they spot what failed), then the failures block (where
they understand why), and only then the N'-vs-K accounting. Putting
counts at the top would clutter the most-read section with numbers that
matter mostly for contract auditing.

The trailing `_Finished at <ts>._` line is added when `finished_at` is
non-empty; partial summaries (SIGINT path) omit it cleanly.

### JUnit XML element attributes are inserted in a fixed order

`xml.etree.ElementTree` preserves attribute insertion order on the
output side (CPython 3.8+). The writer inserts attributes in a fixed
order matching the JUnit XSD convention:

```
testsuite: name, tests, failures, errors, skipped, time, timestamp
testcase:  classname, name, time
skipped:   message, type
failure:   message, type
error:     message, type
```

This is what `test_render_junit_is_byte_stable` is actually verifying —
the SHA-256 of two independent renderings of the same summary matches
because the attribute order is reproducible.

### `testsuite[tests=]` uses `expanded_n_prime`, not `len(evals)`

These are equal by the FR-RPT1 invariant, but the writer reads the
value from `summary.counts.expanded_n_prime` to make the link to
DM-012 explicit. If a downstream reviewer wonders "what does the JUnit
`tests=` attribute correspond to?", the answer is "the canonical N'
count" — readable in code, not "implicitly defined by len(evals)".

### `_format_duration` keeps one decimal even for sub-second values

A duration of `0.05` would otherwise flatten to `"0s"` in `int(seconds)`
formatting, hiding fast evals in the table. Keeping one decimal gives
`"0.1s"` (close enough) and `"12.0s"` (readable). For minute-scale
durations, the `Xm Y.Ys` shape keeps the seconds component aligned
across rows.

### JUnit `<skipped>` carries `message` and `type` attributes

`<skipped message="<skip_reason>" type="<skip_flag_triggered>" />`. The
`type` is the flag that gated the skip (e.g. `--no-mcp`), so an
operator reading `junit.xml` in CI can correlate skipped evals back to
the capability gate that filtered them. JUnit consumers that don't care
about `type` ignore unknown attributes — this is forward-compatible.

### Trailing newline on every file

Every renderer ends with `\n`:

- Markdown: `"\n".join(lines)` with an empty string appended to `lines`.
- JSON: explicit `+ "\n"` after `json.dumps`.
- JUnit: explicit `+ "\n"` after `ET.tostring(...)`.

POSIX text-file convention. Avoids "no newline at end of file" warnings
from `git diff` and lets `cat` two summaries together cleanly.

## Cross-references

- **Module** — `src/superclaude/cli/eval/run_report.py`.
- **Tests** — `tests/cli/eval/test_run_report.py` (19 tests, all
  passing).
- **Schema** — `src/superclaude/cli/eval/schemas/summary.schema.json`
  (D-0053 / T03.10) — the JSON renderer's output validates against
  this in `test_writer_json_validates_against_summary_schema`.
- **Models** — `RunSummary`, `RunCounts`, `RunTotals`, `EvalOutcome`,
  `ExpectResult` from `superclaude.cli.eval.models` (T03.09).
- **Exit codes** — `EXIT_INTERRUPTED = 3` in `signal_handler.py`
  (T03.07) — same module-local-constant pattern reused here.
- **Design spec** — `.dev/releases/current/cliEval/design-spec.md`
  §9 (summary layout) and §4 (exit codes).

## Out-of-scope items (forward references)

- The `AggregatedRunReport` class with four emitter methods
  (`to_markdown` / `to_yaml` / `to_json` / `to_junit`) — T03.13 /
  COMP-008. This module is the file-emitting layer the class sits on
  top of; `to_yaml` is a class-only concern (this task does not emit
  YAML).
- The CLI dispatcher that catches `ReporterContractViolation` and
  exits 2 — Phase 4 (commands wiring).
- TEST-007 schema-fidelity round-trip across recorded summary fixtures
  — T04.17. This task only validates the writer's output for in-line
  fixtures.
- JUnit XSD validation (the optional emitter is best-effort against
  the de-facto JUnit shape, not a formal XSD compliance test).
