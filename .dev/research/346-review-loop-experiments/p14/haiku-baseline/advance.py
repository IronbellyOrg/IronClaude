#!/usr/bin/env python3
"""Detect finished workers (SubagentHandback DONE in the transcript), ingest, prep the next step.
Prints `LAUNCH <model> <PROMPT path>` for every prepped step never launched (AUD2 is sonnet; loop steps haiku), appends a
launch event to launch-ledger.jsonl, and prints RUNNING / ALL DONE. A transcript is matched by the PROMPT path in its first
lines (short 'Read <path>' launches) or, failing that, by the prompt's sandbox dir + brief (pasted-text launches).
Tokens: output tokens, each message id once. After any ingest, collect.py refreshes results.json."""
import json, re, sys, time, glob, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import harness as h
HERE = pathlib.Path(__file__).parent
LEDGER = HERE/"launch-ledger.jsonl"
GLOB = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
MODEL = lambda step: "sonnet" if step in ("AUD", "AUD2") else "haiku"
nxt = {"R1": "V1", "V1": "R2", "R2": "V2", "V2": "R3"}
rx = re.compile(r"p14/haiku-baseline/runs/(a\d-r\d)/PROMPT-(\w+)\.md")

def fingerprints():
    """sandbox-dir marker + escaped brief -> (run, step), for pasted-text launches."""
    fp = {}
    for p in h.RUNS.glob("a*-r*/PROMPT-*.md"):
        try:
            t = p.read_text(errors="ignore")
            sb = re.search(r"SANDBOX: work ONLY inside (\S+?)\.", t).group(1)
            b = t.split("BRIEF (verbatim, from the coordinator):\n", 1)[1].split("\n\nFINAL REPLY", 1)[0]
        except Exception: continue
        fp[(sb + ". Do not read", json.dumps(b)[1:-1])] = (p.parent.name, p.stem.replace("PROMPT-", ""))
    return fp

launched = {}   # (run, step) -> (aid, finished, tokens)
FP = fingerprints()
for f in glob.glob(GLOB):
    try:
        with open(f, errors="ignore") as fh: head = "".join(next(fh, "") for _ in range(6))
    except Exception: continue
    m = rx.search(head[:3000]); key = (m.group(1), m.group(2)) if m else None
    if key is None:
        for (sb, esc), k in FP.items():
            if sb in head and esc in head: key = k; break
    if key is None: continue
    done = False; best = {}
    for line in open(f, errors="ignore"):
        try: d = json.loads(line)
        except Exception: continue
        msg = d.get("message") or {}
        if msg.get("role") != "assistant": continue
        u = msg.get("usage") or {}; mid = msg.get("id") or f"anon{len(best)}"
        best[mid] = max(best.get(mid, 0), u.get("output_tokens") or 0)
        if isinstance(msg.get("content"), list):
            for c in msg["content"]:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "SubagentHandback" and "DONE" in json.dumps(c.get("input")): done = True
    cand = (pathlib.Path(f).stem, done, sum(best.values()))
    if key not in launched or (cand[1], cand[2]) > (launched[key][1], launched[key][2]): launched[key] = cand

def ledger():
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()] if LEDGER.exists() else []
def log_event(run, step):
    with open(LEDGER, "a") as fh: fh.write(json.dumps({"run": run, "step": step, "event": "launch", "model": MODEL(step), "ts": time.time()}) + "\n")
def prep(run, n):
    out = subprocess.run([sys.executable, str(HERE/"harness.py"), "prep", run, n], capture_output=True, text=True)
    print("   ->", n, (out.stdout or out.stderr).strip().splitlines()[-1][-120:])

ingested = False
for run in sorted(p.name for p in h.RUNS.iterdir()):
    for last in h.STEPS:
        st = h.load(run)
        if (run, last) not in launched or last in st["done"]: continue
        aid, done, toks = launched[(run, last)]
        if not done: continue
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()): h.ingest(run, last)
        ingested = True
        st = h.load(run); st["log"][last]["output_tokens"] = toks; h.save(run, st)
        rec = st["log"][last]; v = rec.get("verdict")
        print(f"[{run}] {last} done: verdict={v} blocking_ids={rec.get('blocking_ids')} spec={rec.get('spec_after',{}).get('bytes')} out_exists={rec['output_exists']}")
        if not rec["output_exists"]: print(f"   !! output missing for {run} {last}"); continue
        if last in ("AUD", "AUD2"): continue
        if last in ("R1", "R2", "R3") and v in ("PASS", "INCOMPLETE", "NONE") or last == "R3":
            if v in ("INCOMPLETE", "NONE"): print(f"   !! {run} {last} verdict {v}: check manually")
            for n in ("AUD", "AUD2"):
                if not (h.run_dir(run)/f"PROMPT-{n}.md").exists(): prep(run, n)
            continue
        n = nxt[last]
        if h.arm_of(run) == 1 and n in ("R2", "V2", "R3"):
            print(f"   -> arm1 needs manual substitutions for {n}: run `harness.py peek {run} {last}` then `prep {run} {n} KEY=VAL ...`"); continue
        prep(run, n)

# LAUNCH lines: prepped, never launched (a step already launched/finished before the ledger existed is not relaunched)
ev = ledger(); running = 0; pending_total = 0
for run in sorted(p.name for p in h.RUNS.iterdir()):
    st = h.load(run)
    for step in h.STEPS:
        p = h.run_dir(run)/f"PROMPT-{step}.md"
        if not p.exists() or step in st["done"]: continue
        pending_total += 1
        if (run, step) in launched or any(e["run"] == run and e["step"] == step for e in ev):
            running += 1; continue
        print(f"LAUNCH {MODEL(step)} {p}")
        log_event(run, step)
if ingested:
    r = subprocess.run([sys.executable, str(HERE/"collect.py")], capture_output=True, text=True)
    print("   results.json refreshed" if r.returncode == 0 else "WARN collect.py failed: " + r.stderr.strip()[-160:])
if running: print(f"RUNNING {running}")
if not pending_total: print("ALL DONE")
