"""E5 session 1: zero-call headroom analysis. Writes offline/headroom.{md,json}, packets.json and results.json."""
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tomllib

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import labels_from_audits as la  # noqa: E402
import packets as pk  # noqa: E402

SP = pk.SP
CENTRAL = SP / "central"
JEV = SP / "p15" / "jev"
REASONS = ("cap", "open_blocker", "unchanged_hash", "mandatory_policy")
METRIC_KEYS = ["BLK", "AUD1", "AUD2", "A_mean", "A_median", "R_LOOP", "B_mean", "R_B", "growth_mean_pct", "growth_median_pct",
               "loop_pass", "escalations", "reviews_mean", "fix_cycles_mean"]


def load_decision(path=HERE / "decision.toml"):
    with open(path, "rb") as f:
        return tomllib.load(f)


def code_determined_reason(p):
    """First code-fixed reason for the packet, or None when the action is a real routing choice."""
    if p["slots_remaining"] == 0:
        return "cap"
    if p["open_blockers"] > 0:
        return "open_blocker"
    if not p["changed_since_last_whole_review"]:
        return "unchanged_hash"
    if p.get("mandatory_policy"):
        return "mandatory_policy"
    return None


def classify(p, lab):
    """Attach reason / eligibility / routes. Static route: assurance review whenever a slot remains."""
    reason = code_determined_reason(p)
    eligible = reason is None
    r = dict(p, **{k: lab[k] for k in ("label", "sens_label", "n_audits", "single_audit")})
    r["audits"] = lab.get("audits", [])
    r["fail_unparsed"] = lab.get("fail_unparsed", 0)
    r["code_determined"] = reason
    r["eligible"] = eligible
    r["labeled"] = lab["label"] != "unlabeled"
    r["static_route"] = "assurance" if p["slots_remaining"] > 0 else "deliver"
    r["min_route"] = None if not (eligible and r["labeled"]) else ("assurance" if lab["label"] == "yes" else "deliver")
    r["headroom"] = bool(eligible and lab["label"] == "no")
    r["sens_headroom"] = bool(eligible and lab["sens_label"] == "no")
    return r


def summarize(rows):
    el = [r for r in rows if r["eligible"] and r["labeled"]]
    by = {k: sum(1 for r in rows if r["code_determined"] == k) for k in REASONS}
    return {
        "packets": len(rows), "eligible": len(el), "code_determined_by_reason": by,
        "needs_assurance_yes": sum(1 for r in el if r["label"] == "yes"),
        "needs_assurance_rate": (sum(1 for r in el if r["label"] == "yes") / len(el)) if el else None,
        "headroom": sum(1 for r in el if r["headroom"]),
        "sensitivity_headroom": sum(1 for r in el if r["sens_headroom"]),
        "unlabeled_eligible": sum(1 for r in rows if r["eligible"] and not r["labeled"]),
        "single_audit_eligible": sum(1 for r in el if r["single_audit"]),
    }


def zero_call_rule(s, dec):
    """Pre-registered rule on the decisive (frozen baseline) stratum summary."""
    zc = dec["zero_call"]
    h, e = s["headroom"], s["eligible"]
    frac = (h / e) if e else 0.0
    pct = f"{100 * frac:.1f}%"
    fired = []
    if h < zc["min_headroom_packets"]:
        fired.append(f"< {zc['min_headroom_packets']} packets")
    if frac < zc["min_headroom_fraction"]:
        fired.append(f"< {zc['min_headroom_fraction']:.2f}")
    if fired:
        return "NO-GO-OFFLINE", f"headroom {h}/{e} ({pct}) " + " or ".join(fired)
    return "HEADROOM", f"headroom {h}/{e} ({pct}) >= {zc['min_headroom_fraction']:.2f} and >= {zc['min_headroom_packets']} packets"


def build_results(summary_decisive, summary_other, verdict, rule, dec_path, generated):
    sha = hashlib.sha256(pathlib.Path(dec_path).read_bytes()).hexdigest()
    zero_missing = "zero-call headroom absent" if verdict == "NO-GO-OFFLINE" else "owner cap-neutral scope amendment missing"
    gate = {
        "arm": "E5-zero-call", "arm_label": "Evidence-sufficiency routing: zero-call headroom on frozen audits", "stratum": "offline",
        "role": "offline-gate", "n_planned": None, "n_completed": summary_decisive["packets"], "runs_dir": None,
        "metrics": {k: None for k in METRIC_KEYS},
        "design_metrics": dict(summary_decisive, other_designs=summary_other, label_rule="strict-any-audit-blocker"),
        "haiku": None, "jev": {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0, "model": "jev-1.14.0"},
        "verdict": "NO-GO-OFFLINE" if verdict == "NO-GO-OFFLINE" else "PENDING", "rule": rule, "extension_used": False,
    }
    rows = [gate]
    for arm, label, role in (("k5j", "Jev assurance router (shadow-validated)", "test"),
                             ("k5r", "Conventional assurance router", "control"),
                             ("k5s", "Static routing (assurance whenever a slot remains)", "control")):
        rows.append({
            "arm": arm, "arm_label": label, "stratum": "sonnet", "role": role, "n_planned": 6, "n_completed": 0, "runs_dir": None,
            "metrics": {k: None for k in METRIC_KEYS}, "design_metrics": {}, "haiku": None,
            "jev": {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0, "model": "jev-1.14.0"},
            "verdict": "BLOCKED", "rule": zero_missing, "extension_used": False})
    if verdict == "NO-GO-OFFLINE":
        blocked = [{"experiment": "E5 probe/replay/live", "reason": "zero-call headroom absent (" + rule + ")"}]
    else:
        blocked = [{"experiment": "E5 live", "reason": "owner cap-neutral scope amendment missing"}]
    return {"schema": "p15-results/1", "experiment": "E5", "design_id": "p15-E5", "generated_utc": generated,
            "decision_file": {"path": str(dec_path), "sha256": sha}, "stage": "offline", "status": "complete",
            "rows": rows, "blocked_downstream": blocked,
            "notes": ["Zero paid calls; labels come from the frozen Sonnet audits (strict any-audit-blocker); "
                      "other-design packets are reported, not decisive."]}


REQ_TOP = ["schema", "experiment", "design_id", "generated_utc", "decision_file", "stage", "status", "rows", "blocked_downstream", "notes"]
REQ_ROW = ["arm", "arm_label", "stratum", "role", "n_planned", "n_completed", "runs_dir", "metrics", "design_metrics", "haiku", "jev",
           "verdict", "rule", "extension_used"]
VERDICTS = {"ADOPT", "ADOPT (Haiku robustness pending)", "INCONCLUSIVE", "DROP", "NO-GO-OFFLINE", "BLOCKED", "PENDING", "CONTROL"}


def validate_results(d):
    errs = []
    for k in REQ_TOP:
        if k not in d:
            errs.append(f"missing top-level {k}")
    if d.get("schema") != "p15-results/1":
        errs.append("schema must be p15-results/1")
    if d.get("stage") not in ("offline", "live"):
        errs.append("bad stage")
    if d.get("status") not in ("complete", "partial", "not-run"):
        errs.append("bad status")
    for i, r in enumerate(d.get("rows", [])):
        for k in REQ_ROW:
            if k not in r:
                errs.append(f"row {i} missing {k}")
        if r.get("verdict") not in VERDICTS:
            errs.append(f"row {i} bad verdict {r.get('verdict')}")
        if r.get("role") not in ("baseline", "test", "control", "offline-gate"):
            errs.append(f"row {i} bad role")
        if r.get("stratum") not in ("sonnet", "haiku", "offline"):
            errs.append(f"row {i} bad stratum")
        for k in METRIC_KEYS:
            if k not in (r.get("metrics") or {}):
                errs.append(f"row {i} metrics missing {k}")
    return errs


def write_results(path, d):
    """Use the shared PLAN-0 writer when it exists; otherwise validate locally and write the contract J12.1 schema."""
    errs = validate_results(d)
    if errs:
        raise ValueError("; ".join(errs))
    pathlib.Path(path).write_text(json.dumps(d, indent=1))


def update_matrix():
    bm = CENTRAL / "build_matrix.py"
    if not bm.exists():
        return None
    try:
        return subprocess.run(["uv", "run", "--no-project", "python", str(bm)], capture_output=True, timeout=300).returncode
    except Exception as e:  # printed, never changes the verdict
        print("ERROR matrix build:", e)
        return 1


def render_md(res, rows, sd, so, verdict, rule):
    def line(s):
        return (f"packets {s['packets']}; code-determined {s['code_determined_by_reason']}; eligible {s['eligible']}; "
                f"needs_assurance yes {s['needs_assurance_yes']} (rate {s['needs_assurance_rate'] if s['needs_assurance_rate'] is None else round(s['needs_assurance_rate'], 3)}); "
                f"headroom {s['headroom']}; sensitivity headroom {s['sensitivity_headroom']}; single-audit eligible {s['single_audit_eligible']}")
    out = ["# E5 zero-call headroom", "", f"Generated {res['generated_utc']}. Verdict: **{verdict}** ({rule}).", "",
           "## Decisive stratum (frozen baseline: p11 + p14)", line(sd), "",
           "## Other designs (reported, not decisive)", line(so), "",
           f"Escalated (no provisional PASS): {len(res['escalated'])}; excluded runs: {len(res['excluded'])}.", "",
           "## Packets", "", "| run | design | stratum | k | slots | reason | audits (verdict/blockers) | label | sens | headroom |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        au = ", ".join(f"{a['verdict']}/{a['blocking']}" for a in r["audits"])
        out.append(f"| {r['run']} | {r['design']} | {r['stratum']} | {r['review_k']} | {r['slots_remaining']} | "
                   f"{r['code_determined'] or 'eligible'} | {au} | {r['label']} | {r['sens_label']} | {'yes' if r['headroom'] else 'no'} |")
    out += ["", "## Escalated runs", ""] + [f"- {e['run']} ({e['design']}, {e['stratum']}): last review {e['last_review']} = {e['last_verdict']}"
                                          for e in res["escalated"]]
    out += ["", "## Excluded runs", ""] + [f"- {e['run']} ({e['source']}): {e['reason']}" for e in res["excluded"]]
    return "\n".join(out) + "\n"


def run(sources=None, out_dir=HERE, dec_path=HERE / "decision.toml", do_matrix=True):
    dec = load_decision(dec_path)
    res = pk.enumerate_packets(sources or pk.default_sources())
    generated = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    res["generated_utc"] = generated
    off = pathlib.Path(out_dir) / "offline"
    off.mkdir(parents=True, exist_ok=True)
    (off / "packets.json").write_text(json.dumps(res, indent=1))
    rows = [classify(p, la.label_packet(p)) for p in res["packets"]]
    decisive = [r for r in rows if r["stratum"] in dec["offline"]["decisive_strata"]]
    other = [r for r in rows if r["stratum"] not in dec["offline"]["decisive_strata"]]
    sd, so = summarize(decisive), summarize(other)
    verdict, rule = zero_call_rule(sd, dec)
    (off / "headroom.json").write_text(json.dumps({"generated_utc": generated, "verdict": verdict, "rule": rule, "decisive": sd,
                                                   "other_designs": so, "rows": rows, "escalated": res["escalated"],
                                                   "excluded": res["excluded"]}, indent=1))
    (off / "headroom.md").write_text(render_md(res, rows, sd, so, verdict, rule))
    results = build_results(sd, so, verdict, rule, dec_path, generated)
    write_results(pathlib.Path(out_dir) / "results.json", results)
    mrc = update_matrix() if do_matrix else None
    return {"verdict": verdict, "rule": rule, "decisive": sd, "other": so, "escalated": len(res["escalated"]),
            "excluded": len(res["excluded"]), "matrix_rc": mrc, "rows": rows}


def main():
    r = run()
    sd, so = r["decisive"], r["other"]
    print(f"verdict={r['verdict']} rule={r['rule']}")
    print(f"decisive: {sd}")
    print(f"other: {so}")
    print(f"escalated={r['escalated']} excluded={r['excluded']} matrix_rc={r['matrix_rc']}")


if __name__ == "__main__":
    main()
