"""Pilot analysis: Jev (Noul and Choice) vs ledger labels on cross-reviewer pairs of two 7-reviewer runs, and Jev as a splitter of the merge's rows."""
import json, itertools, collections, sys
from truth import F, lab, pair_truth, pairs
A = json.load(open("answers.json"))
WHO = sys.argv[1] if len(sys.argv) > 1 else "sonnet"
def pid(a, b): return f"{a['key']}~{b['key']}"
def nou(a, b): return A[f"{pid(a,b)}|noul"].get("noul", 0)
def cho(a, b): return A[f"{pid(a,b)}|choice"].get("probs", {}).get("same_defect", 0)
def auc(pos, neg):
    return round(sum((x > y) + 0.5 * (x == y) for x in pos for y in neg) / (len(pos) * len(neg)), 3)
runs = ("d2-r1", "d2-r2") if WHO == "sonnet" else ("d2-r1",)
rows = []
for run in runs:
    L = lab(run, WHO)
    for a, b in pairs(run):
        rows.append((run, a, b, pair_truth(L, a, b)))
lab_rows = [r for r in rows if r[3] != "unknown"]
pos = [r for r in lab_rows if r[3] == "same"]; neg = [r for r in lab_rows if r[3] == "diff"]
print(f"labels: {WHO}; labelled pairs {len(lab_rows)} (same {len(pos)}, overlap {sum(r[3]=='overlap' for r in lab_rows)}, diff {len(neg)}); unknown {len(rows)-len(lab_rows)}")
print("AUC same vs diff: noul", auc([nou(a,b) for _,a,b,_ in pos], [nou(a,b) for _,a,b,_ in neg]), "| choice", auc([cho(a,b) for _,a,b,_ in pos], [cho(a,b) for _,a,b,_ in neg]))
def pr(flag):
    fl = [r for r in lab_rows if flag(r[1], r[2])]; tp = sum(r[3] == "same" for r in fl); tpo = sum(r[3] in ("same", "overlap") for r in fl)
    return f"flagged {len(fl):4d}  precision {tp/max(1,len(fl)):.2f} (same-or-overlap {tpo/max(1,len(fl)):.2f})  recall {tp/len(pos):.2f}"
print("merge row (current code)        ", pr(lambda a, b: a["merge_row"] and a["merge_row"] == b["merge_row"]))
for t in (0.5, 0.7, 0.9):
    print(f"jev noul >= {t}                 ", pr(lambda a, b, t=t: nou(a, b) >= t))
    print(f"merge row AND jev noul >= {t}   ", pr(lambda a, b, t=t: a["merge_row"] and a["merge_row"] == b["merge_row"] and nou(a, b) >= t))
print("jev choice = same_defect         ", pr(lambda a, b: A[f"{pid(a,b)}|choice"].get("choice") == "same_defect"))
# defects hidden behind a row: a merged row carries one claim; every extra distinct ledger defect in it is at risk
def hidden(groups, L):
    h = 0
    for g in groups:
        ds = {(L[f["key"]]["defects"] or [None])[0] for f in g} - {None}
        h += max(0, len(ds) - 1)
    return h
def split(rowfs, t):
    # connected components inside a merge row, linking only pairs Jev calls the same defect
    parent = {f["key"]: f["key"] for f in rowfs}
    def find(x):
        while parent[x] != x: x = parent[x]
        return x
    for a, b in itertools.combinations(rowfs, 2):
        if a["reviewer"] != b["reviewer"] and nou(a, b) >= t: parent[find(a["key"])] = find(b["key"])
    comps = collections.defaultdict(list)
    for f in rowfs: comps[find(f["key"])].append(f)
    return list(comps.values())
for run in runs:
    L = lab(run, WHO)
    byrow = collections.defaultdict(list)
    for f in F[run]:
        byrow[f["merge_row"] or f["key"]].append(f)
    ndef = len({(L[f['key']]['defects'] or [None])[0] for f in F[run]} - {None})
    print(f"\n{run}: {len(F[run])} findings, {ndef} distinct ledger defects; merge rows {len(byrow)}, defects hidden behind another defect's row {hidden(byrow.values(), L)}")
    for t in (0.5, 0.7, 0.9):
        groups = [g for rf in byrow.values() for g in split(rf, t)]
        print(f"   split rows with jev noul >= {t}: rows {len(groups)}, defects hidden {hidden(groups, L)}")
