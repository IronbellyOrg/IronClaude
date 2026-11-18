"""The only two accepted approval texts, and the worker's ``check-approval``.

The short form is ``approved``. The long form is
``approved <record-id> plan-sha256=<64 hex>``, with the record id
``ap-<issue>-plan-<first 12 hex of the plan hash>`` so it is the same for the
same (issue, stage, plan version). Both are matched as the whole text with no
trimming. This module returns closed result words only; it prints nothing and
returns no file text.
"""

from __future__ import annotations

import re
from pathlib import Path

from .plan_hash import PlanHashError, compute

SHORT = "approved"
_LONG = re.compile(
    r"approved (ap-([1-9][0-9]*)-plan-([0-9a-f]{12})) plan-sha256=([0-9a-f]{64})"
)

OK = "ok"
REFUSED_BARE = "refused:bare"
REFUSED_MISMATCH = "refused:mismatch"
REFUSED_MALFORMED = "refused:malformed"


def record_id(issue: int, plan_hash: str) -> str:
    return f"ap-{issue}-plan-{plan_hash[:12]}"


def parse(text: str) -> tuple[str, str | None, str | None]:
    """Return ``("short", None, None)``, ``("long", record_id, hash)`` or ``("none", None, None)``."""
    if text == SHORT:
        return ("short", None, None)
    match = _LONG.fullmatch(text)
    if match:
        return ("long", match.group(1), match.group(4))
    return ("none", None, None)


def check(
    report_dir: str | Path, names: list[str], line: str, issue: int | None = None
) -> str:
    """Return one closed result word for the worker's approval line."""
    kind, rid, claimed = parse(line)
    if kind == "none":
        return REFUSED_MALFORMED
    if kind == "short":
        return REFUSED_BARE  # a bare word is acceptable only for the comment channel
    try:
        _, digest = compute(report_dir, names)
    except PlanHashError as exc:
        return f"refused:{exc.reason}"
    assert rid is not None and claimed is not None
    expected_prefix = rid.rsplit("-", 1)[1]
    if claimed != digest or expected_prefix != digest[:12]:
        return REFUSED_MISMATCH
    if issue is not None and not rid.startswith(f"ap-{issue}-plan-"):
        return REFUSED_MISMATCH
    return OK
