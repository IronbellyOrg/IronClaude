"""Dataclasses and enums for the sprint auto-resume feature.

Field names/types follow design.md §2 verbatim. ``TaskStatus`` / ``PhaseStatus``
are reused from the parent ``sprint.models`` module (the canonical status vocab).

INVARIANT (NFR-3): ``BoundaryReport.coherence_warnings`` is advisory-only and is
NEVER a term in ``BoundaryReport.passed``. The gate verdict is a pure function of
deterministic signals; the Haiku coherence read can only annotate, never veto.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from superclaude.cli.sprint.models import TaskStatus

__all__ = [
    "Granularity",
    "BoundaryTask",
    "ResumePlan",
    "DriftAssessment",
    "BoundaryReport",
    "ResumeDecision",
]


class Granularity(Enum):
    """How the interrupted phase will be resumed."""

    TASK = "task"  # boundary phase has clean per-task data → rerun-tasks engine
    PHASE = "phase"  # no per-task data (hard crash) → executor loop re-runs phase
    NONE = "none"  # nothing to resume / fresh


@dataclass
class BoundaryTask:
    """A single task on the resume seam of the interrupted phase.

    ``persisted_status`` is Signal A (from ``phase-N-result.json``);
    ``derived_status`` is Signal B (independent re-derivation via
    ``_classify_transcript``). ``suspect`` is set when A/B disagree OR declared
    artifacts are missing.
    """

    task_id: str
    persisted_status: TaskStatus | None = None  # Signal A
    derived_status: TaskStatus | None = None  # Signal B
    artifacts_present: bool = False  # declared deliverables/checkpoints exist
    role: str = "pending"  # "last_completed" | "next_unfinished" | "pending"
    suspect: bool = False  # A/B disagree OR artifacts missing
    # The phase this boundary task belongs to. None ⇒ the interrupted phase
    # (default, backward-compatible). Set to a PRIOR phase number when the planner
    # emits a prior-phase-tail `last_completed` on a PHASE hard crash, so the
    # integrity gate resolves the transcript/deliverables under `phase-{phase}-...`
    # rather than the interrupted phase (F-4/CG-3).
    phase: int | None = None


@dataclass
class ResumePlan:
    """Pure-read reconstruction of where the previous run was interrupted."""

    index_path: Path
    release_dir: Path
    completed_phases: list[int] = field(default_factory=list)
    interrupted_phase: int | None = None  # dangling phase_start, or first non-complete
    interrupt_kind: str = "none"  # "complete" | "interrupt" | "crash" | "none"
    start_phase: int = 1
    end_phase: int = 0
    granularity: Granularity = Granularity.NONE
    boundary_tasks: list[BoundaryTask] = field(
        default_factory=list
    )  # interrupted phase only
    rerun_task_ids: list[str] = field(default_factory=list)  # task-level dispatch set
    ambiguous: bool = False  # FR-5 → list + STOP
    ambiguity_reasons: list[str] = field(default_factory=list)


@dataclass
class DriftAssessment:
    """Tiered safety-of-resume confidence for the boundary phase's tasklist."""

    confidence: float  # [0, 1] safety-of-resume
    tier: str = ""  # "hash" | "structural" | "git"
    changed_paths: list[str] = field(default_factory=list)
    explanation: str = ""  # FR-3.5 (why the score is what it is)
    cosmetic_only: bool = False


@dataclass
class BoundaryReport:
    """Integrity-gate verdict for the resume seam.

    ``passed`` is a pure function of deterministic signals (validated_last, no
    unresolved suspects, partial work quarantined-or-accepted). ``coherence_warnings``
    are advisory Haiku flags surfaced for the operator and are NOT part of ``passed``
    (NFR-3).
    """

    validated_last: bool = False
    suspects: list[BoundaryTask] = field(default_factory=list)
    quarantined: dict[Path, Path] = field(
        default_factory=dict
    )  # canonical → quarantine copy
    passed: bool = False  # gate verdict (FR-2.4) — deterministic only
    blocking_reasons: list[str] = field(default_factory=list)
    coherence_warnings: list[tuple[BoundaryTask, str]] = field(
        default_factory=list
    )  # advisory; NOT part of `passed` (NFR-3)
    # report-only suspect paths (FR-2.2 / §4(b) "always"); populated regardless of
    # cleanup_opted_in, so the operator sees half-written artifacts on the default
    # report-only path (F-2/CG-1). NEVER a term in ``passed`` (NFR-3).
    partial_paths: list[Path] = field(default_factory=list)


@dataclass
class ResumeDecision:
    """Aggregate returned by the ``_auto_resume`` commands helper (design §8).

    ``action`` is the control-flow verb the CLI acts on:
    "proceed" | "stop" | "nothing_to_resume" | "ambiguous" | "dry_run".
    ``exit_code`` is the process exit status the caller should honor.
    """

    plan: ResumePlan | None = None
    drift: DriftAssessment | None = None
    report: BoundaryReport | None = None
    action: str = "proceed"
    messages: list[str] = field(default_factory=list)
    exit_code: int = 0
