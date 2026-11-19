"""Several orchestrators: the registry, the in-flight count and the routing (design 5.7 and 4.5 step 10).

There is one orchestrator per repository, and each holds at most
``max_in_flight`` issues (default 3). When a repository has more, the poll
starts another orchestrator for the same repository. The poll is the only
router (layer 1 of 5.7 point 4): it gives each issue to exactly one
orchestrator under ``.orchestrator/state.lock``, writes the dispatch entry
``pending`` with that orchestrator before anything is sent, and never routes
the same issue to another one.

Files under ``<orchestrator-repo>/.orchestrator/``:

* ``orchestrators.json``: the registry, written only by the poll (this module),
  ``{id: {repo, tag, created_at, status: active | ended, [tier, fallback_from]}}``.
* ``runs/<id>.json``: one file per orchestrator, written by it; the poll reads
  ``status`` (``active``, ``ending``, ``ended``) and ``run_id``.
* ``issues/<owner>__<repo>__<N>.json``: the per-issue state file of an
  orchestrator, read only (the poll never writes it); and
  ``issues/plan-<key>.<requested_at>.json``, the plan record of one plan
  request, also read only.

The poll counts what is in flight from those files and from its own store
(5.7 point 1). A file it cannot parse counts as in flight, so a damaged file can
only stop new routing, never cause an extra issue.
"""

from __future__ import annotations

import json
import os
import re
import time
from collections.abc import Callable, Iterable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path

from .predicates import (
    ORCHESTRATOR_ID_PATTERN,
    format_utc,
    issue_key,
    parse_utc,
    split_issue_key,
    valid_repo,
)
from .record import StoreDoc
from .repos import RepoEntry, ReposDoc

STATE_DIR = ".orchestrator"
REGISTRY_FILE = "orchestrators.json"
LOCK_FILE = "state.lock"
ISSUES_DIR = "issues"
RUNS_DIR = "runs"

ORCHESTRATOR_STATUSES = ("active", "ended")
RUN_STATUSES = ("active", "ending", "ended")
STATE_STATUSES = ("in_progress", "done", "skipped", "failed", "escalated")
PLAN_STATUSES = ("in_progress", "done", "failed")
OPEN_PLAN_REQUEST_STATES = ("pending", "woken", "acked")

_ENTRY_KEYS = frozenset({"repo", "tag", "created_at", "status"})
_OPTIONAL_KEYS = frozenset({"tier", "fallback_from"})
_TIER = re.compile(r"tier[0-9][a-z]?")
_PLAN_FILE = re.compile(r"plan-(?P<key>.+)\.(?P<at>[0-9]{8}T[0-9]{6}Z)\.json")
_MAX_FILE = 1024 * 1024


class RegistryError(Exception):
    """The registry is unreadable or malformed (the audit reason ``registry_invalid``)."""

    reason = "registry_invalid"


class StateLockBusy(Exception):
    """``.orchestrator/state.lock`` stayed held (an orchestrator in wave 9); retry next cycle."""


@dataclass(frozen=True)
class OrchEntry:
    """One orchestrator of the registry."""

    id: str
    repo: str
    tag: str
    created_at: datetime
    status: str
    tier: str | None = None
    fallback_from: str | None = None


Registry = dict[str, OrchEntry]


def tag_of(prefix: str, short: str, n: int) -> str:
    """The ccsession tag ``<prefix>-<short>-<n>`` (``orchestrator-ironclaude-1``)."""
    return f"{prefix}-{short}-{n}"


def orchestrator_id(short: str, n: int) -> str:
    """The id ``<short>-<n>``."""
    ident = f"{short}-{n}"
    if ORCHESTRATOR_ID_PATTERN.fullmatch(ident) is None:
        raise ValueError("invalid orchestrator id")
    return ident


def _orch_dir(orchestrator_repo: Path) -> Path:
    return Path(orchestrator_repo) / STATE_DIR


def _read_json(path: Path) -> object:
    with open(path, "rb") as handle:
        data = handle.read(_MAX_FILE + 1)
    if len(data) > _MAX_FILE:
        raise ValueError("file too large")
    return json.loads(data.decode("utf-8"))


def _atomic_write(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        try:
            os.write(fd, text.encode("ascii"))
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, path)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def load_registry(orchestrator_repo: Path) -> Registry:
    """Read ``orchestrators.json``. A missing file is an empty registry.

    Raises ``RegistryError`` for a file that is unreadable, is not a JSON
    object, or holds an entry that breaks its rules (the cycle stops with
    ``registry_invalid``, exit 2).
    """
    path = _orch_dir(orchestrator_repo) / REGISTRY_FILE
    try:
        raw = _read_json(path)
    except FileNotFoundError:
        return {}
    except (OSError, ValueError, RecursionError):
        raise RegistryError from None
    if not isinstance(raw, dict):
        raise RegistryError
    registry: Registry = {}
    for ident, entry in raw.items():
        if (
            not isinstance(ident, str)
            or ORCHESTRATOR_ID_PATTERN.fullmatch(ident) is None
            or not isinstance(entry, dict)
            or not _ENTRY_KEYS <= set(entry)
            or set(entry) - _ENTRY_KEYS - _OPTIONAL_KEYS
            or not valid_repo(entry["repo"])
            or not isinstance(entry["tag"], str)
            or entry["status"] not in ORCHESTRATOR_STATUSES
        ):
            raise RegistryError
        for key in _OPTIONAL_KEYS:
            if entry.get(key) is not None and (
                not isinstance(entry[key], str) or _TIER.fullmatch(entry[key]) is None
            ):
                raise RegistryError
        try:
            created = parse_utc(entry["created_at"])
        except ValueError:
            raise RegistryError from None
        registry[ident] = OrchEntry(
            id=ident,
            repo=entry["repo"],
            tag=entry["tag"],
            created_at=created,
            status=entry["status"],
            tier=entry.get("tier"),
            fallback_from=entry.get("fallback_from"),
        )
    return registry


def save_registry(orchestrator_repo: Path, registry: Mapping[str, OrchEntry]) -> None:
    """Write ``orchestrators.json`` atomically at 0600 (only the poll writes it).

    The caller holds ``state_lock``. Raises ``OSError`` when the write fails.
    """
    raw = {}
    for ident in sorted(registry):
        e = registry[ident]
        item = {
            "repo": e.repo,
            "tag": e.tag,
            "created_at": format_utc(e.created_at),
            "status": e.status,
        }
        if e.tier is not None:
            item["tier"] = e.tier
        if e.fallback_from is not None:
            item["fallback_from"] = e.fallback_from
        raw[ident] = item
    directory = _orch_dir(orchestrator_repo)
    os.makedirs(directory, mode=0o700, exist_ok=True)
    _atomic_write(
        directory / REGISTRY_FILE, json.dumps(raw, sort_keys=True, indent=2) + "\n"
    )


@contextmanager
def state_lock(
    orchestrator_repo: Path,
    wait_s: float = 5.0,
    *,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
) -> Iterator[None]:
    """Hold ``.orchestrator/state.lock`` while the poll routes and writes the wake files.

    Local file work only: nothing is sent while it is held. Waits up to
    ``wait_s`` seconds for an orchestrator that holds it in wave 9, then raises
    ``StateLockBusy`` (the cycle ends ``lock_held``, nothing written).
    """
    import fcntl  # not at module level: importing the package must work off Linux

    directory = _orch_dir(orchestrator_repo)
    os.makedirs(directory, mode=0o700, exist_ok=True)
    fd = os.open(
        directory / LOCK_FILE,
        os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o600,
    )
    try:
        end = monotonic() + wait_s
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if monotonic() >= end:
                    raise StateLockBusy from None
                sleep(0.2)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


# --- what the orchestrators wrote (read only) ---------------------------------------


@dataclass(frozen=True)
class RunInfo:
    """``runs/<id>.json``: ``status`` and ``run_id``; both None when the file is missing."""

    status: str | None
    run_id: str | None


def read_run(orchestrator_repo: Path, ident: str) -> RunInfo:
    """Read ``runs/<id>.json``. Missing (a first start) or unreadable gives ``RunInfo(None, None)``."""
    if ORCHESTRATOR_ID_PATTERN.fullmatch(ident) is None:
        return RunInfo(None, None)
    try:
        raw = _read_json(_orch_dir(orchestrator_repo) / RUNS_DIR / f"{ident}.json")
    except (OSError, ValueError, RecursionError):
        return RunInfo(None, None)
    if not isinstance(raw, dict):
        return RunInfo(None, None)
    status = raw.get("status") if raw.get("status") in RUN_STATUSES else None
    run_id = raw.get("run_id")
    ok = isinstance(run_id, str) and re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", run_id)
    return RunInfo(status, run_id if ok else None)


@dataclass(frozen=True)
class StateFile:
    """One per-issue state file: its status and orchestrator, or ``readable=False``."""

    repo: str
    number: int
    status: str | None
    orchestrator: str | None
    readable: bool

    @property
    def key(self) -> str:
        return issue_key(self.repo, self.number)


def _repo_number_of(stem: str) -> tuple[str, int] | None:
    head, sep, tail = stem.rpartition("__")
    owner, sep2, name = head.partition("__")
    if not sep or not sep2 or not tail.isdigit() or not owner or not name:
        return None
    repo = f"{owner}/{name}"
    try:
        return split_issue_key(f"{repo}#{int(tail)}")
    except ValueError:
        return None


def read_state_files(orchestrator_repo: Path) -> dict[str, StateFile]:
    """Every per-issue state file, by store key. Plan records and sub-folders are skipped.

    A file that cannot be parsed, or whose status is not a known one, is
    ``readable=False`` and counts as in flight.
    """
    directory = _orch_dir(orchestrator_repo) / ISSUES_DIR
    found: dict[str, StateFile] = {}
    try:
        names = sorted(os.listdir(directory))
    except OSError:
        return found
    for name in names:
        path = directory / name
        if (
            not name.endswith(".json")
            or _PLAN_FILE.fullmatch(name)
            or not path.is_file()
        ):
            continue
        parsed = _repo_number_of(name[: -len(".json")])
        if parsed is None:
            continue
        repo, number = parsed
        status: str | None = None
        orch: str | None = None
        readable = False
        try:
            raw = _read_json(path)
            if isinstance(raw, dict) and raw.get("status") in STATE_STATUSES:
                status, readable = raw["status"], True
                cand = raw.get("orchestrator")
                if isinstance(cand, str) and ORCHESTRATOR_ID_PATTERN.fullmatch(cand):
                    orch = cand
        except (OSError, ValueError, RecursionError):
            pass
        sf = StateFile(repo, number, status, orch, readable)
        found[sf.key] = sf
    return found


def plan_record_status(
    orchestrator_repo: Path, repo: str, number: int, requested_at: datetime
) -> str | None:
    """The status of the plan record of ONE request, or None when there is no such record.

    The name is built from the key and the ``requested_at`` of the open request;
    a final record of an earlier request of the same key is never read (4.11).
    A record that cannot be parsed reads as ``in_progress`` (it counts as in
    flight, like a damaged state file).
    """
    from .predicates import file_key

    name = (
        f"plan-{file_key(repo, number)}.{requested_at.strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    path = _orch_dir(orchestrator_repo) / ISSUES_DIR / name
    if not path.is_file():
        return None
    try:
        raw = _read_json(path)
    except (OSError, ValueError, RecursionError):
        return "in_progress"
    status = raw.get("status") if isinstance(raw, dict) else None
    return status if status in PLAN_STATUSES else "in_progress"


# --- the in-flight count (5.7 point 1) --------------------------------------------------


def in_flight(
    registry: Mapping[str, OrchEntry],
    doc: StoreDoc,
    state_files: Mapping[str, StateFile],
    plan_status: Callable[[str, int, datetime], str | None],
) -> dict[str, set[str]]:
    """Count what each orchestrator holds: ``{orchestrator id: set of store keys}``.

    A key is in the set of an orchestrator when (a) its state file is
    ``in_progress`` with that ``orchestrator`` (a file that cannot be parsed
    counts against every active orchestrator of its repository), (b) the poll's
    own entry for it is ``pending``, ``woken`` or ``unknown`` and no state file
    exists yet, or (c) it is an open plan request: the ``holds`` entry has a
    request in ``pending``, ``woken`` or ``acked`` whose plan record is not
    final. ``done``, ``skipped``, ``failed`` and ``escalated`` files do not count,
    and an ``escalated`` file that returns to ``in_progress`` counts again. A key
    is counted once.
    """
    counts: dict[str, set[str]] = {ident: set() for ident in registry}
    for key, sf in state_files.items():
        if sf.readable and sf.status != "in_progress":
            continue
        if sf.orchestrator is not None and sf.orchestrator in counts:
            counts[sf.orchestrator].add(key)
        elif not sf.readable or sf.status == "in_progress":
            for ident, orch in registry.items():
                if orch.repo == sf.repo and orch.status == "active":
                    counts[ident].add(key)
    for key, entry in doc.entries.items():
        if (
            entry.state in ("pending", "woken", "unknown")
            and entry.orchestrator in counts
            and key not in state_files
        ):
            counts[entry.orchestrator].add(key)  # type: ignore[index]
    for key, hold in doc.holds.items():
        if (
            hold.state != "held"  # the label was taken off by hand: the hold ended
            or hold.plan_requested_at is None
            or hold.plan_request not in OPEN_PLAN_REQUEST_STATES
            or hold.plan_request_orchestrator not in counts
        ):
            continue
        repo, number = split_issue_key(key)
        if plan_status(repo, number, hold.plan_requested_at) in ("done", "failed"):
            continue
        counts[hold.plan_request_orchestrator].add(key)  # type: ignore[index]
    return counts


# --- routing -------------------------------------------------------------------------


@dataclass(frozen=True)
class Routed:
    """One routing decision."""

    repo: str
    number: int
    orchestrator: str
    new: bool

    @property
    def key(self) -> str:
        return issue_key(self.repo, self.number)


def n_of(ident: str) -> int:
    return int(ident.rsplit("-", 1)[1])


def next_n(registry: Mapping[str, OrchEntry], short: str) -> int:
    """The smallest positive ``<n>`` not yet used for ``short`` in the registry (never reused)."""
    used = {n_of(i) for i in registry if i.rsplit("-", 1)[0] == short}
    n = 1
    while n in used:
        n += 1
    return n


def _usable(
    registry: Mapping[str, OrchEntry],
    repo: str,
    run_status: Callable[[str], str | None],
) -> list[OrchEntry]:
    """The repo's ``active`` orchestrators whose run is not ``ending`` or ``ended``, in id order."""
    return sorted(
        (
            e
            for e in registry.values()
            if e.repo.lower() == repo.lower()
            and e.status == "active"
            and run_status(e.id) not in ("ending", "ended")
        ),
        key=lambda e: n_of(e.id),
    )


def _new_orchestrator(
    registry: Registry, entry: RepoEntry, prefix: str, now: datetime
) -> OrchEntry:
    n = next_n(registry, entry.short)
    ident = orchestrator_id(entry.short, n)
    made = OrchEntry(ident, entry.repo, tag_of(prefix, entry.short, n), now, "active")
    registry[ident] = made
    return made


def route(
    registry: Registry,
    counts: dict[str, set[str]],
    items: Iterable[tuple[str, int]],
    rdoc: ReposDoc,
    prefix: str,
    now: datetime,
    run_status: Callable[[str], str | None],
    *,
    plan_requests: bool = False,
) -> list[Routed | tuple[str, int]]:
    """Give each ``(repo, number)`` to an orchestrator of its repository (5.7 point 3).

    ``registry`` and ``counts`` are changed in place (a routed issue counts
    against the cap in the same cycle). Items go in the order given (the cycle
    passes repo, then number). An assignment goes to the first ``active``
    orchestrator below ``max_in_flight``, or to a new ``<short>-<n>`` (an id is
    never reused). With ``plan_requests`` the items are plan requests: they go
    only to an active orchestrator with a free place, and a new orchestrator is
    made only when the repository has no active one at all; an item that finds no
    place is returned as the bare ``(repo, number)`` and nothing is sent for it.
    """
    out: list[Routed | tuple[str, int]] = []
    for repo, number in items:
        entry = rdoc.get(repo)
        if entry is None:
            out.append((repo, number))
            continue
        key = issue_key(repo, number)
        usable = _usable(registry, repo, run_status)
        chosen = next(
            (
                e
                for e in usable
                if len(counts.setdefault(e.id, set())) < entry.max_in_flight
            ),
            None,
        )
        new = False
        if chosen is None:
            if plan_requests and usable:
                out.append((repo, number))
                continue
            chosen = _new_orchestrator(registry, entry, prefix, now)
            new = True
        counts.setdefault(chosen.id, set()).add(key)
        out.append(Routed(repo, number, chosen.id, new))
    return out


def end_finished(
    registry: Registry,
    counts: Mapping[str, set[str]],
    in_progress: set[str],
    run_status: Callable[[str], str | None],
    has_session: Callable[[OrchEntry], bool | None],
) -> tuple[list[str], list[str]]:
    """The dead-orchestrator check and the lifecycle (5.7 point 5).

    Returns ``(ended, resume)`` and marks the ``ended`` ones in ``registry``:

    * an ``active`` entry whose ``runs/<id>.json`` says ``ended`` is marked ``ended``;
    * one with no live session (``has_session`` False) and nothing in flight is
      marked ``ended`` and is not started;
    * one with no live session and an ``in_progress`` state file (its id is in
      ``in_progress``) is returned in ``resume``: the poll starts it again with
      the same tag and sends it a ``target.resume`` wake;
    * one with no live session and only unacknowledged wakes or plan requests
      in flight is left alone: the resend of those starts the session.

    ``has_session`` None (the terminal list could not be read) decides nothing.
    ``counts`` is the in-flight count of ``in_flight``.
    """
    ended: list[str] = []
    resume: list[str] = []
    for ident in sorted(registry, key=lambda i: (registry[i].repo, n_of(i))):
        entry = registry[ident]
        if entry.status != "active":
            continue
        if run_status(ident) == "ended":
            registry[ident] = replace(entry, status="ended")
            ended.append(ident)
            continue
        alive = has_session(entry)
        if alive is None or alive:
            continue
        if ident in in_progress:
            resume.append(ident)
        elif not counts.get(ident):
            registry[ident] = replace(entry, status="ended")
            ended.append(ident)
    return ended, resume
