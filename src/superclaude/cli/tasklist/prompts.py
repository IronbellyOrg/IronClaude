"""Tasklist prompt builders -- pure functions returning prompt strings.

All functions are pure: they accept concrete values, return ``str``,
and perform no I/O, subprocess calls, or side effects (NFR-004).

Validation layering guard: tasklist fidelity checks roadmap→tasklist ONLY.
It does NOT check spec→tasklist (that is the spec-fidelity step's job).
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.roadmap.prompts import _OUTPUT_FORMAT_BLOCK


def build_tasklist_fidelity_prompt(
    roadmap_file: Path,
    tasklist_dir: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for the tasklist-fidelity validation step.

    Instructs Claude to compare the roadmap against the generated tasklist,
    checking deliverable coverage, signature preservation, traceability ID
    validity, and dependency chain correctness.

    VALIDATION LAYERING GUARD: This prompt validates roadmap→tasklist
    alignment ONLY. Spec→tasklist validation is NOT in scope here;
    that is handled by the spec-fidelity step in the roadmap pipeline.

    Embeds explicit severity definitions (HIGH/MEDIUM/LOW) to reduce
    LLM classification drift (RSK-007). Reuses the deviation report
    format from Phase 2 (docs/reference/deviation-report-format.md).
    """
    base = (
        "You are a tasklist fidelity analyst.\n\n"
        "Read the provided roadmap file and the generated tasklist files. "
        "Compare them systematically to identify deviations where the tasklist "
        "diverges from or omits requirements in the roadmap.\n\n"
        "## VALIDATION LAYERING GUARD\n\n"
        "IMPORTANT: You are validating ROADMAP → TASKLIST alignment ONLY.\n"
        "Do NOT compare the tasklist against the original specification.\n"
        "Do NOT check whether the roadmap itself is faithful to the spec.\n"
        "Those checks are handled by a separate spec-fidelity step.\n"
        "Your SOLE concern is whether the tasklist accurately reflects the roadmap.\n\n"
        "## Severity Definitions\n\n"
        "Apply these severity classifications precisely:\n\n"
        "**HIGH**: The tasklist omits, contradicts, or fundamentally misrepresents "
        "a roadmap item. The tasklist cannot be used as-is for execution. Examples:\n"
        "- A roadmap item (R-NNN) has no corresponding task in the tasklist\n"
        "- A deliverable ID (D-NNNN) appears in the tasklist but does not exist "
        "in the roadmap (fabricated traceability)\n"
        "- A dependency chain in the tasklist contradicts the roadmap's ordering\n"
        "- A task's deliverables omit outputs specified in the roadmap item\n\n"
        "**MEDIUM**: The tasklist addresses the roadmap item but with insufficient "
        "detail, ambiguous language, or minor misalignment that could lead to "
        "execution issues. Examples:\n"
        "- A task's effort estimate diverges significantly from the roadmap\n"
        "- Acceptance criteria are weaker than the roadmap's success criteria\n"
        "- A dependency is acknowledged but not properly sequenced\n"
        "- Verification method differs from roadmap recommendation\n\n"
        "**LOW**: Minor stylistic, formatting, or organizational differences that "
        "do not affect execution correctness. Examples:\n"
        "- Different heading structure or section ordering\n"
        "- Terminology variations that don't change meaning\n"
        "- Missing cross-references that don't affect understanding\n\n"
        "## Comparison Dimensions\n\n"
        "Compare across ALL of these dimensions:\n"
        "1. **Deliverable Coverage**: Every roadmap deliverable (D-NNNN) has a "
        "corresponding task with matching deliverable IDs\n"
        "2. **Signature Preservation**: Function/method/API signatures from the "
        "roadmap are preserved in task descriptions and acceptance criteria\n"
        "3. **Traceability ID Validity**: Every Roadmap Item ID (R-NNN) and "
        "Deliverable ID (D-NNNN) in the tasklist traces back to the roadmap. "
        "Flag fabricated IDs that do not exist in the roadmap.\n"
        "4. **Dependency Chain Correctness**: Task dependencies match the "
        "roadmap's sequencing and prerequisites\n"
        "5. **Acceptance Criteria Completeness**: Task acceptance criteria "
        "cover all success criteria from the corresponding roadmap items\n\n"
        "## Output Requirements\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- source_pair: roadmap-to-tasklist\n"
        "- upstream_file: (string) the roadmap filename\n"
        "- downstream_file: (string) the tasklist directory path\n"
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
        "- **Upstream Quote**: Verbatim quote from the roadmap\n"
        "- **Downstream Quote**: Verbatim quote from the tasklist, or '[MISSING]' if absent\n"
        "- **Impact**: Assessment of how the deviation affects execution correctness\n"
        "- **Recommended Correction**: Specific action to resolve the deviation\n\n"
        "## Summary\n\n"
        "Provide a brief summary of findings with severity distribution.\n\n"
        "Be thorough and precise. Quote both documents for every deviation. "
        "Do not invent deviations -- only report genuine differences between "
        "the roadmap and tasklist."
    )

    # TDD integration: append supplementary validation when TDD file is provided
    if tdd_file is not None:
        base += (
            "\n\n## Supplementary TDD Validation (when TDD file is provided)\n\n"
            "A Technical Design Document (TDD) is included in the inputs alongside "
            "the roadmap and tasklist. Additionally check:\n"
            "1. Test cases from the TDD's Testing Strategy section (§15) should have "
            "corresponding validation or test tasks in the tasklist.\n"
            "2. Rollback procedures from the TDD's Migration & Rollout Plan section (§19) "
            "should have corresponding contingency or rollback tasks.\n"
            "3. Components listed in the TDD's Component Inventory (§10) should have "
            "corresponding implementation tasks.\n"
            "4. Data model entities from the TDD's Data Models section (§7) should have "
            "corresponding schema implementation tasks in the tasklist.\n"
            "5. API endpoints from the TDD's API Specifications section (§8) should have "
            "corresponding endpoint implementation tasks in the tasklist.\n"
            "Flag missing coverage as MEDIUM severity deviations."
        )

    # PRD integration: append supplementary validation when PRD file is provided
    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Validation (when PRD file is provided)\n\n"
            "A Product Requirements Document (PRD) is included in the inputs alongside "
            "the roadmap and tasklist. Additionally check:\n"
            "1. User persona coverage from the PRD's User Personas section (S7) -- "
            "tasks touching user-facing flows should reference which persona is served.\n"
            "2. Success metrics from the PRD's Success Metrics section (S19) should "
            "have corresponding instrumentation or measurement tasks in the tasklist.\n"
            "3. Acceptance scenarios from the PRD's Scope Definition (S12) and Customer "
            "Journey Map (S22) should have corresponding verification tasks.\n"
            "4. Priority ordering from the PRD's Business Context (S5) -- task priority "
            "should reflect business value hierarchy, not just technical dependency order. "
            "Flag tasks where priority contradicts PRD stakeholder priorities as LOW severity.\n"
            "Flag missing coverage as MEDIUM severity deviations."
        )

    return base + _OUTPUT_FORMAT_BLOCK


def build_tasklist_generate_prompt(
    roadmap_file: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
    """Prompt for tasklist generation enriched with TDD/PRD source documents.

    NOTE: This function is used by the ``/sc:tasklist`` skill protocol for
    inference-based generation workflows. It is NOT currently called by the
    CLI ``tasklist validate`` executor (which only runs fidelity validation).
    There is no ``tasklist generate`` CLI subcommand — generation is handled
    by the skill protocol reading this prompt builder directly.

    When TDD and/or PRD files are provided, the generation prompt includes
    supplementary enrichment blocks that instruct the LLM to use the original
    source documents for richer, more specific task decomposition.

    Without supplementary files, returns a baseline generation prompt that
    works from the roadmap alone (current behavior).
    """
    base = (
        "You are a tasklist generator.\n\n"
        "Read the provided roadmap file and decompose it into a structured "
        "tasklist with individual, actionable tasks. Each roadmap item should "
        "produce one or more tasks with:\n"
        "- A clear task title\n"
        "- Deliverable IDs traced to the roadmap (R-NNN, D-NNNN)\n"
        "- Acceptance criteria\n"
        "- Effort estimate\n"
        "- Dependencies on other tasks\n"
        "- Verification method\n\n"
        "Organize tasks by roadmap phase. Preserve all roadmap item IDs, "
        "deliverable IDs, and dependency chains exactly as specified."
    )

    # TDD enrichment: use original TDD for engineering-specific task detail
    if tdd_file is not None:
        base += (
            "\n\n## Supplementary TDD Enrichment (for task generation)\n\n"
            "A Technical Design Document (TDD) is included alongside the roadmap. "
            "Use it to enrich task decomposition with:\n"
            "1. Specific test cases from S15 Testing Strategy -- each test case should "
            "map to a validation task with exact test name and expected behavior.\n"
            "2. API endpoint schemas from S8 -- each endpoint should have implementation "
            "tasks with request/response field details.\n"
            "3. Component specifications from S10 -- each component should have tasks "
            "with prop types, dependencies, and integration points.\n"
            "4. Migration rollback steps from S19 -- each rollback procedure should be "
            "a contingency task with trigger conditions.\n"
            "5. Data model field definitions from S7 -- each entity should have schema "
            "implementation tasks with exact field types."
        )

    # PRD enrichment: use original PRD for product context in task descriptions
    if prd_file is not None:
        base += (
            "\n\n## Supplementary PRD Enrichment (for task generation)\n\n"
            "A Product Requirements Document (PRD) is included alongside the roadmap. "
            "Use it to enrich task decomposition with:\n"
            "1. User persona context from S7 -- tasks touching user-facing flows should "
            "reference which persona is served and their specific needs.\n"
            "2. Acceptance scenarios from S12 (Scope Definition) and S22 (Customer Journey Map) -- each user story acceptance criterion "
            "should map to a verification task.\n"
            "3. Success metrics from S19 -- tasks should include metric instrumentation "
            "subtasks (tracking, dashboards, alerts) where applicable.\n"
            "4. Stakeholder priorities from S5 -- task priority should reflect business "
            "value ordering, not just technical dependency.\n"
            "5. Scope boundaries from S12 -- tasks must not exceed defined scope; "
            "generate explicit 'out of scope' markers where roadmap milestones approach "
            "scope edges."
        )

    # Combined interaction note when both are provided
    if tdd_file is not None and prd_file is not None:
        base += (
            "\n\n## TDD + PRD Interaction\n\n"
            "When both TDD and PRD are available, TDD provides structural engineering "
            "detail and PRD provides product context. TDD-derived task enrichment "
            "(test cases, schemas, components) takes precedence for implementation "
            "specifics. PRD-derived enrichment (personas, metrics, priorities) shapes "
            "task descriptions, acceptance criteria, and priority ordering."
        )

    return base + _OUTPUT_FORMAT_BLOCK
