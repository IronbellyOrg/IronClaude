"""Tests for ``summary.schema.json`` (Roadmap DM-012 / Deliverable D-0053).

The schema is the canonical machine-readable contract for ``summary.json``
emitted by the cliEval Reporter. These tests pin:

* The required top-level field set (9 fields enumerated by T03.10
  acceptance criteria).
* The required ``counts`` sub-field set (5 fields, DM-012).
* The required ``totals`` sub-field set (6 fields, DM-012).
* The ``status`` enum matches ``EVAL_STATUSES`` from the runtime model.
* Reference fixtures: a minimal-valid and a full-valid summary both
  validate against the schema.
* Invalid fixtures (missing required field, bad status enum, missing
  counts sub-field) fail validation with a deterministic shape.
* ``RunSummary.to_dict()`` output (T03.09) validates against the schema
  for representative configurations (PASS-only, SKIPPED, partial-summary
  with `kept_plus_skipped_equals_n_prime=False`).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from superclaude.cli.eval.models import (
    EVAL_STATUSES,
    EvalOutcome,
    RunCounts,
    RunSummary,
    RunTotals,
)
from superclaude.cli.eval.schemas import (
    SUMMARY_SCHEMA_FILENAME,
    load_summary_schema,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "summary_schema"
SCHEMA_PATH = (
    Path(__file__).parents[3]
    / "src"
    / "superclaude"
    / "cli"
    / "eval"
    / "schemas"
    / SUMMARY_SCHEMA_FILENAME
)


@pytest.fixture(scope="module")
def schema() -> dict:
    """Return the parsed schema document loaded via importlib.resources."""

    return dict(load_summary_schema())


@pytest.fixture(scope="module")
def validator(schema: dict) -> Draft202012Validator:
    """Return a Draft 2020-12 validator bound to the schema."""

    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _load_fixture(name: str) -> dict:
    with (FIXTURE_DIR / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def test_schema_file_exists_under_canonical_path() -> None:
    """Acceptance: file lives at the path the roadmap names."""

    assert SCHEMA_PATH.is_file(), SCHEMA_PATH


def test_schema_is_draft_2020_12(schema: dict) -> None:
    """Acceptance: schema is Draft 2020-12 (decided in T03.10 PLANNING)."""

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    Draft202012Validator.check_schema(schema)


def test_schema_top_level_required_fields(schema: dict) -> None:
    """Acceptance: required fields are exactly the 9 enumerated in T03.10."""

    expected = [
        "run_id",
        "started_at",
        "duration_sec",
        "suite",
        "manifest_version",
        "parallel",
        "counts",
        "totals",
        "evals",
    ]
    assert schema["required"] == expected


def test_schema_counts_required_subfields(schema: dict) -> None:
    """Acceptance: counts requires the 5 sub-fields from DM-012."""

    expected = [
        "manifest_n",
        "expanded_n_prime",
        "kept_k",
        "skipped_s",
        "kept_plus_skipped_equals_n_prime",
    ]
    assert schema["$defs"]["runCounts"]["required"] == expected


def test_schema_totals_required_subfields(schema: dict) -> None:
    """Acceptance: totals requires the 6 sub-fields from DM-012."""

    expected = [
        "passed",
        "failed",
        "skipped",
        "errored",
        "interrupted",
        "timeout",
    ]
    assert schema["$defs"]["runTotals"]["required"] == expected


def test_schema_status_enum_matches_runtime_model(schema: dict) -> None:
    """Acceptance: status enum mirrors DM-001 EVAL_STATUSES verbatim."""

    enum = schema["$defs"]["evalStatus"]["enum"]
    # Order matters: the wire enum is the authoritative literal set, and
    # consumers (Reporter, JUnit emitter) iterate it in declaration order.
    assert tuple(enum) == EVAL_STATUSES


def test_valid_minimal_fixture_validates(validator: Draft202012Validator) -> None:
    """A minimal zero-eval summary is valid."""

    payload = _load_fixture("valid_minimal.json")
    validator.validate(payload)


def test_valid_full_fixture_validates(validator: Draft202012Validator) -> None:
    """The full reference fixture (PASS + SKIPPED) validates."""

    payload = _load_fixture("valid_full.json")
    validator.validate(payload)


def test_invalid_missing_required_top_level_field_fails(
    validator: Draft202012Validator,
) -> None:
    """Missing top-level required field (`evals`) fails validation."""

    payload = _load_fixture("invalid_missing_required.json")
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(payload)
    assert "evals" in str(exc_info.value)


def test_invalid_bad_status_fails(validator: Draft202012Validator) -> None:
    """A status outside EVAL_STATUSES fails validation."""

    payload = _load_fixture("invalid_bad_status.json")
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(payload)
    assert "BOGUS" in str(exc_info.value)


def test_invalid_missing_counts_subfield_fails(
    validator: Draft202012Validator,
) -> None:
    """Missing counts sub-field (`kept_plus_skipped_equals_n_prime`) fails."""

    payload = _load_fixture("invalid_missing_counts_subfield.json")
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(payload)
    assert "kept_plus_skipped_equals_n_prime" in str(exc_info.value)


def test_run_summary_to_dict_validates_for_empty_run(
    validator: Draft202012Validator,
) -> None:
    """RunSummary.to_dict() validates for an empty run (counts all zero)."""

    summary = RunSummary(
        run_id="run-empty",
        started_at="2026-05-20T12:00:00Z",
        finished_at="2026-05-20T12:00:01Z",
        duration_sec=1.0,
        suite="tests/fixtures/empty.yaml",
        manifest_version="1.0",
        parallel=1,
        counts=RunCounts(
            manifest_n=0,
            expanded_n_prime=0,
            kept_k=0,
            skipped_s=0,
            kept_plus_skipped_equals_n_prime=True,
        ),
        totals=RunTotals(),
    )
    validator.validate(summary.to_dict())


def test_run_summary_to_dict_validates_with_pass_outcome(
    validator: Draft202012Validator,
) -> None:
    """RunSummary.to_dict() validates when carrying a PASS EvalOutcome."""

    outcome = EvalOutcome(
        eval_id="E1",
        title="sticky lifecycle",
        status="PASS",
        duration_sec=8.3,
    )
    summary = RunSummary(
        run_id="run-pass",
        started_at="2026-05-20T12:00:00Z",
        finished_at="2026-05-20T12:00:10Z",
        duration_sec=10.0,
        suite="tests/fixtures/one.yaml",
        manifest_version="1.0",
        parallel=1,
        counts=RunCounts(
            manifest_n=1,
            expanded_n_prime=1,
            kept_k=1,
            skipped_s=0,
            kept_plus_skipped_equals_n_prime=True,
        ),
        totals=RunTotals(passed=1),
        evals=(outcome,),
    )
    validator.validate(summary.to_dict())


def test_run_summary_to_dict_validates_partial_summary_path(
    validator: Draft202012Validator,
) -> None:
    """Partial summary (SIGINT) with `flag=False` and mismatch validates.

    Schema documents shape only; the FR-RPT1 invariant guard fires
    downstream and is the canonical mismatch-detection path.
    """

    interrupted = EvalOutcome(
        eval_id="E1",
        title="interrupted run",
        status="INTERRUPTED",
        duration_sec=2.0,
    )
    summary = RunSummary(
        run_id="run-partial",
        started_at="2026-05-20T12:00:00Z",
        finished_at="",
        duration_sec=2.0,
        suite="tests/fixtures/one.yaml",
        manifest_version="1.0",
        parallel=1,
        counts=RunCounts(
            manifest_n=5,
            expanded_n_prime=5,
            kept_k=0,
            skipped_s=1,
            kept_plus_skipped_equals_n_prime=False,
        ),
        totals=RunTotals(interrupted=1),
        evals=(interrupted,),
    )
    validator.validate(summary.to_dict())


def test_schema_parallel_clamped_range(validator: Draft202012Validator) -> None:
    """`parallel=16` violates the [1,15] clamp encoded in the schema."""

    payload = _load_fixture("valid_minimal.json")
    payload["parallel"] = 16
    with pytest.raises(ValidationError):
        validator.validate(payload)


def test_schema_parallel_lower_bound(validator: Draft202012Validator) -> None:
    """`parallel=0` violates the [1,15] clamp encoded in the schema."""

    payload = _load_fixture("valid_minimal.json")
    payload["parallel"] = 0
    with pytest.raises(ValidationError):
        validator.validate(payload)


def test_load_summary_schema_returns_fresh_mapping_each_call() -> None:
    """`load_summary_schema()` returns a new dict the caller may mutate."""

    first = load_summary_schema()
    second = load_summary_schema()
    assert first == second
    assert first is not second
    first["title"] = "mutated"
    assert load_summary_schema()["title"] != "mutated"
