import hashlib, json, os, sys, datetime
from pathlib import Path
P = Path(sys.argv[1])
PR = P/"fixtures/project"; OUT = P/"runs/post-default-attempt-1/artifacts"; PLUG = P/"plugin"
inputs = {"spec": PR/"spec.md", "tasklist": PR/"completed.md", "diff": PR/"changes.patch"}
scope = PR/"src"
def under(a, b):
    a, b = Path(os.path.realpath(a)), Path(os.path.realpath(b))
    return a == b or b in a.parents
out_r = Path(os.path.realpath(OUT))
assert ".." not in OUT.parts
# nearest existing ancestor must resolve to itself (no symlink alias)
anc = OUT
while not anc.exists(): anc = anc.parent
assert Path(os.path.realpath(anc)) == anc, "symlink in output ancestor"
for name, p in list(inputs.items()) + [("scope", scope), ("audit_root", PR)]:
    assert not under(p, out_r) and not under(out_r, p) or name == "audit_root" and not under(out_r, p), f"overlap {name}"
for d in ["skills", "agents", "commands", ".claude-plugin"]:
    dd = PLUG/d
    assert not under(out_r, dd) and not under(dd, out_r), f"plugin overlap {d}"
assert ".claude" not in out_r.parts
OUT.mkdir(parents=False, exist_ok=False) if OUT.parent.exists() else None
(OUT/"artifacts").mkdir()
tree = [inputs["tasklist"], inputs["spec"], inputs["diff"], PR/"src/greeting.py", PR/"tests/test_greeting.py"]
fl = sorted([(str(p.relative_to(PR)), hashlib.sha256(p.read_bytes()).hexdigest()) for p in tree])
th = hashlib.sha256(json.dumps(fl).encode()).hexdigest()
snap = {"input_tree_sha256": th, "file_list": [{"path": a, "sha256": b} for a, b in fl], "file_count": len(fl),
        "notes": "tests/test_greeting.py included as linked T-103 evidence (outside --scope src and outside the diff); execution.log and proposed.md are NOT selected inputs and are excluded"}
(OUT/"artifacts/input-snapshot.json").write_text(json.dumps(snap, indent=2) + "\n")
print(json.dumps(snap, indent=2))
