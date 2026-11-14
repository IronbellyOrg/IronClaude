"""Scripted fake of `claude -p` (DESIGN 15.1). Reads the plan named by FAKE_CLAUDE_PLAN."""

import datetime
import fcntl
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path


def arg(name, argv):
    return argv[argv.index(name) + 1] if name in argv else None


def now_iso():
    return (
        datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    )


def main():
    argv = sys.argv[1:]
    model = arg("--model", argv) or ""
    resume = arg("--resume", argv)
    fmt = arg("--output-format", argv) or "text"
    prompt = sys.stdin.read()
    plan_path = Path(os.environ["FAKE_CLAUDE_PLAN"])
    state_path = plan_path.with_suffix(".state.json")
    with open(str(state_path) + ".lock", "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        st = (
            json.loads(state_path.read_text())
            if state_path.exists()
            else {"used": {}, "calls": {}, "sessions": [], "log": []}
        )
        plan = json.loads(plan_path.read_text())
        st["calls"][model] = st["calls"].get(model, 0) + 1
        nth = st["calls"][model]
        chosen = None
        for i, rule in enumerate(plan):
            m = rule.get("match", {})
            if "model" in m and m["model"] != model:
                continue
            if "resume" in m and bool(m["resume"]) != bool(resume):
                continue
            if "prompt_contains" in m and m["prompt_contains"] not in prompt:
                continue
            if "nth" in m and m["nth"] != nth:
                continue
            times = rule.get("times")
            if times is not None and st["used"].get(str(i), 0) >= times:
                continue
            st["used"][str(i)] = st["used"].get(str(i), 0) + 1
            chosen = rule
            break
        known = set(st["sessions"])
        act = (chosen or {}).get("action", {})
        if resume and (resume not in known or act.get("resume_fail")):
            sid = None
        else:
            sid = resume or act.get("session_id") or str(uuid.uuid4())
            if sid not in known:
                st["sessions"].append(sid)
        st["log"].append(
            {
                "model": model,
                "resume": resume,
                "fmt": fmt,
                "rule": plan.index(chosen) if chosen else None,
                "argv": argv,
                "cwd": os.getcwd(),
                "t": time.time(),
            }
        )
        state_path.write_text(json.dumps(st))
    if chosen is None:
        print(
            f"fake claude: no rule for model={model} resume={resume}", file=sys.stderr
        )
        return 1
    if sid is None:
        print(f"No conversation found with session ID: {resume}", file=sys.stderr)
        return 1
    if "judge_score" in act and "blind scoring judge" in prompt:
        m = re.search(r"Write JSON to (\S+)", prompt)
        if m:
            Path(m.group(1)).write_text(json.dumps(act["judge_score"]))
    if act.get("write_file"):
        Path(act["write_file"]).write_text("written by fake reviewer\n")
    observed = act.get("observed_model", model)
    proj = Path(
        os.environ.get("R3_CLAUDE_PROJECTS", str(Path.home() / ".claude/projects"))
    )
    slug = re.sub(r"[^A-Za-z0-9]", "-", os.getcwd())
    tr = proj / slug / f"{sid}.jsonl"
    tr.parent.mkdir(parents=True, exist_ok=True)

    def transcript(entry):
        e = dict(entry)
        e["timestamp"] = now_iso()
        e["sessionId"] = sid
        with open(tr, "a") as fh:
            fh.write(json.dumps(e) + "\n")

    transcript({"type": "user", "message": {"role": "user", "content": prompt}})
    events = [{"type": "system", "subtype": "init", "session_id": sid, "model": model}]
    if act.get("tool_use_input") is not None:
        tu = {
            "type": "assistant",
            "parent_tool_use_id": None,
            "session_id": sid,
            "message": {
                "model": observed,
                "content": [
                    {
                        "type": "tool_use",
                        "id": "tu1",
                        "name": "Bash",
                        "input": act["tool_use_input"],
                    }
                ],
            },
        }
        events.append(tu)
        transcript({"type": "assistant", "message": tu["message"]})
    text = ""
    if act.get("report"):
        text = Path(act["report"]).read_text()
    elif act.get("text") is not None:
        text = act["text"]
    chunks = act.get("stream_lines")
    streaming = fmt == "stream-json"
    out = sys.stdout

    def emit(ev):
        if streaming:
            out.write(json.dumps(ev) + "\n")
            out.flush()

    for ev in events:
        emit(ev)
    if chunks:
        for c in chunks:
            ev = {
                "type": "assistant",
                "parent_tool_use_id": None,
                "session_id": sid,
                "message": {
                    "model": observed,
                    "content": [{"type": "text", "text": c}],
                },
            }
            events.append(ev)
            transcript({"type": "assistant", "message": ev["message"]})
            emit(ev)
            time.sleep(act.get("chunk_delay_s", 0))
    if act.get("sleep_s"):
        time.sleep(act["sleep_s"])
    if not chunks:
        ev = {
            "type": "assistant",
            "parent_tool_use_id": None,
            "session_id": sid,
            "message": {"model": observed, "content": [{"type": "text", "text": text}]},
        }
        events.append(ev)
        transcript({"type": "assistant", "message": ev["message"]})
        emit(ev)
    if not act.get("no_result"):
        res = {
            "type": "result",
            "subtype": "success",
            "is_error": bool(act.get("result_is_error")),
            "result": text,
            "session_id": sid,
            "usage": {"output_tokens": act.get("tokens", 100)},
            "modelUsage": {observed: {"outputTokens": act.get("tokens", 100)}},
        }
        events.append(res)
        emit(res)
    if act.get("no_stdout"):
        return int(act.get("exit", 1))
    if fmt == "json":
        out.write(json.dumps(events))
        out.flush()
    elif fmt == "text":
        out.write(text)
    return int(act.get("exit", 0))


if __name__ == "__main__":
    sys.exit(main())
