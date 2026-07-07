"""Network-free stub replay of the 2026-07-05 incident + counter-case (§8).

Drives the REAL ``run_fallback_ladder`` controller over injected
``dispatch`` / ``normalize`` / ``stamp`` stubs (no transport, no ``ClaudeProcess``,
no network), then feeds the controller's contributing set + ``t2_fallback``
metadata through the REAL ``build_reflect_contract`` -> ``derive_verdict`` path.
Every asserted signal (tier_reached / reviewer_count / verdict / certified) is
COMPUTED from the real controller + contract, never copied from a fixture.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest

from superclaude.cli.reflect import fallback as fallback_module
from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.contract import derive_verdict
from superclaude.cli.reflect.ensemble import (
    REFLECT_REVIEW_RECIPE,
    build_reflect_contract,
    resolve_t1_fallback_factory,
)
from superclaude.cli.reflect.fallback import run_fallback_ladder
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.swarm.commands import ModelPoolTooSmallError
from superclaude.cli.swarm.models import WorkerResult, WorkerStatus
from superclaude.cli.swarm.transports.openai_compat import TransportEnvError


def _primary(index: int, status: WorkerStatus, model_id: str) -> WorkerResult:
    return WorkerResult(
        index=index,
        status=status,
        model_id=model_id,
        model_label=model_id,
        final_path=f"/tmp/reflect-out/t2-swarm/primary-{index:02d}.final.md",
    )


def _raw_fallback(status: WorkerStatus, model_id: str) -> WorkerResult:
    # Raw dispatch output: no final_path yet (the stamp seam fills it — F2).
    return WorkerResult(index=0, status=status, model_id=model_id, model_label=model_id)


def _make_dispatch(outcomes: list[WorkerResult]):
    """Return a dispatch stub that yields one crafted WorkerResult per attempt.

    The controller dispatches one slot per iteration in ladder order, so the
    queue order is (T1Model01, then T1Model02).
    """
    queue = list(outcomes)

    def _dispatch(preflight, *, transport_for_slot=None, prompt="", worker_spec=None):
        # Touch the slot adapter so the eager-resolved transport path is exercised.
        if transport_for_slot is not None:
            transport_for_slot(0)
        return [queue.pop(0)]

    return _dispatch


def _stamp(workers: list[WorkerResult], output_dir) -> list[WorkerResult]:
    """Stamp a stable final_path (F2: stamp BEFORE normalize)."""
    stamped: list[WorkerResult] = []
    for i, worker in enumerate(workers):
        base = str(Path(output_dir) / f"fallback-{i:02d}")
        stamped.append(
            dataclasses.replace(
                worker,
                path=f"{base}.final.md",
                raw_path=f"{base}.raw.md",
                meta_path=f"{base}.meta.json",
                final_path=f"{base}.final.md",
            )
        )
    return stamped


def _normalize(workers, recipe_name, *, recipe_args=None, **_kwargs):
    """Passthrough normalize stub (no salvage promotion / no mutation)."""
    return list(workers)


def _trivial_factory(_slot_name: str) -> object:
    return object()


def _incident_primaries() -> list[WorkerResult]:
    # §8 incident SHAPE: one surviving primary at index 1, flanked by two terminal
    # fallback-eligible failures at index 0 (proxy_error) and index 2 (parse_error).
    # The eligible failures therefore carry attempt ids ``primary:00`` / ``primary:02``.
    return [
        _primary(0, "proxy_error", "qwen-primary"),
        _primary(1, "success", "deepseek-primary"),
        _primary(2, "parse_error", "gpt-primary"),
    ]


def _config(temp_tasklist: Path):
    config = resolve_config(
        str(temp_tasklist),
        depth="deep",
        model="test-model",
        transport="stub",
        reviewers=3,
    )
    # Stub defaults fallback OFF; force ON for this stub-lane replay.
    return dataclasses.replace(config, tier2_fallback_enabled=True)


def _raising_transport_env_factory(_slot_name: str) -> object:
    """A fallback factory that RAISES ``TransportEnvError`` on call (D1).

    Mirrors the ``openai_compat`` arm's LAZY env read failing when the T1 proxy
    contract is incomplete: the factory raises the moment the controller CALLS it
    inside ``_dispatch_one_fallback`` (before any dispatch), so this exercises the
    ``except (TransportEnvError, ModelPoolTooSmallError)`` fold in
    ``run_fallback_ladder``.
    """
    raise TransportEnvError(("T1ProxyUrl", "T1ProxyKey", "T1Model01"))


def _raising_pool_too_small_factory(_slot_name: str) -> object:
    """A fallback factory that RAISES ``ModelPoolTooSmallError`` on call (D1).

    The sibling failure mode of ``_raising_transport_env_factory``: a T1 pool
    smaller than the requested ladder position. ``make_fallback_slot_factory``
    raises this from inside the returned factory, so it too must fold into
    ``fallback_config_missing`` rather than escaping the controller.
    """
    raise ModelPoolTooSmallError(1, 2)


@contextmanager
def _closing_factory(factory) -> Iterator[object]:
    """Wrap a fallback factory so every transport it hands back is closed (D3).

    The ``openai_compat`` real-binding factory constructs live
    ``OpenAICompatTransport`` instances, each of which owns an ``httpx.Client``
    opened at construction. Without an explicit close those clients leak
    (``ResourceWarning`` at GC). This tracks every transport the factory returns
    and closes it in ``finally`` so the real-binding assertions run network-free
    AND client-leak-free. ``httpx.Client.close`` is idempotent, so a repeated
    slot->model binding is safe to close twice.
    """
    opened: list[object] = []

    def _tracked(slot_name: str) -> object:
        transport = factory(slot_name)
        opened.append(transport)
        return transport

    try:
        yield _tracked
    finally:
        for transport in opened:
            close = getattr(transport, "close", None)
            if callable(close):
                close()


def test_incident_replay_certifies_tier2_with_fallback(
    temp_tasklist, patch_git
) -> None:
    config = _config(temp_tasklist)
    outcome = run_fallback_ladder(
        primaries=_incident_primaries(),
        config=config,
        transport_for_fallback_slot=_trivial_factory,
        prompt="review target",
        swarm_output_dir=Path(config.output_dir) / "t2-swarm",
        stamp=_stamp,
        dispatch=_make_dispatch([_raw_fallback("success", "gemini-fallback")]),
        normalize=_normalize,
        deadline_monotonic=None,
    )

    # Contributing set is exactly the surviving primary + the fallback success.
    model_ids = [w.model_id for w in outcome.contributing_workers]
    assert model_ids == ["deepseek-primary", "gemini-fallback"]

    # F2: the fallback worker carries a stable non-empty final_path.
    fallback_worker = outcome.contributing_workers[1]
    assert fallback_worker.final_path
    assert fallback_worker.final_path.endswith(".final.md")

    # Metadata: certified with fallback, primary failures preserved EXACTLY (a
    # regression preserving the wrong/partial failure set must fail this, so the
    # assert is on exact contents, not truthiness).
    assert outcome.metadata["certified_with_fallback"] is True
    assert outcome.metadata["terminal_reason"] == "certified_t2_with_fallback"
    assert outcome.metadata["primary_failures_preserved"] == [
        "primary:00",
        "primary:02",
    ]
    # Engagement bookkeeping (parity with the counter-case asserts).
    assert outcome.metadata["engaged"] is True
    assert outcome.metadata["fallback_attempt_count"] == 1
    assert outcome.metadata["exhausted"] is False

    contract = build_reflect_contract(
        outcome.contributing_workers,
        adversarial_convergence_score=0.86,
        t2_fallback=outcome.metadata,
    )
    assert contract is not None
    assert contract["tier_reached"] == 2
    assert contract["reviewer_count"] == 2
    assert contract["merge_method"] == "adversarial"

    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_counter_case_both_fallbacks_fail_stays_degraded_tier1(
    temp_tasklist, patch_git
) -> None:
    config = _config(temp_tasklist)
    outcome = run_fallback_ladder(
        primaries=_incident_primaries(),
        config=config,
        transport_for_fallback_slot=_trivial_factory,
        prompt="review target",
        swarm_output_dir=Path(config.output_dir) / "t2-swarm",
        stamp=_stamp,
        dispatch=_make_dispatch(
            [
                _raw_fallback("proxy_error", "gemini-fallback"),
                _raw_fallback("proxy_error", "llama-fallback"),
            ]
        ),
        normalize=_normalize,
        deadline_monotonic=None,
    )

    # Contributing set collapses back to the single surviving primary.
    model_ids = [w.model_id for w in outcome.contributing_workers]
    assert model_ids == ["deepseek-primary"]
    assert outcome.metadata["certified_with_fallback"] is False
    assert outcome.metadata["terminal_reason"] == "fallback_pool_exhausted"
    assert outcome.metadata["exhausted"] is True

    contract = build_reflect_contract(
        outcome.contributing_workers,
        adversarial_convergence_score=0.86,
        t2_fallback=outcome.metadata,
    )
    assert contract is not None
    assert contract["tier_reached"] == 1
    assert contract["reviewer_count"] == 1
    assert contract["merge_method"] == "single-reviewer-fallback"

    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11
    assert result.reason == "degraded-tier1"


@pytest.mark.parametrize(
    "raising_factory",
    [_raising_transport_env_factory, _raising_pool_too_small_factory],
    ids=["transport_env_error", "model_pool_too_small"],
)
def test_raising_fallback_factory_folds_into_config_missing(
    temp_tasklist, patch_git, raising_factory
) -> None:
    """P5-ACT-D1: a fallback factory that RAISES on call is folded by the REAL
    ``run_fallback_ladder`` controller into ``terminal_reason:
    fallback_config_missing`` (never escaping to crash the run).

    Drives the controller with the §8 incident SHAPE (one surviving primary +
    two fallback-eligible failures) so the planner decides to DISPATCH the first
    ladder slot. The factory raises inside ``_dispatch_one_fallback`` BEFORE any
    dispatch, so the dispatch stub queue is intentionally empty. This is the test
    that FAILS if the ``except (TransportEnvError, ModelPoolTooSmallError)`` fold
    at ``fallback.py`` is broken -- a regression there would let the exception
    propagate out of the controller.
    """
    config = _config(temp_tasklist)
    outcome = run_fallback_ladder(
        primaries=_incident_primaries(),
        config=config,
        transport_for_fallback_slot=raising_factory,
        prompt="review target",
        swarm_output_dir=Path(config.output_dir) / "t2-swarm",
        stamp=_stamp,
        # Empty queue: the factory raises before dispatch is ever invoked.
        dispatch=_make_dispatch([]),
        normalize=_normalize,
        deadline_monotonic=None,
    )

    assert outcome.metadata["terminal_reason"] == "fallback_config_missing"
    assert outcome.metadata["certified_with_fallback"] is False
    # The contributing set stayed exactly the single surviving primary; the raised
    # factory contributed no fallback reviewer.
    assert [w.model_id for w in outcome.contributing_workers] == ["deepseek-primary"]


def test_resolve_t1_fallback_factory_stub_arm_returns_live_transport() -> None:
    """The stub arm resolves a live transport-like object without raising."""
    stub_factory = resolve_t1_fallback_factory(
        "stub", ladder=("T1Model01", "T1Model02")
    )
    transport = stub_factory("T1Model01")
    # A transport-like object: exposes the ``model`` identity + a ``send`` callable.
    assert transport is not None
    assert hasattr(transport, "send")
    assert transport.model  # non-empty per-instance model_id


def test_resolve_t1_fallback_factory_openai_compat_missing_env_degrades() -> None:
    """Phase 5 (real binding enabled): with the T1 proxy binding confirmed, the
    openai_compat arm reads the real T1 pool LAZILY. An empty/incomplete T1 env
    (passed explicitly so the check is deterministic, never touching os.environ or
    the real proxy) raises ``TransportEnvError`` on the factory CALL, which
    ``run_fallback_ladder`` folds into ``terminal_reason: fallback_config_missing``.
    """
    factory = resolve_t1_fallback_factory(
        "openai_compat", ladder=("T1Model01", "T1Model02"), env={}
    )
    with pytest.raises(TransportEnvError):
        factory("T1Model01")


def test_resolve_t1_fallback_factory_openai_compat_real_binding_is_slot_name_keyed() -> (
    None
):
    """Phase 5 (Step 5.3): the enabled openai_compat arm binds each ladder slot NAME
    to a DISTINCT T1 pool model by ladder position (F1) via make_fallback_slot_factory,
    reading the dedicated T1 proxy contract from the injected env (never the real
    proxy). Network-free: OpenAICompatTransport is constructed but never `.send()`-ed.

    D3: every constructed transport is closed via ``_closing_factory`` so the owned
    ``httpx.Client`` never leaks (no ResourceWarning).
    """
    env = {
        "T1ProxyUrl": "http://t1-proxy:4000/cli",
        "T1ProxyKey": "unit-test-key",
        "T1Model01": "qwen-t1",
        "T1Model02": "deepseek-t1",
    }
    factory = resolve_t1_fallback_factory(
        "openai_compat", ladder=("T1Model01", "T1Model02"), env=env
    )
    # F1: slot NAME -> distinct pool model by ladder position (never pool[0] twice).
    with _closing_factory(factory) as bind:
        assert bind("T1Model01").model == "qwen-t1"
        assert bind("T1Model02").model == "deepseek-t1"


def test_resolve_t1_fallback_factory_openai_compat_binding_is_positional_not_name() -> (
    None
):
    """P5-ACT-D2: prove the binding is by LADDER POSITION (``ladder[i] -> pool[i]``),
    NOT by matching the slot NAME to a same-named env key.

    Uses a REVERSED ladder whose slot names DIVERGE from the env pool order. The
    pool is read by slot index (``T1Model01`` -> ``qwen-t1`` at pool[0],
    ``T1Model02`` -> ``deepseek-t1`` at pool[1]), but the ladder is
    ``("T1Model02", "T1Model01")`` -- so ladder position 0 (``T1Model02``) MUST
    bind pool[0] (``qwen-t1``) and ladder position 1 (``T1Model01``) MUST bind
    pool[1] (``deepseek-t1``). A name-lookup misimplementation would instead bind
    ``T1Model02 -> deepseek-t1`` (its same-named env slot), failing this test.

    D3: transports closed via ``_closing_factory`` so no httpx client leaks.
    """
    env = {
        "T1ProxyUrl": "http://p",
        "T1ProxyKey": "k",
        "T1Model01": "qwen-t1",
        "T1Model02": "deepseek-t1",
    }
    factory = resolve_t1_fallback_factory(
        "openai_compat", ladder=("T1Model02", "T1Model01"), env=env
    )
    with _closing_factory(factory) as bind:
        # Ladder position 0 is slot NAME "T1Model02" -> pool[0] == "qwen-t1".
        assert bind("T1Model02").model == "qwen-t1"
        # Ladder position 1 is slot NAME "T1Model01" -> pool[1] == "deepseek-t1".
        assert bind("T1Model01").model == "deepseek-t1"


# ---------------------------------------------------------------------------
# F4 wall-clock coverage at the run_fallback_ladder controller level (§7.4).
#
# The controller reads the clock INTERNALLY via ``time.monotonic()`` (fallback.py
# ``run_fallback_ladder`` line 438) against the injected ``deadline_monotonic``;
# there is no injected ``now`` param. So (a) an already-past deadline is expressed
# as a monotonic value guaranteed to leave < the 1.0s floor of budget, and (b) a
# mid-range deadline is made deterministic by freezing ``fallback.time.monotonic``.
# ---------------------------------------------------------------------------


def test_wall_clock_exhausted_deadline_never_dispatches(
    temp_tasklist, patch_git
) -> None:
    """§7.4 F4: an already-exhausted run deadline stops the ladder BEFORE any
    dispatch. A deadline at monotonic time ``0.0`` is always in the deep past
    relative to ``time.monotonic()`` (a large positive process uptime), so
    ``remaining = 0.0 - now`` is far below the ``_FALLBACK_WALL_CLOCK_FLOOR_SEC``
    (1.0s) floor on the very first iteration. The planner returns
    ``fallback_wall_clock_exhausted`` and the dispatch spy is never called."""
    config = _config(temp_tasklist)
    dispatch_calls: list[object] = []

    def _spy_dispatch(
        preflight, *, transport_for_slot=None, prompt="", worker_spec=None
    ):
        dispatch_calls.append(worker_spec)
        return [_raw_fallback("success", "gemini-fallback")]

    outcome = run_fallback_ladder(
        primaries=_incident_primaries(),
        config=config,
        transport_for_fallback_slot=_trivial_factory,
        prompt="review target",
        swarm_output_dir=Path(config.output_dir) / "t2-swarm",
        stamp=_stamp,
        dispatch=_spy_dispatch,
        normalize=_normalize,
        # Monotonic time 0.0 == a deadline in the deep past (now >> 0.0), so
        # remaining < the 1.0s floor immediately.
        deadline_monotonic=0.0,
    )

    # The dispatch spy is NEVER called: the ladder refused to start an attempt.
    assert dispatch_calls == []
    # Exact terminal_reason token (verified against fallback.py TERMINAL_REASONS).
    assert outcome.metadata["terminal_reason"] == "fallback_wall_clock_exhausted"
    # Zero fallback attempts were made / recorded.
    assert outcome.metadata["fallback_attempt_count"] == 0
    assert outcome.metadata["engaged"] is False
    # The contributing set stayed the single surviving primary (no top-up).
    assert [w.model_id for w in outcome.contributing_workers] == ["deepseek-primary"]


def test_wall_clock_remaining_clamps_attempt_timeout(
    temp_tasklist, patch_git, monkeypatch
) -> None:
    """§7.4 F4: a mid-range remaining deadline still permits one attempt, but the
    per-attempt ``timeout_sec`` is clamped to ``min(config.timeout_seconds,
    remaining)``. ``fallback.time.monotonic`` is frozen so ``remaining`` is exact:
    with a frozen now of 1000.0 and a deadline of 1120.0, remaining == 120.0, which
    is far below ``config.timeout_seconds`` (3600), so the clamp MUST bite and the
    dispatched ``worker_spec.timeout_sec`` MUST equal 120."""
    config = _config(temp_tasklist)
    # The clamp source: resolve_config with no explicit --timeout defaults to 3600.
    assert config.timeout_seconds == 3600

    # Freeze the controller's clock so remaining is deterministic (== 120.0).
    monkeypatch.setattr(fallback_module.time, "monotonic", lambda: 1000.0)
    deadline = 1000.0 + 120.0  # remaining == 120 < timeout_seconds (3600)

    captured_timeouts: list[int] = []

    def _spy_dispatch(
        preflight, *, transport_for_slot=None, prompt="", worker_spec=None
    ):
        if transport_for_slot is not None:
            transport_for_slot(0)
        captured_timeouts.append(worker_spec.timeout_sec)
        return [_raw_fallback("success", "gemini-fallback")]

    outcome = run_fallback_ladder(
        primaries=_incident_primaries(),
        config=config,
        transport_for_fallback_slot=_trivial_factory,
        prompt="review target",
        swarm_output_dir=Path(config.output_dir) / "t2-swarm",
        stamp=_stamp,
        dispatch=_spy_dispatch,
        normalize=_normalize,
        deadline_monotonic=deadline,
    )

    # Exactly one attempt (the success fallback certifies quorum, ending the loop),
    # and its per-attempt timeout was clamped to remaining (120), NOT the raw 3600.
    assert captured_timeouts == [120]
    assert captured_timeouts[0] < config.timeout_seconds
    # The clamped attempt still succeeded and certified with fallback.
    assert outcome.metadata["terminal_reason"] == "certified_t2_with_fallback"
    assert outcome.metadata["fallback_attempt_count"] == 1


# ---------------------------------------------------------------------------
# M4: recipe-literal drift guard. ``fallback._REFLECT_REVIEW_RECIPE`` and
# ``ensemble.REFLECT_REVIEW_RECIPE`` are two INDEPENDENT literals (duplicated to
# break the ensemble<->fallback import cycle Phase 1 exists to sever). This guard
# fails if a future edit changes one recipe token without the other.
# ---------------------------------------------------------------------------


def test_fallback_and_ensemble_review_recipe_literals_match() -> None:
    """The independently-defined reviewer normalize recipe tokens must stay equal:
    ``fallback._REFLECT_REVIEW_RECIPE`` == ``ensemble.REFLECT_REVIEW_RECIPE``. The
    duplication (not a shared import) exists ONLY to break the import cycle -- their
    VALUES must never drift, or a fallback reviewer would normalize under a different
    recipe than a primary reviewer."""
    assert fallback_module._REFLECT_REVIEW_RECIPE == REFLECT_REVIEW_RECIPE
