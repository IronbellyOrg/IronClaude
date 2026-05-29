"""Tests for ``superclaude.cli.eval.models.EvalOutcome``.

Covers cliEval Phase 3 / Task T03.01 acceptance criteria (DM-001):

* Module exports a frozen ``EvalOutcome`` dataclass with the 9 fields
  ``eval_id, title, status, duration_sec, expects, skip_reason,
  skip_flag_triggered, artifacts, error_class``.
* Mutation is rejected (``dataclasses.FrozenInstanceError``).
* ``status`` is a ``Literal`` with exactly the 8 DM-001 values; an invalid
  status raises ``ValueError``.
* ``to_dict()`` returns a deterministic JSON-serialisable mapping with
  nested ``ExpectResult`` records unwrapped via their own ``to_dict``.
* Two instances built from identical arguments compare equal.

Cross-link: ``ExpectResult`` (DM-009 / T01.15) is the typed payload for
the ``expects`` field. ``EvalOutcome`` is consumed by COMP-008 Reporter
(T03.13) and RunOrchestrator (T03.15).
"""

from __future__ import annotations

import dataclasses
import json

import pytest

from superclaude.cli.eval.models import (
    EVAL_STATUSES,
    EvalOutcome,
    ExpectResult,
)


def test_eval_outcome_has_required_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(EvalOutcome)]
    # Field order matches DM-001 verbatim so to_dict() output is stable
    # across reporter snapshots.
    assert field_names == [
        "eval_id",
        "title",
        "status",
        "duration_sec",
        "expects",
        "skip_reason",
        "skip_flag_triggered",
        "artifacts",
        "error_class",
    ]


def test_eval_outcome_is_frozen() -> None:
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.1,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        outcome.status = "FAIL"  # type: ignore[misc]


def test_eval_outcome_status_literal_set_is_exactly_dm001() -> None:
    # DM-001 enumerates exactly these 8 statuses; the model must not drift.
    assert set(EVAL_STATUSES) == {
        "PASS",
        "FAIL",
        "ERRORED",
        "TIMEOUT",
        "INTERRUPTED",
        "SKIPPED",
        "XFAIL",
        "XPASS",
    }
    assert len(EVAL_STATUSES) == 8


@pytest.mark.parametrize("status", EVAL_STATUSES)
def test_eval_outcome_accepts_every_valid_status(status: str) -> None:
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status=status,  # type: ignore[arg-type]
        duration_sec=0.0,
    )
    assert outcome.status == status


def test_eval_outcome_rejects_invalid_status() -> None:
    with pytest.raises(ValueError) as excinfo:
        EvalOutcome(
            eval_id="ExampleEval1",
            title="example",
            status="UNKNOWN",  # type: ignore[arg-type]
            duration_sec=0.0,
        )
    # Error message should mention the rejected value so callers see what
    # was passed (matters for JSON-replay paths that build outcomes from
    # dynamic strings).
    assert "UNKNOWN" in str(excinfo.value)


def test_eval_outcome_rejects_lowercased_status() -> None:
    # Status is uppercase by DM-001 contract; case-folded variants must
    # be rejected so the Reporter never sees ambiguous casing.
    with pytest.raises(ValueError):
        EvalOutcome(
            eval_id="ExampleEval1",
            title="example",
            status="pass",  # type: ignore[arg-type]
            duration_sec=0.0,
        )


def test_eval_outcome_defaults() -> None:
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.0,
    )
    assert outcome.expects == ()
    assert outcome.skip_reason is None
    assert outcome.skip_flag_triggered is None
    assert outcome.artifacts == {}
    assert outcome.error_class is None


def test_eval_outcome_artifacts_default_is_independent_per_instance() -> None:
    # default_factory=dict must hand each instance its own mapping so a
    # caller mutating one outcome's artifacts cannot leak across outcomes.
    a = EvalOutcome(eval_id="A1", title="a", status="PASS", duration_sec=0.0)
    b = EvalOutcome(eval_id="B1", title="b", status="PASS", duration_sec=0.0)
    assert a.artifacts is not b.artifacts


def test_eval_outcome_passing_construction_with_expects() -> None:
    expects = (
        ExpectResult(name="exit_code", passed=True, duration_sec=0.001),
        ExpectResult(name="file.contains_event", passed=True, duration_sec=0.002),
    )
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="Example eval one",
        status="PASS",
        duration_sec=0.123,
        expects=expects,
        artifacts={"stdout": "/tmp/run/stdout.log"},
    )
    assert outcome.status == "PASS"
    assert outcome.expects == expects
    assert outcome.artifacts == {"stdout": "/tmp/run/stdout.log"}


def test_eval_outcome_skipped_with_reason_and_flag() -> None:
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="needs tavily",
        status="SKIPPED",
        duration_sec=0.0,
        skip_reason="capability 'mcp.tavily' unresolved",
        skip_flag_triggered="mcp.tavily",
    )
    assert outcome.skip_reason == "capability 'mcp.tavily' unresolved"
    assert outcome.skip_flag_triggered == "mcp.tavily"
    assert outcome.expects == ()


def test_eval_outcome_errored_with_error_class() -> None:
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="harness boom",
        status="ERRORED",
        duration_sec=0.05,
        error_class="builtins.RuntimeError",
    )
    assert outcome.error_class == "builtins.RuntimeError"


def test_eval_outcome_to_dict_field_order_matches_dm001() -> None:
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.0,
    )
    payload = outcome.to_dict()
    assert list(payload.keys()) == [
        "eval_id",
        "title",
        "status",
        "duration_sec",
        "expects",
        "skip_reason",
        "skip_flag_triggered",
        "artifacts",
        "error_class",
    ]


def test_eval_outcome_to_dict_is_json_serialisable() -> None:
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.123,
        expects=(ExpectResult(name="exit_code", passed=True, duration_sec=0.001),),
        artifacts={"stdout": "/tmp/run/stdout.log"},
    )
    payload = outcome.to_dict()
    # Payload must round-trip through json.dumps so the Reporter (COMP-008)
    # can emit it without re-mapping.
    encoded = json.dumps(payload, sort_keys=True)
    decoded = json.loads(encoded)
    assert decoded["status"] == "PASS"
    assert decoded["expects"][0]["name"] == "exit_code"
    assert decoded["artifacts"] == {"stdout": "/tmp/run/stdout.log"}


def test_eval_outcome_to_dict_unwraps_nested_expect_results() -> None:
    expect = ExpectResult(
        name="exit_code",
        passed=False,
        message="exit_code expected 0, got 2",
        details={"expected": 0, "actual": 2},
        duration_sec=0.004,
    )
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="FAIL",
        duration_sec=0.1,
        expects=(expect,),
    )
    payload = outcome.to_dict()
    # The Reporter relies on each ExpectResult being a plain dict, not a
    # nested dataclass, so it can iterate without bespoke unwrapping.
    assert isinstance(payload["expects"], list)
    assert payload["expects"][0] == expect.to_dict()


def test_eval_outcome_to_dict_artifacts_is_independent_of_source() -> None:
    artifacts = {"stdout": "/tmp/run/stdout.log"}
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.0,
        artifacts=artifacts,
    )
    payload = outcome.to_dict()
    payload["artifacts"]["stdout"] = "/dev/null"
    # Mutating the returned mapping must not bleed into the frozen source.
    assert outcome.artifacts["stdout"] == "/tmp/run/stdout.log"


def test_eval_outcome_deterministic_equality() -> None:
    expect = ExpectResult(name="exit_code", passed=True, duration_sec=0.0)
    a = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.5,
        expects=(expect,),
        artifacts={"stdout": "/tmp/a"},
    )
    b = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.5,
        expects=(expect,),
        artifacts={"stdout": "/tmp/a"},
    )
    assert a == b


def test_eval_outcome_unequal_when_field_differs() -> None:
    base = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.0,
    )
    assert base != dataclasses.replace(base, eval_id="ExampleEval2")
    assert base != dataclasses.replace(base, title="other")
    assert base != dataclasses.replace(base, status="FAIL")
    assert base != dataclasses.replace(base, duration_sec=1.0)
    assert base != dataclasses.replace(base, skip_reason="x")
    assert base != dataclasses.replace(base, skip_flag_triggered="x")
    assert base != dataclasses.replace(base, error_class="X")
