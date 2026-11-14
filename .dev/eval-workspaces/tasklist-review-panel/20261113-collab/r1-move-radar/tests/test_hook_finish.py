"""T-6: the finish signal (R-41)."""

from conftest import CAT, ctx_text


def test_finish_once_and_nothing_after(board):
    for _ in range(4):
        board.call("t2b-1", "searcher")
    board.set_clock(2000)
    outs = [board.call("t2b-1", "searcher", finish=2000) for _ in range(10)]  # calls 5..14 include checkpoints 6 and 10
    assert ctx_text(outs[0]) == CAT["finish_text"]
    assert all(o == "" for o in outs[1:])
    assert len(board.events("t2b-1", "finish")) == 1
    assert board.events("t2b-1", "inject") == []
