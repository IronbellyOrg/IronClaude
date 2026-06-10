"""AC-3: the pure AUTO-FIXABLE vs HUMAN-REQUIRED carve-out (`classify_fix`).

One row per spec Section 3 verdict-table trigger, called directly (no subprocess,
no CliRunner) -- proving `classify_fix` is pure. Plus a guard that a malformed
load-bearing boolean routes BLOCKED upstream in `derive_verdict`, so the
classifier is never reached on untrusted input.
"""

from __future__ import annotations

from superclaude.cli.reflect.contract import classify_fix, derive_verdict
from superclaude.cli.reflect.models import Verdict

_CLEAN_BOOLS = {
    "regression_present": False,
    "needs_human_decision": False,
    "user_decision_required": False,
    "unauthorized_deviation_present": False,
}


def _dev(authorized=0, necessary=0, drift=0, regression=0) -> dict[str, int]:
    return {
        "authorized": authorized,
        "necessary": necessary,
        "drift": drift,
        "regression": regression,
    }


def test_drift_only_is_auto_fixable() -> None:
    assert classify_fix(dict(_CLEAN_BOOLS), _dev(drift=2)) == "auto-fixable"


def test_necessary_only_is_auto_fixable() -> None:
    assert classify_fix(dict(_CLEAN_BOOLS), _dev(necessary=1)) == "auto-fixable"


def test_regression_present_is_human_required() -> None:
    c = dict(_CLEAN_BOOLS, regression_present=True)
    assert classify_fix(c, _dev(drift=1)) == "human-required"


def test_regression_count_is_human_required() -> None:
    assert classify_fix(dict(_CLEAN_BOOLS), _dev(regression=1)) == "human-required"


def test_needs_human_decision_is_human_required() -> None:
    c = dict(_CLEAN_BOOLS, needs_human_decision=True)
    assert classify_fix(c, _dev(drift=1)) == "human-required"


def test_user_decision_required_is_human_required() -> None:
    c = dict(_CLEAN_BOOLS, user_decision_required=True)
    assert classify_fix(c, _dev(drift=1)) == "human-required"


def test_unauthorized_deviation_is_human_required() -> None:
    c = dict(_CLEAN_BOOLS, unauthorized_deviation_present=True)
    assert classify_fix(c, _dev(drift=1)) == "human-required"


def test_mixed_drift_and_regression_human_wins() -> None:
    """drift>0 AND regression>0 -> human-required (carve-out is 'solely drift/necessary')."""
    assert (
        classify_fix(dict(_CLEAN_BOOLS), _dev(drift=3, regression=1))
        == "human-required"
    )


def test_authorized_only_is_none() -> None:
    """Authorized-only (no drift/necessary, no hard signal) -> none (nothing to auto-fix)."""
    assert classify_fix(dict(_CLEAN_BOOLS), _dev(authorized=2)) == "none"


def test_all_zero_clean_is_none() -> None:
    assert classify_fix(dict(_CLEAN_BOOLS), _dev()) == "none"


def test_malformed_boolean_routes_blocked_upstream_so_classifier_never_reached() -> (
    None
):
    """A malformed load-bearing boolean (string 'true') routes BLOCKED in derive_verdict.

    The runner consults classify_fix ONLY on a trustworthy Verdict.HALTED, so a
    malformed/untrusted contract is terminal upstream and the classifier never sees it.
    """
    malformed = {
        "contract_version": "1.4.0",
        "status": "partial",
        "tier_reached": 2,
        "regression_present": "true",  # malformed: string, not a real bool
        "deviation_count_by_class": {"drift": 1},
    }
    result = derive_verdict(
        malformed, expected_tier=2, allow_single_vendor=False, child_rc=0
    )
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
