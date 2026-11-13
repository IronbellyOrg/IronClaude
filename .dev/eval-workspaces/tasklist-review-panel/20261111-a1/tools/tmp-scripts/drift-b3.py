import json,hashlib,sys
d="/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/"
fl=sorted([(n,hashlib.sha256(open(d+n,'rb').read()).hexdigest()) for n in ("TASK-WF-designSpec-20261107-075614.md","source.md")])
print(hashlib.sha256(json.dumps(fl,separators=(",",":")).encode()).hexdigest())
