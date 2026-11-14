"""T-8: the hook never breaks a review (R-22)."""

import os

from conftest import ctx_text


def test_corrupt_peer_line(board):
    board.tele("t4-1", '{"n":1,"tool":"Bash","inp')
    outs = [board.call("t2b-1", "searcher") for _ in range(6)]
    assert ctx_text(outs[5])


def test_non_object_json_lines_skipped(board):
    # lines that parse but are not objects, last in the peer file and in the metrics file
    for junk in ("[1]", "42", '"x"', '{"n":1,"tool":"Bash","input":"not an object"}'):
        board.tele("t4-1", junk)
    outs = [board.call("t2b-1", "searcher") for _ in range(10)]
    with (board.dir / "metrics" / "t2b-1.jsonl").open("a") as f:
        f.write("[1]\n")
    board.call("t2b-1", "searcher")
    assert ctx_text(outs[5]) and ctx_text(outs[9])
    assert not [m for m in board.metrics_safe("t2b-1") if m.get("ev") == "hook_error"]
    assert len([m for m in board.metrics_safe("t2b-1") if m.get("ev") == "inject"]) == 2


def test_unwritable_msgs(board):
    (board.dir / "msgs").mkdir()
    os.chmod(board.dir / "msgs", 0o500)
    try:
        outs = [board.call("t2b-1", "searcher") for _ in range(6)]
    finally:
        os.chmod(board.dir / "msgs", 0o700)
    assert all(o == "" for o in outs)
    assert len(board.events("t2b-1", "hook_error")) == 1


def test_stdin_not_json(board):
    assert board.call("t2b-1", "searcher", raw_stdin="not json at all") == ""
    assert len(board.events("t2b-1", "hook_error")) == 1


def test_timing_event_on_every_exit(board):
    for _ in range(3):
        board.call("t2b-1", "searcher")
    ts = board.events("t2b-1", "t")
    assert len(ts) == 3 and all(isinstance(t["ms"], int) for t in ts)


def test_subagent_calls_logged_not_counted(board):
    for _ in range(6):
        board.call("t2b-1", "searcher", agent_id="agent-1")
    assert not (board.dir / "state" / "t2b-1.count").exists()
    assert board.events("t2b-1", "inject") == []
