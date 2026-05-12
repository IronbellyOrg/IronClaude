"""Validation prompt builders -- pure functions returning prompt strings.

All functions are pure: they accept concrete values, return ``str``,
and perform no I/O, subprocess calls, or side effects (NFR-004).

Prompt templates for the validate pipeline:
- ``build_reflect_prompt``: single-agent reflection across 7 validation dimensions
- ``build_merge_prompt``: adversarial merge with agreement categorization
"""

from __future__ import annotations

from .prompts import _OUTPUT_FORMAT_BLOCK


def build_reflect_prompt(
    roadmap: str,
    test_strategy: str,
    extraction: str,
    *,
    spec_file: str | None = None,
    tdd_file: str | None = None,
    prd_file: str | None = None,
) -> str:
    """Prompt for the 'reflect' validation step.

    Instructs Claude to validate pipeline outputs across validation dimensions
    with BLOCKING/WARNING severity classifications.  Returns a structured
    report with YAML frontmatter matching REFLECT_GATE criteria.

    When original input files (spec, TDD, PRD) are provided, two additional
    BLOCKING dimensions are added: Coverage and Proportionality.  These
    compare the roadmap output against the actual input — not just against
    the extraction (which is itself a lossy intermediary).

    Parameters
    ----------
    roadmap:
        Path (as string) to the merged roadmap file.
    test_strategy:
        Path (as string) to the test-strategy file.
    extraction:
        Path (as string) to the extraction file.
    spec_file:
        Path (as string) to the original spec file, or None.
    tdd_file:
        Path (as string) to the original TDD file, or None.
    prd_file:
        Path (as string) to the original PRD file, or None.
    """
    has_inputs = any(f is not None for f in (spec_file, tdd_file, prd_file))
    dim_count = 9 if has_inputs else 7

    base = (
        "You are a validation specialist. You did NOT generate these artifacts.\n\n"
        "Read the provided roadmap, test-strategy, and extraction documents. "
    )
    if has_inputs:
        input_names = [n for n, f in (("spec", spec_file), ("TDD", tdd_file), ("PRD", prd_file)) if f]
        base += (
            f"You are ALSO provided with the original input document(s): "
            f"{', '.join(input_names)}. "
            "These are the PRIMARY source of truth — the extraction is a lossy "
            "intermediary. Compare the roadmap against the ORIGINAL input, not "
            "just the extraction.\n\n"
        )
    base += (
        f"Validate the roadmap across the {dim_count} dimensions listed below. "
        "Be thorough but precise -- false positives waste user time. "
        "Every finding must cite a specific location (file:line or file:section).\n\n"
        "## Validation Dimensions\n\n"
        "Each finding MUST be classified as BLOCKING, WARNING, or INFO.\n\n"
        "### BLOCKING Dimensions (failure = roadmap not ready for tasklist generation)\n\n"
        "1. **Schema** -- YAML frontmatter fields present, non-empty, correctly typed.\n"
        "2. **Structure** -- Milestone DAG acyclic, all refs resolve, no duplicate "
        "deliverable IDs, heading hierarchy valid (H2 > H3 > H4, no gaps).\n"
        "3. **Traceability** -- Every deliverable traces to a requirement AND every "
        "requirement traces to a deliverable. Report untraced items.\n"
        "4. **Cross-file consistency** -- test-strategy milestone refs match roadmap "
        "milestones exactly. No dangling references in either direction.\n"
        "5. **Parseability** -- Content is parseable into actionable items via "
        "headings, bullets, and numbered lists by sc:tasklist's splitter.\n"
    )

    if has_inputs:
        base += (
            "6. **Coverage** -- Compare the roadmap task rows against the original "
            "input document(s). Every requirement (FR-xxx, NFR-xxx) and every entity "
            "(DM-xxx, API-xxx, COMP-xxx, TEST-xxx, MIG-xxx, OPS-xxx) in the input "
            "MUST have a corresponding task row in the roadmap. Report any input "
            "requirements or entities that have NO matching roadmap task. "
            "This is a BLOCKING dimension — missing coverage means the roadmap "
            "is incomplete.\n"
            "7. **Proportionality** -- The number of roadmap task rows must be "
            "proportional to the input detail level. Count entities in the input "
            "document(s) and compare to the number of task rows in the roadmap. "
            "A TDD with 1,200+ lines should produce significantly more task rows "
            "than a 300-line spec. If the roadmap has fewer task rows than the "
            "input has distinct entities, flag as BLOCKING. Report the ratio: "
            "input_entity_count / roadmap_task_rows.\n\n"
            "### WARNING Dimensions (non-blocking but worth reporting)\n\n"
            "8. **Interleave** -- Compute interleave_ratio using this formula:\n"
        )
    else:
        base += (
            "\n### WARNING Dimensions (non-blocking but worth reporting)\n\n"
            "6. **Interleave** -- Compute interleave_ratio using this formula:\n"
        )

    base += (
        "   `interleave_ratio = unique_milestones_with_deliverables / total_milestones`\n"
        "   (initial, subject to refinement)\n"
        "   Ratio must be in [0.1, 1.0]. Test activities must not be back-loaded "
        "(i.e., concentrated only in the final milestone).\n"
    )

    if has_inputs:
        base += (
            "9. **Decomposition** -- Flag compound deliverables that would need splitting "
        )
    else:
        base += (
            "7. **Decomposition** -- Flag compound deliverables that would need splitting "
        )
    base += (
        "by sc:tasklist. A deliverable is compound if it describes multiple distinct "
        "outputs or actions joined by 'and'/'or'.\n\n"
        "## Output Format\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- blocking_issues_count: (integer) total number of BLOCKING findings\n"
        "- warnings_count: (integer) total number of WARNING findings\n"
        "- tasklist_ready: (boolean) true ONLY if blocking_issues_count == 0\n\n"
        "After the frontmatter, provide:\n\n"
        "## Findings\n\n"
        "For each finding, provide:\n"
        "- **[BLOCKING|WARNING|INFO]** Dimension name: Description\n"
        "  - Location: file:line or file:section\n"
        "  - Evidence: what was expected vs. what was found\n"
        "  - Fix guidance: concrete steps to resolve\n\n"
        "## Summary\n\n"
        "Total counts by severity and overall assessment.\n\n"
        "## Interleave Ratio\n\n"
        "Show the computed interleave_ratio with the formula and values used."
    )

    return base + _OUTPUT_FORMAT_BLOCK


def build_merge_prompt(reflect_reports: list[str]) -> str:
    """Prompt for the 'adversarial-merge' validation step.

    Instructs Claude to merge multiple agent reflection reports into a
    single consolidated validation report with agreement categorization.

    Parameters
    ----------
    reflect_reports:
        List of paths (as strings) to individual agent reflection reports.
    """
    agent_count = len(reflect_reports)
    return (
        "You are an adversarial merge specialist consolidating validation reports.\n\n"
        f"Read the {agent_count} provided reflection reports from independent "
        "validation agents. Merge them into a single consolidated validation report.\n\n"
        "## Merge Categorization\n\n"
        "For each finding across reports, categorize it as:\n\n"
        "- **BOTH_AGREE**: Finding appears in both/all reports with consistent severity. "
        "High confidence -- include in final report as-is.\n"
        "- **ONLY_A**: Finding appears only in Agent A's report. "
        "Review recommended -- may be a true positive missed by other agents, "
        "or a false positive.\n"
        "- **ONLY_B**: Finding appears only in Agent B's report. "
        "Review recommended -- likely structural difference in analysis approach.\n"
        "- **CONFLICT**: Finding appears in multiple reports but with different "
        "severity classifications. Escalate to BLOCKING.\n\n"
        "## Agreement Table\n\n"
        "Produce a markdown table with columns:\n"
        "| Finding ID | Agent A | Agent B | Agreement Category |\n"
        "|---|---|---|---|\n\n"
        "Where Agent A/B columns show FOUND/-- and the category is one of "
        "BOTH_AGREE, ONLY_A, ONLY_B, CONFLICT.\n\n"
        "## Output Format\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- blocking_issues_count: (integer) total BLOCKING findings after merge\n"
        "- warnings_count: (integer) total WARNING findings after merge\n"
        "- tasklist_ready: (boolean) true ONLY if blocking_issues_count == 0\n"
        "- validation_mode: adversarial\n"
        f"- validation_agents: (string) agent identifiers, e.g. 'agent-1, agent-2'\n\n"
        "After the frontmatter, provide:\n\n"
        "## Agreement Table\n\n"
        "The categorized finding table as described above.\n\n"
        "## Consolidated Findings\n\n"
        "Merged findings list, ordered by severity (BLOCKING first, then WARNING, "
        "then INFO). For CONFLICT items, explain the disagreement and your resolution.\n\n"
        "## Summary\n\n"
        "Total counts by severity, agreement statistics, and overall assessment."
    ) + _OUTPUT_FORMAT_BLOCK
