"""M4 — dedicated tests for the sprint DAG scheduler (scheduler.py).

The sprint scheduler (``topological_launch_order`` / ``dependencies_of`` /
``is_task_satisfied``) had zero dedicated tests despite gating bounded-parallel
(K>1) launch ordering. This file pins wave ordering (diamond, linear chain,
independent), cycle detection, self-edge drop, unknown/cross-set dep filtering,
dependency de-dup/union, and the tri-state completion oracle. Every expected
output is traced from the real scheduler (research 03) — asserted exactly, not
re-derived.
"""

from __future__ import annotations

import pytest

from superclaude.cli.sprint.models import TaskEntry, TaskResult, TaskStatus
from superclaude.cli.sprint.scheduler import (
    CycleError,
    dependencies_of,
    is_task_satisfied,
    topological_launch_order,
)


def te(task_id: str, deps: list[str] | None = None) -> TaskEntry:
    return TaskEntry(task_id=task_id, title=task_id, dependencies=list(deps or []))


@pytest.mark.unit
def test_diamond_waves() -> None:
    tasks = [te("A"), te("B", ["A"]), te("C", ["A"]), te("D", ["B", "C"])]
    assert topological_launch_order(tasks) == [["A"], ["B", "C"], ["D"]]


@pytest.mark.unit
def test_linear_chain_waves() -> None:
    tasks = [te("A"), te("B", ["A"]), te("C", ["B"])]
    assert topological_launch_order(tasks) == [["A"], ["B"], ["C"]]


@pytest.mark.unit
def test_independent_tasks_single_wave_declared_order() -> None:
    tasks = [te("A"), te("B"), te("C")]
    assert topological_launch_order(tasks) == [["A", "B", "C"]]
    # within-wave order == declared order is deterministic (scheduler.py:94)
    assert topological_launch_order([te("C"), te("A"), te("B")]) == [["C", "A", "B"]]


@pytest.mark.unit
def test_cycle_raises_cycle_error() -> None:
    tasks = [te("A", ["C"]), te("B", ["A"]), te("C", ["B"])]
    with pytest.raises(CycleError) as exc:
        topological_launch_order(tasks)
    assert exc.value.unresolved == ["A", "B", "C"]  # declared order
    assert str(exc.value) == "dependency cycle detected among tasks: A, B, C"


@pytest.mark.unit
def test_self_edge_dropped() -> None:
    tasks = [te("A", ["A"]), te("B", ["A"])]
    assert topological_launch_order(tasks) == [["A"], ["B"]]
    # self-edge dropped at scheduler.py:57-60
    assert dependencies_of("A", {"A": te("A", ["A"])}) == []


@pytest.mark.unit
def test_unknown_dep_filtered() -> None:
    tasks = [te("A", ["Z"]), te("B", ["A"])]
    assert topological_launch_order(tasks) == [["A"], ["B"]]
    # intra-set filter: "Z" not in entry_by_id -> dropped (scheduler.py:58)
    assert dependencies_of("A", {"A": te("A", ["Z"]), "B": te("B", ["A"])}) == []


@pytest.mark.unit
def test_dependencies_of_dedup_preserves_order() -> None:
    # de-dup, declared order, with B and C present in entry_by_id
    assert dependencies_of(
        "D", {"D": te("D", ["B", "B", "C"]), "B": te("B"), "C": te("C")}
    ) == ["B", "C"]


@pytest.mark.unit
def test_dependencies_of_unions_recorded_deps() -> None:
    # declared dep B first, then recorded dep C (scheduler.py:63-70)
    assert dependencies_of(
        "A",
        {"A": te("A", ["B"]), "B": te("B"), "C": te("C")},
        {"A": TaskResult(task=te("A", ["C"]), status=TaskStatus.PASS)},
    ) == ["B", "C"]


@pytest.mark.unit
def test_is_task_satisfied_tristate() -> None:
    assert is_task_satisfied("A", {}) is None  # unknown / not attempted
    assert (
        is_task_satisfied("A", {"A": TaskResult(task=te("A"), status=TaskStatus.PASS)})
        is True
    )
    assert (
        is_task_satisfied(
            "A", {"A": TaskResult(task=te("A"), status=TaskStatus.PASS_RECOVERED)}
        )
        is True
    )
    assert (
        is_task_satisfied(
            "A", {"A": TaskResult(task=te("A"), status=TaskStatus.SKIPPED)}
        )
        is False
    )
