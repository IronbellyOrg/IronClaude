"""T-8: the watcher turns scout exits into cards (R-38, R-41)."""
import json
import subprocess
import sys
import time

from conftest import CT, finding, heading_anchor, report
from r5 import now_ms, read_jsonl


def setup(env, scouts=("t4-1", "t3-1"), receivers=("t1b-1",), k=2, finish_in_s=30):
    d = env["out"] / "runs" / "row" / CT
    (d / "reviews").mkdir(parents=True)
    for s in ("msgs", "delivered", "state", "snap", "metrics", "settings"):
        (d / "board" / s).mkdir(parents=True)
    (d / "board" / "msgs" / "watcher.jsonl").write_text("")
    fin = now_ms() + finish_in_s * 1000
    (d / "run.json").write_text(json.dumps({"scouts": list(scouts), "receivers": list(receivers)}))
    return d, fin


def start(env, d, fin, k=2, deal=0):
    return subprocess.Popen([sys.executable, "-m", "r5.watcher", "--run-dir", str(d), "--candidate",
                             str(env["sb"] / "cand" / CT / "candidate.md"), "--panel", "sl2", "--k", str(k),
                             "--finish-ms", str(fin), "--row", "row", "--pkg", CT, "--deal-r", str(deal), "--poll", "0.2"])


def scout(d, rid, n, tasks, model_ok=True, block=True, api_error=False):
    rep = report([finding(f"F{i}", heading_anchor(CT, t)) for i, t in enumerate(tasks)]) if block else "no block\n"
    (d / "reviews" / f"{rid}.attempt{n}.md").write_text(rep)
    meta = {"model_ok": model_ok, "findings_block": block, "api_error": api_error}
    tmp = d / "reviews" / f"{rid}.attempt{n}.meta.json.tmp"
    tmp.write_text(json.dumps(meta))
    tmp.rename(d / "reviews" / f"{rid}.attempt{n}.meta.json")


def cards(d):
    return read_jsonl(d / "board" / "msgs" / "watcher.jsonl")


def log(d):
    return read_jsonl(d / "board" / "watcher.log")


def wait_for(fn, timeout=4.0):
    end = time.time() + timeout
    while time.time() < end:
        if fn():
            return True
        time.sleep(0.05)
    return fn()


def test_card_then_card2_then_exit(env):
    d, fin = setup(env)
    p = start(env, d, fin)
    all12 = [f"T{i}" for i in range(1, 13)]
    assert wait_for(lambda: any(e["event"] == "start" for e in log(d)), 10)
    scout(d, "t4-1", 1, all12[:9])
    assert wait_for(lambda: len(cards(d)) == 1, 0.5)  # within 2 poll cycles of 0.2 s
    c1 = cards(d)[0]
    assert set(c1["items"]) <= {"T10", "T11", "T12"} and len(c1["items"]) == 2
    scout(d, "t3-1", 1, [c1["items"][0]])
    assert wait_for(lambda: len(cards(d)) == 2)
    c2 = cards(d)[1]
    assert c1["items"][0] not in c2["items"] and c1["items"][1] in c2["items"]
    assert p.wait(timeout=5) == 0
    assert any(e["event"] == "exit" for e in log(d))


def test_unusable_scouts(env):
    d, fin = setup(env)
    p = start(env, d, fin)
    scout(d, "t4-1", 1, ["T1"], model_ok=False)
    scout(d, "t3-1", 1, ["T1"], api_error=True)
    assert wait_for(lambda: sum(e["event"] == "scout_unusable" for e in log(d)) == 2)
    scout(d, "t4-1", 2, [], block=False)
    scout(d, "t3-1", 2, ["T2"], model_ok=True, block=False)
    assert p.wait(timeout=5) == 0
    assert cards(d) == []
    assert sum(e["event"] == "scout_unusable" for e in log(d)) == 4


def test_no_card_after_finish(env):
    d, fin = setup(env, finish_in_s=-1)
    scout(d, "t4-1", 1, ["T1"])
    p = start(env, d, fin)
    assert p.wait(timeout=5) == 0
    assert cards(d) == []
    assert any(e["event"] == "after_finish" for e in log(d))


def test_exits_at_finish(env):
    d, fin = setup(env, finish_in_s=1)
    p = start(env, d, fin)
    assert p.wait(timeout=5) == 0
    assert cards(d) == []
