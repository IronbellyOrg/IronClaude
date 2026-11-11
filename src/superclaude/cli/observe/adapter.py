"""The one read-only edge to the Orca CLI (AD-3, AD-4, AD-5).

Only two argv shapes are ever run: the worker-list template (with optional run and cursor
pairs) and the one-time binary discovery probe that ``_find_orca`` makes. Every argv is
checked against a forbidden set before any call, and the set only ever grows.
"""

from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import threading
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from superclaude.cli.install_user_setup import _find_orca
from superclaude.cli.observe.sanitize import sanitize

Runner = Callable[
    [list, float], tuple
]  # (argv, timeout) -> (returncode, stdout[, stderr])
Discover = Callable[[], "str | None"]

WORKER_LIST_TEMPLATE = ("orchestration", "worker-list", "--json", "--limit", "100")
DISCOVERY_TEMPLATE = ("skills", "list", "--json")
# Matched by prefix against every verb and flag position, never against run or cursor values.
FORBIDDEN_PREFIXES = frozenset(
    {"check", "--ack", "--wait", "--retry-request", "dispatch", "inbox"}
)

RUN_ID_PATTERN = re.compile(
    r"^[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}$"
)  # PROPOSED, not an Orca format
CURSOR_MAX_BYTES = 2048  # PROPOSED

MAX_CALLS_PER_CYCLE = 5
MAX_OUTPUT_BYTES = 8 * 1024 * 1024
STDERR_KEEP_BYTES = 2048
PER_CALL_TIMEOUT = (
    10.0  # seconds; UNVERIFIED until the first permitted live read measures it
)
KILL_GRACE_SECONDS = 2.0

# Closed set of source codes besides ``exit:<n>``.
CODES = frozenset(
    {
        "timeout",
        "spawn-error",
        "output-cap",
        "json",
        "shape",
        "not-found",
        "overrun",
        "cursor-rejected",
        "cursor-stalled",
        "empty-page",
    }
)


class ArgvRejected(ValueError):
    """An argv or one of its values was refused before any call. ``code`` says why."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


class RunnerFailure(Exception):
    """A runner could not give a normal (returncode, stdout): ``code`` is a source code."""

    def __init__(self, code: str, stderr: str = ""):
        super().__init__(code)
        self.code = code
        self.stderr = stderr


# -- argv construction and checks ------------------------------------------------------------


def check_run_id(run_id: object) -> str:
    if not isinstance(run_id, str) or not RUN_ID_PATTERN.match(run_id):
        raise ArgvRejected("run-id", "malformed run id")
    return run_id


def check_cursor(cursor: object) -> str:
    """The cursor is opaque: only its byte bound and its first character are checked."""
    if not isinstance(cursor, str) or not cursor:
        raise ArgvRejected("cursor-rejected", "cursor is not a non-empty string")
    if cursor.startswith("-"):
        raise ArgvRejected("cursor-rejected", "cursor starts with '-'")
    if "\x00" in cursor:
        raise ArgvRejected("cursor-rejected", "cursor holds a NUL byte")
    if len(cursor.encode("utf-8", errors="replace")) > CURSOR_MAX_BYTES:
        raise ArgvRejected("cursor-rejected", "cursor is over the byte bound")
    return cursor


def _option_positions(tokens: list[str]) -> set[int]:
    """Indexes (into ``tokens``) that are verbs or flags rather than option values."""
    positions = set(range(len(tokens)))
    if tokens[:5] == list(WORKER_LIST_TEMPLATE):
        i = 5
        while i + 1 < len(tokens) and tokens[i] in ("--run", "--cursor"):
            positions.discard(i + 1)
            i += 2
    return positions


def assert_allowed(argv: list) -> None:
    """Refuse any argv that is not one of the two templates; names the forbidden token."""
    if not argv or not all(isinstance(a, str) for a in argv) or len(argv) < 2:
        raise ArgvRejected("argv", "not a list of strings")
    if argv[0].startswith("-") or not argv[0]:
        raise ArgvRejected("argv", "binary path is empty or starts with '-'")
    tokens = list(argv[1:])
    for index in sorted(_option_positions(tokens)):
        for prefix in FORBIDDEN_PREFIXES:
            if tokens[index].startswith(prefix):
                raise ArgvRejected(
                    "forbidden", f"{tokens[index]!r} is on the forbidden list"
                )
    if tokens == list(DISCOVERY_TEMPLATE):
        return
    if tokens[:5] != list(WORKER_LIST_TEMPLATE):
        raise ArgvRejected("argv", "not an allow-listed argv")
    rest = tokens[5:]
    seen: list[str] = []
    while rest:
        if len(rest) < 2 or rest[0] not in ("--run", "--cursor") or rest[0] in seen:
            raise ArgvRejected("argv", "unexpected option")
        flag, value = rest[0], rest[1]
        if flag == "--run":
            check_run_id(value)
        else:
            check_cursor(value)
        if value.startswith("-"):
            raise ArgvRejected("argv", "option value starts with '-'")
        seen.append(flag)
        rest = rest[2:]
    if seen not in ([], ["--run"], ["--cursor"], ["--run", "--cursor"]):
        raise ArgvRejected("argv", "options out of order")


def build_argv(
    orca: str, run_id: str | None = None, cursor: str | None = None
) -> list[str]:
    """The worker-list argv: literal template plus optional separate-item pairs."""
    argv = [orca, *WORKER_LIST_TEMPLATE]
    if run_id is not None:
        argv += ["--run", check_run_id(run_id)]
    if cursor is not None:
        argv += ["--cursor", check_cursor(cursor)]
    assert_allowed(argv)
    return argv


# -- the production runner --------------------------------------------------------------------


def _kill_group(proc: subprocess.Popen) -> None:
    try:
        if hasattr(os, "killpg"):
            os.killpg(proc.pid, signal.SIGKILL)
        else:
            proc.kill()
    except (ProcessLookupError, PermissionError):
        proc.kill()
    except OSError:
        pass
    try:
        proc.wait(timeout=KILL_GRACE_SECONDS)  # reap, so no zombie is left behind
    except subprocess.TimeoutExpired:
        pass


def production_runner(argv: list, timeout: float) -> tuple[int, str, str]:
    """Run ``argv`` with no shell, in its own session; return (returncode, stdout, stderr).

    Raises ``RunnerFailure`` with code ``timeout``, ``output-cap`` or ``spawn-error``. On the
    first two the whole process group is killed and reaped. stdout over 8 MiB ends the call;
    stderr is drained on its own thread and only its first 2 KiB is kept.
    """
    try:
        proc = subprocess.Popen(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError as exc:
        raise RunnerFailure("spawn-error", str(exc)) from exc

    out_chunks: list[bytes] = []
    err_chunks: list[bytes] = []
    state = {"out": 0, "err": 0, "overflow": False}
    stdout_done = threading.Event()

    def read_stdout() -> None:
        try:
            while True:
                chunk = proc.stdout.read1(65536)
                if not chunk:
                    return
                state["out"] += len(chunk)
                if state["out"] > MAX_OUTPUT_BYTES:
                    state["overflow"] = True
                    _kill_group(proc)
                    return
                out_chunks.append(chunk)
        except (OSError, ValueError):
            return
        finally:
            stdout_done.set()

    def read_stderr() -> None:
        try:
            while True:
                chunk = proc.stderr.read1(4096)
                if not chunk:
                    return
                room = STDERR_KEEP_BYTES - state["err"]
                if room > 0:
                    err_chunks.append(chunk[:room])
                    state["err"] += min(room, len(chunk))
        except (OSError, ValueError):
            return

    threads = [
        threading.Thread(target=read_stdout, daemon=True),
        threading.Thread(target=read_stderr, daemon=True),
    ]
    for thread in threads:
        thread.start()

    def stderr_text() -> str:
        return b"".join(err_chunks).decode("utf-8", errors="replace")

    if not stdout_done.wait(timeout):
        _kill_group(proc)
        raise RunnerFailure("timeout", stderr_text())
    if state["overflow"]:
        raise RunnerFailure("output-cap", stderr_text())
    try:
        returncode = proc.wait(timeout=KILL_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        _kill_group(proc)
        raise RunnerFailure("timeout", stderr_text()) from None
    for thread in threads:
        thread.join(timeout=KILL_GRACE_SECONDS)
    return (
        returncode,
        b"".join(out_chunks).decode("utf-8", errors="replace"),
        stderr_text(),
    )


# -- results and the live source ---------------------------------------------------------------


@dataclass(frozen=True)
class SourceResult:
    state: str  # "OK" | "FAILED" | "PARTIAL"
    pages: tuple = ()  # decoded JSON of each page read, in order
    code: str | None = None  # a code from CODES, or "exit:<n>"
    diagnostic: str = ""  # sanitized stderr, at most 2 KiB
    capped: bool = False  # paging stopped at the per-cycle call cap
    calls: int = 0


def _peek(page: Any) -> tuple[Any, Any, Any, Any]:
    """(hasMore, nextCursor, total, number of workers or None); strict checks live in parse.py."""
    result = page.get("result") if isinstance(page, dict) else None
    paging = result.get("page") if isinstance(result, dict) else None
    workers = result.get("workers") if isinstance(result, dict) else None
    if not isinstance(paging, dict):
        return None, None, None, len(workers) if isinstance(workers, list) else None
    return (
        paging.get("hasMore"),
        paging.get("nextCursor"),
        paging.get("total"),
        len(workers) if isinstance(workers, list) else None,
    )


class LiveSource:
    """Pages through ``worker-list`` for one cycle, within the call cap and the time budget."""

    mode = "live"
    variant = None  # only fixture sources have a variant

    def __init__(
        self,
        runner: Runner = production_runner,
        discover: Discover = _find_orca,
        per_call_timeout: float = PER_CALL_TIMEOUT,
    ) -> None:
        self._runner = runner
        self._discover = discover
        self.per_call_timeout = per_call_timeout
        self._discovered = False
        self.orca: str | None = None

    def discover(self) -> bool:
        """Run binary discovery once; True when a validated Orca CLI was found."""
        if not self._discovered:
            self._discovered = True
            self.orca = self._discover()
        return self.orca is not None

    @property
    def available(self) -> bool:
        return self.discover()

    @property
    def namespace(self) -> str:
        """The resolved absolute path of the validated Orca CLI (observer-derived)."""
        return os.path.realpath(self.orca) if self.discover() and self.orca else ""

    def _stop(
        self, pages: list, code: str, diagnostic: str, calls: int
    ) -> SourceResult:
        state = "PARTIAL" if pages else "FAILED"
        return SourceResult(
            state,
            tuple(pages),
            code,
            sanitize(diagnostic, "block")[:STDERR_KEEP_BYTES],
            calls=calls,
        )

    def read_pages(
        self, clock: Any, budget_deadline: float, run_id: str | None = None
    ) -> SourceResult:
        if not self.discover():
            return SourceResult("FAILED", code="not-found")
        pages: list = []
        used: set[str] = set()
        cursor: str | None = None
        calls = 0
        while True:
            remaining = budget_deadline - clock.monotonic()
            if remaining <= 0:
                return self._stop(pages, "overrun", "", calls)
            try:
                argv = build_argv(self.orca, run_id, cursor)
            except ArgvRejected as exc:
                if cursor is not None and exc.code == "cursor-rejected":
                    return self._stop(pages, "cursor-rejected", "", calls)
                raise
            budget_limited = remaining < self.per_call_timeout
            calls += 1
            try:
                reply = self._runner(argv, min(self.per_call_timeout, remaining))
            except (TimeoutError, subprocess.TimeoutExpired):
                return self._stop(
                    pages, "overrun" if budget_limited else "timeout", "", calls
                )
            except RunnerFailure as exc:
                code = (
                    "overrun" if exc.code == "timeout" and budget_limited else exc.code
                )
                return self._stop(pages, code, exc.stderr, calls)
            except OSError as exc:
                return self._stop(pages, "spawn-error", str(exc), calls)
            returncode, stdout = reply[0], reply[1]
            stderr = reply[2] if len(reply) > 2 else ""
            if returncode != 0:
                return self._stop(pages, f"exit:{returncode}", stderr, calls)
            try:
                page = json.loads(stdout)
            except (
                ValueError,
                TypeError,
                RecursionError,
            ):  # deep nesting is not JSON we accept
                return self._stop(pages, "json", stderr, calls)
            pages.append(page)
            has_more, next_cursor, total, worker_count = _peek(page)
            if (
                worker_count == 0
                and isinstance(total, int)
                and not isinstance(total, bool)
                and total > 0
            ):
                return self._stop(pages, "empty-page", "", calls)
            if has_more is not True:
                return SourceResult("OK", tuple(pages), calls=calls)
            if calls >= MAX_CALLS_PER_CYCLE:
                return SourceResult("PARTIAL", tuple(pages), capped=True, calls=calls)
            if next_cursor is None or (
                isinstance(next_cursor, str) and not next_cursor
            ):
                return self._stop(pages, "cursor-stalled", "", calls)
            if not isinstance(next_cursor, str):
                return self._stop(pages, "cursor-rejected", "", calls)
            if next_cursor in used:
                return self._stop(pages, "cursor-stalled", "", calls)
            used.add(next_cursor)
            cursor = next_cursor
