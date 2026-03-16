"""Step 3: analyze-workflow — Claude-assisted workflow analysis.

Produces portify-analysis.md with a workflow summary, component analysis,
data-flow diagram, complexity assessment, and recommendations.

Gate: STRICT (SC-003: 5 required sections present in output).
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

from ..models import (
    FailureClassification,
    PortifyConfig,
    PortifyStatus,
    PortifyStepResult,
)
from ..process import PortifyProcess, ProcessResult

log = logging.getLogger(__name__)

STEP_NAME = "analyze-workflow"
STEP_NUMBER = 3
PHASE = 2
GATE_TIER = "STRICT"
ARTIFACT_NAME = "portify-analysis.md"
REQUIRED_SECTIONS = (
    "Workflow Summary",
    "Component Analysis",
    "Data Flow",
    "Complexity Assessment",
    "Recommendations",
)


def run_analyze_workflow(config: PortifyConfig) -> PortifyStepResult:
    """Execute Step 3: analyze-workflow.

    Requires component-inventory.md from Step 2.
    Produces portify-analysis.md with 5 required sections (SC-003).
    """
    start = time.monotonic()
    results_dir = config.output_dir / "results" if config.output_dir else Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = results_dir / ARTIFACT_NAME
    error_path = results_dir / f"{STEP_NAME}-error.log"

    # Check prerequisite: component-inventory.md from Step 2
    inventory_path = results_dir / "component-inventory.md"
    if not inventory_path.exists():
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.MISSING_ARTIFACT,
            gate_tier=GATE_TIER,
            error_message=f"Missing prerequisite: {inventory_path}",
            duration_seconds=time.monotonic() - start,
        )

    # Run Claude subprocess
    work_dir = config.workdir_path or results_dir
    workflow_path = config.workflow_path or Path(".")

    process = PortifyProcess(
        prompt=_build_prompt(config, inventory_path),
        output_file=artifact_path,
        error_file=error_path,
        work_dir=Path(work_dir),
        workflow_path=Path(workflow_path),
        max_turns=config.max_turns,
        model=config.model,
    )
    result: ProcessResult = process.run()

    duration = time.monotonic() - start

    # Handle subprocess failures
    if result.timed_out or result.exit_code == 124:
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.TIMEOUT,
            failure_classification=FailureClassification.TIMEOUT,
            gate_tier=GATE_TIER,
            error_message="Claude subprocess timed out",
            duration_seconds=duration,
        )

    if result.exit_code != 0:
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.GATE_FAILURE,
            gate_tier=GATE_TIER,
            error_message=f"Subprocess exited {result.exit_code}",
            duration_seconds=duration,
        )

    # Read output content
    if result.output_file and result.output_file.exists():
        content = result.output_file.read_text(encoding="utf-8", errors="replace")
    elif artifact_path.exists():
        content = artifact_path.read_text(encoding="utf-8", errors="replace")
    else:
        content = result.stdout_text

    # Run gate check (SC-003)
    gate_status = _check_gate(content)
    if gate_status != PortifyStatus.PASS:
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.GATE_FAILURE,
            gate_tier=GATE_TIER,
            artifact_path=str(artifact_path),
            error_message="Gate SC-003 failed: missing required sections",
            duration_seconds=duration,
        )

    # Write artifact if not already written
    if not artifact_path.exists():
        artifact_path.write_text(content, encoding="utf-8")

    return PortifyStepResult(
        step_name=STEP_NAME,
        step_number=STEP_NUMBER,
        phase=PHASE,
        portify_status=PortifyStatus.PASS,
        gate_tier=GATE_TIER,
        artifact_path=str(artifact_path),
        duration_seconds=duration,
    )


def _check_gate(content: str) -> PortifyStatus:
    """SC-003: All 5 required sections must be present."""
    from ..utils import parse_frontmatter
    _, body = parse_frontmatter(content)
    for section in REQUIRED_SECTIONS:
        if section.lower() not in body.lower():
            return PortifyStatus.FAIL
    return PortifyStatus.PASS


def _build_prompt(config: PortifyConfig, inventory_path: Path) -> str:
    return (
        f"Analyze the workflow at {config.workflow_path}. "
        f"Component inventory: {inventory_path}. "
        "Produce portify-analysis.md with sections: Workflow Summary, "
        "Component Analysis, Data Flow, Complexity Assessment, Recommendations."
    )
