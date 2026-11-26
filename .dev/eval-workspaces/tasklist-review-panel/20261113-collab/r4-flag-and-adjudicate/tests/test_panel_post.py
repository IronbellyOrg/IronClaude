"""bin/panel-post (design 2.2; R-34, R-35, R-41)."""

import json
import subprocess

from r4help import R4, first_card_anchor, jsonl, make_board, now_ms, post


def lines(board):
    return [json.loads(x) for x in (board / "msgs" / "t2b-1.jsonl").read_text().splitlines()]


def last_reason(board):
    return [e for e in jsonl(board / "metrics" / "t2b-1.jsonl") if e["ev"] == "post_rejected"][-1]["reason"]


def test_too_early_then_accepted(tmp_path):
    board, cf = make_board(tmp_path)
    r = post(board, cf, anchor=first_card_anchor(), calls=1)
    assert r.returncode == 1 and "refused: too_early" in r.stderr and last_reason(board) == "too_early"
    r = post(board, cf, anchor=first_card_anchor(), calls=2)
    assert r.returncode == 0 and r.stdout.strip() == "card c0 posted"
    acc = [e for e in jsonl(board / "metrics" / "t2b-1.jsonl") if e["ev"] == "post_accepted"]
    assert acc and acc[0]["id"] == "c0"


def test_after_finish(tmp_path):
    board, cf = make_board(tmp_path)
    r = post(board, cf, anchor=first_card_anchor(), fin=now_ms())
    assert r.returncode == 1 and "refused: after_finish" in r.stderr and last_reason(board) == "after_finish"


def test_whitespace_variant_accepted_and_flattened(tmp_path):
    board, cf = make_board(tmp_path)
    a = first_card_anchor()
    messy = a.replace(" ", "  \n ", 3)
    r = post(board, cf, anchor=messy)
    assert r.returncode == 0, r.stderr
    assert lines(board)[0]["anchor"] == a


def test_not_in_candidate(tmp_path):
    board, cf = make_board(tmp_path)
    r = post(board, cf, anchor="this sentence is certainly not in the candidate text")
    assert r.returncode == 1 and "refused: anchor_not_in_candidate" in r.stderr


def test_bad_args_and_enums(tmp_path):
    board, cf = make_board(tmp_path)
    a = first_card_anchor()
    cases = {
        "bad_args": ["--anchor", a, "--move", "M3", "--category", "other"],
        "bad_move": ["--anchor", a, "--move", "M1", "--category", "other", "--severity", "MAJOR"],
        "bad_category": ["--anchor", a, "--move", "M3", "--category", "nope", "--severity", "MAJOR"],
        "bad_severity": ["--anchor", a, "--move", "M3", "--category", "other", "--severity", "LOW"],
        "bad_anchor_length": ["--anchor", "short", "--move", "M3", "--category", "other", "--severity", "MAJOR"],
    }
    for reason, extra in cases.items():
        r = post(board, cf, anchor=a, extra=extra)
        assert r.returncode == 1 and f"refused: {reason}" in r.stderr, (reason, r.stderr)
    r = post(board, cf, anchor=a, extra=["--anchor", a, "--anchor", a, "--move", "M3", "--category", "other", "--severity", "MAJOR"])
    assert "refused: bad_args" in r.stderr


def test_deal_r0_and_r1(tmp_path):
    for r_coin, expect in ((0, ["t4-1", "t3-1", "t4-1", "t3-1"]), (1, ["t3-1", "t4-1", "t3-1", "t4-1"])):
        board, cf = make_board(tmp_path / f"r{r_coin}")
        for n in range(4):
            assert post(board, cf, anchor=first_card_anchor(n=n), r=r_coin).returncode == 0
        got = lines(board)
        assert [c["to"] for c in got] == expect
        assert [c["id"] for c in got] == ["c0", "c1", "c2", "c3"]


def test_concurrent_posts(tmp_path):
    board, cf = make_board(tmp_path)
    (board / "state" / "t2b-1.calls").write_text("5\n")
    procs = []
    for n in range(8):
        args = [str(R4 / "bin" / "panel-post"), "--board", str(board), "--rid", "t2b-1", "--run", "row/pkg", "--cand-flat", str(cf),
                "--cap", "8", "--t0-ms", str(now_ms()), "--finish-ms", str(now_ms() + 3_600_000), "--r", "0", "--peers", "t4-1,t3-1",
                "--anchor", first_card_anchor(n=n), "--move", "M3", "--category", "other", "--severity", "MAJOR"]
        procs.append(subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    assert all(p.wait() == 0 for p in procs)
    got = lines(board)
    assert sorted(c["id"] for c in got) == [f"c{i}" for i in range(8)]
    assert len(got) == 8
