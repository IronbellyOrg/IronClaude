"""T-7: seal before the first delivery; fail closed on an unreadable transcript (R-10)."""

import hashlib

from conftest import ctx_text


def test_seal_written_before_inject(board):
    for i in range(6):
        out = board.call("t2b-1", "searcher")
    assert ctx_text(out)
    snap = board.dir / "snap" / "t2b-1.jsonl"
    assert snap.read_bytes() == board.transcript.read_bytes()
    sha = hashlib.sha256(snap.read_bytes()).hexdigest()
    assert (board.dir / "snap" / "t2b-1.sha256").read_text().split()[0] == sha
    evs = [m["ev"] for m in board.metrics("t2b-1") if m["ev"] in ("seal", "inject")]
    assert evs == ["seal", "inject"]
    assert board.events("t2b-1", "seal")[0]["sha256"] == sha


def test_unreadable_transcript_fails_closed(board, tmp_path):
    outs = [board.call("t2b-1", "searcher", transcript=tmp_path / "missing.jsonl") for _ in range(12)]
    assert all(o == "" for o in outs)  # nothing at checkpoint 6 nor at 10
    assert len(board.events("t2b-1", "snapshot_missing")) == 1
    assert board.events("t2b-1", "inject") == []
    assert (board.dir / "state" / "t2b-1.sealed").read_text().strip() == "failed"
