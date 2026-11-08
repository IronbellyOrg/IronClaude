"""Find Orca, check the worktree origin and launch one claim session (design 8.4).

The only text this module can put after ``--prompt`` is the string that
``build_claim_prompt`` builds from a validated ``int``; ``launch_argv`` refuses
anything else. Every command runs through the injected ``Runner`` with a real
timeout. This module writes no state and caches nothing: ``OrcaLauncher.launch``
returns a ``LaunchOutcome`` and the cycle records it. It imports only the
standard library, ``runner`` and ``_ORCA_CLIS`` (design 5.3).
"""

from __future__ import annotations

import json
import os
import re
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol

from superclaude.cli.install_user_setup import _ORCA_CLIS

from .runner import CommandResult, Runner

# Orca agent id from the seed brief's launch line (decision DF-11). It names the
# agent Orca starts, not a model alias, and is deliberately not configurable.
ORCA_AGENT = "claude"

MAX_ISSUE_NUMBER = 999_999_999
"""Largest issue number ``build_claim_prompt`` accepts (FR-012)."""

PROMPT_PATTERN = re.compile(r"^/sc:issue --claim [1-9][0-9]{0,8}$")
"""Every prompt ``build_claim_prompt`` can return, and nothing else."""

OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
"""Operation ids that may be stored and printed in a retry command (design 9.2)."""

# [PROPOSAL, UNVERIFIED] key paths of the operation id in Orca's launch reply:
# the success reply first, then the error reply (design 8.4 line 636, FU-1).
# Pinned by the two ``_assumed_shape`` fixtures until a real reply is recorded.
OPERATION_ID_PATHS: tuple[tuple[str, ...], ...] = (
    ("receipt", "operation_id"),
    ("error", "operation_id"),
)

OP_UNKNOWN_TEXT = "agent_session_operation_unknown"
"""Orca's error code for a launch whose reply was lost (C16, UNVERIFIED)."""

ORIGIN_REPO = "ironbellyorg/ironclaude"
"""The only origin ``check_origin`` accepts, compared lower-cased (FR-025)."""

ORIGIN_MISMATCH = "origin_mismatch"
"""Reason ``check_origin`` returns for every failed check."""

LaunchKind = Literal["launched", "unknown", "spawn_error"]

LAUNCH_DETAILS: frozenset[str] = frozenset(
    {
        "ok",
        "spawn_error",
        "timeout",
        "exit_nonzero",
        "non_json",
        "no_operation_id",
        "operation_id_invalid",
        "op_unknown",
    }
)
"""The fixed set of ``LaunchOutcome.detail`` values."""


def _check_timeout(timeout: object) -> float:
    """Return ``timeout`` when it is a positive number, else raise ``ValueError``."""
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or not timeout > 0
    ):
        raise ValueError("timeout must be a positive number of seconds")
    return float(timeout)


def build_claim_prompt(n: object) -> str:
    """Return ``/sc:issue --claim <n>`` for an ``int`` in 1..999999999.

    A ``bool``, a ``str``, a ``float`` or an out-of-range ``int`` raises
    ``ValueError`` (FR-012, design 9.3).
    """
    if type(n) is not int or not 1 <= n <= MAX_ISSUE_NUMBER:
        raise ValueError("issue number must be an int in 1..999999999")
    return f"/sc:issue --claim {n}"


def launch_argv(orca: str, worktree: Path | str, prompt: str) -> list[str]:
    """Return the 12-element ``orca agent launch`` argv (FR-013, design 8.4).

    Raises ``ValueError`` when ``prompt`` is not a string ``build_claim_prompt``
    could have returned, so no other text can reach ``--prompt``.
    """
    if not isinstance(prompt, str) or not PROMPT_PATTERN.fullmatch(prompt):
        raise ValueError("prompt must come from build_claim_prompt")
    return [
        orca,
        "agent",
        "launch",
        "--agent",
        ORCA_AGENT,
        "--worktree",
        "path:" + str(worktree),
        "--surface",
        "terminal",
        "--prompt",
        prompt,
        "--json",
    ]


def retry_argv(
    orca: str, worktree: Path | str, prompt: str, operation_id: str
) -> list[str]:
    """Return ``launch_argv`` with ``--retry-launch <id>`` before ``--json`` (D 741).

    Raises ``ValueError`` when ``operation_id`` fails ``OPERATION_ID_PATTERN``,
    because ``status`` prints this argv as a shell command.
    """
    if not isinstance(operation_id, str) or not OPERATION_ID_PATTERN.fullmatch(
        operation_id
    ):
        raise ValueError("operation_id fails the operation-id pattern")
    argv = launch_argv(orca, worktree, prompt)
    return [*argv[:-1], "--retry-launch", operation_id, argv[-1]]


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
    runner: Runner, worktree: Path | str, timeout: float | None
) -> str | None:
    """Return None when the worktree's origin is IronbellyOrg/IronClaude.

    Otherwise return ``"origin_mismatch"``: a ``timeout`` of None (no process is
    started), a timed-out or failed ``git``, or an unparseable or foreign URL.
    The ``-C`` names the directory, so no ``cwd`` is passed (DF-01).
    """
    if timeout is None:
        return ORIGIN_MISMATCH
    argv = ["git", "-C", str(worktree), "remote", "get-url", "origin"]
    result = runner.run(argv, _check_timeout(timeout))
    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
        return ORIGIN_MISMATCH
    repo = parse_origin(result.stdout)
    if repo is None or repo.lower() != ORIGIN_REPO:
        return ORIGIN_MISMATCH
    return None


@dataclass(frozen=True)
class LaunchOutcome:
    """What one Orca launch gave (design 8.4 outcome table).

    ``operation_id`` is None or a string matching ``OPERATION_ID_PATTERN``;
    ``detail`` is one of ``LAUNCH_DETAILS``.
    """

    kind: LaunchKind
    operation_id: str | None
    detail: str

    def __post_init__(self) -> None:
        if self.kind not in ("launched", "unknown", "spawn_error"):
            raise ValueError("invalid launch kind")
        if self.detail not in LAUNCH_DETAILS:
            raise ValueError("invalid launch detail")
        if self.operation_id is not None and not _valid_id(self.operation_id):
            raise ValueError("operation_id fails the operation-id pattern")
        if self.kind == "launched" and self.operation_id is None:
            raise ValueError("a launched outcome needs an operation_id")


class Launcher(Protocol):
    """Starts one claim session and reports the outcome; writes no state."""

    def launch(
        self, orca: str, worktree: Path, prompt: str, timeout: float
    ) -> LaunchOutcome:
        """Launch ``prompt`` in ``worktree`` with ``orca`` within ``timeout``."""
        ...


def _valid_id(value: object) -> bool:
    """Return True for a ``str`` matching ``OPERATION_ID_PATTERN``."""
    return isinstance(value, str) and bool(OPERATION_ID_PATTERN.fullmatch(value))


def _first_hit(reply: dict) -> tuple[bool, object]:
    """Return ``(True, value)`` for the first ``OPERATION_ID_PATHS`` path present.

    A path is present when every key exists and the value is not None.
    """
    for path in OPERATION_ID_PATHS:
        node: object = reply
        for key in path:
            node = node.get(key) if isinstance(node, dict) else None
        if node is not None:
            return True, node
    return False, None


def _unknown_id(result: CommandResult) -> str | None:
    """Return a valid operation id from the stdout object, then the stderr object.

    Plain text that is not a JSON object never yields an id (OQ-47).
    """
    for text in (result.stdout, result.stderr):
        reply = _json_object(text)
        if reply is None:
            continue
        hit, value = _first_hit(reply)
        if hit and isinstance(value, str) and _valid_id(value):
            return value
    return None


def _unknown(result: CommandResult, detail: str) -> LaunchOutcome:
    """Return an ``unknown`` outcome keeping a valid id when one was parsed."""
    return LaunchOutcome("unknown", _unknown_id(result), detail)


def outcome_of(result: CommandResult) -> LaunchOutcome:
    """Map one launch ``CommandResult`` to a ``LaunchOutcome`` (design 629-634).

    Anything short of exit 0 with a JSON object carrying a valid operation id is
    ``unknown``; the ``agent_session_operation_unknown`` text anywhere in stdout
    or stderr is ``unknown`` even when an id is present (OQ-40).
    """
    if result.spawn_error is not None:
        return LaunchOutcome("spawn_error", None, "spawn_error")
    if result.timed_out:
        return _unknown(result, "timeout")
    if OP_UNKNOWN_TEXT in result.stdout or OP_UNKNOWN_TEXT in result.stderr:
        return _unknown(result, "op_unknown")
    if result.returncode != 0:
        return _unknown(result, "exit_nonzero")
    reply = _json_object(result.stdout)
    if reply is None:
        return _unknown(result, "non_json")
    hit, value = _first_hit(reply)
    if not hit:
        return _unknown(result, "no_operation_id")
    if not isinstance(value, str) or not _valid_id(value):
        return _unknown(result, "operation_id_invalid")
    return LaunchOutcome("launched", value, "ok")


class OrcaLauncher:
    """The real ``Launcher``: runs ``launch_argv`` through the runner in the worktree."""

    def __init__(self, runner: Runner) -> None:
        self._runner = runner

    def launch(
        self, orca: str, worktree: Path, prompt: str, timeout: float
    ) -> LaunchOutcome:
        """Run the launch argv with ``cwd=worktree`` and map the reply.

        The only call in the package that passes ``cwd`` (DF-01, design 625), so
        an operator retry from ``launch_cwd`` matches Orca's rule. Raises
        ``ValueError`` for a prompt ``build_claim_prompt`` could not have built
        or a timeout that is not a positive number.
        """
        argv = launch_argv(orca, worktree, prompt)
        seconds = _check_timeout(timeout)
        return outcome_of(self._runner.run(argv, seconds, cwd=str(worktree)))
