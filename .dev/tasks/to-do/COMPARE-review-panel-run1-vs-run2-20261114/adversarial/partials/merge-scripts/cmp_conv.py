import re, sys, json
from pathlib import Path

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial")
rnd = sys.argv[1]  # r1 or r2
files = {"V1": ROOT / "partials" / f"{rnd}-advocate-V1.md", "V2": ROOT / "partials" / f"{rnd}-advocate-V2.md"}
pc = json.loads((ROOT / "partials/point-cluster.json").read_text())
points = list(pc)  # debate points (S, C, X, promoted A)

def norm(w):
    w = w.strip().strip("*").upper()
    m = re.match(r"(V1|V2|BOTH|MERGE|NEITHER|OPEN)", w)
    return m.group(1) if m else None

def parse(path):
    txt = path.read_text().splitlines()
    cluster, point, expl = {}, {}, {}
    for l in txt:
        if l.startswith("- ") and "(CL-" in l:
            mm = re.match(r"^- ([^()]+)\(CL-[^)]*\):\s*\**(V1|V2|BOTH|MERGE)\**", l)
            if mm:
                for i in re.findall(r"\b([SCXA]-\d{3})\b", mm.group(1)):
                    point[i] = mm.group(2)
            continue
        if not l.startswith("|"):
            continue
        cs = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cs) < 3:
            continue
        m = re.match(r"(CL-\d+)", cs[0])
        if m and norm(cs[1]):
            cluster[m.group(1)] = norm(cs[1])
            continue
        # point rows: may contain several ids joined e.g. "C-001, C-002" or ranges
        ids = re.findall(r"\b([SCXA]-\d{3})\b", cs[0])
        w = norm(cs[1])
        if ids and w:
            for i in ids:
                point[i] = w
    return cluster, point

cl, pt = {}, {}
for k, p in files.items():
    cl[k], pt[k] = parse(p)

# effective point winner = explicit point verdict else cluster verdict
def eff(k, i):
    if i in pt[k]:
        return pt[k][i], "explicit"
    c = pc[i]
    if c in cl[k]:
        return cl[k][c], "cluster"
    return None, None

agree, dis, unk = [], [], []
for i in points:
    a, sa = eff("V1", i); b, sb = eff("V2", i)
    if a is None or b is None:
        unk.append(i); continue
    equiv = (a == b) or ({a, b} <= {"BOTH", "MERGE"})
    (agree if equiv else dis).append((i, a, b, sa, sb))

out = []
out.append(f"# Convergence snapshot after {rnd.upper()}\n")
out.append(f"- Debate points: {len(points)}; agreed: {len(agree)}; disagree: {len(dis)}; no verdict from one side: {len(unk)}")
out.append(f"- Convergence = agreed / total = {len(agree)/len(points):.3f}\n")
out.append("## Cluster-level verdicts\n")
out.append("| Cluster | V1 advocate says | V2 advocate says |")
out.append("|---|---|---|")
for c in sorted(set(cl['V1']) | set(cl['V2'])):
    out.append(f"| {c} | {cl['V1'].get(c,'-')} | {cl['V2'].get(c,'-')} |")
out.append("\n## Points where the advocates disagree (winner by V1 advocate | by V2 advocate)\n")
out.append("| Point | Cluster | V1 advocate | V2 advocate |")
out.append("|---|---|---|---|")
for i, a, b, sa, sb in dis:
    out.append(f"| {i} | {pc[i]} | {a} ({sa}) | {b} ({sb}) |")
if unk:
    out.append("\n## Points with no verdict from at least one advocate\n")
    out.append(", ".join(unk))
(ROOT / "partials" / f"convergence-{rnd}.md").write_text("\n".join(out) + "\n")
print(len(points), len(agree), len(dis), len(unk), f"{len(agree)/len(points):.3f}")
