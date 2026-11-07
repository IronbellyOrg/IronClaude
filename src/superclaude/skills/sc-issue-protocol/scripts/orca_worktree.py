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
file never commits, pushes, stages or removes anything.

``prompt --template <file> --level worktree|full [--submit] --number <N>
--repo <owner/repo> --out <file>`` renders ``launch-prompt.md`` from the four blocks of
``templates/launch-prompt.md`` (``common``, the level block, ``submit`` with
``--submit``) and prints ``{"status": "written", "path": "<out>"}``. ``--submit``
with ``--level worktree`` is a bad argument (exit 2).

``launch --number <N> --source <D> --level worktree|full [--submit]`` starts one
Claude Code agent in the worktree recorded in ``<D>/worktree.json``. It first
publishes the launch record the enforcement hook reads
(``$HOME/.claude/state/launch-level/pending/<nonce>``, one word), then runs
``orca agent launch --surface terminal`` with a prompt that starts with
``[sc-launch:v1:<nonce>]``, checks the agent's screen for the ccsession shim, and
writes a ``launch`` entry into ``worktree.json``. It prints ``{status, warning,
detail, terminal, launched_at, enforcement_hook, hand_command}`` with ``status``
``launched``, ``failed`` or ``already_launched``.
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
import subprocess
import sys
import tempfile
import time
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
    argv: list[str], timeout: float = DEFAULT_TIMEOUT, cwd: str | None = None
) -> Result:
    """Run ``argv`` without a shell; return a failed Result on any problem."""
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=_timeout(timeout),
            check=False,
            cwd=cwd,
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
        "the level is an instruction in the prompt only until the launch-level "
        "hook (#394) ships; do not use full or --submit on a real issue yet"
    ),
}


def home_dir() -> Path:
    return Path(os.environ.get("HOME") or Path.home())


def enforcement_status() -> str:
    """``installed`` when the hook script exists and is executable, else ``missing``."""
    hook = home_dir() / HOOK_SCRIPT
    return "installed" if hook.is_file() and os.access(hook, os.X_OK) else "missing"


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


def behind_ccsession(handle: str) -> bool:
    """Read the agent's screen up to five times, looking for the shim's text."""
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
    }
    base.update(fields)
    return base


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
    hook = enforcement_status()
    notes: list[tuple[str, str]] = []
    word = "full-submit" if args.submit else args.level
    try:
        nonce, pending = publish_pending(word)
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
    if hook == "missing":
        notes.append(
            ("W-ENFORCEMENT-ABSENT", "the launch-level hook script is not installed")
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
    result = launch_result(
        "launched",
        notes,
        terminal=handle,
        launched_at=at,
        enforcement_hook=hook,
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
