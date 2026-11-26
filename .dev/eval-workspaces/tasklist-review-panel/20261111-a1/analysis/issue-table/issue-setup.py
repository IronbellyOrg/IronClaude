"""Build the issue legend (I#/B# labels) and the top-10 panel -> rows map for the per-panel issue table."""
import json, collections
exec(open("/tmp/final-table.py").read().split("def metrics")[0])  # E, PK, DS, AL, DE, GT, SH, valid, excl
import glob, os, statistics as st
# legend: blocking_in_implement true -> B, false -> I; ordered designSpec, alias, control
leg = []; bn = 0; inn = 0
for p, tag in ((DS, "designSpec"), (AL, "alias"), (DE, "control")):
    gt = json.load(open(f"{E}/{p}/ground-truth.json"))["items"]
    for it in gt:
        if it["blocking_in_implement"]: bn += 1; lab = f"B{bn}"
        else: inn += 1; lab = f"I{inn}"
        leg.append(dict(label=lab, package=tag, pkg_id=p, gt=it["id"], blocking=it["blocking_in_implement"], description=it["description"][:260]))
json.dump(leg, open("/tmp/issue-legend.json", "w"), indent=1)
with open("/tmp/issue-legend.tsv", "w") as f:
    f.write("label\tpackage\tgt_id\tblocking\tdescription\n")
    for l in leg: f.write(f"{l['label']}\t{l['package']}\t{l['gt']}\t{l['blocking']}\t{l['description']}\n")
# rows per panel (model multiset), valid era only, with all 3 packages scored
fam = collections.defaultdict(list)
for row in sorted(os.listdir(f"{E}/combos")):
    if not valid(row): continue
    ms = []
    for mf in sorted(glob.glob(f"{E}/{DS}/reviews/combos/{row}/t*.meta.json")):
        if "attempt" in mf: continue
        ms.append(SH.get(json.load(open(mf))["expected_model"], "?"))
    if all(glob.glob(f"{E}/arms/scoring/combos/{row}/{p}/*/score.json") for p in PK): fam[tuple(sorted(ms))].append(row)
def meanany(rows):
    v = []
    for r in rows:
        t = 0
        for p in (DS, AL): t += len(json.load(open(glob.glob(f"{E}/arms/scoring/combos/{r}/{p}/*/score.json")[0]))["gt_covered_any"])
        v.append(t)
    return st.mean(v)
cand = [(k, rows, meanany(rows)) for k, rows in fam.items() if len(rows) >= 4]
cand.sort(key=lambda x: -x[2])
top = [dict(panel=" + ".join(k), models=list(k), rows=rows, n=len(rows), mean_found=round(m, 2)) for k, rows, m in cand[:10]]
json.dump(top, open("/tmp/top10.json", "w"), indent=1)
print(open("/tmp/issue-legend.tsv").read())
for t in top: print(t["panel"], t["n"], t["mean_found"], t["rows"])
print("all replicated panels:", len(cand)); print("next:", [(" + ".join(k), len(r), round(m, 2)) for k, r, m in cand[10:13]])
