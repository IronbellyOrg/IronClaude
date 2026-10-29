import hashlib, json, re, sys, pathlib, datetime
pkg, out = sys.argv[1], sys.argv[2]
tl = pathlib.Path(pkg) / (pathlib.Path(pkg).name + ".md")
spec = pathlib.Path(pkg) / "source.md"
files = [tl, spec]
seen = {str(tl), str(spec)}
for tok in re.findall(r"`([^`\s]+)`", tl.read_text()):
    tok = tok.split(":")[0].rstrip(",.;)")
    if tok.startswith("./"):
        cand = pathlib.Path(pkg) / tok[2:]
    else:
        cand = pathlib.Path(tok)
    if cand.is_file() and str(cand) not in seen and not str(cand).startswith(out):
        seen.add(str(cand)); files.append(cand)
fl = sorted((str(p), hashlib.sha256(p.read_bytes()).hexdigest()) for p in files)
tree = hashlib.sha256(json.dumps(fl).encode()).hexdigest()
with open(f"{out}/artifacts/input-snapshot.yaml", "w") as f:
    f.write(f"input_tree_sha256: {tree}\nfile_count: {len(fl)}\nfile_list:\n")
    for p, h in fl: f.write(f"  - path: {p}\n    sha256: {h}\n")
print(tree, len(fl))
print("tasklist", hashlib.sha256(tl.read_bytes()).hexdigest()); print("spec", hashlib.sha256(spec.read_bytes()).hexdigest())
