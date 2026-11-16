"""Analysis of the severity-rule test (gates in PREREG.md). Reads judge scores, never ground truth text beyond item counts/flags.

    uv run --no-project python -I analyze_s.py --scoring scoring --runs runs --gt ../20261114-recipe-ledger/holdout-gt --out results
"""
import argparse
import json
import random
import statistics
from collections import defaultdict
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--scoring", required=True)
ap.add_argument("--runs", required=True)
ap.add_argument("--gt", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--seed", type=int, default=20261122)
a = ap.parse_args()
sc, rd, gtd, out = Path(a.scoring), Path(a.runs), Path(a.gt), Path(a.out)
out.mkdir(parents=True, exist_ok=True)

n_items, n_blk = {}, {}
for d in sorted(gtd.iterdir()):
    f = d / "ground-truth.json"
    if f.is_file():
        it = json.load(open(f))["items"]
        n_items[d.name], n_blk[d.name] = len(it), sum(bool(i.get("blocking_in_implement")) for i in it)

runs = []
for line in open(sc / "labels.tsv"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 4 or p[3] != "first":
        continue
    label, run, doc = p[0], p[1], p[2]
    f = sc / label / "score.json"
    if not f.is_file():
        continue
    s = json.load(open(f))
    arm = run.split("-")[1].upper()  # sev1-z0-HO-2-r1 -> Z0, sev1-s-... -> S
    t = {}
    try:
        t = json.load(open(rd / run / "timing.json"))
    except OSError:
        pass
    runs.append(dict(arm=arm, doc=doc, run=run, found=len(s["gt_covered_any"]), blk=len(s["gt_covered_blocking"]),
                     rows_blk=s["ledger_rows_blocking"], matched=s["blocking_rows_gt_matched"], wrong=s["wrong_blockers"],
                     rows=s["ledger_rows_total"], elapsed=t.get("panel_elapsed_s")))

by = defaultdict(list)
for r in runs:
    by[r["arm"]].append(r)


def mean(xs):
    xs = list(xs)
    return statistics.fmean(xs) if xs else None


def agg(rs):
    ff = mean(r["found"] / n_items[r["doc"]] for r in rs)
    bd = [r for r in rs if n_blk[r["doc"]]]
    return dict(runs=len(rs), found_fraction=ff,
                blocking_fraction=mean(r["blk"] / n_blk[r["doc"]] for r in bd) if bd else None,
                wrong_per_run=mean(r["wrong"] for r in rs), blocking_rows_per_run=mean(r["rows_blk"] for r in rs),
                matched_total=sum(r["matched"] for r in rs), blocking_rows_total=sum(r["rows_blk"] for r in rs),
                precision=(sum(r["matched"] for r in rs) / max(1, sum(r["rows_blk"] for r in rs))),
                rows_per_run=mean(r["rows"] for r in rs),
                median_elapsed=statistics.median([r["elapsed"] for r in rs if r["elapsed"]]) if any(r["elapsed"] for r in rs) else None)


res = {"arms": {k: agg(v) for k, v in by.items()}, "per_doc": {}}
for k, v in by.items():
    for d in n_items:
        rs = [r for r in v if r["doc"] == d]
        if rs:
            res["per_doc"][f"{k} {d}"] = agg(rs)

z, s = res["arms"].get("Z0"), res["arms"].get("S")
gates = {}
if z and s:
    gates["G1 wrong blockers per run: S at most 0.70 x Z0"] = (s["wrong_per_run"] <= 0.70 * z["wrong_per_run"] + 1e-9,
                                                              f"Z0 {z['wrong_per_run']:.2f}, S {s['wrong_per_run']:.2f}, ratio {s['wrong_per_run'] / z['wrong_per_run']:.2f}" if z["wrong_per_run"] else f"Z0 0, S {s['wrong_per_run']:.2f}")
    gates["G2 real blocking matched (total over runs): S at least Z0"] = (s["matched_total"] >= z["matched_total"], f"Z0 {z['matched_total']}, S {s['matched_total']}")
    gates["G3 found fraction: S at least Z0 - 0.02"] = (s["found_fraction"] >= z["found_fraction"] - 0.02 - 1e-9, f"Z0 {z['found_fraction']:.3f}, S {s['found_fraction']:.3f}")
    if z["median_elapsed"] and s["median_elapsed"]:
        r = s["median_elapsed"] / z["median_elapsed"]
        gates["G4 pooled median time: S at most 1.10 x Z0"] = (r <= 1.10, f"ratio {r:.2f} (Z0 {z['median_elapsed']:.1f} s, S {s['median_elapsed']:.1f} s)")
    rng = random.Random(a.seed)
    docs = sorted(n_items)
    diffs = []
    for _ in range(2000):
        zs, ss = [], []
        for d in (rng.choice(docs) for _ in docs):
            zr = [r["wrong"] for r in by["Z0"] if r["doc"] == d]; sr = [r["wrong"] for r in by["S"] if r["doc"] == d]
            if zr and sr:
                zs += [rng.choice(zr) for _ in zr]; ss += [rng.choice(sr) for _ in sr]
        if zs and ss:
            diffs.append(statistics.fmean(ss) - statistics.fmean(zs))
    diffs.sort()
    res["wrong_blockers_diff_S_minus_Z0_90pct_interval"] = [diffs[int(0.05 * len(diffs))], diffs[int(0.95 * len(diffs))]]
res["gates"] = {k: {"pass": bool(v[0]), "detail": v[1]} for k, v in gates.items()}
res["decision"] = ("ADOPT-CANDIDATE: all gates pass" if gates and all(v[0] for v in gates.values())
                   else "DO NOT ADOPT: failed " + "; ".join(k.split(":")[0] for k, v in gates.items() if not v[0]))
json.dump(res, open(out / "metrics.json", "w"), indent=1)
L = ["# Severity-rule test: analysis", "", f"Runs scored: {len(runs)} (Z0 {len(by['Z0'])}, S {len(by['S'])}); seed {a.seed}.", "", f"**Decision: {res['decision']}**", "",
     "| Arm | runs | found fraction | blocking fraction | wrong blockers/run | blocking rows/run | blocking precision | rows/run | median s |", "|---|---|---|---|---|---|---|---|---|"]
for k, v in res["arms"].items():
    f = lambda x, d=3: "-" if x is None else f"{x:.{d}f}"
    L.append(f"| {k} | {v['runs']} | {f(v['found_fraction'])} | {f(v['blocking_fraction'])} | {f(v['wrong_per_run'], 2)} | {f(v['blocking_rows_per_run'], 2)} | {f(v['precision'], 2)} ({v['matched_total']}/{v['blocking_rows_total']}) | {f(v['rows_per_run'], 1)} | {f(v['median_elapsed'], 1)} |")
L += ["", "## Gates", ""] + [f"- {'PASS' if g['pass'] else 'FAIL'} {k}: {g['detail']}" for k, g in res["gates"].items()]
if "wrong_blockers_diff_S_minus_Z0_90pct_interval" in res:
    lo, hi = res["wrong_blockers_diff_S_minus_Z0_90pct_interval"]
    L += ["", f"Wrong blockers per run, S minus Z0, 90% bootstrap interval (documents, then runs): [{lo:.2f}, {hi:.2f}]"]
L += ["", "## Per document", ""] + [f"- {k}: found {v['found_fraction']:.3f}, wrong/run {v['wrong_per_run']:.2f}, blocking rows/run {v['blocking_rows_per_run']:.2f}, matched {v['matched_total']}/{v['blocking_rows_total']}" for k, v in res["per_doc"].items()]
open(out / "report.md", "w").write("\n".join(L) + "\n")
print(res["decision"])
