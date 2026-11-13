import hashlib,json
fl=sorted([("TASK-WF-designSpec-20261107-075614.md","044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481"),("source.md","a865f397468a076c9c070c031f807b44d9cccd91059b2ad5efb1b926090ba10a")])
t=hashlib.sha256(json.dumps(fl).encode()).hexdigest()
open("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboD-r1/artifacts/input-snapshot.yaml","w").write("input_tree_sha256: %s\nfile_list:\n"%t+"".join("  - path: %s\n    sha256: %s\n"%x for x in fl)+"file_count: 2\n")
print(t)
