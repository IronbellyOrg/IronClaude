"""The hold and the acceptance check on issues (design 4.11).

An issue with no plan is not ready (owner ruling 23). This module holds what is
pure about that rule:

* ``plan_check(body)``: the one definition of "the three plan sections are
  filled in". The verb ``superclaude orchestrator plan-check`` imports it, so
  there is one check. It reads text only: no model and no GitHub call.
* the six-row decision table (``table_row``) and the transitions of one
  ``Hold`` entry (``new_hold``, ``restart_hold``, ``with_evidence``,
  ``plan_request_due``);
* the reads of Orca for the evidence of plan work elsewhere (E4).

The module never posts a comment (ruling 33): the only writes of the hold are
the label add and the label remove, and ``github.LabelWriter`` makes them.
Where the cycle's step 7a is not pure (the live read of row 5, the evidence
reads, the label writes) it lives in ``cycle.py`` and calls these functions.

``plan_check`` reads a heading line as written: ``## Priority``, ``## Fix
approach`` and ``## Test plan``, with trailing white space ignored and no other
change of case or spacing, because plan mode (PR P) appends exactly these
lines. A heading inside a fenced code block is not told apart from a heading
outside one (the format of #651 has none).

A section ends at the next ``## `` heading, at the hidden create marker
``<!-- sc:issue:create ... -->`` (finding F17 of issue 675: text after the
marker is not part of the section) or at the end of the body.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from datetime import datetime, timedelta

from .predicates import BACKLOG_LABEL, HOLD_LABEL
from .record import Hold
from .runner import CommandResult, Runner

__all__ = [
    "BACKLOG_LABEL",
    "HOLD_LABEL",
    "HOLD_QUIET_MINUTES",
    "PLAN_CALL_MAX_MINUTES",
    "PlanCheck",
    "plan_check",
    "table_row",
    "new_hold",
    "with_evidence",
    "quiet_since",
    "plan_request_due",
    "session_evidence",
]

HOLD_QUIET_MINUTES = 60
"""Minutes of quiet before the plan request goes out (ruling 23: one hour, not 30)."""

PLAN_CALL_MAX_MINUTES = 60
"""Minutes a ``taken`` plan call may stay unfinished before ``plan_stuck`` (this design's value)."""

SECTIONS = (
    ("priority", "## Priority"),
    ("fix_approach", "## Fix approach"),
    ("test_plan", "## Test plan"),
)
"""The closed tokens of ``missing`` and the heading line each one names."""

_COMMENT = re.compile(r"<!--.*?(?:-->|\Z)", re.DOTALL)
_CREATE_MARKER = re.compile(r"^\s*<!--\s*sc:issue:create\b")
_NOT_KNOWN = "not known yet"


@dataclass(frozen=True)
class PlanCheck:
    """The result of ``plan_check``: ``ok`` and the closed tokens that are ``missing``."""

    ok: bool
    missing: tuple[str, ...]


def _sections(lines: list[str], heading: str) -> list[str]:
    """The text of every section that starts at a line equal to ``heading``."""
    found: list[list[str]] = []
    open_section: list[str] | None = None
    for text_line in lines:
        stripped = text_line.rstrip()
        if stripped == heading:
            open_section = []
            found.append(open_section)
        elif open_section is not None:
            if stripped.startswith("## ") or _CREATE_MARKER.match(stripped):
                open_section = None
            else:
                open_section.append(text_line)
    return ["\n".join(section) for section in found]


def plan_check(body: object) -> PlanCheck:
    """Say whether the three plan sections of an issue body are filled in (4.11 point 1).

    Each of ``## Priority``, ``## Fix approach`` and ``## Test plan`` must occur
    exactly once, and the section under it, with HTML comments and white space
    removed, must not be empty and must not be only "Not known yet" in any
    letter case. ``missing`` lists, in this order, the tokens ``priority``,
    ``fix_approach`` and ``test_plan`` of every section that is absent,
    repeated, empty or "Not known yet". A body that is not text counts as empty.
    It does not say whether the plan is good.
    """
    lines = body.splitlines() if isinstance(body, str) else []
    missing: list[str] = []
    for token, heading in SECTIONS:
        found = _sections(lines, heading)
        if len(found) != 1:
            missing.append(token)
            continue
        text = _COMMENT.sub("", found[0]).strip()
        if not text or text.casefold() == _NOT_KNOWN:
            missing.append(token)
    return PlanCheck(ok=not missing, missing=tuple(missing))


def table_row(*, backlog: bool, passes: bool, label: bool, entry: Hold | None) -> int:
    """The row (1 to 6) of the decision table of 4.11 point 3 that applies to an S1 issue.

    ``backlog`` is ``hold:backlog`` on the row, ``passes`` the ``plan_check``
    result, ``label`` is ``hold:plan`` on the row and ``entry`` the issue's
    ``holds`` entry (or None).

    1. ``hold:backlog``: skip, nothing else, ever.
    2. passes and no label: clear (any ``holds`` entry is dropped, finding F1 of
       issue 675: an issue that passes with no label and still has a ``held``
       entry is clear).
    3. passes and the label: remove the label, drop the entry.
    4. fails, no label, no entry: add the label, start the hold.
    5. fails, no label, an entry: a hand took the label off.
    6. fails and the label: the issue is held.
    """
    if backlog:
        return 1
    if passes:
        return 3 if label else 2
    if label:
        return 6
    return 4 if entry is None else 5


def new_hold(now: datetime, row_updated_at: datetime, missing: tuple[str, ...]) -> Hold:
    """A fresh ``held`` entry whose quiet clock starts ``now`` (rows 4 and 6).

    ``seen_updated_at`` is the row's own ``updated_at``, so the label that a
    person placed (or the poll's own write, after its re-read) is not evidence.
    A hand that puts the label back after a removal by hand gets a fresh entry
    too: ``first_held_at`` restarts and every field of the old plan request is
    cleared (finding F20 of issue 675), so the second hold has its own one
    request.
    """
    return Hold(
        state="held",
        first_held_at=now,
        seen_updated_at=row_updated_at,
        missing=missing,
    )


def with_evidence(hold: Hold, when: datetime, kind: str) -> Hold:
    """Record a signal of plan work: later of the old ``last_evidence_at`` and ``when``.

    ``kind`` is ``edit``, ``branch``, ``pull_request`` or ``session``; it names
    the signal that holds the issue (``status`` prints it, K26). An older signal
    changes nothing. ``seen_updated_at`` follows an ``edit``.
    """
    if hold.last_evidence_at is not None and when <= hold.last_evidence_at:
        return hold
    seen = when if kind == "edit" else hold.seen_updated_at
    return replace(
        hold, last_evidence_at=when, evidence_kind=kind, seen_updated_at=seen
    )


def quiet_since(hold: Hold) -> datetime:
    """The later of ``first_held_at`` and ``last_evidence_at``: where the quiet hour starts."""
    if hold.last_evidence_at is not None and hold.last_evidence_at > hold.first_held_at:
        return hold.last_evidence_at
    return hold.first_held_at


def plan_request_due(hold: Hold, now: datetime) -> bool:
    """True when the hour has run and no plan request was ever recorded for this hold.

    ``plan_requested_at`` is set once and never cleared, so a restart of the poll
    or a second poll process finds it set and sends nothing (4.11 point 5).
    """
    if hold.state != "held" or hold.plan_requested_at is not None:
        return False
    return now - quiet_since(hold) >= timedelta(minutes=HOLD_QUIET_MINUTES)


# --- E4: a linked session (the Orca reads of the evidence) ---------------------


def _orca_found(result: CommandResult) -> bool | None:
    """True or False for a clean Orca answer; None when the answer cannot be read."""
    if result.timed_out or result.spawn_error is not None:
        return None
    try:
        reply = json.loads(result.stdout) if result.stdout.strip() else None
    except (ValueError, RecursionError):
        reply = None
    if result.returncode == 0:
        if not isinstance(reply, dict) or reply.get("ok") is False:
            return None
        found = reply.get("result", reply)
        if isinstance(found, dict) and "worktrees" in found:
            found = found["worktrees"]
        if isinstance(found, dict) and "matches" in found:
            found = found["matches"]
        return bool(found)
    # A non-zero exit is "not found" only when Orca says so in its error code.
    error = reply.get("error") if isinstance(reply, dict) else None
    text = json.dumps(error) if error is not None else result.stderr
    return False if "not_found" in text or "no_match" in text else None


def session_evidence(
    runner: Runner, orca: str | None, number: int, issue_url: str, timeout: float
) -> bool | None:
    """E4: is a worktree or a reference of the issue known to Orca?

    Runs ``orca worktree show --worktree issue:<N> --json`` and then
    ``orca reference find <issue url> --json``. True when either finds one,
    False when both answer "none", and None when an answer cannot be read (the
    poll then holds the request back for this cycle and tries again). The reply
    shapes are UNVERIFIED until the live test (U9); the tests pin them with
    ``_assumed_shape`` fixtures.
    """
    if orca is None or not isinstance(number, int) or number < 1:
        return None
    if not re.fullmatch(
        r"https://github\.com/[A-Za-z0-9._/-]{1,200}/issues/[1-9][0-9]{0,8}", issue_url
    ):
        return None
    answers = []
    for argv in (
        [orca, "worktree", "show", "--worktree", f"issue:{number}", "--json"],
        [orca, "reference", "find", issue_url, "--json"],
    ):
        answers.append(_orca_found(runner.run(argv, timeout)))
    if True in answers:
        return True
    if None in answers:
        return None
    return False
