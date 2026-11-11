#!/usr/bin/env python3
"""O3 prep: distinct flags per check (dedupe by quote+message over docs of groups orig/final/hist/ref/other),
sample 30 with random.Random(0) when a check has more than 60 distinct flags. usage: adj_prep.py LINTDIR OUTFILE"""
import json, os, glob, sys, random, pathlib, collections
AB = pathlib.Path(os.environ["AB"]); lintdir = pathlib.Path(sys.argv[1]); outf = sys.argv[2]
corpus = {r["sha256"]: r for r in json.load(open(AB/"offline/corpus.json"))}
GROUPS = ("orig", "final", "hist", "ref", "other")
distinct = collections.OrderedDict()  # (check, quote, message) -> rep
for rec in json.load(open(AB/"offline/corpus.json")):
    if rec["group"] not in GROUPS: continue
    d = json.load(open(lintdir/f"{rec['sha256']}.json"))
    for f in d["findings"]:
        key = (f["check"], f["quote"], f["message"])
        if key not in distinct:
            distinct[key] = {"check": f["check"], "doc_sha": rec["sha256"], "group": rec["group"], "path": rec["path"], "lint_id": f["lint_id"],
                              "lines": f["lines"], "other_lines": f["other_lines"], "quote": f["quote"], "message": f["message"], "n_docs": 0, "shas": []}
        distinct[key]["n_docs"] += 1; distinct[key]["shas"].append(rec["sha256"])
by_check = collections.defaultdict(list)
for v in distinct.values(): by_check[v["check"]].append(v)
sel = []; info = {}
for c, items in by_check.items():
    if len(items) > 60:
        picked = random.Random(0).sample(items, 30); info[c] = {"distinct": len(items), "sampled": 30}
    else:
        picked = items; info[c] = {"distinct": len(items), "sampled": len(items)}
    sel.extend(picked)
json.dump({"info": info, "flags": sel}, open(outf, "w"), indent=1)
print(json.dumps(info))
