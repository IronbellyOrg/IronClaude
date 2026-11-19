"""Crash injection at every write and send boundary of a wake (NFR-005, design 4.5 steps 10 and 11).

Each test has one new issue. It runs one cycle with a kill injected at one point,
then runs more cycles against the same state with a plain ``FileStore`` and a fresh
``FakeWaker``. The kill is a ``SystemExit``, which ``run_cycle`` and the CLI never
catch, so it ends the process as a killed one would. The rules under test:

* the entry is saved ``pending`` with its target BEFORE anything is sent;
* a ``pending`` entry at the start of a cycle is a resend to the SAME orchestrator,
  never an ``abandoned`` ``pending_orphan``, never a second orchestrator, never an
  entry with two targets;
* delivery is at least once: the wake is never lost, and it is acknowledged once.
"""

from __future__ import annotations

import json
import os

import pytest

from superclaude.cli.issue_watch import cycle, record, route
from superclaude.cli.issue_watch.record import FileStore

from .conftest import (
    CrashingStore,
    FakeWaker,
    decisions,
    orch_dir,
    read_wake,
    run,
    wake_files,
    write_ack,
)

REPO = "IronbellyOrg/IronClaude"
KEY = f"{REPO}#9"


class Rig:
    """One new issue, the real store and the fakes shared by the runs."""

    def __init__(self, tmp_path, tmp_state, gh_world):
        self.tmp_path = tmp_path
        self.tmp_state = tmp_state
        self.world = gh_world()
        self.world.issue(REPO, 9)
        self.deliveries: list[str] = []

    def waker(self, **kw) -> FakeWaker:
        def record_it(target, wake_id):
            self.deliveries.append(target.orchestrator)

        return FakeWaker(on_deliver=kw.pop("on_deliver", record_it), **kw)

    def crash(self, store, waker=None):
        with pytest.raises(SystemExit):
            cycle.run_cycle(
                self.world.deps(self.tmp_path, store, waker=waker or self.waker()),
                False,
            )

    def entry(self):
        return FileStore(self.tmp_state.state_dir).load().entries.get(KEY)

    def rerun(self, times=1, waker=None):
        out = None
        for _ in range(times):
            out = run(
                self.world,
                self.tmp_path,
                self.tmp_state,
                waker=waker or self.waker(),
                advance=300,
            )
        return out

    def registry(self):
        return sorted(route.load_registry(self.world.config.orchestrator_repo))


@pytest.fixture
def rig(tmp_path, tmp_state, gh_world):
    return Rig(tmp_path, tmp_state, gh_world)


def test_a_kill_before_the_pending_save_loses_nothing_and_starts_no_second_orchestrator(
    rig,
):
    rig.crash(CrashingStore(rig.tmp_state, "C1"))
    assert (
        rig.entry() is None
        and rig.deliveries == []
        and wake_files(rig.world.config) == []
    )
    res = rig.rerun()
    assert res.woken == (KEY,)
    assert rig.registry() == [
        "ironclaude-1"
    ]  # the empty orchestrator of the killed cycle is reused
    assert rig.deliveries == ["ironclaude-1"]


def test_a_kill_after_the_pending_save_and_before_the_wake_file_is_found_as_a_resend(
    rig,
):
    rig.crash(CrashingStore(rig.tmp_state, "C3"))
    e = rig.entry()
    assert (e.state, e.orchestrator, e.wake_attempts) == ("pending", "ironclaude-1", 0)
    assert wake_files(rig.world.config) == [] and rig.deliveries == []
    res = rig.rerun()
    # the same wake goes to the same orchestrator, the count does not change, no second orchestrator
    assert rig.deliveries == ["ironclaude-1"] and rig.registry() == ["ironclaude-1"]
    e = rig.entry()
    assert (e.state, e.orchestrator, e.wake_attempts) == ("woken", "ironclaude-1", 1)
    assert ("pending_orphan", KEY, "pending") in decisions(res) and (
        "woken",
        KEY,
        "woken",
    ) in decisions(res)
    assert res.exit_code == 0  # a resend, not an abandon
    (path,) = wake_files(rig.world.config)
    assert [i["number"] for i in read_wake(path)["assigned"]] == [9]


def test_a_kill_after_the_wake_file_and_before_the_send_sends_the_same_wake_to_the_same_orchestrator(
    rig,
):
    def die(target, wake_id):
        raise SystemExit("killed between the file and the send")

    rig.crash(rig.tmp_state, waker=FakeWaker(on_deliver=die))
    (first,) = wake_files(rig.world.config)
    e = rig.entry()
    assert (e.state, e.orchestrator) == ("pending", "ironclaude-1")
    res = rig.rerun()
    assert rig.deliveries == ["ironclaude-1"] and rig.registry() == ["ironclaude-1"]
    assert (
        len(wake_files(rig.world.config)) == 2
    )  # the orphan file stays; the resend has its own id
    first_data = read_wake(first)
    second = next(read_wake(p) for p in wake_files(rig.world.config) if p != first)
    assert (
        second["assigned"] == first_data["assigned"]
        and second["target"] == first_data["target"]
    )
    e = rig.entry()
    assert (e.state, e.wake_id, e.wake_attempts) == ("woken", second["wake_id"], 1)
    assert res.exit_code == 0


def test_a_kill_before_the_final_commit_after_the_send_gives_at_least_one_more_delivery(
    rig,
):
    rig.crash(CrashingStore(rig.tmp_state, "C4"))
    assert rig.deliveries == ["ironclaude-1"]  # it was sent
    assert (
        rig.entry().state == "pending"
    )  # the poll never learned it, so it will send again: at least once
    rig.rerun()
    assert rig.deliveries == ["ironclaude-1", "ironclaude-1"] and rig.registry() == [
        "ironclaude-1"
    ]
    assert rig.entry().state == "woken"
    write_ack(rig.world.config, rig.entry().wake_id, taken=[(REPO, 9)])
    rig.rerun(waker=rig.waker())
    assert rig.entry().state == "acked"
    rig.rerun(times=3)
    assert len(rig.deliveries) == 2  # acknowledged once: nothing more is ever sent


def test_a_kill_after_the_final_commit_loses_nothing_and_sends_nothing_twice(rig):
    rig.crash(CrashingStore(rig.tmp_state, "C5"))
    assert rig.deliveries == ["ironclaude-1"] and rig.entry().state == "woken"
    rig.rerun()
    assert rig.deliveries == ["ironclaude-1"]  # the lease of 10 minutes has not run out


def test_a_kill_during_the_atomic_write_leaves_the_old_store_whole(rig, monkeypatch):
    before = (rig.tmp_state.state_dir / "dispatch.json").read_bytes()
    calls = {"n": 0}
    real = os.replace

    def boom(src, dst):
        calls["n"] += 1
        if str(dst).endswith("dispatch.json"):
            raise SystemExit("killed during the rename")
        return real(src, dst)

    monkeypatch.setattr(os, "replace", boom)
    rig.crash(rig.tmp_state)
    monkeypatch.undo()
    assert (
        rig.tmp_state.state_dir / "dispatch.json"
    ).read_bytes() == before  # C2: old file, not a half one
    assert rig.deliveries == []
    rig.tmp_state.load()  # still valid
    assert rig.rerun().woken == (KEY,)


@pytest.mark.parametrize("crash_at", [None, "C1", "C3", "C4", "C5"])
def test_after_any_kill_five_more_cycles_never_route_to_a_second_orchestrator_or_abandon_the_issue(
    rig, crash_at
):
    rig.crash(CrashingStore(rig.tmp_state, crash_at or "C3"))
    for _ in range(5):
        res = rig.rerun()
        assert res.exit_code == 0
    assert rig.registry() == ["ironclaude-1"]
    e = rig.entry()
    assert e.orchestrator == "ironclaude-1" and e.state in ("woken", "pending")
    assert e.last_reason != "pending_orphan" or e.state == "pending"
    assert all(who == "ironclaude-1" for who in rig.deliveries)
    doc = FileStore(rig.tmp_state.state_dir).load()
    assert {x.orchestrator for x in doc.entries.values()} == {
        "ironclaude-1"
    }  # no entry with two targets
    assert json.loads(
        (orch_dir(rig.world.config) / "orchestrators.json").read_text()
    ).keys() == {"ironclaude-1"}


def test_a_failing_store_save_ends_the_cycle_with_exit_6_before_anything_is_sent(rig):
    from .conftest import FailingStore

    waker = rig.waker()
    res = run(
        rig.world,
        rig.tmp_path,
        rig.tmp_state,
        waker=waker,
        store=FailingStore(rig.tmp_state, fail_saves=(1,)),
    )
    assert (res.exit_code, res.reason) == (
        6,
        "state_dir_unwritable",
    ) and rig.deliveries == []
    assert wake_files(rig.world.config) == []
    assert record.FileStore(rig.tmp_state.state_dir).load().entries == {}
