import hashlib, json, sys, pathlib
out = pathlib.Path(sys.argv[1]); files = sys.argv[2:]
fl = sorted((pathlib.Path(f).as_posix(), hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()) for f in files)
tree = hashlib.sha256(json.dumps(fl).encode()).hexdigest()
y = f"input_tree_sha256: {tree}\nfile_list:\n" + "".join(f"  - path: {p}\n    sha256: {h}\n" for p, h in fl) + f"file_count: {len(fl)}\n"
(out/"artifacts"/"input-snapshot.yaml").write_text(y); print(y)
