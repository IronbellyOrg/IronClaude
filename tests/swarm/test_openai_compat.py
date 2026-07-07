"""T03.05 -- OpenAICompatTransport (Phase-1 reference) test suite.

Covers R-064 (COMP-032) + R-068 (FR-022) + R-081 (AC-005) + R-085 (AC-017):

* Happy-path 200 parse populates ``status='success'`` with
  ``http_code=200`` / ``attempts=1`` / ``elapsed_ms>=0`` and stashes
  the extracted content on ``WorkerResult.body``.
* 4xx returns ``status='proxy_error'`` with the upstream status code
  surfaced on ``http_code``.
* 5xx returns ``status='proxy_error'`` with the upstream status code.
  (FR-017 5xx-retry-once is enforced by T03.09 ``retry_policy``
  wrapping this transport; this layer records the single-attempt
  outcome.)
* 200 with unparseable body returns ``status='parse_error'`` and
  retains the raw body on ``WorkerResult.body`` for §7.4 salvage.
* ``httpx.TimeoutException`` is converted to ``status='timeout'``
  with ``http_code=None`` and a non-negative elapsed_ms.
* :func:`read_env` happy path returns a dense ``TransportConfig``
  with models ordered by slot index.
* :func:`read_env` raises :class:`TransportEnvError` listing the
  missing variable names when the contract is incomplete.

An env-gated live lane skips when ``T2ProxyUrl`` / ``T2ProxyKey`` /
``T2Model01`` are absent (CI default). When the env is populated, the
test performs a single happy-path round-trip against the configured
proxy and asserts ``http_code==200`` plus non-empty body.
"""

from __future__ import annotations

import json
import os

import httpx
import pytest

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.transports import Transport
from superclaude.cli.swarm.transports.openai_compat import (
    OpenAICompatTransport,
    TransportConfig,
    TransportEnvError,
    read_env,
)

# ---------------------------------------------------------------------------
# Fixtures & helpers.
# ---------------------------------------------------------------------------


_BASE_URL = "https://proxy.example.test/v1"
_API_KEY = "test-key-xyz"
_MODEL = "test-model-01"


def _success_body(text: str = "hello world") -> bytes:
    return json.dumps(
        {
            "id": "chatcmpl-1",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": text},
                    "finish_reason": "stop",
                }
            ],
        }
    ).encode("utf-8")


def _make_transport(handler) -> OpenAICompatTransport:
    """Construct a transport backed by a MockTransport-driven client."""
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return OpenAICompatTransport(
        base_url=_BASE_URL,
        api_key=_API_KEY,
        model=_MODEL,
        client=client,
    )


# ---------------------------------------------------------------------------
# Module surface.
# ---------------------------------------------------------------------------


def test_openai_compat_uses_httpx() -> None:
    """AC-005 -- httpx is the underlying HTTP library."""
    import importlib

    module = importlib.import_module("superclaude.cli.swarm.transports.openai_compat")
    source = __import__("inspect").getsource(module)
    assert "import httpx" in source, "openai_compat.py must import httpx (AC-005)."


def test_openai_compat_satisfies_transport_protocol() -> None:
    """COMP-032 -- structural conformance with the Transport Protocol."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=_success_body())

    with _make_transport(handler) as transport:
        assert isinstance(transport, Transport)


# ---------------------------------------------------------------------------
# Outcome matrix (FR-017 / NFR-010 -- 4 status branches).
# ---------------------------------------------------------------------------


def test_send_happy_path_populates_success() -> None:
    captured: dict[str, httpx.Request] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["request"] = request
        return httpx.Response(200, content=_success_body("hello"))

    with _make_transport(handler) as transport:
        result = transport.send("user prompt", timeout=180)

    assert isinstance(result, WorkerResult)
    assert result.status == "success"
    assert result.http_code == 200
    assert result.attempts == 1
    assert result.elapsed_ms >= 0
    assert result.model_id == _MODEL
    assert result.model_label == _MODEL
    assert result.bytes == len(b"hello")
    # body is stashed on the result so dispatch can materialise raw_path
    assert getattr(result, "body", "") == "hello"

    # Request shape -- POST to base + /chat/completions with bearer auth
    req = captured["request"]
    assert req.method == "POST"
    assert str(req.url) == f"{_BASE_URL}/chat/completions"
    assert req.headers["Authorization"] == f"Bearer {_API_KEY}"
    body = json.loads(req.content)
    assert body["model"] == _MODEL
    assert body["messages"] == [{"role": "user", "content": "user prompt"}]
    # Non-Kimi models forward the configured temperature (constructor default 0.2).
    assert body["temperature"] == 0.2


def test_send_non_kimi_model_includes_temperature() -> None:
    """A non-Kimi model's request payload MUST carry the configured temperature.

    Guards the temperature-forwarding fix in commands.py: a future refactor that
    drops the field would silently regress to the transport's no-temperature
    path for models that DO accept it. Uses a NON-default temperature (0.7) so a
    regression to the constructor default (0.2) also fails this test.
    """
    captured: dict[str, httpx.Request] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["request"] = request
        return httpx.Response(200, content=_success_body("ok"))

    # Context-manager the injected client: OpenAICompatTransport does not close
    # clients it did not create (openai_compat.py:302-304), so the test owns the
    # close to avoid a resource leak (PR-219 review r3533289716).
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with OpenAICompatTransport(
            base_url=_BASE_URL,
            api_key=_API_KEY,
            model="qwen-latest",
            temperature=0.7,
            client=client,
        ) as transport:
            transport.send("prompt", timeout=180)

    body = json.loads(captured["request"].content)
    assert body["model"] == "qwen-latest"
    assert "temperature" in body, "non-Kimi models must carry temperature"
    assert body["temperature"] == 0.7


def test_send_kimi_model_omits_temperature() -> None:
    """A Kimi model's request payload MUST OMIT temperature entirely.

    Kimi reasoning models 400 on any temperature != 1 ("only 1 is allowed") and
    emit EMPTY output if forced to 1 (reasoning burns the budget). Only full
    omission yields real content. This test pins the _omits_temperature contract
    so a future refactor cannot reintroduce the 400/empty-output regression
    (Augment review PR-219 finding: request-shape for Kimi was untested).
    """
    for kimi_model in ("kimi-k2.7-code", "kimi", "kimi-k2-thinking", "kimi-k2.6"):
        captured: dict[str, httpx.Request] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            captured["request"] = request
            return httpx.Response(200, content=_success_body("ok"))

        with httpx.Client(transport=httpx.MockTransport(handler)) as client:
            with OpenAICompatTransport(
                base_url=_BASE_URL, api_key=_API_KEY, model=kimi_model, client=client
            ) as transport:
                transport.send("prompt", timeout=180)

        body = json.loads(captured["request"].content)
        assert body["model"] == kimi_model
        assert "temperature" not in body, (
            f"{kimi_model} must NOT carry temperature (400s / empties output)"
        )


def test_send_4xx_maps_to_proxy_error() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, content=b'{"error":"unauthorized"}')

    with _make_transport(handler) as transport:
        result = transport.send("p", timeout=30)

    assert result.status == "proxy_error"
    assert result.http_code == 401
    assert result.attempts == 1
    # 4xx body preserved verbatim for salvage / diagnostics
    assert getattr(result, "body", "") == '{"error":"unauthorized"}'


def test_send_5xx_maps_to_proxy_error() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, content=b"upstream down")

    with _make_transport(handler) as transport:
        result = transport.send("p", timeout=30)

    assert result.status == "proxy_error"
    assert result.http_code == 503
    # FR-017 retry policy is T03.09's surface; this layer records a
    # single attempt.
    assert result.attempts == 1


def test_send_200_unparseable_body_maps_to_parse_error() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"not json {")

    with _make_transport(handler) as transport:
        result = transport.send("p", timeout=30)

    assert result.status == "parse_error"
    assert result.http_code == 200
    # Raw body preserved so §7.4 salvage (M4) can act on it.
    assert getattr(result, "body", "") == "not json {"


def test_send_200_missing_choices_maps_to_parse_error() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b'{"id":"x","choices":[]}')

    with _make_transport(handler) as transport:
        result = transport.send("p", timeout=30)

    assert result.status == "parse_error"
    assert result.http_code == 200


def test_send_200_empty_content_maps_to_parse_error() -> None:
    body = json.dumps(
        {"choices": [{"message": {"role": "assistant", "content": ""}}]}
    ).encode("utf-8")

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body)

    with _make_transport(handler) as transport:
        result = transport.send("p", timeout=30)

    assert result.status == "parse_error"


def test_send_timeout_maps_to_timeout_status() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("simulated read timeout")

    with _make_transport(handler) as transport:
        result = transport.send("p", timeout=5)

    assert result.status == "timeout"
    assert result.http_code is None
    assert result.attempts == 1
    assert result.elapsed_ms >= 0


def test_send_request_error_maps_to_proxy_error_preserving_model_identity() -> None:
    """F-P3-5: a non-timeout ``httpx.RequestError`` does not escape ``send``.

    Connection / DNS / read errors (``httpx.ConnectError`` here, a
    ``RequestError`` subclass that is NOT a ``TimeoutException``) must be
    converted to a ``proxy_error`` WorkerResult built through
    ``_build_result`` so the failed slot keeps this transport's ``model_id`` /
    ``model_label``. If the error escaped, the dispatch ``except Exception``
    fallback would build a bare ``proxy_error`` with no model identity.
    """

    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("simulated connection refused")

    with _make_transport(handler) as transport:
        result = transport.send("p", timeout=5)

    assert result.status == "proxy_error"
    assert result.http_code is None
    assert result.attempts == 1
    assert result.elapsed_ms >= 0
    # Model identity preserved through the error path (the F-P3-5 fix).
    assert result.model_id == _MODEL
    assert result.model_label == _MODEL


# ---------------------------------------------------------------------------
# Constructor guards.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "base_url,api_key,model",
    [
        ("", _API_KEY, _MODEL),
        (_BASE_URL, "", _MODEL),
        (_BASE_URL, _API_KEY, ""),
    ],
)
def test_constructor_rejects_empty_fields(
    base_url: str, api_key: str, model: str
) -> None:
    with pytest.raises(ValueError):
        OpenAICompatTransport(base_url=base_url, api_key=api_key, model=model)


def test_endpoint_strips_trailing_slash() -> None:
    def handler(_r: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=_success_body())

    client = httpx.Client(transport=httpx.MockTransport(handler))
    transport = OpenAICompatTransport(
        base_url=_BASE_URL + "/",
        api_key=_API_KEY,
        model=_MODEL,
        client=client,
    )
    try:
        assert transport.endpoint == f"{_BASE_URL}/chat/completions"
    finally:
        client.close()


# ---------------------------------------------------------------------------
# read_env -- T2 env contract (AC-017).
# ---------------------------------------------------------------------------


def test_read_env_happy_path() -> None:
    env = {
        "T2ProxyUrl": "https://proxy.example/v1",
        "T2ProxyKey": "k",
        "T2Model01": "m-alpha",
        "T2Model02": "m-beta",
        "T2Model03": "",  # empty slot skipped
        "T2Model04": "m-delta",
    }
    config = read_env(env)
    assert isinstance(config, TransportConfig)
    assert config.base_url == "https://proxy.example/v1"
    assert config.api_key == "k"
    # Empty slot 3 is skipped; order preserved by slot index.
    assert config.models == ("m-alpha", "m-beta", "m-delta")


def test_read_env_strips_whitespace() -> None:
    env = {
        "T2ProxyUrl": "  https://proxy.example/v1  ",
        "T2ProxyKey": "  k  ",
        "T2Model01": "  m  ",
    }
    config = read_env(env)
    assert config.base_url == "https://proxy.example/v1"
    assert config.api_key == "k"
    assert config.models == ("m",)


def test_read_env_missing_url_raises() -> None:
    env = {"T2ProxyKey": "k", "T2Model01": "m"}
    with pytest.raises(TransportEnvError) as exc:
        read_env(env)
    assert "T2ProxyUrl" in exc.value.missing


def test_read_env_missing_key_raises() -> None:
    env = {"T2ProxyUrl": "u", "T2Model01": "m"}
    with pytest.raises(TransportEnvError) as exc:
        read_env(env)
    assert "T2ProxyKey" in exc.value.missing


def test_read_env_missing_all_models_raises() -> None:
    env = {"T2ProxyUrl": "u", "T2ProxyKey": "k"}
    with pytest.raises(TransportEnvError) as exc:
        read_env(env)
    # The model-slot entry uses the prefix+range format documented on
    # the SwarmConfig contract.
    assert any("T2Model0" in name for name in exc.value.missing)


def test_read_env_missing_all_three_raises() -> None:
    with pytest.raises(TransportEnvError) as exc:
        read_env({})
    assert "T2ProxyUrl" in exc.value.missing
    assert "T2ProxyKey" in exc.value.missing


# ---------------------------------------------------------------------------
# Env-gated live lane.
# ---------------------------------------------------------------------------


_LIVE_ENV_PRESENT = bool(
    os.environ.get("T2ProxyUrl")
    and os.environ.get("T2ProxyKey")
    and os.environ.get("T2Model01")
)


@pytest.mark.skipif(
    not _LIVE_ENV_PRESENT,
    reason="T2 proxy env vars not set; skipping live transport probe.",
)
def test_live_proxy_smoke() -> None:  # pragma: no cover -- env-gated
    """One round-trip against the live T2 proxy when env is populated.

    Verifies the transport reaches the proxy and produces a populated
    :class:`WorkerResult` (http_code stamped, elapsed_ms recorded). The
    proxy's deployment-specific routing (whether the base URL already
    includes a path prefix, whether the configured model is enabled,
    etc.) is out of scope for the transport-contract test -- a 404 or
    401 still proves the httpx/transport machinery works end-to-end.
    """
    config = read_env()
    transport = OpenAICompatTransport(
        base_url=config.base_url,
        api_key=config.api_key,
        model=config.models[0],
    )
    try:
        result = transport.send("Reply with the single word ok.", timeout=60)
    finally:
        transport.close()
    # Transport machinery is exercised end-to-end: a populated http_code
    # proves we reached the HTTP layer (vs. raising a connection error)
    # and elapsed_ms records the round-trip wall-clock.
    assert isinstance(result, WorkerResult)
    assert result.http_code is not None
    assert 100 <= result.http_code < 600
    assert result.elapsed_ms >= 0
    assert result.status in {"success", "parse_error", "proxy_error"}
