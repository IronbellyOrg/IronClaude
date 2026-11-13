"""Issue-by-panel table computed directly from score.json (independent cross-check of the 10 agents)."""
import json, glob, sys
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
leg = json.load(open("/tmp/issue-legend.json"))
panels = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/top10.json"))
order = [l["label"] for l in leg if l["blocking"]] + [l["label"] for l in leg if not l["blocking"]]
by = {l["label"]: l for l in leg}
res = []
for pn in panels:
    cnt = {k: 0 for k in order}; blk = {k: 0 for k in order}; den = {"designSpec": 0, "alias": 0, "control": 0}
    for row in pn["rows"]:
        for l in leg:
            sf = glob.glob(f"{E}/arms/scoring/combos/{row}/{l['pkg_id']}/*/score.json")
            if not sf: continue
            s = json.load(open(sf[0]))
            if l["gt"] in s["gt_covered_any"]: cnt[l["label"]] += 1
            if l["gt"] in s["gt_covered_blocking"]: blk[l["label"]] += 1
        for tag, p in (("designSpec", "TASK-WF-designSpec-20261107-075614"), ("alias", "TASK-WF-makeTheAliasOnly-20261105-051649"), ("control", "TASK-WF-design-20261108-041415")):
            if glob.glob(f"{E}/arms/scoring/combos/{row}/{p}/*/score.json"): den[tag] += 1
    res.append(dict(panel=pn["panel"], n=pn["n"], found=cnt, blk=blk, den=den, mean_found=pn["mean_found"]))
json.dump(res, open("/tmp/issue-table-direct.json", "w"), indent=1)
hdr = "| # | Panel | Runs | " + " | ".join(order) + " | Found /14 (mean) |"
sep = "|---|---|---|" + "---|" * len(order) + "---|"
L = [hdr, sep]
for i, r in enumerate(res, 1):
    L.append(f"| {i} | {r['panel']} | {r['n']} | " + " | ".join(str(r['found'][k]) for k in order) + f" | {r['mean_found']} |")
print("\n".join(L))
print("\nLegend:")
for k in order: print(f"{k} [{by[k]['package']} {by[k]['gt']}]: {by[k]['description'][:150]}")
