import hashlib, json, re, sys
from pathlib import Path
out, pkg = Path(sys.argv[1]), Path(sys.argv[2])
plan = pkg / f"{pkg.name}.md"
spec = pkg / "source.md"
files = {plan, spec}
for p in re.findall(r"`([A-Za-z0-9_./-]+\.(?:py|md|yml|yaml|txt|json|toml|sh|mjs))`", plan.read_text()):
    q = Path(p)
    if q.is_file():
        files.add(q)
for f in pkg.rglob("*"):
    if f.is_file():
        files.add(f)
rows = sorted((str(f), hashlib.sha256(f.read_bytes()).hexdigest()) for f in files)
tree = hashlib.sha256(json.dumps(rows).encode()).hexdigest()
lines = [f"input_tree_sha256: {tree}", f"file_count: {len(rows)}", "file_list:"]
lines += [f"  - path: {p}\n    sha256: {h}" for p, h in rows]
(out / "artifacts/input-snapshot.yaml").write_text("\n".join(lines) + "\n")
print(tree, len(rows))
