"""Validation-gate tests (spec FR-5.1–FR-5.4, §10 / §10.1).

T-501 single-file change → targeted tests (not cross-cutting); T-502 cross-cutting
→ `make test` escalation; T-510 lint failure → push blocked; **T-511** format
failure with lint GREEN → push blocked (the VG-3≠VG-4 two-gate regression test);
T-520 test failure → no push AND `round_counter` NOT incremented; T-521 persistent
validation failure → HALT; T-522 partial-green (lint only) → `validation_status !=
"validated"` → push blocked.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import (
    RunConfig,
    is_cross_cutting,
    run_skill,
    run_validation_gates,
)
from superclaude.pr_submit.models import Finding, MonitorState


def _verified(path="src/superclaude/pr_submit/x.py") -> Finding:
    return Finding(
        path=path, line=1, body="bug", in_diff=True, verification_status="verified"
    )


def test_t501_single_file_targeted_not_crosscutting():
    """T-501: a single-file change is targeted (NOT cross-cutting → targeted pytest)."""
    assert is_cross_cutting(["src/superclaude/pr_submit/severity_router.py"]) is False


def test_t502_crosscutting_escalates_to_make_test():
    """T-502: a cross-cutting change (≥2 packages / shared infra) escalates to `make test`."""
    assert (
        is_cross_cutting(
            ["src/superclaude/pr_submit/fsm.py", "src/superclaude/cli/main.py"]
        )
        is True
    )
    # shared infra (hooks) also escalates
    assert (
        is_cross_cutting(["src/superclaude/hooks/scripts/offer-pr-review.sh"]) is True
    )


def test_t510_lint_failure_blocks_push():
    """T-510: a lint (VG-3) failure → validation not validated → push blocked."""
    assert run_validation_gates({"VG-1": True, "VG-3": False, "VG-4": True}) == "failed"


def test_t511_format_failure_lint_green_blocks_push():
    """T-511: format (VG-4) failure with lint (VG-3) GREEN → push blocked (VG-3≠VG-4 split)."""
    # The load-bearing regression: green lint must NOT authorize a push when format fails.
    assert run_validation_gates({"VG-1": True, "VG-3": True, "VG-4": False}) == "failed"
    # And the inverse two-gate independence: format green + lint fail also blocks.
    assert run_validation_gates({"VG-1": True, "VG-3": False, "VG-4": True}) == "failed"
    # Both green → validated (proves they are SEPARATE gates, both required).
    assert (
        run_validation_gates({"VG-1": True, "VG-3": True, "VG-4": True}) == "validated"
    )


def test_t520_validation_failure_no_push_no_round_increment():
    """T-520: a validation failure → no push AND `round_counter` NOT incremented."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            findings=[_verified()],
            run_validation=lambda **_: "failed",
        )
    )
    assert result.state == MonitorState.VALIDATION_FAIL
    assert result.push_count == 0
    assert result.round_counter == 0  # validation retry does NOT increment the round


def test_t521_persistent_validation_failure_halts():
    """T-521: persistent validation failure → HALT (VALIDATION_FAIL terminal)."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            findings=[_verified()],
            run_validation=lambda **_: "failed",
        )
    )
    assert result.state == MonitorState.VALIDATION_FAIL
    assert result.push_count == 0


def test_t522_partial_green_never_validated():
    """T-522: partial-green (lint only, no format) → `validation_status != "validated"`."""
    status = run_validation_gates({"VG-3": True})
    assert status != "validated"
    assert status == "failed"


@pytest.mark.parametrize(
    "results,expected",
    [
        ({"VG-1": True, "VG-2": True, "VG-3": True, "VG-4": True}, "validated"),
        (
            {"VG-1": True, "VG-2": False, "VG-3": True, "VG-4": True},
            "failed",
        ),  # VG-2 escalation fails
    ],
)
def test_ordered_gate_aggregation(results, expected):
    """The ordered §10 aggregation: every gate that ran must be green; mandatory trio required."""
    assert run_validation_gates(results) == expected
