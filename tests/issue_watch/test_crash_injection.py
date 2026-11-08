"""Crash injection at every write and spawn boundary of a launch (NFR-005, AC-17).

Each test has one eligible issue. It runs one cycle with a crash injected at one
of the five points of design section 7.6 (C1 to C5, research/06 Table 1.3), then
runs FIVE more cycles against the same state directory with a plain
``FileStore`` and a fresh ``FakeLauncher``. Across all six runs the launcher is
called at most once in total, and once a launcher call is recorded the stored
entry always says ``launches`` 1 (at-most-once). The crash is a ``SystemExit``,
which ``run_cycle`` and the CLI never catch, so it ends the process as a
killed one would, apart from the lock and file descriptors Python still closes.
"""

from __future__ import annotations

import json
import os
from typing import NamedTuple

import pytest

from superclaude.cli.issue_watch import cycle, github
from superclaude.cli.issue_watch.record import Entry, FileStore

from .conftest import (
    APPROVER_ID,
    CYCLE_NOW,
    OWN_ID,
    OWN_LOGIN,
    T_APPROVED,
    CrashingStore,
    FakeLauncher,
    launched_outcome,
)

ISSUE = 9
RERUNS = 5
GAP_S = 300  # the clock moves 5 minutes before each run, as a timer would
PROMPT = f"/sc:issue --claim {ISSUE}"
USER_ARGV = tuple(github.argv_user())


def _launched_every_time(call_number: int):
    return launched_outcome()


def _audit_bytes(state_dir) -> bytes:
    path = state_dir / "audit.jsonl"
    return path.read_bytes() if path.exists() else b""


def _audit_lines(state_dir) -> list[dict]:
    return [
        json.loads(text)
        for text in _audit_bytes(state_dir).decode("utf-8").splitlines()
    ]


def _decisions(res) -> list[tuple]:
    """``(reason, issue, state)`` of each decision line of one cycle, in order."""
    return [
        (ln["reason"], ln["issue"], ln.get("state"))
        for ln in res.lines
        if ln["kind"] == "decision"
    ]


class Run(NamedTuple):
    when: object
    res: cycle.CycleResult
    entry: Entry | None


class Rig:
    """One eligible issue, the real store and the fakes shared by the six runs."""

    def __init__(self, tmp_path, tmp_state, gh_world, crash_launcher=None):
        self.tmp_path = tmp_path
        self.tmp_state = tmp_state
        self.state_dir = tmp_state.state_dir
        self.world = gh_world()
        self.world.issue(ISSUE)
        self.crash_launcher = crash_launcher or FakeLauncher(_launched_every_time)
        self.rerun_launcher = FakeLauncher(_launched_every_time)
        self.store_before = self.store_bytes()
        self.names_before = self.file_names()
        self.audit_before = _audit_bytes(self.state_dir)

    # -- the state on disk ----------------------------------------------------

    def store_bytes(self) -> bytes:
        return (self.state_dir / "dispatch.json").read_bytes()

    def file_names(self) -> list[str]:
        return sorted(p.name for p in self.state_dir.iterdir())

    def doc(self):
        return FileStore(self.state_dir).load()

    def entry(self) -> Entry | None:
        return self.doc().entries.get(ISSUE)

    # -- the runs ---------------------------------------------------------------

    def deps(self, store, launcher) -> cycle.Deps:
        return self.world.deps(self.tmp_path, store, launcher=launcher)

    def crash(self, store, expected=SystemExit):
        """Run one cycle that must end with ``expected`` (the injected crash)."""
        with pytest.raises(expected) as raised:
            cycle.run_cycle(self.deps(store, self.crash_launcher), False)
        return raised.value

    @property
    def launcher_calls(self) -> int:
        return len(self.crash_launcher.calls) + len(self.rerun_launcher.calls)

    def check_at_most_once(self, label: str) -> None:
        assert self.launcher_calls <= 1, (
            f"{label}: the launcher was called {self.launcher_calls} times in total"
        )
        if self.launcher_calls >= 1:
            entry = self.entry()
            assert entry is not None and entry.launches == 1, (
                f"{label}: a launcher call is recorded but the entry is {entry}"
            )

    def assert_untouched_audit(self) -> None:
        """The crashed cycle wrote no audit line at all (its lines are written last)."""
        assert _audit_bytes(self.state_dir) == self.audit_before

    def reruns(self) -> list[Run]:
        """Run five more cycles with a plain store; check every one (DF-15)."""
        # The lock the crashed cycle held must be free (released in a finally).
        with FileStore(self.state_dir).lock():
            pass
        runs: list[Run] = []
        for number in range(1, RERUNS + 1):
            self.world.clock.advance(GAP_S)
            store = FileStore(self.state_dir)
            res = cycle.run_cycle(self.deps(store, self.rerun_launcher), False)
            runs.append(Run(self.world.clock.now(), res, self.entry()))
            self.check_at_most_once(f"rerun {number}")
            assert (res.exit_code, res.reason) == (0, "cycle_complete"), (
                f"rerun {number}: exit {res.exit_code} reason {res.reason}"
            )
        # All five really ran: each one asked gh for the own login.
        assert self.world.gh_argvs.count(USER_ARGV) == 1 + RERUNS
        assert len({run.res.cycle_id for run in runs}) == RERUNS
        return runs

    def check_runs(self, runs, first, later, launched_first: bool) -> None:
        """The decision lines and the launch of each rerun, and a stable entry."""
        for number, run in enumerate(runs, start=1):
            want = first if number == 1 else later
            assert _decisions(run.res) == want, f"rerun {number}: {run.res.lines}"
            launched = ISSUE if (number == 1 and launched_first) else None
            assert run.res.launched_issue == launched, f"rerun {number}"
            # After the first rerun nothing may change the entry any more.
            assert run.entry == runs[0].entry, f"rerun {number}"

    def launched_decisions(self) -> list[dict]:
        return [
            ln
            for ln in _audit_lines(self.state_dir)
            if ln["kind"] == "decision" and ln["reason"] == "launched"
        ]

    def assert_pending(self, entry: Entry, when) -> None:
        cfg = self.world.config
        assert entry is not None
        assert (entry.state, entry.launches, entry.attempts) == ("pending", 1, 0)
        assert (entry.consumed_at, entry.pending_at) == (when, when)
        assert (entry.operation_id, entry.last_reason) == (None, None)
        assert (entry.approver_id, entry.approval_event_id) == (APPROVER_ID, 2)
        assert entry.approved_at == T_APPROVED
        assert entry.launch_cwd == str(cfg.worktree)
        assert (entry.launch_login, entry.launch_account_id) == (OWN_LOGIN, OWN_ID)


# Rerun expectations: (reason, issue, state) of each decision line.
LAUNCHED = ("launched", ISSUE, "launched")
DISPATCHED = ("already_dispatched", ISSUE, None)
ORPHAN = ("pending_orphan", ISSUE, "abandoned")


def _assert_launched_by_first_rerun(rig: Rig, runs: list[Run]) -> None:
    """C1 and C2: the issue launches exactly once, in the first rerun."""
    rig.check_runs(runs, [LAUNCHED], [DISPATCHED], launched_first=True)
    assert rig.crash_launcher.calls == []
    assert len(rig.rerun_launcher.calls) == 1
    assert rig.rerun_launcher.calls[0][2] == PROMPT
    entry = runs[0].entry
    assert (entry.state, entry.launches) == ("launched", 1)
    assert entry.operation_id == launched_outcome().operation_id
    assert (entry.consumed_at, entry.pending_at) == (runs[0].when, runs[0].when)
    assert len(rig.launched_decisions()) == 1


def _assert_swept_by_first_rerun(rig: Rig, runs: list[Run], when_pending) -> None:
    """C3, C4 and an escaped exception: the pending entry is swept, never relaunched."""
    rig.check_runs(runs, [ORPHAN, DISPATCHED], [DISPATCHED], launched_first=False)
    assert rig.rerun_launcher.calls == []
    entry = runs[0].entry
    assert (entry.state, entry.last_reason) == ("abandoned", "pending_orphan")
    assert entry.launches == 1
    assert entry.operation_id is None
    assert (entry.consumed_at, entry.pending_at) == (when_pending, when_pending)
    assert entry.updated_at == runs[0].when
    assert rig.launched_decisions() == []


# ==============================================================================
# C1: before the pending save
# ==============================================================================


def test_c1_crash_before_the_pending_save_leaves_the_store_untouched__nfr005(
    tmp_path, tmp_state, gh_world
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    store = CrashingStore(tmp_state, "C1")
    assert rig.crash(store).code == "crash C1"
    assert store.saves == 1
    assert rig.store_bytes() == rig.store_before
    assert rig.file_names() == rig.names_before  # no tmp file either
    assert rig.entry() is None
    assert rig.crash_launcher.calls == []
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the crash")
    _assert_launched_by_first_rerun(rig, rig.reruns())


# ==============================================================================
# C2: during write_prepared_bytes (os.replace of the pending save)
# ==============================================================================


def test_c2_crash_during_the_atomic_replace_keeps_the_old_file__nfr005(
    tmp_path, tmp_state, gh_world, monkeypatch, capsys
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    real_replace = os.replace
    hits: list[tuple[str, str]] = []

    def replace_once(src, dst, *args, **kwargs):
        if str(dst).endswith("dispatch.json") and not hits:
            hits.append((str(src), str(dst)))
            raise SystemExit("crash C2")
        return real_replace(src, dst, *args, **kwargs)

    with monkeypatch.context() as patch:  # the reruns use the real os.replace
        patch.setattr(os, "replace", replace_once)
        assert rig.crash(FileStore(rig.state_dir)).code == "crash C2"
    assert os.replace is real_replace
    # The patch was really hit, once, on the store file.
    assert len(hits) == 1
    src, dst = hits[0]
    assert dst == str(rig.state_dir / "dispatch.json")
    assert os.path.basename(src).startswith("dispatch.json.")
    assert src.endswith(".tmp")

    assert rig.store_bytes() == rig.store_before  # the old file, byte for byte
    assert rig.entry() is None
    orphans = sorted(rig.state_dir.glob("dispatch.json.*.tmp"))
    assert [str(p) for p in orphans] == [src]  # SystemExit skips the unlink
    assert rig.file_names() == sorted([*rig.names_before, orphans[0].name])
    orphan_bytes = orphans[0].read_bytes()
    pending = json.loads(orphan_bytes)["entries"][str(ISSUE)]
    assert (pending["state"], pending["launches"]) == ("pending", 1)
    assert rig.crash_launcher.calls == []
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the crash")

    runs = rig.reruns()
    _assert_launched_by_first_rerun(rig, runs)
    # The orphan is ignored: still there, untouched, no error and no audit failure.
    assert orphans[0].read_bytes() == orphan_bytes
    assert capsys.readouterr().err == ""
    assert {ln["kind"] for ln in _audit_lines(rig.state_dir)} == {"decision", "cycle"}


# ==============================================================================
# C3: after the pending save, before the spawn
# ==============================================================================


def test_c3_crash_after_the_pending_save_is_swept_and_never_launched__nfr005(
    tmp_path, tmp_state, gh_world
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    store = CrashingStore(tmp_state, "C3")
    assert rig.crash(store).code == "crash C3"
    assert store.saves == 1
    rig.assert_pending(rig.entry(), CYCLE_NOW)
    doc = rig.doc()  # the second save never happened
    assert (doc.considered, doc.last_completed_cycle_at) == ({}, None)
    assert rig.file_names() == rig.names_before  # the replace completed: no orphan
    assert rig.crash_launcher.calls == []
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the crash")
    _assert_swept_by_first_rerun(rig, rig.reruns(), CYCLE_NOW)
    assert rig.launcher_calls == 0


# ==============================================================================
# C4: after the spawn, before the outcome save
# ==============================================================================


def test_c4_crash_after_the_spawn_is_swept_and_never_launched_again__nfr005(
    tmp_path, tmp_state, gh_world
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    store = CrashingStore(tmp_state, "C4")
    assert rig.crash(store).code == "crash C4"
    assert store.saves == 2
    rig.assert_pending(rig.entry(), CYCLE_NOW)  # the outcome was lost
    doc = rig.doc()
    assert (doc.considered, doc.last_completed_cycle_at) == ({}, None)
    assert [call[2] for call in rig.crash_launcher.calls] == [PROMPT]
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the crash")
    _assert_swept_by_first_rerun(rig, rig.reruns(), CYCLE_NOW)
    assert rig.launcher_calls == 1  # still the one call of the crashed cycle


def test_an_exception_out_of_the_launcher_leaves_the_same_state_as_c4__nfr005(
    tmp_path, tmp_state, gh_world
):
    boom = FakeLauncher(raises=RuntimeError("fake: launcher failed"))
    rig = Rig(tmp_path, tmp_state, gh_world, crash_launcher=boom)
    error = rig.crash(FileStore(rig.state_dir), expected=RuntimeError)
    assert str(error) == "fake: launcher failed"
    rig.assert_pending(rig.entry(), CYCLE_NOW)
    assert [call[2] for call in boom.calls] == [PROMPT]
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the exception")
    _assert_swept_by_first_rerun(rig, rig.reruns(), CYCLE_NOW)
    assert rig.launcher_calls == 1


# ==============================================================================
# C5: after the outcome save, before the audit append
# ==============================================================================


def test_c5_crash_after_the_outcome_save_loses_only_the_audit_lines__nfr005(
    tmp_path, tmp_state, gh_world
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    store = CrashingStore(tmp_state, "C5")
    assert rig.crash(store).code == "crash C5"
    assert store.saves == 2
    entry = rig.entry()  # the final state is on disk
    assert (entry.state, entry.launches) == ("launched", 1)
    assert entry.operation_id == launched_outcome().operation_id
    assert (entry.consumed_at, entry.pending_at) == (CYCLE_NOW, CYCLE_NOW)
    doc = rig.doc()
    assert ISSUE in doc.considered
    assert doc.last_completed_cycle_at == CYCLE_NOW
    assert rig.file_names() == rig.names_before
    assert [call[2] for call in rig.crash_launcher.calls] == [PROMPT]
    # No decision line for this launch (no line of the cycle was written).
    rig.assert_untouched_audit()
    assert rig.launched_decisions() == []
    rig.check_at_most_once("after the crash")

    runs = rig.reruns()
    rig.check_runs(runs, [DISPATCHED], [DISPATCHED], launched_first=False)
    assert all(run.entry == entry for run in runs)  # the saved entry never changed
    assert rig.rerun_launcher.calls == []
    assert rig.launcher_calls == 1
    assert rig.launched_decisions() == []  # that one audit line is the only loss
