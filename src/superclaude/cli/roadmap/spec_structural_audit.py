"""Spec structural audit -- upstream guard on extraction quality.

Counts structural requirement indicators in the raw spec (code blocks,
MUST/SHALL clauses, function signatures, test names, registry patterns)
and compares against the extraction's total_requirements frontmatter value.
If the extraction reports suspiciously few requirements relative to the
spec's structural richness, it flags a potential extraction failure.

Pure function: spec text + extraction requirement count in, result out.
No I/O, no exceptions raised, warning-only enforcement.

Implements FR-MOD4.1 through FR-MOD4.3.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# --- FR-MOD4.1: 7 structural indicator counters ---


@dataclass
class SpecStructuralAudit:
    """Result of structural indicator counting."""

    code_block_count: int  # Number of code blocks in spec
    must_shall_count: int  # Sentences with MUST/SHALL/REQUIRED
    function_signature_count: int  # def foo() patterns in code blocks
    class_definition_count: int  # class Foo patterns in code blocks
    test_name_count: int  # test_* patterns
    registry_pattern_count: int  # UPPERCASE_DICT = { patterns
    pseudocode_blocks: int  # Blocks showing control flow (if/else/for)
    total_structural_indicators: int


def audit_spec_structure(spec_text: str) -> SpecStructuralAudit:
    """Count structural requirement indicators in the raw spec.

    FR-MOD4.1: Counts exactly 7 structural indicators as defined in the spec.
    These indicators approximate the spec's "requirement density."
    """
    code_blocks = re.findall(r"```[\s\S]*?```", spec_text)
    code_text = "\n".join(code_blocks)

    code_block_count = len(code_blocks)
    must_shall_count = len(
        re.findall(r"\b(?:MUST|SHALL|REQUIRED)\b", spec_text)
    )
    function_signature_count = len(
        re.findall(r"\bdef\s+\w+\s*\(", code_text)
    )
    class_definition_count = len(re.findall(r"\bclass\s+\w+", code_text))
    test_name_count = len(re.findall(r"\btest_\w+", spec_text))
    registry_pattern_count = len(
        re.findall(r"\b[A-Z][A-Z_]+\s*=\s*\{", code_text)
    )
    pseudocode_blocks = len(
        re.findall(
            r"```[\s\S]*?(?:if\s|elif\s|else:|for\s|while\s)[\s\S]*?```",
            spec_text,
        )
    )

    total = (
        code_block_count
        + must_shall_count
        + function_signature_count
        + class_definition_count
        + test_name_count
        + registry_pattern_count
        + pseudocode_blocks
    )

    return SpecStructuralAudit(
        code_block_count=code_block_count,
        must_shall_count=must_shall_count,
        function_signature_count=function_signature_count,
        class_definition_count=class_definition_count,
        test_name_count=test_name_count,
        registry_pattern_count=registry_pattern_count,
        pseudocode_blocks=pseudocode_blocks,
        total_structural_indicators=total,
    )


# --- FR-MOD4.2 + FR-MOD4.3: Ratio comparison, warning-only enforcement ---


def check_extraction_adequacy(
    spec_text: str,
    extraction_total_requirements: int,
    threshold: float = 0.5,
) -> tuple[bool, SpecStructuralAudit]:
    """Check whether extraction captured enough of the spec's structural content.

    FR-MOD4.2: Ratio comparison against total_requirements frontmatter.
    FR-MOD4.3: Warning-only enforcement — returns result but never raises
    exceptions or blocks pipeline.

    Returns (passed, audit_result).

    The threshold is conservative (0.5) because structural indicators overcount:
    code examples, alternatives, and non-requirement prose inflate the indicator
    count. A ratio below 0.5 strongly suggests the extraction dropped content.
    """
    audit = audit_spec_structure(spec_text)

    if audit.total_structural_indicators == 0:
        return True, audit  # No indicators to compare against

    ratio = extraction_total_requirements / audit.total_structural_indicators
    return ratio >= threshold, audit
