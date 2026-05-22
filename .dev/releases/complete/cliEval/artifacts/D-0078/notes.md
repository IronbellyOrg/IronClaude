# D-0078 — Implementation notes

## Module-level decisions

* **Self-contained fixtures.** `test_reporter_contract.py` does not
  import helpers from `test_run_report.py`. The contract this module
  pins is the contract every downstream consumer reads; cross-importing
  helpers would couple the contract test to the writer's own test
  scaffolding, and a future refactor of the writer's tests could
  silently lose coverage here. The duplication is small (≈30 lines of
  `_pass` / `_skipped` / `_fail` / `_summary` builders) and the
  decoupling is worth it.

* **Two emitter surfaces tested.** Scenario 3 (mismatch → raise) is
  asserted against both the class-shaped `Reporter` wrapper
  (`to_markdown / to_json / to_yaml / to_junit / write`) *and* the
  underlying module-level renderers (`render_summary_markdown /
  render_summary_json / render_junit_xml / write_aggregated_report`).
  The class delegates to the renderers, but the spec language ("guard
  fires before any emitter writes output") covers both surfaces, so the
  test asserts both.

* **Schema fidelity tested on both bytes.** Scenario 4 validates the
  in-memory string from `Reporter.to_json()` *and* the bytes on disk
  from `Reporter.write(...)["summary.json"]`. The two payloads also
  compare equal, so a future refactor that adds a transformation step
  between the renderer and the file write fails this test loudly.

## Exit-code constant

`REPORTER_CONTRACT_VIOLATION_EXIT_CODE = 2` lives in
`run_report.py`. The CLI dispatcher does not yet catch the exception
and exit with this constant — that wiring lands in T04.10 / T04.19. At
the library boundary this module pins:

1. The constant value (`== 2`).
2. The exception type (`ReporterContractViolation`).
3. The "no artefact written before raise" property (no partial
   `summary.md` / `summary.json` / `summary.yaml` / `junit.xml`).

The TEST-008 module (T04.19) will pin the end-to-end process exit-code
through `subprocess.run` against `superclaude eval run`. Together the
two modules cover the contract at both layers.

## Distinct-row coverage

The Scenario-4 fixture mixes PASS / SKIPPED / FAIL / ERRORED outcomes
so the `oneOf` branch the schema declares for `evals[].expects[].failure`
and the `null`-or-string branches on `skip_reason` /
`skip_flag_triggered` / `error_class` are all exercised. INTERRUPTED /
TIMEOUT / XFAIL / XPASS rows are covered by `test_run_report.py` and
deliberately not duplicated here — this module's purpose is the
four-scenario contract, not exhaustive status taxonomy coverage.

## Imports

The module imports from three layers, mirroring the contract surface
the Reporter exposes:

```
superclaude.cli.eval.models          # RunSummary, RunCounts, RunTotals,
                                      # EvalOutcome, ExpectResult
superclaude.cli.eval.reporter        # Reporter (COMP-008 wrapper)
superclaude.cli.eval.run_report      # module-level renderers + writer +
                                      # REPORTER_CONTRACT_VIOLATION_EXIT_CODE
superclaude.cli.eval.schemas         # load_summary_schema (DM-012)
```

`jsonschema.Draft202012Validator` is the validator class — same one
`test_run_report.py` uses for its parallel schema-fidelity check.

## Hand-off

* **TEST-008 (T04.19)** will pin the end-to-end process exit code
  through `subprocess.run` against `superclaude eval run`.
* **T04.10** will wire the CLI dispatcher to catch
  `ReporterContractViolation` and exit with
  `REPORTER_CONTRACT_VIOLATION_EXIT_CODE`. The constant + exception
  type contract this module pins is the dispatcher's input.
* **CP-P04-T13-T17** checkpoint will include this test module in its
  exit-criteria pytest invocation.
