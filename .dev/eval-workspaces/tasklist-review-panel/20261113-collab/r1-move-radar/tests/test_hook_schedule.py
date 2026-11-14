"""T-5: checkpoint schedule, source.md check, peer coverage, guard, output shape and text."""

import json

from conftest import ctx_text, expected_text


def drive(board, rid, role, calls, **kw):
    outs = {}
    for i in range(1, calls + 1):
        o = board.call(rid, role, **kw)
        if o:
            outs[i] = o
    return outs


def read_src(board, rid, role, **kw):
    return board.call(rid, role, tool="Read", inp={"file_path": board.src}, **kw)


def test_searcher_k2_injects_at_6_and_10_only(board):
    outs = drive(board, "t2b-1", "searcher", 14)
    assert sorted(outs) == [6, 10]
    assert ctx_text(outs[6]) == expected_text(None, "searcher")  # no SRC_OPENED -> the source.md check first
    assert ctx_text(outs[10]) == expected_text("M2", "searcher")  # first of the order, with the suffix
    inj = board.events("t2b-1", "inject")
    assert len(inj) == 2 and inj[0]["slot_type"] == "src" and inj[0]["move"] is None
    assert inj[1]["slot_type"] == "search" and inj[1]["move"] == "M2"


def test_searcher_k1_injects_at_6_only(board):
    assert sorted(drive(board, "t2b-1", "searcher", 14, k=1)) == [6]


def test_reader_injects_at_8_and_12_without_suffix(board):
    read_src(board, "t4-1", "reader")
    outs = drive(board, "t4-1", "reader", 13)
    assert sorted(outs) == [7, 11]  # one call was the Read, so the counted calls 8 and 12 are loop steps 7 and 11
    assert ctx_text(outs[7]) == expected_text("M3", "reader")
    assert ctx_text(outs[11]) == expected_text("M5", "reader")
    assert all("No panel member" not in ctx_text(o) for o in outs.values())
    assert [e["slot_type"] for e in board.events("t4-1", "inject")] == ["static", "static"]


def test_source_check_not_sent_when_opened(board):
    read_src(board, "t2b-1", "searcher")
    outs = drive(board, "t2b-1", "searcher", 9)
    assert ctx_text(outs[5]) == expected_text("M2", "searcher")


def test_peer_coverage_skips_move(board):
    board.tele("t4-1", json.dumps({"n": 1, "t": 0, "rid": "t4-1", "sub": False, "tool": "Bash", "input": {"command": "grep -c x src/"}}))
    read_src(board, "t2b-1", "searcher")
    outs = drive(board, "t2b-1", "searcher", 5)
    assert ctx_text(outs[5]) == expected_text("M7", "searcher")  # M2 covered by a peer -> next uncovered


def test_all_covered_is_no_gap(board):
    for c in ("grep -c x src/", "grep -rn x .", "grep -n HOW-WE-WORK docs/guide.md", "grep -rn merge_guard tests/"):
        board.tele("t3-1", json.dumps({"n": 1, "t": 0, "rid": "t3-1", "sub": False, "tool": "Bash", "input": {"command": c}}))
    read_src(board, "t2b-1", "searcher")
    outs = drive(board, "t2b-1", "searcher", 9)
    assert outs == {}
    assert [e["reason"] for e in board.events("t2b-1", "skip")] == ["no_gap", "no_gap"]
    assert board.events("t2b-1", "inject") == []


def test_no_injection_at_or_after_guard(board):
    board.set_clock(5000)
    outs = drive(board, "t2b-1", "searcher", 12, guard=5000)
    assert outs == {} and [e["reason"] for e in board.events("t2b-1", "skip")] == ["guard", "guard"]


def test_at_most_k_injections(board):
    drive(board, "t2b-1", "searcher", 30)
    assert len(board.events("t2b-1", "inject")) == 2
