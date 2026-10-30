"""Pinned, checksum-verified acquisition of the codegraph binary (stdlib only).

Discovery reuses a copy that already prints the pinned version (no network).
Acquisition downloads the pinned release tarball, checks its SHA-256 against the
table below, extracts it with strict member checks and records everything it
creates in a receipt *before* creating it, so removal never guesses ownership.
Registration with Claude Code lives in ``install_mcp.install_codegraph_mcp``.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Callable

VERSION = "1.6.2"
TAG = f"v{VERSION}"
SHA256 = {
    "linux-x64": "ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828",
    "linux-arm64": "c8c6be292be21d00dea26bad8b28d434731cf612fb8cc475dc10f5b3038b5b64",
    "darwin-x64": "53d1a4d1a9af31d6cec11b346df2ae792087081e13f623f583e27783c1e7f9bc",
    "darwin-arm64": "d74d1bfb4060db63ec3c2b72c4e17f76c31978af3bad6ace4370d1501ac0662e",
}
# Chosen by the schema-cost check in .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md
MCP_TOOLS = "node,search,callers,callees,impact,files,status"

DOWNLOAD_TIMEOUT = 60
VERSION_TIMEOUT = 10
_MAX_MEMBERS = 20_000  # the v1.6.2 tarball has 1380
_MAX_BYTES = 2 * 1024**3

# run(argv, timeout) -> (returncode, stdout); the bounded argv runner of install_mcp
Runner = Callable[[list, float], tuple]


def asset_name() -> str | None:
    """``linux-x64`` style asset name for this machine, or None when unsupported."""
    system = {"linux": "linux", "darwin": "darwin"}.get(platform.system().lower())
    arch = {"x86_64": "x64", "amd64": "x64", "aarch64": "arm64", "arm64": "arm64"}.get(
        platform.machine().lower()
    )
    return f"{system}-{arch}" if system and arch else None


def codegraph_dir() -> Path:
    return Path.home() / ".codegraph"


def receipt_path() -> Path:
    return codegraph_dir() / ".superclaude-receipt.json"


def pointer_path() -> Path:
    return codegraph_dir() / ".superclaude-bin"


def local_bin_link() -> Path:
    return Path.home() / ".local" / "bin" / "codegraph"


def current_link() -> Path:
    return codegraph_dir() / "current"


def _inside(path: Path, directory: Path) -> bool:
    return path == directory or directory in path.parents


def _write_private(path: Path, text: str) -> None:
    """Atomic write, mode 0600."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp, path)


def _reports_pinned_version(run: Runner, binary: Path) -> bool:
    try:
        code, out = run([str(binary), "--version"], VERSION_TIMEOUT)
    except (OSError, subprocess.SubprocessError):
        return False
    return code == 0 and out.strip() == VERSION


def discover(run: Runner) -> Path | None:
    """First of ``PATH`` and ``~/.local/bin`` that prints VERSION; realpath, no network."""
    on_path = shutil.which("codegraph")
    seen: set = set()
    for candidate in (Path(on_path) if on_path else None, local_bin_link()):
        if candidate is None or not candidate.is_file():
            continue
        real = Path(os.path.realpath(candidate))
        if real in seen or not os.access(real, os.X_OK):
            continue
        seen.add(real)
        if _reports_pinned_version(run, candidate):
            return real
    return None


def write_pointer(winner: Path) -> None:
    """Record the winner for the indexing hook; rewritten only when it changes."""
    text = f"{winner}\n"
    try:
        if pointer_path().read_text(encoding="utf-8") == text:
            return
    except OSError:
        pass
    try:
        _write_private(pointer_path(), text)
    except OSError:
        pass  # the hook falls back to `command -v codegraph`


def _path_warning(winner: Path) -> str | None:
    on_path = shutil.which("codegraph")
    if on_path and os.path.realpath(on_path) == str(winner):
        return None
    return (
        f"warning: `codegraph` on your PATH is {on_path or 'not found'}, not the "
        f"registered {winner}. Add {local_bin_link().parent} to PATH to use the "
        "same binary in your shell."
    )


def read_receipt() -> dict | None:
    """The receipt, or None when missing, unreadable or malformed."""
    try:
        data = json.loads(receipt_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not (
        isinstance(data, dict)
        and isinstance(data.get("version_dirs"), list)
        and all(isinstance(d, str) for d in data["version_dirs"])
        and isinstance(data.get("links"), dict)
    ):
        return None
    return data


def _write_receipt(receipt: dict) -> None:
    _write_private(receipt_path(), json.dumps(receipt, indent=2) + "\n")


def _download(url: str, dest: Path, timeout: int) -> None:
    """The one network call; tests patch it."""
    with urllib.request.urlopen(url, timeout=timeout) as response:  # noqa: S310
        with open(dest, "wb") as out:
            shutil.copyfileobj(response, out)


def _check_members(tar: tarfile.TarFile, prefix: str) -> list:
    members = tar.getmembers()
    if len(members) > _MAX_MEMBERS or sum(m.size for m in members) > _MAX_BYTES:
        raise ValueError("archive is too large")
    for member in members:
        parts = PurePosixPath(member.name).parts
        if (
            member.name.startswith("/")
            or ".." in parts
            or not parts
            or parts[0] != prefix
            or not (member.isreg() or member.isdir())
        ):
            raise ValueError(f"unsafe archive member {member.name!r}")
    return members


def _extract(tar: tarfile.TarFile, members: list, dest: Path) -> None:
    """Write regular files and directories only; no tarfile filter argument (py3.10)."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    for member in members:
        target = dest / member.name
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        mode = 0o755 if member.mode & 0o111 else 0o644
        source = tar.extractfile(member)
        if source is None:
            raise ValueError(f"unreadable archive member {member.name!r}")
        with os.fdopen(os.open(target, flags, mode), "wb") as out:
            shutil.copyfileobj(source, out)


def _point(link: Path, target: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    tmp = link.with_name(f".{link.name}.sc-tmp")
    if os.path.lexists(tmp):
        tmp.unlink()
    os.symlink(target, tmp)
    os.replace(tmp, link)


def _owned(link: Path, receipt: dict) -> bool:
    """A link is ours only while it points where the receipt says (or into our dirs)."""
    try:
        target = os.readlink(link)
    except OSError:
        return False
    if receipt["links"].get(str(link)) == target:
        return True
    resolved = Path(os.path.normpath(link.parent / target))
    return any(_inside(resolved, Path(d)) for d in receipt["version_dirs"])


def _flip_links(receipt: dict, vdir: Path) -> list:
    """Point the two convenience links at the new dir; never touch a link we do not own."""
    notes = []
    for link, target in (
        (local_bin_link(), vdir / "bin" / "codegraph"),
        (current_link(), vdir),
    ):
        if os.path.lexists(link):
            if os.path.islink(link) and os.readlink(link) == str(target):
                continue
            if not (os.path.islink(link) and _owned(link, receipt)):
                notes.append(f"left {link} alone (not created by IronClaude)")
                continue
        receipt["links"][str(link)] = str(target)  # record first, then create
        _write_receipt(receipt)
        _point(link, target)
    return notes


def _fail(stage: str, detail: str) -> tuple:
    return False, f"codegraph {stage} failed: {detail}", None


def acquire(run: Runner) -> tuple:
    """Return ``(ok, message, absolute launcher path)``; never raises for expected faults."""
    winner = discover(run)
    if winner is not None:
        write_pointer(winner)
        warning = _path_warning(winner)
        note = f"\n{warning}" if warning else ""
        return True, f"using codegraph {VERSION} at {winner}{note}", winner

    asset = asset_name()
    if asset is None or asset not in SHA256:
        system, machine = platform.system(), platform.machine()
        return (
            False,
            f"codegraph {TAG} has no supported automatic install for "
            f"{system}/{machine}; install it yourself so that `codegraph --version` "
            f"prints {VERSION}, then rerun superclaude install.",
            None,
        )

    home = codegraph_dir()
    vdir = home / "versions" / TAG
    launcher = vdir / "bin" / "codegraph"
    receipt = read_receipt()
    listed = receipt is not None and str(vdir) in receipt["version_dirs"]
    if os.path.lexists(vdir) and not listed:
        # upstream's own install.sh put it there: use it only if it is the pin
        if _reports_pinned_version(run, launcher):
            real = Path(os.path.realpath(launcher))
            write_pointer(real)
            return True, f"using existing codegraph {VERSION} at {real}", real
        return _fail(
            "extract",
            f"{vdir} exists but its codegraph does not print {VERSION}; "
            f"remove it and rerun superclaude install",
        )

    url = f"https://github.com/colbymchenry/codegraph/releases/download/{TAG}/codegraph-{asset}.tar.gz"
    home.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(dir=home, prefix=".dl-"))
    try:
        archive = tmp / f"codegraph-{asset}.tar.gz"
        try:
            _download(url, archive, DOWNLOAD_TIMEOUT)
        except (urllib.error.URLError, OSError, TimeoutError, ValueError) as exc:
            return _fail(
                "download",
                f"{url} ({type(exc).__name__}). Download it yourself, check its "
                f"SHA-256 is {SHA256[asset]}, extract it so that `codegraph --version` "
                f"prints {VERSION} on PATH, then rerun superclaude install.",
            )
        got = hashlib.sha256(archive.read_bytes()).hexdigest()
        if got != SHA256[asset]:
            return _fail("checksum", f"expected {SHA256[asset]}, got {got} for {url}")
        extracted = tmp / "x"
        prefix = f"codegraph-{asset}"
        try:
            with tarfile.open(archive, "r:gz") as tar:
                _extract(tar, _check_members(tar, prefix), extracted)
        except (tarfile.TarError, OSError, ValueError, EOFError) as exc:
            return _fail("extract", f"{type(exc).__name__}: {exc}")
        new_dir = extracted / prefix
        if not _reports_pinned_version(run, new_dir / "bin" / "codegraph"):
            return _fail("extract", f"the extracted codegraph does not print {VERSION}")

        receipt = receipt or {"version_dirs": [], "links": {}}
        receipt.update(tag=TAG, sha256=got, complete=False)
        if str(vdir) not in receipt["version_dirs"]:
            receipt["version_dirs"].append(str(vdir))  # record before creating
        _write_receipt(receipt)
        vdir.parent.mkdir(parents=True, exist_ok=True)
        if listed and os.path.lexists(vdir):
            shutil.rmtree(vdir)  # an interrupted earlier run left it
        os.rename(new_dir, vdir)
        notes = _flip_links(receipt, vdir)
        receipt.update(complete=True, fresh=True)
        _write_receipt(receipt)
    except OSError as exc:
        return _fail("extract", f"{type(exc).__name__} while installing into {home}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    real = Path(os.path.realpath(launcher))
    write_pointer(real)
    parts = [f"installed codegraph {VERSION} (SHA-256 verified) at {vdir}", *notes]
    warning = _path_warning(real)
    if warning:
        parts.append(warning)
    return True, "\n".join(parts), real


def prune_old_versions(registered: Path) -> None:
    """Delete older receipt-listed version dirs nothing resolves into.

    Call only after the registration was verified. A dir installed in this run
    keeps its predecessor for one run (the ``fresh`` flag is cleared here).
    """
    receipt = read_receipt()
    if receipt is None or not receipt.get("complete"):
        return
    if receipt.get("fresh"):
        receipt["fresh"] = False
        _write_receipt(receipt)
        return
    in_use = [Path(os.path.realpath(registered))]
    in_use += [
        Path(os.path.realpath(p))
        for p in (local_bin_link(), current_link())
        if os.path.lexists(p)
    ]
    base = Path(os.path.realpath(codegraph_dir() / "versions"))
    kept = []
    for entry in receipt["version_dirs"]:
        path = Path(entry)
        real = Path(os.path.realpath(path))
        if (
            path.name == TAG
            or real.parent != base
            or any(_inside(u, real) for u in in_use)
        ):
            kept.append(entry)
            continue
        shutil.rmtree(path, ignore_errors=True)
        if os.path.lexists(path):
            kept.append(entry)
    if kept != receipt["version_dirs"]:
        receipt["version_dirs"] = kept
        _write_receipt(receipt)
