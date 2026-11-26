"""Confirming test of wonsol: the frozen decision rule of PREREG.md and the descriptive measures.
W (wonsol, run names with -sonnet-) minus B (ember control). M1 = mean of per-run found fractions; M2 = found / possible over all runs.
Bootstrap: resample plans, then runs within plans, 2000 draws, seed 20261120; lower bound = 5th percentile. Confirmed only if M1 and M2 each
show diff >= +0.10 and lower bound > 0. Usage: uv run python -I analyze.py > RESULTS-raw.txt"""
import collections, json, os, random, statistics

RL = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger"
SC, RUNS = f"{RL}/scoring-confirm", f"{RL}/runs-confirm"
runs = {"B": [], "W": []}   # (doc, found, total, wrong, blkfound, panel_s, kills, run, covered)
second = {}
first = {}
for l, run, doc, role in (x.rstrip("\n").split("\t") for x in open(f"{SC}/labels.tsv")):
    p = f"{SC}/{l}/score.json"
    if not os.path.exists(p):
        continue
    j = json.load(open(p))
    if role == "first":
        if not os.path.isdir(f"{RUNS}/{run}"):
            continue
        t = json.load(open(f"{RUNS}/{run}/timing.json"))
        rj = json.load(open(f"{RUNS}/{run}/run.json"))
        kills = sum(1 for v in rj["reviewers"].values() if v.get("killed"))
        arm = "W" if "-sonnet-" in run else "B"
        runs[arm].append((doc, len(j["gt_covered_any"]) / j["gt_total"], j["gt_total"], j["wrong_blockers"], len(j["gt_covered_blocking"]),
                          t["panel_elapsed_s"], kills, run, set(j["gt_covered_any"])))
        first[run] = set(j["gt_covered_any"])
    else:
        second[run] = set(j["gt_covered_any"])
docs = sorted({r[0] for r in runs["B"]})
GT = {d: next(r[2] for r in runs["B"] if r[0] == d) for d in docs}


def stat(sample, mode):
    return sum(f * GT[d] for d, f in sample) / sum(GT[d] for d, f in sample) if mode == "item" else statistics.mean(f for d, f in sample)


def point(arm, mode, skip=()):
    return stat([(r[0], r[1]) for r in runs[arm] if r[0] not in skip], mode)


def boot(mode, skip=(), n=2000):
    random.seed(20261120)
    da, db = collections.defaultdict(list), collections.defaultdict(list)
    for r in runs["W"]:
        if r[0] not in skip: da[r[0]].append((r[0], r[1]))
    for r in runs["B"]:
        if r[0] not in skip: db[r[0]].append((r[0], r[1]))
    ds = sorted(da); out = []
    for _ in range(n):
        ch = [random.choice(ds) for _ in ds]
        xa = [random.choice(da[d]) for d in ch for _ in da[d]]
        xb = [random.choice(db[d]) for d in ch for _ in db[d]]
        out.append(stat(xa, mode) - stat(xb, mode))
    out.sort()
    return out[int(0.05 * n)], out[int(0.95 * n)]


print(f"runs: B {len(runs['B'])}, W {len(runs['W'])}; plans {docs}; items {GT}")
verdict = {}
print("\n## Decision rule (frozen)\nmeasure\tB\tW\tdiff\tlower5\tupper95\tpasses (diff>=+0.10 and lower5>0)")
for name, mode in (("M1 mean per-run fraction", "run"), ("M2 every defect equal", "item")):
    b, w = point("B", mode), point("W", mode); lo, hi = boot(mode)
    ok = (w - b) >= 0.10 and lo > 0
    verdict[mode] = ok
    print(f"{name}\t{b:.3f}\t{w:.3f}\t{w-b:+.3f}\t{lo:+.3f}\t{hi:+.3f}\t{'YES' if ok else 'no'}")
print("\nVERDICT:", "CONFIRMED" if all(verdict.values()) else ("NOT CONFIRMED, split by weighting" if any(verdict.values()) else "NOT CONFIRMED"))

print("\n## Descriptive\nmeasure\tB\tW")
for name, i in (("wrong blockers/run", 3), ("blocking found/run", 4), ("kills/run", 6)):
    print(f"{name}\t{statistics.mean(r[i] for r in runs['B']):.2f}\t{statistics.mean(r[i] for r in runs['W']):.2f}")
mb, mw = statistics.median(r[5] for r in runs["B"]), statistics.median(r[5] for r in runs["W"])
print(f"median panel s\t{mb:.0f}\t{mw:.0f}\tratio {mw/mb:.2f}")
print("\n## Per plan (found fraction mean; B, W)")
for d in docs:
    print(f"{d} (items {GT[d]})\t{statistics.mean(r[1] for r in runs['B'] if r[0]==d):.2f}\t{statistics.mean(r[1] for r in runs['W'] if r[0]==d):.2f}")
print("\n## Leave one plan out (descriptive; diff M1, M2 with lower5)")
for d in docs:
    row = []
    for mode in ("run", "item"):
        lo, _ = boot(mode, (d,)); row.append(f"{point('W',mode,(d,))-point('B',mode,(d,)):+.3f} (lb {lo:+.3f})")
    print(f"without {d}\t" + "\t".join(row))
anyB = set().union(*[r[8] for r in runs["B"]]); print()
for a in ("B", "W"):
    pl = collections.defaultdict(set)
    for r in runs[a]:
        pl[r[0]] |= {f"{r[0]}:{g}" for g in r[8]}
    print(f"{a}: distinct defects found at least once: {sum(len(v) for v in pl.values())} of {sum(GT.values())}")
k = [(len(first[r] & s), len(first[r] | s)) for r, s in second.items() if r in first]
print(f"\nsecond judge: {len(k)} runs, identical found sets in {sum(1 for a, u in k if a == u)}")
