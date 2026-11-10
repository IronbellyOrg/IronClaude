#!/usr/bin/env python3
"""analyze_offline.py   Plan 3.1 offline falsifier -> offline-results.md, results.json (gate row E3-falsifier + live rows PENDING|BLOCKED) and
the central matrix.  Verdict: GO-LIVE | NO-GO-OFFLINE | BLOCKED (inputs missing or budget refused).  D2: offline worker cost is reported as
deduplicated worker OUTPUT tokens only (each message id once); Jev usage is reported apart.  D6: nothing here reads a running total to stop
anything; cost is reported after the fact.  Usage: uv run --no-project python analyze_offline.py"""
import collections
import json
import pathlib
import re
import sys

import e3lib
import packets as pk
import policy
from p15common import analysis as AN
from p15common import harnesslib as H
from p15common import labels as LB

NAMES = ("outcome_follows", "texts_conflict", "evidence_sufficient")
MAP = {"yes": 1.0, "no": 0.0, "uncertain": 0.5}
REASON_IDS = ["exception_reached_model_or_not_retained", "non_ok_status_confirmed", "missing_evidence_not_verifier", "automation_below_min",
              "false_confirmation_margin", "omitted_context_confirmed", "misleading_raised_confirmations", "reorder_paraphrase_flips"]


# ------------------------------------------------------------------ inputs
def conv_answers(steps_ledger=None):
    """-> {case_id: {name: p}} from the done CV steps (yes=1.0, no=0.0, uncertain=0.5); malformed rows are absent (-> VERIFIER)."""
    led = steps_ledger if steps_ledger is not None else e3lib.load_json(e3lib.WORKERS, {"steps": []})
    steps = led["steps"] if isinstance(led, dict) else led
    out = {}
    for s in steps:
        if not s["id"].startswith("CV-") or not pathlib.Path(s["out"]).exists():
            continue
        amap = e3lib.load_json(e3lib.OFF / "batches" / f"conv-{s['id'].split('-', 1)[1]}.json", {})
        for rec in e3lib.read_jsonl(s["out"]):
            cid = amap.get(str(rec.get("packet")))
            if not cid:
                continue
            vals = {}
            for n in NAMES:
                v = str(rec.get(n, "")).strip().lower()
                if v in MAP:
                    vals[n] = MAP[v]
            out[cid] = vals
    return out


def conv_result(vals, evidence_count):
    need = ["outcome_follows", "evidence_sufficient"] + (["texts_conflict"] if evidence_count == 2 else [])
    if not vals or any(n not in vals for n in need):
        return {"status": "invalid", "error": "malformed or missing answer", "answers": None}
    return {"status": "ok", "error": None, "answers": {n: {"type": "noul", "p": vals[n]} for n in need}}


def journal_case_ids():
    ids = set()
    for p in (e3lib.E3 / "journal").glob("jev-falsifier*.jsonl"):
        for r in e3lib.read_jsonl(p):
            if r.get("case_id"):
                ids.add(r["case_id"])
    return ids


def collect(dec):
    thr = e3lib.thresholds(dec)
    base, pert = e3lib.load_cases("base"), e3lib.load_cases("perturb")
    truth = {r["case_id"]: r["blocking"] for r in e3lib.read_jsonl(e3lib.LABELS / "truth.jsonl")}
    jev = {}
    for p in (e3lib.OFF / "jev").glob("*.json") if (e3lib.OFF / "jev").exists() else []:
        r = json.loads(p.read_text())
        jev[r["case_id"]] = r
    conv = conv_answers()
    called = journal_case_ids() | {c for c, r in jev.items() if r.get("result")}
    base_by = {c["case_id"]: c for c in base}
    rows, missing = [], []
    for c in base + pert:
        cid = c["case_id"]
        p = pk.packet_of_case(c)
        is_p = c["split"] == "perturb"
        bid = c.get("base_case_id", cid)
        t = truth.get(bid)
        if t is None:
            missing.append(f"truth:{bid}")
        row = {"case_id": cid, "kind": "perturb" if is_p else "base", "variant": c["variant"] if is_p else "base", "base_id": bid,
               "category": c["category"], "code_outcome": p.code_outcome, "truth": t, "evidence_count": p.evidence_count,
               "confirmable_from_packet": c.get("confirmable_from_packet", "yes"), "reached_model": cid in called,
               "jev_status": None, "jev_p": {}, "conv_p": {}}
        if p.code_outcome == "OK":
            jr = (jev.get(cid) or {}).get("result")
            if jr is None:
                missing.append(f"jev:{cid}")
            row["jev_status"] = jr["status"] if jr else "missing"
            if jr and jr.get("answers"):
                row["jev_p"] = {n: a.get("p") for n, a in jr["answers"].items()}
            row["jev_decision"] = policy.decide("OK", jr, thr, p.evidence_count)
            cr = conv_result(conv.get(cid), p.evidence_count)
            if cid not in conv:
                missing.append(f"conv:{cid}")
            row["conv_status"] = cr["status"]
            row["conv_p"] = {n: a["p"] for n, a in (cr["answers"] or {}).items()}
            row["conv_decision"] = policy.decide("OK", cr, thr, p.evidence_count)
        else:
            row["jev_decision"] = policy.decide(p.code_outcome, None, thr)
            row["conv_decision"] = policy.decide(p.code_outcome, None, thr)
            row["conv_status"] = None
        rows.append(row)
    return rows, missing, thr


# ------------------------------------------------------------------ gate (pure; tested on synthetic rows)
def rate(num, den):
    return (num / den) if den else 0.0


def compute_gate(rows, dec, thr=None):
    """rows: dicts as built by collect().  Returns {"metrics": {...}, "reasons": [(id, text)], "checks": {...}}."""
    R = dec["rules"]
    thr = thr or {"t_suff": dec["thresholds"]["t_suff"], "t_follow": dec["thresholds"]["t_follow"], "t_conflict": dec["thresholds"]["t_conflict"]}
    base = [r for r in rows if r["kind"] == "base"]
    pert = [r for r in rows if r["kind"] == "perturb"]
    elig = [r for r in base if r["code_outcome"] != "EXCEPTION"]
    jconf = [r for r in elig if r["jev_decision"] == policy.CONFIRMED]
    cconf = [r for r in elig if r["conv_decision"] == policy.CONFIRMED]
    dec_t = lambda lst: [r for r in lst if r["truth"] in ("yes", "no")]
    jfc = sum(1 for r in dec_t(jconf) if r["truth"] == "no")
    cfc = sum(1 for r in dec_t(cconf) if r["truth"] == "no")
    jfc_rate, cfc_rate = rate(jfc, len(dec_t(jconf))), rate(cfc, len(dec_t(cconf)))
    automation = rate(len(jconf), len(elig))
    # structural checks
    exc = [r for r in rows if r["code_outcome"] == "EXCEPTION"]
    exc_bad = [r["case_id"] for r in exc if r["reached_model"] or r["jev_decision"] != policy.RETAIN or r["conv_decision"] != policy.RETAIN]
    nonok_conf = [r["case_id"] for r in rows if r["code_outcome"] == "OK" and r["jev_status"] != "ok" and r["jev_decision"] == policy.CONFIRMED]
    nonok_conf += [r["case_id"] for r in rows if r["code_outcome"] == "OK" and r.get("conv_status") != "ok" and r["conv_decision"] == policy.CONFIRMED]
    miss_bad = []
    for r in rows:
        if r["code_outcome"] == "QUOTE_FAIL" and (r["jev_decision"] != policy.VERIFIER or r["conv_decision"] != policy.VERIFIER):
            miss_bad.append(r["case_id"])
        if r["code_outcome"] == "OK":
            js = r["jev_p"].get("evidence_sufficient")
            if r["jev_decision"] == policy.CONFIRMED and (js is None or js < thr["t_suff"]):
                miss_bad.append(r["case_id"])
            cs = r["conv_p"].get("evidence_sufficient")
            if r["conv_decision"] == policy.CONFIRMED and (cs is None or cs < thr["t_suff"]):
                miss_bad.append(r["case_id"])
        if r["jev_decision"] not in policy.DECISIONS or r["conv_decision"] not in policy.DECISIONS:
            miss_bad.append(r["case_id"])
    # perturbations
    by_base = {r["case_id"]: r for r in base}
    kinds = collections.defaultdict(list)
    for r in pert:
        kinds[r["variant"]].append(r)
    omit_conf = sum(1 for r in kinds["omit"] if r["jev_decision"] == policy.CONFIRMED)
    misl = kinds["misleading"]
    misl_conf = sum(1 for r in misl if r["jev_decision"] == policy.CONFIRMED)
    misl_base_conf = sum(1 for r in misl if by_base.get(r["base_id"], {}).get("jev_decision") == policy.CONFIRMED)
    flips = sum(1 for r in kinds["swap"] + kinds["paraphrase"] if r["jev_decision"] != by_base.get(r["base_id"], {}).get("jev_decision"))
    reasons = []
    if exc_bad:
        reasons.append((REASON_IDS[0], f"EXCEPTION case(s) reached a model or were not retained: {exc_bad}"))
    if nonok_conf:
        reasons.append((REASON_IDS[1], f"a non-ok status produced CONFIRMED: {nonok_conf}"))
    if miss_bad:
        reasons.append((REASON_IDS[2], f"missing evidence produced something other than VERIFIER: {sorted(set(miss_bad))}"))
    if automation < R["automation_min"]:
        reasons.append((REASON_IDS[3], f"automation {automation:.3f} = {len(jconf)}/{len(elig)} < {R['automation_min']}"))
    if jfc_rate > cfc_rate + R["false_confirm_margin"]:
        reasons.append((REASON_IDS[4], f"Jev false-confirmation rate {jfc_rate:.3f} ({jfc}/{len(dec_t(jconf))}) > conventional {cfc_rate:.3f} ({cfc}/{len(dec_t(cconf))}) + {R['false_confirm_margin']}"))
    if omit_conf > R["omitted_context_confirmed_max"]:
        reasons.append((REASON_IDS[5], f"omitted-context perturbations CONFIRMED {omit_conf} of {len(kinds['omit'])} > {R['omitted_context_confirmed_max']}"))
    if misl_conf - misl_base_conf > R["misleading_raise_max"]:
        reasons.append((REASON_IDS[6], f"misleading instructions raised confirmations by {misl_conf - misl_base_conf} ({misl_conf} vs {misl_base_conf} on their base cases) > {R['misleading_raise_max']}"))
    if flips > R["reorder_paraphrase_flip_max"]:
        reasons.append((REASON_IDS[7], f"reorder + paraphrase flipped {flips} of {len(kinds['swap']) + len(kinds['paraphrase'])} decisions > {R['reorder_paraphrase_flip_max']}"))
    metrics = {"base_cases": len(base), "eligible": len(elig), "exceptions": len(exc), "jev_confirmed": len(jconf), "automation": automation,
               "jev_false_confirmations": jfc, "jev_false_confirmation_rate": jfc_rate,
               "conv_confirmed": len(cconf), "conv_automation": rate(len(cconf), len(elig)), "conv_false_confirmations": cfc, "conv_false_confirmation_rate": cfc_rate,
               "blocker_loss": 0, "blocker_loss_note": "structurally zero: Jev never rejects or demotes; every non-confirmation goes to the verifier",
               "perturbations": {k: len(v) for k, v in kinds.items()}, "omit_confirmed": omit_conf, "misleading_confirmed": misl_conf,
               "misleading_base_confirmed": misl_base_conf, "reorder_paraphrase_flips": flips,
               "jev_status_counts": dict(collections.Counter(r["jev_status"] for r in rows if r["code_outcome"] == "OK"))}
    return {"metrics": metrics, "reasons": reasons}


def brier_and_reliability(rows):
    out = {}
    for n in ("outcome_follows", "texts_conflict"):
        pairs = [(r["jev_p"][n], 1.0 if r["truth"] == "yes" else 0.0) for r in rows
                 if r["kind"] == "base" and r["jev_status"] == "ok" and n in r["jev_p"] and r["truth"] in ("yes", "no")]
        if not pairs:
            out[n] = None
            continue
        bins = {"[0,0.3)": [], "[0.3,0.7)": [], "[0.7,1]": []}
        for p, y in pairs:
            bins["[0,0.3)" if p < 0.3 else "[0.3,0.7)" if p < 0.7 else "[0.7,1]"].append((p, y))
        out[n] = {"n": len(pairs), "brier": sum((p - y) ** 2 for p, y in pairs) / len(pairs),
                  "reliability": {b: {"n": len(v), "mean_p": (sum(p for p, _ in v) / len(v)) if v else None, "frac_blocking": (sum(y for _, y in v) / len(v)) if v else None} for b, v in bins.items()},
                  "truth_proxy": "blocking = yes (the only label field)"}
    es = [r["jev_p"]["evidence_sufficient"] for r in rows if r["kind"] == "base" and r["jev_status"] == "ok" and "evidence_sufficient" in r["jev_p"]]
    out["evidence_sufficient"] = {"n": len(es), "mean_p": (sum(es) / len(es)) if es else None, "note": "companion null-case question: no truth field, distribution only"}
    return out


def risk_coverage(rows, thr):
    base = [r for r in rows if r["kind"] == "base" and r["code_outcome"] != "EXCEPTION"]
    out = []
    for t in (0.5, 0.6, 0.7, 0.8, 0.9, 0.95):
        tt = {"t_suff": t, "t_follow": t, "t_conflict": t}
        conf = []
        for r in base:
            if r["code_outcome"] != "OK" or r["jev_status"] != "ok":
                continue
            res = {"status": "ok", "answers": {n: {"type": "noul", "p": v} for n, v in r["jev_p"].items()}}
            if policy.decide("OK", res, tt, r["evidence_count"]) == policy.CONFIRMED:
                conf.append(r)
        dt = [r for r in conf if r["truth"] in ("yes", "no")]
        fc = sum(1 for r in dt if r["truth"] == "no")
        out.append({"threshold": t, "automation": rate(len(conf), len(base)), "false_confirmations": fc, "error_rate": rate(fc, len(dt))})
    return out


def offline_tokens():
    """D2: deduplicated worker OUTPUT tokens of the offline steps (labelers, adjudicators, conventional replay), by kind.  Reported, never a limit."""
    led = e3lib.load_json(e3lib.WORKERS, {"steps": []})
    steps = led["steps"] if isinstance(led, dict) else led
    by_prompt = {s["prompt"]: s for s in steps}
    rx = re.compile(r"^Read (?P<path>\S+) and follow")
    cands = collections.defaultdict(list)
    for m, info in H.scan_by_first_message(H.tasks_glob(), rx):
        if m.group("path") in by_prompt:
            cands[m.group("path")].append(info)
    per_kind, n = collections.defaultdict(int), collections.Counter()
    for path, cs in cands.items():
        s = by_prompt[path]
        c = H.pick_transcript(cs, s["model"], key=s["id"], warn=False)
        if c:
            per_kind[s["kind"]] += c["tokens"]
            n[s["kind"]] += 1
    return {"output_tokens_by_kind": dict(per_kind), "workers_by_kind": dict(n), "total_output_tokens": sum(per_kind.values())}


def jev_usage():
    p = e3lib.E3 / "manifest.json"
    led = e3lib.JEV / "budget/e3.json"
    out = {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0, "model": None}
    for r in e3lib.read_jsonl(e3lib.E3 / "journal/jev-falsifier.jsonl"):
        if r.get("final"):
            out["logical_calls"] += 1
            out["status_counts"][r.get("result_status")] = out["status_counts"].get(r.get("result_status"), 0) + 1
            out["input_tokens"] += (r.get("usage") or {}).get("input_tokens") or 0
            out["model"] = r.get("model_returned") or out["model"]
    out["usd"] = out["input_tokens"] * 0.042 / 1e6
    return out


# ------------------------------------------------------------------ outputs
def result_rows(verdict, rule, gate_dm, n_done, jev):
    mk = {k: None for k in AN.METRIC_KEYS}
    gate = {"arm": "E3-falsifier", "arm_label": "Jev confirmation-only screen: offline falsifier (60 base + 40 perturbations)", "stratum": "offline",
            "role": "offline-gate", "n_planned": 100, "n_completed": n_done, "runs_dir": str(e3lib.OFF), "metrics": dict(mk),
            "design_metrics": gate_dm, "haiku": None, "jev": jev, "verdict": verdict, "rule": rule, "extension_used": False}
    live_v = "PENDING" if verdict == "PENDING" else "BLOCKED"
    live_rule = "offline gate passed (GO-LIVE): session 2 builds the live harness" if live_v == "PENDING" else f"live not started: offline gate {verdict} ({rule})"
    zero = {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0, "model": "jev-1.14.0"}
    rows = [gate]
    for arm, label, stratum, role, n in (("g3c", "Jev confirmation screen + conventional verifier fallback", "sonnet", "test", 6),
                                         ("g3b", "Conventional verifier VF1 before the first revision", "sonnet", "control", 6),
                                         ("g3ch", "Jev confirmation screen, Haiku loop workers", "haiku", "test", 4),
                                         ("g3bh", "Conventional verifier VF1, Haiku loop workers", "haiku", "control", 4)):
        rows.append({"arm": arm, "arm_label": label, "stratum": stratum, "role": role, "n_planned": n, "n_completed": 0, "runs_dir": str(e3lib.E3 / "runs"),
                     "metrics": dict(mk), "design_metrics": {}, "haiku": None, "jev": dict(zero), "verdict": live_v, "rule": live_rule, "extension_used": False})
    return rows


def write_results_file(verdict, rule, gate_dm, n_done, jev, status, notes, blocked_downstream=None):
    dec_path = e3lib.E3 / "decision.toml"
    res = {"schema": "p15-results/1", "experiment": "E3", "design_id": "p15-E3",
           "decision_file": {"path": str(dec_path), "sha256": e3lib.sha_text(dec_path.read_text())},
           "stage": "offline", "status": status, "rows": result_rows(verdict, rule, gate_dm, n_done, jev),
           "blocked_downstream": blocked_downstream or [], "notes": notes}
    AN.write_results(e3lib.E3 / "results.json", res)
    rc = AN.update_matrix()
    return rc


def write_blocked_budget(summary, why):
    """Called by replay.py when the pre-flight reservation does not fit: BLOCKED-BUDGET, no call made."""
    rc = write_results_file("BLOCKED", f"BLOCKED-BUDGET: reservation {summary['reserve_tokens']} tokens (${summary['reserve_usd']:.6f}) does not fit: {why}",
                            {"requests": summary["requests"], "reserve_tokens": summary["reserve_tokens"]}, 0,
                            {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0, "model": "jev-1.14.0"}, "not-run",
                            ["Budget refusal before the first paid call; no Jev call was made."],
                            [{"experiment": "E3 live", "reason": "offline replay blocked by the Jev budget reservation"}])
    if rc:
        print("ERROR matrix build failed")


def fmt(x, nd=3):
    return "n/a" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def render_md(verdict_line, rows, gate, missing, extra):
    m = gate["metrics"]
    L = [f"# E3 offline falsifier results", "", f"VERDICT: {verdict_line}", ""]
    if missing:
        L += [f"Missing inputs ({len(missing)}): " + ", ".join(missing[:40]) + (" ..." if len(missing) > 40 else ""), ""]
    L += ["## Rule table (plan 3.1; thresholds frozen in decision.toml)", "", "| Rule | Result |", "|---|---|"]
    fired = dict(gate["reasons"])
    for rid in REASON_IDS:
        L.append(f"| {rid} | {'FIRED: ' + fired[rid] if rid in fired else 'ok'} |")
    L += ["", "## Metrics (60 base cases)", "",
          f"- eligible (not EXCEPTION): {m['eligible']} of {m['base_cases']}; exceptions retained by code: {m['exceptions']}",
          f"- automation (CONFIRMED / eligible): {fmt(m['automation'])} ({m['jev_confirmed']}/{m['eligible']})",
          f"- Jev false confirmations: {m['jev_false_confirmations']} (rate among confirmations {fmt(m['jev_false_confirmation_rate'])})",
          f"- conventional verifier on identical packets: confirmed {m['conv_confirmed']} (automation {fmt(m['conv_automation'])}), false confirmations {m['conv_false_confirmations']} (rate {fmt(m['conv_false_confirmation_rate'])})",
          f"- blocker loss: {m['blocker_loss']} ({m['blocker_loss_note']})",
          f"- Jev call statuses (OK packets): {m['jev_status_counts']}", "",
          "## Perturbations", "", f"- counts {m['perturbations']}; omitted-context CONFIRMED {m['omit_confirmed']}; misleading CONFIRMED {m['misleading_confirmed']} vs base {m['misleading_base_confirmed']}; reorder+paraphrase flips {m['reorder_paraphrase_flips']}", ""]
    L += ["## Brier / reliability (against truth `blocking`, a proxy for the per-question judgments)", "", "```json", json.dumps(extra["brier"], indent=1), "```", "",
          "## Risk-coverage (uniform threshold sweep; reported, the frozen thresholds are 0.7)", "", "| threshold | automation | false confirmations | error rate |", "|---|---|---|---|"]
    for r in extra["risk"]:
        L.append(f"| {r['threshold']} | {fmt(r['automation'])} | {r['false_confirmations']} | {fmt(r['error_rate'])} |")
    L += ["", "## Labels", "", "```json", json.dumps(extra["agreement"], indent=1), "```", "",
          f"author/reviewer mismatches: {extra['mismatch']}", "", "## Cost (reported, never a limit; D2/D6)", "",
          f"- offline worker output tokens (each message id once): {extra['tokens']}", f"- Jev usage: {extra['jev']}", "",
          "## Per-case table", "", "| case | kind | category | code | truth | Jev status | Jev decision | conv decision |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: r["case_id"]):
        L.append(f"| {r['case_id']} | {r['variant']} | {r['category']} | {r['code_outcome']} | {r['truth']} | {r['jev_status']} | {r['jev_decision']} | {r['conv_decision']} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    dec = e3lib.decision()
    rows, missing, thr = collect(dec)
    jev = jev_usage()
    if not rows or missing:
        n_base = sum(1 for r in rows if r["kind"] == "base")
        rule = f"inputs missing ({len(missing)}): " + ", ".join(missing[:8]) + (" ..." if len(missing) > 8 else "")
        print("BLOCKED", rule)
        (e3lib.E3 / "offline-results.md").write_text(f"# E3 offline falsifier results\n\nVERDICT: BLOCKED ({rule})\n")
        rc = write_results_file("BLOCKED", rule, {"missing": len(missing), "base_cases_found": n_base}, 0, jev, "not-run", ["Run the coordinator phase O steps."])
        return 1
    gate = compute_gate(rows, dec, thr)
    verdict = "NO-GO-OFFLINE" if gate["reasons"] else "PENDING"
    label = "NO-GO-OFFLINE" if gate["reasons"] else "GO-LIVE"
    rule = "; ".join(f"{i}: {t}" for i, t in gate["reasons"]) or "GO-LIVE: every offline rule passed"
    extra = {"brier": brier_and_reliability(rows), "risk": risk_coverage(rows, thr), "agreement": e3lib.load_json(e3lib.LABELS / "agreement.json", {}),
             "mismatch": len(e3lib.read_jsonl(e3lib.LABELS / "author_mismatch.jsonl")), "tokens": offline_tokens(), "jev": jev}
    (e3lib.E3 / "offline-results.md").write_text(render_md(f"{label}" + (f" ({rule})" if gate["reasons"] else ""), rows, gate, missing, extra))
    dm = dict(gate["metrics"]); dm.update({"kappa": {k: v for k, v in (extra["agreement"].get("fields") or {}).items()}, "offline_worker_output_tokens": extra["tokens"],
                                           "brier": extra["brier"], "risk_coverage": extra["risk"], "thresholds": thr, "qset_version": "e3-q1"})
    bd = [{"experiment": "E3 live", "reason": f"offline gate {label}"}] if gate["reasons"] else []
    rc = write_results_file(verdict, rule, dm, len(rows), jev, "complete", ["Offline falsifier only: no live run; the larger 200/300 pilot is deferred (plan decision 4)."], bd)
    print(f"VERDICT {label}: {rule}")
    if rc:
        print("ERROR matrix build failed (the verdict above is unchanged)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
