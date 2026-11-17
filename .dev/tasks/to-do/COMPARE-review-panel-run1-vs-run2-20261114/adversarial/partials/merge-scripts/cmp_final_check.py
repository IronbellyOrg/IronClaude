import re, hashlib, json
from pathlib import Path

B = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do")
O = B / "COMPARE-review-panel-run1-vs-run2-20261114"
A = O / "adversarial"
M = (O / "MERGED-review-panel-unification.md").read_text().splitlines()
mt = "\n".join(M)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
r1 = B / "TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md"
r2 = B / "TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md"
print("orig1==copy1", sha(r1) == sha(A / "variant-1-original.md"), "orig2==copy2", sha(r2) == sha(A / "variant-2-original.md"))
print("first lines:", [l[:90] for l in M[:5]])
h2 = [(i + 1, l) for i, l in enumerate(M) if l.startswith("## ")]
print("H2:", len(h2))
for i, l in h2: print(" ", i, l[:110])
# base subsequence check
base = (A / "partials/merge-stage/base-corrected.md").read_text().splitlines()
pos = 0
missing = []
idx = {}
for n, l in enumerate(M):
    idx.setdefault(l, []).append(n)
last = -1
for bi, l in enumerate(base):
    cand = [n for n in idx.get(l, []) if n > last]
    if not cand:
        missing.append((bi + 1, l[:80]))
        continue
    last = cand[0]
print("base lines not found in order:", len(missing))
for x in missing[:40]: print("   ", x)
# v1 blocks present contiguous
for f in sorted((A / "partials/merge-stage/v1-blocks").glob("*.md")):
    txt = f.read_text().strip("\n")
    print(f.name, "in merged:", txt in mt.replace("\r", ""), "lines", len(txt.splitlines()))
for f in sorted((A / "partials/merge-stage/new-blocks").glob("*.md")):
    txt = f.read_text().strip("\n")
    print(f.name, "in merged:", txt in mt, "lines", len(txt.splitlines()))
print("allowedTools hits:", [(i + 1, M[i][:140]) for i in range(len(M)) if "allowedTools" in M[i]][:20])
print("provenance comments:", sum(1 for l in M if "<!-- Source:" in l))
print("R1-CLS tokens:", len(re.findall(r"R1-CLS-\d\d", mt)), "bad closed:", len(re.findall(r"Closed item R1-C-|GQ:R1-C-", mt)))
