"""T03.07 -- deterministic-fixture (stub) transport.

In-process :class:`Transport` implementation (COMP-033 / FR-023) that
returns seeded, byte-deterministic worker outputs without performing
any network I/O. This is the primary CI lane for the IMM-3 parallelism
test (``tests/swarm/test_imm3_parallel.py`` already ships its own
sleep-based fixture transport for the wall-clock budget; the stub
transport here is the deterministic-output CI lane referenced by the
Phase-3 acceptance criterion).

Determinism contract
====================

Two consecutive runs with identical inputs produce byte-identical
``WorkerResult`` content. The default body shape is a pure function of
``(model_id, prompt)``:

    body = f"stub:{model_id}:{sha256(prompt).hexdigest()[:16]}\\n"

This satisfies AC "Outputs are deterministic across runs given
identical inputs" regardless of which thread the dispatcher schedules
the call onto -- pure-function output sidesteps the
``ThreadPoolExecutor`` scheduling ambiguity that a call-counter scheme
would otherwise carry.

Callers that need per-slot fixture override (T03.07 step 1 corpus)
pass an explicit ``fixtures`` sequence. The transport then serves
``fixtures[counter % len(fixtures)]`` under an internal ``threading.Lock``
so concurrent ``send`` calls receive distinct entries in lock-acquisition
order. Determinism in that mode is per-(call-index, fixture-corpus); the
caller decides whether the slot↔fixture binding matters for their test.

No network, no clock dependency
===============================

* No HTTP / DNS / socket calls. The module imports only stdlib hashlib
  + threading + time.
* ``elapsed_ms`` is set to a small fixed value (zero by default) so
  test assertions on the field stay stable across runs and hosts.
  Callers that want a sleep-budgeted fixture transport (e.g. the IMM-3
  wall-clock budget test) construct their own; the stub does NOT
  introduce wall-clock latency.

Outcome recording
=================

Every :meth:`StubTransport.send` returns a :class:`WorkerResult` with
``status='success'``, ``http_code=200``, ``attempts=1``, and
``model_id`` / ``model_label`` set to the constructor's ``model_id``.
The raw body is stashed on the non-dataclass attribute
``WorkerResult.body`` (mirrors :mod:`openai_compat` -- byte-heavy,
manifest-irrelevant, materialised by the dispatcher to ``raw_path``).
"""

from __future__ import annotations

import hashlib
import threading
from typing import Optional, Sequence

from superclaude.cli.swarm.models import WorkerResult

__all__ = ["StubTransport"]


_DEFAULT_MODEL_ID = "stub-model-00"


class StubTransport:
    """Deterministic in-process transport for tests and CI lanes.

    Args:
        model_id: per-instance model identifier. Echoed onto
            ``WorkerResult.model_id`` / ``model_label`` so downstream
            tests can assert per-slot identity the same way they do
            against :mod:`openai_compat`. Defaults to ``"stub-model-00"``.
        fixtures: optional sequence of canned body strings. When
            supplied, ``send`` returns ``fixtures[counter % len(fixtures)]``
            with the counter incremented under an internal lock so
            concurrent calls receive distinct entries in lock-acquisition
            order. When ``None`` (the default), ``send`` returns a body
            that is a pure function of ``(model_id, prompt)`` -- the
            recommended mode for byte-deterministic dispatch tests
            because it sidesteps thread-scheduling ambiguity.
        elapsed_ms: fixed wall-clock value stamped on every
            :class:`WorkerResult`. Defaults to ``0`` so timing
            assertions stay stable across hosts; callers that want a
            non-zero value pass it explicitly.
    """

    def __init__(
        self,
        model_id: str = _DEFAULT_MODEL_ID,
        *,
        fixtures: Optional[Sequence[str]] = None,
        elapsed_ms: int = 0,
    ) -> None:
        if not model_id:
            raise ValueError("StubTransport.model_id must be non-empty")
        if elapsed_ms < 0:
            raise ValueError(
                f"StubTransport.elapsed_ms must be non-negative, got {elapsed_ms}"
            )
        self._model_id = model_id
        self._fixtures: Optional[tuple[str, ...]] = (
            tuple(fixtures) if fixtures is not None else None
        )
        if self._fixtures is not None and not self._fixtures:
            raise ValueError("StubTransport.fixtures must be non-empty when supplied")
        self._elapsed_ms = elapsed_ms
        self._lock = threading.Lock()
        self._counter = 0

    @property
    def model(self) -> str:
        """Per-instance model identifier (read-only)."""
        return self._model_id

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        """Return a deterministic :class:`WorkerResult` for ``prompt``.

        Args:
            prompt: fully-assembled prompt body. Used verbatim as input
                to the hash in default mode; ignored in fixtures mode
                (the corpus is the source of truth there).
            timeout: per-call wall-clock budget in seconds. Accepted for
                Protocol conformance; the stub does not honour it
                (no I/O to interrupt).

        Returns:
            A :class:`WorkerResult` with ``status='success'``,
            ``http_code=200``, ``attempts=1``, ``elapsed_ms`` fixed by
            the constructor, and ``model_id`` / ``model_label`` matching
            this instance. The body is stashed on the non-dataclass
            attribute :attr:`WorkerResult.body` (mirrors
            :mod:`openai_compat`).
        """
        # timeout intentionally unused -- the stub has no I/O to budget
        # against. Argument accepted to satisfy the Transport Protocol.
        del timeout

        body = self._next_body(prompt)
        result = WorkerResult(
            model_id=self._model_id,
            model_label=self._model_id,
            bytes=len(body.encode("utf-8")),
            status="success",
            http_code=200,
            attempts=1,
            elapsed_ms=self._elapsed_ms,
        )
        # Stash the body on a non-dataclass attribute so the dispatcher
        # can materialise raw_path without a second transport call.
        # Mirrors OpenAICompatTransport._build_result.
        result.body = body  # type: ignore[attr-defined]
        return result

    def _next_body(self, prompt: str) -> str:
        """Resolve the body for the current call.

        Fixtures mode: serve ``fixtures[counter % len(fixtures)]`` under
        the lock; advance the counter so the next call sees the next
        entry. Lock acquisition order determines the slot↔fixture
        binding when the dispatcher fans out concurrent calls.

        Default mode: return a pure function of ``(model_id, prompt)``
        so two runs with identical inputs produce byte-identical bodies
        regardless of scheduling.
        """
        if self._fixtures is not None:
            with self._lock:
                fixture = self._fixtures[self._counter % len(self._fixtures)]
                self._counter += 1
            return fixture

        digest = hashlib.sha256(
            f"{self._model_id}\0{prompt}".encode("utf-8")
        ).hexdigest()[:16]
        return f"stub:{self._model_id}:{digest}\n"
