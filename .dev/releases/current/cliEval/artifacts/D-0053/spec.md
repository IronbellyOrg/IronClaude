# D-0053 — `summary.schema.json` contract spec

**Task:** T03.10 (Phase 3, Roadmap DM-012 / R-053)
**Module:** `src/superclaude/cli/eval/schemas/summary.schema.json`
**Loader:** `src/superclaude/cli/eval/schemas/__init__.py::load_summary_schema`
**Tests:** `tests/cli/eval/test_summary_schema.py` (17 tests, all passing)
**Status:** Implemented 2026-05-20

## Authoritative producers & consumers

| Role          | Module / Function                                                                        |
|---------------|------------------------------------------------------------------------------------------|
| Producer      | `superclaude.cli.eval.models.RunSummary.to_dict()` (T03.09 / DM-004)                     |
| Writer        | `write_aggregated_report(summary, output_dir)` (T03.11 / FR-RPT1) — emits `summary.json` |
| Schema loader | `superclaude.cli.eval.schemas.load_summary_schema()` (this task / T03.10)                |
| Fidelity test | TEST-007 (T04.17) — round-trip + schema-validation harness                               |
| Reporter      | `Reporter.to_json()` (T03.13 / COMP-008) — wraps the writer                              |

## Schema metadata

| Field        | Value                                                |
|--------------|------------------------------------------------------|
| `$schema`    | `https://json-schema.org/draft/2020-12/schema`       |
| `$id`        | `https://superclaude.dev/cliEval/summary.schema.json`|
| Draft        | 2020-12                                              |
| Sibling      | `suite.schema.json` (DM-011 / T01.02) — same draft   |

## Top-level required field set (9 — T03.10 acceptance)

| # | Field              | JSON Type       | Constraint / Notes |
|---|--------------------|------------------|--------------------|
| 1 | `run_id`           | `string`         | `minLength: 1` — opaque orchestrator-stamped identifier. |
| 2 | `started_at`       | `string`         | `minLength: 1` — ISO 8601 wall-clock timestamp. |
| 3 | `duration_sec`     | `number`         | `minimum: 0` — wall-clock seconds, sub-millisecond resolution. |
| 4 | `suite`            | `string`         | `minLength: 1` — manifest path / suite identifier. |
| 5 | `manifest_version` | `string`         | `minLength: 1` — semantic version stamped on the manifest. |
| 6 | `parallel`         | `integer`        | `minimum: 1, maximum: 15` — post-clamp concurrency. |
| 7 | `counts`           | `object`         | `$ref` → `#/$defs/runCounts` (5 required sub-fields). |
| 8 | `totals`           | `object`         | `$ref` → `#/$defs/runTotals` (6 required sub-fields). |
| 9 | `evals`            | `array`          | Items `$ref` → `#/$defs/evalOutcome`. FR-RPT1 enforces `len(evals)==counts.expanded_n_prime` outside the schema. |

## Optional top-level fields (allowed, not required)

| Field         | Type    | Rationale |
|---------------|---------|-----------|
| `finished_at` | `string`| May be `""` for partial summaries written on SIGINT before the orchestrator completed. |
| `artifacts`   | `object`| Orchestrator-emitted artefact-name → path map. Empty map is the default. |

`additionalProperties: true` at the top level so future field additions (e.g.
DM-012 grows a 10th field) do not invalidate existing summaries — the schema
declares *required shape*, not a closed dictionary.

## `counts` sub-field schema (DM-012, 5 required)

| # | Field                              | JSON Type | Constraint |
|---|------------------------------------|-----------|------------|
| 1 | `manifest_n`                       | `integer` | `minimum: 0` |
| 2 | `expanded_n_prime`                 | `integer` | `minimum: 0` |
| 3 | `kept_k`                           | `integer` | `minimum: 0` |
| 4 | `skipped_s`                        | `integer` | `minimum: 0` |
| 5 | `kept_plus_skipped_equals_n_prime` | `boolean` | DM-012 flag (mirrors math). |

`additionalProperties: false` — the counts dictionary is closed; an
orchestrator that smuggles in extra keys is treated as a contract bug.

## `totals` sub-field schema (DM-012, 6 required)

| # | Field         | JSON Type | Constraint |
|---|---------------|-----------|------------|
| 1 | `passed`      | `integer` | `minimum: 0` |
| 2 | `failed`      | `integer` | `minimum: 0` |
| 3 | `skipped`     | `integer` | `minimum: 0` |
| 4 | `errored`     | `integer` | `minimum: 0` |
| 5 | `interrupted` | `integer` | `minimum: 0` |
| 6 | `timeout`     | `integer` | `minimum: 0` |

`additionalProperties: false` — closed tally dictionary.

## `evals[]` item schema (DM-001 EvalOutcome serialisation, 9 required)

`eval_id, title, status, duration_sec, expects, skip_reason, skip_flag_triggered, artifacts, error_class`

`additionalProperties: false`. Field order mirrors `_EVAL_OUTCOME_FIELDS`
(T03.01) verbatim so a reviewer can `git diff` the schema against the
runtime constant line by line.

## `status` enum (DM-001)

```
["PASS", "FAIL", "ERRORED", "TIMEOUT", "INTERRUPTED", "SKIPPED", "XFAIL", "XPASS"]
```

Order matches `superclaude.cli.eval.models.EVAL_STATUSES` verbatim;
`test_schema_status_enum_matches_runtime_model` enforces drift-detection.

## Nested defs

* `#/$defs/expectResult` — DM-009 ExpectResult serialisation
  (`name, passed, message, details, duration_sec, failure`); `failure`
  is `oneOf` `null | expectFailure`.
* `#/$defs/expectFailure` — DM-005 ExpectFailure serialisation
  (`eval_id, expect_id, expect_name, expected, actual, message, artifact_ref, traceback`).
  `expected` / `actual` are schema-free (any JSON value).

## Loader contract

`superclaude.cli.eval.schemas.load_summary_schema()` returns a freshly
decoded mapping per call. Implemented via `importlib.resources` so the
schema is discoverable from editable installs and built wheels alike.
Callers are free to mutate the returned dict; the on-disk file is
never touched.

## Fixtures

| Fixture                                                                    | Purpose                                                                |
|----------------------------------------------------------------------------|------------------------------------------------------------------------|
| `tests/cli/eval/fixtures/summary_schema/valid_minimal.json`                | Empty-run baseline (zero evals, all-zero counts).                      |
| `tests/cli/eval/fixtures/summary_schema/valid_full.json`                   | Reference shape from §9 design-spec (PASS + SKIPPED).                  |
| `tests/cli/eval/fixtures/summary_schema/invalid_missing_required.json`    | Drops `evals` → validation MUST fail.                                  |
| `tests/cli/eval/fixtures/summary_schema/invalid_bad_status.json`          | `status: "BOGUS"` → enum violation.                                    |
| `tests/cli/eval/fixtures/summary_schema/invalid_missing_counts_subfield.json` | Drops `kept_plus_skipped_equals_n_prime` → required violation.       |

## Acceptance coverage matrix

| Acceptance criterion                                                                                          | Test(s)                                                                       |
|---------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| File `src/superclaude/cli/eval/schemas/summary.schema.json` exists                                            | `test_schema_file_exists_under_canonical_path`                                |
| Validates the reference RunSummary serialization                                                              | `test_run_summary_to_dict_validates_for_empty_run`, `..._with_pass_outcome`, `..._partial_summary_path` |
| Required fields: `run_id,started_at,duration_sec,suite,manifest_version,parallel,counts,totals,evals`         | `test_schema_top_level_required_fields`                                       |
| `counts` requires the 5 sub-fields from DM-012                                                                | `test_schema_counts_required_subfields`                                       |
| `totals` requires `passed,failed,skipped,errored,interrupted,timeout`                                         | `test_schema_totals_required_subfields`                                       |
| Negative case: invalid summary fixture fails validation                                                       | `test_invalid_missing_required_top_level_field_fails`, `..._bad_status_fails`, `..._missing_counts_subfield_fails` |

## Out-of-scope / forward references

* FR-RPT1 `write_aggregated_report` + `ReporterContractViolation` (exit 2)
  on N'-vs-K mismatch — T03.11. Schema is shape-only; the invariant
  is enforced by the writer.
* COMP-008 Reporter emitters (`to_markdown` / `to_yaml` / `to_json` /
  `to_junit`) — T03.13.
* TEST-007 schema-fidelity harness — T04.17. Drives the round-trip
  `RunSummary` → `to_dict()` → `summary.schema.json` validation across
  a representative suite of recorded runs.
