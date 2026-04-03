"""Roadmap data models -- RoadmapConfig and AgentSpec.

RoadmapConfig extends PipelineConfig with roadmap-specific fields.
AgentSpec represents a model:persona pair for generate steps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from ..pipeline.models import PipelineConfig


VALID_FINDING_STATUSES = frozenset({"PENDING", "ACTIVE", "FIXED", "FAILED", "SKIPPED"})
VALID_DEVIATION_CLASSES = frozenset(
    {"SLIP", "INTENTIONAL", "AMBIGUOUS", "PRE_APPROVED", "UNCLASSIFIED"}
)


@dataclass
class Finding:
    """A single validation finding extracted from a report.

    Fields align with spec §2.3.1. Status lifecycle defined in D-0003:
    PENDING/ACTIVE -> FIXED | FAILED | SKIPPED (all terminal).

    deviation_class classifies the deviation source (v2.26):
    SLIP, INTENTIONAL, AMBIGUOUS, PRE_APPROVED, or UNCLASSIFIED (default).
    """

    id: str
    severity: str
    dimension: str
    description: str
    location: str
    evidence: str
    fix_guidance: str
    files_affected: list[str] = field(default_factory=list)
    status: str = "PENDING"
    agreement_category: str = ""
    deviation_class: str = "UNCLASSIFIED"
    source_layer: str = "structural"
    # v3.05 extensions (FR-3, FR-6) — all defaulted for backward compatibility
    rule_id: str = ""
    spec_quote: str = ""
    roadmap_quote: str = ""
    stable_id: str = ""

    def __post_init__(self) -> None:
        if self.status not in VALID_FINDING_STATUSES:
            raise ValueError(
                f"Invalid Finding status {self.status!r}. "
                f"Must be one of: {', '.join(sorted(VALID_FINDING_STATUSES))}"
            )
        if self.deviation_class not in VALID_DEVIATION_CLASSES:
            raise ValueError(
                f"Invalid deviation_class {self.deviation_class!r}. "
                f"Must be one of: {', '.join(sorted(VALID_DEVIATION_CLASSES))}"
            )


@dataclass
class AgentSpec:
    """Represents a model:persona pair for a generate step.

    The model value is passed directly to ``claude -p --model``
    (no resolution -- claude CLI accepts opus/sonnet/haiku natively).
    """

    model: str
    persona: str

    @classmethod
    def parse(cls, spec: str) -> AgentSpec:
        """Parse a 'model:persona' or 'model' string into an AgentSpec.

        Examples:
            AgentSpec.parse("opus:architect") -> AgentSpec("opus", "architect")
            AgentSpec.parse("haiku")          -> AgentSpec("haiku", "architect")
        """
        if ":" in spec:
            model, persona = spec.split(":", 1)
            return cls(model=model.strip(), persona=persona.strip())
        return cls(model=spec.strip(), persona="architect")

    @property
    def id(self) -> str:
        """Short identifier for filenames, e.g. 'opus-architect'."""
        return f"{self.model}-{self.persona}"


@dataclass
class RoadmapConfig(PipelineConfig):
    """Configuration for the roadmap generation pipeline.

    Extends PipelineConfig with roadmap-specific fields:
    spec_file, agents, depth, output_dir, retrospective_file.
    """

    spec_file: Path = field(default_factory=lambda: Path("."))
    agents: list[AgentSpec] = field(
        default_factory=lambda: [
            AgentSpec("opus", "architect"),
            AgentSpec("haiku", "architect"),
        ]
    )
    depth: Literal["quick", "standard", "deep"] = "standard"
    output_dir: Path = field(default_factory=lambda: Path("."))
    retrospective_file: Path | None = None
    convergence_enabled: bool = True  # v3.05: deterministic fidelity convergence engine (default ON)
    allow_regeneration: bool = False  # FR-9: override diff-size guard for full regeneration
    input_type: Literal["auto", "tdd", "spec", "prd"] = "auto"  # auto=detect from content, tdd/spec/prd=force
    tdd_file: Path | None = None  # TDD integration: optional TDD file path for downstream enrichment
    prd_file: Path | None = None  # PRD integration: optional PRD file path for business context enrichment


@dataclass
class ValidateConfig(PipelineConfig):
    """Configuration for the roadmap validation pipeline.

    Extends PipelineConfig with validation-specific fields:
    output_dir, agents. Inherits model, max_turns, debug from PipelineConfig.
    """

    output_dir: Path = field(default_factory=lambda: Path("."))
    agents: list[AgentSpec] = field(
        default_factory=lambda: [
            AgentSpec("opus", "architect"),
            AgentSpec("haiku", "architect"),
        ]
    )
