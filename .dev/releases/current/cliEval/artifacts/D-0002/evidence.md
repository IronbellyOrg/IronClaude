# D-0002 — evidence

## Verification command

```
uv run pytest tests/cli/eval/test_schema_load.py -v
```

## Result (2026-05-20)

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
configfile: pyproject.toml
collected 13 items

tests/cli/eval/test_schema_load.py::test_schema_file_exists_at_expected_path PASSED
tests/cli/eval/test_schema_load.py::test_schema_is_valid_json PASSED
tests/cli/eval/test_schema_load.py::test_schema_is_meta_valid_against_draft_2020_12 PASSED
tests/cli/eval/test_schema_load.py::test_schema_declares_dm011_required_fields PASSED
tests/cli/eval/test_schema_load.py::test_schema_rejects_unknown_top_level_keys PASSED
tests/cli/eval/test_schema_load.py::test_reference_manifest_validates_green PASSED
tests/cli/eval/test_schema_load.py::test_missing_required_field_is_rejected PASSED
tests/cli/eval/test_schema_load.py::test_unknown_top_level_key_is_rejected PASSED
tests/cli/eval/test_schema_load.py::test_parameterize_block_accepted_under_evals PASSED
tests/cli/eval/test_schema_load.py::test_eval_id_regex_rejects_traversal PASSED
tests/cli/eval/test_schema_load.py::test_eval_id_regex_rejects_template_tokens PASSED
tests/cli/eval/test_schema_load.py::test_parameterize_row_must_be_non_empty_mapping PASSED
tests/cli/eval/test_schema_load.py::test_failure_mode_enum_enforced PASSED

============================== 13 passed in 0.13s ==============================
```

Full log: `TASKLIST_ROOT/evidence/T01.02/pytest.log`.

## Manual sanity check

```
$ uv run python -c "import json; from superclaude.cli.eval.suites import SCHEMA_PATH; \
    from jsonschema import Draft202012Validator; \
    s=json.load(open(SCHEMA_PATH)); Draft202012Validator.check_schema(s); \
    print('meta-valid:', s['title'])"
meta-valid: cliEval suite manifest
```

## Acceptance-criteria coverage

| AC bullet (T01.02) | Test | Status |
|---|---|---|
| File `suite.schema.json` exists; schema dialect documented. | `test_schema_file_exists_at_expected_path`, `test_schema_is_valid_json`, `test_schema_is_meta_valid_against_draft_2020_12` | PASS |
| Schema declares the 7 DM-011 required fields and forbids unknown required keys. | `test_schema_declares_dm011_required_fields`, `test_schema_rejects_unknown_top_level_keys`, `test_unknown_top_level_key_is_rejected` | PASS |
| Reference fixture manifest validates green. | `test_reference_manifest_validates_green` | PASS |
| Fixture missing a required field is rejected. | `test_missing_required_field_is_rejected` | PASS |
| `spec.md` documents schema field rules and `parameterize` shape. | `TASKLIST_ROOT/artifacts/D-0002/spec.md` | PRESENT |

Additional belt-and-braces coverage (FR-SCH2 cross-link, parameterize
shape, failure_mode enum):

| Defence-in-depth bullet | Test | Status |
|---|---|---|
| `parameterize` block accepted under evals[]. | `test_parameterize_block_accepted_under_evals` | PASS |
| Eval id regex rejects traversal (`../etc`). | `test_eval_id_regex_rejects_traversal` | PASS |
| Eval id regex rejects template tokens (`E{session_id}`). | `test_eval_id_regex_rejects_template_tokens` | PASS |
| Parameterize row requires ≥1 substitution key. | `test_parameterize_row_must_be_non_empty_mapping` | PASS |
| `failure_mode` enum (hard/skip/xfail) enforced. | `test_failure_mode_enum_enforced` | PASS |

## Files produced

- `src/superclaude/cli/eval/suites/__init__.py`
- `src/superclaude/cli/eval/suites/suite.schema.json`
- `tests/cli/eval/fixtures/__init__.py`
- `tests/cli/eval/fixtures/valid_suite.yaml`
- `tests/cli/eval/fixtures/missing_name_suite.yaml`
- `tests/cli/eval/fixtures/unknown_top_level_suite.yaml`
- `tests/cli/eval/test_schema_load.py`
- `pyproject.toml` — added `jsonschema>=4.0.0` to `[project] dependencies`.
- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/notes.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`  (this file)
- `TASKLIST_ROOT/evidence/T01.02/pytest.log`
