"""Tasklist data models -- TasklistValidateConfig.

TasklistValidateConfig extends PipelineConfig with tasklist-specific fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..pipeline.models import PipelineConfig


@dataclass
class TasklistValidateConfig(PipelineConfig):
    """Configuration for the tasklist validation pipeline.

    Extends PipelineConfig with tasklist-specific fields:
    output_dir, roadmap_file, tasklist_dir.
    """

    output_dir: Path = field(default_factory=lambda: Path("."))
    roadmap_file: Path = field(default_factory=lambda: Path("."))
    tasklist_dir: Path = field(default_factory=lambda: Path("."))
    tdd_file: Path | None = None  # TDD integration: optional TDD file for enriched validation
    prd_file: Path | None = None  # PRD integration: optional PRD file for business context enrichment
