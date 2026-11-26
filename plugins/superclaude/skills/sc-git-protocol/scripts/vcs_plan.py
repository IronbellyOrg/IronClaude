"""Planning logic of the read-only ``vcs`` helper: the git runner (FR-011, DD-9).

``GitRunner`` is the one place the helper starts a git process. Every call is built as::

    git --no-optional-locks -c core.fsmonitor=false [-C <dir>] <verb> <options>

and is checked against the allow-list of ``vcs_rules`` before the process starts, so a
verb or option outside the table raises ``ForbiddenArgv`` and nothing runs. The runner
returns ``(rc, stdout)``; a caller must tell exit 1 from exit 128 (an ``--is-ancestor``
exit of 128 means "unknown", never "diverged"). ``TIMEOUT_RC`` is returned when the
timeout runs out; it is not an exit code of git.

The child environment is built from scratch: every inherited ``GIT_*`` variable is
dropped, ``GIT_TERMINAL_PROMPT=0`` makes a credential prompt stop instead of waiting,
and ``GIT_INDEX_FILE`` is set only to a temporary index the runner made itself outside
``.git/`` (``private_index``). The index of the person is never touched. The private
index calls write loose objects, as the snapshot method does; no ref, no user index, no
work-tree file and no config is written. ``-c core.fsmonitor=false`` keeps a status
read from starting a file-system monitor; whether it covers every monitor setup is
UNVERIFIED.

Submodules: implement-side ``status`` and ``diff`` reads get ``--ignore-submodules=all``.
Only a runner made with ``person_invoked=True`` may run ``status`` with
``--ignore-submodules=none`` (the person-typed status and submodule reports), and that
is its default for ``status``.

Recording mode for tests: ``record=True`` keeps each built argv in ``calls``;
``dry_run=True`` also skips the process and returns ``(0, "")``.

The message rule (FR-039, FR-066) lives here too: ``check_message`` judges a drafted
commit message and ``cut_header`` cuts a drafted header, both with the same count (code
points of the decoded header, no normalization), so drafting and checking agree. The
module reads and writes no file and starts no process for them.

The ledger reader (DD-8, design section 4.4) is pure: ``parse_ledger(text)`` turns the
text of an implement ledger into a ``LedgerView``. It copies, unchanged, the nine line
regexes of ``archive_workspace.py`` (``_HEADER``, ``_PLAN``, ``_START``, ``_VERDICT``,
``_RULING``, ``_RETRY``, ``_HALT``, ``_FINAL``, ``_ARCH``); a parity test loads both files
and compares the pattern strings. The design's DD-8 lists seven; ``_HEADER`` and
``_ARCH`` are the recorded override, because a fresh ledger holds only its header line
and a managed ledger can end in ``ARCHIVE: failed``, and both are valid last lines
(``refs/ledger.md``, Resume and the managed-package extension). Only the last line is
checked against the nine patterns (``LedgerCorrupt`` when none matches, as the Resume
rule says); a line in the middle that matches none is not a record and is skipped.
Line numbers are 1-based and count ``\\n`` separators, so they agree with ``ledger_k``.

Boundary identity (FR-058, FR-103, DD-1) is pure too: ``build_boundaries`` groups the
generations of a ledger into ``Boundary`` objects, ``boundary_key`` hashes the identity
tuple, and ``display_label`` / ``resolve_prefix`` give and read the short form of a key
for the person. The state of a boundary (due, pending, ...) is ``derive_state``'s job.

``plan_stage`` plans an add and a commit for named paths or for the index as staged (path
mode); ``plan_ledger`` is ledger mode: it finds the boundary that needs a commit, builds
S from the anchor ``files=`` lines (plus the literal package files of a managed run), runs
the staging checks and, on ``candidate``, builds the frozen candidate tree. Both only read.

``verify_commit`` (FR-036, FR-108, FR-113, FR-130) judges one prepared attempt after the
commit call: ``committed`` only when the FR-108 predicate holds, ``pending`` when HEAD is
still the prepared parent, one of ``HOOK_CLASSES`` for a hook or call that failed, else
``uncertain``; it also compares every path outside S with the pinned worktree tree. It
reads only and never retries.

``reconcile`` (FR-102 to FR-108, FR-132, DD-5) reads the ledger, the sidecar, the run's flag,
the managed plan pins and git and lists every boundary with its state and the one action
this run may take (``derive_state`` is the table). The retry decision (FR-065, FR-116,
FR-132) is ``_retry_decision``, shared with ``plan_ledger``. It reads only.

``resolve_check`` (FR-120 to FR-126) selects one unsettled boundary by its key or a unique
prefix and says which owner answers may be recorded: ``abandon`` always, ``adopt`` only when
the history allows it. It reads only; the executor appends the ``resolved`` line.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple, Union

from vcs_rules import (
    DEV_MIRROR_ALLOW,
    ForbiddenArgv,
    validate_agent_argv,
    validate_argv,
)

PREFIX = ("git", "--no-optional-locks", "-c", "core.fsmonitor=false")
TIMEOUT_RC = 124
_IGNORE_OPT = "--ignore-submodules="

# --- the commit message rule ---------------------------------------------------------------
HEADER_LIMIT = 72
COMMIT_TYPES = (
    "feat", "fix", "refactor", "docs", "test", "build", "ci", "chore", "perf", "style",
)  # fmt: skip
_CTRL = r"\x00-\x1f\x7f"
_HEADER_RE = re.compile(
    rf"^(?P<type>[a-z]+)(?:\([^()\s{_CTRL}][^(){_CTRL}]*\))?!?: \S[^{_CTRL}]*$"
)
_TASK_LINE = re.compile(r"^T([0-9A-Za-z.-]+): \S.*$")
_PLAN_TRAILER = re.compile(r"^Implement-Plan: (\S+)$")
_TASK_TRAILER = re.compile(r"^Implement-Task: T([0-9A-Za-z.-]+) \(([a-z-]+)\)$")
_BOUNDARY_TRAILER = re.compile(r"^Implement-Boundary: ([0-9a-f]{64})$")
_LEDGER_TRAILER = re.compile(rf"^Implement-Ledger: ([^{_CTRL}]+)$")
_OTHER_TRAILER = re.compile(rf"^[A-Za-z][A-Za-z0-9-]*: [^{_CTRL}]+$")


def cut_header(header: str, limit: int = HEADER_LIMIT) -> str:
    """Cut ``header`` at the last space at or before code point ``limit``.

    A header that already fits is returned unchanged. Without a space to cut at
    in the summary the header is cut hard at ``limit`` code points. The result never ends in a space.
    """
    if len(header) <= limit:
        return header
    at = header.rfind(" ", 0, limit + 1)
    # A space inside the type part (before the summary starts) is no place to cut:
    # "feat:" alone is not a header.
    if at > max(header.find(": "), -1) + 2:
        return header[:at].rstrip()
    return header[:limit].rstrip()


def refused_message(rule: str, header_len: int, detail: str) -> Dict[str, Any]:
    """The refusal object of ``check-message``: the rule is both ``reason`` and ``rule``."""
    return {
        "verb": "check-message",
        "status": "refused",
        "reason": rule,
        "rule": rule,
        "header_len": header_len,
        "detail": detail,
    }


def _implement_rule(rest: List[str]) -> Optional[Tuple[str, str]]:
    """Check body and trailers of an implement commit; ``rest`` follows the blank line."""
    start = next(
        (i for i, ln in enumerate(rest) if ln.startswith("Implement-Plan:")), -1
    )
    if start < 0 or not _PLAN_TRAILER.match(rest[start]):
        return "trailer-plan", "the trailer block needs 'Implement-Plan: <slug>'"
    block = rest[start + 1 :]
    tasks = []
    while block and block[0].startswith("Implement-Task:"):
        found = _TASK_TRAILER.match(block.pop(0))
        if not found:
            return "trailer-task", "expected 'Implement-Task: T<id> (<verdict>)'"
        tasks.append(found.group(1))
    if not tasks:
        return "trailer-task", "the trailer block needs one 'Implement-Task:' per task"
    if not block or not _BOUNDARY_TRAILER.match(block[0]):
        return "trailer-boundary", "expected 'Implement-Boundary: <64 lower-case hex>'"
    found = _LEDGER_TRAILER.match(block[1]) if len(block) > 1 else None
    path = found.group(1).strip() if found else ""
    if not path or path.startswith("/") or ".." in path.split("/"):
        return "trailer-ledger", "expected 'Implement-Ledger: <repo-relative path>'"
    for line in block[2:]:
        if line.startswith("Implement-") or not _OTHER_TRAILER.match(line):
            return "trailer-block", f"unexpected line after the helper trailers: {line}"
    body = [ln for ln in rest[:start] if ln.strip()]
    if rest[:start] and rest[start - 1].strip():
        return "trailer-block", "a blank line must separate the body from the trailers"
    ids = [m.group(1) if (m := _TASK_LINE.match(ln)) else None for ln in body]
    if ids != tasks:
        return "body-task-lines", "the body needs one 'T<id>: <title>' line per task"
    return None


def check_message(text: str, implement: bool = False) -> Dict[str, Any]:
    """Judge a drafted commit message; returns the result object of ``check-message``.

    The first violated rule is named in both ``reason`` and ``rule``; ``header_len``
    is in every result. Rule names: ``header-format``, ``unknown-type``,
    ``header-length``, ``blank-second-line`` and, with ``implement``, ``trailer-plan``,
    ``trailer-task``, ``trailer-boundary``, ``trailer-ledger``, ``trailer-block`` and
    ``body-task-lines``. Header rules run first. The helper adds no attribution trailer.
    """
    lines = (text[:-1] if text.endswith("\n") else text).split("\n")
    header = lines[0]
    n = len(header)  # code points; no normalization
    found = _HEADER_RE.match(header)
    if not found:
        form = "<type>[(<scope>)][!]: <summary>"
        return refused_message("header-format", n, f"expected '{form}'")
    if found.group("type") not in COMMIT_TYPES:
        allowed = ", ".join(COMMIT_TYPES)
        return refused_message("unknown-type", n, f"type must be one of: {allowed}")
    if n > HEADER_LIMIT:
        detail = f"header is {n} code points; the limit is {HEADER_LIMIT}"
        return refused_message("header-length", n, detail)
    if len(lines) > 1 and lines[1] != "":
        return refused_message("blank-second-line", n, "the second line must be blank")
    if implement:
        broken = _implement_rule(lines[2:])
        if broken:
            return refused_message(broken[0], n, broken[1])
    return {
        "verb": "check-message",
        "status": "ok",
        "reason": None,
        "rule": None,
        "header_len": n,
    }


# --- the ledger reader (DD-8) --------------------------------------------------------------
# The nine patterns below are copied unchanged from archive_workspace.py (lines 43-67);
# tests/vcs/test_eligibility.py compares each pattern string with the original.
TASK_ID = r"[0-9A-Za-z.-]+"
_HEADER = re.compile(
    r"^# implement ledger — source: .+ — created: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)
_PLAN = re.compile(r"^PLAN: sha256=([0-9a-f]{64}) source_sha256=([0-9a-f]{64})$")
_START = re.compile(rf"^T({TASK_ID}): start sha=([0-9a-f]{{40}}|nogit)$")
_VERDICT = re.compile(
    rf"^T({TASK_ID}): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify)"
    r" ac=([^ ]+) evidence=(.+) extras=lint:(?:pass|fail|skip),typecheck:(?:pass|fail|skip),"
    r"test:(?:pass|fail|skip|unrelated-red) files=(.+)$"
)
_RULING = re.compile(rf"^T({TASK_ID}): Ruling: .+ — .+ — .+$")
_RETRY = re.compile(
    rf"^T({TASK_ID}): retry n=([345]) "
    r"(?:step=open checkpoint=([0-9a-f]{40}) tier=([A-Za-z0-9_]+)"
    r"|step=revert brief=(\S+) supersedes=(T[0-9A-Za-z.-]+_brief-[34]\.md|none)"
    r"|step=review)$"
)
_HALT = re.compile(rf"^T({TASK_ID}): halt review=([2-5]) reason=([a-z][a-z-]*)$")
_FINAL = re.compile(r"^FINAL: (\S+)(?: .*)?$")
_ARCH = re.compile(r"^ARCHIVE: (start|failed|Ruling:) .+$")
_LEDGER_LINES = (
    _HEADER,
    _PLAN,
    _START,
    _VERDICT,
    _RULING,
    _RETRY,
    _HALT,
    _FINAL,
    _ARCH,
)


class LedgerCorrupt(Exception):
    """The last ledger line matches none of the nine line patterns."""

    reason = "ledger-corrupt"


@dataclass
class TaskGen:
    """One generation of a task: one ``start`` record and what followed it.

    ``start_ordinal`` is the 1-based count of the task's ``start`` lines. The anchor is
    the first valid ``complete`` line after that start; ``verdict`` and ``files`` are the
    anchor line's. A later ``complete`` of the same generation (a re-review line) never
    moves the anchor or changes ``files``.
    """

    start_ordinal: int
    start_sha: str
    start_line_no: int
    anchor_line_no: Optional[int] = None
    verdict: Optional[str] = None
    files: List[str] = field(default_factory=list)
    # The first ``complete`` or ``blocked`` line after the start (valid or not): it closes
    # the implement window of ``refs/retry.md`` (check 2), which batch membership reads.
    first_verdict_line_no: Optional[int] = None


@dataclass
class LedgerView:
    """``tasks`` maps a task id to its generations; ids keep source order."""

    tasks: Dict[str, List[TaskGen]] = field(default_factory=dict)
    line_count: int = 0


def parse_ledger(text: str) -> LedgerView:
    """Read an implement ledger into a ``LedgerView`` (pure; raises ``LedgerCorrupt``).

    A ``complete`` line is valid when its verdict is ``compliant`` or when an operator
    ``Ruling`` of the task stands after the generation's start and after its latest
    ``blocked`` line (``refs/ledger.md``, post-ruling complete line). A ``complete`` or
    ``blocked`` line of a task with no ``start`` is not attached to any generation.
    Empty text gives an empty view; a header-only ledger gives no tasks.
    """
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    view = LedgerView(line_count=len(lines))
    if not lines:
        return view
    if not any(rx.match(lines[-1]) for rx in _LEDGER_LINES):
        raise LedgerCorrupt(f"last ledger line {len(lines)} matches no ledger pattern")
    # task id -> a Ruling stands since the latest start or blocked line
    ruled: Dict[str, bool] = {}
    for no, line in enumerate(lines, 1):
        found = _START.match(line)
        if found:
            gens = view.tasks.setdefault(found.group(1), [])
            gens.append(TaskGen(len(gens) + 1, found.group(2), no))
            ruled[found.group(1)] = False
            continue
        found = _RULING.match(line)
        if found:
            if found.group(1) in view.tasks:
                ruled[found.group(1)] = True
            continue
        found = _VERDICT.match(line)
        if not found or found.group(1) not in view.tasks:
            continue
        tid, status, verdict = found.group(1), found.group(2), found.group(3)
        gen = view.tasks[tid][-1]
        if gen.first_verdict_line_no is None:
            gen.first_verdict_line_no = no
        if status == "blocked":
            ruled[tid] = False
        elif gen.anchor_line_no is None and (verdict == "compliant" or ruled[tid]):
            gen.anchor_line_no, gen.verdict = no, verdict
            gen.files = found.group(6).split(",")
    return view


# --- the sidecar commits.md (FR-100..FR-102, FR-120) ----------------------------------------
_IDS = r"T([0-9A-Za-z.,-]+)"
_H40 = r"[0-9a-f]{40}"
_H64 = r"[0-9a-f]{64}"
_DAY = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
# One regex per line form. refs/commit-step.md documents these once; the parity test (T-10)
# compares its text with this table. The two ``resolved`` forms are copied from FR-120.
SIDECAR_FORMS: Dict[str, "re.Pattern[str]"] = {
    "run": re.compile(
        r"^run ([0-9]+): commit-tasks=(on|off)( reason=revoked)? ledger-lines=([0-9]+)"
        r" branch=(refs/\S+|-) at=([0-9]{4}-[0-9]{2}-[0-9]{2}T\S+) args=\"([^\"]*)\""
        r" source=(\S+) worktree=(\S+)$"
    ),
    "prepared": re.compile(
        rf"^{_IDS}: commit prepared key=({_H64}) attempt=([0-9]+) parent=({_H40})"
        rf" branch=(refs/\S+) paths=({_H64}) accepted=(refs/[^\s,]+(?:,refs/[^\s,]+)*)"
        rf" plan=({_H64}|-) source=({_H64}|-)$"
    ),
    "commit": re.compile(
        rf"^{_IDS}: commit (sha|recovered)=({_H40}) key=({_H64}) attempt=([0-9]+)"
        r"(?: outside-changed=([0-9]+) wt=(refs/\S+))?$"
    ),
    "skipped": re.compile(
        rf"^{_IDS}: commit skipped key=({_H64}) reason=(empty|mixed-authorization)$"
    ),
    "refused": re.compile(
        rf"^{_IDS}: commit (refused|uncertain) key=({_H64}) attempt=([0-9]+)"
        r" reason=([a-z][a-z0-9-]*)(?: rewritten=(refs/\S+))?$"
    ),
    "resolved_abandoned": re.compile(
        r"^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=abandoned "
        r'at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$'
    ),
    "resolved_adopted": re.compile(
        r"^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=adopted "
        r"head=[0-9a-f]{40} basis=(candidate|accepted) differs=[0-9]+ "
        r'at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$'
    ),
}
# The FR-120 patterns capture only what they name; these re-read the fields the record needs.
_ADOPT_FIELDS = re.compile(
    rf"head=({_H40}) basis=(candidate|accepted) differs=([0-9]+) at=({_DAY}) quote="
)
_ABANDON_AT = re.compile(rf" at=({_DAY}) quote=")
_ESCAPE = re.compile(r"\\(.)")
_CONTROL = re.compile(f"[{_CTRL}]")
QUOTE_LIMIT = 200


class SidecarCorrupt(Exception):
    """An unknown form, a malformed line or a truncated tail; never repaired (FR-102)."""

    reason = "sidecar-corrupt"


class SidecarMismatch(Exception):
    """A run line contradicts its binding, or the offsets disagree with the ledger."""

    reason = "sidecar-mismatch"


@dataclass
class RunLine:
    run: int
    flag: str  # "on" or "off"
    revoked: bool
    ledger_lines: int  # the offset k of FR-102
    branch: str  # full symbolic ref, or "-" (detached; valid only on an off line)
    at: str
    args: str
    source: str
    worktree: str
    line_no: int = 0


@dataclass
class Attempt:
    """A ``prepared`` line. ``ids`` is the task id list as written (``"1,2"``)."""

    key: str
    attempt: int
    ids: str
    parent: str
    branch: str
    paths: str
    accepted: List[str]
    plan: str
    source: str
    line_no: int = 0


@dataclass
class Terminal:
    """A result line: ``kind`` is sha, recovered, skipped, refused or uncertain."""

    key: str
    kind: str
    ids: str
    attempt: Optional[int] = None
    sha: Optional[str] = None
    reason: Optional[str] = None
    outside_changed: Optional[int] = None
    wt: Optional[str] = None
    rewritten: Optional[str] = None
    line_no: int = 0


@dataclass
class Resolved:
    """An owner answer; ``head``, ``basis`` and ``differs`` exist only for ``adopted``."""

    key: str
    ids: str
    as_: str  # "abandoned" or "adopted"
    at: str
    quote: str  # decoded
    head: Optional[str] = None
    basis: Optional[str] = None
    differs: Optional[int] = None
    line_no: int = 0


@dataclass
class Sidecar:
    """``terminal`` and ``resolved`` hold the last such line of a key in sidecar order."""

    runs: List[RunLine] = field(default_factory=list)
    attempts: Dict[str, List[Attempt]] = field(default_factory=dict)
    terminal: Dict[str, Terminal] = field(default_factory=dict)
    resolved: Dict[str, Resolved] = field(default_factory=dict)


def ledger_k(text: str) -> int:
    """FR-102: newline count, plus one when the text is not empty and unterminated."""
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


def _quote(raw: str, no: int) -> str:
    quote = _ESCAPE.sub(r"\1", raw)
    if not 1 <= len(quote) <= QUOTE_LIMIT or _CONTROL.search(quote):
        raise SidecarCorrupt(
            f"sidecar line {no}: the quote must be 1-{QUOTE_LIMIT} printable code points"
        )
    return quote


def _parse_line(line: str, no: int, side: Sidecar) -> None:
    """Read one sidecar line into ``side`` (raises ``SidecarCorrupt`` / ``SidecarMismatch``)."""
    forms = SIDECAR_FORMS
    m = forms["run"].match(line)
    if m:
        flag, revoked, branch = m.group(2), bool(m.group(3)), m.group(5)
        if flag == "on" and (branch == "-" or revoked):
            raise SidecarMismatch(
                f"sidecar line {no}: branch=- and reason=revoked are valid only on an off run line"
            )
        side.runs.append(
            RunLine(
                int(m.group(1)), flag, revoked, int(m.group(4)), branch, m.group(6),
                m.group(7), m.group(8), m.group(9), no,
            )
        )  # fmt: skip
        return
    m = forms["prepared"].match(line)
    if m:
        ids, key = m.group(1), m.group(2)
        side.attempts.setdefault(key, []).append(
            Attempt(
                key, int(m.group(3)), ids, m.group(4), m.group(5), m.group(6),
                m.group(7).split(","), m.group(8), m.group(9), no,
            )
        )  # fmt: skip
        return
    m = forms["commit"].match(line)
    if m:
        sha_kind = m.group(2)
        side.terminal[m.group(4)] = Terminal(
            m.group(4), sha_kind, m.group(1), int(m.group(5)), m.group(3), None,
            int(m.group(6)) if m.group(6) else None, m.group(7), None, no,
        )  # fmt: skip
        return
    m = forms["skipped"].match(line)
    if m:
        side.terminal[m.group(2)] = Terminal(
            m.group(2), "skipped", m.group(1), reason=m.group(3), line_no=no
        )
        return
    m = forms["refused"].match(line)
    if m:
        side.terminal[m.group(3)] = Terminal(
            m.group(3), m.group(2), m.group(1), int(m.group(4)), None, m.group(5),
            None, None, m.group(6), no,
        )  # fmt: skip
        return
    m = forms["resolved_abandoned"].match(line)
    if m:
        at = _ABANDON_AT.search(line).group(1)
        side.resolved[m.group(2)] = Resolved(
            m.group(2), m.group(1), "abandoned", at, _quote(m.group(3), no), line_no=no
        )
        return
    m = forms["resolved_adopted"].match(line)
    if m:
        f = _ADOPT_FIELDS.search(line)
        side.resolved[m.group(2)] = Resolved(
            m.group(2), m.group(1), "adopted", f.group(4), _quote(m.group(4), no),
            f.group(1), f.group(2), int(f.group(3)), no,
        )  # fmt: skip
        return
    raise SidecarCorrupt(f"sidecar line {no} matches no line form")


def parse_sidecar(text: str) -> Sidecar:
    """Read ``commits.md`` strictly; nothing is repaired (FR-100, FR-102).

    A line that matches none of the forms (a blank line included), and a last line
    without its newline, raise ``SidecarCorrupt``. The missing newline is the one sign
    of a cut write: a cut can still parse (``attempt=1`` from ``attempt=12``). A run
    line with ``branch=-`` or ``reason=revoked`` that says ``on`` raises
    ``SidecarMismatch``. Offsets are checked against a ledger by ``validate_runs``.
    """
    side = Sidecar()
    if not text:
        return side
    if not text.endswith("\n"):
        raise SidecarCorrupt("the last sidecar line is not terminated (truncated tail)")
    for no, line in enumerate(text[:-1].split("\n"), 1):
        _parse_line(line, no, side)
    return side


def validate_runs(runs: Sequence[RunLine], ledger_text: str) -> None:
    """Refuse decreasing offsets and an offset beyond the ledger (FR-102)."""
    end = ledger_k(ledger_text)
    previous = 0
    for run in runs:
        if run.ledger_lines < previous:
            raise SidecarMismatch(
                f"run {run.run}: ledger-lines={run.ledger_lines} decreases"
            )
        if run.ledger_lines > end:
            raise SidecarMismatch(
                f"run {run.run}: ledger-lines={run.ledger_lines} is beyond the ledger ({end} lines)"
            )
        previous = run.ledger_lines


def segment_of(line_no: int, runs: Sequence[RunLine]) -> Optional[RunLine]:
    """The last run line (sidecar order) whose offset is below ``line_no``, else None."""
    found = None
    for run in runs:
        if run.ledger_lines < line_no:
            found = run
    return found


# --- boundary identity (FR-058, FR-103, DD-1) -----------------------------------------------
# A key prefix is for display only; a shorter prefix never selects a key.
DISPLAY_LEN = 12
KEY_VERSION = "vcs-boundary-1"
# The ledger identity is a token made of the pin-id slug, never a path: a managed package
# moves from to-do/ to done/ at archive, and the key must not change with it (DD-1).
_LEDGER_ID = re.compile(r"^(?:managed|legacy):[A-Za-z0-9][A-Za-z0-9._-]*$")
_KEY_PREFIX = re.compile(r"^[0-9a-f]+$")
_NO_END = float("inf")


class KeyPrefixError(Exception):
    """A key prefix selects no key (``unknown-boundary``), more than one
    (``ambiguous-key``) or is shorter than ``DISPLAY_LEN`` (``prefix-too-short``)."""

    def __init__(self, reason: str, detail: str) -> None:
        super().__init__(detail)
        self.reason = reason


@dataclass
class Boundary:
    """One commit boundary: a task generation, or a batch of overlapping generations.

    ``members`` are task ids and ``gens`` their generations, both in ``start`` line order
    (the source order a batch writes its starts in). ``anchors`` holds each member's anchor
    line, None for a member that has no valid ``complete`` yet; ``on`` says whether that
    anchor lies in an ``on`` segment. ``complete`` means every member has an anchor.
    ``eligible`` needs ``complete`` and every anchor in an ``on`` segment (FR-103); a
    complete boundary that is on for some members and off for others is ``mixed``
    (FR-058: settled as ``commit skipped ... reason=mixed-authorization``). A boundary
    completed wholly outside an ``on`` segment is neither eligible nor mixed: it is never
    committed later.
    """

    members: List[str]
    gens: List[TaskGen]
    key: str
    anchors: List[Optional[int]]
    on: List[bool]
    complete: bool
    eligible: bool
    # FR-105, the ledger part: a complete boundary that no other generation's ``start``
    # follows (after any member's anchor) and while no other task is open.
    crash_explained: bool = False

    @property
    def mixed(self) -> bool:
        return self.complete and any(self.on) and not all(self.on)


def ledger_identity(kind: str, slug: str) -> str:
    """The ledger identity token ``managed:<slug>`` or ``legacy:<slug>``; a path is refused."""
    token = f"{kind}:{slug}"
    if not _LEDGER_ID.match(token):
        raise ValueError(
            f"not a ledger identity token (managed:<slug> or legacy:<slug>): {token!r}"
        )
    return token


def boundary_key(
    repo_id: str,
    ledger_id: str,
    source_id: str,
    members: Sequence[Tuple[str, int, str]],
) -> str:
    """SHA-256 (64 lower-case hex) over the canonical tuple of FR-103.

    ``repo_id`` is the repository/worktree identity and ``source_id`` the source identity;
    both are opaque strings the caller keeps stable across the life of the plan (the caller
    must not pass a path that moves with a managed package). ``ledger_id`` comes from
    ``ledger_identity``. ``members`` are ``(task id, start ordinal, full start sha)`` in
    order. The tuple is JSON with ASCII escapes and no spaces, so no two tuples share bytes.
    """
    if not _LEDGER_ID.match(ledger_id):
        raise ValueError(
            f"the ledger identity must be managed:<slug> or legacy:<slug>: {ledger_id!r}"
        )
    canonical = json.dumps(
        [
            KEY_VERSION,
            repo_id,
            ledger_id,
            source_id,
            [[t, int(o), s] for t, o, s in members],
        ],
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


def _window_end(view: LedgerView, task: str, gen: TaskGen) -> float:
    """End of a generation's implement window (``refs/retry.md``, check 2).

    The first verdict line after its ``start``; with none, the next ``start`` of the same
    task (a crashed generation that was restarted), else open-ended.
    """
    if gen.first_verdict_line_no is not None:
        return gen.first_verdict_line_no
    later = view.tasks[task][gen.start_ordinal :]
    return later[0].start_line_no if later else _NO_END


def build_boundaries(
    view: LedgerView,
    runs: Sequence[RunLine],
    repo_id: str,
    ledger_id: str,
    source_id: str,
) -> List[Boundary]:
    """Group every task generation into boundaries, in order of their first ``start``.

    Two generations belong to one boundary when their windows overlap (another's ``start``
    lies inside this window, or this ``start`` lies inside the other's), read from the
    ledger alone and joined transitively. Membership is therefore the original batch and
    never depends on the invocation or on a resume. Later ``complete`` lines never move an
    anchor (``parse_ledger``), so they cannot create or re-authorize a boundary.
    """
    items = sorted(
        ((tid, gen) for tid, gens in view.tasks.items() for gen in gens),
        key=lambda item: item[1].start_line_no,
    )
    ends = [_window_end(view, tid, gen) for tid, gen in items]
    parent = list(range(len(items)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i, (_, a) in enumerate(items):
        for j in range(i + 1, len(items)):
            b = items[j][1]
            # items are sorted by start, so only "b starts inside a's window" can hold
            if a.start_line_no < b.start_line_no < ends[i]:
                parent[find(j)] = find(i)
    groups: Dict[int, List[int]] = {}
    for i in range(len(items)):
        groups.setdefault(find(i), []).append(i)
    found: List[Boundary] = []
    for idx in sorted(groups.values(), key=lambda g: g[0]):
        members = [items[i][0] for i in idx]
        gens = [items[i][1] for i in idx]
        anchors = [g.anchor_line_no for g in gens]
        on = []
        for anchor in anchors:
            run = segment_of(anchor, runs) if anchor is not None else None
            on.append(run is not None and run.flag == "on")
        complete = all(a is not None for a in anchors)
        key = boundary_key(
            repo_id, ledger_id, source_id,
            [(t, g.start_ordinal, g.start_sha) for t, g in zip(members, gens)],
        )  # fmt: skip
        explained = False
        if complete:
            mine = {id(g) for g in gens}
            first_anchor = min(anchors)
            explained = not any(
                g.start_line_no > first_anchor
                for gs in view.tasks.values()
                for g in gs
                if id(g) not in mine
            ) and not any(
                gs[-1].anchor_line_no is None and id(gs[-1]) not in mine
                for gs in view.tasks.values()
            )
        found.append(
            Boundary(
                members,
                gens,
                key,
                anchors,
                on,
                complete,
                complete and all(on),
                explained,
            )
        )
    return found


def display_label(key: str, keys: Sequence[str]) -> str:
    """The shortest prefix of ``key`` (at least ``DISPLAY_LEN``) no other key in ``keys`` shares."""
    pool = set(keys)
    if key not in pool:
        raise ValueError("the key is not among the keys shown")
    for n in range(DISPLAY_LEN, len(key) + 1):
        if sum(1 for other in pool if other.startswith(key[:n])) == 1:
            return key[:n]
    return key


def resolve_prefix(prefix: str, keys: Sequence[str]) -> str:
    """Resolve a typed prefix to one full key of ``keys`` or raise ``KeyPrefixError``.

    A prefix shorter than ``DISPLAY_LEN`` is refused even when it would be unique, so a
    person never selects a key by a label that was not shown.
    """
    if len(prefix) < DISPLAY_LEN:
        raise KeyPrefixError(
            "prefix-too-short", f"give at least {DISPLAY_LEN} hex characters of the key"
        )
    hits = (
        sorted(k for k in set(keys) if k.startswith(prefix))
        if _KEY_PREFIX.match(prefix)
        else []
    )
    if not hits:
        raise KeyPrefixError(
            "unknown-boundary", f"no boundary key starts with {prefix!r}"
        )
    if len(hits) > 1:
        raise KeyPrefixError(
            "ambiguous-key", f"{len(hits)} boundary keys start with {prefix!r}"
        )
    return hits[0]


# --- boundary state and the action table (FR-107, design 5.4, DD-5, DD-11) --------------------
@dataclass(frozen=True)
class GitFacts:
    """Everything ``derive_state`` needs from git, read by the caller (the function reads none).

    ``head`` is the current HEAD and ``q0_head`` the first member's ``q0-head`` (the parent
    of a boundary that was never prepared); None means unknown and fails closed.
    ``s_empty``: the commit set S is empty. ``pins_complete``: the latest attempt's
    candidate and worktree pins exist. ``proves_commit``: the sha ``verify`` proved for the
    latest attempt (FR-108), else None. ``retry_allowed``: the product paths equal the
    accepted tree or the disclosed ``rewritten=`` tree and FR-065's review rule holds
    (FR-107, FR-132).
    """

    head: Optional[str] = None
    q0_head: Optional[str] = None
    s_empty: bool = False
    pins_complete: bool = False
    proves_commit: Optional[str] = None
    retry_allowed: bool = False


def derive_state(
    boundary: Boundary, sidecar: Sidecar, git_facts: GitFacts, flag: bool
) -> Tuple[str, str]:
    """The single FR-107 table: ``(state, action)`` of one boundary (pure, no git, no I/O).

    States: ``due``, ``pending``, ``refused``, ``uncertain``, ``settled``,
    ``out-of-protocol``. Actions: ``none``, ``prepare``, ``retry``, ``record-recovered``,
    ``record-skipped``, ``stop-unsettled``, ``stop-out-of-protocol``, ``stop-uncertain``.
    ``flag`` says this run carries ``--commit-tasks``. An unflagged run never returns
    ``prepare``, ``retry`` or ``record-skipped`` (a ``skipped`` line is not one of the
    lines NFR-018 lets an unflagged run write); it may return ``record-recovered``.

    ``settled`` with ``none`` also covers a boundary with nothing to settle: one that is
    not complete yet, or that was never eligible (FR-103: never committed later). When a
    retry is not allowed the stop carries ``refused reason=candidate-changed`` (FR-107);
    appending that line is the procedure's step, the action stays ``stop-unsettled``.
    Mixed authorization and an empty set settle as ``skipped`` only for a boundary that is
    not out-of-protocol, so a later ``start`` is checked first (design 5.4).
    """
    key = boundary.key
    done = sidecar.terminal.get(key)
    if key in sidecar.resolved or (
        done is not None and done.kind in ("sha", "recovered", "skipped")
    ):
        return "settled", "none"
    if not (boundary.eligible or boundary.mixed):
        return "settled", "none"
    attempts = sidecar.attempts.get(key, [])
    facts = git_facts
    if not attempts and done is None:
        if not boundary.crash_explained:
            return "out-of-protocol", "stop-out-of-protocol"
        if not flag:
            return "due", "stop-unsettled"
        if boundary.mixed or facts.s_empty:
            return "due", "record-skipped"
        return "due", "prepare"
    last = attempts[-1] if attempts else None
    parent = last.parent if last else facts.q0_head
    at_parent = facts.head is not None and facts.head == parent
    retry = "retry" if flag and facts.retry_allowed else "stop-unsettled"
    if done is not None and (last is None or done.line_no > last.line_no):
        if done.kind == "uncertain":
            return "uncertain", "stop-uncertain"
        return "refused", retry if at_parent else "stop-unsettled"
    # a prepared attempt with no result line
    if (
        at_parent
    ):  # nothing was committed (DD-11 also covers a prepared line without pins)
        return "pending", retry
    if facts.pins_complete and facts.proves_commit:
        return "pending", "record-recovered"
    return "uncertain", "stop-uncertain"


class GitRunner:
    """Runs allow-listed git commands for the helper; see the module docstring."""

    def __init__(
        self,
        top: Union[str, "os.PathLike[str]"],
        timeout: float = 10,
        *,
        person_invoked: bool = False,
        record: bool = False,
        dry_run: bool = False,
    ) -> None:
        self.top = os.fspath(top)
        self.timeout = timeout
        self.person_invoked = person_invoked
        self.record = record or dry_run
        self.dry_run = dry_run
        self.calls: List[List[str]] = []
        self.last_stderr = ""
        self._indexes: set = set()

    @contextlib.contextmanager
    def private_index(self) -> Iterator[str]:
        """Yield the path of a temporary index file the runner owns; remove it after."""
        folder = tempfile.mkdtemp(prefix="vcs-index-")
        path = os.path.join(folder, "index")
        self._indexes.add(path)
        try:
            yield path
        finally:
            self._indexes.discard(path)
            shutil.rmtree(folder, ignore_errors=True)

    def _with_submodule_option(self, words: List[str]) -> List[str]:
        verb = words[0]
        if verb not in ("status", "diff"):
            return words
        end = words.index("--") if "--" in words else len(words)
        for token in words[1:end]:
            if not token.startswith(_IGNORE_OPT):
                continue
            value = token[len(_IGNORE_OPT) :]
            if value != "all" and not (
                value == "none" and verb == "status" and self.person_invoked
            ):
                raise ForbiddenArgv(f"{verb}: {token} is not allowed on this runner")
            return words
        value = "none" if verb == "status" and self.person_invoked else "all"
        return [verb, _IGNORE_OPT + value, *words[1:]]

    def _environment(self, index_file: Optional[str]) -> dict:
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
        env["GIT_TERMINAL_PROMPT"] = "0"
        if index_file is not None:
            env["GIT_INDEX_FILE"] = index_file
        return env

    def run(
        self,
        argv: Sequence[str],
        *,
        directory: Optional[str] = None,
        index_file: Optional[str] = None,
        input: Optional[str] = None,
    ) -> Tuple[int, str]:
        """Run one git call (``argv`` starts with the verb) and return ``(rc, stdout)``.

        ``directory`` becomes ``-C <directory>``. ``index_file`` must come from
        ``private_index`` of this runner; ``read-tree``, ``add`` and ``write-tree`` run
        only with it. ``input`` is fed to stdin (otherwise stdin is closed).
        """
        words = list(argv)
        if not words:
            raise ForbiddenArgv("empty argv")
        if index_file is not None and index_file not in self._indexes:
            raise ForbiddenArgv("the index file was not made by this runner")
        words = self._with_submodule_option(words)
        validate_argv(words, index_file=index_file)
        cmd = [*PREFIX]
        if directory is not None:
            cmd += ["-C", os.fspath(directory)]
        cmd += words
        if self.record:
            self.calls.append(list(cmd))
        self.last_stderr = ""
        if self.dry_run:
            return 0, ""
        kwargs = (
            {"input": input} if input is not None else {"stdin": subprocess.DEVNULL}
        )
        try:
            done = subprocess.run(
                cmd,
                cwd=self.top,
                env=self._environment(index_file),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="surrogateescape",
                timeout=self.timeout,
                **kwargs,
            )
        except subprocess.TimeoutExpired:
            self.last_stderr = "timeout"
            return TIMEOUT_RC, ""
        self.last_stderr = done.stderr or ""
        return done.returncode, done.stdout or ""


# --- stage-plan, path mode (FR-031, FR-035, FR-038, FR-062 c to e, FR-063, design 4.5) --------
# The plan only reads. It names the files the agent writes outside the work tree and the
# argv the agent runs; it never writes a file, a ref or an index entry (DD-4, FR-011).
LIST_CAP = 200  # the display cap of ``vcs.emit``; the pathspec file is never cut (DD-3)
RUN_FOLDER = ".dev/implement"
DEV_COPY_FOLDER = ".claude"
GITLINK_MODE = "160000"

# The ``why`` tokens of ``skipped``. The design names a token for each rule but the first
# two: ``LEGACY_RUN_FOLDER`` (paths under ``.dev/implement/``, which is not gitignored) and
# ``IGNORED`` are chosen here, once, for Task 14 and the protocol text to share.
LEGACY_RUN_FOLDER = "legacy-run-folder"
IGNORED = "ignored"
OUTSIDE_REPO = "outside-repo"
GITLINK = "gitlink"
DEV_COPY_PATH = "dev-copy-path"
PATH_UNREPRESENTABLE = "path-unrepresentable"
DIRECTORY_ENTRY = "directory-entry"
ABSENT = "absent"
# FR-031 and FR-062 d, e refuse (the whole plan prints no argv); the other whys only drop
# the path from the commit set.
REFUSING_WHYS = (DEV_COPY_PATH, OUTSIDE_REPO, PATH_UNREPRESENTABLE)
_REFUSAL_TEXT = {
    DEV_COPY_PATH: "files under .claude/ other than settings.json are generated copies "
    "and are never staged here",
    OUTSIDE_REPO: "the path is absolute, climbs out with '..' or resolves through a "
    "symlink, so it is not inside the repository",
    PATH_UNREPRESENTABLE: "a comma, newline or control character cannot be carried by "
    "the ledger",
    DIRECTORY_ENTRY: "a files= entry names a folder; the ledger must list its files one by one",
}
_UNREPRESENTABLE = re.compile(f"[,{_CTRL}]")


class LookupFailed(Exception):
    """A lookup the helper needs failed (exit code 69)."""


def _read(
    git: GitRunner,
    argv: Sequence[str],
    ok: Tuple[int, ...] = (0,),
    input: Optional[str] = None,
) -> Tuple[int, str]:
    """Run one read; any exit code outside ``ok`` (a timeout included) is a failed lookup."""
    rc, out = git.run(argv, input=input)
    if rc not in ok:
        raise LookupFailed(f"git {argv[0]} exited {rc}")
    return rc, out


def _head_sha(git: GitRunner) -> Optional[str]:
    rc, out = _read(git, ["rev-parse", "--verify", "--quiet", "HEAD"], ok=(0, 1))
    return out.strip() if rc == 0 else None


def _head_entries(git: GitRunner, head: Optional[str]) -> Dict[str, Tuple[str, str]]:
    """``path -> (mode, blob)`` of the HEAD tree (a gitlink has mode 160000)."""
    if head is None:
        return {}
    _, out = _read(git, ["ls-tree", "-r", "-z", head])
    entries = {}
    for record in out.split("\0"):
        if record:
            meta, _, path = record.partition("\t")
            mode, _kind, sha = meta.split()
            entries[path] = (mode, sha)
    return entries


def _index_entries(
    git: GitRunner,
) -> Tuple[Dict[str, Tuple[str, str]], set]:
    """``path -> (mode, blob)`` of the index at stage 0, and the set of unmerged paths."""
    _, out = _read(git, ["ls-files", "--stage", "-z"])
    entries: Dict[str, Tuple[str, str]] = {}
    unmerged = set()
    for record in out.split("\0"):
        if record:
            meta, _, path = record.partition("\t")
            mode, sha, stage = meta.split()
            if stage == "0":
                entries[path] = (mode, sha)
            else:
                unmerged.add(path)
    return entries, unmerged


def _changed_in_work_tree(git: GitRunner) -> set:
    """Paths ``status`` reports (staged, unstaged or untracked), one per path."""
    _, out = _read(
        git,
        ["status", "--porcelain=v1", "-z", "--untracked-files=all", "--no-renames"],
    )
    return {record[3:] for record in out.split("\0") if len(record) > 3}


def _ignored_among(git: GitRunner, paths: Sequence[str]) -> set:
    """The paths ``check-ignore`` reports; a tracked path is never reported.

    The command reads its input as pathspecs and refuses magic such as ``:(glob)``. A
    leading ``./`` makes every name literal, and the same prefix comes back on the output.
    """
    if not paths:
        return set()
    _, out = _read(
        git,
        ["check-ignore", "-z", "--stdin"],
        ok=(0, 1),
        input="".join(f"./{path}\0" for path in paths),
    )
    return {path[2:] for path in out.split("\0") if path.startswith("./")}


def _normalize(raw: str) -> Optional[str]:
    """The repository-relative form of ``raw`` ('' for the top folder itself).

    None when it is absolute or climbs out with ``..`` (FR-062 e). Empty and ``.``
    segments drop out, so ``./a`` and ``a`` are one path.
    """
    if raw.startswith("/"):
        return None
    parts = []
    for part in raw.split("/"):
        if part == "..":
            return None
        if part not in ("", "."):
            parts.append(part)
    return "/".join(parts)


def _through_symlink(top: str, rel: str) -> bool:
    """A parent folder of ``rel`` is a symlink. Git cannot stage such a path ("beyond a
    symbolic link"), and one that leaves the repository must never be followed; a link
    that points back inside is refused too, as the same ``outside-repo``. The last
    segment may itself be a link: git stores it as a link."""
    current = top
    for part in rel.split("/")[:-1]:
        current = os.path.join(current, part)
        if os.path.islink(current):
            return True
        if not os.path.isdir(current):
            return False
    return False


def _under(path: str, folder: str) -> bool:
    return path == folder or path.startswith(folder + "/")


def _early_why(
    rel: str, top: str, gitlinks: Sequence[str], pathful: bool
) -> Optional[str]:
    """The first rule that drops ``rel`` before the ignore check, in this order: the legacy
    run folder, outside the repository, a ``.claude/`` copy, a gitlink."""
    if _under(rel, RUN_FOLDER):
        return LEGACY_RUN_FOLDER
    if pathful and _through_symlink(top, rel):
        return OUTSIDE_REPO
    # A `.claude/` path is refused before the ignore rule: the project ignores that
    # folder, and an ignored copy must still be refused, not silently dropped.
    if _under(rel, DEV_COPY_FOLDER) and rel not in {
        f"{DEV_COPY_FOLDER}/{name}" for name in DEV_MIRROR_ALLOW
    }:
        return DEV_COPY_PATH
    if any(_under(rel, link) for link in gitlinks):
        return GITLINK
    return None


def _late_why(rel: str, top: str, ignored: set, tracked: set) -> Optional[str]:
    """The rules after the early ones: ignored, unrepresentable, directory, absent."""
    if rel in ignored:
        return IGNORED
    if _UNREPRESENTABLE.search(rel):
        return PATH_UNREPRESENTABLE
    full = os.path.join(top, rel)
    if os.path.isdir(full) and not os.path.islink(full):
        return DIRECTORY_ENTRY
    if not os.path.lexists(full) and rel not in tracked:
        return ABSENT  # missing from the work tree, the index and HEAD
    return None


def _digest(commit_paths: Sequence[str], head: Optional[str]) -> str:
    raw = ("\0".join(commit_paths) + "\0" + (head or "")).encode(
        "utf-8", "surrogateescape"
    )
    return hashlib.sha256(raw).hexdigest()[:16]


def _empty_plan(
    status: str,
    reason: str,
    detail: Optional[str],
    head: Optional[str],
    skipped: Sequence[Tuple[str, str]],
) -> Dict[str, Any]:
    """A plan that prints no argv: nothing to do, or refused."""
    return {
        "status": status,
        "reason": reason,
        "detail": detail,
        "head_before": head,
        "tasks": [],
        "commit_paths": [],
        "s_count": 0,
        "skipped": [{"path": p, "why": w} for p, w in skipped],
        "add_argv": [],
        "commit_argv": [],
        "message_path": None,
        "pathspec_file": None,
        "truncated": len(skipped) > LIST_CAP,
    }


def plan_stage(
    git: GitRunner,
    paths: Optional[Sequence[str]] = None,
    *,
    extra_gitlinks: Sequence[str] = (),
    refusing: Sequence[str] = REFUSING_WHYS,
    extra_paths: Sequence[str] = (),
    pathspec_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Plan an add or a commit of ``paths`` (path mode of ``stage-plan``).

    ``paths`` are repository-relative (``git.top`` is the top folder). ``None`` plans a
    pathless commit: S is the index change set frozen now (HEAD tree against index,
    renames as both ends, FR-038, FR-117) and the commit runs ``commit -F <message>`` with
    no ``--only``. ``extra_gitlinks`` adds folders to the gitlink rule (the retained Q0
    tree of ledger mode). Returns the plan fields without the envelope; ``status`` is
    ``ok``, ``nothing`` (empty set, or no named path changed) or ``refused`` (a
    ``refusing`` rule hit; the first path in sorted order names the ``reason``).
    ``add_argv`` and ``commit_argv`` are the words after ``git``. Every list is sorted,
    so the same inputs give the same result.

    Ledger mode passes more: ``refusing`` (adds the directory entry), ``extra_paths``
    (the literal package expansion: joined to S as given, only the gitlink rule applies)
    and ``pathspec_path`` (where the agent writes the pathspec file; the default is a
    temporary file).
    """
    top = git.top
    head = _head_sha(git)
    head_entries = _head_entries(git, head)
    index_entries, unmerged = _index_entries(git)
    gitlinks = sorted(
        {p for p, (mode, _) in head_entries.items() if mode == GITLINK_MODE}
        | {p for p, (mode, _) in index_entries.items() if mode == GITLINK_MODE}
        | {link.rstrip("/") for link in extra_gitlinks}
    )
    pathful = paths is not None
    skipped: Dict[str, str] = {}
    pending: List[str] = []

    if pathful:
        for raw in paths:
            rel = _normalize(raw)
            if rel is None:
                skipped[raw] = OUTSIDE_REPO
            elif rel == "":
                skipped[raw] = DIRECTORY_ENTRY
            elif (why := _early_why(rel, top, gitlinks, True)) is not None:
                skipped[rel] = why
            elif rel not in pending:
                pending.append(rel)
        tracked = set(head_entries) | set(index_entries) | unmerged
        ignored = _ignored_among(git, pending)
        kept = []
        for rel in pending:
            why = _late_why(rel, top, ignored, tracked)
            if why is None:
                kept.append(rel)
            else:
                skipped[rel] = why
    else:
        frozen = sorted(
            p
            for p in set(head_entries) | set(index_entries) | unmerged
            if p in unmerged or head_entries.get(p) != index_entries.get(p)
        )
        kept = []
        for rel in frozen:
            why = _early_why(rel, top, gitlinks, False)
            if why is None:
                kept.append(rel)
            else:
                skipped[rel] = why

    skipped_list = sorted(skipped.items())
    hits = [(p, w) for p, w in skipped_list if w in refusing]
    if hits:
        path, why = hits[0]
        return _empty_plan(
            "refused", why, f"{path}: {_REFUSAL_TEXT[why]}", head, skipped_list
        )
    extra = {p for p in extra_paths if not any(_under(p, link) for link in gitlinks)}
    commit_paths = sorted(set(kept) | extra)
    if not commit_paths:
        return _empty_plan("nothing", "empty", None, head, skipped_list)
    if pathful and not (set(commit_paths) & _changed_in_work_tree(git)):
        return _empty_plan("nothing", "no-change", None, head, skipped_list)

    temp = os.path.realpath(tempfile.gettempdir())
    real_top = os.path.realpath(top)
    if _under(temp, real_top):
        raise LookupFailed("the temporary folder is inside the work tree")
    tag = _digest(commit_paths, head)
    message_path = os.path.join(temp, f"vcs-message-{tag}.txt")
    pathspec = None
    if pathful:
        content = "\0".join(commit_paths) + "\0"
        pathspec = {
            "path": pathspec_path or os.path.join(temp, f"vcs-pathspec-{tag}.nul"),
            "content": content,
            "sha256": hashlib.sha256(
                content.encode("utf-8", "surrogateescape")
            ).hexdigest(),
        }
        from_file = [f"--pathspec-from-file={pathspec['path']}", "--pathspec-file-nul"]
        add_argv = ["--literal-pathspecs", "add", *from_file]
        commit_argv = [
            "--literal-pathspecs",
            "commit",
            "--only",
            "-F",
            message_path,
            *from_file,
        ]
    else:
        add_argv = []
        commit_argv = ["commit", "-F", message_path]
    validate_agent_argv(add_argv)
    validate_agent_argv(commit_argv)
    return {
        "status": "ok",
        "reason": None,
        "detail": None,
        "head_before": head,
        "tasks": [],
        "commit_paths": commit_paths,
        "s_count": len(commit_paths),
        "skipped": [{"path": p, "why": w} for p, w in skipped_list],
        "add_argv": add_argv,
        "commit_argv": commit_argv,
        "message_path": message_path,
        "pathspec_file": pathspec,
        "truncated": len(commit_paths) > LIST_CAP or len(skipped_list) > LIST_CAP,
    }


# --- stage-plan, ledger mode (FR-060, FR-062, FR-073 to FR-076, FR-108, FR-110; design 4.5) ---
# Ledger mode finds the one boundary that needs a commit set, builds S from the ledger and
# runs the checks that keep a commit from taking work that is not the task's. It reads only:
# the candidate tree is made in a private index, the helper writes no ref (the agent pins
# the tree with a literal ref update), no index entry and no file.
SIDECAR = "commits.md"
PIN_ROOT = "refs/superclaude/implement"
LEDGER_REFUSING = (*REFUSING_WHYS, DIRECTORY_ENTRY)
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_PATH_FILE = re.compile(r"^commit-paths-[0-9a-f]{64}-a[0-9]+\.txt$")


@dataclass(frozen=True)
class RunLayout:
    """Where one implement run keeps its files (``refs/retry.md``, ``refs/managed-workspace.md``).

    ``base`` is the run folder (legacy) or the package folder (managed). The retries
    folder is ``<run folder>/retries`` or ``<package>/artifacts/retries``. The sidecar is
    ``<run folder>/commits.md`` or ``<package>/artifacts/commits.md`` (FR-100; the design's
    "always beside the ledger" sentence in section 4.3 is the one that gives way, because
    the managed ledger is ``<package>/progress.md``).
    """

    managed: bool
    slug: str
    base: str
    retries: str
    sidecar: str


def run_layout(run_dir: str, package: Optional[str] = None) -> RunLayout:
    """The layout of a run; the slug is the folder name, which survives the move to ``done/``."""
    managed = package is not None
    base = os.path.realpath(package if managed else run_dir)
    inner = os.path.join(base, "artifacts") if managed else base
    return RunLayout(
        managed,
        os.path.basename(base),
        base,
        os.path.join(inner, "retries"),
        os.path.join(inner, SIDECAR),
    )


def boundary_identity(side: Sidecar, layout: RunLayout) -> Tuple[str, str, str]:
    """``(repo_id, ledger_id, source_id)`` for ``build_boundaries``.

    The repository/worktree and source identities are the ``worktree=`` and ``source=`` of
    the sidecar's first ``run`` line: it never changes, so a key stays the same when a
    later run spells the source differently. With no run line there is no grant and no
    boundary is eligible, so the placeholder ``-`` never keys a commit.
    """
    first = side.runs[0] if side.runs else None
    return (
        first.worktree if first else "-",
        ledger_identity("managed" if layout.managed else "legacy", layout.slug),
        first.source if first else "-",
    )


def _read_file(path: str) -> Optional[str]:
    """The text of ``path`` byte for byte (no newline translation); None when it is absent."""
    try:
        with open(
            path, encoding="utf-8", errors="surrogateescape", newline=""
        ) as handle:
            return handle.read()
    except (FileNotFoundError, NotADirectoryError):
        return None


def _current_branch(git: GitRunner) -> Optional[str]:
    rc, out = _read(git, ["symbolic-ref", "-q", "HEAD"], ok=(0, 1))
    return out.strip() if rc == 0 else None


def _tree_entries(git: GitRunner, sha: str) -> Optional[Dict[str, Tuple[str, str]]]:
    """Entries of the tree ``sha``; None when it is not a tree object (``nogit``, a commit
    used as the start fallback, or an object that is gone)."""
    if not _SHA40.match(sha):
        return None
    rc, out = git.run(["cat-file", "-t", sha])
    if rc == 128 or (rc == 0 and out.strip() != "tree"):
        return None
    if rc != 0:
        raise LookupFailed(f"git cat-file exited {rc}")
    return _head_entries(git, sha)


def _tree_with(git: GitRunner, base: Optional[str], paths: Sequence[str]) -> str:
    """The tree of ``base`` (a commit, None for none) with ``paths`` taken from the work tree.

    Made in a private index outside ``.git/``: ``read-tree``, a literal pathspec add (the
    names arrive on stdin with the ``:(literal)`` magic) and ``write-tree``. A path that is
    gone from the work tree and from ``base`` is left out; one gone from the work tree
    but present in ``base`` is a deletion. The method is the Q0 snapshot's (private index,
    read-tree, add, write-tree), so its trees compare with the Q0 and accepted trees.
    """
    held = _head_entries(git, base)
    present = [
        p for p in paths if os.path.lexists(os.path.join(git.top, p)) or p in held
    ]
    with git.private_index() as index:
        argv = ["read-tree", base] if base else ["read-tree", "--empty"]
        rc, _ = git.run(argv, index_file=index)
        if rc != 0:
            raise LookupFailed(f"git read-tree exited {rc}")
        if present:
            names = "".join(f":(literal){p}\0" for p in present)
            rc, _ = git.run(
                ["add", "--pathspec-from-file=-", "--pathspec-file-nul"],
                index_file=index,
                input=names,
            )
            if rc != 0:
                raise LookupFailed(f"the private-index add exited {rc}")
        rc, out = git.run(["write-tree"], index_file=index)
    if rc != 0:
        raise LookupFailed(f"git write-tree exited {rc}")
    return out.strip()


def _failed(
    reason: str,
    detail: str,
    paths: Sequence[str] = (),
    advice: Sequence[str] = (),
) -> Dict[str, Any]:
    return {
        "reason": reason,
        "detail": detail,
        "paths": sorted(paths),
        "advice": list(advice),
    }


def _member_files(boundary: Boundary, product: Sequence[str]) -> Dict[str, List[str]]:
    """Each member's own anchor ``files=`` entries that are product paths of S, sorted."""
    wanted = set(product)
    return {
        tid: sorted({n for f in gen.files if (n := _normalize(f)) in wanted})
        for tid, gen in zip(boundary.members, boundary.gens)
    }


def _check_boundary(
    git: GitRunner,
    boundary: Boundary,
    slug: str,
    retries: str,
    product: Sequence[str],
    head: Optional[str],
    rewritten_tree: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """The first failed staging check of a boundary, else None.

    Order: ``no-snapshot`` (FR-073: a member's start line holds no tree, so no Q0 files
    exist either), ``branch-unproven`` and ``branch-changed`` (FR-054: ``q0-branch`` of the
    first member against the current symbolic ref), ``head-moved`` (HEAD against each
    member's ``q0-head``), ``foreign-change`` (FR-075), ``no-accepted-tree`` and
    ``changed-after-review`` (FR-074). Only product paths are compared (FR-132): the
    package evidence is rebuilt for every attempt. Each member is checked against its own
    start tree and accepted tree for its own anchor files. ``rewritten_tree`` (a retry
    after a ``hook-rewrite`` refusal whose rewritten paths were reviewed again, FR-065,
    FR-107) is a second tree a product path may equal.
    """
    members = list(zip(boundary.members, boundary.gens))
    mine = _member_files(boundary, product)
    starts = {}
    for tid, gen in members:
        entries = _tree_entries(git, gen.start_sha)
        if entries is None:
            return _failed(
                "no-snapshot",
                f"T{tid}: the start line ({gen.start_sha}) holds no tree, so nothing "
                "proves the work tree before the task",
            )
        starts[tid] = entries
    first = boundary.members[0]
    text = _read_file(os.path.join(retries, f"T{first}", "q0-branch"))
    saved = text.strip() if text else ""
    if not saved.startswith("refs/"):
        return _failed(
            "branch-unproven",
            f"T{first}: q0-branch is missing or is not a full branch ref, so the "
            "branch cannot be proved",
        )
    current = _current_branch(git)
    if current != saved:
        return _failed(
            "branch-changed",
            f"T{first}: the task started on {saved}; the branch is now {current or 'detached'}",
        )
    for tid, _ in members:
        text = _read_file(os.path.join(retries, f"T{tid}", "q0-head"))
        recorded = text.strip() if text else None
        if recorded is None or recorded != head:
            return _failed(
                "head-moved",
                f"T{tid}: HEAD is {head or 'unborn'}; q0-head records {recorded or 'nothing'}",
            )
    at_head = _head_entries(git, head)  # HEAD is every member's q0-head here
    foreign = sorted(
        {
            p
            for tid, _ in members
            for p in mine[tid]
            if at_head.get(p) != starts[tid].get(p)
        }
    )
    if foreign:
        return _failed(
            "foreign-change",
            f"{', '.join(foreign)}: carried an uncommitted change before the task started",
            foreign,
        )
    accepted = {}
    for tid, gen in members:
        ref = f"{PIN_ROOT}/{slug}/accepted/T{tid}-s{gen.start_ordinal}"
        rc, out = _read(
            git, ["rev-parse", "--verify", "--quiet", f"{ref}^{{tree}}"], ok=(0, 1)
        )
        if rc != 0:
            return _failed(
                "no-accepted-tree", f"T{tid}: the accepted pin {ref} is missing"
            )
        accepted[tid] = (ref, _head_entries(git, out.strip()))
    now = _head_entries(git, _tree_with(git, head, product)) if product else {}
    rewritten = _head_entries(git, rewritten_tree) if rewritten_tree else None
    changed, advice = set(), []
    for tid, _ in members:
        ref, entries = accepted[tid]
        paths = [p for p in mine[tid] if now.get(p) != entries.get(p)]
        if rewritten is not None:
            paths = [p for p in paths if now.get(p) != rewritten.get(p)]
        if paths:
            changed.update(paths)
            quoted = " ".join(shlex.quote(p) for p in paths)
            advice.append(f"git restore --source={ref} -- {quoted}")
    if changed:
        advice.append("compare first: this overwrites any newer edit")
        names = ", ".join(sorted(changed))
        return _failed(
            "changed-after-review",
            f"{names}: no longer equal to the accepted tree of the review",
            sorted(changed),
            advice,
        )
    return None


def _open_attempt(boundary: Boundary, side: Sidecar) -> Optional[Attempt]:
    """The latest prepared attempt of a boundary that has no result line after it."""
    attempts = side.attempts.get(boundary.key)
    if not attempts or boundary.key in side.resolved:
        return None
    done = side.terminal.get(boundary.key)
    if done is not None and done.line_no > attempts[-1].line_no:
        return None
    return attempts[-1]


def _stage_inputs(
    git: GitRunner, layout: RunLayout, boundary: Boundary, attempt: int
) -> Optional[Dict[str, Any]]:
    """The inputs ``plan_stage`` takes for ``attempt`` of a boundary: ``paths`` (the anchor
    ``files=`` union), the gitlinks of the retained Q0 trees, the refusing rules, the literal
    expansion of the package folder of a managed run (FR-076) and the path file the agent
    writes. None when the package folder is not inside the repository."""
    top = os.path.realpath(git.top)
    extra: List[str] = []
    if layout.managed:
        rel = _normalize(os.path.relpath(layout.base, top))
        if not rel:  # the top folder itself, or a folder that climbs out of it
            return None
        sidecar_folder = os.path.dirname(layout.sidecar)
        _, out = _read(
            git,
            ["ls-files", "-z", "--cached", "--others", "--exclude-standard", "--",
             f":(literal){rel}"],
        )  # fmt: skip
        extra = sorted(
            {
                p
                for p in out.split("\0")
                if p
                and not (
                    os.path.dirname(os.path.join(top, p)) == sidecar_folder
                    and _PATH_FILE.match(os.path.basename(p))
                )
            }
        )
    q0_links: List[str] = []
    for gen in boundary.gens:
        entries = _tree_entries(git, gen.start_sha)
        q0_links += [
            p for p, (mode, _) in (entries or {}).items() if mode == GITLINK_MODE
        ]
    path_file = os.path.join(
        os.path.dirname(layout.sidecar),
        f"commit-paths-{boundary.key}-a{attempt}.txt",
    )
    return {
        "paths": sorted({f for gen in boundary.gens for f in gen.files}),
        "extra_gitlinks": q0_links,
        "refusing": LEDGER_REFUSING,
        "extra_paths": extra,
        "pathspec_path": path_file,
    }


_LEDGER_DEFAULTS: Dict[str, Any] = {
    "key": None,
    "attempt": None,
    "parent": None,
    "branch": None,
    "accepted": [],
    "boundary_ref": None,
    "candidate_tree": None,
    "state": None,
    "paths": [],
    "advice": [],
}


def _ledger_result(plan: Dict[str, Any], **fields: Any) -> Dict[str, Any]:
    """``plan`` with every ledger-mode field present (a fresh list for each list field)."""
    fresh = {
        k: list(v) if isinstance(v, list) else v for k, v in _LEDGER_DEFAULTS.items()
    }
    return {**plan, **fresh, **fields}


def plan_ledger(
    git: GitRunner,
    ledger: str,
    run_dir: str,
    package: Optional[str] = None,
    candidate: bool = False,
) -> Dict[str, Any]:
    """Ledger mode of ``stage-plan``: plan the commit of the one boundary that needs it.

    Without ``candidate`` the boundary is the first one ``derive_state`` leaves unsettled,
    judged for a run that carries the flag. Its action must be ``prepare`` or ``retry``
    (the plan then names the next attempt: 1, or the last attempt plus one, DD-11) or
    ``record-skipped`` (``nothing`` with reason ``mixed-authorization``). An empty set
    is ``nothing`` too (the executor writes ``commit skipped ... reason=empty``). A retry
    is decided by ``_retry_decision``, the same function ``reconcile`` uses, so the two
    verbs never disagree. Refusals of this function: ``no-due-boundary``,
    ``out-of-protocol``, ``unsettled`` (the state is in ``state``), the retry refusals
    ``candidate-changed``, ``no-accepted-tree``, ``index-locked`` and ``commit-interrupted``,
    ``ledger-corrupt``, ``sidecar-corrupt``, ``sidecar-mismatch``, ``ledger-identity``,
    ``outside-repo``, the path refusals, ``pin-conflict`` and the staging checks of
    ``_check_boundary``.

    With ``candidate`` the boundary is the one whose latest prepared attempt has no result
    line; HEAD must still be the prepared parent. The same checks run again. The tree of
    that parent plus S is built in a private index and returned as ``candidate_tree``;
    ``pin-conflict`` when ``boundary_ref`` already exists with another target. S holds the
    managed sidecar as it is on disk now, which is the frozen prepared bytes (FR-108); the
    path file ``commit-paths-<key>-a<n>.txt`` is never part of S.
    """
    head = _head_sha(git)
    layout = run_layout(run_dir, package)

    def refuse(reason: str, detail: str, **fields: Any) -> Dict[str, Any]:
        plan = _empty_plan("refused", reason, detail, head, fields.pop("skipped", ()))
        return _ledger_result(plan, **fields)

    ledger_text = _read_file(ledger)
    if ledger_text is None:
        raise LookupFailed(f"ledger not found: {ledger}")
    try:
        view = parse_ledger(ledger_text)
        side = parse_sidecar(_read_file(layout.sidecar) or "")
        validate_runs(side.runs, ledger_text)
        repo_id, ledger_id, source_id = boundary_identity(side, layout)
    except (LedgerCorrupt, SidecarCorrupt, SidecarMismatch) as err:
        return refuse(err.reason, str(err))
    except ValueError as err:
        return refuse("ledger-identity", str(err))
    boundaries = build_boundaries(view, side.runs, repo_id, ledger_id, source_id)
    ctx = _Ctx(git, layout, side, ledger, ledger_text, head, True)

    chosen: Optional[Boundary] = None
    if candidate:
        for item in boundaries:
            last = _open_attempt(item, side)
            if last is not None:
                chosen, attempt = item, last.attempt
                if last.parent != head:
                    return refuse(
                        "head-moved",
                        f"HEAD is {head or 'unborn'}; the prepared parent is {last.parent}",
                        key=item.key,
                        tasks=item.members,
                    )
                break
        if chosen is None:
            return refuse(
                "no-due-boundary", "no prepared attempt waits for a candidate"
            )
    else:
        for item in boundaries:
            facts, verdict = _boundary_facts(ctx, item, with_s=False)
            state, action = derive_state(item, side, facts, True)
            if (state, action) == ("settled", "none"):
                continue
            chosen = item
            if action == "stop-out-of-protocol":
                return refuse(
                    "out-of-protocol",
                    "a later task started after this boundary was complete",
                    key=item.key, tasks=item.members, state=state,
                )  # fmt: skip
            if action in ("stop-unsettled", "stop-uncertain", "record-recovered"):
                if verdict is not None and not verdict.allowed:
                    return refuse(
                        verdict.reason, verdict.detail,
                        key=item.key, tasks=item.members, state=state,
                        paths=sorted(verdict.paths),
                    )  # fmt: skip
                return refuse(
                    "unsettled",
                    f"the boundary is {state}: it needs the owner's choice or a recovery record",
                    key=item.key, tasks=item.members, state=state,
                )  # fmt: skip
            break
        if chosen is None:
            return refuse("no-due-boundary", "no boundary is waiting for a commit")
        done = side.attempts.get(chosen.key)
        attempt = done[-1].attempt + 1 if done else 1
        if action == "record-skipped":
            plan = _empty_plan("nothing", "mixed-authorization", None, head, ())
            return _ledger_result(
                plan, key=chosen.key, tasks=chosen.members, state=state
            )

    key, members = chosen.key, chosen.members
    boundary_ref = f"{PIN_ROOT}/{layout.slug}/boundary/{key}-a{attempt}"
    accepted = [
        f"{PIN_ROOT}/{layout.slug}/accepted/T{tid}-s{gen.start_ordinal}"
        for tid, gen in zip(members, chosen.gens)
    ]
    common = {
        "key": key,
        "tasks": members,
        "attempt": attempt,
        "parent": head,
        "branch": _current_branch(git),
        "accepted": accepted,
        "boundary_ref": boundary_ref,
    }

    inputs = _stage_inputs(git, layout, chosen, attempt)
    if inputs is None:
        return refuse(
            OUTSIDE_REPO, "the package folder is not inside the repository", **common
        )
    plan = plan_stage(git, inputs.pop("paths"), **inputs)
    if plan["status"] != "ok":
        return _ledger_result(plan, **common)
    kept = set(inputs["extra_paths"])
    product = [p for p in plan["commit_paths"] if p not in kept]
    rewrite, credited = _credited_rewrite(ctx, chosen)
    failed = _check_boundary(
        git, chosen, layout.slug, layout.retries, product, head,
        rewrite if credited else None,
    )  # fmt: skip
    if failed:
        skipped = [(item["path"], item["why"]) for item in plan["skipped"]]
        empty = _empty_plan(
            "refused", failed.pop("reason"), failed.pop("detail"), head, skipped
        )
        return _ledger_result(empty, **common, **failed)
    plan["tasks"] = members
    result = _ledger_result(plan, **common, product_paths=product)
    if candidate:
        tree = _tree_with(git, head, plan["commit_paths"])
        rc, out = _read(
            git, ["rev-parse", "--verify", "--quiet", boundary_ref], ok=(0, 1)
        )
        if rc == 0 and out.strip() != tree:
            return refuse(
                "pin-conflict",
                f"{boundary_ref} already points at {out.strip()}, not at {tree}",
                **common,
            )
        result["candidate_tree"] = tree
    return result


# --- verify (FR-036, FR-108, FR-113, FR-130; design sections 5.5 and 6.1) ---------------------
# ``verify`` is asked what the history proves after the commit call, or by a later run. It
# reads only: the trees it needs are built in a private index and it retries nothing. The
# executor writes the matching ``refused`` or ``uncertain`` line and never retries in the
# same run (the ref text pins that; Task 29 writes it, Task 34 checks it).
HOOK_CLASSES = (
    "blocked-by-host", "hook-failed", "hook-rewrite", "hook-rewrite-evidence",
    "hook-rewrite-committed", "hook-rewrite-pinned", "commit-error",
)  # fmt: skip
# The commit call reports a shell status (0 to 255). A host hook that refuses the Bash call
# gives no status at all, so the caller passes a negative number for "git never ran".
HOST_DENIED_EXIT = -1
INTERRUPTED_ABOVE = (
    128  # FR-116: a status above this (or a timeout) is not classified here
)
NOT_COMPARED = "not-compared"
DEFERRED = "deferred"
OUTSIDE_UNVERIFIED = "outside-unverified"


def _tree_of(git: GitRunner, ref: str) -> Optional[str]:
    """The tree a ref or commit names; None when it does not resolve."""
    rc, out = _read(
        git, ["rev-parse", "--verify", "--quiet", f"{ref}^{{tree}}"], ok=(0, 1)
    )
    return out.strip() if rc == 0 else None


def _changed_between(git: GitRunner, before: str, after: str) -> List[str]:
    """Paths whose entry differs between two trees or commits (an addition, a deletion, a
    mode or a type change included), sorted. Submodule entries are left out, as for every
    implement-side diff."""
    _, out = _read(git, ["diff", "--name-only", "-z", "--no-renames", before, after])
    return sorted(p for p in out.split("\0") if p)


def _snapshot(git: GitRunner, base: str) -> str:
    """The Q0 snapshot method: a private index, ``read-tree``, ``add -A``, ``write-tree``."""
    with git.private_index() as index:
        for argv in (["read-tree", base], ["add", "-A"]):
            rc, _ = git.run(argv, index_file=index)
            if rc != 0:
                raise LookupFailed(f"git {argv[0]} exited {rc} in the private index")
        rc, out = git.run(["write-tree"], index_file=index)
    if rc != 0:
        raise LookupFailed(f"git write-tree exited {rc}")
    return out.strip()


def _read_bytes(path: str) -> Optional[bytes]:
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except (FileNotFoundError, NotADirectoryError, IsADirectoryError):
        return None


def _outside(
    git: GitRunner, parent: str, worktree_ref: str, s_paths: Optional[Sequence[str]]
) -> Dict[str, Any]:
    """FR-113: every path outside S against the worktree tree pinned before the commit.

    A second snapshot (the parent plus the work tree as it is now) is compared with the
    pinned one over the whole tree; S itself is left out. Anything that stops the comparison
    is ``outside-unverified``, never "no changes".
    """
    unverified = {
        "outside": OUTSIDE_UNVERIFIED,
        "outside_changed": None,
        "outside_paths": [],
    }
    if s_paths is None:
        return unverified
    try:
        before = _tree_of(git, worktree_ref)
        if before is None:
            return unverified
        inside = set(s_paths)
        paths = [
            p
            for p in _changed_between(git, before, _snapshot(git, parent))
            if p not in inside
        ]
    except LookupFailed:
        return unverified
    return {
        "outside": "outside-changed" if paths else "unchanged",
        "outside_changed": len(paths),
        "outside_paths": paths,
    }


def _commit_set(
    git: GitRunner,
    folder: Optional[str],
    key: str,
    attempt: int,
    prepared: Optional[Attempt],
    parent: str,
    cand_tree: Optional[str],
) -> Tuple[Optional[List[str]], Optional[bool]]:
    """``(S, proof)``. S is the path file beside the sidecar when its hash is the prepared
    line's ``paths=`` (proof True); a file that does not match gives the paths the candidate
    changes (proof False); no file and no sidecar give the same fallback (proof None). S is
    None when neither source exists."""
    proof: Optional[bool] = None
    raw = (
        _read_bytes(os.path.join(folder, f"commit-paths-{key}-a{attempt}.txt"))
        if folder and prepared
        else None
    )
    if raw is not None:
        proof = hashlib.sha256(raw).hexdigest() == prepared.paths
        if proof:
            names = raw.decode("utf-8", "surrogateescape").split("\0")
            return [p for p in names if p], True
    if cand_tree is None:
        return None, proof
    return _changed_between(git, parent, cand_tree), proof


def _plan_source_hold(pkg: str, prepared: Attempt) -> bool:
    """The work-tree bytes of the managed plan and source still hash to the prepared pins."""
    for name, pin in (
        (f"{os.path.basename(pkg)}.md", prepared.plan),
        ("source.md", prepared.source),
    ):
        if pin == "-":
            continue
        raw = _read_bytes(os.path.join(pkg, name))
        if raw is None or hashlib.sha256(raw).hexdigest() != pin:
            return False
    return True


def _commit_facts(git: GitRunner, sha: str) -> Tuple[List[str], List[str]]:
    """``(parents, Implement-Boundary keys)`` of a commit, from its object text."""
    _, out = _read(git, ["cat-file", "-p", sha])
    header, _, message = out.partition("\n\n")
    parents = [ln[7:] for ln in header.split("\n") if ln.startswith("parent ")]
    keys = [
        m.group(1) for ln in message.split("\n") if (m := _BOUNDARY_TRAILER.match(ln))
    ]
    return parents, keys


@dataclass
class _Verify:
    """What ``verify_commit`` has gathered; the two branches below read it."""

    git: GitRunner
    key: str
    parent: str
    head: Optional[str]
    cand_tree: Optional[str]
    s_paths: Optional[List[str]]
    paths_ok: Optional[bool]
    pins_ok: Optional[bool]  # None: a legacy run, nothing is pinned
    pkg_rel: Optional[str]  # the managed package folder, relative to the top
    proof: Dict[str, Any]

    def in_package(self, path: str) -> bool:
        return self.pkg_rel is not None and path.startswith(self.pkg_rel + "/")


def _verdict(
    status: str, reason: Optional[str], cls: Optional[str] = None, **fields: Any
):
    return {"status": status, "reason": reason, "class": cls, **fields}


def _hook_class(name: str, **fields: Any) -> Dict[str, Any]:
    return _verdict(name, name, name, **fields)


def _at_parent(c: _Verify, exit_code: Optional[int]) -> Dict[str, Any]:
    """HEAD is the prepared parent: nothing was committed (DD-11 covers missing pins)."""
    if exit_code is None or exit_code == 0:
        return _verdict("pending", "head-at-parent")
    if exit_code < 0:
        return _hook_class("blocked-by-host")
    if exit_code != 1:  # 128 is git's own failure; the other statuses are unexpected
        return _hook_class("commit-error")
    if c.cand_tree is None or c.s_paths is None:
        return _verdict("pending", "candidate-missing")
    worktree = _tree_with(c.git, c.parent, c.s_paths)
    changed = _changed_between(c.git, c.cand_tree, worktree)
    if c.pins_ok is False:
        return _hook_class("hook-rewrite-pinned", changed_paths=changed)
    if not changed:
        return _hook_class("hook-failed")
    managed = c.pkg_rel is not None
    only_evidence = managed and all(c.in_package(p) for p in changed)
    name = "hook-rewrite-evidence" if only_evidence else "hook-rewrite"
    return _hook_class(name, changed_paths=changed, rewritten_tree=worktree)


def _moved(c: _Verify) -> Dict[str, Any]:
    """HEAD moved: the FR-108 predicate, in the order that names the most specific cause."""
    if c.head is None:
        return _verdict("uncertain", "history-differs")
    parents, keys = _commit_facts(c.git, c.head)
    c.proof["parent"] = parents == [c.parent]
    c.proof["trailer"] = c.key in keys
    if not c.proof["parent"]:
        return _verdict("uncertain", "history-differs")
    if not c.proof["trailer"]:
        return _verdict("uncertain", "trailer-missing")
    if c.cand_tree is None:
        return _verdict("uncertain", "candidate-missing")
    changed = _changed_between(c.git, c.parent, c.head)
    if c.pins_ok is False:
        return _hook_class("hook-rewrite-pinned", changed_paths=changed)
    head_tree = _tree_of(c.git, c.head)
    if head_tree != c.cand_tree:
        return _hook_class(
            "hook-rewrite-committed", changed_paths=changed, rewritten_tree=head_tree
        )
    if c.paths_ok is False:
        return _verdict("uncertain", "paths-mismatch")
    if c.s_paths is None or not set(changed) <= set(c.s_paths):
        return _verdict("uncertain", "paths-outside-s")
    return _verdict("committed", None, sha=c.head, changed_paths=changed)


def verify_commit(
    git: GitRunner,
    key: str,
    attempt: int,
    parent: str,
    candidate_ref: str,
    worktree_ref: str,
    exit_code: Optional[int] = None,
    ledger: Optional[str] = None,
    sidecar: Optional[str] = None,
    outside: bool = True,
) -> Dict[str, Any]:
    """What happened to attempt ``attempt`` of boundary ``key`` (FR-036, FR-108, FR-130).

    ``status`` is ``committed`` (the commit is proved), ``pending`` (HEAD is the prepared
    ``parent``, nothing was committed), a class of ``HOOK_CLASSES``, ``uncertain`` (other
    history or incomplete proof: the owner decides, FR-120), ``interrupted`` (a status above
    128: not classified, FR-116) or ``refused`` (the sidecar does not hold the attempt).
    ``committed`` needs all of FR-108: HEAD has one parent and it is ``parent``; HEAD's tree
    is the one ``candidate_ref`` pins; the changed paths are inside S; the
    ``Implement-Boundary:`` trailer carries ``key``; the managed plan and source bytes still
    hash to the prepared pins. ``exit_code`` is the commit call's shell status; None means
    unknown (a later run), a negative number means git never ran (``HOST_DENIED_EXIT``).
    S is the ``commit-paths-<key>-a<n>.txt`` file beside the sidecar. ``ledger`` and
    ``sidecar`` are optional; without the sidecar nothing is pinned, so only the candidate,
    the parent and the trailer are proved. The package folder of a managed run is the
    ledger's folder. Every result carries ``head_before`` (``parent``), ``head_after``, the
    FR-113 comparison (``outside``, ``outside_changed``, ``outside_paths``, skipped when
    ``interrupted``) and, for the three rewrite classes that name one, ``rewritten_tree``
    and the ``rewritten_ref`` the executor pins it under. Nothing is written.
    ``outside=False`` skips the comparison (``reconcile`` asks only whether the commit is
    proved; the executor takes the comparison with its own ``verify`` call).
    """
    head = _head_sha(git)
    out: Dict[str, Any] = {
        "status": None, "reason": None, "class": None, "sha": None, "detail": None,
        "key": key, "attempt": attempt, "head_before": parent, "head_after": head,
        "changed_paths": [], "rewritten_tree": None, "rewritten_ref": None,
        "outside": NOT_COMPARED, "outside_changed": None, "outside_paths": [],
        "proof": {
            "parent": None, "trailer": None, "candidate": None, "paths": None,
            "plan_source": None,
        },
    }  # fmt: skip

    def refuse(reason: str, detail: str) -> Dict[str, Any]:
        out.update(status="refused", reason=reason, detail=detail)
        return out

    prepared: Optional[Attempt] = None
    if sidecar:
        try:
            side = parse_sidecar(_read_file(sidecar) or "")
        except (SidecarCorrupt, SidecarMismatch) as err:
            return refuse(err.reason, str(err))
        prepared = next(
            (a for a in side.attempts.get(key, []) if a.attempt == attempt), None
        )
        if prepared is None:
            return refuse(
                "unknown-attempt",
                f"the sidecar has no prepared line for attempt {attempt}",
            )
        if prepared.parent != parent:
            return refuse(
                "parent-mismatch", f"the prepared line names parent {prepared.parent}"
            )
    if exit_code is not None and exit_code > INTERRUPTED_ABOVE:
        out.update(
            status="interrupted",
            reason="commit-interrupted",
            outside=DEFERRED,
            detail="the commit call did not finish normally; establish that no git or "
            "hook process is still running before any classification (FR-116)",
        )
        return out

    cand_tree = _tree_of(git, candidate_ref)
    out["proof"]["candidate"] = cand_tree is not None
    folder = os.path.dirname(os.path.realpath(sidecar)) if sidecar else None
    s_paths, paths_ok = _commit_set(
        git, folder, key, attempt, prepared, parent, cand_tree
    )
    out["proof"]["paths"] = paths_ok
    managed = prepared is not None and (prepared.plan != "-" or prepared.source != "-")
    pkg = pins_ok = pkg_rel = None
    slug = os.path.basename(folder) if folder else None
    if managed:
        base = os.path.dirname(ledger) if ledger else os.path.dirname(folder)
        pkg = os.path.realpath(base)
        pkg_rel = os.path.relpath(pkg, os.path.realpath(git.top))
        pins_ok = _plan_source_hold(pkg, prepared)
        slug = os.path.basename(pkg)
    out["proof"]["plan_source"] = pins_ok
    c = _Verify(
        git,
        key,
        parent,
        head,
        cand_tree,
        s_paths,
        paths_ok,
        pins_ok,
        pkg_rel,
        out["proof"],
    )
    out.update(_at_parent(c, exit_code) if head == parent else _moved(c))
    if out["rewritten_tree"] and slug:
        out["rewritten_ref"] = f"{PIN_ROOT}/{slug}/rewritten/{key}-a{attempt}"
    if outside:
        out.update(_outside(git, parent, worktree_ref, s_paths))
    return out


# --- reconcile (FR-102 to FR-108, FR-065, FR-116, FR-132, DD-5, DD-11; design 5.2, 5.4, 5.6) ---
# ``reconcile`` is asked at the start of every invocation that carries the flag or finds a
# ``commits.md``: for each boundary of the ledger, what state is it in and what is the one
# action this run may take. It reads the ledger, the sidecar, the run's flag, the managed plan
# pins and git, applies ``derive_state`` and prints the result. It writes nothing: the agent
# appends every line and makes every call the action names.
#
# The retry decision lives here (``_retry_decision``), and ``plan_ledger`` calls the same
# function, so ``reconcile`` and ``stage-plan`` never disagree. A retry of a pending or
# refused attempt at the parent needs: (1) for an attempt with no result line, that nothing
# of the earlier commit call may still run (FR-116: no ``index.lock``, no git or hook process
# of this work tree that the probe can see); (2) that the product paths (the ``files=`` union,
# never the package evidence, FR-132) equal the accepted tree; or, after a ``hook-rewrite``
# refusal, the tree it pinned as ``rewritten=``, but only once a member ``complete`` or
# ``Ruling`` line stands after the anchor and after the run that recorded the refusal (FR-065:
# a flag typed before the disclosure is not that review). A refusal line carries no ledger
# offset, so a review line written in the same run before the refusal cannot be told from one
# written after it; the rule credits it (stated limit, it needs a ``hook-rewrite`` refusal
# after a post-anchor review in one run, which the commit step does not produce).
@dataclass(frozen=True)
class RetryVerdict:
    """Whether a new attempt may be made now, and if not, why (``reason`` is a STOP token)."""

    allowed: bool
    reason: str
    detail: str = ""
    paths: Tuple[str, ...] = ()


@dataclass
class _Ctx:
    """What one reconcile or stage-plan call has read; every function below takes it."""

    git: GitRunner
    layout: RunLayout
    side: Sidecar
    ledger_path: Optional[str]
    ledger_text: str
    head: Optional[str]
    flag: bool


def _live_git_processes(top: str) -> Optional[List[str]]:
    """Process ids (as text) of git or hook processes working in ``top`` (Linux ``/proc``).

    A process counts when its working folder is inside the work tree and its command is
    ``git`` or ``git-*``, or one of its first three words names a ``/hooks/`` script (a hook
    run through its interpreter or directly). None when the process table cannot be read
    (no ``/proc``): "unknown" is never proof. UNVERIFIED: a hook framework child with another
    name and folder is not seen, a hooks folder not named ``hooks`` is not seen, and a
    process of another user may hide its working folder.
    """
    root = "/proc"
    try:
        names = os.listdir(root)
    except OSError:
        return None
    here, me = os.path.realpath(top), os.getpid()
    found = []
    for name in sorted(names):
        if not name.isdigit() or int(name) == me:
            continue
        try:
            cwd = os.path.realpath(os.readlink(f"{root}/{name}/cwd"))
            with open(f"{root}/{name}/cmdline", "rb") as handle:
                words = [
                    w.decode("utf-8", "replace") for w in handle.read().split(b"\0")
                ]
        except OSError:
            continue
        words = [w for w in words[:3] if w]
        if not words or not _under(cwd, here):
            continue
        base = os.path.basename(words[0])
        if (
            base == "git"
            or base.startswith("git-")
            or any("/hooks/" in w for w in words)
        ):
            found.append(name)
    return found


def quiescence(git: GitRunner) -> Tuple[Optional[bool], str]:
    """``(proved, basis)``: may an earlier commit call still be running (FR-116)?

    ``(False, "index-locked")`` when ``index.lock`` exists, ``(False, "git-process-running")``
    when ``_live_git_processes`` sees one, ``(None, "unknown")`` when it cannot look, and
    ``(True, "none-seen")`` otherwise. ``True`` is the helper's observation, not a proof about
    every hook process (see ``_live_git_processes``); the protocol text still tells the person
    to confirm before restoring or resolving.
    """
    _, out = _read(git, ["rev-parse", "--git-path", "index.lock"])
    if os.path.exists(os.path.join(git.top, out.rstrip("\n"))):
        return False, "index-locked"
    found = _live_git_processes(git.top)
    if found is None:
        return None, "unknown"
    if found:
        return False, "git-process-running"
    return True, "none-seen"


def _pin_exists(git: GitRunner, ref: str) -> bool:
    rc, _ = _read(git, ["rev-parse", "--verify", "--quiet", ref], ok=(0, 1))
    return rc == 0


def _review_after(ctx: _Ctx, boundary: Boundary, refusal: Terminal) -> bool:
    """A member ``complete`` or ``Ruling`` line stands after the anchors and after the run
    that was current when the refusal was recorded (FR-065)."""
    before = [r.ledger_lines for r in ctx.side.runs if r.line_no < refusal.line_no]
    floor = max([a for a in boundary.anchors if a is not None] + before[-1:] + [0])
    members = set(boundary.members)
    for no, line in enumerate(ctx.ledger_text.split("\n"), 1):
        if no <= floor:
            continue
        ruling, verdict = _RULING.match(line), _VERDICT.match(line)
        if ruling and ruling.group(1) in members:
            return True
        if verdict and verdict.group(2) == "complete" and verdict.group(1) in members:
            return True
    return False


def _credited_rewrite(ctx: _Ctx, boundary: Boundary) -> Tuple[Optional[str], bool]:
    """``(tree, credited)`` of the last ``hook-rewrite`` refusal's ``rewritten=`` pin: the tree
    is None unless the refusal named a pin that resolves, ``credited`` says a renewed review or
    Ruling stands after it (FR-065)."""
    prev = ctx.side.terminal.get(boundary.key)
    if (
        prev is None
        or prev.kind != "refused"
        or prev.reason != "hook-rewrite"
        or not prev.rewritten
    ):
        return None, False
    tree = _tree_of(ctx.git, prev.rewritten)
    return tree, tree is not None and _review_after(ctx, boundary, prev)


def _retry_decision(
    ctx: _Ctx,
    boundary: Boundary,
    last: Optional[Attempt],
    after: bool,
) -> RetryVerdict:
    """May a new attempt be made now? ``after``: a result line follows the last prepared line
    (the attempt finished and was refused); without one the attempt is open (FR-116)."""
    git, layout = ctx.git, ctx.layout
    if not after:
        value, basis = quiescence(git)
        if value is not True:
            if basis == "index-locked":
                return RetryVerdict(
                    False,
                    "index-locked",
                    "an index.lock exists: an earlier git call may still be running",
                )
            return RetryVerdict(
                False,
                "commit-interrupted",
                "the earlier commit call may still be running "
                f"({basis}): check that no git or hook process is still running in "
                "this worktree before any retry (FR-116)",
            )
    attempt = last.attempt + 1 if last else 1
    inputs = _stage_inputs(git, layout, boundary, attempt)
    plan = plan_stage(git, inputs.pop("paths"), **inputs) if inputs else None
    if plan is None or plan["status"] != "ok":
        # nothing to compare, or a path rule refuses: stage-plan reports it with its own token
        return RetryVerdict(True, "retry-allowed", "stage-plan reports what is left")
    extras = set(inputs["extra_paths"])
    product = [p for p in plan["commit_paths"] if p not in extras]
    accepted = {}
    for tid, gen in zip(boundary.members, boundary.gens):
        ref = f"{PIN_ROOT}/{layout.slug}/accepted/T{tid}-s{gen.start_ordinal}"
        tree = _tree_of(git, ref)
        if tree is None:
            return RetryVerdict(
                False, "no-accepted-tree", f"T{tid}: the accepted pin {ref} is missing"
            )
        accepted[tid] = _head_entries(git, tree)
    mine = _member_files(boundary, product)
    now = _head_entries(git, _tree_with(git, ctx.head, product)) if product else {}
    differing = sorted(
        {
            p
            for tid in boundary.members
            for p in mine[tid]
            if now.get(p) != accepted[tid].get(p)
        }
    )
    if not differing:
        return RetryVerdict(True, "retry-allowed")
    tree, credited = _credited_rewrite(ctx, boundary)
    if tree is not None:
        rewritten = _head_entries(git, tree)
        if all(now.get(p) == rewritten.get(p) for p in differing):
            if credited:
                return RetryVerdict(
                    True, "retry-allowed", "the rewritten tree was reviewed again"
                )
            return RetryVerdict(
                False,
                "candidate-changed",
                f"{', '.join(differing)}: equal to the tree the hook rewrote, which needs "
                "a renewed review or Ruling given after the refusal displayed it (FR-065)",
                tuple(differing),
            )
    return RetryVerdict(
        False,
        "candidate-changed",
        f"{', '.join(differing)}: no longer equal to the accepted tree of the review",
        tuple(differing),
    )


def _s_is_empty(ctx: _Ctx, boundary: Boundary) -> bool:
    """The commit set of a due boundary is empty (the plan says ``nothing``)."""
    inputs = _stage_inputs(ctx.git, ctx.layout, boundary, 1)
    if inputs is None:
        return False
    return plan_stage(ctx.git, inputs.pop("paths"), **inputs)["status"] == "nothing"


def _boundary_facts(
    ctx: _Ctx, boundary: Boundary, with_s: bool
) -> Tuple[GitFacts, Optional[RetryVerdict]]:
    """The git facts ``derive_state`` needs for one boundary, read only where its state asks.

    ``with_s`` also reads whether S is empty (a due boundary of a flagged run); ``plan_ledger``
    leaves that to its own plan. The verdict is None unless a retry is possible: the run has
    the flag, a prepared or refused attempt exists, and HEAD is still its parent.
    """
    git, layout, side, head = ctx.git, ctx.layout, ctx.side, ctx.head
    key = boundary.key
    text = _read_file(
        os.path.join(layout.retries, f"T{boundary.members[0]}", "q0-head")
    )
    q0 = text.strip() if text else None
    base = GitFacts(head=head, q0_head=q0)
    if derive_state(boundary, side, base, ctx.flag)[0] == "settled":
        return base, None
    attempts = side.attempts.get(key, [])
    last = attempts[-1] if attempts else None
    prev = side.terminal.get(key)
    if last is None and prev is None:
        empty = with_s and ctx.flag and boundary.crash_explained and not boundary.mixed
        return GitFacts(
            head=head, q0_head=q0, s_empty=empty and _s_is_empty(ctx, boundary)
        ), None
    after = prev is not None and (last is None or prev.line_no > last.line_no)
    parent = last.parent if last else q0
    pins = False
    proves: Optional[str] = None
    if last is not None:
        stem = f"{PIN_ROOT}/{layout.slug}"
        cand = f"{stem}/boundary/{key}-a{last.attempt}"
        work = f"{stem}/boundary-wt/{key}-a{last.attempt}"
        pins = _pin_exists(git, cand) and _pin_exists(git, work)
        if pins and not after and head is not None and head != parent:
            proof = verify_commit(
                git, key, last.attempt, last.parent, cand, work, None,
                ctx.ledger_path, layout.sidecar, outside=False,
            )  # fmt: skip
            if proof["status"] == "committed":
                proves = proof["sha"]
    verdict = None
    if (
        ctx.flag
        and head is not None
        and head == parent
        and not (after and prev.kind == "uncertain")
    ):
        verdict = _retry_decision(ctx, boundary, last, after)
    facts = GitFacts(
        head=head,
        q0_head=q0,
        pins_complete=pins,
        proves_commit=proves,
        retry_allowed=verdict is not None and verdict.allowed,
    )
    return facts, verdict


def _plan_pin_problem(text: str, layout: RunLayout) -> Optional[str]:
    """Why a managed run's plan or source no longer matches its ``PLAN:`` pin, else None.

    The pin is immutable from the first ``start`` line on (``refs/managed-workspace.md``):
    a later ``PLAN:`` line, a missing pin or a differing hash is ``plan-changed``. Before the
    first start a differing hash is re-pinned at Wave 0 step 6, so it is not a refusal here.
    """
    if not layout.managed:
        return None
    pins: List[Tuple[int, Tuple[str, ...]]] = []
    first_start: Optional[int] = None
    for no, line in enumerate(text.split("\n"), 1):
        found = _PLAN.match(line)
        if found:
            pins.append((no, found.groups()))
        elif first_start is None and _START.match(line):
            first_start = no
    if first_start is None:
        return None
    if not pins:
        return "the ledger has no PLAN pin"
    if pins[-1][0] > first_start:
        return "a PLAN pin follows the first start line"
    for name, pin in zip((f"{layout.slug}.md", "source.md"), pins[-1][1]):
        raw = _read_bytes(os.path.join(layout.base, name))
        if raw is None:
            return f"{name} is missing"
        if hashlib.sha256(raw).hexdigest() != pin:
            return f"{name} differs from the PLAN pin"
    return None


def _run_dicts(
    side: Sidecar, total: int
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """The run lines and the ledger segments they open (FR-102): run ``i`` covers the ledger
    lines ``k_i + 1`` to ``k_{i+1}`` (the last run, to the end); two equal offsets leave the
    earlier run an empty segment."""
    runs, segments = [], []
    for i, run in enumerate(side.runs):
        last = side.runs[i + 1].ledger_lines if i + 1 < len(side.runs) else total
        first = run.ledger_lines + 1
        runs.append(
            {
                "run": run.run, "flag": run.flag, "revoked": run.revoked,
                "ledger_lines": run.ledger_lines, "branch": run.branch, "at": run.at,
                "args": run.args, "source": run.source, "worktree": run.worktree,
            }
        )  # fmt: skip
        segments.append(
            {
                "run": run.run, "flag": run.flag, "revoked": run.revoked,
                "first_line": first, "last_line": last, "empty": last < first,
            }
        )  # fmt: skip
    return runs, segments


def _reason(
    boundary: Boundary,
    state: str,
    action: str,
    side: Sidecar,
    verdict: Optional[RetryVerdict],
) -> str:
    """The token that says why the boundary has this action (closed list, see ``reconcile``)."""
    done = side.terminal.get(boundary.key)
    if state == "settled":
        if boundary.key in side.resolved:
            return "resolved"
        if done is not None and done.kind in ("sha", "recovered", "skipped"):
            return "committed" if done.kind == "sha" else done.kind
        return "incomplete" if not boundary.complete else "not-authorized"
    if action == "stop-out-of-protocol":
        return "out-of-protocol"
    if state == "uncertain":
        return "uncertain"
    fixed = {
        "prepare": "crash-explained",
        "retry": "retry-allowed",
        "record-recovered": "commit-proved",
    }
    if action in fixed:
        return fixed[action]
    if action == "record-skipped":
        return "mixed-authorization" if boundary.mixed else "empty"
    if verdict is not None and not verdict.allowed:
        return verdict.reason
    return "unsettled"


def reconcile(
    git: GitRunner,
    ledger: str,
    sidecar: str,
    run_dir: str,
    package: Optional[str] = None,
    flag: bool = False,
) -> Dict[str, Any]:
    """What each boundary of the ledger is, and the one action this run may take (DD-5).

    ``flag``: this run carries ``--commit-tasks``. The result has ``boundaries`` (each with
    ``key``, ``label``, ``members``, ``state``, ``action``, ``reason``, ``detail``, ``parent``,
    ``head``, ``attempt`` (the last prepared one), ``next_attempt`` (for ``prepare`` and
    ``retry``), ``sha`` (the proved commit, for ``record-recovered``), ``rewritten`` (the pin
    a refusal named), ``paths`` (what blocks a retry) and, for a settled commit,
    ``outside_changed`` and ``wt``), ``runs`` and ``segments`` (the sidecar lines it used) and
    ``no_grant_lines`` (the ledger lines before the first run line, which carry no grant).
    States and actions are the closed lists of ``derive_state``. ``reason`` is one of:
    ``resolved``, ``committed``, ``recovered``, ``skipped``, ``incomplete`` (a member has no
    ``complete`` line), ``not-authorized`` (completed outside an ``on`` segment: never
    committed), ``out-of-protocol``, ``uncertain``, ``crash-explained`` (prepare now),
    ``retry-allowed``, ``commit-proved``, ``mixed-authorization``, ``empty``, ``unsettled``,
    and for a denied retry ``candidate-changed``, ``no-accepted-tree``, ``index-locked`` or
    ``commit-interrupted``. ``status`` is ``ok`` or ``refused`` with ``sidecar-corrupt``,
    ``sidecar-mismatch``, ``ledger-corrupt``, ``ledger-identity`` or ``plan-changed``. With
    no ``commits.md`` and no flag nothing is listed. Nothing is written.
    """
    head = _head_sha(git)
    layout = run_layout(run_dir, package)
    out: Dict[str, Any] = {
        "status": "ok", "reason": None, "detail": None, "flag": "on" if flag else "off",
        "head": head, "managed": layout.managed, "ledger_lines": 0, "no_grant_lines": 0,
        "boundaries": [], "runs": [], "segments": [],
    }  # fmt: skip

    def refuse(reason: str, detail: str) -> Dict[str, Any]:
        out.update(status="refused", reason=reason, detail=detail)
        return out

    ledger_text = _read_file(ledger)
    if ledger_text is None:
        raise LookupFailed(f"ledger not found: {ledger}")
    if os.path.realpath(sidecar) != os.path.realpath(layout.sidecar):
        raise LookupFailed(
            f"{sidecar} is not the commits.md of this run ({layout.sidecar})"
        )
    side_text = _read_file(sidecar)
    try:
        view = parse_ledger(ledger_text)
        side = parse_sidecar(side_text or "")
        validate_runs(side.runs, ledger_text)
        repo_id, ledger_id, source_id = boundary_identity(side, layout)
    except (LedgerCorrupt, SidecarCorrupt, SidecarMismatch) as err:
        return refuse(err.reason, str(err))
    except ValueError as err:
        return refuse("ledger-identity", str(err))
    problem = _plan_pin_problem(ledger_text, layout)
    if problem is not None:
        return refuse("plan-changed", problem)
    total = ledger_k(ledger_text)
    out["ledger_lines"] = total
    out["runs"], out["segments"] = _run_dicts(side, total)
    out["no_grant_lines"] = (
        min(side.runs[0].ledger_lines, total) if side.runs else total
    )
    if side_text is None and not flag:
        return out
    ctx = _Ctx(git, layout, side, ledger, ledger_text, head, flag)
    boundaries = build_boundaries(view, side.runs, repo_id, ledger_id, source_id)
    keys = [b.key for b in boundaries]
    for item in boundaries:
        facts, verdict = _boundary_facts(ctx, item, with_s=True)
        state, action = derive_state(item, side, facts, flag)
        attempts = side.attempts.get(item.key, [])
        last = attempts[-1] if attempts else None
        done = side.terminal.get(item.key)
        denied = verdict is not None and not verdict.allowed
        next_attempt = None
        if action in ("prepare", "retry"):
            next_attempt = last.attempt + 1 if last else 1
        out["boundaries"].append(
            {
                "key": item.key,
                "label": display_label(item.key, keys),
                "members": item.members,
                "state": state,
                "action": action,
                "reason": _reason(item, state, action, side, verdict),
                "detail": verdict.detail if denied else None,
                "parent": last.parent if last else facts.q0_head,
                "head": head,
                "attempt": last.attempt if last else None,
                "next_attempt": next_attempt,
                "sha": facts.proves_commit if action == "record-recovered" else None,
                "rewritten": done.rewritten
                if done and done.kind == "refused"
                else None,
                "paths": sorted(verdict.paths) if denied else [],
                "outside_changed": done.outside_changed if done else None,
                "wt": done.wt if done else None,
            }
        )
    return out


# --- resolve-check (FR-116, FR-120 to FR-126, DD-5; design 4.3 and 6.2) -----------------------
# The owner answers ``abandon`` or ``adopt`` for a boundary that cannot be settled by the
# commit step. This reads what the history shows so the executor can disclose it and offer
# only the answers that hold; the executor appends the one ``resolved`` line. Nothing is
# written here.
ADOPT_NOT_DESCENDANT = "adopt-not-descendant"
ADOPT_UNVERIFIABLE = "adopt-unverifiable"
# A key with no unsettled boundary behind it, in the reasons ``_reason`` gives a settled one.
_NOTHING_TO_SETTLE = ("incomplete", "not-authorized")


def _infer_layout(ledger: str, sidecar: str) -> RunLayout:
    """The layout when the caller gives neither ``--run-dir`` nor ``--package``.

    A managed run keeps ``<package>/progress.md`` and ``<package>/artifacts/commits.md``;
    a legacy run keeps both files in the run folder.
    """
    ledger_dir = os.path.dirname(os.path.realpath(ledger))
    side_dir = os.path.dirname(os.path.realpath(sidecar))
    if (
        os.path.basename(side_dir) == "artifacts"
        and os.path.dirname(side_dir) == ledger_dir
    ):
        return run_layout(ledger_dir, ledger_dir)
    return run_layout(ledger_dir)


def _differs(
    ctx: _Ctx, boundary: Boundary, last: Optional[Attempt], head: str
) -> Tuple[str, Optional[int], str]:
    """``(basis, differs, why)``: how many paths of S have another object id, mode or
    presence in HEAD than in the disclosed comparison tree (FR-123).

    The tree is the frozen candidate of the latest prepared attempt (``candidate``), else the
    accepted tree of each member (``accepted``; S is then the members' product paths, the
    package evidence of a managed run is not compared). A tree that is not there, or a
    comparison that fails, gives ``differs`` None with ``why``: unavailable, never zero.
    """
    git, layout, key = ctx.git, ctx.layout, boundary.key
    try:
        if last is not None:
            ref = f"{PIN_ROOT}/{layout.slug}/boundary/{key}-a{last.attempt}"
            tree = _tree_of(git, ref)
            if tree is None:
                return "candidate", None, f"the candidate pin {ref} is missing"
            folder = os.path.dirname(layout.sidecar)
            s_paths, _ = _commit_set(
                git, folder, key, last.attempt, last, last.parent, tree
            )
            inside = set(s_paths or [])
            changed = _changed_between(git, tree, head)
            return "candidate", len([p for p in changed if p in inside]), ""
        differing: set = set()
        for tid, gen in zip(boundary.members, boundary.gens):
            ref = f"{PIN_ROOT}/{layout.slug}/accepted/T{tid}-s{gen.start_ordinal}"
            tree = _tree_of(git, ref)
            if tree is None:
                return "accepted", None, f"the accepted pin {ref} is missing"
            mine = {n for f in gen.files if (n := _normalize(f))}
            differing |= mine & set(_changed_between(git, tree, head))
        return "accepted", len(differing), ""
    except LookupFailed as err:
        basis = "candidate" if last is not None else "accepted"
        return basis, None, f"the comparison could not be made: {err}"


def _adopt_refusal(
    git: GitRunner,
    parent: Optional[str],
    head: Optional[str],
    quiet: Optional[bool],
    quiet_basis: str,
    differs: Optional[int],
    why: str,
) -> Optional[Tuple[str, str]]:
    """``(reason, detail)`` of the first FR-123 condition for ``adopt`` that fails, else None.

    The exit code of ``merge-base --is-ancestor`` is read as 0 (a descendant), 1 (not one) or
    anything else (128 and a timeout: unknown, never success).
    """
    if parent is None:
        return ADOPT_UNVERIFIABLE, "the parent is unknown: no q0-head was recorded"
    if head is None:
        return ADOPT_UNVERIFIABLE, "HEAD is unborn"
    if head == parent:
        return ADOPT_NOT_DESCENDANT, "HEAD is the parent: nothing was committed on it"
    rc, _ = git.run(["merge-base", "--is-ancestor", parent, head])
    if rc == 1:
        return ADOPT_NOT_DESCENDANT, f"HEAD does not descend from the parent {parent}"
    if rc != 0:
        return (
            ADOPT_UNVERIFIABLE,
            f"ancestry could not be established (git exited {rc})",
        )
    if quiet is not True:
        return ADOPT_UNVERIFIABLE, (
            f"quiescence is not proved ({quiet_basis}): check that no git or hook "
            "process is still running in this worktree (FR-116)"
        )
    if differs is None:
        return ADOPT_UNVERIFIABLE, why
    return None


def resolve_check(
    git: GitRunner,
    key: str,
    ledger: str,
    sidecar: str,
    run_dir: Optional[str] = None,
    package: Optional[str] = None,
) -> Dict[str, Any]:
    """What the owner may answer for the boundary ``key`` selects (FR-120 to FR-126).

    ``key`` is the full key or a unique prefix of at least ``DISPLAY_LEN`` characters. The
    result always carries ``key``, ``label``, ``members``, ``state`` and ``action`` (the
    unflagged ``derive_state`` answer), ``choices`` (``abandon``, then ``adopt`` when it
    holds), ``basis`` (``candidate`` once an attempt was prepared, else ``accepted``),
    ``differs`` (None: the comparison tree is unavailable), ``head``, ``parent`` (the
    prepared parent, else the first member's ``q0-head``), ``attempt``, ``quiescent`` (True,
    False, or None for unknown) and ``quiescence`` (its basis).

    ``status`` ``ok``: the key names one unsettled boundary and ``abandon`` is offered; when
    ``adopt`` is not, ``reason`` is ``adopt-not-descendant`` (HEAD is the parent or not a
    descendant of it) or ``adopt-unverifiable`` (no parent, the ancestry or the comparison
    tree cannot be read, or quiescence is not proved) and ``detail`` says why. ``abandon``
    needs none of that, so it is never withdrawn. ``status`` ``refused`` offers nothing:
    ``unknown-boundary`` (no key starts with it, or the boundary has nothing to settle),
    ``ambiguous-key``, ``prefix-too-short`` (not in the design's list: a prefix below
    ``DISPLAY_LEN`` is refused even when unique, Task 11), ``already-settled``, and the
    refusals ``reconcile`` gives for a corrupt ledger or sidecar, a changed managed plan
    or an identity that is not a token (no resolution overrides them, FR-125).

    ``quiescent`` is reported for both answers: FR-116 and FR-125 say the executor records
    neither while it is not True; only ``adopt`` is gated here. Nothing is written.
    """
    head = _head_sha(git)
    layout = (
        _infer_layout(ledger, sidecar)
        if run_dir is None and package is None
        else run_layout(run_dir or package, package)
    )
    out: Dict[str, Any] = {
        "status": "ok", "reason": None, "detail": None, "key": None, "label": None,
        "members": [], "state": None, "action": None, "choices": [], "basis": None,
        "differs": None, "head": head, "parent": None, "attempt": None,
        "quiescent": None, "quiescence": None,
    }  # fmt: skip

    def refuse(reason: str, detail: str) -> Dict[str, Any]:
        out.update(status="refused", reason=reason, detail=detail, choices=[])
        return out

    ledger_text = _read_file(ledger)
    if ledger_text is None:
        raise LookupFailed(f"ledger not found: {ledger}")
    if os.path.realpath(sidecar) != os.path.realpath(layout.sidecar):
        raise LookupFailed(
            f"{sidecar} is not the commits.md of this run ({layout.sidecar})"
        )
    try:
        view = parse_ledger(ledger_text)
        side = parse_sidecar(_read_file(sidecar) or "")
        validate_runs(side.runs, ledger_text)
        repo_id, ledger_id, source_id = boundary_identity(side, layout)
    except (LedgerCorrupt, SidecarCorrupt, SidecarMismatch) as err:
        return refuse(err.reason, str(err))
    except ValueError as err:
        return refuse("ledger-identity", str(err))
    problem = _plan_pin_problem(ledger_text, layout)
    if problem is not None:
        return refuse("plan-changed", problem)
    boundaries = build_boundaries(view, side.runs, repo_id, ledger_id, source_id)
    keys = [b.key for b in boundaries]
    try:
        full = resolve_prefix(key, keys)
    except KeyPrefixError as err:
        return refuse(err.reason, str(err))
    boundary = next(b for b in boundaries if b.key == full)
    ctx = _Ctx(git, layout, side, ledger, ledger_text, head, False)
    facts, _ = _boundary_facts(ctx, boundary, with_s=False)
    state, action = derive_state(boundary, side, facts, False)
    out.update(
        key=full, label=display_label(full, keys), members=boundary.members,
        state=state, action=action,
    )  # fmt: skip
    if state == "settled":
        why = _reason(boundary, state, action, side, None)
        if why in _NOTHING_TO_SETTLE:
            return refuse(
                "unknown-boundary",
                f"{full} has nothing to settle ({why}): it was never authorized "
                "for a commit or is not complete",
            )
        return refuse("already-settled", f"the boundary is settled ({why})")
    attempts = side.attempts.get(full, [])
    last = attempts[-1] if attempts else None
    parent = last.parent if last else facts.q0_head
    quiet, quiet_basis = quiescence(git)
    basis, differs, why = (
        _differs(ctx, boundary, last, head)
        if head is not None
        else ("candidate" if last else "accepted", None, "HEAD is unborn")
    )
    refusal = _adopt_refusal(git, parent, head, quiet, quiet_basis, differs, why)
    out.update(
        basis=basis, differs=differs, parent=parent,
        attempt=last.attempt if last else None, quiescent=quiet,
        quiescence=quiet_basis,
        choices=["abandon"] if refusal else ["abandon", "adopt"],
        reason=refusal[0] if refusal else None,
        detail=refusal[1] if refusal else None,
    )  # fmt: skip
    return out
