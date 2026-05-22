# D-0055 — COMP-008 Reporter / AggregatedRunReport contract spec

**Task:** T03.13 (Phase 3, Roadmap R-055 / COMP-008)
**Module:** `src/superclaude/cli/eval/reporter.py`
**Tests:** `tests/cli/eval/test_reporter.py` (25 tests, all passing)
**Status:** Implemented 2026-05-20

## Purpose

COMP-008 is the class-shaped Reporter surface declared by design-spec
§9. It wraps a `RunSummary` (T03.09 / DM-004) and exposes the four
canonical emitter methods (`to_markdown`, `to_yaml`, `to_json`,
`to_junit`) plus an opt-in multi-artefact writer.

Where T03.11 / D-0054 (`run_report.py`) is the file-emitting layer
behind FR-RPT1, T03.13 / D-0055 is the OO surface callers — CLI
dispatcher, downstream tooling — use to pick one emitter at a time or
to write the standard triplet to disk.

## Public surface

| Symbol                                              | Kind        | Purpose                                                                                  |
|-----------------------------------------------------|-------------|------------------------------------------------------------------------------------------|
| `Reporter`                                          | dataclass   | Frozen wrapper around a `RunSummary`. Stores `summary` and `emit_junit` flag.            |
| `Reporter.to_markdown() -> str`                     | method      | Returns the `summary.md` body (delegates to `render_summary_markdown`).                  |
| `Reporter.to_yaml() -> str`                         | method      | Returns the YAML rendering of `summary.to_dict()` (delegates to `render_summary_yaml`).  |
| `Reporter.to_json() -> str`                         | method      | Returns the canonical `summary.json` payload (delegates to `render_summary_json`).       |
| `Reporter.to_junit() -> str`                        | method      | Returns the JUnit XML payload (delegates to `render_junit_xml`).                         |
| `Reporter.write(output_dir) -> Mapping[str, Path]`  | method      | Writes the artefact set under `output_dir`. JUnit feature-gated by `emit_junit`.         |
| `AggregatedRunReport`                               | alias       | `AggregatedRunReport is Reporter`. Roadmap row uses both names interchangeably.          |
| `render_summary_yaml(summary) -> str`               | function    | Module-level YAML renderer the class delegates to.                                       |

The exception (`ReporterContractViolation`) and exit-code constant
(`REPORTER_CONTRACT_VIOLATION_EXIT_CODE = 2`) continue to live in
`run_report.py`; this module re-exports them for convenience but they
remain the single source of truth.

## Assertion guard wiring

Every emitter method delegates to the corresponding function in
`run_report.py`. Those functions all call `_check_invariant(summary)`
before doing any rendering work:

```
expected = summary.counts.expanded_n_prime
actual   = len(summary.evals)
if expected != actual:
    raise ReporterContractViolation(expected=expected, actual=actual,
                                    run_id=summary.run_id)
```

The `Reporter.write` method calls `_check_invariant(self.summary)`
*before* `mkdir`, mirroring the behaviour of
`write_aggregated_report`. The acceptance criterion "the assertion
guard fires before any emitter writes output on mismatch" therefore
holds across all four methods *and* across `write()`.

The same `ReporterContractViolation` exception class is raised by both
modules; callers map it to exit code 2
(`REPORTER_CONTRACT_VIOLATION_EXIT_CODE`).

## Feature gating of JUnit XML

The acceptance criterion "JUnit XML emitter is feature-gated and only
emitted when explicitly requested" is satisfied by two layers:

1. **`Reporter.write` default skips `junit.xml`.** The `emit_junit`
   dataclass field defaults to `False`. When `False`, `write()` writes
   only `summary.md`, `summary.json`, and `summary.yaml`. Callers must
   construct `Reporter(summary, emit_junit=True)` to opt in.
2. **`Reporter.to_junit()` is the explicit request.** Calling
   `to_junit()` directly always returns the XML body — invoking the
   method *is* the explicit request the gate language refers to.
   `write()` accepts the flag because some callers (CLI dispatcher,
   recorded-run replays) want a single call that emits the whole
   artefact set without composing the four `to_*` methods manually.

## YAML emitter shape

`render_summary_yaml(summary)`:

* Calls `_check_invariant(summary)` first (mismatch → raises before any
  serialisation).
* Calls `summary.to_dict()` to get the DM-004 payload.
* Emits the YAML via `yaml.safe_dump(payload, sort_keys=False,
  default_flow_style=False, allow_unicode=True)`.
* Returns the resulting string.

`sort_keys=False` preserves the DM-004 field declaration order;
`default_flow_style=False` produces canonical block style (one key per
line). The output is byte-stable for a given input because:

* `RunSummary` is a frozen dataclass; `to_dict()` is deterministic.
* `yaml.safe_dump` with the chosen flags is deterministic on the same
  Python value.

`yaml.safe_load(body) == summary.to_dict()` round-trips for every
shape the tests cover (PASS, SKIPPED, FAIL, INTERRUPTED partial).

## Byte stability across all four emitters

| Emitter      | Mechanism                                                                                  |
|--------------|--------------------------------------------------------------------------------------------|
| Markdown     | `render_summary_markdown` iterates `summary.evals` in tuple order; formatting is stable.   |
| YAML         | `yaml.safe_dump(sort_keys=False, default_flow_style=False)` on a deterministic mapping.    |
| JSON         | `json.dumps(payload, indent=2, ensure_ascii=False)` on a deterministic mapping.            |
| JUnit XML    | `xml.etree.ElementTree.tostring` over a tuple-ordered traversal with fixed attribute set.  |

Verified by hashing two independent renderings of the same summary
(see `test_to_*_is_byte_stable`).

## Frozen-dataclass guarantee

`Reporter` is `@dataclass(frozen=True)` so `reporter.summary = ...`
raises `dataclasses.FrozenInstanceError`. This is the same guarantee
`RunSummary` itself carries — Reporter consumers cannot swap the
underlying summary mid-render, so byte-stability across emitter calls
is structurally enforced (not just by convention).

## Out-of-scope / forward references

* CLI dispatcher mapping `ReporterContractViolation` to exit code 2 —
  Phase 4 commands wiring.
* `RunOrchestrator` constructing the `RunSummary` and handing it to
  `Reporter` — T03.15 / COMP-003.
* `AggregatedPhaseReport` probe (read-only pin of the sprint
  executor's shape reference) — T03.14 / COMP-015 sibling task.
* Disk-budget poller + reporter coupling — T03.19 / NFR-PERF4.

## Acceptance criteria coverage

| Acceptance criterion                                                                                            | Test(s)                                                                                                       |
|-----------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `Reporter` exposes `to_markdown/yaml/json/junit`                                                                | `test_reporter_exposes_four_emitter_methods`                                                                  |
| Assertion guard fires before any emitter writes output on mismatch                                              | `test_to_markdown_raises_on_mismatch`, `test_to_yaml_raises_on_mismatch`, `test_to_json_raises_on_mismatch`, `test_to_junit_raises_on_mismatch`, `test_write_raises_before_any_file_is_written` |
| All four emitter outputs byte-stable for a given `RunSummary` (verified by hashing)                              | `test_to_markdown_is_byte_stable`, `test_to_yaml_is_byte_stable`, `test_to_json_is_byte_stable`, `test_to_junit_is_byte_stable` |
| JUnit XML emitter is feature-gated and only emitted when explicitly requested                                   | `test_write_default_skips_junit_xml`, `test_write_emits_junit_when_flag_set`, `test_to_junit_callable_regardless_of_flag` |
| Spec doc documents the emitter contract                                                                         | This file                                                                                                     |
| Class delegate outputs match module-level renderer outputs                                                      | `test_to_markdown_matches_module_renderer`, `test_to_json_matches_module_renderer`, `test_to_junit_matches_module_renderer` |
| `AggregatedRunReport` alias resolves to `Reporter`                                                              | `test_aggregated_run_report_is_reporter_alias`                                                                |
| YAML round-trips to `summary.to_dict()` and preserves DM-004 field order                                        | `test_to_yaml_round_trips_to_summary_dict`, `test_to_yaml_preserves_dm_004_field_order`                       |
| Partial-summary path (SIGINT — `finished_at=""` with INTERRUPTED row) renders cleanly                           | `test_to_yaml_handles_partial_summary`                                                                        |
| `Reporter` is frozen (consumer cannot swap the underlying summary)                                              | `test_reporter_is_frozen`                                                                                     |
