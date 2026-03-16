"""Preflight executor for python-mode sprint phases.

Runs commands via subprocess.run(), produces evidence artifacts and phase
result files, and ensures compatibility with _determine_phase_status().
"""

from __future__ import annotations

import logging
import shlex
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from superclaude.cli.sprint.classifiers import run_classifier
from superclaude.cli.sprint.config import parse_tasklist
from superclaude.cli.sprint.executor import AggregatedPhaseReport
from superclaude.cli.sprint.models import (
    GateOutcome,
    PhaseResult,
    PhaseStatus,
    SprintConfig,
    TaskResult,
    TaskStatus,
)

logger = logging.getLogger(__name__)

_STDOUT_MAX = 10240  # 10 KB
_STDERR_MAX = 2048  # 2 KB


def _truncate(text: str, limit: int) -> str:
    """Truncate *text* to *limit* bytes (UTF-8), appending a marker if cut."""
    encoded = text.encode("utf-8")
    if len(encoded) <= limit:
        return text
    return (
        encoded[:limit].decode("utf-8", errors="replace")
        + f"\n[truncated at {limit} bytes]"
    )


def _write_evidence(
    task_id: str,
    command: str,
    exit_code: int,
    stdout: str,
    stderr: str,
    duration: float,
    classification: str,
    artifacts_dir: Path,
) -> None:
    """Write per-task evidence artifact to ``artifacts_dir/<task_id>/evidence.md``."""
    evidence_dir = artifacts_dir / task_id
    evidence_dir.mkdir(parents=True, exist_ok=True)

    stdout_out = _truncate(stdout, _STDOUT_MAX)
    stderr_out = _truncate(stderr, _STDERR_MAX)

    content = (
        f"# Evidence: {task_id}\n\n"
        f"## Command\n\n```\n{command}\n```\n\n"
        f"## Result\n\n"
        f"- **Exit code:** {exit_code}\n"
        f"- **Duration:** {duration:.3f}s\n"
        f"- **Classification:** {classification}\n\n"
        f"## stdout\n\n```\n{stdout_out}\n```\n\n"
        f"## stderr\n\n```\n{stderr_out}\n```\n"
    )

    (evidence_dir / "evidence.md").write_text(content, encoding="utf-8")


def _inject_source_field(markdown: str) -> str:
    """Inject ``source: preflight`` into the YAML frontmatter block."""
    lines = markdown.split("\n")
    # Find the first closing --- of the frontmatter
    if not lines or lines[0] != "---":
        # No frontmatter — prepend a minimal one
        return "---\nsource: preflight\n---\n\n" + markdown
    for i in range(1, len(lines)):
        if lines[i] == "---":
            lines.insert(i, "source: preflight")
            break
    return "\n".join(lines)


def execute_preflight_phases(config: SprintConfig) -> list[PhaseResult]:
    """Execute all python-mode phases in *config* via subprocess.

    Filters ``config.active_phases`` to those with ``execution_mode == "python"``,
    runs each task's command, captures output, applies classifiers, writes evidence
    artifacts and result files, then returns a ``PhaseResult`` per phase.

    Args:
        config: Sprint configuration with phases and paths.

    Returns:
        List of ``PhaseResult`` objects, one per python-mode phase.
    """
    artifacts_dir = config.results_dir / "preflight-artifacts"
    phase_results: list[PhaseResult] = []

    python_phases = [p for p in config.active_phases if p.execution_mode == "python"]

    for phase in python_phases:
        phase_started = datetime.now(timezone.utc)
        logger.info(
            "Preflight: executing phase %d (%s)", phase.number, phase.display_name
        )

        # Parse task list from the phase file
        phase_content = phase.file.read_text(encoding="utf-8")
        tasks = parse_tasklist(phase_content, execution_mode="python")

        task_results: list[TaskResult] = []
        all_passed = True

        for task in tasks:
            task_started = datetime.now(timezone.utc)
            wall_start = time.monotonic()

            cmd = shlex.split(task.command)
            classification = "pass"
            stdout_text = ""
            stderr_text = ""
            exit_code = 0

            try:
                proc = subprocess.run(
                    cmd,
                    shell=False,
                    capture_output=True,
                    timeout=120,
                    cwd=config.work_dir,
                )
                stdout_text = proc.stdout.decode("utf-8", errors="replace")
                stderr_text = proc.stderr.decode("utf-8", errors="replace")
                exit_code = proc.returncode

                if task.classifier:
                    try:
                        classification = run_classifier(
                            task.classifier, exit_code, stdout_text, stderr_text
                        )
                    except KeyError:
                        logger.warning(
                            "Unknown classifier %r for task %s — using exit-code fallback",
                            task.classifier,
                            task.task_id,
                        )
                        classification = "pass" if exit_code == 0 else "fail"
                else:
                    classification = "pass" if exit_code == 0 else "fail"

            except subprocess.TimeoutExpired:
                exit_code = -1
                classification = "timeout"
                logger.warning("Task %s timed out after 120s", task.task_id)

            duration = time.monotonic() - wall_start
            task_finished = datetime.now(timezone.utc)

            _write_evidence(
                task_id=task.task_id,
                command=task.command,
                exit_code=exit_code,
                stdout=stdout_text,
                stderr=stderr_text,
                duration=duration,
                classification=classification,
                artifacts_dir=artifacts_dir,
            )

            task_status = (
                TaskStatus.PASS if classification == "pass" else TaskStatus.FAIL
            )
            gate_outcome = (
                GateOutcome.PASS if classification == "pass" else GateOutcome.FAIL
            )
            if classification == "timeout":
                task_status = TaskStatus.FAIL
                gate_outcome = GateOutcome.FAIL

            if task_status != TaskStatus.PASS:
                all_passed = False

            task_results.append(
                TaskResult(
                    task=task,
                    status=task_status,
                    turns_consumed=0,
                    exit_code=exit_code,
                    started_at=task_started,
                    finished_at=task_finished,
                    output_bytes=len(stdout_text.encode("utf-8")),
                    gate_outcome=gate_outcome,
                )
            )

        # Build aggregated report
        tasks_passed = sum(1 for tr in task_results if tr.status == TaskStatus.PASS)
        tasks_failed = sum(1 for tr in task_results if tr.status == TaskStatus.FAIL)
        total_duration = sum(tr.duration_seconds for tr in task_results)

        report = AggregatedPhaseReport(
            phase_number=phase.number,
            tasks_total=len(task_results),
            tasks_passed=tasks_passed,
            tasks_failed=tasks_failed,
            task_results=task_results,
            total_duration_seconds=total_duration,
        )

        # Write result file with source: preflight injected into frontmatter
        result_md = _inject_source_field(report.to_markdown())
        result_path = config.result_file(phase)
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(result_md, encoding="utf-8")

        phase_status = PhaseStatus.PREFLIGHT_PASS if all_passed else PhaseStatus.HALT
        phase_finished = datetime.now(timezone.utc)

        phase_results.append(
            PhaseResult(
                phase=phase,
                status=phase_status,
                exit_code=0 if all_passed else 1,
                started_at=phase_started,
                finished_at=phase_finished,
                output_bytes=sum(tr.output_bytes for tr in task_results),
            )
        )

        logger.info(
            "Preflight: phase %d done — %d/%d tasks passed, status=%s",
            phase.number,
            tasks_passed,
            len(task_results),
            phase_status.value,
        )

    return phase_results
