"""alarms.py: arm-level alarms and the time verdict over many rows (R-24, R-25, R-45). DESIGN.md section 2.9.

Usage (from REPO): uv run python tools/alarms.py <panel> [--root R1]     read-only; prints one JSON report.
Rows with rep 0 (smoke) are ignored. A block = the collab-0 and collab-1 rows of one panel with the same rep.
- CONVERGENCE fires for a collab-1 row when its own_line_jaccard mean exceeds the collab-0 mean + 0.15, or its ledger rows
  fall more than 20% below the collab-0 mean (pass: at most 2 of 12 rows).
- SNAPSHOT fires for a collab-1 row when snapshot_missing exceeds 50% of its receiving reviewers.
- SLO budget: each package with elapsed_s > 1.35 x B_c spends one unit (budget 1 in 12), B_c = the collab-0 median of that
  package over the panel's rows.
- baseline_drift per block = median over packages of (collab-0 elapsed / B_f); outside [0.963, 1.10] the block is reported
  but not used for the time verdict.
- SAME_GAPS: every collab-1 row injected the same moves (expected for F3; reported, never a failure).
"""

from __future__ import annotations

import json
import os
import statistics
import sys

R1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def row_jaccard(r):
    return mean(list((r["collab_counters"].get("own_line_jaccard") or {}).values()))


def row_ledger(r):
    """Ledger rows of a complete row; None when any package is not ok (never a partial sum, DESIGN.md 5.4)."""
    ps = list(r["packages"].values())
    if not ps or any(p.get("status") != "ok" or p.get("ledger_rows") is None for p in ps):
        return None
    return sum(p["ledger_rows"] for p in ps)


def report(rows: list[dict]) -> dict:
    rows = [r for r in rows if r["rep"] >= 1]
    c0 = [r for r in rows if r["collab"] == 0]
    c1 = [r for r in rows if r["collab"] == 1]
    j0, l0 = mean([row_jaccard(r) for r in c0]), mean([row_ledger(r) for r in c0])
    conv = []
    for r in c1:
        j, ledg = row_jaccard(r), row_ledger(r)
        why = []
        if j is not None and j0 is not None and j > j0 + 0.15:
            why.append(f"jaccard {j:.3f} > {j0:.3f} + 0.15")
        if ledg is not None and l0 is not None and ledg < 0.8 * l0:
            why.append(f"ledger_rows {ledg} < 0.8 x {l0:.1f}")
        if why:
            conv.append({"row": r["row"], "why": why})
    snap = [r["row"] for r in c1 if r["collab_counters"].get("receivers")
            and r["collab_counters"]["snapshot_missing"] > 0.5 * r["collab_counters"]["receivers"]]
    pkgs = sorted({p for r in rows for p in r["packages"]})
    b_c = {p: statistics.median([r["packages"][p]["elapsed_s"] for r in c0 if r["packages"].get(p, {}).get("elapsed_s") is not None] or [0]) or None
          for p in pkgs}
    arms = {}
    for name, rs in (("collab0", c0), ("collab1", c1)):
        spent = [(r["row"], p) for r in rs for p in pkgs
                 if b_c[p] and r["packages"].get(p, {}).get("elapsed_s") is not None and r["packages"][p]["elapsed_s"] > 1.35 * b_c[p]]
        npk = sum(1 for r in rs for p in pkgs if r["packages"].get(p, {}).get("elapsed_s") is not None)
        hist = {}
        for r in rs:
            for m, n in r["collab_counters"].get("injections_by_move", {}).items():
                hist[m] = hist.get(m, 0) + n
        arms[name] = {"rows": len(rs), "slo_spent": spent, "slo_budget": npk / 12, "slo_over_budget": len(spent) > npk / 12,
                      "median_overhead_pct": {p: statistics.median(v) if (v := [r["packages"][p]["overhead_pct"] for r in rs
                                              if r["packages"].get(p, {}).get("overhead_pct") is not None]) else None for p in pkgs},
                      "injections_by_move": hist}
    blocks = []
    for r1 in c1:
        r0 = next((r for r in c0 if r["rep"] == r1["rep"]), None)
        if not r0:
            continue
        ratios = [r0["packages"][p]["elapsed_s"] / r0["packages"][p]["B_f"] for p in pkgs
                  if r0["packages"].get(p, {}).get("elapsed_s") and r0["packages"][p].get("B_f")]
        drift = statistics.median(ratios) if ratios else None
        blocks.append({"rep": r1["rep"], "baseline_drift": drift, "used": drift is not None and 0.963 <= drift <= 1.10})
    inj = [json.dumps(r["collab_counters"].get("injections_by_move", {}), sort_keys=True) for r in c1]
    return {"convergence": {"fired": conv, "count": len(conv), "pass": len(conv) <= 2, "collab0_jaccard_mean": j0, "collab0_ledger_mean": l0},
            "snapshot": {"fired": snap}, "arms": arms, "blocks": blocks,
            "same_gaps": len(inj) >= 2 and len(set(inj)) == 1}


def main(argv: list[str]) -> int:
    root = R1
    if "--root" in argv:
        i = argv.index("--root")
        root = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    jl = f"{root}/results/results.jsonl"
    rows = [json.loads(x) for x in open(jl).read().splitlines() if x.strip()] if os.path.exists(jl) else []
    rep = report([r for r in rows if r["panel"] == argv[0]])
    print(json.dumps(rep, indent=1))
    if rep["same_gaps"]:
        print("SAME_GAPS every collab-1 row injected the same moves (expected for F3; reported, not a failure)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
