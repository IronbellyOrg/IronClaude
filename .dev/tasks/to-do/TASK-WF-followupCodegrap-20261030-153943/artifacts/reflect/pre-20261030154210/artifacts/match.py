"""Deterministic containment matcher (coverage-mapping.md stage 3, INF rows)."""

import json
import re
import sys
from pathlib import Path

import yaml

STOP = set(
    "a an the and or but nor of in on at to for from by with as is are was were be been being "
    "it its this that these those than then if when which who whom whose what where how not no "
    "do does did has have had can could will would shall should may might must into onto over "
    "under per via each every any all one only also so such".split()
)


def words(text):
    return {w for w in re.findall(r"[a-z0-9_]+", text.casefold()) if w not in STOP}


inferred, plan, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
rows = yaml.safe_load(inferred.read_text())["rows"]
tasks = re.split(r"^## Task (\d+):", plan.read_text(), flags=re.M)
items = [(f"Task {tasks[i]}", words(tasks[i + 1])) for i in range(1, len(tasks), 2)]
matrix, matched = [], 0
for r in rows:
    q = words(r["quote"])
    best = ("", 0.0)
    for tid, tw in items:
        ratio = len(q & tw) / len(q) if q else 0.0
        if ratio > best[1]:
            best = (tid, ratio)
    hit = best[1] >= 0.6
    matched += hit
    matrix.append(
        {
            "requirement_id": r["id"],
            "matched_task_ids": [best[0]] if hit else [],
            "match_method": "containment" if hit else "none",
            "ratio": round(best[1], 4),
            "source": "inferred",
        }
    )
union = round(matched / len(rows), 4) if rows else None
unmapped = [m["requirement_id"] for m in matrix if m["match_method"] == "none"]
out.write_text(
    yaml.safe_dump(
        {
            "parsed_count": 0,
            "inferred_count": len(rows),
            "coverage_pct": None,
            "coverage_pct_union": union,
            "unmapped_requirements_union": unmapped,
            "matrix": matrix,
        },
        sort_keys=False,
    )
)
print(json.dumps({"inferred": len(rows), "matched": matched, "union": union, "unmapped": len(unmapped)}))
