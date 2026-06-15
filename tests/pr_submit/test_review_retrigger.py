"""Post-push re-trigger tests (V1.1 R1 / FR-8, addendum §6.4).

A push does NOT auto-trigger an Augment re-review (memory
`reference_augment_review_triggers`): the skill posts an `auggie review` re-trigger
comment (S5a) after each push and polls for the attributed re-review. The
deterministic core drives this via the injected `do_retrigger` seam + the per-cycle
`rereview_outcome` sequence; the `round_counter` increment is RELOCATED off the
optimistic post-resolve site to fire ONLY on an `"attributed"` outcome.

T-1101 exactly one re-trigger per push; T-1102 + T-PUSH-WITHOUT-REREVIEW-NO-TICK the
deferred increment ticks only on `"attributed"` (a `"timeout"` does NOT advance);
T-1103 `rereview_request_count <= max_rounds` (INV-R1); T-1104 attributed advances;
T-1105 the core holds no hard-coded trigger literal; T-1106 S5a skipped when
`applied_edits == 0`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.pr_submit.fsm import RunConfig, run_skill
from superclaude.pr_submit.models import Finding, MonitorState


def _f(line: int, **kw) -> Finding:
    return Finding(
        path="src/a.py",
        line=line,
        body=f"bug{line}",
        in_diff=True,
        verification_status="verified",
        comment_id=1000 + line,
        **kw,
    )


@pytest.mark.inv
def test_t1101_one_retrigger_per_push():
    """T-1101: after a push, exactly one `auggie review` re-trigger is requested."""
    retriggers: list[dict] = []
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_outcome=["attributed"],
            do_retrigger=lambda **kw: retriggers.append(kw),
        )
    )
    assert result.push_count == 1
    assert len(retriggers) == 1  # exactly one re-trigger comment for the one push
    assert result.rereview_request_count == 1


@pytest.mark.inv
def test_t1102_attributed_outcome_ticks(load_fixture):
    """T-1102: the deferred increment ticks when the outcome is `"attributed"`."""
    fx = load_fixture("rereview-attributed.json")
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=fx["max_rounds"],
            findings=[_f(1)],
            rereview_outcome=fx["rereview_outcome"],
        )
    )
    assert result.round_counter == fx["expected"]["round_counter"] == 1
    assert (
        result.rereview_request_count == fx["expected"]["rereview_request_count"] == 1
    )
    assert result.state.value == fx["expected"]["terminal"]


@pytest.mark.inv
def test_t_push_without_rereview_no_tick():
    """T-PUSH-WITHOUT-REREVIEW-NO-TICK / EC-18: a push whose outcome is `"timeout"`
    (no attributed re-review) does NOT advance `round_counter` — the V1.0 loop-stall bug.

    NON-VACUOUS: asserts round_counter stays at its pre-push value (0) even though the
    cycle pushed (push_count == 1).
    """
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_outcome=["timeout"],
        )
    )
    assert result.push_count == 1  # the cycle DID push
    assert result.round_counter == 0  # ...but no attributed re-review → NO tick
    assert result.state == MonitorState.TERMINAL_TIMEOUT


@pytest.mark.inv
def test_t1103_rereview_request_count_bounded_by_max_rounds():
    """T-1103 / INV-R1: `rereview_request_count` is monotone and <= max_rounds."""
    # 5 residual cycles but max_rounds=2 → the >= gate halts after 2 pushes, so at most
    # 2 re-triggers are requested.
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_findings=[[_f(2)], [_f(3)], [_f(4)], [_f(5)]],
        )
    )
    assert result.rereview_request_count <= result.push_count
    assert result.rereview_request_count <= 2  # <= max_rounds (INV-R1)


@pytest.mark.inv
def test_t1104_attributed_rereview_advances_cycle():
    """T-1104: an attributed re-review advances to the next cycle (counter rises per push)."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_findings=[[_f(2)]],
            rereview_outcome=["attributed", "attributed"],
        )
    )
    assert result.round_counter == 2
    assert result.push_count == 2


@pytest.mark.inv
def test_t1105_core_holds_no_hardcoded_trigger_literal():
    """T-1105 (static, core half): the deterministic core fsm.py holds NO hard-coded
    `auggie review` trigger literal — the trigger token lives in the bash script
    (Phase 6 `scripts/retrigger-review.sh`), reached via the `do_retrigger` seam."""
    fsm_src = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "superclaude"
        / "pr_submit"
        / "fsm.py"
    ).read_text(encoding="utf-8")
    assert "auggie review" not in fsm_src.lower()


@pytest.mark.inv
def test_t1106_s5a_skipped_when_no_edits_applied():
    """T-1106 / FR-8.6: the S5a re-trigger is SKIPPED when the cycle applied no edits
    (`applied_edits == 0`) — no push, no re-trigger comment."""
    retriggers: list[dict] = []
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            apply_edits=lambda _findings: 0,  # zero edits → no push → no S5a
            do_retrigger=lambda **kw: retriggers.append(kw),
        )
    )
    assert result.applied_edits == 0
    assert result.push_count == 0
    assert len(retriggers) == 0  # S5a skipped
    assert result.rereview_request_count == 0
