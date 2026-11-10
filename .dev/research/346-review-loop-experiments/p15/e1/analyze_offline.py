"""E1 offline analysis (plan 3.1 smoke, 3.2 held-out).  Pure metric functions + a CLI that writes offline-results.md and results.json
(contract J12) and rebuilds the central matrix.

  uv run --no-project python analyze_offline.py --phase smoke      # prints SMOKE GO | NO-GO-OFFLINE | BLOCKED
  uv run --no-project python analyze_offline.py --phase heldout    # prints E1 GO-E4 | NO-GO-OFFLINE (needs the frozen calibration)

D2: cost reduction uses the deduplicated output tokens of the conventional checker workers (each message id once), apportioned per packet
equally within its batch; Jev input tokens and USD are reported apart and never added.  D6: nothing here stops anything."""
import _boot  # noqa: F401
import argparse
import datetime
import hashlib
import json
import math
import pathlib
import re
import statistics

import policy
from p15common import analysis as A
from p15common import harnesslib as H
from questions import QSET_VERSION
import prep_offline as P
from ingest_labels import read_jsonl

E1 = _boot.E1
OFFLINE = E1 / "offline"
DECISION = E1 / "decision.toml"
YES = "yes"


# ---------------------------------------------------------------- loading
def load_truth(path=OFFLINE / "labels/truth.jsonl"):
    return {r["case_id"]: r for r in read_jsonl(path)}


def load_rows(phase, path=None):
    p = pathlib.Path(path or OFFLINE / f"replay-{phase}.jsonl")
    return read_jsonl(p)


def load_conv_answers(phase, offline=OFFLINE):
    out = {}
    for p in sorted((pathlib.Path(offline) / "sb").glob(f"CC-{phase}-b*/answers.jsonl")):
        for r in read_jsonl(p):
            if "packet_id" in r:
                out[r["packet_id"]] = r
    return out


def conv_tokens(phase, offline=OFFLINE):
    """-> {batch_id: deduplicated output tokens of the conventional checker worker} from the transcripts, or {} when not found."""
    plan_p = pathlib.Path(offline) / f"phase-{phase}.json"
    if not plan_p.exists():
        return {}
    import re as _re
    rx = _re.compile(r"^Read (?P<path>\S+) and follow")
    found = {}
    for m, info in H.scan_by_first_message(H.tasks_glob(), rx):
        found.setdefault(m.group("path"), []).append(info)
    out = {}
    plan = json.load(open(plan_p))
    for b in plan["conv_batches"]:
        pr = str(pathlib.Path(offline) / "sb" / f"CC-{phase}-{b}" / "PROMPT.md")
        c = H.pick_transcript(found.get(pr, []), "sonnet", key=f"CC-{phase}-{b}", warn=False) if found.get(pr) else None
        if c is not None:
            out[b] = c["tokens"]
    return out


# ---------------------------------------------------------------- generic metrics
def pct(xs, q):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def conventional_decisions(rows, conv, thr):
    """case_id -> conventional decision on the eligible rows (through the same table)."""
    out = {}
    for r in rows:
        if r["precheck"] == "ok" and r["case_id"] in conv:
            ans = {k: v for k, v in conv[r["case_id"]].items() if k not in ("packet_id", "quote")}
            out[r["case_id"]] = policy.conventional_decide("ok", ans, thr, r["n_deps"])
    return out


def jev_totals(rows):
    sc, tok = {}, 0
    for r in rows:
        if r["status"] != "not_called":
            sc[r["status"]] = sc.get(r["status"], 0) + 1
        tok += r.get("input_tokens") or 0
    lat = [r["latency_ms"] for r in rows if r.get("latency_ms") is not None]
    return {"logical_calls": sum(sc.values()), "status_counts": sc, "input_tokens": tok, "usd": round(tok * 0.042 / 1e6, 6),
            "model": next((r["model"] for r in rows if r.get("model")), None), "p50_ms": pct(lat, 0.5), "p95_ms": pct(lat, 0.95)}


def truth_closure(truth, cid):
    t = truth.get(cid)
    return None if t is None else t.get("closure_correct")


def smoke_metrics(rows, truth, conv=None, thr=None, tokens=None, plan=None):
    """Information and stop rules of plan 3.1."""
    thr = thr or policy.DEFAULT_THR
    decided = {c: t["closure_correct"] for c, t in truth.items() if t.get("closure_correct") in ("yes", "no")}
    eligible = [r for r in rows if r["precheck"] == "ok"]
    closes = [r for r in rows if r["decision"] == policy.AUTO_CLOSE]
    false_closures = sorted(r["case_id"] for r in closes if decided.get(r["case_id"]) == "no")
    true_closures = sorted(r["case_id"] for r in closes if decided.get(r["case_id"]) == "yes")
    unlabeled_closes = sorted(r["case_id"] for r in closes if r["case_id"] not in decided)
    calls = [r for r in rows if r["status"] != "not_called"]
    mismatch = [r["case_id"] for r in calls if r.get("error") == "model_mismatch"]
    failed = [r["case_id"] for r in calls if r["status"] in ("invalid", "unavailable")]
    fail_frac = (len(failed) / len(calls)) if calls else 0.0
    conv_dec = conventional_decisions(rows, conv or {}, thr)
    conv_false = sorted(c for c, d in conv_dec.items() if d == policy.AUTO_CLOSE and decided.get(c) == "no")
    agree = [c for c in conv_dec if (conv_dec[c] == policy.AUTO_CLOSE) == (next(r for r in rows if r["case_id"] == c)["decision"] == policy.AUTO_CLOSE)]
    # perturbation consistency per group: decisions identical across the variants of a group
    groups = {}
    for r in rows:
        groups.setdefault(r["group"], []).append(r)
    cons_exact = sum(1 for g in groups.values() if len({x["decision"] for x in g}) == 1)
    cons_class = sum(1 for g in groups.values() if len({x["decision"] == policy.AUTO_CLOSE for x in g}) == 1)
    cost = cost_reduction(rows, tokens, plan)
    return {"n_cases": len(rows), "n_truth_decided": len(decided), "eligible": len(eligible), "auto_close": len(closes),
            "automation_coverage": (len(closes) / len(eligible)) if eligible else None,
            "false_closures": false_closures, "true_closures": true_closures, "auto_close_without_truth": unlabeled_closes,
            "model_mismatch_cases": mismatch, "failed_calls": failed, "failed_frac": fail_frac, "calls": len(calls),
            "conventional_decisions": len(conv_dec), "conventional_false_closures": conv_false,
            "conventional_agreement": (len(agree) / len(conv_dec)) if conv_dec else None,
            "perturbation_groups": len(groups), "perturbation_consistent_exact": cons_exact, "perturbation_consistent_closing": cons_class,
            "decision_counts": _count(r["decision"] for r in rows), "precheck_counts": _count(r["precheck"] for r in rows),
            "cost_reduction": cost, "jev": jev_totals(rows)}


def _count(it):
    out = {}
    for x in it:
        out[x] = out.get(x, 0) + 1
    return out


def cost_reduction(rows, tokens, plan):
    """1 - (checker tokens apportioned to FALLBACK packets) / (checker tokens apportioned to all eligible packets); None without token data."""
    if not tokens or not plan:
        return None
    per = {}
    for b, ids in plan["conv_batches"].items():
        if b in tokens and ids:
            for cid in ids:
                per[cid] = tokens[b] / len(ids)
    el = [r for r in rows if r["precheck"] == "ok" and r["case_id"] in per]
    if not el:
        return None
    total = sum(per[r["case_id"]] for r in el)
    fb = sum(per[r["case_id"]] for r in el if r["decision"] != policy.AUTO_CLOSE)
    return {"reduction": (1 - fb / total) if total else None, "tokens_all_eligible": total, "tokens_fallback": fb}


def smoke_verdict(m, dec) -> tuple:
    """-> (verdict, rule) with verdict in GO | NO-GO-OFFLINE | BLOCKED.  A false AUTO_CLOSE needs an ok Jev result, so it outranks
    infrastructure trouble; model_mismatch / too many failed calls make the component unevaluable (BLOCKED)."""
    r = dec["rules"]
    if len(m["false_closures"]) >= r["smoke_false_closure_stop"]:
        return "NO-GO-OFFLINE", f"smoke STOP: false AUTO_CLOSE on {m['false_closures']} (truth closure_correct = no)"
    if m["auto_close_without_truth"]:
        return "BLOCKED", f"AUTO_CLOSE on cases without decided truth {m['auto_close_without_truth']}: labels incomplete"
    if r["smoke_blocked_on_model_mismatch"] and m["model_mismatch_cases"]:
        return "BLOCKED", f"smoke: model_mismatch on {m['model_mismatch_cases']} (pinned model not served)"
    if m["failed_frac"] > r["smoke_unavailable_max_frac"]:
        return "BLOCKED", f"smoke: {m['failed_frac']:.0%} of calls invalid/unavailable (> {r['smoke_unavailable_max_frac']:.0%})"
    return "GO", "smoke passed: no false AUTO_CLOSE, no model_mismatch, failures within bounds"


# ---------------------------------------------------------------- held-out (plan 3.2)
def brier(pairs):
    return (sum((p - y) ** 2 for p, y in pairs) / len(pairs)) if pairs else None


def reliability(pairs, bins=5):
    out = []
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        ys = [(p, y) for p, y in pairs if lo <= p < hi or (b == bins - 1 and p == 1.0)]
        out.append({"bin": [lo, hi], "n": len(ys), "mean_p": statistics.mean(p for p, _ in ys) if ys else None,
                    "freq": statistics.mean(y for _, y in ys) if ys else None})
    return out


def question_truth(truth_rec):
    """Per-question truth derived from the label fields (None when the labels do not settle it)."""
    r, o = truth_rec.get("resolved"), truth_rec.get("obligation_preserved")
    return {"defect_still_present": None if r not in ("yes", "no") else int(r == "no"),
            "obligation_still_required": None if o not in ("yes", "no", "n/a") else int(o in ("yes", "n/a"))}


def heldout_metrics(rows, truth, conv, thr, tokens, plan):
    base = smoke_metrics(rows, truth, conv, thr, tokens, plan)
    decided = {c: t["closure_correct"] for c, t in truth.items() if t.get("closure_correct") in ("yes", "no")}
    closes = [r for r in rows if r["decision"] == policy.AUTO_CLOSE]
    n = len(closes)
    true_open = [r for r in rows if decided.get(r["case_id"]) == "no"]
    conv_dec = conventional_decisions(rows, conv or {}, thr)
    # final decision of the Jev path = AUTO_CLOSE from Jev, else the conventional answer; versus the conventional checker alone
    add_false_open = 0
    for r in rows:
        if r["precheck"] != "ok" or decided.get(r["case_id"]) != "yes":
            continue
        final = policy.AUTO_CLOSE if r["decision"] == policy.AUTO_CLOSE else conv_dec.get(r["case_id"], policy.OPEN)
        if conv_dec.get(r["case_id"]) == policy.AUTO_CLOSE and final != policy.AUTO_CLOSE:
            add_false_open += 1
    nonok_close = [r["case_id"] for r in closes if r["status"] != "ok"]
    per_cat, per_stratum = {}, {}
    for r in rows:
        for key, d in ((r["category"], per_cat), (r.get("stratum", "synthetic"), per_stratum)):
            e = d.setdefault(key, {"cases": 0, "eligible": 0, "auto_close": 0, "false_closures": 0})
            e["cases"] += 1
            e["eligible"] += int(r["precheck"] == "ok")
            e["auto_close"] += int(r["decision"] == policy.AUTO_CLOSE)
            e["false_closures"] += int(r["decision"] == policy.AUTO_CLOSE and decided.get(r["case_id"]) == "no")
    q = {"defect_still_present": [], "obligation_still_required": []}
    for r in rows:
        if r.get("answers") and r["case_id"] in truth:
            qt = question_truth(truth[r["case_id"]])
            for name in q:
                if qt[name] is not None and name in r["answers"]:
                    q[name].append((r["answers"][name], qt[name]))
    base.update({
        "false_auto_close": len(base["false_closures"]),
        "conditional_error": (len(base["false_closures"]) / n) if n else None,
        "upper_bound_95": (3.0 / n) if n and not base["false_closures"] else None,
        "missed_open_rate": (len(base["false_closures"]) / len(true_open)) if true_open else None,
        "additional_false_open": add_false_open, "nonok_autoclose": nonok_close,
        "per_category": per_cat, "per_stratum": per_stratum,
        "brier": {k: brier(v) for k, v in q.items()}, "reliability": {k: reliability(v) for k, v in q.items()}})
    return base


def heldout_verdict(m, dec) -> tuple:
    r = dec["rules"]
    fails = []
    if m["false_auto_close"] > r["heldout_false_close_max"]:
        fails.append(f"(a) false AUTO_CLOSE {m['false_closures']}")
    if m["automation_coverage"] is None or m["automation_coverage"] < r["heldout_min_automation"]:
        fails.append(f"(b) automation {m['automation_coverage']}")
    cr = (m["cost_reduction"] or {}).get("reduction")
    if cr is None or cr < r["heldout_min_cost_reduction"]:
        fails.append(f"(c) narrow-stage cost reduction {cr}")
    if m["additional_false_open"] > r["heldout_max_additional_false_open"]:
        fails.append(f"(d) additional false OPEN {m['additional_false_open']}")
    if len(m["nonok_autoclose"]) > r["heldout_nonok_autoclose_max"]:
        fails.append(f"(e) non-ok status produced AUTO_CLOSE {m['nonok_autoclose']}")
    if fails:
        return "NO-GO-OFFLINE", "held-out gates failed: " + "; ".join(fails)
    return "GO-E4", "held-out gates (a)-(e) passed"


# ---------------------------------------------------------------- results.json
def results_doc(phase, verdict, rule, m, dec_path=DECISION, extra_notes=None):
    """p15-results/1 for the E1 outcome.  verdict: GO | GO-E4 | NO-GO-OFFLINE | BLOCKED."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    dsha = hashlib.sha256(pathlib.Path(dec_path).read_bytes()).hexdigest()
    gate_arm = {"smoke": "e1-smoke", "heldout": "e1-heldout", "calibration": "e1-calibration"}[phase]
    passed = verdict in ("GO", "GO-E4")
    gate_verdict = "PENDING" if passed else verdict
    if phase == "smoke" and passed:
        down = "PENDING"
    elif phase == "heldout" and passed:
        down = "PENDING"
    else:
        down = "BLOCKED"
    mk = {k: None for k in A.METRIC_KEYS}
    jev = m["jev"]
    dm = {k: m.get(k) for k in ("n_cases", "eligible", "auto_close", "automation_coverage", "false_closures", "true_closures",
                                "model_mismatch_cases", "failed_frac", "conventional_agreement", "conventional_false_closures",
                                "perturbation_groups", "perturbation_consistent_exact", "perturbation_consistent_closing",
                                "decision_counts", "precheck_counts", "cost_reduction")}
    for k in ("false_auto_close", "conditional_error", "upper_bound_95", "missed_open_rate", "additional_false_open", "brier", "per_category", "per_stratum"):
        if k in m:
            dm[k] = m[k]
    dm["latency_ms"] = {"p50": jev.get("p50_ms"), "p95": jev.get("p95_ms")}
    jv = {"logical_calls": jev["logical_calls"], "status_counts": jev["status_counts"], "input_tokens": jev["input_tokens"],
          "usd": jev["usd"], "model": jev.get("model") or "jev-1.14.0"}

    def row(arm, label, role, verdict_, rule_, metrics=None):
        return {"arm": arm, "arm_label": label, "stratum": "offline" if role == "offline-gate" else "sonnet", "role": role,
                "n_planned": m["n_cases"] if role == "offline-gate" else 6, "n_completed": m["n_cases"] if role == "offline-gate" else 0,
                "runs_dir": str(OFFLINE), "metrics": dict(mk), "design_metrics": metrics or {}, "haiku": None,
                "jev": jv if role == "offline-gate" else {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0, "model": "jev-1.14.0"},
                "verdict": verdict_, "rule": rule_, "extension_used": False}

    rows = [row(gate_arm, f"E1 {phase} gate (offline fix-closure replay)", "offline-gate", gate_verdict, rule, dm)]
    down_rule = "E1 gate passed; E4 live not run yet" if down == "PENDING" else f"E1 {phase}: {verdict}"
    rows.append(row("f4b", "Jev checker with conventional fallback (E4)", "test", down, down_rule))
    rows.append(row("f4c", "conventional checker on every eligible packet (E4)", "control", down, down_rule))
    res = {"schema": "p15-results/1", "experiment": "E1", "design_id": "p15-E1", "generated_utc": now,
           "decision_file": {"path": str(dec_path), "sha256": dsha},
           "stage": "offline", "status": "complete" if verdict in ("NO-GO-OFFLINE", "GO-E4") else "partial", "rows": rows,
           "blocked_downstream": [] if passed else [{"experiment": "E4", "reason": f"E1 {phase}: {verdict}: {rule}"}],
           "notes": list(extra_notes or []) + [f"qset {QSET_VERSION}", "exploratory gates, not guarantees"]}
    return res


def render_md(phase, verdict, rule, m) -> str:
    cr = (m.get("cost_reduction") or {}).get("reduction")
    L = [f"# E1 offline results: {phase}", "", f"**{'SMOKE ' if phase == 'smoke' else 'E1 '}{verdict}**: {rule}", "",
         f"- cases {m['n_cases']} (truth decided {m['n_truth_decided']}); eligible packets {m['eligible']}; AUTO_CLOSE {m['auto_close']}; "
         f"automation coverage {m['automation_coverage']}",
         f"- false AUTO_CLOSE: {m['false_closures'] or 'none'}; true AUTO_CLOSE: {len(m['true_closures'])}",
         f"- decisions {m['decision_counts']}; prechecks {m['precheck_counts']}",
         f"- conventional checker: agreement with Jev closing decision {m['conventional_agreement']}; false closures {m['conventional_false_closures'] or 'none'}",
         f"- perturbation consistency: {m['perturbation_consistent_exact']}/{m['perturbation_groups']} groups identical decisions, "
         f"{m['perturbation_consistent_closing']}/{m['perturbation_groups']} identical closing decision",
         f"- narrow-stage cost reduction (checker output tokens, D2): {cr}",
         f"- Jev: calls {m['jev']['logical_calls']}, status {m['jev']['status_counts']}, input tokens {m['jev']['input_tokens']}, "
         f"USD {m['jev']['usd']} (reported apart, never added to worker tokens); latency p50/p95 {m['jev']['p50_ms']}/{m['jev']['p95_ms']} ms"]
    if "per_category" in m:
        L += ["", "## Per category", "", "| category | cases | eligible | AUTO_CLOSE | false |", "|---|---|---|---|---|"]
        for k, v in sorted(m["per_category"].items()):
            L.append(f"| {k} | {v['cases']} | {v['eligible']} | {v['auto_close']} | {v['false_closures']} |")
        L += ["", f"Per stratum: {m['per_stratum']}", f"Brier: {m['brier']}",
              f"Conditional error among automated closures: {m['conditional_error']} (one-sided 95% upper bound: {m['upper_bound_95']})"]
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- cli
def run(phase, offline=OFFLINE, dec_path=DECISION, out_dir=E1, update_matrix=True, tokens=None):
    dec = A.load_decision(dec_path)
    offline = pathlib.Path(offline)
    rows = load_rows(phase, offline / f"replay-{phase}.jsonl")
    if not rows or not any(r.get("live") for r in rows):
        raise SystemExit(f"no live replay rows for {phase}: run replay.py --phase {phase} --live first")
    truth = load_truth(offline / "labels/truth.jsonl")
    if not truth:
        raise SystemExit("no truth.jsonl: run ingest_labels.py first")
    thr = {k: dec["thresholds"][k] for k in policy.DEFAULT_THR}
    if phase == "heldout":
        frozen = json.loads((offline / "calibration-freeze.json").read_text())
        thr = {k: frozen["thresholds"][k] for k in policy.DEFAULT_THR}
    conv = load_conv_answers(phase, offline)
    plan_p = offline / f"phase-{phase}.json"
    plan = json.load(open(plan_p)) if plan_p.exists() else None
    tokens = tokens if tokens is not None else conv_tokens(phase, offline)
    if phase == "smoke":
        m = smoke_metrics(rows, truth, conv, thr, tokens, plan)
        verdict, rule = smoke_verdict(m, dec)
    else:
        m = heldout_metrics(rows, truth, conv, thr, tokens, plan)
        verdict, rule = heldout_verdict(m, dec)
    res = results_doc(phase, verdict, rule, m, dec_path)
    out_dir = pathlib.Path(out_dir)
    (out_dir / "offline-results.md").write_text(render_md(phase, verdict, rule, m))
    A.write_results(out_dir / "results.json", res)
    rc = A.update_matrix() if update_matrix else 0
    label = {"GO": "SMOKE GO", "NO-GO-OFFLINE": ("SMOKE " if phase == "smoke" else "E1 ") + "NO-GO-OFFLINE", "BLOCKED": ("SMOKE " if phase == "smoke" else "E1 ") + "BLOCKED",
             "GO-E4": "E1 GO-E4"}[verdict]
    print(label)
    print(rule)
    return verdict, rule, m, rc


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=["smoke", "heldout"])
    a = ap.parse_args(argv)
    run(a.phase)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
