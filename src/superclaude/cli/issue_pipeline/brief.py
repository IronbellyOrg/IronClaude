"""Build the plan-writing worker's brief from a fixed template (plan Task 7).

The output is the Task spec the coordinator passes to ``worker-start --spec``, in the brief
layout of ``src/superclaude/core/WORKER-CONTRACT.md`` section 5. The only inputs are the issue
number (a validated integer) and two values read from the claim's summary, the type and the
complexity, each checked against a closed set. No issue text can reach the brief: the template
holds every other character. Only the three Feature rows are built; type ``bug`` is refused.
The rows stop before ``/sc:implement`` and ``/task``.
"""

from __future__ import annotations

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


def build(issue: object, type_: object, complexity: object) -> str:
    """Return the brief for a Feature issue, or raise ``BriefRefused`` with a closed reason."""
    if not valid_issue_number(issue):
        raise BriefRefused("bad-issue")
    if type_ not in TYPES:
        raise BriefRefused("bad-type")
    if type_ == "bug":
        raise BriefRefused("type-not-supported")
    if complexity not in COMPLEXITIES:
        raise BriefRefused("bad-complexity")
    sections = _sections()
    lines = [*sections["head"], *sections[str(complexity)]]
    return "\n".join(lines).replace("{N}", str(issue)) + "\n"
