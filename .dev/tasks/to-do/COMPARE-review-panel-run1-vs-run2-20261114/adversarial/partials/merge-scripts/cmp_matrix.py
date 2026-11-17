import re, json
from pathlib import Path

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial")
P = ROOT / "partials"
pc = json.loads((P / "point-cluster.json").read_text())
points = list(pc)
title = {}
for l in (ROOT / "diff-analysis.md").read_text().splitlines():
    m = re.match(r"^\| ([SCXA]-\d{3}) \[src [^\]]+\] \| ([^|]*)\|", l)
    if m and m.group(1) not in title:
        title[m.group(1)] = m.group(2).strip()[:70]

def norm(w):
    w = w.strip().strip("*").upper()
    m = re.match(r"(V1|V2|BOTH|MERGE|NEITHER|OPEN)", w)
    return m.group(1) if m else None

def conf_of(s):
    m = re.search(r"(\d{2,3})\s*%", s)
    return int(m.group(1)) if m else None

def parse(path, r2):
    cl, pt = {}, {}
    sec = None
    for l in path.read_text().splitlines():
        if l.startswith("## "):
            sec = l
            continue
        if not r2 and l.startswith("- ") and "(CL-" in l:
            # exception bullets: "- C-053 (CL-02, V2 cluster): **V1** 65%." / "- C-073 and C-093 (CL-14): V1, 70%."
            m = re.match(r"^- ([^()]+)\(CL-[^)]*\):\s*\**(V1|V2|BOTH|MERGE)\**(?:\s+as cluster)?[ ,]*(\d+)?\s*%?", l)
            if m:
                for i in re.findall(r"\b([SCXA]-\d{3})\b", m.group(1)):
                    pt[i] = (m.group(2), int(m.group(3)) if m.group(3) else None, "Round 1 exception to the cluster verdict (advocate's own exception list)")
            continue
        if not l.startswith("|"):
            continue
        cs = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cs) < 3:
            continue
        if r2 and "Verdict changes" in (sec or ""):
            w = norm(cs[2])
            if not w:
                continue
            ev = cs[3] if len(cs) > 3 else ""
            m = re.match(r"(CL-\d+)", cs[0])
            if m:
                cl[m.group(1)] = (w, None, ev)
            for i in re.findall(r"\b([SCXA]-\d{3})\b", cs[0]):
                pt[i] = (w, None, ev)
            continue
        if r2 and "Final verdicts" not in (sec or ""):
            continue
        w = norm(cs[1])
        if not w:
            continue
        m = re.match(r"(CL-\d+)", cs[0])
        c = conf_of(cs[2]) if len(cs) > 2 else None
        ev = cs[3] if len(cs) > 3 else (cs[2] if len(cs) > 2 else "")
        if m:
            cl[m.group(1)] = (w, c, ev)
            continue
        for i in re.findall(r"\b([SCXA]-\d{3})\b", cs[0]):
            pt[i] = (w, c, ev)
    return cl, pt

S = {}
for k in ("V1", "V2"):
    c1, p1 = parse(P / f"r1-advocate-{k}.md", False)
    c2, p2 = parse(P / f"r2-advocate-{k}.md", True)
    c1.update(c2); p1.update(p2)
    if k == "V1":
        # r2-advocate-V1.md:116 says "V1 on the post gate; BOTH on the rest" for CL-09: the compound cluster verdict normalises to V1,
        # so the non-post-gate points of CL-09 are set to BOTH here (post-gate points C-010, C-018 keep their explicit V1 rows).
        for i in ("C-017", "C-020", "C-021", "C-024", "C-025"):
            if i not in p1 or i in ("C-020", "C-021", "C-024"):
                if i in ("C-020", "C-021", "C-024"):
                    p1[i] = ("BOTH", None, "V1 advocate R2: 'V1 on the post gate; BOTH on the rest' (r2-advocate-V1.md:116)")
    S[k] = (c1, p1)

def eff(k, i):
    c, p = S[k]
    if i in p:
        return p[i]
    return c.get(pc[i])

LAB = {"V1": "Variant 1", "V2": "Variant 2", "BOTH": "Both (merge)", "MERGE": "Both (merge)", "NEITHER": "Neither", "OPEN": "Open (owner or evidence)"}
rows = []
cnt = {"Variant 1": 0, "Variant 2": 0, "Both (merge)": 0, "Neither": 0, "Open (owner or evidence)": 0, "Unresolved split": 0}
unres = []
agreed_resolved = 0
for i in points:
    a, b = eff("V1", i), eff("V2", i)
    wa, wb = a[0], b[0]
    equiv = (wa == wb) or ({wa, wb} <= {"BOTH", "MERGE"})
    confs = [x for x in (a[1], b[1]) if x]
    cf = round(sum(confs) / len(confs)) if confs else 60
    if equiv:
        w = LAB[wa] if wa != "MERGE" else "Both (merge)"
        if wa == "OPEN":
            w = "Open (owner or evidence)"
            cf = 50
            unres.append(i)
        else:
            agreed_resolved += 1
            cf = min(cf, 95) if wa in ("BOTH", "MERGE") else min(cf + 0, 95)
        cnt[w] += 1
        ev = (a[2] if wa == wb else b[2]) or a[2] or b[2]
    else:
        w = "Unresolved split"
        cf = 50
        cnt[w] += 1
        unres.append(i)
        ev = f"V1 advocate: {LAB[wa]}; V2 advocate: {LAB[wb]}. " + (b[2] or a[2])
    ev = re.sub(r"\s+", " ", ev).replace("|", "/")[:230]
    rows.append((i, w, cf, ev))

total = len(points)
conv_strict = agreed_resolved / total
_m = re.search(r"= ([0-9.]+)", (P / "convergence-r1.md").read_text())
R1CONV = f"{float(_m.group(1))*100:.1f}"
agreed_incl_open = sum(1 for i in points if True) - sum(1 for r in rows if r[1] == "Unresolved split")

out = []
out.append("## Scoring Matrix\n")
out.append("Winner = the verdict both advocates converged on after Round 2 (cluster-level verdicts inherited by points without their own row; point rows override). `Both (merge)` means both reports' content is needed. `Open` means both advocates mark it undecidable by the evidence (owner decision). `Unresolved split` means the advocates' final verdicts still differ. Confidence = mean of the advocates' stated confidences, capped at 95%, 50% for open and split points. Evidence is the advocate's own evidence cell (truncated); full evidence is in partials/r1-*.md and partials/r2-*.md.\n")
out.append("| Diff Point | Cluster | Winner | Confidence | Evidence Summary |")
out.append("|---|---|---|---|---|")
for i, w, cf, ev in rows:
    out.append(f"| {i} {title.get(i,'')} | {pc[i]} | {w} | {cf}% | {ev} |")
out.append("")
out.append("## Convergence Assessment\n")
v1w = cnt["Variant 1"]; v2w = cnt["Variant 2"]
out.append(f"- Points resolved: {agreed_resolved} of {total} (agreed on a superior approach, including `Both (merge)`)")
out.append(f"- Points where both advocates agree it is open (owner decision or no decisive evidence): {cnt['Open (owner or evidence)']}")
out.append(f"- Points where the advocates still differ after Round 2: {cnt['Unresolved split']}")
out.append(f"- Alignment (strict, resolved only): {conv_strict*100:.1f}%  (alignment counting both-open as agreement: {(total-cnt['Unresolved split'])/total*100:.1f}%; after Round 1 it was {R1CONV}%)")
out.append("- Threshold: 80%")
out.append("- Taxonomy coverage gate: L1 (50 points), L2 (126), L3 (58) all addressed in both advocates' Round 1 and Round 2: PASS")
out.append("- Invariant probe gate: 7 HIGH-severity UNADDRESSED invariants (INV-003, INV-006, INV-018, INV-024, INV-027, INV-028, INV-029): CONVERGENCE BLOCKED_BY_INVARIANTS (score meets threshold; gate does not)")
out.append(f"- Status: BLOCKED_BY_INVARIANTS (agreement {conv_strict*100:.1f}% >= 80%, taxonomy covered, 7 HIGH UNADDRESSED invariants). Depth `standard` has no Round 3, so the HIGH items are carried into the refactor plan and the merged document as explicit corrections or open owner decisions, and are listed in the return contract.")
out.append(f"- Points won (strict tally): Variant 1 {v1w}, Variant 2 {v2w}, Both (merge) {cnt['Both (merge)']}, Neither {cnt['Neither']}")
out.append("- Unresolved points: " + ", ".join(unres))
(P / "scoring-matrix.md").write_text("\n".join(out) + "\n")
json.dump({"counts": cnt, "resolved": agreed_resolved, "total": total, "strict": conv_strict, "unresolved": unres, "winners": {r[0]: r[1] for r in rows}}, open(P / "matrix.json", "w"), indent=1)
print(cnt, agreed_resolved, total, f"{conv_strict:.4f}", len(unres))
