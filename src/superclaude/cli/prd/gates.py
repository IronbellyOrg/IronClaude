"""PRD pipeline gate criteria -- semantic checks and step-to-gate mappings.

Defines the GATE_CRITERIA dict mapping each PRD pipeline step to its
GateCriteria instance, plus 10 semantic check functions organized in
two layers:

  1. Reusable checks: _check_verdict_field, _check_no_placeholders
  2. PRD-specific checks: _check_parsed_request_fields,
     _check_research_notes_sections, _check_suggested_phases_detail,
     _check_task_phases_present, _check_b2_self_contained,
     _check_parallel_instructions, _check_prd_template_sections,
     _check_qa_verdict

All semantic check functions follow Callable[[str], bool | str] signature:
  - Return True on pass
  - Return an error string on failure

All checks are wrapped in try/except: exceptions return
(False, "check '{name}' crashed: {error}") per F-005.

NFR-PRD.2: All _check_* functions match Callable[[str], bool | str].
"""

from __future__ import annotations

import json
import re
from typing import Callable

from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck


# ---------------------------------------------------------------------------
# Layer 1: Reusable semantic checks
# ---------------------------------------------------------------------------


def _check_verdict_field(content: str) -> bool | str:
    """Check that content contains a verdict field set to PASS or FAIL.

    Accepts both JSON format ("verdict": "PASS") and markdown format
    (verdict: PASS or **Verdict**: PASS).
    """
    # JSON format
    json_match = re.search(r'"verdict"\s*:\s*"(PASS|FAIL)"', content)
    if json_match:
        return True
    # Markdown format (case-insensitive key, case-sensitive value)
    md_match = re.search(
        r"(?:^|\n)\s*\*{0,2}[Vv]erdict\*{0,2}\s*:\s*(PASS|FAIL)",
        content,
    )
    if md_match:
        return True
    return "No verdict field found (expected 'verdict: PASS' or 'verdict: FAIL')"


def _check_no_placeholders(content: str) -> bool | str:
    """Check that content contains no placeholder text.

    Catches TODO, TBD, PLACEHOLDER, [INSERT], and similar markers.
    """
    patterns = [
        (r"\bTODO\b", "TODO"),
        (r"\bTBD\b", "TBD"),
        (r"\bPLACEHOLDER\b", "PLACEHOLDER"),
        (r"\[INSERT[^\]]*\]", "[INSERT...]"),
        (r"\[FILL[^\]]*\]", "[FILL...]"),
    ]
    found = []
    for pattern, label in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            found.append(f"{label} ({len(matches)}x)")
    if found:
        return f"Placeholder text found: {', '.join(found)}"
    return True


# ---------------------------------------------------------------------------
# Layer 2: PRD-specific semantic checks
# ---------------------------------------------------------------------------


def _check_parsed_request_fields(content: str) -> bool | str:
    """Check that parsed request contains GOAL, PRODUCT_SLUG, PRD_SCOPE, SCENARIO."""
    required = ["GOAL", "PRODUCT_SLUG", "PRD_SCOPE", "SCENARIO"]
    missing = []
    for field_name in required:
        # Check JSON key format
        json_pat = re.compile(rf'"{field_name}"\s*:\s*"[^"]+"', re.IGNORECASE)
        # Check markdown key: value format
        md_pat = re.compile(
            rf"(?:^|\n)\s*\*{{0,2}}{field_name}\*{{0,2}}\s*:\s*\S",
            re.IGNORECASE,
        )
        if not json_pat.search(content) and not md_pat.search(content):
            missing.append(field_name)
    if missing:
        return f"Missing required fields: {', '.join(missing)}"
    return True


_RESEARCH_REQUIRED_SECTIONS = [
    "Product Capabilities",
    "Technical Architecture",
    "User Flows",
    "Integration Points",
    "Existing Documentation",
    "Gap Analysis",
    "Suggested Phases",
]


def _check_research_notes_sections(content: str) -> bool | str:
    """Check that research notes contain all 7 required sections."""
    missing = []
    for section in _RESEARCH_REQUIRED_SECTIONS:
        # Match as markdown heading (## or ###) or bold text
        heading_pat = re.compile(
            rf"^\s*#{{1,4}}\s+.*{re.escape(section)}", re.MULTILINE | re.IGNORECASE
        )
        bold_pat = re.compile(
            rf"\*\*{re.escape(section)}\*\*", re.IGNORECASE
        )
        if not heading_pat.search(content) and not bold_pat.search(content):
            missing.append(section)
    if missing:
        return f"Missing research sections: {', '.join(missing)}"
    return True


def _check_suggested_phases_detail(content: str) -> bool | str:
    """Check that the Suggested Phases section contains per-agent detail.

    Expects at least one numbered or bulleted list item under a Phases heading.
    """
    phases_match = re.search(
        r"(?:^|\n)\s*#{1,4}\s+.*(?:Suggested\s+)?Phases",
        content,
        re.IGNORECASE,
    )
    if not phases_match:
        return "No 'Suggested Phases' section found"
    # Check for list items after the heading
    after_heading = content[phases_match.end() :]
    list_pat = re.search(r"(?:^|\n)\s*(?:\d+\.|[-*])\s+\S", after_heading)
    if not list_pat:
        return "Suggested Phases section has no detail items"
    return True


def _check_task_phases_present(content: str) -> bool | str:
    """Check that the task file contains phase definitions.

    Expects headings like 'Phase 1:', 'Phase 2:', etc.
    """
    phase_headings = re.findall(
        r"(?:^|\n)\s*#{1,4}\s+.*Phase\s+\d", content, re.IGNORECASE
    )
    if len(phase_headings) < 2:
        return f"Expected multiple phase headings, found {len(phase_headings)}"
    return True


def _check_b2_self_contained(content: str) -> bool | str:
    """Check that checklist items do not reference external content.

    Catches 'see above', 'as mentioned', 'refer to' violations in
    checklist items (lines starting with '- [ ]' or '- [x]').
    """
    violations = []
    for match in re.finditer(
        r"^\s*-\s+\[[ x]\]\s+(.+)$", content, re.MULTILINE
    ):
        item_text = match.group(1)
        for phrase in ["see above", "as mentioned", "refer to", "as described"]:
            if phrase.lower() in item_text.lower():
                violations.append(f"'{phrase}' in: {item_text[:60]}")
    if violations:
        return (
            f"Self-containment violations in checklist items: "
            f"{'; '.join(violations[:3])}"
        )
    return True


def _check_parallel_instructions(content: str) -> bool | str:
    """Check that phases 2-5 contain parallel execution keywords.

    Validates that later phases include 'parallel', 'concurrent',
    'simultaneously', or 'batch' instructions.
    """
    parallel_keywords = ["parallel", "concurrent", "simultaneously", "batch"]
    # Find phase sections 2+
    phase_sections = list(
        re.finditer(
            r"(?:^|\n)\s*#{1,4}\s+.*Phase\s+(\d+)",
            content,
            re.IGNORECASE,
        )
    )
    later_phases = [m for m in phase_sections if int(m.group(1)) >= 2]
    if not later_phases:
        return True  # No later phases to check

    # Check content between each later phase heading and next heading
    for i, phase_match in enumerate(later_phases):
        start = phase_match.end()
        end = (
            later_phases[i + 1].start()
            if i + 1 < len(later_phases)
            else len(content)
        )
        section_text = content[start:end].lower()
        if not any(kw in section_text for kw in parallel_keywords):
            phase_num = phase_match.group(1)
            return (
                f"Phase {phase_num} missing parallel execution instructions "
                f"(expected one of: {', '.join(parallel_keywords)})"
            )
    return True


_PRD_CRITICAL_SECTIONS = [
    "Executive Summary",
    "Problem Statement",
    "Technical Requirements",
    "Implementation Plan",
    "Success Metrics",
]


def _check_prd_template_sections(content: str) -> bool | str:
    """Check that the assembled PRD contains critical template sections."""
    missing = []
    for section in _PRD_CRITICAL_SECTIONS:
        pat = re.compile(
            rf"^\s*#{{1,3}}\s+.*{re.escape(section)}",
            re.MULTILINE | re.IGNORECASE,
        )
        if not pat.search(content):
            missing.append(section)
    if missing:
        return f"Missing PRD sections: {', '.join(missing)}"
    return True


def _check_qa_verdict(content: str) -> bool | str:
    """Check that QA report contains a verdict of PASS or FAIL."""
    return _check_verdict_field(content)


# ---------------------------------------------------------------------------
# Safe wrapper for semantic checks (F-005)
# ---------------------------------------------------------------------------


def _safe_check(name: str, fn: Callable[[str], bool | str]) -> Callable[[str], bool | str]:
    """Wrap a check function so exceptions become error strings."""

    def wrapper(content: str) -> bool | str:
        try:
            return fn(content)
        except Exception as exc:
            return f"check '{name}' crashed: {exc}"

    return wrapper


def _make_semantic_check(
    name: str,
    fn: Callable[[str], bool | str],
    failure_message: str,
) -> SemanticCheck:
    """Build a SemanticCheck with crash-safe wrapper."""
    return SemanticCheck(
        name=name,
        check_fn=_safe_check(name, fn),
        failure_message=failure_message,
    )


# ---------------------------------------------------------------------------
# Gate Criteria Table (Section 5.2)
# ---------------------------------------------------------------------------


def _tier_min_lines(tier: str) -> int:
    """Return tier-dependent minimum line count for task file gate."""
    return {"lightweight": 200, "standard": 400, "heavyweight": 600}.get(tier, 400)


def _tier_min_lines_assembly(tier: str) -> int:
    """Return tier-dependent minimum line count for assembly gate."""
    return {
        "lightweight": 400,
        "standard": 800,
        "heavyweight": 1500,
    }.get(tier, 800)


GATE_CRITERIA: dict[str, GateCriteria] = {
    # Step 1: Check Existing
    "check-existing": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="EXEMPT",
    ),
    # Step 2: Parse Request
    "parse-request": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "parsed_request_fields",
                _check_parsed_request_fields,
                "Parsed request missing required fields",
            ),
        ],
    ),
    # Step 3: Scope Discovery
    "scope-discovery": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=50,
        enforcement_tier="STANDARD",
    ),
    # Step 4: Research Notes
    "research-notes": GateCriteria(
        required_frontmatter_fields=["Date", "Scenario", "Tier"],
        min_lines=100,
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "research_notes_sections",
                _check_research_notes_sections,
                "Research notes missing required sections",
            ),
            _make_semantic_check(
                "suggested_phases_detail",
                _check_suggested_phases_detail,
                "Suggested Phases section lacks detail",
            ),
        ],
    ),
    # Step 5: Sufficiency Review
    "sufficiency-review": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "verdict_field",
                _check_verdict_field,
                "Sufficiency review missing verdict",
            ),
        ],
    ),
    # Step 6: Template Triage
    "template-triage": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="EXEMPT",
    ),
    # Step 7: Build Task File
    "build-task-file": GateCriteria(
        required_frontmatter_fields=[
            "id",
            "title",
            "status",
            "complexity",
            "created_date",
        ],
        min_lines=400,  # default standard tier; callers override per tier
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "task_phases_present",
                _check_task_phases_present,
                "Task file missing phase definitions",
            ),
            _make_semantic_check(
                "b2_self_contained",
                _check_b2_self_contained,
                "Checklist items reference external content",
            ),
            _make_semantic_check(
                "parallel_instructions",
                _check_parallel_instructions,
                "Later phases missing parallel execution instructions",
            ),
        ],
    ),
    # Step 8: Verify Task File
    "verify-task-file": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "verdict_field",
                _check_verdict_field,
                "Task file verification missing verdict",
            ),
        ],
    ),
    # Step 9: Preparation
    "preparation": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="LIGHT",
    ),
    # Step 10: Investigation (per file)
    "investigation": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=50,
        enforcement_tier="STANDARD",
    ),
    # Step 11: Research QA
    "research-qa": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=20,
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "qa_verdict",
                _check_qa_verdict,
                "Research QA report missing verdict",
            ),
        ],
    ),
    # Step 12: Web Research (per file)
    "web-research": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=30,
        enforcement_tier="STANDARD",
    ),
    # Step 13a: Synthesis (per file)
    "synthesis": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=80,
        enforcement_tier="STANDARD",
    ),
    # Step 13b: Synthesis QA
    "synthesis-qa": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=20,
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "qa_verdict",
                _check_qa_verdict,
                "Synthesis QA report missing verdict",
            ),
        ],
    ),
    # Step 14a: Assembly
    "assembly": GateCriteria(
        required_frontmatter_fields=[
            "id",
            "title",
            "status",
            "created_date",
            "tags",
        ],
        min_lines=800,  # default standard tier; callers override per tier
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "prd_template_sections",
                _check_prd_template_sections,
                "Assembled PRD missing critical sections",
            ),
            _make_semantic_check(
                "no_placeholders",
                _check_no_placeholders,
                "Assembled PRD contains placeholder text",
            ),
        ],
    ),
    # Step 14b: Structural QA
    "structural-qa": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=20,
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "qa_verdict",
                _check_qa_verdict,
                "Structural QA report missing verdict",
            ),
        ],
    ),
    # Step 14c: Qualitative QA
    "qualitative-qa": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=20,
        enforcement_tier="STRICT",
        semantic_checks=[
            _make_semantic_check(
                "qa_verdict",
                _check_qa_verdict,
                "Qualitative QA report missing verdict",
            ),
        ],
    ),
    # Step 15: Present & Complete
    "present-complete": GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="LIGHT",
    ),
}
