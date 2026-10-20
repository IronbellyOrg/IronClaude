"""Shared stdlib-only text primitives for the swarm recipe modules.

Private leaf: imports only ``re`` and ``datetime`` (annotation only). It
holds no caps, defaults, policy, registry or package types and never
reads a clock -- each recipe keeps its own ``iso_now`` clock seam and
passes the acquired value to :func:`format_timestamp`.
"""

from __future__ import annotations

import re
from datetime import datetime


def format_timestamp(value: datetime) -> str:
    """Format ``value`` as the recipes' second-resolution UTC timestamp."""
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def yaml_str(v: str) -> str:
    """Double-quote a scalar for safe single-line YAML emission."""
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def strip_frontmatter(text: str) -> str:
    """Drop a leading ``---``-delimited YAML frontmatter block, if any."""
    if text.lstrip().startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def extract_section(text: str, heading: str, cap: int) -> str:
    m = re.search(
        rf"^#+\s*{re.escape(heading)}\s*$", text, re.IGNORECASE | re.MULTILINE
    )
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"^#+\s", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(body.split())[:cap]


def parse_confidence(cell: str) -> str:
    """Reformat a confidence cell.

    Extract the first digit-run and clamp to ``[0, 100]``. Qualitative
    labels with no digits are returned whitespace-collapsed. Empty /
    pure-whitespace input returns an empty string.
    """
    if not cell or not cell.strip():
        return ""
    m = re.search(r"\d+", cell)
    if m:
        return str(max(0, min(100, int(m.group()))))
    return " ".join(cell.split())
