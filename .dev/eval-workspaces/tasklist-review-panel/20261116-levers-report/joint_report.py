"""Joint report of the levers tests on the four hold-out plans, rebuilt from score.json files (nothing typed by hand).

Sources (each: scoring dir with labels.tsv + <label>/score.json, run dirs holding <run>/run.json and timing.json):
  --source NAME=SCORING_DIR:RUNS_DIR[,RUNS_DIR...][:INVALID_DIR]    (repeat)
  --arm-rule NAME:REGEX=ARMNAME                                     (repeat; first match wins; applied to the run folder name)
Ground truth: --gt DIR (holdout-gt/<doc>/ground-truth.json; only item counts and blocking flags are read).

    uv run --no-project python -I joint_report.py --gt ../20261114-recipe-ledger/holdout-gt --out REPORT-DIR \
        --source sev=../20261116-severity-test/results/scoring:../20261116-severity-test/results/runs ...

Rules fixed before any score of either test was read (PREREG.md and PREREG-ADDENDUM-1.md of 20261116-severity-test):
  - each test keeps its own gate: severity test G1 to G4 against its interleaved Z0; stronger-panel test: lever = found fraction
    difference >= +0.10 and bootstrap lower bound (documents, then runs; 2,000 draws, seed 20261120; 5th percentile) > 0 against arm B;
  - the two ember Z0 controls are pooled only if the 90% bootstrap interval of their difference contains 0 on found fraction AND on
    wrong blockers; otherwise each lever is judged against its own control;
  - "invalid" runs of the second test are shown as-run (the moved-aside originals) and with reruns substituted;
  - several arms against one control: a single hit among them is weak evidence; no multiplicity correction is applied.
"""
import argparse
import json
import random
import re
import statistics
from collections import defaultdict
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--gt", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--source", action="append", default=[])
ap.add_argument("--arm-rule", action="append", default=[])
ap.add_argument("--seed", type=int, default=20261120)
ap.add_argument("--draws", type=int, default=2000)
a = ap.parse_args()
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)

n_items, n_blk = {}, {}
for d in sorted(Path(a.gt).iterdir()):
    f = d / "ground-truth.json"
    if f.is_file():
        it = json.load(open(f))["items"]
        n_items[d.name], n_blk[d.name] = len(it), sum(bool(i.get("blocking_in_implement")) for i in it)

rules = []
for r in a.arm_rule:
    name, rest = r.split(":", 1)
    rx, arm = rest.rsplit("=", 1)
    rules.append((name, re.compile(rx), arm))


def arm_of(source, run):
    base = run.split(".original")[0]
    for s, rx, arm in rules:
        if s == source and rx.search(base):
            return arm
    return None


def read_json(p):
    try:
        return json.load(open(p))
    except (OSError, ValueError):
        return None


def collect(source, scoring, run_dirs, invalid_dir):
    """[{arm, doc, rep, run, original, found, blk, rows_blk, matched, wrong, rows, elapsed, killed}] of the first judge's scores."""
    rows = []
    sc = Path(scoring)
    labels = {}
    for line in open(sc / "labels.tsv"):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 4 and p[3] == "first":
            labels[p[1]] = (p[0], p[2])
    dirs = [(Path(d), False) for d in run_dirs] + ([(Path(invalid_dir), True)] if invalid_dir else [])
    for rd, is_inv in dirs:
        if not rd.is_dir():
            continue
        for rdir in sorted(rd.iterdir()):
            if not rdir.is_dir() or not (rdir / "run.json").exists():
                continue
            run = rdir.name
            arm = arm_of(source, run)
            if arm is None or run not in labels:
                continue
            label, doc = labels[run]
            s = read_json(sc / label / "score.json")
            if s is None:
                continue
            rj = read_json(rdir / "run.json") or {}
            tj = read_json(rdir / "timing.json") or {}
            rev = rj.get("reviewers") or {}
            m = re.search(r"-r(\d+)", run)
            rows.append(dict(source=source, arm=arm, doc=doc, rep=int(m.group(1)) if m else 0, run=run, original=is_inv or ".original" in run,
                             found=len(s["gt_covered_any"]), blk=len(s["gt_covered_blocking"]), rows_blk=s["ledger_rows_blocking"],
                             matched=s["blocking_rows_gt_matched"], wrong=s["wrong_blockers"], rows=s["ledger_rows_total"],
                             elapsed=tj.get("panel_elapsed_s"), conc=rj.get("concurrent_panels_at_start"),
                             killed=any(v.get("killed") for v in rev.values()),
                             bad_status=any(v.get("status") not in ("ok", None) for v in rev.values())))
    return rows


allruns = []
for spec in a.source:
    name, rest = spec.split("=", 1)
    parts = rest.split(":")
    scoring, rdirs = parts[0], parts[1].split(",")
    inv = parts[2] if len(parts) > 2 else None
    allruns += collect(name, scoring, rdirs, inv)


def cells(runs, substituted):
    """One run per (source, arm, doc, rep): as-run prefers the moved-aside original, substituted prefers the rerun."""
    best = {}
    for r in runs:
        k = (r["source"], r["arm"], r["doc"], r["rep"])
        cur = best.get(k)
        if cur is None or (r["original"] == (not substituted)):
            best[k] = r
    return list(best.values())


def agg(rs):
    if not rs:
        return None
    bd = [r for r in rs if n_blk.get(r["doc"])]
    mt = sum(r["matched"] for r in rs)
    rb = sum(r["rows_blk"] for r in rs)
    el = [r["elapsed"] for r in rs if r["elapsed"]]
    return dict(runs=len(rs), found_fraction=statistics.fmean(r["found"] / n_items[r["doc"]] for r in rs),
                blocking_found_fraction=statistics.fmean(r["blk"] / n_blk[r["doc"]] for r in bd) if bd else None,
                wrong_per_run=statistics.fmean(r["wrong"] for r in rs), blocking_rows_per_run=statistics.fmean(r["rows_blk"] for r in rs),
                matched_total=mt, blocking_rows_total=rb, precision=mt / rb if rb else None,
                median_s=statistics.median(el) if el else None, killed_runs=sum(r["killed"] for r in rs),
                bad_status_runs=sum(r["bad_status"] for r in rs),
                conc_range=[min(c), max(c)] if (c := [r["conc"] for r in rs if isinstance(r.get("conc"), int)]) else None)


def census_originals():
    """Moved-aside originals (never judged): per source/arm, how many and why (killed reviewer, bad report status, other)."""
    out_ = defaultdict(lambda: {"runs": 0, "killed": 0, "bad_status": 0, "other": 0})
    for spec in a.source:
        name, rest = spec.split("=", 1)
        parts = rest.split(":")
        inv = parts[2] if len(parts) > 2 else None
        for d in ([inv] if inv else []):
            for rdir in sorted(Path(d).iterdir()) if Path(d).is_dir() else []:
                rj = read_json(rdir / "run.json") if rdir.is_dir() else None
                arm = arm_of(name, rdir.name)
                if rj is None or arm is None:
                    continue
                rev = rj.get("reviewers") or {}
                c = out_[f"{name}/{arm}"]
                c["runs"] += 1
                k = any(v.get("killed") for v in rev.values())
                b = any(v.get("status") not in ("ok", None) for v in rev.values())
                c["killed"] += k
                c["bad_status"] += (b and not k)
                c["other"] += (not k and not b)
    return dict(out_)


def boot_diff(x, y, key, rng, draws):
    """Sorted differences (mean y - mean x) of a per-run value; documents resampled first, then runs."""
    docs = sorted(n_items)
    out_ = []
    for _ in range(draws):
        xs, ys = [], []
        for d in (rng.choice(docs) for _ in docs):
            xr = [key(r) for r in x if r["doc"] == d]
            yr = [key(r) for r in y if r["doc"] == d]
            if xr and yr:
                xs += [rng.choice(xr) for _ in xr]
                ys += [rng.choice(yr) for _ in yr]
        if xs and ys:
            out_.append(statistics.fmean(ys) - statistics.fmean(xs))
    out_.sort()
    return out_


def interval(d, lo=0.05, hi=0.95):
    return (d[int(lo * len(d))], d[min(len(d) - 1, int(hi * len(d)))]) if d else (None, None)


ff = lambda r: r["found"] / n_items[r["doc"]]
res = {"views": {}}
for view, sub in (("as_run", False), ("rerun_substituted", True)):
    cs = cells(allruns, sub)
    by = defaultdict(list)
    for r in cs:
        by[(r["source"], r["arm"])].append(r)
    res["views"][view] = {f"{s}/{ar}": agg(v) for (s, ar), v in sorted(by.items())}
res["n_runs_scored"] = len(allruns)

# controls
rng = random.Random(a.seed)
sub = cells(allruns, True)
byk = defaultdict(list)
for r in sub:
    byk[(r["source"], r["arm"])].append(r)
# the two same-day controls named in the agreement: the severity test's interleaved Z0 and the stronger-panel test's arm B
controls = [k for k in (("sev", "Z0"), ("stronger", "B")) if k in byk]
res["controls"] = [f"{s}/{ar}" for s, ar in controls]
if len(controls) >= 2:
    c1, c2 = byk[controls[0]], byk[controls[1]]
    d1 = interval(boot_diff(c1, c2, ff, rng, a.draws), 0.05, 0.95)
    d2 = interval(boot_diff(c1, c2, lambda r: r["wrong"], rng, a.draws), 0.05, 0.95)
    res["control_difference_90pct"] = {"found_fraction": d1, "wrong_blockers": d2}
    res["pool_controls"] = bool(d1[0] is not None and d1[0] <= 0 <= d1[1] and d2[0] <= 0 <= d2[1])

# stronger-panel lever rule (arms other than B in source 'stronger'), against arm B
res["stronger_panel"] = {}
for (s, ar), v in byk.items():
    if s == "stronger" and ar != "B" and ("stronger", "B") in byk:
        d = boot_diff(byk[("stronger", "B")], v, ff, random.Random(a.seed), a.draws)
        lo, hi = interval(d, 0.05, 0.95)
        diff = statistics.fmean(map(ff, v)) - statistics.fmean(map(ff, byk[("stronger", "B")]))
        res["stronger_panel"][ar] = dict(difference=diff, lower_bound_5pct=lo, lever=bool(diff >= 0.10 and lo is not None and lo > 0))

# secondary (not a pre-registered decision): the same lever rule against the two same-day controls pooled, only if pooling was allowed
res["stronger_vs_pooled_controls"] = {}
if res.get("pool_controls"):
    pooled = [r for k in controls for r in byk[k]]
    for (s, ar), v in byk.items():
        if s == "stronger" and ar != "B":
            d = boot_diff(pooled, v, ff, random.Random(a.seed), a.draws)
            lo, _ = interval(d, 0.05, 0.95)
            diff = statistics.fmean(map(ff, v)) - statistics.fmean(map(ff, pooled))
            res["stronger_vs_pooled_controls"][ar] = dict(difference=diff, lower_bound_5pct=lo, lever=bool(diff >= 0.10 and lo is not None and lo > 0))
    res["pooled_control_found_fraction"] = statistics.fmean(map(ff, pooled))

# sensitivity (descriptive): found-fraction difference against the arm's own control when one document is left out, all arms
res["leave_one_document_out"] = {}
own = {"stronger": ("stronger", "B"), "sev": ("sev", "Z0"), "holdout": ("holdout", "Z0")}
for (s, ar), v in sorted(byk.items()):
    ck = own.get(s)
    if ck is None or ck not in byk or ar in (ck[1],):
        continue
    row = {}
    for d in sorted(n_items):
        keep = lambda rs: [r for r in rs if r["doc"] != d]
        row[f"without {d}"] = statistics.fmean(map(ff, keep(v))) - statistics.fmean(map(ff, keep(byk[ck])))
    row["all four"] = statistics.fmean(map(ff, v)) - statistics.fmean(map(ff, byk[ck]))
    res["leave_one_document_out"][f"{s}/{ar}"] = row

# severity test gates (source 'sev': arms Z0 and S)
sz, ss = agg(byk.get(("sev", "Z0"), [])), agg(byk.get(("sev", "S"), []))
if sz and ss:
    res["severity_gates"] = {
        "G1 wrong blockers S <= 0.70 x Z0": ss["wrong_per_run"] <= 0.70 * sz["wrong_per_run"] + 1e-9,
        "G2 real blocking matches S >= Z0": ss["matched_total"] >= sz["matched_total"],
        "G3 found fraction S >= Z0 - 0.02": ss["found_fraction"] >= sz["found_fraction"] - 0.02 - 1e-9,
        "G4 pooled median time S <= 1.10 x Z0": bool(sz["median_s"] and ss["median_s"] and ss["median_s"] <= 1.10 * sz["median_s"]),
    }
json.dump(res, open(out / "metrics.json", "w"), indent=1, default=str)

f3 = lambda x: "-" if x is None else f"{x:.3f}"
L = ["# Joint report: levers on the plain ember panel, four hold-out plans", ""]
_plain = Path(__file__).resolve().parent / "SUMMARY-plain.md"
if _plain.exists():  # hand-written plain-language summary (owner order 2026-11-17); the tables below are generated
    L += [_plain.read_text().rstrip(), ""]
L += [f"Built by `joint_report.py` from {res['n_runs_scored']} scored runs; rerun it to reproduce every number in the tables. The summary above and the notes after the tables are hand-written.", ""]
for view in ("as_run", "rerun_substituted"):
    L += [f"## All arms ({view.replace('_', ' ')})", "",
          "| Source/arm | runs | found fraction | blocking found | wrong blockers/run | blocking precision | median s | load at start (other claude processes, min-max) | runs with a killed reviewer |", "|---|---|---|---|---|---|---|---|---|"]
    for k, v in res["views"][view].items():
        cr = "-" if not v["conc_range"] else f"{v['conc_range'][0]}-{v['conc_range'][1]}"
        L.append(f"| {k} | {v['runs']} | {f3(v['found_fraction'])} | {f3(v['blocking_found_fraction'])} | {v['wrong_per_run']:.2f} | "
                 f"{f3(v['precision'])} ({v['matched_total']}/{v['blocking_rows_total']}) | {f3(v['median_s'])} | {cr} | {v['killed_runs']} |")
    L.append("")
    if view == "as_run":
        L += ["Moved-aside originals are never judged, so as-run scores exist only where a run needed no rerun; the table below lists what was moved aside and why. "
              "Elapsed times are comparable only between arms with a similar load column.", ""]
res["moved_aside_originals"] = census_originals()
if res["moved_aside_originals"]:
    L += ["## Moved-aside originals (invalid first attempts, rerun once; never judged)", "", "| Source/arm | moved aside | killed reviewer | other bad report status | other |", "|---|---|---|---|---|"]
    for k, c in sorted(res["moved_aside_originals"].items()):
        L.append(f"| {k} | {c['runs']} | {c['killed']} | {c['bad_status']} | {c['other']} |")
    L.append("")
json.dump(res, open(out / "metrics.json", "w"), indent=1, default=str)
if "severity_gates" in res:
    L += ["## Severity-rule test gates (own control, interleaved)", ""] + [f"- {'PASS' if v else 'FAIL'} {k}" for k, v in res["severity_gates"].items()] + [""]
if res["stronger_panel"]:
    L += ["## Stronger-panel test (lever = difference >= +0.10 and bootstrap lower bound above 0, against its same-day arm B)", ""]
    for ar, v in res["stronger_panel"].items():
        L.append(f"- {ar}: difference {v['difference']:+.3f}, lower bound {f3(v['lower_bound_5pct'])}: {'LEVER' if v['lever'] else 'no demonstrated lever'}")
    L += ["", "Several arms are compared with one control: a single hit among them is weak evidence; no multiplicity correction is applied.", ""]
    if res.get("stronger_vs_pooled_controls"):
        L += [f"Secondary, not the registered decision: the same rule against the two same-day controls pooled (found fraction {res['pooled_control_found_fraction']:.3f}; pooling allowed by the rule fixed before any score was read):", ""]
        for ar, v in res["stronger_vs_pooled_controls"].items():
            L.append(f"- {ar}: difference {v['difference']:+.3f}, lower bound {f3(v['lower_bound_5pct'])}: {'LEVER' if v['lever'] else 'no demonstrated lever'}")
        L.append("")
if res["leave_one_document_out"]:
    docs_ = sorted(n_items)
    L += ["## Sensitivity: found-fraction difference against the arm's own control, leaving one plan out (descriptive)", "",
          "HX-1 has only 2 known defects, so one run there swings the pooled mean by up to 0.5 of its plan weight.", "",
          "| Arm | all four plans | " + " | ".join(f"without {d}" for d in docs_) + " |", "|---|---|" + "---|" * len(docs_)]
    for k, row in res["leave_one_document_out"].items():
        L.append(f"| {k} | {row['all four']:+.3f} | " + " | ".join(f"{row['without ' + d]:+.3f}" for d in docs_) + " |")
    L.append("")
if "pool_controls" in res:
    d = res["control_difference_90pct"]
    L += ["## Controls", "",
          f"The two ember Z0 controls ({', '.join(res['controls'])}) differ by a 90% interval of {f3(d['found_fraction'][0])} to {f3(d['found_fraction'][1])} on found fraction and "
          f"{f3(d['wrong_blockers'][0])} to {f3(d['wrong_blockers'][1])} on wrong blockers: **{'pooled analysis allowed' if res['pool_controls'] else 'not pooled; each lever is judged against its own control'}**.",
          "The severity test's control is interleaved with its arm in the same blocks. In the stronger-panel test, arms A and B were interleaved with each other (22:33 to 00:40 UTC on 2026-11-16); sole2 and wonder1 then ran alone (00:47 to 02:39); sonsol, wonsol and emsol2 overlapped each other from 03:44. So arm B is 3 to 5 hours older than the last three arms.", ""]
L += ["## Causes of the moved-aside runs with an error (from the other session's review)", "",
      "- emsol2 HO-2 r1: `claude: not found` (a short window with no Claude Code binary).",
      "- sonsol HO-2 r3 and wonsol HX-3 r5: `[claude-code:unrecognized_model]` for `muse-ember-1.0` and `muse-wonder-1.0` respectively (the program rejected the model name once, one reviewer each; both happened while three panels ran at once, so a link to load cannot be excluded).",
      "- wonsol: one run was cut short by the other session's own restart. sonsol HO-3 r3 was killed again in its rerun and stays as run; sonsol HX-1 r2 has a format-invalid reviewer report and was kept as run (not rerun).", ""]
L += ["## Judging", "", "One blind Opus judge per run; a second judge on a sample (21 runs in the stronger-panel test, agreeing on all 21 found-item sets; 6 in the severity test, agreeing on all 6; 9 in the Recipe Ledger comparison, agreeing on all 9). Judge noise is not the explanation for arm differences; the answer key holds 36 items, and wrong-blocker counts depend on it.", ""]
L += ["## Limits", "", "One panel family (ember or sonnet with luna), plans only, 36 known defects, ground truth by a model session, 5 runs per arm per plan, plans already used for an earlier test. See each test's own pre-registration for the full list.", ""]
open(out / "REPORT.md", "w").write("\n".join(L))
print(f"{res['n_runs_scored']} runs; report in {out}/REPORT.md")
