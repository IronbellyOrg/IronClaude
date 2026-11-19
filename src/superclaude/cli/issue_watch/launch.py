"""Find Orca, check a checkout's origin, build the typed wake line and start a session.

The only text this module can type into a terminal after the session has started
is the string that ``build_wake_line`` builds from a string that matches the wake
id pattern; every other input is refused. The text of the session start is built
by ``session_command`` from a checked tag and a checked tier. Every command runs
through the injected ``Runner`` with a real timeout. This module writes no state
and caches nothing: ``OrcaLauncher.start`` returns a ``LaunchOutcome`` and the
cycle records it. It imports only the standard library, ``runner`` and
``_ORCA_CLIS`` (design 5.3).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol

from superclaude.cli.install_user_setup import _ORCA_CLIS

from .runner import CommandResult, Runner

WAKE_ID_PATTERN = re.compile(r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}")
"""A wake id (spec 3.1); ``predicates.WAKE_ID_PATTERN`` is a pinned copy."""

WAKE_LINE_PATTERN = re.compile(
    r"^/sc:orchestrator --wake [0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$"
)
"""Every line ``build_wake_line`` can return, and nothing else (spec 3.2)."""

WAKE_LINE_MAX_BYTES = 64

TAG_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,31}")
"""A ccsession tag. [UNVERIFIED, U25] that this is the pattern ccsession applies."""

TIER_PATTERN = re.compile(r"tier[0-9][a-z]?")

HANDLE_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
"""Terminal handles that may be stored; ``predicates.OPERATION_ID_PATTERN`` is a pinned copy."""

ORIGIN_MISMATCH = "origin_mismatch"
"""Reason ``check_origin`` returns for every failed check."""

NAME_QUESTION = "Session name"
"""What a fresh Orca terminal shows when ccsession asks for a name (``waker.py:120``)."""

START_WAIT_S = 120.0
SHELL_WAIT_S = 30.0
_PROMPT_LINE = re.compile(r"[$#>❯]\s*$")

LaunchKind = Literal["ready", "unknown", "spawn_error"]

LAUNCH_DETAILS: frozenset[str] = frozenset(
    {
        "ok",
        "spawn_error",
        "timeout",
        "exit_nonzero",
        "non_json",
        "no_handle",
        "handle_invalid",
        "not_started",
        "name_question",
    }
)
"""The fixed set of ``LaunchOutcome.detail`` values."""

# [UNVERIFIED] key paths of the terminal handle in Orca's ``terminal create`` reply
# (design 4.5 step 11, U9). Pinned by ``_assumed_shape`` fixtures until a real
# reply is recorded.
HANDLE_PATHS: tuple[tuple[str, ...], ...] = (
    ("result", "terminal", "handle"),
    ("terminal", "handle"),
    ("result", "handle"),
    ("handle",),
)


def _check_timeout(timeout: object) -> float:
    """Return ``timeout`` when it is a positive number, else raise ``ValueError``."""
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or not timeout > 0
    ):
        raise ValueError("timeout must be a positive number of seconds")
    return float(timeout)


def build_wake_line(wake_id: object) -> str:
    """Return ``/sc:orchestrator --wake <wake_id>`` for a string that matches the pattern.

    The one builder of the typed line (spec 3.2). Anything that is not a ``str``
    holding exactly a wake id (a bool, an int, a longer text, a text with a
    newline) raises ``ValueError``, so no text from GitHub can reach a typed line.
    """
    if not isinstance(wake_id, str) or WAKE_ID_PATTERN.fullmatch(wake_id) is None:
        raise ValueError("wake_id must match the wake id pattern")
    line = f"/sc:orchestrator --wake {wake_id}"
    if len(line.encode("ascii")) > WAKE_LINE_MAX_BYTES:
        raise ValueError("the wake line is too long")
    return line


def session_command(tag: object, tier: object) -> str:
    """Return ``ccsession <tag> --tier <tier>``, the command that starts an orchestrator.

    ``tag`` must match ``TAG_PATTERN`` and ``tier`` ``TIER_PATTERN``; anything
    else raises ``ValueError`` (a tag or tier is never text from GitHub).
    """
    if not isinstance(tag, str) or TAG_PATTERN.fullmatch(tag) is None:
        raise ValueError("tag must match the ccsession tag pattern")
    if not isinstance(tier, str) or TIER_PATTERN.fullmatch(tier) is None:
        raise ValueError("tier must match the tier pattern")
    return f"ccsession {tag} --tier {tier}"


def _json_object(text: str) -> dict | None:
    """Return ``text`` parsed as a JSON object, or None for anything else."""
    try:
        value = json.loads(text)
    except (ValueError, RecursionError):
        return None
    return value if isinstance(value, dict) else None


def _lists_orca_cli(result: CommandResult) -> bool:
    """Return True when a probe reply proves the binary is the Orca CLI.

    Accepted only for exit 0, a JSON object, ``topics`` a list of ``dict``
    elements and one element named ``orca-cli``. Every other shape is False,
    never an exception (DF-36, C19: with exit 0 the original ``_find_orca`` raises
    on a ``topics`` that is null, an int, a bool, a non-empty str or dict, or a
    list with a non-dict element before any ``orca-cli`` dict; an empty str, an
    empty dict and a list with the ``orca-cli`` dict first do not raise).
    """
    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
        return False
    reply = _json_object(result.stdout)
    topics = None if reply is None else reply.get("topics")
    if not isinstance(topics, list) or not all(isinstance(t, dict) for t in topics):
        return False
    return any(t.get("name") == "orca-cli" for t in topics)


def find_orca(
    runner: Runner,
    *,
    which: Callable[[str], str | None] = shutil.which,
    timeout: float | Callable[[], float | None] | None = 10.0,
) -> str | None:
    """Return the first ``_ORCA_CLIS`` binary that answers as Orca, else None.

    Mirrors ``install_user_setup._find_orca`` through the injected ``runner``
    and ``which`` (DF-54). ``timeout`` None (fewer than 5 s left in the cycle)
    starts no process and returns None. ``timeout`` may also be a zero-argument
    callable, called immediately before each probe: its number is that probe's
    timeout (checked like a plain one) and its None ends the search without
    starting that probe, so a cycle deadline is re-read per probe (design 8.5).
    The result is not cached here. A
    candidate whose path is not absolute (``which`` can return ``./orca-ide``
    for a relative ``PATH`` entry) is skipped without a probe, because the
    launch runs with ``cwd`` set to the worktree and would execute a file of
    that name in it. The path probed is the path returned and later launched.
    """
    if timeout is None:
        return None
    if callable(timeout):
        allowance = timeout
    else:
        seconds = _check_timeout(timeout)

        def allowance() -> float:
            return seconds

    for name in _ORCA_CLIS:
        path = which(name)
        if not path or not os.path.isabs(path):
            continue
        left = allowance()
        if left is None:
            return None
        argv = [path, "skills", "list", "--json"]
        if _lists_orca_cli(runner.run(argv, _check_timeout(left))):
            return path
    return None


# Copied rules of ``parse_origin_url`` (sc-issue-protocol/scripts/origin_repo.py
# lines 65-69 and 86-99): case-sensitive host, anchored, optional trailing "/".
_NAME = r"[A-Za-z0-9._-]+"
_ORIGIN_PATTERNS = (
    re.compile(rf"^https://github\.com/(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
    re.compile(rf"^git@github\.com:(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
)


def parse_origin(url: object) -> str | None:
    """Return ``owner/repo`` for a GitHub origin URL, else None."""
    if not isinstance(url, str):
        return None
    url = url.strip()
    for pattern in _ORIGIN_PATTERNS:
        match = pattern.match(url)
        if match:
            owner = match.group("owner")
            repo = match.group("repo")
            if repo.endswith(".git"):
                repo = repo[: -len(".git")]
            if not repo or owner in (".", "..") or repo in (".", ".."):
                return None
            return "/".join((owner, repo))
    return None


def check_origin(
    runner: Runner,
    checkout: Path | str,
    expected_repo: str,
    timeout: float | None,
) -> str | None:
    """Return None when ``checkout``'s origin names ``expected_repo`` (``owner/name``).

    Compared case-insensitively. Otherwise return ``"origin_mismatch"``: a
    ``timeout`` of None (no process is started), a timed-out or failed ``git``,
    or an unparseable or foreign URL. The ``-C`` names the directory, so no
    ``cwd`` is passed (DF-01).
    """
    if timeout is None:
        return ORIGIN_MISMATCH
    argv = ["git", "-C", str(checkout), "remote", "get-url", "origin"]
    result = runner.run(argv, _check_timeout(timeout))
    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
        return ORIGIN_MISMATCH
    repo = parse_origin(result.stdout)
    if repo is None or repo.lower() != expected_repo.lower():
        return ORIGIN_MISMATCH
    return None


@dataclass(frozen=True)
class LaunchOutcome:
    """What one session start gave (design 4.10: ready, unknown and spawn-error).

    ``handle`` is None or a terminal handle matching ``HANDLE_PATTERN``;
    ``detail`` is one of ``LAUNCH_DETAILS``.
    """

    kind: LaunchKind
    handle: str | None
    detail: str

    def __post_init__(self) -> None:
        if self.kind not in ("ready", "unknown", "spawn_error"):
            raise ValueError("invalid launch kind")
        if self.detail not in LAUNCH_DETAILS:
            raise ValueError("invalid launch detail")
        if self.handle is not None and not _valid_handle(self.handle):
            raise ValueError("handle fails the handle pattern")
        if self.kind == "ready" and self.handle is None:
            raise ValueError("a ready outcome needs a handle")


class Launcher(Protocol):
    """Starts one orchestrator session and reports the outcome; writes no state."""

    def start(
        self, orca: str, workspace: Path, tag: str, tier: str, timeout: float
    ) -> LaunchOutcome:
        """Start ``ccsession <tag> --tier <tier>`` in a new terminal of ``workspace``."""
        ...


def _valid_handle(value: object) -> bool:
    """Return True for a ``str`` matching ``HANDLE_PATTERN``."""
    return isinstance(value, str) and bool(HANDLE_PATTERN.fullmatch(value))


def _first_handle(reply: dict) -> tuple[bool, object]:
    """Return ``(True, value)`` for the first ``HANDLE_PATHS`` path present."""
    for path in HANDLE_PATHS:
        node: object = reply
        for key in path:
            node = node.get(key) if isinstance(node, dict) else None
        if node is not None:
            return True, node
    return False, None


def outcome_of(result: CommandResult) -> LaunchOutcome:
    """Map one ``terminal create`` ``CommandResult`` to a ``LaunchOutcome``.

    A spawn error is ``spawn_error``. Anything short of exit 0 with a JSON object
    that carries a valid handle is ``unknown`` (a terminal may exist). Exit 0 and
    a valid handle is ``ready`` here only in the sense that the terminal exists:
    ``OrcaLauncher.start`` goes on to type the command and wait for Claude.
    """
    if result.spawn_error is not None:
        return LaunchOutcome("spawn_error", None, "spawn_error")
    if result.timed_out:
        return LaunchOutcome("unknown", None, "timeout")
    if result.returncode != 0:
        return LaunchOutcome("unknown", None, "exit_nonzero")
    reply = _json_object(result.stdout)
    if reply is None:
        return LaunchOutcome("unknown", None, "non_json")
    hit, value = _first_handle(reply)
    if not hit:
        return LaunchOutcome("unknown", None, "no_handle")
    if not isinstance(value, str) or not _valid_handle(value):
        return LaunchOutcome("unknown", None, "handle_invalid")
    return LaunchOutcome("ready", value, "ok")


class OrcaLauncher:
    """The real ``Launcher``: ``terminal create``, type the command, wait for Claude.

    ``processes`` returns ``{terminal handle: ccsession tag}`` of every running
    Claude process (``wake.claude_processes``); it is injected because this
    module reads no ``/proc``. ``sleep`` and ``monotonic`` are injected so a test
    never waits. A fresh terminal that shows the ccsession name question is
    answered with the tag alone (it cannot carry a tier): the session then runs
    on the workspace default tier. [UNVERIFIED, U9] how a fresh Orca terminal of
    the orchestrator workspace behaves; the live test settles it.
    """

    def __init__(
        self,
        runner: Runner,
        processes: Callable[[], dict[str, str]] | None = None,
        *,
        sleep: Callable[[float], None] = time.sleep,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._runner = runner
        self._processes = processes or (lambda: {})
        self._sleep = sleep
        self._monotonic = monotonic

    def _run(self, argv: list[str], limit: float, deadline: float) -> CommandResult:
        left = max(1.0, deadline - self._monotonic())
        return self._runner.run(argv, min(limit, left))

    def _last_line(self, orca: str, handle: str, deadline: float) -> str:
        reply = _json_object(
            self._run(
                [orca, "terminal", "read", "--terminal", handle, "--screen", "--json"],
                20.0,
                deadline,
            ).stdout
        )
        node: object = reply
        for key in ("result", "terminal"):
            node = node.get(key, node) if isinstance(node, dict) else node
        tail = node.get("tail") if isinstance(node, dict) else None
        lines = (
            [t for t in tail if isinstance(t, str)] if isinstance(tail, list) else []
        )
        return next((t for t in reversed(lines) if t.strip()), "")

    def start(
        self, orca: str, workspace: Path, tag: str, tier: str, timeout: float
    ) -> LaunchOutcome:
        """Start the session; raises ``ValueError`` for a tag or tier ``session_command`` refuses."""
        command = session_command(tag, tier)
        seconds = _check_timeout(timeout)
        deadline = self._monotonic() + seconds
        created = outcome_of(
            self._run(
                [
                    orca,
                    "terminal",
                    "create",
                    "--worktree",
                    f"path:{workspace}",
                    "--json",
                ],
                30.0,
                deadline,
            )
        )
        if created.kind != "ready" or created.handle is None:
            return created
        handle = created.handle
        # A new workspace shell shows ccsession's name question once its start-up
        # finishes; wait for it, or for a plain shell prompt, instead of a delay.
        end = min(deadline, self._monotonic() + SHELL_WAIT_S)
        last = ""
        while self._monotonic() < end:
            last = self._last_line(orca, handle, deadline)
            if NAME_QUESTION in last or _PROMPT_LINE.search(last):
                break
            self._sleep(1.0)
        asks_name = NAME_QUESTION in last
        typed = self._run(
            [
                orca,
                "terminal",
                "send",
                "--terminal",
                handle,
                "--text",
                tag if asks_name else command,
                "--enter",
                "--wait-submit",
                "5",
                "--json",
            ],
            30.0,
            deadline,
        )
        if typed.spawn_error is not None:
            return LaunchOutcome("spawn_error", handle, "spawn_error")
        if typed.timed_out or typed.returncode != 0:
            return LaunchOutcome("unknown", handle, "exit_nonzero")
        while self._monotonic() < deadline:
            if self._processes().get(handle) == tag:
                return LaunchOutcome(
                    "ready", handle, "name_question" if asks_name else "ok"
                )
            self._sleep(3.0)
        return LaunchOutcome("unknown", handle, "not_started")
