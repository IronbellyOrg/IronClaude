"""Apply the literal old -> new rows of one group of cap-edits.yaml or sweep-edits.yaml.

Usage (repo root): uv run python -I .dev/review-severity-rule/implement-tools/apply_rows.py <table.yaml> <group> [--skip ID,...]
Each row must have its `old` exactly `occurrences` times (or already be applied: old absent and new present, reported
as "already"). Any other state stops before writing anything. Prints one line per row.
"""
import pathlib
import sys

import yaml

table, group = sys.argv[1], sys.argv[2]
skip = set(sys.argv[sys.argv.index("--skip") + 1].split(",")) if "--skip" in sys.argv else set()
rows = [r for r in yaml.safe_load(pathlib.Path(table).read_text())["rows"] if r["group"] == group and r["id"] not in skip]
texts, plan, bad = {}, [], []
for r in rows:
    t = texts.setdefault(r["file"], pathlib.Path(r["file"]).read_text())
    n = t.count(r["old"])
    if n == r.get("occurrences", 1):
        plan.append(r)
    elif n == 0 and r["new"] in t:
        print(f"{r['id']} already {r['file']}")
    else:
        bad.append(f"{r['id']} {r['file']}: old occurs {n}x, expected {r.get('occurrences', 1)}")
if bad:
    print("STOP, nothing written:", *bad, sep="\n")
    sys.exit(1)
for r in plan:
    texts[r["file"]] = texts[r["file"]].replace(r["old"], r["new"])
    print(f"{r['id']} applied {r['file']}")
for f, t in texts.items():
    if pathlib.Path(f).read_text() != t:
        pathlib.Path(f).write_text(t)
print(f"{len(rows)} rows in group {group}; applied {len(plan)}")
