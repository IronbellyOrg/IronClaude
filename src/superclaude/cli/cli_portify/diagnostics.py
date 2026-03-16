"""Failure diagnostics collection for CLI Portify pipeline (FR-042).

Implements:
- DiagnosticsBundle dataclass: structured failure context
- DiagnosticsCollector: collects gate failures, exit codes, missing artifacts
- emit_diagnostics(): writes workdir/diagnostics.md on pipeline failure
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from superclaude.cli.cli_portify.gates import GateFailure


# ---------------------------------------------------------------------------
# DiagnosticsBundle
# ---------------------------------------------------------------------------


@dataclass
class DiagnosticsBundle:
    """Structured failure context collected during a pipeline run.

    Attributes:
        step_id: The step identifier where failure occurred.
        gate_failures: List of structured GateFailure records.
        exit_code: Process exit code, or None if not applicable.
        missing_artifacts: List of artifact paths that were expected but not found.
        resume_guidance: Human-readable guidance for resuming the failed run.
    """

    step_id: str = ""
    gate_failures: list[GateFailure] = field(default_factory=list)
    exit_code: Optional[int] = None
    missing_artifacts: list[str] = field(default_factory=list)
    resume_guidance: str = ""


# ---------------------------------------------------------------------------
# DiagnosticsCollector
# ---------------------------------------------------------------------------


class DiagnosticsCollector:
    """Collects diagnostic information during pipeline execution.

    Usage::

        collector = DiagnosticsCollector()
        collector.record_gate_failure(failure)
        collector.record_exit_code(1)
        collector.record_missing_artifact("/path/to/artifact.md")
        collector.set_resume_guidance("superclaude portify --start panel-review")
        path = collector.emit_diagnostics(workdir, step_id="panel-review")
    """

    def __init__(self) -> None:
        self._gate_failures: list[GateFailure] = []
        self._exit_code: Optional[int] = None
        self._missing_artifacts: list[str] = []
        self._resume_guidance: str = ""

    def record_gate_failure(self, failure: GateFailure) -> None:
        """Record a structured gate failure."""
        self._gate_failures.append(failure)

    def record_exit_code(self, code: int) -> None:
        """Record the process exit code."""
        self._exit_code = code

    def record_missing_artifact(self, path: str) -> None:
        """Record a missing artifact path."""
        self._missing_artifacts.append(path)

    def set_resume_guidance(self, guidance: str) -> None:
        """Set resume guidance for the user."""
        self._resume_guidance = guidance

    def build_bundle(self, step_id: str = "") -> DiagnosticsBundle:
        """Construct a DiagnosticsBundle from collected state."""
        return DiagnosticsBundle(
            step_id=step_id,
            gate_failures=list(self._gate_failures),
            exit_code=self._exit_code,
            missing_artifacts=list(self._missing_artifacts),
            resume_guidance=self._resume_guidance,
        )

    def emit_diagnostics(self, workdir: Path, step_id: str = "") -> Path:
        """Write diagnostics.md to workdir and return the path.

        Args:
            workdir: Directory to write the diagnostics file to.
            step_id: Pipeline step where failure occurred.

        Returns:
            Path to the written diagnostics.md file.
        """
        bundle = self.build_bundle(step_id=step_id)
        content = _render_diagnostics_md(bundle)
        workdir.mkdir(parents=True, exist_ok=True)
        diag_path = workdir / "diagnostics.md"
        diag_path.write_text(content, encoding="utf-8")
        return diag_path


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _render_diagnostics_md(bundle: DiagnosticsBundle) -> str:
    """Render a DiagnosticsBundle to Markdown."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    lines: list[str] = [
        "# CLI Portify — Pipeline Failure Diagnostics",
        "",
        f"Generated: {now}",
        "",
    ]

    # Failed step
    if bundle.step_id:
        lines += [f"**Failed Step:** `{bundle.step_id}`", ""]

    # Exit code
    if bundle.exit_code is not None:
        lines += [f"**Exit Code:** {bundle.exit_code}", ""]

    # Gate failures
    if bundle.gate_failures:
        lines += ["## Gate Failures", ""]
        for gf in bundle.gate_failures:
            lines += [
                f"### {gf.gate_id} — {gf.check_name}",
                f"- **Tier:** {gf.tier}",
                f"- **Artifact:** `{gf.artifact_path}`",
                f"- **Reason:** {gf.diagnostic}",
                "",
            ]
    else:
        lines += ["## Gate Failures", "", "_None recorded._", ""]

    # Missing artifacts
    if bundle.missing_artifacts:
        lines += ["## Missing Artifacts", ""]
        for path in bundle.missing_artifacts:
            lines.append(f"- `{path}`")
        lines.append("")
    else:
        lines += ["## Missing Artifacts", "", "_None recorded._", ""]

    # Resume guidance
    lines += ["## Resume Guidance", ""]
    if bundle.resume_guidance:
        lines += [f"```", bundle.resume_guidance, "```", ""]
    else:
        lines += ["_No resume command available for this step._", ""]

    return "\n".join(lines)
