"""Roadmap gate criteria -- data definitions for each pipeline step's gate.

This module defines GateCriteria instances as module-level constants.
Gate criteria are pure data -- no logic, no imports from pipeline/gates.py
enforcement code (NFR-005).

Semantic check functions are defined here as pure functions accepting
file content and returning bool. They are registered on the STRICT-tier
GateCriteria instances.
"""

# TDD Compatibility Notes (TASK-RF-20260325-cli-tdd):
# - Provenance gates (EXTRACT, EXTRACT_TDD, GENERATE_A/B, MERGE, TEST_STRATEGY):
#   accept either ``spec_source`` (single-spec scalar) or ``spec_sources``
#   (multi-spec list) via an OR-group alias tuple, matching the template
#   contract in refs/templates.md (exactly one of the two keys must appear).
# - DEVIATION_ANALYSIS_GATE: NOT TDD-compatible — deferred to separate work.
#   Pre-existing bug: ambiguous_count/ambiguous_deviations field mismatch (B-1).
# - ANTI_INSTINCT_GATE: format-agnostic (pure Python).
#   TDD performance hypothesis unverified (I-5).

from __future__ import annotations

from ..audit.wiring_gate import WIRING_GATE
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


def _no_duplicate_headings(content: str) -> bool | str:
    """No duplicate H2 globally; no duplicate H3 within the same H2 section.

    Returns True on pass. Returns a descriptive string on failure (which is
    truthy but not ``True``; the consumer tests ``result is not True``).
    """
    seen_h2: set[str] = set()
    current_h2: str | None = None
    h3_by_section: dict[str | None, set[str]] = {None: set()}

    for lineno, line in enumerate(content.splitlines(), start=1):
        stripped = line.lstrip()

        if stripped.startswith("## ") and not stripped.startswith("### "):
            text = stripped[3:].strip().lower()
            if text in seen_h2:
                return (
                    f"Duplicate H2 heading '## {stripped[3:].strip()}' "
                    f"at line {lineno}"
                )
            seen_h2.add(text)
            current_h2 = text
            h3_by_section.setdefault(current_h2, set())

        elif stripped.startswith("### "):
            text = stripped[4:].strip().lower()
            section_set = h3_by_section.setdefault(current_h2, set())
            if text in section_set:
                parent_label = current_h2 or "(top-level)"
                return (
                    f"Duplicate H3 heading '### {stripped[4:].strip()}' "
                    f"at line {lineno} within section '## {parent_label}'"
                )
            section_set.add(text)

    return True


def _frontmatter_values_non_empty(content: str) -> bool:
    """All YAML frontmatter fields have non-empty values."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    for _key, value in fm.items():
        if not value.strip():
            return False
    return True


def _has_actionable_content(content: str) -> bool:
    """At least one section contains numbered or bulleted items."""
    import re

    # Look for markdown list items: "- ", "* ", "1. ", "2. ", etc.
    return bool(re.search(r"^\s*(?:[-*]|\d+\.)\s+\S", content, re.MULTILINE))


def _strip_yaml_quotes(value: str) -> str:
    """Strip matching outer YAML quotes (single or double) from a value.

    Handles the common case where LLMs wrap values in quotes:
      '"1:1"'  -> '1:1'
      "'1:1'"  -> '1:1'

    Does NOT strip if quotes are unmatched:
      '"1:1'   -> '"1:1'   (unmatched -- leave as-is)
    """
    if len(value) >= 2:
        if (value[0] == '"' and value[-1] == '"') or (
            value[0] == "'" and value[-1] == "'"
        ):
            return value[1:-1]
    return value


def _parse_frontmatter(content: str) -> dict[str, str] | None:
    """Extract YAML frontmatter key-value pairs from content.

    Returns a dict of key→value strings, or None if no frontmatter found.
    Values are stripped of whitespace and matching outer YAML quotes.
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
            result[key.strip()] = _strip_yaml_quotes(value.strip())
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


def _no_undischarged_obligations(content: str) -> bool:
    """Anti-instinct gate: undischarged_obligations must equal 0.

    Returns True only if frontmatter contains undischarged_obligations: 0.
    Fail-closed: missing field, missing frontmatter, or non-zero value → False.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("undischarged_obligations")
    if value is None:
        return False
    try:
        return int(value) == 0
    except (ValueError, TypeError):
        return False


def _integration_contracts_covered(content: str) -> bool:
    """Anti-instinct gate: uncovered_contracts must equal 0.

    Returns True only if frontmatter contains uncovered_contracts: 0.
    Fail-closed: missing field, missing frontmatter, or non-zero value → False.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("uncovered_contracts")
    if value is None:
        return False
    try:
        return int(value) == 0
    except (ValueError, TypeError):
        return False


def _fingerprint_coverage_check(content: str) -> bool:
    """Anti-instinct gate: fingerprint_coverage must be >= 0.7.

    Returns True if fingerprint_coverage is a float >= 0.7.
    Fail-closed: missing field, missing frontmatter, or unparseable value → False.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("fingerprint_coverage")
    if value is None:
        return False
    try:
        return float(value) >= 0.7
    except (ValueError, TypeError):
        return False


def _convergence_score_valid(content: str) -> bool:
    """convergence_score frontmatter value parses as float in [0.0, 1.0]."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("convergence_score")
    if value is None:
        return False
    try:
        score = float(value)
        return 0.0 <= score <= 1.0
    except (ValueError, TypeError):
        return False


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
    """Validate extraction_mode is 'standard' or starts with 'chunked'.

    Accepts: 'standard', 'chunked', 'chunked (3 chunks)'.
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


# --- Cross-gate deviation count reconciliation (SC-008) ---


def _deviation_counts_reconciled(content: str) -> bool:
    """Cross-gate reconciliation: reported finding counts must match actual routed IDs.

    Compares the sum of routed deviation IDs across all routing fields against
    the reported total_analyzed count. A mismatch indicates an inconsistency
    between what the deviation analysis claims to have processed and what it
    actually routed, causing deterministic gate failure.

    Reconciliation rule:
        total unique IDs across (routing_fix_roadmap + routing_update_spec +
        routing_no_action + routing_human_review) must equal total_analyzed.

    Returns False (deterministic gate failure) if:
    - Frontmatter is missing
    - total_analyzed field is missing or non-integer
    - Count of unique routed IDs != total_analyzed
    Returns True when counts reconcile.
    """
    import re

    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    total_str = fm.get("total_analyzed")
    if total_str is None:
        return False

    try:
        total_analyzed = int(total_str)
    except (ValueError, TypeError):
        return False

    # Collect all unique IDs across all routing fields
    routing_fields = [
        "routing_fix_roadmap",
        "routing_update_spec",
        "routing_no_action",
        "routing_human_review",
    ]
    all_ids: set[str] = set()
    for field in routing_fields:
        raw = fm.get(field, "")
        if not raw:
            continue
        for token in re.split(r"[\s,]+", raw):
            token = token.strip()
            if token and re.match(r"^DEV-\d+$", token):
                all_ids.add(token)

    return len(all_ids) == total_analyzed


# --- Generate gate semantic checks ---


def _minimum_deliverable_rows(content: str) -> bool:
    """Verify the roadmap contains at least 20 deliverable table rows.

    Counts markdown table data rows (lines starting with '|' that contain
    a numeric first cell). Excludes header rows and separator rows.
    The 20-row floor catches catastrophic consolidation where a rich input
    produces only a handful of deliverables.
    """
    import re

    count = 0
    for line in content.splitlines():
        stripped = line.strip()
        # Skip non-table lines
        if not stripped.startswith("|"):
            continue
        # Skip separator rows (|---|---|)
        if re.match(r"^\|[\s:|-]+\|$", stripped):
            continue
        # Count rows where the first data cell is a number (task row #)
        cells = [c.strip() for c in stripped.split("|") if c.strip()]
        if cells and re.match(r"^\d+$", cells[0]):
            count += 1
    return count >= 20


def _no_template_sentinels(content: str) -> bool:
    """Verify no {{SC_PLACEHOLDER:*}} sentinels remain in the output.

    Template sentinels indicate the LLM failed to replace a placeholder
    section. A passing output must have zero remaining sentinels.
    """
    return "{{SC_PLACEHOLDER:" not in content


def _deliverable_table_schema(content: str) -> bool:
    """Verify the deliverable table uses the 9-column schema.

    Required header (case-insensitive, short or long forms accepted):
        | # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |

    At least one such header must be present. Catches LLM drift where
    the milestone table reverts to the old 8-col schema or invents a
    different shape.
    """
    import re

    pattern = re.compile(
        r"\|\s*#\s*"
        r"\|\s*ID\s*"
        r"\|\s*Title\s*"
        r"\|\s*Description\s*"
        r"\|\s*Comp(?:onent)?\s*"
        r"\|\s*Dep(?:endencies|s)?\s*"
        r"\|\s*(?:Acceptance Criteria|AC)\s*"
        r"\|\s*(?:Effort|Eff)\s*"
        r"\|\s*(?:Priority|Pri)\s*\|",
        re.IGNORECASE,
    )
    return bool(pattern.search(content))


# Required top-level H2 sections prescribed by roadmap_template.md.
# Compared against heading text after it has been lowercased and stripped of
# a leading "N." / "N.M." numbering prefix.
_REQUIRED_H2_SECTIONS: frozenset[str] = frozenset(
    {
        "executive summary",
        "milestone summary",
        "dependency graph",
        "resource requirements and dependencies",
        "risk register",
        "success criteria and validation approach",
        "decision summary",
        "timeline estimates",
    }
)

# H3 subsection name-stems that must appear under every `## M{N}:` section.
# The full heading is expected to be "<stem> <dash> M{N}" where <dash> is either
# an em-dash ("\u2014") or a regular hyphen ("-").
_REQUIRED_MILESTONE_SUBSECTIONS: tuple[str, ...] = (
    "integration points",
    "milestone dependencies",
    "risk assessment and mitigation",
)

# H3 subsections required under `## Resource Requirements and Dependencies`.
_REQUIRED_RESOURCE_SUBSECTIONS: frozenset[str] = frozenset(
    {"external dependencies", "infrastructure requirements"}
)


def _normalize_heading(text: str) -> str:
    """Lowercase and strip leading section numbering ("1.", "1.2.", "1.2.3.")."""
    import re

    stripped = re.sub(r"^\s*\d+(?:\.\d+)*\.?\s+", "", text.strip())
    return stripped.lower().strip()


def _template_sections_present(content: str) -> bool:
    """Verify the generated roadmap contains every section prescribed by the template.

    The roadmap template (src/superclaude/examples/roadmap_template.md) defines a
    fixed skeleton: a set of top-level H2 sections plus, for each per-milestone
    section, a set of required H3 subsections. This check catches LLM drift where
    required sections are renamed, merged, split, or silently dropped -- a class
    of failure the other structural checks (sentinels, deliverable schema, heading
    gaps) do not detect on their own.

    Rules:
      - Every entry in `_REQUIRED_H2_SECTIONS` must appear as an H2 heading.
      - At least one `## M{N}: <title>` milestone section must be present.
      - Under every milestone H2, every entry in `_REQUIRED_MILESTONE_SUBSECTIONS`
        must appear as an H3 heading of the form "<stem> <dash> M{N}" where
        <dash> is em-dash ("\u2014") or a regular hyphen.
      - Under `## Resource Requirements and Dependencies`, every entry in
        `_REQUIRED_RESOURCE_SUBSECTIONS` must appear as an H3 heading.
      - `Open Questions -- M{N}` is explicitly NOT required: the template omits
        the subsection when a milestone has zero open questions.

    Leading section numbering ("1.", "2.3.") is tolerated. Matching is
    case-insensitive. Extra sections beyond the template are allowed; only the
    absence of a required section fails the check.
    """
    import re

    lines = content.splitlines()

    # Walk the document once, recording H2 headings and their child H3s.
    h2_headings: list[tuple[int, str]] = []  # (index-in-h2_headings, raw-text)
    h3_by_h2: list[list[str]] = []  # parallel list: h3 raw-texts under each H2
    current_bucket: list[str] | None = None

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("### "):
            if current_bucket is not None:
                current_bucket.append(stripped[4:].strip())
        elif stripped.startswith("## ") and not stripped.startswith("### "):
            text = stripped[3:].strip()
            h2_headings.append((len(h2_headings), text))
            current_bucket = []
            h3_by_h2.append(current_bucket)
        elif stripped.startswith("# ") and not stripped.startswith("## "):
            # H1 resets H2 tracking but does not open a bucket itself.
            current_bucket = None

    h2_normalized = [_normalize_heading(text) for _, text in h2_headings]
    h2_set = set(h2_normalized)

    # Rule 1: all required H2 sections present.
    if not _REQUIRED_H2_SECTIONS.issubset(h2_set):
        return False

    # Rule 2: at least one milestone section, and each has required H3s.
    milestone_pattern = re.compile(r"^m(\d+)\s*:", re.IGNORECASE)
    found_any_milestone = False
    for (idx, _raw), normalized in zip(h2_headings, h2_normalized):
        m = milestone_pattern.match(normalized)
        if m is None:
            continue
        found_any_milestone = True
        n = m.group(1)
        h3_normalized = {_normalize_heading(h) for h in h3_by_h2[idx]}
        for stem in _REQUIRED_MILESTONE_SUBSECTIONS:
            # Accept em-dash or regular hyphen between stem and M{N}.
            candidates = {
                f"{stem} \u2014 m{n}",
                f"{stem} - m{n}",
                f"{stem} -- m{n}",
            }
            if not (candidates & h3_normalized):
                return False

    if not found_any_milestone:
        return False

    # Rule 3: Resource Requirements and Dependencies has the two required H3s.
    try:
        rr_index = h2_normalized.index("resource requirements and dependencies")
    except ValueError:
        # Already caught by Rule 1, but be explicit.
        return False
    rr_subs = {_normalize_heading(h) for h in h3_by_h2[rr_index]}
    if not _REQUIRED_RESOURCE_SUBSECTIONS.issubset(rr_subs):
        return False

    return True


# --- GateCriteria instances ---

EXTRACT_GATE = GateCriteria(
    required_frontmatter_fields=[
        ("spec_source", "spec_sources"),
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
            failure_message="extraction_mode must be 'standard' or 'chunked'",
        ),
    ],
)

EXTRACT_TDD_GATE = GateCriteria(
    required_frontmatter_fields=[
        # 13 standard fields (same as EXTRACT_GATE)
        ("spec_source", "spec_sources"),
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
        # 6 TDD-specific fields
        "data_models_identified",
        "api_surfaces_identified",
        "components_identified",
        "test_artifacts_identified",
        "migration_items_identified",
        "operational_items_identified",
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
            failure_message="extraction_mode must be 'standard' or 'chunked'",
        ),
    ],
)

GENERATE_A_GATE = GateCriteria(
    required_frontmatter_fields=[
        ("spec_source", "spec_sources"),
        "complexity_score",
        "primary_persona",
    ],
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
        SemanticCheck(
            name="minimum_deliverable_rows",
            check_fn=_minimum_deliverable_rows,
            failure_message="Roadmap must contain at least 20 deliverable table rows (granularity floor)",
        ),
        SemanticCheck(
            name="deliverable_table_schema",
            check_fn=_deliverable_table_schema,
            failure_message="Deliverable table header must use 9-column schema: | # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |",
        ),
        SemanticCheck(
            name="no_template_sentinels",
            check_fn=_no_template_sentinels,
            failure_message="Template sentinels {{SC_PLACEHOLDER:*}} remain -- all placeholders must be replaced",
        ),
        SemanticCheck(
            name="template_sections_present",
            check_fn=_template_sections_present,
            failure_message=(
                "Roadmap is missing one or more sections required by the template: "
                "top-level H2s (Executive Summary, Milestone Summary, Dependency Graph, "
                "Resource Requirements and Dependencies, Risk Register, "
                "Success Criteria and Validation Approach, Decision Summary, "
                "Timeline Estimates), at least one `## M{N}: ...` milestone with "
                "Integration Points / Milestone Dependencies / Risk Assessment and "
                "Mitigation subsections, and External Dependencies / Infrastructure "
                "Requirements under Resource Requirements and Dependencies"
            ),
        ),
    ],
)

# GENERATE_A_GATE and GENERATE_B_GATE evaluate identical output shapes (two
# parallel variants of the same roadmap). Keep two names for backwards
# compatibility with callers and ALL_GATES wiring, but share one criteria
# instance so adding or tuning a check happens in exactly one place.
GENERATE_B_GATE = GENERATE_A_GATE

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
    required_frontmatter_fields=[
        ("spec_source", "spec_sources"),
        "complexity_score",
        "adversarial",
    ],
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
            failure_message="Duplicate H2 (global) or H3 (within same H2 section) heading detected",
        ),
        SemanticCheck(
            name="minimum_deliverable_rows",
            check_fn=_minimum_deliverable_rows,
            failure_message="Merged roadmap must contain at least 20 deliverable table rows (granularity floor)",
        ),
        SemanticCheck(
            name="deliverable_table_schema",
            check_fn=_deliverable_table_schema,
            failure_message="Deliverable table header must use 9-column schema: | # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |",
        ),
        SemanticCheck(
            name="no_template_sentinels",
            check_fn=_no_template_sentinels,
            failure_message="Template sentinels {{SC_PLACEHOLDER:*}} remain -- all placeholders must be replaced",
        ),
        SemanticCheck(
            name="template_sections_present",
            check_fn=_template_sections_present,
            failure_message=(
                "Merged roadmap is missing one or more sections required by the "
                "template: top-level H2s (Executive Summary, Milestone Summary, "
                "Dependency Graph, Resource Requirements and Dependencies, Risk "
                "Register, Success Criteria and Validation Approach, Decision "
                "Summary, Timeline Estimates), at least one `## M{N}: ...` "
                "milestone with Integration Points / Milestone Dependencies / "
                "Risk Assessment and Mitigation subsections, and External "
                "Dependencies / Infrastructure Requirements under Resource "
                "Requirements and Dependencies"
            ),
        ),
    ],
)

TEST_STRATEGY_GATE = GateCriteria(
    required_frontmatter_fields=[
        ("spec_source", "spec_sources"),
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

ANTI_INSTINCT_GATE = GateCriteria(
    required_frontmatter_fields=[
        "undischarged_obligations",
        "uncovered_contracts",
        "fingerprint_coverage",
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="no_undischarged_obligations",
            check_fn=_no_undischarged_obligations,
            failure_message="undischarged_obligations must be 0; scaffolding obligations lack discharge in later milestones",
        ),
        SemanticCheck(
            name="integration_contracts_covered",
            check_fn=_integration_contracts_covered,
            failure_message="uncovered_contracts must be 0; integration contracts lack explicit wiring tasks in roadmap",
        ),
        SemanticCheck(
            name="fingerprint_coverage_check",
            check_fn=_fingerprint_coverage_check,
            failure_message="fingerprint_coverage must be >= 0.7; spec code-level identifiers insufficiently represented in roadmap",
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
        SemanticCheck(
            name="deviation_counts_reconciled",
            check_fn=_deviation_counts_reconciled,
            failure_message="Deviation count mismatch: total_analyzed does not equal count of unique routed IDs across all routing fields (SC-008)",
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
    ("anti-instinct", ANTI_INSTINCT_GATE),
    ("test-strategy", TEST_STRATEGY_GATE),
    ("spec-fidelity", SPEC_FIDELITY_GATE),
    ("wiring-verification", WIRING_GATE),
    ("deviation-analysis", DEVIATION_ANALYSIS_GATE),
    ("remediate", REMEDIATE_GATE),
    ("certify", CERTIFY_GATE),
]
