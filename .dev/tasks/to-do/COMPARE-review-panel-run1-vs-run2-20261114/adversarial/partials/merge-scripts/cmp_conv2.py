import re, sys, json
from pathlib import Path

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial")
P = ROOT / "partials"
pc = json.loads((P / "point-cluster.json").read_text())
points = list(pc)

def norm(w):
    w = w.strip().strip("*").upper()
    m = re.match(r"(V1|V2|BOTH|MERGE|NEITHER|OPEN)", w)
    return m.group(1) if m else None

def parse_r1(path):
    cluster, point = {}, {}
    for l in path.read_text().splitlines():
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
            cluster[m.group(1)] = norm(cs[1]); continue
        ids = re.findall(r"\b([SCXA]-\d{3})\b", cs[0]); w = norm(cs[1])
        if ids and w:
            for i in ids:
                point[i] = w
    return cluster, point

def overlay_r2(path, cluster, point):
    sec = None
    for l in path.read_text().splitlines():
        if l.startswith("## "):
            sec = l
            continue
        if not l.startswith("|"):
            continue
        cs = [c.strip() for c in l.strip().strip("|").split("|")]
        if "Final verdicts" in (sec or "") and len(cs) >= 2:
            ids = re.findall(r"\b([SCXA]-\d{3})\b", cs[0]); w = norm(cs[1])
            if ids and w:
                for i in ids:
                    point[i] = w
        elif "Verdict changes" in (sec or "") and len(cs) >= 3:
            w = norm(cs[2])
            if not w:
                continue
            m = re.match(r"(CL-\d+)", cs[0])
            if m:
                cluster[m.group(1)] = w
            for i in re.findall(r"\b([SCXA]-\d{3})\b", cs[0]):
                point[i] = w
    return cluster, point

state = {}
for k in ("V1", "V2"):
    c, p = parse_r1(P / f"r1-advocate-{k}.md")
    c, p = overlay_r2(P / f"r2-advocate-{k}.md", c, p)
    if k == "V1":
        # r2-advocate-V1.md:116: "V1 on the post gate; BOTH on the rest" for CL-09
        for i in ("C-020", "C-021", "C-024"):
            p[i] = "BOTH"
    state[k] = (c, p)

def eff(k, i):
    c, p = state[k]
    if i in p:
        return p[i]
    return c.get(pc[i])

agree, dis, unk = [], [], []
for i in points:
    a, b = eff("V1", i), eff("V2", i)
    if a is None or b is None:
        unk.append(i); continue
    ok = (a == b) or ({a, b} <= {"BOTH", "MERGE"})
    (agree if ok else dis).append((i, a, b))

out = [f"# Convergence snapshot after R2\n",
       f"- Debate points: {len(points)}; agreed: {len(agree)}; disagree: {len(dis)}; no verdict from one side: {len(unk)}",
       f"- Convergence = agreed / total = {len(agree)/len(points):.3f}\n",
       "## Points where the advocates still disagree after Round 2\n",
       "| Point | Cluster | V1 advocate | V2 advocate |", "|---|---|---|---|"]
for i, a, b in dis:
    out.append(f"| {i} | {pc[i]} | {a} | {b} |")
if unk:
    out.append("\n## No verdict: " + ", ".join(unk))
(P / "convergence-r2.md").write_text("\n".join(out) + "\n")
json.dump({"V1": {"point": state["V1"][1], "cluster": state["V1"][0]}, "V2": {"point": state["V2"][1], "cluster": state["V2"][0]}, "disagree": [d[0] for d in dis]}, open(P / "r2-state.json", "w"), indent=1)
print(len(points), len(agree), len(dis), len(unk), f"{len(agree)/len(points):.3f}")
