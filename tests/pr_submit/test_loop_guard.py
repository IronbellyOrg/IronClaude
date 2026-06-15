"""Loop-guard fence-post tests (spec FR-6.3 / INV-001, AC-6) — the P0 surface.

T-620..T-629 the fence-post matrix; **T-626-OFF-BY-ONE** the canonical off-by-one
(`round_counter == 2` not 3 at `max_rounds=2`, and exactly 2 pushes);
T-VANISHED-MONO monotonicity (a counted re-review that vanishes does NOT decrement).
The gate uses `>=` semantics (INV-5). This is the single most important behavioral
test — the spec's named P0 defect.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import RunConfig, run_skill
from superclaude.pr_submit.loop_guard import RoundCounter, should_halt, user_label
from superclaude.pr_submit.models import Finding, MonitorState


def _f(line: int) -> Finding:
    return Finding(
        path="src/a.py",
        line=line,
        body=f"bug{line}",
        in_diff=True,
        verification_status="verified",
        comment_id=1000 + line,
    )


def _run(max_rounds: int, residual_cycles: int):
    """Drive run_skill with `residual_cycles` re-reviews that each still carry a finding."""
    rereview = [[_f(100 + i)] for i in range(residual_cycles)]
    return run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=max_rounds,
            findings=[_f(1)],
            rereview_findings=rereview,
        )
    )


@pytest.mark.loop_guard
@pytest.mark.p0
def test_t626_off_by_one_canonical(load_fixture):
    """T-626-OFF-BY-ONE: at max_rounds=2 with ≥3 residual re-reviews → counter==2, exactly 2 pushes.

    Scenario mirrors round-sequence-residual-x3.json: three successive re-reviews
    each still carrying a residual finding. The `>=` gate fires at counter==2, so the
    third fix cycle never opens — exactly 2 pushes, counter exactly 2 (never 3).
    """
    result = _run(
        max_rounds=2, residual_cycles=2
    )  # cycle0 + 2 residual re-reviews = 3 cycles
    assert result.round_counter == 2  # NOT 3 — the canonical off-by-one
    assert result.push_count == 2  # max_rounds=N → exactly N pushes
    assert result.state == MonitorState.HALT_MAX_ROUNDS
    assert result.summary_posted is True

    # Parity: the dedicated fixture's expected block matches the computed result
    # (guards drift between the inline scenario and round-sequence-residual-x3.json).
    fixture = load_fixture("round-sequence-residual-x3.json")
    assert fixture["expected"]["round_counter"] == result.round_counter == 2
    assert fixture["expected"]["push_count"] == result.push_count == 2


@pytest.mark.loop_guard
@pytest.mark.p0
@pytest.mark.parametrize(
    "max_rounds,residual,exp_counter,exp_pushes",
    [
        (
            1,
            3,
            1,
            1,
        ),  # fence-post: max_rounds=1 with residuals → exactly 1 push, counter==1
        (
            2,
            0,
            1,
            1,
        ),  # fence-post: clean fix before budget → 1 push then clean, counter==1
        (
            2,
            1,
            2,
            2,
        ),  # fence-post: max_rounds=2, one residual → exactly 2 pushes, counter==2
        (
            2,
            5,
            2,
            2,
        ),  # fence-post: max_rounds=2 with excess residuals → capped at 2 pushes
        (
            3,
            5,
            3,
            3,
        ),  # fence-post: max_rounds=3 with excess residuals → exactly 3 pushes
        (
            5,
            9,
            5,
            5,
        ),  # fence-post: hard cap max_rounds=5 → exactly 5 pushes, counter==5
    ],
)
def test_t620_629_fence_post_matrix(max_rounds, residual, exp_counter, exp_pushes):
    """T-620..T-629: the fence-post matrix — max_rounds=N → exactly N pushes, counter==N."""
    result = _run(max_rounds=max_rounds, residual_cycles=residual)
    assert result.round_counter == exp_counter
    assert result.push_count == exp_pushes


@pytest.mark.loop_guard
def test_gate_uses_ge_not_gt():
    """INV-5: the HALT gate uses `>=` (fires AT max_rounds), never `>`."""
    assert should_halt(2, 2) is True  # >= fires at equality
    assert should_halt(1, 2) is False
    assert should_halt(3, 2) is True
    assert user_label(0) == 1  # user-facing label = counter + 1


@pytest.mark.loop_guard
@pytest.mark.p0
def test_t_vanished_mono_irrevocable():
    """T-VANISHED-MONO: a counted re-review that later vanishes does NOT decrement (INV-4)."""
    rc = RoundCounter(max_rounds=2)
    rc.on_rereview(review_observed=True, sha_attributed_to_our_push=True)
    rc.on_rereview(review_observed=True, sha_attributed_to_our_push=True)
    assert rc.value == 2
    rc.vanished_rereview()  # the re-review vanished
    assert rc.value == 2  # monotonic — no decrement
    # A non-attributed re-review never increments in the first place.
    assert (
        rc.on_rereview(review_observed=True, sha_attributed_to_our_push=False) is False
    )
    assert rc.value == 2


# --- V1.1 INV-R1/R3 + deferred increment + fallback cap-1 (addendum §5) -------
# These ADD to the file; the INV-001 fence-post tests above are LEFT UNCHANGED and
# still pass — guarding the verbatim INV-001 preservation.


@pytest.mark.inv
def test_deferred_increment_gated_on_attributed():
    """The relocated increment is gated on `"attributed"`, NOT optimistic: a push whose
    re-trigger poll times out does NOT advance `round_counter` (contrast the legacy
    optimistic tick). Reuses the rereview-then-decline scenario shape."""
    # timeout outcome → push happens, but no tick.
    timed_out = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_outcome=["timeout"],
        )
    )
    assert timed_out.push_count == 1 and timed_out.round_counter == 0
    # attributed outcome → tick.
    attributed = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_outcome=["attributed"],
        )
    )
    assert attributed.push_count == 1 and attributed.round_counter == 1


@pytest.mark.inv
def test_inv_r1_rereview_request_count_monotone_and_bounded():
    """INV-R1: `rereview_request_count` is monotone and `<= max_rounds`."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_findings=[[_f(2)], [_f(3)], [_f(4)]],
        )
    )
    assert result.rereview_request_count <= 2  # <= max_rounds
    assert result.rereview_request_count == result.push_count  # one re-trigger per push


@pytest.mark.inv
def test_inv_r3_clamp_monotone_and_counters_independent():
    """INV-R3: the fallback clamp is monotone non-increasing and the two counters
    (`round_counter`, `fallback_round_counter`) are INDEPENDENT — advancing one never
    moves the other."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=5,
            findings=[_f(1)],
            rereview_findings=[[_f(2)]],
            rereview_outcome=["attributed", "declined"],
            fallback_findings=[_f(9)],
        )
    )
    # round_counter advanced once (the attributed Augment round) then FROZE.
    assert result.round_counter == 1
    # the fallback advanced only its own counter, and clamped the budget to 1.
    assert result.fallback_round_counter == 1
    assert result.effective_max_rounds == 1  # monotone clamp, 5 → 1


@pytest.mark.inv
def test_fallback_round_counter_cap_one():
    """The fallback counter is capped at 1: `should_halt(fallback_round_counter, 1)` halts
    after one fallback cycle (no second fallback remediation)."""
    assert should_halt(0, 1) is False  # the one fallback cycle may open
    assert should_halt(1, 1) is True  # ...and is the last (cap-1, >= gate)
    # End-to-end: the fallback never runs more than one remediation cycle.
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            review_state="declined",
            fallback_findings=[_f(9)],
        )
    )
    assert result.fallback_round_counter == 1
