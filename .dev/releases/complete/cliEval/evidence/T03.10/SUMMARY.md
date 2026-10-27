# T03.10 — Evidence summary

**Task:** Define DM-012 `summary.json` schema (R-053 / D-0053).
**Date:** 2026-05-20

## Deliverable

- `src/superclaude/cli/eval/schemas/summary.schema.json` — Draft 2020-12
  schema for `summary.json`.
- `src/superclaude/cli/eval/schemas/__init__.py` — `load_summary_schema()`
  loader using `importlib.resources` (wheel-safe).

## Tests

`tests/cli/eval/test_summary_schema.py` — **17 tests, all passing**
(see `test-output.txt`). Full eval suite regression in
`pytest-regression.txt`: **866 passed, 1 failed** — the single failure
(`test_ruff_flags_synthetic_anthropic_import_under_cli_eval`) is a
pre-existing failure unrelated to T03.10 (ruff TID251 ban-api rule
drift owned by T02.19; my changes do not touch
`_t02_19_ban_probe.py`, `pyproject.toml` ruff config, or
`test_claude_process_adapter.py`).

## Fixtures

| File                                          | Schema valid? | Purpose                                                    |
|-----------------------------------------------|---------------|------------------------------------------------------------|
| `valid_minimal.json`                         | ✅            | Empty-run baseline (zero evals, all-zero counts).          |
| `valid_full.json`                            | ✅            | Reference shape from design-spec §9 (PASS + SKIPPED).      |
| `invalid_missing_required.json`             | ❌            | Drops `evals` — required top-level field missing.          |
| `invalid_bad_status.json`                   | ❌            | `status: "BOGUS"` — enum violation.                        |
| `invalid_missing_counts_subfield.json`     | ❌            | Drops `kept_plus_skipped_equals_n_prime` — required miss. |

## Acceptance criteria coverage

| Criterion                                                                            | Covered by                                                                                                              |
|--------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| File `summary.schema.json` exists at canonical path                                   | `test_schema_file_exists_under_canonical_path`                                                                          |
| Validates the reference RunSummary serialization                                     | `test_run_summary_to_dict_validates_for_empty_run` + `..._with_pass_outcome` + `..._partial_summary_path` (3 tests)     |
| Required fields enumerated: `run_id,started_at,duration_sec,suite,manifest_version,parallel,counts,totals,evals` | `test_schema_top_level_required_fields`                                                                                 |
| `counts` requires the 5 DM-012 sub-fields                                            | `test_schema_counts_required_subfields`                                                                                 |
| `totals` requires `passed,failed,skipped,errored,interrupted,timeout`                | `test_schema_totals_required_subfields`                                                                                 |
| Spec doc records schema contract                                                     | `TASKLIST_ROOT/artifacts/D-0053/spec.md`                                                                                |

## Manual validation

`jsonschema` (4.26.0) Draft 2020-12 validator was used in-test to
validate three programmatically-constructed `RunSummary.to_dict()`
payloads (empty-run, PASS outcome, partial-summary-on-SIGINT). All
pass; invalid fixtures raise `ValidationError` with informative
messages.

## Artifacts written

- `src/superclaude/cli/eval/schemas/__init__.py`
- `src/superclaude/cli/eval/schemas/summary.schema.json`
- `tests/cli/eval/test_summary_schema.py`
- `tests/cli/eval/fixtures/summary_schema/{valid_minimal,valid_full,invalid_missing_required,invalid_bad_status,invalid_missing_counts_subfield}.json`
- `.dev/releases/current/cliEval/artifacts/D-0053/{spec.md,notes.md,evidence.md}`
- `.dev/releases/current/cliEval/evidence/T03.10/{SUMMARY.md,test-output.txt,pytest-regression.txt}`
