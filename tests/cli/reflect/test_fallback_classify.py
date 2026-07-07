"""Unit tests for reflect Tier-2 fallback outcome classification."""

import pytest

from superclaude.cli.reflect.fallback import (
    FALLBACK_ELIGIBLE_STATUSES,
    classify_outcomes,
    is_fallback_eligible,
)
from superclaude.cli.swarm.models import WorkerResult, WorkerStatus


def _worker(
    index: int, status: WorkerStatus, model_id: str | None = None
) -> WorkerResult:
    return WorkerResult(
        index=index,
        status=status,
        model_id=model_id or f"model-{index}",
    )


def test_success_classifies_as_success_and_not_fallback_eligible() -> None:
    worker = _worker(0, "success")

    successes, eligible_failures = classify_outcomes([worker])

    assert successes == [worker]
    assert eligible_failures == []
    assert not is_fallback_eligible(worker)
    assert "success" not in FALLBACK_ELIGIBLE_STATUSES


@pytest.mark.parametrize("status", ["timeout", "proxy_error", "parse_error"])
def test_terminal_failures_classify_as_fallback_eligible(status: WorkerStatus) -> None:
    worker = _worker(1, status)

    successes, eligible_failures = classify_outcomes([worker])

    assert successes == []
    assert eligible_failures == [worker]
    assert is_fallback_eligible(worker)


def test_salvaged_parse_error_arrives_as_success_and_is_not_eligible() -> None:
    salvaged = _worker(2, "success", model_id="salvaged-model")

    successes, eligible_failures = classify_outcomes([salvaged])

    assert successes == [salvaged]
    assert eligible_failures == []
    assert not is_fallback_eligible(salvaged)


def test_classification_lists_are_disjoint_and_cover_input() -> None:
    workers = [
        _worker(0, "success"),
        _worker(1, "timeout"),
        _worker(2, "proxy_error"),
        _worker(3, "parse_error"),
    ]

    successes, eligible_failures = classify_outcomes(workers)

    assert not any(worker in eligible_failures for worker in successes)
    assert successes + eligible_failures == workers
