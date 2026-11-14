"""Alarms without ground truth (DESIGN 2.9; R-24, R-25, R-40, R-45) and the per-arm summary."""
import statistics
import sys
from pathlib import Path

from r5 import out, read_json, write_json

DRIFT_BAND = (0.963, 1.10)


def convergence(own_jaccard, ledger_rows, ref: dict | None):
    if not ref:
        return None
    a = own_jaccard is not None and ref.get("own_line_jaccard") is not None and own_jaccard > ref["own_line_jaccard"] + 0.15
    b = ledger_rows is not None and ref.get("ledger_rows") is not None and ledger_rows < 0.8 * ref["ledger_rows"]
    return bool(a or b)


def deflection(overlap: float, union: int, ref: dict | None) -> bool:
    fired = overlap > 0.50
    if ref and ref.get("union_anchored_tasks") is not None:
        fired = fired or union < ref["union_anchored_tasks"]
    return fired


def snapshot(missing_flags: list[int]) -> bool:
    """Arm level: snapshot_missing in more than 50% of receiving reviewers."""
    return bool(missing_flags) and sum(1 for x in missing_flags if x) / len(missing_flags) > 0.5


def slo_budget(slos: list[str]) -> dict:
    over = sum(1 for s in slos if s != "ok")
    return {"used": over, "of": len(slos), "stop_arm": over > 1}


def drift(B_c: float, B_f: float) -> dict:
    r = B_c / B_f
    return {"baseline_drift": r, "outside_band": not (DRIFT_BAND[0] <= r <= DRIFT_BAND[1])}


def package(run_dir, ref_file) -> dict:
    d = Path(run_dir)
    c = read_json(d / "collab.json")
    info = read_json(d / "run.json")
    refs = read_json(ref_file) if ref_file else None
    ref = (refs or {}).get("per_pkg", {}).get(info["pkg"])
    a = {"CONVERGENCE": convergence(c["own_line_jaccard"], c["ledger_rows"], ref),
         "DEFLECTION": deflection(c["deflection_overlap"], c["union_anchored_tasks"], ref),
         "SLO": c["slo"], "reference": "ok" if ref else "missing",
         "raw": {k: c[k] for k in ("own_line_jaccard", "ledger_rows", "deflection_overlap", "union_anchored_tasks", "elapsed_s", "baseline_elapsed_s")}}
    write_json(d / "alarms.json", a)
    return a


TCX_COLS = ("B_A1_s", "elapsed_s", "elapsed_over_baseline", "k_measured", "k_forced")


def arm(arm_label: str, rows: list[str]) -> dict:
    per_pkg: dict = {}
    conv, snaps, slos = [], [], []
    tcx_runs: dict = {}
    flags: dict = {}  # row -> time_cap_exception; rows that obeyed the cap and rows that did not are never summarised together
    for row in rows:
        for d in sorted((out() / "runs" / row).iterdir()):
            c = read_json(d / "collab.json")
            if not c:
                continue
            flags[row] = bool(c.get("time_cap_exception"))
            a = read_json(d / "alarms.json") or {}
            conv.append(bool(a.get("CONVERGENCE")))
            slos.append(c["slo"])
            for r in (c.get("reviewers") or {}).values():
                if r.get("role") == "receiver" and r.get("snapshot_missing") is not None:
                    snaps.append(r["snapshot_missing"])
            p = per_pkg.setdefault(d.name, {"own_line_jaccard": [], "ledger_rows": [], "union_anchored_tasks": [], "elapsed_s": []})
            for k in p:
                if c.get(k) is not None:
                    p[k].append(c[k])
            if flags[row]:
                tcx_runs.setdefault(d.name, []).append({"row": row, **{k: c.get(k) for k in TCX_COLS}, "messages_delivered": c.get("messages_delivered")})
    if len(set(flags.values())) > 1:
        raise SystemExit("refused: rows with time_cap_exception true and false are never summarised together: "
                         + ", ".join(f"{r}={v}" for r, v in sorted(flags.items())))
    tcx = bool(flags) and all(flags.values())
    means = {pkg: {k: (statistics.mean(v) if v else None) for k, v in m.items()} for pkg, m in per_pkg.items()}
    s = {"arm": arm_label, "time_cap_exception": tcx, "rows": rows, "runs": len(conv), "convergence_fired": sum(conv),
         "convergence_pass": sum(conv) <= 2, "SNAPSHOT": snapshot(snaps), "SLO": slo_budget(slos), "per_pkg": means}
    if tcx:
        s["time_cap_runs"] = tcx_runs
    # an exception arm never overwrites (or is read as) the summary of the same arm that obeyed the cap
    write_json(out() / "results" / f"arm-summary-{arm_label}{'-tcx' if tcx else ''}.json", s)
    return s


def main(argv: list[str]) -> int:
    import json
    if argv[0] == "package":
        ref = argv[argv.index("--ref") + 1] if "--ref" in argv else None
        print(json.dumps(package(argv[1], ref)))
    elif argv[0] == "arm":
        print(json.dumps(arm(argv[1], argv[2:])))
    else:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
