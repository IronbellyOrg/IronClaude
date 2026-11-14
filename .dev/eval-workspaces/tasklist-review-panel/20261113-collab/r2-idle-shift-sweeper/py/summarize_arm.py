"""Arm-level alarms and stop rules (R-24, R-25, MR 4, DESIGN 2.10) over one arm's results rows, with the same
panel's A1 rows as reference. No rule uses ground truth except wrong blockers (judge scores).

summarize_arm.py --rows results/*.json --baseline-rows <A1 rows...> --out <arm-summary.json>
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import statistics
import sys
from pathlib import Path

EPS = 1e-9

# run under `python -I` (no script dir on sys.path), so load the sibling by path
_spec = importlib.util.spec_from_file_location("r2_values", Path(__file__).with_name("values.py"))
_values = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_values)
slack_s = _values.slack_s


def run_mean(d: dict) -> float | None:
    xs = [v for v in d.values() if v is not None]
    return sum(xs) / len(xs) if xs else None


def ledger_rows(row: dict) -> int:
    return sum(int(p.get("ledger_rows") or 0) for p in row["per_package"].values())


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def summarize(rows: list[dict], base: list[dict]) -> dict:
    planning = [r["row"] for r in rows + base if r.get("planning")]
    if planning:
        raise ValueError(f"planning rows are never counted: {planning}")
    # time-cap exception rows (OVERRIDE.md) are never mixed with rows that obeyed the cap, in either direction
    exc_flags = {bool(r.get("time_cap_exception")) for r in rows + base}
    if len(exc_flags) > 1:
        raise ValueError("rows with time_cap_exception true must not be mixed with rows that obeyed the cap: "
                         f"exception {[r['row'] for r in rows + base if r.get('time_cap_exception')]}, "
                         f"cap-obeying {[r['row'] for r in rows + base if not r.get('time_cap_exception')]}")
    exception = exc_flags == {True}
    reasons, stop, fail = [], False, False
    # CONVERGENCE (own-line rule) and the independence guard
    a1_j = mean([run_mean(r["collab"]["own_line_jaccard"]) for r in base])
    a1_l = mean([ledger_rows(r) for r in base])
    fires = []
    for r in rows:
        j = run_mean(r["collab"]["own_line_jaccard"])
        f = (a1_j is not None and j is not None and j > a1_j + 0.15 + EPS) or \
            (a1_l and ledger_rows(r) < a1_l * 0.80 - EPS)
        if f:
            fires.append(r["row"])
    n = len(rows)
    guard_pass = len(fires) <= 2
    if n <= 6 and len(fires) >= 3:
        stop = True
        reasons.append("convergence_interim")
    elif not guard_pass:
        fail = True
        reasons.append("independence_guard")
    echo = [(r["row"], p, e) for r in rows for p, e in r["collab"]["echo_rate"].items() if e is not None and e > 0.60]
    rec_runs = sum(int(pp.get("receivers") or 0) for r in rows for pp in r["per_package"].values())
    snap = sum(int(pp.get("snapshot_missing") or 0) for r in rows for pp in r["per_package"].values())
    if rec_runs and snap / rec_runs > 0.5:
        stop = True
        reasons.append("snapshot")
    reruns = sum(r["collab"]["reruns"] for r in rows)
    mism = sum(r["collab"]["rerun_mismatches"] for r in rows)
    if reruns and mism / reruns > 0.10 + EPS:
        stop = True
        reasons.append("rerun_mismatch")
    # SLO budget: elapsed above 1.35 B_c + SLACK_S (concurrent per-package median) or slo_breach, more than 1 package
    # (run with the same PANEL_SLACK_S the rows were launched with)
    slack = slack_s()
    by_pkg: dict[str, list[float]] = {}
    for r in rows:
        for p, pp in r["per_package"].items():
            if pp.get("elapsed_s") is not None:
                by_pkg.setdefault(p, []).append(pp["elapsed_s"])
    B_c = {p: statistics.median(v) for p, v in by_pkg.items()}
    # exception rows: the 35% cap is waived by the owner, so only the row's own slo_breach (hang_kill, or elapsed above the
    # widened hang guard) counts; the elapsed / B_A1 ratio is reported below instead
    slo = sum(1 for r in rows for p, pp in r["per_package"].items()
              if pp.get("slo_breach") or (not exception and pp.get("elapsed_s") is not None
                                          and pp["elapsed_s"] > 1.35 * B_c[p] + slack + EPS))
    if slo > 1:
        stop = True
        reasons.append("slo_budget")
    a1_w = mean([r.get("wrong_blockers") for r in base])
    arm_w = mean([r.get("wrong_blockers") for r in rows])
    if a1_w is not None and arm_w is not None and arm_w > a1_w + 1.0 + EPS:
        fail = True
        reasons.append("wrong_blockers")
    flood_pk = []
    for r in rows:
        for p, pp in r["per_package"].items():
            k = pp.get("k") or 0
            if k and pp.get("facts_posted", 0) + pp.get("facts_harvested", 0) >= 2 * k:
                upt = mean([d / k for d in (pp.get("facts_delivered") or {}).values()])
                if upt is not None and upt < 0.5:
                    flood_pk.append((r["row"], p))
    total_pk = sum(len(r["per_package"]) for r in rows)
    flood = bool(total_pk) and len(flood_pk) > total_pk / 2
    exc_cols = [{"row": r["row"], "package": p, "applied": pp.get("time_cap_exception_applied"), "B_A1": pp.get("B_A1"),
                 "elapsed_s": pp.get("elapsed_s"), "elapsed_over_baseline": pp.get("elapsed_over_baseline"),
                 "k_measured": pp.get("k_measured"), "k": pp.get("k"), "messages_delivered": pp.get("messages_delivered")}
                for r in rows for p, pp in r["per_package"].items()] if exception else None
    return {"time_cap_exception": exception, "time_cap_exception_columns": exc_cols,
            "runs": n, "convergence_fires": fires, "independence_guard_pass": guard_pass,
            "a1_own_line_jaccard": a1_j, "a1_ledger_rows": a1_l, "echo_alarms": echo,
            "snapshot_missing_rate": snap / rec_runs if rec_runs else None,
            "rerun_mismatch_rate": mism / reruns if reruns else None, "slo_packages": slo, "B_c": B_c,
            "a1_wrong_blockers": a1_w, "arm_wrong_blockers": arm_w,
            "flood": flood, "flood_packages": flood_pk,
            "flood_runbook": "tighten the sweeper brief to only files outside the plan's named list" if flood else None,
            "stop": stop, "fail": fail, "reasons": reasons}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", nargs="+", required=True)
    ap.add_argument("--baseline-rows", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rows = [json.loads(Path(p).read_text()) for p in a.rows]
    base = [json.loads(Path(p).read_text()) for p in a.baseline_rows]
    try:
        res = summarize(rows, base)
    except ValueError as e:
        print(json.dumps({"error": str(e)}))
        return 2
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: res[k] for k in ("stop", "fail", "reasons")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
