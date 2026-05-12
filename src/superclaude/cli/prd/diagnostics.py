"""PRD pipeline diagnostics -- failure classification, collection, and reporting.

Provides post-failure analysis by collecting step results, gate failures,
and fix cycle history into a structured diagnostic report. The failure
classifier assigns a category based on PrdStepStatus values.

NFR-PRD.1: Zero ``async def`` or ``await`` in this module.
NFR-PRD.6/GAP-007: Resume command generation with step-level and
    per-agent granularity.
NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .models import PrdConfig, PrdPipelineResult, PrdStepResult, PrdStepStatus


# ---------------------------------------------------------------------------
# Failure categories
# ---------------------------------------------------------------------------


class PrdFailureCategory(Enum):
    """Classification of PRD pipeline step failure root cause."""

    TIMEOUT = "timeout"
    QA_FAIL = "qa_fail"
    BUDGET_EXHAUSTED = "budget_exhausted"
    CRASH = "crash"
    GATE_FAIL = "gate_fail"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Diagnostic report
# ---------------------------------------------------------------------------


@dataclass
class PrdDiagnosticReport:
    """Structured diagnostic report for a PRD pipeline run."""

    config: PrdConfig
    total_steps: int = 0
    steps_passed: int = 0
    steps_failed: int = 0
    steps_skipped: int = 0
    failure_details: list[dict] = field(default_factory=list)
    gate_failures: list[dict] = field(default_factory=list)
    fix_cycle_history: list[dict] = field(default_factory=list)
    resume_command: str = ""
    overall_status: str = "success"


# ---------------------------------------------------------------------------
# DiagnosticCollector
# ---------------------------------------------------------------------------


class DiagnosticCollector:
    """Aggregates step results into a structured diagnostic report."""

    def __init__(self, config: PrdConfig) -> None:
        self._config = config
        self._step_results: list[PrdStepResult] = []
        self._gate_failures: list[dict] = []
        self._fix_cycle_history: list[dict] = []

    def record_step(self, result: PrdStepResult) -> None:
        """Record a step result for diagnostic analysis."""
        self._step_results.append(result)

    def record_gate_failure(
        self, step_id: str, reason: str, enforcement: str
    ) -> None:
        """Record a gate failure."""
        self._gate_failures.append({
            "step_id": step_id,
            "reason": reason,
            "enforcement": enforcement,
        })

    def record_fix_cycle(
        self,
        step_id: str,
        cycle_number: int,
        verdict: str,
        agent_id: str = "",
    ) -> None:
        """Record a fix cycle attempt."""
        self._fix_cycle_history.append({
            "step_id": step_id,
            "cycle_number": cycle_number,
            "verdict": verdict,
            "agent_id": agent_id,
        })

    def build_report(
        self, pipeline_result: PrdPipelineResult
    ) -> PrdDiagnosticReport:
        """Build the complete diagnostic report."""
        report = PrdDiagnosticReport(config=self._config)
        report.total_steps = len(self._step_results)
        report.steps_passed = sum(
            1 for r in self._step_results if r.status.is_success
        )
        report.steps_failed = sum(
            1 for r in self._step_results if r.status.is_failure
        )
        report.steps_skipped = sum(
            1
            for r in self._step_results
            if r.status == PrdStepStatus.SKIPPED
        )

        # Collect failure details
        report.failure_details = [
            {
                "step_id": getattr(r.step, "name", "") if r.step else "",
                "status": r.status.value,
                "exit_code": r.exit_code,
                "agent_type": r.agent_type,
                "fix_cycle": r.fix_cycle,
            }
            for r in self._step_results
            if r.status.is_failure
        ]

        report.gate_failures = list(self._gate_failures)
        report.fix_cycle_history = list(self._fix_cycle_history)
        report.resume_command = pipeline_result.resume_command()
        report.overall_status = pipeline_result.outcome

        return report


# ---------------------------------------------------------------------------
# FailureClassifier
# ---------------------------------------------------------------------------


class FailureClassifier:
    """Maps PrdStepStatus values to user-facing failure categories."""

    def classify(self, result: PrdStepResult) -> PrdFailureCategory:
        """Determine the failure category for a step result.

        Classification priority:
        1. TIMEOUT: Step timed out
        2. QA_FAIL: QA check returned FAIL
        3. BUDGET_EXHAUSTED: Fix cycles exhausted
        4. GATE_FAIL: Gate validation failed
        5. CRASH: Unexpected non-zero exit
        6. UNKNOWN: No clear evidence
        """
        status = result.status

        if status == PrdStepStatus.TIMEOUT:
            return PrdFailureCategory.TIMEOUT

        if status == PrdStepStatus.QA_FAIL:
            return PrdFailureCategory.QA_FAIL

        if status == PrdStepStatus.QA_FAIL_EXHAUSTED:
            return PrdFailureCategory.BUDGET_EXHAUSTED

        if status == PrdStepStatus.VALIDATION_FAIL:
            return PrdFailureCategory.GATE_FAIL

        if status == PrdStepStatus.ERROR:
            return PrdFailureCategory.CRASH

        if status == PrdStepStatus.HALT:
            # HALT could be gate failure or crash depending on context
            if result.gate_failure_reason:
                return PrdFailureCategory.GATE_FAIL
            return PrdFailureCategory.CRASH

        return PrdFailureCategory.UNKNOWN


# ---------------------------------------------------------------------------
# ReportGenerator
# ---------------------------------------------------------------------------


class ReportGenerator:
    """Generates human-readable diagnostic reports with resume commands."""

    def generate(self, report: PrdDiagnosticReport) -> str:
        """Produce a diagnostic summary as markdown."""
        lines = [
            "# PRD Pipeline Diagnostic Report",
            "",
            "## Summary",
            f"- **Status**: {report.overall_status}",
            f"- **Total Steps**: {report.total_steps}",
            f"- **Passed**: {report.steps_passed}",
            f"- **Failed**: {report.steps_failed}",
            f"- **Skipped**: {report.steps_skipped}",
        ]

        if report.failure_details:
            lines.append("")
            lines.append("## Failures")
            for detail in report.failure_details:
                step = detail.get("step_id", "unknown")
                status = detail.get("status", "unknown")
                exit_code = detail.get("exit_code", -1)
                agent = detail.get("agent_type", "")
                cycle = detail.get("fix_cycle", 0)
                lines.append(
                    f"- **{step}**: {status} (exit={exit_code}"
                    f"{f', agent={agent}' if agent else ''}"
                    f"{f', cycle={cycle}' if cycle else ''})"
                )

        if report.gate_failures:
            lines.append("")
            lines.append("## Gate Failures")
            for gf in report.gate_failures:
                lines.append(
                    f"- **{gf['step_id']}** [{gf['enforcement']}]: "
                    f"{gf['reason']}"
                )

        if report.fix_cycle_history:
            lines.append("")
            lines.append("## Fix Cycle History")
            for fc in report.fix_cycle_history:
                agent_info = f" (agent: {fc['agent_id']})" if fc.get("agent_id") else ""
                lines.append(
                    f"- **{fc['step_id']}** cycle {fc['cycle_number']}: "
                    f"{fc['verdict']}{agent_info}"
                )

        if report.resume_command:
            lines.append("")
            lines.append("## Resume")
            lines.append(f"```\n{report.resume_command}\n```")
            suggested_budget = report.config.max_turns
            lines.append(f"Suggested budget: {suggested_budget} turns")

        return "\n".join(lines)

    def generate_resume_command(
        self,
        pipeline_result: PrdPipelineResult,
        *,
        failed_agent_id: str = "",
    ) -> str:
        """Generate a CLI resume command for mid-run failures.

        NFR-PRD.6/GAP-007: Step-level and per-agent granularity.

        Args:
            pipeline_result: The pipeline result with halt info.
            failed_agent_id: If the failure occurred in a parallel group,
                the specific agent that failed (GAP-007).

        Returns:
            CLI command string for resuming the pipeline.
        """
        cmd = pipeline_result.resume_command()
        if not cmd:
            return ""

        # Add per-agent resume hint for parallel group failures
        if failed_agent_id:
            cmd += f" --agent {failed_agent_id}"

        # Add budget suggestion
        budget = pipeline_result.suggested_resume_budget
        cmd += f" --max-turns {budget}"

        return cmd
