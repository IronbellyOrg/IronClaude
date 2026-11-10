#!/usr/bin/env python3
"""O4: same-model union baseline. Themes T1,T2,T3 found by the R1 of 12 arm-2/3 runs; all C(12,k) subsets, k=1..4."""
import itertools, json, pathlib, sys
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1")
import c93
SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
R = ".dev/orca-command-refactor/review/round1.md"
runs = [f"a{a}-r{r}" for a in (2, 3) for r in range(1, 7)]
found = {}
for run in runs:
    found[run] = {t for _id, t in c93.blocking_tags(SP / "p11/runs" / run / "ws" / R) if t in ("T1", "T2", "T3")}
    print(run, sorted(found[run]))
out = {"per_run": {k: sorted(v) for k, v in found.items()}, "k": {}}
cat = SP / "p13/catalog/catalog.json"
for k in (1, 2, 3, 4):
    subs = list(itertools.combinations(runs, k))
    sizes = [len(set().union(*(found[r] for r in s))) for s in subs]
    share = {t: sum(t in set().union(*(found[r] for r in s)) for s in subs) / len(subs) for t in ("T1", "T2", "T3")}
    out["k"][k] = {"subsets": len(subs), "mean_themes": sum(sizes) / len(sizes), "share": share}
    print(f"k={k} subsets={len(subs)} mean distinct themes={sum(sizes)/len(sizes):.3f} share T1={share['T1']:.3f} T2={share['T2']:.3f} T3={share['T3']:.3f}")
print("catalog-level repeat:", "catalog.json present but cluster-level union not computed offline" if cat.exists() else "skipped: catalog.json does not exist (PN3 builds it)")
pathlib.Path(__file__).with_name("o4-union.json").write_text(json.dumps(out, indent=1))

# ---- cluster level (catalog-v1), confirmed clusters only
if cat.exists():
    cd = json.loads(cat.read_text())
    conf = {c["cid"]: c for c in cd["clusters"] if c.get("confirmed")}
    cf = {run: set() for run in runs}
    for cid, c in conf.items():
        for m in c["members"]:
            src, _, step = m["source"].partition("/")
            if src in cf and step == "R1" and m.get("blocking"):
                cf[src].add(cid)
    out["catalog"] = {"confirmed_clusters": len(conf), "per_run": {k: sorted(v) for k, v in cf.items()}, "k": {}}
    print(f"catalog-level: {len(conf)} confirmed clusters; per run R1 confirmed-cluster counts:", {k: len(v) for k, v in cf.items()})
    for k in (1, 2, 3, 4):
        subs = list(itertools.combinations(runs, k))
        sizes = [len(set().union(*(cf[r] for r in s))) for s in subs]
        out["catalog"]["k"][k] = {"mean_confirmed_clusters": sum(sizes) / len(sizes), "recall_of_confirmed": sum(sizes) / len(sizes) / len(conf)}
        print(f"  k={k} mean distinct confirmed clusters={sum(sizes)/len(sizes):.2f} (recall {sum(sizes)/len(sizes)/len(conf):.3f})")
    pathlib.Path(__file__).with_name("o4-union.json").write_text(json.dumps(out, indent=1))
