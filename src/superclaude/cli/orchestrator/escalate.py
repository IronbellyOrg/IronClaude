"""The verb ``superclaude orchestrator escalate``: reach Clay, in one of nine ways, and nowhere else (design 5.6, 5.9, 5.12).

    escalate --issue <owner/repo#N> --row <1 to 9> --content-file <file>
             (--question <slug> | --merge-safety-pr <N> --head-sha <sha>) [--interrupt <dispatch id>]
    escalate --flush-held --repo <owner/repo>

The orchestrator decides everything that is not in the table of 5.6 and records "Decided by
the orchestrator: ..." in the entry. A case reaches Clay only when it fits one row, and the
call names that one row. A call that names no row or an unknown row exits 2 and writes and
sends nothing: ``decide it yourself and record it``. The rules are on from the start (ruling
24): there is no ``warn`` phase and no setting that turns them down.

What one call does, in this order
---------------------------------
1. Checks everything that can be checked without a side effect (the row, the question key, the
   content file, the naming rule of 5.12 on every text it will write, the entry file, and for
   ``--interrupt`` the Dispatch). A refusal here writes nothing and sends nothing.
2. Writes the escalation into the issue's own entry in the living report, the ``needs`` slot of
   ``.dev/coordinator/orchestrated/<owner>__<repo>__<N>.json`` (ruling 24: the section of its own
   issue, never a separate list). The block holds, in this order, the question, ``Why this reaches
   you:`` (the row in words, with its number), ``Low-stakes options:``, the options, the key facts,
   the recommendation, what happens after each answer, ``If you do not answer:`` (what stays blocked
   and what keeps going; it never names a default or a later action), the links and a status line
   for each of the three channels. Its first line is ``Entry <entry id> (row N)``, so Clay can cite
   the entry id in his answer. Each question has its own entry id (finding F48 of issue 675): it is
   made from the question key, so a rerun of the same issue, row and question lands on the same id.
3. Records the question (``questions.record_question``: the key ``<issue>:<row>:<question>``, or
   ``merge_safety:<PR>:<head sha>``, the row and the low-stakes options) and moves the entry's
   edit time (``questions.touch``). ``answer-check`` refuses an answer older than that time.
4. With ``--interrupt``: exactly one ``orca terminal send --interrupt`` for that Dispatch, after
   the entry is written and not before (the order is a test), and nothing else: it never closes the
   terminal, stops the Dispatch or kills the session.
5. Creates the Orca decision gate (``gate-create``) when the issue has a Task.
6. Sends the notice: a ClickUp DM, or, without ``CLICKUP_API_TOKEN`` or when the DM fails, the Orca
   unread mark of the orchestrator repo. The daily cap (``reach_daily_max``) can hold the notice
   back; the entry and the gate are written in any case, so nothing is lost (FR-10).
7. Writes the entry again with the final status of each channel and moves the notice time.

Answers to the findings that touch this text
--------------------------------------------
* Finding F5 of issue 665 (``gate-create`` needs a Task and waves 0 to 3 have none): the gate is
  created only when the state file of the issue records a Task (``ids.task_id``). Without one the
  gate line reads ``none, no Task yet``; the entry and the notice still go out. No Task is made up.
* Finding F10 of issue 675 (a failed plan call went into the separate list): ``escalate`` makes the
  issue's entry itself when none exists (the fields ``url``, ``kind`` and ``last_update`` and the
  ``needs`` slot, nothing else). Wave 3's ``report-entry`` adds the rest and must keep the ``needs``
  text it finds. The coordinator's own list stays for what belongs to no issue.
* Finding F22 of issue 675 (the order of the ``failed`` plan record and its escalation): escalate
  first, then write ``failed``. A rerun of ``escalate`` for the same question is harmless, so a
  restart that finds the record still ``in_progress`` raises it again and then writes ``failed``.
* Finding F23 of issue 675 (an invalid ``reach_daily_max``): it is read as 0, which means no cap, as
  spec 4.4 and PR A's validation read it; that is an exception to "never a guess", stated here. The
  cap only holds notices back and never drops an entry, so failing open loses nothing.
* Finding F26 of issue 675: a "free place" is a count of notices below ``reach_daily_max`` in the
  last 24 hours for the ``<short>`` of the repo (``FREE_PLACE``).
* Finding F27 of issue 675: the cases that the audit, the merge gate and the closeout send to rows 8
  and 9 are data in ``ROWS`` (``cases``) and a test fails when one is missing from its row.
* Finding F29 of issue 675: ``--interrupt`` takes only the Dispatch that the issue's own state file
  records (``ids.dispatch_id``), and only when that file belongs to this orchestrator. A Dispatch of
  another Run, a Dispatch taken from quoted worker text, or an issue with no state file is refused
  with exit 2 and nothing is written. Whether Orca agrees that the Dispatch is in this orchestrator's
  Run is not asked (UNVERIFIED: the output of ``worker-show`` is not designed).
* Finding F30 of issue 675 (what ``--interrupt`` sends, and the typing hold): what the flag sends to a
  coding-assistant session is UNVERIFIED (U40 class). The decision, as spec 5.9 N7 and its test say:
  the interrupt is exempt from the 60-second typing hold and from the empty-``draft`` part of that
  rule, because it goes into a turn that is running. The verb therefore never reads the screen. If a
  local run shows that the flag clears unsent text, drop the exemption for a non-empty ``draft``:
  read the screen first and hold the interrupt. A test asserts the present choice.

The one-send rule: a rerun with the same entry and Dispatch never sends a second interrupt (the
action log holds an ``intent`` row before the send), because a send is never repeated blind. A new
try needs a new question.

The daily cap: ``.orchestrator/asks.json``
------------------------------------------
One row per notice: time, ``<short>`` of the repo, issue key, row number, entry id, ``state`` and
``delivered`` (no text, at most 500 rows). ``state`` is ``counted`` (a notice that went out or is on
its way: it counts for 24 hours), ``held`` (over the cap, waiting for a free place, never dropped) or
``released`` (a held notice that went out inside a digest). A row is written under
``.orchestrator/state.lock`` BEFORE the send, so a crash between the count and the send keeps the
count (the reservation rule); ``delivered`` is ``null`` until the send is confirmed. Held notices are
sent as one DM at the next call that finds a free place, or by ``--flush-held`` (the hourly pass).
The file is written only by this module. A file that cannot be read is never overwritten
(``asks_unreadable``, exit 4; the entry and the gate are still written).

Limits and UNVERIFIED points
----------------------------
The ClickUp DM goes through the installed report skill's own ``clickup.send_dm`` (no second copy of
the API calls): this verb runs it as a short Python call by the skill's installed path. That it works
from here is UNVERIFIED (U36 and U38 class; the tests use a stub script). The output of
``orca orchestration gate-create`` is not designed: the gate id is read from the usual places and the
line says ``created`` when none is found. ``reach_daily_max`` is read from ``repos.yaml`` through PR
A's validator; a file that cannot be read is no cap.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Final

import click

from superclaude.cli.issue_watch import repos
from superclaude.cli.issue_watch.predicates import (
    file_key,
    format_utc,
    parse_utc,
    valid_issue_number,
    valid_operation_id,
    valid_repo,
)
from superclaude.cli.issue_watch.runner import Runner

from . import actions, common, ext, questions, state
from .limits import ESCALATE_CALLER
from .names import names_check
from .state import (
    EXIT_CONFLICT,
    EXIT_INVALID,
    EXIT_UNREADABLE,
    StateError,
)

EXIT_EXTERNAL: Final = ext.EXIT_EXTERNAL

# --- the nine rows of 5.6 -------------------------------------------------------------------


@dataclass(frozen=True)
class Row:
    """One row of the table of what reaches Clay (5.6).

    ``needs`` finishes the sentence "Why this reaches you: Row N, ..."; ``was`` holds the rules
    of issue 655 section 9 that the row replaced; ``cases`` lists named cases that other parts of
    the design send to the row (finding F27 of issue 675).
    """

    number: int
    needs: str
    was: tuple[int, ...]
    low_stakes_allowed: bool
    cases: tuple[str, ...] = ()


ROWS: Final[tuple[Row, ...]] = (
    Row(1, "your own identity", (1,), False),
    Row(2, "a secret", (), False),
    Row(3, "money", (1,), False),
    Row(4, "a legal act", (), False),
    Row(
        5,
        "something that cannot be undone, or that changes shared settings",
        (1, 2),
        False,
    ),
    Row(6, "other people's access or data", (), False),
    Row(7, "a breaking change", (), False),
    Row(
        8,
        "a decision only you can make",
        (3, 4, 5, 6),
        True,
        cases=(
            "a scope that creeps into peripheral features",
            "a question still unanswered after the issue, the code, the docs and a web search",
            "a choice between options that changes what the product does",
            "merging over a failing check",
            "a pull request that changes a merge-safety file",
            "audit violation AU4a",
            "audit violation AU4c",
            "audit violation AU5",
        ),
    ),
    Row(
        9,
        "you because it is stuck and nobody else can unstick it",
        (7, 8),
        True,
        cases=(
            "a worker that the check-in, the typed key and the approval did not unstick",
            "a failed handoff",
            "a pull request held because a listed review agent never ran or finished",
            "a merge that your rights or the repo's protection forbid",
            "changes_requested",
            "closed_unmerged",
            "closeout_unclear",
            "closeout_failed",
            "a hand-back that hit its bound",
        ),
    ),
)
"""The only list of what reaches Clay. The old rules 1 to 8 each appear in a ``was`` column."""

ROW_NUMBERS: Final = tuple(r.number for r in ROWS)
DECIDE_MESSAGE: Final = (
    "This case fits none of the nine rows of the table of what reaches Clay, so it does not "
    "reach him: decide it yourself and record it in the report entry as 'Decided by the "
    "orchestrator: ...', then go on."
)

# --- limits ---------------------------------------------------------------------------------

WINDOW: Final = timedelta(hours=24)
"""The cap counts notices in the last 24 hours."""
MAX_ROWS: Final = 500
ASKS_FILE: Final = "asks.json"
ASKS_SCHEMA: Final = "orchestrator-asks/1"
FREE_PLACE: Final = "a count of notices below reach_daily_max in the last 24 hours, per <short>"
MAX_CONTENT_BYTES: Final = 64 * 1024
MAX_ENTRY_BYTES: Final = 1024 * 1024
MAX_NOTE_CHARS: Final = 500
MAX_DM_CHARS: Final = 1500
CLICKUP_TOKEN_ENV: Final = "CLICKUP_API_TOKEN"
ENTRY_SUBPATH: Final = (".dev", "coordinator", "orchestrated")

_SLUG = re.compile(r"[a-z0-9][a-z0-9_-]{0,39}")
_SHA = re.compile(r"[0-9a-f]{7,64}")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_BLOCK_START = re.compile(r"^Entry ([A-Za-z0-9._-]{1,100}) \(row [1-9]\)$")
_URL = re.compile(r"https://[A-Za-z0-9._~:/?#@!$&*+,;=%-]{1,290}")

WHY = "Why this reaches you:"
LOW = "Low-stakes options:"
NO_ANSWER = "If you do not answer:"
ESCALATION_LINES: Final = (WHY, LOW, NO_ANSWER)

_DEFAULT_WORDS: Final = (
    re.compile(r"\bdefaults?\b", re.I),
    re.compile(
        r"\bwill (?:proceed|go ahead|decide|assume|merge|close|start|take|use|choose|pick|apply|act|continue with)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:after|in|within|for) (?:\d+|one|two|three|a few) ?(?:seconds?|minutes?|mins?|hours?|days?|weeks?)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:timers?|time[- ]?outs?|times out|expires?|automatic(?:ally)?|otherwise|assum(?:e|es|ed|ing)|fall ?back|on its own|by itself|go(?:es)? ahead)\b",
        re.I,
    ),
    re.compile(r"\bthen the orchestrator\b", re.I),
)
"""Words that name a later action, a default or a timer: ``If you do not answer:`` never holds one."""
_BLOCKED_WORD = re.compile(
    r"\b(?:stays?|stayed|waits?|waiting|held|holds?|blocked|unmerged|stopped|paused|"
    r"no worker starts?|does not start|do not start|not start|not merge)\b",
    re.I,
)
"""``If you do not answer:`` must say what stays blocked."""


# --- reading the call -----------------------------------------------------------------------


def parse_row(raw: str | None) -> Row:
    """The row a call names; ``row_missing`` or ``row_unknown`` (exit 2, with the message to decide)."""
    if raw is None or raw == "":
        raise StateError("row_missing", EXIT_INVALID, message=DECIDE_MESSAGE)
    if re.fullmatch(r"[1-9]", raw) is None:
        raise StateError("row_unknown", EXIT_INVALID, message=DECIDE_MESSAGE)
    return ROWS[int(raw) - 1]


def parse_issue(raw: str | None) -> tuple[str, int]:
    """``owner/repo#N`` as ``(repo, number)`` (``invalid_issue``, exit 2)."""
    match = re.fullmatch(r"([^#\s]+)#([0-9]{1,15})", raw or "")
    if match is None or not valid_repo(match[1]) or not valid_issue_number(int(match[2])):
        raise StateError("invalid_issue", EXIT_INVALID)
    return match[1], int(match[2])


def build_key(
    repo: str,
    number: int,
    row: Row,
    question: str | None,
    merge_pr: str | None,
    head_sha: str | None,
) -> str:
    """The question key: ``<issue>:<row>:<question>`` or ``merge_safety:<PR>:<head sha>`` (row 8 only)."""
    if merge_pr is not None or head_sha is not None:
        if question is not None:
            raise StateError("question_ambiguous", EXIT_INVALID)
        if row.number != 8:
            raise StateError("merge_safety_row", EXIT_INVALID)
        if (
            merge_pr is None
            or re.fullmatch(r"[1-9][0-9]{0,9}", merge_pr) is None
            or head_sha is None
            or _SHA.fullmatch(head_sha) is None
        ):
            raise StateError("invalid_merge_safety", EXIT_INVALID)
        return f"merge_safety:{merge_pr}:{head_sha}"
    if question is None or _SLUG.fullmatch(question) is None:
        raise StateError("invalid_question", EXIT_INVALID)
    return f"{file_key(repo, number)}:{row.number}:{question}"


def entry_id_for(repo: str, number: int, row: Row, key: str) -> str:
    """The entry id of one question: ``<short>-<N>-r<row>-<6 hex of the key>``, the same for a rerun."""
    digest = hashlib.sha256(key.encode("ascii")).hexdigest()[:6]
    return f"{repos.short_name(repo)}-{number}-r{row.number}-{digest}"


@dataclass(frozen=True)
class Content:
    """What the orchestrator says to Clay, already checked."""

    question: str
    why: str | None
    options: tuple[tuple[str, str], ...]  # (what it does, what happens after it)
    facts: tuple[str, ...]
    recommendation: str
    blocked: str
    low_stakes: tuple[int, ...]
    links: tuple[tuple[str, str], ...]


def starts_like_a_sentence(text: str) -> bool:
    """The rule of the report's template check for a written line (check.py ``capital``)."""
    t = text.strip().removeprefix("- ").lstrip("*_")
    return (
        not t
        or t[0].isupper()
        or t[0].isdigit()
        or t[0] in "[`\"'("
        or t.startswith("N/A")
    )


def _bad(field: str) -> StateError:
    return StateError("content_invalid", EXIT_INVALID, field=field)


def _line(value: object, field: str, limit: int) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or len(value) > limit
        or _CONTROL.search(value)
        or not starts_like_a_sentence(value)
    ):
        raise _bad(field)
    return value.strip()


def _list(doc: Mapping[str, Any], name: str, low: int, high: int) -> list[Any]:
    value = doc.get(name, [])
    if not isinstance(value, list) or not low <= len(value) <= high:
        raise _bad(name)
    return value


def parse_content(doc: object, row: Row) -> Content:
    """Check the content file: single-line texts, one line for each option, no low-stakes option on rows 1 to 7."""
    if not isinstance(doc, dict):
        raise _bad("content")
    unknown = set(doc) - {
        "question",
        "why",
        "options",
        "facts",
        "recommendation",
        "blocked",
        "low_stakes",
        "links",
    }
    if unknown:
        raise _bad("unknown_field")
    options: list[tuple[str, str]] = []
    for i, item in enumerate(_list(doc, "options", 1, 9)):
        if not isinstance(item, dict) or set(item) != {"text", "after"}:
            raise _bad(f"options[{i}]")
        options.append(
            (_line(item["text"], f"options[{i}].text", 300), _line(item["after"], f"options[{i}].after", 300))
        )
    low = _list(doc, "low_stakes", 0, 9)
    if any(type(n) is not int or not 1 <= n <= len(options) for n in low) or len(set(low)) != len(low):
        raise _bad("low_stakes")
    if low and not row.low_stakes_allowed:
        raise StateError("low_stakes_not_allowed", EXIT_INVALID, row=row.number)
    links: list[tuple[str, str]] = []
    for i, item in enumerate(_list(doc, "links", 0, 10)):
        if (
            not isinstance(item, dict)
            or set(item) != {"title", "url"}
            or not isinstance(item["url"], str)
            or _URL.fullmatch(item["url"]) is None
        ):
            raise _bad(f"links[{i}]")
        title = _line(item["title"], f"links[{i}].title", 100)
        if re.search(r"[\[\]()]", title):
            raise _bad(f"links[{i}].title")
        links.append((title, item["url"]))
    why = doc.get("why")
    return Content(
        question=_line(doc.get("question"), "question", 600),
        why=None if why is None else _line(why, "why", 300),
        options=tuple(options),
        facts=tuple(
            _line(f, f"facts[{i}]", 400) for i, f in enumerate(_list(doc, "facts", 0, 20))
        ),
        recommendation=_line(doc.get("recommendation"), "recommendation", 600),
        blocked=_line(doc.get("blocked"), "blocked", 400),
        low_stakes=tuple(sorted(low)),
        links=tuple(links),
    )


# --- the entry block ------------------------------------------------------------------------


def compose(
    entry_id: str,
    row: Row,
    content: Content,
    *,
    gate: str = "pending",
    notice: str = "pending",
) -> str:
    """The block written into the ``needs`` slot of the issue's entry, one line after another."""
    why = f"Row {row.number}, {row.needs}."
    if content.why:
        why += f" {content.why}"
    lines = [
        f"Entry {entry_id} (row {row.number})",
        f"Question: {content.question}",
        f"{WHY} {why}",
        f"{LOW} " + (", ".join(str(n) for n in content.low_stakes) or "none"),
        "Options:",
        *(f"- {i}. {text}" for i, (text, _) in enumerate(content.options, 1)),
    ]
    if content.facts:
        lines += ["Key facts:", *(f"- {fact}" for fact in content.facts)]
    lines += [
        f"Recommendation: {content.recommendation}",
        "After each answer:",
        *(f"- {i}. {after}" for i, (_, after) in enumerate(content.options, 1)),
        f"{NO_ANSWER} {content.blocked}",
    ]
    if content.links:
        lines += ["Links:", *(f"- [{title}]({url})" for title, url in content.links)]
    lines += [
        "Needs you entry: written",
        f"Orca gate: {gate}",
        f"Notice: {notice}",
    ]
    return "\n".join(lines)


def entry_problems(text: str) -> list[str]:
    """What is wrong with an escalation text (empty means it passes).

    Each of the three lines of 5.6 must be there exactly once, in the order ``Why this reaches you:``,
    ``Low-stakes options:``, ``If you do not answer:``; the last must say what stays blocked and must
    not name a default, a timer or a later action. Every written line must start like a sentence
    (the report's template check, which ``report-entry`` applies to this slot).
    """
    problems: list[str] = []
    lines = text.split("\n")
    positions: list[int] = []
    for prefix in ESCALATION_LINES:
        found = [i for i, line in enumerate(lines) if line.startswith(prefix)]
        if len(found) != 1:
            problems.append(f"the line '{prefix}' is {'missing' if not found else 'repeated'}")
        else:
            positions.append(found[0])
    if len(positions) == 3 and positions != sorted(positions):
        problems.append("the three lines are not in the order of 5.6")
    for line in lines:
        if line.startswith(NO_ANSWER):
            said = line[len(NO_ANSWER) :].strip()
            if _BLOCKED_WORD.search(said) is None:
                problems.append("'If you do not answer:' does not say what stays blocked")
            if any(p.search(said) for p in _DEFAULT_WORDS):
                problems.append("'If you do not answer:' names a default, a timer or a later action")
    for number, line in enumerate(lines, 1):
        if line.strip() and not starts_like_a_sentence(line):
            problems.append(f"line {number} does not start like a sentence")
    return problems


def split_needs(text: str | None) -> tuple[str, list[tuple[str, str]]]:
    """``(text before the first block, [(entry id, block text)])`` of a ``needs`` slot."""
    lines = (text or "").split("\n")
    head: list[str] = []
    blocks: list[tuple[str, list[str]]] = []
    for line in lines:
        match = _BLOCK_START.match(line)
        if match:
            blocks.append((match[1], [line]))
        elif blocks:
            blocks[-1][1].append(line)
        else:
            head.append(line)
    return (
        "\n".join(head).strip(),
        [(i, "\n".join(b).strip("\n")) for i, b in blocks],
    )


def merge_needs(existing: object, entry_id: str, block: str) -> str:
    """The ``needs`` slot with this entry's block put in: replaced where it is, appended when new."""
    head, blocks = split_needs(existing if isinstance(existing, str) else None)
    if head == "N/A":
        head = ""
    placed = False
    out: list[tuple[str, str]] = []
    for ident, text in blocks:
        if ident == entry_id:
            out.append((ident, block))
            placed = True
        else:
            out.append((ident, text))
    if not placed:
        out.append((entry_id, block))
    return "\n\n".join([p for p in [head, *(t for _, t in out)] if p])


# --- the entry file -------------------------------------------------------------------------


def entry_path(root: Path | str, repo: str, number: int) -> Path:
    """``<root>/.dev/coordinator/orchestrated/<owner>__<repo>__<N>.json``."""
    return Path(root).joinpath(*ENTRY_SUBPATH, f"{file_key(repo, number)}.json")


def _check_entry_path(root: Path | str, path: Path) -> None:
    """Refuse a folder or file that is a link: the report's readers refuse them too."""
    walk = Path(root)
    for part in (*ENTRY_SUBPATH, path.name):
        walk = walk / part
        if os.path.islink(walk):
            raise StateError("entry_path_unsafe", EXIT_INVALID)


def _read_entry(path: Path) -> dict[str, Any] | None:
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_ENTRY_BYTES + 1)
    except FileNotFoundError:
        return None
    except OSError:
        raise StateError("entry_unreadable", EXIT_UNREADABLE) from None
    try:
        doc = json.loads(data.decode("utf-8")) if len(data) <= MAX_ENTRY_BYTES else None
    except (ValueError, RecursionError):
        doc = None
    if not isinstance(doc, dict):
        raise StateError("entry_unreadable", EXIT_UNREADABLE)
    return doc


def write_entry(
    root: Path | str, repo: str, number: int, entry_id: str, block: str, now: datetime
) -> None:
    """Put ``block`` into the ``needs`` slot of the issue's entry (made when it does not exist).

    The read, the change and the write happen under ``.orchestrator/state.lock`` and the file is
    replaced whole. Every other field of the entry is kept as it is. An entry that cannot be read is
    never overwritten.
    """
    path = entry_path(root, repo, number)
    _check_entry_path(root, path)
    with state.locked(root):
        doc = _read_entry(path)
        if doc is None:
            doc = {
                "url": f"https://github.com/{repo}/issues/{number}",
                "kind": "orchestrated",
            }
        doc["needs"] = merge_needs(doc.get("needs"), entry_id, block)
        doc["last_update"] = format_utc(now)
        ext.write_json(path, doc)


# --- the asks file (the daily cap) ----------------------------------------------------------

_ASK_KEYS: Final = {"ts", "short", "issue", "row", "entry", "state", "delivered"}
_ASK_STATES: Final = ("counted", "held", "released")


def asks_path(root: Path | str) -> Path:
    """``<root>/.orchestrator/asks.json``."""
    return Path(root) / state.STATE_DIR / ASKS_FILE


def _ask_ok(row: object) -> bool:
    if not isinstance(row, dict) or set(row) != _ASK_KEYS:
        return False
    try:
        parse_utc(row["ts"])
    except (ValueError, TypeError):
        return False
    return (
        isinstance(row["short"], str)
        and re.fullmatch(r"[a-z0-9]{1,12}", row["short"]) is not None
        and isinstance(row["issue"], str)
        and re.fullmatch(r"[A-Za-z0-9._-]+__[A-Za-z0-9._-]+__[0-9]+", row["issue"]) is not None
        and type(row["row"]) is int
        and 1 <= row["row"] <= 9
        and isinstance(row["entry"], str)
        and questions.ENTRY_ID.fullmatch(row["entry"]) is not None
        and row["state"] in _ASK_STATES
        and (row["delivered"] is None or type(row["delivered"]) is bool)
    )


def load_asks(root: Path | str) -> list[dict[str, Any]]:
    """The rows of ``asks.json`` (none when the file is missing); ``asks_unreadable`` (exit 4) otherwise."""
    try:
        with open(asks_path(root), "rb") as handle:
            data = handle.read(MAX_ENTRY_BYTES + 1)
    except FileNotFoundError:
        return []
    except OSError:
        raise StateError("asks_unreadable", EXIT_UNREADABLE) from None
    try:
        doc = json.loads(data.decode("utf-8")) if len(data) <= MAX_ENTRY_BYTES else None
    except (ValueError, RecursionError):
        doc = None
    if (
        not isinstance(doc, dict)
        or doc.get("schema") != ASKS_SCHEMA
        or not isinstance(doc.get("rows"), list)
        or not all(_ask_ok(r) for r in doc["rows"])
    ):
        raise StateError("asks_unreadable", EXIT_UNREADABLE)
    return doc["rows"]


def save_asks(root: Path | str, rows: list[dict[str, Any]]) -> None:
    """Write the rows whole (temporary file and ``rename``, mode 0600)."""
    ext.write_json(asks_path(root), {"schema": ASKS_SCHEMA, "rows": rows})


def counted(rows: Sequence[Mapping[str, Any]], short: str, now: datetime) -> int:
    """The notices of ``short`` that count now: ``counted`` rows younger than 24 hours."""
    return sum(
        1
        for r in rows
        if r["short"] == short
        and r["state"] == "counted"
        and parse_utc(r["ts"]) > now - WINDOW
    )


def has_free_place(
    rows: Sequence[Mapping[str, Any]], short: str, cap: int, now: datetime
) -> bool:
    """A free place (``FREE_PLACE``): no cap, or fewer counted notices than the cap in the last 24 hours."""
    return cap == 0 or counted(rows, short, now) < cap


def _prune(rows: list[dict[str, Any]], now: datetime) -> list[dict[str, Any]]:
    """Drop what no longer counts and is not waiting: old ``counted`` rows and ``released`` rows."""
    return [
        r
        for r in rows
        if r["state"] == "held"
        or (r["state"] == "counted" and parse_utc(r["ts"]) > now - WINDOW)
    ]


def read_cap(root: Path | str, runner: Runner, repo: str) -> int:
    """``reach_daily_max`` of the repo: 0 to 50; 0, absent or unreadable is 0 (no cap; finding F23)."""
    try:
        doc = repos.load_repos(Path(root), runner, ext.CALL_TIMEOUT_S)
    except repos.ReposError:
        return 0
    entry = doc.get(repo)
    return entry.reach_daily_max if entry is not None else 0


def reserve(
    root: Path | str,
    *,
    short: str,
    issue_key: str,
    row: int,
    entry: str,
    cap: int,
    now: datetime,
) -> tuple[dict[str, Any], bool]:
    """Count one notice before it is sent: ``(row, new)``. The same entry is never counted twice.

    The row is ``counted`` when there is a free place and ``held`` when there is not. It is on
    disk when this returns, so a crash before the send keeps the count.
    """
    with state.locked(root):
        rows = load_asks(root)
        for old in rows:
            if old["entry"] == entry:
                return dict(old), False
        rows = _prune(rows, now)
        if len(rows) >= MAX_ROWS:
            raise StateError("asks_full", EXIT_CONFLICT)
        new = {
            "ts": format_utc(now),
            "short": short,
            "issue": issue_key,
            "row": row,
            "entry": entry,
            "state": "counted" if has_free_place(rows, short, cap, now) else "held",
            "delivered": None,
        }
        rows.append(new)
        save_asks(root, rows)
    return dict(new), True


def mark_delivered(root: Path | str, entry: str, delivered: bool) -> None:
    """Record whether the notice of ``entry`` is confirmed (``False``: it can be sent again)."""
    with state.locked(root):
        rows = load_asks(root)
        for old in rows:
            if old["entry"] == entry:
                old["delivered"] = delivered
        save_asks(root, rows)


# --- the three channels ---------------------------------------------------------------------

_DM_SNIPPET: Final = (
    "import sys; sys.path.insert(0, sys.argv[1]); import clickup; "
    "ok, detail = clickup.send_dm(sys.argv[2]); print(bool(ok))"
)


def _report_scripts() -> Path | None:
    """The report skill's scripts folder: the installed copy first, then the project's ``.claude/`` copy."""
    for base in (
        Path.home() / ".claude" / "skills" / "agent-work-report",
        Path.cwd() / ".claude" / "skills" / "agent-work-report",
    ):
        if (base / "scripts" / "clickup.py").is_file():
            return base / "scripts"
    return None


def _send_dm(runner: Runner, root: Path, text: str) -> bool:
    """A ClickUp DM through the report skill's own ``send_dm``; False without a token or a skill."""
    scripts = _report_scripts()
    if not os.environ.get(CLICKUP_TOKEN_ENV) or scripts is None:
        return False
    result = runner.run(
        [sys.executable, "-I", "-c", _DM_SNIPPET, str(scripts), text[:MAX_DM_CHARS]],
        ext.CALL_TIMEOUT_S,
        cwd=str(root),
    )
    return (
        not result.timed_out
        and result.spawn_error is None
        and result.returncode == 0
        and result.stdout.strip() == "True"
    )


def _send_mark(runner: Runner, root: Path, note: str) -> bool:
    """The Orca unread mark with a note on the orchestrator repo's workspace."""
    result = runner.run(
        [
            "orca",
            "worktree",
            "set",
            "--worktree",
            f"path:{root}",
            "--unread",
            "--comment",
            note[:MAX_NOTE_CHARS],
            "--json",
        ],
        ext.CALL_TIMEOUT_S,
    )
    return (
        not result.timed_out and result.spawn_error is None and result.returncode == 0
    )


def send_notice(runner: Runner, root: Path, dm_text: str, note: str) -> str:
    """Reach Clay: ``dm`` (a ClickUp DM), ``mark`` (the unread mark) or ``failed`` (neither)."""
    if _send_dm(runner, root, dm_text):
        return "dm"
    return "mark" if _send_mark(runner, root, note) else "failed"


def _gate_id(stdout: str) -> str:
    """The gate id from the JSON of ``gate-create`` (UNVERIFIED shape), or ``created``."""
    try:
        doc = json.loads(stdout)
    except (ValueError, RecursionError):
        return "created"
    spots: list[Any] = []
    if isinstance(doc, dict):
        result = doc.get("result", doc)
        if isinstance(result, dict):
            gate = result.get("gate")
            spots += [result.get("gateId"), result.get("gate_id")]
            if isinstance(gate, dict):
                spots.append(gate.get("id"))
            spots.append(result.get("id"))
    return next((s for s in spots if valid_operation_id(s)), "created")


def _create_gate(runner: Runner, task_id: str, question: str, options: list[str]) -> str | None:
    """Make the Orca decision gate; its id, or None when Orca refused or failed."""
    result = runner.run(
        [
            "orca",
            "orchestration",
            "gate-create",
            "--task",
            task_id,
            "--question",
            question,
            "--options",
            json.dumps(options),
            "--json",
        ],
        ext.CALL_TIMEOUT_S,
    )
    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
        return None
    return _gate_id(result.stdout)


# --- the action log rows of this verb -------------------------------------------------------


def _log_rows(root: Path | str, kind: str, entry: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    try:
        with open(actions.actions_path(root), "rb") as handle:
            for raw in handle:
                try:
                    row = json.loads(raw.decode("utf-8"))
                except (ValueError, RecursionError):
                    continue
                if isinstance(row, dict) and row.get("kind") == kind and row.get("entry") == entry:
                    found.append(row)
    except OSError:
        return []
    return found


# --- the interrupt --------------------------------------------------------------------------


def check_interrupt(root: Path | str, repo: str, number: int, dispatch: str) -> str:
    """Check the Dispatch of ``--interrupt`` before anything is written; the terminal handle to use.

    Only the Dispatch that this issue's own state file records, under this orchestrator's id,
    passes (finding F29 of issue 675). Exit 2 and nothing written otherwise.
    """
    if not valid_operation_id(dispatch):
        raise StateError("invalid_dispatch", EXIT_INVALID)
    try:
        doc = state.load_state(root, repo, number)
    except StateError as exc:
        if exc.reason == "not_found":
            raise StateError("interrupt_no_state", EXIT_INVALID) from None
        raise
    own, _tag = ext.identity(None, None)
    if doc["status"] not in ("in_progress", "escalated"):
        raise StateError("interrupt_issue_final", EXIT_INVALID)
    if doc["orchestrator"] != own or doc["ids"].get("dispatch_id") != dispatch:
        raise StateError("dispatch_not_ours", EXIT_INVALID)
    handle = doc["ids"].get("terminal_handle")
    if not isinstance(handle, str):
        raise StateError("terminal_unknown", EXIT_INVALID)
    return handle


def send_interrupt(
    root: Path | str, runner: Runner, entry: str, dispatch: str, handle: str
) -> str:
    """Send the one interrupt: ``sent``, ``failed`` or ``already_attempted``.

    An ``intent`` row goes into the action log first. A rerun that finds one does not send again, as
    a send is never repeated blind. Only ``orca terminal send --terminal <handle> --interrupt``
    runs: no text, no read of the screen, no close, no stop.
    """
    if _log_rows(root, "escalate-interrupt", entry):
        return "already_attempted"
    actions.append(root, "escalate-interrupt", entry=entry, dispatch=dispatch, phase="intent")
    result = runner.run(
        ["orca", "terminal", "send", "--terminal", handle, "--interrupt", "--json"],
        ext.CALL_TIMEOUT_S,
    )
    ok = not result.timed_out and result.spawn_error is None and result.returncode == 0
    actions.append(
        root, "escalate-interrupt", entry=entry, dispatch=dispatch, phase="done" if ok else "failed"
    )
    return "sent" if ok else "failed"


# --- the verb -------------------------------------------------------------------------------


def _ref_of(key: str) -> str:
    owner, rest = key.split("__", 1)
    name, number = rest.rsplit("__", 1)
    return f"{owner}/{name}#{number}"


def _touch(root: Path | str, entry: str, now: datetime, **which: bool) -> None:
    try:
        questions.touch(root, entry, now=now, **which)
    except StateError:
        pass  # no record yet: nothing to move


def _dm_text(repo: str, number: int, row: Row, entry: str) -> str:
    return (
        f"Orchestrator: https://github.com/{repo}/issues/{number} needs you "
        f"(row {row.number}, {row.needs}). Entry {entry}. Answer it by typing in the "
        "orchestrator terminal; the question is in the living report."
    )


def _note_text(row: Row, entry: str) -> str:
    return f"Orchestrator: entry {entry} needs you (row {row.number}). See the living report."


def flush_held(
    root: Path | str, runner: Runner, repo: str, cap: int, now: datetime
) -> dict[str, Any]:
    """Send the held notices of ``repo`` as one DM when a free place exists; ``{"flushed": n}``.

    The first held row takes the place (it becomes ``counted``); the others become ``released``.
    When neither channel works the rows go back to ``held``, so nothing is lost.
    """
    short = repos.short_name(repo)
    with state.locked(root):
        rows = load_asks(root)
        held = sorted(
            (r for r in rows if r["short"] == short and r["state"] == "held"),
            key=lambda r: r["ts"],
        )
        if not held:
            return {"flushed": 0}
        if not has_free_place(rows, short, cap, now):
            return {"flushed": 0, "reason": "no_free_place"}
        before = [dict(r) for r in held]
        held[0].update(state="counted", ts=format_utc(now), delivered=None)
        for r in held[1:]:
            r["state"] = "released"
        save_asks(root, rows)
    names = "; ".join(
        f"{_ref_of(r['issue'])} (row {r['row']}, entry {r['entry']})" for r in before
    )
    text = f"Orchestrator: {len(before)} notices were held by the daily cap and go out together: {names}."
    if names_check(text):
        text = f"Orchestrator: {len(before)} notices were held by the daily cap. See the living report."
    outcome = send_notice(
        runner,
        Path(root),
        text,
        f"Orchestrator: {len(before)} held notices need you. See the living report.",
    )
    if outcome == "failed":
        with state.locked(root):
            rows = load_asks(root)
            by_entry = {r["entry"]: r for r in rows}
            for old in before:
                by_entry[old["entry"]].update(state="held", ts=old["ts"], delivered=old["delivered"])
            save_asks(root, rows)
        return {"flushed": 0, "reason": "notice_failed"}
    mark_delivered(root, before[0]["entry"], True)
    for old in before:
        _touch(root, old["entry"], now, notified=True)
    return {"flushed": len(before), "via": outcome}


def escalate(
    root: Path | str,
    runner: Runner,
    *,
    repo: str,
    number: int,
    row_raw: str | None,
    question: str | None,
    merge_pr: str | None,
    head_sha: str | None,
    content_doc: object,
    dispatch: str | None,
    now: datetime,
) -> dict[str, Any]:
    """Raise one escalation (the steps of the module docstring); the result for the model to read."""
    root = Path(root)
    # 1. everything that has no side effect
    row = parse_row(row_raw)
    key = build_key(repo, number, row, question, merge_pr, head_sha)
    content = parse_content(content_doc, row)
    entry_id = entry_id_for(repo, number, row, key)
    issue_key = file_key(repo, number)
    short = repos.short_name(repo)
    handle = check_interrupt(root, repo, number, dispatch) if dispatch is not None else None
    block = compose(entry_id, row, content)
    problems = entry_problems(block)
    if problems:
        raise StateError("escalation_invalid", EXIT_INVALID, problems=problems)
    gate_text = (
        f"Needs you (row {row.number}), entry {entry_id}: {content.question} "
        "Answer by typing in the orchestrator terminal."
    )
    texts = [block, gate_text, _dm_text(repo, number, row, entry_id), _note_text(row, entry_id)]
    hits = [h for t in texts for h in names_check(t)]
    if hits:
        raise StateError(
            "names_refused",
            EXIT_INVALID,
            hits=[{"kind": h.kind, "line": h.line} for h in hits],
        )
    path = entry_path(root, repo, number)
    _check_entry_path(root, path)
    _read_entry(path)  # an entry that cannot be read stops the call before anything is written
    old = None
    try:
        old = questions.load_question(root, entry_id)
    except StateError as exc:
        if exc.reason != "question_not_found":
            raise
    issue_ref = f"{repo}#{number}"
    if old is not None and (
        old["question_key"] != key
        or old["row"] != row.number
        or old["issue"] != issue_ref
        or old["low_stakes"] != list(content.low_stakes)
    ):
        raise StateError("entry_id_taken", EXIT_CONFLICT)
    task_id: str | None = None
    try:
        task_id = state.load_state(root, repo, number)["ids"].get("task_id")
    except StateError:
        task_id = None

    # 2 and 3. the entry, then the record of the question
    write_entry(root, repo, number, entry_id, block, now)
    _record, created = questions.record_question(
        root,
        entry_id,
        question_key=key,
        row=row.number,
        issue=issue_ref,
        low_stakes=content.low_stakes,
        now=now,
    )
    if not created:
        _touch(root, entry_id, now, edited=True)
    failures: list[tuple[str, int]] = []

    # 4. the interrupt, after the entry is written and never before
    interrupt = "not_requested"
    if dispatch is not None and handle is not None:
        interrupt = send_interrupt(root, runner, entry_id, dispatch, handle)
        if interrupt == "failed":
            failures.append(("interrupt_failed", EXIT_EXTERNAL))

    # 5. the gate
    gate = "none, no Task yet"
    prior = _log_rows(root, "escalate-gate", entry_id)
    if prior:
        done = [r for r in prior if r.get("phase") == "done"]
        if done:
            gate = done[-1]["gate"]
        elif prior[-1].get("phase") == "failed":
            gate = "not created"
        else:
            gate = "unknown, check Orca"
    elif task_id is not None:
        actions.append(root, "escalate-gate", entry=entry_id, phase="intent")
        gate_id = _create_gate(runner, task_id, gate_text, [text for text, _ in content.options])
        if gate_id is None:
            actions.append(root, "escalate-gate", entry=entry_id, phase="failed")
            gate = "not created"
        else:
            actions.append(root, "escalate-gate", entry=entry_id, phase="done", gate=gate_id)
            gate = gate_id

    # 6. the notice
    notice = "not sent"
    held = False
    try:
        cap = read_cap(root, runner, repo)
        flush_held(root, runner, repo, cap, now)
        ask, new = reserve(
            root, short=short, issue_key=issue_key, row=row.number, entry=entry_id, cap=cap, now=now
        )
        if ask["state"] == "held":
            held = True
            notice = "held, the daily cap is reached; the question stands in this entry"
        elif new or ask["delivered"] is False:
            outcome = send_notice(
                runner, root, _dm_text(repo, number, row, entry_id), _note_text(row, entry_id)
            )
            mark_delivered(root, entry_id, outcome != "failed")
            if outcome == "failed":
                notice = "not sent, neither the ClickUp DM nor the Orca unread mark worked"
                failures.append(("notice_failed", EXIT_EXTERNAL))
            else:
                notice = (
                    "ClickUp DM sent"
                    if outcome == "dm"
                    else "DM not sent, Orca unread mark set"
                )
                _touch(root, entry_id, now, notified=True)
        elif ask["delivered"] is True:
            notice = "already sent"
        else:
            notice = "unconfirmed, a call stopped before the send was confirmed"
    except StateError as exc:
        if exc.reason not in ("asks_unreadable", "asks_full"):
            raise
        notice = f"not sent, the count of notices cannot be kept ({exc.reason})"
        failures.append((exc.reason, exc.code))

    # 7. the entry again, with what each channel did
    write_entry(root, repo, number, entry_id, compose(entry_id, row, content, gate=gate, notice=notice), now)
    _touch(root, entry_id, now, edited=True)

    result: dict[str, Any] = {
        "entry": entry_id,
        "question_key": key,
        "row": row.number,
        "created": created,
        "gate": gate,
        "notice": notice,
        "held": held,
        "interrupt": interrupt,
    }
    if failures:
        reason, code = failures[0]
        raise StateError(reason, code, **result)
    return result


@click.command("escalate")
@click.option("--issue", default=None, help="The issue whose own entry holds the escalation, owner/repo#N.")
@click.option("--row", default=None, help="The row of the table of 5.6, 1 to 9. A call with no row, or an unknown one, writes and sends nothing.")
@click.option("--question", default=None, help="A short id of the question (a-z, 0-9, _ and -), for the key <issue>:<row>:<question>.")
@click.option("--merge-safety-pr", default=None, help="The pull request of the merge-safety hold (row 8); the key is merge_safety:<PR>:<head sha>.")
@click.option("--head-sha", default=None, help="The head sha of that gate run.")
@click.option("--content-file", type=click.Path(dir_okay=False, path_type=Path), default=None, help="JSON: question, options [{text, after}], facts, recommendation, blocked, low_stakes, links, why.")
@click.option("--interrupt", "dispatch", default=None, help="After the entry is written, interrupt this Dispatch once (the one the issue's state file records).")
@click.option("--flush-held", "flush_held_flag", is_flag=True, help="Send the notices held by the daily cap as one DM when a free place exists (needs --repo).")
@click.option("--repo", default=None, help="owner/repo, with --flush-held.")
def escalate_cmd(
    issue, row, question, merge_safety_pr, head_sha, content_file, dispatch, flush_held_flag, repo
) -> None:
    """Reach Clay for one case that fits one row of the table of 5.6; write the entry, the gate and the notice."""

    def action() -> dict[str, Any]:
        root = common.root()
        runner = ext.make_runner(ESCALATE_CALLER)
        now = datetime.now(timezone.utc)
        if flush_held_flag:
            if not valid_repo(repo) or any(
                x is not None for x in (issue, row, question, merge_safety_pr, head_sha, content_file, dispatch)
            ):
                raise StateError("invalid_flush", EXIT_INVALID)
            return flush_held(root, runner, repo, read_cap(root, runner, repo), now)
        if repo is not None:
            raise StateError("invalid_flush", EXIT_INVALID)
        number_repo = parse_issue(issue)
        parse_row(row)  # the refusal that says "decide it yourself", before the file is read
        if content_file is None:
            raise StateError("content_missing", EXIT_INVALID)
        try:
            with open(content_file, "rb") as handle:
                data = handle.read(MAX_CONTENT_BYTES + 1)
            if len(data) > MAX_CONTENT_BYTES:
                raise ValueError
            doc = json.loads(data.decode("utf-8"))
        except (OSError, ValueError, RecursionError):
            raise StateError("content_unreadable", EXIT_INVALID) from None
        return escalate(
            root,
            runner,
            repo=number_repo[0],
            number=number_repo[1],
            row_raw=row,
            question=question,
            merge_pr=merge_safety_pr,
            head_sha=head_sha,
            content_doc=doc,
            dispatch=dispatch,
            now=now,
        )

    common.run(action)


__all__ = [
    "ROWS",
    "Content",
    "Row",
    "compose",
    "entry_problems",
    "escalate",
    "escalate_cmd",
    "flush_held",
    "merge_needs",
]
