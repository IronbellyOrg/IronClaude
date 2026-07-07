"""D2 guard: openai_compat per-slot factory must fail loudly when the env
model pool is smaller than the worker count (instead of silently wrapping via
``pool[i % len(pool)]`` and reusing models).

Reflect finding D2 (post-perworker-models audit): INV-005 validates
``workers.count`` against ``spec.workers.models`` (lens placeholders), NOT the
live ``T2Model0N`` env pool the factory actually binds. So a job can pass
preflight yet have fewer real models than workers. The guard lives in
``_resolve_run_transport_factory`` and raises :class:`ModelPoolTooSmallError`
eagerly (before any slot dispatches), surfaced at the CLI as EXIT_INVALID via
the existing "cannot construct transport" path.

These tests are env-injected and network-free: the guard raises before any
``OpenAICompatTransport`` is constructed, so no proxy call is made.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXIT_INVALID,
    ModelPoolTooSmallError,
    _resolve_run_transport_factory,
)

# A complete T2 env contract with a 2-model pool (read_env reads from this dict).
_ENV_2 = {
    "T2ProxyUrl": "http://proxy.example/cli/v1",
    "T2ProxyKey": "sk-test",
    "T2Model01": "model-a",
    "T2Model02": "model-b",
}


def test_factory_raises_when_pool_smaller_than_workers():
    """pool=2, workers=3 -> ModelPoolTooSmallError naming both counts."""
    with pytest.raises(ModelPoolTooSmallError) as excinfo:
        _resolve_run_transport_factory("openai_compat", env=_ENV_2, workers_requested=3)
    err = excinfo.value
    assert err.pool_size == 2
    assert err.workers_requested == 3
    assert "2 model(s)" in str(err) and "3 worker(s)" in str(err)


def test_factory_ok_when_pool_equals_workers():
    """pool=2, workers=2 -> returns a usable per-slot factory (no raise)."""
    factory = _resolve_run_transport_factory(
        "openai_compat", env=_ENV_2, workers_requested=2
    )
    assert callable(factory)
    # Slots 0 and 1 bind distinct models (no wraparound at the boundary).
    assert factory(0)._model == "model-a"
    assert factory(1)._model == "model-b"


def test_factory_ok_when_pool_larger_than_workers():
    """pool=2, workers=1 -> fine (a subset of the pool is used)."""
    factory = _resolve_run_transport_factory(
        "openai_compat", env=_ENV_2, workers_requested=1
    )
    assert callable(factory)
    assert factory(0)._model == "model-a"


def test_factory_skips_check_when_workers_requested_none():
    """Backward-compat: workers_requested=None disables the guard entirely."""
    factory = _resolve_run_transport_factory("openai_compat", env=_ENV_2)
    assert callable(factory)  # no raise even though we don't know the count


def test_stub_factory_unaffected_by_guard():
    """The guard is openai_compat-only; stub never raises on pool size."""
    factory = _resolve_run_transport_factory("stub", models=["x"], workers_requested=99)
    assert callable(factory)


def test_factory_forwards_temperature_to_transport():
    """The factory MUST forward the JobSpec temperature into OpenAICompatTransport.

    Closes the PR-219 review gap (discussion_r3533289712): the transport-level
    tests only asserted the constructor DEFAULT (0.2), so a regression where
    ``_resolve_run_transport_factory`` stopped forwarding ``temperature`` would
    still pass. This test exercises the actual forwarding path (factory -> ctor)
    with a non-default value and asserts the transport received EXACTLY that
    value -- not the constructor default.

    Note: this asserts the transport's resolved ``_temperature``; the request-
    payload-level behavior (Kimi omits, non-Kimi sends) is covered in
    test_openai_compat.py.
    """
    factory = _resolve_run_transport_factory(
        "openai_compat", env=_ENV_2, workers_requested=2, temperature=0.7
    )
    transport = factory(0)
    assert transport._temperature == 0.7, (
        "factory must forward the non-default temperature into the transport, "
        "not fall back to the 0.2 constructor default"
    )


def test_factory_omits_temperature_falls_back_to_default():
    """temperature=None (the run path when the JobSpec omits it) MUST leave the
    transport on its constructor default -- i.e. forwarding is opt-in, not
    forced. Guards against a regression that unconditionally injects None."""
    factory = _resolve_run_transport_factory(
        "openai_compat", env=_ENV_2, workers_requested=2
    )
    transport = factory(0)
    assert transport._temperature == 0.2  # constructor default preserved


def test_run_cmd_pool_too_small_exits_invalid(tmp_path: Path, monkeypatch):
    """End-to-end wiring: a 3-worker lens with a 1-model env pool exits
    EXIT_INVALID with the guard message, before any dispatch/network."""
    monkeypatch.setenv("T2ProxyUrl", "http://proxy.example/cli/v1")
    monkeypatch.setenv("T2ProxyKey", "sk-test")
    monkeypatch.setenv("T2Model01", "only-one-model")
    for i in range(2, 10):
        monkeypatch.delenv(f"T2Model0{i}", raising=False)

    target = tmp_path / "t.py"
    target.write_text(
        "def calculate_total(items, rate):\n"
        "    total = 0\n"
        "    for it in items:\n"
        "        total = total - it.price\n"
        "    return total + total * rate\n"
    )
    out = tmp_path / "out"
    result = CliRunner().invoke(
        swarm_group,
        [
            "run",
            "--lens",
            "bare-review",  # 3 workers
            "--target",
            str(target),
            "--output",
            str(out),
            "--transport",
            "openai_compat",
        ],
    )
    assert result.exit_code == EXIT_INVALID, result.output
    assert "cannot construct 'openai_compat' transport" in result.output
    assert "model pool has 1 model(s) but the job requests 3 worker(s)" in result.output
