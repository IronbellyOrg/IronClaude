import json
import os
import time

import pytest

from p15common import offline_driver as OD


def mk(tmp_path, n=4, model="sonnet"):
    led = tmp_path / "offline" / "workers.json"
    steps = []
    for i in range(1, n + 1):
        pr = tmp_path / "p15" / "e9" / "offline" / "prompts" / f"L1-b{i:02d}.md"
        pr.parent.mkdir(parents=True, exist_ok=True)
        pr.write_text("x")
        steps.append({"id": f"L1-b{i:02d}", "kind": "label", "model": model, "prompt": str(pr),
                      "out": str(tmp_path / "p15/e9/offline/out" / f"L1-b{i:02d}.jsonl")})
    OD.add_steps(led, steps)
    return led


def transcript(tmp_path, prompt, done=True, name="t.output"):
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content": f"Read {prompt} and follow it exactly."}}),
             json.dumps({"type": "assistant", "uuid": "u1", "message": {"role": "assistant", "id": "m1", "model": "claude-sonnet-5-5",
                         "content": [{"type": "text", "text": "DONE x" if done else "working"}], "usage": {"output_tokens": 9}}})]
    (tmp_path / name).write_text("\n".join(lines))


def test_advance_prints_launch_lines_and_respects_cap(tmp_path, capsys, monkeypatch):
    monkeypatch.setenv("AB_TASKS_GLOB", str(tmp_path / "*.output"))
    monkeypatch.delenv("AB_MAX", raising=False)
    led = mk(tmp_path, 4)
    OD.add_steps(led, [{"id": "L1-b01", "kind": "x", "model": "sonnet", "prompt": "dup", "out": "dup"}])   # duplicate id ignored
    assert len(json.load(open(led))["steps"]) == 4
    OD.advance(led, r"p15/e9/offline", max_concurrent=2)
    out = capsys.readouterr().out
    assert out.count("LAUNCH ") == 2 and "model=sonnet" in out and "RUNNING 2" in out
    OD.advance(led, r"p15/e9/offline", max_concurrent=2)
    out = capsys.readouterr().out
    assert "LAUNCH" not in out and "RUNNING 2" in out
    # finish the first two: output exists and transcript done
    steps = json.load(open(led))["steps"]
    for s in steps[:2]:
        os.makedirs(os.path.dirname(s["out"]), exist_ok=True)
        open(s["out"], "w").write("{}")
    transcript(tmp_path, steps[0]["prompt"])
    OD.advance(led, r"p15/e9/offline", max_concurrent=2)
    out = capsys.readouterr().out
    assert out.count("LAUNCH ") == 1               # the finished step freed a slot (the second one is still running: no transcript)
    monkeypatch.setenv("AB_MAX", "1")
    OD.advance(led, r"p15/e9/offline", max_concurrent=6)
    assert "LAUNCH" not in capsys.readouterr().out


def test_missing_output_relaunch_once_then_lost(tmp_path, capsys, monkeypatch):
    monkeypatch.setenv("AB_TASKS_GLOB", str(tmp_path / "*.output"))
    monkeypatch.delenv("AB_MAX", raising=False)
    led = mk(tmp_path, 1)
    step = json.load(open(led))["steps"][0]
    OD.advance(led, r"p15/e9/offline")
    assert "LAUNCH" in capsys.readouterr().out
    transcript(tmp_path, step["prompt"])                     # worker said DONE but wrote nothing
    OD.advance(led, r"p15/e9/offline")
    out = capsys.readouterr().out
    assert "MANUAL L1-b01 output missing" in out and out.count("LAUNCH") == 1     # relaunched once
    assert json.load(open(led))["steps"][0]["relaunch"] == 1
    OD.advance(led, r"p15/e9/offline")
    out = capsys.readouterr().out
    assert "LOST L1-b01" in out and "ALL DONE" in out
    assert json.load(open(led))["steps"][0]["status"] == "lost"


def test_all_done(tmp_path, capsys, monkeypatch):
    monkeypatch.setenv("AB_TASKS_GLOB", str(tmp_path / "*.output"))
    led = mk(tmp_path, 1)
    step = json.load(open(led))["steps"][0]
    OD.advance(led, r"p15/e9/offline"); capsys.readouterr()
    os.makedirs(os.path.dirname(step["out"]), exist_ok=True)
    open(step["out"], "w").write("{}")
    transcript(tmp_path, step["prompt"])
    OD.advance(led, r"p15/e9/offline")
    assert "ALL DONE" in capsys.readouterr().out
