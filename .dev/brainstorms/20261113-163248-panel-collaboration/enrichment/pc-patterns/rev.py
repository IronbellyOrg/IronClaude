import json,re,collections
E="/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PKD={"DS":"TASK-WF-designSpec-20261107-075614","AL":"TASK-WF-makeTheAliasOnly-20261105-051649","DE":"TASK-WF-design-20261108-041415"}
R=json.load(open("/tmp/pc-patterns/records_gt.json"))
# recursive search over a directory tree (tests/, src/, ., docs ...) rather than a named file
REC=re.compile(r"(grep\s+(-[A-Za-z]*[rR][A-Za-z]*|--recursive|-[A-Za-z]*\s+-[A-Za-z]*[rR])|\brg\b|git grep|find\s+\S+)")
DIRARG=re.compile(r"\s(tests|src|docs|plugins|\.|tests/[\w/]+/|src/[\w/]+/?)(\s|$|;|\|)")
c=collections.Counter(); ct=collections.Counter(); n=collections.Counter(); calls=collections.Counter()
for r in R:
    arr=json.load(open(f"{E}/{PKD[r['pkg']]}/reviews/combos/{r['run']}/{r['rid']}.attempt{r['attempt']}.json"))
    cmds=[b["input"].get("command","") for x in arr if x.get("type")=="assistant" for b in x["message"].get("content",[]) if b.get("type")=="tool_use" and b["name"]=="Bash"]
    segs=[s for c_ in cmds for s in re.split(r"[;\n]|&&", c_)]
    rec=[s for s in segs if REC.search(s) and (DIRARG.search(s+" ") or " -r" in s)]
    rect=[s for s in rec if re.search(r"\btests\b|\s\.(\s|$)", s)]
    mcp=sum(1 for x in arr if x.get("type")=="assistant" for b in x["message"].get("content",[]) if b.get("type")=="tool_use" and b["name"].startswith("mcp__") and ("callers" in b["name"] or "search" in b["name"] or "impact" in b["name"]))
    n[r["model"]]+=1; calls[r["model"]]+=len(rec)
    if rec or mcp: c[r["model"]]+=1
    if rect: ct[r["model"]]+=1
    r["rev_search"]=len(rec); r["rev_tests"]=bool(rect)
print("| model | runs with a recursive repo search (grep -r / rg / find / git grep / codegraph search) | runs with a recursive search over tests/ or the repo root | recursive search segments per run |")
print("|---|---|---|---|")
for m in ["ember","luna","haiku","sonnet","grok","terra","wonder"]:
    print(f"| {m} | {100*c[m]/n[m]:.0f}% | {100*ct[m]/n[m]:.0f}% | {calls[m]/n[m]:.1f} |")
json.dump(R,open("/tmp/pc-patterns/records_gt.json","w"))
