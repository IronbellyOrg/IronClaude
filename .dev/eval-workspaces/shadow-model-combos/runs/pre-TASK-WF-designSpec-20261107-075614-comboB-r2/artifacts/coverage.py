"""Deterministic Wave 1B coverage map (UC-1) for one reflect run.

Pass 1: ID_REGEX over the spec outside fenced blocks (refs/coverage-mapping.md).
Pass 2: quote-pinned inferred rows from inf-rows.tsv; a row is dropped when its quote
        is not found verbatim in the spec, or when it overlaps a parsed-ID span.
Matching: containment rule, case-folded, stopwords stripped, threshold 0.6, single best item.
Items: each '## Task N' section of the tasklist, plus the Goal and Constraints blocks.
"""
import json
import re
import sys
from pathlib import Path

spec_p, tl_p, rows_p, out_dir = map(Path, sys.argv[1:5])
spec = spec_p.read_text(encoding="utf-8").splitlines()
tl = tl_p.read_text(encoding="utf-8").splitlines()

ID_REGEX = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")
parsed, in_fence = [], False
for i, line in enumerate(spec, 1):
    if line.lstrip().startswith("```"):
        in_fence = not in_fence
        continue
    if in_fence:
        continue
    for m in ID_REGEX.finditer(line):
        parsed.append({"id": m.group(1), "line": i})

STOP = set("""a an the and or but nor of to in on at by for with from as is are was were be been being
this that these those it its into onto than then so such not no do does did has have had will shall
may can could should would must if when while which who whom whose there their they them any all
each every per via also only more most other""".split())


def words(text):
    return {w for w in re.findall(r"[a-z0-9_]+", text.casefold()) if w not in STOP and len(w) > 1}


# tasklist items
items, cur = [], None
for i, line in enumerate(tl, 1):
    m = re.match(r"## Task (\d+):", line)
    if m:
        cur = {"id": f"Task {m.group(1)}", "start": i, "text": []}
        items.append(cur)
    elif line.startswith("## ") or line.startswith("# "):
        cur = None if not line.startswith("## Constraints") else None
    if cur is not None:
        cur["text"].append(line)
pre = "\n".join(tl[: next(i for i, l in enumerate(tl) if l.startswith("## Phase 1")) ])
items.insert(0, {"id": "Goal+Constraints", "start": 1, "text": [pre]})
for it in items:
    it["text"] = "\n".join(it["text"])
    it["words"] = words(it["text"])

rows, dropped = [], []
spec_text = "\n".join(spec)
for n, quote in enumerate(rows_p.read_text(encoding="utf-8").splitlines(), 1):
    quote = quote.rstrip("\n")
    if not quote:
        continue
    rid = f"INF-{n:03d}"
    hits = [i for i, l in enumerate(spec, 1) if quote in l]
    if not hits:
        dropped.append({"id": rid, "quote": quote, "reason": "quote not found verbatim on one spec line"})
        continue
    line_no = hits[0]
    if any(p["line"] == line_no for p in parsed):
        dropped.append({"id": rid, "quote": quote, "reason": "overlaps parsed span"})
        continue
    rows.append({"id": rid, "quote": quote, "citation": f"source.md:{line_no}", "source": "inferred", "line": line_no})

matrix = []
for r in rows:
    w = words(r["quote"])
    best, ratio = None, 0.0
    for it in items:
        ra = len(w & it["words"]) / len(w) if w else 0.0
        if ra > ratio:
            best, ratio = it, ra
    if best and ratio >= 0.6:
        matrix.append({**r, "matched_task_ids": [best["id"]], "match_method": "containment", "ratio": round(ratio, 3)})
    else:
        matrix.append({**r, "matched_task_ids": [], "match_method": "none", "ratio": round(ratio, 3), "best_candidate": best["id"] if best else None})

matched = sum(1 for m in matrix if m["matched_task_ids"])
total = len(matrix)
out = {
    "parsed_count": len(parsed),
    "inferred_count": total,
    "inferred_dropped": dropped,
    "coverage_pct": None if not parsed else 0.0,
    "coverage_pct_union": round(matched / total, 4) if total else None,
    "unmapped_requirements": [],
    "unmapped_requirements_union": [m["id"] for m in matrix if not m["matched_task_ids"]],
    "coverage_degraded": "parsed-sparse" if total > len(parsed) else None,
    "coverage_undefined": (total == 0 and not parsed),
    "S_dev_density": round((total - matched) / total, 4) if total else None,
    "matrix": matrix,
}
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "coverage-matrix.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "matrix"}, indent=2))
