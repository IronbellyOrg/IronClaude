"""Analysis of finished runs (DESIGN 14.3, REQ-39): the one place where every metric is defined.

    analyze.py metrics --runs DIR [--gt PATH] [--out FILE]    per arm and per document metrics -> metrics.json
    analyze.py d1      --runs DIR --arm ARM [--base Z0] [--out FILE]    the time inputs of gate D1 -> d1.json

It reads only run folders (`DIR/<run>/run.json`, `timing.json`, `reviews/`, `normalised/`), the judge outputs that each run
names in `scoring/label-key.json`, and `config/`. A ground-truth file is opened only for the path given with `--gt`
(per-class reach needs the class of each item); there is no default ground-truth path in this file.

Definitions (each name below is defined here and nowhere else; `test_analyze.py::test_one_definition_of_found_fraction`):
  found_fraction           items the judge marks covered at any severity, over the items of the document, per run
  found_blocking_fraction  the same for items covered by a blocking ledger row (found-any and found-blocking stay apart)
  share_runs_found_half    share of runs whose found_fraction is at least 0.5
  run_jaccard              mean over pairs of runs of the same arm and document of |A and B| / |A or B| of their found sets;
                           a pair whose union is empty carries no information and is left out
  consistent_items         items reached in at least 60% of the runs of an arm and document (3 of 5): reach * 10 >= 6 * runs
  stable_hit_rate          consistent items over the items found in at least one run
  wrong_blockers           the judge's `wrong_blockers` per run
  nonprobe_findings        findings lines of the reports the merge read, without a `probe` value and without `src: ledger`;
                           a reviewer that is not `ok` contributes no report and so zero
  elapsed_s                `panel_elapsed_s` of timing.json (all runs, killed and fallback runs included: intention to treat)
  output_tokens            sum of `total_output_tokens_all` of the reviewers' cost files (the `tokens` key of the output)
  kills                    reviewers whose status is `killed`
  invalid                  reviewers whose status is neither `ok` nor `killed` (invalid or error: no usable report)
  retries                  sum over reviewers of (attempts - 1)
  fallbacks                runs whose run.json has `fallback: true`
  class_reach              per item class: found item-runs over item-runs, with a 95% Wilson interval
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

SW = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SW))

from scaffold import clock, fnd, judge  # noqa: E402

SCHEMA = "sweep-metrics/1"
CONSISTENT_NUM, CONSISTENT_DEN = 6, 10  # reached in at least 60% of the runs
HALF_NUM, HALF_DEN = 1, 2
WILSON_Z = 1.96
DIGITS = 6
METRICS = (
    "found_fraction",
    "found_blocking_fraction",
    "share_runs_found_half",
    "run_jaccard",
    "consistent_items",
    "stable_hit_rate",
    "wrong_blockers",
    "nonprobe_findings",
    "elapsed_s",
    "output_tokens",
    "kills",
    "invalid",
    "retries",
    "fallbacks",
    "class_reach",
    "ledger_headings",
    "ok_rate_planted",
)


class AnalysisError(Exception):
    """A run folder or an argument that cannot be analysed (never swallowed: the caller sees the reason)."""


@dataclass
class Run:
    name: str
    arm: str
    doc: str
    block: object
    fallback: bool
    reason: object
    elapsed: float
    reviewers: dict  # rid -> {"status", "attempts", "tokens", "nonprobe"}
    panel: str | None = None
    slowest: float | None = None  # timing.json slowest_reviewer_s: the run's own b
    found_any: frozenset | None = None
    found_blocking: frozenset | None = None
    gt_total: int = 0
    wrong: int = 0
    path: Path | None = field(default=None, repr=False)


# --- reading ----------------------------------------------------------------------------------------------------------


def _json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise AnalysisError(f"{path}: {type(e).__name__}: {e}") from e


def _report_nonprobe(path: Path) -> int:
    """Findings lines of one report that are neither probe lines nor promoted ledger lines."""
    n = 0
    for raw in fnd.lenient_lines(path.read_text(encoding="utf-8")):
        try:
            row = json.loads(raw)
        except ValueError:
            continue  # H2 and the reviewer check left only parseable lines for an accepted report
        if not isinstance(row, dict):
            continue
        if row.get("probe") is None and row.get("src") != "ledger":
            n += 1
    return n


def _reviewer(folder: Path, rid: str, status: str) -> dict:
    cost = folder / "reviews" / f"{rid}.cost.json"
    c = _json(cost) if cost.is_file() else {}
    nonprobe = 0
    if status == "ok":  # only an accepted reviewer has a report that the merge read
        for sub in ("normalised", "reviews"):
            rep = folder / sub / f"{rid}.md"
            if rep.is_file():
                nonprobe = _report_nonprobe(rep)
                break
    return {
        "status": status,
        "attempts": int(c.get("attempts", 1)),
        "tokens": int(c.get("total_output_tokens_all", 0)),
        "nonprobe": nonprobe,
    }


def _score(folder: Path):
    key = folder / "scoring" / "label-key.json"
    if not key.is_file():
        return None
    score = Path(_json(key)["dir"]) / "score.json"
    return _json(score) if score.is_file() else None


def load_run(folder, scores=True) -> Run:
    folder = Path(folder)
    meta = _json(folder / "run.json")
    timing = folder / "timing.json"
    if not timing.is_file():
        raise AnalysisError(f"{folder}: run.json without timing.json")
    t = _json(timing)
    status = {
        rid: v["status"] for rid, v in (meta.get("reviewer_status") or {}).items()
    }
    run = Run(
        name=folder.name,
        arm=meta["arm"],
        doc=meta["doc"],
        block=meta.get("block"),
        fallback=bool(meta.get("fallback")),
        reason=meta.get("reason"),
        elapsed=float(t["panel_elapsed_s"]),
        reviewers={rid: _reviewer(folder, rid, st) for rid, st in status.items()},
        panel=meta.get("panel"),
        slowest=t.get("slowest_reviewer_s"),
        path=folder,
    )
    if scores:
        s = _score(folder)
        if s is None:
            raise AnalysisError(f"{folder}: no judge score file")
        run.found_any = frozenset(s["gt_covered_any"])
        run.found_blocking = frozenset(s["gt_covered_blocking"])
        run.gt_total = int(s["gt_total"])
        run.wrong = int(s["wrong_blockers"])
    return run


def load_runs(stage_dir, scores=True) -> list[Run]:
    """Every run folder under stage_dir that holds a run.json, in name order."""
    root = Path(stage_dir)
    if not root.is_dir():
        raise AnalysisError(f"{root} is not a folder")
    runs = [
        load_run(f, scores)
        for f in sorted(root.iterdir())
        if (f / "run.json").is_file()
    ]
    if not runs:
        raise AnalysisError(f"no run folder under {root}")
    return runs


def load_classes(gt_path, doc) -> dict:
    """{item id: class} from a ground-truth file the caller named: a file (every document) or a folder (DIR/<doc>.json)."""
    p = Path(gt_path)
    if p.is_dir():
        p = p / f"{doc}.json"
    return {i["id"]: i["class"] for i in _json(p)["items"]}


# --- arithmetic -------------------------------------------------------------------------------------------------------


def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def median(xs):
    s = sorted(xs)
    n = len(s)
    if not n:
        return None
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def percentile(xs, q):
    """Linear interpolation between the closest ranks (q from 0 to 1)."""
    s = sorted(xs)
    if not s:
        return None
    pos = (len(s) - 1) * q
    lo = math.floor(pos)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def wilson(k, n, z=WILSON_Z):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [max(0.0, c - h), min(1.0, c + h)]


def _r(x):
    """Round every float of a nested result (the output is stable and compares with an expected file)."""
    if isinstance(x, float):
        return round(x, DIGITS)
    if isinstance(x, dict):
        return {k: _r(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_r(v) for v in x]
    return x


# --- the metrics (one definition each) ---------------------------------------------------------------------------------


def found_fraction(run: Run) -> float:
    return len(run.found_any) / run.gt_total


def found_blocking_fraction(run: Run) -> float:
    return len(run.found_blocking) / run.gt_total


def share_runs_found_half(runs) -> float:
    return sum(
        len(r.found_any) * HALF_DEN >= HALF_NUM * r.gt_total for r in runs
    ) / len(runs)


def _by_doc(runs):
    docs = {}
    for r in runs:
        docs.setdefault(r.doc, []).append(r)
    return docs


def run_jaccard(runs):
    vals = []
    for group in _by_doc(runs).values():
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                union = a.found_any | b.found_any
                if union:
                    vals.append(len(a.found_any & b.found_any) / len(union))
    return _mean(vals)


def _reach(runs):
    """[(doc, item id, runs that found it, runs of the document)] for every item of every document."""
    out = []
    for doc, group in sorted(_by_doc(runs).items()):
        for i in range(1, group[0].gt_total + 1):
            gid = f"GT{i}"
            out.append((doc, gid, sum(gid in r.found_any for r in group), len(group)))
    return out


def consistent_items(runs) -> int:
    return sum(
        hit * CONSISTENT_DEN >= CONSISTENT_NUM * n for _, _, hit, n in _reach(runs)
    )


def stable_hit_rate(runs):
    found = [(hit, n) for _, _, hit, n in _reach(runs) if hit]
    if not found:
        return None
    return sum(hit * CONSISTENT_DEN >= CONSISTENT_NUM * n for hit, n in found) / len(
        found
    )


def wrong_blockers(run: Run) -> int:
    return run.wrong


def nonprobe_findings(run: Run) -> int:
    return sum(v["nonprobe"] for v in run.reviewers.values())


def elapsed_s(run: Run) -> float:
    return run.elapsed


def output_tokens(run: Run) -> int:
    return sum(v["tokens"] for v in run.reviewers.values())


def kills(runs) -> int:
    return sum(v["status"] == "killed" for r in runs for v in r.reviewers.values())


def invalid(runs) -> int:
    return sum(
        v["status"] not in ("ok", "killed") for r in runs for v in r.reviewers.values()
    )


def retries(runs) -> int:
    return sum(v["attempts"] - 1 for r in runs for v in r.reviewers.values())


def fallbacks(runs) -> int:
    return sum(r.fallback for r in runs)


def class_reach(runs, classes) -> dict:
    """{class: {found, trials, reach, wilson}} over item-runs; classes maps a document to {item id: class}."""
    tally = {}
    for r in runs:
        for gid, cls in classes[r.doc].items():
            t = tally.setdefault(cls, [0, 0])
            t[0] += gid in r.found_any
            t[1] += 1
    return {
        c: {"found": k, "trials": n, "reach": k / n, "wilson": wilson(k, n)}
        for c, (k, n) in sorted(tally.items())
    }


# --- groups -----------------------------------------------------------------------------------------------------------


def _series(values):
    return {"per_run": list(values), "mean": _mean(values)}


def group_metrics(runs, classes=None) -> dict:
    """Every metric of DESIGN 14.3 for the runs of one arm (one document, or all of its documents)."""
    el = [elapsed_s(r) for r in runs]
    items = sum(r.gt_total for r in {r.doc: r for r in runs}.values())
    consistent = consistent_items(runs)
    out = {
        "runs": len(runs),
        "found_fraction": _series([found_fraction(r) for r in runs]),
        "found_blocking_fraction": _series([found_blocking_fraction(r) for r in runs]),
        "share_runs_found_half": share_runs_found_half(runs),
        "run_jaccard": run_jaccard(runs),
        "consistent_items": consistent,
        "consistent_share": consistent / items,
        "stable_hit_rate": stable_hit_rate(runs),
        "wrong_blockers": _series([wrong_blockers(r) for r in runs]),
        "nonprobe_findings": _series([nonprobe_findings(r) for r in runs]),
        "elapsed_s": {
            "per_run": el,
            "mean": _mean(el),
            "median": median(el),
            "p90": percentile(el, 0.9),
        },
        "tokens": _series([output_tokens(r) for r in runs]),
        "kills": kills(runs),
        "retries": retries(runs),
        "fallbacks": fallbacks(runs),
        "invalid": invalid(runs),
    }
    if classes is not None:
        out["class_reach"] = class_reach(runs, classes)
    return out


def metrics(runs, classes=None) -> dict:
    """{schema, arms: {arm: {runs, docs: {doc: group}, pooled: group}}}. classes: {doc: {item id: class}} or None."""
    arms = {}
    for arm in sorted({r.arm for r in runs}):
        mine = [r for r in runs if r.arm == arm]
        arms[arm] = {
            "runs": len(mine),
            "docs": {
                d: group_metrics(g, classes) for d, g in sorted(_by_doc(mine).items())
            },
            "pooled": group_metrics(mine, classes),
        }
    return _r({"schema": SCHEMA, "arms": arms})


# --- gate D1 inputs ---------------------------------------------------------------------------------------------------


def d1_inputs(runs, arm, base="Z0") -> dict:
    """Per-document medians of the arm against the base arm's runs of the same randomised blocks only.

    A base run whose block holds no run of the arm on that document is ignored (and listed); with no base run left for a
    document the call raises. Every run counts, killed and fallback runs included (intention to treat).
    """
    docs, launched, killed = {}, 0, 0
    mine = [r for r in runs if r.arm == arm]
    if not mine:
        raise AnalysisError(f"no run of arm {arm}")
    for doc, group in sorted(_by_doc(mine).items()):
        blocks = {r.block for r in group}
        basis = [r for r in runs if r.arm == base and r.doc == doc]
        same = [r for r in basis if r.block in blocks]
        if not same:
            raise AnalysisError(f"{doc}: no {base} run in the blocks of {arm}")
        a, z = [r.elapsed for r in group], [r.elapsed for r in same]
        docs[doc] = {
            "arm_runs": len(a),
            "base_runs": len(z),
            "arm_median": median(a),
            "base_median": median(z),
            "ratio": median(a) / median(z),
            "arm_p90": percentile(a, 0.9),
            "base_p90": percentile(z, 0.9),
            "p90_ratio": percentile(a, 0.9) / percentile(z, 0.9),
            "ignored_base_runs": sorted(r.name for r in basis if r.block not in blocks),
        }
    for r in mine:
        launched += len(r.reviewers)
        killed += sum(v["status"] == "killed" for v in r.reviewers.values())
    return _r(
        {
            "arm": arm,
            "base": base,
            "docs": docs,
            "reviewers_launched": launched,
            "reviewers_killed": killed,
            "kill_share": killed / launched if launched else None,
        }
    )


# --- gates D1 to D7 (MR 5.7), shares and the outcome ------------------------------------------------------------------

BOOTSTRAP_SEED = 20261115
BOOTSTRAP_N = 2000
BOOTSTRAP_Q = 0.05  # the lower end of the two-sided 90% interval
EPS = 1e-9
GENERAL_CLASSES = ("C2", "C4", "C5", "C6", "C8")
CLASSES = tuple(f"C{n}" for n in range(1, 9))
# Documents that are not decision documents: the derivation set, the planted set, clean twins, documentation, the sanity set.
NON_DECISION = frozenset(
    {
        "planted",
        "twin",
        "docs",
        "spec",
        "derivation",
        "sanity",
        "defect-rich",
        "control",
    }
)
BLOCKING = ("D6",)
LIMITS = {
    "d1_median_ratio": 1.35,
    "d1_p90_ratio": 1.50,
    "d1_kill_share": 0.10,
    "d2_effect": 0.12,
    "d2_lower_bound": 0.04,
    "d3_consistent_items": 3,
    "d4_wrong_blockers": 1.0,
    "d4_twin_blocking": 0.7,
    "d5_detection": 0.40,
    "d5_classes": 3,
    "d6_within": 0.10,
    "d6_reach_floor": 0.5,
    "d7_gain": 0.04,
}
# REQ-45: the one sentence that may be written about consistency.
CLAIM = (
    "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), "
    "and only for Redesign 1 at the high end of its range"
)
ARMS = ("Z0-raw", "Z0", "K", "SS")
SHARES = (
    ("H share", "Z0", "Z0-raw", "Z0 - Z0raw"),
    ("Prompting share", "K", "Z0", "K - Z0"),
    ("Redesign share", "SS", "Z0", "SS - Z0"),
)
# DESIGN 15.1 decision 2 and 1: recommended values, used until the owner gives others.
ACT_BANDS = {
    "C1": [0.10, 0.40],
    "C2": [0.20, 0.45],
    "C3": [0.03, 0.15],
    "C4": [0.50, 0.75],
    "C5": [0.35, 0.60],
    "C6": [0.05, 0.30],
    "C7": [0.15, 0.35],
    "C8": [0.40, 0.65],
}
RECOMMENDED_FLOOR = 0.45
STAGE1_RUNS = {"panel_runs": 75, "arms_z0_k_ss": 60, "z0_raw": 15}


def load_sets(path=None) -> dict:
    """{document id: set} from config/packages.json (`packages.<doc>.set`). A document that is not listed is a decision document."""
    p = Path(path) if path else SW / "config" / "packages.json"
    return {d: v.get("set") for d, v in _json(p).get("packages", {}).items()}


def doc_set(sets, doc):
    return (sets or {}).get(doc) or "holdout"


def decision_runs(runs, sets=None):
    return [r for r in runs if doc_set(sets, r.doc) not in NON_DECISION]


def _arm(runs, arm):
    return [r for r in runs if r.arm == arm]


def _common(a, b):
    """The runs of the two arms on the documents that both have."""
    docs = {r.doc for r in a} & {r.doc for r in b}
    return [r for r in a if r.doc in docs], [r for r in b if r.doc in docs]


def mean_found(runs):
    return _mean([found_fraction(r) for r in runs])


def bootstrap_lower(
    arm_runs, base_runs, seed=BOOTSTRAP_SEED, n=BOOTSTRAP_N, q=BOOTSTRAP_Q
):
    """Lower bound of the arm-minus-base difference of mean found fraction: documents are resampled first, then the runs."""
    a_by = {d: [found_fraction(r) for r in g] for d, g in _by_doc(arm_runs).items()}
    b_by = {d: [found_fraction(r) for r in g] for d, g in _by_doc(base_runs).items()}
    docs = sorted(set(a_by) & set(b_by))
    if not docs:
        raise AnalysisError("no document with runs of both arms")
    rng = random.Random(seed)
    diffs = []
    for _ in range(n):
        a_vals, b_vals = [], []
        for _d in docs:
            d = docs[rng.randrange(len(docs))]
            a_vals += [rng.choice(a_by[d]) for _ in a_by[d]]
            b_vals += [rng.choice(b_by[d]) for _ in b_by[d]]
        diffs.append(sum(a_vals) / len(a_vals) - sum(b_vals) / len(b_vals))
    return percentile(diffs, q)


def _status(checks):
    if any(c is False for c in checks):
        return "fail"
    if any(c is None for c in checks):
        return "pending"
    return "pass"


def gate_d1(runs, arm, base):
    inputs, checks = {}, []
    for panel in sorted({r.panel or "" for r in _arm(runs, arm)}):
        d = d1_inputs([r for r in runs if (r.panel or "") == panel], arm, base)
        inputs[panel or "unknown"] = d
        docs = d["docs"].values()
        checks += [
            all(v["ratio"] <= LIMITS["d1_median_ratio"] + EPS for v in docs),
            all(v["p90_ratio"] <= LIMITS["d1_p90_ratio"] + EPS for v in docs),
            d["kill_share"] is not None
            and d["kill_share"] <= LIMITS["d1_kill_share"] + EPS,
        ]
    return {"status": _status(checks), "inputs": inputs}


def _effect(arm_runs, base_runs):
    a, b = _common(arm_runs, base_runs)
    if not a:
        return None
    return {
        "difference": mean_found(a) - mean_found(b),
        "lower_bound": bootstrap_lower(a, b),
        "arm_mean": mean_found(a),
        "base_mean": mean_found(b),
    }


def gate_d2(arm_runs, base_runs):
    e = _effect(arm_runs, base_runs)
    if e is None:
        return {"status": "pending"}
    ok = (
        e["difference"] + EPS >= LIMITS["d2_effect"]
        and e["lower_bound"] > LIMITS["d2_lower_bound"]
    )
    return {"status": _status([ok]), **_r(e)}


def gate_d3(arm_runs, base_runs):
    a, b = _common(arm_runs, base_runs)
    if not a:
        return {"status": "pending"}
    ca, cb = consistent_items(a), consistent_items(b)
    ok = ca >= cb + LIMITS["d3_consistent_items"]
    return {
        "status": _status([ok]),
        "arm_consistent_items": ca,
        "base_consistent_items": cb,
    }


def merged_blocking_rows(run) -> int:
    p = run.path / "merged" / "ledger.json"
    if not p.is_file():
        return 0
    return sum(bool(row.get("blocking")) for row in _json(p).get("rows", []))


def gate_d4(runs, arm, base, sets):
    a, b = _common(
        _arm(decision_runs(runs, sets), arm), _arm(decision_runs(runs, sets), base)
    )
    if not a:
        return {"status": "pending"}
    wa, wb = (
        _mean([wrong_blockers(r) for r in a]),
        _mean([wrong_blockers(r) for r in b]),
    )
    out = {
        "wrong_blockers_arm": wa,
        "wrong_blockers_base": wb,
        "wrong_blockers_difference": wa - wb,
    }
    checks = [wa - wb <= LIMITS["d4_wrong_blockers"] + EPS]
    ta = [r for r in _arm(runs, arm) if doc_set(sets, r.doc) == "twin"]
    tb = [r for r in _arm(runs, base) if doc_set(sets, r.doc) == "twin"]
    if ta and tb:
        da, db = (
            _mean([merged_blocking_rows(r) for r in ta]),
            _mean([merged_blocking_rows(r) for r in tb]),
        )
        out.update(
            twin_blocking_arm=da,
            twin_blocking_base=db,
            twin_blocking_difference=da - db,
        )
        checks.append(da - db <= LIMITS["d4_twin_blocking"] + EPS)
    else:
        checks.append(None)  # no clean-twin runs yet
    return {"status": _status(checks), **_r(out)}


def gate_d5(runs, arm, base, sets, classes):
    mine = [r for r in _arm(runs, arm) if doc_set(sets, r.doc) == "planted"]
    out, checks = {}, []
    if mine and classes:
        reach = class_reach(mine, classes)
        det = {c: reach[c]["reach"] for c in GENERAL_CLASSES if c in reach}
        passing = sorted(c for c, v in det.items() if v + EPS >= LIMITS["d5_detection"])
        out.update(planted_detection=det, planted_classes_passing=passing)
        checks.append(len(passing) >= LIMITS["d5_classes"])
    else:
        checks.append(None)
    for label in ("docs", "spec"):
        a = [r for r in _arm(runs, arm) if doc_set(sets, r.doc) == label]
        b = [r for r in _arm(runs, base) if doc_set(sets, r.doc) == label]
        e = _effect(a, b) if a and b else None
        if e is None:
            checks.append(None)
            continue
        out[f"{label}_difference"], out[f"{label}_lower_bound"] = (
            e["difference"],
            e["lower_bound"],
        )
        checks.append(
            e["difference"] + EPS >= LIMITS["d2_effect"] and e["lower_bound"] > 0
        )
    return {"status": _status(checks), **_r(out)}


def _item_reach(runs):
    return {(d, g): hit / n for d, g, hit, n in _reach(runs)}


def gate_d6(arm_runs, base_runs):
    a, b = _common(arm_runs, base_runs)
    if not a:
        return {"status": "pending"}
    ra, rb = _item_reach(a), _item_reach(b)
    checked = sorted(k for k, v in rb.items() if v + EPS >= LIMITS["d6_reach_floor"])
    failing = [
        {
            "doc": d,
            "item": g,
            "base_reach": rb[(d, g)],
            "arm_reach": ra.get((d, g), 0.0),
        }
        for d, g in checked
        if ra.get((d, g), 0.0) < rb[(d, g)] - LIMITS["d6_within"] - EPS
    ]
    status = "fail" if failing else ("pass" if checked else "pending")
    return {
        "status": status,
        "items_checked": len(checked),
        "failing_items": _r(failing),
    }


def gate_d7(arm_runs, checklist_runs):
    e = _effect(arm_runs, checklist_runs)
    if e is None:
        return {"status": "pending"}
    ok = e["difference"] + EPS >= LIMITS["d7_gain"]
    return {
        "status": _status([ok]),
        "gain": round(e["difference"], DIGITS),
        "winner": "arm" if ok else "checklist",
    }


def outcome(g) -> dict:
    """The adoption result of the gates: any failed gate means do not adopt; D6 is blocking (REQ-42)."""
    failed = sorted(k for k, v in g.items() if v["status"] == "fail")
    pending = sorted(k for k, v in g.items() if v["status"] == "pending")
    if failed:
        names = ", ".join(k + (" (blocking)" if k in BLOCKING else "") for k in failed)
        result, text = "do not adopt", f"do not adopt: {names} failed"
    elif pending:
        result, text = (
            "pending",
            "pending: " + ", ".join(pending) + " not yet evaluated",
        )
    else:
        result, text = "adopt", "adopt: every gate passed"
    return {
        "result": result,
        "text": text,
        "failed": failed,
        "pending": pending,
        "blocking": [k for k in failed if k in BLOCKING],
    }


def gates(runs, arm="SS", base="Z0", checklist="K", sets=None, classes=None) -> dict:
    """Gates D1 to D7 of the arm against the base arm and the checklist arm, pooled over the decision documents."""
    dec = decision_runs(runs, sets)
    a, b, k = _arm(dec, arm), _arm(dec, base), _arm(dec, checklist)
    if not a or not b:
        raise AnalysisError(
            f"gates need runs of {arm} and {base} on decision documents"
        )
    g = {
        "D1": gate_d1(dec, arm, base),
        "D2": gate_d2(a, b),
        "D3": gate_d3(a, b),
        "D4": gate_d4(runs, arm, base, sets),
        "D5": gate_d5(runs, arm, base, sets, classes),
        "D6": gate_d6(a, b),
        "D7": gate_d7(a, k),
    }
    return {
        "arm": arm,
        "base": base,
        "checklist": checklist,
        "limits": LIMITS,
        "bootstrap": {
            "seed": BOOTSTRAP_SEED,
            "resamples": BOOTSTRAP_N,
            "lower_quantile": BOOTSTRAP_Q,
        },
        "gates": g,
        "outcome": outcome(g),
    }


def shares(runs) -> list:
    """The three gains as three separate numbers, each over the documents that both of its arms ran. Never added."""
    out = []
    for label, a, b, formula in SHARES:
        ra, rb = _common(_arm(runs, a), _arm(runs, b))
        out.append(
            {
                "label": label,
                "formula": formula,
                "value": mean_found(ra) - mean_found(rb) if ra else None,
                "documents": sorted({r.doc for r in ra}),
            }
        )
    return _r(out)


# --- stages (REQ-41), the rubber-stamp measure, compliance and DD-7 ----------------------------------------------------


def _opt(path):
    return _json(path) if path.is_file() else None


def _span(loc):
    """A 0-based half-open line range from a 1-based inclusive location."""
    if not loc or "line_start" not in loc:
        return None
    return (loc["line_start"] - 1, loc["line_end"])


def covers(text, span, quote, quote_spans) -> bool:
    """DESIGN 14.1: the flattened quote contains the text or is contained in it (text of 12 or more characters), or the
    line spans come within 3 lines of each other (the rule of FND.same_defect)."""
    a, q = fnd.flat(text or ""), fnd.flat(quote)
    if a and q and (q in a or (len(a) >= 12 and a in q)):
        return True
    return span is not None and any(
        span[0] <= s[1] + 3 and s[0] <= span[1] + 3 for s in quote_spans
    )


def _finding_lines(path):
    if not path.is_file():
        return []
    rows = []
    for raw in fnd.lenient_lines(path.read_text(encoding="utf-8")):
        try:
            row = json.loads(raw)
        except ValueError:
            continue
        if isinstance(row, dict) and row.get("anchor"):
            rows.append(row)
    return rows


def _members(run):
    m = _opt(run.path / "merged" / "ledger.json")
    if m is None:
        return None
    return {(x["reviewer_id"], x["fid"]) for row in m["rows"] for x in row["members"]}


def stage_rows(run, gt_items, cand_text) -> list:
    """One row per ground-truth item of the run's document: extraction, selection, act, merge survival, judge credit.

    Sheet arm (SS with a pre-pass): extraction = some candidate covers the item; selection = some selected item covers it;
    act = a PROBLEM row with its quotes or search result (`supported`) on a covering item; survival = a finding of that row
    (a linked finding or the promoted line) is a member of a merged row. Other arms have no extractor or sheet: extraction
    and selection are null, act = a reviewer finding whose anchor covers the item, survival the same through its member.
    A stage whose input file is missing is null. Judge credit = the judge's `gt_covered_any`.
    """
    p = run.path
    items = _opt(p / "prepass" / "items.json")
    cands = _opt(p / "prepass" / "candidates.json")
    members = _members(run)
    ok_reviewers = [rid for rid, v in run.reviewers.items() if v["status"] == "ok"]
    sheet = run.arm == "SS" and items is not None and not run.fallback
    checks = {rid: _opt(p / "check" / f"{rid}.ledger.json") for rid in ok_reviewers}
    findings = {} if sheet else _reports_findings(run, ok_reviewers)
    rows = []
    for g in gt_items:
        spans = fnd.locate(cand_text, g["plan_quote"])
        row = {
            "run": run.name,
            "arm": run.arm,
            "doc": run.doc,
            "item": g["id"],
            "class": g["class"],
            "blocking_in_implement": g.get("blocking_in_implement"),
            "extraction": None,
            "selection": None,
            "act": None,
            "merge_survival": None,
            "judge_credit": g["id"] in run.found_any,
        }
        if sheet:
            if cands is not None:
                row["extraction"] = any(
                    _covers_entry(c, g, spans) for c in cands["candidates"]
                )
            ids = {i["item_id"] for i in items["items"] if _covers_entry(i, g, spans)}
            row["selection"] = bool(ids)
            row["act"], acting = _sheet_acts(checks, ids)
        else:
            acting = [
                (rid, f["id"])
                for rid, lines in findings.items()
                for f in lines
                if covers(
                    f["anchor"],
                    _finding_span(cand_text, f["anchor"]),
                    g["plan_quote"],
                    spans,
                )
            ]
            row["act"] = bool(acting)
        row["merge_survival"] = (
            None if members is None else any(a in members for a in acting)
        )
        rows.append(row)
    return rows


def _covers_entry(entry, g, spans) -> bool:
    return covers(
        entry.get("anchor_text"), _span(entry.get("location")), g["plan_quote"], spans
    )


def _reports_findings(run, rids) -> dict:
    out = {}
    for rid in rids:
        for sub in ("normalised", "reviews"):
            f = run.path / sub / f"{rid}.md"
            if f.is_file():
                out[rid] = _finding_lines(f)
                break
    return out


def _sheet_acts(checks, ids):
    """(did a reviewer write a supported PROBLEM row on one of the items, the (reviewer id, finding id) pairs of those rows)."""
    acted, pairs = False, []
    for rid, led in checks.items():
        if led is None:
            continue
        hit = {
            r["item"]
            for r in led["ledger"]["rows"]
            if r["item"] in ids and r["verdict"] == "PROBLEM" and r.get("supported")
        }
        if hit:
            acted = True
            pairs += [
                (rid, f["id"])
                for f in led["findings"]
                if f.get("row_item") in hit and f.get("link")
            ]
            pairs += [
                (rid, x["id"]) for x in led.get("promoted", []) if x["item"] in hit
            ]
    return acted, pairs


def _finding_span(cand_text, anchor):
    spans = fnd.locate(cand_text, anchor)
    return (min(s[0] for s in spans), max(s[1] for s in spans)) if spans else None


def ok_rate_planted(runs, gt_by_doc, sets) -> dict:
    """Share of OK rows among the rows on selected items that cover a ground-truth item of a planted document.

    gt_by_doc maps a document to {"text": the candidate text, "items": the ground-truth items}. A row counts once in the
    total; in a class's own count once for each class of the items it covers.
    """
    rows = {}  # (run, reviewer, item id) -> [verdict, classes]
    for r in runs:
        if r.arm != "SS" or doc_set(sets, r.doc) != "planted":
            continue
        items = _opt(r.path / "prepass" / "items.json")
        if items is None:
            continue
        for g in gt_by_doc[r.doc]["items"]:
            spans = fnd.locate(gt_by_doc[r.doc]["text"], g["plan_quote"])
            ids = {i["item_id"] for i in items["items"] if _covers_entry(i, g, spans)}
            for rid, v in r.reviewers.items():
                led = (
                    _opt(r.path / "check" / f"{rid}.ledger.json")
                    if v["status"] == "ok"
                    else None
                )
                for row in (led or {}).get("ledger", {}).get("rows", []):
                    if row["item"] in ids:
                        entry = rows.setdefault(
                            (r.name, rid, row["item"]), [row["verdict"], set()]
                        )
                        entry[1].add(g["class"])
    total, ok = len(rows), sum(v == "OK" for v, _ in rows.values())
    per_class = {}
    for verdict, classes in rows.values():
        for c in classes:
            t = per_class.setdefault(c, {"rows": 0, "ok": 0})
            t["rows"] += 1
            t["ok"] += verdict == "OK"
    for t in per_class.values():
        t["ok_rate"] = t["ok"] / t["rows"]
    return _r(
        {
            "rows": total,
            "ok": ok,
            "ok_rate": ok / total if total else None,
            "per_class": dict(sorted(per_class.items())),
        }
    )


def ledger_headings(runs) -> dict:
    """DD-7: for Z0 and K, the accepted reports that hold a `## Ledger` heading (a reviewer reads CB-2 and may write one)."""
    out = {}
    for arm in ("Z0", "K"):
        reports = n = 0
        for r in _arm(runs, arm):
            for rid, v in r.reviewers.items():
                if v["status"] != "ok":
                    continue
                for sub in ("reviews", "normalised"):
                    f = r.path / sub / f"{rid}.md"
                    if f.is_file():
                        reports += 1
                        n += any(
                            ln.strip() == "## Ledger"
                            for ln in f.read_text(encoding="utf-8").splitlines()
                        )
                        break
        out[arm] = {"reports": reports, "with_ledger_heading": n}
    return out


COMPLIANCE_LIMIT = 0.10


def compliance(runs_dir) -> dict:
    """REQ-17: `ledger_missing` rate, quote validity, format errors and format-induced demotions of the compliance-spike runs."""
    root = Path(runs_dir)
    checked = missing = quote_rows = quote_ok = errors = induced = runs = 0
    for run in sorted(
        p for p in root.iterdir() if (p / "check" / "check.json").is_file()
    ):
        ck = _json(run / "check" / "check.json")
        runs += 1
        missing += len(ck.get("ledger_missing") or [])
        errors += int(ck.get("format_errors") or 0)
        induced += int(ck.get("format_induced_demotions") or 0)
        for f in sorted((run / "check").glob("*.ledger.json")):
            checked += 1
            for row in _json(f).get("ledger", {}).get("rows", []):
                if row.get("quote_plan"):
                    quote_rows += 1
                    quote_ok += bool(row.get("quote_plan_ok"))
    if not runs:
        raise AnalysisError(f"no run with check/check.json under {root}")
    rate = missing / checked if checked else None
    return _r(
        {
            "runs": runs,
            "reviewers_checked": checked,
            "ledger_missing": missing,
            "ledger_missing_rate": rate,
            "limit": COMPLIANCE_LIMIT,
            "go": rate is not None and rate <= COMPLIANCE_LIMIT + EPS,
            "quote_rows": quote_rows,
            "quote_plan_ok_share": quote_ok / quote_rows if quote_rows else None,
            "format_errors": errors,
            "format_induced_demotions": induced,
        }
    )


def prereg(owner=None) -> dict:
    """The pre-registration record (REQ-41, REQ-44): arms, run counts, the consistency definition, the gates, the floor and
    the act bands. Without owner values the recommended defaults stand and the record says so."""
    owner = owner or {}
    bands = {c: list(v) for c, v in ACT_BANDS.items()}
    bands.update({c: list(v) for c, v in (owner.get("act_bands") or {}).items()})
    if sorted(bands) != list(CLASSES):
        raise AnalysisError(f"act bands must name exactly {', '.join(CLASSES)}")
    for c, band in bands.items():
        if len(band) != 2 or not 0 <= band[0] < band[1] <= 1:
            raise AnalysisError(
                f"act band of {c} is not [lo, hi] with 0 <= lo < hi <= 1: {band}"
            )
    return {
        "schema": "sweep-prereg/1",
        "arms": list(ARMS),
        "stage1_runs": STAGE1_RUNS,
        "consistency": {
            "reach_at_least": CONSISTENT_NUM / CONSISTENT_DEN,
            "of_runs": "3 of 5",
        },
        "gates": {"limits": LIMITS, "blocking": list(BLOCKING)},
        "selection_recall_floor": owner.get(
            "selection_recall_floor", RECOMMENDED_FLOOR
        ),
        "act_bands": bands,
        "ground_truth_sha256": owner.get("ground_truth_sha256", {}),
        "owner_confirmed": bool(owner),
        "source": "owner values"
        if owner
        else "recommended defaults of DESIGN 15.1, not confirmed by the owner",
    }


# --- break-even and the report ----------------------------------------------------------------------------------------


def breakeven_values(b, values=None) -> dict:
    be = clock.breakeven(b, values=values)
    return {"prepass_s": be.prepass_s, "per_item_s": be.per_item_s}


def breakeven_lines(runs=None, values=None) -> list:
    """The break-even values next to the planned and the measured ones (REQ-31)."""
    v = clock.load_values() if values is None else values
    at = {b: breakeven_values(b, v) for b in (100, 122)}
    spike = v.get("spike") or {}
    c = spike.get("c_luna")
    lines = [
        f"Pre-pass seconds: planned {v.get('prepass_s_planning')} s, measured {v.get('prepass_s')} s; "
        f"break-even {at[100]['prepass_s']:.1f} s at b = 100 and {at[122]['prepass_s']:.1f} s at b = 122.",
        "Seconds per item (luna): planned "
        f"{v.get('breakeven', {}).get('c_ref')} s, measured "
        + (f"{c:.2f} s" if c is not None else "not measured yet (no spike record)")
        + f"; break-even {at[100]['per_item_s']:.2f} s at b = 100 and {at[122]['per_item_s']:.2f} s at b = 122.",
    ]
    if runs:
        for doc, group in sorted(_by_doc(_arm(runs, "Z0")).items()):
            slow = [r.slowest for r in group if r.slowest is not None]
            if slow:
                planned = v.get("b", {}).get(group[0].panel or "primary", {}).get(doc)
                shown = "not set" if planned is None else f"{planned} s"
                lines.append(
                    f"b of {doc} (Z0 slowest reviewer, median): planned {shown}, measured {median(slow):.1f} s."
                )
    return lines


def _fmt(x, nd=4):
    return "n/a" if x is None else f"{x:.{nd}f}"


def render_report(runs, g, sh, ledger, values=None, label=None, audit=None) -> str:
    """results/report.md: three shares as three lines, the one claim sentence, the arms, the gates, break-even, DD-7."""
    out = [f"# Sweep Sheet analysis{' (' + label + ')' if label else ''}", ""]
    out += [
        f"Runs read: {len(runs)}; arms: {', '.join(sorted({r.arm for r in runs}))}.",
        "",
    ]
    out += ["## Gains (three separate numbers, never added)", ""]
    out += [f"- {s['label']} ({s['formula']}): {_fmt(s['value'])}" for s in sh]
    out += ["", "## Claim", "", f"The Sweep Sheet {CLAIM}.", "", "## Arms", ""]
    out += [
        "| arm | runs | found fraction | found blocking | consistent items | elapsed mean s | elapsed median s | kills | fallbacks |"
    ]
    out += ["|---|---|---|---|---|---|---|---|---|"]
    for arm in sorted({r.arm for r in runs}):
        m = group_metrics(_arm(runs, arm))
        out.append(
            f"| {arm} | {m['runs']} | {_fmt(m['found_fraction']['mean'])} | {_fmt(m['found_blocking_fraction']['mean'])} | "
            f"{m['consistent_items']} | {_fmt(m['elapsed_s']['mean'], 1)} | {_fmt(m['elapsed_s']['median'], 1)} | {m['kills']} | {m['fallbacks']} |"
        )
    out += ["", f"## Gates ({g['arm']} against {g['base']} and {g['checklist']})", ""]
    for k, v in g["gates"].items():
        extra = ", ".join(
            f"{a} {_fmt(b, 3) if isinstance(b, float) else b}"
            for a, b in v.items()
            if a
            in (
                "difference",
                "lower_bound",
                "gain",
                "items_checked",
                "arm_consistent_items",
                "base_consistent_items",
            )
        )
        out.append(f"- {k}: {v['status']}" + (f" ({extra})" if extra else ""))
    out += ["", f"Outcome: {g['outcome']['text']}.", "", "## Time and break-even", ""]
    out += [f"- {ln}" for ln in breakeven_lines(runs, values)]
    out += ["", "## Ledger headings in Z0 and K reports (DD-7)", ""]
    out += [
        f"- {arm}: {v['with_ledger_heading']} of {v['reports']} reports"
        for arm, v in ledger.items()
    ]
    if audit is not None:
        out += [
            "",
            "## Judge audit",
            "",
            f"- {audit['checked']} judge folders checked, {audit['bad']} bad.",
        ]
    return "\n".join(out) + "\n"


# --- command line -----------------------------------------------------------------------------------------------------


def _writable(path) -> Path:
    """K1: output only under SW or /tmp."""
    p = Path(path).resolve()
    if SW in p.parents or Path("/tmp") in p.parents:
        return p
    raise AnalysisError(f"E_NOT_WRITABLE: {path} resolves to {p}")


def _write(obj, out):
    p = _writable(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return p


def cmd_metrics(a):
    runs = load_runs(a.runs)
    classes = None
    if a.gt:
        classes = {d: load_classes(a.gt, d) for d in sorted({r.doc for r in runs})}
    _write(metrics(runs, classes), a.out)


def cmd_d1(a):
    _write(d1_inputs(load_runs(a.runs, scores=False), a.arm, a.base), a.out)


def _runs_dir(a) -> Path:
    if a.runs:
        return Path(a.runs)
    if a.stage:
        # `all --stage 1` reads SW/runs/stage1; the other commands take the folder name (`audit-judges stage1`)
        return SW / "runs" / (f"stage{a.stage}" if a.cmd == "all" else a.stage)
    raise AnalysisError("give a stage name or --runs")


def judge_folders(runs_dir) -> list:
    """The judge folders that the label keys of the run folders name: the first judge and, when there is one, the second."""
    out = []
    for f in sorted(Path(runs_dir).iterdir()):
        key = f / "scoring" / "label-key.json"
        if key.is_file():
            k = _json(key)
            out.append(k["dir"])
            if k.get("second"):
                out.append(k["second"]["dir"])
    return out


def _gt_file(gt, doc) -> Path:
    p = Path(gt)
    return p / f"{doc}.json" if p.is_dir() else p


def cmd_all(a):
    runs = load_runs(_runs_dir(a))
    sets, out = load_sets(a.packages), Path(a.out)
    classes = gt_by_doc = None
    if a.gt:
        docs = sorted({r.doc for r in runs})
        classes = {d: load_classes(a.gt, d) for d in docs}
        gt_by_doc = {
            d: {
                "items": _json(_gt_file(a.gt, d))["items"],
                "text": (Path(a.cand_root) / d / "candidate.md").read_text(
                    encoding="utf-8"
                ),
            }
            for d in docs
        }
    result = gates(runs, a.arm, a.base, a.checklist, sets, classes)
    _write(metrics(runs, classes), out / "metrics.json")
    _write(result, out / "gates.json")
    _write(result["gates"]["D1"]["inputs"], out / "d1.json")
    if gt_by_doc:
        rows = [
            row
            for r in runs
            for row in stage_rows(
                r, gt_by_doc[r.doc]["items"], gt_by_doc[r.doc]["text"]
            )
        ]
        stages = _writable(out / "stages.jsonl")
        stages.write_text(
            "".join(json.dumps(x, sort_keys=True) + "\n" for x in rows),
            encoding="utf-8",
        )
        _write(ok_rate_planted(runs, gt_by_doc, sets), out / "ok_rate_planted.json")
    audit = judge.audit(judge_folders(_runs_dir(a)))
    _write(audit, out / "judge_audit.json")
    report = render_report(
        runs, result, shares(runs), ledger_headings(runs), label=a.label, audit=audit
    )
    _writable(out / "report.md").write_text(report, encoding="utf-8")
    print(result["outcome"]["text"])


def cmd_audit_judges(a):
    audit = judge.audit(judge_folders(_runs_dir(a)))
    _write(audit, a.out)
    print(f"judge audit: {audit['checked']} checked, {audit['bad']} bad")
    return 1 if audit["bad"] else 0


def cmd_sample_second_judge(a):
    ids = [
        f.name
        for f in sorted(_runs_dir(a).iterdir())
        if (f / "run.json").is_file() and (f / "merged" / "merged-1.md").is_file()
    ]
    for i in judge.sample(ids, a.seed):
        print(i)


def cmd_compliance(a):
    result = compliance(a.runs)
    _write(result, a.out)
    print(
        f"ledger_missing {result['ledger_missing']} of {result['reviewers_checked']}: {'go' if result['go'] else 'no go'}"
    )
    return 0 if result["go"] else 1


def cmd_prereg(a):
    owner = _json(Path(a.owner_values)) if a.owner_values else None
    record = prereg(owner)
    if a.write:
        print(_write(record, a.out))
    else:
        print(json.dumps(record, indent=1, sort_keys=True))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="analyze.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("metrics", help="per arm and per document metrics")
    m.add_argument("--runs", required=True)
    m.add_argument("--gt", help="a ground-truth file or folder (per-class reach)")
    m.add_argument("--out", default=str(SW / "results" / "metrics.json"))
    m.set_defaults(fn=cmd_metrics)
    d = sub.add_parser("d1", help="time inputs of gate D1")
    d.add_argument("--runs", required=True)
    d.add_argument("--arm", required=True)
    d.add_argument("--base", default="Z0")
    d.add_argument("--out", default=str(SW / "results" / "d1.json"))
    d.set_defaults(fn=cmd_d1)
    al = sub.add_parser(
        "all", help="metrics, gates D1-D7, stages.jsonl, shares and report.md"
    )
    al.add_argument(
        "--stage", help="a stage name or number: runs are read from SW/runs/stage<N>"
    )
    al.add_argument("--runs", help="the run folders (instead of SW/runs/stage<N>)")
    al.add_argument("--out", required=True)
    al.add_argument(
        "--gt", help="a ground-truth file or folder (stages, per-class reach)"
    )
    al.add_argument(
        "--cand-root",
        default=str(Path(os.environ.get("SW_SB_ROOT", "/tmp/evalsb-sweep")) / "cand"),
    )
    al.add_argument("--packages", help="a packages file (default config/packages.json)")
    al.add_argument("--arm", default="SS")
    al.add_argument("--base", default="Z0")
    al.add_argument("--checklist", default="K")
    al.add_argument("--label")
    al.set_defaults(fn=cmd_all)
    aj = sub.add_parser("audit-judges", help="audit every judge folder of a stage")
    aj.add_argument("stage", nargs="?")
    aj.add_argument("--runs")
    aj.add_argument("--out", default=str(SW / "results" / "judge_audit.json"))
    aj.set_defaults(fn=cmd_audit_judges)
    sj = sub.add_parser(
        "sample-second-judge", help="the seeded 15% sample of runs for a second judge"
    )
    sj.add_argument("stage", nargs="?")
    sj.add_argument("--runs")
    sj.add_argument("--seed", type=int, default=20261115)
    sj.set_defaults(fn=cmd_sample_second_judge)
    co = sub.add_parser(
        "compliance",
        help="ledger_missing rate and quote validity of the compliance-spike runs",
    )
    co.add_argument("--runs", required=True)
    co.add_argument("--out", default=str(SW / "results" / "compliance.json"))
    co.set_defaults(fn=cmd_compliance)
    pr = sub.add_parser(
        "prereg",
        help="the pre-registration record (arms, run counts, gates, floor, act bands)",
    )
    pr.add_argument("--write", action="store_true")
    pr.add_argument(
        "--owner-values",
        help="a JSON file: selection_recall_floor, act_bands, ground_truth_sha256",
    )
    pr.add_argument("--out", default=str(SW / "config" / "prereg.json"))
    pr.set_defaults(fn=cmd_prereg)
    args = ap.parse_args(argv)
    try:
        return args.fn(args) or 0
    except AnalysisError as e:
        print(f"analyze: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
