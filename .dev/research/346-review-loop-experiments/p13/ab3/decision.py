"""Decision rules for arm c3, config driven (decision_rules.json). Implements D1-D4 of the owner addendum once.

Run record (dict) fields used: run, stratum ('sonnet'|'haiku'), completed (both audits ingested), decision ('PASS'|'ESCALATE'|...),
growth_pct, loop_tokens (D2: loop only, AUD excluded), audit_tokens (one audit), blk (list of blocking-id counts, one per audit), failed (lost/harness failure).
"""
import json
import pathlib
import statistics

HERE = pathlib.Path(__file__).parent
RULES = json.load(open(HERE / "decision_rules.json"))


def convert_limit(L, rules=RULES):
    """D6: convert a limit L stated on R_B (loop+audit) to a loop-only limit, rounded to two decimals."""
    return round((L * rules["B_BASE"] - rules["AUD_BASE"]) / rules["A_BASE"], 2)


def mean(xs):
    xs = list(xs)
    return statistics.mean(xs) if xs else None


def summarize(runs, rules=RULES):
    """Per-stratum arm summary. D2: R_LOOP (decides) and R_B (reported only)."""
    done = [r for r in runs if r.get("completed")]
    blk_all = [b for r in done for b in r["blk"]]
    a1 = [r["blk"][0] for r in done if len(r["blk"]) > 0]
    a2 = [r["blk"][1] for r in done if len(r["blk"]) > 1]
    loop = mean(r["loop_tokens"] for r in done if r.get("loop_tokens") is not None)
    aud = mean(r["audit_tokens"] for r in done if r.get("audit_tokens") is not None)
    return {
        "n_total": len(runs), "n_completed": len(done),
        "BLK_T": mean(blk_all), "AUD_mean": mean(a1), "AUD2_mean": mean(a2),
        "PASS_T": (sum(1 for r in done if r["decision"] == "PASS") / len(done)) if done else None,
        "GROWTH_T": mean(r["growth_pct"] for r in done if r.get("growth_pct") is not None),
        "A_T": loop, "R_LOOP": (loop / rules["A_BASE"]) if loop is not None else None,
        "B_T": (loop + aud) if loop is not None and aud is not None else None,
        "R_B": ((loop + aud) / rules["B_BASE"]) if loop is not None and aud is not None else None,
        "failure_rate": (sum(1 for r in runs if r.get("failed")) / len(runs)) if runs else None,
    }


def decide_sonnet(summary, rules=RULES):
    """Return ('ADOPT'|'DROP'|'INCONCLUSIVE', [reasons]). D1: three zones, thresholds from config."""
    s, c = summary, rules["sonnet"]
    if s["n_completed"] < c["min_completed"]:
        return "INCONCLUSIVE", [f"only {s['n_completed']} completed runs (< {c['min_completed']})"]
    if s["AUD_mean"] is not None and s["AUD2_mean"] is not None and abs(s["AUD_mean"] - s["AUD2_mean"]) > c["aud_vs_aud2_max_diff"]:
        return "INCONCLUSIVE", [f"AUD and AUD2 means differ by {abs(s['AUD_mean'] - s['AUD2_mean']):.2f} (> {c['aud_vs_aud2_max_diff']})"]
    drop = []
    if s["BLK_T"] > c["blk_drop_frac"] * rules["B_BLK"]:
        drop.append(f"BLK_T {s['BLK_T']:.2f} > {c['blk_drop_frac'] * rules['B_BLK']:.2f}")
    if s["R_LOOP"] > c["r_loop_drop_above"]:
        drop.append(f"R_LOOP {s['R_LOOP']:.2f} > {c['r_loop_drop_above']}")
    if s["PASS_T"] < c["pass_drop_below"]:
        drop.append(f"PASS_T {s['PASS_T']:.2f} < {c['pass_drop_below']:.2f}")
    if drop:
        return "DROP", drop
    ok = (s["BLK_T"] <= c["blk_adopt_frac"] * rules["B_BLK"] and s["PASS_T"] >= c["pass_adopt_at_least"]
          and s["R_LOOP"] <= c["r_loop_adopt_at_most"] and (s["GROWTH_T"] is None or s["GROWTH_T"] <= c["growth_adopt_at_most_pct"]))
    if ok:
        return "ADOPT", []
    return "INCONCLUSIVE", ["between the ADOPT and DROP thresholds"]


def extension_needed(sonnet_decision, n_sonnet_runs, extended, rules=RULES):
    """D4: if the n=6 Sonnet result is INCONCLUSIVE, add 3 Sonnet replicates once; never twice."""
    e = rules["extension"]
    return bool(e["enabled"] and sonnet_decision == "INCONCLUSIVE" and not extended)


def load_haiku_baseline(path=None, rules=RULES):
    """Parse $SP/p14/haiku-baseline/results.json tolerantly. Returns dict(mean_blk, failure_rate, n) or None if absent."""
    p = pathlib.Path(path or rules["haiku"]["baseline_results"])
    if not p.exists():
        return None
    d = json.load(open(p))
    runs = d.get("runs", d) if isinstance(d, (dict, list)) else []
    if isinstance(runs, dict):
        runs = list(runs.values())
    blks, failed = [], 0
    for r in runs:
        if not isinstance(r, dict):
            continue
        b = None
        for k in ("blk", "blocking", "aud_blocking", "audit_blocking", "audit_blockers", "blockers"):
            if k in r:
                b = r[k]
                break
        if isinstance(b, list):
            blks.extend(x for x in b if isinstance(x, (int, float)))
        elif isinstance(b, (int, float)):
            blks.append(b)
        failed += bool(r.get("failed") or r.get("lost"))
    mb = d.get("mean_blk") if isinstance(d, dict) else None
    if mb is None and blks:
        mb = statistics.mean(blks)
    if mb is None:
        return None
    return {"mean_blk": mb, "failure_rate": failed / max(len(runs), 1), "n": len(runs)}


def decide_haiku(summary, baseline, rules=RULES):
    """D3: relative reduction versus the Haiku baseline; never pooled. Returns (status, detail)."""
    if baseline is None or summary["n_completed"] == 0:
        return "pending", "Haiku baseline or Haiku runs missing"
    ratio = summary["BLK_T"] / baseline["mean_blk"] if baseline["mean_blk"] else None
    h = rules["haiku"]
    fail_ok = summary["failure_rate"] <= baseline["failure_rate"] + h["failure_rate_margin_over_baseline"]
    if ratio is None:
        return "pending", "baseline mean is zero"
    ok = ratio < h["required_ratio_below"] and fail_ok
    return ("supports" if ok else "does_not_support"), f"blocker ratio {ratio:.2f} (test/baseline), failure rate {summary['failure_rate']:.2f} vs baseline {baseline['failure_rate']:.2f}"


def final_line(sonnet_decision, haiku_status, extended):
    """Compose the one-line decision. Haiku never changes DROP/INCONCLUSIVE; it can only block or qualify an ADOPT."""
    if sonnet_decision == "ADOPT":
        if haiku_status == "supports":
            return "ADOPT"
        if haiku_status == "pending":
            return "ADOPT (Haiku robustness pending)"
        return "INCONCLUSIVE (Sonnet ADOPT, Haiku stratum does not support)"
    return sonnet_decision
