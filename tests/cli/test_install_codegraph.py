"""Tests for codegraph acquisition and the registration phase (spec cases U1-U25).

No test touches the network, the real HOME, the real PATH or the real ``claude``:
HOME and PATH point at tmp dirs, ``install_codegraph._download`` is the one network
fake and the ``claude`` calls of ``install_mcp`` are replaced by a recording fake.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile
import time
import urllib.error
from pathlib import Path
from types import SimpleNamespace

import pytest

from superclaude.cli import install_codegraph as cg
from superclaude.cli import install_mcp

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


# --- registration phase (install_mcp.install_codegraph_mcp) -------------------------------


@pytest.fixture
def claude(box, monkeypatch):
    """Fake ``claude``: ``--version`` plus an editor of the fixture ~/.claude.json."""
    cfg = box.home / ".claude.json"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(box.home))
    state = SimpleNamespace(
        cfg=cfg, version_rc=0, calls=[], mutations=[], fail_add=0, noop_add=0
    )

    def servers():
        return json.loads(cfg.read_text()).get("mcpServers", {})

    def seed(entries):
        cfg.write_text(json.dumps({"mcpServers": entries}))

    def fake_exec(argv, timeout):
        assert timeout <= 60
        assert argv[-2:] == ["--scope", "user"]
        state.mutations.append(argv)
        data = json.loads(cfg.read_text())
        verb, name = argv[2], argv[3]
        if verb == "add-json":
            if state.fail_add:
                state.fail_add -= 1
                return 1
            if state.noop_add:
                state.noop_add -= 1
                return 0
            data.setdefault("mcpServers", {})[name] = json.loads(argv[4])
        else:
            assert verb == "remove"
            data.setdefault("mcpServers", {}).pop(name, None)
        cfg.write_text(json.dumps(data))
        return 0

    def fake_run(argv, timeout):
        if argv[0] == "claude":
            state.calls.append(argv)
            return state.version_rc, "2.1.314 (Claude Code)\n"
        return run(argv, timeout)

    monkeypatch.setattr(install_mcp, "_exec_claude", fake_exec)
    monkeypatch.setattr(install_mcp, "_run_argv", fake_run)
    state.servers, state.seed = servers, seed
    seed({})
    return state


def expected_entry(launcher: Path) -> dict:
    return install_mcp._codegraph_entry(launcher)


def test_u11_claude_version_failure_stops_before_discovery(box, claude):
    stub(box.path / "codegraph")
    claude.version_rc = 1
    ok, message = install_mcp.install_codegraph_mcp()
    assert not ok and "Claude CLI" in message
    assert claude.calls == [["claude", "--version"]]
    assert not claude.mutations
    assert not cg.pointer_path().exists()  # discovery never ran


def test_u12_absent_registration_is_added_with_exact_json(box, claude):
    baked = stub(box.path / "codegraph")
    ok, message = install_mcp.install_codegraph_mcp()
    assert ok, message
    (argv,) = claude.mutations
    assert argv[:4] == ["claude", "mcp", "add-json", "codegraph"]
    payload = json.loads(argv[4])
    assert payload == expected_entry(baked.resolve())
    assert payload["command"] == str(baked.resolve())
    assert payload["env"]["CODEGRAPH_MCP_TOOLS"] == cg.MCP_TOOLS
    assert claude.servers()["codegraph"] == payload


def test_u13_equal_registration_is_idempotent(box, claude):
    baked = stub(box.path / "codegraph")
    claude.seed({"codegraph": expected_entry(baked.resolve())})
    ok, _ = install_mcp.install_codegraph_mcp()
    assert ok and not claude.mutations


def _owned_variants(good: dict) -> dict:
    no_flag = {k: v for k, v in good.items() if k != "alwaysLoad"}
    no_tools = dict(
        good, env={k: v for k, v in good["env"].items() if k != "CODEGRAPH_MCP_TOOLS"}
    )
    return {
        "old-path": dict(good, command="/old/bin/codegraph"),
        "missing-alwaysLoad": no_flag,
        "env-without-tool-list": no_tools,
        "old-version-dir": dict(
            good, command="/h/.codegraph/versions/v1.5.0/bin/codegraph"
        ),
    }


@pytest.mark.parametrize(
    "variant",
    ["old-path", "missing-alwaysLoad", "env-without-tool-list", "old-version-dir"],
)
def test_u14_owned_registration_is_replaced(box, claude, variant):
    baked = stub(box.path / "codegraph")
    good = expected_entry(baked.resolve())
    claude.seed({"codegraph": _owned_variants(good)[variant]})
    ok, message = install_mcp.install_codegraph_mcp()
    assert ok, message
    assert [m[2] for m in claude.mutations] == ["remove", "add-json"]
    assert claude.servers()["codegraph"] == good


def test_u15_failed_add_restores_previous_entry(box, claude):
    baked = stub(box.path / "codegraph")
    previous = _owned_variants(expected_entry(baked.resolve()))["old-path"]
    claude.seed({"codegraph": previous})
    claude.fail_add = 1
    ok, message = install_mcp.install_codegraph_mcp()
    assert not ok and "previous user registration restored" in message
    assert claude.servers()["codegraph"] == previous


def test_u15_unverified_add_restores_previous_entry(box, claude):
    baked = stub(box.path / "codegraph")
    previous = _owned_variants(expected_entry(baked.resolve()))["old-path"]
    claude.seed({"codegraph": previous})
    claude.noop_add = 1  # claude says success but stores nothing
    ok, message = install_mcp.install_codegraph_mcp()
    assert not ok and "verification failed" in message
    assert "previous user registration restored" in message
    assert claude.servers()["codegraph"] == previous


USER_ENTRIES = {
    "extra-env-key": {"env": {"TOKEN": "x"}},
    "headers": {"headers": {"Authorization": "x"}},
    "url": {"url": "https://example.test/mcp"},
    "other-args": {"args": ["serve", "--mcp", "--extra"]},
}


@pytest.mark.parametrize("kind", sorted(USER_ENTRIES))
def test_u16_user_managed_entry_kept_when_command_runs(box, claude, kind):
    stub(box.path / "codegraph")
    mine = stub(box.tmp / "mine" / "codegraph")
    entry = {"type": "stdio", "command": str(mine), "args": ["serve", "--mcp"]}
    entry.update(USER_ENTRIES[kind])
    claude.seed({"codegraph": entry})
    ok, message = install_mcp.install_codegraph_mcp()
    assert ok and "claude mcp remove codegraph --scope user" in message
    assert not claude.mutations and claude.servers()["codegraph"] == entry


def test_u16_user_managed_entry_fails_when_command_does_not_run(box, claude):
    stub(box.path / "codegraph")
    entry = {"type": "stdio", "command": "/nonexistent/codegraph", "args": ["x"]}
    claude.seed({"codegraph": entry})
    ok, message = install_mcp.install_codegraph_mcp()
    assert not ok and "claude mcp remove codegraph --scope user" in message
    assert not claude.mutations and claude.servers()["codegraph"] == entry


@pytest.mark.parametrize(
    "text",
    ["{not json", '{"mcpServers": {"codegraph": {}, "codegraph": {}}}'],
    ids=["unreadable", "duplicate-keys"],
)
def test_u17_unreadable_claude_json_means_no_mutation(box, claude, text):
    stub(box.path / "codegraph")
    claude.cfg.write_text(text)
    ok, message = install_mcp.install_codegraph_mcp()
    assert not ok and "lookup failed" in message
    assert not claude.mutations


def test_u18_dry_run_changes_nothing(box, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("dry run must not run anything")

    monkeypatch.setattr(install_mcp, "_run_argv", forbidden)
    monkeypatch.setattr(install_mcp, "_exec_claude", forbidden)
    ok, message = install_mcp.install_codegraph_mcp(dry_run=True)
    assert ok and message.startswith("[DRY RUN]")
    assert not (box.home / ".codegraph").exists()
    assert not (box.home / ".claude.json").exists()


def test_u19_second_run_downloads_and_mutates_nothing(box, claude, monkeypatch):
    urls = serve(monkeypatch, tarball())
    assert install_mcp.install_codegraph_mcp()[0]
    assert len(urls) == 1 and len(claude.mutations) == 1
    assert install_mcp.install_codegraph_mcp()[0]
    assert len(urls) == 1 and len(claude.mutations) == 1


def test_u23_mcp_command_dry_run_previews_codegraph(box, monkeypatch):
    from click.testing import CliRunner

    from superclaude.cli.main import main

    def forbidden(*args, **kwargs):
        pytest.fail("dry run must not run anything")

    monkeypatch.setattr(install_mcp, "_run_argv", forbidden)
    monkeypatch.setattr(install_mcp, "_exec_claude", forbidden)
    monkeypatch.setattr(install_mcp, "_run_command", forbidden)
    result = CliRunner().invoke(main, ["mcp", "--servers", "codegraph", "--dry-run"])
    assert result.exit_code == 0, result.output
    assert "[DRY RUN]" in result.output


def _alive(pid: int) -> bool:
    try:
        stat = Path(f"/proc/{pid}/stat").read_text()
    except OSError:
        return False
    return stat.rsplit(")", 1)[1].split()[0] != "Z"


@pytest.mark.skipif(
    not Path("/proc/self/stat").exists(), reason="needs /proc to inspect processes"
)
def test_u25_bounded_runner_kills_the_process_group(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", "/usr/bin:/bin")  # the stub needs a real `sleep`
    pids = tmp_path / "pids"
    script = tmp_path / "stuck"
    script.write_text(
        f"#!/bin/sh\ntrap '' TERM\nsleep 30 &\necho \"$$ $!\" > {pids}\nwait\n"
    )
    script.chmod(0o755)
    with pytest.raises(subprocess.TimeoutExpired):
        install_mcp._run_argv([str(script)], 1)
    shell_pid, sleep_pid = (int(p) for p in pids.read_text().split())
    for _ in range(40):
        if not _alive(shell_pid) and not _alive(sleep_pid):
            break
        time.sleep(0.05)
    assert not _alive(shell_pid) and not _alive(sleep_pid)


def test_list_block_reports_owned_install_and_registration_state(
    box, claude, monkeypatch
):
    serve(monkeypatch, tarball())
    assert install_mcp.install_codegraph_mcp()[0]
    lines = install_mcp.codegraph_list_lines()
    target = vdir(box.home) / "bin" / "codegraph"
    assert lines[0] == "codegraph MCP (pinned v1.6.2; user scope):"
    assert lines[1] == f"   Executable: {target} (1.6.2)"
    assert lines[2].startswith(f"   Owner: owned (receipt) {vdir(box.home)}")
    assert f"{box.home}/.local/bin/codegraph -> {target}" in lines[2]
    assert lines[3] == "   User registration: matches"
    assert not claude.calls[1:]  # only the install's own claude --version

    claude.seed({"codegraph": dict(claude.servers()["codegraph"], command="/old/x")})
    assert (
        install_mcp.codegraph_list_lines()[3] == "   User registration: owned but stale"
    )
    claude.seed({"codegraph": {"type": "stdio", "command": "x", "args": ["y"]}})
    assert install_mcp.codegraph_list_lines()[3] == "   User registration: user-managed"
    claude.cfg.write_text("{broken")
    assert "unknown" in install_mcp.codegraph_list_lines()[3]


def test_list_block_marks_external_copy_not_owned(box, claude):
    baked = stub(box.path / "codegraph")
    lines = install_mcp.codegraph_list_lines()
    assert lines[1] == f"   Executable: {baked.resolve()} (1.6.2)"
    assert lines[2] == f"   Owner: external: {baked.resolve()}, not owned"
    assert lines[3] == "   User registration: absent"


def test_list_block_flags_version_mismatch(box, claude):
    stale = stub(box.path / "codegraph", "1.5.0")
    lines = install_mcp.codegraph_list_lines()
    assert lines[1] == f"   Executable: version mismatch at {stale.resolve()} (1.5.0)"
