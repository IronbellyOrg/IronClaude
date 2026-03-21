"""Structural fingerprint extraction and coverage checking.

Extracts code-level identifiers from spec content (backtick-delimited names,
code-block definitions, ALL_CAPS constants) and verifies a minimum coverage
ratio appears in the roadmap. Catches wholesale omission of design detail
that text-matching on formal IDs would miss.

Pure function: content in, result out. No I/O.

Implements FR-MOD3.1 through FR-MOD3.4.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Fingerprint:
    """A named code-level entity from the spec."""

    text: str  # e.g., "_run_programmatic_step"
    category: str  # "identifier", "definition", "constant"
    source_context: str  # surrounding text for debugging


# FR-MOD3.1 + OQ-011: Common non-specific constants to exclude.
# Aligned with 4-char regex minimum.
_EXCLUDED_CONSTANTS = frozenset(
    {
        "TRUE",
        "FALSE",
        "NONE",
        "TODO",
        "NOTE",
        "WARNING",
        "HIGH",
        "MEDIUM",
        "LOW",
        "YAML",
        "JSON",
        "STRICT",
        "STANDARD",
        "EXEMPT",
        "LIGHT",
        "PASS",
        "FAIL",
        "INFO",
        "DEBUG",
        "ERROR",
        "CRITICAL",
    }
)


def extract_code_fingerprints(content: str) -> list[Fingerprint]:
    """Extract code-level identifiers from spec content.

    FR-MOD3.1: Three-source extraction:
    1. Backtick-delimited identifiers (>= 4 chars)
    2. Code-fenced blocks: function/class definitions
    3. ALL_CAPS constants (likely important data structures)

    FR-MOD3.2: Deduplication by text value.
    """
    fingerprints: list[Fingerprint] = []

    # Source 1: Backtick identifiers (most reliable)
    for match in re.finditer(r"`([a-zA-Z_]\w*(?:\(\))?)`", content):
        text = match.group(1).rstrip("()")
        if len(text) >= 4:  # skip trivial identifiers
            ctx_start = max(0, match.start() - 40)
            ctx_end = min(len(content), match.end() + 40)
            fingerprints.append(
                Fingerprint(
                    text=text,
                    category="identifier",
                    source_context=content[ctx_start:ctx_end].replace("\n", " "),
                )
            )

    # Source 2: Code block function/class definitions
    code_block_pat = re.compile(r"```(?:python)?\n(.*?)```", re.DOTALL)
    for block_match in code_block_pat.finditer(content):
        block = block_match.group(1)
        for def_match in re.finditer(r"(?:def|class)\s+(\w+)", block):
            fingerprints.append(
                Fingerprint(
                    text=def_match.group(1),
                    category="definition",
                    source_context=def_match.group(0),
                )
            )

    # Source 3: ALL_CAPS constants (>= 4 chars per regex minimum)
    for match in re.finditer(r"\b([A-Z][A-Z_]{3,})\b", content):
        text = match.group(1)
        if text not in _EXCLUDED_CONSTANTS:
            fingerprints.append(
                Fingerprint(
                    text=text,
                    category="constant",
                    source_context=content[
                        max(0, match.start() - 40) : match.end() + 40
                    ].replace("\n", " "),
                )
            )

    # FR-MOD3.2: Deduplicate by text value
    seen: set[str] = set()
    unique: list[Fingerprint] = []
    for fp in fingerprints:
        if fp.text not in seen:
            seen.add(fp.text)
            unique.append(fp)

    return unique


def check_fingerprint_coverage(
    spec_content: str,
    roadmap_content: str,
    min_coverage_ratio: float = 0.7,
) -> tuple[int, int, list[str], float]:
    """Check that spec fingerprints appear in roadmap.

    FR-MOD3.3: Case-insensitive roadmap coverage check returning 4-tuple.
    FR-MOD3.4: Threshold gate logic with empty-fingerprint passthrough.

    Returns (total, found, missing_list, ratio).
    """
    spec_fps = extract_code_fingerprints(spec_content)

    # FR-MOD3.4: Empty-fingerprint passthrough
    if not spec_fps:
        return (0, 0, [], 1.0)

    roadmap_lower = roadmap_content.lower()
    missing: list[str] = []
    found = 0

    for fp in spec_fps:
        if fp.text.lower() in roadmap_lower:
            found += 1
        else:
            missing.append(fp.text)

    total = len(spec_fps)
    ratio = found / total if total > 0 else 1.0

    return (total, found, missing, ratio)


def fingerprint_gate_passed(
    spec_content: str,
    roadmap_content: str,
    min_coverage_ratio: float = 0.7,
) -> bool:
    """FR-MOD3.4: Threshold gate logic.

    Returns True when ratio >= min_coverage_ratio or fingerprint set is empty.
    """
    total, found, _, ratio = check_fingerprint_coverage(
        spec_content, roadmap_content, min_coverage_ratio
    )
    if total == 0:
        return True  # passthrough
    return ratio >= min_coverage_ratio
