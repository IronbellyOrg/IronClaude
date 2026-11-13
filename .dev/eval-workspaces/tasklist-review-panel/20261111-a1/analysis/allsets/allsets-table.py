"""Direct per-set issue counts for every set (cross-check for the agents) + final table + comparison with agent outputs."""
import json, glob, os, sys
leg = json.load(open("/tmp/issue-legend.json"))
order = [l["label"] for l in leg if l["blocking"]] + [l["label"] for l in leg if not l["blocking"]]
sets = json.load(open("/tmp/allsets.json"))
direct = {}
for s in sets:
    f = {k: 0 for k in order}; b = {k: 0 for k in order}; per = {}
    for r in s["runs"]:
        pf = []
        for l in leg:
            sc = json.load(open(r["scores"][l["pkg_id"]]))
            if l["gt"] in sc["gt_covered_any"]: f[l["label"]] += 1; pf.append(l["label"])
            if l["gt"] in sc["gt_covered_blocking"]: b[l["label"]] += 1
        per[r["run"]] = pf
    found14 = sum(f[l["label"]] for l in leg if l["package"] != "control") / s["n_runs"]
    distinct = sum(1 for k in order if f[k] > 0)
    direct[s["sid"]] = dict(found=f, blk=b, per=per, found14=found14, distinct=distinct)
json.dump(direct, open("/tmp/allsets-direct.json", "w"), indent=1)
# compare with agents if present
agent = {}
for fn in sorted(glob.glob("/tmp/allsets-out/chunk-*.json")):
    for s in json.load(open(fn)): agent[s["sid"]] = s
mism = 0
for sid, a in agent.items():
    d = direct[sid]
    for k in order:
        if a["found"].get(k) != d["found"][k]: mism += 1; print("MISMATCH found", sid, k, a["found"].get(k), d["found"][k])
        if a.get("blocking_credit", {}).get(k) != d["blk"][k]: mism += 1; print("MISMATCH blk", sid, k, a.get("blocking_credit", {}).get(k), d["blk"][k])
print(f"agent sets: {len(agent)} of {len(sets)}; cell mismatches: {mism}")
# table
def cell(k, d):
    v = d["found"][k]
    if not v: return "0"
    return f"{v} ({d['blk'][k]})" if k.startswith("B") else str(v)
L = ["| Set | Panel | Era | Runs | " + " | ".join(order) + " | Found /14 per run | Distinct issues ever |", "|---|---|---|---|" + "---|" * len(order) + "---|---|"]
for s in sets:
    d = direct[s["sid"]]
    L.append(f"| {s['sid']} | {s['set']} | {'src' if s['era']=='source.md' else 'pre-src'} | {s['n_runs']} | " + " | ".join(cell(k, d) for k in order) + f" | {d['found14']:.2f} | {d['distinct']} |")
tot = {k: sum(direct[s['sid']]['found'][k] for s in sets) for k in order}
runs_total = sum(s["n_runs"] for s in sets)
L.append(f"| ALL | all sets | both | {runs_total} | " + " | ".join(str(tot[k]) for k in order) + " | | |")
src = [s for s in sets if s["era"] == "source.md"]
tots = {k: sum(direct[s['sid']]['found'][k] for s in src) for k in order}
L.append(f"| ALL-src | source.md era | src | {sum(s['n_runs'] for s in src)} | " + " | ".join(str(tots[k]) for k in order) + " | | |")
open("/tmp/allsets-table.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
