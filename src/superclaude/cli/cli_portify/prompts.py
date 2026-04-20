"""Prompt builders for the CLI Portify pipeline.

Each builder constructs a structured prompt for a Claude subprocess invocation,
referencing prior-step artifacts via @path notation.

Prompt builders:
  - AnalyzeWorkflowPrompt     (analyze-workflow)
  - DesignPipelinePrompt      (design-pipeline)
  - SynthesizeSpecPrompt      (synthesize-spec)
  - BrainstormGapsPrompt      (brainstorm-gaps)
  - PanelReviewPrompt         (panel-review)

Phase 5 protocol-mapping pipeline builders:
  - build_protocol_mapping_prompt()    (FR-013, FR-014)
  - build_analysis_synthesis_prompt()  (FR-016, FR-017)

Phase 6 specification pipeline builders:
  - build_step_graph_design_prompt()      (FR-020)
  - build_models_gates_design_prompt()    (FR-021)
  - build_prompts_executor_design_prompt() (FR-022)
  - build_spec_assembly_prompt()          (FR-023)

Phase 7 release spec synthesis builders:
  - load_release_spec_template()           (R-048, AC-009)
  - create_working_copy()                  (R-048)
  - build_section_population_prompt()      (R-049, FR-027)
  - build_brainstorm_prompt()              (R-049, FR-027)
  - incorporate_findings()                 (R-049, FR-027)
  - build_release_spec_prompt()            (R-051, OQ-008)

Registry:
  PROMPT_BUILDERS — dict[str, type[BasePromptBuilder]]
  get_prompt_builder() — factory function
"""

from __future__ import annotations

import re as _re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from superclaude.cli.cli_portify.models import BrainstormFinding

# ---------------------------------------------------------------------------
# Phase 7 T07.04: Inline embed size limit (OQ-008 — --file is broken)
# ---------------------------------------------------------------------------

#: Maximum byte length for inline -p embedding (120 KiB).
_EMBED_SIZE_LIMIT: int = 120 * 1024


# ---------------------------------------------------------------------------
# PromptContext
# ---------------------------------------------------------------------------


@dataclass
class PromptContext:
    """Context passed to all prompt builders."""

    workflow_path: Path
    work_dir: Path
    cli_name: str
    source_skill: str
    iteration: int = 1
    max_convergence: int = 3
    component_count: int = 0
    pipeline_steps: int = 0
    prior_findings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# BasePromptBuilder
# ---------------------------------------------------------------------------


class BasePromptBuilder:
    """Base class for all CLI Portify prompt builders.

    Subclasses must implement:
    - step_name: str
    - _body() -> str  (main prompt body)
    - required_frontmatter() -> list[str]
    - output_contract() -> list[str]
    - input_artifacts() -> list[Path]
    """

    step_name: str = ""

    def __init__(self, ctx: PromptContext) -> None:
        self.ctx = ctx

    def input_artifacts(self) -> list[Path]:
        """Return list of prior-step artifact Paths referenced by this prompt."""
        return []

    def required_frontmatter(self) -> list[str]:
        """Return list of required YAML frontmatter field names."""
        return []

    def output_contract(self) -> list[str]:
        """Return list of output contract requirements."""
        return []

    def _body(self) -> str:
        """Return the main prompt body text."""
        return ""

    def build(self) -> str:
        """Build the full prompt string with @path references, output contract, and frontmatter."""
        parts: list[str] = []

        # @path references for prior artifacts
        for artifact in self.input_artifacts():
            parts.append(f"@{artifact.resolve()}")

        # Main body
        body = self._body()
        if body:
            parts.append(body)

        # Required Frontmatter section
        fm_fields = self.required_frontmatter()
        if fm_fields:
            fm_lines = ["", "## Required Frontmatter", "```yaml", "---"]
            for f in fm_fields:
                fm_lines.append(f"{f}: <value>")
            fm_lines += ["---", "```"]
            parts.append("\n".join(fm_lines))

        # Output Contract section
        oc_items = self.output_contract()
        if oc_items:
            oc_lines = ["", "## Output Contract"]
            for item in oc_items:
                oc_lines.append(f"- {item}")
            parts.append("\n".join(oc_lines))

        return "\n".join(parts)

    def build_retry(
        self,
        failure_reason: str,
        remaining_placeholders: Optional[list[str]] = None,
    ) -> str:
        """Build a retry prompt that includes the original prompt plus retry context."""
        base = self.build()
        retry_parts = [
            base,
            "",
            "## RETRY CONTEXT",
            f"Previous attempt failed: {failure_reason}",
        ]

        if remaining_placeholders:
            retry_parts.append("")
            retry_parts.append("The following placeholder sentinels MUST be resolved:")
            for ph in remaining_placeholders:
                retry_parts.append(f"  - {ph}")

        return "\n".join(retry_parts)


# ---------------------------------------------------------------------------
# AnalyzeWorkflowPrompt
# ---------------------------------------------------------------------------


class AnalyzeWorkflowPrompt(BasePromptBuilder):
    """Prompt builder for the analyze-workflow step."""

    step_name = "analyze-workflow"

    def input_artifacts(self) -> list[Path]:
        return [self.ctx.work_dir / "results" / "component-inventory.md"]

    def required_frontmatter(self) -> list[str]:
        return [
            "step",
            "source_skill",
            "cli_name",
            "component_count",
            "analysis_sections",
        ]

    def output_contract(self) -> list[str]:
        return [
            "Include EXIT_RECOMMENDATION: CONTINUE or EXIT_RECOMMENDATION: HALT at end of output",
            "Include all 5 required section headers (##)",
            "Include component inventory reference",
        ]

    def _body(self) -> str:
        return (
            f"Analyze the workflow for {self.ctx.cli_name} (source skill: {self.ctx.source_skill}).\n"
            f"Review the component inventory and produce a comprehensive workflow analysis.\n"
            f"Include sections: Source Components, Step Graph, Parallel Groups, Gates Summary, Data Flow, "
            f"Classifications, Complexity Assessment.\n"
        )


# ---------------------------------------------------------------------------
# DesignPipelinePrompt
# ---------------------------------------------------------------------------


class DesignPipelinePrompt(BasePromptBuilder):
    """Prompt builder for the design-pipeline step."""

    step_name = "design-pipeline"

    def input_artifacts(self) -> list[Path]:
        return [
            self.ctx.work_dir / "results" / "portify-analysis.md",
            self.ctx.work_dir / "results" / "component-inventory.md",
        ]

    def required_frontmatter(self) -> list[str]:
        return ["step", "source_skill", "cli_name", "pipeline_steps", "gate_count"]

    def output_contract(self) -> list[str]:
        return [
            "Include EXIT_RECOMMENDATION: CONTINUE or EXIT_RECOMMENDATION: HALT",
            "Define all pipeline steps with step IDs",
            "Define gate criteria for each step",
        ]

    def _body(self) -> str:
        return (
            f"Design a CLI pipeline for {self.ctx.cli_name}.\n"
            f"Based on the workflow analysis, define all pipeline steps, gates, and data flow.\n"
        )


# ---------------------------------------------------------------------------
# SynthesizeSpecPrompt
# ---------------------------------------------------------------------------


class SynthesizeSpecPrompt(BasePromptBuilder):
    """Prompt builder for the synthesize-spec step."""

    step_name = "synthesize-spec"

    def input_artifacts(self) -> list[Path]:
        return [
            self.ctx.work_dir / "results" / "portify-analysis.md",
            self.ctx.work_dir / "results" / "portify-spec.md",
        ]

    def required_frontmatter(self) -> list[str]:
        return [
            "step",
            "source_skill",
            "cli_name",
            "synthesis_version",
            "placeholder_count",
        ]

    def output_contract(self) -> list[str]:
        return [
            "Include EXIT_RECOMMENDATION: CONTINUE or EXIT_RECOMMENDATION: HALT",
            "Replace all {{SC_PLACEHOLDER:*}} sentinels with actual content",
            "All sections must be complete — no partial content",
        ]

    def _body(self) -> str:
        return (
            f"Synthesize the final specification for {self.ctx.cli_name}.\n"
            f"Merge the analysis and pipeline design into a complete, implementable spec.\n"
            f"Resolve all placeholder sentinels.\n"
        )


# ---------------------------------------------------------------------------
# BrainstormGapsPrompt
# ---------------------------------------------------------------------------


class BrainstormGapsPrompt(BasePromptBuilder):
    """Prompt builder for the brainstorm-gaps step."""

    step_name = "brainstorm-gaps"

    def input_artifacts(self) -> list[Path]:
        return [self.ctx.work_dir / "results" / "synthesized-spec.md"]

    def required_frontmatter(self) -> list[str]:
        return ["step", "source_skill", "cli_name"]

    def output_contract(self) -> list[str]:
        return [
            "Include EXIT_RECOMMENDATION: CONTINUE or EXIT_RECOMMENDATION: HALT",
            "Include Section 12: Brainstorm / Gaps Analysis",
            "List all identified gaps, risks, and missing scenarios",
        ]

    def _body(self) -> str:
        return (
            f"Review the synthesized specification for {self.ctx.cli_name}.\n"
            f"Identify gaps, edge cases, and missing scenarios.\n"
            f"Include a brainstorm section (Section 12) with all findings.\n"
        )


# ---------------------------------------------------------------------------
# PanelReviewPrompt
# ---------------------------------------------------------------------------


class PanelReviewPrompt(BasePromptBuilder):
    """Prompt builder for the panel-review step."""

    step_name = "panel-review"

    def input_artifacts(self) -> list[Path]:
        return [
            self.ctx.work_dir / "results" / "synthesized-spec.md",
            self.ctx.work_dir / "results" / "brainstorm-gaps.md",
        ]

    def required_frontmatter(self) -> list[str]:
        return ["step", "source_skill", "cli_name", "iteration", "convergence_state"]

    def output_contract(self) -> list[str]:
        return [
            "Include EXIT_RECOMMENDATION: CONTINUE or EXIT_RECOMMENDATION: HALT",
            "Include quality scores: clarity, completeness, testability, consistency, overall",
            "Mark all CRITICAL items as [INCORPORATED] or [DISMISSED]",
            "Set convergence_state to 'converged' or 'blocked' when complete",
        ]

    def _body(self) -> str:
        return (
            f"Conduct a panel review of the specification for {self.ctx.cli_name}.\n"
            f"Iteration {self.ctx.iteration} of {self.ctx.max_convergence}.\n"
            f"Review brainstorm gaps, assess quality, and determine convergence state.\n"
        )




# ---------------------------------------------------------------------------
# Phase 5: Protocol-mapping and Analysis-synthesis prompt builders (FR-013 to FR-017)
# ---------------------------------------------------------------------------


def build_protocol_mapping_prompt(
    config_cli_name: str,
    inventory: list,
    *,
    source_skill: str = "",
) -> str:
    """Build the protocol-mapping analysis prompt (FR-013, FR-014).

    Instructs Claude to:
    - Analyze the component inventory and map execution protocols
    - Produce a protocol-map.md with YAML frontmatter
    - Include EXIT_RECOMMENDATION: CONTINUE at end of output

    Args:
        config_cli_name: The CLI name being portified.
        inventory: List of ComponentEntry objects from the component inventory.
        source_skill: Optional source skill name for frontmatter.

    Returns:
        Prompt string instructing Claude to produce protocol-map.md.
    """
    component_lines: list[str] = []
    for comp in inventory:
        name = getattr(comp, "name", str(comp))
        comp_type = getattr(comp, "component_type", "unknown")
        line_count = getattr(comp, "line_count", 0)
        component_lines.append(f"  - {name} ({comp_type}, {line_count} lines)")

    inventory_text = (
        "\n".join(component_lines) if component_lines else "  (empty inventory)"
    )

    return (
        f"Analyze the following component inventory for CLI '{config_cli_name}' "
        f"and produce a protocol map.\n\n"
        f"## Component Inventory\n{inventory_text}\n\n"
        f"## Task\n"
        f"Map the execution protocol for each component:\n"
        f"1. Identify sequential vs parallel execution paths\n"
        f"2. Map data flow between components\n"
        f"3. Identify gate checkpoints\n"
        f"4. Define timeout budgets per step\n\n"
        f"## Output Requirements\n"
        f"Write your analysis to `protocol-map.md`. The file MUST begin with YAML frontmatter:\n"
        f"```yaml\n"
        f"---\n"
        f"step: protocol-mapping\n"
        f"cli_name: {config_cli_name}\n"
        f"source_skill: {source_skill}\n"
        f"component_count: {len(inventory)}\n"
        f"---\n"
        f"```\n\n"
        f"At the end of the file, include:\n"
        f"EXIT_RECOMMENDATION: CONTINUE\n"
    )


def build_analysis_synthesis_prompt(
    config_cli_name: str,
    inventory: list,
    protocol_map_content: str,
    *,
    source_skill: str = "",
) -> str:
    """Build the analysis-synthesis prompt (FR-016, FR-017).

    Instructs Claude to produce portify-analysis-report.md with all 7 required sections
    and EXIT_RECOMMENDATION marker.

    Required sections (SC-004, FR-016):
    1. Source Components
    2. Step Graph
    3. Parallel Groups
    4. Gates Summary
    5. Data Flow
    6. Classifications
    7. Recommendations

    Args:
        config_cli_name: The CLI name being portified.
        inventory: List of ComponentEntry objects.
        protocol_map_content: Content of the protocol-map.md artifact.
        source_skill: Optional source skill name.

    Returns:
        Prompt string instructing Claude to produce portify-analysis-report.md.
    """
    component_lines: list[str] = []
    for comp in inventory:
        name = getattr(comp, "name", str(comp))
        comp_type = getattr(comp, "component_type", "unknown")
        component_lines.append(f"  - {name} ({comp_type})")

    inventory_text = (
        "\n".join(component_lines) if component_lines else "  (empty inventory)"
    )

    return (
        f"Synthesize a comprehensive analysis report for CLI '{config_cli_name}'.\n\n"
        f"## Component Inventory\n{inventory_text}\n\n"
        f"## Protocol Map Reference\n"
        f"(Use the protocol map content below as input)\n\n"
        f"## Task\n"
        f"Produce `portify-analysis-report.md` with ALL 7 required sections:\n\n"
        f"### Required Sections (ALL must be present)\n"
        f"1. **Source Components** — List all components being portified\n"
        f"2. **Step Graph** — DAG of pipeline steps with dependencies\n"
        f"3. **Parallel Groups** — Groups of steps that can run in parallel\n"
        f"4. **Gates Summary** — Gate IDs, tiers, and criteria for each step\n"
        f"5. **Data Flow** — Data flow between steps and artifact outputs\n"
        f"6. **Classifications** — Component classifications and tier assignments\n"
        f"7. **Recommendations** — Implementation recommendations and risk mitigations\n\n"
        f"## Output Requirements\n"
        f"The file MUST begin with YAML frontmatter:\n"
        f"```yaml\n"
        f"---\n"
        f"step: analysis-synthesis\n"
        f"cli_name: {config_cli_name}\n"
        f"source_skill: {source_skill}\n"
        f"component_count: {len(inventory)}\n"
        f"---\n"
        f"```\n\n"
        f"At the end of the file, include:\n"
        f"EXIT_RECOMMENDATION: CONTINUE\n"
    )


# ---------------------------------------------------------------------------
# Phase 6: Specification pipeline prompt builders (FR-020 to FR-023)
# ---------------------------------------------------------------------------


def build_step_graph_design_prompt(
    config_cli_name: str,
    analysis_report_content: str,
) -> str:
    """Build the step-graph-design prompt (FR-020).

    Instructs Claude to design the step execution graph from the analysis report
    and produce step-graph-spec.md with EXIT_RECOMMENDATION marker (G-005).

    Args:
        config_cli_name: The CLI name being portified.
        analysis_report_content: Content of portify-analysis-report.md.

    Returns:
        Prompt string instructing Claude to produce step-graph-spec.md.
    """
    return (
        f"Design the step execution graph for CLI '{config_cli_name}'.\n\n"
        f"## Analysis Report Reference\n"
        f"(Use the analysis report content below as input)\n\n"
        f"## Task\n"
        f"Produce `step-graph-spec.md` specifying the complete step execution DAG:\n\n"
        f"1. Define all pipeline steps with step IDs and phase assignments\n"
        f"2. Define step dependencies and ordering constraints\n"
        f"3. Identify parallel execution groups where applicable\n"
        f"4. Specify timeout budgets per step (in seconds)\n"
        f"5. Map data inputs/outputs for each step\n\n"
        f"## Analysis Report\n"
        f"{analysis_report_content}\n\n"
        f"## Output Requirements\n"
        f"The file MUST begin with YAML frontmatter:\n"
        f"```yaml\n"
        f"---\n"
        f"step: step-graph-design\n"
        f"cli_name: {config_cli_name}\n"
        f"step_count: <number of steps defined>\n"
        f"---\n"
        f"```\n\n"
        f"At the end of the file, include:\n"
        f"EXIT_RECOMMENDATION: CONTINUE\n"
    )


def build_models_gates_design_prompt(
    config_cli_name: str,
    step_graph_content: str,
) -> str:
    """Build the models-gates-design prompt (FR-021).

    Instructs Claude to design the data model and gate logic for the generated CLI
    and produce models-gates-spec.md with return type pattern (G-006).

    Args:
        config_cli_name: The CLI name being portified.
        step_graph_content: Content of step-graph-spec.md.

    Returns:
        Prompt string instructing Claude to produce models-gates-spec.md.
    """
    return (
        f"Design the data models and gate logic for CLI '{config_cli_name}'.\n\n"
        f"## Step Graph Reference\n"
        f"(Use the step graph content below as input)\n\n"
        f"## Task\n"
        f"Produce `models-gates-spec.md` specifying:\n\n"
        f"1. **Data Models** — Define all dataclasses/models used in the pipeline\n"
        f"2. **Gate Functions** — Define gate functions with return type tuple[bool, str]\n"
        f"3. **Gate Tiers** — Assign STRICT/STANDARD/LIGHT/EXEMPT tier to each gate\n"
        f"4. **Gate Criteria** — Specify semantic checks for each gate\n"
        f"5. **Error Types** — Define error/exception types for gate failures\n\n"
        f"## Step Graph\n"
        f"{step_graph_content}\n\n"
        f"## Output Requirements\n"
        f"The file MUST begin with YAML frontmatter:\n"
        f"```yaml\n"
        f"---\n"
        f"step: models-gates-design\n"
        f"cli_name: {config_cli_name}\n"
        f"gate_count: <number of gates defined>\n"
        f"---\n"
        f"```\n\n"
        f"Gate functions MUST use return type annotation: tuple[bool, str]\n"
        f"Example: def gate_validate_config(artifact_path: Path) -> tuple[bool, str]:\n"
    )


def build_prompts_executor_design_prompt(
    config_cli_name: str,
    step_graph_content: str,
    models_gates_content: str,
) -> str:
    """Build the prompts-executor-design prompt (FR-022).

    Instructs Claude to design the prompt builders and executor for the generated CLI
    and produce prompts-executor-spec.md with EXIT_RECOMMENDATION marker (G-007).

    Args:
        config_cli_name: The CLI name being portified.
        step_graph_content: Content of step-graph-spec.md.
        models_gates_content: Content of models-gates-spec.md.

    Returns:
        Prompt string instructing Claude to produce prompts-executor-spec.md.
    """
    return (
        f"Design the prompt builders and executor for CLI '{config_cli_name}'.\n\n"
        f"## Step Graph Reference\n"
        f"{step_graph_content}\n\n"
        f"## Models and Gates Reference\n"
        f"{models_gates_content}\n\n"
        f"## Task\n"
        f"Produce `prompts-executor-spec.md` specifying:\n\n"
        f"1. **Prompt Builders** — One builder per Claude-assisted step with:\n"
        f"   - input_artifacts() listing prior-step artifact paths\n"
        f"   - required_frontmatter() listing required YAML fields\n"
        f"   - output_contract() listing EXIT_RECOMMENDATION and other requirements\n"
        f"   - _body() with the main prompt instruction\n"
        f"2. **Executor Functions** — execute_<step>() per step with:\n"
        f"   - process_runner parameter for testability\n"
        f"   - Gate application after execution\n"
        f"   - Retry logic on PASS_NO_SIGNAL\n"
        f"   - 600s timeout enforcement\n"
        f"3. **STEP_REGISTRY entries** — timeout_s, retry_limit, phase_type per step\n\n"
        f"## Output Requirements\n"
        f"The file MUST begin with YAML frontmatter:\n"
        f"```yaml\n"
        f"---\n"
        f"step: prompts-executor-design\n"
        f"cli_name: {config_cli_name}\n"
        f"builder_count: <number of prompt builders defined>\n"
        f"---\n"
        f"```\n\n"
        f"At the end of the file, include:\n"
        f"EXIT_RECOMMENDATION: CONTINUE\n"
    )


def build_spec_assembly_prompt(assembled_content: str) -> str:
    """Build the pipeline-spec-assembly synthesis prompt (FR-023).

    Instructs Claude to synthesize the pre-assembled content into a unified
    portify-spec.md with EXIT_RECOMMENDATION marker and consistent step_mapping (G-008).

    Args:
        assembled_content: Pre-assembled and deduplicated content from the 3 input specs.

    Returns:
        Prompt string instructing Claude to produce portify-spec.md.
    """
    return (
        f"Synthesize a unified CLI portify specification from the assembled sub-specs below.\n\n"
        f"## Pre-Assembled Input\n"
        f"{assembled_content}\n\n"
        f"## Task\n"
        f"Produce `portify-spec.md` — the authoritative unified specification by:\n\n"
        f"1. Merging all step definitions into a coherent step_mapping section\n"
        f"2. Resolving any conflicts between sub-specs (prefer more specific)\n"
        f"3. Ensuring step count declared in frontmatter matches actual step definitions\n"
        f"4. Removing all duplicate content\n"
        f"5. Producing a complete, implementation-ready specification\n\n"
        f"## Output Requirements\n"
        f"The file MUST begin with YAML frontmatter:\n"
        f"```yaml\n"
        f"---\n"
        f"step: pipeline-spec-assembly\n"
        f"pipeline_steps: <total number of pipeline steps>\n"
        f"---\n"
        f"```\n\n"
        f"Include a `## Step Mapping` section that lists all pipeline steps.\n"
        f"The count of steps listed under Step Mapping MUST equal pipeline_steps in frontmatter.\n\n"
        f"At the end of the file, include:\n"
        f"EXIT_RECOMMENDATION: CONTINUE\n"
    )


# ---------------------------------------------------------------------------
# Phase 7: Release spec synthesis prompt builders (R-048 to R-051)
# ---------------------------------------------------------------------------


def load_release_spec_template(project_root: Path) -> str:
    """Load the release spec template from the project (R-048, AC-009, D-007).

    Reads ``src/superclaude/examples/release-spec-template.md`` relative to
    *project_root* and returns its content as a string.

    Args:
        project_root: The root of the project (Path where pyproject.toml lives).

    Returns:
        Template content string.

    Raises:
        PortifyValidationError: With failure_type=INVALID_PATH if the template
                                file does not exist.
    """
    from superclaude.cli.cli_portify.models import INVALID_PATH, PortifyValidationError

    template_path = (
        project_root / "src" / "superclaude" / "examples" / "release-spec-template.md"
    )
    if not template_path.exists():
        raise PortifyValidationError(
            INVALID_PATH,
            f"Release spec template not found: {template_path}",
            str(template_path),
        )
    return template_path.read_text(encoding="utf-8")


def create_working_copy(template_content: str, workdir: Path) -> Path:
    """Write a working copy of the release spec template to workdir (R-048).

    Creates ``workdir/release-spec-working.md`` as a byte-identical copy of
    *template_content*.

    Args:
        template_content: Template content from load_release_spec_template().
        workdir: Working directory where the copy will be written.

    Returns:
        Path to the written working copy.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    working_copy_path = workdir / "release-spec-working.md"
    working_copy_path.write_text(template_content, encoding="utf-8")
    return working_copy_path


def build_section_population_prompt(
    working_copy: str,
    portify_spec: str,
    analysis_report: str,
) -> str:
    """Build the 13-section population prompt (R-049, FR-027, substep 3b).

    Instructs Claude to populate all 13 sections of the release spec working
    copy, replacing every ``{{SC_PLACEHOLDER:*}}`` sentinel with actual content
    derived from the portify spec and analysis report.

    Args:
        working_copy: Content of release-spec-working.md.
        portify_spec: Content of portify-spec.md.
        analysis_report: Content of portify-analysis-report.md.

    Returns:
        Prompt string instructing Claude to produce release-spec-draft.md.
    """
    return (
        "Populate the release spec working copy below by replacing every "
        "{{SC_PLACEHOLDER:*}} sentinel with accurate content.\n\n"
        "## Release Spec Working Copy\n"
        f"{working_copy}\n\n"
        "## Portify Specification (source material)\n"
        f"{portify_spec}\n\n"
        "## Analysis Report (source material)\n"
        f"{analysis_report}\n\n"
        "## Task\n"
        "1. Replace ALL {{SC_PLACEHOLDER:*}} sentinels with accurate values derived from the source materials above.\n"
        "2. Ensure all 13 sections are complete — no partial content.\n"
        "3. Write the populated draft to `release-spec-draft.md`.\n\n"
        "## Output Requirements\n"
        "- Zero {{SC_PLACEHOLDER:*}} sentinels must remain in the output.\n"
        "- All 13 sections must be present and populated.\n"
        "- At the end of the file, include:\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )


def build_brainstorm_prompt(draft_content: str, persona: str) -> str:
    """Build the brainstorm gap-analysis prompt for a single persona (R-049, FR-027, substep 3c).

    Instructs Claude to adopt the given *persona* and review the release spec
    draft for gaps, risks, and missing scenarios.  The output must contain one
    JSON object per finding with the required fields.

    Args:
        draft_content: Content of release-spec-draft.md.
        persona: One of 'architect', 'analyzer', or 'backend'.

    Returns:
        Prompt string instructing Claude to return structured BrainstormFinding JSON.
    """
    persona_descriptions = {
        "architect": (
            "systems architect focused on scalability, design consistency, "
            "and architectural completeness"
        ),
        "analyzer": (
            "deep-analysis specialist focused on edge cases, logical gaps, "
            "and requirement ambiguities"
        ),
        "backend": (
            "backend engineer focused on implementation feasibility, "
            "API contracts, and data-flow correctness"
        ),
    }
    persona_desc = persona_descriptions.get(
        persona, f"{persona} specialist reviewing for gaps and risks"
    )

    return (
        f"You are a {persona_desc}.\n\n"
        "Review the release spec draft below and identify gaps, risks, and missing scenarios.\n\n"
        "## Release Spec Draft\n"
        f"{draft_content}\n\n"
        "## Task\n"
        "Identify all gaps and risks you observe. For each finding, output a JSON object "
        "on its own line with exactly these fields:\n"
        '{"gap_id": "GAP-XXX", "description": "...", "severity": "CRITICAL|MAJOR|MINOR|INFO", '
        '"affected_section": "...", "persona": "' + persona + '"}\n\n'
        "## Severity Guidelines\n"
        "- CRITICAL: Will cause implementation failure or spec-level defect\n"
        "- MAJOR: Significant gap that needs addressing before implementation\n"
        "- MINOR: Small gap; acceptable to defer\n"
        "- INFO: Observation only; no action required\n\n"
        "Output findings as newline-delimited JSON objects. "
        "At the end of the findings, include:\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )


def incorporate_findings(draft: str, findings: "list[BrainstormFinding]") -> str:
    """Incorporate brainstorm findings into the draft (R-049, FR-027, substep 3d).

    Routing rules:
    - CRITICAL or MAJOR findings with `affected_section` → append note to body
    - Unresolvable (no `affected_section`) or INFO findings → route to Section 12

    This is a purely programmatic operation; it does not call Claude.

    Args:
        draft: Content of release-spec-draft.md.
        findings: List of BrainstormFinding objects from all 3 persona passes.

    Returns:
        Updated draft string with findings incorporated.
    """
    body_findings: list[str] = []
    section12_findings: list[str] = []

    for f in findings:
        if f.severity in ("CRITICAL", "MAJOR") and f.affected_section:
            body_findings.append(
                f"<!-- [{f.gap_id}] [{f.persona.upper()}] {f.severity}: {f.description} "
                f"(affects: {f.affected_section}) -->"
            )
        else:
            section12_findings.append(
                f"| {f.gap_id} | {f.persona} | {f.severity} | "
                f"{f.affected_section or 'N/A'} | {f.description} |"
            )

    result = draft

    # Append body findings before Section 12 or at end of body
    if body_findings:
        body_block = "\n".join(body_findings)
        # Insert before Section 12 if present, else append
        if _re.search(r"^##\s+12\b", result, _re.MULTILINE):
            result = _re.sub(
                r"(^##\s+12\b)",
                body_block + "\n\n\\1",
                result,
                flags=_re.MULTILINE,
                count=1,
            )
        else:
            result = result.rstrip() + "\n\n" + body_block + "\n"

    # Append Section 12 if there are section12 findings
    if section12_findings:
        table_header = "| Gap ID | Persona | Severity | Section | Description |\n|--------|---------|----------|---------|-------------|"
        table_body = "\n".join(section12_findings)
        section12_block = (
            "\n\n## 12. Brainstorm Gap Analysis\n\n"
            + table_header
            + "\n"
            + table_body
            + "\n"
        )
        # Merge into existing Section 12 or append
        if _re.search(r"^##\s+12\b", result, _re.MULTILINE):
            result = result.rstrip() + "\n\n" + table_header + "\n" + table_body + "\n"
        else:
            result = result.rstrip() + section12_block

    return result


def build_release_spec_prompt(template_content: str, cli_name: str = "") -> str:
    """Build the release spec synthesis prompt with inline embed guard (R-051, OQ-008).

    Guards against content >120 KiB. Transport is now stdin (see ClaudeProcess.start),
    so the kernel MAX_ARG_STRLEN ceiling no longer applies; this threshold survives as
    a product-level sanity check on oversized templates.

    Args:
        template_content: Release spec template content.
        cli_name: Optional CLI name for context in the prompt.

    Returns:
        Prompt string suitable for inline embedding.

    Raises:
        PortifyValidationError: With failure_type=CONTENT_TOO_LARGE if
                                ``len(template_content) > _EMBED_SIZE_LIMIT``.
    """
    from superclaude.cli.cli_portify.models import (
        CONTENT_TOO_LARGE,
        PortifyValidationError,
    )

    if len(template_content) > _EMBED_SIZE_LIMIT:
        raise PortifyValidationError(
            CONTENT_TOO_LARGE,
            f"Template size {len(template_content)} exceeds {_EMBED_SIZE_LIMIT} byte inline limit",
            f"size={len(template_content)}, limit={_EMBED_SIZE_LIMIT}",
        )

    cli_context = f" for CLI '{cli_name}'" if cli_name else ""
    return (
        f"Produce a release specification{cli_context} using the template below.\n\n"
        "## Release Spec Template\n"
        f"{template_content}\n\n"
        "## Task\n"
        "Populate all sections, replacing every {{SC_PLACEHOLDER:*}} sentinel "
        "with accurate content.\n\n"
        "At the end of the file, include:\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )


