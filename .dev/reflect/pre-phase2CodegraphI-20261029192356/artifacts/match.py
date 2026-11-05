"""Deterministic containment matcher (refs/coverage-mapping.md stage 3, INF rows).

usage: match.py <tasklist.md> <inferred-requirements.yaml> <out-matrix.yaml>
"""
import re
import sys

import yaml

STOP = set("""a an the and or but nor so yet for of to in on at by with from into onto over under
as is are was were be been being am do does did has have had will would shall should can could may might must
it its this that these those than then there here which who whom whose what when where why how not no
if else each every all any both either neither per via own such same other only also just very""".split())


def words(text):
    return [w for w in re.findall(r"[a-z0-9_]+", text.casefold()) if w not in STOP]


tl_text = open(sys.argv[1]).read()
tasks = []
for m in re.finditer(r"^## Task (\d+):(.*?)(?=^## Task \d+:|^## Phase |\Z)", tl_text, re.S | re.M):
    tasks.append((f"Task {m.group(1)}", set(words(m.group(2)))))
constraints = re.search(r"^## Constraints(.*?)(?=^## Phase )", tl_text, re.S | re.M)
if constraints:
    tasks.append(("Constraints", set(words(constraints.group(1)))))

rows = yaml.safe_load(open(sys.argv[2]))["rows"]
matrix, matched = [], 0
for r in rows:
    w = words(r["quote"])
    best, ratio = None, 0.0
    for tid, tw in tasks:
        if not w:
            break
        rr = sum(1 for x in w if x in tw) / len(w)
        if rr > ratio:
            best, ratio = tid, rr
    hit = ratio >= 0.6
    matched += hit
    matrix.append({"requirement_id": r["id"], "section": r.get("section"), "citation": r["citation"],
                   "matched_task_ids": [best] if hit else [], "ratio": round(ratio, 4),
                   "match_method": "containment" if hit else "none", "source": "inferred"})
total = len(rows)
out = {"parsed_total": 0, "inferred_total": total, "matched": matched,
       "coverage_pct": None, "coverage_pct_union": round(matched / total, 4) if total else None,
       "unmapped_requirements": [], "unmapped_requirements_union": [m["requirement_id"] for m in matrix if not m["matched_task_ids"]],
       "coverage_degraded": "parsed-sparse" if total > 0 else None, "matrix": matrix}
yaml.safe_dump(out, open(sys.argv[3], "w"), sort_keys=False, width=200)
print(f"total={total} matched={matched} union={out['coverage_pct_union']} unmapped={len(out['unmapped_requirements_union'])}")
