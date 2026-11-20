"""``wake-check`` (design 3.4, 3.5): every case of the table of 3.5, each with a mutation of the golden wake file."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import wake
from superclaude.cli.orchestrator import state

from .fake_world import (
    ORCH,
    REPO,
    TAG,
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


@pytest.fixture
def world(monkeypatch) -> World:
    w = install(monkeypatch, World())
    yield w
    assert not w.unexpected, w.unexpected


@pytest.fixture
def root(tmp_path: Path, world: World) -> Path:
    return make_root(tmp_path)


def check(root: Path, **kw) -> tuple[int, dict]:
    return call(root, "wake-check", WID, **kw)


def nothing_taken(root: Path) -> None:
    """No acknowledgment and no state file: a refused wake takes nothing."""
    assert not (root / WAKES / f"{WID}.ack.json").exists()
    assert not (root / ".orchestrator" / "issues").exists()


def mutate(path: list, value) -> dict:
    doc = golden()
    node = doc
    for part in path[:-1]:
        node = node[part]
    node[path[-1]] = value
    return doc


# --- the golden wake is accepted ---------------------------------------------------------------


def test_the_golden_wake_is_read_and_each_item_is_new(root: Path) -> None:
    put_wake(root)
    code, out = check(root)
    assert code == 0 and out["ok"] is True and out["already_acked"] is False
    assert out["wake"] == golden()  # the normalized wake is what the poll wrote
    assert out["assigned"] == [
        {
            "repo": REPO,
            "number": 655,
            "decision": "new",
            "reason": None,
            "same_wake": False,
            "checkout_state": "ok",
        }
    ]
    assert out["plan_requests"] == [
        {
            "repo": REPO,
            "number": 656,
            "requested_at": "2026-11-19T10:15:00Z",
            "decision": "new",
            "reason": None,
        }
    ]
    assert out["rejected_items"] == [] and out["warnings"] == []
    assert out["own"] == {"orchestrator": ORCH, "tag": TAG}
    nothing_taken(root)
    assert not (root / WAKES / f"{WID}.rejected.json").exists()


def test_a_flag_cannot_name_another_orchestrator_than_the_session_tag_does(
    root: Path,
) -> None:
    put_wake(root)
    code, out = call(
        root, "wake-check", WID, "--orchestrator", "ironclaude-2"
    )  # the tag is ironclaude-1
    assert (code, out["reason"]) == (2, "identity_mismatch")
    assert not (root / WAKES / f"{WID}.rejected.json").exists()


@pytest.mark.parametrize(
    "flags",
    [
        ["--tag", "orchestrator-ironclaude-2"],
        ["--orchestrator", "ironclaude-2", "--tag", "orchestrator-ironclaude-2"],
        ["--orchestrator", "ironclaude-1", "--tag", "orchestrator-ironclaude-2"],
    ],
)
def test_no_flag_can_move_the_identity_away_from_the_tag_of_the_session(
    root: Path, flags: list[str]
) -> None:
    put_wake(root)
    code, out = call(root, "wake-check", WID, *flags)  # the session tag is ironclaude-1
    assert (code, out["reason"]) == (2, "identity_mismatch")
    assert not (root / WAKES / f"{WID}.rejected.json").exists()


def test_the_identity_can_be_given_by_flags_and_is_otherwise_unknown(
    root: Path,
) -> None:
    put_wake(root)
    code, out = call(
        root, "wake-check", WID, "--orchestrator", ORCH, "--tag", TAG, tag=None
    )
    assert code == 0 and out["own"]["orchestrator"] == ORCH
    code, out = call(root, "wake-check", WID, tag=None)
    assert (code, out["reason"]) == (2, "own_identity_unknown")
    assert not (
        root / WAKES / f"{WID}.rejected.json"
    ).exists()  # nothing could be judged


def test_a_bad_wake_id_is_refused_and_names_no_file(root: Path) -> None:
    code, out = call(root, "wake-check", "../../etc/passwd")
    assert (code, out["reason"]) == (2, "invalid_wake_id")
    assert list((root / ".orchestrator").glob("**/*rejected*")) == []


# --- row 1 of 3.5: the whole wake is rejected ---------------------------------------------------


def _missing(root: Path) -> None:
    pass  # no file at all


def _unreadable(root: Path) -> None:
    os.symlink(
        root / "repos.yaml", root / WAKES / f"{WID}.json"
    )  # a link is never followed


def _too_large(root: Path) -> None:
    put_wake(
        root, raw=json.dumps(golden()).encode().ljust(wake.MAX_WAKE_BYTES + 5, b" ")
    )


def _not_json(root: Path) -> None:
    put_wake(root, raw=b"this is not json")


def _not_an_object(root: Path) -> None:
    put_wake(root, raw=b'["orchestrator-wake/1"]')


def _future_schema(root: Path) -> None:
    put_wake(root, mutate(["schema"], "orchestrator-wake/2"))


def _no_schema(root: Path) -> None:
    doc = golden()
    del doc["schema"]
    put_wake(root, doc)


def _id_differs(root: Path) -> None:
    put_wake(root, mutate(["wake_id"], "20261119T101500Z-00000000"))


def _id_malformed(root: Path) -> None:
    put_wake(root, mutate(["wake_id"], "not-a-wake-id"))


def _other_orchestrator(root: Path) -> None:
    put_wake(root, mutate(["target", "orchestrator"], "ironclaude-2"))


def _other_tag(root: Path) -> None:
    put_wake(root, mutate(["target", "tag"], "orchestrator-ironclaude-2"))


WHOLE_WAKE = [
    (_missing, "missing"),
    (_unreadable, "missing"),
    (_too_large, "too_large"),
    (_not_json, "not_json"),
    (_not_an_object, "not_json"),
    (_future_schema, "schema_unsupported"),
    (_no_schema, "schema_unsupported"),
    (_id_differs, "id_mismatch"),
    (_id_malformed, "id_mismatch"),
    (_other_orchestrator, "wrong_target"),
    (_other_tag, "wrong_target"),
]


@pytest.mark.parametrize(
    ("mutation", "why"), WHOLE_WAKE, ids=[m.__name__ for m, _ in WHOLE_WAKE]
)
def test_a_whole_wake_is_rejected_with_one_closed_reason_and_nothing_is_taken(
    root: Path, mutation, why: str
) -> None:
    (root / WAKES).mkdir(parents=True, exist_ok=True)
    mutation(root)
    code, out = check(root)
    assert (code, out["ok"], out["reason"], out["why"]) == (
        3,
        False,
        "wake_rejected",
        why,
    )
    marker = root / WAKES / f"{WID}.rejected.json"
    doc = json.loads(marker.read_text())
    assert (
        doc["reason"] == why and doc["wake_id"] == WID and doc["orchestrator"] == ORCH
    )
    assert why in wake.REJECT_REASONS
    assert stat.S_IMODE(marker.stat().st_mode) == 0o600
    nothing_taken(root)


def test_the_unmutated_golden_file_passes_where_each_mutation_fails(root: Path) -> None:
    put_wake(root)
    assert check(root)[0] == 0


def test_a_wake_for_another_orchestrator_names_wrong_target_and_the_right_one_still_reads_it(
    root: Path,
) -> None:
    put_wake(root)
    code, out = call(root, "wake-check", WID, tag="orchestrator-ironclaude-2")
    assert (code, out["why"]) == (3, "wrong_target")
    # the marker belongs to the wake, not to the reader; the target is unaffected
    code, out = check(root)
    assert code == 0 and out["wake"]["target"]["orchestrator"] == ORCH


# --- row 3: one bad item is dropped ---------------------------------------------------------------


BAD_ASSIGNED_FIELD = {
    "repo": "not a repo",
    "number": "655",  # a string, never an integer
    "assignees": ["bad login!"],
    "checkout_state": "nope",
}


@pytest.mark.parametrize("field", list(BAD_ASSIGNED_FIELD))
def test_one_bad_assigned_item_is_dropped_and_the_rest_is_processed(
    root: Path, field: str
) -> None:
    doc = golden()
    doc["assigned"][0][field] = BAD_ASSIGNED_FIELD[field]
    put_wake(root, doc)
    code, out = check(root)
    assert code == 0
    assert out["rejected_items"] == [{"index": 0, "reason": "malformed_item"}]
    assert out["assigned"] == []
    assert [p["number"] for p in out["plan_requests"]] == [656]  # the rest goes on


def test_a_bad_plan_request_is_indexed_after_the_assigned_items(root: Path) -> None:
    doc = golden()
    doc["plan_requests"][0]["missing"] = ["priority", "bogus"]
    put_wake(root, doc)
    code, out = check(root)
    assert code == 0
    assert out["rejected_items"] == [{"index": 1, "reason": "malformed_item"}]
    assert [a["number"] for a in out["assigned"]] == [655] and out[
        "plan_requests"
    ] == []


def test_a_bad_information_item_is_counted_and_never_takes_the_index_of_an_entry(
    root: Path,
) -> None:
    doc = golden()
    doc["info"]["mentions"][0]["kind"] = "discussion"  # an unknown kind
    doc["skipped"][0]["reason"] = "Not A Token"
    put_wake(root, doc)
    code, out = check(root)
    assert code == 0
    assert out["rejected_items"] == []  # index 0 is the first assigned item, not these
    assert (
        out["dropped_info_items"] == 2 and "malformed_info_items:2" in out["warnings"]
    )
    assert [a["number"] for a in out["assigned"]] == [655]


# --- row 4: repo not listed or disabled ----------------------------------------------------------


def test_an_unlisted_repo_is_skipped_repo_not_listed(
    tmp_path: Path, world: World
) -> None:
    root = make_root(tmp_path, text=repos_text(repos=[]))
    put_wake(root)
    code, out = check(root)
    assert code == 0
    assert (out["assigned"][0]["decision"], out["assigned"][0]["reason"]) == (
        "skipped",
        "repo_not_listed",
    )
    assert (out["plan_requests"][0]["decision"], out["plan_requests"][0]["reason"]) == (
        "skipped",
        "repo_not_listed",
    )


def test_a_disabled_repo_is_skipped_repo_disabled(tmp_path: Path, world: World) -> None:
    listed = {"repo": REPO, "enabled": False, "checkout": None}
    root = make_root(tmp_path, text=repos_text(repos=[listed]))
    put_wake(root)
    code, out = check(root)
    assert code == 0
    assert out["assigned"][0]["reason"] == "repo_disabled"
    assert out["plan_requests"][0]["reason"] == "repo_disabled"


def test_a_broken_repos_file_stops_the_check_and_writes_nothing(
    tmp_path: Path, world: World
) -> None:
    root = make_root(tmp_path, text="schema_version: 2\n")
    put_wake(root)
    code, out = check(root)
    assert (code, out["reason"]) == (2, "repos_invalid")
    assert not (root / WAKES / f"{WID}.rejected.json").exists()
    nothing_taken(root)


# --- row 5: unknown extra keys -----------------------------------------------------------------


def test_unknown_keys_become_warnings(root: Path) -> None:
    doc = golden()
    doc["future_field"] = 1
    doc["not a safe name"] = 2
    put_wake(root, doc)
    code, out = check(root)
    assert code == 0
    assert sorted(out["warnings"]) == ["unknown_key", "unknown_key:future_field"]
    assert out["assigned"][0]["decision"] == "new"


# --- row 6: a wake that was already acknowledged -------------------------------------------------


def _ack_doc(**over) -> dict:
    doc = {
        "schema": "orchestrator-wake-ack/1",
        "wake_id": WID,
        "acked_at": "2026-11-19T10:16:00Z",
        "orchestrator": {"id": ORCH, "run_id": "run_abc123", "host": "ws-aidev02"},
        "taken": [{"repo": REPO, "number": 655}],
        "skipped": [],
        "rejected_items": [],
        "warnings": [],
    }
    doc.update(over)
    return doc


def test_an_acknowledged_wake_prints_the_same_acknowledgment_and_processes_nothing(
    root: Path,
) -> None:
    put_wake(root)
    ack = root / WAKES / f"{WID}.ack.json"
    ack.write_text(json.dumps(_ack_doc()))
    code, out = check(root)
    assert code == 0 and out["already_acked"] is True and out["ack"] == _ack_doc()
    assert "assigned" not in out
    assert not (root / ".orchestrator" / "issues").exists()


def test_the_acknowledgment_is_found_after_the_poll_moved_both_files_to_done(
    root: Path,
) -> None:
    done = root / WAKES / "done"
    done.mkdir(parents=True)
    put_wake(root)
    for suffix in (".json",):
        (root / WAKES / f"{WID}{suffix}").rename(done / f"{WID}{suffix}")
    (done / f"{WID}.ack.json").write_text(json.dumps(_ack_doc()))
    code, out = check(root)
    assert code == 0 and out["already_acked"] is True and out["ack"] == _ack_doc()


def test_an_acknowledgment_with_another_wake_id_is_not_one(root: Path) -> None:
    put_wake(root)
    (root / WAKES / f"{WID}.ack.json").write_text(
        json.dumps(_ack_doc(wake_id="20261119T101500Z-00000000"))
    )
    code, out = check(root)
    assert code == 0 and out["already_acked"] is False


# --- row 7: an item that already has a state file ------------------------------------------------


@pytest.mark.parametrize(
    "status", ["in_progress", "done", "skipped", "failed", "escalated"]
)
def test_an_item_with_a_state_file_is_skipped_already_dispatched(
    root: Path, status: str
) -> None:
    put_wake(root)
    state.create_state(root, REPO, 655, ORCH, wake_id="20261118T000000Z-aaaaaaaa")
    if status != "in_progress":
        state.set_status(root, REPO, 655, status if status != "done" else "done")
    code, out = check(root)
    assert code == 0
    assert (out["assigned"][0]["decision"], out["assigned"][0]["reason"]) == (
        "skipped",
        "already_dispatched",
    )
    assert out["assigned"][0]["same_wake"] is False
    assert (
        out["plan_requests"][0]["decision"] == "new"
    )  # a plan request has no state file


def test_a_state_file_made_for_this_wake_says_so(root: Path) -> None:
    put_wake(root)
    state.create_state(root, REPO, 655, ORCH, wake_id=WID)
    code, out = check(root)
    assert code == 0 and out["assigned"][0]["same_wake"] is True


def test_an_unreadable_state_file_is_never_taken(root: Path) -> None:
    put_wake(root)
    path = state.state_path(root, REPO, 655)
    path.parent.mkdir(parents=True)
    path.write_text("{not json")
    code, out = check(root)
    assert code == 0 and out["assigned"][0]["reason"] == "already_dispatched"
    assert path.read_text() == "{not json"  # never overwritten


# --- a resume wake ------------------------------------------------------------------------------


def test_a_resume_wake_has_no_items(root: Path) -> None:
    doc = golden()
    doc["target"]["resume"] = True
    doc["assigned"], doc["plan_requests"] = [], []
    put_wake(root, doc)
    code, out = check(root)
    assert code == 0 and out["wake"]["target"]["resume"] is True
    assert out["assigned"] == [] and out["plan_requests"] == []
