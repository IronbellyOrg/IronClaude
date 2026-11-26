import glob, json, os, re, collections
E="/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
DS="TASK-WF-designSpec-20261107-075614"
d=f"{E}/{DS}/reviews/combos"
def ms(r):
    return tuple(sorted(json.load(open(f))["expected_model"] for f in glob.glob(f"{d}/{r}/*.meta.json") if "attempt" not in f))
for r in sorted(os.listdir(d)):
    m=re.match(r"(.*)-(contaminated|superseded)-\d+$", r)
    if m:
        live=m.group(1)
        a,b=ms(r),(ms(live) if os.path.isdir(f"{d}/{live}") else None)
        print(r, "SAME" if a==b else f"DIFF {a} vs {b}")
# i1/i2 + e4 scoring presence
for r in ("i1-grok-sonnet-r1","i2-haiku-sonnet-r1","e4-haiku2-ember","b4-muse-luna2"):
    print(r, ms(r), os.path.isdir(f"{E}/arms/scoring/combos/{r}"), len(glob.glob(f"{d}/{r}/*.cost.json")))
