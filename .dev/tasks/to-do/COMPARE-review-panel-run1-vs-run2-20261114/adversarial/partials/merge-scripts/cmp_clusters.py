import re, json
from pathlib import Path

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial")
text = (ROOT / "diff-analysis.md").read_text().splitlines()
idmap = json.loads((ROOT / "partials/id-map.json").read_text())
rev = {v: k for k, v in idmap.items()}

# parse rows: id -> (title, severity, section)
rows = {}
sec = None
for l in text:
    if l.startswith("## "):
        sec = l[3:].split()[0]
    if l.startswith("### Contradiction verification"):
        sec = "verifskip"
    m = re.match(r"^\| ([SCXUA]-\d{3}) \[src ([^\]]+)\] \| (.*)$", l)
    if m and sec in ("Structural", "Content", "Contradictions", "Unique", "Shared"):
        i = m.group(1)
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", m.group(3))]
        if i in rows:
            continue
        if cells and cells[-1] == "":
            cells = cells[:-1]
        title = cells[0][:90] if cells else ""
        last = cells[-1] if sec != "Shared" else (cells[-2] if len(cells) > 1 else "")
        sv = re.match(r"\W*(High|Medium|Low)", cells[-1] if sec != "Shared" else cells[-2], re.I)
        promoted = (cells[-1] == "Yes") if sec == "Shared" else None
        rows[i] = dict(title=title, sev=sv.group(1).capitalize() if sv else "?", src=m.group(2), promoted=promoted)

def ids(prefix, *spec):
    out = []
    for s in spec:
        if isinstance(s, tuple):
            for n in range(s[0], s[1] + 1):
                out.append(f"{prefix}-{n:03d}")
        else:
            out.append(f"{prefix}-{s:03d}")
    return out

C = {}
def cl(cid, name, level, pts):
    C[cid] = dict(name=name, level=level, pts=pts)

cl("CL-01", "Core shape and engine boundary (one superset core vs thin shared contract plus per-module engines)", "L2",
   ids("S", 40) + ids("C", 5, 50, 61, 76, 90) + ids("X", 2, 38, 42, 51))
cl("CL-02", "Finding contract, location types (anchor vs citations), PR fields, brief/input contract", "L2",
   ids("C", 51, 53, 66, 88) + ids("X", 7, 59))
cl("CL-03", "Over-length lines, truncation, claim cut and itemised drop record", "L3",
   ids("C", 52, 77) + ids("X", 40, 56))
cl("CL-04", "Who decides blocking; quorum; blind grader; calibration; exit codes", "L3",
   ids("C", 11, 54, 56, 65, 78, 80, 87) + ids("X", 3, 4, 6, 39, 55, 58))
cl("CL-05", "Ledger rounds, clearing by silence, verdict derivation, verdict contract", "L3",
   ids("C", 55, 63, 64, 79, 85) + ids("X", 44, 46))
cl("CL-06", "Dispatch, identity, tier data, environments, read-only enforcement", "L2",
   ids("C", 12, 37, 38, 58, 59, 67, 82) + ids("X", 9, 45))
cl("CL-07", "Panel resolver distinctness default (soft vs declared per slot)", "L3",
   ids("C", 60, 81) + ids("X", 41, 57))
cl("CL-08", "Run record, manifest, telemetry (manifest vs events.jsonl; telemetry producer)", "L2",
   ids("C", 34, 57, 83) + ids("X", 10))
cl("CL-09", "Reflect Tier 2 engines (fix ensemble.py now vs freeze), shadow exit, contract writer", "L3",
   ids("C", 10, 17, 18, 20, 21, 22, 23, 24, 25, 62, 84) + ids("X", 43, 54))
cl("CL-10", "Consumers and entry points (tasklist/workflow, PR review, rf-qa, future exposures)", "L2",
   ids("S", 21) + ids("C", 6, 14, 40, 41, 68, 69, 86, 89) + ids("X", 5, 47, 60))
cl("CL-11", "E2 collaboration designs and process-redesign brainstorms", "L2",
   ids("S", 18) + ids("C", 2, 28, 72, 91))
cl("CL-12", "Installed-only E3 variants and experiment evidence", "L2",
   ids("S", 23) + ids("C", 30, 31, 71, 94) + ids("X", 34) + ["A-019"])
cl("CL-13", "Evaluation, acceptance, ground truth, E1/E2 evidence independence", "L2",
   ids("S", 20) + ids("C", 13, 26, 27, 29, 43, 70, 92) + ids("X", 21, 25, 26))
cl("CL-14", "Decisions only one report treats as an axis (panel size and cost, calibration, clustering, identity check)", "L2",
   ids("S", 45) + ids("C", 73, 93))
cl("CL-15", "Severity ratings of agreed facts and application of rule C8 (Critical vs Important)", "L1",
   ids("C", 3, 9) + ids("X", (11, 19)) + ["A-008"])
cl("CL-16", "Evidence baseline: E2 pin, HEAD, scope slices, line-number freshness", "L2",
   ids("S", 15, 16, 41) + ids("C", 1) + ids("X", 1, 62, 63) + ["A-002", "A-024", "A-036", "A-037", "A-055"])
cl("CL-17", "Section 6 method: conflict classification, debates run, status taxonomy, tiebreaker winners", "L2",
   ids("S", (32, 39), 43, 44, 55) + ids("C", 74, 75, 97) + ids("X", 52) + ["A-052"])
cl("CL-18", "Fact disputes settled by code or data (KeyError path, 1,398, census counts, key counts, timeouts, calibrator)", "L3",
   ids("X", 20, 22, 23, 24, 27, 28, 29, 30, 31, 32, 33, 48, 49, 50, 53, 61) + ["A-057"])
cl("CL-19", "Section 7 shape and the adjudication-override layer between Sections 3/4 and 7", "L2",
   ids("S", 7, 13, 46, 54) + ids("C", 4, 95))
cl("CL-20", "Section 8 form (migration plan vs inputs for a later plan) and the value inventory", "L2",
   ids("S", 47, 48, 49, 56) + ids("C", 96) + ["A-056", "A-059"])
cl("CL-23", "Section 5 external research (source sets, severity, calibration, fingerprinting, runtime and git topics)", "L2",
   ids("S", (27, 31)) + ids("C", (44, 49)) + ids("X", 35, 36, 37))
cl("CL-24", "Sections 9 and 10, open questions, id namespaces, appendices", "L1",
   ids("S", 50, 51, 52, 53) + ids("C", 16) + ["A-006", "A-012", "A-058"])

assigned = {}
for cid, d in C.items():
    for p in d["pts"]:
        if p in assigned:
            raise SystemExit(f"DUP {p}: {assigned[p]} and {cid}")
        assigned[p] = cid

# defaults for residual points
def default_cluster(i):
    src = rows[i]["src"]
    part = re.match(r"[SCXUA]-([ABCD])-(\d+)", src)
    pl, num = part.group(1), int(part.group(2))
    k = i[0]
    if pl == "A":
        return "CL-21"
    if pl == "B":
        sec5 = {"S": range(13, 18), "C": range(25, 31), "X": range(12, 15), "A": range(11, 14)}
        return "CL-23" if num in sec5.get(k, range(0)) else "CL-22"
    if pl == "C":
        return "CL-25"
    return "CL-26"

names_default = {
    "CL-21": ("Sections 1, 3 and 4: structure, target-state layout, gap-table design (residual)", "L1"),
    "CL-22": ("Section 2 organisation and evidence depth (residual)", "L1"),
    "CL-25": ("Section 6 residual points not in a topical cluster", "L2"),
    "CL-26": ("Sections 7 to 10 residual points not in a topical cluster", "L2"),
}
for cid, (n, lv) in names_default.items():
    C[cid] = dict(name=n, level=lv, pts=[])

debate_pts = [i for i in rows if i[0] in "SCX"] + [i for i in rows if i[0] == "A" and rows[i]["promoted"]]
for i in debate_pts:
    if i not in assigned:
        c = default_cluster(i)
        assigned[i] = c
        C[c]["pts"].append(i)

# Clusters CL-23 may have got default points too
order = sorted(C)
tot = 0
lines = []
lines.append("# Debate Points and Clusters (Step 2 input)\n")
lines.append("Generated from `diff-analysis.md`. Skill formula: total diff points = S + C + X + promoted A. Clusters group related points so two advocates can debate 234 points in a bounded number of rounds; every point belongs to exactly one cluster. Unique contributions (U) are not diff points under the skill; they are handled in the U-register at the end.\n")
nS = sum(1 for i in debate_pts if i[0] == "S"); nC = sum(1 for i in debate_pts if i[0] == "C"); nX = sum(1 for i in debate_pts if i[0] == "X"); nA = sum(1 for i in debate_pts if i[0] == "A")
lines.append(f"- Debate points: {len(debate_pts)} (S {nS}, C {nC}, X {nX}, promoted A {nA})")
lines.append(f"- Clusters: {len(order)}")
lines.append("- Taxonomy level is tagged per cluster (L1 surface/format/rating; L2 structural/architecture/organisation; L3 state mechanics: guards, quorum, ledger state, invariants, verified code facts). Per skill, each point has exactly one level; a point inherits its cluster level.")
lv = {"L1": 0, "L2": 0, "L3": 0}
for c in order:
    lv[C[c]["level"]] += len(C[c]["pts"])
lines.append(f"- Points per level: L1 {lv['L1']}, L2 {lv['L2']}, L3 {lv['L3']}")
lines.append("")
lines.append("## Cluster table\n")
lines.append("| Cluster | Level | Topic | #pts | Member points (id: short title [severity]) |")
lines.append("|---|---|---|---|---|")
for c in order:
    pts = sorted(C[c]["pts"], key=lambda p: ("SCXA".index(p[0]), p))
    mem = "; ".join(f"{p}: {rows[p]['title'][:60].replace('|','/')} [{rows[p]['sev']}]" for p in pts)
    lines.append(f"| {c} | {C[c]['level']} | {C[c]['name']} | {len(pts)} | {mem} |")
lines.append("")
lines.append("## Promoted shared assumptions (answer ACCEPT / REJECT / QUALIFY)\n")
for i in debate_pts:
    if i[0] == "A":
        lines.append(f"- {i}: {rows[i]['title']} (cluster {assigned[i]})")
lines.append("")
lines.append("## U-register (unique contributions; for retention in the merge)\n")
lines.append("| id | Variant | Value | Contribution (short) |")
lines.append("|---|---|---|---|")
for i in sorted(k for k in rows if k[0] == "U"):
    r = rows[i]
    lines.append(f"| {i} | (see diff-analysis) | {r['sev']} | {r['title']} |")
(ROOT / "debate-points.md").write_text("\n".join(lines) + "\n")
json.dump(assigned, open(ROOT / "partials/point-cluster.json", "w"), indent=1)
print(len(debate_pts), {c: len(C[c]['pts']) for c in order}, lv)
