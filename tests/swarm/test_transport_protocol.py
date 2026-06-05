"""T01.11 -- Transport Protocol structural-conformance tests.

Covers R-010 / COMP-031 from the MultiModelSwarm roadmap. The
``Transport`` Protocol defined in
``src/superclaude/cli/swarm/transports/__init__.py`` is the strategy
interface that both M3 implementations (``openai_compat`` and
``stub``) must satisfy.

This suite pins the *contract* so M3 inherits a stable surface:

1. ``Transport`` is importable from ``superclaude.cli.swarm.transports``.
2. ``Transport`` is a ``typing.Protocol`` and ``@runtime_checkable``.
3. ``Transport.send`` has the signature ``send(self, prompt: str,
   timeout: int) -> WorkerResult``.
4. A mock implementation with the matching signature passes
   ``isinstance(mock, Transport)`` (structural conformance).
5. An object missing ``send`` fails ``isinstance`` -- mutation guard
   that the Protocol is doing real work.
"""

from __future__ import annotations

import inspect
import typing

import pytest

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.transports import Transport


# ---------------------------------------------------------------------------
# Surface (import + Protocol shape).
# ---------------------------------------------------------------------------


def test_transport_is_protocol() -> None:
    """``Transport`` must be a ``typing.Protocol`` subclass."""
    # ``Protocol`` subclasses carry ``_is_protocol = True`` per PEP 544.
    assert getattr(Transport, "_is_protocol", False), (
        "Transport must be declared as `class Transport(Protocol)` so "
        "M3 implementations can satisfy it structurally without "
        "inheritance."
    )


def test_transport_is_runtime_checkable() -> None:
    """``@runtime_checkable`` lets dispatch validate registry entries."""
    assert getattr(Transport, "_is_runtime_protocol", False), (
        "Transport must be decorated with @runtime_checkable so "
        "isinstance(driver, Transport) is usable in the dispatch "
        "registry (COMP-007)."
    )


def test_send_signature_matches_contract() -> None:
    """``send(self, prompt: str, timeout: int) -> WorkerResult``."""
    sig = inspect.signature(Transport.send)
    params = list(sig.parameters.values())

    # self + prompt + timeout
    assert [p.name for p in params] == ["self", "prompt", "timeout"], (
        f"Transport.send must take (self, prompt, timeout); got "
        f"{[p.name for p in params]}"
    )

    hints = typing.get_type_hints(Transport.send)
    assert hints.get("prompt") is str, (
        f"prompt annotation must be `str`; got {hints.get('prompt')!r}"
    )
    assert hints.get("timeout") is int, (
        f"timeout annotation must be `int`; got {hints.get('timeout')!r}"
    )
    assert hints.get("return") is WorkerResult, (
        f"return annotation must be `WorkerResult`; got "
        f"{hints.get('return')!r}"
    )


# ---------------------------------------------------------------------------
# Structural conformance (mock impl satisfies the Protocol).
# ---------------------------------------------------------------------------


class _MockTransport:
    """Minimal structural impl used to validate the Protocol contract."""

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        return WorkerResult()


def test_mock_implementation_passes_isinstance() -> None:
    """A class with matching ``send`` satisfies the Protocol at runtime."""
    assert isinstance(_MockTransport(), Transport), (
        "_MockTransport defines send(prompt, timeout) -> WorkerResult "
        "but isinstance check failed -- Transport may not be "
        "@runtime_checkable or its signature drifted."
    )


def test_mock_send_returns_worker_result() -> None:
    """Sanity: the mock returns the contracted type."""
    result = _MockTransport().send("hello", 180)
    assert isinstance(result, WorkerResult)


# ---------------------------------------------------------------------------
# Mutation guard (object without `send` does NOT satisfy the Protocol).
# ---------------------------------------------------------------------------


class _MissingSend:
    """Negative control -- no ``send`` method."""


def test_object_missing_send_fails_isinstance() -> None:
    """Mutation guard: removing ``send`` breaks conformance."""
    assert not isinstance(_MissingSend(), Transport), (
        "An object without `send` must NOT pass isinstance(Transport); "
        "if this passes, the Protocol is not enforcing the contract."
    )


# ---------------------------------------------------------------------------
# Docstring presence (acceptance criterion: 'Docstring documents the contract').
# ---------------------------------------------------------------------------


def test_transport_class_has_docstring() -> None:
    assert Transport.__doc__ and Transport.__doc__.strip(), (
        "Transport must carry a class docstring describing the contract."
    )


def test_send_method_has_docstring() -> None:
    assert Transport.send.__doc__ and Transport.send.__doc__.strip(), (
        "Transport.send must carry a docstring describing args + return."
    )


# ---------------------------------------------------------------------------
# Module re-export.
# ---------------------------------------------------------------------------


def test_transport_in_module_all() -> None:
    from superclaude.cli.swarm import transports

    assert "Transport" in transports.__all__, (
        "Transport must be listed in transports.__all__ so star-imports "
        "and tooling surface the public symbol."
    )


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
