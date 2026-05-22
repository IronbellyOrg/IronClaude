"""Tests for ``superclaude.cli.eval.models.ExpectResult``.

Covers cliEval Phase 1 / Task T01.15 acceptance criteria (DM-009):

* Module exports a frozen ``ExpectResult`` dataclass with fields
  ``name, passed, message, details, duration_sec, failure``.
* Mutation is rejected (``dataclasses.FrozenInstanceError``).
* Construction with valid field types succeeds; ``failure`` is Optional
  with no required-when-failed coupling per DM-009.
* ``to_dict()`` (and ``dataclasses.asdict``) yields a JSON-serialisable
  mapping per the DM-009 "serializable" requirement.
* Two instances built from identical arguments compare equal.

Cross-link: DM-005 ``ExpectFailure`` (T01.16) is referenced via a string
forward annotation; tests use ``object()`` stand-ins or skip the
populated-failure branch so this module does not preempt T01.16.
"""

from __future__ import annotations

import dataclasses
import json

import pytest

from superclaude.cli.eval.models import ExpectResult


def test_expect_result_has_required_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(ExpectResult)]
    # Ordering matters: DM-009 lists name, passed, message, details,
    # duration_sec, failure in that order so to_dict() output is stable
    # across reporter snapshots.
    assert field_names == [
        "name",
        "passed",
        "message",
        "details",
        "duration_sec",
        "failure",
    ]


def test_expect_result_is_frozen() -> None:
    result = ExpectResult(name="exit_code", passed=True)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.passed = False  # type: ignore[misc]


def test_expect_result_defaults() -> None:
    result = ExpectResult(name="exit_code", passed=True)
    assert result.message == ""
    assert result.details == {}
    assert result.duration_sec == 0.0
    assert result.failure is None


def test_expect_result_passing_construction() -> None:
    result = ExpectResult(
        name="file.contains_event",
        passed=True,
        message="event 'SessionStart' observed",
        details={"event": "SessionStart", "count": 1},
        duration_sec=0.012,
    )
    assert result.passed is True
    assert result.failure is None
    assert result.details == {"event": "SessionStart", "count": 1}


def test_expect_result_failing_without_failure_attached_is_allowed() -> None:
    # DM-009 explicitly: "failure is Optional ... no required-when-failed
    # coupling". A failing result with failure=None is well-formed.
    result = ExpectResult(
        name="exit_code",
        passed=False,
        message="exit_code expected 0, got 2",
    )
    assert result.passed is False
    assert result.failure is None


def test_expect_result_failing_with_failure_stand_in() -> None:
    # T01.16 lands the real ExpectFailure; here we use a dataclass stand-in
    # to prove the ``failure`` field accepts a populated value and that
    # ``to_dict`` recursively unwraps nested dataclasses.
    @dataclasses.dataclass(frozen=True)
    class _FailureStandIn:
        eval_id: str
        expect_id: str
        expected: str
        actual: str

    stand_in = _FailureStandIn(
        eval_id="ExampleEval1",
        expect_id="exit_code[0]",
        expected="0",
        actual="2",
    )
    result = ExpectResult(
        name="exit_code",
        passed=False,
        message="exit_code mismatch",
        details={"expected": 0, "actual": 2},
        duration_sec=0.004,
        failure=stand_in,  # type: ignore[arg-type]
    )
    assert result.failure is stand_in


def test_expect_result_to_dict_is_json_serialisable() -> None:
    result = ExpectResult(
        name="exit_code",
        passed=True,
        message="ok",
        details={"value": 0},
        duration_sec=0.001,
    )
    payload = result.to_dict()
    # The payload must round-trip through json.dumps so the Reporter
    # (COMP-008) can emit it without re-mapping.
    encoded = json.dumps(payload, sort_keys=True)
    assert json.loads(encoded) == payload


def test_expect_result_asdict_matches_to_dict() -> None:
    result = ExpectResult(name="x", passed=True, duration_sec=0.5)
    assert dataclasses.asdict(result) == result.to_dict()


def test_expect_result_asdict_unwraps_nested_dataclass_failure() -> None:
    @dataclasses.dataclass(frozen=True)
    class _FailureStandIn:
        eval_id: str
        message: str

    stand_in = _FailureStandIn(eval_id="ExampleEval1", message="boom")
    result = ExpectResult(
        name="exit_code",
        passed=False,
        failure=stand_in,  # type: ignore[arg-type]
    )
    payload = result.to_dict()
    # ``dataclasses.asdict`` recurses into nested dataclasses so the
    # reporter does not need bespoke handling for the optional failure.
    assert payload["failure"] == {
        "eval_id": "ExampleEval1",
        "message": "boom",
    }


def test_expect_result_deterministic_equality() -> None:
    a = ExpectResult(
        name="exit_code",
        passed=True,
        message="ok",
        details={"value": 0},
        duration_sec=0.001,
    )
    b = ExpectResult(
        name="exit_code",
        passed=True,
        message="ok",
        details={"value": 0},
        duration_sec=0.001,
    )
    assert a == b


def test_expect_result_unequal_when_field_differs() -> None:
    base = ExpectResult(name="exit_code", passed=True)
    assert base != dataclasses.replace(base, name="duration")
    assert base != dataclasses.replace(base, passed=False)
    assert base != dataclasses.replace(base, message="x")
    assert base != dataclasses.replace(base, details={"k": 1})
    assert base != dataclasses.replace(base, duration_sec=0.5)


def test_expect_result_details_default_is_independent_per_instance() -> None:
    # default_factory=dict must hand each instance its own mapping so a
    # caller mutating the default does not leak across results.
    a = ExpectResult(name="x", passed=True)
    b = ExpectResult(name="y", passed=True)
    assert a.details is not b.details
