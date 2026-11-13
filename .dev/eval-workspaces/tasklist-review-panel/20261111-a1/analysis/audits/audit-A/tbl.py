import json,os,collections
E="/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
P=["TASK-WF-designSpec-20261107-075614","TASK-WF-makeTheAliasOnly-20261105-051649","TASK-WF-design-20261108-041415"]
rows=collections.defaultdict(lambda: collections.defaultdict(set))
for p in P:
    b=f"{E}/{p}/reviews/combos"
    for r in os.listdir(b):
        if any(s in r for s in("contaminated","superseded","quarantine")):continue
        for f in os.listdir(f"{b}/{r}"):
            if f.endswith(".meta.json") and ".attempt" not in f:
                m=json.load(open(f"{b}/{r}/{f}")); rows[r][f.split(".")[0]].add(m["observed_model"]+("" if m["observed_model"]==m["expected_model"] else "!exp="+m["expected_model"]))
for r in sorted(rows):
    res=os.path.exists(f"{E}/combos/{r}/{P[0]}/resolution.json")
    print(("R " if res else "- ")+r, {k:sorted(v) for k,v in sorted(rows[r].items())})
