import json, os, re, collections, hashlib
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PK = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
rows = [r for r in sorted(os.listdir(f"{E}/combos")) if not re.search(r"contaminated|superseded|quarantine|^i1-|^i2-", r)]
cats = collections.Counter()
reasons = collections.Counter()
out = []
for row in rows:
    for pkg in PK:
        d = f"{E}/combos/{row}/{pkg}"
        if not os.path.exists(f"{d}/ledger.json"):
            continue
        led = json.load(open(f"{d}/ledger.json"))
        for rv in led["rounds"][-1]["reviewers"]:
            cats[("ledger_cats", )] += 0
            if rv["block_ok"]:
                continue
            rid = rv["reviewer_id"]
            rp = rv["report"]
            t = open(rp, errors="replace").read() if os.path.exists(rp) else ""
            m = re.findall(r"```findings-v1\s*\n(.*?)```", t, re.S)
            fs = []
            if m:
                for ln in m[-1].splitlines():
                    if ln.strip():
                        try: fs.append(json.loads(ln))
                        except Exception: fs.append({"id": "?", "category": "UNPARSABLE"})
            kept = {mm["fid"] for r in led["rows"] for mm in r["members"] if mm["reviewer_id"] == rid}
            dropped = [f for f in fs if f.get("id") not in kept]
            c = tuple(sorted({(f.get("category"), f.get("severity")) for f in dropped}))
            reasons[tuple(sorted({f.get("category") for f in dropped})) or ("none-dropped",)] += 1
            out.append((row, pkg[8:20], rid, len(fs), len(kept), [(f.get("id"), f.get("category")) for f in dropped]))
print(reasons)
for o in out[:90]:
    print(o)
# category universe from all ledgers
u = collections.Counter()
for row in rows:
    for pkg in PK:
        p = f"{E}/combos/{row}/{pkg}/ledger.json"
        if os.path.exists(p):
            for r in json.load(open(p))["rows"]:
                u[r["category"]] += 1
print(u)
