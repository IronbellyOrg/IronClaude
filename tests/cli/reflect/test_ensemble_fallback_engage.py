"""Ensemble-level Tier-2 fallback GATE integration (P3-ACT-001/004/005).

Unlike ``test_ensemble_fallback_stub.py`` (which drives ``run_fallback_ladder``
in isolation, so the ``tier2_fallback_enabled`` flag is inert), these tests drive
the REAL ``run_tier2_ensemble`` -- the function that actually OWNS the
``config.tier2_fallback_enabled`` gate, wires the real ``stamp=_stamp_worker_paths``
seam (P3-ACT-004), and resolves the real ``resolve_t1_fallback_factory("stub")``
arm (P3-ACT-005 stub arm). The proof is therefore that ENABLING engages the ladder
and certifies Tier-2 with a fallback, while DISABLING byte-skips the ladder and
degrades to Tier-1 -- exactly the enable/disable behavior the flag exists for.

Network-free: slot 0 is a real vendor-distinct ``StubTransport`` success; slots 1
and 2 are ``_FailingTransport`` (proxy_error). No transport, no ``ClaudeProcess``,
no network. Every asserted signal is COMPUTED from the real ensemble + contract,
never copied from a fixture. ``_FailingTransport`` and ``_const_score`` mirror the
patterns in ``test_ensemble_stub_integration.py``.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import yaml

from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.contract import derive_verdict, parse_contract
from superclaude.cli.reflect.ensemble import (
    AdversarialResult,
    run_tier2_ensemble,
    stub_model_id,
)
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.transports.stub import StubTransport

_FIXED_SCORE = 0.86


def _const_score(_paths: list[str], _out: Path) -> AdversarialResult:
    """Clean-default adversarial result injected through the production seam.

    A non-None convergence score with no deviation/regression signal, so the
    healthy-ensemble ENGAGE run routes PASS without launching the adversarial
    ``ClaudeProcess`` child.
    """
    return AdversarialResult(
        convergence_score=_FIXED_SCORE,
        regression_present=False,
        unauthorized_deviation_present=False,
        needs_human_decision=False,
        deviation_count_by_class={
            "authorized": 0,
            "necessary": 0,
            "drift": 0,
            "regression": 0,
        },
        report_path=None,
    )


class _FailingTransport:
    """Network-free transport whose ``send`` always reports ``proxy_error``.

    ``http_code=None`` => the §7 retry matrix's ``other`` bucket: no retry, the
    proxy_error stands, and ``reduce_wave3`` does NOT count it toward M. This makes
    the slot a fallback-ELIGIBLE primary failure so the ladder has work to do.
    """

    def __init__(self, model_id: str) -> None:
        self._model_id = model_id

    @property
    def model(self) -> str:
        return self._model_id

    def send(self, prompt: str, timeout: int) -> WorkerResult:  # noqa: ARG002
        result = WorkerResult(
            model_id=self._model_id,
            model_label=self._model_id,
            status="proxy_error",
            http_code=None,
            attempts=1,
        )
        result.body = ""  # type: ignore[attr-defined]
        return result


def _factory(slot_index: int):
    """Slot 0 -> vendor-distinct StubTransport success; slots 1/2 -> proxy_error.

    One surviving primary + two fallback-eligible primary failures is the §8
    incident shape at the ensemble seam.
    """
    if slot_index == 0:
        return StubTransport(model_id=stub_model_id(0))
    return _FailingTransport(f"stub-model-{slot_index:02d}")


def _all_success_factory(slot_index: int):
    """All 3 slots -> vendor-distinct StubTransport successes (healthy pool)."""
    return StubTransport(model_id=stub_model_id(slot_index))


def _base_config(temp_tasklist: Path):
    return resolve_config(
        str(temp_tasklist),
        depth="deep",
        model="test-model",
        transport="stub",
        reviewers=3,
    )


def test_gate_on_engages_ladder_and_certifies_tier2(
    temp_tasklist, patch_git, tmp_path
) -> None:
    """ENGAGE: with ``tier2_fallback_enabled=True`` the ensemble runs the real
    T1 fallback ladder (real ``resolve_t1_fallback_factory("stub")`` +
    ``_stamp_worker_paths``), tops the 1 surviving primary up with the stub
    fallback success, and certifies Tier-2. 1 surviving primary (vendor-distinct)
    + the stub fallback success = distinct vendors -> certify.
    """
    base = _base_config(temp_tasklist)
    # resolve_config forces stub fallback OFF; force it ON at the ensemble gate.
    config_on = dataclasses.replace(
        base, tier2_fallback_enabled=True, output_dir=tmp_path / "on"
    )

    run_tier2_ensemble(
        config_on,
        transport_for_slot=_factory,
        adversarial_score_fn=_const_score,
    )
    contract = parse_contract(config_on.contract_path)

    assert contract is not None
    # The ladder engaged and certified with a fallback.
    assert contract["t2_fallback"] is not None
    assert contract["t2_fallback"]["engaged"] is True
    assert contract["t2_fallback"]["certified_with_fallback"] is True
    # Tier-2 restored: the fallback repaired the quorum.
    assert contract["tier_reached"] == 2
    assert contract["reviewer_count"] == 2

    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_gate_on_healthy_pool_not_mismarked_partial_full_reviewer_count(
    temp_tasklist, patch_git, tmp_path
) -> None:
    """REGRESSION (PR #220 / Augment high finding): a HEALTHY fallback-ENABLED run
    where all 3 primaries succeed must NOT be mis-marked ``partial`` and must report
    the FULL reviewer_count.

    The ensemble hands ``reduce_wave3`` (and ``build_reflect_contract``) the full
    augmented worker set (``ladder_outcome.all_workers``), NOT the smallest
    certifying subset. Feeding the trimmed subset (size 2) with
    ``workers_requested=3`` made ``determine_status`` see ``M(2) < N(3)`` and mark
    the swarm subrun ``partial`` even though every primary succeeded, and
    under-reported ``reviewer_count`` (2 instead of 3). Both assertions below fail
    against that pre-fix behavior.
    """
    base = _base_config(temp_tasklist)
    config_on = dataclasses.replace(
        base, tier2_fallback_enabled=True, output_dir=tmp_path / "healthy"
    )

    run_tier2_ensemble(
        config_on,
        transport_for_slot=_all_success_factory,
        adversarial_score_fn=_const_score,
    )
    contract = parse_contract(config_on.contract_path)

    assert contract is not None
    # Primaries already met quorum -> the ladder did NOT need to engage.
    if contract.get("t2_fallback") is not None:
        assert contract["t2_fallback"]["engaged"] is False
    # reviewer_count reflects ALL 3 succeeding reviewers, NOT the trimmed subset (2).
    assert contract["reviewer_count"] == 3
    assert contract["tier_reached"] == 2

    # The swarm subrun status is computed over the full worker set: 3 succeeded of
    # 3 requested -> ``success``, NOT ``partial``. This is the exact regression the
    # Augment finding described.
    swarm_contract = yaml.safe_load(
        (config_on.output_dir / "t2-swarm" / "return-contract.yaml").read_text()
    )
    assert swarm_contract["status"] == "success"
    assert swarm_contract["workers_failed"] == 0

    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_gate_off_skips_ladder_and_degrades_tier1(
    temp_tasklist, patch_git, tmp_path
) -> None:
    """SKIP: with ``tier2_fallback_enabled=False`` the ladder is byte-skipped
    (``t2_fallback`` absent), the single surviving primary is the only reviewer,
    and the run degrades to Tier-1. This is the disabled path staying byte-
    equivalent to today.
    """
    base = _base_config(temp_tasklist)
    # Stub already resolves False; be explicit + isolate the contract dir.
    config_off = dataclasses.replace(
        base, tier2_fallback_enabled=False, output_dir=tmp_path / "off"
    )

    run_tier2_ensemble(
        config_off,
        transport_for_slot=_factory,
        adversarial_score_fn=_const_score,
    )
    contract = parse_contract(config_off.contract_path)

    assert contract is not None
    # The ladder was byte-skipped: no t2_fallback metadata block.
    assert "t2_fallback" not in contract or contract.get("t2_fallback") is None
    # Collapses to the single surviving primary at Tier-1.
    assert contract["tier_reached"] == 1
    assert contract["reviewer_count"] == 1

    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11
    assert result.reason == "degraded-tier1"
