#!/usr/bin/env python3
"""Detect finished workers (SubagentHandback DONE in the transcript), ingest, prep the next step.
Prints the prompt files that still need an Agent launch. Arm-1 substitutions are NOT automatic: it stops and says so."""
import json, re, sys, pathlib, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import harness as h
nxt = {"R1": "V1", "V1": "R2", "R2": "V2", "V2": "R3", "R3": "AUD"}
launched = {}   # (run, step) -> (aid, finished, tokens)
for f in h.TASKS.glob("*.output"):
    try: lines = f.read_text(errors="ignore").splitlines()
    except Exception: continue
    head = "\n".join(lines[:6])
    m = re.search(r"p11/runs/(a\d-r\d)/PROMPT-(\w+)\.md", head)
    if not m: continue
    done = False; toks = 0
    for line in lines:
        try: d = json.loads(line)
        except Exception: continue
        msg = d.get("message") or {}
        if isinstance(msg.get("content"), list):
            for c in msg["content"]:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "SubagentHandback" and "DONE" in json.dumps(c.get("input")): done = True
        u = msg.get("usage")
        if u and msg.get("role") == "assistant": toks += (u.get("output_tokens") or 0)
    launched[(m.group(1), m.group(2))] = (f.stem, done, toks)
todo = []
for run in sorted(p.name for p in h.RUNS.iterdir()):
    st = h.load(run)
    seq = [s for s in h.STEPS if (run, s) in launched]
    if not seq: continue
    last = seq[-1]; aid, done, toks = launched[(run, last)]
    if last in st["done"] or not done: continue
    h.ingest(run, last) if False else None
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()): h.ingest(run, last)
    st = h.load(run); st["log"][last]["output_tokens"] = toks; h.save(run, st)
    rec = st["log"][last]; v = rec.get("verdict")
    print(f"[{run}] {last} done: verdict={v} blocking_ids={rec.get('blocking_ids')} spec={rec.get('spec_after',{}).get('bytes')} out_exists={rec['output_exists']}")
    if not rec["output_exists"]: print(f"   !! output missing for {run} {last}"); continue
    if last == "AUD": continue
    if last in ("R1", "R2", "R3") and v in ("PASS", "INCOMPLETE", "NONE") or last == "R3":
        n = "AUD"
        if v in ("INCOMPLETE", "NONE"): print(f"   !! {run} {last} verdict {v}: check manually")
    else: n = nxt[last]
    if h.arm_of(run) == 1 and n in ("R2", "V2", "R3"):
        print(f"   -> arm1 needs manual substitutions for {n}: run `harness.py peek {run} {last}` then `prep {run} {n} KEY=VAL ...`"); continue
    import subprocess
    out = subprocess.run([sys.executable, str(pathlib.Path(__file__).parent/"harness.py"), "prep", run, n], capture_output=True, text=True)
    print("   ->", n, (out.stdout or out.stderr).strip().splitlines()[-1][-120:])
