"""Two processes on one store, and the lock-file failure modes (FR-017, AC-11).

``test_two_processes_one_store_one_launch`` starts real ``spawn`` processes that
run one whole cycle each against the same ``tmp_path`` store. The order is fixed
by files, not by sleeping: worker 1 is started alone and, from inside its
``FakeLauncher`` (that is, while it holds the lock), writes ``worker1.holding``
and waits for ``worker2.result``. The main process starts worker 2 only after
``worker1.holding`` exists, so worker 2 always meets a held lock. Every wait is
a bounded poll for a file; a worker that does not finish is terminated.

The single-process cases drive ``run_cycle`` through a ``lock`` that is a
symlink, a directory, missing, or replaced after ``flock`` (decision DF-34).
"""

from __future__ import annotations

import fcntl
import json
import multiprocessing
import os
import sys
import time
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import cycle
from superclaude.cli.issue_watch.record import FileStore

from .conftest import (
    CYCLE_NOW,
    FakeClock,
    FakeLauncher,
    GhWorld,
    launched_outcome,
    make_config,
    make_deps,
)

ISSUE = 11
# A bound, not a delay: a poll returns as soon as its file exists. It is far above
# the few seconds a spawned interpreter needs, even on a loaded xdist machine.
WAIT_S = 30.0
JOIN_S = 60.0
ROOT_LINE = "20 1 8:1 / / rw,relatime shared:1 - ext4 /dev/sda1 rw"


@pytest.fixture(autouse=True)
def _no_real_mountinfo(monkeypatch):
    """The cycle checks the state directory's filesystem; never read the real /proc."""
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: ROOT_LINE + "\n")


def _wait_for(path: Path, timeout_s: float, *, stop=lambda: False) -> bool:
    """Poll for ``path`` for at most ``timeout_s``; True when it exists."""
    deadline = time.monotonic() + timeout_s
    while True:
        if path.exists():
            return True
        if stop() or time.monotonic() >= deadline:
            return False
        time.sleep(0.01)


def _write_atomic(path: Path, text: str) -> None:
    """Write ``text`` so that a reader sees the whole file or no file."""
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _lock_is_held(lock: Path) -> bool:
    """True when another open file description holds ``lock`` (probe, then undo)."""
    fd = os.open(lock, os.O_RDWR)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    finally:
        os.close(fd)


def _worker(root: str, name: str) -> None:
    """Run one cycle against the store under ``root`` and exit with its code.

    Module level so that the ``spawn`` start method can import it by name
    (``tests.issue_watch.test_concurrency``). It builds its own fakes and writes
    ``<name>.result`` (JSON) in ``root`` before it exits.
    """
    base = Path(root)
    state_dir = base / "state"
    outcome: dict = {"name": name, "exit_code": 99, "reason": "worker_crashed"}
    try:
        cycle._read_mountinfo = lambda: ROOT_LINE + "\n"  # no real /proc read
        config = make_config(base)  # the files exist already; nothing is rewritten
        clock = FakeClock(CYCLE_NOW)
        world = GhWorld(clock, config)
        world.issue(ISSUE)
        probe: dict = {}

        def hold_and_wait() -> None:
            # Runs inside the launcher call, so inside the cycle's lock.
            probe["held"] = _lock_is_held(state_dir / "lock")
            _write_atomic(base / "worker1.holding", "1")
            _wait_for(base / "worker2.result", WAIT_S)

        launcher = FakeLauncher(
            [launched_outcome()], on_call=hold_and_wait if name == "worker1" else None
        )
        deps = make_deps(
            base,
            FileStore(state_dir),
            runner=world.runner,
            launcher=launcher,
            clock=clock,
            config=config,
            which=world.which,
        )
        res = cycle.run_cycle(deps, False)
        outcome = {
            "name": name,
            "exit_code": res.exit_code,
            "reason": res.reason,
            "launcher_calls": len(launcher.calls),
            "runner_calls": len(world.runner.calls),
            "unexpected": [list(argv) for argv in world.runner.unexpected],
            "lock_held_during_launch": probe.get("held"),
        }
    finally:
        _write_atomic(base / f"{name}.result", json.dumps(outcome))
    sys.exit(outcome["exit_code"])


def _read_result(base: Path, name: str) -> dict:
    return json.loads((base / f"{name}.result").read_text(encoding="utf-8"))


def _cycle_lines(state_dir: Path) -> list[dict]:
    lines = (state_dir / "audit.jsonl").read_text(encoding="utf-8").splitlines()
    return [ln for ln in map(json.loads, lines) if ln["kind"] == "cycle"]


def test_two_processes_one_store_one_launch__fr017_ac11(tmp_path, tmp_state):
    make_config(tmp_path)  # worktree and approvers exist before any worker starts
    ctx = multiprocessing.get_context("spawn")
    one = ctx.Process(target=_worker, args=(str(tmp_path), "worker1"))
    two = ctx.Process(target=_worker, args=(str(tmp_path), "worker2"))
    started: list = []
    try:
        one.start()
        started.append(one)
        holding = _wait_for(
            tmp_path / "worker1.holding", WAIT_S, stop=lambda: one.exitcode is not None
        )
        assert holding, f"worker 1 never held the lock (exitcode {one.exitcode})"
        two.start()
        started.append(two)
        two.join(timeout=JOIN_S)
        one.join(timeout=JOIN_S)
        assert two.exitcode is not None, "worker 2 did not finish"
        assert one.exitcode is not None, "worker 1 did not finish"
    finally:
        for proc in started:
            if proc.is_alive():
                proc.terminate()
                proc.join(timeout=10)

    first, second = _read_result(tmp_path, "worker1"), _read_result(tmp_path, "worker2")
    assert (one.exitcode, two.exitcode) == (0, 75), (first, second)
    assert first["lock_held_during_launch"] is True, first
    assert (first["exit_code"], first["reason"]) == (0, "cycle_complete"), first
    assert first["launcher_calls"] == 1, first
    assert (second["exit_code"], second["reason"]) == (75, "lock_held"), second
    # Worker 2 made no external call at all: no gh, no git, no Orca.
    assert (second["runner_calls"], second["launcher_calls"]) == (0, 0), second
    assert first["unexpected"] == [] and second["unexpected"] == []
    assert first["launcher_calls"] + second["launcher_calls"] == 1

    entry = tmp_state.load().entries[ISSUE]
    assert (entry.state, entry.launches) == ("launched", 1)
    cycle_lines = sorted(
        (ln["exit"], ln["reason"]) for ln in _cycle_lines(tmp_state.state_dir)
    )
    assert cycle_lines == [(0, "cycle_complete"), (75, "lock_held")]


# ---- single-process lock-file cases -------------------------------------------


def _run(tmp_path, tmp_state, gh_world):
    """One real-store cycle with one eligible issue; returns (result, world, deps)."""
    world = gh_world()
    world.issue(ISSUE)
    deps = world.deps(tmp_path, tmp_state)
    return cycle.run_cycle(deps, False), world, deps


def _assert_stopped_before_any_call(res, world, deps, tmp_state, before, exit_code):
    assert res.exit_code == exit_code
    assert world.runner.calls == []  # no gh, git or Orca call
    assert deps.launcher.calls == []
    assert (tmp_state.state_dir / "dispatch.json").read_bytes() == before


def test_intact_lock_launches_the_eligible_issue__fr017(tmp_path, tmp_state, gh_world):
    res, world, deps = _run(tmp_path, tmp_state, gh_world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert len(deps.launcher.calls) == 1
    assert world.gh_argvs  # the control: this world does reach gh


def test_symlinked_lock_is_exit_6_with_no_call__fr017_ac11(
    tmp_path, tmp_state, gh_world
):
    lock = tmp_state.state_dir / "lock"
    target = tmp_path / "real-lock"
    target.write_bytes(b"")  # a regular file of our own: only O_NOFOLLOW refuses it
    lock.unlink()
    lock.symlink_to(target)
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    res, world, deps = _run(tmp_path, tmp_state, gh_world)
    _assert_stopped_before_any_call(res, world, deps, tmp_state, before, 6)
    assert res.reason == "lock_invalid"
    assert lock.is_symlink()  # nothing deleted or replaced it


def test_directory_in_place_of_lock_is_exit_6_with_no_call__fr017_ac11(
    tmp_path, tmp_state, gh_world
):
    lock = tmp_state.state_dir / "lock"
    lock.unlink()
    lock.mkdir()
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    res, world, deps = _run(tmp_path, tmp_state, gh_world)
    _assert_stopped_before_any_call(res, world, deps, tmp_state, before, 6)
    assert res.reason == "lock_invalid"
    assert lock.is_dir()


def test_missing_lock_is_exit_6_and_is_not_created__fr017_ac11(
    tmp_path, tmp_state, gh_world
):
    lock = tmp_state.state_dir / "lock"
    lock.unlink()
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    res, world, deps = _run(tmp_path, tmp_state, gh_world)
    _assert_stopped_before_any_call(res, world, deps, tmp_state, before, 6)
    assert res.reason == "lock_missing"
    assert not os.path.lexists(lock)  # only init-state creates the lock


def test_lock_path_replaced_after_flock_is_exit_75_with_no_call__fr017_ac11(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    lock = tmp_state.state_dir / "lock"
    real = fcntl.flock
    swaps: list[bool] = []

    def flock_then_replace(fd, op):
        real(fd, op)
        if op & fcntl.LOCK_EX and not swaps:
            swaps.append(True)
            fresh = lock.with_name("lock.new")
            fresh.write_bytes(b"")
            os.replace(fresh, lock)  # the locked inode is no longer the path's

    monkeypatch.setattr(fcntl, "flock", flock_then_replace)
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    res, world, deps = _run(tmp_path, tmp_state, gh_world)
    assert swaps == [True]
    _assert_stopped_before_any_call(res, world, deps, tmp_state, before, 75)
    assert res.reason == "lock_held"
