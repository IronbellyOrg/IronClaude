"""Unit tests for reflect Tier-2 fallback planning."""

from superclaude.cli.reflect.fallback import (
    QuorumState,
    make_fallback_slot_factory,
    plan_next_attempt,
)
from superclaude.cli.swarm.models import WorkerResult

LADDER = ("T1Model01", "T1Model02")
AVAILABLE = {"T1Model01": True, "T1Model02": True}


class RecordingTransport:
    def __init__(self, model_id: str) -> None:
        self.model_id = model_id


def _quorum(*, satisfies_tier2: bool = False, reviewer_count: int = 1) -> QuorumState:
    return QuorumState(
        reviewer_count=reviewer_count,
        model_class_diversity="full" if satisfies_tier2 else "insufficient",
        vendor_diversity="multi" if satisfies_tier2 else None,
        satisfies_tier2=satisfies_tier2,
    )


def _failure(index: int = 0) -> WorkerResult:
    return WorkerResult(index=index, status="proxy_error", model_id=f"failed-{index}")


def test_certified_when_primary_quorum_already_satisfies_tier2() -> None:
    decision = plan_next_attempt(
        _quorum(satisfies_tier2=True, reviewer_count=2),
        eligible_failures=[],
        attempts_made=[],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "certified"
    assert decision.slot is None
    assert decision.reason == "not_needed_primary_quorum_met"


def test_certified_with_fallback_after_attempt_satisfies_tier2() -> None:
    decision = plan_next_attempt(
        _quorum(satisfies_tier2=True, reviewer_count=2),
        eligible_failures=[_failure()],
        attempts_made=["T1Model01"],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "certified"
    assert decision.slot is None
    assert decision.reason == "certified_t2_with_fallback"


def test_dispatches_first_ladder_slot_when_quorum_unmet() -> None:
    decision = plan_next_attempt(
        _quorum(),
        eligible_failures=[_failure()],
        attempts_made=[],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "dispatch"
    assert decision.slot == "T1Model01"


def test_first_pass_with_multiple_primary_failures_still_dispatches_t1model01() -> None:
    decision = plan_next_attempt(
        _quorum(),
        eligible_failures=[_failure(0), _failure(1)],
        attempts_made=[],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "dispatch"
    assert decision.slot == "T1Model01"


def test_second_attempt_dispatches_t1model02_not_t1model01_again() -> None:
    decision = plan_next_attempt(
        _quorum(),
        eligible_failures=[_failure()],
        attempts_made=["T1Model01"],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "dispatch"
    assert decision.slot == "T1Model02"


def test_second_attempt_planner_decision_resolves_to_second_pool_model() -> None:
    decision = plan_next_attempt(
        _quorum(),
        eligible_failures=[_failure()],
        attempts_made=["T1Model01"],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )
    factory = make_fallback_slot_factory(
        pool=("pool-0", "pool-1"),
        ladder=LADDER,
        build_transport=RecordingTransport,
    )

    assert decision.action == "dispatch"
    assert decision.slot == "T1Model02"
    assert factory(decision.slot).model_id == "pool-1"
    assert factory("T1Model01").model_id == "pool-0"


def test_later_pass_can_escalate_when_t1model01_success_did_not_repair_diversity() -> (
    None
):
    decision = plan_next_attempt(
        QuorumState(
            reviewer_count=2,
            model_class_diversity="full",
            vendor_diversity="single",
            satisfies_tier2=False,
        ),
        eligible_failures=[_failure()],
        attempts_made=["T1Model01"],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "dispatch"
    assert decision.slot == "T1Model02"


def test_wall_clock_exhaustion_stops_before_dispatch() -> None:
    decision = plan_next_attempt(
        _quorum(),
        eligible_failures=[_failure()],
        attempts_made=[],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=False,
    )

    assert decision.action == "degraded"
    assert decision.slot is None
    assert decision.reason == "fallback_wall_clock_exhausted"


def test_no_eligible_failures_with_unrepairable_diversity_degrades() -> None:
    decision = plan_next_attempt(
        QuorumState(
            reviewer_count=2,
            model_class_diversity="full",
            vendor_diversity="single",
            satisfies_tier2=False,
        ),
        eligible_failures=[],
        attempts_made=[],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "degraded"
    assert decision.slot is None
    assert decision.reason == "diversity_unrepairable"


def test_no_eligible_failures_with_quorum_short_degrades_as_no_primary_failure() -> (
    None
):
    decision = plan_next_attempt(
        _quorum(reviewer_count=1),
        eligible_failures=[],
        attempts_made=[],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "degraded"
    assert decision.slot is None
    assert decision.reason == "no_fallback_eligible_primary_failure"


def test_missing_fallback_slot_reports_config_missing() -> None:
    decision = plan_next_attempt(
        _quorum(),
        eligible_failures=[_failure()],
        attempts_made=[],
        ladder=LADDER,
        fallback_available={"T1Model01": False, "T1Model02": True},
        wall_clock_ok=True,
    )

    assert decision.action == "degraded"
    assert decision.slot == "T1Model01"
    assert decision.reason == "fallback_config_missing"


def test_missing_second_fallback_slot_reports_t1model02_config_missing() -> None:
    decision = plan_next_attempt(
        _quorum(),
        eligible_failures=[_failure()],
        attempts_made=["T1Model01"],
        ladder=LADDER,
        fallback_available={"T1Model01": True, "T1Model02": False},
        wall_clock_ok=True,
    )

    assert decision.action == "degraded"
    assert decision.slot == "T1Model02"
    assert decision.reason == "fallback_config_missing"


def test_ladder_exhaustion_reports_pool_exhausted() -> None:
    decision = plan_next_attempt(
        _quorum(),
        eligible_failures=[_failure()],
        attempts_made=["T1Model01", "T1Model02"],
        ladder=LADDER,
        fallback_available=AVAILABLE,
        wall_clock_ok=True,
    )

    assert decision.action == "degraded"
    assert decision.slot is None
    assert decision.reason == "fallback_pool_exhausted"
