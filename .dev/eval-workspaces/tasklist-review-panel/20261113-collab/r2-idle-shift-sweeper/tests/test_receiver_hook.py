"""hooks/receiver-hook.sh (R-19, R-20, R-21, R-41): DESIGN 6.1 cases."""
import concurrent.futures as cf
import hashlib
import json
import time

from conftest import CAND_A

UNNAMED = {"items": ["tests/test_other.py"]}
ROOT = {"items": ["CHANGELOG.md"], "move": "M7", "cmd": "grep -rn greeting ."}
OTHER = {"items": ["src/other.py"], "move": "M2", "cmd": "grep -rl greet src"}


def calls(w, s, n, **kw):
    return [w.call_hook(s, **kw) for _ in range(n)]


def delivered(w, rid="t4-1"):
    p = w.B / f"state/{rid}.delivered"
    return p.read_text().split() if p.exists() else []


def test_no_delivery_on_calls_1_to_5(world):
    world.board()
    world.seed(UNNAMED)
    s = world.hook_settings()
    assert calls(world, s, 5) == [""] * 5
    out = world.call_hook(s)
    assert json.loads(out)["hookSpecificOutput"]["hookEventName"] == "PostToolUse"


def test_no_seal_without_fact(world):
    world.board()
    s = world.hook_settings()
    calls(world, s, 8)
    assert not (world.B / "state/t4-1.sealed").exists() and not (world.B / "snap/t4-1.jsonl").exists()


def test_seal_before_first_delivery_same_call(world):
    world.board()
    s = world.hook_settings()
    calls(world, s, 7)
    world.seed(UNNAMED)
    out = world.call_hook(s)
    assert out
    ev = [m for m in world.metrics("t4-1") if m["ev"] in ("seal", "deliver")]
    assert [e["ev"] for e in ev] == ["seal", "deliver"] and ev[1]["c"] == 8
    snap = (world.B / "snap/t4-1.jsonl").read_bytes()
    assert (world.B / "snap/t4-1.sha256").read_text().strip() == hashlib.sha256(snap).hexdigest() == ev[0]["sha256"]


def _deal(world, r):
    world.board(k=2)
    world.seed(UNNAMED, UNNAMED, UNNAMED, UNNAMED)
    s0 = world.hook_settings("t4-1", 0, k=2, deal_r=r)
    s1 = world.hook_settings("t3-1", 1, k=2, deal_r=r)
    calls(world, s0, 8)
    calls(world, s1, 8)
    return delivered(world, "t4-1"), delivered(world, "t3-1")


def test_deal_r0(world):
    assert _deal(world, 0) == (["f-0", "f-2"], ["f-1", "f-3"])


def test_deal_r1(world):
    assert _deal(world, 1) == (["f-1", "f-3"], ["f-0", "f-2"])


def test_at_most_k_1(world):
    world.board(k=1)
    world.seed(*[UNNAMED] * 6)
    s = world.hook_settings(k=1)
    calls(world, s, 12)
    assert len(delivered(world)) == 1


def test_at_most_k_2(world):
    world.board(k=2)
    world.seed(*[UNNAMED] * 6)
    s = world.hook_settings(k=2)
    calls(world, s, 12)
    assert len(delivered(world)) == 2


def test_at_most_one_per_call(world):
    world.board(k=2)
    world.seed(*[UNNAMED] * 6)
    s = world.hook_settings(k=2)
    calls(world, s, 5)
    out = world.call_hook(s)
    assert out.count("Search result to check yourself") == 1 and len(delivered(world)) == 1


def test_rank_order(world):
    world.board(k=2)
    # receiver 0 with r=0 gets even indices: 0 other, 2 root doc, 4 unnamed test, 6 unnamed test
    world.seed(OTHER, OTHER, ROOT, OTHER, UNNAMED, OTHER, UNNAMED)
    s = world.hook_settings(k=2)
    calls(world, s, 10)
    assert delivered(world) == ["f-4", "f-6"]


def test_rank_root_before_other(world):
    world.board(k=2)
    world.seed(OTHER, OTHER, ROOT)
    s = world.hook_settings(k=2)
    calls(world, s, 10)
    assert delivered(world) == ["f-2", "f-0"]


def test_n_zero_rendered_without_count(world):
    world.board()
    world.seed({**UNNAMED, "n": 0, "move": "M2", "anchor": CAND_A})
    s = world.hook_settings()
    out = calls(world, s, 6)[-1]
    text = json.loads(out)["hookSpecificOutput"]["additionalContext"]
    assert "Count:" not in text and "Re-run this command yourself" in text


def test_rendered_at_most_1500(world):
    world.board()
    world.seed({"items": ["tests/test_other.py"] * 8, "anchor": CAND_A, "cmd": "grep -rln " + "q" * 220 + " tests/"})
    s = world.hook_settings()
    out = calls(world, s, 6)[-1]
    assert len(json.loads(out)["hookSpecificOutput"]["additionalContext"]) <= 1500


def test_finish_signal_once_then_nothing(world):
    world.board()
    world.seed(UNNAMED)
    s = world.hook_settings(finish_ms=int(time.time() * 1000) - 1000)
    outs = calls(world, s, 8)
    assert "finish now with what you have" in json.loads(outs[0])["hookSpecificOutput"]["additionalContext"]
    assert outs[1:] == [""] * 7 and delivered(world) == []
    assert [m["ev"] for m in world.metrics("t4-1")].count("finish_signal") == 1


def test_read_appends_opened(world):
    world.board()
    s = world.hook_settings()
    world.call_hook(s, tool="Read", tool_input={"file_path": str(world.SB / "repo/tests/test_other.py")})
    assert (world.B / "state/opened.txt").read_text().split() == ["tests/test_other.py"]


def test_output_is_valid_hook_json(world):
    world.board()
    world.seed(UNNAMED)
    s = world.hook_settings()
    out = calls(world, s, 6)[-1]
    j = json.loads(out)
    assert set(j) == {"hookSpecificOutput"} and j["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    assert "tests/test_other.py" in j["hookSpecificOutput"]["additionalContext"]


def test_empty_environment_still_delivers(world):
    world.board()
    world.seed(UNNAMED)
    s = world.hook_settings()
    outs = [world.call_hook(s, envi=True) for _ in range(6)]
    assert outs[-1] and delivered(world) == ["f-0"]


def test_call_events_logged(world):
    world.board()
    s = world.hook_settings()
    calls(world, s, 3)
    c = [m for m in world.metrics("t4-1") if m["ev"] == "call"]
    assert [x["c"] for x in c] == [1, 2, 3] and all("ms" in x for x in c)


def test_parallel_calls_never_exceed_k(world):
    """Regression (smoke 2026-11-13): parallel tool calls ran two hooks 2 ms apart and both delivered the same fact."""
    world.board(k=2)
    world.seed(*[{"items": ["tests/test_other.py"]}] * 8)
    s = world.hook_settings(k=2)
    for _ in range(5):
        world.call_hook(s)
    with cf.ThreadPoolExecutor(8) as ex:
        outs = list(ex.map(lambda _: world.call_hook(s), range(8)))
    d = delivered(world)
    assert len(d) == 2 and len(set(d)) == 2 and sum(bool(o) for o in outs) == 2
    calls = sorted(m["c"] for m in world.metrics("t4-1") if m["ev"] == "call")
    assert calls == list(range(1, 14))
