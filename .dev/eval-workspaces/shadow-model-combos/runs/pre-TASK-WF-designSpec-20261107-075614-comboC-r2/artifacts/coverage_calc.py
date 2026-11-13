"""Deterministic coverage mapping (SKILL 1B.0 / refs/coverage-mapping.md). Stdlib only."""
import json
import re
import sys
from pathlib import Path

out, spec_p, plan_p = (Path(a) for a in sys.argv[1:4])
spec = spec_p.read_text().splitlines()
plan = plan_p.read_text().splitlines()

ID_RE = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")


def strip_fences(lines):
    keep, fence = [], False
    for i, l in enumerate(lines, 1):
        if l.strip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            keep.append((i, l))
    return keep


parsed_spec = sorted({m for _, l in strip_fences(spec) for m in ID_RE.findall(l)})
parsed_plan = sorted({m for _, l in strip_fences(plan) for m in ID_RE.findall(l)})

# task items = "## Task N" sections of the plan
tasks, cur = {}, None
for i, l in enumerate(plan, 1):
    m = re.match(r"## Task (\d+):", l)
    if m:
        cur = int(m.group(1))
        tasks[cur] = {"start": i, "text": []}
    elif l.startswith("## ") and cur is not None:
        cur = None
    if cur is not None:
        tasks[cur]["text"].append(l)
        tasks[cur]["end"] = i

STOP = set("a an the and or but of to in on at for by with from as is are was were be been being it its this that these those not no will must shall may can should would which who whom whose when where while if then than so such into onto over under after before between per via also any each every all only same other".split())


def words(s):
    return {w for w in re.findall(r"[a-z0-9_]+", s.lower()) if w not in STOP and len(w) > 1}


task_words = {n: words("\n".join(t["text"])) for n, t in tasks.items()}

rows, dropped = [], []
for k, raw in enumerate(Path(out / "artifacts/pass2-rows.txt").read_text().splitlines(), 1):
    if not raw.strip():
        continue
    ls, le, quote = raw.split("|", 2)
    ls, le = int(ls), int(le)
    span = "\n".join(spec[ls - 1:le])
    rid = f"INF-{k:03d}"
    if quote not in span:
        dropped.append({"id": rid, "line": ls, "quote": quote, "reason": "quote not verbatim in cited lines"})
        continue
    w = words(quote)
    best, bn = 0.0, None
    for n in sorted(task_words):
        r = len(w & task_words[n]) / len(w) if w else 0.0
        if r > best + 1e-12:
            best, bn = r, n
    ok = best >= 0.6
    rows.append({"id": rid, "source": "inferred", "citation": f"source.md:{ls}" + (f"-{le}" if le != ls else ""),
                 "quote": quote, "match_method": "containment" if ok else "none",
                 "matched_task_ids": [f"Task {bn}"] if ok else [], "best_ratio": round(best, 4),
                 "best_task": f"Task {bn}" if bn else None})

matched = sum(1 for r in rows if r["match_method"] != "none")
total = len(rows)
unmapped = [r["id"] for r in rows if r["match_method"] == "none"]
res = {
    "parsed_spec_ids": parsed_spec, "parsed_plan_ids": parsed_plan,
    "parsed_count": len(parsed_spec), "inferred_count": total, "dropped_at_emission": dropped,
    "coverage_pct": None if not parsed_spec else 0.0,
    "coverage_pct_union": round(matched / total, 4) if total else None,
    "matched": matched, "total": total, "unmapped_requirements_union": unmapped,
    "coverage_degraded": "parsed-sparse" if total > len(parsed_spec) else None,
    "tasks": {n: {"lines": f"{t['start']}-{t.get('end')}"} for n, t in tasks.items()},
    "rows": rows,
}
(out / "artifacts/coverage-matrix.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k not in ("rows", "tasks")}, indent=1))
