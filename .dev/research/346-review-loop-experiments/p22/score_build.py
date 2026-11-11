"""Blind scoring inputs for the p22 A/B finals: sids s130-s141, fixed by a seeded shuffle of the 12 runs; builds inputs only for completed runs."""
import json, hashlib, random, subprocess, sys
from pathlib import Path
SP = Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
P17 = SP / "p17"; SC = P17 / "score"; P22 = SP / "p22"
REL = ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
runs = [("pn1c", f"c3-r{i}") for i in range(1, 7)] + [("pn1j", f"j3-r{i}") for i in range(1, 7)]
rnd = random.Random(20261112); order = list(range(12)); rnd.shuffle(order)
sid_of = {runs[idx][1]: f"s{130 + j}" for j, idx in enumerate(order)}
key = json.load(open(SC / "key.json"))
tmpl = (SC / "prompt-template.md").read_text()
built = []
for arm, run in runs:
    sid = sid_of[run]
    st = json.load(open(P22 / arm / "runs" / run / "state.json"))
    if st["phase"] != "complete" or sid in key:
        continue
    p = P22 / arm / "runs" / run / "aud" / "ws" / REL
    data = p.read_bytes()
    (SC / "in" / f"{sid}.md").write_bytes(data)
    d = subprocess.run(["diff", "-u", str(P17 / "in" / "spec-original.md"), f"in/{sid}.md"], cwd=str(SC), capture_output=True, text=True).stdout
    assert d.strip(), sid
    (SC / "in" / f"{sid}.diff").write_text(d)
    (SC / "prompts" / f"{sid}.md").write_text(tmpl.replace("__SID__", sid).replace("__OUT__", str(SC / "out" / f"{sid}.json")))
    key[sid] = {"arm": "p22-" + ("c3" if arm == "pn1c" else "j3"), "run": run, "sha": hashlib.sha256(data).hexdigest()}
    built.append(sid)
json.dump(key, open(SC / "key.json", "w"), indent=1)
print("built", built)
