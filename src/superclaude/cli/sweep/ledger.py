"""Run ledger: which Orca Runs ``superclaude sweep run`` should read (issue #895).

Orca keeps every Run for ever and has no open/settled status, so a deterministic
rebuild (no model) decides which Runs are still worth sweeping and writes them to one
JSON file. This module holds the pure inclusion rules (``decide``), the Orca reader and
guards, the file store, and the ``sweep ledger`` click command.
"""

from __future__ import annotations

import contextlib
import fcntl  # shortcut: fcntl is Linux and macOS only, add msvcrt locking if Windows is ever needed
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections.abc import Callable, Iterator
from datetime import datetime, timedelta, timezone
from pathlib import Path

import click

from .probes import RUN_ID_RE, parse_time

TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled"})
NEW_FALLBACK_HOURS = 24
STALE_TASK_DAYS = 7
LEGACY_RUN_ID = "run_legacy_local"
LEDGER_VERSION = 1
LEDGER_STALE_MINUTES = (
    90  # three missed 30-minute builds; the sweep header then says so
)
_OBJECTIVE_CHARS = 120
_STALE_STATUSES = frozenset({"ready", "blocked"})

# shortcut: no age cutoff and no main-checkout exclusion (over-inclusion is the safe
# direction), add one only if the owner decides
#
# Time rule: every comparison parses both sides with ``parse_time`` (Orca emits the SQLite
# form "2026-11-26 18:12:55" and the ISO form "2026-11-26T18:12:41Z"). A value that does
# not parse is treated as "not new, not recent, not stale"; it never raises.
#
# Task timestamp: a real ``orca orchestration task-list --run <id> --json`` row has the keys
# id, run_id, status, created_at, completed_at, dispatch_id, ... and no ``updated_at``, so
# the stale test below uses the Task's own ``created_at`` (SQLite form).


def iso_utc(value: datetime) -> str:
    """``YYYY-MM-DDTHH:MM:SSZ`` for an aware datetime."""
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _as_dt(value: object) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return parse_time(value)


def _is_legacy(run: dict) -> bool:
    return bool(run.get("legacy")) or run.get("id") == LEGACY_RUN_ID


def _live_ids(workers: list, live_ids: set[str]) -> list[str]:
    """Worker ``resource.worktreeId`` values that equal a listed worktree id, in first-seen order."""
    seen: list[str] = []
    for worker in workers:
        resource = worker.get("resource") if isinstance(worker, dict) else None
        wid = resource.get("worktreeId") if isinstance(resource, dict) else None
        if isinstance(wid, str) and wid in live_ids and wid not in seen:
            seen.append(wid)
    return seen


def _stale_flag(
    reasons: list[str], unfinished: list[dict], generated: datetime
) -> bool | None:
    """True/False/None for ``stale_open_tasks_only`` (None: the Tasks carry no usable timestamp)."""
    if reasons != ["unfinished_task"]:
        return False
    if any(task.get("status") not in _STALE_STATUSES for task in unfinished):
        return False
    cutoff = generated - timedelta(days=STALE_TASK_DAYS)
    stamps = [_as_dt(task.get("created_at")) for task in unfinished]
    if any(stamp is None for stamp in stamps):
        return None
    return all(stamp < cutoff for stamp in stamps)  # type: ignore[operator]


def decide(
    runs: list,
    workers_by_run: dict,
    tasks_by_run: dict,
    live_worktrees: list,
    previous: dict | None,
    generated_at: datetime | str,
) -> tuple[list[dict], dict]:
    """Pure inclusion rules: ``(ledger run entries, counts block)``. No I/O.

    ``live_worktrees`` are the ``worktree list --json`` rows (``id``, ``isMainWorktree``).
    A Run missing from ``workers_by_run`` or ``tasks_by_run`` has no rows there.
    """
    generated = _as_dt(generated_at)
    if generated is None:
        raise ValueError(f"generated_at is not a usable time: {generated_at!r}")
    live = {w["id"]: bool(w.get("isMainWorktree")) for w in live_worktrees if "id" in w}
    prev_time = (
        _as_dt(previous.get("generated_at")) if isinstance(previous, dict) else None
    )
    new_since = prev_time or generated - timedelta(hours=NEW_FALLBACK_HOURS)

    entries: list[dict] = []
    for run in runs:
        if _is_legacy(run):
            continue
        run_id = run["id"]
        tasks = tasks_by_run.get(run_id) or []
        unfinished = [t for t in tasks if t.get("status") not in TERMINAL_STATUSES]
        created = _as_dt(run.get("created_at"))
        matched = _live_ids(workers_by_run.get(run_id) or [], set(live))

        reasons: list[str] = []
        if matched:
            reasons.append("live_worktree")
        if unfinished:
            reasons.append("unfinished_task")
        if created is not None and created >= new_since:
            reasons.append("new")
        if not reasons:
            continue
        entries.append(
            {
                "id": run_id,
                "created_at": run.get("created_at"),
                "objective": str(run.get("objective") or "")[:_OBJECTIVE_CHARS],
                "reasons": reasons,
                "source": "build",
                "added_at": iso_utc(generated),
                "live_worktree_ids": matched,
                "unfinished_task_count": len(unfinished),
                "main_checkout_only": reasons == ["live_worktree"]
                and all(live[w] for w in matched),
                "stale_open_tasks_only": _stale_flag(reasons, unfinished, generated),
                # held in only by `blocked` Tasks (reported, changes no rule)
                "blocked_only": reasons == ["unfinished_task"]
                and all(t.get("status") == "blocked" for t in unfinished),
            }
        )
    return entries, compute_counts(entries)


def compute_counts(entries: list[dict]) -> dict:
    """The ``counts`` block, derived from the entries alone (so a merge can recompute it)."""
    counts = {
        "live_worktree": 0,
        "unfinished_task": 0,
        "new": 0,
        "hook_added": 0,
        "main_checkout_only": 0,
        "open_task_stale_7d_only": 0,
        "blocked_only": 0,
    }
    for entry in entries:
        for reason in entry.get("reasons", []):
            if reason in counts:
                counts[reason] += 1
        counts["main_checkout_only"] += bool(entry.get("main_checkout_only"))
        counts["open_task_stale_7d_only"] += entry.get("stale_open_tasks_only") is True
        counts["blocked_only"] += bool(entry.get("blocked_only"))
    return counts


# --- Orca reader and implausible-result guards ------------------------------------------

ORCA_TIMEOUT_SECONDS = 30
WORKER_PAGE_LIMIT = 100
MAX_WORKER_PAGES = 50
_ORCA_HINT = "orca not found or Orca app not running"

# A runner takes the argv after the binary name and returns ``(returncode, stdout)``.
Runner = Callable[[list[str]], "tuple[int, str]"]


class OrcaFailure(Exception):
    """An Orca call failed; the message starts ``orca-failure:``."""


class Implausible(Exception):
    """The result looks like a broken read; the message starts ``implausible:``."""


def orca_runner(args: list[str]) -> tuple[int, str]:
    """Run ``orca <args>`` with a fixed argv, no shell and a 30 s timeout.

    Resolved with ``shutil.which`` (an absolute path only). ``find_orca`` of
    ``cli/issue_watch/launch.py`` is not reused: it needs that package's Runner object and
    an extra ``orca skills list --json`` probe.
    """
    binary = shutil.which("orca")
    if binary is None:
        raise FileNotFoundError("orca")
    proc = subprocess.run(
        [binary, *args],
        capture_output=True,
        text=True,
        timeout=ORCA_TIMEOUT_SECONDS,
        check=False,
    )
    return proc.returncode, proc.stdout


def _call(runner: Runner, args: list[str]) -> dict:
    """One Orca call; returns ``result`` of an ``"ok": true`` reply, else raises ``OrcaFailure``."""
    shown = "orca " + " ".join(args)
    try:
        code, out = runner(args)
    except FileNotFoundError:
        raise OrcaFailure(f"orca-failure: {_ORCA_HINT}") from None
    except subprocess.TimeoutExpired:
        raise OrcaFailure(
            f"orca-failure: `{shown}` timed out after {ORCA_TIMEOUT_SECONDS} s"
        ) from None
    if code != 0:
        raise OrcaFailure(f"orca-failure: `{shown}` exited {code} ({_ORCA_HINT}?)")
    try:
        data = json.loads(out)
    except ValueError:
        raise OrcaFailure(f"orca-failure: `{shown}` did not return JSON") from None
    if not isinstance(data, dict) or data.get("ok") is not True:
        raise OrcaFailure(f"orca-failure: `{shown}` did not return ok=true")
    result = data.get("result")
    if not isinstance(result, dict):
        raise OrcaFailure(f"orca-failure: `{shown}` returned no result object")
    return result


def _list_field(result: dict, key: str, shown: str) -> list:
    rows = result.get(key)
    if not isinstance(rows, list):
        raise OrcaFailure(f"orca-failure: `{shown}` returned no `{key}` list")
    return rows


def _fetch_workers(runner: Runner, run_id: str) -> list:
    """All worker rows of a Run, paging ``worker-list`` by ``result.page``."""
    workers: list = []
    seen: set[str] = set()
    cursor: str | None = None
    for _ in range(MAX_WORKER_PAGES):
        args = [
            "orchestration",
            "worker-list",
            "--run",
            run_id,
            "--json",
            "--limit",
            str(WORKER_PAGE_LIMIT),
        ]
        if cursor is not None:
            args += ["--cursor", cursor]
        result = _call(runner, args)
        workers += _list_field(result, "workers", "worker-list")
        page = result.get("page")
        if not (isinstance(page, dict) and page.get("hasMore") is True):
            return workers
        cursor = page.get("nextCursor")
        if not isinstance(cursor, str) or cursor in seen:
            raise OrcaFailure(
                f"orca-failure: worker-list for {run_id} repeated or lost its cursor"
            )
        seen.add(cursor)
    raise OrcaFailure(
        f"orca-failure: worker-list for {run_id} needed more than {MAX_WORKER_PAGES} pages"
    )


def _recent_non_legacy(runs: list, generated: datetime) -> bool:
    """A non-legacy Run created or updated within the last 24 h (unparseable times never count)."""
    cutoff = generated - timedelta(hours=NEW_FALLBACK_HOURS)
    for run in runs:
        if _is_legacy(run):
            continue
        for key in ("created_at", "updated_at"):
            stamp = parse_time(run.get(key))
            if stamp is not None and stamp >= cutoff:
                return True
    return False


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def build_ledger(
    runner: Runner,
    previous: dict | None,
    now: Callable[[], datetime] = utc_now,
    accept_empty: bool = False,
) -> dict:
    """Read Orca and return the whole new ledger in memory; nothing is written here.

    ``generated_at`` is taken from ``now()`` before the first Orca call, so a Run created
    mid-build is never missed by the ``new`` rule. Calls only ``run-list``, ``worktree list``,
    ``task-list`` and ``worker-list`` (never through ``probes``). Raises ``OrcaFailure`` or
    ``Implausible``; ``accept_empty`` bypasses only the zero-included guard.
    """
    generated = now()
    runs = _list_field(
        _call(runner, ["orchestration", "run-list", "--json"]), "runs", "run-list"
    )
    worktrees = _list_field(
        _call(runner, ["worktree", "list", "--json"]), "worktrees", "worktree list"
    )
    if not worktrees:
        raise Implausible(
            "implausible: `worktree list` returned 0 worktrees (the main checkout always exists)"
        )
    if not runs and previous is not None:
        raise Implausible(
            "implausible: `run-list` returned 0 Runs while a previous ledger exists"
        )

    candidates = [run for run in runs if not _is_legacy(run)]
    tasks_by_run = {
        run["id"]: _list_field(
            _call(runner, ["orchestration", "task-list", "--run", run["id"], "--json"]),
            "tasks",
            "task-list",
        )
        for run in candidates
    }
    # Short-circuit: workers are fetched only for Runs not already IN by Task or `new`.
    already_in = {
        e["id"]
        for e in decide(candidates, {}, tasks_by_run, worktrees, previous, generated)[0]
    }
    workers_by_run = {
        run["id"]: _fetch_workers(runner, run["id"])
        for run in candidates
        if run["id"] not in already_in
    }
    entries, counts = decide(
        candidates, workers_by_run, tasks_by_run, worktrees, previous, generated
    )

    had_runs = isinstance(previous, dict) and bool(previous.get("runs"))
    if (
        not entries
        and had_runs
        and _recent_non_legacy(candidates, generated)
        and not accept_empty
    ):
        raise Implausible(
            "implausible: 0 Runs would be kept, the previous ledger had some and a Run is under 24 h old "
            "(pass --accept-empty if that is right)"
        )
    return {
        "version": LEDGER_VERSION,
        "generated_at": iso_utc(generated),
        "orca": {"runs_listed": len(runs), "worktrees_listed": len(worktrees)},
        "counts": counts,
        "runs": entries,
    }


# shortcut: a partial read that returns a plausible non-empty list is not caught, add a
# shrink guard if one is ever seen


# --- File store: path, read, lock, atomic write, hook merge, --add ----------------------

LEDGER_ENV = "SUPERCLAUDE_RUN_LEDGER"
LEDGER_NAME = "run-ledger.json"
LOCK_NAME = "run-ledger.lock"
LOCK_TIMEOUT_SECONDS = 10


class LockTimeout(Exception):
    """The ledger lock was not free within the timeout."""


class LedgerUnavailable(Exception):
    """``--add`` needs a readable ledger and there is none."""


def ledger_path(cli_value: str | os.PathLike | None = None) -> Path:
    """``--ledger`` value, else ``SUPERCLAUDE_RUN_LEDGER``, else the XDG state folder (never the repo)."""
    chosen = cli_value or os.environ.get(LEDGER_ENV)
    if chosen:
        return Path(chosen).expanduser()
    state = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(state) / "superclaude" / LEDGER_NAME


def read_ledger(path: Path) -> dict | None:
    """The parsed ledger, or None when it is missing, not JSON, not version 1 or holds a bad id.

    Each id must ``re.fullmatch(RUN_ID_RE, id)`` (a trailing-junk id makes the whole file
    unreadable, as one bad id means a damaged file); duplicate ids collapse, first seen wins.
    """
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("version") != LEDGER_VERSION:
        return None
    if not isinstance(data.get("generated_at"), str) or not isinstance(
        data.get("runs"), list
    ):
        return None
    unique: dict[str, dict] = {}
    for entry in data["runs"]:
        run_id = entry.get("id") if isinstance(entry, dict) else None
        if not isinstance(run_id, str) or re.fullmatch(RUN_ID_RE, run_id) is None:
            return None
        unique.setdefault(run_id, entry)
    return {**data, "runs": list(unique.values())}


@contextlib.contextmanager
def locked(path: Path, timeout: float = LOCK_TIMEOUT_SECONDS) -> Iterator[None]:
    """Exclusive ``flock`` on the sidecar ``run-ledger.lock``; ``LockTimeout`` after ``timeout`` s."""
    lock_file = Path(path).parent / LOCK_NAME
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_file, "a") as handle:
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise LockTimeout(
                        f"lock {lock_file} not free within {timeout} s"
                    ) from None
                time.sleep(0.05)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def write_atomic(path: Path, data: dict) -> None:
    """Temp file in the same folder, ``fsync``, ``os.replace``; the temp file never survives a failure."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=1)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def merge_hook_entries(
    new_ledger: dict, current_ledger: dict | None, generated_at: datetime
) -> dict:
    """``new_ledger`` plus every hook entry of ``current_ledger`` added since the rebuild started.

    A current entry is kept when ``source == "hook"`` and its ``added_at`` is at or after
    ``generated_at`` (both parsed with ``parse_time``; an unparseable ``added_at`` is not kept,
    and ``generated_at`` is cut to whole seconds, the precision ``added_at`` has). Same id as a
    build row: the build row keeps its fields and gains the ``hook_added`` reason. ``counts`` is
    recomputed. Neither input is changed.
    """
    cutoff = parse_time(iso_utc(generated_at))
    runs = [
        dict(entry, reasons=list(entry.get("reasons", [])))
        for entry in new_ledger["runs"]
    ]
    by_id = {entry["id"]: entry for entry in runs}
    for entry in (current_ledger or {}).get("runs", []):
        if entry.get("source") != "hook":
            continue
        added = parse_time(entry.get("added_at"))
        if added is None or cutoff is None or added < cutoff:
            continue
        existing = by_id.get(entry["id"])
        if existing is None:
            runs.append(dict(entry, reasons=list(entry.get("reasons", ["hook_added"]))))
            by_id[entry["id"]] = runs[-1]
        elif "hook_added" not in existing["reasons"]:
            existing["reasons"].append("hook_added")
    return {**new_ledger, "runs": runs, "counts": compute_counts(runs)}


def add_run(path: Path, run_id: str, now: datetime | None = None) -> bool:
    """Append ``run_id`` as a hook entry; True if added, False if already present. No Orca call.

    Takes the lock, keeps ``generated_at`` unchanged (so sweep staleness is not masked) and
    raises ``ValueError`` for a malformed id and ``LedgerUnavailable`` for a missing or
    unreadable ledger.
    """
    if re.fullmatch(RUN_ID_RE, run_id) is None:
        raise ValueError(f"invalid Run id: {run_id!r}")
    with locked(path):
        data = read_ledger(path)
        if data is None:
            raise LedgerUnavailable(f"no readable ledger at {path}")
        if any(entry["id"] == run_id for entry in data["runs"]):
            return False
        data["runs"].append(
            {
                "id": run_id,
                "source": "hook",
                "reasons": ["hook_added"],
                "added_at": iso_utc(now or utc_now()),
            }
        )
        data["counts"] = compute_counts(data["runs"])
        write_atomic(path, data)
    return True


# --- The ``superclaude sweep ledger`` command ------------------------------------------

EXIT_FAILURE = 1  # OrcaFailure, Implausible, or --add with no readable ledger
EXIT_LOCK = 3  # LockTimeout (usage errors exit 2 through click)


def _fail(message: str, code: int) -> None:
    click.echo(message, err=True)
    sys.exit(code)


def _summary(path: Path, data: dict, written: bool) -> str:
    counts, orca = data["counts"], data["orca"]
    reasons = " ".join(
        f"{k}={counts[k]}"
        for k in ("live_worktree", "unfinished_task", "new", "hook_added")
    )
    return "\n".join(
        [
            f"run ledger {'written' if written else 'dry run, nothing written'}: {path}",
            f"generated_at: {data['generated_at']}  Runs kept: {len(data['runs'])} "
            f"of {orca['runs_listed']} listed ({orca['worktrees_listed']} worktrees)",
            f"reasons: {reasons}",
            f"admitted only through the main checkout: {counts['main_checkout_only']}",
            f"admitted only by ready or blocked Tasks older than {STALE_TASK_DAYS} days: "
            f"{counts['open_task_stale_7d_only']}",
            f"held in only by blocked Tasks: {counts['blocked_only']}",
        ]
    )


@click.command("ledger")
@click.option(
    "--ledger",
    "ledger_opt",
    default=None,
    help="Ledger file (default: see the user guide).",
)
@click.option(
    "--dry-run", is_flag=True, help="Build and print the ledger; write nothing."
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Print one JSON object instead of the summary.",
)
@click.option(
    "--accept-empty",
    is_flag=True,
    help="Allow a ledger with 0 Runs (overrides one guard only).",
)
@click.option(
    "--add",
    "add_id",
    default=None,
    help="Append one Run id to the ledger; no Orca call.",
)
def ledger_command(ledger_opt, dry_run, as_json, accept_empty, add_id):
    """Rebuild the Run ledger that `superclaude sweep run` reads, or append one Run to it."""
    path = ledger_path(ledger_opt)
    if add_id is not None:
        if dry_run or accept_empty:
            raise click.UsageError(
                "--add cannot be combined with --dry-run or --accept-empty"
            )
        try:
            added = add_run(path, add_id)
        except ValueError as exc:
            raise click.UsageError(str(exc)) from None
        except LedgerUnavailable as exc:
            _fail(
                f"implausible: {exc}; run `superclaude sweep ledger` first",
                EXIT_FAILURE,
            )
        except LockTimeout as exc:
            _fail(f"lock-timeout: {exc}", EXIT_LOCK)
        click.echo(f"{add_id} {'added' if added else 'already in the ledger'}")
        return
    try:
        new = build_ledger(orca_runner, read_ledger(path), accept_empty=accept_empty)
    except (OrcaFailure, Implausible) as exc:
        _fail(str(exc), EXIT_FAILURE)
    generated = parse_time(new["generated_at"])
    try:
        if dry_run:
            merged = merge_hook_entries(new, read_ledger(path), generated)
        else:
            with locked(path):
                merged = merge_hook_entries(new, read_ledger(path), generated)
                write_atomic(path, merged)
    except LockTimeout as exc:
        _fail(f"lock-timeout: {exc}", EXIT_LOCK)
    if as_json:
        click.echo(
            json.dumps(
                {"path": str(path), "written": not dry_run, "ledger": merged}, indent=1
            )
        )
    else:
        click.echo(_summary(path, merged, written=not dry_run))
        if dry_run:
            click.echo("Runs: " + " ".join(r["id"] for r in merged["runs"]))


def source_line(data: dict, now: datetime) -> str:
    """Sweep header line saying the Run ids came from the ledger, plus its age when it is stale.

    ``generated_at`` that does not parse (``parse_time`` gives None) adds no age and never raises.
    """
    text = f"Run ids from the Run ledger built {data['generated_at']}"
    built = parse_time(data["generated_at"])
    if built is not None and now - built > timedelta(minutes=LEDGER_STALE_MINUTES):
        text += f" . ledger is {int((now - built).total_seconds() // 60)} min old"
    return text
