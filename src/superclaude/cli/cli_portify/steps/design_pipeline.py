"""Step 4: design-pipeline — Claude-assisted pipeline design.

Produces portify-pipeline-design.md with step definitions, gate assignments,
and data-flow mapping.

Gate: STRICT (SC-004).
Dry-run halt: if config.dry_run=True, emits dry_run contract and returns SKIPPED.
Review gate: pauses for user approval (y/n) before synthesis phase (unless skip_review).
"""

from __future__ import annotations

import json
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

STEP_NAME = "design-pipeline"
STEP_NUMBER = 4
PHASE = 2
GATE_TIER = "STRICT"
ARTIFACT_NAME = "portify-spec.md"


def run_design_pipeline(config: PortifyConfig) -> PortifyStepResult:
    """Execute Step 4: design-pipeline.

    Requires portify-analysis.md from Step 3.
    Produces portify-pipeline-design.md.

    Dry-run halt (SC-011): if config.dry_run=True, emits contract JSON and returns SKIPPED.
    Review gate: prompts user for approval (y/n) unless config.skip_review=True.
    """
    start = time.monotonic()
    results_dir = (
        config.output_dir / "results" if config.output_dir else Path("results")
    )
    results_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = results_dir / ARTIFACT_NAME
    error_path = results_dir / f"{STEP_NAME}-error.log"

    # Check prerequisite: portify-analysis.md from Step 3
    analysis_path = results_dir / "portify-analysis.md"
    if not analysis_path.exists():
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.MISSING_ARTIFACT,
            gate_tier=GATE_TIER,
            error_message=f"Missing prerequisite: {analysis_path}",
            duration_seconds=time.monotonic() - start,
        )

    # Run Claude subprocess
    work_dir = config.workdir_path or results_dir
    workflow_path = config.workflow_path or Path(".")

    process = PortifyProcess(
        prompt=_build_prompt(config, analysis_path),
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
            failure_classification=FailureClassification.MISSING_ARTIFACT,
            gate_tier=GATE_TIER,
            error_message=f"Subprocess exited {result.exit_code}",
            duration_seconds=duration,
        )

    # Read output
    if result.output_file and result.output_file.exists():
        content = result.output_file.read_text(encoding="utf-8", errors="replace")
    elif artifact_path.exists():
        content = artifact_path.read_text(encoding="utf-8", errors="replace")
    else:
        content = result.stdout_text

    # Gate check (SC-004)
    if not _check_gate(content):
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.GATE_FAILURE,
            gate_tier=GATE_TIER,
            artifact_path=str(artifact_path),
            error_message="Gate SC-004 failed",
            duration_seconds=duration,
        )

    # Write artifact if not already written
    if not artifact_path.exists():
        artifact_path.write_text(content, encoding="utf-8")

    # Dry-run halt (SC-011 / SC-012): emit dry_run contract and return SKIPPED
    if getattr(config, "dry_run", False):
        from ..contract import build_dry_run_contract, StepTiming

        contract = build_dry_run_contract(
            step_results=[],
            artifacts=[str(artifact_path)],
            step_timings=[StepTiming(step_name=STEP_NAME, duration_seconds=duration)],
            total_duration=duration,
        )
        print(contract.to_json())
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.SKIPPED,
            gate_tier=GATE_TIER,
            artifact_path=str(artifact_path),
            duration_seconds=duration,
        )

    # Review gate (unless skip_review)
    if not getattr(config, "skip_review", True):
        try:
            answer = (
                input(
                    f"\nReview the pipeline design at {artifact_path}\nAccept? [y/n]: "
                )
                .strip()
                .lower()
            )
        except (EOFError, KeyboardInterrupt):
            answer = "n"

        if answer != "y":
            return PortifyStepResult(
                step_name=STEP_NAME,
                step_number=STEP_NUMBER,
                phase=PHASE,
                portify_status=PortifyStatus.FAIL,
                failure_classification=FailureClassification.USER_REJECTION,
                gate_tier=GATE_TIER,
                artifact_path=str(artifact_path),
                review_required=True,
                review_accepted=False,
                error_message="User rejected pipeline design",
                duration_seconds=duration,
            )

        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.PASS,
            gate_tier=GATE_TIER,
            artifact_path=str(artifact_path),
            review_required=True,
            review_accepted=True,
            duration_seconds=duration,
        )

    return PortifyStepResult(
        step_name=STEP_NAME,
        step_number=STEP_NUMBER,
        phase=PHASE,
        portify_status=PortifyStatus.PASS,
        gate_tier=GATE_TIER,
        artifact_path=str(artifact_path),
        duration_seconds=duration,
    )


def _check_gate(content: str) -> bool:
    """SC-004: pipeline_steps frontmatter field must be present and > 0."""
    from ..utils import parse_frontmatter

    frontmatter, _ = parse_frontmatter(content)
    return bool(frontmatter) and int(frontmatter.get("pipeline_steps", 0)) > 0


def _build_prompt(config: PortifyConfig, analysis_path: Path) -> str:
    return (
        f"Design a CLI pipeline for the workflow at {config.workflow_path}. "
        f"Analysis: {analysis_path}. "
        "Produce portify-pipeline-design.md with step definitions and gate assignments."
    )
