"""PRD pipeline logging -- dual-format JSONL + Markdown execution logs.

Dual logging for machine-readability (JSONL) and human-readability (Markdown).
All log files are append-only to support resume without overwriting.

NFR-PRD.1: Zero ``async def`` or ``await`` in this module.
NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
NFR-PRD.10: Dual JSONL + Markdown logging.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Status emoji mapping for Markdown logs
# ---------------------------------------------------------------------------

_STATUS_EMOJI: dict[str, str] = {
    "pass": "PASS",
    "pass_no_signal": "PASS (no signal)",
    "pass_no_report": "PASS (no report)",
    "halt": "HALT",
    "timeout": "TIMEOUT",
    "error": "ERROR",
    "skipped": "SKIP",
    "qa_fail": "QA FAIL",
    "qa_fail_exhausted": "QA FAIL (exhausted)",
    "validation_fail": "VALIDATION FAIL",
    "running": "RUNNING",
    "pending": "PENDING",
    "incomplete": "INCOMPLETE",
}


# ---------------------------------------------------------------------------
# PrdLogger
# ---------------------------------------------------------------------------


class PrdLogger:
    """Dual-format PRD pipeline logger: JSONL (machine) + Markdown (human).

    Both log files are append-only. Each step start/complete/gate event
    is written to both files simultaneously.
    """

    def __init__(self, task_dir: Path) -> None:
        self._task_dir = task_dir
        self._jsonl_path = task_dir / "execution-log.jsonl"
        self._md_path = task_dir / "execution-log.md"

        # Ensure task dir exists
        task_dir.mkdir(parents=True, exist_ok=True)

        # Write Markdown header if file doesn't exist yet
        if not self._md_path.exists():
            header = (
                "# PRD Pipeline Execution Log\n\n"
                f"**Started**: {datetime.now(timezone.utc).isoformat()}\n"
                f"**Task Dir**: {task_dir}\n\n"
                "| Step | Status | Duration | Details |\n"
                "|------|--------|----------|---------|\n"
            )
            self._md_path.write_text(header, encoding="utf-8")

    def log_step_start(self, step_id: str, step_name: str) -> None:
        """Log the start of a pipeline step.

        Args:
            step_id: Unique step identifier (e.g. "parse-request").
            step_name: Human-readable step name.
        """
        now = datetime.now(timezone.utc)

        # JSONL entry
        self._write_jsonl({
            "timestamp": now.isoformat(),
            "event_type": "step_start",
            "step_id": step_id,
            "step_name": step_name,
        })

        # Markdown entry (inline note)
        self._write_md(
            f"| {step_id} | RUNNING | - | Started: {step_name} |\n"
        )

    def log_step_complete(
        self,
        step_id: str,
        result: str,
        *,
        duration_seconds: float = 0.0,
        exit_code: int = 0,
        details: str = "",
    ) -> None:
        """Log the completion of a pipeline step.

        Args:
            step_id: Unique step identifier.
            result: Status string (e.g. "pass", "halt", "qa_fail").
            duration_seconds: Wall-clock duration of the step.
            exit_code: Subprocess exit code.
            details: Additional context string.
        """
        now = datetime.now(timezone.utc)

        # JSONL entry
        self._write_jsonl({
            "timestamp": now.isoformat(),
            "event_type": "step_complete",
            "step_id": step_id,
            "duration_seconds": round(duration_seconds, 2),
            "exit_code": exit_code,
            "result": result,
            "details": details,
        })

        # Markdown entry
        status_display = _STATUS_EMOJI.get(result, result.upper())
        duration_display = self._format_duration(duration_seconds)
        detail_text = details or f"exit={exit_code}"
        self._write_md(
            f"| {step_id} | {status_display} | {duration_display} "
            f"| {detail_text} |\n"
        )

    def log_gate_result(
        self,
        step_id: str,
        passed: bool,
        message: str,
    ) -> None:
        """Log a gate evaluation result.

        Args:
            step_id: Step the gate applies to.
            passed: Whether the gate passed.
            message: Description of gate result.
        """
        now = datetime.now(timezone.utc)

        # JSONL entry
        self._write_jsonl({
            "timestamp": now.isoformat(),
            "event_type": "gate_result",
            "step_id": step_id,
            "passed": passed,
            "message": message,
        })

        # Markdown entry
        gate_status = "GATE PASS" if passed else "GATE FAIL"
        self._write_md(
            f"| {step_id} | {gate_status} | - | {message} |\n"
        )

    # -------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------

    def _write_jsonl(self, data: dict) -> None:
        """Append a JSON line to the JSONL log file."""
        with open(self._jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, default=str) + "\n")

    def _write_md(self, line: str) -> None:
        """Append a line to the Markdown log file."""
        with open(self._md_path, "a", encoding="utf-8") as f:
            f.write(line)

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration as human-readable string."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m{secs:.0f}s"
