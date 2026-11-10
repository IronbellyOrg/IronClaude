#!/usr/bin/env python3
"""O1: build corpus.json (distinct documents by sha256, with every path and group)."""
import hashlib, json, pathlib, re, subprocess, glob, os
SP = pathlib.Path(os.environ["SP"]); CLONE = pathlib.Path(os.environ["CLONE"]); AB = pathlib.Path(os.environ["AB"])
ORIG = SP/"exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
D = ".dev/orca-command-refactor"
entries = []  # (path, group, label)
entries.append((ORIG, "orig", "orig"))
for p in sorted(glob.glob(str(SP/f"p11/runs/*/ws/{D}/specs/orca-worker-contract-spec.md"))):
    run = pathlib.Path(p).parts[-6]
    entries.append((pathlib.Path(p), "final", run))
for p in sorted(glob.glob(str(SP/f"p11/runs/*/ws/{D}/specs/history/spec-v*.md"))):
    run = pathlib.Path(p).parts[-7]
    entries.append((pathlib.Path(p), "hist", f"{run}/{pathlib.Path(p).name}"))
for n in ("spec-v2-after-round1.md", "spec-v3-after-round2.md", "spec-v4-after-round3.md"):
    entries.append((SP/"exp346/.dev/experiments/346-validation/phase2/S1/inputs/reference-snapshots"/n, "ref", n))
for n in ("seeded", "cand_deletion", "cand_regression"):
    entries.append((SP/f"p5/docs/{n}.md", "pos", n))
for n in ("clean", "minor"):
    entries.append((SP/f"p5/docs/{n}.md", "clean", n))
# other: 10 largest tracked docs/*.md with >= 3 numbered headings
tracked = subprocess.run(["git", "-C", str(CLONE), "ls-files", "docs/*.md", "docs/**/*.md"], capture_output=True, text=True).stdout.split()
numbered = re.compile(r"^#{1,6}\s+\d+(?:\.\d+)*[.\s]", re.M)
cands = []
for t in sorted(set(tracked)):
    p = CLONE/t
    if p.is_file():
        txt = p.read_text(errors="replace")
        if len(numbered.findall(txt)) >= 3:
            cands.append((p.stat().st_size, t, p))
cands.sort(key=lambda x: (-x[0], x[1]))
for size, t, p in cands[:10]:
    entries.append((p, "other", t))

docs = {}  # sha -> record
order = []
for path, group, label in entries:
    assert path.exists(), path
    b = path.read_bytes(); sha = hashlib.sha256(b).hexdigest()
    if sha not in docs:
        docs[sha] = {"sha256": sha, "bytes": len(b), "group": group, "path": str(path), "paths": [], "labels": []}
        order.append(sha)
    r = docs[sha]
    r["paths"].append(str(path)); r["labels"].append(f"{group}:{label}")
    r.setdefault("groups", [])
    if group not in r["groups"]: r["groups"].append(group)
# 'group' = first group seen (orig wins over hist/final for the original text)
out = [docs[s] for s in order]
(AB/"offline/corpus.json").write_text(json.dumps(out, indent=1))
from collections import Counter
print(len(entries), "entries ->", len(out), "distinct documents")
print(Counter(r["group"] for r in out))
print("other:", [r["labels"][0] for r in out if r["group"] == "other"])
print("final entries:", sum(1 for _,g,_ in entries if g=="final"), "hist entries:", sum(1 for _,g,_ in entries if g=="hist"))
