#!/usr/bin/env python3
"""O3: merge the R1 fixtures of a3-r1, a3-r3, a3-r6 (same original spec) as one 3-reviewer round."""
import json, pathlib, re, subprocess, shutil

SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
AB = SP / "p13/ab1"
CLONE = SP / "p13/clones/pn1"
OV = SP / "exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
CLI = ["uv", "run", "--project", str(CLONE), "superclaude", "review"]
THEMES = [("T3", r"AC-0\.4|\bP0\b|Phase 0"), ("T2", r"WC-4|contract (?:file )?(?:path|location)|--output"),
          ("T1", r"AC-1\.[12]|/sc:load|\bP1\b|Phase 1|command counts?|\b36\b")]


def theme(text):
    for t, rx in THEMES:
        if re.search(rx, text, re.I):
            return t
    return "other"


wd = AB / "offline/o3"
shutil.rmtree(wd, ignore_errors=True)
wd.mkdir(parents=True)
runs = {"t1b-1": "a3-r1", "t2-1": "a3-r3", "t3-1": "a3-r6"}
args = ["merge", "--ledger", wd / "ledger.json", "--doc", OV, "--round", 1, "--out", wd / "merged.md"]
inputs = {}
for rid, run in runs.items():
    lines = (AB / "fixtures" / run / "round1.findings").read_text()
    rep = wd / f"{rid}.md"
    rep.write_text("review: 1 of 3\n\n## Findings block\n\n```findings-v1\n" + lines + "```\n\nverdict: FAIL\n")
    inputs[rid] = [json.loads(x) for x in lines.splitlines() if x.strip()]
    args += ["--report", f"{rid}={rep}"]
r = subprocess.run([*CLI, *map(str, args)], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
out = json.loads(r.stdout)
led = json.loads((wd / "ledger.json").read_text())
members = [(m["reviewer_id"], m["fid"]) for row in led["rows"] for m in row["members"]]
want = [(rid, f["id"]) for rid, fs in inputs.items() for f in fs]
print("inputs:", len(want), "members:", len(members), "each exactly once:", sorted(members) == sorted(want))
print("verdict", out["verdict"], out["decision"], "brief", out["brief_ids"])
for row in led["rows"]:
    th = theme(" ".join([row["anchor"], row.get("anchor2") or "", row.get("claim", "")]))
    print(f"  {row['lid']} {th} conf={row['confidence']} refs={row['refs']} members={[(m['reviewer_id'], m['fid']) for m in row['members']]}")
