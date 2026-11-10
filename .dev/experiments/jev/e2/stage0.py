"""E2 Stage 0: headroom falsifier.  No paid calls, no Jev, no workers: code only.

Per defect case (truth after labeling): extraction coverage (every evidence passage text is contained in one extracted passage),
candidate coverage (the evidence passages are connected by pairs of the pool), static coverage at 12 (connected by pairs in the
rendered static hint list).  H = defect cases covered by the pool but NOT by the static top-12 (headroom a better router could use).

Rules (decision.toml [stage0], plan 3.3):
  extraction loses any required evidence -> STOP (fix extract.py, rerun; the failed pass is logged, its data are not used)
  H == 0                                 -> NO-GO-OFFLINE (E2 live rows BLOCKED)
  H >= 1                                 -> GO-REPLAY (pool misses reported separately; > 2 -> raise pool_cap / extend prefilter, rerun)

Usage:
  uv run --no-project python stage0.py                 # uses offline/labels/truth.jsonl (after ingest_labels.py)
  uv run --no-project python stage0.py --provisional   # author evidence, NOT labels: information only, writes no results.json
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
JEV = HERE.parent / "jev"
if str(JEV) not in sys.path:
    sys.path.insert(0, str(JEV))

import candidates as C   # noqa: E402
import extract as X      # noqa: E402
import hints as Hn       # noqa: E402
import static as St      # noqa: E402

E2 = HERE
OFF = E2 / "offline"


def load_decision(path=None) -> dict:
    with open(path or (E2 / "decision.toml"), "rb") as f:
        return tomllib.load(f)


# ------------------------------------------------------------------ pure measures
def connected(pids, pair_keys) -> bool:
    """True when the pairs (restricted to the evidence passages) connect ALL evidence passages.  One pid -> trivially True."""
    pids = list(dict.fromkeys(pids))
    if len(pids) <= 1:
        return bool(pids)
    parent = {p: p for p in pids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    s = set(pids)
    for a, b in pair_keys:
        if a in s and b in s:
            parent[find(a)] = find(b)
    return len({find(p) for p in pids}) == 1


def resolve_evidence(passages, quotes):
    """-> (pids, lost): a quote is lost when no single extracted passage contains it."""
    pids, lost = [], []
    for q in quotes:
        hits = X.find_quote(passages, q)
        if not hits:
            lost.append(q)
        else:
            if hits[0].pid not in pids:
                pids.append(hits[0].pid)
    return pids, lost


def static_hint_pairs(pool, seed, budget_tokens=1200, max_pairs=12):
    ranked = St.rank(pool, seed)
    for q in ranked:
        q.reason = St.reason_for(q)
    return ranked, Hn.select(ranked, budget_tokens, max_pairs)


def measure_case(doc_text, quotes, cfg_prefilter, static_seed, budget_tokens=1200, max_pairs=12) -> dict:
    passages = X.extract(doc_text)
    pids, lost = resolve_evidence(passages, quotes)
    out = {"n_passages": len(passages), "evidence_pids": pids, "lost_quotes": lost, "extraction_ok": not lost}
    uncapped = C.prefilter_uncapped(passages, cfg_prefilter)
    pool = uncapped[: cfg_prefilter.get("pool_cap", C.DEFAULT_CFG["pool_cap"])]
    out.update({"exhaustive_pairs": C.exhaustive(passages), "admitted_pairs": len(uncapped), "pool_size": len(pool)})
    if lost:
        out.update({"pool_cover": None, "static_cover": None, "headroom": None})
        return out
    pool_keys = [q.key for q in pool]
    ranked, shown = static_hint_pairs(pool, static_seed, budget_tokens, max_pairs)
    shown_keys = [q.key for q in shown]
    all_keys = [q.key for q in uncapped]
    out["admitted_cover"] = connected(pids, all_keys)           # admitted by the prefilter rules before the cap
    out["pool_cover"] = connected(pids, pool_keys)
    out["static_cover"] = connected(pids, shown_keys)
    out["headroom"] = bool(out["pool_cover"] and not out["static_cover"])
    pos = {q.key: i + 1 for i, q in enumerate(ranked)}
    ev = set(pids)
    out["evidence_pairs_in_pool"] = [{"pair": list(k), "static_rank": pos[k], "tier": St.tier(next(q for q in pool if q.key == k))}
                                     for k in pool_keys if k[0] in ev and k[1] in ev]
    return out


def stage0_rules(m: dict) -> dict:
    """m: {"n_defect", "extraction_lost" (count of defect cases with lost evidence), "H", "pool_misses", "min_h", "miss_threshold"}"""
    if m["n_defect"] == 0:
        return {"outcome": "STOP", "verdict": "BLOCKED", "rule": "STOP-NO-CASES: no retained defect case"}
    if m["extraction_lost"] > 0:
        return {"outcome": "STOP", "verdict": "BLOCKED",
                "rule": f"STOP-EXTRACTION: {m['extraction_lost']} defect case(s) lose required evidence; fix extract.py and rerun"}
    action = ""
    if m["pool_misses"] > m["miss_threshold"]:
        action = (f" Candidate-pool misses {m['pool_misses']} > {m['miss_threshold']}: raise pool_cap or extend the prefilter "
                  "BEFORE Stage 1 and rerun Stage 0.")
    if m["H"] >= m["min_h"]:
        return {"outcome": "GO-REPLAY", "verdict": "PENDING",
                "rule": f"GO-REPLAY: H={m['H']} >= {m['min_h']} of {m['n_defect']} defect cases.{action}"}
    return {"outcome": "NO-GO-OFFLINE", "verdict": "NO-GO-OFFLINE",
            "rule": f"NO-GO-OFFLINE: H={m['H']} of {m['n_defect']} defect cases (static top-12 already covers every pooled "
                    f"must-read relation; no demonstrated Jev headroom).{action}"}


# ------------------------------------------------------------------ data
def load_cases(case_dir=None) -> list:
    d = pathlib.Path(case_dir or (OFF / "cases" / "s0"))
    return [json.loads(p.read_text()) for p in sorted(d.glob("*.json"))]


def load_truth(path=None) -> dict:
    p = pathlib.Path(path or (OFF / "labels" / "truth.jsonl"))
    if not p.exists():
        return {}
    out = {}
    for ln in p.read_text().splitlines():
        if ln.strip():
            r = json.loads(ln)
            out[r["case_id"]] = r
    return out


def provisional_truth(cases) -> dict:
    """Author intent as truth: ONLY for the information-only --provisional run."""
    return {c["case_id"]: {"case_id": c["case_id"], "defect_real": "yes" if c["author_intent"]["expect"] == "defect" else "no",
                           "evidence_sufficient": "yes", "evidence_minimal": "yes",
                           "final_evidence_quotes": c["packet"]["evidence_quotes"], "unresolved": False} for c in cases}


def read_doc(case) -> str:
    return (E2 / case["packet"]["doc"]).read_text(encoding="utf-8")


def classify(cases, truth):
    """-> defect cases, clean cases, dropped (listed), with the evidence quotes to use."""
    defect, clean, dropped = [], [], []
    for c in cases:
        t = truth.get(c["case_id"])
        if t is None:
            dropped.append({"case_id": c["case_id"], "reason": "no truth label"})
            continue
        if t.get("unresolved") or t.get("defect_real") == "undecidable":
            dropped.append({"case_id": c["case_id"], "reason": "undecidable"})
        elif t["defect_real"] == "yes" and t.get("evidence_sufficient") == "yes":
            defect.append((c, t.get("final_evidence_quotes") or c["packet"]["evidence_quotes"]))
        elif t["defect_real"] == "yes":
            dropped.append({"case_id": c["case_id"], "reason": "defect real but evidence set insufficient and not corrected"})
        else:
            if c["author_intent"]["expect"] == "defect":
                dropped.append({"case_id": c["case_id"], "reason": "labelers judged the proposed defect not blocking/real"})
            clean.append(c)
    return defect, clean, dropped


def run(cases, truth, dec, provisional=False) -> dict:
    pf = dec["prefilter"]
    seed = dec["static"]["seed"]
    hb, hm = dec["hints"]["budget_tokens"], dec["hints"]["max_pairs"]
    defect, clean, dropped = classify(cases, truth)
    rows = []
    for c, quotes in defect:
        m = measure_case(read_doc(c), quotes, pf, seed, hb, hm)
        rows.append({"case_id": c["case_id"], "category": c["category"], "layer": c["author_intent"]["layer"],
                     "quotes_used": quotes, **m})
    clean_rows = []
    for c in clean:
        text = read_doc(c)
        ps = X.extract(text)
        unc = C.prefilter_uncapped(ps, pf)
        clean_rows.append({"case_id": c["case_id"], "category": c["category"], "n_passages": len(ps),
                           "admitted_pairs": len(unc), "pool_size": min(len(unc), pf["pool_cap"])})
    lost = [r for r in rows if not r["extraction_ok"]]
    ok = [r for r in rows if r["extraction_ok"]]
    H = sum(1 for r in ok if r["headroom"])
    pool_miss = [r for r in ok if not r["pool_cover"]]
    rules = stage0_rules({"n_defect": len(rows), "extraction_lost": len(lost), "H": H, "pool_misses": len(pool_miss),
                          "min_h": dec["stage0"]["min_h_for_go"], "miss_threshold": dec["stage0"]["pool_miss_action_threshold"]})
    return {"rows": rows, "clean_rows": clean_rows, "dropped": dropped, "H": H, "n_defect": len(rows), "n_clean": len(clean_rows),
            "extraction_lost": len(lost), "pool_misses": len(pool_miss),
            "admitted_misses": sum(1 for r in ok if not r.get("admitted_cover")),
            "extraction_coverage": f"{len(ok)}/{len(rows)}",
            "candidate_coverage": f"{sum(1 for r in ok if r['pool_cover'])}/{len(ok)}",
            "static_coverage": f"{sum(1 for r in ok if r['static_cover'])}/{len(ok)}",
            "provisional": provisional, **rules}


# ------------------------------------------------------------------ outputs
def render_md(res: dict, dec: dict, passes: list) -> str:
    L = []
    tag = "PROVISIONAL (author evidence, no labels; information only)" if res["provisional"] else "FINAL (labeled truth)"
    L += [f"# E2 Stage 0 headroom falsifier: {res['outcome']}  [{tag}]", "",
          f"Rule fired: {res['rule']}", "",
          f"- defect cases measured: {res['n_defect']}; clean cases: {res['n_clean']}; dropped/undecidable: {len(res['dropped'])}",
          f"- extraction coverage: {res['extraction_coverage']}",
          f"- candidate coverage (pool, pool_cap={dec['prefilter']['pool_cap']}): {res['candidate_coverage']}; "
          f"admitted-before-cap misses: {res['admitted_misses']}",
          f"- static coverage at {dec['hints']['max_pairs']} pairs / {dec['hints']['budget_tokens']} tokens: {res['static_coverage']}",
          f"- H (pooled but not in static top-{dec['hints']['max_pairs']}): {res['H']}",
          f"- candidate-pool misses (hurt every router equally, reported separately): {res['pool_misses']}", "",
          "## Per defect case", "",
          "| case | layer | category | passages | exhaustive | admitted | pool | evidence | extract | pool cover | static cover | H |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["rows"]:
        L.append(f"| {r['case_id']} | {r['layer']} | {r['category']} | {r['n_passages']} | {r['exhaustive_pairs']} | "
                 f"{r['admitted_pairs']} | {r['pool_size']} | {','.join(r['evidence_pids'])} | {r['extraction_ok']} | "
                 f"{r.get('pool_cover')} | {r.get('static_cover')} | {r.get('headroom')} |")
    L += ["", "## Static ranks of the evidence pairs that are in the pool", ""]
    for r in res["rows"]:
        for e in r.get("evidence_pairs_in_pool", []):
            L.append(f"- {r['case_id']} {e['pair'][0]}-{e['pair'][1]}: static rank {e['static_rank']} (tier {e['tier']})")
    L += ["", "## Clean controls (no defect; pool size only)", ""]
    for r in res["clean_rows"]:
        L.append(f"- {r['case_id']} {r['category']}: {r['n_passages']} passages, {r['admitted_pairs']} admitted pairs, pool {r['pool_size']}")
    if res["dropped"]:
        L += ["", "## Dropped cases (listed)", ""]
        L += [f"- {d['case_id']}: {d['reason']}" for d in res["dropped"]]
    L += ["", "## Passes", ""]
    L += [f"- pass {p['pass']} {p['ts_utc']} {p['mode']}: {p['outcome']} (H={p.get('H')}, extraction_lost={p.get('extraction_lost')})"
          for p in passes]
    return "\n".join(L) + "\n"


def _passes_path():
    return OFF / "stage0-passes.jsonl"


def log_pass(res: dict, mode: str) -> list:
    p = _passes_path()
    prev = [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []
    rec = {"pass": len(prev) + 1, "ts_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "mode": mode, "outcome": res["outcome"], "H": res["H"], "extraction_lost": res["extraction_lost"],
           "n_defect": res["n_defect"], "pool_misses": res["pool_misses"]}
    with open(p, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return prev + [rec]


def results_payload(res: dict, dec_path: pathlib.Path) -> dict:
    sha = hashlib.sha256(pathlib.Path(dec_path).read_bytes()).hexdigest()
    zero = {"BLK": None, "AUD1": None, "AUD2": None, "A_mean": None, "A_median": None, "R_LOOP": None, "B_mean": None, "R_B": None,
            "growth_mean_pct": None, "growth_median_pct": None, "loop_pass": None, "escalations": None, "reviews_mean": None,
            "fix_cycles_mean": None}
    jev0 = {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0, "model": "jev-1.14.0"}
    go = res["outcome"] == "GO-REPLAY"
    live_verdict = "PENDING" if go else "BLOCKED"
    live_rule = ("Stage 0 passed; Stage 1 replay (Session 2) and GO-LIVE gate not yet run" if go
                 else f"Stage 0 {res['outcome']}: " + res["rule"])
    gate = {"arm": "E2-stage0", "arm_label": "Stage 0 headroom falsifier (static top-12 vs pooled must-read relations)",
            "stratum": "offline", "role": "offline-gate", "n_planned": 24, "n_completed": res["n_defect"] + res["n_clean"],
            "runs_dir": str(E2 / "offline"), "metrics": dict(zero),
            "design_metrics": {"H": res["H"], "n_defect_cases": res["n_defect"], "n_clean_cases": res["n_clean"],
                               "extraction_coverage": res["extraction_coverage"], "candidate_coverage": res["candidate_coverage"],
                               "static_coverage": res["static_coverage"], "candidate_pool_misses": res["pool_misses"],
                               "dropped": [d["case_id"] for d in res["dropped"]], "outcome": res["outcome"]},
            "haiku": None, "jev": jev0, "verdict": res["verdict"], "rule": res["rule"], "extension_used": False}
    rows = [gate]
    for arm, label, stratum, role in (("h2j", "Jev hints (first review)", "sonnet", "test"),
                                      ("h2s", "static hints (first review)", "sonnet", "control"),
                                      ("h2r", "conventional router hints (first review)", "sonnet", "control")):
        rows.append({"arm": arm, "arm_label": label, "stratum": stratum, "role": role, "n_planned": 6, "n_completed": 0,
                     "runs_dir": str(E2 / "runs"), "metrics": dict(zero), "design_metrics": {}, "haiku": None, "jev": dict(jev0),
                     "verdict": live_verdict, "rule": live_rule, "extension_used": False})
    return {"schema": "p15-results/1", "experiment": "E2", "design_id": "p15-E2",
            "decision_file": {"path": str(dec_path), "sha256": sha}, "stage": "offline", "status": "partial",
            "rows": rows, "blocked_downstream": [] if go else [{"experiment": "E2-live", "reason": "Stage 0 " + res["outcome"]}],
            "notes": ["Stage 0 uses no paid calls, no Jev, no workers beyond the labelers of the 24 cases."]}


def init_payload(dec_path: pathlib.Path) -> dict:
    """Placeholder results (Stage 0 not yet run): gate row PENDING so the central matrix lists E2 from Session 1 on."""
    res = {"rule": "Stage 0 not yet run: labelers and stage0.py are the coordinator's next steps", "verdict": "PENDING",
           "outcome": "NOT-RUN", "H": None, "n_defect": 0, "n_clean": 0, "extraction_coverage": None, "candidate_coverage": None,
           "static_coverage": None, "pool_misses": None, "dropped": []}
    p = results_payload(res, dec_path)
    p["status"] = "not-run"
    for r in p["rows"][1:]:
        r["verdict"] = "PENDING"
        r["rule"] = "waiting for the Stage 0 gate"
    p["blocked_downstream"] = []
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provisional", action="store_true", help="author evidence instead of labels; information only")
    ap.add_argument("--pool-cap", type=int, default=None, help="sensitivity run: only with --provisional")
    ap.add_argument("--init", action="store_true", help="write the not-run placeholder results.json and update the matrix")
    ap.add_argument("--no-matrix", action="store_true")
    a = ap.parse_args(argv)
    dec_path = E2 / "decision.toml"
    dec = load_decision(dec_path)
    from p15common import analysis  # noqa: E402
    if a.init:
        analysis.write_results(E2 / "results.json", init_payload(dec_path))
        if not a.no_matrix:
            analysis.update_matrix()
        print("wrote placeholder results.json (Stage 0 not run)")
        return 0
    if a.pool_cap is not None:
        if not a.provisional:
            print("ERROR --pool-cap is for information-only --provisional runs; the final pool_cap lives in decision.toml")
            return 2
        dec["prefilter"]["pool_cap"] = a.pool_cap
    cases = load_cases()
    if a.provisional:
        truth = provisional_truth(cases)
    else:
        truth = load_truth()
        if not truth:
            print("ERROR no labeled truth at offline/labels/truth.jsonl (run the labelers and ingest_labels.py first); "
                  "use --provisional for an information-only pass")
            return 5
    res = run(cases, truth, dec, provisional=a.provisional)
    passes = [] if a.provisional else log_pass(res, "final")
    md = render_md(res, dec, passes)
    suffix = f"-cap{a.pool_cap}" if a.pool_cap is not None else ""
    outp = OFF / (f"stage0-provisional{suffix}.md" if a.provisional else "stage0-results.md")
    if res["outcome"] == "STOP":
        failp = OFF / f"stage0-failed-pass-{len(passes) or 0}.md"
        failp.write_text(md)
        print(f"STOP {res['rule']} (report of the failed pass: {failp}; no data from it is used)")
        return 4
    outp.write_text(md)
    if not a.provisional:
        analysis.write_results(E2 / "results.json", results_payload(res, dec_path))
        if not a.no_matrix:
            analysis.update_matrix()
    print(res["outcome"], "|", res["rule"])
    print(f"H={res['H']} n_defect={res['n_defect']} extraction={res['extraction_coverage']} pool={res['candidate_coverage']} "
          f"static={res['static_coverage']} pool_misses={res['pool_misses']}  report: {outp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
