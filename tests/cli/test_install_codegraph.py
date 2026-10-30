"""Tests for the pinned codegraph acquisition module (spec cases U1-U10, U20-U22, U24).

No test touches the network, the real HOME or the real PATH: HOME and PATH point at
tmp dirs and ``install_codegraph._download`` is the one fake.
"""

from __future__ import annotations

import hashlib
import io
import os
import re
import shutil
import subprocess
import tarfile
import urllib.error
from pathlib import Path
from types import SimpleNamespace

import pytest

from superclaude.cli import install_codegraph as cg

REPO = Path(__file__).resolve().parents[2]
ASSET = "linux-x64"


def run(argv, timeout):
    """Real runner for the shell stubs below (no shell, bounded)."""
    done = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    return done.returncode, done.stdout


def stub(path: Path, version: str = "1.6.2") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"#!/bin/sh\necho {version}\n")
    path.chmod(0o755)
    return path


def tarball(version: str = "1.6.2", extra=None) -> bytes:
    """A fixture release tarball: codegraph-linux-x64/bin/codegraph printing version."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for name in (f"codegraph-{ASSET}", f"codegraph-{ASSET}/bin"):
            info = tarfile.TarInfo(name)
            info.type = tarfile.DIRTYPE
            info.mode = 0o755
            tar.addfile(info)
        body = f"#!/bin/sh\necho {version}\n".encode()
        info = tarfile.TarInfo(f"codegraph-{ASSET}/bin/codegraph")
        info.size = len(body)
        info.mode = 0o755
        tar.addfile(info, io.BytesIO(body))
        for info, data in extra or []:
            tar.addfile(info, io.BytesIO(data) if data is not None else None)
    return buf.getvalue()


@pytest.fixture(autouse=True)
def box(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    path_dir = tmp_path / "pathbin"
    path_dir.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PATH", str(path_dir))
    monkeypatch.setattr(cg.platform, "system", lambda: "Linux")
    monkeypatch.setattr(cg.platform, "machine", lambda: "x86_64")

    def no_network(url, dest, timeout):
        pytest.fail(f"unexpected download of {url}")

    monkeypatch.setattr(cg, "_download", no_network)
    return SimpleNamespace(home=home, path=path_dir, tmp=tmp_path)


def serve(monkeypatch, data: bytes, *, pin: bool = True) -> list:
    """Fake the download with ``data``; ``pin`` makes the SHA256 table match it."""
    urls: list = []

    def fake(url, dest, timeout):
        urls.append(url)
        Path(dest).write_bytes(data)

    monkeypatch.setattr(cg, "_download", fake)
    if pin:
        monkeypatch.setitem(cg.SHA256, ASSET, hashlib.sha256(data).hexdigest())
    return urls


def vdir(home: Path, tag: str = "v1.6.2") -> Path:
    return home / ".codegraph" / "versions" / tag


# --- U1 ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("system", "machine", "expected"),
    [
        ("Linux", "x86_64", "linux-x64"),
        ("Linux", "amd64", "linux-x64"),
        ("Linux", "aarch64", "linux-arm64"),
        ("Linux", "arm64", "linux-arm64"),
        ("Darwin", "x86_64", "darwin-x64"),
        ("Darwin", "arm64", "darwin-arm64"),
        ("Windows", "AMD64", None),
        ("FreeBSD", "amd64", None),
        ("Linux", "armv7l", None),
    ],
)
def test_u1_asset_name(monkeypatch, system, machine, expected):
    monkeypatch.setattr(cg.platform, "system", lambda: system)
    monkeypatch.setattr(cg.platform, "machine", lambda: machine)
    assert cg.asset_name() == expected


# --- U2 ---------------------------------------------------------------------


def test_u2_pin_integrity():
    assert set(cg.SHA256) == {"linux-x64", "linux-arm64", "darwin-x64", "darwin-arm64"}
    assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in cg.SHA256.values())
    assert cg.TAG == "v" + cg.VERSION
    evidence = REPO / ".dev/codegraph-migration/evidence/P2-mcp-tools-schema.md"
    selected = re.search(r"^Selected MCP_TOOLS: (.+)$", evidence.read_text(), re.M)
    assert selected and cg.MCP_TOOLS == selected.group(1)
    assert "explore" not in cg.MCP_TOOLS.split(",")


# --- U3, U4: reuse, no download ------------------------------------------------


def test_u3_path_copy_is_reused(box):
    baked = stub(box.path / "codegraph")
    ok, message, launcher = cg.acquire(run)
    assert ok and launcher == baked.resolve()
    assert "using codegraph 1.6.2" in message
    assert "warning" not in message


def test_u4_local_bin_wins_over_stale_path_copy(box):
    stub(box.path / "codegraph", "1.5.0")
    local = stub(box.home / ".local/bin/codegraph")
    ok, _, launcher = cg.acquire(run)
    assert ok and launcher == local.resolve()


# --- U5, U6: verified download --------------------------------------------------


def test_u5_download_extracts_and_links(box, monkeypatch):
    urls = serve(monkeypatch, tarball())
    ok, message, launcher = cg.acquire(run)
    assert ok, message
    assert urls == [
        "https://github.com/colbymchenry/codegraph/releases/download/"
        "v1.6.2/codegraph-linux-x64.tar.gz"
    ]
    target = vdir(box.home) / "bin" / "codegraph"
    assert launcher == target.resolve()
    assert run([str(target), "--version"], 10) == (0, "1.6.2\n")
    assert os.readlink(box.home / ".local/bin/codegraph") == str(target)
    assert os.readlink(box.home / ".codegraph/current") == str(vdir(box.home))
    assert not list((box.home / ".codegraph").glob(".dl-*"))


def test_u6_checksum_mismatch_leaves_nothing(box, monkeypatch):
    serve(monkeypatch, tarball(), pin=False)
    ok, message, launcher = cg.acquire(run)
    assert not ok and launcher is None
    assert "checksum" in message and cg.SHA256[ASSET] in message
    assert not (box.home / ".codegraph/versions").exists()
    assert not os.path.lexists(box.home / ".local/bin/codegraph")
    assert not cg.receipt_path().exists()
    assert not list((box.home / ".codegraph").glob(".dl-*"))


# --- U7: unsafe members are rejected before anything is written ------------------


def _member(name, kind=tarfile.REGTYPE, link=""):
    info = tarfile.TarInfo(name)
    info.type = kind
    info.linkname = link
    info.mode = 0o755
    return info


@pytest.mark.parametrize(
    "extra",
    [
        [(_member("codegraph-linux-x64/../../evil"), None)],
        [(_member("/abs/evil"), None)],
        [
            (
                _member("codegraph-linux-x64/bin/link", tarfile.SYMTYPE, "../../evil"),
                None,
            )
        ],
        [(_member("other-prefix/bin/codegraph"), None)],
    ],
    ids=["dotdot", "absolute", "symlink", "wrong-prefix"],
)
def test_u7_unsafe_members_rejected(box, monkeypatch, extra):
    serve(monkeypatch, tarball(extra=extra))
    ok, message, _ = cg.acquire(run)
    assert not ok and "extract" in message
    assert not (box.home / ".codegraph/versions").exists()
    assert not (box.tmp / "evil").exists() and not (box.home / "evil").exists()


# --- U8, U9, U10 -------------------------------------------------------------------


@pytest.mark.parametrize("error", [urllib.error.URLError("offline"), TimeoutError()])
def test_u8_download_failure_names_url_and_recovery(box, monkeypatch, error):
    def boom(url, dest, timeout):
        raise error

    monkeypatch.setattr(cg, "_download", boom)
    ok, message, _ = cg.acquire(run)
    assert not ok
    assert "download" in message and "releases/download/v1.6.2" in message
    assert "rerun superclaude install" in message
    assert "Traceback" not in message
    assert not list((box.home / ".codegraph").glob(".dl-*"))


def test_u9_unsupported_platform_without_copy(box, monkeypatch):
    monkeypatch.setattr(cg.platform, "system", lambda: "Windows")
    monkeypatch.setattr(cg.platform, "machine", lambda: "AMD64")
    ok, message, _ = cg.acquire(run)  # the autouse fake fails on any download
    assert not ok and "Windows/AMD64" in message


def test_u10_unsupported_platform_with_copy_still_reuses(box, monkeypatch):
    monkeypatch.setattr(cg.platform, "system", lambda: "Windows")
    monkeypatch.setattr(cg.platform, "machine", lambda: "AMD64")
    baked = stub(box.path / "codegraph")
    ok, _, launcher = cg.acquire(run)
    assert ok and launcher == baked.resolve()


# --- U20: receipt ---------------------------------------------------------------------


def test_u20_receipt_only_after_verified_download(box, monkeypatch):
    stub(box.path / "codegraph")
    assert cg.acquire(run)[0]
    assert not cg.receipt_path().exists()  # a reused copy is never recorded

    (box.path / "codegraph").unlink()
    serve(monkeypatch, tarball())
    assert cg.acquire(run)[0]
    receipt = cg.read_receipt()
    assert receipt["tag"] == "v1.6.2" and receipt["complete"] is True
    assert receipt["sha256"] == cg.SHA256[ASSET]
    assert receipt["version_dirs"] == [str(vdir(box.home))]
    assert set(receipt["links"]) == {
        str(box.home / ".local/bin/codegraph"),
        str(box.home / ".codegraph/current"),
    }
    assert cg.receipt_path().stat().st_mode & 0o777 == 0o600


def test_u20_corrupt_receipt_deletes_nothing_and_is_rewritten(box, monkeypatch):
    serve(monkeypatch, tarball())
    ok, _, launcher = cg.acquire(run)
    assert ok
    cg.receipt_path().write_text("{not json")
    assert cg.read_receipt() is None
    cg.prune_old_versions(launcher)  # does not fail, deletes nothing
    assert vdir(box.home).is_dir()
    # links gone and the dir unlisted: the dir is reused without a download, receipt untouched
    os.unlink(box.home / ".local/bin/codegraph")
    os.unlink(box.home / ".codegraph/current")
    ok, message, _ = cg.acquire(run)
    assert ok, message
    assert cg.read_receipt() is None
    # the next verified download rewrites the receipt
    shutil.rmtree(vdir(box.home))
    urls = serve(monkeypatch, tarball())
    ok, message, _ = cg.acquire(run)
    assert ok, message
    assert urls
    assert cg.read_receipt()["complete"] is True


# --- U21: pin bump ----------------------------------------------------------------------


def _bump(monkeypatch, version="1.6.3"):
    monkeypatch.setattr(cg, "VERSION", version)
    monkeypatch.setattr(cg, "TAG", f"v{version}")
    serve(monkeypatch, tarball(version))


def test_u21_pin_bump_keeps_previous_then_prunes(box, monkeypatch):
    serve(monkeypatch, tarball())
    assert cg.acquire(run)[0]
    old = vdir(box.home)

    _bump(monkeypatch)
    ok, message, launcher = cg.acquire(run)
    assert ok, message
    new = vdir(box.home, "v1.6.3")
    assert launcher == (new / "bin/codegraph").resolve()
    assert os.readlink(box.home / ".local/bin/codegraph") == str(new / "bin/codegraph")
    assert os.readlink(box.home / ".codegraph/current") == str(new)
    assert old.is_dir() and new.is_dir()

    cg.prune_old_versions(launcher)  # same run as the install: previous kept
    assert old.is_dir()
    cg.prune_old_versions(launcher)  # next run: nothing resolves into it
    assert not old.exists() and new.is_dir()
    assert cg.read_receipt()["version_dirs"] == [str(new)]


def test_u21_registered_command_inside_old_dir_blocks_pruning(box, monkeypatch):
    serve(monkeypatch, tarball())
    ok, _, old_launcher = cg.acquire(run)
    old = vdir(box.home)
    _bump(monkeypatch)
    assert cg.acquire(run)[0]
    cg.prune_old_versions(old_launcher)
    cg.prune_old_versions(old_launcher)
    assert old.is_dir()
    assert str(old) in cg.read_receipt()["version_dirs"]


# --- U22: a link we do not own ------------------------------------------------------------


def test_u22_non_owned_link_is_left_alone(box, monkeypatch):
    elsewhere = stub(box.tmp / "elsewhere" / "codegraph", "1.5.0")
    link = box.home / ".local/bin/codegraph"
    link.parent.mkdir(parents=True)
    link.symlink_to(elsewhere)
    serve(monkeypatch, tarball())
    ok, message, launcher = cg.acquire(run)
    assert ok, message
    assert os.readlink(link) == str(elsewhere)
    assert launcher == (vdir(box.home) / "bin/codegraph").resolve()
    assert f"left {link} alone" in message
    assert str(link) not in cg.read_receipt()["links"]
    assert os.readlink(box.home / ".codegraph/current") == str(vdir(box.home))


# --- U24: pointer file and PATH warning ------------------------------------------------------


def test_u24_pointer_for_baked_copy_rewritten_only_on_change(box):
    baked = stub(box.path / "codegraph")
    assert cg.acquire(run)[0]
    pointer = cg.pointer_path()
    assert pointer.read_text() == f"{baked.resolve()}\n"
    assert pointer.stat().st_mode & 0o777 == 0o600
    before = pointer.stat().st_mtime_ns
    assert cg.acquire(run)[0]
    assert pointer.stat().st_mtime_ns == before


def test_u24_pointer_for_downloaded_copy(box, monkeypatch):
    serve(monkeypatch, tarball())
    _, _, launcher = cg.acquire(run)
    assert cg.pointer_path().read_text() == f"{launcher}\n"


def test_u24_winner_not_on_path_warns_but_passes(box):
    local = stub(box.home / ".local/bin/codegraph")  # PATH holds no codegraph
    ok, message, launcher = cg.acquire(run)
    assert ok and launcher == local.resolve()
    assert "warning" in message and str(local.parent) in message
