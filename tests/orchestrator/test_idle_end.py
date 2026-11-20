"""``idle-end`` (5.7 point 5, wave 9): end only when nothing is pending, holding ``state.lock`` the whole time."""

from __future__ import annotations

import json
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import route, wake
from superclaude.cli.orchestrator import idle_end, state
from superclaude.cli.orchestrator.state import StateError

from .fake_world import ORCH, REPO, WID, call, golden, make_root, put_wake

ACK = {
    "schema": "orchestrator-wake-ack/1",
    "wake_id": WID,
    "acked_at": "2026-11-19T10:16:00Z",
    "orchestrator": {"id": ORCH, "run_id": "run_abc123", "host": "ws-aidev02"},
    "taken": [],
    "skipped": [],
    "rejected_items": [],
    "warnings": [],
}


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return make_root(tmp_path)


def run_status(root: Path) -> str:
    return state.load_run(root, ORCH)["status"]


def end(root: Path) -> tuple[int, dict]:
    return call(root, "idle-end")


def lock_is_held(root: Path) -> bool:
    """True when another open file description cannot take ``state.lock`` right now."""
    try:
        with route.state_lock(root, wait_s=0.05):
            return False
    except route.StateLockBusy:
        return True


@pytest.fixture
def sequence(monkeypatch) -> list[str]:
    """Every status ``idle-end`` sets, in order (the real function still runs)."""
    seen: list[str] = []
    real = state.set_run_status

    def spy(root, ident, status):
        seen.append(status)
        return real(root, ident, status)

    monkeypatch.setattr(state, "set_run_status", spy)
    return seen


# --- outcome 1: nothing pending, the run ends -------------------------------------------------------


def test_with_nothing_pending_the_run_goes_ending_then_ended(
    root: Path, sequence: list[str]
) -> None:
    code, out = end(root)
    assert code == 0 and out == {
        "ok": True,
        "run_status": "ended",
        "already_ended": False,
        "blockers": [],
        "ignored": [],
    }
    assert run_status(root) == "ended" and sequence == ["ending", "ended"]


def test_an_ended_run_stays_ended_and_changes_nothing(
    root: Path, sequence: list[str]
) -> None:
    end(root)
    before = state.run_path(root, ORCH).read_bytes()
    sequence.clear()
    code, out = end(root)
    assert code == 0 and out["already_ended"] is True and sequence == []
    assert state.run_path(root, ORCH).read_bytes() == before


def test_a_wake_for_another_orchestrator_does_not_hold_this_one(root: Path) -> None:
    put_wake(
        root,
        {
            **golden(),
            "target": {
                **golden()["target"],
                "orchestrator": "ironclaude-2",
                "tag": "orchestrator-ironclaude-2",
            },
        },
    )
    code, out = end(root)
    assert code == 0 and out["blockers"] == [] and run_status(root) == "ended"


def test_acknowledged_wakes_and_wakes_moved_to_done_do_not_hold_it(root: Path) -> None:
    put_wake(root)
    (root / ".orchestrator/wakes" / f"{WID}.ack.json").write_text(json.dumps(ACK))
    assert wake.read_ack(root, WID) is not None
    other = "20261119T111500Z-aaaaaaaa"
    done = root / ".orchestrator/wakes/done"
    done.mkdir()
    put_wake(root, {**golden(), "wake_id": other}, wake_id=other).rename(
        done / f"{other}.json"
    )
    code, out = end(root)
    assert code == 0 and out["run_status"] == "ended"


def test_a_wake_that_cannot_be_read_does_not_say_whom_it_is_for_and_is_only_listed(
    root: Path,
) -> None:
    put_wake(root, raw=b"not json")
    code, out = end(root)
    assert (
        code == 0 and out["ignored"] == [f"{WID}.json"] and run_status(root) == "ended"
    )


@pytest.mark.parametrize("status", ["done", "skipped", "failed", "escalated"])
def test_a_state_file_that_is_not_in_progress_does_not_hold_it(
    root: Path, status: str
) -> None:
    state.create_state(root, REPO, 7, ORCH, wake_id=WID)
    state.set_status(root, REPO, 7, status)
    assert end(root)[0] == 0


def test_a_state_file_of_another_orchestrator_does_not_hold_it(root: Path) -> None:
    state.create_state(root, REPO, 7, "ironclaude-2", wake_id=WID)
    assert end(root)[0] == 0


# --- outcome 2: something is pending, the run stays running and the blocker is named ------------------


def test_an_unacknowledged_wake_addressed_to_it_keeps_the_run_active_and_is_named(
    root: Path, sequence: list[str]
) -> None:
    put_wake(root)
    code, out = end(root)
    assert (code, out["ok"], out["reason"]) == (3, False, "pending_work")
    assert (
        out["blockers"] == [{"kind": "wake", "wake_id": WID}]
        and out["run_status"] == "active"
    )
    assert run_status(root) == "active" and sequence == ["ending", "active"]


def test_an_acknowledgment_that_cannot_be_trusted_is_no_acknowledgment(
    root: Path,
) -> None:
    put_wake(root)
    (root / ".orchestrator/wakes" / f"{WID}.ack.json").write_text("{broken")
    code, out = end(root)
    assert code == 3 and out["blockers"] == [{"kind": "wake", "wake_id": WID}]


def test_a_resume_wake_holds_it_too(root: Path) -> None:
    doc = golden()
    doc["target"]["resume"], doc["assigned"], doc["plan_requests"] = True, [], []
    put_wake(root, doc)
    assert end(root)[1]["blockers"] == [{"kind": "wake", "wake_id": WID}]


def test_the_run_ends_once_the_wake_is_acknowledged(root: Path) -> None:
    put_wake(root)
    assert end(root)[0] == 3
    (root / ".orchestrator/wakes" / f"{WID}.ack.json").write_text(json.dumps(ACK))
    code, out = end(root)
    assert code == 0 and run_status(root) == "ended"


def test_an_in_progress_state_file_keeps_the_run_active_and_names_the_intent(
    root: Path,
) -> None:
    state.create_state(root, REPO, 7, ORCH, wake_id=WID)
    state.record_intent(root, REPO, 7, 4, "worker_start_intent")
    code, out = end(root)
    assert (code, out["reason"]) == (3, "pending_work") and run_status(root) == "active"
    (blocker,) = out["blockers"]
    assert (blocker["kind"], blocker["repo"], blocker["number"]) == ("issue", REPO, 7)
    assert blocker["step"] == "worker_start_intent"
    assert (
        blocker["pending_intent"]["step"] == "worker_start_intent"
    )  # the act a restart must settle first


def test_an_in_progress_plan_record_holds_it_until_it_is_final(root: Path) -> None:
    state.create_plan(root, REPO, 8, "2026-11-19T10:15:00Z", ORCH)
    code, out = end(root)
    assert code == 3
    assert out["blockers"] == [
        {
            "kind": "plan",
            "repo": REPO,
            "number": 8,
            "requested_at": "2026-11-19T10:15:00Z",
            "step": "plan_call_started",
        }
    ]
    state.record_plan_step(root, REPO, 8, "2026-11-19T10:15:00Z", "plan_done")
    assert end(root)[0] == 0


def test_a_state_file_that_cannot_be_read_holds_it_like_the_poll_counts_it(
    root: Path,
) -> None:
    path = state.state_path(root, REPO, 9)
    path.parent.mkdir(parents=True)
    path.write_text("{broken")
    code, out = end(root)
    assert code == 3 and out["blockers"] == [{"kind": "unreadable", "file": path.name}]
    assert path.read_text() == "{broken"  # never overwritten


def test_every_blocker_is_listed_not_only_the_first(root: Path) -> None:
    put_wake(root)
    state.create_state(root, REPO, 7, ORCH, wake_id=WID)
    state.create_plan(root, REPO, 8, "2026-11-19T10:15:00Z", ORCH)
    kinds = sorted(b["kind"] for b in end(root)[1]["blockers"])
    assert kinds == ["issue", "plan", "wake"]


def test_after_a_blocked_end_the_poll_may_route_again_and_a_later_end_can_succeed(
    root: Path,
) -> None:
    state.create_state(root, REPO, 7, ORCH, wake_id=WID)
    assert end(root)[0] == 3 and run_status(root) == "active"
    state.set_status(root, REPO, 7, "done")
    assert end(root)[0] == 0 and run_status(root) == "ended"


def test_a_missing_run_file_is_run_not_found(tmp_path: Path) -> None:
    code, out = end(make_root(tmp_path, run=False))
    assert (code, out["reason"]) == (5, "run_not_found")


# --- the lock is held from the first line to the last --------------------------------------------------


def test_the_lock_is_held_at_every_step_of_the_sequence(
    root: Path, monkeypatch
) -> None:
    put_wake(root)
    held: dict[str, bool] = {}
    real_ack, real_open, real_set = wake.read_ack, state.list_open, state.set_run_status

    def spy_ack(*args, **kw):
        held["read the wake acknowledgments"] = lock_is_held(root)
        return real_ack(*args, **kw)

    def spy_open(*args, **kw):
        held["read the state files"] = lock_is_held(root)
        return real_open(*args, **kw)

    def spy_set(r, ident, status):
        held[f"set {status}"] = lock_is_held(root)
        return real_set(r, ident, status)

    monkeypatch.setattr(wake, "read_ack", spy_ack)
    monkeypatch.setattr(state, "list_open", spy_open)
    monkeypatch.setattr(state, "set_run_status", spy_set)
    with pytest.raises(StateError):  # the wake is not acknowledged: this end is blocked
        idle_end.idle_end(root, ORCH, wait_s=1.0)
    assert held == {
        "set ending": True,
        "read the wake acknowledgments": True,
        "read the state files": True,
        "set active": True,
    }
    assert not lock_is_held(root)  # and it is let go at the end, blocked or not
    (root / ".orchestrator/wakes" / f"{WID}.ack.json").write_text(json.dumps(ACK))
    held.clear()
    idle_end.idle_end(root, ORCH, wait_s=1.0)
    assert held["set ended"] is True and not lock_is_held(root)


def test_a_second_caller_is_refused_while_the_first_is_in_the_middle_of_the_check(
    root: Path, monkeypatch
) -> None:
    second: dict = {}
    real_ack = wake.read_ack
    put_wake(root)

    def spy_ack(*args, **kw):
        def other_caller() -> None:
            try:
                idle_end.idle_end(root, ORCH, wait_s=0.2)
            except StateError as exc:
                second["reason"], second["code"] = exc.reason, exc.code

        thread = threading.Thread(
            target=other_caller
        )  # a separate thread has its own lock holding
        thread.start()
        thread.join()
        return real_ack(*args, **kw)

    monkeypatch.setattr(wake, "read_ack", spy_ack)
    with pytest.raises(StateError) as first:
        idle_end.idle_end(root, ORCH, wait_s=1.0)
    assert (
        first.value.reason == "pending_work"
    )  # the first caller finished its own check
    assert second == {
        "reason": "lock_busy",
        "code": 75,
    }  # the second was refused, not let in


def test_a_caller_that_finds_the_lock_taken_is_refused_and_changes_nothing(
    root: Path,
) -> None:
    before = state.run_path(root, ORCH).read_bytes()
    with state.locked(root):
        result: dict = {}

        def other() -> None:
            try:
                idle_end.idle_end(root, ORCH, wait_s=0.2)
            except StateError as exc:
                result["reason"], result["code"] = exc.reason, exc.code

        thread = threading.Thread(target=other)
        thread.start()
        thread.join()
    assert result == {"reason": "lock_busy", "code": 75}
    assert (
        state.run_path(root, ORCH).read_bytes() == before
        and run_status(root) == "active"
    )


def test_a_real_second_process_is_refused_while_this_one_holds_the_lock(
    root: Path,
) -> None:
    script = (
        "import sys; from superclaude.cli.orchestrator import idle_end; "
        "from superclaude.cli.orchestrator.state import StateError\n"
        "try:\n    idle_end.idle_end(sys.argv[1], sys.argv[2], wait_s=0.3)\nexcept StateError as e:\n    print(e.reason, e.code)\n"
    )
    with state.locked(root):
        done = subprocess.run(
            [sys.executable, "-c", script, str(root), ORCH],
            capture_output=True, text=True, timeout=120, check=False,
        )  # fmt: skip
    assert done.stdout.split() == ["lock_busy", "75"], done.stderr
    assert run_status(root) == "active"


# --- a kill half way ---------------------------------------------------------------------------------


def test_a_kill_between_ending_and_ended_leaves_ending_and_the_next_call_finishes_it(
    root: Path, monkeypatch
) -> None:
    def killed(*args, **kw):
        raise RuntimeError("killed in the middle of the check")

    with monkeypatch.context() as patch:
        patch.setattr(wake, "read_ack", killed)
        put_wake(root)
        with pytest.raises(RuntimeError):
            idle_end.idle_end(root, ORCH, wait_s=1.0)
    assert (
        run_status(root) == "ending"
    )  # the poll never routes to a Run that is not active
    assert not lock_is_held(root)
    (root / ".orchestrator/wakes" / f"{WID}.ack.json").write_text(json.dumps(ACK))
    code, out = end(root)
    assert code == 0 and run_status(root) == "ended"


def test_an_ending_run_with_something_pending_is_set_active_again(root: Path) -> None:
    state.set_run_status(root, ORCH, "ending")
    state.create_state(root, REPO, 7, ORCH, wake_id=WID)
    assert end(root)[0] == 3 and run_status(root) == "active"


# --- the lock can be taken again by the thread that holds it ---------------------------------------------


def test_the_lock_can_be_taken_again_in_the_same_thread_and_is_let_go_at_the_end(
    root: Path,
) -> None:
    with state.locked(root):
        with state.locked(root):
            assert lock_is_held(root)
        assert lock_is_held(root)  # the inner exit did not let go
        state.set_run_status(
            root, ORCH, "ending"
        )  # a function that takes the lock itself works inside
    assert not lock_is_held(root)


def test_the_lock_is_let_go_when_the_body_raises_and_when_the_inner_one_does(
    root: Path,
) -> None:
    with pytest.raises(ValueError):
        with state.locked(root):
            with state.locked(root):
                raise ValueError
    assert not lock_is_held(root)
    with state.locked(root):  # and the count did not leak: it can be taken fresh
        assert lock_is_held(root)


def test_another_thread_cannot_ride_on_the_lock_this_thread_holds(root: Path) -> None:
    outcome: dict = {}

    def other() -> None:
        try:
            with state.locked(root, wait_s=0.2):
                outcome["entered"] = True
        except StateError as exc:
            outcome["reason"] = exc.reason

    with state.locked(root):
        thread = threading.Thread(target=other)
        thread.start()
        thread.join()
    assert outcome == {"reason": "lock_busy"}


def test_two_orchestrator_repos_have_separate_locks(tmp_path: Path) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(), b.mkdir()
    with state.locked(a):
        with state.locked(b, wait_s=0.2):
            assert lock_is_held(a) and lock_is_held(b)


# --- the identity ----------------------------------------------------------------------------------------


def test_the_orchestrator_is_named_by_flag_or_by_the_session_tag(root: Path) -> None:
    code, out = call(root, "idle-end", tag=None)  # no flag, no tag in the session
    assert (code, out["reason"]) == (2, "own_identity_unknown") and run_status(
        root
    ) == "active"
    assert call(root, "idle-end", "--orchestrator", ORCH, tag=None)[0] == 0
    assert run_status(root) == "ended"
