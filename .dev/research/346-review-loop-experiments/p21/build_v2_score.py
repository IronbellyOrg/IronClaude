"""Blind scoring inputs for the intermediate spec (after V1, before V2) of the 24 PN1-family runs: sids s106+."""
import json, hashlib, random, subprocess, sys
from pathlib import Path
SP = Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
P17 = SP/"p17"; SC = P17/"score"
REL = ".dev/orca-command-refactor/specs/history/spec-v2.md"
runs = []
for arm, d, pre in (("pn1o","p19/rep/pn1o","o2"),("pn1d2","p19/rep/pn1d2","d2"),("pn1d","p19/pn1d","d1"),("pn1m","p19/pn1m","m1")):
    for i in range(1,7):
        runs.append((arm, f"{pre}-r{i}", SP/d/"runs"/f"{pre}-r{i}"/"ws"/REL))
assert all(p.exists() for _,_,p in runs)
key = json.load(open(SC/"key.json"))
n0 = max(int(k[1:]) for k in key) + 1
assert n0 == 106, n0
rnd = random.Random(20261111); order = list(range(len(runs))); rnd.shuffle(order)
tmpl = (SC/"prompt-template.md").read_text()
for j, idx in enumerate(order):
    arm, r, p = runs[idx]; sid = f"s{n0+j}"; data = p.read_bytes()
    (SC/"in"/f"{sid}.md").write_bytes(data)
    d = subprocess.run(["diff","-u",str(P17/"in"/"spec-original.md"),f"in/{sid}.md"],cwd=str(SC),capture_output=True,text=True).stdout
    assert d.strip(), sid
    (SC/"in"/f"{sid}.diff").write_text(d)
    (SC/"prompts"/f"{sid}.md").write_text(tmpl.replace("__SID__", sid).replace("__OUT__", str(SC/"out"/f"{sid}.json")))
    key[sid] = {"arm": f"v2-{arm}", "run": r, "stage": "after-V1", "sha": hashlib.sha256(data).hexdigest()}
    print(sid, arm, r, len(d.splitlines()))
json.dump(key, open(SC/"key.json","w"), indent=1)
