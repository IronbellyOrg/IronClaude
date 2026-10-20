"""Tasklist validation executor -- orchestrates tasklist fidelity checking.

Reads a roadmap file and tasklist directory, builds a validation step,
applies the TASKLIST_FIDELITY_GATE, and writes a fidelity report.

Reuses ``execute_pipeline()`` and ``ClaudeProcess`` from the pipeline module.
No new subprocess abstractions.

Context isolation: each subprocess receives only its prompt via inline embedding.
--file is a cloud download mechanism and does not inject local file content.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from superclaude.cli.pipeline.executor import execute_pipeline
from superclaude.cli.pipeline.models import PipelineConfig, Step, StepResult, StepStatus
from superclaude.cli.pipeline.process import ClaudeProcess
from superclaude.cli.pipeline.validation_text import embed_inputs as _embed_inputs
from superclaude.cli.pipeline.validation_text import sanitize_output

from .gates import TASKLIST_FIDELITY_GATE
from .models import TasklistValidateConfig
from .prompts import build_tasklist_fidelity_prompt

_log = logging.getLogger("superclaude.tasklist.executor")

# Token-context advisory threshold (soft warning, non-fatal).
# Prompts are delivered via stdin in ClaudeProcess.start, bypassing the Linux
# MAX_ARG_STRLEN ceiling. This threshold only surfaces prompts that may strain
# the model's context window.
_LARGE_PROMPT_WARN_BYTES = 500 * 1024  # 500 KB


def _collect_tasklist_files(tasklist_dir: Path) -> list[Path]:
    """Collect all markdown files in the tasklist directory.

    Returns sorted list of .md files for deterministic ordering.
    """
    if not tasklist_dir.is_dir():
        raise FileNotFoundError(f"Tasklist directory not found: {tasklist_dir}")
    files = sorted(tasklist_dir.glob("*.md"))
    if not files:
        raise FileNotFoundError(
            f"No markdown files found in tasklist directory: {tasklist_dir}"
        )
    return files


def _sanitize_output(output_file: Path) -> int:
    """Strip conversational preamble before YAML frontmatter."""
    return sanitize_output(output_file, logger=_log)


def tasklist_run_step(
    step: Step,
    config: PipelineConfig,
    cancel_check: Callable[[], bool],
) -> StepResult:
    """Execute a single tasklist validation step as a Claude subprocess.

    Mirrors ``validate_run_step`` from ``roadmap/validate_executor.py``.
    """
    started_at = datetime.now(timezone.utc)

    if config.dry_run:
        _log.info("[dry-run] Would execute step '%s'", step.id)
        return StepResult(
            step=step,
            status=StepStatus.PASS,
            attempt=1,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )

    # Prompt + inputs are composed inline and delivered via stdin downstream.
    embedded = _embed_inputs(step.inputs)
    if embedded:
        composed = step.prompt + "\n\n" + embedded
        if len(composed.encode("utf-8")) > _LARGE_PROMPT_WARN_BYTES:
            _log.warning(
                "tasklist executor: composed prompt is %d bytes (> %d);"
                " may strain model context window",
                len(composed.encode("utf-8")),
                _LARGE_PROMPT_WARN_BYTES,
            )
        effective_prompt = composed
        extra_args: list[str] = []
    else:
        effective_prompt = step.prompt
        extra_args = []

    proc = ClaudeProcess(
        prompt=effective_prompt,
        output_file=step.output_file,
        error_file=step.output_file.with_suffix(".err"),
        max_turns=config.max_turns,
        model=step.model or config.model,
        permission_flag=config.permission_flag,
        timeout_seconds=step.timeout_seconds,
        output_format="text",
        extra_args=extra_args,
    )

    proc.start()

    while proc._process is not None and proc._process.poll() is None:
        if cancel_check():
            proc.terminate()
            return StepResult(
                step=step,
                status=StepStatus.CANCELLED,
                attempt=1,
                gate_failure_reason="Cancelled by external signal",
                started_at=started_at,
                finished_at=datetime.now(timezone.utc),
            )
        time.sleep(1)

    exit_code = proc.wait()
    finished_at = datetime.now(timezone.utc)

    if exit_code == 124:
        return StepResult(
            step=step,
            status=StepStatus.TIMEOUT,
            attempt=1,
            gate_failure_reason=f"Step '{step.id}' timed out after {step.timeout_seconds}s",
            started_at=started_at,
            finished_at=finished_at,
        )

    if exit_code != 0:
        return StepResult(
            step=step,
            status=StepStatus.FAIL,
            attempt=1,
            gate_failure_reason=f"Step '{step.id}' exited with code {exit_code}",
            started_at=started_at,
            finished_at=finished_at,
        )

    _sanitize_output(step.output_file)

    return StepResult(
        step=step,
        status=StepStatus.PASS,
        attempt=1,
        started_at=started_at,
        finished_at=finished_at,
    )


def _build_steps(config: TasklistValidateConfig) -> list[Step]:
    """Build the tasklist validation pipeline steps."""
    tasklist_files = _collect_tasklist_files(config.tasklist_dir)
    all_inputs = [config.roadmap_file] + tasklist_files
    # TDD integration: include TDD file in validation inputs when provided
    if config.tdd_file is not None:
        all_inputs.append(config.tdd_file)
    # PRD integration: include PRD file in validation inputs when provided
    if config.prd_file is not None:
        all_inputs.append(config.prd_file)

    return [
        Step(
            id="tasklist-fidelity",
            prompt=build_tasklist_fidelity_prompt(
                config.roadmap_file,
                config.tasklist_dir,
                tdd_file=config.tdd_file,
                prd_file=config.prd_file,
            ),
            output_file=config.output_dir / "tasklist-fidelity.md",
            gate=TASKLIST_FIDELITY_GATE,
            timeout_seconds=600,
            inputs=all_inputs,
            retry_limit=1,
            model=config.model,
        ),
    ]


def _has_high_severity(report_path: Path) -> bool:
    """Check if the fidelity report has HIGH severity deviations.

    Returns True if high_severity_count > 0, used for CLI exit code.
    """
    if not report_path.exists():
        return True  # No report = assume failure

    content = report_path.read_text(encoding="utf-8")
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return True

    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return True

    for line in rest[:end_idx].splitlines():
        line = line.strip()
        if line.startswith("high_severity_count:"):
            value = line.split(":", 1)[1].strip()
            try:
                return int(value) > 0
            except (ValueError, TypeError):
                return True

    return True  # Field not found = assume failure


def execute_tasklist_validate(config: TasklistValidateConfig) -> bool:
    """Execute the tasklist validation pipeline.

    Returns True if validation passed (no HIGH severity deviations),
    False otherwise (used for CLI exit code).
    """
    steps = _build_steps(config)

    results = execute_pipeline(
        steps=steps,
        config=config,
        run_step=tasklist_run_step,
    )

    report_path = config.output_dir / "tasklist-fidelity.md"

    # Check for pipeline failures
    failures = [r for r in results if r.status in (StepStatus.FAIL, StepStatus.TIMEOUT)]
    if failures:
        _log.error(
            "Tasklist validation pipeline halted: %d step(s) failed",
            len(failures),
        )
        return False

    return not _has_high_severity(report_path)
