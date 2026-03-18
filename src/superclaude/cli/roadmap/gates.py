"""Roadmap gate criteria -- data definitions for each pipeline step's gate.

This module defines GateCriteria instances as module-level constants.
Gate criteria are pure data -- no logic, no imports from pipeline/gates.py
enforcement code (NFR-005).

Semantic check functions are defined here as pure functions accepting
file content and returning bool. They are registered on the STRICT-tier
GateCriteria instances.
"""

from __future__ import annotations

from ..pipeline.models import GateCriteria, SemanticCheck


# --- Semantic check functions (pure: content -> bool) ---


def _no_heading_gaps(content: str) -> bool:
    """Verify heading levels increment by at most 1 (no H2 -> H4 skip)."""
    prev_level = 0
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#"):
            level = 0
            for ch in stripped:
                if ch == "#":
                    level += 1
                else:
                    break
            if prev_level > 0 and level > prev_level + 1:
                return False
            prev_level = level
    return True


def _cross_refs_resolve(content: str) -> bool:
    """Verify all 'See section' / cross-reference patterns have matching headings.

    Checks that internal references like 'See section X.Y' or 'See X.Y'
    have corresponding headings. Unresolved references emit warnings but
    do not block the pipeline (warning-only mode per OQ-001 for v2.20).
    """
    import re
    import warnings

    # Extract heading anchors (simplified: heading text, lowercased)
    headings: set[str] = set()
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#"):
            heading_text = stripped.lstrip("#").strip().lower()
            headings.add(heading_text)

    # Find cross-references like "See section X" or "(see X.Y)"
    refs = re.findall(r'[Ss]ee\s+(?:[Ss]ection\s+)?["\']?(\d+(?:\.\d+)*)', content)
    # If there are no cross-references, that's fine
    if not refs:
        return True

    # Check each reference against headings
    unresolved: list[str] = []
    for ref in refs:
        found = any(ref in h for h in headings)
        if not found:
            # Also check if the section number appears as a heading prefix
            found = any(h.startswith(ref) for h in headings)
        if not found:
            unresolved.append(ref)

    if unresolved:
        for ref in unresolved:
            warnings.warn(
                f"Unresolved cross-reference: 'See section {ref}' has no matching heading",
                stacklevel=2,
            )
        # Warning-only mode (OQ-001): return True to avoid blocking pipeline
        return True

    return True


def _no_duplicate_headings(content: str) -> bool:
    """No duplicate H2 or H3 heading text."""
    seen: dict[int, set[str]] = {2: set(), 3: set()}
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            text = stripped[3:].strip().lower()
            if text in seen[2]:
                return False
            seen[2].add(text)
        elif stripped.startswith("### "):
            text = stripped[4:].strip().lower()
            if text in seen[3]:
                return False
            seen[3].add(text)
    return True


def _frontmatter_values_non_empty(content: str) -> bool:
    """All YAML frontmatter fields have non-empty values."""
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return False

    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return False

    frontmatter_text = rest[:end_idx]
    for line in frontmatter_text.splitlines():
        line = line.strip()
        if ":" in line:
            _key, value = line.split(":", 1)
            if not value.strip():
                return False
    return True


def _has_actionable_content(content: str) -> bool:
    """At least one section contains numbered or bulleted items."""
    import re

    # Look for markdown list items: "- ", "* ", "1. ", "2. ", etc.
    return bool(re.search(r"^\s*(?:[-*]|\d+\.)\s+\S", content, re.MULTILINE))


def _parse_frontmatter(content: str) -> dict[str, str] | None:
    """Extract YAML frontmatter key-value pairs from content.

    Returns a dict of key→value strings, or None if no frontmatter found.
    """
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return None

    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return None

    result: dict[str, str] = {}
    for line in rest[:end_idx].splitlines():
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def _high_severity_count_zero(content: str) -> bool:
    """Validate that high_severity_count equals zero in fidelity report frontmatter.

    Returns True only if the frontmatter contains high_severity_count with
    integer value 0. Returns False if:
    - Frontmatter is missing
    - high_severity_count field is missing
    - high_severity_count > 0

    Raises TypeError if high_severity_count value is not parseable as an integer.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("high_severity_count")
    if value is None:
        return False

    try:
        count = int(value)
    except (ValueError, TypeError):
        raise TypeError(f"high_severity_count must be an integer, got: {value!r}")

    return count == 0


def _has_per_finding_table(content: str) -> bool:
    """Verify the certification report contains a per-finding results table.

    Checks for a markdown table with the required columns:
    Finding | Severity | Result | Justification
    """
    import re

    # Look for the table header row with required columns
    has_header = bool(
        re.search(
            r"\|\s*Finding\s*\|\s*Severity\s*\|\s*Result\s*\|\s*Justification\s*\|",
            content,
            re.IGNORECASE,
        )
    )
    # Also check for at least one data row (| F-XX | ... |)
    has_data = bool(
        re.search(
            r"\|\s*F-\d+\s*\|",
            content,
        )
    )
    return has_header and has_data


def _all_actionable_have_status(content: str) -> bool:
    """Verify all non-SKIPPED entries in remediation tasklist have FIXED or FAILED status.

    Scans for checklist entries matching `- [ ] F-XX | file | STATUS -- desc`
    and ensures STATUS is one of FIXED or FAILED (not PENDING).
    SKIPPED entries (marked `- [x]`) are excluded from the check.

    Returns True if all actionable entries have terminal status, or if there
    are no actionable entries. Returns False if any PENDING entry is found.
    """
    import re

    # Match actionable (unchecked) entries: - [ ] F-XX | file | STATUS -- desc
    actionable_pattern = re.compile(
        r"^-\s+\[ \]\s+F-\d+\s*\|[^|]*\|\s*(\w+)\s*--",
        re.MULTILINE,
    )
    for match in actionable_pattern.finditer(content):
        status = match.group(1).upper()
        if status not in ("FIXED", "FAILED"):
            return False
    return True


def _tasklist_ready_consistent(content: str) -> bool:
    """Validate tasklist_ready is consistent with severity counts.

    Consistency rule: tasklist_ready=true requires high_severity_count=0
    AND validation_complete=true. If tasklist_ready=true but either
    condition fails, this returns False (inconsistency detected).

    Returns False if:
    - Frontmatter is missing
    - tasklist_ready field is missing
    - Inconsistency: tasklist_ready=true but high_severity_count > 0
    - Inconsistency: tasklist_ready=true but validation_complete != true
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    tasklist_ready_str = fm.get("tasklist_ready")
    if tasklist_ready_str is None:
        return False

    tasklist_ready = tasklist_ready_str.lower() == "true"

    if not tasklist_ready:
        # If tasklist_ready is false, that's always consistent
        return True

    # tasklist_ready is true -- verify consistency
    high_str = fm.get("high_severity_count")
    if high_str is None:
        return False
    try:
        high_count = int(high_str)
    except (ValueError, TypeError):
        return False

    if high_count > 0:
        return False

    validation_str = fm.get("validation_complete")
    if validation_str is None:
        return False
    if validation_str.lower() != "true":
        return False

    return True


def _convergence_score_valid(content: str) -> bool:
    """convergence_score frontmatter value parses as float in [0.0, 1.0]."""
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return False

    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return False

    frontmatter_text = rest[:end_idx]
    for line in frontmatter_text.splitlines():
        line = line.strip()
        if line.startswith("convergence_score:"):
            value = line.split(":", 1)[1].strip()
            try:
                score = float(value)
                return 0.0 <= score <= 1.0
            except ValueError:
                return False
    return False  # convergence_score field not found


# --- DEVIATION_ANALYSIS_GATE semantic check functions ---


def _no_ambiguous_deviations(content: str) -> bool:
    """Fail-closed: ambiguous_deviations must equal 0.

    Returns True only if frontmatter contains ambiguous_deviations: 0.
    Returns False for:
    - Missing frontmatter
    - Missing ambiguous_deviations field
    - Non-integer value (fail-closed, no exception raised)
    - Value > 0
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("ambiguous_deviations")
    if value is None:
        return False

    try:
        count = int(value)
    except (ValueError, TypeError):
        return False

    return count == 0


def _certified_is_true(content: str) -> bool:
    """certified frontmatter field must equal boolean true (case-insensitive).

    Accepts: 'true', 'True', 'TRUE'.
    Rejects: 'false', 'yes', '1', empty, missing, no frontmatter.
    Fail-closed: any non-true value returns False.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("certified")
    if value is None:
        return False

    return value.lower() == "true"


def _validation_complete_true(content: str) -> bool:
    """analysis_complete frontmatter field must equal true.

    Returns True only if frontmatter has analysis_complete: true.
    Returns False for missing field, missing frontmatter, or false value.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("analysis_complete")
    if value is None:
        return False

    return value.lower() == "true"


def _routing_ids_valid(content: str) -> bool:
    """All routing IDs in deviation-analysis must match DEV-\\d+ pattern.

    Checks routing_fix_roadmap, routing_update_spec, routing_no_action,
    routing_human_review fields. Empty values are valid (no IDs routed there).
    Returns False if any ID does not match DEV-\\d+.
    Returns True if all routing fields are absent or contain only valid IDs.
    """
    import re

    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    routing_fields = [
        "routing_fix_roadmap",
        "routing_update_spec",
        "routing_no_action",
        "routing_human_review",
    ]
    id_pattern = re.compile(r"^DEV-\d+$")

    for field in routing_fields:
        raw = fm.get(field, "")
        if not raw:
            continue
        for token in re.split(r"[\s,]+", raw):
            token = token.strip()
            if not token:
                continue
            if not id_pattern.match(token):
                return False

    return True


def _slip_count_matches_routing(content: str) -> bool:
    """slip_count must equal the number of IDs in routing_fix_roadmap.

    Returns False if:
    - Frontmatter missing
    - slip_count field missing or non-integer
    - routing_fix_roadmap field count != slip_count
    Returns True when counts match (including both == 0).
    """
    import re

    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    slip_str = fm.get("slip_count")
    if slip_str is None:
        return False

    try:
        slip_count = int(slip_str)
    except (ValueError, TypeError):
        return False

    routing_raw = fm.get("routing_fix_roadmap", "")
    if not routing_raw:
        routing_ids = []
    else:
        routing_ids = [t.strip() for t in re.split(r"[\s,]+", routing_raw) if t.strip()]

    return slip_count == len(routing_ids)


def _routing_consistent_with_slip_count(content: str) -> bool:
    """Alias for _slip_count_matches_routing for gate naming consistency."""
    return _slip_count_matches_routing(content)


def _pre_approved_not_in_fix_roadmap(content: str) -> bool:
    """IDs in routing_no_action (pre-approved) must not appear in routing_fix_roadmap.

    Returns False if any ID appears in both routing_no_action and routing_fix_roadmap.
    Returns True if no overlap, or if either field is empty.
    """
    import re

    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    def parse_ids(raw: str) -> set[str]:
        if not raw:
            return set()
        return {t.strip() for t in re.split(r"[\s,]+", raw) if t.strip()}

    no_action = parse_ids(fm.get("routing_no_action", ""))
    fix_roadmap = parse_ids(fm.get("routing_fix_roadmap", ""))

    return len(no_action & fix_roadmap) == 0


def _total_analyzed_consistent(content: str) -> bool:
    """total_analyzed must equal sum of slip_count + intentional_count + pre_approved_count + ambiguous_count.

    Returns False if:
    - Frontmatter missing
    - total_analyzed or any count field missing
    - Any count is non-integer (fail-closed)
    - Sum does not match total_analyzed
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    fields = [
        "total_analyzed",
        "slip_count",
        "intentional_count",
        "pre_approved_count",
        "ambiguous_count",
    ]
    values: dict[str, int] = {}
    for f in fields:
        raw = fm.get(f)
        if raw is None:
            return False
        try:
            values[f] = int(raw)
        except (ValueError, TypeError):
            return False

    expected_total = (
        values["slip_count"]
        + values["intentional_count"]
        + values["pre_approved_count"]
        + values["ambiguous_count"]
    )
    return values["total_analyzed"] == expected_total


def _total_annotated_consistent(content: str) -> bool:
    """total_annotated (if present) must equal slip_count + intentional_count + pre_approved_count.

    The total_annotated field sums the three classified (non-ambiguous) deviations.
    Returns True if field is absent (optional field).
    Returns False if present but doesn't match the sum.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    total_str = fm.get("total_annotated")
    if total_str is None:
        return True  # Optional field; absence is valid

    try:
        total_annotated = int(total_str)
    except (ValueError, TypeError):
        return False

    component_fields = ["slip_count", "intentional_count", "pre_approved_count"]
    total_components = 0
    for f in component_fields:
        raw = fm.get(f)
        if raw is None:
            return False
        try:
            total_components += int(raw)
        except (ValueError, TypeError):
            return False

    return total_annotated == total_components


def _complexity_class_valid(content: str) -> bool:
    """Validate complexity_class is one of LOW, MEDIUM, HIGH (case-insensitive)."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("complexity_class")
    if value is None:
        return False

    return value.strip().upper() in ("LOW", "MEDIUM", "HIGH")


def _extraction_mode_valid(content: str) -> bool:
    """Validate extraction_mode is 'standard' or starts with 'chunked' (case-insensitive).

    Accepts: 'standard', 'chunked', 'chunked (3 chunks)', etc.
    Rejects: 'full', 'partial', 'incremental'.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("extraction_mode")
    if value is None:
        return False

    normalized = value.strip().lower()
    return normalized == "standard" or normalized.startswith("chunked")


def _interleave_ratio_consistent(content: str) -> bool:
    """Validate interleave_ratio is consistent with complexity_class.

    Required mapping: LOW→1:3, MEDIUM→1:2, HIGH→1:1.
    Rejects mismatches like LOW+1:1 or HIGH+1:3.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    complexity = fm.get("complexity_class")
    ratio = fm.get("interleave_ratio")
    if complexity is None or ratio is None:
        return False

    expected = {
        "LOW": "1:3",
        "MEDIUM": "1:2",
        "HIGH": "1:1",
    }
    normalized_complexity = complexity.strip().upper()
    expected_ratio = expected.get(normalized_complexity)
    if expected_ratio is None:
        return False

    return ratio.strip() == expected_ratio


def _milestone_counts_positive(content: str) -> bool:
    """Validate validation_milestones and work_milestones are positive integers."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    for field in ("validation_milestones", "work_milestones"):
        value = fm.get(field)
        if value is None:
            return False
        try:
            count = int(value)
        except (ValueError, TypeError):
            return False
        if count <= 0:
            return False

    return True


def _validation_philosophy_correct(content: str) -> bool:
    """Validate validation_philosophy is exactly 'continuous-parallel' (hyphenated).

    Rejects: 'continuous_parallel' (underscore), 'continuous parallel' (space).
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("validation_philosophy")
    if value is None:
        return False

    return value.strip() == "continuous-parallel"


def _major_issue_policy_correct(content: str) -> bool:
    """Validate major_issue_policy is exactly 'stop-and-fix'."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("major_issue_policy")
    if value is None:
        return False

    return value.strip() == "stop-and-fix"


# --- GateCriteria instances ---

EXTRACT_GATE = GateCriteria(
    required_frontmatter_fields=[
        "spec_source",
        "generated",
        "generator",
        "functional_requirements",
        "nonfunctional_requirements",
        "total_requirements",
        "complexity_score",
        "complexity_class",
        "domains_detected",
        "risks_identified",
        "dependencies_identified",
        "success_criteria_count",
        "extraction_mode",
    ],
    min_lines=50,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="complexity_class_valid",
            check_fn=_complexity_class_valid,
            failure_message="complexity_class must be one of LOW, MEDIUM, HIGH",
        ),
        SemanticCheck(
            name="extraction_mode_valid",
            check_fn=_extraction_mode_valid,
            failure_message="extraction_mode must be 'standard' or start with 'chunked'",
        ),
    ],
)

GENERATE_A_GATE = GateCriteria(
    required_frontmatter_fields=["spec_source", "complexity_score", "primary_persona"],
    min_lines=100,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="frontmatter_values_non_empty",
            check_fn=_frontmatter_values_non_empty,
            failure_message="One or more required frontmatter fields have empty values",
        ),
        SemanticCheck(
            name="has_actionable_content",
            check_fn=_has_actionable_content,
            failure_message="No numbered or bulleted items found -- roadmap must contain actionable content",
        ),
    ],
)

GENERATE_B_GATE = GateCriteria(
    required_frontmatter_fields=["spec_source", "complexity_score", "primary_persona"],
    min_lines=100,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="frontmatter_values_non_empty",
            check_fn=_frontmatter_values_non_empty,
            failure_message="One or more required frontmatter fields have empty values",
        ),
        SemanticCheck(
            name="has_actionable_content",
            check_fn=_has_actionable_content,
            failure_message="No numbered or bulleted items found -- roadmap must contain actionable content",
        ),
    ],
)

DIFF_GATE = GateCriteria(
    required_frontmatter_fields=["total_diff_points", "shared_assumptions_count"],
    min_lines=30,
    enforcement_tier="STANDARD",
)

DEBATE_GATE = GateCriteria(
    required_frontmatter_fields=["convergence_score", "rounds_completed"],
    min_lines=50,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="convergence_score_valid",
            check_fn=_convergence_score_valid,
            failure_message="convergence_score must be a float in [0.0, 1.0]",
        ),
    ],
)

SCORE_GATE = GateCriteria(
    required_frontmatter_fields=["base_variant", "variant_scores"],
    min_lines=20,
    enforcement_tier="STANDARD",
)

MERGE_GATE = GateCriteria(
    required_frontmatter_fields=["spec_source", "complexity_score", "adversarial"],
    min_lines=150,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="no_heading_gaps",
            check_fn=_no_heading_gaps,
            failure_message="Heading level gap detected (e.g. H2 -> H4 without H3)",
        ),
        SemanticCheck(
            name="cross_refs_resolve",
            check_fn=_cross_refs_resolve,
            failure_message="Internal cross-reference does not resolve to an existing heading",
        ),
        SemanticCheck(
            name="no_duplicate_headings",
            check_fn=_no_duplicate_headings,
            failure_message="Duplicate H2 or H3 heading text detected",
        ),
    ],
)

TEST_STRATEGY_GATE = GateCriteria(
    required_frontmatter_fields=[
        "spec_source",
        "generated",
        "generator",
        "complexity_class",
        "validation_philosophy",
        "validation_milestones",
        "work_milestones",
        "interleave_ratio",
        "major_issue_policy",
    ],
    min_lines=40,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="complexity_class_valid",
            check_fn=_complexity_class_valid,
            failure_message="complexity_class must be one of LOW, MEDIUM, HIGH",
        ),
        SemanticCheck(
            name="interleave_ratio_consistent",
            check_fn=_interleave_ratio_consistent,
            failure_message="interleave_ratio must match complexity_class: LOW→1:3, MEDIUM→1:2, HIGH→1:1",
        ),
        SemanticCheck(
            name="milestone_counts_positive",
            check_fn=_milestone_counts_positive,
            failure_message="validation_milestones and work_milestones must be positive integers",
        ),
        SemanticCheck(
            name="validation_philosophy_correct",
            check_fn=_validation_philosophy_correct,
            failure_message="validation_philosophy must be exactly 'continuous-parallel' (hyphenated)",
        ),
        SemanticCheck(
            name="major_issue_policy_correct",
            check_fn=_major_issue_policy_correct,
            failure_message="major_issue_policy must be exactly 'stop-and-fix'",
        ),
    ],
)

SPEC_FIDELITY_GATE = GateCriteria(
    required_frontmatter_fields=[
        "high_severity_count",
        "medium_severity_count",
        "low_severity_count",
        "total_deviations",
        "validation_complete",
        "tasklist_ready",
    ],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="high_severity_count_zero",
            check_fn=_high_severity_count_zero,
            failure_message="high_severity_count must be 0 for spec-fidelity gate to pass",
        ),
        SemanticCheck(
            name="tasklist_ready_consistent",
            check_fn=_tasklist_ready_consistent,
            failure_message="tasklist_ready is inconsistent with severity counts or validation_complete",
        ),
    ],
)

REMEDIATE_GATE = GateCriteria(
    required_frontmatter_fields=[
        "type",
        "source_report",
        "source_report_hash",
        "total_findings",
        "actionable",
        "skipped",
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="frontmatter_values_non_empty",
            check_fn=_frontmatter_values_non_empty,
            failure_message="One or more required frontmatter fields have empty values",
        ),
        SemanticCheck(
            name="all_actionable_have_status",
            check_fn=_all_actionable_have_status,
            failure_message="Not all actionable findings have FIXED or FAILED status",
        ),
    ],
)

CERTIFY_GATE = GateCriteria(
    required_frontmatter_fields=[
        "findings_verified",
        "findings_passed",
        "findings_failed",
        "certified",
        "certification_date",
    ],
    min_lines=15,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="frontmatter_values_non_empty",
            check_fn=_frontmatter_values_non_empty,
            failure_message="One or more required frontmatter fields have empty values",
        ),
        SemanticCheck(
            name="per_finding_table_present",
            check_fn=_has_per_finding_table,
            failure_message="Certification report missing per-finding results table",
        ),
        SemanticCheck(
            name="certified_is_true",
            check_fn=_certified_is_true,
            failure_message="certified field must be true for certification gate to pass",
        ),
    ],
)

DEVIATION_ANALYSIS_GATE = GateCriteria(
    required_frontmatter_fields=[
        "schema_version",
        "total_analyzed",
        "slip_count",
        "intentional_count",
        "pre_approved_count",
        "ambiguous_count",
        "routing_fix_roadmap",
        "routing_no_action",
        "analysis_complete",
    ],
    min_lines=20,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="no_ambiguous_deviations",
            check_fn=_no_ambiguous_deviations,
            failure_message="ambiguous_deviations must be 0; ambiguous items require human review before pipeline can continue",
        ),
        SemanticCheck(
            name="validation_complete_true",
            check_fn=_validation_complete_true,
            failure_message="analysis_complete must be true for deviation analysis gate to pass",
        ),
        SemanticCheck(
            name="routing_ids_valid",
            check_fn=_routing_ids_valid,
            failure_message="All routing IDs must match DEV-\\d+ pattern",
        ),
        SemanticCheck(
            name="slip_count_matches_routing",
            check_fn=_slip_count_matches_routing,
            failure_message="slip_count must equal the number of IDs in routing_fix_roadmap",
        ),
        SemanticCheck(
            name="pre_approved_not_in_fix_roadmap",
            check_fn=_pre_approved_not_in_fix_roadmap,
            failure_message="Pre-approved IDs (routing_no_action) must not appear in routing_fix_roadmap",
        ),
        SemanticCheck(
            name="total_analyzed_consistent",
            check_fn=_total_analyzed_consistent,
            failure_message="total_analyzed must equal slip_count + intentional_count + pre_approved_count + ambiguous_count",
        ),
    ],
)

# All gates in pipeline order for reference
ALL_GATES = [
    ("extract", EXTRACT_GATE),
    ("generate-A", GENERATE_A_GATE),
    ("generate-B", GENERATE_B_GATE),
    ("diff", DIFF_GATE),
    ("debate", DEBATE_GATE),
    ("score", SCORE_GATE),
    ("merge", MERGE_GATE),
    ("test-strategy", TEST_STRATEGY_GATE),
    ("spec-fidelity", SPEC_FIDELITY_GATE),
    ("deviation-analysis", DEVIATION_ANALYSIS_GATE),
    ("remediate", REMEDIATE_GATE),
    ("certify", CERTIFY_GATE),
]
