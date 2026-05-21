"""Tests for ``src/superclaude/cli/eval/suites/suite.schema.json``.

Covers cliEval Phase 1 / Task T01.02 acceptance criteria (Deliverable D-0002):

* File exists and parses as JSON.
* Schema is meta-valid against its declared dialect (Draft 2020-12).
* Schema declares the 7 DM-011 required top-level fields and rejects unknown
  top-level keys.
* Reference fixture manifest validates green.
* Manifest missing a required field (e.g., ``name``) is rejected with an
  error message naming the offending field.
* ``parameterize`` rows under ``evals[]`` are accepted as arrays of
  key->value substitutions.
* Eval ids inside the schema honour the FR-SCH2 regex (template tokens in
  ``id:`` are rejected by jsonschema before T01.05's runtime guard runs).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from superclaude.cli.eval.suites import SCHEMA_PATH


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="module")
def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def validator(schema: dict) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _load_yaml(name: str) -> dict:
    return yaml.safe_load((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def test_schema_file_exists_at_expected_path() -> None:
    assert SCHEMA_PATH.exists()
    assert SCHEMA_PATH.name == "suite.schema.json"
    assert SCHEMA_PATH.parent.name == "suites"


def test_schema_is_valid_json(schema: dict) -> None:
    assert isinstance(schema, dict)
    assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"


def test_schema_is_meta_valid_against_draft_2020_12(schema: dict) -> None:
    Draft202012Validator.check_schema(schema)


def test_schema_declares_dm011_required_fields(schema: dict) -> None:
    assert set(schema["required"]) == {
        "name",
        "version",
        "description",
        "defaults",
        "required_binaries",
        "optional_capabilities",
        "evals",
    }


def test_schema_rejects_unknown_top_level_keys(schema: dict) -> None:
    assert schema.get("additionalProperties") is False


def test_reference_manifest_validates_green(validator: Draft202012Validator) -> None:
    manifest = _load_yaml("valid_suite.yaml")
    errors = sorted(validator.iter_errors(manifest), key=lambda e: list(e.path))
    assert errors == [], [str(e) for e in errors]


def test_missing_required_field_is_rejected(validator: Draft202012Validator) -> None:
    manifest = _load_yaml("missing_name_suite.yaml")
    errors = list(validator.iter_errors(manifest))
    assert errors, "expected jsonschema to reject manifest missing `name`"
    assert any("name" in err.message for err in errors), [e.message for e in errors]


def test_unknown_top_level_key_is_rejected(validator: Draft202012Validator) -> None:
    manifest = _load_yaml("unknown_top_level_suite.yaml")
    errors = list(validator.iter_errors(manifest))
    assert errors, "expected unknown top-level key to be rejected"
    assert any("mystery_field" in err.message for err in errors)


def test_parameterize_block_accepted_under_evals(validator: Draft202012Validator) -> None:
    manifest = _load_yaml("valid_suite.yaml")
    e2 = next(e for e in manifest["evals"] if e["id"] == "E2")
    assert "parameterize" in e2
    assert isinstance(e2["parameterize"], list) and e2["parameterize"]
    errors = list(validator.iter_errors(manifest))
    assert errors == [], [str(e) for e in errors]


def test_eval_id_regex_rejects_traversal(validator: Draft202012Validator) -> None:
    bad = {
        "name": "x",
        "version": "1.0",
        "description": "x",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [{"id": "../etc", "title": "traversal"}],
    }
    errors = list(validator.iter_errors(bad))
    assert errors, "FR-SCH2 regex must reject traversal ids at schema layer"


def test_eval_id_regex_rejects_template_tokens(validator: Draft202012Validator) -> None:
    bad = {
        "name": "x",
        "version": "1.0",
        "description": "x",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [{"id": "E{session_id}", "title": "template-id"}],
    }
    errors = list(validator.iter_errors(bad))
    assert errors, "schema must reject template tokens in id (T01.05 invariant)"


def test_parameterize_row_must_be_non_empty_mapping(validator: Draft202012Validator) -> None:
    bad = {
        "name": "x",
        "version": "1.0",
        "description": "x",
        "defaults": {},
        "required_binaries": [],
        "optional_capabilities": [],
        "evals": [
            {
                "id": "E1",
                "title": "empty parameterize row",
                "parameterize": [{}],
            }
        ],
    }
    errors = list(validator.iter_errors(bad))
    assert errors, "parameterize row must have at least one key"


def test_failure_mode_enum_enforced(validator: Draft202012Validator) -> None:
    bad = {
        "name": "x",
        "version": "1.0",
        "description": "x",
        "defaults": {},
        "required_binaries": [
            {"name": "claude", "failure_mode": "explode"}
        ],
        "optional_capabilities": [],
        "evals": [{"id": "E1", "title": "ok"}],
    }
    errors = list(validator.iter_errors(bad))
    assert errors, "failure_mode must be one of hard/skip/xfail"
