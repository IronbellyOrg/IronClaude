import json, sys, pathlib, os
sel = json.load(open(sys.argv[1])); checks = sys.argv[2].split(","); lo = int(sys.argv[3]) if len(sys.argv)>3 else 0; hi = int(sys.argv[4]) if len(sys.argv)>4 else 999
n = 0
for i, f in enumerate(sel["flags"]):
    if f["check"] not in checks: continue
    n += 1
    if not (lo <= n-1 < hi): continue
    lines = pathlib.Path(f["path"]).read_text(errors="replace").split("\n")
    a = f["lines"][0]; ol = f["other_lines"]
    print(f"#{i} {f['check']} {f['lint_id']} docs={f['n_docs']} {pathlib.Path(f['path']).name[:30]} L{f['lines']} other={ol}")
    print("   MSG:", f["message"][:230])
    print("   A:", lines[a-1][:260])
    if ol: print("   B:", lines[ol[0]-1][:260])
