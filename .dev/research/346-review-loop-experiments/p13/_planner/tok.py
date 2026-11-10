import json,re,glob,collections
T="/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/tasks/*.output"
per=collections.defaultdict(list)
for f in glob.glob(T):
    L=open(f,errors="ignore").read().splitlines()
    m=re.search(r"p11/runs/(a\d-r\d)/PROMPT-(\w+)\.md","\n".join(L[:6]))
    if not m: continue
    seen={};model=set()
    for l in L:
        try:d=json.loads(l)
        except: continue
        msg=d.get("message") or {}
        if msg.get("role")=="assistant" and msg.get("usage"):
            seen[msg.get("id")]=msg["usage"].get("output_tokens") or 0; model.add(msg.get("model"))
    per[(m.group(1),m.group(2))].append((sum(seen.values()),tuple(model)))
steps=collections.defaultdict(list)
for (run,st),v in sorted(per.items()):
    best=max([x for x in v if any('sonnet' in (mm or '') for mm in x[1])] or v)
    if run.startswith("a3"): steps[st].append(best[0]); print(run,st,best[0],len(v))
for s,v in steps.items(): print(s,len(v),sum(v)//len(v))
