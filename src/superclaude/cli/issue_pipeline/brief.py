"""Build the coordinator's worker brief from a fixed template (plan Tasks 7 and 11).

The output is the Task spec the coordinator passes to ``worker-start --spec``, in the brief
layout of ``src/superclaude/core/WORKER-CONTRACT.md`` section 5. It is used only at launch
level ``none``. The inputs are the issue number (a validated integer), the stage word of the
issue's Status (research, spec, plan or debug) and, for the spec stage, the route read from the
``spec-route:`` line of the claim's ``issue-summary.md`` (design or brainstorm), each checked
against a closed set. No issue text can reach the brief: the template holds every other
character. The rows stop before ``/sc:implement`` and ``/task``, and the debug row has no ``--fix``.
"""

from __future__ import annotations

import re
from importlib import resources

from superclaude.cli.issue_watch.predicates import valid_issue_number

STAGES = ("research", "spec", "plan", "debug")
ROUTES = ("design", "brainstorm")


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
    issue: object, stage: object, route: object = None, nonce: object = None
) -> str:
    """Return the brief for one Status of an issue, or raise ``BriefRefused`` with a closed reason.

    ``route`` is required for the spec stage and refused for every other stage. ``nonce`` is
    the launch nonce a governed worker is bound with (the coordinator gets it from
    ``orca_worktree.py pending``); only then does the brief carry the one
    ``[sc-launch:v1:<nonce>]`` marker line. The brief of the one G1 test issue has none.
    """
    if not valid_issue_number(issue):
        raise BriefRefused("bad-issue")
    if stage not in STAGES:
        raise BriefRefused("bad-stage")
    if stage == "spec":
        if route not in ROUTES:
            raise BriefRefused("bad-route")
        row = f"spec-{route}"
    else:
        if route is not None:
            raise BriefRefused("bad-route")
        row = str(stage)
    if nonce is not None and not (isinstance(nonce, str) and _NONCE.fullmatch(nonce)):
        raise BriefRefused("bad-nonce")
    sections = _sections()
    marker = sections["marker"] if nonce is not None else []
    lines = [*sections["head"], *marker, *sections[row]]
    text = "\n".join(lines).replace("{N}", str(issue)).replace("{STAGE}", str(stage))
    return text.replace("{NONCE}", str(nonce)) + "\n"
