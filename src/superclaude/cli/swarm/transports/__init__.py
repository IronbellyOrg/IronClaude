"""Swarm transports -- Transport Protocol + concrete worker drivers.

Swarm-specific divergence from ``cli/sprint/`` (which shells out via
``process.py``). Swarm fans a prompt across heterogeneous
OpenAI-compatible workers, so the network I/O is abstracted behind a
``typing.Protocol``.

T01.11 lands the ``Transport`` Protocol with the ``send(prompt,
timeout) -> WorkerResult`` contract (COMP-031). M3 lands two concrete
implementations:

* ``openai_compat.py`` -- HTTP driver for any OpenAI-compatible
  endpoint (DM-004 kind='openai_compat'), built on httpx, returning a
  ``WorkerResult`` populated with ``http_code`` / ``attempts`` /
  ``elapsed_ms``.
* ``stub.py`` -- deterministic in-process driver for tests and dry
  runs (DM-004 kind='stub'). Returns fixed outputs so CI can exercise
  the parallel-dispatch path without network I/O (AC-005, FR-022/023).

Contract
========

``Transport.send(prompt: str, timeout: int) -> WorkerResult``

* ``prompt`` -- the fully-assembled prompt body the worker should
  receive. Whitespace is preserved verbatim by ``PromptSpec`` upstream
  (T01.17), so the transport MUST NOT re-normalize.
* ``timeout`` -- per-call wall-clock budget in seconds. Default is
  ``WorkerSpec.timeout_sec`` (180s per NFR-010). Transports SHOULD
  raise a transport-specific timeout error rather than blocking past
  this budget; the dispatch layer (COMP-007) records the outcome as a
  failed ``WorkerResult`` with ``status='timeout'``.
* return -- a ``WorkerResult`` (DM-013) carrying the per-worker
  outcome. Fields ``http_code``, ``attempts``, and ``elapsed_ms`` are
  populated by the transport; the dispatch layer fills the path
  fields after the body is materialised to disk.

Implementations declare conformance structurally (Python protocols);
no explicit base-class inheritance is required. The protocol is
``@runtime_checkable`` so dispatch can ``isinstance(driver,
Transport)`` for defensive registry checks.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from superclaude.cli.swarm.models import WorkerResult


@runtime_checkable
class Transport(Protocol):
    """Strategy interface for swarm worker drivers (COMP-031).

    Concrete implementations land in M3:

    * ``openai_compat.OpenAICompatTransport`` -- httpx driver for any
      OpenAI-compatible endpoint (TransportSpec.kind='openai_compat').
    * ``stub.StubTransport`` -- deterministic in-process driver for
      tests (TransportSpec.kind='stub').

    The dispatch layer (COMP-007, M3) selects the implementation from
    ``TransportSpec.kind`` and invokes ``send`` once per worker inside
    the ThreadPoolExecutor fan-out.
    """

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        """Send ``prompt`` to the worker; return the ``WorkerResult``.

        Args:
            prompt: Fully-assembled prompt body. Verbatim -- the
                transport MUST NOT re-normalize whitespace.
            timeout: Per-call wall-clock budget in seconds
                (``WorkerSpec.timeout_sec``, default 180 per NFR-010).
                Transports SHOULD honour this budget rather than block
                indefinitely.

        Returns:
            A ``WorkerResult`` (DM-013) carrying the per-worker
            outcome. The transport fills ``http_code`` / ``attempts``
            / ``elapsed_ms``; the dispatch layer fills the path fields
            after materialising the body to disk.
        """
        ...


__all__: list[str] = ["Transport"]
