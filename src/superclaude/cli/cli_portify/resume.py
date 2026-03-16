"""Resume semantics for the CLI Portify pipeline.

Implements:
- ResumabilityEntry dataclass (per step metadata)
- RESUMABILITY_MATRIX: dict[str, ResumabilityEntry] for all 7 steps
- TOTAL_STEPS constant
- is_resumable(), get_entry_requirements(), get_preserved_context()
- suggest_budget(), build_resume_command()
- validate_resume_entry(), build_resume_context()

Steps 1-4 are NOT resumable (deterministic, fast to re-run).
Steps 5-7 ARE resumable (Claude-assisted, expensive to re-run).

Per D-0037, D-0038 (SC-014), D-0052.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .models import FailureClassification, PortifyStepResult, PortifyStatus


# ---------------------------------------------------------------------------
# ResumabilityEntry
# ---------------------------------------------------------------------------


@dataclass
class ResumabilityEntry:
    """Metadata for a single pipeline step's resumability."""

    step_name: str
    step_number: int
    resumable: bool
    required_artifacts: tuple[str, ...] = field(default_factory=tuple)
    preserved_context: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# RESUMABILITY_MATRIX
# ---------------------------------------------------------------------------

RESUMABILITY_MATRIX: dict[str, ResumabilityEntry] = {
    "validate-config": ResumabilityEntry(
        step_name="validate-config",
        step_number=1,
        resumable=False,
        required_artifacts=(),
        preserved_context=(),
    ),
    "discover-components": ResumabilityEntry(
        step_name="discover-components",
        step_number=2,
        resumable=False,
        required_artifacts=(),
        preserved_context=(),
    ),
    "analyze-workflow": ResumabilityEntry(
        step_name="analyze-workflow",
        step_number=3,
        resumable=False,
        required_artifacts=(),
        preserved_context=(),
    ),
    "design-pipeline": ResumabilityEntry(
        step_name="design-pipeline",
        step_number=4,
        resumable=False,
        required_artifacts=(),
        preserved_context=(),
    ),
    "synthesize-spec": ResumabilityEntry(
        step_name="synthesize-spec",
        step_number=5,
        resumable=True,
        required_artifacts=("portify-analysis.md", "portify-spec.md"),
        preserved_context=(),
    ),
    "brainstorm-gaps": ResumabilityEntry(
        step_name="brainstorm-gaps",
        step_number=6,
        resumable=True,
        required_artifacts=("synthesized-spec.md",),
        preserved_context=("focus-findings.md",),
    ),
    "panel-review": ResumabilityEntry(
        step_name="panel-review",
        step_number=7,
        resumable=True,
        required_artifacts=("synthesized-spec.md", "brainstorm-gaps.md"),
        preserved_context=("focus-findings.md",),
    ),
}

TOTAL_STEPS: int = len(RESUMABILITY_MATRIX)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def is_resumable(step_name: str) -> bool:
    """Return True if the step can be resumed mid-pipeline."""
    entry = RESUMABILITY_MATRIX.get(step_name)
    return entry is not None and entry.resumable


def get_entry_requirements(step_name: str) -> tuple[str, ...]:
    """Return required artifact filenames for the given step, or ()."""
    entry = RESUMABILITY_MATRIX.get(step_name)
    if entry is None:
        return ()
    return entry.required_artifacts


def get_preserved_context(step_name: str) -> tuple[str, ...]:
    """Return preserved context filenames for the given step, or ()."""
    entry = RESUMABILITY_MATRIX.get(step_name)
    if entry is None or not entry.resumable:
        return ()
    return entry.preserved_context


def suggest_budget(
    step_name: str,
    max_convergence: int = 3,
) -> Optional[int]:
    """Return suggested turn budget for resuming at step_name.

    Returns None for non-resumable steps.
    """
    if not is_resumable(step_name):
        return None
    return max_convergence


def build_resume_command(
    step_name: str,
    workflow_path: str = "",
    max_convergence: Optional[int] = None,
) -> str:
    """Build a resume CLI command string for the given step.

    Returns empty string for non-resumable steps.
    """
    if not is_resumable(step_name):
        return ""

    parts = ["superclaude cli-portify run"]
    if workflow_path:
        parts.append(workflow_path)
    parts.append(f"--start {step_name}")
    if max_convergence is not None:
        parts.append(f"--max-convergence {max_convergence}")
    return " ".join(parts)


def validate_resume_entry(
    step_name: str,
    workdir: Path,
) -> tuple[bool, list[str], list[str]]:
    """Validate that a workdir contains all artifacts needed to resume at step.

    Returns:
        (valid, missing_list, preserved_list)
        - valid: True if all required artifacts present
        - missing_list: names of missing artifacts (or error messages)
        - preserved_list: absolute paths of present preserved-context files
    """
    entry = RESUMABILITY_MATRIX.get(step_name)
    if entry is None:
        return False, [f"Unknown step: {step_name!r}"], []

    if not entry.resumable:
        return False, [f"Step {step_name!r} is not resumable"], []

    missing: list[str] = []
    for artifact in entry.required_artifacts:
        if not (workdir / artifact).exists():
            missing.append(artifact)

    preserved: list[str] = []
    for ctx_file in entry.preserved_context:
        p = workdir / ctx_file
        if p.exists():
            preserved.append(str(p))

    return (len(missing) == 0), missing, preserved


# ---------------------------------------------------------------------------
# ResumeContext dataclass
# ---------------------------------------------------------------------------


@dataclass
class StepResumeContext:
    """Context produced by build_resume_context() for a failed step."""

    failed_step: str = ""
    failed_step_number: int = 0
    last_completed_step: str = ""
    last_completed_step_number: int = 0
    failure_classification: Optional[FailureClassification] = None
    re_run_required: bool = True
    resume_command: str = ""
    artifacts_preserved: list[str] = field(default_factory=list)


def build_resume_context(
    step_result: PortifyStepResult,
    workdir: Path,
    max_convergence: Optional[int] = None,
) -> StepResumeContext:
    """Build a StepResumeContext from a failed step result."""
    step_name = step_result.step_name
    step_number = step_result.step_number

    # Last completed step is step_number - 1
    last_number = max(0, step_number - 1)
    last_name = ""
    for name, entry in RESUMABILITY_MATRIX.items():
        if entry.step_number == last_number:
            last_name = name
            break

    cmd = build_resume_command(step_name, max_convergence=max_convergence)

    _, _, preserved = validate_resume_entry(step_name, workdir)

    # Also include required artifacts that exist
    entry = RESUMABILITY_MATRIX.get(step_name)
    if entry is not None:
        for artifact in entry.required_artifacts:
            p = workdir / artifact
            if p.exists() and str(p) not in preserved:
                preserved.append(str(p))

    return StepResumeContext(
        failed_step=step_name,
        failed_step_number=step_number,
        last_completed_step=last_name,
        last_completed_step_number=last_number,
        failure_classification=step_result.failure_classification,
        re_run_required=True,  # Failed step always needs to be re-run
        resume_command=cmd,
        artifacts_preserved=preserved,
    )
