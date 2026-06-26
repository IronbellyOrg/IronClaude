"""Unit tests for ``contract.derive_verdict`` -- the §6 verdict/exit matrix.

Calls ``derive_verdict`` directly against the fixture contracts and asserts the
exact ``Verdict`` and its ``.exit_code`` (==0/10/11/2, never just !=0), covering
the first-match-wins ordering blocked -> degraded -> halted -> pass.
"""

from __future__ import annotations

import yaml

from superclaude.cli.reflect.contract import derive_verdict
from superclaude.cli.reflect.models import Verdict

from .conftest import FIXTURES_DIR


def _load(name: str) -> dict:
    return yaml.safe_load((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def test_pass_full_tier2() -> None:
    """A clean full non-degraded Tier-2 contract -> pass / exit 0."""
    result = derive_verdict(
        _load("pass.yaml"), expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_halted_regression() -> None:
    """status partial + regression -> halted / exit 10."""
    result = derive_verdict(
        _load("halted_regression.yaml"),
        expected_tier=2,
        allow_single_vendor=False,
        child_rc=0,
    )
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10


def test_degraded_serena() -> None:
    """degraded_components contains serena -> degraded / exit 11."""
    result = derive_verdict(
        _load("degraded_serena.yaml"),
        expected_tier=2,
        allow_single_vendor=False,
        child_rc=0,
    )
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11


def test_degraded_expected_t2_ran_t1() -> None:
    """status success but tier_reached 1 while expecting 2 -> degraded / 11."""
    result = derive_verdict(
        _load("degraded_tier1.yaml"),
        expected_tier=2,
        allow_single_vendor=False,
        child_rc=0,
    )
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11


def test_single_vendor_degraded_without_flag() -> None:
    """single vendor -> degraded / 11 when --allow-single-vendor is NOT set."""
    result = derive_verdict(
        _load("degraded_single_vendor.yaml"),
        expected_tier=2,
        allow_single_vendor=False,
        child_rc=0,
    )
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11


def test_single_vendor_pass_with_flag() -> None:
    """single vendor -> pass / 0 when --allow-single-vendor IS set."""
    result = derive_verdict(
        _load("degraded_single_vendor.yaml"),
        expected_tier=2,
        allow_single_vendor=True,
        child_rc=0,
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_blocked_missing_contract() -> None:
    """No contract (None) -> blocked / exit 2."""
    result = derive_verdict(
        None, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2


def test_blocked_timeout() -> None:
    """child rc 124 -> blocked (timeout) / exit 2, even with a usable contract."""
    result = derive_verdict(
        _load("pass.yaml"), expected_tier=2, allow_single_vendor=False, child_rc=124
    )
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    assert result.reason == "timeout"


def test_blocked_child_crash_no_contract() -> None:
    """Non-zero, non-124 rc with no usable contract -> blocked / exit 2."""
    result = derive_verdict(
        None, expected_tier=2, allow_single_vendor=False, child_rc=1
    )
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2


def test_blocked_unknown_major_version() -> None:
    """contract_version 2.0.0 -> blocked (fail-loud) / exit 2."""
    result = derive_verdict(
        _load("blocked_unknown_major.yaml"),
        expected_tier=2,
        allow_single_vendor=False,
        child_rc=0,
    )
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2


def test_tolerant_unknown_field_1x() -> None:
    """1.9.0 + an unknown top-level field still maps to pass / 0 (NFR-8)."""
    result = derive_verdict(
        _load("tolerant_unknown_field.yaml"),
        expected_tier=2,
        allow_single_vendor=False,
        child_rc=0,
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_serena_summary_corroboration_unavailable_not_degraded() -> None:
    """serena_summary_corroboration: unavailable must NOT route to degraded."""
    contract = _load("pass.yaml")
    contract["serena_summary_corroboration"] = "unavailable"
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_verification_skip_exemption_not_degraded() -> None:
    """verification_ran False with an exempted skip reason must NOT degrade."""
    contract = _load("pass.yaml")
    contract["verification_ran"] = False
    contract["verification_skip_reason"] = "read-only-project"
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_verification_not_run_unexempted_is_degraded() -> None:
    """verification_ran False with no exemption -> degraded / 11 (control)."""
    contract = _load("pass.yaml")
    contract["verification_ran"] = False
    contract["verification_skip_reason"] = None
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11


def test_extrapolated_citations_do_not_gate() -> None:
    """citations_dropped_extrapolated > 0 (sample 0) must NOT degrade."""
    contract = _load("pass.yaml")
    contract["citations_dropped"] = 0
    contract["citations_dropped_extrapolated"] = 12
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_benign_degraded_component_does_not_over_halt() -> None:
    """A benign fail-open token must NOT route to degraded (exact membership)."""
    contract = _load("pass.yaml")
    contract["degraded_components"] = [
        "search_deps:lsp_unindexed",
        "serena:onboarding-parse",
    ]
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_nonzero_child_exit_with_present_success_contract_blocks() -> None:
    """F0: a non-zero, non-124 child rc vetoes a PRESENT success contract.

    Pre-fix, ``child_rc=1`` + ``pass.yaml`` reached PASS (the fail-closed hole).
    Post-fix it routes BLOCKED / exit 2 / reason ``child-crash`` BEFORE the
    contract's success fields are trusted; the 124 timeout case remains a
    distinct labelled subset (proven by the companion assertion).
    """
    result = derive_verdict(
        _load("pass.yaml"), expected_tier=2, allow_single_vendor=False, child_rc=1
    )
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    assert result.reason == "child-crash"

    # Companion: rc 124 with the SAME contract is still timeout (a subset).
    timeout = derive_verdict(
        _load("pass.yaml"), expected_tier=2, allow_single_vendor=False, child_rc=124
    )
    assert timeout.verdict is Verdict.BLOCKED
    assert timeout.verdict.exit_code == 2
    assert timeout.reason == "timeout"


def test_malformed_truthy_load_bearing_boolean_blocks() -> None:
    """F2: a PRESENT load-bearing boolean that is truthy-but-not-bool BLOCKS.

    ``regression_present: "true"`` (str) and ``needs_human_decision: 1`` (int)
    are truthy but NOT ``is True``, so pre-fix they bypassed the halt triggers
    and a success contract leaked to PASS. Post-fix they route BLOCKED / exit 2
    / reason ``malformed-contract-boolean``. The control proves valid contracts
    are NOT over-blocked.
    """
    str_contract = _load("pass.yaml")
    str_contract["regression_present"] = "true"
    str_result = derive_verdict(
        str_contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert str_result.verdict is Verdict.BLOCKED
    assert str_result.verdict.exit_code == 2
    assert str_result.reason == "malformed-contract-boolean"

    int_contract = _load("pass.yaml")
    int_contract["needs_human_decision"] = 1
    int_result = derive_verdict(
        int_contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert int_result.verdict is Verdict.BLOCKED
    assert int_result.verdict.exit_code == 2
    assert int_result.reason == "malformed-contract-boolean"

    # Control: a proper-bool / absent-field contract still passes (no over-block).
    control = derive_verdict(
        _load("pass.yaml"), expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert control.verdict is Verdict.PASS
    assert control.verdict.exit_code == 0


def test_status_failed_halts_with_status_failed_reason() -> None:
    """F5: a ``status: failed`` contract halts with reason ``status-failed``.

    The exit code was already correct (10, halted); pre-fix the reason slug was
    the misleading ``tier-mismatch``. The fix is reason-slug-only.
    """
    contract = _load("pass.yaml")
    contract["status"] = "failed"
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    assert result.reason == "status-failed"


def test_reachability_1_7_0_additive_fields_tolerated() -> None:
    """FR-RH1 R4/R7: a 1.7.0 contract carrying only the canonical R7 reachability block
    (gate ran, all clean) is tolerated by the consumer -> pass / 0."""
    result = derive_verdict(
        _load("reachability_1_7_0_gate_ran.yaml"),
        expected_tier=2,
        allow_single_vendor=False,
        child_rc=0,
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_reachability_no_reachability_skip_is_telemetry_only() -> None:
    """FR-RH1 R2: --no-reachability skip is telemetry-only -> pass / 0 (no degrade/halt)."""
    contract = _load("reachability_skip_no_reachability.yaml")
    assert contract["reachability_gate_ran"] is False
    assert contract["reachability_skip_reason"] == "--no-reachability"
    assert contract["reachability_ledger_path"] is None
    assert contract["needs_human_decision"] is False
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_reachability_spec_absent_skip_is_telemetry_only() -> None:
    """FR-RH1 R3: spec-and-tasklist-absent skip is telemetry-only -> pass / 0."""
    contract = _load("reachability_skip_spec_absent.yaml")
    assert contract["reachability_skip_reason"] == "spec-and-tasklist-absent"
    assert contract["reachability_gate_ran"] is False
    assert contract["needs_human_decision"] is False
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_reachability_semantic_fallback_advisory_does_not_gate() -> None:
    """FR-RH1 R9: semantic fallback without an explicit durable_sink:/@sink annotation is
    advisory-only -> does not route to DEGRADED/HALTED and does not increment unproven."""
    contract = _load("reachability_semantic_fallback_advisory.yaml")
    assert contract["reachability_unproven"] == 0
    assert contract["needs_human_decision"] is False
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_reachability_proxy_oracle_unproven_is_not_regression_but_halts() -> None:
    """FR-RH1 R1: proxy/oracle-only evidence (no real boot) can NEVER green a real-boot
    Regression. The unproven Grounding Gap halts for human decision (exit 10) while
    regression_present stays false and reachability_unreachable stays 0."""
    contract = _load("reachability_proxy_oracle_unproven.yaml")
    assert contract["reachability_unproven"] == 1
    assert contract["reachability_unreachable"] == 0
    assert contract["reachability_real_boot_ran"] is False
    assert contract["regression_present"] is False
    assert contract["needs_human_decision"] is True
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10


def test_reachability_unwired_surface_real_boot_is_regression_not_degrade() -> None:
    """R5 §5.3 falsifier: an annotated contracted sink unobserved by a REAL boot
    (real_boot_ran true, unreachable>=1) resolves to Regression -> HALTED/10,
    NOT a degrade-only pass and NOT a clean pass. Together with the proxy-oracle
    unproven test this forms the complete B-vs-C discriminator: proxy-only ->
    unproven/HALT (not regression); real-boot-unobserved -> Regression/HALT."""
    contract = _load("reachability_unwired_surface_regression.yaml")
    assert contract["reachability_real_boot_ran"] is True
    assert contract["reachability_unreachable"] >= 1
    assert contract["regression_present"] is True
    result = derive_verdict(
        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
