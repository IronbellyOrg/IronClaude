import json, re, sys
base = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/"
S = base + "source.md"; P = base + "TASK-WF-designSpec-20261107-075614.md"
out = sys.argv[1]
spec = open(S).read().split("\n"); plan = open(P).read().split("\n")
# task sections "## Task N:"
secs = []; cur = None
for i, l in enumerate(plan, 1):
    m = re.match(r"## (Task \d+):", l)
    if m: cur = [m.group(1), i, []]; secs.append(cur)
    elif l.startswith("## ") and cur: cur = None
    if cur: cur[2].append(l)
stop = set("a an the and or but of to in on at for from by with as is are was were be been being it its this that these those not no nor so if then than also into over under after before when while which who whom whose can may must should shall will would does do did has have had".split())
def cw(t): return [w for w in re.findall(r"[a-z0-9_]+", t.lower()) if len(w) > 1 and w not in stop]
secw = {s[0]: set(cw("\n".join(s[2]))) for s in secs}
rows = []; bad = []
for n, raw in enumerate(open(out + "/artifacts/inf-rows.txt").read().strip().split("\n"), 1):
    ln, q = raw.split("|||", 1); ln = int(ln)
    if q not in spec[ln - 1]: bad.append((n, ln, q)); continue
    w = set(cw(q)); best = ("none", 0.0)
    for name, sw in secw.items():
        r = len(w & sw) / len(w) if w else 0
        if r > best[1] + 1e-12: best = (name, r)
    ok = best[1] >= 0.6
    rows.append({"requirement_id": "INF-%03d" % n, "source": "inferred", "quote": q,
      "citation": S + ":%d" % ln, "matched_task_ids": [best[0]] if ok else [],
      "match_method": "containment" if ok else "none", "best_ratio": round(best[1], 4)})
if bad:
    print("QUOTE MISMATCH", bad); sys.exit(1)
tot = len(rows); m = sum(1 for r in rows if r["matched_task_ids"])
un = [r["requirement_id"] for r in rows if not r["matched_task_ids"]]
res = {"parsed_total": 0, "parsed_matched": 0, "inferred_total": tot, "inferred_matched": m,
 "coverage_pct": None, "coverage_pct_union": round(m / tot, 4), "unmapped_requirements": [],
 "unmapped_requirements_union": un, "coverage_degraded": "parsed-sparse" if tot > 0 else None,
 "S_dev_density": round(len(un) / tot, 4),
 "rule": "containment >=0.6 content-word ratio vs one '## Task N' section; stopwords stripped, tokens [a-z0-9_]+ len>1; ties first-in-order",
 "rows": rows}
json.dump(res, open(out + "/artifacts/coverage-matrix.json", "w"), indent=1)
print(tot, m, res["coverage_pct_union"], un, res["S_dev_density"])
