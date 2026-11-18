"""Deterministic coverage map (sc:reflect Step 1B.0 / coverage-mapping.md). Usage: coverage.py SPEC TASKLIST ROWS OUTDIR"""
import json
import re
import sys

spec_p, task_p, rows_p, out = sys.argv[1:5]
spec = open(spec_p, encoding="utf-8").read().split("\n")
task = open(task_p, encoding="utf-8").read().split("\n")
ID = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")

# Pass 1: parsed IDs outside fenced regions
parsed, fence = [], False
for i, ln in enumerate(spec, 1):
    if ln.strip().startswith("```"):
        fence = not fence
        continue
    if not fence:
        for m in ID.finditer(ln):
            if m.group(1) not in [p[0] for p in parsed]:
                parsed.append((m.group(1), i))

# tasklist items = "## Task N" sections
items, cur = {}, None
for ln in task:
    m = re.match(r"## (Task \d+)", ln)
    if m:
        cur = m.group(1)
        items[cur] = []
    if cur:
        items[cur].append(ln)
items = {k: "\n".join(v) for k, v in items.items()}
tl_ids = set(ID.findall("\n".join(task)))

STOP = set("a an the and or but of to in on at for from by with as is are was were be been being it its this that these those not no than then so if when which who whom whose will would shall should can could may might must do does did has have had into onto over under only also any each per via after before until while".split())


def words(s):
    return {w for w in re.findall(r"[a-z0-9_]+", s.casefold()) if w not in STOP and len(w) > 1}


iw = {k: words(v) for k, v in items.items()}
rows, dropped = [], []
for n, raw in enumerate([r for r in open(rows_p, encoding="utf-8").read().split("\n") if r.strip()], 1):
    ln, q = raw.split("||", 1)
    ln = int(ln)
    span = " ".join(spec[ln - 1: ln + 1]) if ln < len(spec) else spec[ln - 1]
    rid = "INF-%03d" % n
    if q not in spec[ln - 1] and q not in span:
        dropped.append({"id": rid, "line": ln, "quote": q, "reason": "quote not verbatim at cited lines"})
        continue
    qw = words(q)
    best, bt = 0.0, None
    for k, w in iw.items():
        r = len(qw & w) / len(qw) if qw else 0
        if r > best:
            best, bt = r, k
    ok = best >= 0.6
    rows.append({"id": rid, "source": "inferred", "citation": f"{spec_p.split('/')[-1]}:{ln}", "quote": q,
                 "match_method": "containment" if ok else "none", "matched_task_ids": [bt] if ok else [],
                 "ratio": round(best, 3), "best_task": bt})
matched = [r for r in rows if r["matched_task_ids"]]
res = {
    "parsed_count": len(parsed), "parsed_ids": parsed, "tasklist_id_refs": sorted(tl_ids),
    "inferred_count": len(rows), "inferred_dropped_at_emission": dropped,
    "matched_union": len(matched), "total_union": len(rows) + len(parsed),
    "coverage_pct": None if not parsed else 0.0,
    "coverage_pct_union": round(len(matched) / (len(rows) + len(parsed)), 4) if rows or parsed else None,
    "unmapped_requirements_union": [r["id"] for r in rows if not r["matched_task_ids"]],
    "S_dev_density": round(1 - len(matched) / (len(rows) + len(parsed)), 4),
    "coverage_degraded": "parsed-sparse" if len(rows) > len(parsed) else None,
    "S_scope_tasks": len(items), "rows": rows,
}
json.dump(res, open(out + "/coverage-matrix.json", "w"), indent=1)
print({k: v for k, v in res.items() if k not in ("rows",)})
for r in rows:
    print(r["id"], r["citation"], r["match_method"], r["best_task"], r["ratio"], "|", r["quote"][:70])
