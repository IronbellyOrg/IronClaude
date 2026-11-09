#!/usr/bin/env python3
"""Orca worktree and agent-launch steps of ``/sc:issue --claim``.

Standard library only. Called by the claim flow as
``orca_worktree.py <subcommand> ...`` (subcommands ``preflight``, ``worktree``,
``prompt``, ``launch``); the skill reads the one JSON object printed on stdout.

Every runtime outcome exits 0 with a JSON object; exit code 2 is reserved for
bad command-line arguments (argparse). Every subprocess runs without a shell,
with captured output and a timeout: 120 s by default, 30 s for ``preflight``
and 15 s for each ``orca terminal read``. A timeout is a failed command, never
an exception. The environment variable ``SC_ORCA_TIMEOUT`` (seconds, a float)
replaces every timeout; tests use it so a hanging fake ``orca`` is cut fast.

``preflight`` prints ``{"ok": true}`` when ``orca status --json`` exits 0 and
reports ``ok: true`` and ``result.runtime.reachable: true``; otherwise
``{"ok": false, "detail": "<first stderr line, or why the JSON failed>"}``. A
missing ``orca`` binary gives the same shape.

``worktree --repo <owner/repo> --number <N> --base origin/<B> --source <D>``
finds or creates the Orca worktree ``issue-<N>`` and copies ``<D>`` (the
``.dev/issues/<N>/`` directory) into it, file by file. It prints
``{status, path, branch, match_key, warning, detail, tracked_files,
tracked_known}`` with ``status`` ``created``, ``reused`` or ``failed``. It runs
only these commands: ``git rev-parse --path-format=absolute --git-common-dir``,
``git fetch origin``, ``git rev-parse --verify origin/<B>``,
``orca worktree list``, ``orca worktree create`` (no link flag, no agent flag),
``git -C <wt> rev-parse --path-format=absolute --git-common-dir`` and
``git -C <wt> ls-files .dev/issues/<N>``. Only Orca makes the worktree; this
file never commits, pushes, stages or removes anything. The create has no agent
because the claim must copy ``<D>`` into the worktree before its agent starts; a
create without ``--agent`` makes Orca open one plain first terminal tab, so after
a successful copy of a newly created worktree it also runs ``orca terminal list
--worktree path:<wt> --json`` and, only when that lists exactly one terminal with
no agent, ``orca terminal close --terminal <handle> --tab --json``. Any reason it
cannot close the tab is the non-fatal warning ``W-FIRST-TAB-LEFT``; it never
changes ``status``, and a reused worktree gets no ``terminal`` call.

``prompt --template <file> --level worktree|full [--submit] --number <N>
--repo <owner/repo> [--source <D>] --out <file>`` renders ``launch-prompt.md`` from the four blocks of
``templates/launch-prompt.md`` (``common``, the level block, ``submit`` with
``--submit``) and prints ``{"status": "written", "path": "<out>"}``. ``--submit``
with ``--level worktree`` is a bad argument (exit 2).

``launch --number <N> --source <D> --level worktree|full [--submit]`` starts one
Claude Code agent in the worktree recorded in ``<D>/worktree.json``. It first
runs the IR-4 preflight (jq, uv, Linux, the installed guard and its settings
registrations; read only) and refuses the launch with ``W-ENFORCEMENT-ABSENT``
when the guard would not be effective. It then installs the owned L2
pre-push hook (``install_l2``, advisory) and re-checks it read-only
(``l2_status``); any state other than ``owned`` adds the warning
``W-L2-ABSENT`` with the reason, and the launch goes ahead (IR-7 stays a
warning; an off ``IR7_REFUSE`` switch arrives in a later commit). It then publishes the launch record the enforcement hook reads
(``$HOME/.claude/state/launch-level/pending/<nonce>``, one word), then runs
``orca agent launch --surface terminal`` with a prompt that starts with
``[sc-launch:v1:<nonce>]``, checks for the ccsession shim (its screen text, which
is visible for only 1 to 2 seconds, or the ``sc-launch-v1-...`` session name that
stays in the tab title, read with ``orca terminal show``), and writes a ``launch`` entry into ``worktree.json``. It prints ``{status, warning,
detail, terminal, launched_at, enforcement_hook, hand_command, release,
layers}`` with ``status`` ``launched``, ``failed`` or ``already_launched``;
``release`` (how a person releases the session) and ``layers`` (one status line
for L1 and one for L2) are set only for ``launched``, else null.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import re
import secrets
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_TIMEOUT = 120.0
PREFLIGHT_TIMEOUT = 30.0
TERMINAL_READ_TIMEOUT = 15.0
TIMEOUT_ENV = "SC_ORCA_TIMEOUT"


@dataclass
class Result:
    """Outcome of one subprocess call. ``run`` never raises."""

    rc: int | None
    out: str = ""
    err: str = ""
    timed_out: bool = False
    missing: bool = False

    @property
    def ok(self) -> bool:
        return self.rc == 0 and not self.timed_out and not self.missing

    def first_error_line(self) -> str:
        """First non-empty stderr line, else a short reason for the failure."""
        for line in self.err.splitlines():
            if line.strip():
                return line.strip()
        if self.timed_out:
            return "timed out"
        if self.missing:
            return "command not found"
        return f"exit {self.rc}"


def _timeout(default: float) -> float:
    raw = os.environ.get(TIMEOUT_ENV)
    if raw:
        try:
            value = float(raw)
        except ValueError:
            return default
        if value > 0:
            return value
    return default


def run(
    argv: list[str],
    timeout: float = DEFAULT_TIMEOUT,
    cwd: str | None = None,
    env: Mapping[str, str] | None = None,
    input: str | None = None,
) -> Result:
    """Run ``argv`` without a shell; return a failed Result on any problem.

    ``env=None`` inherits the current environment; ``input`` is sent on stdin
    (``None`` leaves stdin inherited, as before).
    """
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=_timeout(timeout),
            check=False,
            cwd=cwd,
            env=dict(env) if env is not None else None,
            input=input,
        )
    except subprocess.TimeoutExpired as exc:
        return Result(
            rc=None,
            out=_text(exc.stdout),
            err=_text(exc.stderr),
            timed_out=True,
        )
    except (FileNotFoundError, PermissionError) as exc:
        return Result(rc=None, err=str(exc), missing=True)
    except OSError as exc:
        return Result(rc=None, err=str(exc), missing=True)
    return Result(rc=proc.returncode, out=proc.stdout or "", err=proc.stderr or "")


def _text(value: object) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value if isinstance(value, str) else ""


def parse_json(text: str) -> object | None:
    """Parse ``text`` as JSON; ``None`` when it is not valid JSON."""
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


def atomic_write_text(path: Path, text: str) -> None:
    """Write ``text`` to ``path`` through a random, exclusive temp file and a rename.

    A fixed temp name next to the target could be a planted symlink that a plain
    ``write_text`` would follow. ``mkstemp`` creates a fresh name with O_EXCL, and
    ``os.replace`` swaps the directory entry, so a symlink or hard link at the
    final name is replaced, never written through.
    """
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.chmod(tmp_name, 0o644)
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise


def emit(payload: dict) -> int:
    """Print one JSON object on stdout; every runtime outcome exits 0."""
    print(json.dumps(payload))
    return 0


def cmd_preflight(_args: argparse.Namespace) -> int:
    res = run(["orca", "status", "--json"], PREFLIGHT_TIMEOUT)
    if not res.ok:
        return emit({"ok": False, "detail": res.first_error_line()})
    data = parse_json(res.out)
    if not isinstance(data, dict):
        return emit({"ok": False, "detail": "orca status did not print a JSON object"})
    if data.get("ok") is not True:
        return emit({"ok": False, "detail": "orca status reported ok is not true"})
    result = data.get("result")
    runtime = result.get("runtime") if isinstance(result, dict) else None
    if not isinstance(runtime, dict) or runtime.get("reachable") is not True:
        return emit({"ok": False, "detail": "the Orca runtime is not reachable"})
    return emit({"ok": True})


# --- worktree -------------------------------------------------------------

# When several codes apply to a created or reused worktree, the first of these
# is the ``warning`` field and the rest are appended to ``detail``.
WARNING_ORDER = [
    "W-ORCA-LIST-FAILED",
    "W-ORIGIN-BASE-MISSING",
    "W-WORKTREE-CREATE-FAILED",
    "W-WORKTREE-AMBIGUOUS",
    "W-WORKTREE-STALE",
    "W-WORKTREE-COPY-FAILED",
    "W-ORIGIN-BASE-STALE",
    "W-FIRST-TAB-LEFT",  # cosmetic: an empty tab to close by hand, so it ranks last
]
RECORD_NAME = "worktree.json"


@dataclass
class Outcome:
    """The one JSON object ``worktree`` prints."""

    status: str = "failed"
    path: str | None = None
    branch: str | None = None
    match_key: str | None = None
    primary: str | None = None
    notes: list[tuple[str, str]] = field(default_factory=list)
    tracked_files: list[str] = field(default_factory=list)
    tracked_known: bool = False

    def note(self, code: str, text: str) -> None:
        self.notes.append((code, text))

    def fail(self, code: str, text: str) -> Outcome:
        self.status = "failed"
        self.primary = code
        self.note(code, text)
        return self

    def as_dict(self) -> dict:
        warning = self.primary
        if warning is None and self.notes:
            warning = min((c for c, _ in self.notes), key=WARNING_ORDER.index)
        parts = [t for c, t in self.notes if c == warning]
        parts += [f"also {c}: {t}" for c, t in self.notes if c != warning]
        return {
            "status": self.status,
            "path": self.path,
            "branch": self.branch,
            "match_key": self.match_key,
            "warning": warning,
            "detail": "; ".join(parts),
            "tracked_files": self.tracked_files,
            "tracked_known": self.tracked_known,
        }


def real(path: str) -> str:
    return os.path.realpath(path)


def git_common_dir(checkout: str | None = None) -> str | None:
    argv = ["git"] + (["-C", checkout] if checkout else [])
    res = run(argv + ["rev-parse", "--path-format=absolute", "--git-common-dir"])
    out = res.out.strip()
    return out if res.ok and out else None


def main_checkout(common_dir: str) -> str:
    common = real(common_dir)
    return os.path.dirname(common) if os.path.basename(common) == ".git" else common


def row_id(row: dict) -> str:
    return str(row.get("id") or row.get("path") or "")


def row_basename(row: dict) -> str:
    return os.path.basename(str(row.get("path") or "").rstrip("/"))


def short_branch(row: dict) -> str | None:
    branch = row.get("branch")
    if not isinstance(branch, str) or not branch:
        return None
    return branch.removeprefix("refs/heads/")


def list_rows(main: str) -> tuple[list[dict] | None, str]:
    """``orca worktree list`` rows, or ``(None, why)`` when the list is unusable."""
    res = run(
        [
            "orca",
            "worktree",
            "list",
            "--repo",
            f"path:{main}",
            "--limit",
            "500",
            "--json",
        ]
    )
    if not res.ok:
        return None, f"orca worktree list failed: {res.first_error_line()}"
    data = parse_json(res.out)
    result = data.get("result") if isinstance(data, dict) else None
    if not isinstance(data, dict) or data.get("ok") is not True:
        return None, "orca worktree list did not report ok"
    if not isinstance(result, dict) or not isinstance(result.get("worktrees"), list):
        return None, "orca worktree list printed no worktree rows"
    rows = [r for r in result["worktrees"] if isinstance(r, dict)]
    if result.get("truncated") is True:
        return None, (
            f"orca worktree list is truncated ({len(rows)} rows of "
            f"{result.get('totalCount')})"
        )
    host = result.get("hostScope")
    omitted = host.get("omittedHostIds") if isinstance(host, dict) else None
    if omitted:
        return None, f"orca worktree list omits hosts {omitted}"
    if not rows:
        return None, "orca worktree list has zero rows"
    if not any(r.get("isMainWorktree") is True for r in rows):
        return None, f"orca worktree list has no main worktree row ({len(rows)} rows)"
    return rows, ""


def read_record(source: Path) -> dict | None:
    try:
        data = json.loads((source / RECORD_NAME).read_text())
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def guarded_record_path(source: Path, main_common: str) -> str | None:
    """The path in ``worktree.json`` when it exists and shares the main git dir."""
    record = read_record(source)
    path = record.get("path") if record else None
    if not isinstance(path, str) or not os.path.isdir(path):
        return None
    common = git_common_dir(path)
    if common is None or real(common) != real(main_common):
        return None
    return real(path)


def lookup(
    rows: list[dict], repo: str, number: int, record_real: str | None
) -> tuple[str | None, list[dict]]:
    """Duplicate detection: first key with a hit decides; hits are deduplicated."""
    pattern = re.compile(rf"^issue-{number}(-|$)")
    marker = re.compile(
        r"(?<![\w./-])" + re.escape(f"sc:issue {repo}#{number}") + r"(?!\d)"
    )

    def by_marker(row: dict) -> bool:
        return bool(marker.search(str(row.get("comment") or "")))

    def by_record(row: dict) -> bool:
        return (
            record_real is not None and real(str(row.get("path") or "")) == record_real
        )

    def by_basename(row: dict) -> bool:
        return bool(pattern.match(row_basename(row)))

    def by_branch(row: dict) -> bool:
        return bool(pattern.match(str(row.get("branch") or "").rsplit("/", 1)[-1]))

    candidates = [
        r for r in rows if not r.get("isArchived") and not r.get("isMainWorktree")
    ]
    for key, test in (
        ("marker", by_marker),
        ("record", by_record),
        ("basename", by_basename),
        ("branch", by_branch),
    ):
        hits: dict[str, dict] = {}
        for row in candidates:
            if test(row):
                hits.setdefault(row_id(row), row)
        if hits:
            return key, list(hits.values())
    return None, []


def tracked_under(worktree: str, number: int) -> tuple[set[str], bool]:
    """Paths git tracks under ``.dev/issues/<N>`` in the worktree, and whether known."""
    res = run(["git", "-C", worktree, "ls-files", f".dev/issues/{number}"])
    lines = [ln for ln in res.out.splitlines() if ln]
    # A quoted line means git escaped an unusual name; we cannot trust the set.
    if not res.ok or any(ln.startswith('"') for ln in lines):
        return set(), False
    return set(lines), True


def first_symlink(root: Path, target: Path) -> Path | None:
    """The first symlink among the components of ``target`` below ``root``, if any.

    A symlinked directory in the worktree (a tracked symlink arrives through git)
    would send the copy to wherever it points, so every component is checked, not
    only the ones that resolve outside the worktree.
    """
    current = root
    for part in target.relative_to(root).parts:
        current = current / part
        if current.is_symlink():
            return current
    return None


def copy_issue_dir(
    source: Path,
    dest: Path,
    number: int,
    tracked: set[str],
    tracked_known: bool,
    root: Path,
) -> tuple[list[str], list[str]]:
    """Copy ``source`` into ``dest`` file by file; return (named files, errors).

    ``root`` is the worktree directory; nothing is written through a symlink below it.
    """
    named: list[str] = []
    errors: list[str] = []

    def walk_error(exc: OSError) -> None:
        errors.append(f"{exc.filename}: {exc.strerror or exc}")

    for walk_root, dirs, files in os.walk(source, onerror=walk_error):
        dirs.sort()
        for name in list(dirs):
            if (Path(walk_root) / name).is_symlink():
                shown = (Path(walk_root) / name).relative_to(source)
                named.append(f"{shown} (a symlinked source directory, not copied)")
        for name in sorted(files):
            src_file = Path(walk_root) / name
            rel = src_file.relative_to(source)
            if rel.as_posix() == RECORD_NAME:
                continue
            dst_file = dest / rel
            bad = first_symlink(root, dst_file.parent)
            if bad is not None:
                errors.append(
                    f"{rel}: {bad} is a symlink, nothing was written through it"
                )
                continue
            try:
                if f".dev/issues/{number}/{rel.as_posix()}" in tracked:
                    named.append(f"{rel} (tracked in the worktree, not copied)")
                    continue
                exists = dst_file.exists() or dst_file.is_symlink()
                if exists and filecmp.cmp(src_file, dst_file, shallow=False):
                    continue
                if exists and not tracked_known:
                    named.append(
                        f"{rel} (differs; git could not be asked what it tracks, "
                        "so it was not overwritten)"
                    )
                    continue
                if exists and f".dev/issues/{number}/{rel.as_posix()}.prev" in tracked:
                    named.append(
                        f"{rel} (differs; its backup name {rel}.prev is tracked in "
                        "the worktree, so it was not overwritten)"
                    )
                    continue
                if exists:
                    prev = dst_file.with_name(dst_file.name + ".prev")
                    os.replace(dst_file, prev)
                    named.append(f"{rel} (the older copy was kept as {rel}.prev)")
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src_file, dst_file)
                if not filecmp.cmp(src_file, dst_file, shallow=False):
                    errors.append(f"{rel}: bytes differ after the copy")
            except OSError as exc:
                errors.append(f"{rel}: {exc}")
    return named, errors


def write_record(source: Path, path: str, status: str) -> None:
    """Write ``worktree.json``.

    An earlier ``launch`` entry is kept only for a reused worktree at the same path:
    a newly created worktree has never had an agent, and a replacement at another
    path must not inherit the old worktree's launch.
    """
    record: dict = {"path": path, "status": status}
    old = read_record(source)
    if (
        status == "reused"
        and old
        and isinstance(old.get("launch"), dict)
        and isinstance(old.get("path"), str)
        and real(old["path"]) == real(path)
    ):
        record["launch"] = old["launch"]
    atomic_write_text(source / RECORD_NAME, json.dumps(record, indent=2) + "\n")


def finish(
    out: Outcome,
    row: dict | None,
    wt: str,
    source: Path,
    number: int,
    main_common: str,
    status: str,
    key: str | None,
) -> None:
    """Check the worktree, copy the issue directory into it, write the record."""
    out.path, out.match_key = wt, key
    out.branch = short_branch(row) if row else None
    common = git_common_dir(wt)
    if common is None or real(common) != real(main_common):
        out.fail(
            "W-WORKTREE-STALE",
            f"{wt} does not belong to this repository (git common dir differs)",
        )
        return
    tracked, known = tracked_under(wt, number)
    out.tracked_files, out.tracked_known = sorted(tracked), known
    dest = Path(wt) / ".dev" / "issues" / str(number)
    if not source.is_dir():
        out.fail("W-WORKTREE-COPY-FAILED", f"source directory {source} is missing")
        return
    if real(str(source)) != real(str(dest)):
        named, errors = copy_issue_dir(source, dest, number, tracked, known, Path(wt))
        if errors:
            out.fail("W-WORKTREE-COPY-FAILED", "; ".join(errors))
            return
        if named:
            out.note("W-WORKTREE-COPY-FAILED", "not copied as is: " + "; ".join(named))
    try:
        write_record(source, str(Path(wt).resolve()), status)
    except OSError as exc:
        out.fail("W-WORKTREE-COPY-FAILED", f"could not write {RECORD_NAME}: {exc}")
        return
    out.status = status


def close_first_tab(out: Outcome, created: Result) -> None:
    """Close the plain first tab Orca opens for a create without ``--agent``.

    Runs only for a worktree this call just created, after the copy succeeded. It
    never changes ``out.status``: every reason it cannot close the tab becomes the
    warning ``W-FIRST-TAB-LEFT``, and an unknown create reply never leads to a close.
    """

    def left(why: str) -> None:
        out.note("W-FIRST-TAB-LEFT", f"the plain first tab was left open: {why}")

    data = None if created.timed_out else parse_json(created.out)
    reply = (
        data.get("result")
        if isinstance(data, dict) and data.get("ok") is True
        else None
    )
    if not isinstance(reply, dict):
        left("the create reply is missing, timed out or not an ok JSON object")
        return
    if reply.get("setup") or reply.get("defaultTabs"):
        left("the create reported a setup or default tabs, so the tab count is unknown")
        return
    listed = run(
        ["orca", "terminal", "list", "--worktree", f"path:{out.path}", "--json"]
    )
    data = parse_json(listed.out) if listed.ok else None
    result = (
        data.get("result")
        if isinstance(data, dict) and data.get("ok") is True
        else None
    )
    terminals = result.get("terminals") if isinstance(result, dict) else None
    if not isinstance(terminals, list) or not all(
        isinstance(t, dict) for t in terminals
    ):
        left(
            f"orca terminal list gave no usable terminal rows ({listed.first_error_line()})"
        )
        return
    if len(terminals) != 1:
        left(f"{len(terminals)} terminals are listed, not exactly one")
        return
    terminal = terminals[0]
    handle = terminal.get("handle")
    if terminal.get("agentIdentity"):
        left("the one terminal runs an agent")
        return
    if not isinstance(handle, str) or not handle:
        left("the one terminal has no handle")
        return
    closed = run(["orca", "terminal", "close", "--terminal", handle, "--tab", "--json"])
    reply = parse_json(closed.out)
    if not closed.ok or (isinstance(reply, dict) and reply.get("ok") is False):
        left(f"orca terminal close failed: {closed.first_error_line()}")


def cmd_worktree(args: argparse.Namespace) -> int:
    out = Outcome()
    source = Path(args.source)
    number = args.number
    main_common = git_common_dir()
    if main_common is None:
        out.fail("W-WORKTREE-CREATE-FAILED", "not inside a git checkout")
        return emit(out.as_dict())
    main = main_checkout(main_common)

    def reuse_record(why: str) -> bool:
        path = guarded_record_path(source, main_common)
        if path is None:
            out.fail("W-ORCA-LIST-FAILED", why)
            return False
        out.note("W-ORCA-LIST-FAILED", f"unverified, reused from {RECORD_NAME}: {why}")
        finish(out, None, path, source, number, main_common, "reused", "record")
        return True

    rows, why = list_rows(main)
    if rows is None:
        reuse_record(why)
        return emit(out.as_dict())

    key, hits = lookup(
        rows, args.repo, number, guarded_record_path(source, main_common)
    )
    if key is not None:
        live = [r for r in hits if os.path.isdir(str(r.get("path") or ""))]
        paths = ", ".join(str(r.get("path")) for r in hits)
        if len(live) > 1:
            out.fail(
                "W-WORKTREE-AMBIGUOUS", f"several worktrees match ({key}): {paths}"
            )
        elif not live:
            out.fail(
                "W-WORKTREE-STALE", f"the worktree is gone from disk ({key}): {paths}"
            )
        else:
            row = live[0]
            finish(
                out, row, str(row["path"]), source, number, main_common, "reused", key
            )
        return emit(out.as_dict())

    # No existing worktree: make sure the base ref exists, then create one.
    fetch = run(["git", "fetch", "origin"])
    if not run(["git", "rev-parse", "--verify", args.base]).ok:
        out.fail(
            "W-ORIGIN-BASE-MISSING",
            f"{args.base} does not resolve; run git fetch origin",
        )
        return emit(out.as_dict())
    if not fetch.ok:
        out.note(
            "W-ORIGIN-BASE-STALE",
            f"git fetch origin failed: {fetch.first_error_line()}",
        )
    ids_before = {row_id(r) for r in rows}
    created = run(
        [
            "orca",
            "worktree",
            "create",
            "--repo",
            f"path:{main}",
            "--name",
            f"issue-{number}",
            "--base-branch",
            args.base,
            "--no-parent",
            "--comment",
            f"sc:issue {args.repo}#{number}",
            "--json",
        ]
    )
    if not created.ok and not created.timed_out:
        out.fail("W-WORKTREE-CREATE-FAILED", created.first_error_line())
        return emit(out.as_dict())
    after, why = list_rows(main)
    if after is None:
        reuse_record(why)
        return emit(out.as_dict())
    pattern = re.compile(rf"^issue-{number}(-|$)")
    new = [
        r
        for r in after
        if row_id(r) not in ids_before and pattern.match(row_basename(r))
    ]
    if len(new) > 1:
        paths = ", ".join(str(r.get("path")) for r in new)
        out.fail("W-WORKTREE-AMBIGUOUS", f"several new worktrees appeared: {paths}")
    elif not new:
        text = "orca worktree create timed out" if created.timed_out else "created"
        out.fail("W-WORKTREE-CREATE-FAILED", f"{text} but not listed")
    elif not os.path.isdir(str(new[0].get("path") or "")):
        out.fail(
            "W-WORKTREE-CREATE-FAILED",
            f"created but {new[0].get('path')} is not on disk",
        )
    else:
        finish(
            out,
            new[0],
            str(new[0]["path"]),
            source,
            number,
            main_common,
            "created",
            None,  # a new worktree was matched by no lookup key
        )
        if out.status == "created":
            close_first_tab(out, created)
    return emit(out.as_dict())


# --- prompt ---------------------------------------------------------------

BLOCK_MARKER = re.compile(r"^<!-- block:([a-z]+) -->[ \t]*$", re.M)


def render_prompt(
    template: str, level: str, submit: bool, number: int, repo: str
) -> str:
    """Keep ``common`` + the level block (+ ``submit``); drop markers and the rest.

    ``<N>`` becomes the issue number and ``<R>`` the origin repository (validated as
    ``owner/repo`` by the argument parser, so it carries no markup).
    """
    parts = BLOCK_MARKER.split(template)  # [preamble, name, body, name, body, ...]
    blocks = dict(zip(parts[1::2], parts[2::2]))
    wanted = ["common", level] + (["submit"] if submit else [])
    missing = [name for name in wanted if name not in blocks]
    if missing:
        raise ValueError(f"template has no block: {', '.join(missing)}")
    text = "\n\n".join(blocks[name].strip() for name in wanted) + "\n"
    return text.replace("<N>", str(number)).replace("<R>", repo)


def cmd_prompt(args: argparse.Namespace) -> int:
    if args.source:
        # A prompt that a running agent has read is kept, but only while that agent's
        # worktree still exists: a replacement worktree gets a freshly rendered prompt.
        source, common = Path(args.source), git_common_dir()
        record = read_record(source)
        if (
            record
            and isinstance(record.get("launch"), dict)
            and common
            and guarded_record_path(source, common)
            and Path(args.out).is_file()
        ):
            return emit({"status": "kept", "path": str(args.out)})
    try:
        template = Path(args.template).read_text(encoding="utf-8")
        text = render_prompt(template, args.level, args.submit, args.number, args.repo)
        atomic_write_text(Path(args.out), text)
    except (OSError, ValueError) as exc:
        return emit({"status": "failed", "detail": str(exc)})
    return emit({"status": "written", "path": str(args.out)})


# --- launch ---------------------------------------------------------------

# The launch record the enforcement hook of issue 394 reads. The agent cannot
# edit it: the hook consumes it by nonce, and the agent only sees the nonce.
PENDING_PARTS = (".claude", "state", "launch-level", "pending")
SHIM_MARKERS = ("[ccsession]", "Session name (Enter or Ctrl+C")
# The shim's text is on the screen for only about 1 to 2 seconds before Claude's
# interface draws over it, so a read can miss it. ccsession also names the session
# from the launch prompt's first words (sc-launch-v1-<nonce>) plus a stamp, and that
# name stays in the tab title, so the title is the signal that does not go away.
SHIM_TITLE = re.compile(r"sc-launch-v1-[0-9a-f]{1,12}-\d{4}-\d{6}-[0-9a-f]{4}\b")
SHIM_TRIES = 5
SHIM_INTERVAL_ENV = "SC_ORCA_SHIM_INTERVAL"
SHIM_INTERVAL = 2.0
HOOK_SCRIPT = ".claude/hooks/launch-level-guard.sh"
REMEDY = {
    "W-LAUNCH-FAILED": "re-run the claim; the hand command is printed for reference",
    "W-LAUNCH-NOT-CCSESSION": (
        "this agent is NOT behind the ccsession shim, or could not be verified; "
        "close it. Orca's Claude command must be the ccsession-orca wrapper"
    ),
    "W-ENFORCEMENT-ABSENT": (
        "the launch was refused and no agent was started; fix each condition "
        "named above (most are fixed by running superclaude install), then "
        "claim the issue again"
    ),
    "W-L2-ABSENT": (
        "the L2 pre-push hook is not in effect for this worktree, so the limits "
        "are enforced by the L1 guard only; the agent was started"
    ),
}
# IR-7 (design section 13) says refuse when L2 is not owned; the refusal stays
# off (owner decision OD-3), so the claim warns with l2_status's reason
# appended to this prefix and the launch goes ahead.
L2_ABSENT_WHY = "the owned L2 pre-push hook is not in effect for this worktree: "
# IR-4: what the claim checks before a governed launch. It reads files and the
# environment only and never edits any configuration.
GUARD_COMMAND = "~/.claude/hooks/launch-level-guard.sh"
IDENTITY_COMMAND = "~/.claude/hooks/launch-job-identity.sh"
GUARD_VERSION_LINE = "# launch-level-guard-version: 1"
L2_VERSION_LINE = "# launch-level-pre-push-version: 1"
GOVERNED_TOOLS = (
    "Bash",
    "Skill",
    "Agent",
    "Task",
    "Edit",
    "Write",
    "NotebookEdit",
    "Monitor",
    "Workflow",
    "RemoteTrigger",
    "SendMessage",
    "CronCreate",
    "CronDelete",
    "ScheduleWakeup",
    # The mcp__ branch of the design matcher: one name per keyword (each holds only
    # that keyword), so a registration that dropped any one of them is refused.
    "mcp__x__merge_it",
    "mcp__x__push_it",
    "mcp__x__commit_it",
    "mcp__x__pull_request_it",
    "mcp__x__create_or_update_file",
    "mcp__x__delete_file",
    "mcp__x__update_ref",
    "mcp__x__create_ref",
    "mcp__x__create_branch",
)
# External commands the guard script calls. A missing `cat` makes it read an empty
# payload and allow (the session runs ungoverned); the others fail closed or leave
# files behind, but a host without them cannot bind a session either.
GUARD_COMMANDS = ("cat", "sed", "tr", "mkdir", "mv", "ln", "rm")
FIRE_ALWAYS = (None, "", "*")
LINUX_FILES = ("/proc/self/stat", "/proc/sys/kernel/random/boot_id")
PR_GET_CHILD_SUBREAPER = 37  # linux/prctl.h


def process_interface_gaps() -> list[str]:
    """The process interfaces of the job identity hook that this host lacks.

    Read-only probes on the claim process itself: the /proc files, pidfd_open of
    its own pid, and the query form of the child-subreaper call.
    """
    if not sys.platform.startswith("linux"):
        return [f"sys.platform is {sys.platform}, not Linux"]
    gaps = [p for p in LINUX_FILES if not os.path.exists(p)]
    try:
        import ctypes

        libc = ctypes.CDLL(None, use_errno=True)
    except OSError:
        return gaps + ["pidfd_open", "prctl(PR_GET_CHILD_SUBREAPER)"]
    try:
        # libc, like the hook: some UV Python builds omit os.pidfd_open.
        fd = libc.pidfd_open(os.getpid(), 0)
        if fd < 0:
            gaps.append("pidfd_open")
        else:
            os.close(fd)
    except AttributeError:
        gaps.append("pidfd_open")
    try:
        flag = ctypes.c_int()
        if libc.prctl(PR_GET_CHILD_SUBREAPER, ctypes.byref(flag), 0, 0, 0) != 0:
            gaps.append("prctl(PR_GET_CHILD_SUBREAPER)")
    except AttributeError:
        gaps.append("prctl(PR_GET_CHILD_SUBREAPER)")
    return gaps


def home_dir() -> Path:
    return Path(os.environ.get("HOME") or Path.home())


def read_settings(path: Path, required: bool) -> tuple[dict, str | None]:
    """The settings object at ``path`` and why it could not be used, else None."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return (
            {},
            f"{path} does not exist (run superclaude install)" if required else None,
        )
    except (OSError, ValueError) as exc:
        return {}, f"{path} cannot be read as JSON: {exc} (fix that file)"
    if not isinstance(data, dict):
        return {}, f"{path} is not a JSON object (fix that file)"
    return data, None


def matchers_for(settings: dict, event: str, command: str) -> list[object]:
    """The matcher of every ``event`` registration that holds ``command``."""
    hooks = settings.get("hooks")
    groups = hooks.get(event) if isinstance(hooks, dict) else None
    found: list[object] = []
    for group in groups if isinstance(groups, list) else []:
        inner = group.get("hooks") if isinstance(group, dict) else None
        if isinstance(inner, list) and any(
            isinstance(h, dict) and h.get("command") == command for h in inner
        ):
            found.append(group.get("matcher"))
    return found


def fires_for(matcher: object, tool: str) -> bool:
    if matcher in FIRE_ALWAYS:
        return True
    if not isinstance(matcher, str):
        return False
    try:
        return re.search(matcher, tool) is not None
    except re.error:
        return False


def enforcement_preflight(wt: str) -> list[str]:
    """IR-4: every reason the launch-level guard would not be effective; [] if none.

    Only the claim process is seen: its HOME, PATH and environment, and the
    settings files on disk. The agent Orca starts may run with another one.
    """
    home = home_dir()
    stale = "run superclaude install --force to replace it"
    restale = "run superclaude install --force to replace the registration"
    failures: list[str] = []
    for tool in ("jq", "uv", *GUARD_COMMANDS):
        if shutil.which(tool) is None:
            failures.append(f"{tool} is not on PATH (install {tool})")
    gaps = process_interface_gaps()
    if gaps:
        failures.append(
            "this host lacks "
            + ", ".join(gaps)
            + ", which the job identity hook needs (governed launches are Linux only)"
        )
    script = home / HOOK_SCRIPT
    if not script.is_file():
        failures.append(f"{script} is not installed (run superclaude install)")
    else:
        if not os.access(script, os.X_OK):
            failures.append(f"{script} is installed but not executable ({stale})")
        try:
            lines = script.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            lines, why = [], f"cannot be read: {exc}"
        else:
            why = f"lacks the line '{GUARD_VERSION_LINE}'"
        if GUARD_VERSION_LINE not in (line.rstrip() for line in lines):
            failures.append(f"{script} is installed but stale: it {why} ({stale})")
    config = os.environ.get("CLAUDE_CONFIG_DIR")
    if config and os.path.realpath(os.path.expanduser(config)) != os.path.realpath(
        home / ".claude"
    ):
        failures.append(
            f"CLAUDE_CONFIG_DIR is {config}, not {home / '.claude'}, so the user "
            "settings checked here may not be the ones Claude Code loads (unset it "
            "or point it at $HOME/.claude)"
        )
    user_path = home / ".claude" / "settings.json"
    user, user_why = read_settings(user_path, required=True)
    failures += [user_why] if user_why else []
    files = [(user_path, user)]
    for name in ("settings.json", "settings.local.json"):
        path = Path(wt) / ".claude" / name
        data, why = read_settings(path, required=False)
        failures += [why] if why else []
        files.append((path, data))
    for path, data in files:
        if data.get("disableAllHooks") is True:
            failures.append(
                f"{path} sets disableAllHooks to true, so no hook runs (remove that "
                "setting; the claim never edits it)"
            )
    if not user_why:
        prompt = matchers_for(user, "UserPromptSubmit", GUARD_COMMAND)
        if not prompt:
            failures.append(
                f"{user_path} has no UserPromptSubmit registration of "
                f"{GUARD_COMMAND} (run superclaude install)"
            )
        elif not any(m in FIRE_ALWAYS or m == ".*" for m in prompt):
            failures.append(
                f"the UserPromptSubmit registration of {GUARD_COMMAND} in {user_path} "
                f"has a matcher that may stop it firing ({restale})"
            )
        tools = matchers_for(user, "PreToolUse", GUARD_COMMAND)
        missed = [t for t in GOVERNED_TOOLS if not any(fires_for(m, t) for m in tools)]
        if not tools:
            failures.append(
                f"{user_path} has no PreToolUse registration of {GUARD_COMMAND} "
                "(run superclaude install)"
            )
        elif missed:
            failures.append(
                f"the PreToolUse registration of {GUARD_COMMAND} in {user_path} "
                f"does not fire for {', '.join(missed)} ({restale})"
            )
        identity = matchers_for(user, "PreToolUse", IDENTITY_COMMAND)
        if not any(fires_for(m, "Bash") for m in identity):
            failures.append(
                f"{user_path} has no PreToolUse registration of {IDENTITY_COMMAND} "
                "that fires for Bash (run superclaude install"
                + (", with --force" if identity else "")
                + ")"
            )
    return failures


def l2_status(wt: str) -> tuple[str, str]:
    """IR-6, source §3.4: the L2 pre-push state of ``wt`` as (state, reason).

    ``owned`` (empty reason) only when the entry at the common hooks directory
    is the packaged version-1 hook and its data file matches; else ``absent``,
    ``conflict`` or ``unsupported`` with the reason. Read only: it never
    writes, never creates the hooks directory and never runs the hook or the
    selector (FR-042). ``install_l2`` reports its own precondition and
    packaged-hook failures, then reports through this same check.
    """
    env = clean_git_env()
    state, why, hooks = _l2_preconditions(wt, env, create=False)
    if hooks is None:
        return state, why
    if not os.path.lexists(hooks / "pre-push"):
        return "absent", L2_WHY_NO_HOOK
    why, packaged, expected = _l2_packaged()
    if why:
        return "absent", why
    return _l2_entry_verdict(hooks, expected, packaged)


def _l2_as_install(state: str, why: str, linked: bool = False) -> tuple[str, str]:
    """Map an ``l2_status`` answer to ``install_l2``'s states (FR-031 has no absent)."""
    if state == "owned":
        return ("installed" if linked else "owned"), ""
    return ("unavailable" if state == "absent" else state), why


# U-14(c): above the hook's 10 s selector bound, under DEFAULT_TIMEOUT.
L2_SELFTEST_TIMEOUT = 30.0
L2_DATA_NAME = "pre-push.launch-level"
_L2_VERSION_PREFIX = "# launch-level-pre-push-version:"
_GIT_ENV_DROP = (
    "GIT_DIR",
    "GIT_COMMON_DIR",
    "GIT_WORK_TREE",
    "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG_COUNT",
)
L2_WHY_HOOKSPATH = (
    "core.hooksPath is set, so git does not run hooks from the common hooks directory"
)
L2_WHY_CONFIG = "config-read-failed: git config core.hooksPath could not be read"
L2_WHY_GIT = "git-failed: git rev-parse failed (the path check needs git 2.31 or later)"
L2_WHY_HOOKS_DIR = "hooks-dir-unsafe"
L2_WHY_NO_UV = "uv was not found on PATH"
L2_WHY_NO_HOOK = "no pre-push hook"
L2_WHY_NOT_INSTALLED = (
    "the packaged pre-push hook is not installed (run superclaude install)"
)
L2_WHY_DATA_PATHS = "HOME or the uv directory is not a single-line absolute path"
# The selector line shapes the hook accepts (s1-s5, launch-level-pre-push.sh).
_L2_SELECTOR_RE = re.compile(
    r'\{"status": "ordinary"\}'
    r'|\{"status": "ordinary", "reason": "released"\}'
    r'|\{"status": "governed", "session_id": "[A-Za-z0-9][A-Za-z0-9_-]{0,127}"\}'
    r'|\{"status": "unknown"\}'
    r'|\{"status": "unknown", "reason": "(?:stale|orphaned|foreign|unreadable)",'
    r' "record": "/[^"\'\\\x00-\x1f\x7f]*"\}'
)
_L2_ZERO = "0" * 40
_L2_ONE = "1" * 40


def clean_git_env() -> dict[str, str]:
    """The environment without the variables that redirect git (source §6.3)."""
    return {
        k: v
        for k, v in os.environ.items()
        if k not in _GIT_ENV_DROP
        and not k.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))
    }


def publish_no_replace(dir_fd: int, name: str, data: bytes, mode: int) -> bool:
    """Write ``data`` as ``name`` in ``dir_fd`` only if no entry has that name.

    The bytes go to a private temporary file first and are hard-linked in, so
    a reader never sees a partial file and an existing entry is never
    replaced. False when ``name`` already exists.
    """
    tmp = f".{name}.{uuid.uuid4().hex}"
    fd = os.open(
        tmp,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
        dir_fd=dir_fd,
    )
    try:
        try:
            view = memoryview(data)
            while view:
                view = view[os.write(fd, view) :]
            os.fchmod(fd, mode)
            os.fsync(fd)
        finally:
            os.close(fd)
        try:
            os.link(
                tmp,
                name,
                src_dir_fd=dir_fd,
                dst_dir_fd=dir_fd,
                follow_symlinks=False,
            )
        except FileExistsError:
            return False
        return True
    finally:
        os.unlink(tmp, dir_fd=dir_fd)
        os.fsync(dir_fd)


def l2_data_expected() -> bytes | None:
    """The data file L2 needs: HOME on line 1, the uv directory on line 2.

    None when uv is not on PATH or a path is not absolute and single-line.
    """
    uv = shutil.which("uv")
    if not uv:
        return None
    home = str(home_dir())
    uv_dir = os.path.dirname(os.path.abspath(uv))
    for p in (home, uv_dir):
        if not os.path.isabs(p) or "\n" in p or "\r" in p:
            return None
    return f"{home}\n{uv_dir}\n".encode()


def _l2_packaged() -> tuple[str, bytes, bytes]:
    """(why, packaged hook bytes, expected data bytes); ``why`` empty when usable."""
    src = home_dir() / ".claude" / "hooks" / "launch-level-pre-push.sh"
    try:
        packaged = src.read_bytes() if not src.is_symlink() and src.is_file() else b""
    except OSError:
        packaged = b""
    if L2_VERSION_LINE.encode() not in packaged:
        return L2_WHY_NOT_INSTALLED, b"", b""
    if shutil.which("uv") is None:
        return L2_WHY_NO_UV, b"", b""
    expected = l2_data_expected()
    if expected is None:
        return L2_WHY_DATA_PATHS, b"", b""
    return "", packaged, expected


def _l2_data_ok(path: Path, expected: bytes) -> bool:
    """The data file is a regular file of ours, not group/other writable,
    holds exactly ``expected``, and its uv directory holds an executable uv."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        return False
    try:
        st = os.fstat(fd)
        if (
            not stat.S_ISREG(st.st_mode)
            or st.st_uid != os.geteuid()
            or st.st_mode & 0o022
        ):
            return False
        with os.fdopen(os.dup(fd), "rb") as f:
            data = f.read(len(expected) + 1)
    except OSError:
        return False
    finally:
        os.close(fd)
    if data != expected:
        return False
    uv = Path(expected.decode().split("\n")[1]) / "uv"
    return uv.is_file() and os.access(uv, os.X_OK)


def _l2_conflict(why: str, hooks: Path) -> str:
    return (
        f"{why}: remove both files with "
        f"`rm {hooks}/pre-push {hooks}/{L2_DATA_NAME}` and claim again; "
        "the claim never deletes them"
    )


def _l2_entry_verdict(hooks: Path, expected: bytes, packaged: bytes) -> tuple[str, str]:
    """Source §3.4 steps 5-11: what the existing ``hooks/pre-push`` entry is."""
    entry = hooks / "pre-push"
    try:
        st = entry.lstat()
    except OSError:
        return "absent", L2_WHY_NO_HOOK
    if not stat.S_ISREG(st.st_mode):
        return "conflict", _l2_conflict("symlink", hooks)
    if st.st_uid != os.geteuid():  # FR-102 forgery "wrong uid"
        return "conflict", _l2_conflict("wrong owner", hooks)
    if st.st_mode & 0o022:  # FR-102 forgery "wrong mode"
        return "conflict", _l2_conflict("group or other writable", hooks)
    try:
        body = entry.read_bytes()
    except OSError:
        return "conflict", _l2_conflict("foreign", hooks)
    if body != packaged:
        why = "stale" if _L2_VERSION_PREFIX.encode() in body else "foreign"
        return "conflict", _l2_conflict(why, hooks)
    if not os.access(entry, os.X_OK):
        return "conflict", _l2_conflict("not executable", hooks)
    if not _l2_data_ok(hooks / L2_DATA_NAME, expected):
        return "conflict", _l2_conflict("data-file-differs", hooks)  # OC-12
    return "owned", ""


def _l2_selftest(wt: str, staged: Path, data_copy: Path, env: Mapping[str, str]) -> str:
    """Source §3.3 T4: run the staged hook; '' on pass, else the failed step."""

    def hook(stdin: str) -> Result:
        return run(
            [str(staged), "origin", "origin"],
            timeout=L2_SELFTEST_TIMEOUT,
            cwd=wt,
            env=env,
            input=stdin,
        )

    def push(ref: str) -> str:
        return f"{ref} {_L2_ONE} {ref} {_L2_ZERO}\n"

    res = hook("")
    if not res.ok or res.err:
        return "empty-push"
    home = str(home_dir())
    uv_dir = os.path.dirname(os.path.abspath(shutil.which("uv") or "/"))
    sel = run(
        [
            "/usr/bin/env",
            "-i",
            f"HOME={home}",
            f"PATH={uv_dir}:/usr/bin:/bin",
            "UV_NO_CONFIG=1",
            "/usr/bin/timeout",
            "10",
            f"{home}/.claude/hooks/launch-job-identity.sh",
            "identify",
            str(os.getpid()),
        ],
        timeout=L2_SELFTEST_TIMEOUT,
        cwd="/",
        input="",
    )
    lines = sel.out.split("\n")
    if (
        not sel.ok
        or len(lines) != 2
        or lines[1] != ""
        or not _L2_SELECTOR_RE.fullmatch(lines[0])
    ):
        return "selector-env"
    if not hook(push("refs/heads/main")).ok:
        return "main-push"
    data_copy.unlink()
    for ref in ("refs/heads/main", "refs/heads/master"):
        res = hook(push(ref))
        if res.rc != 1 or "L2-UNKNOWN" not in res.err:
            return "no-data-refusal"
    if not hook(push("refs/heads/l2-selftest")).ok:
        return "no-data-refusal"
    return ""


def _l2_preconditions(
    wt: str, env: Mapping[str, str], create: bool = True
) -> tuple[str, str, Path | None]:
    """Source §3.3 S1 / §3.4: ('', '', hooks dir) when L2 can be checked, else a verdict.

    Verdicts use ``l2_status``'s states; a git failure is ``absent`` (FR-041),
    which ``install_l2`` reports as ``unsupported`` (FR-033, OC-10). Only
    ``create`` makes a missing hooks directory; without it a missing one is
    ``absent``.
    """
    git = ["git", "-C", wt]
    # The plain get also reads config.worktree when extensions.worktreeConfig
    # is on; `config --worktree` exits 128 in a linked worktree without it.
    res = run([*git, "config", "--get", "core.hooksPath"], env=env)
    if res.rc == 0 and not res.timed_out and not res.missing:
        return "unsupported", L2_WHY_HOOKSPATH, None
    if res.rc != 1 or res.timed_out or res.missing:
        return "absent", L2_WHY_CONFIG, None
    # Ask for the hooks directory, not hooks/pre-push: the absolute path format
    # resolves symlinks, so a symlinked pre-push would read as redirected and
    # never reach the entry check that reports it as a conflict.
    pp = run(
        [*git, "rev-parse", "--path-format=absolute", "--git-path", "hooks"],
        env=env,
    )
    common = run(
        [*git, "rev-parse", "--path-format=absolute", "--git-common-dir"], env=env
    )
    if not (pp.ok and common.ok and common.out.strip()):
        return "absent", L2_WHY_GIT, None
    hooks = Path(common.out.strip()) / "hooks"
    if pp.out.strip() != str(hooks):
        return "unsupported", f"git's pre-push hook path is not {hooks}/pre-push", None
    try:
        try:
            st = hooks.lstat()
        except FileNotFoundError:
            if not create:
                return "absent", L2_WHY_NO_HOOK, None
            try:
                os.mkdir(hooks, 0o755)
            except FileExistsError:
                pass
            st = hooks.lstat()
    except OSError:
        return "unsupported", L2_WHY_HOOKS_DIR, None
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.geteuid() or st.st_mode & 0o022:
        return "unsupported", L2_WHY_HOOKS_DIR, None
    return "", "", hooks


def install_l2(wt: str) -> tuple[str, str]:
    """Source §3.3: claim the L2 pre-push hook for ``wt``; (state, reason).

    ``installed`` or ``owned`` with an empty reason, else ``conflict``,
    ``unsupported`` or ``unavailable`` with a reason a person can act on. An
    existing entry is never replaced or deleted.
    """
    env = clean_git_env()
    state, why, hooks = _l2_preconditions(wt, env)
    if hooks is None:
        # With create=True, `absent` here is only a config or git failure:
        # FR-033 and OC-10 make that `unsupported`, nothing written.
        return ("unsupported" if state == "absent" else state), why
    why, packaged, expected = _l2_packaged()
    if why:
        return "unavailable", why
    entry = hooks / "pre-push"
    if os.path.lexists(entry):  # S2: the same check l2_status makes
        return _l2_as_install(*l2_status(wt))
    linked = False
    private: Path | None = None
    hooks_fd = priv_fd = -1
    try:
        hooks_fd = os.open(hooks, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        # S3: the data file, never replacing one that is already there.
        if not publish_no_replace(hooks_fd, L2_DATA_NAME, expected, 0o644):
            if not _l2_data_ok(hooks / L2_DATA_NAME, expected):
                return "conflict", _l2_conflict("data-file-differs", hooks)
        # S4: stage the hook and a data copy privately, then self-test.
        name = f".{uuid.uuid4().hex}"
        os.mkdir(name, 0o700, dir_fd=hooks_fd)
        private = hooks / name
        priv_fd = os.open(
            name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=hooks_fd
        )
        publish_no_replace(priv_fd, "pre-push", packaged, 0o755)
        publish_no_replace(priv_fd, L2_DATA_NAME, expected, 0o644)
        failed = _l2_selftest(wt, private / "pre-push", private / L2_DATA_NAME, env)
        if failed:
            return "unavailable", f"the hook self-test failed at step {failed}"
        # S5: link the tested hook in; a racing writer keeps its entry.
        try:
            os.link(private / "pre-push", entry, follow_symlinks=False)
            linked = True
        except FileExistsError:
            linked = False
    except OSError as e:
        return "unavailable", f"write failed: {e.strerror}"
    finally:
        if private is not None:
            shutil.rmtree(private, ignore_errors=True)
        for fd in (priv_fd, hooks_fd):
            if fd >= 0:
                os.close(fd)
    # S6: report what is there now, through the read-only check (a raced
    # delete reads absent, which install_l2 reports as unavailable).
    return _l2_as_install(*l2_status(wt), linked=linked)


def session_report(
    wt: str, l2: tuple[str, str], inode: int | None = None
) -> tuple[str, list[str]]:
    """IR-6: how a person releases the launched session, and one line per layer.

    Called only after the IR-4 preflight passed, so L1 is effective. ``l2`` is
    the (state, reason) l2_status() answer the launch already used, so both
    always agree.
    """
    store = home_dir().joinpath(*PENDING_PARTS[:-1])
    if inode is None:
        find = (
            "the claim could not read its record's inode number, so check which "
            "session file belongs to this launch before removing anything"
        )
    else:
        find = (
            f"this launch's record has inode number {inode}: run ls -i on the "
            f"sessions folder and take the name whose number is {inode} (once the "
            "agent has read its first prompt the guard keeps the session file as a "
            "hard link of this record, so the number matches); if no name has that "
            "number, the session was bound another way, so check which session "
            "file belongs to this launch before removing anything"
        )
    release = (
        "to release this session, a person runs in their own terminal: "
        f'rm "{store}/sessions/<session id>" "{store}/sessions/<session id>.ok" '
        "(every file in the sessions folder is named by a session id and holds "
        "only the level word, and a name ending in .ok is an approval; the launch "
        f"does not print the id; {find}; a guard block about touching the "
        "launch-level state prints the exact rm command)"
    )
    state, reason = l2
    l2_line = (
        "L2 pre-push: owned (the launch-level pre-push hook, version 1, refuses "
        "this session's pushes to main and master)"
        if state == "owned"
        else f"L2 pre-push: {state} ({reason}; the limits are enforced by the "
        "L1 guard only)"
    )
    return release, ["L1 guard: effective (the IR-4 preflight passed)", l2_line]


def publish_pending(word: str) -> tuple[str, Path]:
    """Write ``pending/<nonce>`` (mode 0600, directories 0700); return nonce, path."""
    base = home_dir()
    for part in PENDING_PARTS:
        base = base / part
        if base.is_symlink():
            raise OSError(f"{base} is a symlink")
        if not base.exists():
            os.mkdir(base, 0o700)
            os.chmod(base, 0o700)
        elif not base.is_dir():
            raise OSError(f"{base} is not a directory")
        elif part != PENDING_PARTS[0]:
            os.chmod(base, 0o700)
    nonce = secrets.token_hex(16)
    tmp = base / f".tmp-{nonce}"
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as handle:
            handle.write(word)
        os.replace(tmp, base / nonce)
    except OSError:
        tmp.unlink(missing_ok=True)
        raise
    return nonce, base / nonce


def find_handle(node: object) -> str | None:
    """First string value under a key named ``handle``, by a recursive walk."""
    if isinstance(node, dict):
        value = node.get("handle")
        if isinstance(value, str) and value:
            return value
        children = list(node.values())
    elif isinstance(node, list):
        children = node
    else:
        return None
    for child in children:
        found = find_handle(child)
        if found:
            return found
    return None


def shim_interval() -> float:
    try:
        return max(0.0, float(os.environ.get(SHIM_INTERVAL_ENV, SHIM_INTERVAL)))
    except ValueError:
        return SHIM_INTERVAL


def ccsession_title(handle: str) -> bool:
    """True when the terminal's tab title carries the name ccsession gave the launch."""
    res = run(
        ["orca", "terminal", "show", "--terminal", handle, "--json"],
        TERMINAL_READ_TIMEOUT,  # not the 120 s default: this runs after every screen miss
    )
    data = parse_json(res.out) if res.ok else None
    result = data.get("result") if isinstance(data, dict) else None
    terminal = result.get("terminal") if isinstance(result, dict) else None
    title = terminal.get("title") if isinstance(terminal, dict) else None
    return isinstance(title, str) and SHIM_TITLE.search(title) is not None


def behind_ccsession(handle: str) -> bool:
    """Look up to five times for the shim's screen text or its session name in the title."""
    for attempt in range(SHIM_TRIES):
        res = run(
            ["orca", "terminal", "read", "--terminal", handle, "--screen", "--json"],
            TERMINAL_READ_TIMEOUT,
        )
        data = parse_json(res.out) if res.ok else None
        result = data.get("result") if isinstance(data, dict) else None
        terminal = result.get("terminal") if isinstance(result, dict) else None
        tail = terminal.get("tail") if isinstance(terminal, dict) else None
        if isinstance(tail, list):
            tail = "\n".join(str(line) for line in tail)
        if isinstance(tail, str) and any(m in tail for m in SHIM_MARKERS):
            return True
        if ccsession_title(handle):
            return True
        if attempt < SHIM_TRIES - 1:
            time.sleep(shim_interval())
    return False


def launch_mirror(wt: str, number: int) -> Path | None:
    """Where the worktree itself remembers a launch: a file in its own git directory.

    It is untracked by construction, never inside the working tree, and disappears
    with the worktree, so a claim run from the worktree (or from another checkout
    with a fresh record) still sees that an agent was started there.
    """
    res = run(["git", "-C", wt, "rev-parse", "--absolute-git-dir"])
    out = res.out.strip()
    if not res.ok or not out:
        return None
    return Path(out) / f"sc-issue-launch-{number}.json"


def read_mirror(wt: str, number: int) -> tuple[Path | None, dict | None]:
    """The mirror path and its ``launch`` entry (only when it names this worktree)."""
    path = launch_mirror(wt, number)
    if path is None:
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return path, None
    if (
        isinstance(data, dict)
        and isinstance(data.get("launch"), dict)
        and isinstance(data.get("path"), str)
        and real(data["path"]) == real(wt)
    ):
        return path, data["launch"]
    return path, None


def record_launch(
    source: Path, level: str, submit: bool, at: str, wt: str, number: int
) -> list[str]:
    """Write the ``launch`` entry to the source record and to the worktree mirror.

    Returns one message per file that could not be written.
    """
    entry = {"level": level, "submit": submit, "at": at}
    errors: list[str] = []
    record = read_record(source) or {}
    record["launch"] = entry
    try:
        atomic_write_text(source / RECORD_NAME, json.dumps(record, indent=2) + "\n")
    except OSError as exc:
        errors.append(f"{source / RECORD_NAME}: {exc}")
    mirror = launch_mirror(wt, number)
    if mirror is None:
        errors.append(f"{wt}: could not find the worktree's git directory")
    else:
        body = json.dumps({"path": wt, "launch": entry}, indent=2) + "\n"
        try:
            atomic_write_text(mirror, body)
        except OSError as exc:
            errors.append(f"{mirror}: {exc}")
    return errors


def launch_result(status: str, notes: list[tuple[str, str]], **fields: object) -> dict:
    """One launch JSON object; ``warning`` is the first code, the rest go in detail."""
    warning = notes[0][0] if notes else None
    parts = [f"{notes[0][1]} ({REMEDY[warning]})"] if notes else []
    parts += [f"also {c}: {t} ({REMEDY[c]})" for c, t in notes[1:]]
    base: dict = {
        "status": status,
        "warning": warning,
        "detail": "; ".join(parts),
        "terminal": None,
        "launched_at": None,
        "enforcement_hook": None,
        "hand_command": None,
        "release": None,
        "layers": None,
    }
    base.update(fields)
    return base


def stale_prompt(source: Path, wt: Path, number: int) -> str | None:
    """Why the worktree's launch prompt is not the one rendered for this claim, else None.

    The copy never overwrites a tracked file, so the worktree can hold an older,
    possibly more permissive prompt than ``<source>/launch-prompt.md``.
    """
    rel = f".dev/issues/{number}/launch-prompt.md"
    mine, theirs = source / "launch-prompt.md", wt / rel
    bad = first_symlink(wt, theirs.parent)
    try:
        if bad is not None or theirs.is_symlink():
            why = f"{bad or theirs} is a symlink"
        elif not mine.is_file():
            why = f"no prompt was rendered at {mine}"
        elif not theirs.is_file():
            why = "the file is missing there"
        elif filecmp.cmp(mine, theirs, shallow=False):
            return None
        else:
            why = f"it differs from {mine}"
    except OSError as exc:
        why = str(exc)
    return (
        f"{rel} in the worktree is not the launch prompt rendered for this claim "
        f"({why}), so no agent was started: it would follow another prompt. Make "
        f"that file match {mine} (a tracked copy needs git rm or git checkout), "
        "then re-run the claim"
    )


def cmd_launch(args: argparse.Namespace) -> int:
    source, number = Path(args.source), args.number
    failed = "W-LAUNCH-FAILED"
    main_common = git_common_dir()
    wt = guarded_record_path(source, main_common) if main_common else None
    if wt is None:
        return emit(launch_result("failed", [(failed, "no usable worktree record")]))
    record = read_record(source) or {}
    mirror_path, mirrored = read_mirror(wt, number)
    earlier = record.get("launch")
    if not isinstance(earlier, dict):
        earlier = mirrored
    if isinstance(earlier, dict):
        at = str(earlier.get("at") or "")
        files = [str(source / RECORD_NAME)] + (
            [str(mirror_path)] if mirror_path else []
        )
        return emit(
            launch_result(
                "already_launched",
                [],
                detail=f"agent already launched at {at}; to launch again, remove the "
                f"launch entry from {' and from '.join(files)}",
                launched_at=at or None,
            )
        )
    stale = stale_prompt(source, Path(wt), number)
    if stale:
        return emit(launch_result("failed", [(failed, stale)]))
    # Order: the already-launched and stale-prompt checks above come first, the
    # IR-4 preflight next, and only then publish_pending, so a refusal leaves no
    # launch record and starts no agent. enforcement_hook in the result means:
    # "installed" the preflight passed, "missing" it failed and the launch was
    # refused, null (the launch_result default) no preflight ran.
    absent = enforcement_preflight(wt)
    if absent:
        return emit(
            launch_result(
                "failed",
                [
                    (
                        "W-ENFORCEMENT-ABSENT",
                        "the launch-level guard would not be effective: "
                        + "; ".join(absent)
                        + ". This check verified the claim process only (its "
                        "HOME, PATH, environment and the settings files on "
                        "disk), not the environment the agent would run in",
                    )
                ],
                enforcement_hook="missing",
            )
        )
    hook = "installed"
    notes: list[tuple[str, str]] = []
    # Source §3.2 steps 4-6, before publish_pending: claim the L2 hook (its
    # answer is advisory), re-check it read-only (that answer is the one the
    # launch reports), and warn when it is not owned. IR-7 stays a warning
    # (owner decision OD-3; the off IR7_REFUSE switch comes in a later commit).
    install_l2(wt)
    l2, l2_reason = l2_status(wt)
    l2_notes = [("W-L2-ABSENT", L2_ABSENT_WHY + l2_reason)] if l2 != "owned" else []
    word = "full-submit" if args.submit else args.level
    try:
        nonce, pending = publish_pending(word)
        # The guard keeps the bound session file as a hard link of this record, so
        # its inode number picks this launch's session file out of the sessions folder.
        try:
            inode: int | None = pending.stat().st_ino
        except OSError:
            inode = None
    except OSError as exc:
        return emit(
            launch_result(
                "failed",
                [(failed, f"could not write the launch record: {exc}")],
                enforcement_hook=hook,
            )
        )
    text = f"Read .dev/issues/{number}/launch-prompt.md and follow it."
    argv = ["orca", "agent", "launch", "--agent", "claude", "--worktree"]
    argv += [f"path:{wt}", "--surface", "terminal", "--prompt"]
    marked = argv + [f"[sc-launch:v1:{nonce}] {text}", "--json"]
    res = run(marked)
    data = parse_json(res.out) if res.ok else None
    if not res.ok or not isinstance(data, dict) or data.get("ok") is not True:
        pending.unlink(missing_ok=True)
        if res.timed_out:
            why = "orca agent launch timed out; an agent may have started, check Orca before re-running"
        elif res.ok:
            why = "orca agent launch did not report ok"
        else:
            why = f"orca agent launch failed: {res.first_error_line()}"
        hand = shlex.join(argv + [text, "--json"]) + (
            "  # an agent started by hand is not governed by the launch-level hook; "
            "re-running the claim is preferred"
        )
        return emit(
            launch_result(
                "failed",
                [(failed, why)],
                enforcement_hook=hook,
                hand_command=hand,
            )
        )
    handle = find_handle(data)
    if handle is None or not behind_ccsession(handle):
        notes.append(
            (
                "W-LAUNCH-NOT-CCSESSION",
                "the agent's screen showed no ccsession text"
                if handle
                else "the launch result named no terminal",
            )
        )
    at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    unrecorded = ""
    problems = record_launch(source, args.level, args.submit, at, wt, number)
    if problems:
        # The agent is running, so "re-run the claim" would start a second one.
        unrecorded = (
            f"the agent is running but its launch was not fully recorded "
            f"({'; '.join(problems)}); do not re-run the claim, add the launch entry "
            f"to {source / RECORD_NAME} by hand"
        )
    release, layers = session_report(wt, (l2, l2_reason), inode)
    result = launch_result(
        "launched",
        notes + l2_notes,  # the ccsession warning, when any, stays first
        terminal=handle,
        launched_at=at,
        enforcement_hook=hook,
        release=release,
        layers=layers,
    )
    if unrecorded:
        result["detail"] = "; ".join(filter(None, [result["detail"], unrecorded]))
    return emit(result)


def issue_number(text: str) -> int:
    if not text.isdigit() or int(text) < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return int(text)


def repo_name(text: str) -> str:
    if not re.fullmatch(
        r"[A-Za-z0-9_][A-Za-z0-9._-]*/[A-Za-z0-9_][A-Za-z0-9._-]*", text
    ):
        raise argparse.ArgumentTypeError("must look like owner/repo")
    return text


def origin_ref(text: str) -> str:
    if not re.fullmatch(r"origin/[A-Za-z0-9._/-]+", text):
        raise argparse.ArgumentTypeError("must look like origin/<branch>")
    return text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="orca_worktree.py",
        description="Orca worktree and agent-launch steps of /sc:issue --claim.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    pre = sub.add_parser("preflight", help="check that the Orca runtime is reachable")
    pre.set_defaults(func=cmd_preflight)
    wt = sub.add_parser("worktree", help="create or reuse the worktree issue-<N>")
    wt.add_argument("--repo", required=True, type=repo_name)
    wt.add_argument("--number", required=True, type=issue_number)
    wt.add_argument("--base", required=True, type=origin_ref)
    wt.add_argument("--source", required=True)
    wt.set_defaults(func=cmd_worktree)
    pr = sub.add_parser("prompt", help="render launch-prompt.md from the template")
    pr.add_argument("--template", required=True)
    pr.add_argument("--level", required=True, choices=["worktree", "full"])
    pr.add_argument("--submit", action="store_true")
    pr.add_argument("--number", required=True, type=issue_number)
    pr.add_argument("--repo", required=True, type=repo_name)
    pr.add_argument("--source", help="issue folder; keeps the prompt of a live launch")
    pr.add_argument("--out", required=True)
    pr.set_defaults(func=cmd_prompt)
    la = sub.add_parser("launch", help="launch one agent in the issue worktree")
    la.add_argument("--number", required=True, type=issue_number)
    la.add_argument("--source", required=True)
    la.add_argument("--level", required=True, choices=["worktree", "full"])
    la.add_argument("--submit", action="store_true")
    la.set_defaults(func=cmd_launch)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command in ("prompt", "launch") and args.submit and args.level != "full":
        parser.error("--submit needs --level full")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
