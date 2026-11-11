"""Build blind scoring inputs for the replicate finals (sids s94+)."""
import json, hashlib, random, subprocess, shutil, sys, os
from pathlib import Path
SP = Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
P17 = SP/"p17"; SC = P17/"score"
REL = ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
runs = []
for arm, d, pre in (("pn1o","pn1o","o2"),("pn1d2","pn1d2","d2")):
    for i in range(1,7):
        r = f"{pre}-r{i}"
        p = SP/"p19"/"rep"/d/"runs"/r/"aud"/"ws"/REL
        runs.append((arm, r, p))
missing = [str(p) for _,_,p in runs if not p.exists()]
if missing:
    print("MISSING", *missing, sep="\n"); sys.exit(1)
key = json.load(open(SC/"key.json"))
n0 = max(int(k[1:]) for k in key) + 1
assert n0 == 94, n0
rnd = random.Random(20261110)
order = list(range(len(runs))); rnd.shuffle(order)
tmpl = (SC/"prompt-template.md").read_text()
for j, idx in enumerate(order):
    arm, r, p = runs[idx]
    sid = f"s{n0+j}"
    data = p.read_bytes()
    (SC/"in"/f"{sid}.md").write_bytes(data)
    d = subprocess.run(["diff","-u",str(P17/"in"/"spec-original.md"),f"in/{sid}.md"],cwd=str(SC),capture_output=True,text=True).stdout
    (SC/"in"/f"{sid}.diff").write_text(d)
    (SC/"prompts"/f"{sid}.md").write_text(tmpl.replace("__SID__", sid).replace("__OUT__", str(SC/"out"/f"{sid}.json")))
    key[sid] = {"arm":arm,"run":r,"sha":hashlib.sha256(data).hexdigest()}
    print(sid, arm, r)
json.dump(key, open(SC/"key.json","w"), indent=1)
