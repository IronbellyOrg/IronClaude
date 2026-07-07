"""Unit tests for additive reflect Tier-2 fallback metadata."""

import pytest
import yaml

from superclaude.cli.reflect.contract import derive_verdict
from superclaude.cli.reflect.ensemble import build_reflect_contract
from superclaude.cli.reflect.fallback import build_fallback_metadata
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.swarm.models import WorkerResult


def _worker(index: int, status: str, model_id: str) -> WorkerResult:
    return WorkerResult(
        index=index,
        status=status,
        model_id=model_id,
        final_path=f"/tmp/reflect-out/worker-{index}.md",
    )


def _attempt_ledger() -> list[dict]:
    return [
        {
            "attempt_id": "primary:00",
            "role": "primary",
            "model_id": "qwen-primary",
            "vendor": "qwen",
            "status": "proxy_error",
            "failure_class": "proxy_error",
            "fallback_for": None,
            "fallback_reason": None,
            "contributes_to_quorum": False,
        },
        {
            "attempt_id": "primary:01",
            "role": "primary",
            "model_id": "deepseek-primary",
            "vendor": "deepseek",
            "status": "success",
            "failure_class": None,
            "fallback_for": None,
            "fallback_reason": None,
            "contributes_to_quorum": True,
        },
        {
            "attempt_id": "primary:02",
            "role": "primary",
            "model_id": "gpt-primary",
            "vendor": "openai",
            "status": "parse_error",
            "failure_class": "parse_error",
            "fallback_for": None,
            "fallback_reason": None,
            "contributes_to_quorum": False,
        },
        {
            "attempt_id": "fallback:T1Model01",
            "role": "fallback",
            "model_id": "qwen-fallback",
            "vendor": "qwen",
            "status": "success",
            "failure_class": None,
            "fallback_for": ["primary:00", "primary:02"],
            "fallback_reason": "primary_terminal_failure",
            "contributes_to_quorum": True,
        },
    ]


def _fallback_metadata() -> dict:
    return build_fallback_metadata(
        ladder=("T1Model01", "T1Model02"),
        engaged=True,
        attempt_ledger=_attempt_ledger(),
        contributing_ids=["primary:01", "fallback:T1Model01"],
        primary_failures=["primary:00", "primary:02"],
        terminal_reason="certified_t2_with_fallback",
        certification_basis="primary_plus_fallback_quorum",
        original_primary_pool_fully_succeeded=False,
    )


def _passing_workers() -> list[WorkerResult]:
    return [
        _worker(1, "success", "deepseek-primary"),
        _worker(3, "success", "qwen-fallback"),
    ]


def _build_contract(t2_fallback: dict | None = None) -> dict:
    contract = build_reflect_contract(
        _passing_workers(),
        adversarial_convergence_score=0.86,
        t2_fallback=t2_fallback,
    )
    assert contract is not None
    return contract


def test_reviewer_count_uses_contributing_workers_not_attempt_ledger() -> None:
    metadata = _fallback_metadata()
    contract = _build_contract(t2_fallback=metadata)

    assert contract["reviewer_count"] == 2
    assert len(contract["t2_fallback"]["reviewer_attempts"]) == 4


def test_populated_fallback_metadata_does_not_change_verdict() -> None:
    without_fallback = derive_verdict(
        _build_contract(), expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    with_fallback = derive_verdict(
        _build_contract(t2_fallback=_fallback_metadata()),
        expected_tier=2,
        allow_single_vendor=False,
        child_rc=0,
    )

    assert without_fallback.verdict is Verdict.PASS
    assert with_fallback.verdict is without_fallback.verdict
    assert with_fallback.verdict.exit_code == without_fallback.verdict.exit_code
    # P2-HON-002: additive fallback telemetry must not alter the returned reason
    # text either (a PASS/0 with a changed reason slug would still be dishonest).
    assert with_fallback.reason == without_fallback.reason


def test_degraded_with_fallback_metadata_keeps_real_verdict_reason() -> None:
    """Design §8 counter-case: a degraded Tier-1 / single-reviewer-fallback outcome
    that ALSO carries a populated ``t2_fallback`` block (terminal_reason
    ``fallback_pool_exhausted``, certification_basis ``not_certified``) must STILL
    return the real first-match verdict reason ``degraded-tier1``. The additive
    fallback telemetry is never allowed to change or soften the verdict.

    Exactly ONE successful worker -> ``reviewer_count == 1`` -> ``tier_reached == 1``
    -> ``merge_method`` ``single-reviewer-fallback`` (``build_reflect_contract``
    returns None for zero successes, so one success is the minimal degraded shape).
    With ``expected_tier == 2`` the degraded ladder's first match is trigger 6
    (expected-T2-but-ran-T1) -> ``degraded-tier1``, which precedes the trigger-10
    ``single-reviewer-fallback`` slug -- proving the honest first-match reason wins."""
    metadata = build_fallback_metadata(
        ladder=("T1Model01", "T1Model02"),
        engaged=True,
        attempt_ledger=_attempt_ledger(),
        contributing_ids=["primary:01"],
        primary_failures=["primary:00", "primary:02"],
        terminal_reason="fallback_pool_exhausted",
        certification_basis="not_certified",
        original_primary_pool_fully_succeeded=False,
    )
    contract = build_reflect_contract(
        [_worker(1, "success", "deepseek-primary")],
        adversarial_convergence_score=0.86,
        t2_fallback=metadata,
    )
    assert contract is not None
    assert contract["reviewer_count"] == 1
    assert contract["tier_reached"] == 1
    assert contract["merge_method"] == "single-reviewer-fallback"

    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )

    assert result.reason == "degraded-tier1"
    assert contract["t2_fallback"]["terminal_reason"] == "fallback_pool_exhausted"


def test_primary_failures_are_preserved_even_when_fallback_certifies() -> None:
    metadata = _fallback_metadata()

    assert metadata["certified_with_fallback"] is True
    assert metadata["primary_failures_preserved"] == ["primary:00", "primary:02"]


def test_tier2_certification_basis_distinguishes_fallback_from_primary_only() -> None:
    fallback_metadata = _fallback_metadata()
    primary_only = build_fallback_metadata(
        ladder=("T1Model01", "T1Model02"),
        engaged=False,
        attempt_ledger=[],
        contributing_ids=["primary:00", "primary:01"],
        primary_failures=[],
        terminal_reason="not_needed_primary_quorum_met",
        certification_basis="primary_only_quorum",
        original_primary_pool_fully_succeeded=True,
    )

    assert (
        fallback_metadata["tier2_certification_basis"] == "primary_plus_fallback_quorum"
    )
    assert primary_only["tier2_certification_basis"] == "primary_only_quorum"
    assert primary_only["certified_with_fallback"] is False


def test_build_fallback_metadata_rejects_unknown_terminal_reason() -> None:
    """An unknown ``terminal_reason`` fails loudly with the offending token named.

    ``build_fallback_metadata`` guards ``terminal_reason`` against the closed
    ``TERMINAL_REASONS`` tuple (checked BEFORE ``certification_basis``); an unknown
    token raises ``ValueError`` whose message includes the token so a producer bug
    is diagnosable, not silently written into the contract."""
    with pytest.raises(ValueError) as excinfo:
        build_fallback_metadata(
            ladder=("T1Model01", "T1Model02"),
            engaged=True,
            attempt_ledger=_attempt_ledger(),
            contributing_ids=["primary:01"],
            primary_failures=["primary:00"],
            terminal_reason="not_a_real_reason",
            certification_basis="primary_plus_fallback_quorum",
            original_primary_pool_fully_succeeded=False,
        )
    assert "not_a_real_reason" in str(excinfo.value)


def test_build_fallback_metadata_rejects_unknown_certification_basis() -> None:
    """An unknown ``certification_basis`` fails loudly with the offending token named.

    ``terminal_reason`` is kept valid (``certified_t2_with_fallback``) so the guard
    under test is the ``certification_basis`` membership check against
    ``TIER2_CERTIFICATION_BASES``; an unknown token raises ``ValueError`` whose
    message includes the offending ``bogus`` token."""
    with pytest.raises(ValueError) as excinfo:
        build_fallback_metadata(
            ladder=("T1Model01", "T1Model02"),
            engaged=True,
            attempt_ledger=_attempt_ledger(),
            contributing_ids=["primary:01"],
            primary_failures=["primary:00"],
            terminal_reason="certified_t2_with_fallback",
            certification_basis="bogus",
            original_primary_pool_fully_succeeded=False,
        )
    assert "bogus" in str(excinfo.value)


def test_contract_metadata_does_not_leak_proxy_secret_names_or_urls() -> None:
    dumped = yaml.safe_dump(_build_contract(t2_fallback=_fallback_metadata()))

    # P2-HON-003: guard both env-var-name fragments AND lower-case/value leak
    # shapes (proxy urls, keys, and raw endpoints). ``proxy_error`` is a
    # legitimate WorkerStatus telemetry token and is deliberately NOT forbidden.
    forbidden_tokens = (
        "ProxyUrl",
        "ProxyKey",
        "T1ProxyKey",
        "T2ProxyKey",
        "T1ProxyUrl",
        "T2ProxyUrl",
        "proxy_url",
        "proxy_key",
        "api_key",
        "base_url",
        "http://",
        "https://",
        ":4000/cli",
    )
    for forbidden in forbidden_tokens:
        assert forbidden not in dumped, f"leaked proxy secret token: {forbidden!r}"
