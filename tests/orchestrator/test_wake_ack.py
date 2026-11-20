"""``wake-ack`` (design 3.6): the acknowledgment is whole, decided item by item, and written after its records."""

from __future__ import annotations

import json
import stat
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import wake
from superclaude.cli.orchestrator import ext, repos_file, state, wake_ack, wakefiles

from .fake_world import (
    ORCH,
    REPO,
    WID,
    World,
    call,
    golden,
    install,
    make_root,
    put_wake,
    repos_text,
)

WAKES = Path(".orchestrator/wakes")
REQUESTED = "2026-11-19T10:15:00Z"
ITEM = f"{REPO}#655"
PLAN = f"{REPO}#656"


@pytest.fixture
def world(monkeypatch) -> World:
    w = install(monkeypatch, World())
    yield w
    assert not w.unexpected, w.unexpected


@pytest.fixture
def root(tmp_path: Path, world: World) -> Path:
    path = make_root(tmp_path)
    put_wake(path)
    return path


def records(root: Path) -> None:
    """What wave 0 writes before it acknowledges: the state file and the plan record."""
    state.create_state(root, REPO, 655, ORCH, wake_id=WID)
    state.create_plan(root, REPO, 656, REQUESTED, ORCH)


def ack(root: Path, *args: str) -> tuple[int, dict]:
    return call(root, "wake-ack", WID, *args)


def ack_path(root: Path) -> Path:
    return root / WAKES / f"{WID}.ack.json"


# --- the acknowledgment ------------------------------------------------------------------------


def test_the_acknowledgment_holds_each_item_in_exactly_one_list(root: Path) -> None:
    records(root)
    code, out = ack(root, "--taken", ITEM, "--taken", PLAN)
    assert code == 0 and out["already_acked"] is False
    doc = json.loads(ack_path(root).read_text())
    assert doc == out["ack"]
    assert doc["schema"] == "orchestrator-wake-ack/1" and doc["wake_id"] == WID
    assert doc["orchestrator"] == {
        "id": ORCH,
        "run_id": "run_abc123",
        "host": "ws-aidev02",
    }
    assert doc["taken"] == [
        {"repo": REPO, "number": 655},
        {"repo": REPO, "number": 656},
    ]
    assert (
        doc["skipped"] == [] and doc["rejected_items"] == [] and doc["warnings"] == []
    )
    assert stat.S_IMODE(ack_path(root).stat().st_mode) == 0o600
    assert [p.name for p in (root / WAKES).iterdir() if "tmp" in p.name] == []


def test_the_poll_reads_the_acknowledgment_this_verb_wrote(root: Path) -> None:
    records(root)
    ack(root, "--taken", ITEM, "--skipped", f"{PLAN}:already_planned")
    parsed = wake.read_ack(root, WID)
    assert parsed is not None
    assert parsed.taken == frozenset({(REPO, 655)})
    assert parsed.skipped == {(REPO, 656): "already_planned"}
    assert parsed.rejected_indexes == ()


def test_an_item_left_undecided_is_named_and_nothing_is_written(root: Path) -> None:
    records(root)
    code, out = ack(root, "--taken", ITEM)
    assert (code, out["reason"], out["items"]) == (2, "item_undecided", [PLAN])
    code, out = ack(root, "--taken", PLAN)
    assert (code, out["reason"], out["items"]) == (2, "item_undecided", [ITEM])
    assert not ack_path(root).exists()


def test_a_decision_for_an_item_that_is_not_in_the_wake_is_refused(root: Path) -> None:
    records(root)
    code, out = ack(root, "--taken", ITEM, "--taken", PLAN, "--taken", f"{REPO}#999")
    assert (code, out["reason"]) == (2, "unknown_item")
    assert not ack_path(root).exists()


def test_an_item_cannot_be_taken_and_skipped_or_decided_twice(root: Path) -> None:
    records(root)
    for args in (
        ("--taken", ITEM, "--skipped", f"{ITEM}:already_claimed", "--taken", PLAN),
        ("--taken", ITEM, "--taken", ITEM, "--taken", PLAN),
    ):
        code, out = ack(root, *args)
        assert (code, out["reason"]) == (2, "duplicate_decision")
    assert not ack_path(root).exists()


@pytest.mark.parametrize("reason", ["Already Claimed", "x" * 41, "9lives", ""])
def test_a_skip_reason_must_be_a_token(root: Path, reason: str) -> None:
    records(root)
    code, out = ack(root, "--skipped", f"{ITEM}:{reason}", "--taken", PLAN)
    assert (code, out["reason"]) == (2, "invalid_reason")
    assert not ack_path(root).exists()


def test_an_assigned_item_may_be_skipped_with_any_token(root: Path) -> None:
    records(root)
    code, out = ack(root, "--skipped", f"{ITEM}:already_claimed", "--taken", PLAN)
    assert code == 0
    assert out["ack"]["skipped"] == [
        {"repo": REPO, "number": 655, "reason": "already_claimed"}
    ]


@pytest.mark.parametrize("reason", ["already_planned", "held_backlog", "not_open"])
def test_a_plan_request_skip_reason_is_one_of_the_closed_three(
    root: Path, reason: str
) -> None:
    state.create_state(root, REPO, 655, ORCH, wake_id=WID)
    code, out = ack(root, "--taken", ITEM, "--skipped", f"{PLAN}:{reason}")
    assert code == 0 and out["ack"]["skipped"] == [
        {"repo": REPO, "number": 656, "reason": reason}
    ]


def test_a_plan_request_cannot_be_skipped_with_another_reason(root: Path) -> None:
    state.create_state(root, REPO, 655, ORCH, wake_id=WID)
    code, out = ack(root, "--taken", ITEM, "--skipped", f"{PLAN}:claimed_elsewhere")
    assert (code, out["reason"]) == (2, "invalid_reason")
    assert not ack_path(root).exists()


# --- record first, acknowledgment second --------------------------------------------------------


def test_an_assigned_item_is_not_taken_before_its_state_file_exists(root: Path) -> None:
    state.create_plan(root, REPO, 656, REQUESTED, ORCH)
    code, out = ack(root, "--taken", ITEM, "--taken", PLAN)
    assert (code, out["reason"]) == (3, "taken_without_record")
    assert not ack_path(root).exists()


@pytest.mark.parametrize(
    ("wake_id", "orchestrator"),
    [("20261118T000000Z-aaaaaaaa", ORCH), (WID, "ironclaude-2")],
    ids=["file of another wake", "file of another orchestrator"],
)
def test_a_state_file_of_another_wake_or_orchestrator_is_no_record_of_this_take(
    root: Path, wake_id: str, orchestrator: str
) -> None:
    state.create_state(root, REPO, 655, orchestrator, wake_id=wake_id)
    state.create_plan(root, REPO, 656, REQUESTED, ORCH)
    code, out = ack(root, "--taken", ITEM, "--taken", PLAN)
    assert (code, out["reason"]) == (
        2,
        "conflicts_with_check",
    )  # it is another take's issue
    assert not ack_path(root).exists()


def test_a_plan_request_is_not_taken_before_its_plan_record_exists(root: Path) -> None:
    state.create_state(root, REPO, 655, ORCH, wake_id=WID)
    code, out = ack(root, "--taken", ITEM, "--taken", PLAN)
    assert (code, out["reason"]) == (3, "taken_without_plan_record")
    assert not ack_path(root).exists()
    state.create_plan(
        root, REPO, 656, REQUESTED, ORCH
    )  # record first, then the acknowledgment
    assert ack(root, "--taken", ITEM, "--taken", PLAN)[0] == 0


# --- what the check already decided -------------------------------------------------------------


def test_an_unlisted_repo_is_skipped_for_the_caller(
    tmp_path: Path, world: World
) -> None:
    root = make_root(tmp_path, text=repos_text(repos=[]))
    put_wake(root)
    code, out = ack(root)  # the caller has nothing to decide
    assert code == 0 and out["ack"]["taken"] == []
    assert out["ack"]["skipped"] == [
        {"repo": REPO, "number": 655, "reason": "repo_not_listed"},
        {"repo": REPO, "number": 656, "reason": "repo_not_listed"},
    ]


def test_a_forced_skip_cannot_be_taken_or_given_another_reason(
    tmp_path: Path, world: World
) -> None:
    listed = {"repo": REPO, "enabled": False, "checkout": None}
    root = make_root(tmp_path, text=repos_text(repos=[listed]))
    put_wake(root)
    code, out = ack(root, "--taken", ITEM)
    assert (code, out["reason"]) == (2, "conflicts_with_check")
    code, out = ack(root, "--skipped", f"{ITEM}:already_claimed")
    assert (code, out["reason"]) == (2, "conflicts_with_check")
    code, out = ack(
        root, "--skipped", f"{ITEM}:repo_disabled", "--skipped", f"{PLAN}:repo_disabled"
    )
    assert code == 0  # the same reason is accepted


def test_an_issue_with_the_state_file_of_another_wake_is_skipped_already_dispatched(
    root: Path,
) -> None:
    state.create_state(root, REPO, 655, ORCH, wake_id="20261118T000000Z-aaaaaaaa")
    state.create_plan(root, REPO, 656, REQUESTED, ORCH)
    code, out = ack(root, "--taken", PLAN)
    assert code == 0
    assert out["ack"]["skipped"] == [
        {"repo": REPO, "number": 655, "reason": "already_dispatched"}
    ]
    code, out = ack(
        root, "--taken", ITEM, "--taken", PLAN
    )  # a second call: the first one stands
    assert out["already_acked"] is True


def test_a_state_file_made_for_this_wake_after_a_crash_may_be_skipped_as_dispatched(
    root: Path,
) -> None:
    records(root)  # the kill came after the state file and before the acknowledgment
    code, out = ack(root, "--skipped", f"{ITEM}:already_dispatched", "--taken", PLAN)
    assert code == 0
    assert out["ack"]["skipped"] == [
        {"repo": REPO, "number": 655, "reason": "already_dispatched"}
    ]


# --- rejected items and warnings come from the parse --------------------------------------------


def test_malformed_items_and_unknown_keys_are_listed_by_the_verb_and_not_the_caller(
    root: Path,
) -> None:
    doc = golden()
    doc["assigned"].append({**doc["assigned"][0], "number": "x"})  # index 1: malformed
    doc["plan_requests"][0]["missing"] = []  # index 2: malformed
    doc["info"]["mentions"][0]["kind"] = "nope"  # no entry to point at
    doc["new_field"] = True
    put_wake(root, doc)
    state.create_state(root, REPO, 655, ORCH, wake_id=WID)
    code, out = ack(root, "--taken", ITEM)
    assert code == 0
    assert out["ack"]["rejected_items"] == [
        {"index": 1, "reason": "malformed_item"},
        {"index": 2, "reason": "malformed_item"},
    ]
    assert sorted(out["ack"]["warnings"]) == [
        "malformed_info_items:1",
        "unknown_key:new_field",
    ]
    assert wake.read_ack(root, WID).rejected_indexes == (
        1,
        2,
    )  # the indexes the poll maps back


# --- already acknowledged, and not acknowledgeable ------------------------------------------------


def test_an_acknowledged_wake_is_not_written_again(root: Path) -> None:
    records(root)
    ack(root, "--taken", ITEM, "--taken", PLAN)
    before = ack_path(root).read_bytes()
    code, out = ack(
        root, "--taken", ITEM, "--skipped", f"{PLAN}:not_open"
    )  # even other decisions
    assert code == 0 and out["already_acked"] is True
    assert ack_path(root).read_bytes() == before
    assert out["ack"] == json.loads(before)


@pytest.mark.parametrize("tag", ["orchestrator-ironclaude-2"])
def test_a_wake_that_wake_check_would_refuse_is_not_acknowledged(
    root: Path, tag: str
) -> None:
    code, out = call(root, "wake-ack", WID, tag=tag)
    assert (code, out["reason"], out["why"]) == (3, "wake_not_ackable", "wrong_target")
    assert not ack_path(root).exists()
    assert not (
        root / WAKES / f"{WID}.rejected.json"
    ).exists()  # wake-check writes that, not this


def test_a_wake_that_is_missing_is_not_acknowledged(root: Path) -> None:
    (root / WAKES / f"{WID}.json").unlink()
    code, out = ack(root)
    assert (code, out["why"]) == (3, "missing")


def test_the_run_file_must_exist_first(tmp_path: Path, world: World) -> None:
    root = make_root(tmp_path, run=False)
    put_wake(root)
    code, out = ack(
        root, "--skipped", f"{ITEM}:already_claimed", "--skipped", f"{PLAN}:not_open"
    )
    assert (code, out["reason"]) == (5, "run_not_found")
    assert not ack_path(root).exists()


@pytest.mark.parametrize(
    "args",
    [["--taken", "not-an-item"], ["--skipped", "no-colon"], ["--skipped", "x#1:y"]],
)
def test_a_malformed_item_argument_is_refused(root: Path, args: list[str]) -> None:
    code, out = ack(root, *args)
    assert (code, out["reason"]) == (2, "invalid_item")


# --- the write is whole or absent ---------------------------------------------------------------


def test_a_kill_during_the_write_leaves_no_acknowledgment_and_no_temporary_file(
    root: Path, monkeypatch
) -> None:
    records(root)
    doc = repos_file.load_doc(root, ext.make_runner("test"))

    def fail(src, dst):
        raise OSError("killed")

    monkeypatch.setattr("superclaude.cli.swarm.atomic.os.replace", fail)
    with pytest.raises(OSError):
        wake_ack.acknowledge(
            root,
            WID,
            ORCH,
            "orchestrator-ironclaude-1",
            doc,
            [(REPO, 655), (REPO, 656)],
            [],
        )
    assert not ack_path(root).exists()
    assert [p.name for p in (root / WAKES).iterdir() if p.name.endswith(".tmp")] == []
    assert wakefiles.load_ack(root, WID) is None
