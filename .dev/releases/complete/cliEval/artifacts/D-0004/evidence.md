# D-0004 — evidence index

## Code

- `src/superclaude/cli/eval/loader.py` — `validate_manifest`,
  `SchemaError`, `SCHEMA_ERROR_EXIT_CODE`.
- `src/superclaude/cli/eval/__init__.py` — re-exports the three public
  symbols so callers can `from superclaude.cli.eval import …`.

## Tests

- `tests/cli/eval/test_schema_validate.py` — 14 tests covering positive
  path, schema violations, read/decode errors, FR-SCH1 no-FS-write
  invariant, exit-code mapping, and deterministic violation ordering.
- `tests/cli/eval/fixtures/invalid_eval_entry_suite.yaml` — negative
  fixture exercising violations nested inside `evals[0]`.

## Pytest run

See `TASKLIST_ROOT/evidence/T01.04/pytest.log` for the full run; summary
line: `14 passed in 0.23s` (also confirmed alongside T01.01–T01.03 tests
in a 33-passed aggregate run).

## Acceptance verification

| AC bullet | Evidence |
|---|---|
| Function raises `SchemaError` for missing required field with field-path in message. | `test_missing_required_field_raises_schema_error_with_field_name` (PASSED). |
| Valid fixture returns `list[EvalSpec]` matching `evals[]` length. | `test_valid_manifest_length_matches_evals_block` (PASSED). |
| No FS writes occur before validation succeeds. | `test_rejection_does_not_write_to_default_scratch_root` (PASSED). |
| `spec.md` records error → exit-code mapping. | `artifacts/D-0004/spec.md` "Error → exit-code mapping" table. |

## Cross-task links

- T01.02 schema (`D-0002`) — consumed verbatim via `SCHEMA_PATH`.
- T01.03 model (`D-0003`) — `EvalSpec.from_dict` is the projection target.
- T01.05 (`D-0005`) — adds the runtime `validate_eval_id` guard layered
  on top of `validate_manifest` by T01.07 (SuiteLoader).
- T01.13 (`D-0011`) — `eval doctor` consumes `validate_manifest` and the
  `SCHEMA_ERROR_EXIT_CODE` constant.
