"""Sprint auto-resume package.

Read-first modules that reconstruct, validate, and risk-assess a resume plan
from on-disk sprint state. Nothing here mutates canonical results except the
BoundaryIntegrityGate's opt-in copy-to-quarantine (audit-logged, reversible).

Public surface (wired as each module lands):
    ResumePlanner          -> ResumePlan          (FR-1)
    DriftAssessor          -> DriftAssessment      (FR-3)
    BoundaryIntegrityGate  -> BoundaryReport       (FR-2)
    models                 -> dataclasses + enums

See .dev/brainstorms/20260602-sprint-auto-resume-default/design.md (DD-1..DD-5).
"""

from .drift import DriftAssessor
from .integrity import BoundaryIntegrityGate
from .models import (
    BoundaryReport,
    BoundaryTask,
    DriftAssessment,
    Granularity,
    ResumeDecision,
    ResumePlan,
)
from .planner import ResumePlanner

__all__ = [
    "BoundaryReport",
    "BoundaryTask",
    "BoundaryIntegrityGate",
    "DriftAssessment",
    "DriftAssessor",
    "Granularity",
    "ResumeDecision",
    "ResumePlan",
    "ResumePlanner",
]
