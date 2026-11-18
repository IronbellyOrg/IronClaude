"""Wave 0.4 input snapshot + Wave 1B coverage matrix for the stage 2 plan review.

Deterministic: hashing and the containment rule only, no LLM.
Run: uv run python <this file>   (cwd = repo root)
"""
import hashlib
import json
import re
from pathlib import Path

OUT = Path(".dev/reflect/pre-TASK-WF-blockerStage2-20261116-030156-20261116030415")
PKG = Path(".dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156")
SPEC = PKG / "source.md"
PLAN = PKG / "TASK-WF-blockerStage2-20261116-030156.md"

STOP = set("""a an the and or but nor of to in on at by for from with without into onto over under as is are was were be been
being it its this that these those which who whom whose there here then than so such not no only also each every any all
both either neither does do did done has have had will would shall should can could may might must we you they he she i""".split())


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---- Step 0.4 input tree (UC-1): spec, tasklist, files the tasklist references (depth 1, existing, not under output root)
plan_text = PLAN.read_text()
cands = set(re.findall(r"`([A-Za-z0-9_./~-]+/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+)`", plan_text))
tree = {SPEC, PLAN}
for c in cands:
    p = Path(c)
    if c.startswith("./") or c.startswith("~"):
        continue
    if p.is_file():
        tree.add(p)
file_list = sorted((str(p), sha(p)) for p in tree)
tree_sha = hashlib.sha256(json.dumps(file_list).encode()).hexdigest()
snap = ["input_tree_sha256: " + tree_sha, "file_list:"]
for rel, h in file_list:
    snap += [f"  - path: {rel}", f"    sha256: {h}"]
snap.append(f"file_count: {len(file_list)}")
(OUT / "artifacts" / "input-snapshot.yaml").write_text("\n".join(snap) + "\n")

# ---- Step 1B.0 Pass 1 (regex ID extraction) over the spec
ID_RE = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")
spec_lines = SPEC.read_text().splitlines()
parsed = sorted({m for ln in spec_lines for m in ID_RE.findall(ln)})

# ---- Pass 2 rows: validate quote is verbatim in cited line
inf = json.loads((OUT / "artifacts" / "inf_rows.json").read_text())
valid, invalid = [], []
for r in inf:
    line = spec_lines[r["line"] - 1]
    (valid if r["quote"] in line else invalid).append(r)

# ---- tasklist items: each "## Task N" block; Constraints block kept apart
blocks = re.split(r"(?m)^(?=## )", plan_text)
items = {}
constraints = ""
for b in blocks:
    m = re.match(r"## Task (\d+):", b)
    if m:
        items[f"Task {m.group(1)}"] = b
    elif b.startswith("## Constraints"):
        constraints = b


def words(s: str):
    return [w for w in re.findall(r"[a-z0-9_]+", s.casefold()) if w not in STOP]


rows = []
for r in valid:
    qw = set(words(r["quote"]))
    best, ratio = None, 0.0
    for tid, text in items.items():
        tw = set(words(text))
        rt = len(qw & tw) / len(qw) if qw else 0.0
        if rt > ratio:
            best, ratio = tid, rt
    cw = set(words(constraints))
    cratio = len(qw & cw) / len(qw) if qw else 0.0
    rows.append({"id": r["id"], "line": r["line"], "source": "inferred",
                 "match": best if ratio >= 0.6 else "none", "task_ratio": round(ratio, 3),
                 "best_task": best, "constraints_ratio": round(cratio, 3), "quote": r["quote"]})

matched = sum(1 for r in rows if r["match"] != "none")
total = len(rows)
cov_union = round(matched / total, 4) if total else None
out = ["# Coverage matrix (Step 1B.0 / 1B.0 matching)", "",
       f"parsed_count: {len(parsed)}   inferred_count: {len(valid)}   inferred_invalid_dropped: {len(invalid)}",
       f"coverage_pct (parsed-only): null   coverage_pct_union: {cov_union}   (matched {matched} of {total})",
       f"coverage_degraded: {'parsed-sparse' if len(valid) > len(parsed) else 'null'}",
       f"input_tree_sha256: {tree_sha}   file_count: {len(file_list)}", "",
       "| id | spec line | source | containment match | best task ratio | constraints ratio | quote |", "|---|---|---|---|---|---|---|"]
for r in rows:
    q = r["quote"].replace("|", "&#124;")
    out.append(f"| {r['id']} | source.md:{r['line']} | inferred | {r['match']} | {r['task_ratio']} ({r['best_task']}) | {r['constraints_ratio']} | {q} |")
(OUT / "artifacts" / "coverage-matrix.md").write_text("\n".join(out) + "\n")
(OUT / "artifacts" / "coverage-matrix.json").write_text(json.dumps(
    {"parsed": parsed, "inferred_valid": len(valid), "inferred_invalid": [r["id"] for r in invalid],
     "coverage_pct_union": cov_union, "rows": rows}, indent=1))
print("tree files:", len(file_list), "sha", tree_sha[:12])
print("parsed:", parsed, "inferred valid:", len(valid), "invalid:", [r["id"] for r in invalid])
print("matched", matched, "of", total, "union", cov_union)
for r in rows:
    print(r["id"], r["match"], r["task_ratio"], r["best_task"], "constraints", r["constraints_ratio"])
