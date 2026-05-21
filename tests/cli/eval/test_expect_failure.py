"""Tests for ``superclaude.cli.eval.models.ExpectFailure``.

Covers cliEval Phase 1 / Task T01.16 acceptance criteria (DM-005):

* Module exports a frozen ``ExpectFailure`` dataclass with the 8 fields
  ``eval_id, expect_id, expect_name, expected, actual, message,
  artifact_ref, traceback``.
* Mutation is rejected (``dataclasses.FrozenInstanceError``).
* ``to_dict()`` (and ``dataclasses.asdict``) yields a JSON-serialisable
  mapping per DM-005's implicit serialization requirement.
* Two instances built from identical arguments compare equal; one
  ``ExpectFailure`` entry per failing Expect (the per-failure-entry
  semantic is validated via construction patterns here; the
  one-per-failing-Expect integration assertion belongs to the Reporter
  test set / T03.13).

Cross-link: DM-009 ``ExpectResult`` (T01.15) consumes ``ExpectFailure``
via its optional ``failure`` field; this module locks the contract that
``dataclasses.asdict`` recurses cleanly across the pair.
"""

from __future__ import annotations

import dataclasses
import json

import pytest

from superclaude.cli.eval.models import ExpectFailure, ExpectResult


def test_expect_failure_has_required_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(ExpectFailure)]
    # Ordering matters: DM-005 lists eval_id, expect_id, expect_name,
    # expected, actual, message, artifact_ref, traceback in that order so
    # to_dict() output is stable across reporter snapshots.
    assert field_names == [
        "eval_id",
        "expect_id",
        "expect_name",
        "expected",
        "actual",
        "message",
        "artifact_ref",
        "traceback",
    ]


def test_expect_failure_is_frozen() -> None:
    failure = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        failure.actual = 0  # type: ignore[misc]


def test_expect_failure_defaults() -> None:
    failure = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
    )
    assert failure.message == ""
    assert failure.artifact_ref is None
    assert failure.traceback is None


def test_expect_failure_fully_populated() -> None:
    failure = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="file.contains_event[1]",
        expect_name="file.contains_event",
        expected={"event": "SessionStart"},
        actual={"event": "SessionEnd"},
        message="expected SessionStart, observed SessionEnd",
        artifact_ref="artifacts/ExampleEval1/diff-file.json",
        traceback=None,
    )
    assert failure.eval_id == "ExampleEval1"
    assert failure.artifact_ref == "artifacts/ExampleEval1/diff-file.json"
    assert failure.traceback is None


def test_expect_failure_traceback_captured_on_exception_path() -> None:
    # When an Expect raises rather than producing a clean diff, the
    # reporter captures the formatted traceback. Verify the field
    # accepts the string and round-trips via to_dict().
    failure = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="duration[0]",
        expect_name="duration",
        expected="<=5s",
        actual=None,
        message="duration probe raised",
        traceback="Traceback (most recent call last):\n  File ...\nRuntimeError",
    )
    payload = failure.to_dict()
    assert payload["traceback"].startswith("Traceback")
    assert payload["actual"] is None


def test_expect_failure_to_dict_is_json_serialisable() -> None:
    failure = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
        message="exit_code mismatch",
        artifact_ref="artifacts/ExampleEval1/exit-code.json",
    )
    payload = failure.to_dict()
    encoded = json.dumps(payload, sort_keys=True)
    assert json.loads(encoded) == payload


def test_expect_failure_to_dict_field_order_matches_dm005() -> None:
    failure = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
    )
    payload = failure.to_dict()
    # Stable ordering is essential for snapshot-style reporter diffs.
    assert list(payload.keys()) == [
        "eval_id",
        "expect_id",
        "expect_name",
        "expected",
        "actual",
        "message",
        "artifact_ref",
        "traceback",
    ]


def test_expect_failure_asdict_matches_to_dict() -> None:
    failure = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
    )
    # asdict() and to_dict() must agree on field values (ordering is
    # owned by to_dict per the spec).
    assert dataclasses.asdict(failure) == dict(failure.to_dict())


def test_expect_failure_deterministic_equality() -> None:
    a = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
        message="mismatch",
    )
    b = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
        message="mismatch",
    )
    assert a == b


def test_expect_failure_unequal_when_field_differs() -> None:
    base = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
    )
    assert base != dataclasses.replace(base, eval_id="OtherEval1")
    assert base != dataclasses.replace(base, expect_id="exit_code[1]")
    assert base != dataclasses.replace(base, expect_name="duration")
    assert base != dataclasses.replace(base, expected=1)
    assert base != dataclasses.replace(base, actual=0)
    assert base != dataclasses.replace(base, message="changed")
    assert base != dataclasses.replace(base, artifact_ref="x.json")
    assert base != dataclasses.replace(base, traceback="Traceback:...")


def test_expect_failure_round_trips_inside_expect_result() -> None:
    # DM-009 ExpectResult.failure now holds a real ExpectFailure. Confirm
    # ``ExpectResult.to_dict()`` unwraps it recursively so the Reporter
    # gets a plain dict with the DM-005 fields.
    failure = ExpectFailure(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expect_name="exit_code",
        expected=0,
        actual=2,
        message="exit_code mismatch",
    )
    result = ExpectResult(
        name="exit_code",
        passed=False,
        message="exit_code mismatch",
        failure=failure,
    )
    payload = result.to_dict()
    assert payload["failure"] == {
        "eval_id": "ExampleEval1",
        "expect_id": "exit_code[0]",
        "expect_name": "exit_code",
        "expected": 0,
        "actual": 2,
        "message": "exit_code mismatch",
        "artifact_ref": None,
        "traceback": None,
    }


def test_expect_failure_two_per_eval_pattern() -> None:
    # The reporter produces exactly one ExpectFailure per failing Expect.
    # Two failing Expects within one eval ⇒ two ExpectFailure entries.
    # This test locks the per-entry construction pattern; the full
    # reporter aggregation is covered by T03.13.
    failures = [
        ExpectFailure(
            eval_id="ExampleEval1",
            expect_id="exit_code[0]",
            expect_name="exit_code",
            expected=0,
            actual=2,
        ),
        ExpectFailure(
            eval_id="ExampleEval1",
            expect_id="duration[0]",
            expect_name="duration",
            expected="<=5s",
            actual="7.2s",
        ),
    ]
    assert len(failures) == 2
    assert {f.expect_id for f in failures} == {"exit_code[0]", "duration[0]"}
    # Each entry serialises independently — no shared state.
    payloads = [f.to_dict() for f in failures]
    assert payloads[0]["expect_name"] == "exit_code"
    assert payloads[1]["expect_name"] == "duration"


def test_expect_failure_importable_from_package() -> None:
    # Confirm the package re-export so callers can mirror the
    # ``from superclaude.cli.eval import ExpectResult`` pattern.
    from superclaude.cli.eval import ExpectFailure as PackageExpectFailure

    assert PackageExpectFailure is ExpectFailure
