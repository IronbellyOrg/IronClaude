"""The wake file, its parser, the acknowledgment and the delivery (design section 3 and DQ2)."""

from __future__ import annotations

import copy
import json
import os
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import wake
from superclaude.cli.issue_watch.launch import LaunchOutcome

from .conftest import load_fixture, result

GOLDEN = Path(__file__).parent / "fixtures" / "orchestrator_wake_golden.json"
ORCA = "/opt/orca/bin/orca"
WORKSPACE = Path("/orch")
NOW = datetime(2026, 11, 19, 10, 15, 0, tzinfo=timezone.utc)
T = lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)  # noqa: E731
WID = "20261119T101500Z-3fa9c1d2"


def sample(**over) -> wake.Wake:
    base = dict(
        wake_id=WID,
        created_at=T("2026-11-19T10:15:00Z"),
        cycle_id="0123456789abcdef0123456789abcdef",
        host="ws-aidev02",
        login="clayphi",
        since=T("2026-11-19T10:10:00Z"),
        gh_calls=9,
        target=wake.WakeTarget("ironclaude-1", "orchestrator-ironclaude-1", "IronbellyOrg/IronClaude", False),
        attempt=1,
        assigned=(wake.AssignedItem("IronbellyOrg/IronClaude", 655, ("clayphi",), T("2026-11-19T10:15:00Z"), "ok"),),
        mentions=(wake.InfoRef("IronbellyGroup/example", 12, "issue", T("2026-11-19T10:12:41Z")),),
        plan_requests=(
            wake.PlanRequestItem(
                "IronbellyOrg/IronClaude", 656, "Add the hold to the poll",
                "https://github.com/IronbellyOrg/IronClaude/issues/656", ("fix_approach", "test_plan"),
                T("2026-11-19T09:10:00Z"), T("2026-11-19T10:15:00Z"),
            ),
        ),
        skipped=(wake.SkippedItem("IronbellyOrg/Coder", 477, "repo_not_listed"),),
    )  # fmt: skip
    base.update(over)
    return wake.Wake(**base)


def golden() -> dict:
    return json.loads(GOLDEN.read_text(encoding="utf-8"))


def parse(data: dict | bytes, name: str | None = None, **kw):
    raw = data if isinstance(data, bytes) else json.dumps(data).encode()
    if name is None:
        name = (
            f"{json.loads(raw).get('wake_id')}.json"
            if not isinstance(data, bytes)
            else f"{WID}.json"
        )
    return wake.parse_wake(raw, name, **kw)


# --- the golden file shared with the orchestrator skill (PR B) ---------------------------------------------


def normalise(d: dict) -> dict:
    """Replace the ids and times of a wake file by placeholders."""
    d = copy.deepcopy(d)

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in {"wake_id", "cycle_id", "host"}:
                    node[k] = f"<{k}>"
                elif k in {
                    "created_at",
                    "since",
                    "first_seen_at",
                    "updated_at",
                    "held_since",
                    "requested_at",
                }:
                    node[k] = "<time>"
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(d)
    return d


def test_the_writers_output_equals_the_golden_file_apart_from_ids_and_times():
    made = wake.wake_to_json(
        sample(wake_id="20270101T000000Z-aaaaaaaa", host="other-host")
    )
    assert normalise(made) == normalise(golden())
    assert wake.wake_to_json(sample()) == golden()  # and exactly, with the golden ids


def test_the_golden_file_has_the_fields_of_section_3_4_and_nothing_else():
    g = golden()
    assert set(g) == {
        "schema",
        "wake_id",
        "created_at",
        "poll",
        "target",
        "attempt",
        "assigned",
        "info",
        "plan_requests",
        "skipped",
    }
    assert g["schema"] == "orchestrator-wake/1"
    assert (
        set(g["poll"]) == {"cycle_id", "host", "login", "since", "gh_calls", "dry_run"}
        and g["poll"]["dry_run"] is False
    )
    assert set(g["target"]) == {"orchestrator", "tag", "repo", "resume"}
    assert set(g["assigned"][0]) == {
        "repo",
        "number",
        "assignees",
        "first_seen_at",
        "checkout_state",
    }
    assert set(g["info"]) == {"mentions", "could_assign", "affects"}
    assert set(g["plan_requests"][0]) == {
        "repo",
        "number",
        "title",
        "url",
        "missing",
        "held_since",
        "requested_at",
    }
    assert set(g["skipped"][0]) == {"repo", "number", "reason"}
    assert (
        "hold" not in g["assigned"][0] and "missing" not in g["assigned"][0]
    )  # a held issue is never assigned
    assert not (
        {"title", "body", "labels", "checkout", "merge_method"} & set(g["assigned"][0])
    )


def test_the_parser_accepts_the_golden_file_and_reads_every_item():
    parsed = parse(golden())
    assert parsed.rejected == () and parsed.warnings == ()
    assert parsed.wake == sample()
    assert wake.wake_to_json(parsed.wake) == golden()  # a round trip


def test_the_golden_file_is_under_the_size_limit_and_ends_with_a_newline():
    raw = GOLDEN.read_bytes()
    assert len(raw) < wake.MAX_WAKE_BYTES and raw.endswith(b"\n") and raw.isascii()


# --- the parser: each case of 3.5 has a mutation that makes it fail ---------------------------------------------


def mutate(path: list, value: object) -> dict:
    d = golden()
    node = d
    for key in path[:-1]:
        node = node[key]
    if value is KeyError:
        del node[path[-1]]
    else:
        node[path[-1]] = value
    return d


@pytest.mark.parametrize(
    ("bad", "reason"),
    [
        (b"x" * (wake.MAX_WAKE_BYTES + 1), "too_large"),
        (b"{not json", "not_json"),
        (b"\xff\xfe", "not_json"),
        (b"[1, 2]", "not_json"),
        (
            mutate(["schema"], "orchestrator-wake/2"),
            "schema_unsupported",
        ),  # a future version
        (mutate(["schema"], KeyError), "schema_unsupported"),
        (mutate(["wake_id"], "20261119T101500Z-ffffffff"), "id_mismatch"),
        (mutate(["wake_id"], "not-an-id"), "id_mismatch"),
        (
            mutate(["poll", "dry_run"], True),
            "not_json",
        ),  # a dry run never writes a wake
        (mutate(["target", "resume"], "no"), "not_json"),
        (mutate(["attempt"], 4), "not_json"),
        (mutate(["created_at"], "yesterday"), "not_json"),
        (mutate(["info", "mentions"], "x"), "not_json"),
        (mutate(["assigned"], [golden()["assigned"][0]] * 11), "too_large"),
        (
            mutate(["plan_requests"], [golden()["plan_requests"][0]] * 11),
            "too_large",
        ),  # finding F5
        (mutate(["skipped"], [golden()["skipped"][0]] * 101), "too_large"),
    ],
)
def test_a_whole_wake_is_rejected_with_a_closed_reason(bad, reason):
    with pytest.raises(wake.WakeRejected) as err:
        raw = bad if isinstance(bad, bytes) else json.dumps(bad).encode()
        wake.parse_wake(raw, f"{WID}.json")
    assert err.value.reason == reason and reason in wake.REJECT_REASONS


def test_a_wake_for_another_orchestrator_or_tag_is_wrong_target():
    for kw in ({"own_id": "ironclaude-2"}, {"own_tag": "orchestrator-ironclaude-2"}):
        with pytest.raises(wake.WakeRejected) as err:
            parse(golden(), **kw)
        assert err.value.reason == "wrong_target"
    assert (
        parse(
            golden(), own_id="ironclaude-1", own_tag="orchestrator-ironclaude-1"
        ).rejected
        == ()
    )


def test_the_file_name_must_equal_the_wake_id():
    with pytest.raises(wake.WakeRejected, match="id_mismatch"):
        parse(golden(), name="20261119T101500Z-00000000.json")
    with pytest.raises(wake.WakeRejected, match="id_mismatch"):
        parse(golden(), name=f"{WID}.rejected.json")


@pytest.mark.parametrize(
    ("array", "index", "field", "value"),
    [
        ("assigned", 0, "repo", "no-slash"),
        ("assigned", 0, "repo", "Other/Repo"),  # not the target's repo
        ("assigned", 0, "number", "655"),
        ("assigned", 0, "number", True),
        ("assigned", 0, "number", 0),
        ("assigned", 0, "number", 10**9),
        ("assigned", 0, "assignees", []),
        ("assigned", 0, "assignees", ["bad login!"]),
        ("assigned", 0, "assignees", ["a"] * 11),
        ("assigned", 0, "checkout_state", "elsewhere"),
        ("assigned", 0, "first_seen_at", "soon"),
        ("plan_requests", 0, "title", "a\nb"),
        ("plan_requests", 0, "title", ""),
        ("plan_requests", 0, "title", "x" * 257),
        ("plan_requests", 0, "url", "https://example.com/x"),
        (
            "plan_requests",
            0,
            "url",
            "https://github.com/IronbellyOrg/IronClaude/issues/1",
        ),
        ("plan_requests", 0, "missing", ["title"]),
        ("plan_requests", 0, "missing", []),
        ("plan_requests", 0, "missing", ["priority", "priority"]),
    ],
)
def test_one_item_that_fails_its_rule_is_dropped_and_the_rest_is_processed(
    array, index, field, value
):
    d = golden()
    d[array][index][field] = value
    parsed = parse(d)
    assert parsed.rejected == (
        (index + (1 if array == "plan_requests" else 0), "malformed_item"),
    )
    assert len(getattr(parsed.wake, array if array != "assigned" else "assigned")) == 0
    assert (
        len(parsed.wake.mentions) == 1 and len(parsed.wake.skipped) == 1
    )  # the rest is processed


def test_a_bad_info_item_or_skip_is_dropped_and_unknown_keys_are_named_as_warnings():
    d = golden()
    d["info"]["mentions"].append(
        {
            "repo": "x",
            "number": 1,
            "kind": "issue",
            "updated_at": "2026-11-19T10:12:41Z",
        }
    )
    d["info"]["affects"].append(
        {
            "repo": "o/r",
            "number": 1,
            "kind": "branch",
            "updated_at": "2026-11-19T10:12:41Z",
        }
    )
    d["skipped"].append({"repo": "o/r", "number": 1, "reason": "Not A Token"})
    d["surprise"] = 1
    d["another"] = 2
    parsed = parse(d)
    assert (
        len(parsed.wake.mentions) == 1
        and parsed.wake.affects == ()
        and len(parsed.wake.skipped) == 1
    )
    assert parsed.warnings == ("another", "surprise")


def test_a_resume_wake_has_no_items():
    d = golden()
    d["target"]["resume"] = True
    d["assigned"], d["plan_requests"] = [], []
    parsed = parse(d)
    assert parsed.wake.target.resume is True and parsed.wake.assigned == ()
    with pytest.raises(wake.WakeError):
        wake.wake_to_json(
            sample(
                target=wake.WakeTarget(
                    "ironclaude-1",
                    "orchestrator-ironclaude-1",
                    "IronbellyOrg/IronClaude",
                    True,
                )
            )
        )


# --- the writer ----------------------------------------------------------------------------------------------------


def test_the_writer_makes_the_file_at_mode_0600_through_a_rename(tmp_path):
    path = wake.write_wake_file(tmp_path, sample())
    assert path == tmp_path / ".orchestrator" / "wakes" / f"{WID}.json"
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
    assert stat.S_IMODE(os.stat(path.parent).st_mode) == 0o700
    assert sorted(p.name for p in path.parent.iterdir()) == [
        f"{WID}.json"
    ]  # no temp file left
    assert wake.parse_wake(path.read_bytes(), path.name).wake == sample()


def test_the_writer_refuses_a_wake_over_a_limit_or_over_64_kib(tmp_path):
    big = sample(
        skipped=tuple(
            wake.SkippedItem("o/r", n, "repo_not_listed") for n in range(1, 102)
        )
    )
    with pytest.raises(wake.WakeError):
        wake.write_wake_file(tmp_path, big)
    many = tuple(
        wake.AssignedItem("IronbellyOrg/IronClaude", n, ("a",), NOW, "ok")
        for n in range(1, 12)
    )
    with pytest.raises(wake.WakeError):
        wake.write_wake_file(tmp_path, sample(assigned=many))
    fat = sample(
        assigned=tuple(
            wake.AssignedItem(
                "IronbellyOrg/IronClaude",
                n,
                tuple("a" * 39 for _ in range(10)),
                NOW,
                "ok",
            )
            for n in range(1, 11)
        ),
        plan_requests=tuple(
            wake.PlanRequestItem(
                "IronbellyOrg/IronClaude",
                n,
                "t" * 256,
                f"https://github.com/IronbellyOrg/IronClaude/issues/{n}",
                ("priority",),
                NOW,
                NOW,
            )
            for n in range(1, 11)
        ),
    )
    assert (
        len(json.dumps(wake.wake_to_json(fat))) < wake.MAX_WAKE_BYTES
    )  # the caps keep a wake small
    assert not (
        tmp_path / ".orchestrator" / "wakes"
    ).exists()  # nothing was written for a refused wake


def test_a_failed_write_is_a_wake_error_and_leaves_no_temp_file(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise OSError("disk")

    monkeypatch.setattr(os, "replace", boom)
    with pytest.raises(wake.WakeError):
        wake.write_wake_file(tmp_path, sample())
    assert [p.name for p in (tmp_path / ".orchestrator" / "wakes").iterdir()] == []


def test_the_wake_id_is_the_time_and_eight_hex_digits_and_nothing_from_github():
    made = wake.new_wake_id(NOW)
    assert made.startswith("20261119T101500Z-") and len(made) == len(WID)
    assert wake.new_wake_id(NOW, "0000000a") == "20261119T101500Z-0000000a"
    with pytest.raises(ValueError):
        wake.new_wake_id(NOW, "title: x")
    assert wake.clean_title("a\tb\nc\x1b[0m " + "x" * 400).isprintable()
    assert (
        len(wake.clean_title("x" * 400)) == wake.PLAN_TITLE_MAX
        and wake.clean_title(" \n ") == "(no title)"
    )
    assert wake.issue_url("o/r", 5) == "https://github.com/o/r/issues/5"
    with pytest.raises(ValueError):
        wake.issue_url("o/r/../x", 5)


# --- the acknowledgment (3.6) ------------------------------------------------------------------------------------------


def ack_file(tmp_path, **data):
    base = {
        "schema": "orchestrator-wake-ack/1",
        "wake_id": WID,
        "taken": [],
        "skipped": [],
        "rejected_items": [],
    }
    base.update(data)
    folder = tmp_path / ".orchestrator" / "wakes"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{WID}.ack.json").write_text(json.dumps(base))


def test_an_acknowledgment_lists_taken_skipped_and_rejected_items(tmp_path):
    assert wake.read_ack(tmp_path, WID) is None  # none yet
    ack_file(
        tmp_path,
        taken=[{"repo": "o/r", "number": 1}],
        skipped=[
            {"repo": "o/r", "number": 2, "reason": "claimed_elsewhere"},
            {"repo": "o/r", "number": 3, "reason": "Bad Text"},
        ],
        rejected_items=[{"index": 4, "reason": "malformed_item"}],
    )
    ack = wake.read_ack(tmp_path, WID)
    assert ack.taken == {("o/r", 1)} and ack.rejected_indexes == (4,)
    assert ack.skipped == {("o/r", 2): "claimed_elsewhere", ("o/r", 3): "unrecognized"}


@pytest.mark.parametrize(
    "data",
    [
        {"schema": "orchestrator-wake-ack/2"},
        {"wake_id": "20261119T101500Z-00000000"},
        {"taken": [{"repo": "bad", "number": 1}]},
        {"taken": [{"repo": "o/r", "number": "1"}]},
        {"taken": "x"},
        {"skipped": [5]},
    ],
)
def test_an_acknowledgment_the_poll_cannot_trust_reads_as_none(tmp_path, data):
    ack_file(tmp_path, **data)
    assert wake.read_ack(tmp_path, WID) is None


def test_read_ack_never_reads_a_path_built_from_a_bad_id(tmp_path):
    assert wake.read_ack(tmp_path, "../../etc/passwd") is None
    (tmp_path / ".orchestrator" / "wakes").mkdir(parents=True)
    (tmp_path / ".orchestrator" / "wakes" / f"{WID}.ack.json").write_text("{" * 10)
    assert wake.read_ack(tmp_path, WID) is None


def test_the_wake_and_its_acknowledgment_move_to_done_and_are_never_deleted(tmp_path):
    wake.write_wake_file(tmp_path, sample())
    ack_file(tmp_path)
    wake.move_to_done(tmp_path, WID)
    base = tmp_path / ".orchestrator" / "wakes"
    assert sorted(p.name for p in base.iterdir()) == ["done"]
    assert sorted(p.name for p in (base / "done").iterdir()) == [
        f"{WID}.ack.json",
        f"{WID}.json",
    ]
    wake.move_to_done(tmp_path, WID)  # nothing left: not an error
    wake.move_to_done(tmp_path, "../x")


# --- the session lookup (a port of orca_term.py) -------------------------------------------------------------------------


def fake_proc(root: Path, entries: dict[int, tuple[str, dict]]) -> Path:
    for pid, (cmd, env) in entries.items():
        d = root / str(pid)
        d.mkdir(parents=True)
        (d / "cmdline").write_bytes(cmd.encode() + b"\0--flag\0")
        (d / "environ").write_bytes(
            b"\0".join(f"{k}={v}".encode() for k, v in env.items()) + b"\0"
        )
    return root


def test_claude_processes_maps_a_terminal_handle_to_its_ccsession_tag(tmp_path):
    root = fake_proc(
        tmp_path,
        {
            101: (
                "/usr/bin/claude",
                {
                    "ORCA_TERMINAL_HANDLE": "term_a",
                    "CLAUDE_TOPIC": "orchestrator-ironclaude-1",
                },
            ),
            102: (
                "/usr/bin/vim",
                {"ORCA_TERMINAL_HANDLE": "term_b", "CLAUDE_TOPIC": "x"},
            ),  # not claude
            103: ("/usr/bin/claude", {"CLAUDE_TOPIC": "y"}),  # no terminal handle
            104: ("/usr/bin/claude", {"ORCA_TERMINAL_HANDLE": "term_c"}),  # no topic
        },
    )
    (root / "notapid").mkdir()
    (root / "105").mkdir()  # a process with nothing readable
    assert wake.claude_processes(root) == {
        "term_a": "orchestrator-ironclaude-1",
        "term_c": "",
    }
    assert wake.claude_processes(tmp_path / "missing") == {}


# --- the delivery -------------------------------------------------------------------------------------------------------------


def terminals(*items):
    return result(
        stdout=json.dumps(
            {"ok": True, "result": {"truncated": False, "terminals": list(items)}}
        )
    )


def live_terminal(handle="term_live-0001", last_output_ms=None):
    t = {"handle": handle, "connected": True, "worktreePath": str(WORKSPACE)}
    if last_output_ms is not None:
        t["lastOutputAt"] = last_output_ms
    return t


LIST = (ORCA, "terminal", "list", "--worktree", f"path:{WORKSPACE}", "--json")
TAG = "orchestrator-ironclaude-1"
LINE = f"/sc:orchestrator --wake {WID}"


def mail_argv(run_id="run_1"):
    payload = json.dumps(
        {"kind": "orchestrator-wake", "wake_id": WID}, separators=(",", ":")
    )
    return (ORCA, "orchestration", "send", "--to", f"run:{run_id}", "--type", "status",
            "--subject", f"orchestrator-wake {WID}", "--payload", payload, "--json")  # fmt: skip


def screen_argv(handle="term_live-0001"):
    return (ORCA, "terminal", "read", "--terminal", handle, "--screen", "--json")


def wait_argv(handle="term_live-0001", ms=4000):
    return (
        ORCA,
        "terminal",
        "wait",
        "--terminal",
        handle,
        "--for",
        "tui-idle",
        "--timeout-ms",
        str(ms),
        "--json",
    )


def send_argv(handle="term_live-0001"):
    return (
        ORCA,
        "terminal",
        "send",
        "--terminal",
        handle,
        "--text",
        LINE,
        "--enter",
        "--wait-submit",
        "15",
        "--json",
    )


def ok(payload):
    return result(stdout=json.dumps(payload))


def waker_for(fake_runner, tmp_path, script, *, live_tag=TAG, launcher=None):
    root = fake_proc(
        tmp_path / "proc",
        {
            101: (
                "/usr/bin/claude",
                {"ORCA_TERMINAL_HANDLE": "term_live-0001", "CLAUDE_TOPIC": live_tag},
            )
        },
    )
    runner = fake_runner(script)
    return wake.Waker(runner, launcher, proc_root=root), runner


def target(run_id="run_1", tier="tier1b"):
    return wake.WakeTargetRun("ironclaude-1", TAG, WORKSPACE, run_id, tier)


def idle_script(last_output_ms=None, draft="", **extra):
    script = {
        LIST: terminals(live_terminal(last_output_ms=last_output_ms)),
        screen_argv(): ok(
            {"ok": True, "result": {"terminal": {"tail": ["$ "]}, "draft": draft}}
        ),
        wait_argv(): ok(load_fixture("orca_terminal_wait_idle.json")["payload"]),
        mail_argv(): ok({"ok": True, "result": {}}),
        send_argv(): ok(load_fixture("orca_terminal_send_receipt.json")["payload"]),
    }
    script.update(extra)
    return script


def test_an_idle_session_gets_the_mailbox_message_and_the_typed_line_with_receipt_stages(
    fake_runner, tmp_path
):
    waker, runner = waker_for(fake_runner, tmp_path, idle_script())
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert (out.kind, out.mailbox, out.typed, out.stages) == (
        "woken",
        "sent",
        True,
        ("input_accepted", "turn_started"),
    )
    assert out.started is False
    order = runner.argvs()
    assert (
        order.index(mail_argv()) < order.index(LIST) < order.index(send_argv())
    )  # mailbox, lookup, line
    typed = send_argv()[send_argv().index("--text") + 1]
    assert typed == LINE  # the wake id and nothing else


def test_a_session_with_output_in_the_last_60_seconds_gets_the_mailbox_message_alone(
    fake_runner, tmp_path
):
    recent = int((NOW - timedelta(seconds=30)).timestamp() * 1000)
    waker, runner = waker_for(fake_runner, tmp_path, idle_script(last_output_ms=recent))
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert (out.kind, out.mailbox, out.typed, out.detail) == (
        "woken",
        "sent",
        False,
        "fresh_output",
    )
    assert send_argv() not in runner.argvs()
    older = int((NOW - timedelta(seconds=61)).timestamp() * 1000)
    waker, runner = waker_for(
        fake_runner, tmp_path / "b", idle_script(last_output_ms=older)
    )
    assert waker.deliver(ORCA, target(), WID, NOW, 30).typed is True


def test_a_draft_on_the_screen_means_someone_is_typing_and_nothing_is_typed(
    fake_runner, tmp_path
):
    waker, runner = waker_for(
        fake_runner, tmp_path, idle_script(draft="half a sentence")
    )
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert (out.kind, out.typed, out.detail) == (
        "woken",
        False,
        "typing",
    ) and send_argv() not in runner.argvs()


@pytest.mark.parametrize("draft", [None, 5, ["x"]])
def test_a_screen_read_with_no_text_draft_field_is_not_an_empty_draft(
    fake_runner, tmp_path, draft
):
    script = idle_script()
    script[screen_argv()] = ok(
        {"ok": True, "result": {"terminal": {"tail": ["$ "]}, "draft": draft}}
    )
    waker, runner = waker_for(fake_runner, tmp_path, script)
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert (out.kind, out.typed, out.detail) == (
        "woken",
        False,
        "screen_unreadable",
    ) and send_argv() not in runner.argvs()
    missing = idle_script()
    missing[screen_argv()] = ok({"ok": True, "result": {"terminal": {"tail": ["$ "]}}})
    waker, runner = waker_for(fake_runner, tmp_path / "b", missing)
    assert waker.deliver(ORCA, target(), WID, NOW, 30).typed is False


def test_a_busy_session_is_not_typed_to(fake_runner, tmp_path):
    script = idle_script()
    script[wait_argv()] = ok({"ok": True, "result": {"satisfied": False}})
    waker, runner = waker_for(fake_runner, tmp_path, script)
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert (out.kind, out.typed, out.detail) == ("woken", False, "busy")
    script[wait_argv()] = result(timed_out=True)  # a timeout counts as not idle
    assert (
        waker_for(fake_runner, tmp_path / "b", script)[0]
        .deliver(ORCA, target(), WID, NOW, 30)
        .typed
        is False
    )


def test_a_failed_mailbox_falls_back_to_the_typed_line_alone_and_is_recorded(
    fake_runner, tmp_path
):
    script = idle_script()
    script[mail_argv()] = result(returncode=1, stderr="error: sender in no Run")
    waker, _ = waker_for(fake_runner, tmp_path, script)
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert (out.kind, out.mailbox, out.typed) == ("woken", "unavailable", True)
    script[send_argv()] = result(returncode=1)
    out = waker_for(fake_runner, tmp_path / "b", script)[0].deliver(
        ORCA, target(), WID, NOW, 30
    )
    assert (out.kind, out.mailbox, out.typed) == (
        "unknown",
        "unavailable",
        False,
    )  # resent after 10 minutes


def test_a_new_orchestrator_has_no_run_yet_so_no_mailbox_message_is_sent_or_missed(
    fake_runner, tmp_path
):
    waker, runner = waker_for(fake_runner, tmp_path, idle_script())
    out = waker.deliver(ORCA, target(run_id=None), WID, NOW, 30)
    assert (out.mailbox, out.kind) == ("skipped", "woken")
    assert not [a for a in runner.argvs() if a[1:3] == ("orchestration", "send")]


def test_the_session_is_found_by_its_running_process_and_tag_never_by_title(
    fake_runner, tmp_path
):
    other = terminals(
        {
            **live_terminal("term_live-0001"),
            "title": "orchestrator-ironclaude-1 · Claude Code",
        },
        live_terminal("term_other"),
    )
    script = idle_script()
    script[LIST] = other
    waker, _ = waker_for(
        fake_runner, tmp_path, script, live_tag="coordinator"
    )  # the process runs ANOTHER tag
    assert (
        waker.find_session(ORCA, WORKSPACE, TAG, 30) == []
    )  # a stale title proves nothing
    waker, _ = waker_for(fake_runner, tmp_path / "b", script)
    (found,) = waker.find_session(ORCA, WORKSPACE, TAG, 30)
    assert found["handle"] == "term_live-0001"


def test_the_newest_session_of_a_tag_is_the_one_used(fake_runner, tmp_path):
    root = fake_proc(
        tmp_path / "proc",
        {
            1: (
                "/usr/bin/claude",
                {"ORCA_TERMINAL_HANDLE": "term_old", "CLAUDE_TOPIC": TAG},
            ),
            2: (
                "/usr/bin/claude",
                {"ORCA_TERMINAL_HANDLE": "term_new", "CLAUDE_TOPIC": TAG},
            ),
        },
    )
    runner = fake_runner(
        {
            LIST: terminals(
                live_terminal("term_old", 1000), live_terminal("term_new", 9000)
            )
        }
    )
    found = wake.Waker(runner, proc_root=root).find_session(ORCA, WORKSPACE, TAG, 30)
    assert [t["handle"] for t in found] == ["term_new", "term_old"]


@pytest.mark.parametrize(
    "reply",
    [
        result(
            stdout=json.dumps(
                {"ok": True, "result": {"truncated": True, "terminals": []}}
            )
        ),
        result(returncode=1),
        result(timed_out=True),
        result(stdout="not json"),
        result(stdout=json.dumps({"ok": False})),
        result(stdout=json.dumps({"ok": True, "result": {"terminals": "x"}})),
    ],
)
def test_an_unreadable_or_cut_terminal_list_never_starts_a_second_session(
    fake_runner, tmp_path, reply
):
    started = []

    class Never:
        def start(self, *a, **k):
            started.append(a)
            raise AssertionError("must not start")

    waker, _ = waker_for(
        fake_runner, tmp_path, {LIST: reply, mail_argv(): ok({})}, launcher=Never()
    )
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert out.kind == "unknown" and out.detail == "terminal_list" and started == []


class FakeLauncher:
    def __init__(self, outcome):
        self.outcome, self.calls = outcome, []

    def start(self, orca, workspace, tag, tier, timeout):
        self.calls.append((orca, workspace, tag, tier, timeout))
        return self.outcome


def no_session_script(tiers):
    from .conftest import TIERS_TEXT

    return {
        LIST: terminals(),
        ("ccsession", "--help"): result(
            stdout=tiers if tiers is not None else TIERS_TEXT
        ),
        mail_argv(): ok({}),
        wait_argv("term_new-0001", 90000): ok(
            {"ok": True, "result": {"satisfied": True}}
        ),
        send_argv("term_new-0001"): ok(
            load_fixture("orca_terminal_send_receipt.json")["payload"]
        ),
    }


def test_a_missing_session_is_started_with_the_orchestrator_tier_and_then_typed_to(
    fake_runner, tmp_path
):
    launcher = FakeLauncher(LaunchOutcome("ready", "term_new-0001", "ok"))
    waker, runner = waker_for(
        fake_runner,
        tmp_path,
        no_session_script(None),
        live_tag="other",
        launcher=launcher,
    )
    out = waker.deliver(ORCA, target(tier="tier1b"), WID, NOW, 30)
    assert launcher.calls == [(ORCA, WORKSPACE, TAG, "tier1b", 30)]
    assert (out.kind, out.started, out.tier, out.fallback_from, out.typed) == (
        "woken",
        True,
        "tier1b",
        None,
        True,
    )
    assert send_argv("term_new-0001") in runner.argvs()


def test_a_tier_the_user_may_not_use_falls_once_and_the_fallback_is_reported(
    fake_runner, tmp_path
):
    member = "Tiers in this workspace:\n    ccsession --tier tier2\n    ccsession --tier tier3\n"
    launcher = FakeLauncher(LaunchOutcome("ready", "term_new-0001", "ok"))
    waker, _ = waker_for(
        fake_runner,
        tmp_path,
        no_session_script(member),
        live_tag="other",
        launcher=launcher,
    )
    out = waker.deliver(ORCA, target(tier="tier1b"), WID, NOW, 30)
    assert (launcher.calls[0][3], out.tier, out.fallback_from) == (
        "tier2",
        "tier2",
        "tier1b",
    )


@pytest.mark.parametrize(
    ("tiers", "tier", "detail"),
    [
        (
            "Tiers in this workspace:\n    ccsession --tier tier2\n",
            "tier4",
            "no_tier",
        ),  # none left after it
        ("no tiers at all", "tier1b", "tiers_unreadable"),
    ],
)
def test_no_listed_tier_or_an_unreadable_list_is_no_session_and_starts_nothing(
    fake_runner, tmp_path, tiers, tier, detail
):
    launcher = FakeLauncher(LaunchOutcome("ready", "term_new-0001", "ok"))
    waker, _ = waker_for(
        fake_runner,
        tmp_path,
        no_session_script(tiers),
        live_tag="other",
        launcher=launcher,
    )
    out = waker.deliver(ORCA, target(tier=tier), WID, NOW, 30)
    assert (out.kind, out.detail) == ("no_session", detail) and launcher.calls == []


@pytest.mark.parametrize(
    ("launched", "kind"),
    [
        (LaunchOutcome("unknown", None, "timeout"), "no_session"),
        (LaunchOutcome("unknown", "term_new-0001", "not_started"), "no_session"),
        (LaunchOutcome("spawn_error", None, "spawn_error"), "spawn_error"),
    ],
)
def test_a_session_that_did_not_start_is_no_session_or_spawn_error(
    fake_runner, tmp_path, launched, kind
):
    waker, _ = waker_for(
        fake_runner,
        tmp_path,
        no_session_script(None),
        live_tag="other",
        launcher=FakeLauncher(launched),
    )
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert out.kind == kind and out.tier == "tier1b" and out.typed is False


def test_a_new_session_that_is_still_loading_is_unknown_and_found_live_next_time(
    fake_runner, tmp_path
):
    script = no_session_script(None)
    script[wait_argv("term_new-0001", 90000)] = ok(
        {"ok": True, "result": {"satisfied": False}}
    )
    launcher = FakeLauncher(LaunchOutcome("ready", "term_new-0001", "ok"))
    waker, runner = waker_for(
        fake_runner, tmp_path, script, live_tag="other", launcher=launcher
    )
    out = waker.deliver(ORCA, target(), WID, NOW, 30)
    assert (out.kind, out.detail, out.started) == ("unknown", "starting", True)
    assert send_argv("term_new-0001") not in runner.argvs()


def test_an_information_only_wake_never_starts_a_session(fake_runner, tmp_path):
    launcher = FakeLauncher(LaunchOutcome("ready", "term_new-0001", "ok"))
    waker, _ = waker_for(
        fake_runner,
        tmp_path,
        no_session_script(None),
        live_tag="other",
        launcher=launcher,
    )
    out = waker.deliver(ORCA, target(), WID, NOW, 30, start_session=False)
    assert (out.kind, out.detail) == (
        "no_session",
        "not_started",
    ) and launcher.calls == []


def test_unread_mark_uses_a_fixed_note_and_refuses_free_text(fake_runner, tmp_path):
    argv = (
        ORCA,
        "worktree",
        "set",
        "--worktree",
        f"path:{WORKSPACE}",
        "--unread",
        "--comment",
        "issue-watch: ack_not_observed",
        "--json",
    )
    waker, runner = waker_for(fake_runner, tmp_path, {argv: ok({"ok": True})})
    assert waker.mark_unread(ORCA, WORKSPACE, "ack_not_observed", 10) is True
    with pytest.raises(ValueError):
        waker.mark_unread(ORCA, WORKSPACE, "Title of an issue", 10)
    failing, _ = waker_for(fake_runner, tmp_path / "b", {argv: result(returncode=1)})
    assert failing.mark_unread(ORCA, WORKSPACE, "ack_not_observed", 10) is False


def test_deliver_refuses_a_wake_id_that_is_not_one(fake_runner, tmp_path):
    waker, runner = waker_for(fake_runner, tmp_path, {})
    with pytest.raises(ValueError):
        waker.deliver(ORCA, target(), "x; rm -rf /", NOW, 30)
    assert runner.calls == []


def test_only_known_receipt_stages_are_kept(fake_runner, tmp_path):
    script = idle_script()
    script[send_argv()] = ok(
        {
            "ok": True,
            "result": {
                "accepted": True,
                "stages": ["input_accepted", "secret_stage", 5],
            },
        }
    )
    out = waker_for(fake_runner, tmp_path, script)[0].deliver(
        ORCA, target(), WID, NOW, 30
    )
    assert out.stages == ("input_accepted",)
