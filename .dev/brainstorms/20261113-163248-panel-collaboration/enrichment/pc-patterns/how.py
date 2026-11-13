import json,re
E="/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
R=json.load(open("/tmp/pc-patterns/records_gt.json"))
for r in R:
    if r["pkg"]!="DE" or not any(f.endswith("test_worker_contract.py") for f in r["repo_files"]): continue
    arr=json.load(open(f"{E}/TASK-WF-design-20261108-041415/reviews/combos/{r['run']}/{r['rid']}.attempt{r['attempt']}.json"))
    prev=None
    for x in arr:
        if x.get("type")=="assistant":
            for b in x["message"].get("content",[]):
                if b.get("type")=="tool_use":
                    s=json.dumps(b["input"])
                    if "worker_contract" in s:
                        print(r["model"],r["run"],"| PREV:",(prev or "")[:200],"\n   HIT:",s[:260]); break
                    prev=s
            else: continue
            break
# how many DE runs grepped tests/ for gh api or for the edited file names (reverse dependency search)
pat=re.compile(r"grep[^\n|;]*(tests|-r)[^\n]*(gh api|create\.md|labels\.md|issue-worker-t3|SKILL\.md)")
import collections
c=collections.Counter(); n=collections.Counter()
for r in R:
    if r["pkg"]!="DE": continue
    arr=json.load(open(f"{E}/TASK-WF-design-20261108-041415/reviews/combos/{r['run']}/{r['rid']}.attempt{r['attempt']}.json"))
    cmds=[b["input"].get("command","") for x in arr if x.get("type")=="assistant" for b in x["message"].get("content",[]) if b.get("type")=="tool_use" and b["name"]=="Bash"]
    n[r["model"]]+=1
    if any(re.search(r"grep[^\n]*\btests\b", c_) and re.search(r"gh api|create\.md|labels\.md|issue-worker-t3|sc-issue-protocol|SKILL\.md", c_) for c_ in cmds): c[r["model"]]+=1
print({m: f"{c[m]}/{n[m]}" for m in n})
