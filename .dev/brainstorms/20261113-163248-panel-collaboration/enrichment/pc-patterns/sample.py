import json,glob,random,collections
E="/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
R=json.load(open("/tmp/pc-patterns/records.json"))
random.seed(1)
for m in ["sonnet","haiku","ember","luna"]:
    rs=[r for r in R if r["model"]==m]
    for r in random.sample(rs,2):
        pkg={"DS":"TASK-WF-designSpec-20261107-075614","AL":"TASK-WF-makeTheAliasOnly-20261105-051649","DE":"TASK-WF-design-20261108-041415"}[r["pkg"]]
        arr=json.load(open(f"{E}/{pkg}/reviews/combos/{r['run']}/{r['rid']}.attempt{r['attempt']}.json"))
        print("=====",m,r["run"],r["pkg"],r["rid"])
        for x in arr:
            if x.get("type")=="assistant":
                for b in x["message"].get("content",[]):
                    if b.get("type")=="tool_use":
                        print("  ",b["name"], json.dumps(b["input"])[:220])
