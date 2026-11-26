"""Ledger file store: path, read, lock, atomic write, hook merge and ``add_run``."""

from __future__ import annotations

import json
import multiprocessing
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from superclaude.cli.sweep import ledger
from superclaude.cli.sweep.ledger import (
    LedgerUnavailable,
    LockTimeout,
    add_run,
    compute_counts,
    ledger_path,
    locked,
    merge_hook_entries,
    read_ledger,
    write_atomic,
)

GEN = datetime(2026, 11, 26, 18, 0, 0, 400000, tzinfo=timezone.utc)  # has microseconds


def rid(n: int) -> str:
    return f"run_{n:012x}"


def entry(
    n: int,
    source: str = "build",
    reasons=("unfinished_task",),
    added="2026-11-26T18:00:00Z",
):
    return {"id": rid(n), "source": source, "reasons": list(reasons), "added_at": added}


def make_ledger(runs, generated="2026-11-26T18:00:00Z") -> dict:
    return {
        "version": 1,
        "generated_at": generated,
        "orca": {"runs_listed": 0, "worktrees_listed": 0},
        "counts": compute_counts(runs),
        "runs": runs,
    }


def test_path_precedence_flag_env_xdg(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    monkeypatch.delenv("SUPERCLAUDE_RUN_LEDGER", raising=False)
    assert ledger_path(None) == tmp_path / "xdg" / "superclaude" / "run-ledger.json"
    monkeypatch.setenv("SUPERCLAUDE_RUN_LEDGER", str(tmp_path / "env.json"))
    assert ledger_path(None) == tmp_path / "env.json"
    assert ledger_path(str(tmp_path / "flag.json")) == tmp_path / "flag.json"
    monkeypatch.delenv("XDG_STATE_HOME")
    monkeypatch.delenv("SUPERCLAUDE_RUN_LEDGER")
    assert (
        ledger_path(None)
        == Path.home() / ".local" / "state" / "superclaude" / "run-ledger.json"
    )


def test_atomic_write_leaves_old_file_and_no_tmp_on_failure(monkeypatch, tmp_path):
    path = tmp_path / "run-ledger.json"
    write_atomic(path, make_ledger([entry(1)]))
    before = path.read_bytes()

    def boom(*args, **kwargs):
        raise OSError("replace failed")

    monkeypatch.setattr(os, "replace", boom)
    with pytest.raises(OSError):
        write_atomic(path, make_ledger([entry(1), entry(2)]))
    assert path.read_bytes() == before
    assert [p.name for p in tmp_path.iterdir()] == ["run-ledger.json"]


def test_lock_timeout(tmp_path):
    path = tmp_path / "run-ledger.json"
    with locked(path):
        started = time.monotonic()
        with pytest.raises(LockTimeout), locked(path, timeout=0.2):
            pass
        assert time.monotonic() - started < 2
    with locked(path, timeout=0.2):  # free again after the holder left
        pass


def test_corrupt_ledger_reads_as_none(tmp_path):
    path = tmp_path / "run-ledger.json"
    assert read_ledger(path) is None  # missing
    path.write_text("{not json", encoding="utf-8")
    assert read_ledger(path) is None
    path.write_text(json.dumps({**make_ledger([]), "version": 2}), encoding="utf-8")
    assert read_ledger(path) is None
    path.write_text(
        json.dumps({"version": 1, "runs": []}), encoding="utf-8"
    )  # no generated_at
    assert read_ledger(path) is None
    path.write_text(json.dumps(make_ledger([])), encoding="utf-8")
    assert read_ledger(path)["runs"] == []


def test_read_ledger_rejects_trailing_junk_in_id_and_dedupes(tmp_path):
    path = tmp_path / "run-ledger.json"
    for bad in (rid(1) + "x", rid(1) + "\n", "run_ZZZZZZZZZZZZ", 5):
        path.write_text(
            json.dumps(make_ledger([{**entry(2), "id": bad}])), encoding="utf-8"
        )
        assert read_ledger(path) is None
    first = {**entry(1), "objective": "first"}
    dup = {**entry(1), "objective": "second"}
    path.write_text(json.dumps(make_ledger([first, entry(2), dup])), encoding="utf-8")
    runs = read_ledger(path)["runs"]
    assert [r["id"] for r in runs] == [rid(1), rid(2)]
    assert runs[0]["objective"] == "first"


def test_add_idempotent_and_rejects_bad_id(tmp_path):
    path = tmp_path / "run-ledger.json"
    write_atomic(path, make_ledger([entry(1)]))
    assert add_run(path, rid(2), GEN) is True
    assert add_run(path, rid(2), GEN) is False
    assert add_run(path, rid(1), GEN) is False  # already there as a build row
    data = read_ledger(path)
    assert [r["id"] for r in data["runs"]] == [rid(1), rid(2)]
    added = data["runs"][1]
    assert added == {
        "id": rid(2),
        "source": "hook",
        "reasons": ["hook_added"],
        "added_at": "2026-11-26T18:00:00Z",
    }
    assert data["counts"]["hook_added"] == 1
    for bad in ("run_1", rid(3) + "x", "", "RUN_" + "a" * 12):
        with pytest.raises(ValueError):
            add_run(path, bad, GEN)


def test_add_on_missing_ledger_refuses(tmp_path):
    path = tmp_path / "run-ledger.json"
    with pytest.raises(LedgerUnavailable):
        add_run(path, rid(1), GEN)
    assert not path.exists()
    path.write_text("garbage", encoding="utf-8")
    with pytest.raises(LedgerUnavailable):
        add_run(path, rid(1), GEN)
    assert path.read_text(encoding="utf-8") == "garbage"


def test_add_keeps_generated_at(tmp_path):
    path = tmp_path / "run-ledger.json"
    write_atomic(path, make_ledger([], generated="2026-11-26T10:00:00Z"))
    add_run(path, rid(1), GEN)
    assert read_ledger(path)["generated_at"] == "2026-11-26T10:00:00Z"


def test_merge_replaces_same_id_unions_reasons_and_recomputes_counts():
    new = make_ledger(
        [entry(1, reasons=["live_worktree"]), entry(2, reasons=["unfinished_task"])],
        generated="2026-11-26T18:00:00Z",
    )
    current = make_ledger(
        [
            entry(
                1, source="hook", reasons=["hook_added"], added="2026-11-26T18:00:00Z"
            ),  # same second as GEN
            entry(
                3, source="hook", reasons=["hook_added"], added="2026-11-26T18:05:00Z"
            ),  # new hook row
            entry(
                4, source="hook", reasons=["hook_added"], added="2026-11-26T17:59:59Z"
            ),  # before the rebuild
            entry(
                5, source="hook", reasons=["hook_added"], added="not a time"
            ),  # unparseable
            entry(
                6, source="build", reasons=["new"], added="2026-11-26T18:30:00Z"
            ),  # not a hook row
        ]
    )
    merged = merge_hook_entries(new, current, GEN)
    by_id = {r["id"]: r for r in merged["runs"]}
    assert set(by_id) == {rid(1), rid(2), rid(3)}
    assert by_id[rid(1)]["reasons"] == ["live_worktree", "hook_added"]
    assert by_id[rid(1)]["source"] == "build"  # the build row wins its fields
    assert by_id[rid(3)]["source"] == "hook"
    assert merged["counts"] == compute_counts(merged["runs"])
    assert merged["counts"]["hook_added"] == 2
    assert merged["counts"]["live_worktree"] == 1
    assert new["runs"][0]["reasons"] == ["live_worktree"]  # input not changed


def _adder(path: str, n: int) -> None:
    add_run(Path(path), rid(100 + n), datetime.now(timezone.utc))


def _slow_rebuild(path: str, generated: datetime, delay: float) -> None:
    new = make_ledger([entry(1)], generated=ledger.iso_utc(generated))
    time.sleep(delay)  # the Orca reads, done without the lock
    with locked(Path(path), timeout=30):
        merged = merge_hook_entries(new, read_ledger(Path(path)), generated)
        write_atomic(Path(path), merged)


def test_concurrent_add_and_build_no_lost_append(tmp_path):
    path = tmp_path / "run-ledger.json"
    generated = datetime.now(timezone.utc)
    write_atomic(path, make_ledger([entry(1)], generated=ledger.iso_utc(generated)))
    procs = [
        multiprocessing.Process(target=_slow_rebuild, args=(str(path), generated, 0.6))
    ]
    procs += [
        multiprocessing.Process(target=_adder, args=(str(path), n)) for n in range(20)
    ]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join(60)
        assert proc.exitcode == 0
    ids = [r["id"] for r in read_ledger(path)["runs"]]
    assert {rid(100 + n) for n in range(20)} <= set(ids)
    assert len(ids) == len(set(ids)) == 21
    assert [p.name for p in tmp_path.iterdir() if ".tmp." in p.name] == []
