"""Wave 1B coverage map (UC-1): Pass 1 regex, Pass 2 quote-pinned rows, containment matching.
usage: uv run python coverage-map.py <out> <spec> <tasklist>   (run from the repo root)"""
import json, re, sys, pathlib

out, spec_p, plan_p = (pathlib.Path(a) for a in sys.argv[1:4])
spec_lines = spec_p.read_text().splitlines()
plan_lines = plan_p.read_text().splitlines()
ID_RE = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")
STOP = set("a an the and or but of to in on at by for with from as is are was were be been being it its this that these those "
           "not no nor so if then than when which who whom whose will shall must may can could should would do does did has have had "
           "any all each every into out up over under after before only also such per via".split())

# Pass 1: regex outside fenced blocks, spec side
parsed, fence = [], False
for n, line in enumerate(spec_lines, 1):
    if line.strip().startswith("```"):
        fence = not fence
        continue
    if not fence:
        for m in ID_RE.finditer(line):
            parsed.append({"id": m.group(1), "line": n})
plan_ids = sorted({m.group(1) for l in plan_lines for m in ID_RE.finditer(l)})

# Pass 2: inferred rows, each quote must be verbatim in the spec; the line is resolved here
inf_in = json.loads((out / "artifacts" / "inferred-rows.json").read_text())
inferred, dropped = [], []
for r in inf_in:
    hits = [i for i, l in enumerate(spec_lines, 1) if r["quote"] in l]
    if not hits:
        dropped.append(r["quote"]); continue
    inferred.append({"quote": r["quote"], "line": hits[0], "g": r["g"]})
inferred.sort(key=lambda r: r["line"])
for i, r in enumerate(inferred, 1):
    r["id"] = f"INF-{i:03d}"

# tasklist items = "## Task N" sections
tasks, cur = {}, None
for l in plan_lines:
    m = re.match(r"## Task (\d+):", l)
    if m:
        cur = f"Task {m.group(1)}"; tasks[cur] = []
    elif l.startswith("## ") and not l.startswith("## Task"):
        cur = None
    if cur:
        tasks[cur].append(l)
tasks = {k: " ".join(v) for k, v in tasks.items()}

def words(s):
    return {w for w in re.findall(r"[a-z0-9_]+", s.casefold()) if w not in STOP and len(w) > 1}

matrix = []
for r in inferred:
    qw = words(r["quote"]); best, ratio = None, 0.0
    for t, txt in tasks.items():
        x = len(qw & words(txt)) / len(qw) if qw else 0
        if x > ratio + 1e-12:
            best, ratio = t, x
    ok = ratio >= 0.6
    matrix.append({"requirement_id": r["id"], "source": "inferred", "spec_line": r["line"], "quote": r["quote"], "group": r["g"],
                   "matched_task_ids": [best] if ok else [], "match_method": "containment" if ok else "none", "ratio": round(ratio, 3)})
for p in parsed:
    matrix.append({"requirement_id": p["id"], "source": "parsed", "spec_line": p["line"], "matched_task_ids": [], "match_method": "none"})

pt, it = len(parsed), len(inferred)
matched = [m for m in matrix if m["match_method"] != "none"]
unm = [m["requirement_id"] for m in matrix if m["match_method"] == "none"]
summary = {
    "parsed_count": pt, "inferred_count": it, "dropped_pass2_rows": dropped, "plan_task_count": len(tasks), "plan_ids_found": plan_ids,
    "coverage_pct": None if pt == 0 else round(sum(1 for m in matched if m["source"] == "parsed") / pt, 4),
    "coverage_pct_union": None if pt + it == 0 else round(len(matched) / (pt + it), 4),
    "unmapped_requirements_union": unm,
    "S_dev_density": None if pt + it == 0 else round(len(unm) / (pt + it), 4),
    "coverage_degraded": "parsed-sparse" if it > pt else None,
    "coverage_undefined": (pt + it == 0),
    "task_hit_counts": {t: sum(1 for m in matched if t in m["matched_task_ids"]) for t in tasks},
}
(out / "artifacts" / "coverage-matrix.json").write_text(json.dumps({"summary": summary, "matrix": matrix}, indent=1))
assigned = {"reviewer-1": [], "reviewer-2": [], "reviewer-3": []}
for r in inferred:
    assigned[{"a": "reviewer-1", "q": "reviewer-2", "r": "reviewer-3"}[r["g"]]].append(r["id"])
(out / "artifacts" / "assigned-rows.json").write_text(json.dumps(assigned, indent=1))
print(json.dumps(summary, indent=1))
print({k: len(v) for k, v in assigned.items()})
for m in matrix:
    print(m["requirement_id"], m["spec_line"], m["match_method"], m["matched_task_ids"], m["ratio"] if "ratio" in m else "")
