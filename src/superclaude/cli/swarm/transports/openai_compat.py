"""T03.05 -- OpenAI-compatible httpx transport (Phase-1 reference).

Concrete :class:`Transport` implementation (COMP-032 / FR-022) that
routes prompts to any OpenAI-compatible Chat Completions endpoint via
httpx. The Phase-1 deployment routes through the T2 proxy: endpoint,
key, and per-slot model identifiers are resolved from environment
variables ``T2ProxyUrl`` / ``T2ProxyKey`` / ``T2Model01..T2Model0N``
per AC-017.

Env-var contract
================

The transport reads the T2 proxy contract from the process environment
via :func:`read_env`:

* ``T2ProxyUrl``    -- base URL of the OpenAI-compatible proxy
                       (e.g. ``https://proxy.example.com/v1``). The
                       transport appends ``/chat/completions`` at send
                       time.
* ``T2ProxyKey``    -- bearer token sent as
                       ``Authorization: Bearer <key>``.
* ``T2Model01``     -- model identifier for worker slot 1.
* ``T2Model02``..   -- model identifier for worker slot 2.. (zero or
                       more; up to ``T2_MODEL_MAX_SLOTS`` from
                       ``cli/swarm/config.py``).

All values are mandatory; :func:`read_env` raises
:class:`TransportEnvError` listing the missing names when any are
absent. That structured failure is the Wave-0 anchor the dispatcher
(M3) feeds into the INV-007 empty-pool failure path (T02.11).

Outcome recording (FR-017 / NFR-010)
====================================

Every :meth:`OpenAICompatTransport.send` call records ``http_code``,
``attempts``, and ``elapsed_ms`` on the returned :class:`WorkerResult`
regardless of branch. Status mapping (per §5 + dispatch.py module
docstring):

* ``success``     -- HTTP 200 and the response body parses to a
                      Chat-Completions shape with a non-empty
                      ``choices[0].message.content``.
* ``parse_error`` -- HTTP 200 but the body is not JSON, lacks
                      ``choices``, or has empty content. The §7.4
                      salvage promotion is a Wave-2 normalize concern
                      (T03 leaves the raw body accessible via
                      ``WorkerResult.body`` for downstream salvage).
* ``proxy_error`` -- any non-200 HTTP status (4xx / 5xx) and any
                      connection / network error short of timeout.
                      The retry-once-on-5xx matrix is enforced by
                      T03.09 ``retry_policy`` wrapping this send call;
                      the transport itself records a single-attempt
                      outcome (``attempts=1``).
* ``timeout``     -- :class:`httpx.TimeoutException` raised inside
                      :meth:`send`. The ``timeout`` argument is the
                      per-call wall-clock budget in seconds
                      (NFR-010 default 180s); ``elapsed_ms`` records
                      the actual elapsed time at the raise point.

The transport stashes the raw response body on a non-dataclass
attribute :attr:`WorkerResult.body` (string, possibly empty) so the
Phase-1 dispatcher can materialize ``raw_path`` without an additional
transport call. The attribute is intentionally not a dataclass field
(it is byte-heavy, not serializable into manifests, and irrelevant
once dispatch has persisted it).

Routing guard (AC-010)
======================

The transport only addresses OpenAI-compatible Chat-Completions
endpoints; native endpoints of the host vendor that invokes the swarm
(the caller's own provider) are out of scope and not reachable from
this surface. The T2 proxy presents an OpenAI-compatible surface
backed by upstream providers; routing constraints live at proxy-config
time. The T03.20 grep test under ``tests/swarm/`` reinforces that no
host-vendor URL or host-vendor model identifier appears in any
transport-config source.

Caching guard (NFR-014 / AC-015)
================================

The transport contains no response-cache layer. Every
:meth:`send` issues a fresh HTTP request. Test
``tests/swarm/test_no_response_cache.py`` (T03.19) reinforces this by
greping the package for forbidden cache imports.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Mapping, Optional

import httpx

from superclaude.cli.swarm.config import (
    T2_MODEL_ENV_PREFIX,
    T2_MODEL_MAX_SLOTS,
    T2_PROXY_KEY_ENV,
    T2_PROXY_URL_ENV,
)
from superclaude.cli.swarm.models import WorkerResult


__all__ = [
    "OpenAICompatTransport",
    "TransportConfig",
    "TransportEnvError",
    "read_env",
]


# NFR-010 -- 180s per-worker timeout default. Mirrors
# ``WorkerSpec.timeout_sec`` so a transport constructed without an
# explicit timeout still honours the contract.
_DEFAULT_TIMEOUT_SEC = 180

# Chat-Completions path appended to the configured base URL. Mirrors
# the OpenAI public API shape; OpenAI-compatible proxies (vLLM, OpenRouter,
# litellm, T2) all serve this endpoint at the same suffix.
_CHAT_COMPLETIONS_PATH = "/chat/completions"


class TransportEnvError(RuntimeError):
    """Raised by :func:`read_env` when required T2 env vars are missing.

    Carries the list of missing variable names so callers (preflight /
    dispatch / the INV-007 contract emitter) can surface a structured
    diagnostic rather than letting httpx fail with an unhelpful
    401 / connection-refused later.
    """

    def __init__(self, missing: tuple[str, ...]) -> None:
        self.missing: tuple[str, ...] = missing
        names = ", ".join(missing) if missing else "(none)"
        super().__init__(
            f"T2 proxy env contract incomplete; missing: {names}. "
            f"Set {T2_PROXY_URL_ENV}, {T2_PROXY_KEY_ENV}, and at least "
            f"one {T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS} slot."
        )


@dataclass(frozen=True)
class TransportConfig:
    """Structured T2 env-var contract (AC-017).

    Emitted by :func:`read_env` and consumed by the dispatcher to
    construct one :class:`OpenAICompatTransport` per worker slot
    (model). The dataclass is ``frozen=True`` so downstream stages
    cannot accidentally rewrite the resolved contract after Wave 0.
    """

    base_url: str
    api_key: str
    models: tuple[str, ...]


def read_env(env: Optional[Mapping[str, str]] = None) -> TransportConfig:
    """Read the T2 proxy env-var contract; raise on missing values.

    Args:
        env: optional mapping to read from (defaults to ``os.environ``).
            Tests pass an explicit dict so construction stays
            deterministic.

    Returns:
        A :class:`TransportConfig` carrying ``base_url`` / ``api_key`` /
        ``models``. ``models`` is dense (empty slots are skipped) and
        ordered by slot index (``T2Model01`` first).

    Raises:
        TransportEnvError: when ``T2ProxyUrl`` / ``T2ProxyKey`` is
            unset / empty, or when no ``T2Model0N`` slot resolves to a
            non-empty value.
    """
    env_map: Mapping[str, str] = env if env is not None else os.environ
    base_url = (env_map.get(T2_PROXY_URL_ENV) or "").strip()
    api_key = (env_map.get(T2_PROXY_KEY_ENV) or "").strip()

    models: list[str] = []
    for index in range(1, T2_MODEL_MAX_SLOTS + 1):
        value = (env_map.get(f"{T2_MODEL_ENV_PREFIX}{index}") or "").strip()
        if value:
            models.append(value)

    missing: list[str] = []
    if not base_url:
        missing.append(T2_PROXY_URL_ENV)
    if not api_key:
        missing.append(T2_PROXY_KEY_ENV)
    if not models:
        missing.append(f"{T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS}")

    if missing:
        raise TransportEnvError(tuple(missing))

    return TransportConfig(
        base_url=base_url,
        api_key=api_key,
        models=tuple(models),
    )


class OpenAICompatTransport:
    """OpenAI-compatible Chat Completions transport via httpx.

    One instance is bound to a single ``model`` identifier; the
    dispatcher constructs N instances (one per slot) from a single
    :class:`TransportConfig`. The transport is thread-safe: ``send``
    issues a fresh request through the shared :class:`httpx.Client`
    (which is itself thread-safe per httpx docs) and never mutates
    instance state.

    Args:
        base_url: OpenAI-compatible base URL
            (e.g. ``https://proxy.example.com/v1``). ``/chat/completions``
            is appended at send time. Trailing slashes are stripped so
            either ``.../v1`` or ``.../v1/`` work.
        api_key: bearer token sent as
            ``Authorization: Bearer <key>``.
        model: per-instance model identifier
            (e.g. ``gpt-5-codex``, ``mistral-large-2407``). One transport
            per worker slot; the dispatcher fans out across N transports.
        client: optional pre-configured :class:`httpx.Client`. Tests
            inject an ``httpx.MockTransport`` here so the protocol-level
            outcome matrix can be exercised without a live network. When
            ``None`` a fresh ``httpx.Client`` is constructed and owned by
            this instance (closed in :meth:`close`).
        temperature: sampling temperature forwarded to the API. Defaults
            to the recipe convention (0.2 -- ``roadmap-haiku-architect.md``
            L100). Per-call override is not exposed at this Phase-1
            reference layer.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        *,
        client: Optional[httpx.Client] = None,
        temperature: float = 0.2,
    ) -> None:
        if not base_url:
            raise ValueError("OpenAICompatTransport.base_url must be non-empty")
        if not api_key:
            raise ValueError("OpenAICompatTransport.api_key must be non-empty")
        if not model:
            raise ValueError("OpenAICompatTransport.model must be non-empty")

        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._owns_client = client is None
        self._client = client if client is not None else httpx.Client()

    @property
    def model(self) -> str:
        """Per-instance model identifier (read-only)."""
        return self._model

    @property
    def endpoint(self) -> str:
        """Fully-qualified chat-completions URL for this transport."""
        return f"{self._base_url}{_CHAT_COMPLETIONS_PATH}"

    def close(self) -> None:
        """Close the underlying httpx client when this transport owns it.

        Tests that inject a client retain ownership and are responsible
        for closing it themselves; this avoids double-close traps.
        """
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "OpenAICompatTransport":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        """Send ``prompt`` to the configured endpoint; return a WorkerResult.

        Records ``http_code`` / ``attempts`` / ``elapsed_ms`` on every
        outcome. Status mapping is documented in the module docstring.
        The raw response body (when available) is stashed on the
        returned ``WorkerResult.body`` attribute so the dispatcher can
        materialize ``raw_path`` without a second call. The ``body``
        attribute is intentionally not a dataclass field -- it is
        byte-heavy and irrelevant to manifest serialization.

        Args:
            prompt: fully-assembled user prompt body. Forwarded verbatim
                as the single user message; the transport MUST NOT
                re-normalize per COMP-031.
            timeout: per-call wall-clock budget in seconds. Translated
                into ``httpx.Timeout(timeout)`` so connect, read, write,
                and pool waits all share the budget.

        Returns:
            A populated :class:`WorkerResult` with ``model_id`` /
            ``model_label`` / ``status`` / ``http_code`` / ``attempts``
            / ``elapsed_ms`` / ``bytes`` set. ``index`` is left at the
            zero default for the dispatcher to stamp at the fan-out
            site.
        """
        effective_timeout = timeout if timeout and timeout > 0 else _DEFAULT_TIMEOUT_SEC
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self._temperature,
        }

        start = time.monotonic()
        try:
            response = self._client.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=httpx.Timeout(float(effective_timeout)),
            )
        except httpx.TimeoutException:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            return self._build_result(
                status="timeout",
                http_code=None,
                elapsed_ms=elapsed_ms,
                body="",
            )

        elapsed_ms = int((time.monotonic() - start) * 1000)
        body_text = response.text or ""

        if response.status_code != 200:
            return self._build_result(
                status="proxy_error",
                http_code=response.status_code,
                elapsed_ms=elapsed_ms,
                body=body_text,
            )

        content = self._extract_content(body_text)
        if content is None:
            return self._build_result(
                status="parse_error",
                http_code=response.status_code,
                elapsed_ms=elapsed_ms,
                body=body_text,
            )

        return self._build_result(
            status="success",
            http_code=response.status_code,
            elapsed_ms=elapsed_ms,
            body=content,
        )

    def _build_result(
        self,
        *,
        status: str,
        http_code: Optional[int],
        elapsed_ms: int,
        body: str,
    ) -> WorkerResult:
        """Stamp a WorkerResult with transport-side metrics + body attr."""
        result = WorkerResult(
            model_id=self._model,
            model_label=self._model,
            bytes=len(body.encode("utf-8")),
            status=status,  # type: ignore[arg-type]
            http_code=http_code,
            attempts=1,
            elapsed_ms=elapsed_ms,
        )
        # Stash the body on a non-dataclass attribute so the dispatcher
        # can materialise raw_path without a second transport call. Not
        # a dataclass field -- byte-heavy, not relevant to manifest
        # round-trip.
        result.body = body  # type: ignore[attr-defined]
        return result

    @staticmethod
    def _extract_content(body_text: str) -> Optional[str]:
        """Pull ``choices[0].message.content`` from an OpenAI-compat JSON body.

        Returns the content string on success, or ``None`` when the
        body fails to parse / lacks the expected shape / yields an
        empty content string. ``None`` drives the ``parse_error``
        branch in :meth:`send`.
        """
        try:
            payload = json.loads(body_text)
        except json.JSONDecodeError:
            return None
        if not isinstance(payload, dict):
            return None
        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices:
            return None
        first = choices[0]
        if not isinstance(first, dict):
            return None
        message = first.get("message")
        if not isinstance(message, dict):
            return None
        content = message.get("content")
        if not isinstance(content, str) or not content:
            return None
        return content
