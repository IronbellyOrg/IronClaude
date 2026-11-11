"""Common decision machinery (contract J10.5), adapted from $SP/p12/ab2/harness.py and $SP/p13/ab2/analysis.py.

D2: cost decides on the loop only (R_LOOP); R_B is reported beside it.  D3: Haiku is a separate stratum, never pooled.
D4: one +3 Sonnet extension, only from a Sonnet n=6 INCONCLUSIVE.  D6: cost enters only these post-hoc functions;
nothing here is called to stop, truncate or skip a run."""
import datetime
import hashlib
import json
import os
import pathlib
import re
import statistics
import subprocess
import sys
import tomllib

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S / "scratchpad"
P11 = SP / "p11"
CENTRAL = SP / "central"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
AUD_OUT = f"{D}/review/audit.md"
SPEC_BYTES = 57763

DEFAULT_DEC = {
    "baseline": {"a_base": 100424, "audit_base": 69044, "b_base": 169468, "b_blk": 1.50, "growth_mean_pct": 1.41,
                 "growth_median_pct": 0.97, "loop_pass": "6/6", "escalations": 0, "reviews_mean": 2.17, "a_median": 95106},
    "strata": {"sonnet_n": 6, "haiku_n": 4, "haiku_baseline": str(SP / "p14/haiku-baseline/results.json"),
               "haiku_failure_margin": 0.25},
    "extension": {"extra_sonnet": 3, "max_extensions": 1},
    "validity": {"min_completed": 5, "aud_gap_max": 0.75},
}

VERDICTS = {"ADOPT", "ADOPT (Haiku robustness pending)", "INCONCLUSIVE", "DROP", "NO-GO-OFFLINE", "BLOCKED", "PENDING", "CONTROL"}
ROW_KEYS = ["arm", "arm_label", "stratum", "role", "n_planned", "n_completed", "runs_dir", "metrics", "design_metrics",
            "haiku", "jev", "verdict", "rule", "extension_used"]
METRIC_KEYS = ["BLK", "AUD1", "AUD2", "A_mean", "A_median", "R_LOOP", "B_mean", "R_B", "growth_mean_pct", "growth_median_pct",
               "loop_pass", "escalations", "reviews_mean", "fix_cycles_mean"]
PASS_ENDS = ("PASS", "VERIFIED-PASS")


def _sc():
    if str(CENTRAL) not in sys.path:
        sys.path.insert(0, str(CENTRAL))
    import score_themes
    return score_themes


def _sec(dec, name):
    return {**DEFAULT_DEC.get(name, {}), **((dec or {}).get(name) or {})}


def load_decision(path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def _median(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


# ---------------------------------------------------------------- cost (D2, D6)
def cost_ratios(loop_mean, aud_mean, dec=None) -> dict:
    """The one place where the D2 convention lives.  R_LOOP decides; R_B is reported only."""
    b = _sec(dec, "baseline")
    A = loop_mean
    B = None if loop_mean is None or aud_mean is None else loop_mean + aud_mean
    return {"R_LOOP": None if A is None else A / b["a_base"],
            "R_B": None if B is None else B / b["b_base"], "A": A, "B": B}


def d6_limit(L: float, dec=None) -> float:
    """A limit L on R_B (loop + one audit) expressed as a limit on R_LOOP, rounded to two decimals."""
    b = _sec(dec, "baseline")
    return round((L * b["b_base"] - b["audit_base"]) / b["a_base"], 2)


# ---------------------------------------------------------------- baselines
def _blk(path):
    """(verdict, number of blocking findings) of an audit file, or None when it is not a PASS/FAIL audit."""
    sc = _sc()
    p = pathlib.Path(path)
    if not p.exists():
        return None
    v = sc.verdict_of(p.read_text(errors="ignore"))
    if v not in ("PASS", "FAIL"):
        return None
    return v, len(sc.blocking_findings(p))


def baseline_sonnet(dec=None, runs_dir=None, audit2_dir=None) -> dict:
    """Stage 2 arm 3 rescored from the files; the J10.6 constants are the fallback (provisional=True)."""
    b = _sec(dec, "baseline")
    runs_dir = pathlib.Path(runs_dir or P11 / "runs"); a2 = pathlib.Path(audit2_dir or SP / "p12/baseline-audit2")
    a1v, a2v, growth = [], [], []
    for k in range(1, 7):
        r = f"a3-r{k}"
        x = _blk(runs_dir / r / "aud/ws" / AUD_OUT)
        if x:
            a1v.append(x[1])
        y = _blk(a2 / r / "ws" / AUD_OUT)
        if y:
            a2v.append(y[1])
        sp = runs_dir / r / "aud/ws" / SPEC
        if sp.exists():
            growth.append((sp.stat().st_size - SPEC_BYTES) / SPEC_BYTES * 100)
    allv = a1v + a2v
    out = {"a_base": b["a_base"], "audit_base": b["audit_base"], "b_base": b["b_base"], "a_median": b["a_median"],
           "loop_pass": b["loop_pass"], "escalations": b["escalations"], "reviews_mean": b["reviews_mean"],
           "n_audits": len(allv), "provisional": False, "single_audit": not a2v}
    if allv:
        out.update(B_BLK=statistics.mean(allv), AUD1=_mean(a1v), AUD2=_mean(a2v))
    else:
        out.update(B_BLK=b["b_blk"], AUD1=None, AUD2=None, provisional=True)
    if growth:
        out.update(growth_mean_pct=statistics.mean(growth), growth_median_pct=statistics.median(growth))
    else:
        out.update(growth_mean_pct=b["growth_mean_pct"], growth_median_pct=b["growth_median_pct"], provisional=True)
    return out


def baseline_haiku(dec=None, path=None):
    """Shared Haiku baseline (D3) rescored from the p14 audit files; None when results.json is absent."""
    p = pathlib.Path(path or _sec(dec, "strata")["haiku_baseline"])
    if not p.exists():
        return None
    raw = json.load(open(p))
    runs = raw.get("runs", []) if isinstance(raw, dict) else raw
    runs = [r for r in runs if isinstance(r, dict)]
    base = p.parent / "runs"
    per_run, n_a1, n_a2, loops, auds, growth, passes, reviews = [], 0, 0, [], [], [], 0, []
    for v in runs:
        name = v.get("run")
        vals = []
        x = _blk(base / name / "aud/ws" / AUD_OUT) if name else None
        if x:
            vals.append(x[1]); n_a1 += 1
        elif v.get("audit1_blocking") is not None:
            vals.append(float(v["audit1_blocking"])); n_a1 += 1
        y = _blk(base / name / "aud2/ws" / AUD_OUT) if name else None
        if y:
            vals.append(y[1]); n_a2 += 1
        if vals:
            per_run.append(statistics.mean(vals))
        for key, lst in (("loop_tokens", loops), ("audit_tokens", auds), ("growth_pct", growth), ("reviews", reviews)):
            if v.get(key) is not None:
                lst.append(float(v[key]))
        if v.get("loop_verdict") == "PASS":
            passes += 1
    if not per_run:
        return None
    fail = raw.get("harness_failure_rate") if isinstance(raw, dict) else None
    return {"n": len(runs), "H_BLK": statistics.mean(per_run), "single_audit": n_a2 < len(runs), "n_audits": n_a1 + n_a2,
            "H_LOOP": _mean(loops), "H_AUDIT": _mean(auds), "growth_mean_pct": _mean(growth), "loop_pass": passes,
            "reviews_mean": _mean(reviews), "fail_rate": 0.0 if fail is None else float(fail),
            "provisional": n_a2 < len(runs), "path": str(p)}


# ---------------------------------------------------------------- runs
def _audit(cfg, run, sub):
    return _blk(cfg.runs_dir / run / sub / "ws" / AUD_OUT)


def run_metrics(state, cfg) -> dict:
    """Per run: BLK per audit, growth, LOOP tokens, AUD tokens, reviews, fix cycles, loop_end, escalated.
    An incomplete or lost run returns complete=False and no numbers."""
    run = state["run"]
    rec = {"run": run, "arm": state.get("arm"), "stratum": state.get("stratum", "sonnet"),
           "complete": bool(state.get("complete")) and not state.get("lost"), "lost": bool(state.get("lost")),
           "harness_failure": bool(state.get("lost") or state.get("manual") or sum((state.get("relaunch") or {}).values()))}
    if not rec["complete"]:
        return rec
    log = state["log"]
    a1, a2 = _audit(cfg, run, "aud"), _audit(cfg, run, "aud2")
    fb = (state.get("final_spec") or {}).get("bytes")
    if fb is None:
        sp = cfg.runs_dir / run / "ws" / SPEC
        fb = sp.stat().st_size if sp.exists() else None
    loop_steps = [s for s in cfg.worker_loop_steps if s in log and log[s].get("kind") != "coordinator"]
    toks = [log[s].get("output_tokens") for s in loop_steps]
    aud_t = [log[s].get("output_tokens") for s in ("AUD", "AUD2") if s in log and log[s].get("output_tokens") is not None]
    rec.update(
        aud1_blk=a1[1] if a1 else None, aud2_blk=a2[1] if a2 else None,
        aud1_verdict=a1[0] if a1 else None, aud2_verdict=a2[0] if a2 else None,
        BLK=_mean([x[1] for x in (a1, a2) if x]),
        growth_pct=None if fb is None else (fb - SPEC_BYTES) / SPEC_BYTES * 100,
        LOOP=sum(t for t in toks if t is not None), tokens_missing=[s for s, t in zip(loop_steps, toks) if t is None],
        AUD_tokens=_mean(aud_t), reviews=sum(1 for s in log if re.fullmatch(r"R\d+", s)),
        fix_cycles=sum(1 for s in log if re.fullmatch(r"V\d+", s)), loop_end=state.get("loop_end"),
        escalated=state.get("loop_end") == "ESCALATED")
    return rec


def arm_summary(runs, pass_ends=PASS_ENDS) -> dict:
    done = [r for r in runs if r.get("complete")]
    n = len(done)
    if not n:
        return {"n_completed": 0, "BLK": None, "AUD1": None, "AUD2": None, "A_mean": None, "A_median": None, "B_mean": None,
                "growth_mean_pct": None, "growth_median_pct": None, "loop_pass": "0/0", "escalations": 0, "reviews_mean": None,
                "fix_cycles_mean": None}
    a = [r["LOOP"] for r in done]
    aud = _mean([r["AUD_tokens"] for r in done])
    return {"n_completed": n, "BLK": _mean([r["BLK"] for r in done]), "AUD1": _mean([r["aud1_blk"] for r in done]),
            "AUD2": _mean([r["aud2_blk"] for r in done]), "A_mean": statistics.mean(a), "A_median": statistics.median(a),
            "B_mean": None if aud is None else statistics.mean(a) + aud,
            "growth_mean_pct": _mean([r["growth_pct"] for r in done]), "growth_median_pct": _median([r["growth_pct"] for r in done]),
            "loop_pass": f"{sum(1 for r in done if r.get('loop_end') in pass_ends)}/{n}",
            "escalations": sum(1 for r in done if r.get("escalated")),
            "reviews_mean": _mean([r["reviews"] for r in done]), "fix_cycles_mean": _mean([r["fix_cycles"] for r in done])}


# ---------------------------------------------------------------- verdict machinery (D3, D4)
def replica_agreement(rule_fn, runs_by_arm, *args, **kw):
    """rule_fn(runs_by_arm, which, *args, **kw) -> verdict string, `which` = (1,) or (2,) (audit-1-only / audit-2-only).
    Returns (agree, {"audit1": v1, "audit2": v2}); a disagreement means the experiment's verdict is INCONCLUSIVE."""
    v1 = rule_fn(runs_by_arm, (1,), *args, **kw)
    v2 = rule_fn(runs_by_arm, (2,), *args, **kw)
    return v1 == v2, {"audit1": v1, "audit2": v2}


def haiku_condition(test_runs, hb, dec=None) -> dict:
    """D3: test_runs = run_metrics() records of ALL Haiku runs of one arm (incomplete ones count towards the failure rate)."""
    margin = _sec(dec, "strata")["haiku_failure_margin"]
    done = [r for r in test_runs if r.get("complete")]
    out = {"state": "pending", "HR": None, "one_minus_HR": None, "fail_rate": None, "baseline_fail_rate": None,
           "n_completed": len(done), "BLK_H": None, "baseline_provisional": bool(hb and hb.get("provisional"))}
    if test_runs:
        out["fail_rate"] = sum(1 for r in test_runs if r.get("harness_failure")) / len(test_runs)
    if not hb or not hb.get("H_BLK") or not done:
        return out
    blk = _mean([r["BLK"] for r in done])
    hr = blk / hb["H_BLK"]
    out.update(BLK_H=blk, HR=hr, one_minus_HR=1 - hr, baseline_fail_rate=hb.get("fail_rate", 0.0))
    ok = (1 - hr) > 0 and out["fail_rate"] <= out["baseline_fail_rate"] + margin
    out["state"] = "agrees" if ok else "disagrees"
    return out


def final_verdict(sonnet_verdict, haiku_state) -> str:
    if sonnet_verdict != "ADOPT":
        return sonnet_verdict
    if haiku_state == "agrees":
        return "ADOPT"
    if haiku_state == "disagrees":
        return "INCONCLUSIVE"
    return "ADOPT (Haiku robustness pending)"


def extension_allowed(results, dec=None) -> bool:
    """D4: the Sonnet n=6 verdict is INCONCLUSIVE and the extension has not been used yet (never a second)."""
    st = _sec(dec, "strata"); ex = _sec(dec, "extension")
    rows = [r for r in results.get("rows", []) if r.get("stratum") == "sonnet"]
    tests = [r for r in rows if r.get("role") == "test"]
    if not tests or any(r.get("extension_used") for r in rows):
        return False
    if any(r.get("n_planned", 0) > st["sonnet_n"] for r in tests):
        return False
    return ex["max_extensions"] >= 1 and any(
        str(r.get("verdict", "")).startswith("INCONCLUSIVE") and r.get("extendable", True) for r in tests)


# ---------------------------------------------------------------- results file (p15-results/1)
def _validate_results(res) -> list:
    errs = []
    for k in ("schema", "experiment", "design_id", "decision_file", "stage", "status", "rows"):
        if k not in res:
            errs.append(f"missing key {k}")
    if res.get("schema") != "p15-results/1":
        errs.append("schema must be p15-results/1")
    if res.get("stage") not in ("offline", "live"):
        errs.append("stage must be offline|live")
    if res.get("status") not in ("complete", "partial", "not-run"):
        errs.append("status must be complete|partial|not-run")
    if not isinstance(res.get("rows"), list):
        errs.append("rows must be a list")
        return errs
    for i, row in enumerate(res["rows"]):
        for k in ROW_KEYS:
            if k not in row:
                errs.append(f"rows[{i}] missing {k}")
        if row.get("verdict") not in VERDICTS:
            errs.append(f"rows[{i}] verdict {row.get('verdict')!r} not allowed")
        if row.get("stratum") not in ("sonnet", "haiku", "offline"):
            errs.append(f"rows[{i}] stratum {row.get('stratum')!r} not allowed")
        if row.get("role") not in ("test", "control", "offline-gate"):
            errs.append(f"rows[{i}] role {row.get('role')!r} not allowed")
        m = row.get("metrics")
        if not isinstance(m, dict):
            errs.append(f"rows[{i}] metrics must be an object")
        else:
            for k in METRIC_KEYS:
                if k not in m:
                    errs.append(f"rows[{i}].metrics missing {k}")
    return errs


def write_results(path, results: dict) -> None:
    res = dict(results)
    res.setdefault("schema", "p15-results/1")
    res.setdefault("generated_utc", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
    errs = _validate_results(res)
    if errs:
        raise ValueError("invalid p15-results/1: " + "; ".join(errs))
    p = pathlib.Path(path)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(res, indent=1, default=str))
    os.replace(tmp, p)


def update_matrix() -> int:
    p = subprocess.run(["uv", "run", "--no-project", "python", str(CENTRAL / "build_matrix.py")],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print("ERROR matrix build failed:", (p.stdout + p.stderr)[-500:])
    return p.returncode
