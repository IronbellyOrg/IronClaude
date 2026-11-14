"""Collect the counted rows of the five collaboration designs into one table (stdout, markdown).
Run: uv run --no-project python -I collect-results.py > counted-results.md
Reads each design's results folder as it is now; rows that are not finished are skipped. n = 1 row per cell: not a result, a snapshot."""
import json, glob, os
C = os.path.dirname(os.path.abspath(__file__))
def num(x, key=None):
    if isinstance(x, dict):
        if key and key in x: return x[key]
        vals = [v for v in x.values() if isinstance(v, (int, float))]
        return sum(vals) if vals else None
    return x
def mean(d):
    v = [x for x in (d or {}).values() if isinstance(x, (int, float))] if isinstance(d, dict) else []
    return sum(v) / len(v) if v else None
rows = []
def add(design, panel, arm, r, over=None, deliv=None, invalid=None):
    rows.append(dict(design=design, panel=panel, arm=arm, found=r.get("found_14", r.get("found14")),
        rb=r.get("real_blocking_8", r.get("real_blocking8")), wrong=r.get("wrong_blockers"),
        ctl=r.get("control_found_2", r.get("control_found2")), cw=r.get("control_wrong_blockers"),
        tok=num(r.get("output_tokens"), "total"), el=num(r.get("elapsed_s")), over=over, deliv=deliv, invalid=invalid))
def ld(p):
    try: return json.load(open(p))
    except Exception: return None
# design 1: el2-c1x-r1 (collab), el2-c0-r4 (baseline), same for hl2 sl2
for P in ("el2", "hl2", "sl2"):
    for arm, row in (("collab", f"{P}-c1x-r1"), ("base", f"{P}-c0-r4")):
        r = ld(f"{C}/r1-move-radar/results/{row}.json")
        if r and r.get("status") == "complete":
            pk = r.get("packages", {})
            ov = mean({k: v.get("elapsed_over_baseline") for k, v in pk.items()}) if arm == "collab" else None
            dl = sum(sum((v.get("delivered") or {}).values()) for v in pk.values()) if arm == "collab" else None
            add("1 Move Radar", P, arm, r, over=ov, deliv=dl)
# design 2
for P in ("el2", "hl2", "sl2"):
    for arm, row in (("collab", f"f4-{P}-exc-r1"), ("base", f"a1-{P}-exc-r1")):
        r = ld(f"{C}/r2-idle-shift-sweeper/results/{row}.json")
        if r:
            pp = r.get("per_package", {})
            dl = sum(sum((v.get("facts_delivered") or {}).values()) for v in pp.values()) if arm == "collab" else None
            ov = mean({k: v for k, v in (r.get("overhead_pct") or {}).items()})
            add("2 Idle-Shift Sweeper", P, arm, r, over=(None if ov is None else 1 + ov / 100), deliv=dl, invalid=len(r.get("invalid") or []))
# design 3 (results.jsonl: arm A3 collab with tce, arm A1 base); take the latest row per (panel, arm)
last = {}
for line in open(f"{C}/r3-axis-flip-challenge/results/results.jsonl"):
    r = json.loads(line)
    if r.get("smoke"): continue
    last[(r["panel"], r["arm"])] = r
for (P, a), r in sorted(last.items()):
    if a == "A3":
        by = (r.get("tce") or {}).get("by_pkg", {})
        ov = mean({k: v.get("ratio") for k, v in by.items()}); dl = sum(sum((v.get("delivered") or {}).values()) for v in by.values())
        add("3 Axis-Flip Challenge", P, "collab", r, over=ov, deliv=dl, invalid=len(r.get("invalid_pkgs") or []))
    elif a == "A1":
        add("3 Axis-Flip Challenge", P, "base", r, invalid=len(r.get("invalid_pkgs") or []))
# design 4
for P in ("el2", "hl2", "sl2"):
    for arm, row in (("collab", f"tce-f7-{P}-r01"), ("base", f"a1-{P}-r01")):
        r = ld(f"{C}/r4-flag-and-adjudicate/results/{row}.json")
        if r and r.get("valid") is not None:
            cb = r.get("collab") or {}
            dl = sum(sum((v.get("delivered_per_reviewer") or {}).values()) for v in cb.values() if isinstance(v, dict)) if arm == "collab" else None
            oh = mean(r.get("overhead_pct")); add("4 Flag-and-Adjudicate", P, arm, r, over=(None if oh is None else 1 + oh / 100), deliv=dl)
# design 5
for P in ("el2", "hl2"):
    for arm, row in (("collab", f"f6x-{P}-r01"), ("base", f"a1x-{P}-r01")):
        r = ld(f"{C}/r5-coverage-deflection/results/{row}.json")
        if r:
            oh = mean(r.get("overhead_pct")); add("5 Coverage Deflection", P, arm, r, over=(None if oh is None else 1 + oh / 100), invalid=len(r.get("invalid") or []))
def f(x, d=1): return "-" if x is None else (f"{x:.{d}f}" if isinstance(x, float) else str(x))
print("| Design | Panel | Arm | Found /14 | Real blocking /8 | Wrong blockers | Control found /2 | Output tokens | Panel seconds (sum of 3 packages) | Elapsed / baseline (mean) | Messages delivered | Invalid pkgs |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in sorted(rows, key=lambda r: (r["panel"], r["design"], r["arm"] != "collab")):
    print(f"| {r['design']} | {r['panel']} | {r['arm']} | {f(r['found'])} | {f(r['rb'])} | {f(r['wrong'])} | {f(r['ctl'])} | {f(r['tok'])} | {f(r['el'],0)} | {f(r['over'],2)} | {f(r['deliv'])} | {f(r['invalid'])} |")
