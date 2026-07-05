"""T03.07 -- StubTransport (deterministic-fixture) test suite.

Covers R-065 (COMP-033) + R-069 (FR-023):

* :class:`StubTransport` implements the :class:`Transport` Protocol
  structurally (``isinstance(stub, Transport)`` holds).
* Default mode -- body is a pure function of ``(model_id, prompt)``;
  two consecutive calls with identical inputs return byte-identical
  bodies (and byte-identical ``WorkerResult`` field tuples).
* Fixtures mode -- the corpus is served in lock-acquisition order with
  modular wrap-around; per-call-index determinism holds.
* Outcome shape -- ``status='success'`` / ``http_code=200`` /
  ``attempts=1`` and the ``model_id`` propagates to both
  ``WorkerResult.model_id`` and ``WorkerResult.model_label``.
* No network -- the module imports only stdlib + ``WorkerResult``;
  ``send`` makes no socket / DNS / HTTP calls (asserted by guarding
  ``socket.socket`` for the duration of the call).
* Dispatch integration -- ``dispatch_wave1`` against a single
  ``StubTransport`` returns N ``WorkerResult`` entries whose bodies
  are byte-identical across two consecutive runs (the AC-005
  end-to-end CI-default lane).
"""

from __future__ import annotations

import socket

import pytest

from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.models import (
    Manifest,
    PreflightSummary,
    SwarmState,
)
from superclaude.cli.swarm.preflight import PreflightResult
from superclaude.cli.swarm.transports import Transport
from superclaude.cli.swarm.transports.stub import StubTransport

# ---------------------------------------------------------------------------
# Protocol conformance.
# ---------------------------------------------------------------------------


def test_stub_transport_implements_protocol() -> None:
    """StubTransport satisfies the runtime-checkable Transport Protocol."""
    transport = StubTransport()
    assert isinstance(transport, Transport)


# ---------------------------------------------------------------------------
# Default-mode determinism (pure function of model_id + prompt).
# ---------------------------------------------------------------------------


def test_default_mode_identical_inputs_yield_identical_body() -> None:
    """Two send() calls with the same prompt return the same body bytes."""
    transport = StubTransport(model_id="model-A")
    first = transport.send("the quick brown fox", timeout=180)
    second = transport.send("the quick brown fox", timeout=180)
    assert first.body == second.body  # type: ignore[attr-defined]


def test_default_mode_two_run_byte_identical() -> None:
    """Fresh transport per run + identical prompt => byte-identical body."""
    body_run1 = StubTransport(model_id="model-A").send("hello", timeout=180).body  # type: ignore[attr-defined]
    body_run2 = StubTransport(model_id="model-A").send("hello", timeout=180).body  # type: ignore[attr-defined]
    assert body_run1 == body_run2


def test_default_mode_distinct_models_yield_distinct_bodies() -> None:
    """``model_id`` participates in the hash so per-slot bindings differ."""
    body_a = StubTransport(model_id="model-A").send("hello", timeout=180).body  # type: ignore[attr-defined]
    body_b = StubTransport(model_id="model-B").send("hello", timeout=180).body  # type: ignore[attr-defined]
    assert body_a != body_b


def test_default_mode_distinct_prompts_yield_distinct_bodies() -> None:
    """``prompt`` participates in the hash."""
    transport = StubTransport(model_id="model-A")
    first = transport.send("alpha", timeout=180).body  # type: ignore[attr-defined]
    second = transport.send("beta", timeout=180).body  # type: ignore[attr-defined]
    assert first != second


# ---------------------------------------------------------------------------
# Fixtures-mode determinism.
# ---------------------------------------------------------------------------


def test_fixtures_mode_cycles_in_lock_order() -> None:
    """Sequential send calls receive the corpus in declared order."""
    corpus = ("output-0", "output-1", "output-2")
    transport = StubTransport(model_id="m", fixtures=corpus)
    bodies = [transport.send("p", timeout=10).body for _ in range(4)]  # type: ignore[attr-defined]
    # Wraps around modularly after the third call.
    assert bodies == ["output-0", "output-1", "output-2", "output-0"]


def test_fixtures_mode_rejects_empty_sequence() -> None:
    with pytest.raises(ValueError):
        StubTransport(model_id="m", fixtures=())


# ---------------------------------------------------------------------------
# WorkerResult outcome shape.
# ---------------------------------------------------------------------------


def test_send_records_success_outcome_shape() -> None:
    transport = StubTransport(model_id="model-X", elapsed_ms=7)
    result = transport.send("hello", timeout=180)
    assert result.status == "success"
    assert result.http_code == 200
    assert result.attempts == 1
    assert result.elapsed_ms == 7
    assert result.model_id == "model-X"
    assert result.model_label == "model-X"
    assert result.bytes == len(result.body.encode("utf-8"))  # type: ignore[attr-defined]


def test_constructor_rejects_negative_elapsed_ms() -> None:
    with pytest.raises(ValueError):
        StubTransport(elapsed_ms=-1)


def test_constructor_rejects_empty_model_id() -> None:
    with pytest.raises(ValueError):
        StubTransport(model_id="")


# ---------------------------------------------------------------------------
# No-network guarantee.
# ---------------------------------------------------------------------------


def test_send_makes_no_socket_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    """Guard ``socket.socket`` to prove the stub performs no network I/O."""

    def _explode(*_args: object, **_kwargs: object) -> None:
        raise AssertionError(
            "StubTransport.send must not open sockets; "
            "see module docstring 'No network, no clock dependency'."
        )

    monkeypatch.setattr(socket, "socket", _explode)
    transport = StubTransport(model_id="model-A")
    # Exercises both the hash branch and the WorkerResult build path.
    result = transport.send("anything", timeout=180)
    assert result.status == "success"


# ---------------------------------------------------------------------------
# Dispatch integration -- the CI-default AC lane.
# ---------------------------------------------------------------------------


def _make_preflight(workers_requested: int) -> PreflightResult:
    manifest = Manifest(
        contract_version="1.0",
        job_id="job-stub",
        preflight=PreflightSummary(
            target_checksum="cafebabe",
            workers_requested=workers_requested,
            transport_kind="stub",
        ),
    )
    return PreflightResult(
        manifest=manifest,
        state=SwarmState(state="preflight_ok", job_id="job-stub"),
    )


def test_dispatch_against_stub_two_runs_byte_identical() -> None:
    """Two consecutive dispatch_wave1 runs against StubTransport yield
    byte-identical per-slot bodies and field tuples.

    The bodies use the default pure-function mode so call-order
    ambiguity (which thread services which slot) cannot perturb the
    output. The slot index is stamped by the dispatcher; this test
    asserts the body content + outcome shape are stable.
    """
    preflight = _make_preflight(workers_requested=4)

    def _capture_run() -> list[tuple[int, str, str, int, int]]:
        transport = StubTransport(model_id="stub-model-00")
        results = dispatch_wave1(preflight, transport=transport, prompt="hello")
        return [
            (
                r.index,
                r.body,  # type: ignore[attr-defined]
                r.status,
                r.http_code or 0,
                r.attempts,
            )
            for r in results
        ]

    first = _capture_run()
    second = _capture_run()
    assert first == second
    assert len(first) == 4
    assert all(entry[2] == "success" for entry in first)
    assert all(entry[3] == 200 for entry in first)
    assert [entry[0] for entry in first] == [0, 1, 2, 3]
