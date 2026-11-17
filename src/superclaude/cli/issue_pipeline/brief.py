"""Build the plan-writing worker's brief from a fixed template (plan Task 7).

The output is the Task spec the coordinator passes to ``worker-start --spec``, in the brief
layout of ``src/superclaude/core/WORKER-CONTRACT.md`` section 5. The only inputs are the issue
number (a validated integer) and two values read from the claim's summary, the type and the
complexity, each checked against a closed set. No issue text can reach the brief: the template
holds every other character. Only the three Feature rows are built; type ``bug`` is refused.
The rows stop before ``/sc:implement`` and ``/task``.
"""

from __future__ import annotations

import re
from importlib import resources

from superclaude.cli.issue_watch.predicates import valid_issue_number

TYPES = ("feature", "bug")
COMPLEXITIES = ("simple", "medium", "complex")


class BriefRefused(Exception):
    """A closed refusal; no brief is produced. ``reason`` never holds input text."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def _sections() -> dict[str, list[str]]:
    text = (
        resources.files(__package__)
        .joinpath("templates/worker-brief.txt")
        .read_text(encoding="utf-8")
    )
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    for line in text.splitlines():
        if line.startswith("#") or not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            current = sections.setdefault(line[1:-1], [])
        elif current is not None:
            current.append(line)
    return sections


_NONCE = re.compile(r"[0-9a-f]{32}")


def build(
    issue: object, type_: object, complexity: object, nonce: object = None
) -> str:
    """Return the brief for a Feature issue, or raise ``BriefRefused`` with a closed reason.

    ``nonce`` is the launch nonce a governed worker is bound with (the coordinator gets
    it from ``orca_worktree.py pending``); only then does the brief carry the one
    ``[sc-launch:v1:<nonce>]`` marker line. The brief of the one G1 test issue has none.
    """
    if not valid_issue_number(issue):
        raise BriefRefused("bad-issue")
    if type_ not in TYPES:
        raise BriefRefused("bad-type")
    if type_ == "bug":
        raise BriefRefused("type-not-supported")
    if complexity not in COMPLEXITIES:
        raise BriefRefused("bad-complexity")
    if nonce is not None and not (isinstance(nonce, str) and _NONCE.fullmatch(nonce)):
        raise BriefRefused("bad-nonce")
    sections = _sections()
    marker = sections["marker"] if nonce is not None else []
    lines = [*sections["head"], *marker, *sections[str(complexity)]]
    text = "\n".join(lines).replace("{N}", str(issue))
    return text.replace("{NONCE}", str(nonce)) + "\n"
