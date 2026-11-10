#!/usr/bin/env python3
"""Detect finished workers (SubagentHandback DONE in the transcript), ingest, move each run's state machine, and print
`LAUNCH <model-alias> <absolute PROMPT path>` for the prompts that still need an Agent launch (C9.5).
At most 6 - running lines are printed. A launched worker whose transcript ended without DONE is relaunched once, then marked lost.
Usage: advance.py [--dry-run]   (--dry-run prints the LAUNCH lines without recording them)"""
import glob
import json
import os
import re
import shutil
import sys
import time

import harness as H
import tokens as TK

MAX_RUNNING = 6
LEDGER = H.AB / "launch_ledger.json"
TASKS_GLOB = TK.TASKS_GLOB
MAX_LAUNCHES = 2


def load_ledger():
    return json.load(open(LEDGER)) if LEDGER.exists() else {}


def save_ledger(led):
    tmp = f"{LEDGER}.tmp"
    json.dump(led, open(tmp, "w"), indent=1)
    os.replace(tmp, LEDGER)


def scan(glob_pat=None):
    """{(run, step): [dict(done, ended, file)]} over every transcript whose first 6 lines name a c3 PROMPT file."""
    out = {}
    for f in glob.glob(glob_pat or TASKS_GLOB):
        try:
            lines = open(f, errors="ignore").read().splitlines()
        except OSError:
            continue
        m = re.search(H.TASK_RE, "\n".join(lines[:6]))
        if not m:
            continue
        done, ended = False, False
        for line in lines:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            msg = d.get("message") or {}
            if msg.get("role") != "assistant":
                continue
            ended = msg.get("stop_reason") in ("end_turn", "stop_sequence", "max_tokens")
            if isinstance(msg.get("content"), list):
                for c in msg["content"]:
                    if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "SubagentHandback" and "DONE" in json.dumps(c.get("input")):
                        done = True
        out.setdefault((m.group("run"), m.group("step")), []).append({"done": done, "ended": ended, "file": f})
    return out


def restore_for_relaunch(run, step):
    """A reviser that crashed may have half-edited the spec: put the pre-revision copy back."""
    if re.fullmatch(r"V\d", step):
        src = H.ws(run) / H.D / "specs/history" / f"spec-v{step[1]}.md"
        if src.exists():
            shutil.copy(src, H.ws(run) / H.SPEC)


def lose(run):
    st = H.load(run)
    st["lost"] = True
    st["decision"] = "LOST"
    st["cursor"] = {"kind": "done"}
    st["events"].append({"kind": "lost"})
    H.save(run, st)


def refresh(led, tr, now=None):
    msgs = []
    for key, ent in sorted(led.items()):
        if ent["state"] != "launched":
            continue
        run, step = key.split("/", 1)
        att = tr.get((run, step), [])
        if any(a["done"] for a in att):
            H.ingest(run, step)
            ent["state"] = "done"
            msgs.append(f"[{run}] {step} done")
        elif att and all(a["ended"] for a in att) and len(att) >= len(ent["launches"]):
            if len(ent["launches"]) < MAX_LAUNCHES:
                restore_for_relaunch(run, step)
                ent["state"] = "relaunch"
                msgs.append(f"[{run}] {step} ended without DONE: relaunch once")
            else:
                ent["state"] = "lost"
                lose(run)
                msgs.append(f"[{run}] {step} lost after {len(ent['launches'])} launches")
    return msgs


def main(dry_run=False, tr=None, now=None):
    led = load_ledger()
    tr = scan() if tr is None else tr
    for m in refresh(led, tr):
        print(m)
    runs = sorted(p.name for p in H.RUNS.iterdir() if (p / "state.json").exists()) if H.RUNS.exists() else []
    cands = []
    for run in runs:
        st = H.load(run)
        if st["cursor"]["kind"] == "done":
            continue
        for step in H.progress(run):
            key = f"{run}/{step}"
            ent = led.get(key)
            if ent is None or ent["state"] == "relaunch":
                cands.append((run, step, key))
    running = sum(1 for e in led.values() if e["state"] == "launched")
    budget = max(MAX_RUNNING - running, 0)
    lines = []
    for run, step, key in cands[:budget]:
        p = H.RUNS / run / f"PROMPT-{step}.md"
        lines.append(f"LAUNCH {H.model_for(run, step)} {p}")
        if not dry_run:
            ent = led.setdefault(key, {"launches": [], "state": "launched"})
            ent["launches"].append(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now or time.time())))
            ent["state"] = "launched"
            ent["model"] = H.model_for(run, step)
    if not dry_run:
        save_ledger(led)
    for l in lines:
        print(l)
    print(f"# running {running}, budget {budget}, ready {len(cands)}, printed {len(lines)}")
    return lines


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
