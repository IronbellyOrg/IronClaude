import json, re, glob
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
pat = re.compile(r"ground-truth\.json|ground-truth-draft|resolution-(default|live7)\.json|reviews/combos|20261111-a1|eval-workspaces/tasklist|COMBO-REPORT|PILOT-REPORT|quarantine-pre|/tmp/evalsb/(jobs|progress|start|xargs)|/tmp/(r1jobs|n2run|r2|b[0-9]+-)|eval-tasklist-review-panel|\.dev/eval-workspaces/tasklist", re.I)
for f in glob.glob(E + "/TASK-WF-designSpec-20261107-075614/reviews/combos/r5-glm-haiku2/t3-1.attempt*.json"):
    if not re.search(r"attempt\d+\.json$", f): continue
    j = json.load(open(f))
    for m in j:
        c = (m.get("message") or {}).get("content")
        if m.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if b.get("type") == "tool_use":
                    s = json.dumps(b["input"])
                    mm = pat.search(s)
                    if mm: print(f[-20:], b["name"], mm.group(0), s[max(0, mm.start()-150):mm.end()+150])
