"""Collect every blocking finding (first reviews + audits) from all arms into p17/findings.jsonl."""
import sys, glob, pathlib, json, re
sys.path.insert(0, 'central'); import score_themes as sc
R = '.dev/orca-command-refactor/review/'
rows = []
def add(kind, arm, run, step, f):
    for x in sc.blocking_findings(f):
        rows.append({"kind": kind, "arm": arm, "run": run, "step": step, "fid": x["id"], "heading": (x["heading"] or "")[:300], "body": x["body"] or "", "cited": sorted(x["cited"]), "theme": x["theme"], "file": str(f)})
ARMS = [("stage2", "p11/runs/a3-r*", None), ("ab1", "p12/ab1/runs/b1-r*", None), ("ab1h", "p12/ab1/runs/b1h-r*", None), ("ab2", "p12/ab2/runs/b2-r*", None),
        ("ab2h", "p12/ab2/runs/b2h-r*", None), ("ab3", "p12/ab3/runs/b3-r*", None), ("ab3h", "p12/ab3/runs/b3h-r*", None), ("pn1", "p13/ab1/runs/b1-r*", None),
        ("pn2", "p13/ab2/runs/l2-r*", None), ("base-fresh", "p16/base-drift/runs/a3d-r*", None), ("ab4", "p16/ab4/runs/d4-r*", None), ("ab4h", "p16/ab4/runs/d4h-r*", None),
        ("haiku-base", "p14/haiku-baseline/runs/a3-r*", None)]
for arm, pat, _ in ARMS:
    for rd in sorted(glob.glob(pat)):
        run = pathlib.Path(rd).name
        for sub in ("aud", "aud2"):
            f = pathlib.Path(rd) / sub / "ws" / R / "audit.md"
            if f.exists(): add("audit", arm, run, sub, f)
        # first reviews: single-reviewer arms write round1.md/spec-panel.md in ws; k>1 arms write r1a/r1b/r1c sandboxes
        for sub in ("r1a", "r1b", "r1c"):
            f = pathlib.Path(rd) / sub / "ws" / R / "round1.md"
            if f.exists(): add("first", arm, run, sub, f)
        for name in ("round1.orig.md", "round1.md", "spec-panel.md"):
            f = pathlib.Path(rd) / "ws" / R / name
            if f.exists() and not (pathlib.Path(rd) / "r1a").exists():
                add("first", arm, run, "r1", f); break
for rd in sorted(glob.glob("p12/baseline-audit2/a3-r*")):
    f = pathlib.Path(rd) / "ws" / R / "audit.md"
    if f.exists(): add("audit", "stage2", pathlib.Path(rd).name, "aud2", f)
with open("p17/findings.jsonl", "w") as o:
    for i, r in enumerate(rows): r["gid"] = i; o.write(json.dumps(r) + "\n")
import collections
print(len(rows), collections.Counter((r["kind"]) for r in rows), collections.Counter(r["arm"] for r in rows))
