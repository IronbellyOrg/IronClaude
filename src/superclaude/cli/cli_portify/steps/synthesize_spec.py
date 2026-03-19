"""Step 5: synthesize-spec — Claude-assisted spec synthesis.

Produces synthesized-spec.md from the portify template.

Gate: STRICT (SC-005: zero {{SC_PLACEHOLDER:*}} sentinels in output).
Retry logic: on sentinel detection, retries with specific placeholder names.

This step is RESUMABLE (steps >= 5).
"""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path
from typing import Optional, Union

from ..models import (
    FailureClassification,
    PortifyConfig,
    PortifyStatus,
    PortifyStepResult,
)
from ..process import PortifyProcess, ProcessResult

log = logging.getLogger(__name__)

STEP_NAME = "synthesize-spec"
STEP_NUMBER = 5
PHASE = 3
GATE_TIER = "STRICT"
ARTIFACT_NAME = "synthesized-spec.md"

SENTINEL_PATTERN = re.compile(r"\{\{SC_PLACEHOLDER:([^}]+)\}\}")
MAX_RETRIES = 1


def scan_sentinels(content_or_path: Union[str, Path]) -> list[str]:
    """Return list of sentinel names found in content or file.

    Accepts either a string of content or a Path to a file.
    Returns just the sentinel name (not the full {{...}} wrapper).
    Returns [] if path doesn't exist.
    """
    if isinstance(content_or_path, Path):
        if not content_or_path.exists():
            return []
        text = content_or_path.read_text(encoding="utf-8", errors="replace")
    else:
        text = content_or_path
    return SENTINEL_PATTERN.findall(text)


def run_synthesize_spec(
    config: PortifyConfig,
    template_path: Optional[Path] = None,
) -> PortifyStepResult:
    """Execute Step 5: synthesize-spec.

    Requires portify-analysis.md and optionally a template file.
    Produces synthesized-spec.md with zero sentinels (SC-005).
    """
    start = time.monotonic()
    results_dir = (
        config.output_dir / "results" if config.output_dir else Path("results")
    )
    results_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = results_dir / ARTIFACT_NAME
    error_path = results_dir / f"{STEP_NAME}-error.log"

    # Template handling: if not explicitly provided, look in workflow dir
    if template_path is None:
        workflow_dir = config.workflow_path if config.workflow_path else Path(".")
        candidate = Path(workflow_dir) / "release-spec-template.md"
        # If no template anywhere, fail with MISSING_ARTIFACT
        if not candidate.exists():
            return PortifyStepResult(
                step_name=STEP_NAME,
                step_number=STEP_NUMBER,
                phase=PHASE,
                portify_status=PortifyStatus.FAIL,
                failure_classification=FailureClassification.MISSING_ARTIFACT,
                gate_tier=GATE_TIER,
                error_message=f"Missing template: {candidate}",
                duration_seconds=time.monotonic() - start,
            )
        template_path = candidate
    # If template_path is explicitly provided, trust the caller (allows mocking)

    # Check prerequisites
    prereq = results_dir / "portify-analysis.md"
    if not prereq.exists():
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.MISSING_ARTIFACT,
            gate_tier=GATE_TIER,
            error_message="Missing prerequisite: portify-analysis.md",
            duration_seconds=time.monotonic() - start,
        )

    # Run Claude subprocess
    work_dir = config.workdir_path or results_dir
    workflow_path = config.workflow_path or Path(".")

    process = PortifyProcess(
        prompt=_build_prompt(config, results_dir, template_path),
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

    # Read output content
    if result.output_file and result.output_file.exists():
        content = result.output_file.read_text(encoding="utf-8", errors="replace")
    elif artifact_path.exists():
        content = artifact_path.read_text(encoding="utf-8", errors="replace")
    else:
        content = result.stdout_text

    # Scan for sentinels (SC-005)
    sentinels = scan_sentinels(content)
    if sentinels:
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.PARTIAL_ARTIFACT,
            gate_tier=GATE_TIER,
            artifact_path=str(artifact_path),
            error_message=f"Unresolved sentinels: {sentinels}",
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


def _build_prompt(
    config: PortifyConfig,
    results_dir: Path,
    template_path: Optional[Path] = None,
) -> str:
    template_str = f" Template: {template_path}." if template_path else ""
    return (
        f"Synthesize a portify spec for the workflow at {config.workflow_path}. "
        f"Results directory: {results_dir}.{template_str} "
        "Produce synthesized-spec.md with all {{SC_PLACEHOLDER:*}} sentinels resolved."
    )
