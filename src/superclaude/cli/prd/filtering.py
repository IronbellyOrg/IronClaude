"""PRD pipeline filtering -- partitioning, gap compilation, and synthesis mapping.

Pure-function module for splitting file lists into partitions, compiling
gap reports from research files, merging QA partition reports with
pessimistic verdict strategy, and loading the synthesis mapping table.

Dependencies: models (via type hints only)
"""

from __future__ import annotations

import math
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# File Partitioning (FR-PRD.11)
# ---------------------------------------------------------------------------


def partition_files(
    files: list, threshold: int
) -> list[list]:
    """Split a file list into partitions for parallel processing.

    If the file count is at or below the threshold, returns a single
    partition containing all files. Above the threshold, splits into
    roughly even partitions where each partition has at most ``threshold``
    items.

    Args:
        files: List of file paths (or any items) to partition.
        threshold: Maximum items per partition.

    Returns:
        A list of partitions (each partition is a list of items).
        Returns an empty list if files is empty.
    """
    if not files:
        return []
    if len(files) <= threshold:
        return [list(files)]

    num_partitions = math.ceil(len(files) / threshold)
    partition_size = math.ceil(len(files) / num_partitions)

    partitions: list[list] = []
    for i in range(0, len(files), partition_size):
        partitions.append(list(files[i : i + partition_size]))
    return partitions


# ---------------------------------------------------------------------------
# Gap Compilation
# ---------------------------------------------------------------------------


def compile_gaps(research_dir: Path) -> list[dict]:
    """Extract and deduplicate gaps from research files.

    Scans all ``.md`` files in the research directory for gap entries.
    Gaps are identified by lines matching patterns like:
    - ``- GAP: description``
    - ``- [ ] Gap: description``
    - Lines under a ``## Gap Analysis`` or ``## Gaps`` heading

    Returns a deduplicated list of gap dictionaries with keys:
    ``description``, ``source_file``, ``severity`` (if present).
    """
    if not research_dir.is_dir():
        return []

    seen_descriptions: set[str] = set()
    gaps: list[dict] = []

    for md_file in sorted(research_dir.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        file_gaps = _extract_gaps_from_content(content, md_file.name)
        for gap in file_gaps:
            desc_key = gap["description"].lower().strip()
            if desc_key not in seen_descriptions:
                seen_descriptions.add(desc_key)
                gaps.append(gap)

    return gaps


def _extract_gaps_from_content(content: str, source_file: str) -> list[dict]:
    """Extract gap entries from file content."""
    gaps: list[dict] = []

    # Pattern 1: Explicit GAP markers
    for match in re.finditer(
        r"^\s*[-*]\s+(?:\[[ x]\]\s+)?(?:GAP|Gap)\s*:\s*(.+)$",
        content,
        re.MULTILINE,
    ):
        gaps.append({
            "description": match.group(1).strip(),
            "source_file": source_file,
        })

    # Pattern 2: Items under Gap Analysis heading
    gap_section = re.search(
        r"(?:^|\n)\s*#{{1,4}}\s+(?:Gap\s+Analysis|Gaps)\s*\n(.*?)(?=\n\s*#|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if gap_section:
        section_text = gap_section.group(1)
        for line_match in re.finditer(
            r"^\s*[-*]\s+(.+)$", section_text, re.MULTILINE
        ):
            desc = line_match.group(1).strip()
            if desc and not desc.startswith("#"):
                gaps.append({
                    "description": desc,
                    "source_file": source_file,
                })

    return gaps


# ---------------------------------------------------------------------------
# QA Partition Report Merging (GAP-005)
# ---------------------------------------------------------------------------


def merge_qa_partition_reports(reports: list[dict]) -> dict:
    """Merge multiple QA partition reports with pessimistic verdict.

    GAP-005: Overall verdict is FAIL if ANY partition reports FAIL.
    Only returns PASS if ALL partitions pass.

    Args:
        reports: List of dicts, each with at least a ``verdict`` key
                 ("PASS" or "FAIL") and optional ``issues`` list.

    Returns:
        Merged report dict with ``verdict``, ``partition_count``,
        ``partitions_passed``, ``partitions_failed``, and ``issues``.
    """
    if not reports:
        return {
            "verdict": "PASS",
            "partition_count": 0,
            "partitions_passed": 0,
            "partitions_failed": 0,
            "issues": [],
        }

    all_issues: list[str] = []
    passed = 0
    failed = 0

    for report in reports:
        verdict = report.get("verdict", "FAIL").upper()
        if verdict == "PASS":
            passed += 1
        else:
            failed += 1
        issues = report.get("issues", [])
        all_issues.extend(issues)

    return {
        "verdict": "FAIL" if failed > 0 else "PASS",
        "partition_count": len(reports),
        "partitions_passed": passed,
        "partitions_failed": failed,
        "issues": all_issues,
    }


# ---------------------------------------------------------------------------
# Synthesis Mapping (F-002)
# ---------------------------------------------------------------------------


_DEFAULT_SYNTHESIS_MAPPING: list[dict] = [
    {
        "synth_file": "synth-01-exec-problem-vision.md",
        "sections": [
            "1. Executive Summary",
            "2. Problem Statement",
            "3. Background & Strategic Fit",
            "4. Product Vision",
        ],
        "source_research": [
            "product capabilities",
            "web research (market context)",
            "existing docs",
        ],
    },
    {
        "synth_file": "synth-02-business-market.md",
        "sections": [
            "5. Business Context",
            "6. JTBD",
            "7. User Personas",
            "8. Value Proposition Canvas",
        ],
        "source_research": [
            "user flows",
            "web research (market context)",
            "product capabilities",
        ],
    },
    {
        "synth_file": "synth-03-competitive-scope.md",
        "sections": [
            "9. Competitive Analysis",
            "10. Assumptions & Constraints",
            "11. Dependencies",
            "12. Scope Definition",
        ],
        "source_research": [
            "web research (competitive landscape)",
            "technical stack",
            "integration points",
        ],
    },
    {
        "synth_file": "synth-04-stories-requirements.md",
        "sections": [
            "13. Open Questions",
            "21.1 Epics Features & Stories",
            "21.2 Product Requirements",
        ],
        "source_research": [
            "per-area research files",
            "user flows",
            "gaps log",
        ],
    },
    {
        "synth_file": "synth-05-technical-stack.md",
        "sections": [
            "14. Technical Requirements",
            "15. Technology Stack",
        ],
        "source_research": [
            "technical stack",
            "architecture research",
            "web research (technology trends)",
        ],
    },
    {
        "synth_file": "synth-06-ux-legal-business.md",
        "sections": [
            "16. UX Requirements",
            "17. Legal & Compliance",
            "18. Business Requirements",
        ],
        "source_research": [
            "user flows",
            "product capabilities",
            "web research (compliance, market)",
        ],
    },
    {
        "synth_file": "synth-07-metrics-risk-impl.md",
        "sections": [
            "19. Success Metrics",
            "20. Risk Analysis",
            "21.3 Implementation Phasing",
            "21.4 Release Criteria & DoD",
            "21.5 Timeline & Milestones",
        ],
        "source_research": [
            "all research files",
            "web research",
            "technical stack",
        ],
    },
    {
        "synth_file": "synth-08-journey-design-api.md",
        "sections": [
            "22. Customer Journey",
            "23. Error Handling",
            "24. User Interaction",
            "25. API Contracts",
        ],
        "source_research": [
            "user flows",
            "per-area research",
            "technical stack",
        ],
    },
    {
        "synth_file": "synth-09-resources-maintenance.md",
        "sections": [
            "26. Contributors",
            "27. Related Resources",
            "28. Maintenance & Ownership",
        ],
        "source_research": [
            "existing docs",
            "all research files",
            "gaps log",
        ],
    },
]


def load_synthesis_mapping(refs_dir: Path) -> list[dict]:
    """Load the synthesis mapping table.

    F-002: Returns exactly 9 entries mapping synthesis files to
    PRD template sections and their source research inputs.

    Falls back to the built-in default mapping if the refs directory
    or mapping file is not available.

    Args:
        refs_dir: Path to the skill refs directory containing
                  synthesis-mapping.md.

    Returns:
        List of 9 mapping dicts, each with keys:
        ``synth_file``, ``sections``, ``source_research``.
    """
    # The mapping is compiled from the spec; the .md file is the
    # human-readable reference. We use the built-in default.
    return list(_DEFAULT_SYNTHESIS_MAPPING)


def _filter_research_for_sections(
    research_files: list[Path], mapping_entry: dict
) -> list[Path]:
    """Filter research files relevant to a synthesis section mapping.

    Matches research files to a mapping entry's source_research
    descriptors using filename heuristics.

    Args:
        research_files: All available research files.
        mapping_entry: A single entry from the synthesis mapping table.

    Returns:
        Subset of research_files relevant to the mapping entry.
    """
    source_hints = mapping_entry.get("source_research", [])

    # "all research files" means return everything
    for hint in source_hints:
        if "all research" in hint.lower():
            return list(research_files)

    matched: list[Path] = []
    for f in research_files:
        fname = f.stem.lower().replace("-", " ").replace("_", " ")
        for hint in source_hints:
            # Extract keywords from the hint
            hint_lower = hint.lower()
            # Remove parenthetical qualifiers
            hint_clean = re.sub(r"\(.*?\)", "", hint_lower).strip()
            keywords = [w for w in hint_clean.split() if len(w) > 2]
            if any(kw in fname for kw in keywords):
                matched.append(f)
                break

    return matched
