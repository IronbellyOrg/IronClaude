"""Tests for ``superclaude.cli.eval.models.EvalResult``.

Covers cliEval Phase 3 / Task T03.02 acceptance criteria (DM-003):

* Module exports an ``EvalResult`` dataclass with the 9 fields
  ``eval_id, outcome, start, end, duration_sec, stdout, stderr, artifacts,
  error``.
* ``duration_sec`` is computed from ``end - start`` consistently — any
  caller-supplied value is overwritten so the field cannot drift from the
  timestamps.
* ``to_dict()`` returns a deterministic JSON-serialisable mapping with the
  nested ``EvalOutcome`` unwrapped via its own ``to_dict`` and ``error``
  rendered as ``{"type": "<fqcn>", "message": str}`` (or ``None``).
* The dataclass is frozen so reporter consumers cannot mutate it mid-render.

Cross-link: ``EvalOutcome`` (DM-001 / T03.01) is the runner emission carried
by the ``outcome`` field. ``EvalResult`` is consumed by COMP-008 Reporter
(T03.13).
"""

from __future__ import annotations

import dataclasses
import json

import pytest

from superclaude.cli.eval.models import (
    EvalOutcome,
    EvalResult,
    ExpectResult,
)


def _outcome(status: str = "PASS") -> EvalOutcome:
    return EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status=status,  # type: ignore[arg-type]
        duration_sec=0.123,
    )


def test_eval_result_has_required_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(EvalResult)]
    # Field order matches DM-003 verbatim so to_dict() ordering stays stable
    # across reporter snapshots and review diffs.
    assert field_names == [
        "eval_id",
        "outcome",
        "start",
        "end",
        "duration_sec",
        "stdout",
        "stderr",
        "artifacts",
        "error",
    ]


def test_eval_result_is_frozen() -> None:
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:01",
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.stdout = "tampered"  # type: ignore[misc]


def test_eval_result_defaults() -> None:
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:00",
    )
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.artifacts == {}
    assert result.error is None


def test_eval_result_artifacts_default_is_independent_per_instance() -> None:
    a = EvalResult(
        eval_id="A1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:00",
    )
    b = EvalResult(
        eval_id="B1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:00",
    )
    assert a.artifacts is not b.artifacts


def test_eval_result_duration_sec_is_computed_from_timestamps() -> None:
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:01.500000",
    )
    assert result.duration_sec == pytest.approx(1.5)


def test_eval_result_duration_sec_caller_value_is_overwritten() -> None:
    # Acceptance: duration_sec is computed from end - start consistently.
    # A caller-supplied value must not be honoured if the timestamps disagree
    # — otherwise the Reporter could emit inconsistent rows.
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:02",
        duration_sec=99.0,
    )
    assert result.duration_sec == pytest.approx(2.0)


def test_eval_result_duration_sec_kept_when_timestamps_missing() -> None:
    # Partial summaries (e.g. SIGINT-interrupted runs that captured a start
    # but no end) must still be constructible. With an empty ``end`` we keep
    # whatever the caller supplied so the Reporter can render the row.
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(status="INTERRUPTED"),
        start="2026-05-20T11:00:00",
        end="",
        duration_sec=0.42,
    )
    assert result.duration_sec == pytest.approx(0.42)


def test_eval_result_to_dict_field_order_matches_dm003() -> None:
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:00",
    )
    payload = result.to_dict()
    assert list(payload.keys()) == [
        "eval_id",
        "outcome",
        "start",
        "end",
        "duration_sec",
        "stdout",
        "stderr",
        "artifacts",
        "error",
    ]


def test_eval_result_to_dict_is_json_serialisable() -> None:
    outcome = EvalOutcome(
        eval_id="ExampleEval1",
        title="example",
        status="PASS",
        duration_sec=0.123,
        expects=(ExpectResult(name="exit_code", passed=True, duration_sec=0.001),),
        artifacts={"stdout": "/tmp/run/stdout.log"},
    )
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=outcome,
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:01",
        stdout="hello\n",
        stderr="",
        artifacts={"stdout": "/tmp/run/stdout.log"},
    )
    payload = result.to_dict()
    # Round-trips through json.dumps so the Reporter (COMP-008 / T03.13) can
    # emit it without re-mapping.
    encoded = json.dumps(payload, sort_keys=True)
    decoded = json.loads(encoded)
    assert decoded["eval_id"] == "ExampleEval1"
    assert decoded["duration_sec"] == pytest.approx(1.0)
    assert decoded["outcome"]["status"] == "PASS"
    assert decoded["outcome"]["expects"][0]["name"] == "exit_code"
    assert decoded["artifacts"] == {"stdout": "/tmp/run/stdout.log"}
    assert decoded["error"] is None


def test_eval_result_to_dict_unwraps_nested_outcome() -> None:
    outcome = _outcome()
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=outcome,
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:01",
    )
    payload = result.to_dict()
    # The Reporter relies on the nested outcome being a plain dict so it can
    # iterate without bespoke recursion.
    assert isinstance(payload["outcome"], dict)
    assert payload["outcome"] == outcome.to_dict()


def test_eval_result_to_dict_artifacts_is_independent_of_source() -> None:
    artifacts = {"stdout": "/tmp/run/stdout.log"}
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:00",
        artifacts=artifacts,
    )
    payload = result.to_dict()
    payload["artifacts"]["stdout"] = "/dev/null"
    # Mutating the returned mapping must not bleed into the frozen source.
    assert result.artifacts["stdout"] == "/tmp/run/stdout.log"


def test_eval_result_to_dict_renders_error_as_typed_mapping() -> None:
    err = RuntimeError("boom")
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(status="ERRORED"),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:00",
        error=err,
    )
    payload = result.to_dict()
    assert payload["error"] == {
        "type": "builtins.RuntimeError",
        "message": "boom",
    }
    # The fully-qualified-class-name shape must remain JSON serializable.
    json.dumps(payload, sort_keys=True)


def test_eval_result_to_dict_error_none_when_no_error() -> None:
    result = EvalResult(
        eval_id="ExampleEval1",
        outcome=_outcome(),
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:00",
    )
    assert result.to_dict()["error"] is None


def test_eval_result_deterministic_equality() -> None:
    outcome = _outcome()
    a = EvalResult(
        eval_id="ExampleEval1",
        outcome=outcome,
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:01",
        stdout="hello",
        artifacts={"stdout": "/tmp/a"},
    )
    b = EvalResult(
        eval_id="ExampleEval1",
        outcome=outcome,
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:01",
        stdout="hello",
        artifacts={"stdout": "/tmp/a"},
    )
    assert a == b


def test_eval_result_unequal_when_field_differs() -> None:
    outcome = _outcome()
    base = EvalResult(
        eval_id="ExampleEval1",
        outcome=outcome,
        start="2026-05-20T11:00:00",
        end="2026-05-20T11:00:01",
    )
    assert base != dataclasses.replace(base, eval_id="ExampleEval2")
    assert base != dataclasses.replace(base, stdout="other")
    assert base != dataclasses.replace(base, stderr="oops")
    assert base != dataclasses.replace(base, end="2026-05-20T11:00:05")


def test_eval_result_reexported_from_package() -> None:
    # Consumers (Reporter, RunOrchestrator) import the symbol from the
    # package root, not the private models module.
    from superclaude.cli.eval import EvalResult as PkgEvalResult

    assert PkgEvalResult is EvalResult
