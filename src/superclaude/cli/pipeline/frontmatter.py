"""The single canonical frontmatter parser (Contract #6, §MVR §1).

Before R1.6 the pipeline carried two divergent frontmatter parsers that
could return *different* parses of the same artifact and therefore *different*
gate verdicts:

- ``roadmap/gates.py:_parse_frontmatter`` -- required ``---`` at the start of
  the (lstripped) content, split top-level ``key: value`` lines into a
  quote-stripped ``dict[str, str]``, used by the 23 STRICT-tier semantic
  checks to read field *values*.
- ``pipeline/gates.py:_check_frontmatter`` -- a preamble-tolerant regex scan
  that accepted the first ``---`` ... ``---`` block containing a top-level
  ``key:`` line and validated *required field presence* (keys only).

That divergence is exactly the Contract #6 brittleness driver. This module
collapses both into ONE parser. It lives under ``pipeline/`` (not
``roadmap/``) so that BOTH ``pipeline/gates.py`` and ``roadmap/gates.py`` can
import it without violating the import-direction invariants:

- **NFR-007**: ``pipeline/`` must not import ``roadmap/`` -- this module
  imports nothing from ``roadmap/`` (or ``sprint/``).
- **NFR-005**: ``roadmap/gates.py`` must not import ``pipeline/gates.py``
  enforcement code -- it imports this pure-parsing module instead, which is
  not the gate-enforcement module.

``extract_frontmatter`` is a behavioral **superset** of the two parsers it
replaces:

- Preamble-tolerant: scans for the first ``---`` ... ``---`` block that
  contains at least one top-level ``key:`` line, so CONV comments or other
  preamble before the frontmatter are tolerated (the former
  ``_check_frontmatter`` behavior, a strict generalization of the former
  ``_parse_frontmatter`` "``---`` at start" behavior).
- Returns a ``dict`` of *top-level* ``key -> value`` with values stripped of
  surrounding whitespace and matching outer YAML quotes (the former
  ``_parse_frontmatter`` behavior). Nested / indented lines (e.g.
  ``  - id: M1``) are intentionally ignored -- only top-level keys satisfy
  ``required_frontmatter_fields`` and the scalar field look-ups in the 23
  roadmap semantic checks.
- Returns ``None`` when no frontmatter block is present (callers map ``None``
  to "frontmatter not found").

NFR-003 analogue: pure Python, no subprocess / no LLM invocation.
"""

from __future__ import annotations

import re

# Non-greedy ``---`` delimiter pair (with ``re.DOTALL``) so nested YAML
# structures -- list items like ``  - id: M1`` and block scalars -- appear
# intact inside the captured frontmatter body. Horizontal rules (``---`` with
# no ``key: value`` content between delimiters) are rejected by the
# top-level-key post-check below. ``re.MULTILINE`` lets the scan start from any
# line, so conversational preamble / CONV comments before the frontmatter are
# tolerated.
_FRONTMATTER_RE = re.compile(
    r"^---[ \t]*\n(.*?)\n---[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

# Top-level ``key:`` lines (no leading indentation, at least one non-space,
# non-dash word char before the colon). Nested list items (``  - id: M1``) and
# continuation lines inside a list value are intentionally ignored -- only
# top-level keys satisfy ``required_frontmatter_fields`` checks and the scalar
# field look-ups in the roadmap semantic checks.
_TOPLEVEL_KEY_RE = re.compile(r"^([A-Za-z_][\w\-]*)\s*:", re.MULTILINE)


def _strip_yaml_quotes(value: str) -> str:
    """Strip matching outer YAML quotes (single or double) from a value.

    Handles the common case where LLMs wrap values in quotes::

        '"1:1"'  -> '1:1'
        "'1:1'"  -> '1:1'

    Does NOT strip if quotes are unmatched::

        '"1:1'   -> '"1:1'   (unmatched -- leave as-is)
    """
    if len(value) >= 2:
        if (value[0] == '"' and value[-1] == '"') or (
            value[0] == "'" and value[-1] == "'"
        ):
            return value[1:-1]
    return value


def extract_frontmatter(content: str) -> dict[str, str] | None:
    """Extract top-level YAML frontmatter key/value pairs from ``content``.

    Returns a dict of top-level ``key -> value`` (values stripped of
    whitespace and matching outer YAML quotes), or ``None`` if no frontmatter
    block is found. This is the single canonical frontmatter parser
    (Contract #6) -- every gate-layer caller in ``pipeline/`` and ``roadmap/``
    routes through this function.
    """
    # Normalize line endings before matching. The old roadmap parser used
    # ``str.splitlines()`` (which treats CRLF/CR as line breaks), so a CRLF
    # artifact parsed fine; the ``_FRONTMATTER_RE`` closing delimiter
    # (``\n---[ \t]*$``) would otherwise reject a ``---\r\n`` block and flip a
    # passing gate to FAIL. Normalizing keeps the canonical parser a true
    # behavioral superset of both legacy parsers.
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    frontmatter_text: str | None = None
    for match in _FRONTMATTER_RE.finditer(content):
        body = match.group(1)
        if _TOPLEVEL_KEY_RE.search(body):
            frontmatter_text = body
            break

    if frontmatter_text is None:
        return None

    result: dict[str, str] = {}
    for line in frontmatter_text.splitlines():
        # Only top-level ``key: value`` lines (column-0 key). Indented list
        # items and continuation lines are skipped.
        if not _TOPLEVEL_KEY_RE.match(line):
            continue
        key, _, value = line.partition(":")
        result[key.strip()] = _strip_yaml_quotes(value.strip())
    return result
