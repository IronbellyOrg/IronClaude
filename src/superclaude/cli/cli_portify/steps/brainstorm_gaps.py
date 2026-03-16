"""Step 6: brainstorm-gaps — Claude-assisted gap analysis.

Produces brainstorm-gaps.md with gap findings using 3 personas
(architect, analyzer, backend).

Gate: STANDARD (SC-006: Section 12 content present).
Falls back to inline prompt if sc:brainstorm skill is unavailable.

This step is RESUMABLE.
"""

from __future__ import annotations

import logging
import re
import shutil
import time
from dataclasses import dataclass, field
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

STEP_NAME = "brainstorm-gaps"
STEP_NUMBER = 6
PHASE = 4
GATE_TIER = "STANDARD"
ARTIFACT_NAME = "brainstorm-gaps.md"


@dataclass
class GapFinding:
    """A single gap or risk finding from a brainstorm persona."""

    gap_id: str = ""
    description: str = ""
    severity: str = "MINOR"
    affected_section: str = ""
    persona: str = ""

    def to_row(self) -> str:
        """Render as a Markdown table row."""
        return f"| {self.gap_id} | {self.description} | {self.severity} | {self.affected_section} |"


def check_brainstorm_skill_available() -> bool:
    """Return True if the sc:brainstorm skill is installed.

    Checks for the brainstorm skill directory in ~/.claude/skills/.
    """
    import os
    skills_base = Path(os.path.expanduser("~/.claude/skills"))
    brainstorm_skill = skills_base / "sc-brainstorm"
    brainstorm_protocol = skills_base / "sc-brainstorm-protocol"
    return brainstorm_skill.is_dir() or brainstorm_protocol.is_dir()


def parse_findings(content: str) -> list[GapFinding]:
    """Parse structured gap findings from markdown table output.

    Accepts rows with 4 or 5 columns:
      | GAP-NNN | description | severity | section |
      | GAP-NNN | description | severity | section | persona |

    Severity can be any value (CRITICAL, MAJOR, MINOR, INFO, HIGH, MEDIUM, LOW).
    Skips separator rows (e.g., |---|---|).
    """
    findings = []
    # Match GAP-NNN rows with at least 4 pipe-separated columns
    pattern = re.compile(
        r"^\|\s*(GAP-\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*(?:\|\s*([^|]*?)\s*)?\|",
        re.MULTILINE,
    )
    for m in pattern.finditer(content):
        gap_id = m.group(1).strip()
        description = m.group(2).strip()
        severity = m.group(3).strip()
        section = m.group(4).strip()
        persona = (m.group(5) or "").strip()

        # Skip separator rows
        if re.match(r"^[-:]+$", gap_id) or not gap_id.startswith("GAP-"):
            continue

        findings.append(GapFinding(
            gap_id=gap_id,
            description=description,
            severity=severity,
            affected_section=section,
            persona=persona,
        ))
    return findings


def has_section_12_content(content: str) -> bool:
    """Return True if content contains substantive Section 12 content.

    Requires both a Section 12 heading AND actual content (findings table
    or descriptive text with at least one gap/risk item).
    """
    heading_match = re.search(
        r"(?:Section\s+12|##\s+12\b|##.*[Gg]ap|##.*[Rr]isk)", content
    )
    if not heading_match:
        return False
    # Must have actual content beyond the heading (at least one GAP entry or descriptive line)
    after_heading = content[heading_match.end():]
    return bool(
        re.search(r"GAP-\d+|CRITICAL|MAJOR|MINOR|INFO|gap|risk", after_heading, re.IGNORECASE)
    )


def run_brainstorm_gaps(config: PortifyConfig) -> PortifyStepResult:
    """Execute Step 6: brainstorm-gaps.

    Requires synthesized-spec.md from Step 5.
    Produces brainstorm-gaps.md with Section 12 content.
    """
    start = time.monotonic()
    results_dir = config.output_dir / "results" if config.output_dir else Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = results_dir / ARTIFACT_NAME
    error_path = results_dir / f"{STEP_NAME}-error.log"

    # Check prerequisites
    spec_path = results_dir / "synthesized-spec.md"
    if not spec_path.exists():
        return PortifyStepResult(
            step_name=STEP_NAME,
            step_number=STEP_NUMBER,
            phase=PHASE,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.MISSING_ARTIFACT,
            gate_tier=GATE_TIER,
            error_message="Missing prerequisite: synthesized-spec.md",
            duration_seconds=time.monotonic() - start,
        )

    # Run Claude subprocess
    work_dir = config.workdir_path or results_dir
    workflow_path = config.workflow_path or Path(".")

    process = PortifyProcess(
        prompt=_build_prompt(config, spec_path),
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


def _build_prompt(config: PortifyConfig, spec_path: Path) -> str:
    return (
        f"Brainstorm gaps and risks for the portify spec at {spec_path}. "
        "Use architect, analyzer, and backend personas. "
        "Produce brainstorm-gaps.md with Section 12 gap analysis."
    )
