"""``superclaude sweep ledger`` through click's CliRunner with a fake Orca runner."""

from __future__ import annotations

import contextlib
import json
import os
from datetime import datetime, timedelta, timezone

import pytest
from click.testing import CliRunner

from superclaude.cli.sweep import commands, ledger
from superclaude.cli.sweep.ledger import LockTimeout, read_ledger, write_atomic
from tests.run_ledger.test_build import WT, FakeOrca, rid
from tests.run_ledger.test_store import entry, make_ledger


def ago(**delta) -> str:
    """SQLite-form time (as Orca prints it) this long ago."""
    return (datetime.now(timezone.utc) - timedelta(**delta)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def iso_ago(**delta) -> str:
    return ledger.iso_utc(datetime.now(timezone.utc) - timedelta(**delta))


def make_run(n: int, created: str, updated: str | None = None) -> dict:
    return {
        "id": rid(n),
        "objective": f"run {n}",
        "legacy": 0,
        "created_at": created,
        "updated_at": updated or created,
    }


def invoke(args, fake=None, monkeypatch=None):
    if fake is not None:
        monkeypatch.setattr(ledger, "orca_runner", fake)
    return CliRunner().invoke(commands.sweep_group, ["ledger", *args])


@pytest.fixture
def old_ledger(tmp_path):
    path = tmp_path / "run-ledger.json"
    write_atomic(path, make_ledger([entry(9)], generated=iso_ago(hours=1)))
    return path


def test_orca_failure_keeps_old_ledger(monkeypatch, old_ledger):
    before, mtime = old_ledger.read_bytes(), old_ledger.stat().st_mtime_ns
    result = invoke(["--ledger", str(old_ledger)], lambda args: (1, ""), monkeypatch)
    assert result.exit_code == 1
    assert result.stderr.startswith("orca-failure:")
    assert old_ledger.read_bytes() == before
    assert old_ledger.stat().st_mtime_ns == mtime


def test_implausibly_empty_keeps_old_ledger(monkeypatch, old_ledger):
    before = old_ledger.read_bytes()
    fake = FakeOrca(
        [make_run(1, ago(hours=12))], worktrees=[WT]
    )  # recent, not new, no Task: 0 kept
    result = invoke(["--ledger", str(old_ledger)], fake, monkeypatch)
    assert result.exit_code == 1
    assert result.stderr.startswith("implausible:")
    assert old_ledger.read_bytes() == before


def test_accept_empty_overrides_guard_not_orca_failure(monkeypatch, old_ledger):
    fake = FakeOrca([make_run(1, ago(hours=12))], worktrees=[WT])
    result = invoke(["--ledger", str(old_ledger), "--accept-empty"], fake, monkeypatch)
    assert result.exit_code == 0, result.stderr
    assert read_ledger(old_ledger)["runs"] == []
    failed = invoke(
        ["--ledger", str(old_ledger), "--accept-empty"],
        lambda args: (1, ""),
        monkeypatch,
    )
    assert failed.exit_code == 1
    assert failed.stderr.startswith("orca-failure:")


def test_dry_run_writes_nothing(monkeypatch, tmp_path):
    path = tmp_path / "run-ledger.json"
    fake = FakeOrca([make_run(1, ago(hours=1))], worktrees=[WT])
    result = invoke(["--ledger", str(path), "--dry-run"], fake, monkeypatch)
    assert result.exit_code == 0, result.stderr
    assert "dry run, nothing written" in result.stdout
    assert rid(1) in result.stdout
    assert list(tmp_path.iterdir()) == []


def test_summary_reports_stale_and_blocked_counts(monkeypatch, tmp_path):
    path = tmp_path / "run-ledger.json"
    old_blocked = {"status": "blocked", "created_at": ago(days=10)}
    fake = FakeOrca(
        [make_run(1, ago(days=20))],
        worktrees=[WT],
        tasks={rid(1): [old_blocked]},
    )
    result = invoke(["--ledger", str(path)], fake, monkeypatch)
    assert result.exit_code == 0, result.stderr
    assert "older than 7 days: 1" in result.stdout
    assert "held in only by blocked Tasks: 1" in result.stdout
    as_json = invoke(["--ledger", str(path), "--json", "--dry-run"], fake, monkeypatch)
    data = json.loads(as_json.stdout)
    assert data["written"] is False
    assert data["ledger"]["counts"]["open_task_stale_7d_only"] == 1
    assert data["ledger"]["counts"]["blocked_only"] == 1
    assert read_ledger(path)["runs"][0]["id"] == rid(1)


def test_add_exit_codes(tmp_path):
    path = tmp_path / "run-ledger.json"
    missing = CliRunner().invoke(
        commands.sweep_group, ["ledger", "--ledger", str(path), "--add", rid(1)]
    )
    assert missing.exit_code == 1
    assert missing.stderr.startswith("implausible:")
    assert not path.exists()
    write_atomic(path, make_ledger([], generated=iso_ago(hours=1)))
    added = CliRunner().invoke(
        commands.sweep_group, ["ledger", "--ledger", str(path), "--add", rid(1)]
    )
    assert added.exit_code == 0
    assert rid(1) in [r["id"] for r in read_ledger(path)["runs"]]
    malformed = CliRunner().invoke(
        commands.sweep_group, ["ledger", "--ledger", str(path), "--add", "run_zz"]
    )
    assert malformed.exit_code == 2


def test_lock_timeout_exit_3(monkeypatch, old_ledger):
    @contextlib.contextmanager
    def busy(path, timeout=10):
        raise LockTimeout("busy")
        yield

    monkeypatch.setattr(ledger, "locked", busy)
    before = old_ledger.read_bytes()
    fake = FakeOrca([make_run(1, ago(hours=1))], worktrees=[WT])
    rebuild = invoke(["--ledger", str(old_ledger)], fake, monkeypatch)
    assert rebuild.exit_code == 3
    adding = invoke(["--ledger", str(old_ledger), "--add", rid(2)])
    assert adding.exit_code == 3
    assert old_ledger.read_bytes() == before
    assert [p.name for p in old_ledger.parent.iterdir()] == [old_ledger.name]


def test_first_build_with_no_previous_ledger_uses_24h_fallback(monkeypatch, tmp_path):
    path = tmp_path / "run-ledger.json"
    fake = FakeOrca(
        [make_run(1, ago(hours=2)), make_run(2, ago(hours=30))],
        worktrees=[WT],
    )
    result = invoke(["--ledger", str(path)], fake, monkeypatch)
    assert result.exit_code == 0, result.stderr
    data = read_ledger(path)
    assert [r["id"] for r in data["runs"]] == [rid(1)]
    assert data["runs"][0]["reasons"] == ["new"]
    assert os.stat(path).st_mode & 0o777  # written, readable
