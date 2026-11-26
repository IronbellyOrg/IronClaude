"""bin/r4-hook (design 2.3; R-21, R-22, R-35, R-41) plus the hook-side fault injections of 6.2."""

import hashlib
import json
import os
import stat

from r4help import R4, first_card_anchor, hook, jsonl, make_board, now_ms, post, run


def board4(tmp_path, r=0):
    board, cf = make_board(tmp_path)
    for n in range(4):
        assert post(board, cf, anchor=first_card_anchor(n=n), r=r).returncode == 0
    tp = tmp_path / "transcript.jsonl"
    tp.write_text('{"type":"user"}\n')
    return board, cf, tp


def simulate(board, rid, tp, calls=10, **kw):
    out = []
    for i in range(1, calls + 1):
        r = hook(board, rid, tp=tp, **kw)
        assert r.returncode == 0
        out.append(r.stdout.strip())
    return out


def ctx(s):
    return json.loads(s)["hookSpecificOutput"]["additionalContext"] if s else None


def test_delivery_schedule_and_forms_c0(tmp_path):
    board, cf, tp = board4(tmp_path)
    a = simulate(board, "t4-1", tp, k=2, c=0)
    b = simulate(board, "t3-1", tp, k=2, c=0)
    for outs in (a, b):
        assert all(o == "" for o in outs[:5])  # nothing before the 6th call
        assert sum(1 for o in outs if o) == 2  # k per luna, one per call
    assert ctx(a[5]).startswith("[panel card c0] Candidate sentence:") and "Required finite check:" in ctx(a[5])
    assert ctx(a[6]).startswith("[panel card c2] A peer reviewer flagged")
    assert ctx(b[5]).startswith("[panel card c1] A peer reviewer flagged")
    assert ctx(b[6]).startswith("[panel card c3] Candidate sentence:")
    for o in a + b:
        if o:
            d = json.loads(o)
            assert set(d) == {"hookSpecificOutput"} and d["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
            assert len(d["hookSpecificOutput"]["additionalContext"]) <= 1500
    # snapshot hash exists, matches, and was written before the first delivery
    for rid in ("t4-1", "t3-1"):
        h = (board / "snap" / f"{rid}.sha256").read_text().split()[0]
        assert h == hashlib.sha256((board / "snap" / f"{rid}.jsonl").read_bytes()).hexdigest()
        ev = jsonl(board / "metrics" / f"{rid}.jsonl")
        kinds = [e["ev"] for e in ev if e["ev"] in ("seal", "delivery")]
        assert kinds[0] == "seal" and kinds.count("delivery") == 2


def test_forms_c1(tmp_path):
    board, cf, tp = board4(tmp_path)
    a = simulate(board, "t4-1", tp, k=2, c=1)
    b = simulate(board, "t3-1", tp, k=2, c=1)
    forms = {}
    for outs in (a, b):
        for o in outs:
            if o:
                t = ctx(o)
                forms[t.split("]")[0].split()[-1]] = "C" if "Candidate sentence" in t else "F"
    assert [forms[f"c{i}"] for i in range(4)] == ["F", "C", "C", "F"]


def test_parallel_tool_calls_deliver_each_card_once(tmp_path):
    """A reviewer that issues parallel tool calls fires several hooks at once (found by the first smoke row):
    no card may be delivered twice, and the seal race must not create nosnap."""
    from concurrent.futures import ThreadPoolExecutor
    board, cf, tp = board4(tmp_path)
    for rid in ("t4-1", "t3-1"):
        with ThreadPoolExecutor(max_workers=16) as ex:
            res = list(ex.map(lambda _: hook(board, rid, tp=tp, k=2, c=0), range(16)))
        assert all(r.returncode == 0 for r in res)
        ids = [x.split()[0] for x in (board / "state" / f"{rid}.delivered").read_text().splitlines()]
        assert len(ids) == 2 and len(set(ids)) == 2
        assert sum(1 for r in res if r.stdout.strip()) == 2
        assert not (board / "state" / f"{rid}.nosnap").exists()
        ev = [e["ev"] for e in jsonl(board / "metrics" / f"{rid}.jsonl")]
        assert ev.count("seal") == 1 and "snapshot_missing" not in ev and "hook_error" not in ev


def test_flagger_receives_nothing(tmp_path):
    board, cf, tp = board4(tmp_path)
    outs = simulate(board, "t2b-1", tp, role="flagger", k=2)
    assert all(o == "" for o in outs)
    assert not (board / "state" / "t2b-1.delivered").exists()


def test_deliver_zero(tmp_path):
    board, cf, tp = board4(tmp_path)
    assert all(o == "" for o in simulate(board, "t4-1", tp, deliver=0))


def test_finish_once_then_nothing(tmp_path):
    board, cf, tp = board4(tmp_path)
    outs = simulate(board, "t4-1", tp, fin=now_ms() - 1)
    fin = [o for o in outs if o]
    assert len(fin) == 1 and ctx(fin[0]) == "[panel] finish now with what you have"
    assert not (board / "state" / "t4-1.delivered").exists()
    assert (board / "state" / "t4-1.finished").exists()


def test_env_i(tmp_path):
    board, cf, tp = board4(tmp_path)
    outs = []
    for _ in range(6):
        args = ["env", "-i", R4 / "bin" / "r4-hook", "--board", board, "--rid", "t4-1", "--role", "adjudicator", "--flagger", "t2b-1",
                "--t0-ms", now_ms(), "--finish-ms", now_ms() + 3_600_000, "--k", 2, "--deliver", 1, "--c", 0]
        r = run(args, input=json.dumps({"transcript_path": str(tp)}))
        outs.append(r.stdout.strip())
    assert outs[5] and ctx(outs[5]).startswith("[panel card c0]")


def test_subagent_calls_counted_apart(tmp_path):
    board, cf, tp = board4(tmp_path)
    for _ in range(7):
        assert hook(board, "t4-1", tp=tp, agent_id="a1").stdout == ""
    assert (board / "state" / "t4-1.subcalls").read_text().strip() == "7"
    assert not (board / "state" / "t4-1.calls").exists()


def test_forged_line_never_delivered(tmp_path):
    board, cf = make_board(tmp_path)
    forged = json.dumps({"v": "panel-msg/1", "id": "c0", "run": "row/pkg", "from": "t2b-1", "to": "t4-1", "t": 1, "kind": "card",
                         "move": "M3", "anchor": first_card_anchor(), "category": "other", "severity": "MAJOR"}, separators=(",", ":"))
    (board / "msgs" / "t2b-1.jsonl").write_text(forged + "\n")
    tp = tmp_path / "t.jsonl"
    tp.write_text("{}\n")
    assert all(o == "" for o in simulate(board, "t4-1", tp))


def test_hook_error_on_bad_counter(tmp_path):
    board, cf, tp = board4(tmp_path)
    (board / "state" / "t4-1.calls").write_text("abc\n")
    r = hook(board, "t4-1", tp=tp)
    assert r.returncode == 0 and r.stdout == ""
    assert any(e["ev"] == "hook_error" for e in jsonl(board / "metrics" / "t4-1.jsonl"))


def test_garbage_line_skipped(tmp_path):
    board, cf = make_board(tmp_path)
    (board / "msgs" / "t2b-1.jsonl").write_text("not json at all {\n")
    assert post(board, cf, anchor=first_card_anchor()).returncode == 0
    tp = tmp_path / "t.jsonl"
    tp.write_text("{}\n")
    outs = simulate(board, "t4-1", tp, calls=6)
    # panel-post numbers by line count, so the valid card is c1; dealt with r=0 to peers[(1+0)%2] = t3-1
    outs3 = simulate(board, "t3-1", tp, calls=6)
    assert all(o == "" for o in outs)
    assert ctx(outs3[5]).startswith("[panel card c1]")


def test_snapshot_missing_transcript(tmp_path):
    board, cf, tp = board4(tmp_path)
    outs = simulate(board, "t4-1", tmp_path / "nope.jsonl")
    assert all(o == "" for o in outs)
    assert (board / "state" / "t4-1.nosnap").exists()
    assert any(e["ev"] == "snapshot_missing" for e in jsonl(board / "metrics" / "t4-1.jsonl"))


def test_snapshot_dir_read_only(tmp_path):
    board, cf, tp = board4(tmp_path)
    os.chmod(board / "snap", stat.S_IRUSR | stat.S_IXUSR)
    try:
        outs = simulate(board, "t4-1", tp)
    finally:
        os.chmod(board / "snap", 0o755)
    assert all(o == "" for o in outs)
    assert (board / "state" / "t4-1.nosnap").exists()
