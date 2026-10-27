# D-0053 — Evidence

**Task:** T03.10 (Phase 3, Roadmap DM-012 / R-053)
**Date:** 2026-05-20

## Test results

```
tests/cli/eval/test_summary_schema.py
  17 passed in 0.16s
```

Full per-test log: `TASKLIST_ROOT/evidence/T03.10/test-output.txt`.

## Per-test coverage

| #  | Test                                                              | What it pins                                                                                          |
|----|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| 1  | `test_schema_file_exists_under_canonical_path`                    | File at `src/superclaude/cli/eval/schemas/summary.schema.json`.                                       |
| 2  | `test_schema_is_draft_2020_12`                                    | `$schema` URI + `Draft202012Validator.check_schema()` accepts the document.                           |
| 3  | `test_schema_top_level_required_fields`                          | Required-field list matches T03.10 acceptance verbatim.                                               |
| 4  | `test_schema_counts_required_subfields`                          | `counts.required` matches DM-012 5-field list.                                                        |
| 5  | `test_schema_totals_required_subfields`                          | `totals.required` matches DM-012 6-field list.                                                        |
| 6  | `test_schema_status_enum_matches_runtime_model`                  | `status` enum equals `EVAL_STATUSES` tuple from `models.py`.                                          |
| 7  | `test_valid_minimal_fixture_validates`                           | Empty-run fixture validates.                                                                          |
| 8  | `test_valid_full_fixture_validates`                              | Reference design-spec §9 fixture validates.                                                           |
| 9  | `test_invalid_missing_required_top_level_field_fails`           | Removing `evals` triggers `ValidationError`.                                                          |
| 10 | `test_invalid_bad_status_fails`                                  | `status: "BOGUS"` triggers `ValidationError`.                                                         |
| 11 | `test_invalid_missing_counts_subfield_fails`                    | Removing `kept_plus_skipped_equals_n_prime` triggers `ValidationError`.                              |
| 12 | `test_run_summary_to_dict_validates_for_empty_run`               | `RunSummary.to_dict()` for zero-eval run validates.                                                   |
| 13 | `test_run_summary_to_dict_validates_with_pass_outcome`           | `RunSummary.to_dict()` carrying a PASS EvalOutcome validates.                                         |
| 14 | `test_run_summary_to_dict_validates_partial_summary_path`        | Partial summary (`finished_at=""`, `flag=False`, mismatched counts) still validates (FR-RPT1 guard is downstream). |
| 15 | `test_schema_parallel_clamped_range`                             | `parallel=16` rejected by schema (`maximum: 15`).                                                     |
| 16 | `test_schema_parallel_lower_bound`                               | `parallel=0` rejected by schema (`minimum: 1`).                                                       |
| 17 | `test_load_summary_schema_returns_fresh_mapping_each_call`       | `load_summary_schema()` returns a fresh mapping each call; mutation does not affect later reads.      |

## Regression

`uv run pytest tests/cli/eval/ -q` — 866 passed, 1 pre-existing failure
unrelated to T03.10 (`test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
fails because the ruff TID251 ban-api rule for the T02.19 probe trips
on `I001` first; that test and its source were not touched by T03.10).
Log: `TASKLIST_ROOT/evidence/T03.10/pytest-regression.txt`.

## Reference fixtures (all in `tests/cli/eval/fixtures/summary_schema/`)

| Fixture                                       | Validates? | Drives test                                                |
|-----------------------------------------------|------------|------------------------------------------------------------|
| `valid_minimal.json`                          | ✅         | #7                                                          |
| `valid_full.json`                             | ✅         | #8                                                          |
| `invalid_missing_required.json`              | ❌         | #9                                                          |
| `invalid_bad_status.json`                    | ❌         | #10                                                         |
| `invalid_missing_counts_subfield.json`      | ❌         | #11                                                         |

## Manual validation against the spec snippet

The §9 reference JSON from `design-spec.md` was transcribed verbatim
into `valid_full.json` (with field names normalised to the DM-009
ExpectResult shape — `evidence` → `message + details`). Validation
under `jsonschema` 4.26.0 passes; test #8 enforces this in CI.

## Dependencies and downstream

- **Upstream:** T03.09 (`RunSummary` / `RunCounts` / `RunTotals`).
- **Downstream:** T03.11 (FR-RPT1 writer — emits `summary.json` matching
  this schema), T03.13 (Reporter `to_json` / `to_yaml`), T04.17 (TEST-007
  schema fidelity).
