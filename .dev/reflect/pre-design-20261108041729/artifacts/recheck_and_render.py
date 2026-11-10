"""Wave-5 mechanical gate: input drift guard, full re-read of the 55 inferred-row quotes, and the INF table for REPORT.md."""
import hashlib
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
PKG = Path(".dev/tasks/to-do/TASK-WF-design-20261108-041415")
SPEC = PKG / "source.md"
TASKLIST = PKG / "TASK-WF-design-20261108-041415.md"
EXPECTED_TREE = "610c54d0685761c83993d5c70d3b5ec86c300bfa7688628c2909dc296d18b439"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


files = sorted((str(p), sha(p)) for p in (SPEC, TASKLIST))
tree = hashlib.sha256(json.dumps(files, separators=(",", ":")).encode()).hexdigest()
drift = tree != EXPECTED_TREE

lines = SPEC.read_text().splitlines()
rows = json.loads((OUT / "artifacts/inf-rows.json").read_text())
matrix = {r["id"]: r for r in json.loads((OUT / "artifacts/coverage-matrix.json").read_text())["rows"]}
bad = [r["id"] for r in rows if r["quote"] not in lines[r["line"] - 1]]

table = ["| Row | Spec line | Match |", "|---|---|---|"]
for r in rows:
    m = matrix[r["id"]]
    res = f"Task {m['best_task']} (containment {m['ratio']})" if m["match_method"] == "containment" else f"none (best Task {m['best_task']}, {m['ratio']})"
    table.append(f"| {r['id']} | source.md:{r['line']} | {res} |")
(OUT / "artifacts/inf-table.md").write_text("\n".join(table) + "\n")

print(json.dumps({"input_drift_detected": drift, "input_tree_sha256": tree,
                  "inf_rows": len(rows), "inf_quotes_not_found": bad}, indent=1))
