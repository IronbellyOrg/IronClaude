"""Gate definitions for the CLI Portify pipeline (Steps 3-7).

Each gate is a GateCriteria instance combined with a gate function that
performs step-specific semantic checks beyond the base pipeline.gates logic.

Gate IDs (G-000 through G-011) map to pipeline steps:
  G-000 validate-config         EXEMPT  — config YAML valid
  G-001 discover-components     STANDARD — inventory ≥1 component with SKILL.md
  G-002 analyze-workflow-draft  STANDARD — EXIT_RECOMMENDATION present
  G-003 analyze-workflow        STRICT   — EXIT_RECOMMENDATION + analysis sections
  G-004 design-pipeline-draft   STANDARD — approval_status field present
  G-005 design-pipeline/step-graph-design  STRICT — EXIT_RECOMMENDATION present
  G-006 synthesize-spec-draft/models-gates-design  STANDARD — return type pattern check
  G-007 synthesize-spec/prompts-executor-design  STRICT — EXIT_RECOMMENDATION present
  G-008 brainstorm-gaps/pipeline-spec-assembly  STRICT — EXIT_RECOMMENDATION + step-count consistency
  G-009 panel-report            STANDARD — approval_status field present
  G-010 synthesize-spec (final) STRICT   — EXIT_RECOMMENDATION + zero placeholders + brainstorm section
  G-011 panel-review            STRICT   — quality_scores + criticals_addressed

For the 7-step portify workflow, gates are registered by step name.
Phase 6 specification pipeline gates: step-graph-design (G-005), models-gates-design (G-006),
prompts-executor-design (G-007), pipeline-spec-assembly (G-008).

NFR-004: All gate functions return tuple[bool, str].
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from superclaude.cli.pipeline.models import GateCriteria, GateMode, SemanticCheck


# ---------------------------------------------------------------------------
# GateFailure dataclass (T04.03, AC-004)
# ---------------------------------------------------------------------------


@dataclass
class GateFailure:
    """Structured representation of a gate failure.

    Attributes:
        gate_id: Gate identifier (e.g. 'G-003').
        check_name: Name of the failing semantic check.
        diagnostic: Human-readable diagnostic message.
        artifact_path: Path to the artifact that failed the gate.
        tier: Enforcement tier ('STRICT', 'STANDARD', 'LIGHT', 'EXEMPT').
    """

    gate_id: str
    check_name: str
    diagnostic: str
    artifact_path: str
    tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"


# ---------------------------------------------------------------------------
# Gate diagnostics formatting (T04.03)
# ---------------------------------------------------------------------------

# Remediation hints by check name
_REMEDIATION_HINTS: dict[str, str] = {
    "has_valid_yaml_config": "Add required fields (workflow_path, cli_name, output_dir) to the YAML config",
    "has_component_inventory": "Ensure the workflow directory contains at least one component with SKILL.md",
    "has_required_analysis_sections": "Add all 7 required sections: Source Components, Step Graph, Parallel Groups, Gates Summary, Data Flow, Classifications, Recommendations",
    "has_approval_status": "Add 'approval_status: pending|approved|rejected' to the artifact frontmatter",
    "has_exit_recommendation": "Add 'EXIT_RECOMMENDATION: CONTINUE' or 'EXIT_RECOMMENDATION: HALT' to the artifact",
    "has_zero_placeholders": "Replace all {{SC_PLACEHOLDER:*}} sentinels with actual content",
    "has_brainstorm_section": "Add Section 12 (Brainstorm / Gaps Analysis) to the artifact",
    "has_quality_scores": "Add quality score fields (clarity, completeness, testability, consistency, overall) to the artifact",
    "has_criticals_addressed": "Resolve all CRITICAL items by marking them [INCORPORATED] or [DISMISSED]",
    "has_return_type_pattern": "Ensure return type pattern tuple[bool, str] is present in the artifact",
    "has_step_count_consistency": "Reconcile declared step count with actual step definitions in the artifact",
    "section_count": "Add more section headers (##) to reach the minimum required count",
    "zero_placeholders": "Replace all {{SC_PLACEHOLDER:*}} sentinels with actual content",
    "convergence_terminal": "Set convergence_state to 'converged' or 'blocked' before passing this gate",
}

_DEFAULT_REMEDIATION = "Review the artifact against the gate specification and correct the identified issue"


def format_gate_failure(
    gate_id: str,
    check_name: str,
    diagnostic: str,
    artifact_path: str,
) -> str:
    """Format a gate failure into a human-readable multi-line string.

    Args:
        gate_id: Gate identifier (e.g. 'G-003').
        check_name: Name of the failing semantic check.
        diagnostic: Diagnostic message from the check.
        artifact_path: Path to the artifact that failed the gate.

    Returns:
        Multi-line string with gate_id, check_name, artifact_path, and remediation hint.
    """
    remediation = _REMEDIATION_HINTS.get(check_name, _DEFAULT_REMEDIATION)
    return (
        f"Gate {gate_id} FAILED: {check_name}\n"
        f"  Artifact: {artifact_path}\n"
        f"  Reason: {diagnostic}\n"
        f"  Fix: {remediation}"
    )


# ---------------------------------------------------------------------------
# Semantic check helper functions (FR-047, AC-004)
# All return tuple[bool, str] — (passed, diagnostic_message)
# ---------------------------------------------------------------------------


def has_valid_yaml_config(content: str) -> tuple[bool, str]:
    """Check that YAML frontmatter contains workflow_path, cli_name, output_dir."""
    required = {"workflow_path", "cli_name", "output_dir"}
    found: set[str] = set()
    in_frontmatter = False
    lines = content.splitlines()
    fence_count = 0
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            fence_count += 1
            if fence_count == 1:
                in_frontmatter = True
            elif fence_count == 2:
                break
            continue
        if in_frontmatter and ":" in stripped:
            key = stripped.split(":", 1)[0].strip()
            if key:
                found.add(key)
    missing = required - found
    if missing:
        return False, f"Missing required config fields: {sorted(missing)}"
    return True, ""


def has_component_inventory(content: str) -> tuple[bool, str]:
    """Check that inventory lists ≥1 component with SKILL.md reference."""
    # Check for at least one component entry
    has_components = bool(
        re.search(r"component_count:\s*[1-9]", content)
        or re.search(r"##\s+.*(Skill|Component|Inventory)", content, re.IGNORECASE)
        or re.search(r"SKILL\.md", content)
    )
    if not has_components:
        return False, "Inventory does not list any components with SKILL.md"
    return True, ""


def has_required_analysis_sections(content: str) -> tuple[bool, str]:
    """Check for all 7 required section headers in analysis output."""
    required_sections = [
        "Source Components",
        "Step Graph",
        "Parallel Groups",
        "Gates Summary",
        "Data Flow",
        "Classifications",
        "Recommendations",
    ]
    missing = []
    for section in required_sections:
        if not re.search(re.escape(section), content, re.IGNORECASE):
            missing.append(section)
    if missing:
        return False, f"Missing required analysis sections: {missing}"
    return True, ""


def has_approval_status(content: str) -> tuple[bool, str]:
    """Check that approval_status field is present (approved/rejected/pending)."""
    if re.search(r"approval_status\s*:", content):
        return True, ""
    return False, "Missing required field: approval_status"


def has_exit_recommendation(content: str) -> tuple[bool, str]:
    """Check that EXIT_RECOMMENDATION marker is present."""
    if "EXIT_RECOMMENDATION" in content:
        return True, ""
    return False, "Missing EXIT_RECOMMENDATION marker"


def has_zero_placeholders(content: str) -> tuple[bool, str]:
    """Check that no {{SC_PLACEHOLDER:*}} sentinels remain."""
    match = re.search(r"\{\{SC_PLACEHOLDER:[^}]*\}\}", content)
    if match:
        return False, f"Placeholder sentinel found: {match.group(0)}"
    return True, ""


def has_brainstorm_section(content: str) -> tuple[bool, str]:
    """Check that Section 12 (brainstorm / gaps) is present."""
    # Accept various heading patterns for brainstorm/gaps section
    patterns = [
        r"(?:^|\n)#{1,3}\s+(?:Section\s+12|Brainstorm|Gaps|Gap Analysis|Missing)",
    ]
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True, ""
    return False, "Missing brainstorm/gaps section (Section 12)"


def has_quality_scores(content: str) -> tuple[bool, str]:
    """Check for quality score fields: clarity, completeness, testability, consistency, overall."""
    required_scores = [
        "clarity",
        "completeness",
        "testability",
        "consistency",
        "overall",
    ]
    missing = []
    for score in required_scores:
        if not re.search(rf"\b{score}\b\s*:", content, re.IGNORECASE):
            missing.append(score)
    if missing:
        return False, f"Missing quality score fields: {missing}"
    return True, ""


def has_criticals_addressed(content: str) -> tuple[bool, str]:
    """Check that all CRITICAL items are marked [INCORPORATED] or [DISMISSED]."""
    # Find all CRITICAL markers
    critical_markers = re.findall(r"CRITICAL", content)
    if not critical_markers:
        return True, ""  # No criticals to address
    # Check that each CRITICAL has an adjacent [INCORPORATED] or [DISMISSED]
    unresolved = re.findall(
        r"CRITICAL(?!.*?\[(?:INCORPORATED|DISMISSED)\])",
        content,
        re.DOTALL,
    )
    if unresolved:
        return (
            False,
            f"Found {len(unresolved)} CRITICAL item(s) not marked [INCORPORATED] or [DISMISSED]",
        )
    return True, ""


def has_return_type_pattern(content: str) -> tuple[bool, str]:
    """Check for return type pattern (tuple[bool, str] or return type annotation)."""
    if re.search(
        r"tuple\[bool,\s*str\]|-> tuple|return.*bool.*str", content, re.IGNORECASE
    ):
        return True, ""
    return False, "Missing return type pattern (tuple[bool, str])"


def has_step_count_consistency(content: str) -> tuple[bool, str]:
    """Check that step_mapping count matches declared steps."""
    # Look for a declared step count and a step_mapping/step_definitions section
    count_match = re.search(
        r"(?:pipeline_steps|step_count|steps)\s*:\s*(\d+)", content, re.IGNORECASE
    )
    if not count_match:
        return True, ""  # Can't verify without declared count, pass
    declared = int(count_match.group(1))
    # Count actual step headings
    actual_steps = len(re.findall(r"###\s+Step\s+\d+:", content, re.IGNORECASE))
    if actual_steps == 0:
        return True, ""  # No step headings to count against
    if actual_steps != declared:
        return (
            False,
            f"Step count mismatch: declared {declared} but found {actual_steps} step definitions",
        )
    return True, ""


# ---------------------------------------------------------------------------
# Gate criteria constants (G-000 through G-011 as per spec)
# ---------------------------------------------------------------------------

# G-000: validate-config (EXEMPT)
VALIDATE_CONFIG_GATE = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=0,
    enforcement_tier="EXEMPT",
    semantic_checks=None,
)

# G-001: discover-components (STANDARD)
DISCOVER_COMPONENTS_GATE = GateCriteria(
    required_frontmatter_fields=["source_skill", "component_count"],
    min_lines=5,
    enforcement_tier="STANDARD",
    semantic_checks=None,
)

# G-002: (not mapped to named step — EXIT_RECOMMENDATION present, STANDARD)
# G-003: analyze-workflow (STRICT)
ANALYZE_WORKFLOW_GATE = GateCriteria(
    required_frontmatter_fields=[
        "step",
        "source_skill",
        "cli_name",
        "component_count",
        "analysis_sections",
    ],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="section_count",
            check_fn=lambda c: _check_min_sections(c, 5),
            failure_message="Analysis must contain at least 5 section headers (##)",
        ),
    ],
)

# G-004: (approval_status gate, STANDARD)
# G-005: design-pipeline (STRICT)
DESIGN_PIPELINE_GATE = GateCriteria(
    required_frontmatter_fields=[
        "step",
        "source_skill",
        "cli_name",
        "pipeline_steps",
        "gate_count",
    ],
    min_lines=30,
    enforcement_tier="STRICT",
    semantic_checks=None,
)

# G-006: (return type pattern, STANDARD)
# G-007: synthesize-spec (STRICT)
SYNTHESIZE_SPEC_GATE = GateCriteria(
    required_frontmatter_fields=[
        "step",
        "source_skill",
        "cli_name",
        "synthesis_version",
        "placeholder_count",
    ],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="zero_placeholders",
            check_fn=lambda c: "{{SC_PLACEHOLDER:" not in c,
            failure_message="Placeholder sentinels {{SC_PLACEHOLDER:*}} must be removed before passing gate",
        ),
    ],
)

# G-008: (EXIT_RECOMMENDATION + step-count consistency, STRICT)
# G-009: (approval_status, STANDARD)
# G-010: (EXIT_RECOMMENDATION + zero placeholders + brainstorm section, STRICT)
# G-011: panel-review (STRICT)
BRAINSTORM_GAPS_GATE = GateCriteria(
    required_frontmatter_fields=["step", "source_skill", "cli_name"],
    min_lines=10,
    enforcement_tier="STANDARD",
    semantic_checks=None,
)

PANEL_REVIEW_GATE = GateCriteria(
    required_frontmatter_fields=[
        "step",
        "source_skill",
        "cli_name",
        "iteration",
        "convergence_state",
    ],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="convergence_terminal",
            check_fn=lambda c: _check_convergence_terminal(c),
            failure_message="convergence_state must be 'converged' or 'blocked' (terminal states only)",
        ),
    ],
)


# ---------------------------------------------------------------------------
# Helper functions for semantic checks
# ---------------------------------------------------------------------------


def _check_min_sections(content: str, min_count: int) -> bool:
    """Return True if content has at least min_count ## section headers."""
    sections = re.findall(r"^#{2,3}\s+\S", content, re.MULTILINE)
    return len(sections) >= min_count


def _check_convergence_terminal(content: str) -> bool:
    """Return True if convergence_state is a terminal state (converged or blocked)."""
    match = re.search(r"convergence_state\s*:\s*(\w+)", content)
    if not match:
        return False
    state = match.group(1).lower()
    return state in ("converged", "blocked")


# ---------------------------------------------------------------------------
# Gate registry
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Phase 6: Specification pipeline gate criteria (G-005 through G-008)
# ---------------------------------------------------------------------------

# G-005: step-graph-design (STRICT) — EXIT_RECOMMENDATION present
STEP_GRAPH_DESIGN_GATE = GateCriteria(
    required_frontmatter_fields=["step", "cli_name", "step_count"],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=None,
)

# G-006: models-gates-design (STANDARD) — return type pattern check
MODELS_GATES_DESIGN_GATE = GateCriteria(
    required_frontmatter_fields=["step", "cli_name", "gate_count"],
    min_lines=10,
    enforcement_tier="STANDARD",
    semantic_checks=None,
)

# G-007: prompts-executor-design (STRICT) — EXIT_RECOMMENDATION present
PROMPTS_EXECUTOR_DESIGN_GATE = GateCriteria(
    required_frontmatter_fields=["step", "cli_name", "builder_count"],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=None,
)

# G-008: pipeline-spec-assembly (STRICT) — EXIT_RECOMMENDATION + step-count consistency
PIPELINE_SPEC_ASSEMBLY_GATE = GateCriteria(
    required_frontmatter_fields=["step", "pipeline_steps"],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=None,
)


GATE_REGISTRY: dict[str, GateCriteria] = {
    "validate-config": VALIDATE_CONFIG_GATE,
    "discover-components": DISCOVER_COMPONENTS_GATE,
    "analyze-workflow": ANALYZE_WORKFLOW_GATE,
    "design-pipeline": DESIGN_PIPELINE_GATE,
    "synthesize-spec": SYNTHESIZE_SPEC_GATE,
    "brainstorm-gaps": BRAINSTORM_GAPS_GATE,
    "panel-review": PANEL_REVIEW_GATE,
    # Phase 6 specification pipeline gates
    "step-graph-design": STEP_GRAPH_DESIGN_GATE,
    "models-gates-design": MODELS_GATES_DESIGN_GATE,
    "prompts-executor-design": PROMPTS_EXECUTOR_DESIGN_GATE,
    "pipeline-spec-assembly": PIPELINE_SPEC_ASSEMBLY_GATE,
}


def get_gate_criteria(step_name: str) -> GateCriteria:
    """Look up gate criteria by step name.

    Raises:
        KeyError: If step_name is not registered.
    """
    if step_name not in GATE_REGISTRY:
        raise KeyError(f"No gate criteria registered for step: '{step_name}'")
    return GATE_REGISTRY[step_name]


# ---------------------------------------------------------------------------
# Gate functions (return tuple[bool, str] per NFR-004)
# ---------------------------------------------------------------------------


def gate_analyze_workflow(artifact_path: Path) -> tuple[bool, str]:
    """Gate for analyze-workflow step (STRICT).

    Checks:
    - File exists
    - Minimum 5 section headers
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")
    section_count = len(re.findall(r"^#{2,3}\s+\S", content, re.MULTILINE))
    if section_count < 5:
        return False, f"Insufficient section_count: found {section_count}, need ≥5"
    return True, ""


def gate_design_pipeline(artifact_path: Path) -> tuple[bool, str]:
    """Gate for design-pipeline step (STRICT).

    Checks:
    - File exists
    - Required frontmatter fields present
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")

    required = {"step", "source_skill", "cli_name", "pipeline_steps", "gate_count"}
    found: set[str] = set()
    in_fm = False
    fence_count = 0
    for line in content.splitlines():
        if line.strip() == "---":
            fence_count += 1
            if fence_count == 1:
                in_fm = True
            elif fence_count == 2:
                break
            continue
        if in_fm and ":" in line:
            key = line.split(":", 1)[0].strip()
            if key:
                found.add(key)
    missing = required - found
    if missing:
        return False, f"Missing required frontmatter fields: {sorted(missing)}"
    return True, ""


def gate_synthesize_spec(artifact_path: Path) -> tuple[bool, str]:
    """Gate for synthesize-spec step (STRICT).

    Checks:
    - File exists
    - No placeholder sentinels
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")
    match = re.search(r"\{\{SC_PLACEHOLDER:[^}]*\}\}", content)
    if match:
        return False, f"Placeholder sentinel found: {match.group(0)}"
    return True, ""


def gate_brainstorm_gaps(artifact_path: Path) -> tuple[bool, str]:
    """Gate for brainstorm-gaps step (STANDARD).

    Checks:
    - File exists
    - Has YAML frontmatter
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")
    if not re.search(r"^---\s*$", content, re.MULTILINE):
        return False, "Missing YAML frontmatter"
    return True, ""


def gate_panel_review(artifact_path: Path) -> tuple[bool, str]:
    """Gate for panel-review step (STRICT).

    Checks:
    - File exists
    - convergence_state is a terminal state (converged or blocked)
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")
    match = re.search(r"convergence_state\s*:\s*(\w+)", content)
    if not match:
        return False, "Missing convergence_state field in frontmatter"
    state = match.group(1).lower()
    if state not in ("converged", "blocked"):
        return (
            False,
            f"Non-terminal convergence state '{state}' — must be 'converged' or 'blocked'",
        )
    return True, ""


# ---------------------------------------------------------------------------
# Phase 6 gate functions (G-005 through G-008)
# ---------------------------------------------------------------------------


def gate_step_graph_design(artifact_path: Path) -> tuple[bool, str]:
    """Gate G-005 for step-graph-design step (STRICT).

    Checks:
    - File exists
    - EXIT_RECOMMENDATION marker present
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")
    passed, diagnostic = has_exit_recommendation(content)
    if not passed:
        return False, diagnostic
    return True, ""


def gate_models_gates_design(artifact_path: Path) -> tuple[bool, str]:
    """Gate G-006 for models-gates-design step (STANDARD).

    Checks:
    - File exists
    - Return type pattern tuple[bool, str] present
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")
    passed, diagnostic = has_return_type_pattern(content)
    if not passed:
        return False, diagnostic
    return True, ""


def gate_prompts_executor_design(artifact_path: Path) -> tuple[bool, str]:
    """Gate G-007 for prompts-executor-design step (STRICT).

    Checks:
    - File exists
    - EXIT_RECOMMENDATION marker present
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")
    passed, diagnostic = has_exit_recommendation(content)
    if not passed:
        return False, diagnostic
    return True, ""


def gate_pipeline_spec_assembly(artifact_path: Path) -> tuple[bool, str]:
    """Gate G-008 for pipeline-spec-assembly step (STRICT).

    Checks:
    - File exists
    - EXIT_RECOMMENDATION marker present
    - step_mapping count consistent with declared steps (SC-005)
    """
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    content = artifact_path.read_text(encoding="utf-8")
    passed, diagnostic = has_exit_recommendation(content)
    if not passed:
        return False, diagnostic
    passed, diagnostic = has_step_count_consistency(content)
    if not passed:
        return False, diagnostic
    return True, ""
