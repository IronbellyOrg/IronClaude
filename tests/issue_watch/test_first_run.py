"""Task 21: the first-run check and enabling a repo.

No real ``gh``, Orca or network call is made: the cycles run over a ``GhWorld`` and a
``FakeLauncher``, the label and field reads over a scripted runner. HOME and XDG are redirected
into ``tmp_path`` and the tests assert nothing was written there.
"""

from __future__ import annotations

import dataclasses
import json
import os
import stat
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import (
    audit,
    cycle,
    defaults,
    first_run,
    launch,
    record,
    repo_init,
)
from superclaude.cli.issue_watch.record import FileStore

from .conftest import (
    CYCLE_NOW,
    FakeClock,
    FakeLauncher,
    GhWorld,
    default_which,
    launched_outcome,
    result,
)

REPO = "IronbellyOrg/IronClaude"
DEFAULTS = defaults.Defaults()
LAUNCH_ID = 1001


@pytest.fixture(autouse=True)
def _home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))


def _config(tmp_path: Path, *, approvers=(11, 22), worktree=True, **extra) -> Path:
    work = tmp_path / "worktrees" / "IronClaude" / "Coordinator"
    if worktree:
        work.mkdir(parents=True)
    approvers_file = tmp_path / "cfg" / "approvers.txt"
    approvers_file.parent.mkdir(parents=True, exist_ok=True)
    approvers_file.write_text("".join(f"{i}\n" for i in approvers))
    approvers_file.chmod(0o600)
    raw = {
        "schema_version": 1,
        "enabled": False,
        "repo": REPO,
        "project_id": "PVT_abc",
        "owner_account_id": LAUNCH_ID,
        "worktree": str(work),
        "approvers_file": str(approvers_file),
        "state_dir": str(tmp_path / "state" / "issue-watch" / "IronClaude"),
        **extra,
    }
    path = tmp_path / "cfg" / "IronClaude.json"
    path.write_text(json.dumps(raw))
    path.chmod(0o600)
    return path


class Router:
    """The label and field reads go to a script; everything else to the world's runner."""

    def __init__(self, world: GhWorld, labels=("bug",), field_ok=True) -> None:
        self.world, self.calls = world, []
        self.created: list[tuple[str, ...]] = []
        self.labels = list(labels)
        self.field_ok = field_ok

    def run(self, argv, timeout, *, cwd=None):
        key = tuple(argv)
        self.calls.append(key)
        if key[:3] == ("gh", "label", "list"):
            return result(stdout=json.dumps([{"name": n} for n in self.labels]))
        if key[:3] == ("gh", "label", "create"):
            self.created.append(key)
            self.labels.append(key[3])
            return result()
        if key[:4] == ("gh", "api", "--method", "GET") and "issue-fields" in key[4]:
            row = {"name": "Approved", "data_type": "single_select"}
            row["options"] = [{"name": "Yes" if self.field_ok else "No"}]
            return result(stdout=json.dumps([row]))
        return self.world.runner.run(argv, timeout, cwd=cwd)


class Harness:
    def __init__(self, tmp_path: Path, **config_kw) -> None:
        self.path = _config(tmp_path, **config_kw)
        self.cfg = cycle.load_config(self.path)
        self.world = GhWorld(FakeClock(CYCLE_NOW), self.cfg)
        self.router = Router(self.world)
        self.launcher = FakeLauncher([launched_outcome()])
        self.factory_calls = 0
        self.on_factory = None

    def factory(self, cfg: cycle.Config) -> cycle.Deps:
        self.factory_calls += 1
        if self.on_factory:
            self.on_factory(self.factory_calls, cfg)
        return cycle.Deps(
            runner=self.world.runner,
            store=FileStore(cfg.state_dir),
            launcher=self.launcher,
            clock=self.world.clock,
            audit=audit.AuditLog(cfg.state_dir),
            config=cfg,
            which=default_which,
            host="test-host",
        )

    def run(self):
        return first_run.first_run(
            self.path,
            DEFAULTS,
            self.router,
            self.factory,
            now=lambda: CYCLE_NOW,
        )

    def enabled(self) -> bool:
        return json.loads(self.path.read_text())["enabled"]

    @property
    def report(self) -> Path:
        return self.cfg.state_dir / first_run.REPORT_FILE


def _no_real_calls(h: Harness, tmp_path: Path) -> None:
    assert h.launcher.calls == []  # no Orca launch
    assert not (tmp_path / "home").exists()  # nothing under the redirected home
    assert not any(a[0] == "orca" for a, _ in h.world.runner.calls)


def test_when_every_step_passes_the_config_is_enabled(tmp_path) -> None:
    h = Harness(tmp_path)
    out = h.run()
    assert out.status == "enabled" and out.enabled and h.enabled()
    assert [(s.name, s.ok) for s in out.steps] == [(n, True) for n in first_run.STEPS]
    assert cycle.load_config(h.path).enabled is True
    assert stat.S_IMODE(h.path.stat().st_mode) == 0o600
    assert (h.cfg.state_dir / "dispatch.json").exists()
    assert h.report.read_text().splitlines()[0] == "first-run: passed"
    assert h.router.created == [
        (
            "gh",
            "label",
            "create",
            "issue-watch:trigger",
            "--repo",
            REPO,
            "--color",
            repo_init.LABEL_COLOR,
            "--description",
            repo_init.LABEL_DESCRIPTION,
        )
    ]
    _no_real_calls(h, tmp_path)


def test_a_worktree_that_does_not_exist_keeps_the_config_disabled(tmp_path) -> None:
    h = Harness(tmp_path, worktree=False)
    out = h.run()
    assert out.status == "failed" and not h.enabled()
    assert [s.name for s in out.steps] == ["config"]
    text = h.report.read_text() if h.report.exists() else out.report
    assert "worktree_invalid" in text and "first-run: failed config" in text
    assert h.router.calls == []  # nothing was read or created
    assert not (h.cfg.state_dir / "dispatch.json").exists()


def test_a_dry_run_failure_keeps_the_config_disabled(tmp_path) -> None:
    h = Harness(tmp_path)
    h.world.fail("origin", "foreign_origin", times=None)
    out = h.run()
    assert out.status == "failed" and not h.enabled()
    failing = out.steps[-1]
    assert (failing.name, failing.ok) == ("dry_run", False)
    assert failing.reason == "origin_mismatch"
    assert h.report.read_text().splitlines()[0] == (
        "first-run: failed dry_run: origin_mismatch"
    )


def test_a_failed_label_stops_before_the_state_is_created(tmp_path) -> None:
    h = Harness(tmp_path)

    class NoCreate(Router):
        def run(self, argv, timeout, *, cwd=None):
            if tuple(argv)[:3] == ("gh", "label", "create"):
                return result(stderr="HTTP 403", returncode=1)
            return super().run(argv, timeout, cwd=cwd)

    h.router = NoCreate(h.world)
    out = h.run()
    assert (out.steps[-1].name, out.steps[-1].reason) == ("label", "label_failed")
    assert not h.enabled() and not (h.cfg.state_dir / "dispatch.json").exists()


def test_a_held_lock_is_detected_by_the_lock_test(tmp_path) -> None:
    h = Harness(tmp_path)
    out = h.run()
    lock = next(s for s in out.steps if s.name == "lock")
    assert lock.ok  # the second cycle really ended with exit 75 while the lock was held


def test_a_lock_that_does_not_hold_fails_the_lock_test(tmp_path, monkeypatch) -> None:
    h = Harness(tmp_path)
    real = cycle.run_cycle
    seen = {"n": 0}

    def fake(deps, dry_run):
        seen["n"] += 1
        res = real(deps, dry_run)
        if seen["n"] == 2:  # the cycle that ran while the lock was held
            assert res.exit_code == 75  # the real lock did hold; now pretend it did not
            return dataclasses.replace(res, exit_code=0, reason="ok")
        return res

    monkeypatch.setattr(first_run.cycle, "run_cycle", fake)
    out = h.run()
    assert (out.steps[-1].name, out.steps[-1].reason) == ("lock", "lock_not_detected")
    assert not h.enabled()


def test_a_state_document_that_does_not_reload_fails_the_restart_test(tmp_path) -> None:
    h = Harness(tmp_path)

    def corrupt(n: int, cfg: cycle.Config) -> None:
        if n == 3:  # deps made for the lock test's second cycle
            (cfg.state_dir / "dispatch.json").write_bytes(b"{not json")

    h.on_factory = corrupt
    out = h.run()
    assert (out.steps[-1].name, out.steps[-1].reason) == (
        "restart",
        "state_not_reloadable",
    )
    assert not h.enabled()
    assert "first-run: failed restart: state_not_reloadable" in h.report.read_text()


def test_a_second_dry_run_that_changes_the_store_fails_the_restart_test(
    tmp_path,
) -> None:
    h = Harness(tmp_path)

    def tweak(n: int, cfg: cycle.Config) -> None:
        if n == 4:  # deps made for the restart test's dry-run
            path = cfg.state_dir / "dispatch.json"
            doc = json.loads(path.read_text())
            doc["considered"] = {"7": "2026-11-16T10:00:00Z"}
            path.write_text(json.dumps(doc))

    h.on_factory = tweak
    out = h.run()
    assert (out.steps[-1].name, out.steps[-1].reason) == ("restart", "state_changed")
    assert not h.enabled()


def test_a_second_run_changes_nothing(tmp_path) -> None:
    h = Harness(tmp_path)
    assert h.run().status == "enabled"
    config_bytes = h.path.read_bytes()
    store_bytes = (h.cfg.state_dir / "dispatch.json").read_bytes()
    calls = (len(h.router.calls), len(h.world.runner.calls), h.factory_calls)
    again = h.run()
    assert again.status == "already_enabled" and again.steps == ()
    assert h.path.read_bytes() == config_bytes
    assert (h.cfg.state_dir / "dispatch.json").read_bytes() == store_bytes
    assert (len(h.router.calls), len(h.world.runner.calls), h.factory_calls) == calls


def test_a_state_that_already_exists_is_kept_and_not_re_initialised(tmp_path) -> None:
    h = Harness(tmp_path)
    store = record.init_state(h.cfg.state_dir, CYCLE_NOW)
    before = (h.cfg.state_dir / "dispatch.json").read_bytes()
    out = h.run()
    step = next(s for s in out.steps if s.name == "init_state")
    assert (step.ok, step.reason) == (True, "state_exists")
    assert out.status == "enabled"
    assert (h.cfg.state_dir / "dispatch.json").read_bytes() == before
    assert store is not None


def test_the_report_shows_the_closed_gate_and_the_launch_account_warning(
    tmp_path,
) -> None:
    h = Harness(tmp_path, approvers=(11, LAUNCH_ID))
    out = h.run()
    lines = h.report.read_text().splitlines()
    assert launch.GOVERNED_LEVELS_ALLOWED is False
    assert "ship_gate: closed (only Pipeline None launches)" in lines
    assert "warning: approver_is_launch_account" in lines
    assert "approved_field: approved_field_present" in lines
    assert "trigger_label: created" in lines
    assert out.report == h.report.read_text()


def test_the_label_made_is_the_configs_own_trigger_not_the_default(tmp_path) -> None:
    h = Harness(tmp_path, labels={"trigger": "go-watch"})
    h.run()
    assert [k[3] for k in h.router.created] == ["go-watch"]


def test_no_warning_when_the_launch_account_is_not_an_approver(tmp_path) -> None:
    h = Harness(tmp_path)
    h.run()
    assert "approver_is_launch_account" not in h.report.read_text()


def test_an_open_gate_is_reported_open(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(launch, "GOVERNED_LEVELS_ALLOWED", True)
    h = Harness(tmp_path)
    h.run()
    assert "ship_gate: open (all pipeline levels may launch)" in h.report.read_text()


def test_a_missing_approved_field_is_reported_but_does_not_block(tmp_path) -> None:
    h = Harness(tmp_path)
    h.router.field_ok = False
    out = h.run()
    assert out.status == "enabled"
    assert "approved_field: approved_field_missing" in h.report.read_text()


def test_the_report_file_is_private(tmp_path) -> None:
    h = Harness(tmp_path)
    h.run()
    assert stat.S_IMODE(h.report.stat().st_mode) == 0o600
    assert stat.S_IMODE(h.cfg.state_dir.stat().st_mode) == 0o700


def test_an_unreadable_config_reports_next_to_itself_under_its_own_name(
    tmp_path,
) -> None:
    path = tmp_path / "cfg" / "Broken.json"
    path.parent.mkdir()
    path.write_text("not json")
    h = Harness(tmp_path)  # only for its router and factory
    out = first_run.first_run(path, DEFAULTS, h.router, h.factory)
    assert out.status == "failed" and not out.enabled
    assert out.report_path == path.parent / "Broken-first-run.txt"
    assert "config_invalid" in out.report_path.read_text()
    assert os.path.exists(path) and path.read_text() == "not json"


# --- failed_step: the read-only check dispatch uses to retry a failed first run --------------


def _plain_config(tmp_path: Path, **raw) -> Path:
    path = tmp_path / "cfg" / "Plain.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(raw))
    return path


def test_failed_step_names_the_step_of_a_real_failed_first_run(tmp_path) -> None:
    h = Harness(tmp_path, worktree=False)
    assert h.run().status == "failed"
    found = first_run.failed_step(h.path)
    assert found is not None and found[0] == "config"
    assert found[1].tzinfo is not None
    assert abs(found[1].timestamp() - h.report.stat().st_mtime) < 1


def test_failed_step_reads_the_step_after_failed_up_to_the_colon(tmp_path) -> None:
    state = tmp_path / "state"
    state.mkdir()
    path = _plain_config(tmp_path, state_dir=str(state))
    (state / first_run.REPORT_FILE).write_text(
        "first-run: failed dry_run: origin_mismatch\nship_gate: closed\n"
    )
    found = first_run.failed_step(path)
    assert found is not None and found[0] == "dry_run"


def test_failed_step_is_none_for_a_passed_report(tmp_path) -> None:
    h = Harness(tmp_path)
    assert h.run().status == "enabled"
    assert first_run.failed_step(h.path) is None


def test_failed_step_is_none_when_there_is_no_report(tmp_path) -> None:
    h = Harness(tmp_path)
    assert not h.report.exists()
    assert first_run.failed_step(h.path) is None


def test_failed_step_does_not_follow_a_symlinked_report(tmp_path) -> None:
    state = tmp_path / "state"
    state.mkdir()
    path = _plain_config(tmp_path, state_dir=str(state))
    real = tmp_path / "real.txt"
    real.write_text("first-run: failed config: worktree_invalid\n")
    os.symlink(real, state / first_run.REPORT_FILE)
    assert first_run.failed_step(path) is None


def test_failed_step_is_none_for_a_non_utf8_first_line(tmp_path) -> None:
    state = tmp_path / "state"
    state.mkdir()
    path = _plain_config(tmp_path, state_dir=str(state))
    (state / first_run.REPORT_FILE).write_bytes(b"first-run: failed \xff\xfe: x\n")
    assert first_run.failed_step(path) is None


def test_failed_step_finds_the_report_beside_a_config_with_a_relative_state_dir(
    tmp_path,
) -> None:
    path = _plain_config(tmp_path, state_dir="relative/state")
    (path.parent / f"Plain-{first_run.REPORT_FILE}").write_text(
        "first-run: failed config: config_invalid\n"
    )
    found = first_run.failed_step(path)
    assert found is not None and found[0] == "config"


def test_failed_step_finds_the_report_of_an_unreadable_config(tmp_path) -> None:
    path = tmp_path / "cfg" / "Broken.json"
    path.parent.mkdir()
    path.write_text("not json")
    h = Harness(tmp_path)  # only for its router and factory
    first_run.first_run(path, DEFAULTS, h.router, h.factory)
    found = first_run.failed_step(path)
    assert found is not None and found[0] == "config"


def test_failed_step_writes_nothing(tmp_path) -> None:
    h = Harness(tmp_path, worktree=False)
    h.run()
    before = sorted(str(p) for p in tmp_path.rglob("*"))
    first_run.failed_step(h.path)
    assert sorted(str(p) for p in tmp_path.rglob("*")) == before


def test_failed_step_does_not_block_on_a_fifo_at_the_report_path(tmp_path) -> None:
    import threading

    state = tmp_path / "state"
    state.mkdir()
    path = _plain_config(tmp_path, state_dir=str(state))
    os.mkfifo(state / first_run.REPORT_FILE)
    found: list[object] = []
    worker = threading.Thread(
        target=lambda: found.append(first_run.failed_step(path)), daemon=True
    )
    worker.start()
    worker.join(2)
    assert not worker.is_alive(), "failed_step blocked on a FIFO"
    assert found == [None]


def test_failed_step_finds_a_later_step_report_when_the_config_has_no_state_dir(
    tmp_path,
) -> None:
    # first_run writes the report of a step after the config step in the validated state dir,
    # which is the default one when the config names none.
    h = Harness(tmp_path)
    raw = json.loads(h.path.read_text())
    del raw["state_dir"]
    h.path.write_text(json.dumps(raw))
    state = cycle.load_config(h.path).state_dir
    state.mkdir(parents=True)
    (state / first_run.REPORT_FILE).write_text(
        "first-run: failed label: label_failed\n"
    )
    found = first_run.failed_step(h.path)
    assert found is not None and found[0] == "label"


def test_failed_step_finds_a_later_step_report_when_state_dir_is_the_config_folder(
    tmp_path,
) -> None:
    h = Harness(tmp_path, state_dir=str(tmp_path / "cfg"))
    (tmp_path / "cfg" / first_run.REPORT_FILE).write_text(
        "first-run: failed dry_run: origin_mismatch\n"
    )
    found = first_run.failed_step(h.path)
    assert found is not None and found[0] == "dry_run"


def test_failed_step_takes_the_newer_of_the_two_report_locations(tmp_path) -> None:
    h = Harness(tmp_path, state_dir=str(tmp_path / "cfg"))
    old = tmp_path / "cfg" / f"IronClaude-{first_run.REPORT_FILE}"
    new = tmp_path / "cfg" / first_run.REPORT_FILE
    old.write_text("first-run: failed config: worktree_invalid\n")
    new.write_text("first-run: passed\n")
    os.utime(old, (1_000_000, 1_000_000))
    os.utime(new, (2_000_000, 2_000_000))
    assert first_run.failed_step(h.path) is None
    os.utime(old, (3_000_000, 3_000_000))
    found = first_run.failed_step(h.path)
    assert found is not None and found[0] == "config"
