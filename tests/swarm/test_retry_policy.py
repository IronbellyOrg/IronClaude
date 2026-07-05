"""T03.09 -- ``retry_policy`` FR-017/NFR-010/NFR-011 matrix test suite.

Pins the §7 retry/timeout matrix exactly:

* ``200`` (success)              -> attempts=1, no backoff, no retry
* ``4xx`` (proxy_error 400..499) -> attempts=1, no backoff, no retry
* ``5xx`` (proxy_error 500..599) -> attempts=2, backoff sleep called
                                    exactly once with the configured
                                    ``on_5xx_backoff_sec`` value
* ``timeout``                    -> attempts=1, no backoff, no retry
* ``network`` (proxy_error,      -> attempts=1, no backoff, no retry
   http_code=None)                  (covers connection / DNS / TLS
                                    failures + raised non-Timeout
                                    exceptions)

Additional pins:

* ``5xx -> 200`` second attempt succeeds: attempts=2, status='success'.
* ``5xx -> 5xx`` second attempt also 5xx: attempts=2, status='proxy_error'
  (single retry only, never escalates to a third attempt).
* ``elapsed_ms`` accumulates transport wall-clock across both
  attempts on the retry branch; backoff itself is excluded so the
  metric reflects transport work.
* ``RetryPolicy(on_5xx=False)`` disables the 5xx branch -> attempts=1
  even on 5xx (proves the policy flag is consulted, not hardcoded).
* ``WorkerSpec.timeout_sec`` is forwarded to ``transport.send`` so
  the per-call budget matches the dispatcher's contract.

Network branch: covered by both a ``proxy_error`` WorkerResult with
``http_code=None`` AND a raised non-Timeout exception (connection /
DNS / TLS failure surface). Both paths terminate with attempts=1
because §7 has no ``on_network`` retry flag.
"""

from __future__ import annotations

from typing import Optional

import pytest

from superclaude.cli.swarm.dispatch import retry_policy
from superclaude.cli.swarm.models import RetryPolicy, WorkerResult, WorkerSpec

# ---------------------------------------------------------------------------
# Recording-stub helpers.
# ---------------------------------------------------------------------------


class _ScriptedTransport:
    """Transport that returns / raises a scripted sequence of outcomes.

    Each entry is either:

    * a :class:`WorkerResult` -- returned verbatim from ``send``.
    * a :class:`BaseException` instance -- raised from ``send``.

    Records every ``(prompt, timeout)`` invocation so tests can assert
    the per-call timeout was honoured and the call count matches the
    matrix branch.
    """

    def __init__(self, outcomes: list[object]) -> None:
        self._outcomes = list(outcomes)
        self._cursor = 0
        self.calls: list[tuple[str, int]] = []

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        self.calls.append((prompt, timeout))
        if self._cursor >= len(self._outcomes):
            raise AssertionError(
                "scripted transport exhausted -- test asked for "
                f"{self._cursor + 1} calls but only scripted "
                f"{len(self._outcomes)} outcomes"
            )
        outcome = self._outcomes[self._cursor]
        self._cursor += 1
        if isinstance(outcome, BaseException):
            raise outcome
        assert isinstance(outcome, WorkerResult)
        return outcome


class _RecordingSleep:
    """``time.sleep`` stub recording every backoff call."""

    def __init__(self) -> None:
        self.calls: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.calls.append(float(seconds))


def _success(http_code: int = 200) -> WorkerResult:
    return WorkerResult(
        status="success",
        http_code=http_code,
        attempts=1,
        elapsed_ms=10,
    )


def _proxy_error(http_code: Optional[int]) -> WorkerResult:
    return WorkerResult(
        status="proxy_error",
        http_code=http_code,
        attempts=1,
        elapsed_ms=7,
    )


def _timeout() -> WorkerResult:
    return WorkerResult(
        status="timeout",
        http_code=None,
        attempts=1,
        elapsed_ms=180_000,
    )


def _parse_error() -> WorkerResult:
    return WorkerResult(
        status="parse_error",
        http_code=200,
        attempts=1,
        elapsed_ms=5,
    )


# ---------------------------------------------------------------------------
# §7 retry matrix -- parametrized over the five terminal classes.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "branch,outcomes,expected_status,expected_http,expected_attempts,expected_backoff_calls",
    [
        pytest.param(
            "200",
            [_success(200)],
            "success",
            200,
            1,
            0,
            id="200_no_retry",
        ),
        pytest.param(
            "4xx",
            [_proxy_error(400)],
            "proxy_error",
            400,
            1,
            0,
            id="4xx_no_retry",
        ),
        pytest.param(
            "4xx",
            [_proxy_error(404)],
            "proxy_error",
            404,
            1,
            0,
            id="404_no_retry",
        ),
        pytest.param(
            "4xx",
            [_proxy_error(429)],
            "proxy_error",
            429,
            1,
            0,
            id="429_no_retry",
        ),
        pytest.param(
            "5xx_then_success",
            [_proxy_error(503), _success(200)],
            "success",
            200,
            2,
            1,
            id="5xx_retry_then_200",
        ),
        pytest.param(
            "5xx_then_5xx",
            [_proxy_error(502), _proxy_error(502)],
            "proxy_error",
            502,
            2,
            1,
            id="5xx_retry_then_5xx",
        ),
        pytest.param(
            "5xx_500",
            [_proxy_error(500), _success(200)],
            "success",
            200,
            2,
            1,
            id="5xx_500_retry_then_200",
        ),
        pytest.param(
            "5xx_599",
            [_proxy_error(599), _success(200)],
            "success",
            200,
            2,
            1,
            id="5xx_599_retry_then_200",
        ),
        pytest.param(
            "timeout",
            [_timeout()],
            "timeout",
            None,
            1,
            0,
            id="timeout_no_retry",
        ),
        pytest.param(
            "network",
            [_proxy_error(None)],
            "proxy_error",
            None,
            1,
            0,
            id="network_no_retry",
        ),
        pytest.param(
            "parse_error",
            [_parse_error()],
            "parse_error",
            200,
            1,
            0,
            id="parse_error_no_retry",
        ),
    ],
)
def test_retry_policy_matrix(
    branch: str,
    outcomes: list[object],
    expected_status: str,
    expected_http: Optional[int],
    expected_attempts: int,
    expected_backoff_calls: int,
) -> None:
    """§7 retry matrix: every branch produces the exact attempts+status+http_code."""
    transport = _ScriptedTransport(outcomes)
    sleep = _RecordingSleep()
    spec = WorkerSpec()  # FR-017 / NFR-011 defaults

    result = retry_policy(transport, prompt="hello", spec=spec, sleep_fn=sleep)

    assert result.status == expected_status
    assert result.http_code == expected_http
    assert result.attempts == expected_attempts
    assert len(transport.calls) == expected_attempts
    # Every call honours the NFR-010 180s budget by default.
    assert all(timeout == 180 for _prompt, timeout in transport.calls)
    # Backoff sleep called once on retry branches, never on no-retry.
    assert len(sleep.calls) == expected_backoff_calls
    if expected_backoff_calls:
        assert sleep.calls == [float(spec.retry.on_5xx_backoff_sec)]


# ---------------------------------------------------------------------------
# Network / raised-exception branches (no http_code observed).
# ---------------------------------------------------------------------------


def test_retry_policy_raised_timeout_no_retry() -> None:
    """``TimeoutError`` raised by the transport -> ``status='timeout'`` once."""
    transport = _ScriptedTransport([TimeoutError("budget exhausted")])
    sleep = _RecordingSleep()

    result = retry_policy(transport, prompt="x", spec=WorkerSpec(), sleep_fn=sleep)

    assert result.status == "timeout"
    assert result.http_code is None
    assert result.attempts == 1
    assert len(transport.calls) == 1
    assert sleep.calls == []


def test_retry_policy_raised_network_error_no_retry() -> None:
    """Non-Timeout exception -> ``status='proxy_error'`` (network branch) once."""
    transport = _ScriptedTransport([ConnectionError("DNS failure")])
    sleep = _RecordingSleep()

    result = retry_policy(transport, prompt="x", spec=WorkerSpec(), sleep_fn=sleep)

    assert result.status == "proxy_error"
    assert result.http_code is None
    assert result.attempts == 1
    assert len(transport.calls) == 1
    assert sleep.calls == []


# ---------------------------------------------------------------------------
# Policy flag honoured: ``on_5xx=False`` disables the retry branch.
# ---------------------------------------------------------------------------


def test_retry_policy_honours_on_5xx_flag() -> None:
    """``RetryPolicy(on_5xx=False)`` -> 5xx is NOT retried; attempts=1."""
    transport = _ScriptedTransport([_proxy_error(503)])
    sleep = _RecordingSleep()
    spec = WorkerSpec(retry=RetryPolicy(on_5xx=False))

    result = retry_policy(transport, prompt="x", spec=spec, sleep_fn=sleep)

    assert result.status == "proxy_error"
    assert result.http_code == 503
    assert result.attempts == 1
    assert len(transport.calls) == 1
    assert sleep.calls == []


def test_retry_policy_honours_on_4xx_flag() -> None:
    """``RetryPolicy(on_4xx=True)`` -> 4xx IS retried once."""
    transport = _ScriptedTransport([_proxy_error(429), _success(200)])
    sleep = _RecordingSleep()
    spec = WorkerSpec(retry=RetryPolicy(on_4xx=True))

    result = retry_policy(transport, prompt="x", spec=spec, sleep_fn=sleep)

    assert result.status == "success"
    assert result.http_code == 200
    assert result.attempts == 2
    assert len(transport.calls) == 2
    # Backoff also applies on the 4xx branch when policy enables it.
    assert sleep.calls == [float(spec.retry.on_5xx_backoff_sec)]


def test_retry_policy_honours_on_timeout_flag() -> None:
    """``RetryPolicy(on_timeout=True)`` -> timeout IS retried once."""
    transport = _ScriptedTransport([_timeout(), _success(200)])
    sleep = _RecordingSleep()
    spec = WorkerSpec(retry=RetryPolicy(on_timeout=True))

    result = retry_policy(transport, prompt="x", spec=spec, sleep_fn=sleep)

    assert result.status == "success"
    assert result.http_code == 200
    assert result.attempts == 2
    assert len(transport.calls) == 2
    assert sleep.calls == [float(spec.retry.on_5xx_backoff_sec)]


# ---------------------------------------------------------------------------
# Timeout forwarding -- ``WorkerSpec.timeout_sec`` reaches transport.send.
# ---------------------------------------------------------------------------


def test_retry_policy_forwards_configured_timeout() -> None:
    """``WorkerSpec.timeout_sec=42`` -> ``transport.send`` called with 42."""
    transport = _ScriptedTransport([_success(200)])
    spec = WorkerSpec(timeout_sec=42)

    retry_policy(transport, prompt="x", spec=spec, sleep_fn=lambda _s: None)

    assert transport.calls == [("x", 42)]


def test_retry_policy_default_timeout_180() -> None:
    """Default ``WorkerSpec`` -> ``transport.send`` called with 180."""
    transport = _ScriptedTransport([_success(200)])

    retry_policy(transport, prompt="x", spec=None, sleep_fn=lambda _s: None)

    assert transport.calls == [("x", 180)]


def test_retry_policy_zero_timeout_falls_back_to_default() -> None:
    """``WorkerSpec.timeout_sec=0`` falls back to the NFR-010 180s default."""
    transport = _ScriptedTransport([_success(200)])
    spec = WorkerSpec(timeout_sec=0)

    retry_policy(transport, prompt="x", spec=spec, sleep_fn=lambda _s: None)

    assert transport.calls == [("x", 180)]


# ---------------------------------------------------------------------------
# Elapsed-ms accumulation across the retry branch.
# ---------------------------------------------------------------------------


def test_retry_policy_accumulates_elapsed_across_retry() -> None:
    """``elapsed_ms`` is the sum of transport wall-clock across attempts.

    The two attempts each report a non-zero ``elapsed_ms`` (10ms + 7ms
    via the helper fixtures); the returned result carries the sum
    (17ms), with backoff *not* included (policy overhead, not
    transport work).
    """
    transport = _ScriptedTransport([_proxy_error(503), _success(200)])
    sleep = _RecordingSleep()

    result = retry_policy(transport, prompt="x", spec=WorkerSpec(), sleep_fn=sleep)

    assert result.attempts == 2
    # _proxy_error helper stamps elapsed_ms=7; _success helper stamps 10.
    assert result.elapsed_ms == 17


# ---------------------------------------------------------------------------
# Zero / negative backoff: never call sleep.
# ---------------------------------------------------------------------------


def test_retry_policy_skips_sleep_when_backoff_zero() -> None:
    """``on_5xx_backoff_sec=0`` -> retry happens but sleep is not invoked."""
    transport = _ScriptedTransport([_proxy_error(503), _success(200)])
    sleep = _RecordingSleep()
    spec = WorkerSpec(retry=RetryPolicy(on_5xx=True, on_5xx_backoff_sec=0))

    result = retry_policy(transport, prompt="x", spec=spec, sleep_fn=sleep)

    assert result.status == "success"
    assert result.attempts == 2
    assert sleep.calls == []


# ---------------------------------------------------------------------------
# Docstring contract: dispatch.retry_policy module docstring carries the
# §7 matrix table. T03.09 acceptance: "Retry matrix table in dispatch.py
# docstring matches §7 exactly."
# ---------------------------------------------------------------------------


def test_dispatch_module_docstring_carries_retry_matrix_table() -> None:
    """``dispatch.py`` module docstring lists every §7 matrix row."""
    import superclaude.cli.swarm.dispatch as dispatch_mod

    doc = dispatch_mod.__doc__ or ""
    # Every named outcome class appears in the docstring matrix.
    for token in ("success", "proxy_error", "5xx", "4xx", "timeout"):
        assert token in doc, f"dispatch.py docstring missing matrix row token {token!r}"
    # FR-017 / NFR-010 / NFR-011 explicit references anchor the matrix
    # to its driving requirement IDs.
    assert "FR-017" in doc
    assert "NFR-010" in doc
    assert "NFR-011" in doc
