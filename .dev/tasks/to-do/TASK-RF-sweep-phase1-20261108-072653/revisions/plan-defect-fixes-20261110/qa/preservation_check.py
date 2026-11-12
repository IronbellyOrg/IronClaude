"""Preservation check for revision plan-defect-fixes-20261110 (R2).

Compares the baseline task file with the edited one and writes preservation-check.json.
Run: uv run python -I <this file>   (from the repo root)
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PKG = Path(".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653")
R1 = PKG / "revisions/chat-output-exception-20261109-133150"
R2 = PKG / "revisions/plan-defect-fixes-20261110"
BASE = (R2 / "baseline/task-before-rev2.md").read_text().split("\n")
CUR = (PKG / "TASK-RF-sweep-phase1-20261108-072653.md").read_text().split("\n")
LEDGER = Path(".dev/implement/task-rf-sweep-phase1-202-c7ea3265")

HEADER = re.compile(r"^- \[( |x)\] \*\*(\d+\.\d+[a-z]?) ")
BODY = re.compile(r"^  - \*\*(Context|Action|Output|Verification|Completion gate)\*\*:")
dm = (R1 / "delta-manifest.md").read_text().split("\n")
labels = set()
for ln in dm[20:117]:
    m = re.match(r"^\| (\d+\.\d+[a-z]?) \|", ln)
    if m:
        labels.add(m.group(1))
r1_count = len(labels)
labels |= {"13.1", "8.19", "10.5"}

res = {"r1_labels": r1_count, "allowed_labels": len(labels), "base_lines": len(BASE), "cur_lines": len(CUR)}
fail = []
if len(BASE) != len(CUR):
    fail.append(f"line count {len(BASE)} -> {len(CUR)}")

cur_label = None
headers_base = [(i, l) for i, l in enumerate(BASE) if HEADER.match(l)]
headers_cur = [(i, l) for i, l in enumerate(CUR) if HEADER.match(l)]
res["headers"] = len(headers_base)
if headers_base != headers_cur:
    fail.append("header lines differ")
completed_bodies = 0
changed = {}
state = None  # (label, ticked)
for i in range(min(len(BASE), len(CUR))):
    m = HEADER.match(BASE[i])
    if m:
        state = (m.group(2), m.group(1) == "x")
        if state[1]:
            completed_bodies += 1
    if BASE[i] != CUR[i]:
        if state is None:
            fail.append(f"line {i+1} differs before first item")
            continue
        label, ticked = state
        if HEADER.match(BASE[i]) or not BODY.match(BASE[i]) or not BODY.match(CUR[i]):
            fail.append(f"line {i+1} ({label}) differs but is not an editable body line")
        if ticked:
            fail.append(f"line {i+1} ({label}) is in a completed item")
        if label not in labels:
            fail.append(f"line {i+1} ({label}) is not an allowed label")
        changed.setdefault(label, []).append(i + 1)
res["completed_items"] = completed_bodies
res["changed_labels"] = len(changed)
res["changed_lines"] = sum(len(v) for v in changed.values())
res["changed_by_label"] = {k: v for k, v in sorted(changed.items())}
# the appended-note region must be untouched: everything after the last item header identical
# (covered by the per-line check: those lines are not body lines of an allowed label)

# frozen sources
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

frozen = {
    str(LEDGER / "progress.md"): "b72f9236",
    str(LEDGER / "item-map.tsv"): "2ec35fe4",
    "docs/designs/orchestrator-mode.md": "e4a06d0c",
}
for p, pre in frozen.items():
    h = sha(p)
    ok = h.startswith(pre)
    res.setdefault("frozen", {})[p] = {"sha256": h, "expected_prefix": pre, "ok": ok}
    if not ok:
        fail.append(f"{p} hash changed")
res["pass"] = not fail
res["failures"] = fail
out = R2 / "qa/preservation-check.json"
out.write_text(json.dumps(res, indent=2))
print(json.dumps({k: res[k] for k in ("pass", "headers", "completed_items", "changed_labels", "changed_lines", "cur_lines", "allowed_labels", "r1_labels")}))
print("failures:", fail[:10])
sys.exit(0 if res["pass"] else 1)
