#!/usr/bin/env python3
"""Fail-closed archiver for managed TASK-WF task packages (sc:implement).

Moves ``.dev/tasks/to-do/<id>`` to ``.dev/tasks/done/<id>`` with Linux
``renameat2(RENAME_NOREPLACE)`` (stdlib ctypes). There is no copy, ``mv``,
``os.rename`` or mkdir-then-rename fallback: unsupported platform/libc/kernel/
filesystem, EINVAL, ENOSYS and EXDEV all fail closed with source intact.

Modes (stdout is one JSON object; failures print ``E-ARCHIVE-*`` on stderr, exit 1):

  archive_workspace.py --package <to-do/<id>> [--root <checkout>]
      validate + archive (default)
  archive_workspace.py --package <pkg> --print-state
      read-only: validate everything except FINAL/ARCHIVE state and print the
      ``state`` digest the fresh FINAL review must record
  archive_workspace.py --package <pkg> --clear-marker <token>
      operator-confirmed removal of a leftover ``.archiving`` marker (token is in
      ``<pkg>/.archiving/owner``). Never moves anything, never infers liveness.

The caller (sc:implement) must have joined every writer first; concurrent writers
for one package, or non-cooperating checkout writers, are unsupported.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import json
import os
import re
import secrets
import sys
from pathlib import Path

AT_FDCWD = -100
RENAME_NOREPLACE = 1
MARKER = ".archiving"
# subject: lower camelCase, 1-16 ASCII chars, first a lowercase letter, no hyphens.
# The tasklist file is exactly "<id>.md" (the full directory basename).
ID_RE = re.compile(r"^TASK-WF-[a-z][A-Za-z0-9]{0,15}-\d{8}-\d{6}(?:-[2-9])?$")
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
_FINAL = re.compile(r"^FINAL: (\S+)(?: .*)?$")
_FINAL_OK = re.compile(r"^FINAL: pass evidence=(.+) state=([0-9a-f]{64})$")
_ARCH = re.compile(r"^ARCHIVE: (start|failed|Ruling:) .+$")
_ARCH_RULING = re.compile(r"^ARCHIVE: Ruling: (.+) — (.+) — (.+)$")
_TASK_HEADING = re.compile(
    r"^#{2,6}\s+(?:Task\s+|T)([0-9][0-9A-Za-z.-]*?)(?::|\s|$)", re.M
)


class ArchiveError(Exception):
    def __init__(self, code: str, msg: str):
        super().__init__(msg)
        self.code, self.msg = code, msg


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --- the only movement primitive ------------------------------------------------
def rename_noreplace(src: str, dst: str, _libc=None) -> None:
    """renameat2(AT_FDCWD, src, AT_FDCWD, dst, RENAME_NOREPLACE) or raise ArchiveError."""
    if _libc is None and not sys.platform.startswith("linux"):
        raise ArchiveError(
            "E-ARCHIVE-PLATFORM", "archiving needs Linux renameat2; no fallback"
        )
    try:
        fn = (_libc or ctypes.CDLL(None, use_errno=True)).renameat2
    except (OSError, AttributeError) as exc:
        raise ArchiveError("E-ARCHIVE-PLATFORM", f"libc renameat2 unavailable: {exc}")
    fn.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    fn.restype = ctypes.c_int
    if (
        fn(AT_FDCWD, os.fsencode(src), AT_FDCWD, os.fsencode(dst), RENAME_NOREPLACE)
        == 0
    ):
        return
    err = ctypes.get_errno()
    name = errno.errorcode.get(err, str(err))
    if err in (errno.EEXIST, errno.ENOTEMPTY):
        raise ArchiveError(
            "E-ARCHIVE-DEST", f"destination exists (no-replace, {name}): {dst}"
        )
    if err in (errno.ENOSYS, errno.EINVAL, errno.EXDEV, errno.ENOTSUP):
        raise ArchiveError(
            "E-ARCHIVE-PLATFORM",
            f"no-replace move unsupported or cross-filesystem ({name}); nothing moved, no fallback",
        )
    raise ArchiveError(
        "E-ARCHIVE-MOVE", f"renameat2 failed ({name}): {os.strerror(err)}"
    )


# --- location / containment ------------------------------------------------------
class Loc:
    def __init__(self, root: Path, package: str):
        self.root = Path(os.path.realpath(root))
        if not (self.root / ".git").exists():
            raise ArchiveError(
                "E-ARCHIVE-SOURCE", f"{self.root} is not a checkout root (.git missing)"
            )
        tasks = self.root / ".dev" / "tasks"
        for d in (self.root / ".dev", tasks, tasks / "to-do", tasks / "done"):
            if (
                os.path.islink(d)
                or (os.path.lexists(d) and not os.path.isdir(d))
                or (not os.path.lexists(d) and d.name != "done")
            ):
                raise ArchiveError(
                    "E-ARCHIVE-SOURCE", f"{d} must be a real directory (no symlink)"
                )
        pkg = Path(os.path.abspath(package))
        self.id = pkg.name
        self.todo, self.done = tasks / "to-do" / self.id, tasks / "done" / self.id
        if not ID_RE.match(self.id):
            raise ArchiveError(
                "E-ARCHIVE-SOURCE", f"not a TASK-WF package id: {self.id}"
            )
        if os.path.realpath(pkg.parent) not in (
            str(tasks / "to-do"),
            str(tasks / "done"),
        ):
            raise ArchiveError(
                "E-ARCHIVE-SOURCE",
                f"{pkg} is not a direct child of to-do/done in {self.root}",
            )

    @staticmethod
    def real_dir(p: Path) -> bool:
        return os.path.isdir(p) and not os.path.islink(p)


# --- package/ledger validation ---------------------------------------------------
def _kv(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        k, sep, v = line.partition(":")
        if sep and not line.startswith((" ", "-", "#")):
            out[k.strip()] = v.strip().strip("\"'")
    return out


def _front(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return _kv(m.group(1)) if m else {}


def _parse_ledger(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        raise ArchiveError("E-ARCHIVE-LEDGER", "ledger last line truncated")
    recs = []
    for i, line in enumerate(text.splitlines()):
        for kind, rx in (
            ("header", _HEADER),
            ("plan", _PLAN),
            ("start", _START),
            ("verdict", _VERDICT),
            ("ruling", _RULING),
            ("final", _FINAL),
            ("archive", _ARCH),
        ):
            m = rx.match(line)
            if m:
                break
        else:
            raise ArchiveError("E-ARCHIVE-LEDGER", f"unparseable ledger line {i + 1}")
        if (i == 0) != (kind == "header"):
            raise ArchiveError("E-ARCHIVE-LEDGER", "header must be line 1 only")
        recs.append((kind, m, line))
    if not recs:
        raise ArchiveError("E-ARCHIVE-LEDGER", "empty ledger")
    return recs


def _digest(root: Path, plan_sha: str, source_sha: str, files: list[str]) -> str:
    h = hashlib.sha256(f"plan {plan_sha}\nsource {source_sha}\n".encode())
    for rel in sorted(files):
        p = root / rel
        if os.path.isabs(rel) or ".." in Path(rel).parts or not rel:
            raise ArchiveError(
                "E-ARCHIVE-LEDGER", f"unsafe delivery path in ledger: {rel!r}"
            )
        if not Path(os.path.realpath(p.parent)).is_relative_to(root):
            raise ArchiveError(
                "E-ARCHIVE-LEDGER", f"delivery path escapes checkout: {rel}"
            )
        if os.path.islink(p):
            d = "link:" + os.readlink(p)
        elif p.is_dir():
            sub = hashlib.sha256()
            for dp, dn, fn in os.walk(p):
                dn[:] = sorted(x for x in dn if x != ".git")
                for name in sorted(dn + fn):
                    q = Path(dp) / name
                    if q.is_symlink():
                        value = "link:" + os.readlink(q)
                    elif q.is_file():
                        value = "file:" + _sha(q)
                    elif q.is_dir():
                        value = "dir"
                    else:
                        raise ArchiveError(
                            "E-ARCHIVE-LEDGER", f"unsupported delivery entry: {q}"
                        )
                    sub.update(f"{q.relative_to(p)}\0{value}\n".encode())
            d = "dir:" + sub.hexdigest()
        elif p.is_file():
            d = _sha(p)
        else:
            d = "absent"
        h.update(f"{rel}\0{d}\n".encode())
    return h.hexdigest()


def validate(
    loc: Loc,
    pkg: Path,
    *,
    allow_marker: bool = False,
    need_final: bool = True,
    archived: bool = False,
) -> dict:
    """Return {'plan','source','files','digest','ledger_sha'} or raise ArchiveError.

    ``archived=True`` validates a package already at done/: the ledger must end with
    this id's ``ARCHIVE: start`` (legitimately after FINAL) and a qualifying FINAL
    must precede it; the delivery digest is not re-compared (later work may move on).
    """
    if not Loc.real_dir(pkg):
        raise ArchiveError("E-ARCHIVE-SOURCE", f"{pkg} is not a real directory")
    if os.path.lexists(pkg / MARKER) and not allow_marker:
        raise ArchiveError(
            "E-ARCHIVE-MARKER",
            f"{pkg / MARKER} exists; never reclaimed automatically. Confirm the owner stopped, then "
            f"run with --clear-marker <token from {pkg / MARKER / 'owner'}>",
        )
    for name in (f"{loc.id}.md", "source.md", "return-contract.yaml", "progress.md"):
        f = pkg / name
        if os.path.islink(f) or not f.is_file():
            raise ArchiveError(
                "E-ARCHIVE-PACKAGE", f"{name} must be a regular file in the package"
            )
    if os.path.lexists(pkg / "artifacts") and not Loc.real_dir(pkg / "artifacts"):
        raise ArchiveError("E-ARCHIVE-PACKAGE", "artifacts must be a real directory")
    plan_text = (pkg / f"{loc.id}.md").read_text(encoding="utf-8")
    fm = _front(plan_text)
    if fm.get("schema") != "workflow-plan/1.2" or fm.get("slug") != loc.id:
        raise ArchiveError(
            "E-ARCHIVE-PACKAGE",
            "plan must be schema workflow-plan/1.2 with slug == package id",
        )
    contract = _kv((pkg / "return-contract.yaml").read_text(encoding="utf-8"))
    if (
        contract.get("contract_version") != "1.1"
        or contract.get("slug") != loc.id
        or contract.get("status") not in ("success", "partial")
    ):
        raise ArchiveError(
            "E-ARCHIVE-PACKAGE",
            "contract must be 1.1, same slug, status success|partial",
        )
    plan_sha, source_sha = _sha(pkg / f"{loc.id}.md"), _sha(pkg / "source.md")
    tasks = [f"T{m.group(1)}" for m in _TASK_HEADING.finditer(plan_text)]
    if not tasks or len(set(tasks)) != len(tasks):
        raise ArchiveError("E-ARCHIVE-TASKS", "plan needs unique '## Task N' headings")
    recs = _parse_ledger(pkg / "progress.md")
    idx = {
        k: [i for i, r in enumerate(recs) if r[0] == k]
        for k in ("plan", "start", "verdict", "ruling", "final", "archive")
    }
    # pins: append-only before the first start record; latest pin must match disk
    if not idx["plan"]:
        raise ArchiveError("E-ARCHIVE-PIN", "ledger has no PLAN pin")
    if idx["start"] and idx["plan"][-1] > idx["start"][0]:
        raise ArchiveError("E-ARCHIVE-PIN", "PLAN pin after first start record")
    if recs[idx["plan"][-1]][1].groups() != (plan_sha, source_sha):
        raise ArchiveError(
            "E-ARCHIVE-PIN", "plan/source changed since pinned (E-PLAN-CHANGED)"
        )
    # tasks
    known = set(tasks)
    latest, ruled = {}, set()
    for i, (k, m, _) in enumerate(recs):
        if k in ("start", "verdict", "ruling") and f"T{m.group(1)}" not in known:
            raise ArchiveError(
                "E-ARCHIVE-LEDGER", f"ledger names unknown task T{m.group(1)}"
            )
        if k == "ruling":
            ruled.add(m.group(1))
        if k == "verdict":
            tid = m.group(1)
            if (
                m.group(3) != "compliant"
                and m.group(2) == "complete"
                and tid not in ruled
            ):
                raise ArchiveError(
                    "E-ARCHIVE-TASKS",
                    f"T{tid} complete non-compliant without operator Ruling",
                )
            latest[tid] = (m.group(2), m.group(3))
    waive = []
    for t in tasks:
        st = latest.get(t[1:])
        if st is None or st[0] != "complete":
            raise ArchiveError("E-ARCHIVE-TASKS", f"{t} is pending or blocked")
        if st[1] != "compliant":
            waive.append(t[1:])
    archive_rulings = [
        r.group(1)
        for k, _, line in recs
        if k == "archive" and (r := _ARCH_RULING.match(line))
    ]
    for tid in waive:
        rx = re.compile(rf"(?<![0-9A-Za-z.-])T{re.escape(tid)}(?![0-9A-Za-z.-])")
        if not any(rx.search(w) for w in archive_rulings):
            raise ArchiveError(
                "E-ARCHIVE-TASKS",
                f"T{tid} non-compliant: needs operator 'ARCHIVE: Ruling:' naming it",
            )
    delivery_files = set()
    for k, m, _ in recs:
        if k != "verdict":
            continue
        for f in m.group(6).split(","):
            if f.startswith("./"):
                if not f.startswith("./artifacts/") or ".." in Path(f).parts:
                    raise ArchiveError(
                        "E-ARCHIVE-LEDGER",
                        f"ambiguous package-relative delivery path: {f!r}; use a repo-relative path",
                    )
                continue
            if f:
                delivery_files.add(f)
    files = sorted(delivery_files)
    digest = _digest(loc.root, plan_sha, source_sha, files)
    if need_final:
        body = recs
        if archived:
            last = recs[-1]
            if last[0] != "archive" or not last[2].startswith(
                f"ARCHIVE: start id={loc.id} "
            ):
                raise ArchiveError(
                    "E-ARCHIVE-PACKAGE",
                    "archived package ledger must end with its own 'ARCHIVE: start'",
                )
            body = recs[:-1]
        last_other = max(i for i, r in enumerate(body) if r[0] != "final")
        finals = idx["final"]
        if not finals or finals[-1] < last_other:
            raise ArchiveError(
                "E-ARCHIVE-FINAL",
                "no fresh FINAL after the latest plan/task/ARCHIVE record",
            )
        fl = recs[finals[-1]][2]
        ok = _FINAL_OK.match(fl)
        if not ok:
            raise ArchiveError(
                "E-ARCHIVE-FINAL",
                f"latest FINAL is not 'pass evidence=… state=<sha256>': {fl}",
            )
        if ok.group(2) != digest and not archived:
            raise ArchiveError(
                "E-ARCHIVE-FINAL",
                "FINAL state digest is stale (plan/source/delivery files changed)",
            )
    return {
        "plan": plan_sha,
        "source": source_sha,
        "files": files,
        "digest": digest,
        "ledger_sha": _sha(pkg / "progress.md"),
    }


# --- marker ----------------------------------------------------------------------
def _remove_marker(pkg: Path, token: str) -> None:
    m = pkg / MARKER
    marker_fd = None
    try:
        marker_fd = os.open(m, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        owner_fd = os.open("owner", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=marker_fd)
        with os.fdopen(owner_fd, encoding="utf-8") as fh:
            owner = fh.read().strip()
        if owner != token:
            raise ArchiveError(
                "E-ARCHIVE-MARKER",
                f"marker at {m} is not owned by this token; left in place",
            )
        os.unlink("owner", dir_fd=marker_fd)
        os.rmdir(m)
    except OSError as exc:
        raise ArchiveError(
            "E-ARCHIVE-MARKER", f"cannot safely clear marker at {m}: {exc}"
        )
    finally:
        if marker_fd is not None:
            os.close(marker_fd)


def _append(pkg: Path, line: str) -> None:
    with open(pkg / "progress.md", "a", encoding="utf-8") as f:
        f.write(line + "\n")


# --- operations ------------------------------------------------------------------
def archive(root, package, *, rename=rename_noreplace) -> dict:
    loc = Loc(Path(root), package)
    if not os.path.lexists(loc.todo):
        if Loc.real_dir(loc.done):
            if os.path.lexists(loc.done / MARKER):
                raise ArchiveError(
                    "E-ARCHIVE-MARKER",
                    f"already moved to {loc.done} but {MARKER} remains; operator recovery required (--clear-marker)",
                )
            validate(
                loc, loc.done, archived=True
            )  # never report done from mere existence
            return {"status": "already-archived", "path": str(loc.done)}
        raise ArchiveError("E-ARCHIVE-SOURCE", f"{loc.todo} does not exist")
    if os.path.lexists(loc.done):
        raise ArchiveError(
            "E-ARCHIVE-CONFLICT",
            f"both locations exist (or destination is occupied): {loc.done}; nothing changed",
        )
    info = validate(loc, loc.todo)
    try:
        os.makedirs(
            loc.done.parent, exist_ok=True
        )  # parent only; the leaf is created by renameat2
        os.mkdir(loc.todo / MARKER)
    except FileExistsError:
        raise ArchiveError(
            "E-ARCHIVE-MARKER", f"{MARKER} appeared concurrently; not reclaimed"
        )
    except OSError as exc:
        raise ArchiveError("E-ARCHIVE-IO", f"cannot prepare archive: {exc}")
    token = secrets.token_hex(8)
    started = False
    try:
        (loc.todo / MARKER / "owner").write_text(token + "\n", encoding="utf-8")
        again = validate(loc, loc.todo, allow_marker=True)
        if again != info:
            raise ArchiveError(
                "E-ARCHIVE-PIN", "package state changed during archive preparation"
            )
        _append(loc.todo, f"ARCHIVE: start id={loc.id} token={token}")
        started = True
        rename(str(loc.todo), str(loc.done))
    except (ArchiveError, OSError) as exc:
        if isinstance(exc, OSError):
            exc = ArchiveError("E-ARCHIVE-IO", f"{type(exc).__name__}: {exc}")
        if os.path.lexists(loc.todo):  # source survived: record + drop only our marker
            try:
                if started:
                    _append(
                        loc.todo,
                        f"ARCHIVE: failed id={loc.id} token={token} reason={exc.code}",
                    )
                _remove_marker(loc.todo, token)
            except (ArchiveError, OSError) as cleanup:
                exc = ArchiveError(
                    exc.code,
                    f"{exc.msg}; marker cleanup failed ({cleanup}); not reclaimed",
                )
        raise exc
    # moved: marker (and evidence) now live at the done path
    try:
        if (
            os.path.lexists(loc.todo)
            or not Loc.real_dir(loc.done)
            or _sha(loc.done / f"{loc.id}.md") != info["plan"]
        ):
            raise ArchiveError(
                "E-ARCHIVE-MOVE",
                f"post-move verification failed; {MARKER} left at {loc.done}",
            )
        _remove_marker(loc.done, token)
    except OSError as exc:
        raise ArchiveError(
            "E-ARCHIVE-MOVE",
            f"moved to {loc.done} but finalization failed ({exc}); {MARKER} left for operator recovery",
        )
    return {"status": "archived", "path": str(loc.done)}


def print_state(root, package) -> dict:
    loc = Loc(Path(root), package)
    pkg = loc.todo if os.path.lexists(loc.todo) else loc.done
    info = validate(loc, pkg, need_final=False)
    return {"status": "state", "state": info["digest"], "files": info["files"]}


def clear_marker(root, package, token: str) -> dict:
    loc = Loc(Path(root), package)
    if os.path.lexists(loc.todo) and os.path.lexists(loc.done):
        raise ArchiveError(
            "E-ARCHIVE-CONFLICT", "both locations exist; nothing changed"
        )
    pkg = loc.todo if os.path.lexists(loc.todo) else loc.done
    if not Loc.real_dir(pkg) or not os.path.lexists(pkg / MARKER):
        raise ArchiveError("E-ARCHIVE-MARKER", f"no marker to clear under {pkg}")
    if not token or not token.strip():
        raise ArchiveError("E-ARCHIVE-MARKER", "empty token never clears a marker")
    _remove_marker(pkg, token)
    return {"status": "cleared", "path": str(pkg)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="checkout root (default: cwd)")
    ap.add_argument("--package", required=True, help=".dev/tasks/to-do/<TASK-WF-id>")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--print-state", action="store_true")
    g.add_argument("--clear-marker", metavar="TOKEN")
    a = ap.parse_args(argv)
    if a.clear_marker is not None and not a.clear_marker.strip():
        print(
            "E-ARCHIVE-MARKER: --clear-marker needs a non-empty token", file=sys.stderr
        )
        return 1
    try:
        if a.print_state:
            out = print_state(a.root, a.package)
        elif a.clear_marker is not None:
            out = clear_marker(a.root, a.package, a.clear_marker)
        else:
            out = archive(a.root, a.package)
    except ArchiveError as exc:
        print(f"{exc.code}: {exc.msg}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"E-ARCHIVE-IO: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
