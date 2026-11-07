"""Recompute the pinned input hash without touching input files."""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "src/superclaude/cli/install_user_setup.py").is_file())
snapshot = (HERE / "input-snapshot.yaml").read_text()
old = re.search(r"^input_tree_sha256: (\w+)$", snapshot, re.M).group(1)
rows = re.findall(r"^- path: (.+)\n  sha256: (\w+)", snapshot, re.M)
assert len(rows) == 8
new_rows, changes = [], []
for rel, digest in rows:
    path = ROOT / rel
    current = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    if current:
        new_rows.append((rel, current))
    if current != digest:
        changes.append({"path": rel, "old_sha": digest, "new_sha": current, "change_kind": "modified" if current else "removed"})
missing_section = snapshot.split("missing_links:\n", 1)[1].split("output_root:", 1)[0]
missing_links = re.findall(r"^- (.+)$", missing_section, re.M)
assert len(missing_links) == 4
for missing in missing_links:
    if (ROOT / missing).is_file():
        current = hashlib.sha256((ROOT / missing).read_bytes()).hexdigest()
        new_rows.append((missing, current))
        changes.append({"path": missing, "old_sha": None, "new_sha": current, "change_kind": "added"})
new = hashlib.sha256(json.dumps(sorted(new_rows), separators=(",", ":")).encode()).hexdigest()
result = {"old_sha256": old, "new_sha256": new, "input_drift_detected": old != new, "input_drift_diff": changes, "file_count": len(new_rows)}
assert (old != new) == bool(changes)
(HERE / "input-integrity-result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
