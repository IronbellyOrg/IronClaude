"""Dependency-respecting DAG scheduler for per-task parallel execution (Stage 3, H6).

Reuses the dependency-edge SHAPE that ``rerun_tasks.walk_dependencies`` /
``_dependencies_of`` already establish — the order-preserving, de-duplicated union
of a task's declared ``TaskEntry.dependencies`` and any deps recorded in a prior
``TaskResult`` — rather than introducing a fresh tasklist parser. The existing
``walk_dependencies`` does a single-level dependency expansion for rerun targets
(not a full topological order), so this module adds the topological/wave wrapper
that bounded parallelism (K>1) needs, while keeping the same audited edge
definition and the same ``_is_satisfied`` completion oracle semantics.

``topological_launch_order`` groups task ids into WAVES: each inner list is a set
of task ids whose dependencies are all already satisfied, so they may be launched
concurrently. Waves are emitted in dependency order; within a wave the declared
task order is preserved for determinism. A dependency cycle is detected and
surfaced via :class:`CycleError` (never silently dropped).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .models import TaskEntry, TaskResult


class CycleError(ValueError):
    """Raised when the task dependency graph contains a cycle.

    ``unresolved`` holds the task ids that could not be ordered (the members of
    the cycle and anything transitively waiting on it).
    """

    def __init__(self, unresolved: list[str]) -> None:
        self.unresolved = list(unresolved)
        super().__init__(
            f"dependency cycle detected among tasks: {', '.join(self.unresolved)}"
        )


def dependencies_of(
    task_id: str,
    entry_by_id: dict[str, "TaskEntry"],
    result_by_id: Optional[dict[str, "TaskResult"]] = None,
) -> list[str]:
    """Order-preserving de-duplicated union of a task's declared + recorded deps.

    Mirrors ``rerun_tasks._dependencies_of``: the declared ``TaskEntry.dependencies``
    unioned with any dependencies recorded on a persisted ``TaskResult`` (when a
    ``result_by_id`` snapshot is supplied). Self-edges are dropped. Only deps that
    refer to tasks present in ``entry_by_id`` (intra-set) are kept — cross-phase
    deps are resolved elsewhere (``walk_dependencies`` / checkpoints).
    """
    ordered: list[str] = []
    seen: set[str] = set()

    def _add(dep: str) -> None:
        if dep and dep != task_id and dep in entry_by_id and dep not in seen:
            seen.add(dep)
            ordered.append(dep)

    entry = entry_by_id.get(task_id)
    if entry is not None:
        for dep in entry.dependencies:
            _add(dep)
    if result_by_id is not None:
        recorded = result_by_id.get(task_id)
        recorded_deps = getattr(getattr(recorded, "task", None), "dependencies", [])
        for dep in recorded_deps or []:
            _add(dep)
    return ordered


def topological_launch_order(
    tasks: list["TaskEntry"],
    result_by_id: Optional[dict[str, "TaskResult"]] = None,
) -> list[list[str]]:
    """Return a dependency-respecting wave grouping of task ids.

    Each inner list is a wave: task ids whose every dependency is already in a
    prior wave, hence safe to launch concurrently. Declared order is preserved
    within a wave for determinism. Raises :class:`CycleError` if a cycle prevents
    ordering some tasks.
    """
    ordered_ids = [t.task_id for t in tasks]
    entry_by_id = {t.task_id: t for t in tasks}
    deps = {tid: dependencies_of(tid, entry_by_id, result_by_id) for tid in ordered_ids}

    satisfied: set[str] = set()
    remaining = list(ordered_ids)
    waves: list[list[str]] = []

    while remaining:
        wave = [tid for tid in remaining if all(d in satisfied for d in deps[tid])]
        if not wave:
            # No task has all deps satisfied, yet tasks remain → a cycle (or a
            # dep on a missing task that survived the intra-set filter, which the
            # filter prevents). Surface it instead of dropping tasks.
            raise CycleError(remaining)
        waves.append(wave)
        satisfied.update(wave)
        remaining = [tid for tid in remaining if tid not in satisfied]

    return waves


def is_task_satisfied(
    task_id: str, result_by_id: dict[str, "TaskResult"]
) -> Optional[bool]:
    """Completion oracle mirroring ``rerun_tasks._is_satisfied``.

    Returns True if the task has a recorded validated-success result
    (``status.is_success``), False if recorded-but-not-successful, and None if
    there is no record (unknown / not yet attempted).
    """
    tr = result_by_id.get(task_id)
    if tr is None:
        return None
    return tr.status.is_success
