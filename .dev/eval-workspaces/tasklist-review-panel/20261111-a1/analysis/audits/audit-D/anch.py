import json, os, re, collections
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PK = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
rows = [r for r in sorted(os.listdir(f"{E}/combos")) if not re.search(r"contaminated|superseded|quarantine|^i1-|^i2-", r)]
cand = {p: open(f"{E}/{p}/candidate.md").read() for p in PK}
st = collections.Counter()
ex = []
for row in rows:
    for pkg in PK:
        d = f"{E}/combos/{row}/{pkg}"
        if not os.path.exists(f"{d}/ledger.json"):
            continue
        led = json.load(open(f"{d}/ledger.json"))
        for rv in led["rounds"][-1]["reviewers"]:
            rp = rv["report"]
            t = open(rp, errors="replace").read() if os.path.exists(rp) else ""
            m = re.findall(r"```findings-v1\s*\n(.*?)```", t, re.S)
            kept = {mm["fid"] for r in led["rows"] for mm in r["members"] if mm["reviewer_id"] == rv["reviewer_id"]}
            for ln in (m[-1].splitlines() if m else []):
                if not ln.strip():
                    continue
                f = json.loads(ln)
                a1 = f.get("anchor", ""); a2 = f.get("anchor2", "")
                ok1 = a1 in cand[pkg]; ok2 = (a2 in cand[pkg]) if a2 else None
                k = f["id"] in kept
                st[(rv["block_ok"], k, ok1, ok2)] += 1
                if not k and rv["block_ok"] is False and len(ex) < 4:
                    ex.append((row, pkg[8:20], rv["reviewer_id"], f["id"], ok1, ok2, a1[:80], (a2 or "")[:80]))
for k, v in sorted(st.items(), key=str):
    print("block_ok,kept,anchor1_in_cand,anchor2_in_cand =", k, v)
for e in ex: print(e)
