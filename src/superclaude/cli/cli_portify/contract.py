"""Return contract emission for the CLI Portify pipeline.

Implements:
- ContractStatus enum (SUCCESS, PARTIAL, FAILED, DRY_RUN)
- PhaseStatus dataclass
- StepTiming dataclass
- PortifyContract dataclass with to_dict() / to_json()
- build_success_contract(), build_partial_contract(),
  build_failed_contract(), build_dry_run_contract()
- generate_resume_command()
- RESUMABLE_STEPS

Per D-0003 / SC-011: return-contract.yaml emitted on all exit paths.
Per NFR-009: no None/empty fields on failure paths.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .models import PortifyStepResult, PortifyStatus


# ---------------------------------------------------------------------------
# ContractStatus
# ---------------------------------------------------------------------------


class ContractStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    DRY_RUN = "dry_run"


# ---------------------------------------------------------------------------
# RESUMABLE_STEPS — steps 5-7 are resumable
# ---------------------------------------------------------------------------

RESUMABLE_STEPS: frozenset[str] = frozenset(
    {
        "synthesize-spec",
        "brainstorm-gaps",
        "panel-review",
    }
)


# ---------------------------------------------------------------------------
# PhaseStatus
# ---------------------------------------------------------------------------


@dataclass
class PhaseStatus:
    name: str = ""
    status: str = "pending"
    steps_total: int = 0
    steps_completed: int = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "steps_total": self.steps_total,
            "steps_completed": self.steps_completed,
        }


# ---------------------------------------------------------------------------
# StepTiming
# ---------------------------------------------------------------------------


@dataclass
class StepTiming:
    step_name: str = ""
    duration_seconds: float = 0.0
    # Accept 'step' as an alias for 'step_name' for backward compatibility
    step: str = ""

    def __post_init__(self) -> None:
        # If 'step' was provided but 'step_name' was not, use step as step_name
        if self.step and not self.step_name:
            self.step_name = self.step

    def to_dict(self) -> dict:
        return {
            "step_name": self.step_name or self.step,
            "duration_seconds": self.duration_seconds,
        }


# ---------------------------------------------------------------------------
# PortifyContract
# ---------------------------------------------------------------------------


@dataclass
class PortifyContract:
    """Return contract emitted on all pipeline exit paths (SC-011).

    Default state is FAILED per NFR-009.
    """

    status: ContractStatus = ContractStatus.FAILED
    phases: list[PhaseStatus] = field(default_factory=lambda: _default_phases())
    artifacts: list[str] = field(default_factory=list)
    step_timings: list[StepTiming] = field(default_factory=list)
    gate_results: dict[str, str] = field(default_factory=dict)
    total_duration: float = 0.0
    error_message: str = ""
    resume_command: str = ""

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "phases": [p.to_dict() for p in self.phases],
            "artifacts": self.artifacts,
            "timing": {"total_duration": self.total_duration},
            "step_timings": [t.to_dict() for t in self.step_timings],
            "gate_results": self.gate_results,
            "error_message": self.error_message,
            "resume_command": self.resume_command,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


def _default_phases() -> list[PhaseStatus]:
    return [
        PhaseStatus("prerequisites", "pending", 2, 0),
        PhaseStatus("analysis", "pending", 2, 0),
        PhaseStatus("specification", "pending", 2, 0),
        PhaseStatus("synthesis", "pending", 1, 0),
    ]


# ---------------------------------------------------------------------------
# generate_resume_command
# ---------------------------------------------------------------------------


def generate_resume_command(
    resume_step: str,
    workflow_path: str = "",
    suggested_budget: Optional[int] = None,
) -> str:
    """Generate a resume CLI command for the given step.

    Returns empty string for non-resumable steps.
    """
    if resume_step not in RESUMABLE_STEPS:
        return ""

    parts = ["superclaude cli-portify run"]
    if workflow_path:
        parts.append(workflow_path)
    parts.append(f"--start {resume_step}")
    if suggested_budget is not None:
        parts.append(f"--max-convergence {suggested_budget}")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Builder helpers
# ---------------------------------------------------------------------------


def _all_completed_phases() -> list[PhaseStatus]:
    return [
        PhaseStatus("prerequisites", "completed", 2, 2),
        PhaseStatus("analysis", "completed", 2, 2),
        PhaseStatus("specification", "completed", 2, 2),
        PhaseStatus("synthesis", "completed", 1, 1),
    ]


def _dry_run_phases() -> list[PhaseStatus]:
    return [
        PhaseStatus("prerequisites", "completed", 2, 2),
        PhaseStatus("analysis", "completed", 2, 2),
        PhaseStatus("specification", "skipped", 2, 0),
        PhaseStatus("synthesis", "skipped", 1, 0),
    ]


def build_success_contract(
    artifacts: list[str],
    step_timings: list[StepTiming],
    gate_results: dict[str, str],
    total_duration: float,
) -> PortifyContract:
    """Build a SUCCESS return contract (all steps passed)."""
    return PortifyContract(
        status=ContractStatus.SUCCESS,
        phases=_all_completed_phases(),
        artifacts=artifacts,
        step_timings=step_timings,
        gate_results=gate_results,
        total_duration=total_duration,
        resume_command="",
    )


def build_partial_contract(
    step_results: list[PortifyStepResult],
    artifacts: list[str],
    step_timings: list[StepTiming],
    gate_results: dict[str, str],
    total_duration: float,
    resume_step: str = "",
) -> PortifyContract:
    """Build a PARTIAL return contract (halted mid-pipeline, resumable)."""
    return PortifyContract(
        status=ContractStatus.PARTIAL,
        phases=_default_phases(),
        artifacts=artifacts,
        step_timings=step_timings,
        gate_results=gate_results,
        total_duration=total_duration,
        resume_command=generate_resume_command(resume_step),
    )


def build_failed_contract(
    step_results: list[PortifyStepResult],
    artifacts: list[str],
    step_timings: list[StepTiming],
    gate_results: dict[str, str],
    total_duration: float,
    error_message: str = "",
    resume_step: str = "",
) -> PortifyContract:
    """Build a FAILED return contract (NFR-009: all fields populated)."""
    return PortifyContract(
        status=ContractStatus.FAILED,
        phases=_default_phases(),
        artifacts=artifacts,
        step_timings=step_timings,
        gate_results=gate_results,
        total_duration=total_duration,
        error_message=error_message,
        resume_command=generate_resume_command(resume_step),
    )


def build_dry_run_contract(
    step_results: list[PortifyStepResult],
    artifacts: list[str],
    step_timings: list[StepTiming],
    total_duration: float,
) -> PortifyContract:
    """Build a DRY_RUN return contract (phases 3-4 skipped per D-0003)."""
    return PortifyContract(
        status=ContractStatus.DRY_RUN,
        phases=_dry_run_phases(),
        artifacts=artifacts,
        step_timings=step_timings,
        gate_results={},
        total_duration=total_duration,
        resume_command="",
    )
