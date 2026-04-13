"""PRD pipeline data models -- domain types for the PRD generation pipeline.

Extends the shared pipeline primitives (PipelineConfig, StepResult) with
PRD-specific configuration, step statuses, and aggregate result types.

NFR-PRD.1: Zero ``async def`` or ``await`` in this module.
NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

from superclaude.cli.pipeline.models import PipelineConfig, StepResult


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ExistingWorkState(Enum):
    """Detection result for pre-existing PRD work in the task directory."""

    NO_EXISTING = "no_existing"
    RESUME_STAGE_A = "resume_stage_a"
    RESUME_STAGE_B = "resume_stage_b"
    ALREADY_COMPLETE = "already_complete"


class PrdStepStatus(Enum):
    """Lifecycle status for PRD pipeline steps.

    Thirteen states covering normal execution, partial success,
    fix-cycle triggers, and terminal failures.
    """

    PENDING = "pending"
    RUNNING = "running"
    PASS = "pass"
    PASS_NO_SIGNAL = "pass_no_signal"
    PASS_NO_REPORT = "pass_no_report"
    INCOMPLETE = "incomplete"
    HALT = "halt"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"
    QA_FAIL = "qa_fail"
    QA_FAIL_EXHAUSTED = "qa_fail_exhausted"
    VALIDATION_FAIL = "validation_fail"

    @property
    def is_terminal(self) -> bool:
        """True if no further processing will occur for this step."""
        return self in (
            PrdStepStatus.PASS,
            PrdStepStatus.PASS_NO_SIGNAL,
            PrdStepStatus.PASS_NO_REPORT,
            PrdStepStatus.HALT,
            PrdStepStatus.TIMEOUT,
            PrdStepStatus.ERROR,
            PrdStepStatus.SKIPPED,
            PrdStepStatus.QA_FAIL_EXHAUSTED,
            PrdStepStatus.VALIDATION_FAIL,
        )

    @property
    def is_success(self) -> bool:
        """True if the step completed successfully (any pass variant)."""
        return self in (
            PrdStepStatus.PASS,
            PrdStepStatus.PASS_NO_SIGNAL,
            PrdStepStatus.PASS_NO_REPORT,
        )

    @property
    def is_failure(self) -> bool:
        """True if the step ended in a non-recoverable failure."""
        return self in (
            PrdStepStatus.HALT,
            PrdStepStatus.TIMEOUT,
            PrdStepStatus.ERROR,
            PrdStepStatus.QA_FAIL_EXHAUSTED,
            PrdStepStatus.VALIDATION_FAIL,
        )

    @property
    def needs_fix_cycle(self) -> bool:
        """True if this status should trigger a fix cycle retry."""
        return self in (
            PrdStepStatus.QA_FAIL,
            PrdStepStatus.INCOMPLETE,
        )


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class PrdConfig(PipelineConfig):
    """Configuration for the PRD pipeline.

    Extends PipelineConfig with PRD-specific fields for request parsing,
    template selection, partitioning thresholds, and resume control.
    """

    user_message: str = ""
    product_name: str = ""
    product_slug: str = ""
    prd_scope: str = "feature"
    scenario: str = "B"
    where: list[str] = field(default_factory=list)
    why: str = ""
    output_path: Path = field(default_factory=lambda: Path("."))
    tier: str = "standard"
    task_dir: Path = field(default_factory=lambda: Path("."))
    template_path: Path = field(
        default_factory=lambda: Path(
            "docs/docs-product/templates/prd_template.md"
        )
    )
    skill_refs_dir: Path = field(
        default_factory=lambda: Path("src/superclaude/skills/prd/refs")
    )
    max_turns: int = 300
    stall_timeout: int = 120
    stall_action: str = "warn"
    max_research_fix_cycles: int = 3
    max_synthesis_fix_cycles: int = 2
    research_partition_threshold: int = 6
    synthesis_partition_threshold: int = 4
    resume_from: Optional[str] = None

    @property
    def research_dir(self) -> Path:
        """Directory for research output files."""
        return self.task_dir / "research"

    @property
    def synthesis_dir(self) -> Path:
        """Directory for synthesis output files."""
        return self.task_dir / "synthesis"

    @property
    def qa_dir(self) -> Path:
        """Directory for QA report files."""
        return self.task_dir / "qa"


# ---------------------------------------------------------------------------
# Step Results
# ---------------------------------------------------------------------------


@dataclass
class PrdStepResult(StepResult):
    """Outcome of executing a single PRD pipeline step.

    Extends StepResult with execution telemetry fields specific to
    subprocess-driven PRD generation.
    """

    exit_code: int = 0
    output_bytes: int = 0
    error_bytes: int = 0
    artifacts_produced: list[str] = field(default_factory=list)
    agent_type: str = ""
    fix_cycle: int = 0
    qa_verdict: Optional[str] = None


# ---------------------------------------------------------------------------
# Pipeline Result
# ---------------------------------------------------------------------------


@dataclass
class PrdPipelineResult:
    """Aggregate result for the entire PRD pipeline run."""

    config: PrdConfig
    step_results: list[PrdStepResult] = field(default_factory=list)
    outcome: str = "success"
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    finished_at: Optional[datetime] = None
    halt_step: Optional[str] = None
    halt_reason: Optional[str] = None
    research_agent_count: int = 0
    web_agent_count: int = 0
    synthesis_agent_count: int = 0
    research_fix_cycles: int = 0
    synthesis_fix_cycles: int = 0
    final_prd_lines: int = 0
    final_prd_path: str = ""

    def resume_command(self) -> str:
        """Generate CLI invocation to resume from the halted step."""
        if not self.halt_step:
            return ""
        parts = ["superclaude", "prd", "resume", self.halt_step]
        if self.config.product_name:
            parts.extend(["--product", self.config.product_name])
        if self.config.model:
            parts.extend(["--model", self.config.model])
        if self.config.tier != "standard":
            parts.extend(["--tier", self.config.tier])
        return " ".join(parts)

    @property
    def suggested_resume_budget(self) -> int:
        """Estimate remaining turn budget for a resumed run."""
        used_turns = sum(
            1 for r in self.step_results if r.status.is_terminal
        ) if self.step_results else 0
        remaining = max(self.config.max_turns - (used_turns * 10), 50)
        return remaining


# ---------------------------------------------------------------------------
# Monitor State
# ---------------------------------------------------------------------------


@dataclass
class PrdMonitorState:
    """Real-time state extracted by the sidecar monitor thread.

    Updated from NDJSON signal lines emitted by subprocess agents.
    """

    output_bytes: int = 0
    last_event_time: float = field(default_factory=time.monotonic)
    events_received: int = 0
    last_step_id: str = ""
    current_artifact: str = ""
    research_files_completed: int = 0
    synth_files_completed: int = 0
    qa_verdict: Optional[str] = None
    current_agent_type: str = ""
    fix_cycle_count: int = 0
