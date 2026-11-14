"""T-9 and F-3, F-4, F-15: the receiver PostToolUse hook (R-19 pattern, R-21, R-22, R-41)."""
import hashlib
import json
import subprocess

import pytest
from conftest import R5, bin_
from r5 import now_ms, read_jsonl

RID = "t1b-1"


@pytest.fixture
def board(env):
    b = env["tmp"] / "board"
    for s in ("msgs", "delivered", "state", "snap", "metrics"):
        (b / s).mkdir(parents=True)
    (b / "msgs" / "watcher.jsonl").write_text("")
    tr = env["tmp"] / "transcript.jsonl"
    tr.write_text('{"type":"user"}\n{"type":"assistant"}\n')
    return {"dir": b, "tr": tr}


def add_card(b, n, items, to=RID):
    c = {"v": "panel-msg/1", "id": f"c-{to}-{n}", "run": "r/p", "from": "watcher", "to": to, "t": now_ms(), "kind": "coverage", "items": items}
    with open(b["dir"] / "msgs" / "watcher.jsonl", "a") as f:
        f.write(json.dumps(c) + "\n")


def call(b, fin_off_ms=600000, agent=None, envmin=False, tr=None, k=2, minc=6):
    inp = {"session_id": "s", "transcript_path": str(tr or b["tr"]), "tool_name": "Bash", "tool_input": {}, "tool_use_id": "x"}
    if agent:
        inp["agent_id"] = agent
    cmd = ["bash", bin_("hook-posttool.sh"), str(b["dir"]), RID, str(now_ms()), str(now_ms() + fin_off_ms), str(minc), str(k), str(R5)]
    r = subprocess.run((["env", "-i", "PATH=/usr/bin:/bin"] if envmin else []) + cmd, input=json.dumps(inp), capture_output=True, text=True)
    assert r.returncode == 0
    return r.stdout.strip()


def metrics(b):
    return read_jsonl(b["dir"] / "metrics" / f"{RID}.jsonl")


def delivered(b):
    return read_jsonl(b["dir"] / "delivered" / f"{RID}.jsonl")


def test_min_calls_seal_output_and_card2(board):
    add_card(board, 1, ["T9", "T12"])
    for _ in range(5):  # (a) calls 1-5 deliver nothing
        assert call(board) == ""
    out = call(board)  # call 6 delivers
    o = json.loads(out)  # (c)
    assert o["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    text = o["hookSpecificOutput"]["additionalContext"]
    assert len(text) <= 1500 and text.startswith("Panel request") and "Task 9, Task 12" in text
    snap = board["dir"] / "snap"  # (b)
    assert (snap / f"{RID}.jsonl").read_bytes() == board["tr"].read_bytes()
    assert (snap / f"{RID}.sha256").read_text().split()[0] == hashlib.sha256(board["tr"].read_bytes()).hexdigest()
    assert delivered(board)[0]["text_sha256"] == hashlib.sha256(text.encode()).hexdigest()
    assert call(board) == ""  # nothing pending
    add_card(board, 2, ["T3"])  # (d) second card -> card-2 text
    t2 = json.loads(call(board))["hookSpecificOutput"]["additionalContext"]
    assert t2.startswith("Updated panel request") and "Task 3" in t2
    add_card(board, 3, ["T4"])
    add_card(board, 4, ["T5"])
    t4 = json.loads(call(board))["hookSpecificOutput"]["additionalContext"]
    assert "Task 5" in t4 and "Task 4" not in t4
    st = {d["id"]: d["status"] for d in delivered(board)}
    assert st[f"c-{RID}-3"] == "superseded" and st[f"c-{RID}-4"] == "delivered"
    assert all("ms" in m for m in metrics(board) if m["event"] == "call")  # (h) duration logged
    assert sum(m["event"] == "call" for m in metrics(board)) == 9  # 5 + 1 + 1 + 1 + 1 calls


def test_finish_signal_once(board):  # (e)
    add_card(board, 1, ["T9"])
    out = call(board, fin_off_ms=-1, minc=1)
    assert "Finish now" in json.loads(out)["hookSpecificOutput"]["additionalContext"]
    assert call(board, fin_off_ms=-1, minc=1) == ""
    assert delivered(board) == []
    assert sum(m["event"] == "finish_signal_t" for m in metrics(board)) == 1


def test_subagent_call_skipped(board):  # (f) and F-15
    add_card(board, 1, ["T9"])
    assert call(board, minc=1, agent="a1") == ""
    assert any(m["event"] == "subagent_call" for m in metrics(board))
    assert json.loads(call(board, minc=1))  # next main-session call delivers


def test_env_minimal(board):  # (g)
    add_card(board, 1, ["T9"])
    assert json.loads(call(board, minc=1, envmin=True))


def test_snapshot_missing_transcript(board, env):  # F-3 (missing transcript)
    add_card(board, 1, ["T9"])
    assert call(board, minc=1, tr=env["tmp"] / "nope.jsonl") == ""
    add_card(board, 2, ["T3"])
    assert call(board, minc=1) == ""  # nothing for the rest of the run
    assert any(m["event"] == "snapshot_missing" for m in metrics(board))
    assert delivered(board) == []


def test_snapshot_dir_readonly(board):  # F-3 (snap dir read-only)
    add_card(board, 1, ["T9"])
    (board["dir"] / "snap").chmod(0o500)
    try:
        assert call(board, minc=1) == ""
        assert call(board, minc=1) == ""
    finally:
        (board["dir"] / "snap").chmod(0o700)
    assert any(m["event"] == "snapshot_missing" for m in metrics(board))
    assert delivered(board) == []


def test_corrupt_board_line(board):  # F-4
    add_card(board, 1, ["T9"])
    with open(board["dir"] / "msgs" / "watcher.jsonl", "a") as f:
        f.write("{corrupt\n")
    assert call(board, minc=1) == ""
    assert any(m["event"] == "hook_error" for m in metrics(board))
