"""Arm-level alarms, stop rules, SLO budget and the form contrast (design 2.9; R-24, R-25, R-36, R-37).

usage: arm_summary.py --panel <P> --a1 <results files...> --arm <results files...> --out results/<P>-<arm>-summary.json
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import sys

R4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLACK_S = float(os.environ.get("PANEL_SLACK_S", "0") or 0)  # owner decision 2026-11-14: the cap is 1.35 B + SLACK_S (0 = old cap)
SHORT = {"TASK-WF-designSpec-20261107-075614": "DS", "TASK-WF-makeTheAliasOnly-20261105-051649": "AL", "TASK-WF-design-20261108-041415": "DE"}


def fisher_one_sided(a: int, n: int, b: int, m: int) -> float:
    """P(X >= a) for X ~ Hypergeometric: a successes of n in the arm, b of m in A1."""
    K, N = a + b, n + m
    den = math.comb(N, n)
    return sum(math.comb(K, x) * math.comb(N - K, n - x) for x in range(a, min(K, n) + 1)) / den


def two_prop_z(x1: int, n1: int, x2: int, n2: int) -> float | None:
    if not n1 or not n2:
        return None
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return None if se == 0 else (x1 / n1 - x2 / n2) / se


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def run_jaccard(r):
    return _mean([c.get("own_line_jaccard") for c in (r.get("collab") or {}).values()])


def run_ledger_rows(r):
    v = [c.get("ledger_rows") for c in (r.get("collab") or {}).values()]
    return sum(x for x in v if x is not None) if any(x is not None for x in v) else None


def _tce_table(r: dict) -> dict:
    """Time-cap exception columns of one row, per package (OVERRIDE.md)."""
    t = {}
    for pkg, s in SHORT.items():
        c = (r.get("collab") or {}).get(pkg) or {}
        t[s] = {"B_A1": c.get("baseline_elapsed_s"), "elapsed_s": (r.get("elapsed_s") or {}).get(s),
                "elapsed_over_baseline": c.get("elapsed_over_baseline"), "k_measured": c.get("k_measured"),
                "k_forced": c.get("k_forced"), "k": c.get("k"), "delivered_per_reviewer": c.get("delivered_per_reviewer"),
                "cards_sent": c.get("cards_sent"), "cards_delivered": c.get("cards_delivered")}
    return {"row": r.get("row"), "valid": r.get("valid"), "found_14": r.get("found_14"), "wrong_blockers": r.get("wrong_blockers"),
            "control_wrong_blockers": r.get("control_wrong_blockers"), "packages": t}


def summarize(panel: str, a1: list[dict], arm: list[dict], schedule: list[dict] | None = None, act_rates=None) -> dict:
    """Rows stamped time_cap_exception never enter the cap-obeying statistics; they get their own block."""
    exc = [r for r in arm if r.get("time_cap_exception")]
    a1 = [r for r in a1 if not r.get("time_cap_exception")]
    out = _summarize(panel, a1, [r for r in arm if not r.get("time_cap_exception")], schedule, act_rates)
    out["n_arm_time_cap_exception"] = len(exc)
    if exc:
        st = _summarize(panel, a1, exc, schedule, act_rates)
        for k in ("time_verdict", "slo", "interim_futility", "blocks_excluded_from_time_verdict"):  # these test the +35% cap the exception waives
            st.pop(k, None)
        out["time_cap_exception"] = {"rows": [_tce_table(r) for r in exc], "stats": st,
                                     "note": "owner-authorised exception to the +35% cap; not comparable with the cap-obeying statistics above"}
    return out


def _summarize(panel: str, a1: list[dict], arm: list[dict], schedule: list[dict] | None = None, act_rates=None) -> dict:
    out: dict = {"panel": panel, "n_a1": len(a1), "n_arm": len(arm)}
    # STOP:no_cards (R-37, (h))
    no_cards = sum(1 for r in arm if sum((c.get("cards_sent") or 0) for c in (r.get("collab") or {}).values()) == 0)
    out["no_cards_runs"] = no_cards
    out["STOP:no_cards"] = no_cards > 0.5 * len(arm) if arm else False
    # STOP:flag_finding_overlap (pooled over packages with cards)
    num = den = 0.0
    for r in arm:
        for c in (r.get("collab") or {}).values():
            if c.get("flag_finding_overlap") is not None and c.get("cards_sent"):
                num += c["flag_finding_overlap"] * c["cards_sent"]
                den += c["cards_sent"]
    ffo = num / den if den else None
    out["flag_finding_overlap_pooled"] = ffo
    out["STOP:flag_finding_overlap"] = ffo is not None and ffo > 0.5
    # CONVERGENCE (R-25)
    a1_j = _mean([run_jaccard(r) for r in a1])
    a1_rows = _mean([run_ledger_rows(r) for r in a1])
    conv = []
    for r in arm:
        j, lr = run_jaccard(r), run_ledger_rows(r)
        fired = (j is not None and a1_j is not None and j > a1_j + 0.15) or (lr is not None and a1_rows and lr < 0.8 * a1_rows)
        conv.append({"row": r.get("row"), "own_line_jaccard": j, "ledger_rows": lr, "fired": bool(fired)})
    out["a1_own_line_jaccard"], out["a1_ledger_rows"] = a1_j, a1_rows
    out["CONVERGENCE"] = conv
    n_conv = sum(1 for c in conv if c["fired"])
    # SNAPSHOT
    recv = miss = 0  # receiving lunas: lunas dealt at least one card in a package-run
    for r in arm:
        for c in (r.get("collab") or {}).values():
            recv += c.get("receiving_lunas", 0)
            miss += c.get("snapshot_missing", 0)
    out["SNAPSHOT"] = recv > 0 and miss > 0.5 * recv
    out["snapshot_missing_share"] = miss / recv if recv else None
    # independence
    audit_viol = [r.get("row") for r in arm if not (r.get("audit") or {}).get("audit_ok", True)
                  or ((r.get("audit") or {}).get("harness_text_gt_overlap") or 0) > 0]
    out["independence"] = {"pass": n_conv <= 2 and not audit_viol, "convergence_runs": n_conv, "audit_violation_rows": audit_viol}
    # AGREEMENT (pooled)
    dl = cv = 0
    for r in arm:
        for c in (r.get("collab") or {}).values():
            for f in ("challenge", "finding"):
                x = (c.get("conversions") or {}).get(f) or {}
                dl += x.get("delivered", 0)
                cv += x.get("converted", 0)
    ag = cv / dl if dl else None
    out["adjudication_agreement_pooled"] = ag
    out["AGREEMENT"] = ag is not None and (ag > 0.90 or ag < 0.05)
    # SLO budget and time verdict (R-24)
    bc = {}
    for s in SHORT.values():
        xs = [r["elapsed_s"].get(s) for r in a1 if (r.get("elapsed_s") or {}).get(s) is not None]
        bc[s] = statistics.median(xs) if xs else None
    over, total, hang = 0, 0, 0
    per_pkg = {s: [] for s in SHORT.values()}
    for r in arm:
        for s, e in (r.get("elapsed_s") or {}).items():
            if e is None:
                continue
            total += 1
            per_pkg[s].append(e)
            if bc.get(s) and e > 1.35 * bc[s] + SLACK_S:
                over += 1
        hang += sum(1 for c in (r.get("collab") or {}).values() if c.get("hang_kill"))
    out["B_c"] = bc
    out["slo"] = {"over": over, "package_runs": total, "share": over / total if total else None,
                  "budget_exceeded": bool(total and over / total > 1 / 12), "hang_kills": hang, "SLO_BREACH": hang > 0}
    # baseline drift per randomised block: B_c (block's A1 rows) / B_f (frozen B_A1); out-of-band blocks leave the time verdict
    row_block = {e["row"]: e.get("block") for e in (schedule or []) if e.get("row")}
    by_short = {v: k for k, v in SHORT.items()}
    drift, excluded = {}, set()
    for blk in sorted({b for b in row_block.values() if b}):
        d = {}
        for s in SHORT.values():
            xs = [r["elapsed_s"][s] for r in a1 if row_block.get(r.get("row")) == blk and (r.get("elapsed_s") or {}).get(s) is not None]
            bfs = [(r.get("collab") or {}).get(by_short[s], {}).get("baseline_elapsed_s") for r in a1 + arm]
            bf = next((x for x in bfs if x), None)
            d[s] = round(statistics.median(xs) / bf, 4) if xs and bf else None
        drift[blk] = d
        if any(x is not None and not (0.963 <= x <= 1.10) for x in d.values()):
            excluded.add(blk)
    out["baseline_drift"] = drift
    out["blocks_excluded_from_time_verdict"] = sorted(excluded)
    tv = {}
    for s in SHORT.values():
        v = [r["elapsed_s"][s] for r in arm if row_block.get(r.get("row")) not in excluded and (r.get("elapsed_s") or {}).get(s) is not None]
        bf = next((x for x in ((r.get("collab") or {}).get(by_short[s], {}).get("baseline_elapsed_s") for r in arm) if x), None)
        over_hang = [e for e in v if bf and e > 1.5 * bf]
        tv[s] = {"median": statistics.median(v) if v else None, "B_c": bc[s], "B_f": bf, "above_hang_guard": len(over_hang),
                 "ok": bool(v and bc[s] and statistics.median(v) <= 1.35 * bc[s] + SLACK_S and not over_hang)}
    out["time_verdict"] = tv
    # no loss
    def m(rows, k):
        return _mean([r.get(k) for r in rows if r.get("valid")])
    nl = {k: (m(arm, k), m(a1, k)) for k in ("found_14", "wrong_blockers", "control_wrong_blockers")}
    out["no_loss"] = {
        "found_14": nl["found_14"], "wrong_blockers": nl["wrong_blockers"], "control_wrong_blockers": nl["control_wrong_blockers"],
        "pass": all(x is not None for p in nl.values() for x in p)
        and nl["found_14"][0] >= nl["found_14"][1] - 0.25
        and nl["wrong_blockers"][0] <= nl["wrong_blockers"][1] + 1.0
        and nl["control_wrong_blockers"][0] <= nl["control_wrong_blockers"][1] + 0.5,
    }
    # reach (Fisher one-sided)
    ra = sum(1 for r in arm if r.get("reach"))
    rb = sum(1 for r in a1 if r.get("reach"))
    out["reach"] = {"arm": ra, "n_arm": len(arm), "a1": rb, "n_a1": len(a1),
                    "fisher_p": round(fisher_one_sided(ra, len(arm), rb, len(a1)), 6) if arm and a1 else None}
    # form contrast (R-36)
    fc = {"challenge": [0, 0], "finding": [0, 0]}
    diffs = []
    for r in arm:
        per = {"challenge": [0, 0], "finding": [0, 0]}
        for c in (r.get("collab") or {}).values():
            for f in fc:
                x = (c.get("conversions") or {}).get(f) or {}
                per[f][0] += x.get("converted", 0)
                per[f][1] += x.get("delivered", 0)
        for f in fc:
            fc[f][0] += per[f][0]
            fc[f][1] += per[f][1]
        if per["challenge"][1] and per["finding"][1]:
            diffs.append(per["challenge"][0] / per["challenge"][1] - per["finding"][0] / per["finding"][1])
    out["form_contrast"] = {"challenge": fc["challenge"], "finding": fc["finding"],
                            "z": two_prop_z(fc["challenge"][0], fc["challenge"][1], fc["finding"][0], fc["finding"][1]),
                            "run_paired_mean_diff": _mean(diffs), "n_paired_runs": len(diffs)}
    # interim futility (after 6 runs)
    if len(arm) >= 6:
        first = arm[:6]
        hard_arm = sum(len(r.get("reach_ids") or []) for r in first)
        hard_a1 = sum(len(r.get("reach_ids") or []) for r in a1[:6])
        ovh = [o for r in first for o in (r.get("overhead_pct") or {}).values() if o is not None]
        conv6 = sum(1 for c in conv[:6] if c["fired"])
        out["interim_futility"] = {"hard_credits": [hard_arm, hard_a1], "median_overhead_pct": statistics.median(ovh) if ovh else None,
                                   "convergence_runs": conv6,
                                   "futile": hard_arm <= hard_a1 or (bool(ovh) and statistics.median(ovh) > 35) or conv6 >= 3}
    out["act_rates"] = {"measured": act_rates, "planning": {"posting": [0.6, 0.8], "reaching_defect": [0.3, 0.5]}}
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", required=True)
    ap.add_argument("--a1", nargs="+", required=True)
    ap.add_argument("--arm", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv[1:])
    load = lambda ps: [json.load(open(p)) for p in ps]  # noqa: E731
    sched = []
    sp = os.path.join(os.environ.get("R4_OUT", R4), "runs", "schedule.jsonl")
    if os.path.exists(sp):
        sched = [json.loads(ln) for ln in open(sp) if ln.strip()]
    ar = os.path.join(R4, "spikes", "out", "act-rates.json")
    acts = json.load(open(ar)) if os.path.exists(ar) else None
    out = summarize(a.panel, load(a.a1), load(a.arm), sched, acts)
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
