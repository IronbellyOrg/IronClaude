"""Roadmap prompt builders -- pure functions returning prompt strings.

All functions are pure: they accept concrete values, return ``str``,
and perform no I/O, subprocess calls, or side effects (NFR-004).

The returned string is passed to ``claude -p "<prompt>"``. The executor
separately appends ``--file <path>`` for each entry in ``step.inputs``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from .models import AgentSpec

_DEPTH_INSTRUCTIONS = {
    "quick": (
        "Conduct a single focused debate round. Each perspective states its "
        "position on the key divergence points, then provide a convergence assessment."
    ),
    "standard": (
        "Conduct two debate rounds:\n"
        "  Round 1: Each perspective states initial positions on divergence points.\n"
        "  Round 2: Each perspective rebuts the other's key claims.\n"
        "Then provide a convergence assessment."
    ),
    "deep": (
        "Conduct three debate rounds:\n"
        "  Round 1: Each perspective states initial positions on divergence points.\n"
        "  Round 2: Each perspective rebuts the other's key claims.\n"
        "  Round 3: Final synthesis -- each perspective identifies concessions and "
        "remaining disagreements.\n"
        "Then provide a convergence assessment."
    ),
}

_INTEGRATION_ENUMERATION_BLOCK = (
    "\n\n## Integration Points\n\n"
    "IMPORTANT: For each component that uses dispatch tables, registries, "
    "dependency injection, callback wiring, middleware chains, event bindings, "
    "or strategy patterns, enumerate in a table:\n"
    "| Artifact | Type | Wired | Milestone | Consumed By |\n"
    "|---|---|---|---|---|\n"
    "Do NOT assume that standard skeleton→implement sequencing covers custom "
    "dispatch/wiring mechanisms. Each mechanism requires an explicit wiring deliverable.\n"
)

_INTEGRATION_WIRING_DIMENSION = (
    "6. **Integration Wiring Completeness**: For each dispatch table, registry, "
    "DI injection point, callback binding, middleware chain, or strategy pattern "
    "in the specification, verify the roadmap contains an explicit task to:\n"
    "   - Create/populate the mechanism\n"
    "   - Wire concrete implementations into it\n"
    "   - Test the wiring end-to-end\n"
    "   Flag as HIGH severity if a mechanism exists in the spec but has no "
    "corresponding wiring task in the roadmap.\n"
)

_OUTPUT_FORMAT_BLOCK = (
    "\n\n<output_format>\n"
    "CRITICAL: Your response MUST begin with YAML frontmatter (--- delimited block).\n"
    "Do NOT include any text, preamble, or commentary before the opening ---.\n"
    'Do NOT say "Here is...", "Sure!", or any conversational text before the frontmatter.\n'
    "\n"
    "Correct start:\n"
    "---\n"
    "key: value\n"
    "---\n"
    "\n"
    "Incorrect start:\n"
    "Here is the output:\n"
    "---\n"
    "key: value\n"
    "---\n"
    "\n"
    "FORMATTING: Minimize output size without losing data.\n"
    "- Use single blank lines between sections (never double).\n"
    "- No horizontal rules (---) between milestones.\n"
    "- No trailing milestone summary lines (e.g. 'M1 total: 28 rows').\n"
    "- Use minimal table separator rows: |---|---|---|...|\n"
    "- Per-milestone metadata on one line: **M{N}: Title** | duration | exit criteria\n"
    "</output_format>"
)

_TEMPLATE_STRUCTURE_DIRECTIVE = (
    "\n\nThe roadmap template file defines the complete output skeleton \u2014 section order, "
    "table schemas, heading hierarchy, and YAML frontmatter fields. Follow it exactly.\n\n"
    "Key constraints reinforced here:\n"
    "- Every milestone section uses heading format `## M{N}: Title`\n"
    "- Every milestone MUST contain a 9-column deliverable table: "
    "| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |\n"
    "- All `{{SC_PLACEHOLDER:*}}` sentinels must be replaced with real content\n"
    "- Include these top-level sections: Executive Summary, Milestone Summary table, "
    "Dependency Graph, per-milestone sections (each contains its own "
    "`### Risk Assessment and Mitigation \u2014 M{N}` subsection), "
    "Resource Requirements and Dependencies, Risk Register, "
    "Success Criteria and Validation Approach, Decision Summary, Timeline Estimates\n"
    "- Open Questions live PER-MILESTONE. Each milestone with one or more unresolved "
    "questions MUST contain a `### Open Questions \u2014 M{N}` subsection as its final "
    "subsection (after `### Milestone Dependencies \u2014 M{N}`). Columns: "
    "| # | ID | Question | Impact | Resolution Owner | Target |. "
    "OMIT the subsection entirely when the milestone has zero open questions. "
    "Do NOT emit a global `## Open Questions` section at the end of the file.\n"
    "- OQ-xxx IDs are decisions, NOT deliverables. Do NOT create rows in the "
    "9-column deliverable table whose `ID` column is `OQ-xxx`. Each OQ belongs in "
    "the per-milestone `### Open Questions \u2014 M{N}` subsection of the milestone "
    "whose exit criteria require its resolution. OQ-xxx MAY appear in the `Deps` "
    "column of deliverable rows that wait on the decision.\n"
)


def wrap_for_incremental_write(
    base_prompt: str,
    output_path: Path,
    template_path: Path | None = None,
) -> str:
    """Augment a prompt with incremental-write instructions.

    Instructs the LLM to write output to *output_path* using the Write tool,
    section by section, instead of producing output on stdout.

    When *template_path* is provided, the LLM is told to read the template
    first and use it as the structural skeleton for the output.

    This is composable: call it on any prompt builder's return value to
    switch that step from one-shot stdout to tool-use file writing.
    """
    parts = [
        "## INCREMENTAL WRITE MODE\n\n"
        "CRITICAL: Do NOT produce your output as a response on stdout. "
        "Instead, you MUST write the output file using the Write tool.\n\n"
        f"**Output file path:** `{output_path}`\n\n"
        "**Writing procedure:**\n"
    ]

    if template_path is not None:
        parts.append(
            f"1. Read the template at `{template_path}` to understand the "
            "required output structure.\n"
            f"2. Create the output file at `{output_path}` using the Write tool. "
            "Start with the frontmatter and first major section.\n"
            "3. Use the Edit tool to append each subsequent section one at a time. "
            "Read what you have already written before adding the next section "
            "to ensure cross-section coherence.\n"
            "4. After writing all sections, read the completed file and verify "
            "that every `{{SC_PLACEHOLDER:` sentinel has been replaced. "
            "Fix any remaining sentinels with targeted edits.\n\n"
        )
    else:
        parts.append(
            f"1. Create the output file at `{output_path}` using the Write tool. "
            "Start with the frontmatter and first major section.\n"
            "2. Use the Edit tool to append each subsequent section one at a time. "
            "Read what you have already written before adding the next section "
            "to ensure cross-section coherence.\n"
            "3. After writing all sections, read the completed file to verify "
            "structural completeness and internal consistency.\n\n"
        )

    parts.append(
        "**Why incremental writing:** Writing section-by-section produces "
        "dramatically better output than generating everything in a single "
        "response. Each section gets your full attention, format is enforced "
        "by the template, and you can self-correct by reading prior sections "
        "before writing subsequent ones.\n\n"
        "After writing the complete file, output a single line on stdout: "
        f"`INCREMENTAL_WRITE_COMPLETE: {output_path}`\n\n"
        "---\n\n"
    )

    return "".join(parts) + base_prompt


def build_extract_prompt(
    spec_file: Path,
    retrospective_content: str | None = None,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'extract'.

    Instructs Claude to read the provided specification and produce
    extraction.md with YAML frontmatter containing all 13 required
    protocol fields plus 8 structured body sections.

    Parameters
    ----------
    spec_file:
        Path to the specification file being extracted.
    retrospective_content:
        Optional retrospective text from a prior release cycle.
        When provided, it is framed as advisory "areas to watch"
        context -- NOT as hard requirements (RSK-004 mitigation).
    """
    base = (
        "You are a requirements extraction specialist.\n\n"
        "Read the provided specification file and produce a requirements extraction document.\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- spec_source: (string) the source specification filename\n"
        "- generated: (string) ISO-8601 timestamp of extraction\n"
        "- generator: (string) identifier of the extraction agent\n"
        "- functional_requirements: (integer) count of identified functional requirements\n"
        "- nonfunctional_requirements: (integer) count of identified non-functional requirements\n"
        "- total_requirements: (integer) sum of functional + non-functional requirements\n"
        "- complexity_score: (float 0.0-1.0) assessing overall complexity\n"
        "- complexity_class: (string) one of: LOW, MEDIUM, HIGH\n"
        "- domains_detected: (list) array of domain name strings, e.g. [backend, security, frontend]\n"
        "- risks_identified: (integer) count of risks found in the specification\n"
        "- dependencies_identified: (integer) count of external dependencies\n"
        "- success_criteria_count: (integer) count of measurable success criteria\n"
        "- extraction_mode: (string) one of: standard, chunked\n\n"
        "After the frontmatter, provide the following 8 structured sections:\n\n"
        "## Functional Requirements\n"
        "Use the spec's exact requirement identifiers verbatim as primary IDs. "
        "Do NOT create a new numbering scheme (e.g., do NOT renumber as FR-001, FR-002). "
        "If a spec uses FR-EVAL-001.1, use FR-EVAL-001.1. "
        "If a requirement needs sub-decomposition, use suffixes on the original ID "
        "(e.g., FR-EVAL-001.1a, FR-EVAL-001.1b). "
        "If the spec has no requirement IDs, then use FR-NNN as a fallback. "
        "The functional_requirements frontmatter count must equal the number of "
        "top-level requirements in the spec, not sub-decompositions.\n"
        "For each requirement, also record the EXACT endpoint paths, URLs, or route "
        "patterns from the spec -- including paths shown in workflow diagrams, sequence "
        "diagrams, and ASCII art, not just paths in requirement tables. Preserve the "
        "verbatim path from the spec; do not rename, restyle, or substitute "
        "alternative paths.\n\n"
        "## Non-Functional Requirements\n"
        "Use the spec's exact NFR identifiers verbatim. Do NOT renumber. "
        "If the spec has no NFR IDs, use NFR-NNN as a fallback. "
        "Include performance, security, scalability, maintainability.\n\n"
        "## Complexity Assessment\n"
        "Provide complexity_score and complexity_class with detailed scoring rationale.\n\n"
        "## Architectural Constraints\n"
        "List all architectural constraints, technology mandates, and integration boundaries.\n\n"
        "## Component Inventory\n"
        "Scan the specification for named components, services, classes, modules, "
        "interfaces, DTOs, and type definitions defined in dependency graphs, component "
        "tables, module listings, data model sections, or architecture sections -- even "
        "if they are not tagged with explicit IDs. For each one, assign a synthetic ID:\n"
        "- COMP-xxx for services, classes, modules, and middleware\n"
        "- DM-xxx for data model interfaces, DTOs, and type definitions "
        "(e.g., a response DTO or a shared type union)\n\n"
        "Record for each:\n"
        "- Name and source file path (if specified)\n"
        "- Role/responsibility (one sentence)\n"
        "- Dependencies (other components it depends on)\n"
        "- Fields or methods (for interfaces/DTOs: list every field with its type)\n"
        "- Source reference (section number and line or paragraph where it is defined)\n\n"
        "This inventory ensures that architectural components AND data contracts described "
        "in prose or code blocks are not lost during roadmap generation. "
        "The IDs you assign here become deliverable row IDs in the roadmap.\n\n"
        "## Risk Inventory\n"
        "Numbered list of identified risks with severity (high/medium/low) and mitigation.\n\n"
        "## Dependency Inventory\n"
        "List all external dependencies, libraries, services, and integration points.\n\n"
        "## Success Criteria\n"
        "Measurable success criteria with acceptance thresholds.\n\n"
        "## Open Questions\n"
        "Ambiguities, gaps, or items requiring stakeholder clarification.\n\n"
        "Be thorough and precise. Extract every requirement, even implicit ones."
    )

    if retrospective_content:
        advisory = (
            "\n\n## Advisory: Areas to Watch (from prior retrospective)\n\n"
            "The following retrospective content is provided as advisory context "
            "only. These are areas to watch during extraction -- they are NOT "
            "additional requirements and MUST NOT be treated as such. Use them "
            "to inform your risk assessment and open questions sections.\n\n"
            f"{retrospective_content}"
        )
        base += advisory

    if tdd_file is not None:
        base += (
            "\n\n## Supplementary TDD Context (when TDD file is provided)\n\n"
            "A Technical Design Document (TDD) is included in the inputs alongside "
            "the specification. Use it to enrich the extraction with technical detail "
            "the spec may not fully define:\n"
            "1. Data model definitions from the TDD's Data Models section (§7) -- "
            "surface entity names, field types, and relationships in Architectural Constraints.\n"
            "2. API endpoint specifications from the TDD's API Specifications section (§8) -- "
            "surface endpoint contracts as implicit Functional Requirements if not in the spec.\n"
            "3. Component inventory from the TDD's Component Inventory section (§10) -- "
            "note component dependencies in Dependency Inventory.\n"
            "4. Testing strategy from the TDD's Testing Strategy section (§15) -- "
            "surface test coverage targets as Success Criteria.\n"
            "5. Migration and rollout details from the TDD's Migration section (§19) -- "
            "surface rollback procedures and feature flags in Risk Inventory.\n"
            "6. Operational readiness from the TDD's Operational Readiness section (§25) -- "
            "surface monitoring and on-call requirements as Non-Functional Requirements.\n"
            "The TDD provides technical depth -- use it to fill gaps in the spec, "
            "but preserve the spec's requirement IDs and language as primary."
        )

    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
            "A Product Requirements Document (PRD) is included in the inputs alongside "
            "the specification. Use it as supplementary business context for extraction. "
            "Additionally extract:\n"
            "1. Business objectives and success metrics from the PRD's Success Metrics "
            "section (S19) -- surface as additional Success Criteria.\n"
            "2. User personas from the PRD's User Personas section (S7) -- note in the "
            "Architectural Constraints section as persona-driven design requirements.\n"
            "3. Scope boundaries from the PRD's Scope Definition section (S12) -- use to "
            "validate that extracted requirements fall within stated scope.\n"
            "4. Legal and compliance requirements from the PRD's Legal & Compliance "
            "section (S17) -- surface as Non-Functional Requirements if not already "
            "present in the spec.\n"
            "5. Jobs To Be Done from the PRD's JTBD section (S6) -- note in Open "
            "Questions if any JTBD lack corresponding functional requirements.\n"
            "The PRD defines business requirements (personas, compliance, success metrics, scope). "
            "Treat these as authoritative for business context. When PRD business requirements "
            "conflict with the specification's technical approach, the specification wins on "
            "implementation details but the PRD wins on business intent and constraints."
        )

    return base + _OUTPUT_FORMAT_BLOCK


def build_extract_prompt_tdd(
    spec_file: Path,
    retrospective_content: str | None = None,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'extract' when input is a TDD (Technical Design Document).

    Extends the standard extract prompt with 6 additional body sections
    targeting TDD-specific structured content (data models, API specs,
    component inventory, testing strategy, migration plan, operational
    readiness). All 8 standard sections are retained for backward
    compatibility with downstream consumers.

    Parameters
    ----------
    spec_file:
        Path to the TDD file being extracted.
    retrospective_content:
        Optional retrospective text from a prior release cycle.
    """
    base = (
        "You are a requirements and design extraction specialist.\n\n"
        "Read the provided source specification or technical design document "
        "and produce a requirements and design extraction document.\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- spec_source: (string) the filename of the input document\n"
        "- generated: (string) ISO-8601 timestamp of extraction\n"
        "- generator: (string) identifier of the extraction agent\n"
        "- functional_requirements: (integer) count of identified functional requirements\n"
        "- nonfunctional_requirements: (integer) count of identified non-functional requirements\n"
        "- total_requirements: (integer) sum of functional + non-functional requirements\n"
        "- complexity_score: (float 0.0-1.0) assessing overall complexity\n"
        "- complexity_class: (string) one of: LOW, MEDIUM, HIGH\n"
        "- domains_detected: (list) array of domain name strings, e.g. [backend, security, frontend, testing, devops]\n"
        "- risks_identified: (integer) count of risks found in the document\n"
        "- dependencies_identified: (integer) count of external dependencies\n"
        "- success_criteria_count: (integer) count of measurable success criteria\n"
        "- extraction_mode: (string) one of: standard, chunked\n"
        "- data_models_identified: (integer) count of data entities/interfaces identified, or 0 if section absent\n"
        "- api_surfaces_identified: (integer) count of API endpoints identified, or 0 if section absent\n"
        "- components_identified: (integer) count of components/routes identified, or 0 if section absent\n"
        "- test_artifacts_identified: (integer) count of test cases/strategies identified, or 0 if section absent\n"
        "- migration_items_identified: (integer) count of migration phases/rollback steps identified, or 0 if section absent\n"
        "- operational_items_identified: (integer) count of runbook scenarios/alerts identified, or 0 if section absent\n\n"
        "Set `spec_source` to the filename of the input document.\n\n"
        "Preserve exact identifiers from the source document including "
        "requirement IDs (FR-xxx, NFR-xxx), interface names, endpoint identifiers, "
        "component names, migration phase names, and test case IDs. "
        "If a source uses FR-EVAL-001.1, use FR-EVAL-001.1. "
        "If identifiers need sub-decomposition, use suffixes on the original ID "
        "(e.g., FR-EVAL-001.1a, FR-EVAL-001.1b). "
        "If the source has no requirement IDs, then use FR-NNN as a fallback. "
        "The functional_requirements frontmatter count must equal the number of "
        "top-level requirements in the document, not sub-decompositions.\n\n"
        "After the frontmatter, provide the following 14 structured sections:\n\n"
        # --- 8 standard sections (same as build_extract_prompt) ---
        "## Functional Requirements\n"
        "Use the document's exact requirement identifiers verbatim as primary IDs. "
        "Do NOT create a new numbering scheme (e.g., do NOT renumber as FR-001, FR-002). "
        "If the document uses FR-EVAL-001.1, use FR-EVAL-001.1. "
        "If a requirement needs sub-decomposition, use suffixes on the original ID "
        "(e.g., FR-EVAL-001.1a, FR-EVAL-001.1b). "
        "If the document has no requirement IDs, then use FR-NNN as a fallback. "
        "The functional_requirements frontmatter count must equal the number of "
        "top-level requirements in the document, not sub-decompositions.\n\n"
        "## Non-Functional Requirements\n"
        "Use the document's exact NFR identifiers verbatim. Do NOT renumber. "
        "If the document has no NFR IDs, use NFR-NNN as a fallback. "
        "Include performance, security, scalability, maintainability.\n\n"
        "## Complexity Assessment\n"
        "Provide complexity_score and complexity_class with detailed scoring rationale.\n\n"
        "## Architectural Constraints\n"
        "List all architectural constraints, technology mandates, and integration boundaries.\n\n"
        "## Risk Inventory\n"
        "Numbered list of identified risks with severity (high/medium/low) and mitigation.\n\n"
        "## Dependency Inventory\n"
        "List all external dependencies, libraries, services, and integration points.\n\n"
        "## Success Criteria\n"
        "Measurable success criteria with acceptance thresholds.\n\n"
        "## Open Questions\n"
        "Ambiguities, gaps, or items requiring stakeholder clarification.\n\n"
        # --- 6 new TDD-specific sections ---
        "## Data Models and Interfaces\n"
        "(Maps to TDD template S7: S7.1 Data Entities, S7.2 Data Flow, S7.3 Storage Strategy)\n"
        "Assign each data entity a unique ID using the scheme DM-NNN (DM-001, DM-002, etc.). "
        "Each identified entity must appear as a separate ### heading with its ID, "
        "following the same pattern as Functional Requirements above. "
        "Extract all data entities, TypeScript/code interfaces, field definitions with "
        "types/constraints/required status, entity relationships, data-flow steps, and "
        "storage/retention/backup strategy from fenced code blocks and markdown tables. "
        "For each entity: ID, name, fields, types, constraints, relationships.\n\n"
        "## API Specifications\n"
        "(Maps to TDD template S8: S8.1 API Overview table, S8.2 Endpoint Details, S8.4 API Governance)\n"
        "Assign each endpoint a unique ID using the scheme API-NNN (API-001, API-002, etc.). "
        "Each identified endpoint must appear as a separate ### heading with its ID, "
        "following the same pattern as Functional Requirements above. "
        "Extract endpoint inventory: HTTP method, URL path, auth requirements, rate limits, "
        "query parameters, request body schema, response schema, error codes and responses, "
        "versioning strategy, deprecation policy. Extract from endpoint tables and code "
        "examples even when no behavioral shall/must language is present.\n\n"
        "## Component Inventory\n"
        "(Maps to TDD template S10: S10.1 Routes/Pages, S10.2 Shared Components, S10.3 Component Hierarchy)\n"
        "Assign each component a unique ID using the scheme COMP-NNN (COMP-001, COMP-002, etc.). "
        "Each identified component must appear as a separate ### heading with its ID, "
        "following the same pattern as Functional Requirements above. "
        "Extract route/page tables, shared component tables with props/usage/locations, "
        "ASCII component hierarchy trees, state stores with shape/transitions/triggers/side "
        "effects. For each component: ID, name, type, location, dependencies.\n\n"
        "## Testing Strategy\n"
        "(Maps to TDD template S15: S15.1 Test Pyramid, S15.2 Test Cases per level)\n"
        "Assign each test case a unique ID using the scheme TEST-NNN (TEST-001, TEST-002, etc.). "
        "Each identified test case must appear as a separate ### heading with its ID, "
        "following the same pattern as Functional Requirements above. "
        "Extract test pyramid breakdown with coverage levels/tooling/targets/ownership, "
        "concrete test case tables with test-name/input/expected-output/mocks for "
        "unit/integration/E2E levels, and test environment matrix.\n\n"
        "## Migration and Rollout Plan\n"
        "(Maps to TDD template S19: S19.1 Strategy, S19.2 Feature Flags, S19.3 Rollout Stages, S19.4 Rollback)\n"
        "Assign each migration phase or task a unique ID using the scheme MIG-NNN (MIG-001, MIG-002, etc.). "
        "Each identified migration item must appear as a separate ### heading with its ID, "
        "following the same pattern as Functional Requirements above. "
        "Extract migration phases with tasks/duration/dependencies/rollback, feature flags "
        "with purpose/status/cleanup-date/owner, rollout stages with audience/success-criteria/"
        "monitoring/rollback-triggers, and numbered rollback procedure steps. Preserve "
        "sequential ordering as it implies task dependencies.\n\n"
        "## Operational Readiness\n"
        "(Maps to TDD template S25: S25.1 Runbook, S25.2 On-Call, S25.3 Capacity Planning; "
        "also S14: S14.1 Logging, S14.2 Metrics, S14.3 Tracing, S14.4 Alerts)\n"
        "Assign each operational item a unique ID using the scheme OPS-NNN (OPS-001, OPS-002, etc.). "
        "Each identified operational item must appear as a separate ### heading with its ID, "
        "following the same pattern as Functional Requirements above. "
        "Extract runbook scenarios with symptoms/diagnosis/resolution/escalation/prevention, "
        "on-call expectations with page-volume/MTTD/MTTR/knowledge-prerequisites, capacity "
        "planning with current/projected/scaling-triggers, and observability including log "
        "formats, metric definitions, alert thresholds, trace sampling, and dashboard "
        "specifications.\n\n"
        "Be thorough and precise. Extract every requirement and design artifact, even implicit ones."
    )

    if retrospective_content:
        advisory = (
            "\n\n## Advisory: Areas to Watch (from prior retrospective)\n\n"
            "The following retrospective content is provided as advisory context "
            "only. These are areas to watch during extraction -- they are NOT "
            "additional requirements and MUST NOT be treated as such. Use them "
            "to inform your risk assessment and open questions sections.\n\n"
            f"{retrospective_content}"
        )
        base += advisory

    # if tdd_file is not None:
    #     base += (
    #         "\n\n## Supplementary TDD Context (when additional TDD file is provided)\n\n"
    #         "An additional Technical Design Document (TDD) is included in the inputs "
    #         "alongside the primary document. Use it to cross-reference and enrich "
    #         "the extraction:\n"
    #         "1. Verify data model consistency between documents -- flag discrepancies "
    #         "in entity definitions, field types, or relationships in Open Questions.\n"
    #         "2. Cross-check API endpoint specifications -- surface any endpoints in the "
    #         "supplementary TDD not covered in the primary document.\n"
    #         "3. Verify component inventory alignment -- flag components mentioned in one "
    #         "document but absent from the other.\n"
    #         "4. Cross-check testing strategy coverage -- surface test cases from the "
    #         "supplementary TDD that extend the primary document's strategy.\n"
    #         "5. Verify migration plan consistency -- flag rollback procedures or feature "
    #         "flags that differ between documents.\n"
    #         "The supplementary TDD provides additional technical reference -- use it "
    #         "to validate completeness, not to override the primary document."
    #     )

    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
            "A Product Requirements Document (PRD) is included in the inputs alongside "
            "the TDD. Use it as supplementary business context for extraction. "
            "Additionally extract:\n"
            "1. Business objectives and success metrics from the PRD's Success Metrics "
            "section (S19: S19.1 Product Metrics, S19.2 Business Metrics, S19.3 Technical "
            "Metrics) -- surface as additional Success Criteria.\n"
            "2. User personas from the PRD's User Personas section (S7: S7.1 Primary, "
            "S7.2 Secondary, S7.3 Tertiary, S7.4 Anti-Personas) -- note in the "
            "Architectural Constraints section as persona-driven design requirements.\n"
            "3. Scope boundaries from the PRD's Scope Definition section (S12: S12.1 In "
            "Scope, S12.2 Out of Scope, S12.3 Permanently Out of Scope) -- use to "
            "validate that extracted requirements fall within stated scope.\n"
            "4. Legal and compliance requirements from the PRD's Legal & Compliance "
            "section (S17: S17.1 Regulatory Compliance table, S17.2 Data Privacy) -- "
            "surface as Non-Functional Requirements if not already present in the TDD.\n"
            "5. Jobs To Be Done from the PRD's JTBD section (S6: S6.1 Primary Jobs, "
            "S6.2 Related Jobs) -- note in Open Questions if any JTBD lack corresponding "
            "functional requirements.\n"
            "6. Risk factors from the PRD's Risk Analysis section (S20: S20.1 Technical "
            "Risks, S20.2 Business Risks, S20.3 Operational Risks) -- cross-reference with "
            "TDD risks and surface any business/operational risks not covered.\n"
            "The PRD defines business requirements (personas, compliance, success metrics, scope). "
            "Treat these as authoritative for business context. When PRD business requirements "
            "conflict with the TDD's technical approach, the TDD wins on implementation details "
            "but the PRD wins on business intent and constraints."
        )

    return base + _OUTPUT_FORMAT_BLOCK


def build_generate_prompt(
    agent: AgentSpec,
    extraction_path: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'generate-{agent.id}'.

    Instructs Claude to read the extraction document and generate a
    complete project roadmap with the agent's persona as a role instruction.
    References expanded extraction fields for richer context.
    """
    base = (
        f"You are a {agent.persona} specialist creating a project roadmap.\n\n"
        "Read the provided requirements extraction document and generate a comprehensive "
        "project roadmap.\n\n"
        "The extraction document contains YAML frontmatter with these fields you should "
        "reference for context:\n"
        "- spec_source, generated, generator: provenance metadata\n"
        "- functional_requirements, nonfunctional_requirements, total_requirements: scope counts\n"
        "- complexity_score, complexity_class: complexity assessment\n"
        "- domains_detected: list of technical domain names to address\n"
        "- risks_identified: number of risks to mitigate in the roadmap\n"
        "- dependencies_identified: external dependencies to plan around\n"
        "- success_criteria_count: measurable criteria to validate against\n"
        "- extraction_mode: extraction completeness indicator\n"
        "\n"
        "The extraction body contains these standard sections:\n"
        "- Functional Requirements: requirement IDs, descriptions, acceptance criteria\n"
        "- Non-Functional Requirements: performance, security, scalability constraints\n"
        "- Complexity Assessment: scoring rationale and classification\n"
        "- Architectural Constraints: technology mandates, integration boundaries\n"
        "- Risk Inventory: identified risks with severity and mitigation\n"
        "- Dependency Inventory: external dependencies and integration points\n"
        "- Success Criteria: measurable validation thresholds\n"
        "- Open Questions: ambiguities requiring stakeholder clarification\n"
    )

    # -- Output structure (delegated to template) + semantic rules --
    base += _TEMPLATE_STRUCTURE_DIRECTIVE
    base += (
        f"\n- primary_persona: {agent.persona}\n\n"
        "FIELD-LEVEL FIDELITY for DM-xxx and COMP-xxx rows: AC MUST enumerate "
        "EVERY field/column/property from the source definition in compact notation. "
        "Example: 'id:UUID-PK; email:unique-idx; display_name:varchar; "
        "password_hash:varchar; is_locked:bool; created_at:timestamptz; "
        "updated_at:timestamptz'. All source fields must appear. "
        "Missing field = spec-fidelity deviation.\n\n"
        "   Every ID from the extraction MUST appear as its own row. "
        "Do NOT merge multiple IDs into one row.\n\n"
        f"Apply your {agent.persona} perspective throughout: prioritize concerns, "
        f"risks, and recommendations that a {agent.persona} would emphasize.\n\n"
        "Use numbered and bulleted lists for actionable items. Be specific and concrete.\n\n"
        "IMPORTANT: Preserve ALL IDs from the extraction document — requirement IDs "
        "(FR-xxx, NFR-xxx) AND entity IDs (DM-xxx, API-xxx, COMP-xxx, TEST-xxx, "
        "MIG-xxx, OPS-xxx). Do NOT renumber, relabel, or create new IDs. "
        "Each ID must appear as a separate deliverable row in the milestone-based implementation plan. "
        "If the extraction uses FR-EVAL-001.1, your roadmap must use FR-EVAL-001.1. "
        "If the extraction uses API-001, your roadmap must have a deliverable row for API-001."
        "\n\n"
        "ARCHITECTURAL COMPONENT COVERAGE: Beyond extraction IDs, scan the source "
        "document for named components, services, classes, or modules defined in "
        "architecture sections (dependency graphs, component tables, module listings). "
        "If the extraction assigned COMP-xxx IDs to these, use those IDs. If any "
        "prose-described component lacks an extraction ID, assign a new COMP-xxx ID "
        "and create a deliverable row for it. Example: if the source defines an orchestrator "
        "class in a dependency graph (e.g., 'auth-service.ts → token-manager.ts'), "
        "that orchestrator MUST have its own COMP-xxx deliverable row even if it has no "
        "explicit ID in the source."
        "\n\n"
        "GRANULARITY FLOOR: The number of deliverable rows MUST be proportional to input "
        "detail. Use these minimums:\n"
        "- Input with <50 entities/requirements: at least 40 deliverable rows\n"
        "- Input with 50-100 entities/requirements: at least 80 deliverable rows\n"
        "- Input with 100-200 entities/requirements: at least 120 deliverable rows\n"
        "- Input with 200+ entities/requirements: at least 150 deliverable rows\n"
        "Count entities from the extraction frontmatter (total_requirements + all "
        "entity IDs). If the extraction lists 14 FR + 9 NFR + data models + API "
        "endpoints + components + test cases = ~80 entities, produce at least 80 "
        "deliverable rows. One entity = one row minimum."
        "\n\n"
        "INTERNAL CONSISTENCY — MILESTONE DURATIONS: When the roadmap represents "
        "milestone durations in more than one place (milestone section headings, Timeline Estimates "
        "table), EVERY representation of a given milestone "
        "MUST agree on the same start week, end week, and total duration. Before "
        "finalizing output, cross-check each milestone's week range in the heading "
        "against its row in the Timeline Estimates table and fix any disagreement. "
        "Do not emit two different schedules in the same document."
    )

    if tdd_file is not None:
        base += (
            "\n\n## TDD as Primary Work Item Source\n\n"
            "A Technical Design Document (TDD) is included in the inputs. The TDD is the "
            "PRIMARY source of work items for the roadmap — it contains granular, individually "
            "specified implementation artifacts that the extraction document summarizes.\n\n"
            "CRITICAL: Read the TDD directly and create a SEPARATE deliverable table row for EACH "
            "independently implementable item found in the TDD, including but not limited to:\n"
            "- Each data model/interface from S7 (S7.1 Data Entities with TypeScript interfaces, "
            "S7.2 Data Flow diagrams, S7.3 Storage Strategy) AND each field within it\n"
            "- Each API endpoint from S8 (S8.1 Overview table, S8.2 Endpoint Details with "
            "request/response schemas, S8.4 API Governance) AND its sub-concerns (request "
            "validation, response schema, error handling, rate limiting, auth integration)\n"
            "- Each UI/service component from S10 (S10.1 Routes/Pages, S10.2 Shared Components "
            "with props/usage, S10.3 Component Hierarchy) AND its sub-concerns\n"
            "- Each test case from S15 (S15.1 Test Pyramid levels, S15.2 Test Cases tables)\n"
            "- Each migration phase, feature flag, and rollback step from S19 (S19.1 Strategy, "
            "S19.2 Feature Flags with cleanup dates, S19.3 Rollout Stages, S19.4 Rollback)\n"
            "- Each operational readiness item from S25 (S25.1 Runbook scenarios, S25.2 On-Call, "
            "S25.3 Capacity Planning) and each observability item from S14 (S14.1 Logging, "
            "S14.2 Metrics, S14.3 Tracing, S14.4 Alerts)\n\n"
            "The extraction document provides requirement IDs (FR-xxx, NFR-xxx) that map TDD "
            "items back to requirements. Use these IDs for traceability but use the TDD's "
            "granularity for task decomposition. A TDD with 876 lines should produce MORE "
            "roadmap deliverable rows than a 312-line spec, not fewer.\n\n"
            "Preserve exact identifiers from the TDD: interface names, endpoint paths, "
            "component names, test case IDs, and migration phase names.\n\n"
            "Use technical-layer phasing (Foundation → Core Logic → Integration → Hardening → "
            "Production Readiness) unless doing so would split acceptance criteria that the "
            "source packages together at a single milestone exit. The TDD's rollout plan "
            "informs the Production Readiness milestone, not the overall milestone structure."
            "\n\n"
            "FEATURE-BUNDLE INTEGRITY RULE: When the source packages multiple acceptance "
            "criteria or requirement sub-clauses together as the exit condition of one of its "
            "milestones, every one of those ACs must land in, or before, the roadmap milestone "
            "that claims to deliver the parent requirement. If technical layering forces a "
            "split, the earlier milestone's deliverable row must carry a gating acceptance "
            "criterion that prevents external exposure of the partial feature until the "
            "dependent AC lands (disabled by default, feature-flagged off, restricted to "
            "internal tenants, or equivalent mechanism). Shipping an externally reachable "
            "partial feature while its source-packaged co-requirement slips to a later "
            "milestone is a spec-fidelity deviation."
            "\n\n"
            "MEASURABLE-TARGET INSTRUMENTATION RULE: For every numeric target the source "
            "documents tie to a time bound, success window, or per-operation budget — "
            "regardless of which section the source states it in — create a dedicated "
            "implementation deliverable row (emitter plus histogram or counter, plus an alert "
            "rule where a threshold is named). This covers, non-exhaustively: component-level "
            "performance budgets stated in architecture or design sections, end-to-end SLAs "
            "stated in user journeys or product acceptance criteria, availability and "
            "error-rate SLOs, and adoption or business metrics with explicit time-to-target "
            "windows. A target whose only roadmap trace is a success-criteria row, a "
            "validation-task acceptance criterion, or an aggregate envelope covering multiple "
            "sub-targets is not instrumented — that is a spec-fidelity deviation.\n"
            "- A later task may VALIDATE these deliverables exist and function correctly, "
            "but validation acceptance criteria without a corresponding implementation task "
            "create a 'validate what was never built' gap -- this is a HIGH severity "
            "spec-fidelity deviation.\n"
            "- Distinguish operational alert thresholds (degradation-level monitoring) from "
            "rollback triggers (crisis-level automated response). If the TDD specifies both, "
            "each needs its own task.\n"
            "- Distinguish structured application logging (stdout/JSON for operational "
            "debugging) from audit database persistence (compliance records in a data store). "
            "If the TDD specifies both, each needs its own task."
            "\n\n"
            "ROLLBACK AND PROCEDURE FIDELITY RULE: Rollback triggers stated in the source as "
            "automatic conditions (phrased as 'triggered when / if ... occurs') must be "
            "implemented as automated triggers from the first rollout. Any human-confirmation "
            "gate, burn-in period, staged activation, or approval layer changes the source "
            "contract and must be recorded as an Open Question with source citation, not "
            "silently inserted into deliverable acceptance criteria. Numbered procedures in "
            "the source (rollback steps, incident response steps, remediation steps) must be "
            "carried into the implementing task's acceptance criteria as an ordered checklist "
            "covering every step in source order, including any SLAs or time bounds attached "
            "to individual steps. Collapsing multiple source steps into a prose summary is a "
            "spec-fidelity deviation."
            "\n\n"
            "TDD OPEN QUESTIONS PRESERVATION RULE: If the source TDD contains an "
            "Open Questions section (S22), EVERY unresolved TDD Open Question MUST be carried "
            "forward into the relevant milestone's `### Open Questions — M{N}` subsection — "
            "the milestone whose exit criteria require the OQ's resolution. Preserve verbatim:\n"
            "- the original question text,\n"
            "- the original owner (or TBD if none was assigned),\n"
            "- the original target resolution date if present,\n"
            "- a source reference back to the TDD section.\n"
            "Do NOT create rows in the 9-column deliverable table whose ID column is OQ-xxx "
            "— OQ-xxx is a decision, not an implementation deliverable. The only exception to "
            "preservation is when the roadmap definitively CLOSES the question with a documented "
            "resolution — in that case record the closure rationale in the per-milestone "
            "Open Questions subsection (status: closed, resolution: ...). Silently dropping TDD "
            "Open Questions removes a forcing function for scheduled resolution."
            "\n\n"
            "QUALITY THRESHOLD INHERITANCE RULE: Every numeric quality, success, or "
            "acceptance target stated anywhere in the TDD or PRD — including NFR SLOs, "
            "coverage targets, latency and error-rate budgets, uptime commitments, success "
            "metrics, funnel thresholds, adoption targets, and any other numeric gate — MUST "
            "be inherited VERBATIM wherever the roadmap references it (milestone exit "
            "criteria, deliverable acceptance criteria, success criteria table, Timeline "
            "Estimates milestones). Verbatim means: same number, same unit, same measurement "
            "dimension, and same comparison operator. Do not tighten, do not loosen, do not "
            "round, do not unit-convert across measurement dimensions, and do not restate a "
            "target in a dimension the source did not use. Do not combine categories under a "
            "single higher bar. If an internal stretch target exists, it is an annotation on "
            "an aspirational row, never the validation gate. The source documents are "
            "authoritative for quality thresholds."
            "\n\n"
            "TIMELINE ANCHORING RULE: If the TDD provides a milestone schedule (S23 "
            "Timeline & Milestones) with "
            "absolute calendar dates, the roadmap Timeline Estimates section MUST:\n"
            "1. Use absolute dates anchored to those milestones — either in the Start/End "
            "columns directly, or alongside relative week numbers.\n"
            "2. Include a milestone mapping (either a separate table or an "
            "additional column in the Timeline Estimates table) showing which roadmap "
            "milestone corresponds to which TDD milestone, so either document can be used "
            "as the planning reference.\n"
            "3. Not exceed the TDD's committed end date for the default schedule. If the "
            "technically-phased roadmap requires more time than the TDD committed, the "
            "overshoot MUST be flagged as a blocking Open Question in the earliest affected "
            "milestone's `### Open Questions — M{N}` subsection, proposing either a "
            "rescheduled end date or a compressed execution plan, not presented as the "
            "silent default. A 'compressed alternative' noted in prose does not satisfy "
            "this rule — the committed default must respect the TDD schedule or the "
            "conflict must be an OQ."
            "\n\n"
            "NON-GOALS ARE HARD DELIVERABLE SCOPE: Before writing any deliverable row, "
            "check the row's capability against the TDD's Non-Goals / Out-of-Scope section "
            "(S4 Scope, if present) and Deferred sections. Items explicitly marked as "
            "out-of-scope or deferred to a later version are LOCKED SCOPE DECISIONS. If the "
            "row would implement, enforce, or gate on an out-of-scope capability, do not "
            "emit the row. If an in-scope behavior requires interaction with an out-of-scope "
            "subsystem, use a mechanism that does not assume that subsystem is present. "
            "Relitigating a Non-Goal inside acceptance criteria, deliverable descriptions, "
            "or gating predicates is forbidden and is a HIGH severity spec-fidelity "
            "deviation. Do NOT create Open Questions that relitigate these decisions. If "
            "genuine ambiguity remains about a Non-Goal, cite the Non-Goal identifier in "
            "the OQ entry and mark the entry as closed with the deferral target version as "
            "the resolution."
        )

    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
            "A Product Requirements Document (PRD) is included in the inputs alongside "
            "the extraction. Use PRD content to inform roadmap prioritization and phasing:\n"
            "1. **Value-based phasing**: Use the PRD's Business Context (S5) and Success "
            "Metrics (S19: S19.1 Product Metrics, S19.2 Business Metrics, S19.3 Technical "
            "Metrics) to prioritize milestones that deliver measurable business value earliest.\n"
            "2. **Persona-driven sequencing**: Use the PRD's User Personas (S7: S7.1 Primary, "
            "S7.2 Secondary, S7.3 Tertiary, S7.4 Anti-Personas) and Customer Journey Map "
            "(S22) to ensure the roadmap addresses highest-impact user needs first.\n"
            "3. **Compliance gates**: If the PRD's Legal & Compliance section (S17: S17.1 "
            "Regulatory Compliance table, S17.2 Data Privacy requirements) defines "
            "regulatory requirements, ensure the roadmap includes compliance validation "
            "milestones at appropriate points.\n"
            "4. **Scope guardrails**: Use the PRD's Scope Definition (S12: S12.1 In Scope, "
            "S12.2 Out of Scope, S12.3 Permanently Out of Scope) as a hard block: do NOT "
            "emit deliverable rows that implement, enforce, or gate on capabilities listed "
            "in S12.2 or S12.3. Relitigating an Out-of-Scope or Permanently Out-of-Scope "
            "boundary inside acceptance criteria or gating predicates is forbidden and is "
            "a HIGH severity spec-fidelity deviation.\n"
            "5. **Jobs To Be Done**: Use the PRD's JTBD section (S6: S6.1 Primary Jobs, "
            "S6.2 Related Jobs) to verify every primary job has corresponding deliverable rows. "
            "Flag any JTBD without implementation coverage in the `### Open Questions — M{N}` "
            "subsection of the milestone most closely linked to the uncovered capability "
            "(create the subsection if absent). Do NOT add OQ-xxx rows to the 9-column deliverable table.\n"
            "6. **Risk alignment**: Cross-reference PRD risks (S20: S20.1 Technical Risks, "
            "S20.2 Business Risks, S20.3 Operational Risks) with the roadmap's Risk Register "
            "to ensure coverage of business-side risks the TDD may omit.\n"
            "The PRD provides business 'why' context. It informs priority WITHIN milestones "
            "and enriches task descriptions. It does NOT change the number of milestones, the "
            "milestone paradigm (technical layers, not delivery milestones), or reduce the "
            "number of deliverable rows. PRD personas, compliance requirements, and success metrics "
            "should appear as ADDITIONAL deliverable rows or acceptance criteria, not as reasons to "
            "consolidate existing deliverables."
            "\n\n"
            "PRD USER STORY COMPLETENESS RULE: For each PRD in-scope user story (S21: "
            "S21.1 Epics & User Stories, S21.3 Phasing) or "
            "capability, verify that the roadmap contains ALL implementation tasks "
            "required to deliver that capability end-to-end:\n"
            "- If a user story implies an API endpoint (e.g., logout implies a session "
            "termination endpoint), create an API-xxx deliverable row even if the TDD omits it.\n"
            "- If a user story specifies a security behavior in its acceptance criteria "
            "(e.g., password reset invalidates all existing sessions), add that behavior "
            "as an AC on the relevant implementation task.\n"
            "- If a user story implies a frontend action with a backend counterpart, "
            "ensure both implementation deliverable rows exist.\n"
            "Flag any PRD-derived additions as gap fills in the `### Open Questions — M{N}` "
            "subsection of the milestone that owns the gap-filling deliverable (create the "
            "subsection if absent) with resolution 'PRD requires; TDD should be updated'. "
            "Do NOT add OQ-xxx rows to the 9-column deliverable table."
        )

    if tdd_file is not None and prd_file is not None:
        base += (
            "\n\n## Document Conflict Resolution\n\n"
            "When the TDD and PRD specify DIFFERENT values for the same parameter "
            "(e.g., retention period, timeline/milestone dates, milestone count or structure, "
            "success metric thresholds), you MUST:\n"
            "1. Document each conflict as an Open Question entry (OQ-xxx) in the "
            "`### Open Questions — M{N}` subsection of the earliest milestone whose exit "
            "criteria depend on the resolution (create the subsection if absent). The entry "
            "must include: the TDD value, the PRD value, which takes precedence and why, and "
            "the downstream impact on other roadmap items. Do NOT add OQ-xxx rows to the "
            "9-column deliverable table — OQs are decisions, not deliverables.\n"
            "2. RESOLVE the conflict — do not leave it hanging. The OQ must state the "
            "chosen value AND the precedence rule used. Then pick ONE of the two paths "
            "below; do NOT mix them:\n"
            "   (a) **Commit path**: apply the chosen value verbatim and consistently "
            "across EVERY affected section — task acceptance criteria, timeline estimates, "
            "success criteria, infrastructure sizing, data-model fields. Cite the OQ ID "
            "next to each committed value for traceability.\n"
            "   (b) **TBD path**: if the conflict genuinely cannot be resolved during "
            "generation, mark every affected field as `TBD-pending-OQ-xxx` (not a "
            "concrete value) and flag the OQ as a M1 blocker.\n"
            "Committing to one side in any section while citing the OQ as 'unresolved' "
            "elsewhere — or committing to DIFFERENT sides in different sections — is a "
            "HIGH severity spec-fidelity deviation. Every downstream section must "
            "reflect the same choice.\n"
            "3. When the roadmap restructures the TDD's milestone layout "
            "(e.g., splitting 3 milestones into 5), include a milestone-mapping table showing "
            "how TDD milestones map to roadmap milestones so teams referencing either "
            "document can reconcile.\n"
            "Undocumented conflicts are MEDIUM severity spec-fidelity deviations; "
            "documented-but-inconsistently-applied conflicts are HIGH severity."
        )

    return base + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK


def build_diff_prompt(variant_a_path: Path, variant_b_path: Path) -> str:
    """Prompt for step 'diff'.

    Instructs Claude to compare two roadmap variants and produce
    diff-analysis.md with frontmatter fields total_diff_points,
    shared_assumptions_count.
    """
    return (
        "You are a comparative analysis specialist.\n\n"
        "Read the two provided roadmap variants and produce a structured diff analysis.\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- total_diff_points: (integer count of identified divergence points)\n"
        "- shared_assumptions_count: (integer count of shared assumptions)\n\n"
        "After the frontmatter, provide:\n"
        "1. Shared assumptions and agreements between variants\n"
        "2. Numbered list of divergence points, each with:\n"
        "   - Description of the difference\n"
        "   - Which variant takes which position\n"
        "   - Potential impact of each approach\n"
        "3. Areas where one variant is clearly stronger\n"
        "4. Areas requiring debate to resolve\n\n"
        "Be objective. Present both positions fairly without bias."
    ) + _OUTPUT_FORMAT_BLOCK


def build_debate_prompt(
    diff_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    depth: Literal["quick", "standard", "deep"],
) -> str:
    """Prompt for step 'debate'.

    Depth controls the number of debate rounds embedded in the prompt.
    """
    depth_instruction = _DEPTH_INSTRUCTIONS[depth]
    return (
        "You are a structured debate facilitator.\n\n"
        "Read the provided diff analysis and both roadmap variants. "
        "Facilitate a structured adversarial debate between the two approaches.\n\n"
        f"Debate format:\n{depth_instruction}\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- convergence_score: (float 0.0-1.0 indicating how much agreement was reached)\n"
        "- rounds_completed: (integer number of debate rounds conducted)\n\n"
        "After the frontmatter, provide the full debate transcript with:\n"
        "- Each round clearly labeled\n"
        "- Positions attributed to Variant A and Variant B\n"
        "- A convergence assessment summarizing areas of agreement and remaining disputes\n\n"
        "Ensure each perspective argues its strongest case. Do not artificially force agreement."
    ) + _OUTPUT_FORMAT_BLOCK


def build_score_prompt(
    debate_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'score'.

    Instructs Claude to select a base variant and score both.
    """
    base = (
        "You are an objective evaluation specialist.\n\n"
        "Read the debate transcript and both roadmap variants. "
        "Score each variant and select a base for the final merge.\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- base_variant: (string: the identifier of the selected base variant)\n"
        "- variant_scores: (string summary of scores, e.g. 'A:78 B:72')\n\n"
        "After the frontmatter, provide:\n"
        "1. Scoring criteria used (derived from the debate)\n"
        "2. Per-criterion scores for each variant\n"
        "3. Overall scores with justification\n"
        "4. Base variant selection rationale\n"
        "5. Specific improvements from the non-base variant to incorporate in merge\n\n"
        "Be evidence-based. Reference specific debate points and variant content."
    )

    if tdd_file is not None:
        base += (
            "\n\n## Supplementary TDD Context (when TDD file is provided)\n\n"
            "A Technical Design Document (TDD) is included in the inputs. When "
            "scoring variants, include these additional scoring dimensions:\n"
            "1. **Technical completeness**: Score whether each variant addresses all "
            "data models (§7), API endpoints (§8), and components (§10) from the TDD.\n"
            "2. **Testing strategy alignment**: Score whether each variant's test "
            "milestones match the TDD's test pyramid and coverage targets (§15).\n"
            "3. **Migration feasibility**: Score whether each variant's rollout plan "
            "accounts for the TDD's migration phases and rollback procedures (§19).\n"
            "Weight these alongside debate-derived scoring criteria."
        )

    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
            "A Product Requirements Document (PRD) is included in the inputs. When "
            "scoring variants, include these additional scoring dimensions:\n"
            "1. **Business value delivery**: Score how quickly each variant delivers "
            "against the PRD's Success Metrics (S19).\n"
            "2. **Persona coverage**: Score whether each variant addresses all user "
            "personas defined in the PRD (S7).\n"
            "3. **Compliance alignment**: Score whether each variant accounts for "
            "legal and compliance requirements from the PRD (S17).\n"
            "Weight these alongside technical scoring criteria."
        )

    return base + _OUTPUT_FORMAT_BLOCK


def build_merge_prompt(
    base_selection_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    debate_path: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'merge'.

    Instructs Claude to produce the final merged roadmap.
    """
    base = (
        "You are a synthesis specialist producing the final merged roadmap.\n\n"
        "Read the base selection document, both roadmap variants, and the debate transcript. "
        "Produce a final merged roadmap that uses the selected base variant as foundation "
        "and incorporates the best elements from the other variant as identified in the debate.\n"
        + _TEMPLATE_STRUCTURE_DIRECTIVE +
        "\nDuring merge, preserve the 9-column deliverable table schema from the variants. "
        "Do NOT invent a new table format.\n\n"
        "FIELD-LEVEL FIDELITY: For DM-xxx and COMP-xxx rows, AC MUST enumerate "
        "every field/column/property in compact notation (field:type). "
        "When merging, keep the version with MORE fields. Missing field = deviation.\n\n"
        "Use proper heading hierarchy (H2, H3, H4) with no gaps. "
        "Ensure all internal cross-references resolve. "
        "Do not duplicate heading text at H2 or H3 level.\n\n"
        "IMPORTANT — ID Preservation and Anti-Consolidation:\n"
        "- Preserve ALL task IDs from both variants. Do NOT renumber, relabel, or drop IDs.\n"
        "- The merged roadmap MUST have AT LEAST as many deliverable rows as the base variant. "
        "Merging means ADDING the best elements from the non-base variant, not consolidating "
        "rows from the base.\n"
        "- If both variants have a deliverable row for the same ID, keep the richer version. "
        "If only one variant has an ID, include it.\n"
        "- Do NOT merge multiple deliverable rows into one. Each ID = one row.\n\n"
        "COMPLETENESS CHECKLIST — Before emitting `INCREMENTAL_WRITE_COMPLETE`, verify "
        "every item below is present in the output file. Omitting any item is a merge failure "
        "that will be rejected by the completeness gate:\n"
        "- YAML frontmatter with all required fields populated (no `{{SC_PLACEHOLDER:*}}` left).\n"
        "- Executive Summary section.\n"
        "- Milestone Summary table enumerating every milestone `M1..M{N}`.\n"
        "- For EACH milestone `M{N}` declared in the Milestone Summary, a `## M{N}:` body "
        "section containing: the 9-column deliverable table, `### Integration Points — M{N}`, "
        "`### Milestone Dependencies — M{N}`, (only when the milestone has at least one "
        "open question) `### Open Questions — M{N}`, and "
        "`### Risk Assessment and Mitigation — M{N}` with the milestone's risk table.\n"
        "- `## Risk Register` aggregating every per-milestone risk into the 7-column schema "
        "`| ID | Risk | Affected Milestones | Probability | Impact | Mitigation | Owner |`. "
        "Each R-### row consolidates the risks listed in the per-milestone subsections; "
        "`Affected Milestones` is a comma-separated list of M{N} IDs.\n"
        "- `## Success Criteria and Validation Approach` with populated success table.\n"
        "- `## Decision Summary` section.\n"
        "- `## Timeline Estimates` section.\n"
        "- NO global `## Open Questions` section at the end of the document.\n"
        "- NO global `## Risk Assessment and Mitigation` section — risks live per-milestone "
        "(as `### Risk Assessment and Mitigation — M{N}`) and aggregate into `## Risk Register`.\n"
        "- NO row in any 9-column deliverable table whose `ID` column value matches `OQ-\\d+`.\n"
        "Write sections in order and call `INCREMENTAL_WRITE_COMPLETE` only after the final tail "
        "section is on disk. If turn budget is running low, prioritise writing the tail sections "
        "(Risk Register → Success Criteria → Decision Summary → Timeline Estimates) before "
        "expanding any milestone body further."
    )

    if tdd_file is not None:
        base += (
            "\n\n## Supplementary TDD Context (when TDD file is provided)\n\n"
            "A Technical Design Document (TDD) is included in the inputs. During merge:\n"
            "1. Preserve exact technical identifiers from both variants: interface names "
            "from S7.1 Data Entities, endpoint paths from S8.2 Endpoint Details "
            "(e.g., /api/v1/auth/login), component names from S10, test case IDs "
            "from S15.2, and migration phase names from S19.1.\n"
            "2. When variants disagree on API contracts (S8), data model schemas (S7), "
            "or component boundaries (S10), prefer the variant that more closely matches the TDD.\n"
            "3. Ensure the merged roadmap retains all TDD-derived implementation tasks "
            "(data model setup from S7, endpoint implementation from S8, observability "
            "instrumentation from S14, test execution from S15, migration rollout from S19, "
            "operational readiness from S25) from the selected base variant.\n"
            "4. Verify that quality thresholds from S5.2 (SLOs, coverage targets) are "
            "preserved verbatim in the merged variant — do not average or weaken targets."
        )

    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
            "A Product Requirements Document (PRD) is included in the inputs. During merge:\n"
            "1. Maintain alignment with PRD personas (S7: S7.1 Primary, S7.2 Secondary, "
            "S7.3 Tertiary, S7.4 Anti-Personas) — the merged roadmap should "
            "address all user personas mentioned in both variants.\n"
            "2. Preserve success metric targets from the PRD (S19: S19.1 Product Metrics, "
            "S19.2 Business Metrics, S19.3 Technical Metrics) — quantitative targets "
            "(e.g., >60% registration rate, <200ms latency) must appear in the merged "
            "success criteria, not be averaged or dropped.\n"
            "3. Ensure compliance requirements from the PRD (S17: S17.1 Regulatory "
            "Compliance, S17.2 Data Privacy) are not weakened during "
            "merge — if either variant has stronger compliance gates, prefer the stronger.\n"
            "4. Use PRD business context (S5 Business Context, S6 JTBD, S20 Risk Analysis) "
            "to break ties when variants conflict on prioritization or phasing order.\n"
            "5. Verify scope boundaries (S12: S12.1 In Scope, S12.2 Out of Scope) "
            "are respected in the merged output — do not include deliverables that either "
            "variant added but the PRD explicitly places out of scope."
        )

    return base + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK


def build_spec_fidelity_prompt(
    spec_file: Path,
    roadmap_path: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'spec-fidelity'.

    Instructs Claude to compare the specification against the roadmap,
    quote both documents for each deviation, and produce structured YAML
    frontmatter output with severity counts and tasklist_ready field.

    Embeds explicit severity definitions (HIGH/MEDIUM/LOW) to reduce
    LLM classification drift (RSK-007).
    """
    base = (
        "You are a source-document fidelity analyst.\n\n"
        "Read the provided source specification or TDD file and the generated roadmap. "
        "Compare them systematically to identify deviations where the roadmap "
        "diverges from or omits requirements, design decisions, or commitments in the source document.\n\n"
        "## Severity Definitions\n\n"
        "Apply these severity classifications precisely:\n\n"
        "**HIGH**: The roadmap omits, contradicts, or fundamentally misrepresents "
        "a source document requirement or commitment. The roadmap cannot be used as-is without "
        "risking incorrect implementation. Examples:\n"
        "- A functional requirement (FR-NNN) or interface definition (interface-name) is entirely missing from the roadmap\n"
        "- A non-functional requirement (NFR-NNN) is contradicted by the roadmap\n"
        "- A success criterion (SC-NNN) or test case (test-case-id) has no corresponding validation in the roadmap\n"
        "- An architectural constraint is violated by the roadmap's proposed approach\n"
        "- An API endpoint (endpoint-path) or component (component-name) is missing from the roadmap\n"
        "- A migration phase (migration-phase) or rollback procedure is omitted\n\n"
        "**MEDIUM**: The roadmap addresses the requirement but with insufficient "
        "detail, ambiguous language, or minor misalignment that could lead to "
        "implementation issues. Examples:\n"
        "- A requirement is mentioned but lacks specific acceptance criteria\n"
        "- The roadmap's phasing differs from the source document's priority ordering or stated importance hierarchy\n"
        "- A dependency is acknowledged but not properly sequenced\n\n"
        "**LOW**: Minor stylistic, formatting, or organizational differences that "
        "do not affect correctness. Examples:\n"
        "- Different heading structure or section ordering\n"
        "- Terminology variations that don't change meaning\n"
        "- Missing cross-references that don't affect understanding\n\n"
        "## Comparison Dimensions\n\n"
        "Compare across ALL of these dimensions:\n"
        "1. **Signatures**: Function/method/API signatures specified vs. roadmapped\n"
        "2. **Data Models**: Data structures, schemas, field definitions\n"
        "3. **Gates**: Quality gates, validation checkpoints, acceptance criteria\n"
        "4. **CLI Options**: Command-line flags, arguments, configuration options\n"
        "5. **NFRs**: Performance targets, security requirements, scalability constraints\n"
        + _INTEGRATION_WIRING_DIMENSION
    )

    # Dimensions 7-11: TDD-specific — only include when TDD input is provided
    if tdd_file is not None:
        base += (
            "7. **API Endpoints**: Endpoint contracts, request/response schemas, error codes, versioning policy\n"
            "8. **Component Inventory**: Module boundaries, component responsibilities, route coverage\n"
            "9. **Testing Strategy**: Test levels, coverage targets, validation matrix, test case coverage\n"
            "10. **Migration & Rollout**: Migration phases, rollback procedures, feature flag lifecycle\n"
            "11. **Operational Readiness**: Runbook scenarios, on-call expectations, alert configurations, capacity plans\n"
            "12. **Observability Implementation Completeness (anti-pattern: 'validate what was "
            "never built')**: For each metric, distributed trace span, alert threshold, or "
            "structured log format defined in the source document's observability/monitoring "
            "sections, verify the roadmap contains an IMPLEMENTATION task that creates the "
            "instrumentation -- not just a validation or verification AC in a later milestone. "
            "If a deliverable appears ONLY as acceptance criteria on a validation task "
            "(e.g., metrics listed in an M5 operational-readiness AC) with no earlier "
            "task to implement the instrumentation code, flag as HIGH severity. Also check:\n"
            "   - Operational alert thresholds (degradation-level monitoring) are tasked "
            "separately from rollback triggers (crisis-level automated response) when the "
            "source defines both with different threshold values.\n"
            "   - Structured application logging (stdout/JSON emission) is tasked separately "
            "from audit database persistence when the source defines both.\n"
        )

    base += (
        "\n## Output Requirements\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- high_severity_count: (integer) number of HIGH severity deviations\n"
        "- medium_severity_count: (integer) number of MEDIUM severity deviations\n"
        "- low_severity_count: (integer) number of LOW severity deviations\n"
        "- total_deviations: (integer) total number of deviations found\n"
        "- validation_complete: (boolean) true if analysis completed fully\n"
        "- tasklist_ready: (boolean) true ONLY if high_severity_count is 0 AND "
        "validation_complete is true\n\n"
        "After the frontmatter, provide:\n\n"
        "## Deviation Report\n\n"
        "For each deviation, provide a numbered entry with:\n"
        "- **ID**: DEV-NNN (zero-padded 3-digit)\n"
        "- **Severity**: HIGH, MEDIUM, or LOW\n"
        "- **Deviation**: Concise description of what differs\n"
        "- **Source Quote**: Verbatim quote from the source document\n"
        "- **Roadmap Quote**: Verbatim quote from the roadmap, or '[MISSING]' if absent\n"
        "- **Impact**: Assessment of how the deviation affects correctness\n"
        "- **Recommended Correction**: Specific action to resolve the deviation\n\n"
        "## Summary\n\n"
        "Provide a brief summary of findings with severity distribution.\n\n"
        "Be thorough and precise. Quote both documents for every deviation. "
        "Do not invent deviations -- only report genuine differences between "
        "the source document and roadmap."
    )

    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Validation (when PRD file is provided)\n\n"
            "A Product Requirements Document (PRD) is included in the inputs alongside "
            "the specification and roadmap. Additionally check these PRD-derived dimensions:\n"
            "12. **Persona Coverage**: Every user persona defined in the PRD (S7) should "
            "have at least one roadmap milestone or task addressing their primary needs. Flag "
            "missing persona coverage as MEDIUM severity.\n"
            "13. **Business Metric Traceability**: Success metrics from the PRD (S19) "
            "should have corresponding validation milestones or acceptance criteria in "
            "the roadmap. Flag untraced metrics as MEDIUM severity.\n"
            "14. **Compliance & Legal Coverage**: Legal and compliance requirements from "
            "the PRD (S17) should have corresponding roadmap tasks or gates. Flag missing "
            "compliance coverage as HIGH severity.\n"
            "15. **Scope Boundary Enforcement**: The roadmap should not contain items that "
            "fall outside the PRD's Scope Definition (S12 In-Scope vs Out-of-Scope). Flag "
            "out-of-scope roadmap items as MEDIUM severity.\n"
            "16. **PRD User Story Functional Completeness**: For each PRD in-scope user "
            "story, verify the roadmap contains ALL implementation tasks needed to deliver "
            "the capability end-to-end. Check specifically:\n"
            "   - API endpoints implied by user stories (e.g., a logout user story requires "
            "a session termination endpoint implementation task, not just a design component).\n"
            "   - Security behaviors stated in PRD acceptance criteria (e.g., 'password reset "
            "invalidates all sessions' must appear as an AC on the password reset implementation "
            "task, not be silently omitted).\n"
            "   - Frontend actions that require backend counterparts must have both tasks.\n"
            "   Flag missing implementation tasks as HIGH severity when the PRD explicitly "
            "lists the capability as in-scope."
        )

    return base + _OUTPUT_FORMAT_BLOCK


def build_wiring_verification_prompt(
    merge_file: Path,
    spec_source: str,
) -> str:
    """Prompt for step 'wiring-verification'.

    Instructs Claude to perform static wiring analysis on the merged
    roadmap output directory, checking for unwired callables, orphan
    modules, and unregistered dispatch entries (section 5.7 Step 2).

    Parameters
    ----------
    merge_file:
        Path to the merged roadmap file (roadmap.md).
    spec_source:
        The source specification filename for provenance.
    """
    return (
        "You are a static wiring verification analyst.\n\n"
        "Read the provided merged roadmap and verify the structural wiring "
        "integrity of the codebase described in the roadmap. Check for:\n\n"
        "1. **Unwired Optional Callable Injections (G-001)**: Constructor "
        "parameters typed as Optional[Callable] or Callable | None with "
        "default None that are never wired via keyword arguments.\n\n"
        "2. **Orphan Modules (G-002)**: Modules under provider directories "
        "(steps/, handlers/, validators/, checks/) with zero inbound imports "
        "from outside those directories.\n\n"
        "3. **Unregistered Dispatch Entries (G-003)**: Dict-based registries "
        "containing callable references that cannot be resolved in scope.\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- gate: wiring-verification\n"
        f"- target_dir: (the directory analyzed)\n"
        "- files_analyzed: (integer count)\n"
        "- files_skipped: (integer count)\n"
        "- rollout_mode: shadow\n"
        "- analysis_complete: true\n"
        "- audit_artifacts_used: 0\n"
        "- unwired_callable_count: (integer)\n"
        "- orphan_module_count: (integer)\n"
        "- unwired_registry_count: (integer)\n"
        "- critical_count: (integer)\n"
        "- major_count: (integer)\n"
        "- info_count: (integer)\n"
        "- total_findings: (integer)\n"
        "- blocking_findings: (integer)\n"
        "- whitelist_entries_applied: (integer)\n\n"
        "After the frontmatter, provide:\n"
        "1. Summary of analysis scope and findings\n"
        "2. Unwired Optional Callable Injections (if any)\n"
        "3. Orphan Modules / Symbols (if any)\n"
        "4. Unregistered Dispatch Entries (if any)\n"
        "5. Suppressions and Dynamic Retention notes\n"
        "6. Recommended Remediation actions\n"
        "7. Evidence and Limitations\n\n"
        "In shadow mode, report all findings but do not block the pipeline."
    ) + _OUTPUT_FORMAT_BLOCK


def build_test_strategy_prompt(
    roadmap_path: Path,
    extraction_path: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for step 'test-strategy'.

    Instructs Claude to produce a test strategy for the roadmap with
    6 frontmatter fields, complexity-to-ratio mapping, and issue
    classification table.
    """
    base = (
        "You are a test strategy specialist.\n\n"
        "Read the final roadmap and the requirements extraction document. "
        "Produce a comprehensive test strategy.\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- complexity_class: (string) one of: LOW, MEDIUM, HIGH -- from the extraction\n"
        "- validation_philosophy: (string) MUST be exactly 'continuous-parallel' (hyphenated, not underscored)\n"
        "- validation_milestones: (integer) count of validation milestones defined -- "
        "count M# headings in the roadmap\n"
        "- work_milestones: (integer) count of implementation work milestones -- "
        "count M# headings in the roadmap\n"
        "- interleave_ratio: (string) test-to-implementation ratio, determined by complexity_class:\n"
        "  LOW → 1:3 (one validation milestone per three work milestones)\n"
        "  MEDIUM → 1:2 (one validation milestone per two work milestones)\n"
        "  HIGH → 1:1 (one validation milestone per work milestone)\n"
        "- major_issue_policy: (string) MUST be exactly 'stop-and-fix' -- "
        "major issues halt progress until resolved\n\n"
        "## Issue Classification\n\n"
        "Classify issues found during validation as:\n"
        "| Severity | Action | Gate Impact |\n"
        "|----------|--------|-------------|\n"
        "| CRITICAL | stop-and-fix immediately | Blocks current milestone |\n"
        "| MAJOR | stop-and-fix before next milestone | Blocks next milestone |\n"
        "| MINOR | Track and fix in next sprint | No gate impact |\n"
        "| COSMETIC | Backlog | No gate impact |\n\n"
        "After the frontmatter, provide:\n"
        "1. Validation milestones mapped to roadmap milestones\n"
        "2. Test categories (unit, integration, E2E, acceptance)\n"
        "3. Test-implementation interleaving strategy with ratio justification\n"
        "4. Risk-based test prioritization\n"
        "5. Acceptance criteria per milestone\n"
        "6. Quality gates between milestones\n\n"
        "Be specific about what to test at each milestone."
    )

    if tdd_file is not None:
        base += (
            "\n\n## Supplementary TDD Context (when TDD file is provided)\n\n"
            "A Technical Design Document (TDD) is included in the inputs alongside "
            "the roadmap and extraction. Use TDD content to enrich the test strategy:\n"
            "1. **Test pyramid alignment**: Use the TDD's Testing Strategy section (§15) "
            "to set coverage targets per level (unit, integration, E2E) and adopt the "
            "TDD's specified tooling and test runner configuration.\n"
            "2. **Named test cases**: Incorporate specific test cases from the TDD's "
            "test case tables (§15) into the strategy with their exact names, inputs, "
            "expected outputs, and mock requirements.\n"
            "3. **API contract tests**: Use the TDD's API Specifications (§8) to define "
            "per-endpoint contract tests validating request/response schemas, error codes, "
            "auth requirements, and rate limits.\n"
            "4. **Data model validation**: Use the TDD's Data Models (§7) to define "
            "schema validation tests for entity field types, constraints, and relationships.\n"
            "5. **Migration rollback tests**: Use the TDD's Migration and Rollout Plan "
            "(§19) to define rollback verification tests for each migration phase.\n"
            "6. **Operational readiness tests**: Use the TDD's Operational Readiness "
            "section (§25) to define monitoring, alerting, and runbook validation tests.\n"
            "Preserve exact test case IDs and names from the TDD."
        )

    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Context (when PRD file is provided)\n\n"
            "A Product Requirements Document (PRD) is included in the inputs alongside "
            "the roadmap and extraction. Use PRD content to enrich the test strategy:\n"
            "1. **Persona-based acceptance tests**: For each user persona in the PRD "
            "(S7), define at least one acceptance test scenario that validates their "
            "primary workflow.\n"
            "2. **Customer journey E2E tests**: Map the PRD's Customer Journey Map "
            "(S22) to end-to-end test flows covering the critical path for each journey.\n"
            "3. **KPI validation tests**: For each success metric in the PRD (S19), "
            "define a validation test that measures or proxies the metric.\n"
            "4. **Compliance test category**: If the PRD's Legal & Compliance section "
            "(S17) defines regulatory requirements, add a dedicated compliance test "
            "category with specific test cases.\n"
            "5. **Edge case coverage**: Reference the PRD's Error Handling & Edge Cases "
            "section (S23) to ensure negative test scenarios are included."
        )

    return base + _OUTPUT_FORMAT_BLOCK
