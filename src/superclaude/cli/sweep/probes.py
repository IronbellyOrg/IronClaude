"""Read side of ``superclaude sweep``: the only module that starts a subprocess.

It holds the two seams (``_git`` and ``_orca``), the argv allowlists, the time budget,
the readers for disk and git state, and ``collect``, which gathers one ``SweepInput``
(DESIGN sections 2.1, 7.1 and 7.3). Nothing here writes a file, takes a lock or uses the
network: every ``open`` is a read, every subprocess is one allowlisted ``git status`` or
one allowlisted ``orca-ide`` read verb.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .models import (
    CONTRACT_FILE,
    SHOW_CAP_REASON,
    TIME_BUDGET_REASON,
    ContractRecord,
    OrcaObservation,
    PackageRecord,
    SourceCoverage,
    StatusParse,
    SweepContext,
    SweepInput,
    TabMapEntry,
    TranscriptTail,
    WorktreeState,
    report_folders,
)

# --- Allowlist constants (DESIGN 7.3) ---------------------------------------------------

ORCA_BINARY_DEFAULT = "orca-ide"  # never bare "orca" (SPEC section 8, INV-017)

# Id shapes from the step 1.0a capture; matched with ``re.fullmatch``.
RUN_ID_RE = r"run_[0-9a-f]{12}"
DISPATCH_ID_RE = r"ctx_[0-9a-f]{12}"

ALLOWED_ORCA: tuple[tuple[str, ...], ...] = (
    ("orchestration", "run-current"),
    ("orchestration", "worker-list", "--run", "<run>", "--json"),
    ("orchestration", "worker-show", "--dispatch", "<dispatch>", "--json"),
    ("orchestration", "task-list", "--ready", "--run", "<run>", "--json"),
    ("orchestration", "task-list", "--run", "<run>", "--json"),
    ("worktree", "ps", "--json"),
    ("worktree", "list", "--json"),  # pinned, not called in Phase 1
    ("worktree", "current", "--json"),  # pinned, not called in Phase 1
    ("worktree", "ps", "--agent-wait"),  # allowed by R5 (owner 2026-11-08), not called
    ("worktree", "ps", "--agent-wait", "--json"),  # allowed by R5, not called
)  # 10 templates, 7 verbs (NFR-014)

FORBIDDEN_TOKENS = frozenset({"--include-remote"})  # rejected in any position

# The allowed git calls; the seam prepends
# ``git --no-optional-locks -C <path> -c core.fsmonitor=false``. Index 0 is the status
# call (submodules are ignored: a submodule's own config could start a program, issue 547).
# Indexes 1 to 3 are the read-only inspections that decide whether a git filter could run.
ALLOWED_GIT: tuple[tuple[str, ...], ...] = (
    (
        "status",
        "--porcelain=v1",
        "-z",
        "--branch",
        "--untracked-files=all",
        "--ignore-submodules=all",
    ),
    ("config", "--show-origin", "--list", "-z"),
    ("ls-files", "-z"),
    ("check-attr", "--stdin", "-z", "filter"),
)
CONFIG_LIST, LS_FILES, CHECK_ATTR = ALLOWED_GIT[1], ALLOWED_GIT[2], ALLOWED_GIT[3]

ORCA_VERSION_FILE = Path("/opt/Orca/resources/app.asar.unpacked/out/package.json")
# Byte limits; a limit is hit only when a size is over it.
OUTPUT_LIMIT = 8 * 1024 * 1024  # proposed (DESIGN 17 open item 19)
CONTRACT_LIMIT = LEDGER_LIMIT = 1024 * 1024  # proposed (DESIGN 17 open item 19)
LEDGER_SPLIT = 512 * 1024  # proposed (DESIGN 17 open item 19)
TRANSCRIPT_TAIL = 256 * 1024  # proposed (DESIGN 17 open item 19)
WORKER_LIST_PAGE = 100  # a full page sets truncated (page size from the 1.0a capture)

_PLACEHOLDERS = {"<run>": RUN_ID_RE, "<dispatch>": DISPATCH_ID_RE}
_MIB = 1024 * 1024
_NO_BINDING = "No Run is bound to this terminal."  # captured no-binding sentence
# The two accepted time forms (DESIGN 7.2): SQLite, or ISO 8601 with seconds.
_TIME_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|z|[+-]\d{2}:\d{2})?"
)


class GitCallFailed(Exception):
    """A git call exited non-zero, timed out, could not start or printed too much."""


class BindingError(Exception):
    """No Run could be bound; ``commands`` maps this to exit 2 with the message."""


class ReadFailed(Exception):
    """A disk reader could not use a file; the message is the ``unscanned`` reason."""


@dataclass(frozen=True)
class OrcaResult:
    kind: str  # "ok" | "no_binding" | "unavailable" | "call_failed"
    data: (
        object | None
    )  # for "ok": the envelope's ``result`` object (run-current: the Run id)
    reason: str | None


# --- Budget -----------------------------------------------------------------------------


class Budget:
    """Call, show and time limits for one sweep; passed into ``collect``, never global."""

    def __init__(
        self,
        shows: int = 50,
        total_s: float = 90.0,
        per_call_s: float = 10.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.shows = shows
        self.total_s = total_s
        self.per_call_s = per_call_s
        self._clock = clock
        self._start = clock()
        self._shares: dict[str, int] = {}
        self._taken: dict[str, int] = {}
        self._cut = False
        # Orca calls started so far; the first call's failure means unavailable.
        self.orca_calls = 0

    def share_shows(
        self, runs: tuple[str, ...], wanted: dict[str, int] | None = None
    ) -> None:
        """Split the show cap evenly across ``runs``; the remainder goes to the first.

        ``wanted`` (shows each Run needs, known once every ``worker-list`` is read) lets
        a Run that needs less than its share hand the rest to the Runs that still need
        shows, so ``worker-show`` is ``min(D, shows)`` (DESIGN 7.1 counts table).
        """
        self._shares = {}
        if not runs:
            return
        base, rest = divmod(self.shows, len(runs))
        for i, run in enumerate(runs):
            self._shares[run] = base + (rest if i == 0 else 0)
        if wanted is None:
            return
        for run in runs:
            self._shares[run] = min(self._shares[run], wanted.get(run, 0))
        left = self.shows - sum(self._shares.values())
        for run in runs:
            extra = min(left, wanted.get(run, 0) - self._shares[run])
            if extra > 0:
                self._shares[run] += extra
                left -= extra

    def take_show(self, run: str) -> bool:
        """True and count one show for ``run``; False once its share is spent."""
        used = sum(self._taken.values())
        if used >= self.shows:
            return False
        if run in self._shares:
            allowed = self._shares[run] - self._taken.get(run, 0)
        else:
            allowed = self.shows - used
        if allowed <= 0:
            return False
        self._taken[run] = self._taken.get(run, 0) + 1
        return True

    def call_timeout(self) -> float | None:
        """``min(per_call_s, remaining)``, or None when under 1 s of the total is left."""
        remaining = self._remaining()
        if remaining < 1.0:
            return None
        self._cut = remaining < self.per_call_s
        return min(self.per_call_s, remaining)

    def _remaining(self) -> float:
        return self.total_s - (self._clock() - self._start)

    def spent(self) -> bool:
        """True when under 1 s of the total is left: no call gets a timeout and no re-read runs."""
        return self._remaining() < 1.0

    def cut(self) -> bool:
        """True when the last timeout handed out was cut below ``per_call_s``."""
        return self._cut

    def budget_reason(self) -> str:
        return f"unscanned: {TIME_BUDGET_REASON} ({self.total_s:g} s)"

    def show_cap_reason(self) -> str:
        return f"{SHOW_CAP_REASON} ({self.shows})"


# --- Seams ------------------------------------------------------------------------------


def orca_binary() -> str:
    """``$ORCA_CLI_COMMAND`` when set, else ``orca-ide`` (never bare ``orca``)."""
    return os.environ.get("ORCA_CLI_COMMAND") or ORCA_BINARY_DEFAULT


def _token_matches(template: str, token: str) -> bool:
    pattern = _PLACEHOLDERS.get(template)
    if pattern is None:
        return template == token
    return re.fullmatch(pattern, token) is not None


def check_orca_argv(args: tuple[str, ...]) -> None:
    """Raise ValueError unless ``args`` matches one ``ALLOWED_ORCA`` template exactly."""
    argv = tuple(args)
    if not all(isinstance(a, str) for a in argv):
        raise ValueError(f"orca arguments are not allowed: {argv!r}")
    if FORBIDDEN_TOKENS.intersection(argv):
        raise ValueError(f"orca arguments are not allowed: {argv!r}")
    for template in ALLOWED_ORCA:
        if len(template) == len(argv) and all(
            _token_matches(t, a) for t, a in zip(template, argv)
        ):
            return
    raise ValueError(f"orca arguments are not allowed: {argv!r}")


def check_git_args(args: tuple[str, ...]) -> None:
    """Raise ValueError unless ``args`` equals an ``ALLOWED_GIT`` entry exactly."""
    if tuple(args) not in ALLOWED_GIT:
        raise ValueError(f"git arguments are not allowed: {args!r}")


def _json_or_none(text: str) -> object | None:
    try:
        return json.loads(text)
    except ValueError:
        return None


def _run_current_result(text: str) -> OrcaResult:
    """Plain-text ``run-current``: the no-binding sentence, or exactly one Run id."""
    if not text.strip():
        return OrcaResult("call_failed", None, "orca call failed (invalid response)")
    if text.strip().startswith(_NO_BINDING):
        return OrcaResult("no_binding", None, "no Run bound")
    ids = set(re.findall(rf"\b{RUN_ID_RE}\b", text))
    if len(ids) == 1:
        return OrcaResult("ok", ids.pop(), None)
    return OrcaResult("call_failed", None, "orca call failed (invalid response)")


def _orca(*args: str, timeout: float) -> OrcaResult:
    """Run one allowlisted Orca read and classify the result once (SPEC section 8)."""
    check_orca_argv(tuple(args))  # ValueError before any process starts
    binary = orca_binary()
    # shortcut: subprocess.run buffers the whole output and the 8 MiB limit is checked after the
    # child exits; the 10 s timeout kills a runaway. Upgrade to Popen with a chunked read and a kill
    # at the limit only if a call is seen to exceed the limit (owner ruling 2026-11-12, D-01).
    try:
        proc = subprocess.run(
            [binary, *args],
            capture_output=True,
            timeout=timeout,
            check=False,
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return OrcaResult("unavailable", None, f"timeout after {timeout:g} s")
    except FileNotFoundError:
        return OrcaResult("unavailable", None, f"binary not found: {binary}")
    except OSError as exc:
        return OrcaResult("unavailable", None, f"could not start {binary}: {exc}")
    if len(proc.stdout) + len(proc.stderr) > OUTPUT_LIMIT:
        return OrcaResult(
            "call_failed", None, f"output over {OUTPUT_LIMIT // _MIB} MiB"
        )
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace").strip()
    parsed = _json_or_none(out)
    error = parsed.get("error") if isinstance(parsed, dict) else None
    code = error.get("code") if isinstance(error, dict) else None
    first_err = err.splitlines()[0].strip() if err else ""
    # The marker counts only as the error code or the whole first stderr line.
    if code == "runtime_unavailable" or first_err == "runtime_unavailable":
        return OrcaResult("unavailable", None, "runtime_unavailable")
    if proc.returncode != 0:
        return OrcaResult(
            "call_failed", None, f"orca call failed (exit {proc.returncode})"
        )
    if tuple(args) == ("orchestration", "run-current"):
        return _run_current_result(out)
    if (
        isinstance(parsed, dict)
        and parsed.get("ok") is True
        and isinstance(parsed.get("result"), dict)
    ):
        return OrcaResult("ok", parsed["result"], None)
    return OrcaResult("call_failed", None, "orca call failed (invalid response)")


def _git(
    cwd: Path,
    *args: str,
    timeout: float,
    stdin: bytes | None = None,
    binary: bool = False,
) -> str | bytes:
    """Run an allowed git call in ``cwd`` and return its stdout (text, or bytes if ``binary``).

    The argv always starts ``git --no-optional-locks -C <cwd> -c core.fsmonitor=false`` and
    the child runs with ``GIT_OPTIONAL_LOCKS=0``, so a caller cannot build a git argv
    without them. Fsmonitor is always off: a command named by repository configuration or
    by the inherited environment would otherwise run during status (issue 547). ``stdin``
    is fed to the child; ``binary`` keeps paths that are not valid UTF-8 intact.
    """
    check_git_args(args)
    argv = [
        "git",
        "--no-optional-locks",
        "-C",
        str(cwd),
        "-c",
        "core.fsmonitor=false",
        *args,
    ]
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    extra = {} if stdin is None else {"input": stdin}
    # shortcut: same as ``_orca``: run buffers the output; see the note there (owner ruling 2026-11-12).
    try:
        proc = subprocess.run(
            argv, capture_output=True, timeout=timeout, check=False, env=env, **extra
        )
    except subprocess.TimeoutExpired as exc:
        raise GitCallFailed(f"timeout after {timeout:g} s") from exc
    except OSError as exc:
        raise GitCallFailed(f"could not start git: {exc}") from exc
    if len(proc.stdout) + len(proc.stderr) > OUTPUT_LIMIT:
        raise GitCallFailed(f"output over {OUTPUT_LIMIT} bytes")
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip().splitlines()
        raise GitCallFailed(
            f"git exited {proc.returncode}" + (f": {detail[0]}" if detail else "")
        )
    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")


# The result key that must hold a list in each captured list reply (steps 1.0a and 1.4).
_LIST_KEY = {
    ("orchestration", "worker-list"): "workers",
    ("orchestration", "task-list"): "tasks",
    ("worktree", "ps"): "worktrees",
}


def _call(budget: Budget, *args: str) -> OrcaResult:
    """One budgeted Orca call. A budget-cut timeout is ``call_failed``, never unavailable."""
    timeout = budget.call_timeout()
    if timeout is None:
        return OrcaResult("call_failed", None, budget.budget_reason())
    first = budget.orca_calls == 0
    budget.orca_calls += 1
    result = _orca(*args, timeout=timeout)
    list_key = _LIST_KEY.get(tuple(args[:2]))
    if (
        result.kind == "ok"
        and list_key is not None
        and not isinstance(_get(result.data, list_key), list)
    ):
        # SPEC section 8: JSON without the captured list shape is an invalid response.
        result = OrcaResult("call_failed", None, "orca call failed (invalid response)")
    if (
        result.kind == "unavailable"
        and (result.reason or "").startswith("timeout")
        and budget.cut()
    ):
        return OrcaResult("call_failed", None, budget.budget_reason())
    if first and result.kind == "call_failed":
        # A nonzero exit or invalid response on the very first Orca call means unavailable.
        return OrcaResult("unavailable", None, result.reason)
    return result


def bind_run(budget: Budget) -> str:
    """``run-current``: the bound Run id, else ``BindingError`` (commands maps it to exit 2)."""
    result = _call(budget, "orchestration", "run-current")
    if result.kind == "ok" and isinstance(result.data, str):
        return result.data
    if result.kind == "no_binding":
        raise BindingError("no Run bound: pass --run <id>")
    raise BindingError(
        f"Orca unavailable ({result.reason}); no Run binding could be established: "
        "pass --run <id>"
    )


# --- Parsing helpers --------------------------------------------------------------------


def parse_time(value: object) -> datetime | None:
    """Aware UTC ``datetime`` from the two accepted forms (DESIGN 7.2); never raises.

    Accepted: SQLite ``YYYY-MM-DD HH:MM:SS`` (no zone, read as UTC) and ISO 8601 with
    ``Z`` or an offset. Anything else, including a non-string, is None.
    """
    if not isinstance(value, str):
        return None
    text = value.strip()
    if _TIME_RE.fullmatch(text) is None:  # date-only, no seconds or basic format
        return None
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        if "T" in text:  # a naive ISO form is neither accepted form
            return None
        return parsed.replace(tzinfo=timezone.utc)
    try:
        return parsed.astimezone(timezone.utc)
    except (OverflowError, ValueError):
        return None


def _get(obj: object, *path: str) -> object | None:
    """Nested dict lookup that returns None at the first missing step."""
    for key in path:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(key)
    return obj


def _text(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _first(*values: object) -> object | None:
    """The first value that is not None: the ``worker-show`` value wins over the list row."""
    return next((v for v in values if v is not None), None)


def parse_worker_show(
    run: str, list_row: object, show: object | None
) -> OrcaObservation:
    """Build one observation from a ``worker-list`` row and its ``worker-show`` result.

    Never raises. The show value wins for every field both return. Fields that only the
    show returns stay None when there is no show, so such a row prints could not
    determine (WC-10) and counts toward ``bound_reached``.
    """
    dispatch = _text(_first(_get(list_row, "dispatchId"), _get(show, "dispatch", "id")))
    # No agentWait field is read: its live name was not captured (step 1.0a, open item 6),
    # so ``agent_wait``, ``agent_wait_present`` and ``agent_wait_since`` keep their model
    # defaults until a read-only capture records the names.
    return OrcaObservation(
        dispatch=dispatch or "",
        run=run,
        session_join=_text(_get(show, "dispatch", "assigneeHandle")),
        dispatch_started=parse_time(_get(show, "dispatch", "dispatchedAt")),
        dispatch_ended=parse_time(_get(show, "dispatch", "completedAt")),
        dispatch_status=_text(_get(show, "dispatch", "status")),
        liveness_verdict=_text(_get(show, "projection", "liveness", "verdict")),
        status=_text(_get(show, "dispatch", "status")),
        outcome=_text(_get(show, "projection", "outcome")),
        parent=_text(
            _first(
                _get(show, "projection", "parent"),
                _get(list_row, "projection", "parent"),
            )
        ),
        worktree_path=_text(_get(show, "terminal", "worktreePath")),
        terminal_state=_text(
            _first(
                _get(show, "projection", "resource", "terminalState"),
                _get(list_row, "terminalState"),
                _get(list_row, "projection", "resource", "terminalState"),
            )
        ),
        next_action=_text(
            _first(
                _get(show, "projection", "nextAction", "kind"),
                _get(list_row, "projection", "nextAction", "kind"),
            )
        ),
    )


def parse_status(raw: str) -> StatusParse:
    """Parse ``git status --porcelain=v1 -z --branch`` output (NUL fields, rename pairs)."""
    fields = raw.split("\0")
    if fields and fields[-1] == "":
        fields.pop()
    header = ""
    if fields and fields[0].startswith("## "):
        header = fields.pop(0)[3:]
    entries: list[tuple[str, str]] = []
    i = 0
    while i < len(fields):
        field = fields[i]
        i += 1
        if len(field) < 4 or field[2] != " ":
            continue
        code, path = field[:2], field[3:]
        entries.append((code, path))
        if ("R" in code or "C" in code) and i < len(fields):
            entries.append((code, fields[i]))  # rename or copy: the old path as well
            i += 1
    ahead, has_upstream, note = _parse_header(header)
    return StatusParse(tuple(entries), header, ahead, has_upstream, note)


def _parse_header(header: str) -> tuple[int | None, bool | None, str | None]:
    """(ahead, has_upstream, note) from the branch header line (M7)."""
    if header.startswith("No commits yet"):
        return None, None, "no commits yet"
    if header.startswith("HEAD (no branch)"):
        return None, None, "detached HEAD"
    names, _, counts = header.partition(" [")
    if "..." not in names:
        return None, False, "no upstream"
    parts = [p.strip() for p in counts.rstrip("]").split(",")] if counts else []
    if "gone" in parts:
        return None, None, "upstream gone"
    ahead = 0
    for part in parts:
        match = re.fullmatch(r"ahead (\d+)", part)
        if match:
            ahead = int(match.group(1))
    return ahead, True, (f"ahead {ahead}" if ahead > 0 else None)


# --- Disk readers -----------------------------------------------------------------------


def _unscanned(reason: str | None) -> str | None:
    """The ``SourceCoverage.unscanned`` text: a reason without its ``unscanned:`` prefix."""
    if reason is None:
        return None
    return reason[len("unscanned: ") :] if reason.startswith("unscanned: ") else reason


def _inside(path: Path, root: Path) -> bool:
    """True when ``path`` re-resolved (symlinks followed) stays under ``root`` resolved."""
    try:
        return path.resolve().is_relative_to(root.resolve())
    except (OSError, RuntimeError, ValueError):
        return False


def _check_inside(path: Path, root: Path | None) -> None:
    if root is not None and not _inside(path, root):
        raise ReadFailed("outside root")


def _stat_key(path: Path) -> tuple[int, int]:
    st = os.stat(path)
    return st.st_size, st.st_mtime_ns


def _stable(
    path: Path, read: Callable[[], object], budget: Budget | None = None
) -> object:
    """Run ``read``; if the file changed meanwhile read once more while ``budget`` allows.

    A second change, or a change with no budget left (DESIGN 7.2, NFR-007), is a conflict.
    """
    for _ in range(2):
        before = _stat_key(path)
        result = read()
        if _stat_key(path) == before:
            return result
        if budget is not None and budget.spent():
            break
    raise ReadFailed("conflict: inconsistent observation")


def _ledger_has_final(path: Path) -> bool:
    size = os.stat(path).st_size
    with open(path, "rb") as handle:
        if size > LEDGER_LIMIT:
            # Over the limit: only the last LEDGER_SPLIT bytes are searched, and the first
            # (partial) line of that tail is dropped.
            handle.seek(size - LEDGER_SPLIT)
            data = handle.read(LEDGER_SPLIT)
            data = data.split(b"\n", 1)[1] if b"\n" in data else b""
        else:
            data = handle.read()
    text = data.decode("utf-8", "replace")
    return any(line.lstrip().startswith("FINAL:") for line in text.splitlines())


def _ledger(
    path: Path, root: Path | None, budget: Budget | None = None
) -> tuple[bool | None, str | None]:
    try:
        _check_inside(path, root)
        return bool(_stable(path, lambda: _ledger_has_final(path), budget)), None
    except ReadFailed as exc:
        return None, str(exc)
    except FileNotFoundError:
        return (
            False,
            None,
        )  # no ledger means no FINAL line, so the package is unfinished (GQ-105)
    except OSError:
        return None, "ledger not readable"


def read_ledger(path: Path, root: Path | None = None) -> bool | None:
    """True when a line starts with ``FINAL:`` (after optional blanks); None when unread."""
    return _ledger(path, root)[0]


def _marker(path: Path, root: Path) -> bool:
    """True when ``path`` exists and re-resolves inside ``root`` (an outside file is no marker)."""
    if not _inside(path, root):
        return False
    try:
        os.stat(path)
    except OSError:
        return False
    return True


def _packages(
    worktree: Path, budget: Budget | None = None
) -> tuple[tuple[PackageRecord, ...], tuple[SourceCoverage, ...]]:
    """Package records plus one unscanned row for each folder or ledger that was not read."""
    where: dict[str, dict[str, Path]] = {}
    rows: list[SourceCoverage] = []
    for location in ("to-do", "done"):
        folder = worktree / ".dev" / "tasks" / location
        if not _inside(folder, worktree):
            rows.append(
                SourceCoverage(
                    f"package folder {folder}", "unscanned", None, "outside root"
                )
            )
            continue
        try:
            with os.scandir(folder) as entries:
                names = sorted(e.name for e in entries if e.is_dir())
        except FileNotFoundError:
            continue  # no such folder: nothing to read
        except OSError:
            rows.append(
                SourceCoverage(
                    f"package folder {folder}",
                    "unscanned",
                    None,
                    "package folder not readable",
                )
            )
            continue
        for name in names:
            if not _inside(folder / name, worktree):
                rows.append(
                    SourceCoverage(
                        f"package {folder / name}", "unscanned", None, "outside root"
                    )
                )
                continue
            where.setdefault(name, {})[location] = folder / name
    records = []
    for name in sorted(where):
        places = where[name]
        location = "both" if len(places) == 2 else next(iter(places))
        marker = any(_marker(p / ".archiving", worktree) for p in places.values())
        final: bool | None = None
        if "to-do" in places:
            ledger = places["to-do"] / "progress.md"
            final, reason = _ledger(ledger, worktree, budget)
            if reason is not None:
                rows.append(
                    SourceCoverage(
                        f"package ledger {ledger}", "unscanned", None, reason
                    )
                )
        records.append(PackageRecord(name, location, final, marker, None, "unknown"))
    return tuple(records), tuple(rows)


def read_packages(worktree: Path) -> tuple[PackageRecord, ...]:
    """Package folders under ``<worktree>/.dev/tasks/{to-do,done}/``; fixed pattern only.

    ``active`` stays None (``read_worktree`` sets it from the one status call) and
    ``state`` is a placeholder that ``classify.package_state`` replaces.
    """
    return _packages(worktree)[0]


def _yaml_top(text: str) -> dict[str, object]:
    """The top-level mapping of a contract file; ``{}`` for invalid YAML or a non-mapping.

    ``yaml.safe_load`` is what ``cli/reflect/contract.py`` uses on the same file name. The
    caller has already bounded ``text`` to ``CONTRACT_LIMIT``; ``safe_load`` never builds an
    object from a tag, a document nested too deep for the parser is one more invalid file, and
    a scalar the loader rejects (``ValueError``, for example the date ``2026-13-45``) is too.
    """
    try:
        data = yaml.safe_load(text)
    except (yaml.YAMLError, RecursionError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _contract_from_text(
    path: Path, text: str, mtime: datetime | None = None
) -> ContractRecord:
    top = _yaml_top(text)

    def scalar(key: str) -> str | None:
        value = top.get(key)
        value = value.strip() if isinstance(value, str) else None
        return value or None

    artifacts = top.get("artifacts")
    report = scalar("report_path")
    return ContractRecord(
        path=path,
        worker_status=scalar("worker_status"),
        blocked_question=scalar("blocked_question"),
        reason=scalar("reason"),
        report_path=Path(report) if report else None,
        artifacts=tuple(Path(a) for a in artifacts if isinstance(a, str) and a)
        if isinstance(artifacts, list)
        else (),
        command=scalar("command"),
        mtime=mtime,
    )


def _contract(
    path: Path, root: Path | None, budget: Budget | None = None
) -> tuple[ContractRecord | None, str | None]:
    try:
        _check_inside(path, root)
        if os.stat(path).st_size > CONTRACT_LIMIT:
            return None, f"over {CONTRACT_LIMIT // _MIB} MiB"
        raw = _stable(path, lambda: path.read_bytes(), budget)
        # The file time of the bytes just read (SP-15 age); read once, here.
        mtime = datetime.fromtimestamp(os.stat(path).st_mtime, timezone.utc)
    except ReadFailed as exc:
        return None, str(exc)
    except (OSError, ValueError, OverflowError):
        return None, "contract not readable"
    assert isinstance(raw, bytes)
    return _contract_from_text(path, raw.decode("utf-8", "replace"), mtime), None


def read_contract(path: Path, root: Path | None = None) -> ContractRecord | None:
    """The parsed worker contract at ``path``; None when over 1 MiB, unreadable or escaping."""
    return _contract(path, root)[0]


def _tail_from_bytes(
    path: Path, data: bytes, complete: bool, mtime: datetime
) -> TranscriptTail:
    stamps: list[datetime] = []
    session_id: str | None = None
    last_ts: datetime | None = None
    for line in data.decode("utf-8", "replace").splitlines():
        if not line.strip():
            continue
        record = _json_or_none(line)
        if not isinstance(record, dict):
            continue  # a last line cut mid-object, or not an object
        ts = parse_time(record.get("timestamp"))
        sid = record.get("sessionId")
        if ts is not None:
            stamps.append(ts)
        if ts is not None and isinstance(sid, str) and sid:
            session_id = sid  # a complete record: both fields
            last_ts = ts  # only a complete record sets the last time (a trailing
            # record without a timestamp must not blank it)
    readable = session_id is not None
    return TranscriptTail(
        path=path,
        session_id=session_id,
        readable=readable,
        last_record_ts=last_ts if readable else None,
        first_record_ts=min(stamps) if readable and stamps else None,
        tail_complete=complete,
        mtime=mtime,
        project_key=path.parent.name,
    )


def _transcript(
    path: Path, root: Path | None, budget: Budget | None = None
) -> tuple[TranscriptTail, str | None]:
    epoch = datetime.fromtimestamp(0, timezone.utc)

    def unreadable(mtime: datetime, reason: str) -> tuple[TranscriptTail, str]:
        return (
            TranscriptTail(
                path, None, False, None, None, False, mtime, path.parent.name
            ),
            reason,
        )

    try:
        _check_inside(path, root)
        mtime = datetime.fromtimestamp(os.stat(path).st_mtime, timezone.utc)
    except ReadFailed as exc:
        return unreadable(epoch, str(exc))
    except OSError:
        return unreadable(epoch, "transcript not readable")

    def read() -> tuple[bytes, bool]:
        size = os.stat(path).st_size
        with open(path, "rb") as handle:
            if size > TRANSCRIPT_TAIL:
                handle.seek(size - TRANSCRIPT_TAIL)
                data = handle.read(TRANSCRIPT_TAIL)
                # Drop bytes up to and including the first newline (a partial line).
                return (data.split(b"\n", 1)[1] if b"\n" in data else b""), False
            return handle.read(), True

    try:
        result = _stable(path, read, budget)
        reason = None
    except ReadFailed as exc:
        reason = str(exc)
        try:  # keep the last read so the row still has data; the reason forces could not determine
            result = read()
        except OSError:
            return unreadable(mtime, "transcript not readable")
    except OSError:
        return unreadable(mtime, "transcript not readable")
    data, complete = result  # type: ignore[misc]
    return _tail_from_bytes(path, data, complete, mtime), reason


def read_transcript_tail(path: Path, root: Path | None = None) -> TranscriptTail:
    """The last 256 KiB of a transcript, first partial line dropped (DESIGN 7.1)."""
    return _transcript(path, root)[0]


def _tab_map(state_dir: Path) -> tuple[tuple[TabMapEntry, ...], str | None]:
    folder = state_dir / "ccsession" / "orca-tabs"
    try:
        with os.scandir(folder) as scan:
            names = sorted(e.name for e in scan if not e.name.startswith("."))
    except FileNotFoundError:
        return (), None  # a missing folder is readable and empty
    except OSError:
        return (), "tab map folder not readable"
    entries: list[TabMapEntry] = []
    problem: str | None = None
    for name in names:
        path = folder / name
        if not _inside(path, folder):
            problem = "outside root"
            continue
        try:
            if not path.is_file():
                continue
            lines = [s.strip() for s in path.read_text("utf-8", "replace").splitlines()]
        except OSError:
            problem = "tab map entry not readable"
            continue
        if len(lines) >= 3 and all(lines[:3]):
            entries.append(TabMapEntry(name, lines[0], lines[1], lines[2]))
    return tuple(entries), problem


def read_tab_map(state_dir: Path) -> tuple[TabMapEntry, ...]:
    """Entries of ``<state_dir>/ccsession/orca-tabs/``: pane key, session id, folder, handle."""
    return _tab_map(state_dir)[0]


def read_orca_version(path: Path = ORCA_VERSION_FILE) -> str | None:
    """The ``version`` field of Orca's ``package.json``; None when it cannot be read."""
    try:
        with open(path, "rb") as handle:
            data = handle.read(CONTRACT_LIMIT + 1)
    except OSError:
        return None
    if len(data) > CONTRACT_LIMIT:
        return None
    parsed = _json_or_none(data.decode("utf-8", "replace"))
    version = parsed.get("version") if isinstance(parsed, dict) else None
    return version if isinstance(version, str) and version else None


# --- Git reader -------------------------------------------------------------------------


def _worktree_state(
    path: Path, status: StatusParse | None, packages: tuple[PackageRecord, ...]
) -> WorktreeState:
    if status is None:
        return WorktreeState(
            path=str(path),
            status_read=False,
            uncommitted=None,
            unpushed=None,
            dev_tasks_unsaved=None,
            changed_paths=(),
            packages=packages,
            shared_package_ids=(),
            frozen=None,
        )
    changed = tuple(p for _, p in status.entries)
    unpushed: bool | None
    if status.ahead is not None and status.ahead > 0:
        unpushed = True
    elif status.has_upstream and status.ahead == 0:
        unpushed = False
    else:
        unpushed = None
    marked = tuple(
        replace(pkg, active=_package_active(pkg, changed)) for pkg in packages
    )
    return WorktreeState(
        path=str(path),
        status_read=True,
        uncommitted=bool(changed),
        unpushed=unpushed,
        dev_tasks_unsaved=any(p.startswith(".dev/tasks/") for p in changed),
        changed_paths=changed,
        packages=marked,
        shared_package_ids=(),
        frozen=None,  # set to True by classify_all from the rows' policy, never here
        upstream_note=status.header_note,
    )


def _package_active(pkg: PackageRecord, changed: tuple[str, ...]) -> bool:
    """GQ-101: active when the one status call lists a path inside the package folder."""
    places = ("to-do", "done") if pkg.location == "both" else (pkg.location,)
    prefixes = tuple(f".dev/tasks/{place}/{pkg.id}/" for place in places)
    return any(p.startswith(prefixes) for p in changed)


FILTER_REASON = "git filter could run a program"


def _filter_drivers(config: bytes) -> set[bytes]:
    """Filter driver names whose effective ``clean`` or ``process`` command is non-empty.

    ``config`` is ``git config --show-origin --list -z`` output: for each entry the origin,
    then ``key\\nvalue``. Anything else raises ``GitCallFailed`` (an unclear list is refused).
    """
    parts = config.split(b"\0")
    if parts and parts[-1] == b"":
        parts.pop()
    if len(parts) % 2:
        raise GitCallFailed("unreadable git configuration")
    effective: dict[bytes, bytes] = {}
    for entry in parts[1::2]:
        key, _, value = entry.partition(b"\n")
        effective[key] = value  # a later entry overrides an earlier one
    return {
        key[len(b"filter.") : key.rindex(b".")]
        for key, value in effective.items()
        if value
        and key.startswith(b"filter.")
        and key.endswith((b".clean", b".process"))
        and key.count(b".") >= 2
    }


def _filter_blocks_status(path: Path, timeout: float) -> bool:
    """True when a git filter with a command is selected by a tracked path of ``path``.

    ``git status`` runs that command for a file it has to re-read. The three calls only
    read; each runs with fsmonitor off (``_git``). A driver defined only in a submodule's
    own config is not seen here; ``--ignore-submodules=all`` on the status call closes it.
    Raises ``GitCallFailed`` when any call fails or its output cannot be parsed.
    """
    # shortcut: a filter named only in a submodule's own config is not seen here; the status
    # call's --ignore-submodules=all closes it. Upgrade if submodule state is ever reported.
    drivers = _filter_drivers(_git(path, *CONFIG_LIST, timeout=timeout, binary=True))
    if not drivers:
        return False
    tracked = _git(path, *LS_FILES, timeout=timeout, binary=True)
    if not tracked:
        return False
    attrs = _git(path, *CHECK_ATTR, timeout=timeout, stdin=tracked, binary=True).split(
        b"\0"
    )
    if attrs and attrs[-1] == b"":
        attrs.pop()
    if len(attrs) % 3:  # path, attribute, value per tracked path
        raise GitCallFailed("unreadable git attributes")
    return any(value in drivers for value in attrs[2::3])


def _read_worktree(
    path: Path, budget: Budget
) -> tuple[WorktreeState, tuple[SourceCoverage, ...]]:
    """The state plus its git row and one row per unread package folder or ledger."""
    name = f"git status {path}"
    packages, package_rows = _packages(path, budget)
    try:
        os.stat(path)
    except OSError:
        state, row = _failed_worktree(path, packages, name, "worktree not readable")
        return state, (row, *package_rows)
    timeout = budget.call_timeout()
    if timeout is None:
        reason = _unscanned(budget.budget_reason())
        state, row = _failed_worktree(path, packages, name, reason)
        return state, (row, *package_rows)
    try:
        if _filter_blocks_status(path, timeout):
            state, row = _failed_worktree(path, packages, name, FILTER_REASON)
            return state, (row, *package_rows)
        raw = _git(path, *ALLOWED_GIT[0], timeout=timeout)
    except GitCallFailed as exc:
        cut = str(exc).startswith("timeout") and budget.cut()
        reason = _unscanned(budget.budget_reason()) if cut else "worktree not readable"
        state, row = _failed_worktree(path, packages, name, reason)
        return state, (row, *package_rows)
    state = _worktree_state(path, parse_status(raw), packages)
    return state, (SourceCoverage(name, "read", None, None), *package_rows)


def read_worktree(path: Path, budget: Budget) -> tuple[WorktreeState, SourceCoverage]:
    """One ``git status`` for ``path`` plus its package folders; never raises."""
    state, rows = _read_worktree(path, budget)
    return state, rows[0]


def _failed_worktree(
    path: Path, packages: tuple[PackageRecord, ...], name: str, reason: str | None
) -> tuple[WorktreeState, SourceCoverage]:
    state = _worktree_state(path, None, packages)
    return state, SourceCoverage(name, "unscanned", None, reason)


# --- collect ----------------------------------------------------------------------------


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _age(now: datetime, mtime: datetime) -> int:
    return max(0, int((now - mtime).total_seconds()))


def _project_key(path: Path) -> str:
    """Claude Code's project folder name: every non-alphanumeric character becomes ``-``."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def _task_body(task: dict) -> str | None:
    """The worker report ``body`` stored in a Task's ``result`` JSON, if any."""
    result = task.get("result")
    parsed = _json_or_none(result) if isinstance(result, str) else result
    return _text(parsed.get("body")) if isinstance(parsed, dict) else None


_CONTRACT_PATH_RE = re.compile(rf"(/[^\s'\"`<>()]*/{re.escape(CONTRACT_FILE)})")
# A quoted full path may hold spaces; it is one value, read whole before the bare scan.
_QUOTED_CONTRACT_RE = re.compile(rf"([\"'])(/[^\"'\n]*/{re.escape(CONTRACT_FILE)})\1")


def _contract_candidates(obs: OrcaObservation) -> tuple[Path, ...]:
    """Contract files an Orca row's own text names: a full path or a report folder."""
    found: dict[str, None] = {}
    for text in (obs.task_spec_text, obs.body_text):
        if not text:
            continue
        for match in _QUOTED_CONTRACT_RE.finditer(text):
            found[match.group(2)] = None
        # Blank the quoted paths so a slash after a space is not read as a new path.
        for match in _CONTRACT_PATH_RE.finditer(_QUOTED_CONTRACT_RE.sub(" ", text)):
            found[match.group(1)] = None
        for folder in report_folders(text, obs.worktree_path):
            found[f"{folder}/{CONTRACT_FILE}"] = None
    return tuple(Path(p) for p in found)


@dataclass
class _OrcaState:
    available: bool = True
    truncated: bool = False


def _orca_reads(
    runs: tuple[str, ...],
    budget: Budget,
    state: _OrcaState,
    sources: list[SourceCoverage],
) -> list[OrcaObservation]:
    """worker-list and task-list (ready and all) for every Run, then worker-show.

    The shows start only after every ``worker-list`` is read, so the show cap is split by
    the rows each Run really has (DESIGN 7.1: ``min(D, 50)``).
    """
    rows: list[OrcaObservation] = []
    fetched: list[tuple[str, list[dict], list[dict], dict[str, dict]]] = []

    def skip(name: str) -> None:
        sources.append(SourceCoverage(name, "unscanned", None, "orca unavailable"))

    def record(name: str, result: OrcaResult, note: str = "read") -> bool:
        """Source row for one call; True when the call gave data."""
        if result.kind == "ok":
            sources.append(SourceCoverage(name, note, None, None))
            return True
        sources.append(
            SourceCoverage(name, "unscanned", None, _unscanned(result.reason))
        )
        if result.kind == "unavailable":
            state.available = False
        return False

    for run in runs:
        list_name, task_name = f"orca worker-list {run}", f"orca task-list {run}"
        ready_name = f"orca task-list --ready {run}"
        if not state.available:
            for name in (list_name, ready_name, task_name):
                skip(name)
            continue
        listing = _call(budget, "orchestration", "worker-list", "--run", run, "--json")
        workers: list[dict] = []
        if record(list_name, listing):
            raw = _get(listing.data, "workers")
            workers = (
                [w for w in raw if isinstance(w, dict)] if isinstance(raw, list) else []
            )
            more = _get(listing.data, "page", "hasMore") is True
            if len(workers) >= WORKER_LIST_PAGE or more:
                state.truncated = True
        tasks_by_id: dict[str, dict] = {}
        ready_tasks: list[dict] = []
        if state.available:
            ready = _call(
                budget, "orchestration", "task-list", "--ready", "--run", run, "--json"
            )
            if record(ready_name, ready):
                raw = _get(ready.data, "tasks")
                ready_tasks = (
                    [t for t in raw if isinstance(t, dict)]
                    if isinstance(raw, list)
                    else []
                )
        else:
            skip(ready_name)
        if state.available:
            every = _call(budget, "orchestration", "task-list", "--run", run, "--json")
            if record(task_name, every):
                raw = _get(every.data, "tasks")
                for task in raw if isinstance(raw, list) else []:
                    if isinstance(task, dict) and isinstance(task.get("id"), str):
                        tasks_by_id[task["id"]] = task
        else:
            skip(task_name)
        fetched.append((run, workers, ready_tasks, tasks_by_id))
    budget.share_shows(runs, {run: _show_demand(w) for run, w, _, _ in fetched})
    for run, workers, ready_tasks, tasks_by_id in fetched:
        rows.extend(
            _run_rows(run, workers, ready_tasks, tasks_by_id, budget, state, sources)
        )
    return rows


def _show_demand(workers: list[dict]) -> int:
    """Shows a Run needs: one per valid Dispatch id whose duplicate rows all agree."""
    raws: dict[str, list[dict]] = {}
    for row in workers:
        dispatch = row.get("dispatchId")
        if isinstance(dispatch, str) and re.fullmatch(DISPATCH_ID_RE, dispatch):
            raws.setdefault(dispatch, []).append(row)
    return sum(1 for rs in raws.values() if all(r == rs[0] for r in rs))


def _run_rows(
    run: str,
    workers: list[dict],
    ready_tasks: list[dict],
    tasks_by_id: dict[str, dict],
    budget: Budget,
    state: _OrcaState,
    sources: list[SourceCoverage],
) -> list[OrcaObservation]:
    raws: dict[str, list[dict]] = {}
    for row in workers:
        raws.setdefault(str(row.get("dispatchId")), []).append(row)
    shows: dict[str, object | None] = {}
    rows: list[OrcaObservation] = []
    for index, row in enumerate(workers):
        dispatch = row.get("dispatchId")
        if not isinstance(dispatch, str) or not re.fullmatch(DISPATCH_ID_RE, dispatch):
            # An id the allowlist would refuse is never put into an argv. A row whose id is
            # missing, not a string or empty is dropped (only this source row remains), so
            # the FR-010 guard cannot see it; whether real Orca emits such rows is unverified.
            name = f"orca worker-list {run} row {index}"
            sources.append(
                SourceCoverage(
                    name, "unscanned", None, "row without a valid Dispatch id"
                )
            )
            if isinstance(dispatch, str) and dispatch:
                rows.append(
                    _with_task(parse_worker_show(run, row, None), row, tasks_by_id)
                )
            continue
        disagree = any(r != raws[dispatch][0] for r in raws[dispatch])
        if disagree:
            # Duplicate rows that differ are kept apart; no show is used to pick one.
            obs = replace(
                parse_worker_show(run, row, None),
                dispatch_status=_text(row.get("dispatchStatus")),
            )
            rows.append(_with_task(obs, row, tasks_by_id))
            continue
        show = shows.get(dispatch)
        if dispatch not in shows:
            show = _show(dispatch, run, budget, state, sources)
            shows[dispatch] = show
        rows.append(_with_task(parse_worker_show(run, row, show), row, tasks_by_id))
    known = {r.get("taskId") for r in workers}
    for task in ready_tasks:
        task_id = task.get("id")
        if isinstance(task_id, str) and task_id not in known:
            rows.append(
                OrcaObservation(
                    dispatch=task_id,
                    run=run,
                    status="ready",
                    task_spec_text=_text(task.get("spec")),
                )
            )
    return rows


def _show(
    dispatch: str,
    run: str,
    budget: Budget,
    state: _OrcaState,
    sources: list[SourceCoverage],
) -> object | None:
    name = f"orca worker-show {dispatch}"
    if not state.available:
        sources.append(SourceCoverage(name, "unscanned", None, "orca unavailable"))
        return None
    if not budget.take_show(run):
        sources.append(
            SourceCoverage(name, "unscanned", None, budget.show_cap_reason())
        )
        return None
    result = _call(
        budget, "orchestration", "worker-show", "--dispatch", dispatch, "--json"
    )
    if result.kind == "ok":
        sources.append(SourceCoverage(name, "read", None, None))
        return result.data
    sources.append(SourceCoverage(name, "unscanned", None, _unscanned(result.reason)))
    if result.kind == "unavailable":
        state.available = False
    return None


def _with_task(
    obs: OrcaObservation, row: dict, tasks_by_id: dict[str, dict]
) -> OrcaObservation:
    task = (
        tasks_by_id.get(row.get("taskId"))
        if isinstance(row.get("taskId"), str)
        else None
    )
    if task is None:
        return obs
    return replace(
        obs, task_spec_text=_text(task.get("spec")), body_text=_task_body(task)
    )


def _worktree_paths(root: Path, result: OrcaResult | None) -> tuple[Path, ...]:
    """The root, then each distinct canonical path from ``worktree ps``."""
    paths: dict[Path, None] = {root: None}
    raw = _get(result.data, "worktrees") if result is not None else None
    for item in raw if isinstance(raw, list) else []:
        text = _get(item, "path")
        if isinstance(text, str) and text:
            try:
                paths[Path(text).resolve()] = None
            except (OSError, RuntimeError):
                continue
    return tuple(paths)


def collect(
    ctx: SweepContext, runs: tuple[str, ...], root: Path, budget: Budget
) -> SweepInput:
    """Gather every source into one ``SweepInput``; a failed source becomes an unscanned row."""
    started = _utcnow()
    runs = tuple(dict.fromkeys(runs))
    sources: list[SourceCoverage] = []
    version = read_orca_version()
    state = _OrcaState()
    orca_rows = _orca_reads(runs, budget, state, sources)

    ps_result: OrcaResult | None = None
    if state.available:
        ps_result = _call(budget, "worktree", "ps", "--json")
        if ps_result.kind == "ok":
            cut = _get(ps_result.data, "truncated") is True
            sources.append(
                SourceCoverage(
                    "orca worktree ps",
                    "read",
                    None,
                    "worktree list truncated" if cut else None,
                )
            )
        else:
            sources.append(
                SourceCoverage(
                    "orca worktree ps", "unscanned", None, _unscanned(ps_result.reason)
                )
            )
            if ps_result.kind == "unavailable":
                state.available = False
            ps_result = None
    else:
        sources.append(
            SourceCoverage("orca worktree ps", "unscanned", None, "orca unavailable")
        )

    paths = _worktree_paths(root.resolve(), ps_result)
    worktrees = []
    for path in paths:
        worktree, rows = _read_worktree(path, budget)
        worktrees.append(worktree)
        sources.extend(rows)

    contracts = _read_contracts(orca_rows, paths, started, sources, budget)
    transcripts = _read_transcripts(paths, sources, budget)
    state_dir = Path(
        os.environ.get("XDG_STATE_HOME") or (Path.home() / ".local" / "state")
    )
    tab_map, problem = _tab_map(state_dir)
    sources.append(
        SourceCoverage(
            "ccsession orca-tabs",
            "unscanned" if problem else f"{len(tab_map)} entries",
            None,
            problem,
        )
    )
    sources.append(SourceCoverage("remote hosts", "unknown", None, None))

    return SweepInput(
        orca_rows=tuple(orca_rows),
        contracts=contracts,
        transcripts=transcripts,
        tab_map=tab_map,
        worktrees=tuple(worktrees),
        sources=tuple(sources),
        orca_available=state.available,
        orca_binary=orca_binary(),
        orca_version=version,
        truncated=state.truncated,
        collected_start=started,
        collected_end=_utcnow(),
    )


def _read_contracts(
    rows: list[OrcaObservation],
    paths: tuple[Path, ...],
    now: datetime,
    sources: list[SourceCoverage],
    budget: Budget | None = None,
) -> tuple[ContractRecord, ...]:
    allowed = tuple(paths)
    loaded: dict[Path, tuple[ContractRecord | None, str | None]] = {}
    records: dict[Path, ContractRecord] = {}
    for obs in rows:
        for candidate in _contract_candidates(obs):
            name = f"contract {obs.dispatch}"
            try:
                if candidate not in loaded:
                    if not any(_inside(candidate, base) for base in allowed):
                        loaded[candidate] = (None, "outside root")
                    elif not candidate.exists():
                        loaded[candidate] = (
                            None,
                            "absent",
                        )  # not written yet: not a source
                    else:
                        loaded[candidate] = _contract(candidate, None, budget)
                record, reason = loaded[candidate]
                if reason == "absent":
                    continue
                if record is not None and record.mtime is not None:
                    records[candidate] = record
                    sources.append(
                        SourceCoverage(name, "read", _age(now, record.mtime), None)
                    )
                else:
                    sources.append(
                        SourceCoverage(
                            name, "unscanned", None, reason or "contract not readable"
                        )
                    )
            except (OSError, ValueError, OverflowError):
                # A contract that vanished or turned unreadable mid-sweep is one row.
                sources.append(
                    SourceCoverage(name, "unscanned", None, "contract not readable")
                )
    return tuple(records.values())


def _read_transcripts(
    paths: tuple[Path, ...],
    sources: list[SourceCoverage],
    budget: Budget | None = None,
) -> tuple[TranscriptTail, ...]:
    home = Path.home()
    tails: dict[Path, TranscriptTail] = {}
    for key in dict.fromkeys(_project_key(p) for p in paths):
        folder = home / ".claude" / "projects" / key
        name = f"claude project {key}"
        try:
            with os.scandir(folder) as scan:
                files = sorted(
                    e.name for e in scan if e.name.endswith(".jsonl") and e.is_file()
                )
        except FileNotFoundError:
            sources.append(SourceCoverage(name, "no folder", None, None))
            continue
        except OSError:
            sources.append(
                SourceCoverage(name, "unscanned", None, "project folder not readable")
            )
            continue
        sources.append(SourceCoverage(name, f"{len(files)} files", None, None))
        for file_name in files:
            path = folder / file_name
            tail, reason = _transcript(path, folder, budget)
            tails[path] = tail
            if reason is not None:  # only a problem gets its own row
                sources.append(
                    SourceCoverage(f"transcript {path}", "unscanned", None, reason)
                )
    return tuple(tails.values())
