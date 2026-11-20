"""What survives a restart (design 5.5): state files, plan records, run files, the verb and the failpoint."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_watch import route
from superclaude.cli.orchestrator import failpoint, state
from superclaude.cli.orchestrator.group import orchestrator_group
from superclaude.cli.orchestrator.state import StateError

REPO = "IronbellyOrg/IronClaude"
OTHER = "IronbellyGroup/Other"
ORCH = "ironclaude-1"
WAKE = "20261119T100000Z-0123abcd"
REQUESTED = "2026-11-19T10:00:00Z"
NOW = datetime(2026, 11, 19, 10, 0, 0, tzinfo=timezone.utc)
SHA = "0123456789abcdef0123456789abcdef01234567"


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return tmp_path


def make(root: Path, repo: str = REPO, number: int = 7, **kw) -> dict:
    return state.create_state(root, repo, number, ORCH, wake_id=WAKE, **kw)


def read_raw(root: Path, repo: str = REPO, number: int = 7) -> dict:
    return json.loads(state.state_path(root, repo, number).read_text())


# --- create ---------------------------------------------------------------------------------


def test_create_writes_the_fields_of_5_5_at_mode_0600(root: Path) -> None:
    doc = make(root)
    path = state.state_path(root, REPO, 7)
    assert path == root / ".orchestrator/issues/IronbellyOrg__IronClaude__7.json"
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert read_raw(root) == doc
    assert doc == {
        "schema": "orchestrator-state/1",
        "repo": REPO,
        "number": 7,
        "orchestrator": ORCH,
        "tiers": {},
        "status": "in_progress",
        "wave": 1,
        "step": "claim",
        "wake_id": WAKE,
        "ids": {},
        "round": 1,
        "remaining": [],
        "rounds": [],
        "body_sha": None,
        "log": [],
    }
    assert [p.name for p in path.parent.iterdir()] == [
        path.name
    ]  # no temporary file left


def test_the_poll_reads_what_this_module_writes(root: Path) -> None:
    """``issue_watch.route`` counts the files this module makes (5.7 point 1)."""
    make(root, number=7)
    make(root, number=8)
    state.set_status(root, REPO, 8, "escalated")
    state.create_plan(root, REPO, 9, REQUESTED, ORCH)
    found = route.read_state_files(root)
    assert {k: (v.status, v.orchestrator, v.readable) for k, v in found.items()} == {
        f"{REPO}#7": ("in_progress", ORCH, True),
        f"{REPO}#8": ("escalated", ORCH, True),
    }  # a plan record is not a state file
    at = datetime(2026, 11, 19, 10, 0, 0, tzinfo=timezone.utc)
    assert route.plan_record_status(root, REPO, 9, at) == "in_progress"
    state.record_plan_step(root, REPO, 9, REQUESTED, "plan_done")
    assert route.plan_record_status(root, REPO, 9, at) == "done"


def test_exclusive_create_refuses_a_second_state_file_for_one_key(root: Path) -> None:
    first = make(root)
    before = state.state_path(root, REPO, 7).read_bytes()
    with pytest.raises(StateError) as caught:
        state.create_state(root, REPO, 7, "other-2", wake_id=None)
    assert (caught.value.reason, caught.value.code) == ("already_exists", 3)
    assert caught.value.info == {"status": "in_progress", "step": "claim"}
    assert state.state_path(root, REPO, 7).read_bytes() == before
    assert state.load_state(root, REPO, 7) == first
    make(root, OTHER, 7)  # the same number in another repo is another key


@pytest.mark.parametrize("step", state.RETAKE_STEPS)
def test_retake_moves_an_escalated_closeout_or_handback_file_aside(
    root: Path, step: str
) -> None:
    make(root)
    state.record_done(root, REPO, 7, 8, step)
    state.set_status(root, REPO, 7, "escalated")
    fresh = state.create_state(root, REPO, 7, ORCH, retake=True)
    assert fresh["log"] == [] and fresh["step"] == "claim"
    (moved,) = (root / ".orchestrator/issues/retaken").iterdir()
    assert moved.name.startswith("IronbellyOrg__IronClaude__7-")
    assert json.loads(moved.read_text())["step"] == step
    # the poll does not read the folder
    assert list(route.read_state_files(root)) == [f"{REPO}#7"]


def test_retake_refuses_every_other_existing_file(root: Path) -> None:
    make(root)
    with pytest.raises(StateError, match="already_exists"):  # in_progress
        state.create_state(root, REPO, 7, ORCH, retake=True)
    state.record_done(root, REPO, 7, 5, "worker_started")
    state.set_status(
        root, REPO, 7, "escalated"
    )  # escalated, but not at a closeout step
    with pytest.raises(StateError, match="already_exists"):
        state.create_state(root, REPO, 7, ORCH, retake=True)
    assert not (root / ".orchestrator/issues/retaken").exists()
    assert state.load_state(root, REPO, 7)["step"] == "worker_started"


@pytest.mark.parametrize(
    "kw",
    [
        {"repo": "not a repo", "number": 7},
        {"repo": REPO, "number": 0},
        {"repo": REPO, "number": 7, "wave": 10},
        {"repo": REPO, "number": 7, "step": "Bad Step"},
        {"repo": REPO, "number": 7, "wake_id": "20261119"},
    ],
)
def test_create_refuses_bad_input_and_writes_nothing(root: Path, kw: dict) -> None:
    kw = {"orchestrator": ORCH, **kw}
    repo, number = kw.pop("repo"), kw.pop("number")
    with pytest.raises((StateError, ValueError)):
        state.create_state(root, repo, number, kw.pop("orchestrator"), **kw)
    assert not (root / ".orchestrator/issues").exists() or not list(
        (root / ".orchestrator/issues").iterdir()
    )


# --- the write-ahead log: intent, then done ---------------------------------------------------


def test_intent_then_done_lines_and_the_position(root: Path) -> None:
    make(root)
    doc = state.record_intent(root, REPO, 7, 1, "lease_posted", "post", now=NOW)
    assert doc["step"] == "lease_posted" and doc["wave"] == 1
    assert doc["log"] == [
        {
            "ts": "2026-11-19T10:00:00Z",
            "wave": 1,
            "step": "lease_posted",
            "phase": "intent",
            "detail": "post",
        }
    ]
    assert state.pending_intent(doc) == doc["log"][0]
    doc = state.record_done(root, REPO, 7, 1, "lease_posted", "comment 99", now=NOW)
    assert [e["phase"] for e in doc["log"]] == ["intent", "done"]
    assert state.pending_intent(doc) is None
    assert read_raw(root) == doc  # saved


def test_the_log_is_append_only_and_keeps_every_line(root: Path) -> None:
    make(root)
    for i, step in enumerate(["a_step", "b_step", "c_step"]):
        state.record_intent(root, REPO, 7, i, step)
        before = read_raw(root)["log"]
        state.record_done(root, REPO, 7, i, step)
        assert read_raw(root)["log"][: len(before)] == before
    assert [(e["step"], e["phase"]) for e in read_raw(root)["log"]] == [
        ("a_step", "intent"),
        ("a_step", "done"),
        ("b_step", "intent"),
        ("b_step", "done"),
        ("c_step", "intent"),
        ("c_step", "done"),
    ]


def test_a_second_intent_is_refused_while_one_has_no_done(root: Path) -> None:
    make(root)
    state.record_intent(root, REPO, 7, 1, "claim_posted")
    with pytest.raises(StateError) as caught:
        state.record_intent(
            root, REPO, 7, 1, "claim_posted"
        )  # the act must not be repeated
    assert (caught.value.reason, caught.value.code) == ("intent_open", 3)
    assert caught.value.info == {"wave": 1, "step": "claim_posted"}
    with pytest.raises(StateError, match="intent_open"):
        state.record_intent(root, REPO, 7, 2, "other_step")
    assert len(read_raw(root)["log"]) == 1


def test_done_for_another_step_is_refused_and_done_with_no_intent_is_recorded(
    root: Path,
) -> None:
    make(root)
    state.record_intent(root, REPO, 7, 1, "claim_posted")
    with pytest.raises(StateError, match="intent_mismatch"):
        state.record_done(root, REPO, 7, 1, "plan_recorded")
    state.record_done(root, REPO, 7, 1, "claim_posted")
    doc = state.record_done(
        root, REPO, 7, 2, "plan_recorded", "already visible outside"
    )  # rule 3
    assert doc["log"][-1]["phase"] == "done" and doc["step"] == "plan_recorded"
    assert state.pending_intent(doc) is None


@pytest.mark.parametrize("status", state.FINAL_STATUSES)
def test_a_final_file_takes_no_more_lines(root: Path, status: str) -> None:
    make(root)
    state.set_status(root, REPO, 7, status)
    with pytest.raises(StateError, match="final_status"):
        state.record_intent(root, REPO, 7, 9, "x_step")
    with pytest.raises(StateError, match="final_status"):
        state.set_fields(root, REPO, 7, body_sha=SHA)


@pytest.mark.parametrize(
    ("wave", "step", "detail"),
    [
        (10, "x", None),
        (-1, "x", None),
        (1, "X", None),
        (1, "a b", None),
        (1, "x", "line\nbreak"),
        (1, "x", "a" * 2001),
    ],
)
def test_intent_refuses_bad_input(
    root: Path, wave: int, step: str, detail: str | None
) -> None:
    make(root)
    with pytest.raises(StateError):
        state.record_intent(root, REPO, 7, wave, step, detail)
    assert read_raw(root)["log"] == []


# --- a kill after each intent and before its done resumes without repeating the act ---------------

STEPS = [
    (1, "lease_posted"),
    (1, "claim_posted"),
    (2, "plan_recorded"),
    (4, "worker_started"),
    (7, "merged"),
]


class Outside:
    """The outside world: each act is visible here once and a repeat would show as a second one."""

    def __init__(self) -> None:
        self.acts: list[str] = []

    def do(self, step: str) -> None:
        self.acts.append(step)

    def visible(self, step: str) -> bool:
        return step in self.acts


class Killed(Exception):
    pass


def run_wave(root: Path, outside: Outside, kill_at: tuple[str, str] | None) -> None:
    """The waves of 5.5: intent, act, done. A restart settles an open intent from the outside state."""
    doc = state.load_state(root, REPO, 7)
    open_line = state.pending_intent(doc)
    if open_line is not None:  # rule 2: read the outside state, never repeat the act
        if outside.visible(open_line["step"]):
            state.record_done(
                root, REPO, 7, open_line["wave"], open_line["step"], "seen outside"
            )
    done = {
        e["step"]
        for e in state.load_state(root, REPO, 7)["log"]
        if e["phase"] == "done"
    }
    pending = state.pending_intent(state.load_state(root, REPO, 7))
    for wave, step in STEPS:
        if step in done:
            continue
        if pending is None or pending["step"] != step:
            state.record_intent(root, REPO, 7, wave, step)
        if kill_at == (step, "after_intent"):
            raise Killed
        if not outside.visible(step):
            outside.do(step)
        if kill_at == (step, "after_act"):
            raise Killed
        state.record_done(root, REPO, 7, wave, step)
        pending = None


@pytest.mark.parametrize("when", ["after_intent", "after_act"])
@pytest.mark.parametrize(("wave", "step"), STEPS)
def test_a_kill_after_each_intent_and_before_done_resumes_without_repeating_the_act(
    root: Path, wave: int, step: str, when: str
) -> None:
    make(root)
    outside = Outside()
    with pytest.raises(Killed):
        run_wave(root, outside, kill_at=(step, when))
    assert (
        state.pending_intent(state.load_state(root, REPO, 7))["step"] == step
    )  # found open
    run_wave(root, outside, kill_at=None)  # the restart
    assert sorted(outside.acts) == sorted(s for _, s in STEPS)  # every act exactly once
    assert state.pending_intent(state.load_state(root, REPO, 7)) is None


# --- replaced whole, never half a file; an unreadable file is never overwritten ---------------------


def test_a_write_replaces_the_file_whole_through_a_temporary_file(root: Path) -> None:
    make(root)
    path = state.state_path(root, REPO, 7)
    inode = path.stat().st_ino
    state.record_intent(root, REPO, 7, 1, "x_step")
    assert path.stat().st_ino != inode  # a new file was renamed over the old one
    assert json.loads(path.read_text())["step"] == "x_step"
    assert [p.name for p in path.parent.iterdir()] == [path.name]
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


@pytest.mark.parametrize(
    "content",
    [
        b"",
        b"{not json",
        b"[]",
        b'{"schema": "other"}',
        b"\xff\xfe",
        b"x" * (state.MAX_READ_BYTES + 1),
    ],
)
def test_an_unparseable_file_is_reported_and_never_overwritten(
    root: Path, content: bytes
) -> None:
    make(root)
    path = state.state_path(root, REPO, 7)
    path.write_bytes(content)
    calls = [
        lambda: state.load_state(root, REPO, 7),
        lambda: state.record_intent(root, REPO, 7, 1, "x_step"),
        lambda: state.record_done(root, REPO, 7, 1, "x_step"),
        lambda: state.set_fields(root, REPO, 7, body_sha=SHA),
        lambda: state.set_status(root, REPO, 7, "done"),
        lambda: state.create_state(root, REPO, 7, ORCH),
    ]
    for call in calls:
        with pytest.raises(StateError) as caught:
            call()
        assert (caught.value.reason, caught.value.code) == ("state_unreadable", 4)
        assert path.read_bytes() == content
    assert state.list_open(root) == [{"file": path.name, "reason": "state_unreadable"}]
    assert (
        route.read_state_files(root)[f"{REPO}#7"].readable is False
    )  # the poll counts it in flight


def test_a_file_with_a_wrong_field_is_unreadable_too(root: Path) -> None:
    make(root)
    path = state.state_path(root, REPO, 7)
    doc = json.loads(path.read_text())
    doc["status"] = "paused"
    path.write_text(json.dumps(doc))
    with pytest.raises(StateError, match="state_unreadable"):
        state.record_intent(root, REPO, 7, 1, "x_step")
    other = json.loads(path.read_text())
    other["status"], other["number"] = (
        "in_progress",
        8,
    )  # a file under another key's name
    path.write_text(json.dumps(other))
    with pytest.raises(StateError, match="state_unreadable"):
        state.load_state(root, REPO, 7)


def test_a_file_too_big_for_the_poll_is_refused_and_left_alone(
    root: Path, monkeypatch
) -> None:
    make(root)
    monkeypatch.setattr(state, "MAX_WRITE_BYTES", 2000)
    before = state.state_path(root, REPO, 7).read_bytes()
    with pytest.raises(StateError) as caught:
        state.record_intent(root, REPO, 7, 1, "x_step", "d" * 1900)
        state.record_done(root, REPO, 7, 1, "x_step", "d" * 1900)
    assert caught.value.reason == "state_too_large"
    assert state.state_path(root, REPO, 7).read_bytes() != b""
    assert (
        json.loads(state.state_path(root, REPO, 7).read_text())["status"]
        == "in_progress"
    )
    assert len(before) < 2000


# --- ids, tiers, body hash, status ---------------------------------------------------------------


def test_set_fields_records_ids_and_clears_one(root: Path) -> None:
    make(root)
    doc = state.set_fields(
        root,
        REPO,
        7,
        ids={
            "lease_comment_id": 4086353871,
            "claim_comment_id": 12,
            "plan_marker": "sc:issue:plan",
            "task_id": "task_1",
            "dispatch_id": "ctx_a5287",
            "terminal_handle": "term_0b70-1",
            "worktree_path": "/work/tree",
            "branch": "issue-7-r2",
            "pr_number": 99,
            "pr_head_sha": SHA,
            "merge_commit": SHA,
        },
        body_sha="abcdef0",
        tiers={"worker": {"requested": "tier2", "effective": "tier2"}},
    )
    assert doc["ids"]["pr_number"] == 99 and doc["body_sha"] == "abcdef0"
    doc = state.set_fields(
        root,
        REPO,
        7,
        ids={"pr_number": None},
        tiers={"worker": {"fallback_from": "tier1b"}},
    )
    assert "pr_number" not in doc["ids"]
    assert doc["tiers"] == {
        "worker": {
            "requested": "tier2",
            "effective": "tier2",
            "fallback_from": "tier1b",
        }
    }
    assert read_raw(root) == doc


@pytest.mark.parametrize(
    "ids",
    [
        {"nothing": 1},
        {"pr_number": "12"},
        {"pr_number": 0},
        {"pr_number": True},
        {"pr_head_sha": "xyz"},
        {"worktree_path": "relative/path"},
        {"branch": "has space"},
        {"task_id": "bad id"},
        {"plan_marker": ""},
    ],
)
def test_set_fields_refuses_unknown_names_and_bad_values_and_writes_nothing(
    root: Path, ids: dict
) -> None:
    make(root)
    before = state.state_path(root, REPO, 7).read_bytes()
    with pytest.raises(StateError) as caught:
        state.set_fields(root, REPO, 7, ids=ids)
    assert caught.value.reason in ("unknown_id_name", "invalid_value")
    assert caught.value.code == 2
    assert state.state_path(root, REPO, 7).read_bytes() == before


def test_set_fields_refuses_bad_tiers_and_an_empty_call(root: Path) -> None:
    make(root)
    for tiers in (
        {"orchestrator": {"requested": "tier1b"}},
        {"worker": {"model": "x"}},
        {"worker": {"requested": "a\nb"}},
    ):
        with pytest.raises(StateError, match="invalid_value"):
            state.set_fields(root, REPO, 7, tiers=tiers)
    with pytest.raises(StateError, match="nothing_to_set"):
        state.set_fields(root, REPO, 7)
    with pytest.raises(StateError, match="invalid_value"):
        state.set_fields(root, REPO, 7, body_sha="not hex")


def test_mutate_writes_nothing_when_the_changed_document_is_not_valid(
    root: Path,
) -> None:
    make(root)
    before = state.state_path(root, REPO, 7).read_bytes()

    def bad(doc: dict) -> None:
        doc["remaining"] = ["x"] * 21

    with pytest.raises(StateError, match="invalid_value"):
        state.mutate(root, REPO, 7, bad)
    assert state.state_path(root, REPO, 7).read_bytes() == before

    def good(
        doc: dict,
    ) -> None:  # what handback does: round, remaining, rounds, ids cleared
        doc["round"], doc["remaining"], doc["ids"] = 2, ["one criterion"], {}
        doc["rounds"].append({"round": 1, "pr": 5, "head_sha": SHA})

    assert state.mutate(root, REPO, 7, good)["round"] == 2


def test_status_moves(root: Path) -> None:
    make(root)
    assert (
        state.set_status(root, REPO, 7, "in_progress")["log"] == []
    )  # same status: nothing
    doc = state.set_status(root, REPO, 7, "escalated", now=NOW)
    assert doc["log"][-1] == {
        "ts": "2026-11-19T10:00:00Z",
        "wave": 1,
        "step": "status_escalated",
        "phase": "done",
        "detail": None,
    }
    assert (
        state.set_status(root, REPO, 7, "in_progress")["status"] == "in_progress"
    )  # after the answer
    assert state.set_status(root, REPO, 7, "done")["status"] == "done"
    for status in ("in_progress", "escalated", "failed"):
        with pytest.raises(StateError) as caught:
            state.set_status(root, REPO, 7, status)
        assert (caught.value.reason, caught.value.code) == ("bad_transition", 3)
    with pytest.raises(StateError, match="invalid_status"):
        state.set_status(root, REPO, 7, "paused")


@pytest.mark.parametrize("last_step", ["landed_open", *state.RETAKE_STEPS])
def test_an_escalated_ending_is_never_turned_into_done(
    root: Path, last_step: str
) -> None:
    """Finding F36 of issue 675: wave 9 must not overwrite an escalated closeout ending."""
    make(root)
    state.record_done(root, REPO, 7, 8, last_step)
    state.set_status(root, REPO, 7, "escalated")
    with pytest.raises(StateError) as caught:
        state.set_status(root, REPO, 7, "done")
    assert (caught.value.reason, caught.value.code) == ("bad_transition", 3)
    doc = state.load_state(root, REPO, 7)
    assert (doc["status"], doc["step"]) == ("escalated", last_step)
    assert state.set_status(root, REPO, 7, "skipped")["status"] == "skipped"


def test_a_status_move_does_not_settle_an_open_intent(root: Path) -> None:
    make(root)
    state.record_intent(root, REPO, 7, 5, "worker_started")
    doc = state.set_status(root, REPO, 7, "escalated")
    assert state.pending_intent(doc)["step"] == "worker_started"


# --- plan records ---------------------------------------------------------------------------------


def test_plan_record_create_is_exclusive_and_a_second_create_finds_the_first(
    root: Path,
) -> None:
    doc, created = state.create_plan(root, REPO, 7, REQUESTED, ORCH, now=NOW)
    assert created
    path = state.plan_path(root, REPO, 7, REQUESTED)
    assert path.name == "plan-IronbellyOrg__IronClaude__7.20261119T100000Z.json"
    assert doc["schema"] == "orchestrator-plan/1" and doc["kind"] == "plan"
    assert (doc["status"], doc["step"], doc["requested_at"]) == (
        "in_progress",
        "plan_call_started",
        REQUESTED,
    )
    again, created = state.create_plan(
        root, REPO, 7, REQUESTED, ORCH
    )  # left by a kill before the ack
    assert not created and again == doc
    other, created = state.create_plan(root, REPO, 7, "2026-11-19T12:00:00Z", ORCH)
    assert (
        created and other["requested_at"] != doc["requested_at"]
    )  # a later request has its own file
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_plan_steps_and_the_final_record(root: Path) -> None:
    state.create_plan(root, REPO, 7, REQUESTED, ORCH)
    doc = state.record_plan_step(root, REPO, 7, REQUESTED, "plan_written", SHA)
    assert (doc["status"], doc["step"]) == ("in_progress", "plan_written")
    doc = state.record_plan_step(root, REPO, 7, REQUESTED, "plan_done")
    assert (doc["status"], doc["step"]) == ("done", "plan_done")
    for step in ("plan_written", "plan_failed", "plan_done"):
        with pytest.raises(StateError) as caught:
            state.record_plan_step(
                root, REPO, 7, REQUESTED, step, SHA if step == "plan_written" else "why"
            )
        assert (caught.value.reason, caught.value.code) == ("plan_final", 3)
    assert state.load_plan(root, REPO, 7, REQUESTED)["status"] == "done"


def test_a_failed_plan_needs_its_reason_and_ends_failed(root: Path) -> None:
    state.create_plan(root, REPO, 7, REQUESTED, ORCH)
    with pytest.raises(StateError, match="invalid_detail"):
        state.record_plan_step(root, REPO, 7, REQUESTED, "plan_failed")
    with pytest.raises(StateError, match="invalid_detail"):
        state.record_plan_step(root, REPO, 7, REQUESTED, "plan_written", "not a hash")
    with pytest.raises(StateError, match="invalid_plan_step"):
        state.record_plan_step(root, REPO, 7, REQUESTED, "plan_call_started")
    doc = state.record_plan_step(
        root, REPO, 7, REQUESTED, "plan_failed", "repeated_heading"
    )
    assert (doc["status"], doc["step"]) == ("failed", "plan_failed")
    assert doc["log"][-1]["detail"] == "repeated_heading"


def test_plan_records_are_found_by_the_restart_rule_and_unknown_ones_are_not_made(
    root: Path,
) -> None:
    with pytest.raises(StateError, match="not_found"):
        state.load_plan(root, REPO, 7, REQUESTED)
    with pytest.raises(StateError, match="not_found"):
        state.record_plan_step(root, REPO, 7, REQUESTED, "plan_done")
    with pytest.raises(ValueError):
        state.plan_path(root, REPO, 7, "yesterday")


# --- run files ----------------------------------------------------------------------------------------


def test_run_file_create_and_the_poll_reads_it(root: Path) -> None:
    doc = state.create_run(
        root,
        ORCH,
        "run-1:abc",
        "orchestrator-ironclaude-1",
        REPO,
        "host.local",
        now=NOW,
    )
    assert doc == {
        "schema": "orchestrator-run/1",
        "run_id": "run-1:abc",
        "tag": "orchestrator-ironclaude-1",
        "repo": REPO,
        "host": "host.local",
        "created_at": "2026-11-19T10:00:00Z",
        "status": "active",
    }
    info = route.read_run(root, ORCH)
    assert (info.status, info.run_id) == ("active", "run-1:abc")
    with pytest.raises(StateError, match="already_exists"):
        state.create_run(
            root, ORCH, "run-2", "orchestrator-ironclaude-1", REPO, "host.local"
        )
    assert state.load_run(root, ORCH) == doc
    assert stat.S_IMODE(state.run_path(root, ORCH).stat().st_mode) == 0o600
    with pytest.raises(StateError, match="not_found"):
        state.load_run(root, "ironclaude-2")  # a missing file is a first start


def test_run_status_moves_and_ended_is_final(root: Path) -> None:
    state.create_run(root, ORCH, "run-1", "orchestrator-ironclaude-1", REPO, "h")
    assert state.set_run_status(root, ORCH, "active")["status"] == "active"
    assert state.set_run_status(root, ORCH, "ending")["status"] == "ending"
    assert (
        state.set_run_status(root, ORCH, "active")["status"] == "active"
    )  # work arrived: stay
    state.set_run_status(root, ORCH, "ending")
    assert state.set_run_status(root, ORCH, "ended")["status"] == "ended"
    assert route.read_run(root, ORCH).status == "ended"
    for status in ("active", "ending"):
        with pytest.raises(StateError, match="bad_transition"):
            state.set_run_status(root, ORCH, status)
    with pytest.raises(StateError, match="invalid_status"):
        state.set_run_status(root, ORCH, "gone")


@pytest.mark.parametrize(
    "kw",
    [
        {"run_id": "bad id"},
        {"tag": "x" * 33},
        {"repo": "nope"},
        {"host": ""},
        {"ident": "Bad_Id"},
    ],
)
def test_run_create_refuses_bad_input(root: Path, kw: dict) -> None:
    args = {
        "ident": ORCH,
        "run_id": "r1",
        "tag": "orchestrator-x-1",
        "repo": REPO,
        "host": "h",
        **kw,
    }
    with pytest.raises(StateError):
        state.create_run(
            root, args["ident"], args["run_id"], args["tag"], args["repo"], args["host"]
        )
    assert not (root / ".orchestrator/runs").exists() or not list(
        (root / ".orchestrator/runs").iterdir()
    )


# --- what is open ----------------------------------------------------------------------------------------


def test_list_open_returns_the_files_to_resume_with_their_open_intent(
    root: Path,
) -> None:
    make(root, number=1)
    make(root, number=2)
    make(root, OTHER, 3)
    state.create_state(root, REPO, 4, "ironclaude-2")
    state.record_intent(root, REPO, 2, 4, "worker_started")
    state.set_status(root, REPO, 1, "done")
    state.create_plan(root, REPO, 5, REQUESTED, ORCH)
    items = state.list_open(root, ORCH)
    assert [(i["kind"], i["repo"], i["number"]) for i in items] == [
        ("issue", OTHER, 3),  # in the order of the file names
        ("issue", REPO, 2),
        ("plan", REPO, 5),
    ]
    assert (
        items[1]["pending_intent"]["step"] == "worker_started"
        and items[0]["pending_intent"] is None
    )
    assert items[2]["requested_at"] == REQUESTED
    assert [i["number"] for i in state.list_open(root, "ironclaude-2")] == [4]
    assert [i["number"] for i in state.list_open(root, ORCH, "done")] == [1]
    assert state.list_open(root / "nowhere") == []


# --- the lock -----------------------------------------------------------------------------------------------


def test_a_write_waits_for_the_lock_the_poll_also_takes(root: Path) -> None:
    make(root)
    with route.state_lock(root):
        with pytest.raises(StateError) as caught:
            with state.locked(root, wait_s=0.0):
                pass
    assert (caught.value.reason, caught.value.code) == ("lock_busy", 75)
    with state.locked(root, wait_s=0.0):
        pass  # free again


# --- the verb ---------------------------------------------------------------------------------------------


def cli(root: Path, *args: str) -> tuple[int, dict]:
    result = CliRunner().invoke(
        orchestrator_group, ["--root", str(root), "state", *args]
    )
    return result.exit_code, json.loads(result.output.strip().splitlines()[-1])


def test_the_verb_is_registered_under_the_superclaude_command() -> None:
    from superclaude.cli.main import main

    result = CliRunner().invoke(main, ["orchestrator", "--help"])
    assert result.exit_code == 0 and "state" in result.output
    assert "orchestrator" in CliRunner().invoke(main, ["--help"]).output


def test_the_verb_walks_one_issue_through_intent_done_set_and_status(
    root: Path,
) -> None:
    base = ["--repo", REPO, "--number", "7"]
    code, out = cli(root, "create", *base, "--orchestrator", ORCH, "--wake-id", WAKE)
    assert (code, out["ok"], out["status"], out["step"]) == (
        0,
        True,
        "in_progress",
        "claim",
    )
    code, out = cli(root, "create", *base, "--orchestrator", ORCH)
    assert (code, out) == (
        3,
        {
            "ok": False,
            "reason": "already_exists",
            "status": "in_progress",
            "step": "claim",
        },
    )
    assert cli(root, "intent", *base, "--wave", "1", "--step", "lease_posted")[0] == 0
    code, out = cli(root, "pending", *base)
    assert (code, out["pending_intent"]["step"]) == (0, "lease_posted")
    code, out = cli(root, "intent", *base, "--wave", "1", "--step", "again")
    assert (code, out["reason"]) == (3, "intent_open")
    assert (
        cli(
            root,
            "done",
            *base,
            "--wave",
            "1",
            "--step",
            "lease_posted",
            "--detail",
            "comment 5",
        )[0]
        == 0
    )
    assert cli(root, "pending", *base)[1]["pending_intent"] is None
    code, out = cli(
        root,
        "set",
        *base,
        "--id",
        "lease_comment_id=5",
        "--id",
        "branch=issue-7",
        "--body-sha",
        "abcdef0",
        "--tiers-json",
        '{"worker": {"requested": "tier2"}}',
    )
    assert (code, out["ok"]) == (0, True)
    code, out = cli(root, "show", *base)
    assert out["state"]["ids"] == {"lease_comment_id": 5, "branch": "issue-7"}
    assert out["state"]["tiers"] == {"worker": {"requested": "tier2"}}
    assert (
        cli(root, "set", *base, "--id", "branch=")[0] == 0
    )  # an empty value removes the id
    assert cli(root, "show", *base)[1]["state"]["ids"] == {"lease_comment_id": 5}
    code, out = cli(root, "list", "--orchestrator", ORCH)
    assert [i["number"] for i in out["items"]] == [7]
    assert cli(root, "status", *base, "escalated")[0] == 0
    code, out = cli(root, "status", *base, "done")  # never straight from escalated
    assert (code, out["reason"]) == (3, "bad_transition")
    assert cli(root, "status", *base, "in_progress")[0] == 0  # after the answer
    assert cli(root, "status", *base, "done")[0] == 0
    code, out = cli(root, "status", *base, "in_progress")
    assert (code, out["reason"]) == (3, "bad_transition")


@pytest.mark.parametrize(
    ("args", "code", "reason"),
    [
        (["show", "--repo", REPO, "--number", "9"], 5, "not_found"),
        (["show", "--repo", "bad repo", "--number", "9"], 2, "invalid_input"),
        (
            [
                "intent",
                "--repo",
                REPO,
                "--number",
                "9",
                "--wave",
                "1",
                "--step",
                "x_step",
            ],
            5,
            "not_found",
        ),
        (
            ["set", "--repo", REPO, "--number", "9", "--id", "nope=1"],
            2,
            "unknown_id_name",
        ),
        (
            ["set", "--repo", REPO, "--number", "9", "--id", "no_equals"],
            2,
            "unknown_id_name",
        ),
        (
            ["set", "--repo", REPO, "--number", "9", "--tiers-json", "[1]"],
            2,
            "invalid_tiers",
        ),
        (
            ["set", "--repo", REPO, "--number", "9", "--tiers-json", "{"],
            2,
            "invalid_tiers",
        ),
        (
            ["plan-show", "--repo", REPO, "--number", "9", "--requested-at", "never"],
            2,
            "invalid_input",
        ),
        (["run-show", "--id", ORCH], 5, "not_found"),
        (["run-show", "--id", "Bad_Id"], 2, "invalid_orchestrator_id"),
    ],
)
def test_the_verb_prints_a_reason_code_and_exits_with_its_code(
    root: Path, args: list, code: int, reason: str
) -> None:
    got_code, out = cli(root, *args)
    assert (got_code, out["ok"], out["reason"]) == (code, False, reason)


def test_the_verb_keeps_plan_records_and_run_files(root: Path) -> None:
    base = ["--repo", REPO, "--number", "7", "--requested-at", REQUESTED]
    code, out = cli(root, "plan-create", *base, "--orchestrator", ORCH)
    assert (code, out["created"], out["step"]) == (0, True, "plan_call_started")
    assert (
        cli(root, "plan-create", *base, "--orchestrator", ORCH)[1]["created"] is False
    )
    assert (
        cli(root, "plan-step", *base, "--step", "plan_written", "--detail", SHA)[0] == 0
    )
    code, out = cli(root, "plan-step", *base, "--step", "plan_failed")
    assert (code, out["reason"]) == (2, "invalid_detail")
    assert cli(root, "plan-step", *base, "--step", "plan_done")[1]["status"] == "done"
    assert cli(root, "plan-show", *base)[1]["plan"]["status"] == "done"
    code, out = cli(
        root,
        "run-create",
        "--id",
        ORCH,
        "--run-id",
        "run-1",
        "--tag",
        "orchestrator-ironclaude-1",
        "--repo",
        REPO,
        "--host",
        "h",
    )
    assert (code, out["run"]["status"]) == (0, "active")
    assert (
        cli(
            root,
            "run-create",
            "--id",
            ORCH,
            "--run-id",
            "run-2",
            "--tag",
            "t",
            "--repo",
            REPO,
            "--host",
            "h",
        )[0]
        == 3
    )
    assert (
        cli(root, "run-status", "--id", ORCH, "ending")[1]["run"]["status"] == "ending"
    )
    assert cli(root, "run-show", "--id", ORCH)[1]["run"]["run_id"] == "run-1"


def test_the_root_comes_from_the_option_the_environment_or_the_current_directory(
    root: Path, monkeypatch
) -> None:
    base = ["--repo", REPO, "--number", "7", "--orchestrator", ORCH]
    runner = CliRunner()
    monkeypatch.setenv(failpoint.ENABLE_VAR, "0")
    env_root = root / "from_env"
    env_root.mkdir()
    result = runner.invoke(
        orchestrator_group,
        ["state", "create", *base],
        env={"SUPERCLAUDE_ORCHESTRATOR_ROOT": str(env_root)},
    )
    assert result.exit_code == 0 and state.state_path(env_root, REPO, 7).exists()
    cwd_root = root / "from_cwd"
    cwd_root.mkdir()
    monkeypatch.chdir(cwd_root)
    assert runner.invoke(orchestrator_group, ["state", "create", *base]).exit_code == 0
    assert state.state_path(cwd_root, REPO, 7).exists()
    missing = runner.invoke(
        orchestrator_group, ["--root", str(root / "nowhere"), "state", "create", *base]
    )
    assert missing.exit_code == 2  # click refuses a root that is not a folder


# --- the failpoint of T5 (open question Q11) ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("env", "wave", "step", "active"),
    [
        ({}, 1, "lease_posted", False),
        (
            {"SUPERCLAUDE_FAILPOINT": "after_intent"},
            1,
            "lease_posted",
            False,
        ),  # not enabled
        (
            {"SUPERCLAUDE_TEST_FAILPOINTS": "1"},
            1,
            "lease_posted",
            False,
        ),  # no place named
        (
            {
                "SUPERCLAUDE_TEST_FAILPOINTS": "true",
                "SUPERCLAUDE_FAILPOINT": "after_intent",
            },
            1,
            "x",
            False,
        ),
        (
            {"SUPERCLAUDE_TEST_FAILPOINTS": "1", "SUPERCLAUDE_FAILPOINT": "after_done"},
            1,
            "x",
            False,
        ),
        (
            {
                "SUPERCLAUDE_TEST_FAILPOINTS": "1",
                "SUPERCLAUDE_FAILPOINT": "after_intent",
            },
            1,
            "lease_posted",
            True,
        ),
        (
            {
                "SUPERCLAUDE_TEST_FAILPOINTS": "1",
                "SUPERCLAUDE_FAILPOINT": "after_intent:lease_posted",
            },
            1,
            "lease_posted",
            True,
        ),
        (
            {
                "SUPERCLAUDE_TEST_FAILPOINTS": "1",
                "SUPERCLAUDE_FAILPOINT": "after_intent:other",
            },
            1,
            "lease_posted",
            False,
        ),
        (
            {
                "SUPERCLAUDE_TEST_FAILPOINTS": "1",
                "SUPERCLAUDE_FAILPOINT": "after_intent:1:lease_posted",
            },
            1,
            "lease_posted",
            True,
        ),
        (
            {
                "SUPERCLAUDE_TEST_FAILPOINTS": "1",
                "SUPERCLAUDE_FAILPOINT": "after_intent:2:lease_posted",
            },
            1,
            "lease_posted",
            False,
        ),
        (
            {
                "SUPERCLAUDE_TEST_FAILPOINTS": "1",
                "SUPERCLAUDE_FAILPOINT": "after_intent:1:a:b",
            },
            1,
            "a",
            False,
        ),
    ],
)
def test_the_failpoint_is_active_only_with_both_variables_and_a_matching_place(
    env, wave, step, active
) -> None:
    stops: list[int] = []
    failpoint.after_intent(wave, step, env=env, stop=stops.append)
    assert stops == ([failpoint.EXIT_CODE] if active else [])
    assert failpoint.active_for(wave, step, env) is active


def test_the_failpoint_does_nothing_in_the_process_environment_of_the_tests(
    root: Path,
) -> None:
    """The variables are not set in a normal run, so the verb never stops."""
    assert (
        failpoint.ENABLE_VAR not in os.environ
        or os.environ[failpoint.ENABLE_VAR] != "1"
    )
    make(root)
    code, _ = cli(
        root,
        "intent",
        "--repo",
        REPO,
        "--number",
        "7",
        "--wave",
        "1",
        "--step",
        "x_step",
    )
    assert code == 0


def run_main(
    root: Path, home: Path, env_extra: dict, *args: str
) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("SUPERCLAUDE_")}
    env.update({"HOME": str(home), **env_extra})
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "superclaude.cli.main",
            "orchestrator",
            "--root",
            str(root),
            "state",
            *args,
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
        check=False,
    )


def test_the_failpoint_ends_the_real_process_after_the_intent_line_and_the_restart_settles_it(
    root: Path, tmp_path_factory
) -> None:
    home = tmp_path_factory.mktemp("home")
    base = ["--repo", REPO, "--number", "7"]
    make(root)
    on = {
        "SUPERCLAUDE_TEST_FAILPOINTS": "1",
        "SUPERCLAUDE_FAILPOINT": "after_intent:worker_started",
    }
    other = run_main(
        root, home, on, "intent", *base, "--wave", "4", "--step", "other_step"
    )
    assert other.returncode == 0  # a different step does not stop
    run_main(root, home, {}, "done", *base, "--wave", "4", "--step", "other_step")
    killed = run_main(
        root, home, on, "intent", *base, "--wave", "4", "--step", "worker_started"
    )
    assert killed.returncode == failpoint.EXIT_CODE
    assert killed.stdout == ""  # ended before any output, like a kill
    assert "failpoint" in killed.stderr
    doc = state.load_state(root, REPO, 7)  # the line is saved
    assert state.pending_intent(doc)["step"] == "worker_started"
    # the restart (no failpoint variables) finds it open, and a repeated intent is refused
    pending = json.loads(run_main(root, home, {}, "pending", *base).stdout)
    assert pending["pending_intent"]["step"] == "worker_started"
    again = run_main(
        root, home, {}, "intent", *base, "--wave", "4", "--step", "worker_started"
    )
    assert (again.returncode, json.loads(again.stdout)["reason"]) == (3, "intent_open")
    settled = run_main(
        root,
        home,
        {},
        "done",
        *base,
        "--wave",
        "4",
        "--step",
        "worker_started",
        "--detail",
        "seen outside",
    )
    assert settled.returncode == 0
    assert state.pending_intent(state.load_state(root, REPO, 7)) is None
