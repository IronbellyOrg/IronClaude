"""Roadmap data models -- RoadmapConfig and AgentSpec.

RoadmapConfig extends PipelineConfig with roadmap-specific fields.
AgentSpec represents a model:persona pair for generate steps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from superclaude.cli.pipeline.models import PipelineConfig

VALID_FINDING_STATUSES = frozenset({"PENDING", "ACTIVE", "FIXED", "FAILED", "SKIPPED"})
VALID_DEVIATION_CLASSES = frozenset(
    {"SLIP", "INTENTIONAL", "AMBIGUOUS", "PRE_APPROVED", "UNCLASSIFIED"}
)


@dataclass
class Finding:
    """A single validation finding extracted from a report.

    Fields align with spec §2.3.1. Status lifecycle defined in D-0003:
    PENDING/ACTIVE -> FIXED | FAILED | SKIPPED (all terminal).

    deviation_class classifies the deviation source (v2.26):
    SLIP, INTENTIONAL, AMBIGUOUS, PRE_APPROVED, or UNCLASSIFIED (default).
    """

    id: str
    severity: str
    dimension: str
    description: str
    location: str
    evidence: str
    fix_guidance: str
    files_affected: list[str] = field(default_factory=list)
    status: str = "PENDING"
    agreement_category: str = ""
    deviation_class: str = "UNCLASSIFIED"
    source_layer: str = "structural"
    # v3.05 extensions (FR-3, FR-6) — all defaulted for backward compatibility
    rule_id: str = ""
    spec_quote: str = ""
    roadmap_quote: str = ""
    stable_id: str = ""

    def __post_init__(self) -> None:
        if self.status not in VALID_FINDING_STATUSES:
            raise ValueError(
                f"Invalid Finding status {self.status!r}. "
                f"Must be one of: {', '.join(sorted(VALID_FINDING_STATUSES))}"
            )
        if self.deviation_class not in VALID_DEVIATION_CLASSES:
            raise ValueError(
                f"Invalid deviation_class {self.deviation_class!r}. "
                f"Must be one of: {', '.join(sorted(VALID_DEVIATION_CLASSES))}"
            )


@dataclass
class AgentSpec:
    """Represents a model:persona pair for a generate step.

    The model value is passed directly to ``claude -p --model``
    (no resolution -- claude CLI accepts opus/sonnet/haiku natively).
    """

    model: str
    persona: str

    @classmethod
    def parse(cls, spec: str) -> AgentSpec:
        """Parse a 'model:persona' or 'model' string into an AgentSpec.

        Examples:
            AgentSpec.parse("opus:architect") -> AgentSpec("opus", "architect")
            AgentSpec.parse("sonnet")          -> AgentSpec("sonnet", "architect")
        """
        if ":" in spec:
            model, persona = spec.split(":", 1)
            return cls(model=model.strip(), persona=persona.strip())
        return cls(model=spec.strip(), persona="architect")

    @property
    def id(self) -> str:
        """Short identifier for filenames, e.g. 'opus-architect'."""
        return f"{self.model}-{self.persona}"


@dataclass
class RoadmapConfig(PipelineConfig):
    """Configuration for the roadmap generation pipeline.

    Extends PipelineConfig with roadmap-specific fields:
    spec_file, agents, depth, output_dir, retrospective_file.
    """

    spec_file: Path = field(default_factory=lambda: Path("."))
    agents: list[AgentSpec] = field(
        default_factory=lambda: [
            AgentSpec("opus", "architect"),
            AgentSpec("sonnet", "architect"),
        ]
    )
    depth: Literal["quick", "standard", "deep"] = "standard"
    output_dir: Path = field(default_factory=lambda: Path("."))
    retrospective_file: Path | None = None
    convergence_enabled: bool = (
        True  # v3.05: deterministic fidelity convergence engine (default ON)
    )
    allow_regeneration: bool = (
        False  # FR-9: override diff-size guard for full regeneration
    )
    input_type: Literal["auto", "tdd", "spec", "prd"] = (
        "auto"  # auto=detect from content, tdd/spec/prd=force
    )
    tdd_file: Path | None = (
        None  # TDD integration: optional TDD file path for downstream enrichment
    )
    prd_file: Path | None = (
        None  # PRD integration: optional PRD file path for business context enrichment
    )
    compress_enabled: bool = True  # Compress spec, generated roadmaps, and merge output before LLM consumption
    tool_write_extract: bool = False  # R1.4 dual-write opt-in: when True, extract step emits structured JSON rendered to markdown via tool_writer. Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
    tool_write_extract_tdd: bool = False  # R1.4 Step 9.3 dual-write opt-in: when True, the TDD-input extract step emits structured JSON rendered to markdown via tool_writer. Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
    tool_write_generate: bool = False  # R1.4 Step 9.4 dual-write opt-in: when True, the generate step (PRIMARY phantom-ID source) emits structured JSON validated (schema + generation-time phantom-ID rejection) and rendered to markdown via tool_writer. Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
    tool_write_diff: bool = False  # R1.4 Step 9.5 dual-write opt-in: when True, the diff step (SIMPLE comparative analysis, no phantom-ID constraint) emits structured JSON validated against diff.schema.json and rendered to markdown via tool_writer (PLAIN render_step_tool_write). Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
    tool_write_debate: bool = False  # R1.4 Step 9.6 dual-write opt-in: when True, the debate step (PRESERVED adversarial-debate mechanism, no phantom-ID constraint) emits structured JSON validated against debate.schema.json and rendered to markdown via tool_writer (PLAIN render_step_tool_write). semantic_layer.py stays byte-untouched. Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
    tool_write_score: bool = False  # R1.4 Step 9.7 dual-write opt-in: when True, the score step (SIMPLE evaluation, no phantom-ID constraint) emits structured JSON validated against score.schema.json and rendered to markdown via tool_writer (PLAIN render_step_tool_write). CONTRACT #8: variant_scores are 0-100 evaluation points; convergence thresholds are sourced from superclaude.contracts.CONVERGENCE_THRESHOLDS, never hardcoded. Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
    tool_write_merge: bool = False  # R1.4 Step 9.8 dual-write opt-in: when True, the merge step (SECOND primary phantom-ID source, master:§Top-3 #3) emits structured JSON validated (schema + generation-time phantom-ID rejection, same as generate) against merge.schema.json and rendered to markdown via tool_writer (render_step_tool_write_with_id_check). Default False (incremental markdown-write path is production) until cutover per Vector A >=3 release cycles.
    tool_write_spec_fidelity: bool = False  # R1.4 Step 9.9 dual-write opt-in: when True, the spec-fidelity step (convergence-loop CORE, no phantom-ID constraint) emits structured JSON validated against spec_fidelity.schema.json and rendered to markdown via tool_writer (PLAIN render_step_tool_write). PRESERVE: when convergence_enabled the executor runs _run_convergence_spec_fidelity and never reaches this path (convergence.py/semantic_layer.py byte-untouched). Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
    tool_write_test_strategy: bool = False  # R1.4 Step 9.11 dual-write opt-in (SECONDARY step): when True, the test-strategy step (no phantom-ID constraint) emits structured JSON validated against test_strategy.schema.json and rendered to markdown via tool_writer (PLAIN render_step_tool_write). CONTRACT #8: interleave_ratio is a test:work milestone ratio, never a convergence threshold. Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
    tool_write_certify: bool = False  # R1.4 Step 9.11 dual-write opt-in (SECONDARY step): when True, the certify step (no phantom-ID constraint) emits structured JSON validated against certify.schema.json and rendered to markdown via tool_writer (PLAIN render_step_tool_write). R1.3 CodeAssertion (assert_step_reachable) on CERTIFY_GATE is unaffected -- tool-write only changes HOW the markdown is produced, not the dispatch wiring. Default False (deterministic generate_certification_report path is production) until cutover per Vector A >=3 release cycles.
    tool_write_remediate: bool = False  # R1.4 Step 9.11 surface-consistency opt-in (remediate prompt builder ONLY): build_remediation_prompt is a file-EDIT-instruction prompt that emits NO roadmap-ID-bearing artifact, so there is NO schema, template, registry entry, or executor render hook (PARITY-ONLY). When True it may append a structured-output hint; the LOAD-BEARING guarantee is that the default (False) prompt stays byte-identical to the pre-R1.4 prompt. remediate carries no roadmap_ids, so no §MVR §3 / Contract #3 phantom-ID subset check applies. Default False.


@dataclass
class ValidateConfig(PipelineConfig):
    """Configuration for the roadmap validation pipeline.

    Extends PipelineConfig with validation-specific fields:
    output_dir, agents. Inherits model, max_turns, debug from PipelineConfig.
    """

    output_dir: Path = field(default_factory=lambda: Path("."))
    agents: list[AgentSpec] = field(
        default_factory=lambda: [
            AgentSpec("opus", "architect"),
            AgentSpec("sonnet", "architect"),
        ]
    )
    tool_write_validate_reflect: bool = False  # R1.4 Step 9.11 dual-write opt-in (SECONDARY validate-subsystem step): when True, the validate reflect step emits structured JSON validated against reflect.schema.json and rendered to markdown via tool_writer (PLAIN render_step_tool_write). Wired in validate_run_step (the validate sub-executor's per-step hook). Default False (markdown path is production) until cutover per Vector A >=3 release cycles.
