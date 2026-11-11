import json, glob, re, sys, collections
pat = re.compile(sys.argv[1])  # e.g. p11/runs/(a3-r\d)/PROMPT-(\w+)\.md
best = {}
for f in glob.glob("/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"):
    first=None; msgs={}; models=set(); done=False
    try:
        for line in open(f, errors="ignore"):
            try: d=json.loads(line)
            except Exception: continue
            m=d.get("message") or {}
            if first is None and d.get("type")=="user":
                c=m.get("content"); first = c if isinstance(c,str) else json.dumps(c)
            if d.get("type")=="assistant":
                mid=m.get("id") or d.get("uuid"); ot=(m.get("usage") or {}).get("output_tokens",0) or 0
                msgs[mid]=max(msgs.get(mid,0),ot); models.add(m.get("model",""))
                if "DONE" in json.dumps(m.get("content")): done=True
    except Exception: continue
    if not first: continue
    mm=pat.search(first)
    if not mm: continue
    key=(mm.group(1),mm.group(2)); tot=sum(msgs.values())
    son=any("sonnet" in x for x in models)
    best.setdefault(key,[]).append((son,done,tot,f,sorted(models)))
res={}
for k,v in sorted(best.items()):
    v.sort(key=lambda x:(x[0],x[2]),reverse=True)
    res[k]=v[0][2]
    if len(v)>1: print("MULTI",k,[(x[0],x[2],x[4]) for x in v],file=sys.stderr)
json.dump({f"{a}|{b}":t for (a,b),t in res.items()},sys.stdout,indent=0)
