"""The analysis of Recipe Ledger runs (DESIGN 12.2 to 12.5, REQ-17, REQ-29, REQ-31, REQ-39 to REQ-45).

Every metric of DESIGN 12.5 is defined in this file and nowhere else (`METRIC_FUNCTIONS`; test_one_definition_of_found_fraction
searches the tree). It reads run folders, judge folders and a ground-truth path that the caller gives; the path has no
default and the build never runs the analysis on real data.

    analyze.py all --stage N --gt PATH [--runs DIR] [--scoring DIR] [--out DIR] [--sets FILE] [--seed S]
        metrics.json, d1.json, stages.jsonl and report.md in --out; prints the decision of MR 5.8 for RL against Z0 and K.
        A run with no valid first-judge score stops it (exit 1) unless --allow-unscored.
    analyze.py compliance --runs DIR... [--out FILE]
        REQ-17 over RL run folders: ledger_missing rate, recipe_missing, quote validity, format errors, none_found per class.
    analyze.py prereg [--write] [--owner-values FILE] [--out FILE]
        the pre-registered arms, run counts, consistency definition, gates D1 to D7 and the per-class act bands.
    analyze.py audit-judges [STAGE] [--scoring-dir DIR] [--out FILE] [--invalidate]
        judge_audit.py audit: every judge folder (exit 1 if any is bad).
    analyze.py sample-second-judge --seed S (RUN... | --runs-dir DIR --stage STAGE)
        judge_audit.py sample: round(0.15 n) runs, the same for a fixed seed.
    analyze.py ablate-report --gt PATH [--runs DIR] [--stage N]
        for each class, the change in the other classes' selection if its rows were absent (lens-cap displacement),
        computed from the ledgers of runs that exist; it is a report, not an ablation run (REQ-35).

Definitions chosen where MR 5.6 and 5.7 leave room (each is also printed in report.md):
    found fraction  covered items / items of the document, from the judge's `gt_covered_any`; pooled means are over runs.
    half share      runs that find at least half of the items.
    Jaccard         mean over pairs of runs of one arm and document; a pair of two empty sets is left out.
    consistent      an item reached in at least 60% of the runs of an arm; stable-hit rate = consistent / reached at all.
    nonprobe        findings lines of the reports that reach the merge, without `probe` and without `src: ledger`.
    bootstrap       resample documents with replacement, then runs within each chosen document; 5th percentile of the
                    difference = the lower bound of the 90% interval.
    D1              per document, same block only; every document's median ratio at most 1.35, 90th percentile ratio at
                    most 1.50, killed reviewer runs at most 10% of the candidate's reviewer runs.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_RL = os.path.dirname(_HERE)
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _HERE]
if _RL not in sys.path:
    sys.path.insert(0, _RL)

import argparse  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import random  # noqa: E402
import statistics  # noqa: E402
from pathlib import Path  # noqa: E402

from analysis import judge_audit as ja  # noqa: E402
from rl import lens as lens_mod  # noqa: E402
from scaffold import clock, fnd, telemetry  # noqa: E402

RL = Path(_RL)
CLASSES = tuple(f"C{n}" for n in range(1, 9))
GENERAL = ("C2", "C4", "C5", "C6", "C8")  # the five general classes of gate D5
Z = 1.96
EPS = 1e-9
BOOT_N = 2000
SEED = 20261115
CONSISTENT_AT = 0.6
LUNA = "gpt-6-luna"
READ_S = 4  # seconds a luna reviewer needs to read the recipes (DESIGN 12.4, MR 3.2(c))
LIMITS = {
    "d1_median": 1.35,
    "d1_p90": 1.50,
    "d1_kills": 0.10,
    "d2_diff": 0.12,
    "d2_lower": 0.04,
    "d3_extra": 3,
    "d4_wrong": 1.0,
    "d4_clean": 0.7,
    "d5_rate": 0.40,
    "d5_classes": 3,
    "d6_floor": 0.5,
    "d6_slack": 0.10,
    "d7_gain": 0.04,
    "k_close": 0.03,
    "g0_ledger_missing": 0.10,
}
# DESIGN 12.2: the act ranges of MR 3.2(d); the owner confirms them before the freeze (13.1 item 7)
ACT_BANDS = {
    "C1": [0.10, 0.30],
    "C2": [0.15, 0.35],
    "C3": [0.05, 0.20],
    "C4": [0.40, 0.70],
    "C5": [0.20, 0.45],
    "C6": [0.05, 0.30],
    "C7": [0.10, 0.30],
    "C8": [0.20, 0.45],
}
# REQ-45, word for word
CLAIM = (
    "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), "
    "and only for Redesign 1 at the high end of its range"
)
SHARES = (
    ("H share", "Z0 - Z0raw", "Z0", "Z0-raw"),
    ("prompting share", "K - Z0", "K", "Z0"),
    ("redesign share", "RL - Z0", "RL", "Z0"),
)
PAIRS = (
    ("RL", "Z0"),
    ("RLh", "Zh"),
)  # candidate, control: primary and haiku panels (D1 applies to both)
PANEL_LABEL = {
    ("Z0", "haiku"): "Zh",
    ("RL", "haiku"): "RLh",
    ("Z0", "sonnet"): "Zs",
    ("RL", "sonnet"): "RLs",
}
METRIC_FUNCTIONS = (
    "found_fraction",
    "half_found_share",
    "run_jaccard",
    "stable_hit_rate",
    "consistent_items",
    "wrong_blockers",
    "found_blocking",
    "nonprobe_findings",
    "elapsed_stats",
    "class_reach",
    "wilson",
    "percentile",
    "bootstrap_diff",
    "ledger_counts",
    "reask_yield",
)


# ---------------------------------------------------------------- the metrics (defined here only)


def percentile(xs, q):
    """Linear interpolation between order statistics (the 'inclusive' rule); q in [0, 1]."""
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def wilson(hits, n, z=Z):
    """The Wilson score interval (lo, hi) of hits successes in n trials; (None, None) for n = 0."""
    if n == 0:
        return None, None
    p = hits / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, mid - half), min(1.0, mid + half)


def found_fraction(found, n_items):
    """Share of the document's items that the judge credits to the run."""
    return len(found) / n_items if n_items else 0.0


def half_found_share(fractions):
    """Share of runs that find at least half of the items."""
    return sum(f >= 0.5 - EPS for f in fractions) / len(fractions)


def run_jaccard(a, b):
    """Jaccard index of two found sets; None when both are empty."""
    u = a | b
    return len(a & b) / len(u) if u else None


def consistent_items(reach):
    """Items reached in at least 60% of the runs: (count, items). `reach` maps an item to its reach rate."""
    items = sorted(i for i, rate in reach.items() if rate >= CONSISTENT_AT - EPS)
    return len(items), items


def stable_hit_rate(n_consistent, n_reached):
    """Consistent items over items reached in at least one run; None when nothing was reached."""
    return n_consistent / n_reached if n_reached else None


def wrong_blockers(scores):
    """Mean wrong blockers per run (the judge's count)."""
    return statistics.fmean(s["wrong_blockers"] for s in scores)


def found_blocking(blocking_sets, n_items_per_run):
    """Mean share of items covered by a blocking ledger row; found-any is `found_fraction`."""
    return statistics.fmean(
        found_fraction(b, n) for b, n in zip(blocking_sets, n_items_per_run)
    )


def nonprobe_findings(text):
    """Findings lines of a report without `probe` and without `src: ledger` (REQ-42); a missing report gives 0."""
    return sum(
        1
        for f in finding_lines(text)
        if not f.get("probe") and f.get("src") != "ledger"
    )


def elapsed_stats(xs):
    """Mean, median and 90th percentile of panel_elapsed_s (REQ-29)."""
    return {
        "mean": statistics.fmean(xs),
        "median": statistics.median(xs),
        "p90": percentile(xs, 0.9),
    }


def class_reach(trials):
    """{class: {hits, trials, rate, lo, hi}} from {class: [hits, trials]} with Wilson intervals."""
    out = {}
    for cls, (hits, n) in sorted(trials.items()):
        lo, hi = wilson(hits, n)
        out[cls] = {"hits": hits, "trials": n, "rate": hits / n, "lo": lo, "hi": hi}
    return out


def ledger_counts(ledgers):
    """The ledger metrics of DESIGN 12.5 over the ledger dicts of one arm (`check/<rid>.ledger.json`; an arm with no
    check has none and gets zeros). Keys:
      over_budget      {recipe, lens}: rows flagged over budget, by reason.
      recipe_missing   {class: n}: reviewer-runs whose lens recipe for the class has no row.
      unknown_item     n: rows whose id is outside the grammar or the reviewer's lens.
      none_found_share {class: {none_found, ran, share}}: `ran` is the reviewer-runs that wrote at least one accepted
                       (not unknown_item) row of the class; `none_found` is those that wrote a NONE FOUND row for it, so
                       the share is at most 1. A missing ledger has no rows and is in neither count.
      rows_per_lens    {rid: mean rows}: a lens is named by its reviewer id; ledgers that are missing are left out."""
    over = {"recipe": 0, "lens": 0}
    missing, ran, none_found, rows_by = {}, {}, {}, {}
    unknown = 0
    for x in ledgers:
        unknown += len(x["unknown_item"])
        if not x["ledger_missing"]:
            rows_by.setdefault(x["rid"], []).append(len(x["rows"]))
        for c in x["recipe_missing"]:
            missing[c] = missing.get(c, 0) + 1
        seen, found = set(), set()
        for r in x["rows"]:
            if r["over_budget"]:
                over[r["over_budget"]] += 1
            c = telemetry.class_of(r["item"])
            if c and not r["unknown_item"]:
                seen.add(c)
                if r["none_found"]:
                    found.add(c)
        for c in seen:
            ran[c] = ran.get(c, 0) + 1
        for c in found:
            none_found[c] = none_found.get(c, 0) + 1
    return {
        "over_budget": over,
        "recipe_missing": dict(sorted(missing.items())),
        "unknown_item": unknown,
        "none_found_share": {
            c: {
                "none_found": none_found.get(c, 0),
                "ran": n,
                "share": none_found.get(c, 0) / n,
            }
            for c, n in sorted(ran.items())
        },
        "rows_per_lens": {k: statistics.fmean(v) for k, v in sorted(rows_by.items())},
    }


def reask_yield(fractions, reasked):
    """Found-fraction yield of the runs with a re-asked reviewer and of the runs without one (DESIGN 8 row 23).
    `fractions` and `reasked` are parallel lists, one entry per run. The judge credits a run, not a reviewer, so this
    compares two groups of runs; a group with no run has mean None."""
    out = {}
    for name, flag in (("with", True), ("without", False)):
        xs = [f for f, a in zip(fractions, reasked, strict=True) if a == flag]
        out[name] = {
            "runs": len(xs),
            "found_fraction_mean": statistics.fmean(xs) if xs else None,
        }
    return out


def bootstrap_diff(cand, ctrl, seed, n=BOOT_N):
    """Sorted differences of pooled means; `cand` and `ctrl` map a document to its per-run values.

    Each draw picks the documents with replacement first, then the runs of each chosen document with replacement.
    """
    rng = random.Random(seed)
    docs = sorted(set(cand) & set(ctrl))
    out = []
    for _ in range(n):
        a, b = [], []
        for d in [rng.choice(docs) for _ in docs]:
            a += [rng.choice(cand[d]) for _ in cand[d]]
            b += [rng.choice(ctrl[d]) for _ in ctrl[d]]
        out.append(statistics.fmean(a) - statistics.fmean(b))
    return sorted(out)


# ---------------------------------------------------------------- reading run folders


def read_json(path):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def arm_label(meta):
    """Z0-raw, Z0, K, RL on the primary panel; Zh, RLh, Zs, RLs on the others (MR 5.3)."""
    arm, panel = meta["arm"], meta.get("panel", "primary")
    if panel == "primary":
        return arm
    return PANEL_LABEL.get((arm, panel), f"{arm}-{panel}")


def load_runs(runs_dir, prefix=""):
    out = []
    for d in sorted(Path(runs_dir).iterdir()):
        meta = read_json(d / "run.json") if d.is_dir() else None
        if meta and d.name.startswith(prefix):
            out.append(
                {
                    "id": d.name,
                    "dir": d,
                    "meta": meta,
                    "timing": read_json(d / "timing.json") or {},
                    "label": arm_label(meta),
                    "doc": meta["doc"],
                    "block": meta.get("block"),
                }
            )
    return out


def load_scores(scoring_dir):
    """({run: score}, {run: flags}) of the first judge of each run; a folder the audit flags gives no score."""
    sd = Path(scoring_dir)
    scores, bad = {}, {}
    for line in (sd / "labels.tsv").read_text(encoding="utf-8").splitlines():
        label, run, _doc, role = line.split("\t")
        if role == "first":
            flags = ja.audit_one(sd / label)
            if flags:
                bad[run] = flags
            else:
                scores[run] = read_json(sd / label / "score.json")
    return scores, bad


def load_gt(path):
    """{document: [items]} from a ground-truth path the caller names: a file with `docs`, or `doc_id` and `items`,
    or a folder of <document>/ground-truth.json. There is no default (K3)."""
    p = Path(path)
    if p.is_dir():
        files = {d.name: d / "ground-truth.json" for d in sorted(p.iterdir())}
        return {k: read_json(f)["items"] for k, f in files.items() if f.is_file()}
    data = read_json(p)
    if "docs" in data:
        return {k: v["items"] for k, v in data["docs"].items()}
    return {data["doc_id"]: data["items"]}


def reviewers(run):
    """{rid: record} of the reviewers whose report reaches the merge (not killed, not invalid, not in error)."""
    return {
        rid: v
        for rid, v in run["meta"].get("reviewers", {}).items()
        if v.get("status", "ok") == "ok" and not v.get("killed")
    }


def run_ledgers(run):
    """The ledger dicts of a run's reviewers (RL runs whose check ran; none for any other run)."""
    leds = (
        read_json(run["dir"] / "check" / f"{rid}.ledger.json")
        for rid in run["meta"].get("reviewers", {})
    )
    return [x for x in leds if x is not None]


def report_text(run, rid):
    """The report as it reaches the merge: normalised, else the checked report, else the raw final message."""
    d = run["dir"]
    for rel in (f"normalised/{rid}.md", f"check/{rid}.checked.md", f"reviews/{rid}.md"):
        if (d / rel).is_file():
            return (d / rel).read_text(encoding="utf-8")
    return ""


def finding_lines(text):
    """The JSON objects of the findings block (the last findings-v1 fence), `prior` lines and bad lines left out."""
    out = []
    for raw in fnd.lenient_lines(text):
        try:
            obj = json.loads(raw)
        except ValueError:
            continue
        if isinstance(obj, dict) and "prior" not in obj:
            out.append(obj)
    return out


def run_nonprobe(run):
    return sum(nonprobe_findings(report_text(run, rid)) for rid in reviewers(run))


def run_tokens(run):
    return sum(
        (read_json(run["dir"] / "reviews" / f"{rid}.cost.json") or {}).get(
            "total_output_tokens_all", 0
        )
        for rid in run["meta"].get("reviewers", {})
    )


def candidate_text(run, cand_root=None):
    """The reviewed document of a run: the path the merge ledger records, else CAND_ROOT/<doc>/candidate.md."""
    led = read_json(run["dir"] / "merged" / "ledger.json") or {}
    for p in (
        led.get("doc"),
        cand_root and Path(cand_root) / run["doc"] / "candidate.md",
    ):
        if p and Path(p).is_file():
            return Path(p).read_text(encoding="utf-8")
    return None


# ---------------------------------------------------------------- per arm and per document


def arm_metrics(runs, gt, scores):
    """Every metric of one set of runs (one arm, all documents or one document)."""
    by_doc = {}
    for r in runs:
        by_doc.setdefault(r["doc"], []).append(r)
    fr, fb, wb, npf, el, tk, pairs = [], [], [], [], [], [], []
    reach, trials = {}, {}
    cnt = dict.fromkeys(
        (
            "kills",
            "reviewer_runs",
            "retries",
            "reasks",
            "fallbacks",
            "invalid",
            "check_skipped",
        ),
        0,
    )
    ledgers, reasked, lost, asked, accepted = [], [], {}, 0, 0
    for doc, rs in sorted(by_doc.items()):
        items = gt[doc]
        ids = {i["id"] for i in items}
        sets = []
        for r in rs:
            s = scores[r["id"]]
            found = set(s["gt_covered_any"]) & ids
            sets.append(found)
            fr.append(found_fraction(found, len(items)))
            ledgers += run_ledgers(r)
            reasked.append(bool(r["meta"].get("reask")))
            chk = read_json(r["dir"] / "check" / "check.json") or {}
            for rec in (chk.get("reask") or {}).values():
                was = rec.get("asked", rec.get("allowed", False))
                asked += bool(was)
                accepted += bool(was and rec.get("accepted"))
            for classes in (chk.get("classes_lost") or {}).values():
                for c in classes:
                    lost[c] = lost.get(c, 0) + 1
            fb.append(found_fraction(set(s["gt_covered_blocking"]) & ids, len(items)))
            wb.append(s)
            npf.append(run_nonprobe(r))
            el.append(r["timing"]["panel_elapsed_s"])
            tk.append(run_tokens(r))
            rv = r["meta"].get("reviewers", {})
            cnt["kills"] += sum(bool(v.get("killed")) for v in rv.values())
            cnt["invalid"] += sum(v.get("status") == "invalid" for v in rv.values())
            cnt["reviewer_runs"] += len(rv)
            cnt["retries"] += r["meta"].get("retries", 0)
            cnt["reasks"] += len(r["meta"].get("reask") or [])
            cnt["fallbacks"] += bool(r["meta"].get("fallback"))
            cnt["check_skipped"] += bool(r["meta"].get("check_skipped"))
        pairs += [
            run_jaccard(sets[i], sets[j])
            for i in range(len(sets))
            for j in range(i + 1, len(sets))
        ]
        for it in items:
            k = sum(it["id"] in s for s in sets)
            reach[f"{doc}/{it['id']}"] = k / len(rs)
            t = trials.setdefault(it["class"], [0, 0])
            t[0] += k
            t[1] += len(rs)
    pairs = [p for p in pairs if p is not None]
    n_cons, cons = consistent_items(reach)
    n_reached = sum(v > 0 for v in reach.values())
    blocking = [
        set(scores[r["id"]]["gt_covered_blocking"]) & {i["id"] for i in gt[r["doc"]]}
        for r in runs
    ]
    return {
        "runs": len(runs),
        "found_fraction_mean": statistics.fmean(fr),
        "half_found_share": half_found_share(fr),
        "jaccard_mean": statistics.fmean(pairs) if pairs else None,
        "jaccard_pairs": len(pairs),
        "consistent_items": n_cons,
        "consistent_item_ids": cons,
        "consistent_share": n_cons / len(reach),
        "stable_hit_rate": stable_hit_rate(n_cons, n_reached),
        "wrong_blockers_per_run": wrong_blockers(wb),
        "found_any_mean": statistics.fmean(fr),
        "found_blocking_mean": found_blocking(
            blocking, [len(gt[r["doc"]]) for r in runs]
        ),
        "nonprobe_findings_per_run": statistics.fmean(npf),
        "elapsed_mean": elapsed_stats(el)["mean"],
        "elapsed_median": elapsed_stats(el)["median"],
        "elapsed_p90": elapsed_stats(el)["p90"],
        "tokens_per_run": statistics.fmean(tk),
        **cnt,
        **ledger_counts(ledgers),
        "classes_lost": dict(sorted(lost.items())),
        "reask_asked": asked,
        "reask_accepted": accepted,
        "reask_yield": reask_yield(fr, reasked),
        "item_reach": reach,
        "class_reach": class_reach(trials),
    }


def split_arms(runs):
    out = {}
    for r in runs:
        out.setdefault(r["label"], []).append(r)
    return out


# ---------------------------------------------------------------- gates D1 to D7


def d1(cand_runs, ctrl_runs):
    """D1 (REQ-29): per-document medians against the same-block control runs. A control run from a block the candidate
    did not run is ignored; a candidate run with no control run in its block raises ValueError."""
    per_doc = {}
    for doc in sorted({r["doc"] for r in cand_runs}):
        c = [r for r in cand_runs if r["doc"] == doc]
        z = [r for r in ctrl_runs if r["doc"] == doc]
        orphans = sorted(
            r["id"] for r in c if r["block"] not in {x["block"] for x in z}
        )
        if orphans:
            raise ValueError(f"no same-block control run for {doc}: {orphans}")
        used = [r for r in z if r["block"] in {x["block"] for x in c}]
        ec = elapsed_stats([r["timing"]["panel_elapsed_s"] for r in c])
        ez = elapsed_stats([r["timing"]["panel_elapsed_s"] for r in used])
        per_doc[doc] = {
            "candidate": ec,
            "control": ez,
            "ratio_median": ec["median"] / ez["median"],
            "ratio_mean": ec["mean"] / ez["mean"],
            "ratio_p90": ec["p90"] / ez["p90"],
            "ignored_control_runs": sorted(
                r["id"] for r in z if r["id"] not in {u["id"] for u in used}
            ),
        }
    reviewer_runs = sum(len(r["meta"].get("reviewers", {})) for r in cand_runs)
    kills = sum(
        bool(v.get("killed"))
        for r in cand_runs
        for v in r["meta"].get("reviewers", {}).values()
    )
    rate = kills / reviewer_runs
    ok = (
        all(
            d["ratio_median"] <= LIMITS["d1_median"] + EPS
            and d["ratio_p90"] <= LIMITS["d1_p90"] + EPS
            for d in per_doc.values()
        )
        and rate <= LIMITS["d1_kills"] + EPS
    )
    return {"per_doc": per_doc, "kills": kills, "kill_rate": rate, "pass": ok}


def doc_fractions(runs, gt, scores):
    out = {}
    for r in runs:
        ids = {i["id"] for i in gt[r["doc"]]}
        found = set(scores[r["id"]]["gt_covered_any"]) & ids
        out.setdefault(r["doc"], []).append(found_fraction(found, len(ids)))
    return out


def pool(by_doc):
    return statistics.fmean([x for v in by_doc.values() for x in v])


def effect(cand_runs, ctrl_runs, gt, scores, seed, n):
    """Difference of pooled mean found fractions and the lower bound of its 90% bootstrap interval."""
    a, b = doc_fractions(cand_runs, gt, scores), doc_fractions(ctrl_runs, gt, scores)
    diffs = bootstrap_diff(a, b, seed, n)
    return pool(a) - pool(b), percentile(diffs, 0.05)


def d5(cand_runs, ctrl_runs, gt, scores, sets, seed, n):
    """D5 from the planted set, the documentation set and the specification set named in `sets` (doc -> set)."""
    planted = [r for r in cand_runs if sets.get(r["doc"]) == "planted"]
    if not planted:
        return {"pass": None, "status": "no planted documents in --sets"}
    trials = {}
    for r in planted:
        found = set(scores[r["id"]]["gt_covered_any"])
        for it in gt[r["doc"]]:
            t = trials.setdefault(it["class"], [0, 0])
            t[0] += it["id"] in found
            t[1] += 1
    rates = {c: t[0] / t[1] for c, t in trials.items()}
    holding = [c for c in GENERAL if rates.get(c, 0) >= LIMITS["d5_rate"] - EPS]
    out = {
        "pass": len(holding) >= LIMITS["d5_classes"],
        "planted_rates": rates,
        "general_classes_holding": holding,
        "claim_scope": "plans and other targets",
    }
    for kind in ("docs", "spec"):
        c = [r for r in cand_runs if sets.get(r["doc"]) == kind]
        z = [r for r in ctrl_runs if sets.get(r["doc"]) == kind]
        if c and z:
            diff, low = effect(c, z, gt, scores, seed, n)
            ok = diff >= LIMITS["d2_diff"] - EPS and low > 0
            out[kind] = {"diff": diff, "lower": low, "d2_holds": ok}
            if not ok:
                out["claim_scope"] = "plans only"
    return out


def gates_for(cand, ctrl, kk, arms, gt, scores, sets, seed=SEED, n=BOOT_N):
    """Gates D1 to D7 of arm `cand` against `ctrl` (and `kk` for D7). Pooled gates use the decision documents:
    every document that `sets` does not call planted, docs, spec or clean."""
    decision = {d for d in gt if sets.get(d, "decision") == "decision"}

    def pick(label, docs):
        return [r for r in arms.get(label, []) if r["doc"] in docs]

    c, z = pick(cand, decision), pick(ctrl, decision)
    g = {"D1": dict(d1(arms[cand], arms[ctrl]))}
    diff, low = effect(c, z, gt, scores, seed, n)
    g["D2"] = {
        "diff": diff,
        "lower": low,
        "pass": diff >= LIMITS["d2_diff"] - EPS and low > LIMITS["d2_lower"],
    }
    mc, mz = arm_metrics(c, gt, scores), arm_metrics(z, gt, scores)
    g["D3"] = {
        "candidate": mc["consistent_items"],
        "control": mz["consistent_items"],
        "pass": mc["consistent_items"] >= mz["consistent_items"] + LIMITS["d3_extra"],
    }
    wrong = mc["wrong_blockers_per_run"] - mz["wrong_blockers_per_run"]
    clean = {d for d, s in sets.items() if s == "clean"}
    cc, cz = pick(cand, clean), pick(ctrl, clean)
    clean_diff = None
    if cc and cz:
        clean_diff = statistics.fmean(
            scores[r["id"]]["ledger_rows_blocking"] for r in cc
        ) - statistics.fmean(scores[r["id"]]["ledger_rows_blocking"] for r in cz)
    g["D4"] = {
        "wrong_blockers_diff": wrong,
        "clean_blocking_diff": clean_diff,
        "pass": wrong <= LIMITS["d4_wrong"] + EPS
        and (clean_diff is None or clean_diff <= LIMITS["d4_clean"] + EPS),
    }
    g["D5"] = d5(arms[cand], arms[ctrl], gt, scores, sets, seed, n)
    worse = {
        i: {"control": rate, "candidate": mc["item_reach"][i]}
        for i, rate in mz["item_reach"].items()
        if rate >= LIMITS["d6_floor"] - EPS
        and mc["item_reach"][i] < rate - LIMITS["d6_slack"] - EPS
    }
    g["D6"] = {"blocking": True, "regressed_items": worse, "pass": not worse}
    k = pick(kk, decision) if kk else []
    if k:
        mk = arm_metrics(k, gt, scores)
        gain = mc["found_fraction_mean"] - mk["found_fraction_mean"]
        g["D7"] = {
            "gain_over_k": gain,
            "k_within_0_03": abs(gain) <= LIMITS["k_close"] + EPS,
            "pass": gain >= LIMITS["d7_gain"] - EPS,
        }
    else:
        g["D7"] = {"pass": None, "status": "no K runs"}
    return g


def decide(gates, stage=1):
    """MR 5.8 for one candidate: adopt only if every required gate passes. D6 blocks; a gate not evaluated is not a pass."""
    required = ["D1", "D2", "D3", "D4", "D6", "D7"] + (["D5"] if stage >= 2 else [])
    failed = [d for d in required if gates.get(d, {}).get("pass") is not True]
    return {
        "decision": "do not adopt" if failed else "adopt",
        "failed": failed,
        "blocking_failed": [d for d in failed if gates.get(d, {}).get("blocking")],
        "required": required,
    }


# ---------------------------------------------------------------- stages (REQ-41)


def covers(quote, item_quote, cand_text):
    """The selection rule (DESIGN 12.2, the rule of FND.same_defect): one flattened text contains the other, or the two
    line spans in the candidate lie within 3 lines."""
    q, g = fnd.flat(quote or ""), fnd.flat(item_quote or "")
    if not q or not g:
        return False
    if q in g or g in q:
        return True
    if cand_text:
        return any(
            s1[0] <= s2[1] + 3 and s2[0] <= s1[1] + 3
            for s1 in fnd.locate(cand_text, quote)
            for s2 in fnd.locate(cand_text, item_quote)
        )
    return False


def covering_rows(rows, item_quote, cand_text):
    """The accepted, within-budget rows of a ledger whose quote_plan or quote_other covers the item."""
    return [
        r
        for r in rows
        if not r["unknown_item"]
        and not r["over_budget"]
        and (
            covers(r["quote_plan"], item_quote, cand_text)
            or covers(r["quote_other"], item_quote, cand_text)
        )
    ]


def stage_rows(run, items, score, cand_text=None):
    """One row per (ground-truth item, reviewer): extraction null, selection, act, merge survival, judge credit,
    class and reviewer id. Selection and act are null for an arm with no ledger, for a run that fell back to Z0 and
    for a run whose check was skipped; merge survival then follows the anchors of the merge ledger."""
    meta, d = run["meta"], run["dir"]
    merged = read_json(d / "merged" / "ledger.json") or {"rows": []}
    members = {
        (m["reviewer_id"], m["fid"]) for r in merged["rows"] for m in r["members"]
    }
    ledgered = (
        meta["arm"] == "RL"
        and meta.get("check_ran")
        and not meta.get("check_skipped")
        and not meta.get("fallback")
    )
    out = []
    for rid in meta.get("reviewers", {}):
        led = read_json(d / "check" / f"{rid}.ledger.json") if ledgered else None
        for it in items:
            sel = act = None
            merge = False
            if ledgered:
                sel = act = False
                if led and not led["ledger_missing"]:
                    cov = covering_rows(led["rows"], it["plan_quote"], cand_text)
                    sel = bool(cov)
                    act = any(r["verdict"] == "PROBLEM" and r["supported"] for r in cov)
                    for r in cov:
                        fids = [
                            f for f, item in led["links"].items() if item == r["item"]
                        ]
                        fids += (
                            [f"P{r['item']}"]
                            if f"P{r['item']}" in led["promoted"]
                            else []
                        )
                        merge = merge or any((rid, f) in members for f in fids)
            else:
                for row in merged["rows"]:
                    mine = any(m["reviewer_id"] == rid for m in row["members"])
                    merge = merge or (
                        mine and covers(row["anchor"], it["plan_quote"], cand_text)
                    )
            out.append(
                {
                    "run": run["id"],
                    "arm": run["label"],
                    "doc": run["doc"],
                    "item": it["id"],
                    "class": it["class"],
                    "blocking_in_implement": it.get("blocking_in_implement"),
                    "reviewer_id": rid,
                    "extraction": None,
                    "selection": sel,
                    "act": act,
                    "merge_survival": merge,
                    "judge_credit": {
                        "any": it["id"] in score["gt_covered_any"],
                        "blocking": it["id"] in score["gt_covered_blocking"],
                    },
                }
            )
    return out


def stage_rates(rows):
    """{arm: {class: {items, judge_credit_any, judge_credit_blocking, by_reviewer: {rid: {rows, ledger_rows,
    selection, act, merge_survival}}}}}: reach per class per reviewer id. `items` counts (run, item) pairs; selection
    and act are counted over the `ledger_rows` only (rows of a run whose check ran)."""
    out = {}
    seen = set()
    for r in rows:
        c = out.setdefault(r["arm"], {}).setdefault(
            r["class"],
            {
                "items": 0,
                "judge_credit_any": 0,
                "judge_credit_blocking": 0,
                "by_reviewer": {},
            },
        )
        if (r["run"], r["item"]) not in seen:
            seen.add((r["run"], r["item"]))
            c["items"] += 1
            c["judge_credit_any"] += r["judge_credit"]["any"]
            c["judge_credit_blocking"] += r["judge_credit"]["blocking"]
        b = c["by_reviewer"].setdefault(
            r["reviewer_id"],
            {
                "rows": 0,
                "ledger_rows": 0,
                "selection": 0,
                "act": 0,
                "merge_survival": 0,
            },
        )
        b["rows"] += 1
        b["merge_survival"] += r["merge_survival"]
        if r["selection"] is not None:
            b["ledger_rows"] += 1
            b["selection"] += r["selection"]
            b["act"] += r["act"]
    return out


def rebudget(rows, cap, drop):
    """The rows of a ledger without the class `drop`, over_budget recomputed for the lens cap in the order written
    (DESIGN 7.2): a row over its recipe budget stays out; a row beyond `cap` within-budget rows is over the lens."""
    out, within = [], 0
    for r in rows:
        if telemetry.class_of(r["item"]) == drop:
            continue
        r = dict(r)
        if r["over_budget"] != "recipe" and not r["unknown_item"]:
            within += 1
            r["over_budget"] = "lens" if within > cap else None
        out.append(r)
    return out


def ablate(runs, gt, cand_root=None):
    """{class: {rows, gained, points}}: for each class X, how many stage rows of the other classes would be selected
    that are not now, if X's rows were absent from every ledger (a row pushed out by the lens cap comes back)."""
    out = {x: {"rows": 0, "gained": 0} for x in CLASSES}
    for run in runs:
        meta = run["meta"]
        if not (
            meta["arm"] == "RL"
            and meta.get("check_ran")
            and not meta.get("check_skipped")
            and not meta.get("fallback")
        ):
            continue
        text = candidate_text(run, cand_root)
        for rid in meta.get("reviewers", {}):
            led = read_json(run["dir"] / "check" / f"{rid}.ledger.json")
            for it in gt[run["doc"]]:
                now = bool(
                    led
                    and not led["ledger_missing"]
                    and covering_rows(led["rows"], it["plan_quote"], text)
                )
                for x in CLASSES:
                    if it["class"] == x:
                        continue
                    out[x]["rows"] += 1
                    if led and not led["ledger_missing"] and not now:
                        rows = rebudget(led["rows"], led["row_cap"], x)
                        out[x]["gained"] += bool(
                            covering_rows(rows, it["plan_quote"], text)
                        )
    for v in out.values():
        v["points"] = 100 * v["gained"] / v["rows"] if v["rows"] else None
    return out


# ---------------------------------------------------------------- time: planned and measured (REQ-31)


def time_table(runs, values=None):
    """Planned against measured: b, the break-even row cost, the luna cost per row and the row cap that follows."""
    v = values or lens_mod.values()
    b_planned = min(v["b"]["primary"].values())
    c_planned = v["c"][LUNA]
    z0 = [r for r in runs if r["label"] == "Z0"]
    slowest = {}
    for r in z0:
        slowest.setdefault(r["doc"], []).append(r["timing"]["slowest_reviewer_s"])
    b_doc = {d: statistics.median(x) for d, x in sorted(slowest.items())}
    b_meas = min(b_doc.values()) if b_doc else None
    walls_z = [
        m["wall_s"] for r in z0 for m in reviewers(r).values() if m.get("model") == LUNA
    ]
    walls_r, rows = [], []
    for r in runs:
        if (
            r["label"] == "RL"
            and r["meta"].get("check_ran")
            and not r["meta"].get("check_skipped")
        ):
            for rid, m in reviewers(r).items():
                led = read_json(r["dir"] / "check" / f"{rid}.ledger.json")
                if m.get("model") == LUNA and led and not led["ledger_missing"]:
                    walls_r.append(m["wall_s"])
                    rows.append(len(led["rows"]))
    c_meas = None
    if walls_z and walls_r:
        c_meas = (
            statistics.median(walls_r) - statistics.median(walls_z) - READ_S
        ) / statistics.fmean(rows)
    table_cap = v["row_cap"]["hard_cap"]
    return {
        "b_per_doc_measured": b_doc,
        "b": {"planned": b_planned, "measured": b_meas},
        "breakeven_row_cost_14": {
            "planned": clock.breakeven_row_cost(b_planned, table_cap),
            "measured": clock.breakeven_row_cost(b_meas, table_cap) if b_meas else None,
        },
        "luna_cost_per_row": {"planned": c_planned, "measured": c_meas},
        "luna_row_cap": {
            "planned": lens_mod.lens_row_cap(b_planned, c_planned, table_cap),
            "measured": lens_mod.lens_row_cap(b_meas, c_meas, table_cap)
            if b_meas and c_meas
            else None,
        },
    }


# ---------------------------------------------------------------- compliance (REQ-17)


def _forgiven_kinds(ledgers):
    """{kind: count} of everything the ledger reader forgave (owner-approved small allowances), id prefixes included."""
    out = {}
    for x in ledgers:
        for k in x.get("forgiven") or []:
            out[k] = out.get(k, 0) + 1
        n = sum(1 for r in x.get("rows") or [] if r.get("item_raw"))
        if n:
            out["item_affix"] = out.get("item_affix", 0) + n
    return dict(sorted(out.items()))


def _forgiven_in(x):
    return bool(x.get("forgiven")) or any(r.get("item_raw") for r in x.get("rows") or [])


def compliance(run_dirs):
    """The REQ-17 numbers over RL run folders that have a check: ledger_missing before any re-ask, recipe_missing,
    quote validity, format errors and none_found per class."""
    ledgers, dropped, runs = [], 0, 0
    asked = accepted = 0
    for d in run_dirs:
        chk = read_json(Path(d) / "check" / "check.json")
        if chk is None:
            continue
        runs += 1
        for rid, rec in (chk.get("reask") or {}).items():
            was = rec.get("asked", rec.get("allowed", False))
            asked += bool(was)
            accepted += bool(was and rec.get("accepted"))
        meta = read_json(Path(d) / "run.json") or {}
        for rid in meta.get("reviewers", {}):
            led = read_json(Path(d) / "check" / f"{rid}.ledger.json")
            if led is None:
                dropped += 1
            else:
                ledgers.append(led)
    n = len(ledgers)
    final_missing = sum(bool(x["ledger_missing"]) for x in ledgers)
    initial = (
        final_missing + accepted
    )  # an accepted re-ask answered a message whose ledger was missing
    quote_rows = [r for x in ledgers for r in x["rows"] if r["quote_plan"]]
    rows_by = {}
    recipe_missing, none_found = {}, {}
    over = {"recipe": 0, "lens": 0}
    strict_missing = initial + sum(
        1 for x in ledgers if not x["ledger_missing"] and _forgiven_in(x)
    )
    for x in ledgers:
        if not x["ledger_missing"]:
            rows_by.setdefault(x["rid"], []).append(len(x["rows"]))
        for c in x["recipe_missing"]:
            recipe_missing[c] = recipe_missing.get(c, 0) + 1
        for r in x["rows"]:
            if r["none_found"]:
                c = telemetry.class_of(r["item"])
                none_found[c] = none_found.get(c, 0) + 1
            if r["over_budget"]:
                over[r["over_budget"]] += 1
    return {
        "runs_checked": runs,
        "reviewer_runs": n,
        "reviewers_without_ledger_file": dropped,
        "ledger_missing": {
            "count": initial,
            "rate": initial / n if n else None,
            "limit": LIMITS["g0_ledger_missing"],
            "pass": bool(n) and initial / n <= LIMITS["g0_ledger_missing"] + EPS,
        },
        # owner order 2026-11-15: the small allowances are reported both ways. `strict` counts a reviewer report as missing
        # when its ledger is missing OR anything was forgiven in it (id prefix or suffix, a heading between the blocks,
        # heading or fence label slips, trailing commas), so the two readings can be compared per arm.
        "strict": {
            "forgiven_reports": sum(_forgiven_in(x) for x in ledgers),
            "forgiven_by_kind": _forgiven_kinds(ledgers),
            "ledger_missing_strict": {
                "count": strict_missing,
                "rate": strict_missing / n if n else None,
                "pass": bool(n)
                and strict_missing / n <= LIMITS["g0_ledger_missing"] + EPS,
            },
        },
        "recipe_missing": dict(sorted(recipe_missing.items())),
        "quote_plan": {
            "rows_with_quote": len(quote_rows),
            "ok": sum(bool(r["quote_plan_ok"]) for r in quote_rows),
            "share": sum(bool(r["quote_plan_ok"]) for r in quote_rows) / len(quote_rows)
            if quote_rows
            else None,
        },
        "format_errors": sum(x["format_errors"] for x in ledgers),
        "none_found": dict(sorted(none_found.items())),
        "over_budget": over,
        "reask": {"asked": asked, "accepted": accepted},
        "rows_per_reviewer": {
            k: statistics.fmean(v) for k, v in sorted(rows_by.items())
        },
    }


def run_dirs_of(paths):
    """Run folders named by --runs: a run folder, or a folder of run folders."""
    out = []
    for p in map(Path, paths):
        if (p / "run.json").is_file():
            out.append(p)
        else:
            out += [d for d in sorted(p.iterdir()) if (d / "run.json").is_file()]
    return out


# ---------------------------------------------------------------- pre-registration (REQ-41, REQ-44)


def prereg(owner=None):
    """The record committed before the first hold-out run. `owner` may replace the act bands; a band must satisfy
    0 <= lo < hi <= 1 for each of C1 to C8 (ValueError otherwise)."""
    bands = {c: list(b) for c, b in ACT_BANDS.items()}
    for c, b in ((owner or {}).get("act_bands") or {}).items():
        bands[c] = list(b)
    for c in CLASSES:
        lo, hi = bands[c]
        if not 0 <= lo < hi <= 1:
            raise ValueError(
                f"act band of {c} must satisfy 0 <= lo < hi <= 1, got {bands[c]}"
            )
    return {
        "schema": "rl-prereg/1",
        "arms": {
            "stage1": ["Z0", "K", "RL"],
            "stage1_harness": ["Z0-raw"],
            "stage2": ["Z0", "RL"],
            "panels": ["Zh", "RLh", "Zs", "RLs"],
        },
        "run_counts": {
            "stage1_panel_runs": 75,
            "stage2_panel_runs": 154,
            "per_document": 5,
            "note": "DESIGN 12.1: 3 arms x 4 documents x 5 plus Z0-raw 3 x 5; Stage 2 without SS",
        },
        "consistency": {
            "definition": "an item reached in at least 60% of the runs of an arm (3 of 5)",
            "reach_at": CONSISTENT_AT,
            "primary_metric": "share of hold-out items that are consistent, per arm",
        },
        "gates": {
            "G0": f"ledger_missing at most {LIMITS['g0_ledger_missing']:.0%} in the compliance spike, luna cost per row at or below its break-even",
            "D1": f"per-document median elapsed at most {LIMITS['d1_median']} x Z0 in the same block, 90th percentile at most {LIMITS['d1_p90']} x, kills at most {LIMITS['d1_kills']:.0%}",
            "D2": f"mean found fraction at least Z0 + {LIMITS['d2_diff']}, 90% bootstrap lower bound above Z0 + {LIMITS['d2_lower']}",
            "D3": f"consistent items at least Z0's count + {LIMITS['d3_extra']}",
            "D4": f"wrong blockers per run at most Z0 + {LIMITS['d4_wrong']}, blocking findings on clean twins at most Z0 + {LIMITS['d4_clean']}",
            "D5": f"planted detection at least {LIMITS['d5_rate']} on at least {LIMITS['d5_classes']} of C2, C4, C5, C6, C8; documentation and HO-5: D2 holds with lower bound above 0, else the claim is withdrawn to plans only",
            "D6": f"items Z0 reaches at {LIMITS['d6_floor']} or more stay within {LIMITS['d6_slack']} of Z0 (blocking gate)",
            "D7": f"gain over K at least {LIMITS['d7_gain']} on D2's metric, otherwise K wins",
        },
        "act_bands": bands,
    }


# ---------------------------------------------------------------- report


def fmt(x, nd=3):
    return "n/a" if x is None else f"{x:.{nd}f}"


def share_values(arms, gt, scores):
    """The three shares of REQ-40: each is a difference of pooled mean found fractions on the documents both arms ran."""
    out = {}
    for name, label, hi, lo in SHARES:
        docs = {r["doc"] for r in arms.get(hi, [])} & {
            r["doc"] for r in arms.get(lo, [])
        }
        if not docs:
            out[name] = {"label": label, "value": None}
            continue

        def pooled(arm):
            runs = [r for r in arms[arm] if r["doc"] in docs]
            return pool(doc_fractions(runs, gt, scores))

        out[name] = {
            "label": label,
            "value": pooled(hi) - pooled(lo),
            "documents": sorted(docs),
        }
    return out


def build_report(m):
    """report.md from the metrics dictionary. No line holds two share names; the word that sums is never used."""
    out = ["# Recipe Ledger analysis", ""]
    out.append(
        f"Stage {m['stage']}; {m['runs']} runs; seed {m['seed']}; bootstrap draws {m['bootstrap_draws']}."
    )
    out += ["", "## Decision (MR 5.8, RL against Z0 and K)", ""]
    for cand, dec in m["decisions"].items():
        extra = f" (failed: {', '.join(dec['failed'])})" if dec["failed"] else ""
        block = (
            f" Blocking gate failed: {', '.join(dec['blocking_failed'])}."
            if dec["blocking_failed"]
            else ""
        )
        out.append(f"{cand}: {dec['decision']}{extra}.{block}")
    out += ["", "## Shares of the gain, one line each", ""]
    for name, s in m["shares"].items():
        v = s["value"]
        out.append(f"{name} ({s['label']}): {'n/a' if v is None else f'{v:+.3f}'}")
    out += ["", "## Claim wording (REQ-45)", "", f"Claim: {m['claim']}.", ""]
    out += ["## Per arm (pooled over documents)", ""]
    cols = (
        "runs found_fraction_mean half_found_share jaccard_mean consistent_items stable_hit_rate "
        "wrong_blockers_per_run found_any_mean found_blocking_mean nonprobe_findings_per_run elapsed_mean "
        "elapsed_median tokens_per_run kills retries reasks fallbacks invalid check_skipped"
    ).split()
    out.append("| arm | " + " | ".join(cols) + " |")
    out.append("|---|" + "---|" * len(cols))
    for arm, a in m["arms"].items():
        p = a["pooled"]
        out.append(
            f"| {arm} | "
            + " | ".join(
                fmt(p[c]) if isinstance(p[c], float) or p[c] is None else str(p[c])
                for c in cols
            )
            + " |"
        )
    out += [
        "",
        "Elapsed time is reported as mean and median (REQ-29); re-asks are a column of their own, apart from retries.",
        "",
    ]
    out += ["## Per document", ""]
    for arm, a in m["arms"].items():
        for doc, p in a["documents"].items():
            out.append(
                f"- {arm} {doc}: found fraction {fmt(p['found_fraction_mean'])}, elapsed mean {fmt(p['elapsed_mean'], 1)}, "
                f"median {fmt(p['elapsed_median'], 1)}, p90 {fmt(p['elapsed_p90'], 1)}, consistent items {p['consistent_items']}"
            )
    out += [
        "",
        "## Reach per class with Wilson intervals (95%)",
        "",
        "| arm | class | hits | runs x items | rate | low | high |",
        "|---|---|---|---|---|---|---|",
    ]
    for arm, a in m["arms"].items():
        for c, r in a["pooled"]["class_reach"].items():
            out.append(
                f"| {arm} | {c} | {r['hits']} | {r['trials']} | {fmt(r['rate'])} | {fmt(r['lo'])} | {fmt(r['hi'])} |"
            )
    out += report_ledger_sections(m)
    out += ["", "## Gates", ""]
    for cand, g in m["gates"].items():
        for name in ("D1", "D2", "D3", "D4", "D5", "D6", "D7"):
            x = g[name]
            out.append(
                f"- {cand} {name}: {'pass' if x['pass'] else 'not run' if x['pass'] is None else 'FAIL'} "
                + gate_detail(name, x)
            )
    out += [
        "",
        "## Time: planned and measured (REQ-31)",
        "",
        "| quantity | planned | measured |",
        "|---|---|---|",
    ]
    t = m["time"]
    out.append(
        f"| b, smallest Z0 median of the slowest reviewer (s) | {fmt(t['b']['planned'], 1)} | {fmt(t['b']['measured'], 1)} |"
    )
    out.append(
        f"| break-even row cost, 14 rows (s) | {fmt(t['breakeven_row_cost_14']['planned'], 2)} | {fmt(t['breakeven_row_cost_14']['measured'], 2)} |"
    )
    out.append(
        f"| luna cost per row c (s) | {fmt(t['luna_cost_per_row']['planned'], 2)} | {fmt(t['luna_cost_per_row']['measured'], 2)} |"
    )
    out.append(
        f"| luna row cap (rows) | {t['luna_row_cap']['planned']} | {t['luna_row_cap']['measured'] if t['luna_row_cap']['measured'] is not None else 'n/a'} |"
    )
    out += [
        "",
        "## Stages (REQ-41)",
        "",
        "Per-row detail is in stages.jsonl (extraction is null for RL: there is no extractor).",
        "",
    ]
    out += ["## Definitions", ""]
    out += [
        "- found fraction: covered items over items of the document (judge's `gt_covered_any`); pooled means are over runs.",
        "- consistent: an item reached in at least 60% of the runs of an arm; stable-hit rate is consistent items over items reached at all.",
        "- non-probe findings: findings lines that reach the merge without `probe` and without `src: ledger`.",
        "- bootstrap: documents first, then runs; the lower bound is the 5th percentile of the difference.",
    ]
    return "\n".join(out) + "\n"


def report_ledger_sections(m):
    """The per-arm ledger tables of DESIGN 12.5: checks and re-asks, none_found share, rows per lens, reach per class
    per reviewer id."""
    out = [
        "",
        "## Ledger checks and re-asks per arm (DESIGN 12.5)",
        "",
        "| arm | over_budget recipe | over_budget lens | recipe_missing | unknown_item | classes_lost | re-asks asked | re-asks accepted | yield with re-ask (runs) | yield without re-ask (runs) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for arm, a in m["arms"].items():
        p = a["pooled"]
        y = p["reask_yield"]
        out.append(
            f"| {arm} | {p['over_budget']['recipe']} | {p['over_budget']['lens']} | {p['recipe_missing']} | "
            f"{p['unknown_item']} | {p['classes_lost']} | {p['reask_asked']} | {p['reask_accepted']} | "
            f"{fmt(y['with']['found_fraction_mean'])} ({y['with']['runs']}) | "
            f"{fmt(y['without']['found_fraction_mean'])} ({y['without']['runs']}) |"
        )
    out += [
        "",
        "none_found share: reviewer-runs with a NONE FOUND row of the class over reviewer-runs with a row of the class.",
        "",
        "| arm | class | none_found | ran | share |",
        "|---|---|---|---|---|",
    ]
    for arm, a in m["arms"].items():
        for c, v in a["pooled"]["none_found_share"].items():
            out.append(
                f"| {arm} | {c} | {v['none_found']} | {v['ran']} | {fmt(v['share'])} |"
            )
    out += ["", "## Rows per lens (mean rows of a ledger, by reviewer id)", ""]
    out += ["| arm | reviewer id | mean rows |", "|---|---|---|"]
    for arm, a in m["arms"].items():
        for rid, v in a["pooled"]["rows_per_lens"].items():
            out.append(f"| {arm} | {rid} | {fmt(v)} |")
    out += [
        "",
        "## Reach per class per reviewer id",
        "",
        "| arm | class | reviewer id | rows | ledger rows | selection | act | merge survival |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for arm, classes in m["stages"].items():
        for c, v in sorted(classes.items()):
            for rid, b in sorted(v["by_reviewer"].items()):
                out.append(
                    f"| {arm} | {c} | {rid} | {b['rows']} | {b['ledger_rows']} | {b['selection']} | {b['act']} | {b['merge_survival']} |"
                )
    return out


def gate_detail(name, x):
    if name == "D1":
        parts = [
            f"{d}: median ratio {fmt(v['ratio_median'])}, mean ratio {fmt(v['ratio_mean'])}, p90 ratio {fmt(v['ratio_p90'])}"
            for d, v in x["per_doc"].items()
        ]
        return "; ".join(parts) + f"; kills {x['kills']} ({fmt(x['kill_rate'])})"
    if name == "D2":
        return f"difference {fmt(x['diff'])}, lower bound {fmt(x['lower'])}"
    if name == "D3":
        return f"candidate {x['candidate']}, control {x['control']}"
    if name == "D4":
        return f"wrong blockers difference {fmt(x['wrong_blockers_diff'])}, clean twins {fmt(x['clean_blocking_diff'])}"
    if name == "D6":
        return (
            "regressed items: "
            + (", ".join(x["regressed_items"]) or "none")
            + " (blocking gate)"
        )
    if name == "D7":
        return x.get("status") or f"gain over K {fmt(x['gain_over_k'])}"
    return (
        x.get("status")
        or f"general classes holding: {', '.join(x['general_classes_holding']) or 'none'}"
    )


# ---------------------------------------------------------------- subcommands


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def analyse(
    runs,
    gt,
    scores,
    stage=1,
    sets=None,
    seed=SEED,
    n=BOOT_N,
    cand_root=None,
    values=None,
):
    """The metrics dictionary (metrics.json) and the stage rows."""
    sets = sets or {}
    arms = split_arms(runs)
    m = {
        "schema": "rl-metrics/1",
        "stage": stage,
        "runs": len(runs),
        "seed": seed,
        "bootstrap_draws": n,
        "claim": CLAIM,
        "arms": {
            a: {
                "pooled": arm_metrics(rs, gt, scores),
                "documents": {
                    d: arm_metrics([r for r in rs if r["doc"] == d], gt, scores)
                    for d in sorted({r["doc"] for r in rs})
                },
            }
            for a, rs in sorted(arms.items())
        },
        "shares": share_values(arms, gt, scores),
        "gates": {},
        "decisions": {},
        "time": time_table(runs, values),
        "ablation": ablate(runs, gt, cand_root),
    }
    for cand, ctrl in PAIRS:
        if cand in arms and ctrl in arms:
            m["gates"][cand] = gates_for(
                cand,
                ctrl,
                "K" if cand == "RL" else None,
                arms,
                gt,
                scores,
                sets,
                seed,
                n,
            )
            m["decisions"][cand] = decide(m["gates"][cand], stage)
    rows = []
    for r in runs:
        rows += stage_rows(
            r, gt[r["doc"]], scores[r["id"]], candidate_text(r, cand_root)
        )
    m["stages"] = stage_rates(rows)
    return m, rows


def cmd_all(a):
    gt_path = a.gt or os.environ.get("RL_GT")
    if not gt_path:
        print(
            "E_USAGE: give the ground-truth path with --gt or RL_GT (it has no default)",
            file=sys.stderr,
        )
        return 2
    runs = load_runs(a.runs, f"stage{a.stage}-" if a.stage else "")
    scores, bad = load_scores(a.scoring)
    missing = [r["id"] for r in runs if r["id"] not in scores]
    if missing and not a.allow_unscored:
        print(
            f"E_UNSCORED: no valid first-judge score for {len(missing)} runs (audit-judges): {missing}",
            file=sys.stderr,
        )
        return 1
    runs = [r for r in runs if r["id"] in scores]
    sets = read_json(a.sets) if a.sets else {}
    try:
        m, rows = analyse(
            runs,
            load_gt(gt_path),
            scores,
            a.stage or 1,
            sets,
            a.seed,
            a.boot,
            a.cand_root,
            read_json(a.values) if a.values else None,
        )
    except ValueError as e:
        print(f"E_ANALYSIS: {e}", file=sys.stderr)
        return 1
    m["unscored"] = missing
    out = Path(a.out)
    write_json(out / "metrics.json", m)
    write_json(out / "d1.json", {c: g["D1"] for c, g in m["gates"].items()})
    (out / "stages.jsonl").write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8"
    )
    (out / "report.md").write_text(build_report(m), encoding="utf-8")
    for cand, dec in m["decisions"].items():
        print(
            f"{cand}: {dec['decision']}"
            + (f" (failed: {', '.join(dec['failed'])})" if dec["failed"] else "")
        )
    return 0


def cmd_compliance(a):
    res = compliance(run_dirs_of(a.runs))
    if a.out:
        write_json(a.out, res)
    lm = res["ledger_missing"]
    print(
        f"reviewer runs {res['reviewer_runs']} in {res['runs_checked']} runs; without a ledger file {res['reviewers_without_ledger_file']}"
    )
    print(
        f"ledger_missing: {lm['count']} of {res['reviewer_runs']} ({fmt(lm['rate'])}), limit {lm['limit']}: {'pass' if lm['pass'] else 'FAIL'}"
    )
    st = res["strict"]
    print(
        f"strict reading (nothing forgiven): ledger_missing {st['ledger_missing_strict']['count']} of {res['reviewer_runs']} "
        f"({fmt(st['ledger_missing_strict']['rate'])}): {'pass' if st['ledger_missing_strict']['pass'] else 'FAIL'}; "
        f"reports with a forgiven slip {st['forgiven_reports']}; by kind {st['forgiven_by_kind']}"
    )
    print(f"recipe_missing per class: {res['recipe_missing']}")
    q = res["quote_plan"]
    print(
        f"quote validity (quote_plan_ok): {q['ok']} of {q['rows_with_quote']} ({fmt(q['share'])})"
    )
    print(f"format errors: {res['format_errors']}")
    print(f"none_found per class: {res['none_found']}")
    print(
        f"over_budget: {res['over_budget']}; re-ask: {res['reask']}; rows per reviewer: {res['rows_per_reviewer']}"
    )
    return 0 if lm["pass"] else 1


def cmd_prereg(a):
    try:
        rec = prereg(read_json(a.owner_values) if a.owner_values else None)
    except ValueError as e:
        print(f"E_PREREG: {e}", file=sys.stderr)
        return 2
    if a.write:
        write_json(a.out or RL / "config" / "prereg.json", rec)
    else:
        print(json.dumps(rec, indent=1, sort_keys=True))
    return 0


def cmd_audit(a):
    argv = ["audit", "--scoring-dir", str(a.scoring_dir)]
    if a.out:
        argv += ["--out", a.out]
    return ja.main(argv + (["--invalidate"] if a.invalidate else []))


def cmd_sample(a):
    runs = list(a.runs)
    if a.runs_dir:
        runs += [
            r["id"] for r in load_runs(a.runs_dir, f"{a.stage}-" if a.stage else "")
        ]
    if not runs:
        print("E_USAGE: name runs, or --runs-dir and --stage", file=sys.stderr)
        return 2
    print("\n".join(ja.sample(runs, a.seed)))
    return 0


def cmd_ablate(a):
    gt_path = a.gt or os.environ.get("RL_GT")
    if not gt_path:
        print(
            "E_USAGE: give the ground-truth path with --gt or RL_GT (it has no default)",
            file=sys.stderr,
        )
        return 2
    res = ablate(
        load_runs(a.runs, f"stage{a.stage}-" if a.stage else ""),
        load_gt(gt_path),
        a.cand_root,
    )
    worst = max((v["points"] or 0) for v in res.values())
    for c, v in res.items():
        print(
            f"{c}: other classes gain {fmt(v['points'], 2)} points ({v['gained']} of {v['rows']} rows)"
        )
    print(
        f"largest change {worst:.2f} points; limit 15: {'pass' if worst <= 15 else 'revise the lens table'}"
    )
    return 0 if worst <= 15 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("all")
    p.add_argument("--stage", type=int, default=0)
    p.add_argument("--runs", default=str(RL / "runs"))
    p.add_argument("--scoring", default=str(RL / "scoring"))
    p.add_argument("--gt")
    p.add_argument("--out", default=str(RL / "results"))
    p.add_argument("--sets")
    p.add_argument("--values")
    p.add_argument("--cand-root")
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--boot", type=int, default=BOOT_N)
    p.add_argument("--allow-unscored", action="store_true")
    p.set_defaults(fn=cmd_all)
    p = sub.add_parser("compliance")
    p.add_argument("--runs", nargs="+", required=True)
    p.add_argument("--out")
    p.set_defaults(fn=cmd_compliance)
    p = sub.add_parser("prereg")
    p.add_argument("--write", action="store_true")
    p.add_argument("--owner-values")
    p.add_argument("--out")
    p.set_defaults(fn=cmd_prereg)
    p = sub.add_parser("audit-judges")
    p.add_argument(
        "stage",
        nargs="?",
        help="names the stage in the log only; every judge folder of --scoring-dir is audited",
    )
    p.add_argument("--scoring-dir", default=str(RL / "scoring"))
    p.add_argument("--out")
    p.add_argument("--invalidate", action="store_true")
    p.set_defaults(fn=cmd_audit)
    p = sub.add_parser("sample-second-judge")
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--runs-dir")
    p.add_argument("--stage")
    p.add_argument("runs", nargs="*")
    p.set_defaults(fn=cmd_sample)
    p = sub.add_parser("ablate-report")
    p.add_argument("--stage", type=int, default=0)
    p.add_argument("--runs", default=str(RL / "runs"))
    p.add_argument("--gt")
    p.add_argument("--cand-root")
    p.set_defaults(fn=cmd_ablate)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
