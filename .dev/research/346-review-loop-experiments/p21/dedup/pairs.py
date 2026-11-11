"""Test 1 ground truth: pairs of first-review findings in the same run, labelled by their p17 ledger mapping."""
import json, glob, itertools, collections, re
P17 = "/home/user/IronClaude/.dev/research/346-review-loop-experiments/p17"
F = [json.loads(l) for l in open(f"{P17}/findings.jsonl")]
L = json.load(open(f"{P17}/ledger.json"))
src = collections.defaultdict(set)
for d in L["defects"]:
    for s in d["sources"]:
        src[s].add(d["id"])
g2d = collections.defaultdict(set)
for f in sorted(glob.glob(f"{P17}/chunk-outputs/*.json")):
    for d in json.load(open(f))["defects"]:
        for g in d.get("gids", []):
            g2d[g] |= src.get(d["local_id"], set())
def lines(f):
    return set(int(x) for x in re.findall(r"SPEC:(\d+)", f["heading"] + " " + f["body"])) | set(f.get("cited") or [])
byrun = collections.defaultdict(list)
for f in F:
    if f["kind"] == "first" and g2d.get(f["gid"]):
        byrun[(f["arm"], f["run"])].append(f)
pairs = []
for (arm, run), fs in byrun.items():
    for a, b in itertools.combinations(fs, 2):
        la, lb = lines(a), lines(b)
        pairs.append({"id": f"{a['gid']}-{b['gid']}", "arm": arm, "run": run, "a": a["gid"], "b": b["gid"],
                      "same_reviewer": a["step"] == b["step"], "same": g2d[a["gid"]] == g2d[b["gid"]], "overlap": bool(g2d[a["gid"]] & g2d[b["gid"]]), "da": sorted(g2d[a["gid"]]), "db": sorted(g2d[b["gid"]]),
                      "shared_lines": len(la & lb), "jacc": round(len(la & lb) / max(1, len(la | lb)), 3)})
json.dump(pairs, open("pairs.json", "w"), indent=0)
c = collections.Counter(("same" if p["same"] else "overlap" if p["overlap"] else "diff", p["same_reviewer"]) for p in pairs)
print(len(pairs), c, "runs", len(byrun))
print("cross-reviewer positives", sum(p["same"] and not p["same_reviewer"] for p in pairs))
