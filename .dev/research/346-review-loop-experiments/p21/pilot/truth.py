"""Pilot ground truth: pair labels from the ledger mapping; label agreement; merge-row baseline."""
import json, itertools, collections
F = json.load(open("findings.json"))
def lab(run, who):
    return json.load(open(f"labels-{run}-{who}.json"))
def pair_truth(L, a, b):
    da, db = set(L[a["key"]]["defects"] or []), set(L[b["key"]]["defects"] or [])
    if da and db:
        return "same" if da == db else "overlap" if da & db else "diff"
    if da or db:
        return "diff"            # one maps to a ledger defect, the other is NEW or NOT_DEFECT
    return "unknown"            # both NEW/NOT_DEFECT: may or may not be the same problem
def pairs(run):
    return [(a, b) for a, b in itertools.combinations(F[run], 2) if a["reviewer"] != b["reviewer"]]
if __name__ == "__main__":
    for run in ("d2-r1", "d2-r2"):
        L = lab(run, "sonnet"); ps = pairs(run)
        c = collections.Counter(pair_truth(L, a, b) for a, b in ps)
        merged = [(a, b) for a, b in ps if a["merge_row"] and a["merge_row"] == b["merge_row"]]
        cm = collections.Counter(pair_truth(L, a, b) for a, b in merged)
        print(run, "cross-reviewer pairs", len(ps), dict(c))
        print("   merge puts in one row:", len(merged), dict(cm), f"-> precision vs same {cm['same']/max(1,sum(v for k,v in cm.items() if k!='unknown')):.2f}, recall {cm['same']/max(1,c['same']):.2f}")
        mapped = sum(1 for f in F[run] if L[f["key"]]["defects"]); print("   findings mapped to ledger:", mapped, "of", len(F[run]), "| distinct defects:", len({d for f in F[run] for d in (L[f['key']]['defects'] or [])}))
    Ls, Lo = lab("d2-r1", "sonnet"), lab("d2-r1", "opus"); ps = pairs("d2-r1")
    agree = collections.Counter((pair_truth(Ls, a, b), pair_truth(Lo, a, b)) for a, b in ps)
    print("d2-r1 Sonnet vs Opus pair labels:", {f"{k[0]}/{k[1]}": v for k, v in agree.items() if v})
    fa = sum((Ls[f["key"]]["defects"] or [None])[0] == (Lo[f["key"]]["defects"] or [None])[0] for f in F["d2-r1"])
    print("d2-r1 finding-level agreement on main defect (incl. both none):", fa, "/", len(F["d2-r1"]))
