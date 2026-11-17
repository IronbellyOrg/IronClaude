import re, json
from pathlib import Path
P = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial/partials")
def parse(f):
    d = {}
    for l in (P/f).read_text().splitlines():
        if not l.startswith("|"): continue
        cs = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cs) < 5: continue
        m = re.match(r"\**([CKSLRE]\d)\b", cs[0])
        if not m: continue
        v1, v2 = cs[1].upper(), cs[3].upper()
        n = lambda s: "NOT MET" if "NOT" in s else ("MET" if "MET" in s else None)
        d[m.group(1)] = (n(v1), n(v2), cs[2][:200], cs[4][:200], cs[0][:80])
    return d
a, b = parse("qual-pass1.md"), parse("qual-pass2.md")
print(len(a), len(b))
dis = []
for k in sorted(set(a)|set(b)):
    if k not in a or k not in b: print("missing", k); continue
    for vi, vn in ((0,"V1"),(1,"V2")):
        if a[k][vi] != b[k][vi]:
            dis.append((k, vn, a[k][vi], b[k][vi]))
print(dis)
for vi, vn in ((0,"V1"),(1,"V2")):
    print(vn, sum(1 for k in a if a[k][vi]=="MET"), sum(1 for k in b if b[k][vi]=="MET"))
json.dump({"pass1": {k:v[:2] for k,v in a.items()}, "pass2": {k:v[:2] for k,v in b.items()}, "disagreements": dis}, open(P/"qual-parse.json","w"), indent=1)
