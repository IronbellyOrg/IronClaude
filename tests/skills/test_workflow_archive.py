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
import re
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


@pytest.mark.parametrize("archive_ruling", [None, "waive T2", "waive T20 and T1"])
def test_legacy_task_ruling_needs_no_duplicate_archive_approval(
    tmp_path, archive_ruling
):
    pk = _noncompliant(tmp_path, archive_ruling=archive_ruling)
    assert pk.run()["status"] == "archived"
    ledger = (pk.done / "progress.md").read_text()
    assert "T2: complete verdict=missing" in ledger
    assert pk.run()["status"] == "already-archived"


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


def _session_accepted(tmp_path, task="T2"):
    pk = Pkg(tmp_path / "r")
    ledger = pk.pkg / "progress.md"
    text = ledger.read_text()
    complete = next(
        line for line in text.splitlines() if line.startswith("T2: complete")
    )
    complete = complete.replace("verdict=compliant", "verdict=missing")
    blocked = complete.replace("T2: complete", "T2: blocked")
    ruling = (
        f"{task}: Ruling: accept {task} gap; user confirmed in current conversation "
        f'"yes, accept {task} as explained" — deferred — cost-if-wrong: gap ships'
    )
    ledger.write_text(
        text.replace(
            complete.replace("verdict=missing", "verdict=compliant"),
            f"{blocked}\n{ruling}\n{complete}",
        )
    )
    return pk, complete, blocked, ruling


def test_session_acceptance_archives_without_rewriting_history_or_second_approval(
    tmp_path,
):
    pk, complete, blocked, ruling = _session_accepted(tmp_path)
    before = (pk.pkg / "progress.md").read_text()
    pk.final()
    assert pk.run()["status"] == "archived"
    after = (pk.done / "progress.md").read_text()
    assert after.startswith(before)
    assert f"{blocked}\n{ruling}\n{complete}\n" in after
    assert "ARCHIVE: Ruling:" not in after
    assert pk.run()["status"] == "already-archived"


def test_confirmation_for_another_task_does_not_authorize_completion(tmp_path):
    pk, *_ = _session_accepted(tmp_path, task="T1")
    fails(pk, "E-ARCHIVE-TASKS")


@pytest.mark.parametrize("renew", [False, True])
def test_reopened_task_requires_new_scoped_acceptance(tmp_path, renew):
    pk, complete, blocked, ruling = _session_accepted(tmp_path)
    pk.append(blocked)
    if renew:
        pk.append(ruling)
    pk.append(complete)
    if renew:
        pk.final()
        assert pk.run()["status"] == "archived"
    else:
        fails(pk, "E-ARCHIVE-TASKS")


@pytest.mark.parametrize("ending", ["none", "ruling", "complete", "renewed"])
def test_new_start_requires_new_completion_and_acceptance(tmp_path, ending):
    pk, complete, _, ruling = _session_accepted(tmp_path)
    pk.append(f"T2: start sha={'1' * 40}")
    if ending in ("ruling", "renewed"):
        pk.append(ruling)
    if ending in ("complete", "renewed"):
        pk.append(complete)
    if ending == "renewed":
        pk.final()
        assert pk.run()["status"] == "archived"
    else:
        fails(pk, "E-ARCHIVE-TASKS")


def test_new_start_cannot_reuse_compliant_completion(p):
    p.append(f"T2: start sha={'1' * 40}")
    fails(p, "E-ARCHIVE-TASKS")


@pytest.mark.parametrize(
    "old,new",
    [
        ("verdict=missing", "verdict=extra"),
        ("ac=T2.AC1", "ac=T2.AC2"),
        ("evidence=src/a.py:1", "evidence=src/a.py:2"),
        ("test:skip", "test:fail"),
        ("files=src/a.py", "files=./artifacts/evidence.txt"),
    ],
)
def test_acceptance_cannot_cover_changed_verdict_fields(tmp_path, old, new):
    pk, complete, *_ = _session_accepted(tmp_path)
    pk.append(complete.replace(old, new))
    fails(pk, "E-ARCHIVE-TASKS")


@pytest.mark.parametrize(
    "gate", ["missing-final", "issues", "stale-final", "delivery", "plan", "source"]
)
def test_scoped_acceptance_does_not_waive_final_or_immutable_inputs(tmp_path, gate):
    pk, _, _, ruling = _session_accepted(tmp_path)
    if gate != "missing-final":
        pk.final(word="issues" if gate == "issues" else "pass")
    if gate == "stale-final":
        pk.append(ruling)
    elif gate == "delivery":
        (pk.root / "src/a.py").write_text("changed after FINAL\n")
    elif gate in ("plan", "source"):
        path = pk.pkg / (PLAN if gate == "plan" else "source.md")
        path.write_text(path.read_text() + "changed\n")
    fails(pk, "E-ARCHIVE-PIN" if gate in ("plan", "source") else "E-ARCHIVE-FINAL")


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


@pytest.mark.parametrize("directory", [False, True])
def test_delivery_executable_mode_change_invalidates_final(p, directory):
    delivery = p.root / "src/a.py"
    delivery.chmod(0o755)
    if directory:
        ledger = p.pkg / "progress.md"
        ledger.write_text(ledger.read_text().replace("files=src/a.py", "files=src"))
    before = p.state()
    p.final(state=before)
    delivery.chmod(0o644)
    assert p.state() != before
    fails(p, "E-ARCHIVE-FINAL")


def test_directory_traversal_error_cannot_produce_final_state(p, monkeypatch):
    ledger = p.pkg / "progress.md"
    ledger.write_text(ledger.read_text().replace("files=src/a.py", "files=src"))
    original = aw.os.scandir

    def denied(path):
        if Path(path) == p.root / "src":
            raise PermissionError("unreadable delivery directory")
        return original(path)

    monkeypatch.setattr(aw.os, "scandir", denied)
    with pytest.raises(aw.ArchiveError) as exc:
        p.state()
    assert exc.value.code == "E-ARCHIVE-LEDGER"
    assert p.pkg.exists() and not p.done.exists()


# --- retry / halt ledger records -------------------------------------------------
CK = "a" * 40
RUNGS = [
    "T3_Model01",
    "T2_Model02",
    "T1_Model02",
    "T1_Model01",
    "haiku",
    "sonnet",
    "opus",
]
BRIEF3 = "./artifacts/retries/T1_brief-3.md"


def _rt(n=3, **kw):
    f = {"checkpoint": CK, "tier": "T2_Model02", "brief": BRIEF3, "supersedes": "none"}
    f.update(kw)
    return {
        "open": f"T1: retry n={n} step=open checkpoint={f['checkpoint']} tier={f['tier']}",
        "revert": f"T1: retry n={n} step=revert brief={f['brief']} supersedes={f['supersedes']}",
        "review": f"T1: retry n={n} step=review",
    }


@pytest.mark.parametrize("n", [3, 4, 5])
@pytest.mark.parametrize("step", ["open", "revert", "review"])
def test_retry_record_regex(n, step):
    sup = "none" if n == 3 else f"T1_brief-{n - 1}.md"
    brief = f"./artifacts/retries/T1_brief-{n}.md"
    assert aw._RETRY.match(_rt(n, brief=brief, supersedes=sup)[step])


@pytest.mark.parametrize("tier", RUNGS + ["unknown"])
def test_retry_record_regex_accepts_every_rung_name(tier):
    assert aw._RETRY.match(_rt(tier=tier)["open"])


@pytest.mark.parametrize(
    "line",
    [
        "T1: retry n=2 step=review",
        "T1: retry n=6 step=review",
        f"T1: retry n=3 step=open checkpoint={'a' * 39} tier=opus",
        f"T1: retry n=3 step=open checkpoint={CK} tier=",
        f"T1: retry n=3 step=open checkpoint={CK} tier=bad-tier",
        f"T1: retry n=3 step=open checkpoint={CK} tier=T2.Model",
        "T1: retry n=3 step=revert supersedes=none",
        "T1: retry n=3 step=revert brief=./artifacts/retries/T1_brief-3.md",
        "T1: retry n=3 step=revert brief=./b.md supersedes=T1_brief-5.md",
        "T1: retry n=3 step=revert brief=./b.md supersedes=T1_brief-2.md",
        "T1: retry n=3 step=other",
    ],
)
def test_retry_record_regex_rejects(line, tmp_path):
    assert not aw._RETRY.match(line)
    pk = Pkg(tmp_path / "r", tasks=("1",))
    pk.append(line)
    with pytest.raises(aw.ArchiveError) as e:
        aw._parse_ledger(pk.pkg / "progress.md")
    assert e.value.code == "E-ARCHIVE-LEDGER"


def _brief_pkg(tmp_path, line, brief=None, legacy=None):
    pk = Pkg(tmp_path / "r", tasks=("1",))
    if brief:
        (pk.pkg / "artifacts/retries").mkdir(parents=True)
        (pk.pkg / "artifacts/retries" / brief).write_text("brief\n")
    if legacy:
        d = pk.root / ".dev/implement/s/retries"
        d.mkdir(parents=True)
        (d / legacy).write_text("brief\n")
    pk.append(line)
    pk.final()
    return pk


def _revert(n, brief, sup):
    return f"T1: retry n={n} step=revert brief={brief} supersedes={sup}"


@pytest.mark.parametrize(
    "line,brief",
    [
        (_revert(3, BRIEF3, "none"), "T1_brief-3.md"),
        (
            _revert(4, "./artifacts/retries/T1_brief-4.md", "T1_brief-3.md"),
            "T1_brief-4.md",
        ),
        (
            _revert(5, "./artifacts/retries/T1_brief-5.md", "T1_brief-4.md"),
            "T1_brief-5.md",
        ),
    ],
)
def test_retry_brief_chain_and_existence(tmp_path, line, brief):
    # managed: resolved against the package directory, also once archived in done/
    pk = _brief_pkg(tmp_path, line, brief=brief)
    assert pk.run()["status"] == "archived"
    assert (pk.done / "artifacts/retries" / brief).is_file()
    assert pk.run()["status"] == "already-archived"


def test_retry_brief_chain_and_existence_legacy_root(tmp_path):
    line = _revert(3, ".dev/implement/s/retries/T1_brief-3.md", "none")
    assert (
        _brief_pkg(tmp_path, line, legacy="T1_brief-3.md").run()["status"] == "archived"
    )
    # a package-relative file does not satisfy a legacy path, and vice versa
    with pytest.raises(aw.ArchiveError) as e:
        _brief_pkg(tmp_path / "x", line, brief="T1_brief-3.md").run()
    assert e.value.code == "E-ARCHIVE-PACKAGE"
    with pytest.raises(aw.ArchiveError) as e:
        _brief_pkg(
            tmp_path / "y", _revert(3, BRIEF3, "none"), legacy="T1_brief-3.md"
        ).run()
    assert e.value.code == "E-ARCHIVE-PACKAGE"


@pytest.mark.parametrize(
    "line,present",
    [
        (_revert(4, "./artifacts/retries/T1_brief-4.md", "none"), "T1_brief-4.md"),
        (
            _revert(5, "./artifacts/retries/T1_brief-5.md", "T1_brief-3.md"),
            "T1_brief-5.md",
        ),
        (
            _revert(3, "./artifacts/retries/T1_brief-3.md", "T1_brief-4.md"),
            "T1_brief-3.md",
        ),
        (_revert(3, "./artifacts/retries/T1_brief-4.md", "none"), "T1_brief-4.md"),
        (_revert(3, "./artifacts/retries/T2_brief-3.md", "none"), "T2_brief-3.md"),
        (
            _revert(3, "./artifacts/../artifacts/retries/T1_brief-3.md", "none"),
            "T1_brief-3.md",
        ),
        (_revert(3, ".dev/implement/../retries/T1_brief-3.md", "none"), None),
        (_revert(3, "artifacts/retries/T1_brief-3.md", "none"), "T1_brief-3.md"),
        (_revert(3, BRIEF3, "none"), None),  # brief file missing
    ],
)
def test_retry_brief_chain_and_existence_rejected(tmp_path, line, present):
    with pytest.raises(aw.ArchiveError) as e:
        _brief_pkg(tmp_path, line, brief=present).run()
    assert e.value.code == "E-ARCHIVE-PACKAGE"


@pytest.mark.parametrize("n", [2, 3, 4, 5])
def test_halt_record_regex_review_range(n):
    assert bool(aw._HALT.match(f"T1: halt review={n} reason=budget")) == (n >= 2)


@pytest.mark.parametrize("n", [1, 6, 10])
def test_halt_record_regex_rejects_review_out_of_range(n):
    assert not aw._HALT.match(f"T1: halt review={n} reason=budget")


@pytest.mark.parametrize(
    "line",
    [
        "T1: halt review=6 reason=batch",
        "T1: halt reason=no-evidence",
        "T1: halt review=2 reason=Bad Reason",
        "T1: halt review=2 reason=Bad",
        "T1: halt review=2 reason=",
        "T1: halt review=2 reason=-x",
    ],
)
def test_halt_record_regex(line, tmp_path):
    assert not aw._HALT.match(line)
    pk = Pkg(tmp_path / "r", tasks=("1",))
    pk.append(line)
    with pytest.raises(aw.ArchiveError) as e:
        aw._parse_ledger(pk.pkg / "progress.md")
    assert e.value.code == "E-ARCHIVE-LEDGER"


@pytest.mark.parametrize(
    "line",
    [
        "T9: retry n=3 step=review",
        "T9: halt review=2 reason=budget",
        f"T9: retry n=3 step=open checkpoint={CK} tier=unknown",
        "T9: retry n=3 step=revert brief=./artifacts/retries/T9_brief-3.md supersedes=none",
    ],
)
def test_retry_or_halt_for_unknown_task_rejected(tmp_path, line):
    pk = Pkg(tmp_path / "r", tasks=("1",))
    pk.append(line)
    pk.final(state="0" * 64)
    with pytest.raises(aw.ArchiveError) as e:
        pk.run()
    assert e.value.code == "E-ARCHIVE-LEDGER"
    with pytest.raises(aw.ArchiveError) as e2:
        pk.state()
    assert e2.value.code == "E-ARCHIVE-LEDGER"


def _ladder_pkg(tmp_path, halt="T1: halt review=3 reason=dispute"):
    pk = Pkg(tmp_path / "r", tasks=("1",))
    head = (pk.pkg / "progress.md").read_text().splitlines()[:2]
    blocked = (
        f"T1: blocked verdict=missing ac=T1.AC1 evidence=T1.AC1 {OK} files=src/a.py"
    )
    post = f"T1: complete verdict=missing ac=T1.AC1 evidence=T1.AC1 {OK} files=src/a.py"
    r = _rt()
    lines = head + [
        f"T1: start sha={'0' * 40}",
        blocked,
        r["open"],
        r["revert"],
        r["review"],
        blocked,
        halt,
        "T1: Ruling: accept — operator reviewed — cost-if-wrong: AC unmet",
        post,
    ]
    (pk.pkg / "progress.md").write_text("\n".join(lines) + "\n")
    (pk.pkg / "artifacts/retries").mkdir(parents=True)
    (pk.pkg / "artifacts/retries/T1_brief-3.md").write_text("brief\n")
    pk.append("ARCHIVE: Ruling: waive T1 — operator accepts — cost-if-wrong: AC unmet")
    pk.final()
    return pk


def test_full_ladder_managed_ledger_archives(tmp_path):
    pk = _ladder_pkg(tmp_path)
    assert pk.state()  # --print-state accepts the ladder records
    out = pk.run()
    assert out == {"status": "archived", "path": str(pk.done)}
    text = (pk.done / "progress.md").read_text()
    assert "step=open" in text and "step=revert" in text and "step=review" in text
    assert "halt review=3 reason=dispute" in text
    assert (pk.done / "artifacts/retries/T1_brief-3.md").is_file()


def test_plugin_helper_copy_is_byte_identical():
    plugin = Path(str(_SCRIPT).replace("src/superclaude/", "plugins/superclaude/"))
    assert plugin != _SCRIPT and plugin.is_file()
    assert plugin.read_bytes() == _SCRIPT.read_bytes()


# --- every legal halt reason line archives -----------------------------------------
_RETRY_REF = _SCRIPT.parents[1] / "refs/retry.md"


def _retry_ref_table_and_examples():
    text = _RETRY_REF.read_text(encoding="utf-8")
    pairs = []
    for m in re.finditer(
        r"^\| `([a-z][a-z-]*)` \| .+ \| ([2-5](?:, [2-5])*) \|$", text, re.M
    ):
        pairs += [(m.group(1), int(v)) for v in m.group(2).split(", ")]
    block = re.search(r"```halt-examples\n(.*?)```", text, re.S).group(1)
    return pairs, block.splitlines()


def _halt_pkg(tmp_path, halt_line):
    pk = Pkg(tmp_path / "r", tasks=("1",))
    head = (pk.pkg / "progress.md").read_text().splitlines()[:2]
    blocked = (
        f"T1: blocked verdict=missing ac=T1.AC1 evidence=T1.AC1 {OK} files=src/a.py"
    )
    post = f"T1: complete verdict=missing ac=T1.AC1 evidence=T1.AC1 {OK} files=src/a.py"
    lines = head + [
        f"T1: start sha={'0' * 40}",
        blocked,
        halt_line,
        "T1: Ruling: accept — operator reviewed — cost-if-wrong: AC unmet",
        post,
    ]
    (pk.pkg / "progress.md").write_text("\n".join(lines) + "\n")
    pk.append("ARCHIVE: Ruling: waive T1 — operator accepts — cost-if-wrong: AC unmet")
    return pk


def test_halt_examples_block_equals_reason_table():
    pairs, lines = _retry_ref_table_and_examples()
    assert len(lines) == 22 and len(pairs) == 22
    got = [(aw._HALT.match(x).group(3), int(aw._HALT.match(x).group(2))) for x in lines]
    assert sorted(got) == sorted(pairs)


@pytest.mark.parametrize("line", _retry_ref_table_and_examples()[1])
def test_every_halt_reason_line_parses_and_archives(tmp_path, line):
    assert aw._HALT.match(line)
    pk = _halt_pkg(tmp_path, line)
    pk.final()
    assert pk.run()["status"] == "archived"


# negative-test-cases (fixtures of this test only)
@pytest.mark.parametrize(
    "line", ["T1: halt reason=no-evidence", "T1: halt review=6 reason=batch"]
)
def test_malformed_halt_reason_lines_are_rejected(tmp_path, line):
    pk = _halt_pkg(tmp_path, line)
    with pytest.raises(aw.ArchiveError) as e:
        pk.state()
    assert e.value.code == "E-ARCHIVE-LEDGER"


def test_issues_then_shifted_final_archives_then_already_archived(tmp_path):
    # per-task line numbers are historical pointers: the helper must never resolve them,
    # and a later fresh FINAL pass (naming a to-do path that stops existing) still archives
    pk = Pkg(tmp_path / "r")
    led = pk.pkg / "progress.md"
    led.write_text(
        led.read_text().replace("evidence=src/a.py:1", "evidence=src/a.py:99999", 1)
    )
    pk.append(f"FINAL: issues evidence=src/a.py:1 state={pk.state()}")
    fails(pk, "E-ARCHIVE-FINAL")
    pk.append(
        f"FINAL: pass evidence=.dev/tasks/to-do/{ID}/progress.md:1,src/a.py:99999 state={pk.state()}"
    )
    assert pk.run()["status"] == "archived"
    assert not pk.pkg.exists()
    assert pk.run() == {"status": "already-archived", "path": str(pk.done)}


# --- a symlinked managed retries directory must not validate ------------------------
def _symlinked_retries_pkg(tmp_path):
    pk = Pkg(tmp_path / "r", tasks=("1",))
    shared = (
        pk.todo_root / "shared-retries"
    )  # outside the package; moves are not followed
    shared.mkdir()
    (shared / "T1_brief-3.md").write_text("brief\n")
    (pk.pkg / "artifacts/retries").symlink_to(
        "../../shared-retries", target_is_directory=True
    )
    pk.append(_revert(3, BRIEF3, "none"))
    pk.final(state="0" * 64)  # state() itself rejects the package, which is the point
    return pk


def test_symlinked_retries_directory_is_rejected_before_any_move(tmp_path):
    pk = _symlinked_retries_pkg(tmp_path)
    with pytest.raises(aw.ArchiveError) as e:
        pk.state()
    assert e.value.code == "E-ARCHIVE-PACKAGE"
    fails(pk, "E-ARCHIVE-PACKAGE")  # also asserts the package is still in to-do/
    assert not pk.done.exists()


def test_symlinked_brief_file_is_rejected(tmp_path):
    pk = Pkg(tmp_path / "r", tasks=("1",))
    real = pk.pkg / "artifacts/retries"
    real.mkdir(parents=True)
    (pk.pkg / "artifacts/elsewhere.md").write_text("brief\n")
    (real / "T1_brief-3.md").symlink_to("../elsewhere.md")
    pk.append(_revert(3, BRIEF3, "none"))
    pk.final(state="0" * 64)
    fails(pk, "E-ARCHIVE-PACKAGE")
    assert not pk.done.exists()
