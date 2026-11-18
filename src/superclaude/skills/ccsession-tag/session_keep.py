#!/usr/bin/env python3
"""Sessions already saved: tell agent-saved ones from a person's, and keep them
for different times (ccsession --classify and --prune).

A saved session is a name file <list>/<name>.txt whose first line is the session
id, in a list folder ~/.claude/projects/<key>/topics. Who chose the name is a
marker file <list>/.origin/<session id> holding one line, "human" or "agent"
(written by ccsession's hook and by ccsession --mark). A session with no marker is
unmarked and counts as a person's everywhere: it is listed and never pruned.

    session_keep.py classify [--apply] <projects-dir>
        Mark as "agent" the unmarked sessions whose every saved name, in every
        list, ends in the stamp --auto-name adds (-MMDD-HHMMSS-xxxx, with an
        optional -N). A session with a "human" marker, or with any other name in
        any list (a person's rename), is left alone, and so is every marker that
        exists. Without --apply nothing is written.

    session_keep.py prune [--apply] [--days N] <projects-dir> <home> <orca-dir>
        Delete the sessions an agent saved that have not changed in more than N
        days (default CCSESSION_AGENT_KEEP_DAYS, else 30; a whole number of at
        least 30), with their transcripts, session folders, file history, names,
        marker and Orca tab record, and the names, markers and tab records whose
        conversation is already gone. A session saved in any list without an
        "agent" marker, an unmarked or human one, is never touched. Without
        --apply it only lists what it would delete and writes nothing.

    session_keep.py hint <projects-dir> <home>
        Print one line when agent sessions are past the days above, else
        nothing. Read-only; never fails (ccsession --list and --here call it).

The functions take every path and value as an argument and keep no state, so a
caller (the command line below, or a later automatic run) uses them unchanged.
Standard library only; Python 3.10.
"""

from __future__ import annotations

import contextlib
import fcntl
import importlib.util
import os
import re
import shutil
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Mapping, NamedTuple

LOCK = ".ccsession-lock"  # the file ccsession's shell code flocks (lock_list)
ORIGIN = ".origin"  # <list>/.origin/<session id>
LOCK_WAIT = 4.0  # seconds, as lock_list waits
VALUES = ("human", "agent")
SESSION_ID = re.compile(r"[A-Za-z0-9_-]+\Z")  # what ccsession accepts as an id
# What `ccsession --auto-name` ends a label with: month day, time with seconds, four
# lowercase hex digits; "-N" is added when the label was already taken.
AUTO_STAMP = re.compile(r"-[0-9]{4}-[0-9]{6}-[0-9a-f]{4}(?:-[0-9]+)?\Z")

DAY = 86400
AGENT_FLOOR_DAYS = 30  # no value can make --prune delete a younger session
CLAUDE_DEFAULT_DAYS = 30  # Claude Code's own limit when no file sets one
GRACE = 2 * DAY  # a name, marker or tab record this young is never called stale
KEEP_ENV = "CCSESSION_AGENT_KEEP_DAYS"


class Busy(Exception):
    """A list's lock could not be taken in LOCK_WAIT seconds."""


class NameFile(NamedTuple):
    list_dir: Path
    path: Path
    name: str
    session: str


def file_to_name(stem: str) -> str:
    """ccsession's file_to_name: %2E at the start is ".", then %2F is "/", %25 is "%"."""
    if stem.startswith("%2E"):
        stem = "." + stem[3:]
    return stem.replace("%2F", "/").replace("%25", "%")


def auto_shaped(name: str) -> bool:
    """True only for a label that ends in an exact --auto-name stamp."""
    return AUTO_STAMP.search(name) is not None


def is_session_id(value: str) -> bool:
    return SESSION_ID.match(value) is not None


class Listing(list):
    """The lists found. `complete` is False when a folder could not be read, so a
    list (and a human marker in it) may be missing from it."""

    complete: bool = True


def lists(projects_dir: Path) -> Listing:
    """Every <projects-dir>/<key>/topics folder, the old per-folder lists included.

    A hidden key and a symlinked folder are not lists.
    """
    found = Listing()
    try:
        keys = sorted(os.scandir(projects_dir), key=lambda e: e.name)
    except OSError:
        found.complete = False
        return found
    for key in keys:
        topics = Path(key.path) / "topics"
        try:
            if key.name.startswith(".") or key.is_symlink():
                continue
            if topics.is_dir() and not topics.is_symlink():
                found.append(topics)
        except OSError:  # a folder that cannot be read may hold a list
            found.complete = False
    return found


def first_line(path: Path) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.readline().rstrip("\r\n")
    except OSError:
        return ""


def names(list_dir: Path) -> list[NameFile]:
    """The saved names of one list: a regular <name>.txt whose first line is a session id."""
    found = []
    try:
        entries = sorted(os.scandir(list_dir), key=lambda e: e.name)
    except OSError:
        return []
    for entry in entries:
        if (
            entry.name.startswith(".")
            or not entry.name.endswith(".txt")
            or entry.is_symlink()
            or not entry.is_file()
        ):
            continue
        session = first_line(Path(entry.path))
        if is_session_id(session):
            found.append(
                NameFile(
                    list_dir,
                    Path(entry.path),
                    file_to_name(entry.name[: -len(".txt")]),
                    session,
                )
            )
    return found


def marker(list_dir: Path, session: str) -> str:
    """ "human", "agent" or "" (unmarked, or a file that holds anything else)."""
    if not is_session_id(session):
        return ""
    value = first_line(list_dir / ORIGIN / session)
    return value if value in VALUES else ""


@contextlib.contextmanager
def locked(list_dir: Path) -> Iterator[None]:
    """Hold the list's flock (the one ccsession's shell code takes) for the block."""
    path = list_dir / LOCK
    if path.is_dir():  # an old build's empty lock folder: the shell code removes it
        raise Busy(str(list_dir))
    try:
        fd = os.open(
            path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o600
        )
    except OSError as exc:
        raise Busy(str(list_dir)) from exc
    try:
        end = time.monotonic() + LOCK_WAIT
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() > end:
                    raise Busy(str(list_dir)) from None
                time.sleep(0.02)
        yield
    finally:
        os.close(fd)  # closing releases the lock


def write_marker(list_dir: Path, session: str, value: str) -> None:
    """Replace the marker atomically; the caller holds the list's lock."""
    if value not in VALUES or not is_session_id(session):
        raise ValueError("not a marker: %r %r" % (session, value))
    folder = list_dir / ORIGIN
    if folder.is_symlink():
        raise OSError("%s is a symlink" % folder)
    folder.mkdir(exist_ok=True)
    fd, staged = tempfile.mkstemp(dir=folder, prefix=".ccsession-origin.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(value + "\n")
        os.replace(staged, folder / session)
    finally:
        if os.path.exists(staged):
            os.unlink(staged)


def key_of(folder: Path) -> str:
    return folder.parent.name


def by_session(projects_dir: Path) -> dict[str, list[NameFile]]:
    found: dict[str, list[NameFile]] = {}
    for folder in lists(projects_dir):
        for row in names(folder):
            found.setdefault(row.session, []).append(row)
    return found


# --- classify ------------------------------------------------------------------


@dataclass
class Classified:
    auto_shaped: int = 0  # sessions marked agent, or that would be
    left_unmarked: int = 0  # sessions with an unmarked copy that are not auto-named
    already_marked: int = 0  # sessions with a marker in every list that names them
    would_mark: list[tuple[Path, str, str]] = field(default_factory=list)
    marked: int = 0  # markers written (apply only)
    skipped: list[str] = field(default_factory=list)  # a list that could not be written


def classify(projects_dir: Path, apply: bool = False) -> Classified:
    """Mark as agent the unmarked sessions whose every name is an exact auto-name.

    A session is marked only when every name saved for it, in every list, is
    auto-shaped and no list holds a human marker for it. A marker that exists is
    never changed and a name never is. Nothing is written unless apply is true.
    """
    result = Classified()
    for session, rows in sorted(by_session(projects_dir).items()):
        marks = {row.list_dir: marker(row.list_dir, session) for row in rows}
        pending = sorted(folder for folder, mark in marks.items() if not mark)
        if not pending:
            result.already_marked += 1
            continue
        if "human" in marks.values() or not all(auto_shaped(r.name) for r in rows):
            result.left_unmarked += 1
            continue
        result.auto_shaped += 1
        for folder in pending:
            name = next(r.name for r in rows if r.list_dir == folder)
            result.would_mark.append((folder, name, session))
    if apply:
        for folder, name, session in result.would_mark:
            try:
                with locked(folder):
                    if marker(folder, session):  # someone marked it meanwhile
                        continue
                    write_marker(folder, session, "agent")
                result.marked += 1
            except (Busy, OSError) as exc:
                result.skipped.append("%s: %s" % (folder, exc))
    return result


def print_classify(result: Classified, apply: bool) -> None:
    done = "Marked agent" if apply else "Would mark agent"
    count = result.marked if apply else len(result.would_mark)
    print("%s: %d session name%s" % (done, count, "" if count == 1 else "s"))
    print(
        "Auto-named sessions: %d. Left unmarked (a name a person gave, or not an "
        "auto-name): %d. Already marked: %d."
        % (result.auto_shaped, result.left_unmarked, result.already_marked)
    )
    for folder, name, _ in result.would_mark:
        print("  %s  (%s)" % (name, key_of(folder)))
    for line in result.skipped:
        print("Skipped %s" % line)
    if not apply:
        print("Dry run: nothing was written. Run with --apply to write the markers.")


# --- prune ---------------------------------------------------------------------


def valid_days(value: object) -> int | None:
    """A whole number of days of at least AGENT_FLOOR_DAYS, else None."""
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        if not re.fullmatch(r"[0-9]{1,6}", value):
            return None
        value = int(value)
    if isinstance(value, int) and value >= AGENT_FLOOR_DAYS:
        return value
    return None


def load_retention():
    """retention.py beside this file (None when it is missing or cannot load)."""
    path = Path(__file__).resolve().with_name("retention.py")
    # A dry run writes nothing: loading the module must not leave a .pyc behind.
    before = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("ccsession_retention", path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (OSError, ImportError, SyntaxError):
        return None
    finally:
        sys.dont_write_bytecode = before


def claude_limit(home: Path) -> int:
    """The days after which Claude Code deletes a saved conversation here.

    Claude Code's managed settings win, then the user's settings, then its default
    of 30. A value that is not a whole number of at least 1 counts as the default.
    Where retention.py cannot be read the answer is the default, which makes
    prune do nothing (the safe direction).
    """
    retention = load_retention()
    if retention is None:
        return CLAUDE_DEFAULT_DAYS
    managed = retention.managed_value()
    if managed is not None:
        value = managed[0]
    else:
        data = retention.read_object(home / ".claude" / "settings.json")
        value = data.get(retention.KEY) if data else None
    if retention.is_days(value) and value >= 1:
        return value
    return CLAUDE_DEFAULT_DAYS


class Copy(NamedTuple):
    path: Path
    mtime: float
    size: int
    is_link: bool


class Transcripts(dict):
    """Copies by session id. `complete` is False when any folder or file could not be
    read: then a session missing from it may only be unreadable, never "gone"."""

    complete: bool = True


def transcripts(projects_dir: Path) -> Transcripts:
    """Every <projects-dir>/<folder>/<session id>.jsonl, by session id."""
    found = Transcripts()
    try:
        folders = sorted(os.scandir(projects_dir), key=lambda e: e.name)
    except OSError:
        found.complete = False
        return found
    for folder in folders:
        try:
            if (
                folder.name.startswith(".")
                or folder.is_symlink()
                or not folder.is_dir()
            ):
                continue
            entries = list(os.scandir(folder.path))
        except OSError:
            found.complete = False
            continue
        for entry in entries:
            if not entry.name.endswith(".jsonl"):
                continue
            session = entry.name[: -len(".jsonl")]
            if not is_session_id(session):
                continue
            try:
                info = entry.stat(follow_symlinks=False)
            except OSError:
                found.complete = False
                continue
            found.setdefault(session, []).append(
                Copy(Path(entry.path), info.st_mtime, info.st_size, entry.is_symlink())
            )
    return found


def has_conversation(projects_dir: Path, session: str) -> bool:
    """True when any <projects-dir>/<folder>/<session>.jsonl exists now. Anything
    that cannot be read counts as "yes": only a clear absence deletes a record."""
    try:
        for folder in os.scandir(projects_dir):
            if folder.name.startswith(".") or folder.is_symlink():
                continue
            if os.path.lexists(os.path.join(folder.path, session + ".jsonl")):
                return True
    except OSError:
        return True
    return False


def tree_size(path: Path) -> int:
    """Bytes in a file or folder, links counted as themselves and never followed."""
    try:
        if path.is_symlink() or not path.is_dir():
            return path.lstat().st_size
        total = 0
        for root, folders, files in os.walk(path, followlinks=False):
            for item in files + folders:
                with contextlib.suppress(OSError):
                    total += os.lstat(os.path.join(root, item)).st_size
        return total
    except OSError:
        return 0


def inside(path: Path, root: Path) -> bool:
    """True when path is a real (not linked) entry whose resolved place is under root."""
    try:
        if path.is_symlink():
            return False
        real, base = path.resolve(), root.resolve()
        return base in real.parents
    except (OSError, RuntimeError):
        return False


@dataclass
class Candidate:
    session: str
    names: list[NameFile]
    last_change: float
    size: int
    transcripts: list[Path]
    folders: list[Path]  # session folders and the file-history folder
    markers: list[Path]
    tabs: list[Path]

    @property
    def label(self) -> str:
        extra = len(self.names) - 1
        return self.names[0].name + (" (+%d more names)" % extra if extra else "")


@dataclass
class Pruned:
    days: int = AGENT_FLOOR_DAYS
    limit: int = CLAUDE_DEFAULT_DAYS  # Claude Code's own, from its settings
    now: float = 0.0
    candidates: list[Candidate] = field(default_factory=list)
    recent: int = 0  # agent sessions that changed within the days: kept
    kept: list[str] = field(default_factory=list)  # "<name>: <reason>"
    skipped: list[str] = field(default_factory=list)  # unsafe, busy or failed
    claude_deletes_first: bool = False  # limit is at or below days: nothing to do
    store_empty: bool = False  # no conversation anywhere: stale names stay
    scan_incomplete: bool = False  # a folder or file could not be read: nothing goes
    stale_names: list[NameFile] = field(default_factory=list)
    stale_markers: list[Path] = field(default_factory=list)
    stale_tabs: list[Path] = field(default_factory=list)
    stale_tab_sessions: dict[Path, str] = field(default_factory=dict)  # as planned
    deleted: int = 0  # agent sessions removed (apply only)
    removed_stale: int = 0  # stale names, markers and tab records removed

    @property
    def total_size(self) -> int:
        return sum(c.size for c in self.candidates)

    def lowered(self) -> list[Candidate]:
        """Candidates Claude Code would still keep: newer than its own limit."""
        cutoff = self.now - self.limit * DAY
        return [c for c in self.candidates if c.last_change > cutoff]

    def limit_line(self) -> str:
        """The line that says the limit is lowered, or "" when it is not."""
        if self.days >= self.limit:
            return ""
        spared = self.lowered()
        return (
            "LOWERS THE LIMIT: Claude Code keeps sessions %d days here; this removes "
            "%d agent sessions that are between %d and %d days old (%d bytes)."
            % (
                self.limit,
                len(spared),
                self.days,
                self.limit,
                sum(c.size for c in spared),
            )
        )


def tab_records(orca_dir: Path | None) -> list[tuple[Path, str]]:
    """The Orca tab records (a file per pane) and the session id each names."""
    found: list[tuple[Path, str]] = []
    if orca_dir is None:
        return found
    try:
        entries = sorted(os.scandir(orca_dir), key=lambda e: e.name)
    except OSError:
        return found
    for entry in entries:
        if entry.name.startswith(".") or entry.is_symlink() or not entry.is_file():
            continue
        session = first_line(Path(entry.path))
        if is_session_id(session):
            found.append((Path(entry.path), session))
    return found


def mtime_of(path: Path, missing: float | None = None) -> float:
    """The file's modification time. A file that cannot be read counts as just
    changed (so it is never called old), or as `missing` when it is gone."""
    try:
        return path.lstat().st_mtime
    except FileNotFoundError:
        return time.time() if missing is None else missing
    except OSError:
        return time.time()


def plan(
    projects_dir: Path,
    home: Path,
    days: int,
    orca_dir: Path | None = None,
    current_session: str = "",
    now: float | None = None,
) -> Pruned:
    """What prune would delete. Reads only; writes nothing, not even a stamp.

    A candidate is a session with at least one saved name whose marker is agent in
    every list that names it and whose newest transcript copy has not changed in
    more than days days. Anything else is kept.
    """
    checked = valid_days(days)
    if checked is None:
        raise ValueError(
            "days must be a whole number of at least %d" % AGENT_FLOOR_DAYS
        )
    days = checked
    base = home / ".claude"
    if projects_dir.resolve() != (base / "projects").resolve():
        raise ValueError("%s is not the projects folder of %s" % (projects_dir, home))
    history = base / "file-history"
    now = time.time() if now is None else now
    result = Pruned(days=days, limit=claude_limit(home), now=now)
    result.claude_deletes_first = result.limit <= days
    copies = transcripts(projects_dir)
    result.store_empty = not copies
    # An unreadable folder may hold a newer copy of a session, or the conversation
    # of a name: with the inventory incomplete nothing is called old or gone.
    result.scan_incomplete = not copies.complete or not lists(projects_dir).complete
    tabs = tab_records(orca_dir)
    all_names = by_session(projects_dir)
    cutoff = now - days * DAY

    if not result.claude_deletes_first and not result.scan_incomplete:
        for session, rows in sorted(all_names.items()):
            marks = {row.list_dir: marker(row.list_dir, session) for row in rows}
            if "agent" not in marks.values():
                continue  # unmarked or human: not an agent session
            first = next(r.name for r in rows if marks[r.list_dir] == "agent")
            others = sorted(key_of(f) for f, m in marks.items() if m != "agent")
            if others:
                result.kept.append("%s: also saved in %s" % (first, others[0]))
                continue
            if session == current_session:
                result.kept.append("%s: this is the running session" % first)
                continue
            found = copies.get(session)
            if not found:
                continue  # no conversation: a stale name, handled below
            last = max(c.mtime for c in found)
            if last > cutoff:
                result.recent += 1
                continue
            parts = [c.path for c in found]
            folders = []
            for project in sorted({p.parent for p in parts}):
                if (project / session).exists() or (project / session).is_symlink():
                    folders.append(project / session)
            if (history / session).exists() or (history / session).is_symlink():
                folders.append(history / session)
            markers = [
                f / ORIGIN / session
                for f in marks
                if (f / ORIGIN / session).is_file()
                or (f / ORIGIN / session).is_symlink()
            ]
            tab_files = [p for p, s in tabs if s == session]
            unsafe = [
                p
                for p in parts + [n.path for n in rows] + markers
                if not inside(p, projects_dir)
            ]
            unsafe += [
                p
                for p in folders
                if not inside(p, projects_dir if p.parent != history else history)
            ]
            unsafe += [
                p for p in tab_files if orca_dir is None or not inside(p, orca_dir)
            ]
            if history.is_symlink() and any(p.parent == history for p in folders):
                # A linked file-history would make its target the boundary.
                unsafe.append(history)
            if unsafe:
                result.skipped.append(
                    "%s: %s is not a plain file under the saved sessions; left alone"
                    % (first, unsafe[0])
                )
                continue
            size = sum(c.size for c in found) + sum(tree_size(p) for p in folders)
            result.candidates.append(
                Candidate(session, rows, last, size, parts, folders, markers, tab_files)
            )

    # Names, markers and tab records whose conversation is gone, whatever their
    # origin. Nothing is called stale when no conversation exists anywhere: an
    # unreadable or missing store must not take every name with it.
    if not result.store_empty and not result.scan_incomplete:
        grace = now - GRACE
        for session, rows in all_names.items():
            if session in copies or session == current_session:
                continue
            for row in rows:
                if mtime_of(row.path) < grace and inside(row.path, projects_dir):
                    result.stale_names.append(row)
        named = {
            (row.list_dir, row.session) for rows in all_names.values() for row in rows
        }
        for folder in lists(projects_dir):
            try:
                found_markers = sorted(
                    os.scandir(folder / ORIGIN), key=lambda e: e.name
                )
            except OSError:
                continue
            for entry in found_markers:
                path = Path(entry.path)
                if (
                    is_session_id(entry.name)
                    and entry.name not in copies
                    and entry.name != current_session
                    and (folder, entry.name) not in named
                    and mtime_of(path) < grace
                    and inside(path, projects_dir)
                ):
                    result.stale_markers.append(path)
        for path, session in tabs:
            if (
                session not in copies
                and session != current_session
                and mtime_of(path) < grace
                and orca_dir is not None
                and inside(path, orca_dir)
            ):
                result.stale_tabs.append(path)
                result.stale_tab_sessions[path] = session
    return result


def remove_file(path: Path, root: Path, result: Pruned, what: str) -> bool:
    """Unlink one file after checking it again; report and return False on failure."""
    if not inside(path, root):
        result.skipped.append(
            "%s: not a plain file under %s; left alone" % (path, root)
        )
        return False
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    except OSError as exc:
        result.skipped.append("%s %s: %s" % (what, path, exc))
        return False
    return True


def prune_one(
    cand: Candidate, result: Pruned, projects_dir: Path, history: Path, cutoff: float
) -> bool:
    """Delete one candidate; the caller holds the lock of every list that names it.
    True when the session is gone, with its names and marker."""
    label = cand.label
    # Seen again right before the delete: a copy that changed meanwhile is a
    # session in use.
    if any(mtime_of(p, missing=0.0) > cutoff for p in cand.transcripts):
        result.skipped.append("%s: changed while pruning; kept" % label)
        return False
    # So is a session that was renamed or marked since the plan: it must still
    # have exactly the names it had, every one marked agent.
    now_rows = by_session(projects_dir).get(cand.session, [])
    if {r.path for r in now_rows} != {n.path for n in cand.names} or any(
        marker(r.list_dir, cand.session) != "agent" for r in now_rows
    ):
        result.skipped.append("%s: renamed or marked while pruning; kept" % label)
        return False
    clean = True
    for path in cand.transcripts:
        clean &= remove_file(path, projects_dir, result, "transcript")
    if not clean:
        return False  # a conversation that stays keeps everything else of the session
    for folder in cand.folders:
        root = history if folder.parent == history else projects_dir
        if not inside(folder, root) or (root == history and history.is_symlink()):
            result.skipped.append(
                "%s: not a plain folder under %s; left alone" % (folder, root)
            )
            clean = False
            continue
        try:
            shutil.rmtree(folder)
        except FileNotFoundError:
            pass
        except OSError as exc:
            result.skipped.append("folder %s: %s" % (folder, exc))
            clean = False
    if not clean:
        return False
    # The conversation is gone; now its names and marker.
    for row in cand.names:
        if first_line(row.path) == cand.session:
            remove_file(row.path, projects_dir, result, "name")
    for list_dir in sorted({n.list_dir for n in cand.names}):
        marker_file = list_dir / ORIGIN / cand.session
        if marker_file.is_file() or marker_file.is_symlink():
            remove_file(marker_file, projects_dir, result, "marker")
    return True


def apply_plan(
    result: Pruned, projects_dir: Path, home: Path, orca_dir: Path | None
) -> None:
    """Delete what plan found. Transcripts first: a name, marker or tab record goes
    only after its session's conversation is gone, and a conversation that could not
    be removed keeps all of them."""
    history = home / ".claude" / "file-history"
    cutoff = result.now - result.days * DAY
    for cand in result.candidates:
        # Every list that names the session is locked from the last look at its
        # names and markers until they are gone: ccsession --mark and the hook take
        # the same lock, so a promotion cannot slip in between the look and the delete.
        try:
            with contextlib.ExitStack() as stack:
                for folder in sorted({n.list_dir for n in cand.names}):
                    stack.enter_context(locked(folder))
                removed = prune_one(cand, result, projects_dir, history, cutoff)
        except Busy as exc:
            result.skipped.append(
                "%s: list is busy (%s); kept for the next run" % (cand.label, exc)
            )
            continue
        if removed:
            remove_tabs(cand.tabs, cand.session, orca_dir, result)
            result.deleted += 1
    # Stale names, markers and tab records, each checked again under the lock: the
    # name still holds the id and no conversation has appeared for it (looked for
    # again at that moment, with the lock held, not from the plan's inventory).
    for row in result.stale_names:
        try:
            with locked(row.list_dir):
                if first_line(row.path) == row.session and not has_conversation(
                    projects_dir, row.session
                ):
                    result.removed_stale += remove_file(
                        row.path, projects_dir, result, "name"
                    )
                    # The last name of a session in this list takes its marker too.
                    if not any(r.session == row.session for r in names(row.list_dir)):
                        gone = row.list_dir / ORIGIN / row.session
                        if gone.is_file() or gone.is_symlink():
                            result.removed_stale += remove_file(
                                gone, projects_dir, result, "marker"
                            )
        except (Busy, OSError) as exc:
            result.skipped.append("%s: %s" % (row.path, exc))
    for path in result.stale_markers:
        try:
            with locked(path.parent.parent):
                if not has_conversation(projects_dir, path.name) and not any(
                    r.session == path.name for r in names(path.parent.parent)
                ):
                    result.removed_stale += remove_file(
                        path, projects_dir, result, "marker"
                    )
        except (Busy, OSError) as exc:
            result.skipped.append("%s: %s" % (path, exc))
    if result.stale_tabs and orca_dir is not None:
        try:
            with locked(orca_dir):
                for path in result.stale_tabs:
                    # The record may have been replaced since the plan: it goes only
                    # while it still names the planned session, that session still
                    # has no conversation, and it is still older than the grace.
                    planned = result.stale_tab_sessions.get(path, "")
                    if (
                        planned
                        and first_line(path) == planned
                        and not has_conversation(projects_dir, planned)
                        and mtime_of(path) < result.now - GRACE
                    ):
                        result.removed_stale += remove_file(
                            path, orca_dir, result, "tab record"
                        )
        except (Busy, OSError) as exc:
            result.skipped.append("%s: %s" % (orca_dir, exc))


def remove_tabs(
    paths: list[Path], session: str, orca_dir: Path | None, result: Pruned
) -> None:
    if not paths or orca_dir is None:
        return
    try:
        with locked(orca_dir):
            for path in paths:
                if first_line(path) == session:
                    remove_file(path, orca_dir, result, "tab record")
    except (Busy, OSError) as exc:
        result.skipped.append("%s: %s" % (orca_dir, exc))


def prune(
    projects_dir: Path,
    home: Path,
    days: int,
    apply: bool = False,
    current_session: str = "",
    orca_dir: Path | None = None,
    now: float | None = None,
) -> Pruned:
    """Plan, and with apply delete, the agent sessions older than days (see plan)."""
    result = plan(projects_dir, home, days, orca_dir, current_session, now)
    if apply:
        apply_plan(result, projects_dir, home, orca_dir)
    return result


def human_size(count: int) -> str:
    size = float(count)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return "%d B" % size if unit == "B" else "%.1f %s" % (size, unit)
        size /= 1024
    return "%d B" % count


def print_prune(result: Pruned, apply: bool) -> None:
    days = result.days
    if result.claude_deletes_first:
        print(
            "Claude Code already deletes saved sessions after %d days here, which is "
            "at or before the %d days asked for, so no agent session is removed."
            % (result.limit, days)
        )
    else:
        print(
            "Agent sessions that have not changed in more than %d days "
            "(Claude Code keeps sessions %d days here):" % (days, result.limit)
        )
        for cand in result.candidates:
            print(
                "  %s  last change %s  %d days old  %s"
                % (
                    cand.label,
                    time.strftime("%Y-%m-%d", time.localtime(cand.last_change)),
                    int((result.now - cand.last_change) // DAY),
                    human_size(cand.size),
                )
            )
        if not result.candidates:
            print("  none")
        verb = "Deleted" if apply else "Would delete"
        count = result.deleted if apply else len(result.candidates)
        print(
            "%s %d agent session%s (%s)."
            % (
                verb,
                count,
                "" if count == 1 else "s",
                human_size(result.total_size),
            )
        )
    for line in result.kept:
        print("kept: %s" % line)
    if result.scan_incomplete:
        print(
            "Some saved conversations could not be read, so nothing was called old "
            "or gone: no session, name, marker or tab record is removed."
        )
    if result.store_empty:
        print("No saved conversation found anywhere: stale names are not removed.")
    stale = len(result.stale_names) + len(result.stale_markers) + len(result.stale_tabs)
    if stale:
        count = result.removed_stale if apply else stale
        noun = "entry" if count == 1 else "entries"
        if apply:
            print("Removed %d stale %s whose conversation was gone." % (count, noun))
        else:
            print(
                "Would remove %d stale %s whose conversation is gone (%d names, "
                "%d markers, %d tab records)."
                % (
                    count,
                    noun,
                    len(result.stale_names),
                    len(result.stale_markers),
                    len(result.stale_tabs),
                )
            )
    for line in result.skipped:
        print("Skipped %s" % line)
    limit_line = result.limit_line()
    if limit_line:
        print(limit_line)
    if not apply:
        print("Dry run: nothing was deleted. Run with --apply to delete.")


def keep_days(environ: Mapping[str, str], option: str | None) -> int | None:
    """The days to keep an agent session: --days, else the variable, else 30.
    None when the value given is not a whole number of at least 30."""
    from_env = environ.get(KEEP_ENV) or None  # set but empty counts as not set
    if from_env is not None and valid_days(from_env) is None:
        return None  # an invalid variable stops --prune even when --days is valid
    if option is not None:
        return valid_days(option)
    return valid_days(from_env) if from_env is not None else AGENT_FLOOR_DAYS


def hint(projects_dir: Path, home: Path, environ: Mapping[str, str]) -> str:
    """The one line for --list and --here, or "" (read-only; never raises)."""
    try:
        days = valid_days(environ.get(KEEP_ENV, "")) or AGENT_FLOOR_DAYS
        result = plan(
            projects_dir, home, days, None, environ.get("CLAUDE_SESSION_ID", "")
        )
        count = len(result.candidates)
        if count:
            return (
                "%d agent sessions are older than %d days: ccsession --prune shows "
                "what would be removed" % (count, days)
            )
    except Exception:  # a listing never fails on this
        pass
    return ""


USAGE = (
    "usage: session_keep.py classify [--apply] <projects-dir>\n"
    "       session_keep.py prune [--apply] [--days N] <projects-dir> <home> <orca-dir>\n"
    "       session_keep.py hint <projects-dir> <home>"
)


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or args[0] not in ("classify", "prune", "hint"):
        print(USAGE, file=sys.stderr)
        return 2
    command, rest = args[0], args[1:]
    apply = False
    option = None
    positional = []
    i = 0
    while i < len(rest):
        item = rest[i]
        if item == "--apply" and command != "hint":
            apply = True
        elif command == "prune" and item == "--days" and i + 1 < len(rest):
            option = rest[i + 1]
            i += 1
        elif command == "prune" and item.startswith("--days="):
            option = item[len("--days=") :]
        elif item.startswith("-") and item != "-":
            print(USAGE, file=sys.stderr)
            return 2
        else:
            positional.append(item)
        i += 1
    if command == "classify":
        if len(positional) != 1:
            print(USAGE, file=sys.stderr)
            return 2
        print_classify(classify(Path(positional[0]), apply), apply)
        return 0
    if command == "hint":
        if len(positional) != 2:
            return 0  # a listing never fails on it
        line = hint(Path(positional[0]), Path(positional[1]), os.environ)
        if line:
            print(line)
        return 0
    if len(positional) != 3:
        print(USAGE, file=sys.stderr)
        return 2
    days = keep_days(os.environ, option)
    if days is None:
        print(
            "ccsession: --days and %s must be a whole number of at least %d "
            "(an agent session is never kept shorter); nothing was deleted."
            % (KEEP_ENV, AGENT_FLOOR_DAYS),
            file=sys.stderr,
        )
        return 2
    projects_dir, home, orca_dir = (Path(p) for p in positional)
    try:
        result = prune(
            projects_dir,
            home,
            days,
            apply,
            os.environ.get("CLAUDE_SESSION_ID", ""),
            orca_dir,
        )
    except ValueError as exc:
        print("ccsession: %s; nothing was deleted." % exc, file=sys.stderr)
        return 2
    print_prune(result, apply)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
