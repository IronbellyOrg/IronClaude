"""Pipeline gate validation -- pure Python, no subprocess, no LLM invocation.

Validates step outputs against GateCriteria with tier-proportional checks:
  EXEMPT  -> always passes
  LIGHT   -> file exists + non-empty
  STANDARD -> + min lines + YAML frontmatter fields
  STRICT  -> + semantic checks (if defined)

NFR-003: No subprocess import. NFR-007: No sprint/roadmap imports.
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import GateCriteria, SemanticCheck


def gate_passed(output_file: Path, criteria: GateCriteria) -> tuple[bool, str | None]:
    """Validate a step's output against its gate criteria.

    Returns (True, None) on pass.
    Returns (False, reason) on failure where reason is human-readable.
    """
    tier = criteria.enforcement_tier

    # EXEMPT: always passes
    if tier == "EXEMPT":
        return True, None

    # LIGHT, STANDARD, STRICT: file must exist
    if not output_file.exists():
        return False, f"File not found: {output_file}"

    # LIGHT, STANDARD, STRICT: file must be non-empty
    content = output_file.read_text(encoding="utf-8")
    if len(content.strip()) == 0:
        return False, f"File empty (0 bytes): {output_file}"

    # LIGHT stops here
    if tier == "LIGHT":
        return True, None

    # STANDARD, STRICT: minimum line count
    lines = content.splitlines()
    if len(lines) < criteria.min_lines:
        return False, (
            f"Below minimum line count: {len(lines)} < {criteria.min_lines} "
            f"in {output_file}"
        )

    # STANDARD, STRICT: YAML frontmatter fields
    if criteria.required_frontmatter_fields:
        ok, reason = _check_frontmatter(
            content, criteria.required_frontmatter_fields, output_file
        )
        if not ok:
            return False, reason

    # STANDARD stops here
    if tier == "STANDARD":
        return True, None

    # STRICT: semantic checks
    if criteria.semantic_checks:
        for check in criteria.semantic_checks:
            result = check.check_fn(content)
            if result is not True:
                detail = result if isinstance(result, str) else check.failure_message
                return (
                    False,
                    f"Semantic check '{check.name}' failed: {detail}",
                )

    return True, None


_FRONTMATTER_RE = re.compile(
    r"^---[ \t]*\n(.*?)\n---[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

# Top-level key: value lines (no leading indentation, at least one non-space,
# non-dash word char before the colon). Nested list items (``  - id: M1``)
# and continuation lines inside a list value are intentionally ignored here
# because only top-level keys satisfy ``required_frontmatter_fields`` checks.
_TOPLEVEL_KEY_RE = re.compile(r"^([A-Za-z_][\w\-]*)\s*:", re.MULTILINE)


def _check_frontmatter(
    content: str, required_fields: list[str], output_file: Path
) -> tuple[bool, str | None]:
    """Extract and validate YAML frontmatter fields.

    Uses a non-greedy ``---`` delimiter pair (with ``re.DOTALL``) so nested
    YAML structures — list items like ``  - id: M1`` and block scalars —
    appear intact inside the captured frontmatter body. Horizontal rules
    (``---`` with no ``key: value`` content between delimiters) are rejected
    by a post-match check that requires at least one top-level ``key:`` line.
    Conversational preamble, CONV comments, and any other pre-frontmatter
    lines are tolerated because ``re.search`` scans from any line start.
    """
    # Scan every ``---`` delimiter pair; accept the first one whose body
    # contains at least one top-level ``key:`` line. This rejects pure
    # horizontal rules while still accepting YAML frontmatter that sits
    # after preamble / CONV comments.
    frontmatter_text: str | None = None
    for match in _FRONTMATTER_RE.finditer(content):
        body = match.group(1)
        if _TOPLEVEL_KEY_RE.search(body):
            frontmatter_text = body
            break

    if frontmatter_text is None:
        return False, f"YAML frontmatter not found in {output_file}"

    found_keys = set(_TOPLEVEL_KEY_RE.findall(frontmatter_text))

    for field in required_fields:
        if field not in found_keys:
            return (
                False,
                f"Missing required frontmatter field '{field}' in {output_file}",
            )

    return True, None
