#!/usr/bin/env python3
"""Detect finished workers (SubagentHandback DONE in the transcript), ingest, prep the next step, and print the prompts
that still need an Agent launch as `LAUNCH <model> <absolute PROMPT path>` (at most 6 - running).

  advance.py [--dry-run]     --dry-run reads everything, writes nothing (no ledger line, no ingest, no prep)

Flow per run (Stage 2 arm 3): R1 -> PASS: AUD+AUD2 | FAIL: V1 -> R2 -> PASS: AUD+AUD2 | FAIL: V2 -> R3 -> AUD+AUD2.
AUD and AUD2 are launched together (both slots free) and always on sonnet; loop steps follow the run's stratum (haiku for l2h-*).
A prompt with no transcript after launch.lost_after_minutes is relaunched once, then marked lost. MANUAL lines need the coordinator.
Nothing here reads a token count: tokens are summed by analysis.py after steps finished (owner decision D6)."""
import json, sys, time, pathlib, subprocess, os
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import harness as h
import analysis

DRY = "--dry-run" in sys.argv
LEDGER = h.AB/"launch-ledger.jsonl"
CFG = h.CFG
NEXT = {"V1": "R2", "V2": "R3"}

def read_ledger():
    ev = []
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            if line.strip(): ev.append(json.loads(line))
    return ev

def log_event(**kw):
    if DRY: return
    kw["ts"] = time.time()
    with open(LEDGER, "a") as fh: fh.write(json.dumps(kw) + "\n")

def prompt_path(run, step): return h.run_dir(run)/f"PROMPT-{step}.md"

def transcript_state(run, step):
    """None when no transcript has the prompt path in its first lines; else {'done': bool}."""
    t = analysis.step_tokens(prompt_path(run, step), analysis.MODEL_SUBSTR[h.model_for(run, step)], h.TASKS_GLOB)
    return None if t is None else {"done": t["done"], "warn": t["warn"]}

def prep(run, step):
    if DRY:
        print(f"   DRY would prep {run} {step}"); return
    out = subprocess.run([sys.executable, str(pathlib.Path(__file__).parent/"harness.py"), "prep", run, step], capture_output=True, text=True, env=os.environ)
    if out.returncode != 0:
        print(f"MANUAL {run} {step}: prep failed: {(out.stderr or out.stdout).strip().splitlines()[-1][-160:]}")
    else:
        print("   ->", step, (out.stdout or out.stderr).strip().splitlines()[-1][-120:])

def advance_run(run, events):
    st = h.load(run)
    pending_next = []
    for step in h.STEPS:
        p = prompt_path(run, step)
        if not p.exists() or step in st["done"] or st["log"].get(step, {}).get("lost"): continue
        launched = [e for e in events if e["run"] == run and e["step"] == step and e["event"] in ("launch", "relaunch")]
        if not launched: continue
        ts = transcript_state(run, step)
        if ts and ts["done"]:
            if ts["warn"]: print(f"WARN {run} {step}: several transcripts match; kept the expected-model one with the most output tokens")
            if DRY: print(f"   DRY would ingest {run} {step}"); continue
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()): h.ingest(run, step)
            st = h.load(run); rec = st["log"][step]; v = rec.get("verdict")
            print(f"[{run}] {step} done: verdict={v} blocking_ids={rec.get('blocking_ids')} spec={rec.get('spec_after',{}).get('bytes')} out_exists={rec['output_exists']}")
            if not rec["output_exists"]:
                print(f"MANUAL {run} {step}: output missing"); continue
            if step in ("AUD", "AUD2"): continue
            if step in ("R1", "R2", "R3"):
                if v in ("INCOMPLETE", "NONE"): print(f"MANUAL {run} {step}: verdict {v}, check the report; continuing to the audits as in Stage 2")
                if v in ("PASS", "INCOMPLETE", "NONE") or step == "R3": pending_next += ["AUD", "AUD2"]
                else: pending_next.append({"R1": "V1", "R2": "V2"}[step])
            else: pending_next.append(NEXT[step])
        elif not ts:
            age = (time.time() - max(e["ts"] for e in launched)) / 60
            if age > CFG["launch"]["lost_after_minutes"]:
                if len(launched) < 2:
                    log_event(run=run, step=step, event="relaunch", model=h.model_for(run, step), prompt=str(p))
                    print(f"RELAUNCH {run} {step}: no transcript after {age:.0f} min")
                    print(f"LAUNCH {h.model_for(run, step)} {p}")
                else:
                    print(f"LOST {run} {step}: no transcript after relaunch; MANUAL")
                    if not DRY:
                        st["log"][step] = {"lost": True, "output_exists": False}; h.save(run, st)
    for n in pending_next: prep(run, n)

def main():
    runs = sorted(p.name for p in h.RUNS.iterdir() if (p/"state.json").exists()) if h.RUNS.exists() else []
    events = read_ledger()
    for run in runs: advance_run(run, events)
    events = read_ledger()
    # running = launched, not done, not lost
    def finished(run, step):
        st = h.load(run); return step in st["done"] or st["log"].get(step, {}).get("lost")
    running = 0
    for run in runs:
        for step in h.STEPS:
            if any(e["run"] == run and e["step"] == step and e["event"] == "launch" for e in events) and not finished(run, step) and prompt_path(run, step).exists():
                running += 1
    slots = CFG["launch"]["max_concurrent"] - running
    # new launches: prepped, never launched
    for run in runs:
        st = h.load(run)
        todo = [s for s in h.STEPS if prompt_path(run, s).exists() and s not in st["done"]
                and not any(e["run"] == run and e["step"] == s for e in events)]
        group = [todo[i:] for i in range(len(todo))]
        if not todo: continue
        # AUD and AUD2 go together
        if "AUD" in todo and "AUD2" in todo:
            need = [s for s in todo if s in ("AUD", "AUD2")]
            others = [s for s in todo if s not in ("AUD", "AUD2")]
            batches = [[s] for s in others] + [need]
        else:
            batches = [[s] for s in todo]
        for batch in batches:
            if len(batch) > slots: continue
            for s in batch:
                print(f"LAUNCH {h.model_for(run, s)} {prompt_path(run, s)}")
                log_event(run=run, step=s, event="launch", model=h.model_for(run, s), prompt=str(prompt_path(run, s)))
            slots -= len(batch)

if __name__ == "__main__":
    main()
