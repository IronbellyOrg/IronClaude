"""Behavior tests for the managed-package archive helper (real filesystem + real
renameat2 where the kernel supports it; simulated libc for fail-closed paths).

Enforcement type: EXECUTABLE (script behavior). Protocol wording is covered in
test_task_workspace_lifecycle.py.
"""

import ctypes
import errno
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

_SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py"
)
_spec = importlib.util.spec_from_file_location("archive_workspace", _SCRIPT)
aw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aw)

ID = "TASK-WF-authLogin-20261001-063000"
PLAN = f"{ID}.md"  # tasklist filename == full package directory basename + .md
OK = "extras=lint:skip,typecheck:skip,test:skip"


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _kernel_supports_noreplace(tmp_path) -> bool:
    if not sys.platform.startswith("linux"):
        return False
    a, b = tmp_path / "probe-a", tmp_path / "probe-b"
    a.mkdir()
    try:
        aw.rename_noreplace(str(a), str(b))
    except aw.ArchiveError:
        return False
    return True


class Pkg:
    def __init__(self, root: Path, tasks=("1", "2")):
        self.root, self.tasks = root, tasks
        (root / ".git").mkdir(parents=True)
        self.todo_root = root / ".dev/tasks/to-do"
        self.todo_root.mkdir(parents=True)
        self.done = root / ".dev/tasks/done" / ID
        self.pkg = self.todo_root / ID
        (self.pkg / "artifacts").mkdir(parents=True)
        (self.pkg / "artifacts/evidence.txt").write_text("log\n")
        (root / "src").mkdir()
        (root / "src/a.py").write_text("print('a')\n")
        self.plan = (
            f"---\nschema: workflow-plan/1.2\nslug: {ID}\n---\n# Demo\n"
            + "".join(
                f"\n## Task {t}: do {t}\n\nAcceptance criteria:\n- ok\n" for t in tasks
            )
        )
        (self.pkg / PLAN).write_text(self.plan)
        (self.pkg / "source.md").write_text("source\n")
        (self.pkg / "return-contract.yaml").write_text(
            f'contract_version: "1.1"\nstatus: success\nslug: {ID}\n'
            f"plan_path: ./{PLAN}\nsource_path: ./source.md\n"
        )
        lines = [
            f"# implement ledger — source: ./{PLAN} — created: 2026-10-01T06:30:00Z",
            f"PLAN: sha256={_sha(self.plan.encode())} source_sha256={_sha(b'source' + bytes([10]))}",
        ]
        for t in tasks:
            lines.append(f"T{t}: start sha={'0' * 40}")
            lines.append(
                f"T{t}: complete verdict=compliant ac=T{t}.AC1 evidence=src/a.py:1 {OK} files=src/a.py"
            )
        (self.pkg / "progress.md").write_text("\n".join(lines) + "\n")

    def append(self, line: str):
        with open(self.pkg / "progress.md", "a") as f:
            f.write(line + "\n")

    def state(self) -> str:
        return aw.print_state(self.root, self.pkg)["state"]

    def final(self, word="pass", state=None):
        self.append(f"FINAL: {word} evidence=src/a.py:1 state={state or self.state()}")

    def run(self, **kw):
        return aw.archive(self.root, self.pkg, **kw)


@pytest.fixture
def p(tmp_path):
    pk = Pkg(tmp_path / "repo")
    pk.final()
    return pk


def fails(p, code, **kw):
    with pytest.raises(aw.ArchiveError) as e:
        p.run(**kw)
    assert e.value.code == code, e.value.msg
    assert p.pkg.is_dir() and (p.pkg / PLAN).is_file()  # source always survives
    return e.value


# --- AC1 ---------------------------------------------------------------------
def test_valid_package_moves_intact_without_marker(p):
    before = {
        r.name: r.read_bytes()
        for r in p.pkg.rglob("*")
        if r.is_file() and r.name != "progress.md"
    }
    out = p.run()
    assert out == {"status": "archived", "path": str(p.done)}
    assert not p.pkg.exists() and p.done.name == ID
    assert not (p.done / ".archiving").exists()
    after = {
        r.name: r.read_bytes()
        for r in p.done.rglob("*")
        if r.is_file() and r.name != "progress.md"
    }
    assert after == before
    assert "ARCHIVE: start" in (p.done / "progress.md").read_text()
    assert p.run() == {
        "status": "already-archived",
        "path": str(p.done),
    }  # stale to-do invocation


# --- AC2: destination never overwritten -----------------------------------------
@pytest.mark.parametrize("kind", ["file", "empty", "nonempty", "dangling"])
def test_existing_destination_is_never_overwritten(p, kind):
    d = p.done
    d.parent.mkdir(parents=True)
    if kind == "file":
        d.write_text("keep")
    elif kind == "dangling":
        d.symlink_to(p.root / "nowhere")
    else:
        d.mkdir()
        if kind == "nonempty":
            (d / "x").write_text("keep")
    fails(p, "E-ARCHIVE-CONFLICT")
    assert os.path.lexists(d)
    if kind in ("file", "nonempty"):
        assert (d.read_text() if kind == "file" else (d / "x").read_text()) == "keep"
    assert not (p.pkg / ".archiving").exists()


def test_destination_created_just_before_syscall_is_preserved(p, tmp_path):
    if not _kernel_supports_noreplace(tmp_path):
        pytest.skip("renameat2 RENAME_NOREPLACE unsupported here")

    def racing(src, dst):
        os.mkdir(dst)
        Path(dst, "winner").write_text("keep")
        aw.rename_noreplace(src, dst)

    err = fails(p, "E-ARCHIVE-DEST", rename=racing)
    assert (p.done / "winner").read_text() == "keep" and not (p.done / PLAN).exists()
    assert not (p.pkg / ".archiving").exists()  # only our marker, removed
    assert "ARCHIVE: failed" in (p.pkg / "progress.md").read_text()
    assert "no-replace" in err.msg


def test_kernel_noreplace_rejects_empty_dir_and_symlink(tmp_path):
    if not _kernel_supports_noreplace(tmp_path):
        pytest.skip("renameat2 RENAME_NOREPLACE unsupported here")
    s = tmp_path / "s"
    s.mkdir()
    for kind in ("dir", "link"):
        d = tmp_path / f"d-{kind}"
        d.mkdir() if kind == "dir" else d.symlink_to(tmp_path / "gone")
        with pytest.raises(aw.ArchiveError) as e:
            aw.rename_noreplace(str(s), str(d))
        assert e.value.code == "E-ARCHIVE-DEST" and s.is_dir()


# --- AC3: closed failure states -------------------------------------------------
def test_stale_plan_pin(p):
    (p.pkg / PLAN).write_text(p.plan + "\nedited\n")
    fails(p, "E-ARCHIVE-PIN")


def test_mismatched_or_legacy_plan_filename_is_rejected(p):
    (p.pkg / PLAN).rename(p.pkg / "plan.md")  # no silent fallback to plan.md
    with pytest.raises(aw.ArchiveError) as e:
        aw.archive(p.root, p.pkg)
    assert (
        e.value.code == "E-ARCHIVE-PACKAGE" and p.pkg.is_dir() and not p.done.exists()
    )


def test_stale_source_pin(p):
    (p.pkg / "source.md").write_text("changed\n")
    fails(p, "E-ARCHIVE-PIN")


def test_pin_after_first_start_rejected(tmp_path):
    pk = Pkg(tmp_path / "r")
    text = (pk.pkg / "progress.md").read_text().splitlines()
    pk.final()
    pk.append(text[1])  # re-pin after the first start record
    fails(pk, "E-ARCHIVE-PIN")


def test_missing_final(tmp_path):
    fails(Pkg(tmp_path / "r"), "E-ARCHIVE-FINAL")


@pytest.mark.parametrize(
    "line",
    [
        "FINAL: skipped evidence=none",
        "FINAL: issues evidence=a.py:1 state={s}",
        "FINAL: pass evidence=src/a.py:1",
    ],
)
def test_skipped_issues_or_unbound_final(tmp_path, line):
    pk = Pkg(tmp_path / "r")
    pk.append(line.format(s=pk.state()))
    fails(pk, "E-ARCHIVE-FINAL")


def test_final_before_later_record_is_stale(p):
    p.append("T2: Ruling: x — y — z")  # any record after FINAL requires a fresh FINAL
    fails(p, "E-ARCHIVE-FINAL")


def test_delivery_change_after_final_invalidates_but_unrelated_does_not(p):
    (p.root / "unrelated.txt").write_text("noise")
    (p.root / "src/other.py").write_text("noise")
    (p.root / "src/a.py").write_text("print('changed')\n")
    fails(p, "E-ARCHIVE-FINAL")


def test_unrelated_change_keeps_final_valid(p):
    (p.root / "unrelated.txt").write_text("noise")
    assert p.run()["status"] == "archived"


def test_each_attempt_needs_fresh_final(p):
    def boom(s, d):
        raise aw.ArchiveError("E-ARCHIVE-PLATFORM", "simulated")

    fails(p, "E-ARCHIVE-PLATFORM", rename=boom)  # appends ARCHIVE: start/failed
    fails(p, "E-ARCHIVE-FINAL")  # old FINAL cannot be reused
    p.final()
    assert p.run()["status"] == "archived"


def test_pending_task(tmp_path):
    pk = Pkg(tmp_path / "r", tasks=("1", "2"))
    pk.final()
    lines = [
        x
        for x in (pk.pkg / "progress.md").read_text().splitlines()
        if not x.startswith("T2:")
    ]
    (pk.pkg / "progress.md").write_text("\n".join(lines) + "\n")
    fails(pk, "E-ARCHIVE-TASKS")


def test_blocked_task(tmp_path):
    pk = Pkg(tmp_path / "r")
    pk.final()
    t = (
        (pk.pkg / "progress.md")
        .read_text()
        .replace("T2: complete verdict=compliant", "T2: blocked verdict=missing")
    )
    (pk.pkg / "progress.md").write_text(t)
    fails(pk, "E-ARCHIVE-TASKS")


def _noncompliant(tmp_path, ruling=True, archive_ruling=None):
    pk = Pkg(tmp_path / "r")
    st = pk.state()
    t = (
        (pk.pkg / "progress.md")
        .read_text()
        .replace("T2: complete verdict=compliant", "T2: complete verdict=missing")
    )
    if ruling:
        t = t.replace(
            "T2: complete", "T2: Ruling: drop — deferred — cost: none\nT2: complete"
        )
    (pk.pkg / "progress.md").write_text(t)
    if archive_ruling:
        pk.append(
            f"ARCHIVE: Ruling: {archive_ruling} — operator accepts — cost-if-wrong: gap ships"
        )
    pk.final(state=st)
    return pk


def test_noncompliant_without_task_ruling(tmp_path):
    fails(
        _noncompliant(tmp_path, ruling=False, archive_ruling="waive T2"),
        "E-ARCHIVE-TASKS",
    )


def test_noncompliant_without_archive_ruling_or_with_wrong_task(tmp_path):
    fails(_noncompliant(tmp_path), "E-ARCHIVE-TASKS")
    fails(
        _noncompliant(tmp_path / "x", archive_ruling="waive T20 and T1"),
        "E-ARCHIVE-TASKS",
    )


def test_named_operator_archive_ruling_waives_task_not_final(tmp_path):
    pk = _noncompliant(tmp_path, archive_ruling="waive T2")
    assert pk.run()["status"] == "archived"
    pk2 = Pkg(tmp_path / "second")
    t = (
        (pk2.pkg / "progress.md")
        .read_text()
        .replace("T2: complete verdict=compliant", "T2: complete verdict=missing")
    )
    (pk2.pkg / "progress.md").write_text(
        t.replace("T2: complete", "T2: Ruling: a — b — c\nT2: complete")
    )
    pk2.append("ARCHIVE: Ruling: waive T2 — operator — cost")
    fails(pk2, "E-ARCHIVE-FINAL")  # ruling never waives FINAL


@pytest.mark.parametrize(
    "mutate",
    [
        lambda t: t + "garbage line\n",
        lambda t: t.rstrip("\n"),
        lambda t: t.replace("# implement ledger", "# other ledger", 1),
        lambda t: t + "T9: start sha=" + "0" * 40 + "\n",
    ],
)
def test_malformed_ledger(p, mutate):
    f = p.pkg / "progress.md"
    f.write_text(mutate(f.read_text()))
    fails(p, "E-ARCHIVE-LEDGER")


@pytest.mark.parametrize(
    "fix",
    [
        lambda p: (p.pkg / "return-contract.yaml").write_text(
            f'contract_version: "1.1"\nstatus: failed\nslug: {ID}\n'
        ),
        lambda p: (p.pkg / "return-contract.yaml").write_text(
            f'contract_version: "1.0"\nstatus: success\nslug: {ID}\n'
        ),
        lambda p: (p.pkg / "source.md").unlink(),
    ],
)
def test_invalid_package_contract(p, fix):
    fix(p)
    fails(p, "E-ARCHIVE-PACKAGE")


def test_existing_marker_is_never_reclaimed(p):
    m = p.pkg / ".archiving"
    m.mkdir()
    (m / "owner").write_text("someone-else\n")
    fails(p, "E-ARCHIVE-MARKER")
    assert (m / "owner").read_text() == "someone-else\n"


def test_source_symlink_escape(p, tmp_path):
    outside = tmp_path / "outside"
    p.pkg.rename(outside)
    p.pkg.symlink_to(outside)
    with pytest.raises(aw.ArchiveError) as e:
        p.run()
    assert e.value.code == "E-ARCHIVE-PACKAGE" or e.value.code == "E-ARCHIVE-SOURCE"
    assert outside.is_dir() and (outside / PLAN).is_file()


def test_parent_symlink_escape(p, tmp_path):
    real = tmp_path / "elsewhere"
    p.todo_root.rename(real)
    p.todo_root.symlink_to(real)
    with pytest.raises(aw.ArchiveError) as e:
        p.run()
    assert e.value.code == "E-ARCHIVE-SOURCE"
    assert (real / ID / PLAN).is_file()


def test_not_under_checkout_or_wrong_name(p, tmp_path):
    other = tmp_path / "other" / ".dev/tasks/to-do"
    other.mkdir(parents=True)
    with pytest.raises(aw.ArchiveError):
        aw.archive(p.root, other / ID)
    with pytest.raises(aw.ArchiveError):
        aw.archive(p.root, p.todo_root / "not-a-task")


# --- AC4: unsupported primitives preserve content -----------------------------
def _fake_libc(err=None):
    def fn(*a):
        ctypes.set_errno(err)
        return -1

    return types.SimpleNamespace(renameat2=fn) if err else types.SimpleNamespace()


@pytest.mark.parametrize("err", [None, errno.ENOSYS, errno.EINVAL, errno.EXDEV])
def test_unsupported_primitive_fails_closed_without_fallback(p, err):
    fails(
        p,
        "E-ARCHIVE-PLATFORM",
        rename=lambda s, d: aw.rename_noreplace(s, d, _libc=_fake_libc(err)),
    )
    assert not p.done.exists()
    assert not (p.pkg / ".archiving").exists()
    assert (p.pkg / "artifacts/evidence.txt").read_text() == "log\n"


def test_non_linux_platform_fails_closed(p, monkeypatch):
    monkeypatch.setattr(sys, "platform", "darwin")
    fails(p, "E-ARCHIVE-PLATFORM")
    assert not p.done.exists()


# --- AC5: interrupt after move + operator-confirmed recovery -------------------
def test_interrupt_after_move_keeps_marker_until_operator_clears(p, tmp_path):
    if not _kernel_supports_noreplace(tmp_path):
        pytest.skip("renameat2 RENAME_NOREPLACE unsupported here")

    def move_then_die(src, dst):
        aw.rename_noreplace(src, dst)
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        p.run(rename=move_then_die)
    marker = p.done / ".archiving"
    assert marker.is_dir() and not p.pkg.exists()
    token = (marker / "owner").read_text().strip()
    # no automatic reclaim, from the stale to-do path or by wrong token
    with pytest.raises(aw.ArchiveError) as e:
        p.run()
    assert e.value.code == "E-ARCHIVE-MARKER" and marker.is_dir()
    with pytest.raises(aw.ArchiveError):
        aw.clear_marker(p.root, p.pkg, "wrong-token")
    assert marker.is_dir()
    assert aw.clear_marker(p.root, p.pkg, token) == {
        "status": "cleared",
        "path": str(p.done),
    }
    assert not marker.exists() and (p.done / PLAN).is_file()
    assert p.run()["status"] == "already-archived"


def test_clear_marker_never_touches_conflicting_locations(p):
    (p.pkg / ".archiving").mkdir()
    (p.pkg / ".archiving/owner").write_text("t\n")
    p.done.mkdir(parents=True)
    with pytest.raises(aw.ArchiveError) as e:
        aw.clear_marker(p.root, p.pkg, "t")
    assert (
        e.value.code == "E-ARCHIVE-CONFLICT" and (p.pkg / ".archiving/owner").exists()
    )


# --- archived-directory identity + OSError handling (integration fixes) ---------
def test_empty_or_unproven_done_dir_is_not_already_archived(p):
    p.pkg.rename(p.root / "parked")
    p.done.mkdir(parents=True)
    with pytest.raises(aw.ArchiveError) as e:  # empty done dir
        p.run()
    assert e.value.code == "E-ARCHIVE-PACKAGE"
    p.done.rmdir()
    (p.root / "parked").rename(p.done)  # complete package but never archived
    with pytest.raises(aw.ArchiveError) as e:
        p.run()
    assert e.value.code == "E-ARCHIVE-PACKAGE" and "ARCHIVE: start" in e.value.msg


def test_archived_dir_with_tampered_plan_or_no_final_is_rejected(p):
    p.run()
    (p.done / PLAN).write_text(p.plan + "\nedited after archive\n")
    with pytest.raises(aw.ArchiveError) as e:
        p.run()
    assert e.value.code == "E-ARCHIVE-PIN"


def test_already_archived_survives_later_delivery_edits(p):
    p.run()
    (p.root / "src/a.py").write_text("later work\n")
    assert p.run() == {"status": "already-archived", "path": str(p.done)}


def test_oserror_before_move_is_reported_and_cleaned(p, monkeypatch):
    def eio(src, dst):
        raise OSError(errno.EIO, "boom")

    err = fails(p, "E-ARCHIVE-IO", rename=eio)
    assert "boom" in err.msg and not p.done.exists()
    assert not (p.pkg / ".archiving").exists()
    assert "ARCHIVE: failed" in (p.pkg / "progress.md").read_text()


def test_oserror_creating_marker_is_reported(p, monkeypatch):
    real_mkdir = os.mkdir

    def deny(path, *a, **k):
        if str(path).endswith(".archiving"):
            raise PermissionError(errno.EACCES, "denied")
        return real_mkdir(path, *a, **k)

    monkeypatch.setattr(aw.os, "mkdir", deny)
    fails(p, "E-ARCHIVE-IO")
    assert not (p.pkg / ".archiving").exists()


def test_cli_reports_oserror_without_traceback(p, monkeypatch, capsys):
    def boom(*a, **k):
        raise OSError(errno.EIO, "disk")

    monkeypatch.setattr(aw, "archive", boom)
    assert aw.main(["--root", str(p.root), "--package", str(p.pkg)]) == 1
    assert capsys.readouterr().err.startswith("E-ARCHIVE-IO")


# --- CLI / real process ---------------------------------------------------------
def test_cli_real_process_archive_and_error_exit(p):
    cmd = [sys.executable, str(_SCRIPT), "--root", str(p.root), "--package", str(p.pkg)]
    st = subprocess.run(cmd + ["--print-state"], capture_output=True, text=True)
    assert st.returncode == 0 and json.loads(st.stdout)["state"] == p.state()
    (p.pkg / PLAN).write_text("tampered")
    bad = subprocess.run(cmd, capture_output=True, text=True)
    assert bad.returncode == 1 and bad.stderr.startswith("E-ARCHIVE-")
    (p.pkg / PLAN).write_text(p.plan)
    ok = subprocess.run(cmd, capture_output=True, text=True)
    assert ok.returncode == 0 and json.loads(ok.stdout)["path"] == str(p.done)


# --- corrections: empty --clear-marker token ------------------------------------
@pytest.mark.parametrize("tok", ["", "  "])
def test_main_empty_clear_marker_errors_and_never_archives(p, tok, monkeypatch, capsys):
    def boom(*a, **k):
        raise AssertionError("archive must not be called")

    monkeypatch.setattr(aw, "archive", boom)
    assert (
        aw.main(["--root", str(p.root), "--package", str(p.pkg), "--clear-marker", tok])
        == 1
    )
    assert capsys.readouterr().err.startswith("E-ARCHIVE-MARKER")
    assert p.pkg.is_dir() and not p.done.exists()


def test_cli_process_empty_clear_marker_leaves_valid_package(p):
    cmd = [sys.executable, str(_SCRIPT), "--root", str(p.root), "--package", str(p.pkg)]
    r = subprocess.run(cmd + ["--clear-marker", ""], capture_output=True, text=True)
    assert r.returncode == 1 and r.stderr.startswith("E-ARCHIVE-MARKER")
    assert (p.pkg / PLAN).is_file() and not p.done.exists()


def test_direct_empty_token_cannot_remove_ownerless_or_owned_marker(p):
    m = p.pkg / ".archiving"
    m.mkdir()
    with pytest.raises(aw.ArchiveError):
        aw.clear_marker(p.root, p.pkg, "")
    assert m.is_dir()
    (m / "owner").write_text("\n")  # blank owner must not match an empty token
    with pytest.raises(aw.ArchiveError):
        aw.clear_marker(p.root, p.pkg, "")
    assert (m / "owner").exists()


@pytest.mark.parametrize("link_owner", [False, True])
def test_recovery_rejects_symlink_marker_or_owner(p, tmp_path, link_owner):
    outside = tmp_path / "outside"
    outside.mkdir()
    owner = outside / "owner"
    owner.write_text("token\n")
    marker = p.pkg / ".archiving"
    if link_owner:
        marker.mkdir()
        (marker / "owner").symlink_to(owner)
    else:
        marker.symlink_to(outside, target_is_directory=True)
    with pytest.raises(aw.ArchiveError) as exc:
        aw.clear_marker(p.root, p.pkg, "token")
    assert exc.value.code == "E-ARCHIVE-MARKER"
    assert owner.read_text() == "token\n"
    assert marker.exists()
    assert p.pkg.exists() and not p.done.exists()


@pytest.mark.parametrize("path", ["./src/a.py", "./artifacts/../src/a.py"])
def test_ambiguous_relative_delivery_is_rejected(p, path):
    ledger = p.pkg / "progress.md"
    ledger.write_text(ledger.read_text().replace("files=src/a.py", f"files={path}"))
    (p.root / "src/a.py").write_text("changed\n")
    fails(p, "E-ARCHIVE-LEDGER")


@pytest.mark.parametrize("kind", ["file", "directory", "dangling"])
def test_directory_digest_tracks_nested_symlink_targets(p, kind):
    src = p.root / "src"
    if kind == "directory":
        (src / "first").mkdir()
        (src / "second").mkdir()
    elif kind == "file":
        (src / "first").write_text("one\n")
        (src / "second").write_text("two\n")
    link = src / "link"
    link.symlink_to("first", target_is_directory=kind == "directory")
    ledger = p.pkg / "progress.md"
    ledger.write_text(ledger.read_text().replace("files=src/a.py", "files=src"))
    before = p.state()
    p.final(state=before)
    link.unlink()
    link.symlink_to("second", target_is_directory=kind == "directory")
    assert p.state() != before
    fails(p, "E-ARCHIVE-FINAL")
