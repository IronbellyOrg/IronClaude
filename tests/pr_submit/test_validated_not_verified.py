"""Validated-not-verified audit (spec AC-13 / INV-015).

T-VALIDATED-NOT-VERIFIED: the INV-015 audit distinguishes "validation passed" from
"finding behaviorally verified". A genuine fix that PASSES validation but drifts an
untested behavior (behavioral_test_failures present) is FLAGGED `validated_not_verified`
and recorded in the run-log — NOT auto-resolved. This is the OUTPUT-side residual,
distinct from the INPUT-side verify-before-remediate filter (FR-3.5).
"""

from __future__ import annotations

from superclaude.pr_submit.fsm import audit_validated_not_verified
from superclaude.pr_submit.run_log import RunLog


def test_validated_not_verified_flags_behavioral_drift(tmp_path, load_fixture):
    """T-VALIDATED-NOT-VERIFIED: a validated fix with behavioral drift is flagged, not resolved.

    Mirrors behavioral-drift.json: validation_status=="validated" but a behavioral
    test (not part of the targeted validation) reveals a drifted, untested behavior.
    """
    # Parity: the dedicated fixture's validation_status + behavioral_test_failures
    # drive the SAME audit verdict (guards drift from behavioral-drift.json).
    fixture = load_fixture("behavioral-drift.json")
    assert fixture["behavioral_test_failures"]  # non-empty
    fixture_audit = audit_validated_not_verified(
        validation_status=fixture["validation_status"],
        behavioral_test_failures=fixture["behavioral_test_failures"],
    )
    assert fixture_audit["validated_not_verified"] is True

    audit = audit_validated_not_verified(
        validation_status="validated",
        behavioral_test_failures=["test_legacy_flow drifted: expected 200, got 500"],
    )
    assert audit["validated_not_verified"] is True
    assert audit["behavioral_test_failures"]

    # The audit result is recorded in the run-log (not auto-resolved).
    rl = RunLog(15, tmp_path)
    rl.append(
        {
            "event_type": "validation_completed",
            "status": "validated",
            "validated_not_verified": audit["validated_not_verified"],
            "behavioral_test_failures": audit["behavioral_test_failures"],
        }
    )
    ev = rl.read_events()[-1]
    assert ev["validated_not_verified"] is True
    assert ev["behavioral_test_failures"]


def test_validated_and_verified_not_flagged():
    """A validated fix with NO behavioral failures is NOT flagged (the clean path)."""
    audit = audit_validated_not_verified(
        validation_status="validated", behavioral_test_failures=[]
    )
    assert audit["validated_not_verified"] is False


def test_unvalidated_not_flagged_as_validated_not_verified():
    """A fix that did not even validate is not a 'validated-not-verified' case (distinct state)."""
    audit = audit_validated_not_verified(
        validation_status="failed", behavioral_test_failures=["something"]
    )
    # validation_status != "validated" → this is a validation failure, not INV-015.
    assert audit["validated_not_verified"] is False
