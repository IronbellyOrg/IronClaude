#!/usr/bin/env python3
"""Randomized-order, equal-concurrency scheduler for the p22 A/B (7-reviewer panel: current merge c3 vs Jev-split merge j3).
12 runs in 6 blocks of 2 (one of each arm, order random within the block, block order fixed); at most K runs in flight at any time;
a run dir is built only when a slot frees. Writes slots.json (planned order, actual build times)."""
import json, pathlib, random, subprocess, sys, datetime, os
SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
REP = SP / "p22"; K = int(os.environ.get("REP_K", "12"))
ARMS = {"c": ("pn1c", "c3"), "j": ("pn1j", "j3")}
f = REP / "slots.json"
if not f.exists():
    rnd = random.Random(20261111); order = []
    for b in range(6):
        pair = ["c", "j"]; rnd.shuffle(pair); order += pair
    f.write_text(json.dumps({"seed": 20261111, "k": K, "order": order, "built": []}, indent=1))
S = json.loads(f.read_text())
def active():
    n = 0
    for arm, (d, pre) in ARMS.items():
        for p in (REP / d / "runs").glob("*/state.json") if (REP / d / "runs").exists() else []:
            ph = json.loads(p.read_text()).get("phase")
            if ph not in ("complete", "lost"): n += 1
    return n
nxt = len(S["built"])
while nxt < len(S["order"]) and active() < S["k"]:
    arm = S["order"][nxt]; d, pre = ARMS[arm]
    rep = sum(1 for x in S["built"] if x["arm"] == arm) + 1
    r = subprocess.run(["uv", "run", "--no-project", "python", "-c", f"import harness; harness.build('sonnet',[{rep}])"], cwd=REP / d, capture_output=True, text=True)
    S["built"].append({"i": nxt, "arm": arm, "run": f"{pre}-r{rep}", "t": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")})
    f.write_text(json.dumps(S, indent=1)); print(f"SLOT built {pre}-r{rep} ({nxt+1}/12) active={active()}"); nxt += 1
print(f"# slots: built {len(S['built'])}/12, active {active()}/{S['k']}")
if len(S["built"]) == len(S["order"]) and active() == 0: print("ALL SLOTS DONE")
