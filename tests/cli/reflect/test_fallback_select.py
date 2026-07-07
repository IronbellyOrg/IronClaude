"""Unit tests for reflect Tier-2 fallback contributing-set selection."""

from superclaude.cli.reflect.ensemble import (
    _vendor_from_model_id as ensemble_vendor_from_model_id,
)
from superclaude.cli.reflect.fallback import evaluate_quorum, select_contributing_set
from superclaude.cli.swarm.models import WorkerResult, WorkerStatus


def _worker(index: int, status: WorkerStatus, model_id: str) -> WorkerResult:
    return WorkerResult(index=index, status=status, model_id=model_id)


def test_evaluate_quorum_one_success_is_not_tier2() -> None:
    state = evaluate_quorum(
        [_worker(0, "success", "qwen-primary")], allow_single_vendor=False
    )

    assert state.reviewer_count == 1
    assert state.model_class_diversity == "insufficient"
    assert state.vendor_diversity is None
    assert not state.satisfies_tier2


def test_evaluate_quorum_two_distinct_model_and_vendor_successes_satisfy_tier2() -> (
    None
):
    state = evaluate_quorum(
        [
            _worker(0, "success", "qwen-primary"),
            _worker(1, "success", "deepseek-primary"),
        ],
        allow_single_vendor=False,
    )

    assert state.reviewer_count == 2
    assert state.model_class_diversity == "full"
    assert state.vendor_diversity == "multi"
    assert state.satisfies_tier2


def test_evaluate_quorum_same_vendor_requires_allow_single_vendor() -> None:
    workers = [
        _worker(0, "success", "gpt-4"),
        _worker(1, "success", "gpt-5"),
    ]

    strict = evaluate_quorum(workers, allow_single_vendor=False)
    allowed = evaluate_quorum(workers, allow_single_vendor=True)

    assert strict.reviewer_count == 2
    assert strict.model_class_diversity == "full"
    assert strict.vendor_diversity == "single"
    assert not strict.satisfies_tier2
    assert allowed.satisfies_tier2


def test_evaluate_quorum_same_model_id_is_insufficient_even_when_single_vendor_allowed() -> (
    None
):
    state = evaluate_quorum(
        [
            _worker(0, "success", "qwen-same"),
            _worker(1, "success", "qwen-same"),
        ],
        allow_single_vendor=True,
    )

    assert state.reviewer_count == 2
    assert state.model_class_diversity == "insufficient"
    assert state.vendor_diversity == "single"
    assert not state.satisfies_tier2


def test_vendor_helper_remains_importable_from_ensemble_backcompat_surface() -> None:
    assert ensemble_vendor_from_model_id("gpt-5") == "openai"


def test_smallest_passing_set_is_chosen_not_larger_set() -> None:
    primary_a = _worker(0, "success", "qwen-primary")
    primary_b = _worker(1, "success", "deepseek-primary")
    fallback = _worker(2, "success", "gpt-fallback")

    selected = select_contributing_set(
        [primary_a, primary_b], [fallback], allow_single_vendor=False
    )

    assert selected == [primary_a, primary_b]


def test_primaries_are_preferred_over_fallbacks_on_ties() -> None:
    primary_a = _worker(0, "success", "qwen-primary")
    primary_b = _worker(1, "success", "deepseek-primary")
    fallback = _worker(2, "success", "gpt-fallback")

    selected = select_contributing_set(
        [primary_a, primary_b], [fallback], allow_single_vendor=False
    )

    assert selected == [primary_a, primary_b]


def test_same_vendor_pair_is_insufficient_unless_allowed() -> None:
    first = _worker(0, "success", "gpt-4")
    same_vendor = _worker(1, "success", "gpt-5")
    distinct_vendor = _worker(2, "success", "qwen-fallback")

    selected_strict = select_contributing_set(
        [first], [same_vendor, distinct_vendor], allow_single_vendor=False
    )
    selected_allowed = select_contributing_set(
        [first], [same_vendor, distinct_vendor], allow_single_vendor=True
    )

    assert selected_strict == [first, distinct_vendor]
    assert selected_allowed == [first, same_vendor]


def test_same_model_id_pair_is_insufficient() -> None:
    first = _worker(0, "success", "qwen-same")
    same_model = _worker(1, "success", "qwen-same")
    distinct_model = _worker(2, "success", "deepseek-fallback")

    selected = select_contributing_set(
        [first], [same_model, distinct_model], allow_single_vendor=True
    )

    assert selected == [first, distinct_model]


def test_incident_inputs_select_t2model02_and_t1model01() -> None:
    t2_model01 = _worker(0, "proxy_error", "qwen-primary")
    t2_model02 = _worker(1, "success", "deepseek-primary")
    t2_model03 = _worker(2, "parse_error", "gpt-primary")
    t1_model01 = _worker(0, "success", "qwen-fallback")

    selected = select_contributing_set(
        [t2_model01, t2_model02, t2_model03],
        [t1_model01],
        allow_single_vendor=False,
    )

    assert selected == [t2_model02, t1_model01]
