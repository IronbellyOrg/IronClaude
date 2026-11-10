"""Deterministic UC-1 coverage matcher (reflect Step 1B.0 Pass-2 containment rule).

No LLM: regex extraction, fixed stopword set, content-word containment >= 0.6.
Also computes the input tree hash (Step 0.4) and verifies each INF quote against its cited spec line.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PKG = Path(".dev/tasks/to-do/TASK-WF-design-20261108-041415")
SPEC = PKG / "source.md"
TASKLIST = PKG / "TASK-WF-design-20261108-041415.md"
OUT = Path(sys.argv[1])

STOP = set("""a an the and or but nor of to in on at by for from with into as is are was were be been being
do does did has have had will would may can could should must it its this that these those than then so if
also only other every each all any""".split())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# Step 0.4 tree hash (canonical JSON of sorted (relative_path, sha256))
files = sorted((str(p), sha(p)) for p in (SPEC, TASKLIST))
tree = hashlib.sha256(json.dumps(files, separators=(",", ":")).encode()).hexdigest()

spec_lines = SPEC.read_text().splitlines()
rows = json.loads((OUT / "artifacts/inf-rows.json").read_text())


def words(text):
    return [w for w in re.findall(r"[a-z0-9_]+", text.casefold()) if w not in STOP]


# split tasklist into task items
tl = TASKLIST.read_text()
tasks = {}
for m in re.finditer(r"^## Task (\d+):.*?(?=^## |\Z)", tl, re.S | re.M):
    tasks[int(m.group(1))] = m.group(0)

matrix = []
dropped = []
for r in rows:
    line = spec_lines[r["line"] - 1]
    if r["quote"] not in line:
        dropped.append(r["id"])
        continue
    qw = words(r["quote"])
    best = (0.0, None)
    for n, text in tasks.items():
        tw = set(words(text))
        ratio = sum(1 for w in qw if w in tw) / len(qw)
        if ratio > best[0]:
            best = (ratio, n)
    matched = best[0] >= 0.6
    matrix.append({
        "id": r["id"], "line": r["line"], "source": "inferred",
        "ratio": round(best[0], 4), "best_task": best[1],
        "match_method": "containment" if matched else "none",
        "matched_task_ids": [best[1]] if matched else [],
    })

total = len(matrix)
matched_n = sum(1 for m in matrix if m["match_method"] == "containment")
unmapped = [m["id"] for m in matrix if m["match_method"] == "none"]
summary = {
    "input_tree_sha256": tree,
    "file_list": [{"path": p, "sha256": h} for p, h in files],
    "parsed_count": 0, "inferred_count": len(rows), "inf_dropped_at_emission": dropped,
    "total_union": total, "matched_union": matched_n,
    "coverage_pct": None, "coverage_pct_union": round(matched_n / total, 4) if total else None,
    "unmapped_requirements_union": unmapped,
    "S_dev_density": round(len(unmapped) / total, 4) if total else None,
    "S_scope_tasks": len(tasks),
}
(OUT / "artifacts/coverage-matrix.json").write_text(json.dumps({"summary": summary, "rows": matrix}, indent=1))
print(json.dumps(summary, indent=1))
for m in matrix:
    if m["match_method"] == "none":
        print("UNMAPPED", m["id"], m["ratio"], "best task", m["best_task"])
