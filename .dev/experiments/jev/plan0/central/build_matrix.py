#!/usr/bin/env python3
"""Central matrix builder (contract J12): one row per design x arm x stratum, from every design's own results file.

  uv run --no-project python build_matrix.py [--check]

Reads (never writes) the experiment dirs; writes only $CENTRAL/matrix.json and $CENTRAL/MATRIX.md (temp file + os.replace).
`--check` validates every source and exits 1 on schema errors without writing.  Stdlib only.

Two layers per row: the values the design reported, and values rescored uniformly here from the frozen-audit files
(`runs/<run>/aud/ws/<AUD_OUT>` and `aud2/ws/<AUD_OUT>`, blockers via score_themes.blocking_findings).  BLK in the matrix is the
rescored one when available; a gap of more than 0.01 to the reported one sets blk_mismatch."""
import datetime
import hashlib
import json
import os
import pathlib
import re
import statistics
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_themes as sc  # noqa: E402

SCORE_THEMES_SHA = "0790276664f3f676cccb13fc0348da6a5dce7dcc08b737b67d6a5859eb430ecc"   # byte copy of $SP/p12/ab2/score_themes.py
CENTRAL = HERE
SP = HERE.parent
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
AUD_OUT = f"{D}/review/audit.md"
SPEC_BYTES = 57763
A_BASE, AUD_BASE, B_BASE = 100424, 69044, 169468

COLUMNS = ["design_id", "label", "arm", "arm_label", "stratum", "role", "n_planned", "n_completed", "BLK", "BLK_reported",
           "blk_mismatch", "AUD1", "AUD2", "A_mean", "R_LOOP", "B_mean", "R_B", "growth_mean_pct", "loop_pass", "escalations",
           "reviews_mean", "HR", "haiku_pending", "jev_input_tokens", "jev_usd", "verdict", "verdict_raw", "rule",
           "extension_used", "provisional", "source", "missing_keys", "notes"]

WARNINGS = []
SOURCES = []
BLOCKED = []


def warn(msg):
    WARNINGS.append(msg)


# ---------------------------------------------------------------- generic helpers
def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def register_source(design_id, path):
    p = pathlib.Path(path)
    if p.exists() and p.is_file():
        SOURCES.append({"design_id": design_id, "path": str(p), "sha256": sha256_file(p),
                        "mtime": datetime.datetime.fromtimestamp(p.stat().st_mtime, datetime.timezone.utc).isoformat(timespec="seconds")})


def load_json(p):
    try:
        return json.load(open(p))
    except (OSError, ValueError):
        return None


def mkrow(**kw):
    row = {c: None for c in COLUMNS}
    row.update(blk_mismatch=False, haiku_pending=False, extension_used=False, provisional=False, missing_keys=[], notes=[])
    row.update(kw)
    return row


def pick(d, path, missing, default=None):
    """Nested lookup that records a missing key (a present key whose value is null is not missing)."""
    cur = d
    for k in path:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            missing.append(".".join(path))
            return default
    return cur


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def frac_to_pct(x):
    """Growth is a fraction in some files and a percent in others: a value below 0.5 in magnitude is treated as a fraction."""
    x = num(x)
    if x is None:
        return None
    return x * 100 if abs(x) < 0.5 else x


def mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def ratio(a, b):
    return None if a is None or not b else a / b


# ---------------------------------------------------------------- verdict normalization (J12.3)
def normalize_verdict(raw):
    """-> (verdict, flags).  flags: haiku_pending, unmapped."""
    flags = {"haiku_pending": False, "unmapped": False}
    s = (raw or "").strip()
    u = s.upper()
    if not s or u in ("NOT RUN", "PENDING") or u.startswith("NOT RUN"):
        return "PENDING", flags
    if u.startswith("ADOPT"):
        flags["haiku_pending"] = "HAIKU ROBUSTNESS PENDING" in u
        return "ADOPT", flags
    if re.match(r"DROP(-\d)?\b", u):
        return "DROP", flags
    if u.startswith("INCONCLUSIVE"):
        return "INCONCLUSIVE", flags
    if u.startswith("NO-GO-OFFLINE") or u.startswith("FALSIFIED"):
        return "NO-GO-OFFLINE", flags
    if u.startswith("BLOCKED"):
        return "BLOCKED", flags
    if u.startswith("BASELINE"):
        return "BASELINE", flags
    if u.startswith("CONTROL"):
        return "CONTROL", flags
    flags["unmapped"] = True
    return "UNMAPPED", flags


def set_verdict(row, raw, design_id):
    v, flags = normalize_verdict(raw)
    row["verdict"], row["verdict_raw"] = v, raw
    row["haiku_pending"] = flags["haiku_pending"]
    if flags["unmapped"]:
        warn(f"UNMAPPED verdict {raw!r} in {design_id}")
    return v


# ---------------------------------------------------------------- rescoring
def _audit_blk(path):
    p = pathlib.Path(path)
    if not p.exists():
        return None
    v = sc.verdict_of(p.read_text(errors="ignore"))
    if v not in ("PASS", "FAIL"):
        return None
    return len(sc.blocking_findings(p))


def _stratum_of(state, name):
    if state and state.get("stratum") in ("sonnet", "haiku"):
        return state["stratum"]
    return "haiku" if re.search(r"h-r\d+$", name) else "sonnet"


def rescore_runs(runs_dir, arm=None):
    """-> {stratum: {n, BLK, AUD1, AUD2, growth_mean_pct, growth_median_pct, reviews_mean, escalations, runs}} over the runs of
    `runs_dir` whose two audits both have a PASS/FAIL verdict.  `arm` restricts to runs whose state.json arm equals it."""
    runs_dir = pathlib.Path(runs_dir)
    out = {}
    if not runs_dir.is_dir():
        return out
    for d in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
        a1 = _audit_blk(d / "aud/ws" / AUD_OUT)
        a2 = _audit_blk(d / "aud2/ws" / AUD_OUT)
        if a1 is None or a2 is None:
            continue
        st = load_json(d / "state.json") or {}
        if arm is not None and st.get("arm") != arm:
            continue
        spec = d / "aud/ws" / SPEC
        growth = (spec.stat().st_size - SPEC_BYTES) / SPEC_BYTES * 100 if spec.exists() else None
        rounds = {m.group(1) for k in (st.get("log") or {}) for m in [re.match(r"R(\d+)(?:\.|$)", k)] if m}
        s = _stratum_of(st, d.name)
        b = out.setdefault(s, {"runs": []})
        b["runs"].append({"run": d.name, "a1": a1, "a2": a2, "growth": growth, "reviews": len(rounds) or None,
                          "escalated": st.get("loop_end") == "ESCALATED" or (st.get("final") or {}).get("decision") == "ESCALATE"})
    for s, b in out.items():
        rs = b["runs"]
        b.update(n=len(rs), BLK=mean([(r["a1"] + r["a2"]) / 2 for r in rs]), AUD1=mean([r["a1"] for r in rs]),
                 AUD2=mean([r["a2"] for r in rs]), growth_mean_pct=mean([r["growth"] for r in rs]),
                 growth_median_pct=(statistics.median([r["growth"] for r in rs if r["growth"] is not None])
                                    if any(r["growth"] is not None for r in rs) else None),
                 reviews_mean=mean([r["reviews"] for r in rs]), escalations=sum(1 for r in rs if r["escalated"]))
    return out


def apply_rescore(row, rs):
    """Merge the uniform rescoring into a row: BLK becomes the rescored value, the design's own stays in BLK_reported."""
    row["BLK_reported"] = row["BLK"]
    if not rs or not rs.get("n"):
        return row
    row["BLK"] = rs["BLK"]
    if row["BLK_reported"] is not None and abs(row["BLK_reported"] - rs["BLK"]) > 0.01:
        row["blk_mismatch"] = True
    row["AUD1"], row["AUD2"] = rs["AUD1"], rs["AUD2"]
    if row["growth_mean_pct"] is None:
        row["growth_mean_pct"] = rs["growth_mean_pct"]
    if row["reviews_mean"] is None:
        row["reviews_mean"] = rs["reviews_mean"]
    if row["escalations"] is None:
        row["escalations"] = rs["escalations"]
    row["notes"].append(f"BLK rescored over {rs['n']} runs / {2 * rs['n']} audits")
    return row


def _pending_row(design, why, stratum="sonnet", **kw):
    r = mkrow(design_id=design["design_id"], label=design.get("label"), arm=design["design_id"], arm_label=design.get("label"),
              stratum=stratum, role="test", n_planned=kw.pop("n_planned", None), n_completed=0, source=why)
    set_verdict(r, "PENDING", design["design_id"])
    r["missing_keys"].append(why)
    r.update(kw)
    return r


# ---------------------------------------------------------------- baselines
def adapt_baseline_sonnet(design):
    runs_dir = pathlib.Path(design.get("runs_dir") or SP / "p11/runs")
    a2dir = pathlib.Path(design.get("audit2_dir") or SP / "p12/baseline-audit2")
    a1v, a2v, growth = [], [], []
    for k in range(1, 7):
        r = f"a3-r{k}"
        x = _audit_blk(runs_dir / r / "aud/ws" / AUD_OUT)
        y = _audit_blk(a2dir / r / "ws" / AUD_OUT)
        if x is not None:
            a1v.append(x)
        if y is not None:
            a2v.append(y)
        sp = runs_dir / r / "aud/ws" / SPEC
        if sp.exists():
            growth.append((sp.stat().st_size - SPEC_BYTES) / SPEC_BYTES * 100)
    allv = a1v + a2v
    row = mkrow(design_id=design["design_id"], label=design.get("label"), arm="a3", arm_label="Stage 2 arm 3 (PR #484 rules)",
                stratum="sonnet", role="baseline", n_planned=6, n_completed=len(a1v), A_mean=A_BASE, R_LOOP=1.0,
                B_mean=A_BASE + AUD_BASE, R_B=1.0, loop_pass="6/6", escalations=0, reviews_mean=2.17,
                source="rescored p11/runs/a3-r* + p12/baseline-audit2", extension_used=False)
    if allv:
        row.update(BLK=statistics.mean(allv), AUD1=mean(a1v), AUD2=mean(a2v))
    else:
        row.update(BLK=1.50, provisional=True)
        row["missing_keys"].append("baseline audit files")
        row["notes"].append("constants only (audit files not found)")
    row["BLK_reported"] = 1.50
    row["blk_mismatch"] = bool(allv) and abs(row["BLK"] - 1.50) > 0.01
    if growth:
        row.update(growth_mean_pct=statistics.mean(growth))
        row["notes"].append(f"growth median {statistics.median(growth):.2f}")
    else:
        row.update(growth_mean_pct=1.41, provisional=True)
    if not a2v:
        row["provisional"] = True
        row["notes"].append("single baseline audit")
    set_verdict(row, "BASELINE", design["design_id"])
    return [row]


def haiku_baseline_stats(path):
    """From <path>/results.json + runs/*/aud*/ws audits.  None when absent."""
    p = pathlib.Path(path) / "results.json"
    raw = load_json(p)
    if not isinstance(raw, dict):
        return None
    runs = [r for r in raw.get("runs", []) if isinstance(r, dict)]
    per_run, n_a2, a1s, a2s = [], 0, [], []
    for v in runs:
        name = v.get("run")
        vals = []
        x = _audit_blk(pathlib.Path(path) / "runs" / name / "aud/ws" / AUD_OUT) if name else None
        if x is not None:
            vals.append(x); a1s.append(x)
        elif num(v.get("audit1_blocking")) is not None:
            vals.append(v["audit1_blocking"]); a1s.append(v["audit1_blocking"])
        y = _audit_blk(pathlib.Path(path) / "runs" / name / "aud2/ws" / AUD_OUT) if name else None
        if y is not None:
            vals.append(y); n_a2 += 1; a2s.append(y)
        if vals:
            per_run.append(statistics.mean(vals))
    return {"raw": raw, "runs": runs, "BLK": mean(per_run), "single_audit": n_a2 < len(runs), "n_a2": n_a2,
            "AUD1": mean(a1s), "AUD2": mean(a2s)}


def adapt_baseline_haiku(design):
    path = design["path"]
    register_source(design["design_id"], pathlib.Path(path) / "results.json")
    hb = haiku_baseline_stats(path)
    if hb is None:
        return [_pending_row(design, "results.json", stratum="haiku", role="baseline")]
    runs, raw = hb["runs"], hb["raw"]
    miss = []
    A = mean([num(r.get("loop_tokens")) for r in runs])
    AUD = mean([num(r.get("audit_tokens")) for r in runs])
    row = mkrow(design_id=design["design_id"], label=design.get("label"), arm="a3h", arm_label="Stage 2 arm 3 design, Haiku loop workers",
                stratum="haiku", role="baseline", n_planned=raw.get("n", len(runs)), n_completed=len(runs), BLK=hb["BLK"],
                AUD1=hb["AUD1"], AUD2=hb["AUD2"], BLK_reported=num(raw.get("mean_blocking")), A_mean=A, R_LOOP=ratio(A, A_BASE),
                B_mean=None if A is None or AUD is None else A + AUD,
                growth_mean_pct=mean([num(r.get("growth_pct")) for r in runs]),
                loop_pass=f"{sum(1 for r in runs if r.get('loop_verdict') == 'PASS')}/{len(runs)}",
                reviews_mean=mean([num(r.get("reviews")) for r in runs]), HR=1.0,
                provisional=hb["single_audit"], source="p14/haiku-baseline/results.json + rescored audits")
    row["R_B"] = ratio(row["B_mean"], B_BASE)
    if A is None:
        miss.append("runs[].loop_tokens")
    if hb["BLK"] is None:
        miss.append("audit files and runs[].audit1_blocking")
    row["missing_keys"] = miss
    row["blk_mismatch"] = row["BLK_reported"] is not None and hb["BLK"] is not None and abs(row["BLK_reported"] - hb["BLK"]) > 0.01
    row["notes"].append("R_LOOP_H = 1.00 (own baseline); harness_failure_rate " + str(raw.get("harness_failure_rate")))
    if hb["single_audit"]:
        row["notes"].append("single audit per final spec so far (aud2 missing)")
    set_verdict(row, "BASELINE", design["design_id"])
    return [row]


# ---------------------------------------------------------------- p12 designs
def _p12_rows(design, sonnet, haiku, raw_verdict, rule, tag):
    """Common tail of the p12 adapters.  `sonnet`/`haiku` are dicts of already-picked reported values (or None)."""
    rs = rescore_runs(pathlib.Path(design["path"]) / "runs")
    rows = []
    r = mkrow(design_id=design["design_id"], label=design.get("label"), arm=tag, arm_label=design.get("label"), stratum="sonnet",
              role="test", n_planned=sonnet.get("n_planned"), n_completed=sonnet.get("n_completed"), BLK=sonnet.get("BLK"),
              A_mean=sonnet.get("A"), R_LOOP=sonnet.get("R_LOOP"), B_mean=sonnet.get("B"), R_B=sonnet.get("R_B"),
              growth_mean_pct=sonnet.get("growth"), loop_pass=sonnet.get("loop_pass"), rule=rule,
              source=sonnet.get("source"), missing_keys=list(sonnet.get("missing", [])))
    set_verdict(r, raw_verdict, design["design_id"])
    apply_rescore(r, rs.get("sonnet"))
    rows.append(r)
    if haiku:
        h = mkrow(design_id=design["design_id"], label=design.get("label"), arm=tag + "h", arm_label=(design.get("label") or "") + " (Haiku)",
                  stratum="haiku", role="test", n_completed=haiku.get("n_completed"), BLK=haiku.get("BLK"), A_mean=haiku.get("A"),
                  R_LOOP=ratio(haiku.get("A"), A_BASE), growth_mean_pct=haiku.get("growth"), loop_pass=haiku.get("loop_pass"),
                  rule=rule, source=sonnet.get("source"), missing_keys=list(haiku.get("missing", [])))
        h["notes"].append(f"reported HR {haiku.get('HR')}; R_LOOP_H {haiku.get('R_LOOP_H')}; fail_rate {haiku.get('fail_rate')}")
        set_verdict(h, raw_verdict, design["design_id"])
        h["verdict_raw"] = f"{raw_verdict}; haiku state {haiku.get('state')}"
        apply_rescore(h, rs.get("haiku"))
        rows.append(h)
    return rows


def _missing_metrics(design, fname="metrics.json"):
    return [_pending_row(design, fname, n_planned=6)]


def adapt_p12_ab1(design):
    p = pathlib.Path(design["path"]) / "metrics.json"
    m = load_json(p)
    if not isinstance(m, dict):
        return _missing_metrics(design)
    register_source(design["design_id"], p)
    miss = []
    s = m.get("sonnet") or {}
    g = lambda k: pick(m, ["sonnet", k], miss)
    n_c = g("n_completed")
    sonnet = {"n_planned": pick(m, ["sonnet", "n_runs"], miss), "n_completed": n_c, "BLK": g("BLK_T"), "A": g("LOOP_T"),
              "R_LOOP": g("R_LOOP"), "B": g("TOK_T"), "R_B": g("R_B"), "growth": frac_to_pct(g("growth")),
              "loop_pass": None if g("loop_pass") is None else f"{g('loop_pass')}/{n_c}", "missing": miss, "source": "p12/ab1/metrics.json"}
    raw = pick(m, ["sonnet", "outcome_final"], miss)
    hk = m.get("haiku") or {}
    haiku = None
    if isinstance(hk, dict) and hk.get("state") not in (None, "pending") and "BLK_TH" in hk:
        haiku = {"n_completed": hk.get("n_done"), "BLK": hk.get("BLK_TH"), "A": None, "growth": frac_to_pct(hk.get("growth")),
                 "loop_pass": None if hk.get("loop_pass") is None or hk.get("n_done") is None else f"{hk['loop_pass']}/{hk['n_done']}",
                 "HR": hk.get("HR"), "R_LOOP_H": hk.get("R_LOOP_H"), "fail_rate": hk.get("fail_rate"), "state": hk.get("state"), "missing": []}
    rows = _p12_rows(design, sonnet, haiku, raw, pick(m, ["sonnet", "rule"], miss), "b1")
    return rows


def adapt_p12_ab2(design):
    p = pathlib.Path(design["path"]) / "metrics.json"
    m = load_json(p)
    if not isinstance(m, dict):
        return _missing_metrics(design)
    register_source(design["design_id"], p)
    miss = []
    g = lambda *k: pick(m, ["stratum_sonnet", "full", *k], miss)
    n_c = g("completed")
    lp = g("loop_pass")
    sonnet = {"n_planned": pick(m, ["stratum_sonnet", "n_planned"], miss), "n_completed": n_c, "BLK": g("BLK_T"), "A": g("LOOP"),
              "R_LOOP": g("R_LOOP"), "B": g("TOK"), "R_B": g("R_B"), "growth": None,
              "loop_pass": None if lp is None else f"{lp}/{n_c}", "missing": miss, "source": "p12/ab2/metrics.json"}
    raw = pick(m, ["final_outcome"], miss)
    hk = m.get("haiku") or {}
    haiku = None
    if isinstance(hk, dict) and "BLK_TH" in hk:
        haiku = {"n_completed": hk.get("complete"), "BLK": hk.get("BLK_TH"), "A": hk.get("LOOP_TH"), "growth": frac_to_pct(hk.get("growth_pct")),
                 "loop_pass": None if hk.get("loop_pass") is None or hk.get("complete") is None else f"{hk['loop_pass']}/{hk['complete']}",
                 "HR": hk.get("HR"), "R_LOOP_H": hk.get("R_LOOP_H"), "fail_rate": hk.get("harness_failure_rate"),
                 "state": "agrees" if (hk.get("one_minus_HR") or 0) > 0 else "disagrees", "missing": []}
    return _p12_rows(design, sonnet, haiku, raw, g("fired"), "b2")


def adapt_p12_ab3(design):
    p = pathlib.Path(design["path"]) / "metrics.json"
    m = load_json(p)
    if not isinstance(m, dict):
        return _missing_metrics(design)
    register_source(design["design_id"], p)
    miss = []
    nums = pick(m, ["sonnet", "numbers"], miss) or {}
    g = lambda k: pick(m, ["sonnet", "numbers", k], miss) if isinstance(nums, dict) and nums else None
    sonnet = {"n_planned": g("n_runs"), "n_completed": g("n_runs"), "BLK": g("BLK"), "A": g("LOOP"), "R_LOOP": g("R_LOOP"), "B": g("TOK"),
              "R_B": g("R_B"), "growth": frac_to_pct(g("growth")),
              "loop_pass": None if g("final_pass") is None else f"{g('final_pass')}/{g('n_runs')}", "missing": miss, "source": "p12/ab3/metrics.json"}
    raw = pick(m, ["sonnet", "final_outcome"], miss)
    hk = m.get("haiku") or {}
    hn = hk.get("numbers") if isinstance(hk, dict) else None
    haiku = None
    if isinstance(hn, dict) and hn.get("n_runs"):
        hr = (hk.get("result") or {})
        haiku = {"n_completed": hn.get("n_runs"), "BLK": hn.get("BLK"), "A": hn.get("LOOP"), "growth": frac_to_pct(hn.get("growth")),
                 "loop_pass": f"{hn.get('final_pass')}/{hn.get('n_runs')}", "HR": hr.get("HR"), "R_LOOP_H": hr.get("R_LOOP_H"),
                 "fail_rate": hr.get("harness_failure_rate"), "state": "agrees" if hr.get("agrees") else "disagrees", "missing": []}
    return _p12_rows(design, sonnet, haiku, raw, pick(m, ["sonnet", "note"], miss), "b3")


# ---------------------------------------------------------------- p13 designs
def _snapshot(tree):
    """{relative path: mtime_ns} of a tree, excluding __pycache__ and the live `runs/` subtree."""
    tree = pathlib.Path(tree)
    out = {}
    for root, dirs, files in os.walk(tree):
        dirs[:] = [d for d in dirs if d != "__pycache__" and not (pathlib.Path(root) == tree and d == "runs")]
        for f in files:
            fp = pathlib.Path(root) / f
            try:
                out[str(fp.relative_to(tree))] = fp.stat().st_mtime_ns
            except OSError:
                pass
    return out


def run_compute_results(path, timeout=120):
    """`cd <path> && uv run --no-project python -c "import json,harness; print(json.dumps(harness.compute_results(), default=str))"`.
    Returns (dict | None, changed_files list).  Output is discarded and None returned if the tree changed (side-effect guard)."""
    before = _snapshot(path)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    data = None
    try:
        p = subprocess.run(["uv", "run", "--no-project", "python", "-c",
                            "import json,harness; print(json.dumps(harness.compute_results(), default=str))"],
                           cwd=str(path), capture_output=True, text=True, timeout=timeout, env=env)
        if p.returncode == 0 and p.stdout.strip():
            data = json.loads(p.stdout.strip().splitlines()[-1])
    except (subprocess.TimeoutExpired, OSError, ValueError):
        data = None
    after = _snapshot(path)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    if changed:
        return None, changed
    return data, []


def _results_md_decision(path):
    p = pathlib.Path(path) / "RESULTS.md"
    if not p.exists():
        return None
    m = re.search(r"^DECISION:\s*(.+)$", p.read_text(errors="ignore"), re.M)
    return m.group(1).strip() if m else None


def adapt_p13_ab1(design, runner=run_compute_results):
    path = pathlib.Path(design["path"])
    res, changed = runner(path)
    rs = rescore_runs(path / "runs")
    if changed:
        warn("p13_ab1 compute_results modified files")
        print("WARN p13_ab1 compute_results modified files")
    if res is None:
        dec = _results_md_decision(path)
        if dec is None and not rs:
            row = _pending_row(design, "compute_results()/RESULTS.md", n_planned=6)
            row["source"] = "RESULTS.md (compute_results unavailable)"
            return [row]
        row = mkrow(design_id=design["design_id"], label=design.get("label"), arm="b1", arm_label=design.get("label"), stratum="sonnet",
                    role="test", n_planned=6, n_completed=(rs.get("sonnet") or {}).get("n", 0), source="RESULTS.md",
                    missing_keys=["compute_results()"])
        set_verdict(row, dec or "PENDING", design["design_id"])
        row["notes"].append("source=RESULTS.md; numbers from uniform rescoring only")
        apply_rescore(row, rs.get("sonnet"))
        return [row]
    register_source(design["design_id"], path / "harness.py")
    miss = []
    g = lambda *k: pick(res, ["sonnet", "stats", *k], miss)
    son = res.get("sonnet") or {}
    st = son.get("stats")
    n_c = g("completed") if st else 0
    pt = g("PASS_T") if st else None
    row = mkrow(design_id=design["design_id"], label=design.get("label"), arm="b1", arm_label=design.get("label"), stratum="sonnet",
                role="test", n_planned=6, n_completed=n_c, BLK=g("BLK_T") if st else None,
                A_mean=g("tokens", "A") if st else None, R_LOOP=g("R_LOOP") if st else None,
                B_mean=g("tokens", "B") if st else None, R_B=g("R_B") if st else None,
                growth_mean_pct=frac_to_pct(g("GROWTH_T")) if st else None,
                loop_pass=None if pt is None or not n_c else f"{round(pt * n_c)}/{n_c}",
                rule="; ".join((son.get("class") or {}).get("reasons") or []), source="compute_results()",
                missing_keys=miss if st else [])
    if st and (g("tokens", "AUD") or 0) == 0:
        row["notes"].append("audit tokens missing/zero: R_B is loop-only and not comparable")
    if (son.get("class") or {}).get("cost_hold"):
        row["notes"].append("COST-HOLD")
    set_verdict(row, res.get("final"), design["design_id"])
    apply_rescore(row, rs.get("sonnet"))
    rows = [row]
    hk = res.get("haiku") or {}
    if isinstance(hk.get("stats"), dict):
        hs = hk["stats"]
        h = mkrow(design_id=design["design_id"], label=design.get("label"), arm="b1h", arm_label=(design.get("label") or "") + " (Haiku)",
                  stratum="haiku", role="test", n_planned=4, n_completed=hs.get("completed"), BLK=hs.get("BLK_T"),
                  A_mean=(hs.get("tokens") or {}).get("A"), R_LOOP=ratio((hs.get("tokens") or {}).get("A"), A_BASE),
                  growth_mean_pct=frac_to_pct(hs.get("GROWTH_T")), source="compute_results()")
        h["notes"].append("gate " + json.dumps(hk.get("gate"), default=str))
        set_verdict(h, res.get("final"), design["design_id"])
        apply_rescore(h, rs.get("haiku"))
        rows.append(h)
    return rows


def adapt_p13_ab2(design):
    path = pathlib.Path(design["path"])
    p = path / "results.json"
    m = load_json(p)
    if not isinstance(m, dict):
        return _missing_metrics(design, "results.json")
    register_source(design["design_id"], p)
    miss = []
    g = lambda k: pick(m, ["summary", k], miss)
    n_c = g("n_completed")
    pt = g("PASS_T")
    loop, oa = g("loop_tokens"), g("one_audit_tokens")
    rs = rescore_runs(path / "runs")
    row = mkrow(design_id=design["design_id"], label=design.get("label"), arm="l2", arm_label=design.get("label"), stratum="sonnet",
                role="test", n_planned=g("n_planned"), n_completed=n_c, BLK=g("BLK_T"), AUD1=g("AUD_mean"), AUD2=g("AUD2_mean"),
                A_mean=loop, R_LOOP=g("R_LOOP"), B_mean=None if loop is None or oa is None else loop + oa, R_B=g("R_B"),
                growth_mean_pct=g("GROWTH_T"), loop_pass=None if pt is None or not n_c else f"{round(pt * n_c)}/{n_c}",
                rule="; ".join(pick(m, ["reasons"], miss) or []), source="p13/ab2/results.json", missing_keys=miss,
                extension_used=bool(m.get("extension_used")))
    set_verdict(row, pick(m, ["decision"], miss), design["design_id"])
    keep_aud = (row["AUD1"], row["AUD2"])
    apply_rescore(row, rs.get("sonnet"))
    if row["AUD1"] is None:
        row["AUD1"], row["AUD2"] = keep_aud
    rows = [row]
    hk = m.get("haiku") or {}
    if isinstance(hk, dict) and hk.get("mean_blocking") is not None:
        h = mkrow(design_id=design["design_id"], label=design.get("label"), arm="l2h", arm_label=(design.get("label") or "") + " (Haiku)",
                  stratum="haiku", role="test", n_planned=hk.get("n_planned"), n_completed=hk.get("n_completed"),
                  BLK=hk.get("mean_blocking"), source="p13/ab2/results.json")
        h["notes"].append(f"status {hk.get('status')}, relative_reduction {hk.get('relative_reduction')}, failure_rate {hk.get('failure_rate')}")
        set_verdict(h, pick(m, ["decision"], miss), design["design_id"])
        apply_rescore(h, rs.get("haiku"))
        rows.append(h)
    return rows


def adapt_p13_ab3(design):
    path = pathlib.Path(design["path"])
    gate = load_json(path / "gate.json")
    dec = _results_md_decision(path)
    register_source(design["design_id"], path / "gate.json")
    if not isinstance(gate, dict):
        return [_pending_row(design, "gate.json", stratum="offline", role="offline-gate")]
    runs_exist = any((path / "runs").glob("*/state.json")) if (path / "runs").is_dir() else False
    f1 = gate.get("F1")
    row = mkrow(design_id=design["design_id"], label=design.get("label"), arm="c3", arm_label=design.get("label"),
                stratum="offline", role="offline-gate", n_planned=0, n_completed=0, source="p13/ab3/gate.json")
    if gate.get("pass") is False and not runs_exist:
        set_verdict(row, "NO-GO-OFFLINE", design["design_id"])
        row["rule"] = "gate: F1 " + str(f1)
        row["notes"].append(f"RESULTS.md: {dec}")
    elif gate.get("pass") is True and not runs_exist:
        set_verdict(row, "PENDING", design["design_id"])
        row["rule"] = "gate passed; live not run"
    else:
        row["stratum"], row["role"] = "sonnet", "test"
        set_verdict(row, dec or "PENDING", design["design_id"])
        row["rule"] = "gate: F1 " + str(f1)
        apply_rescore(row, rescore_runs(path / "runs").get("sonnet"))
    return [row]


# ---------------------------------------------------------------- p15 (auto-discovered)
P15_SCHEMA = "p15-results/1"
P15_METRICS = ["BLK", "AUD1", "AUD2", "A_mean", "A_median", "R_LOOP", "B_mean", "R_B", "growth_mean_pct", "growth_median_pct",
               "loop_pass", "escalations", "reviews_mean", "fix_cycles_mean"]


def p15_schema_errors(res):
    errs = []
    for k in ("schema", "experiment", "design_id", "stage", "status", "rows"):
        if k not in res:
            errs.append(f"missing {k}")
    for i, r in enumerate(res.get("rows") or []):
        for k in ("arm", "stratum", "role", "verdict", "metrics"):
            if k not in r:
                errs.append(f"rows[{i}] missing {k}")
        for k in P15_METRICS:
            if k not in (r.get("metrics") or {}):
                errs.append(f"rows[{i}].metrics missing {k}")
        if normalize_verdict(r.get("verdict"))[0] == "UNMAPPED":
            errs.append(f"rows[{i}] unmapped verdict {r.get('verdict')!r}")
    return errs


def adapt_p15(results_json, path=None):
    res = load_json(results_json) if isinstance(results_json, (str, os.PathLike)) else results_json
    if not isinstance(res, dict) or res.get("schema") != P15_SCHEMA:
        return []
    did = res.get("design_id") or res.get("experiment")
    if path:
        register_source(did, path)
    for b in res.get("blocked_downstream") or []:
        BLOCKED.append({"from": res.get("experiment"), **b})
    rows = []
    for r in res.get("rows") or []:
        m = r.get("metrics") or {}
        hk = r.get("haiku") or {}
        jev = r.get("jev") or {}
        runs_dir = r.get("runs_dir")
        rs = rescore_runs(runs_dir, arm=r.get("arm")) if runs_dir and r.get("stratum") in ("sonnet", "haiku") else {}
        row = mkrow(design_id=did, label=res.get("label") or res.get("experiment"), arm=r.get("arm"), arm_label=r.get("arm_label"),
                    stratum=r.get("stratum"), role=r.get("role"), n_planned=r.get("n_planned"), n_completed=r.get("n_completed"),
                    BLK=m.get("BLK"), AUD1=m.get("AUD1"), AUD2=m.get("AUD2"), A_mean=m.get("A_mean"), R_LOOP=m.get("R_LOOP"),
                    B_mean=m.get("B_mean"), R_B=m.get("R_B"), growth_mean_pct=m.get("growth_mean_pct"), loop_pass=m.get("loop_pass"),
                    escalations=m.get("escalations"), reviews_mean=m.get("reviews_mean"), HR=hk.get("HR"),
                    jev_input_tokens=jev.get("input_tokens"), jev_usd=jev.get("usd"), rule=r.get("rule"),
                    extension_used=bool(r.get("extension_used")), source=f"{res.get('experiment')}/results.json",
                    missing_keys=[k for k in P15_METRICS if k not in m])
        set_verdict(row, r.get("verdict"), did)
        stage_rs = rs.get(r.get("stratum"))
        apply_rescore(row, stage_rs)
        if row["BLK_reported"] is None:
            row["BLK_reported"] = m.get("BLK")
        if r.get("design_metrics"):
            row["notes"].append("design_metrics: " + json.dumps(r["design_metrics"], default=str)[:300])
        rows.append(row)
    return rows


def discover_p15(sp):
    out = []
    for p in sorted(pathlib.Path(sp).glob("p15/*/results.json")):
        res = load_json(p)
        if isinstance(res, dict) and res.get("schema") == P15_SCHEMA:
            out.append((p, res))
    return out


# ---------------------------------------------------------------- assemble
ADAPTERS = {"baseline_sonnet": adapt_baseline_sonnet, "baseline_haiku": adapt_baseline_haiku, "p12_ab1": adapt_p12_ab1,
            "p12_ab2": adapt_p12_ab2, "p12_ab3": adapt_p12_ab3, "p13_ab1": adapt_p13_ab1, "p13_ab2": adapt_p13_ab2,
            "p13_ab3": adapt_p13_ab3}
ORDER = {"baseline": 0, "control": 1, "test": 2, "offline-gate": 3}


def build(sp=SP, designs_path=None, adapters=None):
    """-> (matrix dict, errors list).  Resets the module-level WARNINGS/SOURCES/BLOCKED."""
    WARNINGS.clear(); SOURCES.clear(); BLOCKED.clear()
    errors = []
    adapters = adapters or ADAPTERS
    designs = json.load(open(designs_path or CENTRAL / "designs.json"))
    register_source("central", CENTRAL / "score_themes.py")
    if sha256_file(CENTRAL / "score_themes.py") != SCORE_THEMES_SHA:
        warn("score_themes.py differs from the recorded sha256 (not the byte copy of p12/ab2)")
    rows = []
    for d in designs:
        fn = adapters.get(d["adapter"])
        if fn is None:
            warn(f"unknown adapter {d['adapter']} for {d['design_id']}")
            continue
        try:
            rows += fn(d)
        except Exception as e:  # one broken source must not hide the others
            errors.append(f"{d['design_id']}: adapter error {type(e).__name__}: {e}")
            warn(f"{d['design_id']}: adapter error {type(e).__name__}: {e}")
    for p, res in discover_p15(sp):
        errs = p15_schema_errors(res)
        if errs:
            errors += [f"{p}: {e}" for e in errs]
            for e in errs:
                warn(f"{p}: {e}")
            continue
        rows += adapt_p15(res, p)
    # Haiku rows: HR = row BLK / Haiku-baseline BLK
    hb = next((r["BLK"] for r in rows if r["design_id"] == "p14-haiku-a3" and r["role"] == "baseline"), None)
    for r in rows:
        if r["stratum"] == "haiku" and r["role"] != "baseline":
            if hb and r["BLK"] is not None:
                reported = r["HR"]
                r["HR"] = r["BLK"] / hb
                if reported is not None and abs(reported - r["HR"]) > 0.01:
                    r["notes"].append(f"reported HR {reported:.2f}")
            r["provisional"] = bool(r["provisional"]) or any(x["provisional"] for x in rows if x["design_id"] == "p14-haiku-a3")
    rows.sort(key=lambda r: (ORDER.get(r["role"], 9) if r["role"] == "baseline" else 5, r["design_id"], str(r["arm"])))
    matrix = {"schema": "central-matrix/1", "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
              "sources": list(SOURCES), "rows": rows, "blocked_downstream": list(BLOCKED), "warnings": list(WARNINGS)}
    return matrix, errors


# ---------------------------------------------------------------- rendering
def _f(x, nd=2):
    if x is None:
        return "-"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return f"{x:,.{nd}f}"
    if isinstance(x, int):
        return f"{x:,}"
    return str(x)


def render_md(rows, generated=None, blocked=None, warnings=None) -> str:
    L = ["# CENTRAL MATRIX", "", f"Generated {generated or datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}", "",
         "Conventions: BLK = mean blocking findings per frozen Sonnet audit, two audits per final spec, rescored uniformly; "
         "A = loop-only output tokens, each message id once; R_LOOP = A/100,424 decides cost; R_B = (A + one audit)/169,468 reported only; "
         "Haiku rows judged on HR vs the shared Haiku baseline, never pooled.", ""]
    hdr = ["design", "arm", "role", "n", "BLK", "AUD1", "AUD2", "A", "R_LOOP", "R_B", "growth%", "pass", "rev", "HR", "verdict", "flags"]

    def line(r):
        flags = []
        if r.get("haiku_pending"):
            flags.append("haiku-pending")
        if r.get("provisional"):
            flags.append("provisional")
        if r.get("blk_mismatch"):
            flags.append(f"blk-mismatch(rep {_f(r.get('BLK_reported'))})")
        if r.get("extension_used"):
            flags.append("extended")
        if r.get("missing_keys"):
            flags.append("missing:" + ",".join(r["missing_keys"])[:60])
        n = f"{_f(r.get('n_completed'))}/{_f(r.get('n_planned'))}"
        cells = [r["design_id"], r["arm"] or "", r["role"] or "", n, _f(r["BLK"]), _f(r["AUD1"]), _f(r["AUD2"]), _f(r["A_mean"], 0),
                 _f(r["R_LOOP"]), _f(r["R_B"]), _f(r["growth_mean_pct"]), _f(r["loop_pass"]), _f(r["reviews_mean"]), _f(r["HR"]),
                 r["verdict"] or "", ", ".join(flags)]
        return "| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |"

    for title, st in (("Sonnet stratum", "sonnet"), ("Haiku stratum", "haiku"), ("Offline gates", "offline")):
        sel = [r for r in rows if r["stratum"] == st]
        L += [f"## {title}", ""]
        if not sel:
            L += ["(no rows)", ""]
            continue
        L += ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
        L += [line(r) for r in sel]
        rules = [f"- {r['design_id']} {r['arm']}: {r['rule']}" for r in sel if r.get("rule")]
        L += [""] + rules + [""]
    L += ["## Blocked downstream", ""]
    L += [f"- {b.get('experiment')}: {b.get('reason')} (from {b.get('from')})" for b in (blocked or [])] or ["(none)"]
    L += ["", "## WARN", ""]
    L += [f"WARN {w}" for w in (warnings or [])] or ["(none)"]
    return "\n".join(L) + "\n"


def write_outputs(matrix, central=CENTRAL):
    central = pathlib.Path(central)
    for name, text in (("matrix.json", json.dumps(matrix, indent=1, default=str)),
                       ("MATRIX.md", render_md(matrix["rows"], matrix["generated_utc"], matrix["blocked_downstream"], matrix["warnings"]))):
        tmp = central / f".{name}.tmp{os.getpid()}"
        tmp.write_text(text)
        os.replace(tmp, central / name)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    check = "--check" in args
    matrix, errors = build()
    for w in matrix["warnings"]:
        print("WARN", w)
    if check:
        print("CHECK", "FAILED" if errors else "OK", f"rows={len(matrix['rows'])}")
        for e in errors:
            print("ERROR", e)
        return 1 if errors else 0
    write_outputs(matrix)
    print(f"matrix rows={len(matrix['rows'])} -> {CENTRAL / 'MATRIX.md'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
