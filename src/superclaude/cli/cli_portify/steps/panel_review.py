"""Panel review step (Step 7) for the CLI Portify pipeline.

Implements:
- run_panel_review(): orchestrate the full panel-review step
- parse_quality_scores(): extract 4-dimension scores from Claude output
- compute_overall_score(): mean of 4 quality dimensions
- check_downstream_readiness(): overall >= 7.0 gate (FR-034, SC-009)
- count_unaddressed_criticals(): count unresolved CRITICAL findings (FR-032)
- capture_section_hashes(): hash all ## sections for additive-only enforcement
- generate_panel_report(): write panel-report.md with YAML frontmatter (FR-035)
- User review gate delegated to canonical review.py
- DOWNSTREAM_READINESS_THRESHOLD: 7.0 constant
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from superclaude.cli.cli_portify.convergence import (
    ConvergenceEngine,
    ConvergenceResult,
    ConvergenceState,
    EscalationReason,
    IterationResult,
)
from superclaude.cli.cli_portify.models import (
    FailureClassification,
    PortifyConfig,
    PortifyStatus,
    PortifyStepResult,
)
from superclaude.cli.cli_portify.process import PortifyProcess
from superclaude.cli.cli_portify.review import review_gate
from superclaude.cli.cli_portify.utils import extract_sections, hash_section


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DOWNSTREAM_READINESS_THRESHOLD: float = 7.0

_QUALITY_DIMENSIONS: tuple[str, ...] = (
    "clarity",
    "completeness",
    "testability",
    "consistency",
)


# ---------------------------------------------------------------------------
# Quality scoring
# ---------------------------------------------------------------------------


def parse_quality_scores(content: str) -> dict[str, float]:
    """Extract quality scores from Claude output.

    Supports two formats:
      - Colon format:  ``clarity: 8.5``
      - Table format:  ``| clarity | 8.5 |``

    Returns:
        Dict of {dimension: score}. Empty dict if no scores found.
    """
    scores: dict[str, float] = {}

    # Colon format: "dimension: 8.5"
    colon_pattern = re.compile(
        r"^\s*(" + "|".join(_QUALITY_DIMENSIONS) + r")\s*:\s*(\d+(?:\.\d+)?)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    for m in colon_pattern.finditer(content):
        dim = m.group(1).lower()
        scores[dim] = float(m.group(2))

    # Table format: "| clarity | 8.5 |"
    if not scores:
        table_pattern = re.compile(
            r"\|\s*("
            + "|".join(_QUALITY_DIMENSIONS)
            + r")\s*\|\s*(\d+(?:\.\d+)?)\s*\|",
            re.IGNORECASE,
        )
        for m in table_pattern.finditer(content):
            dim = m.group(1).lower()
            scores[dim] = float(m.group(2))

    return scores


def compute_overall_score(scores: dict[str, float]) -> float:
    """Return the mean of the 4 quality dimensions (missing dimensions = 0)."""
    if not scores:
        return 0.0
    total = sum(scores.get(d, 0.0) for d in _QUALITY_DIMENSIONS)
    return total / 4.0


def check_downstream_readiness(overall: float) -> bool:
    """Return True if overall score meets the downstream readiness threshold (FR-034)."""
    return overall >= DOWNSTREAM_READINESS_THRESHOLD


# ---------------------------------------------------------------------------
# Critical counting
# ---------------------------------------------------------------------------


def count_unaddressed_criticals(content: str) -> int:
    """Count CRITICAL findings NOT marked [RESOLVED] or [INCORPORATED] or [DISMISSED].

    A CRITICAL is unaddressed when the line contains 'CRITICAL' but does NOT
    start with a resolved/dismissed marker.
    """
    count = 0
    for line in content.splitlines():
        stripped = line.strip()
        if "CRITICAL" not in stripped.upper():
            continue
        upper = stripped.upper()
        # Skip if any resolved marker appears anywhere before CRITICAL
        critical_pos = upper.find("CRITICAL")
        prefix = upper[:critical_pos]
        if (
            "[RESOLVED]" in prefix
            or "[INCORPORATED]" in prefix
            or "[DISMISSED]" in prefix
        ):
            continue
        count += 1
    return count


# ---------------------------------------------------------------------------
# Section hashing
# ---------------------------------------------------------------------------


def capture_section_hashes(content: str) -> dict[str, str]:
    """Capture hashes of all ## sections in content.

    Returns:
        Dict of {section_title: sha256_hex}.
    """
    sections = extract_sections(content)
    return {title: hash_section(body) for title, body in sections.items()}


# ---------------------------------------------------------------------------
# Panel report generation
# ---------------------------------------------------------------------------


def generate_panel_report(
    convergence_result: ConvergenceResult,
    quality_scores: dict[str, float],
    overall_score: float,
    downstream_ready: bool,
    output_path: Path,
) -> None:
    """Write panel-report.md with YAML frontmatter and human-readable sections.

    The frontmatter includes all machine-readable fields required by FR-035 and SC-010:
      terminal_state, iteration_count, overall, downstream_ready,
      individual quality dimensions, and escalation_reason (if escalated).

    Args:
        convergence_result: Final convergence engine result.
        quality_scores: Dict of dimension scores.
        overall_score: Pre-computed overall (mean of 4 dimensions).
        downstream_ready: Whether the overall threshold was met.
        output_path: Where to write panel-report.md.
    """
    terminal_state = convergence_result.state.value.lower()
    iteration_count = convergence_result.iterations_completed

    # --- YAML frontmatter ---
    fm_lines = [
        "---",
        f"terminal_state: {terminal_state}",
        f"iteration_count: {iteration_count}",
        f"overall: {overall_score}",
        f"downstream_ready: {'true' if downstream_ready else 'false'}",
    ]

    for dim in _QUALITY_DIMENSIONS:
        if dim in quality_scores:
            fm_lines.append(f"{dim}: {quality_scores[dim]}")

    if convergence_result.escalation_reason is not None:
        fm_lines.append(
            f"escalation_reason: {convergence_result.escalation_reason.value}"
        )

    fm_lines.append("---")
    fm_lines.append("")

    # --- Human-readable body ---
    body_lines: list[str] = []

    body_lines += [
        "## Convergence Summary",
        "",
        f"**Terminal State**: {terminal_state.upper()}",
        f"**Iterations Completed**: {iteration_count}",
    ]

    if convergence_result.escalation_reason is not None:
        body_lines.append(
            f"**Escalation Reason**: {convergence_result.escalation_reason.value}"
        )

    body_lines += ["", "## Quality Scores", ""]
    body_lines.append("| Dimension | Score |")
    body_lines.append("|-----------|-------|")
    for dim in _QUALITY_DIMENSIONS:
        score = quality_scores.get(dim, 0.0)
        body_lines.append(f"| {dim} | {score} |")
    body_lines.append(f"| **overall** | {overall_score} |")

    body_lines += [
        "",
        "## Downstream Readiness",
        "",
        f"**downstream_ready**: {'true' if downstream_ready else 'false'}",
        "",
        f"Threshold: {DOWNSTREAM_READINESS_THRESHOLD} — "
        + ("PASSED" if downstream_ready else "NOT MET"),
        "",
    ]

    content = "\n".join(fm_lines + body_lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# run_panel_review
# ---------------------------------------------------------------------------


def run_panel_review(config: PortifyConfig) -> PortifyStepResult:
    """Execute the full panel-review step (Step 7, Phase 4).

    Requires:
        - ``config.results_dir / "synthesized-spec.md"`` (prior step artifact)
        - ``config.results_dir / "brainstorm-gaps.md"``  (prior step artifact)

    Produces:
        - ``config.results_dir / "panel-reviewed-spec.md"``
        - ``config.results_dir / "panel-report.md"``

    Returns:
        PortifyStepResult with step_name="panel-review", step_number=7, phase=4,
        gate_tier="STRICT".
    """
    from superclaude.cli.cli_portify.executor import STEP_REGISTRY

    step_name = "panel-review"
    step_number = 7
    phase = 4
    gate_tier = "STRICT"

    results_dir = config.results_dir
    if results_dir is None:
        return PortifyStepResult(
            step_name=step_name,
            step_number=step_number,
            phase=phase,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.MISSING_ARTIFACT,
            gate_tier=gate_tier,
            error_message="No results_dir configured on PortifyConfig",
        )

    # --- Check required prior artifacts ---
    spec_path = results_dir / "synthesized-spec.md"
    gaps_path = results_dir / "brainstorm-gaps.md"

    if not spec_path.exists():
        return PortifyStepResult(
            step_name=step_name,
            step_number=step_number,
            phase=phase,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.MISSING_ARTIFACT,
            gate_tier=gate_tier,
            error_message=f"Required artifact missing: {spec_path}",
        )

    if not gaps_path.exists():
        return PortifyStepResult(
            step_name=step_name,
            step_number=step_number,
            phase=phase,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.MISSING_ARTIFACT,
            gate_tier=gate_tier,
            error_message=f"Required artifact missing: {gaps_path}",
        )

    # --- Build output paths ---
    results_dir.mkdir(parents=True, exist_ok=True)
    output_artifact = results_dir / "panel-reviewed-spec.md"
    error_file = results_dir / "panel-review.err"
    report_path = results_dir / "panel-report.md"

    # --- Determine timeout from registry ---
    timeout_s: int = STEP_REGISTRY.get(step_name, {}).get("timeout_s", 1200)

    # --- Build prompt ---
    spec_content = spec_path.read_text(encoding="utf-8")
    gaps_content = gaps_path.read_text(encoding="utf-8")
    prompt = _build_panel_review_prompt(spec_content, gaps_content)

    # --- Determine working dirs ---
    work_dir = config.workdir_path or results_dir
    workflow_path = config.workflow_path

    # --- Execute subprocess ---
    process = PortifyProcess(
        prompt=prompt,
        output_file=output_artifact,
        error_file=error_file,
        work_dir=work_dir,
        workflow_path=workflow_path,
        max_turns=config.max_turns,
        model=config.model,
        timeout_seconds=timeout_s,
    )
    proc_result = process.run()

    # --- Handle timeout ---
    if proc_result.timed_out or proc_result.exit_code == 124:
        return PortifyStepResult(
            step_name=step_name,
            step_number=step_number,
            phase=phase,
            portify_status=PortifyStatus.TIMEOUT,
            failure_classification=FailureClassification.TIMEOUT,
            gate_tier=gate_tier,
            error_message="panel-review step timed out",
            iteration_timeout=timeout_s,
        )

    # --- Parse output ---
    output_text = proc_result.stdout_text or ""
    quality_scores = parse_quality_scores(output_text)
    overall = compute_overall_score(quality_scores)
    unaddressed = count_unaddressed_criticals(output_text)

    # --- Run convergence engine (internal loop, not outer retry) ---
    engine = ConvergenceEngine(max_iterations=3)
    engine.submit(
        IterationResult(
            iteration=1,
            unaddressed_criticals=unaddressed,
            quality_scores=quality_scores,
        )
    )
    convergence_result = engine.result()

    # --- Determine downstream_ready ---
    downstream_ready = check_downstream_readiness(overall)

    # --- Emit panel-report.md on BOTH terminal paths ---
    generate_panel_report(
        convergence_result=convergence_result,
        quality_scores=quality_scores,
        overall_score=overall,
        downstream_ready=downstream_ready,
        output_path=report_path,
    )

    # --- User review gate — delegates to canonical review.py ---
    should_continue, decision = review_gate(
        step_name, str(output_artifact), skip_review=config.skip_review,
    )
    if not should_continue:
        return PortifyStepResult(
            step_name=step_name,
            step_number=step_number,
            phase=phase,
            portify_status=PortifyStatus.FAIL,
            failure_classification=FailureClassification.USER_REJECTION,
            gate_tier=gate_tier,
            artifact_path=str(output_artifact),
            error_message="User rejected panel review artifact",
            review_accepted=False,
        )

    # Write panel-review.md as canonical artifact name (alongside panel-reviewed-spec.md)
    panel_review_path = results_dir / "panel-review.md"
    if output_artifact.exists() and not panel_review_path.exists():
        import shutil as _shutil

        _shutil.copy2(str(output_artifact), str(panel_review_path))

    return PortifyStepResult(
        step_name=step_name,
        step_number=step_number,
        phase=phase,
        portify_status=PortifyStatus.PASS,
        gate_tier=gate_tier,
        artifact_path=str(output_artifact),
        iteration_timeout=timeout_s,
        review_accepted=True,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_panel_review_prompt(spec_content: str, gaps_content: str) -> str:
    """Build the panel-review prompt for Claude."""
    return f"""You are conducting a final quality review of a CLI pipeline specification.

## Synthesized Specification

{spec_content}

## Gap Analysis Findings

{gaps_content}

## Review Instructions

Review the specification against the gap analysis findings. For each finding:
1. Assess whether it has been addressed in the specification.
2. Rate the severity: CRITICAL (must fix), MAJOR (should fix), MINOR (nice to fix).
3. Either mark as [INCORPORATED] if addressed or provide the unaddressed concern.

After reviewing all findings, provide quality scores on a 1-10 scale:

## Quality Scores

clarity: <score>
completeness: <score>
testability: <score>
consistency: <score>

Provide a concise convergence assessment indicating whether zero CRITICAL issues remain.
"""
