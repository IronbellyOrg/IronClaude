#!/usr/bin/env python3
"""replay.py --phase falsifier [--live]   Offline Jev replay of the 100 packets (60 base + 40 perturbations).  Coordinator-run only.

Without --live: dry-run preflight (contract J4): builds every request with live=False, journals the manifest to journal/jev-dryrun.jsonl,
prints the number of requests and the reservation estimate ($, tokens) against the $5 / 30M-token offline ceiling.  No network object,
no key.  With --live (needs JEV_API_KEY, sourced by the coordinator inside the single bash -c command, contract J2): reserves the phase
BEFORE the first paid call (refuses to start with BLOCKED-BUDGET if it does not fit), then asks Jev once per OK packet and writes
offline/jev/<case_id>.json.  EXCEPTION and QUOTE_FAIL packets never reach Jev.  A failed call is never an answer (the truth table routes
it to the verifier).  No cost check stops a started phase (D6); exit 3 = key missing/rejected."""
import json
import math
import pathlib
import sys

import e3lib
import packets as pk
import policy
import questions
import screen
from jevlib import config as C
from jevlib.budget import Budget, BudgetExhausted, usd
from jevlib.cache import ResponseCache
from jevlib.client import JevClient, KeyMissing, KeyRejected
from jevlib.journal import Journal
from jevlib.manifest import update as manifest_update
from jevlib.questions import build_request, canonical_bytes

PHASE = "falsifier"


def all_cases():
    return e3lib.load_cases("base") + e3lib.load_cases("perturb")


def build_items(cases):
    """-> [dict(case, packet, req|None, est)] for every case; req only for packets that reach the screen."""
    items = []
    for c in sorted(cases, key=lambda c: c["case_id"]):
        p = pk.packet_of_case(c)
        it = {"case": c, "packet": p, "req": None, "est": 0}
        if p.code_outcome == "OK":
            req = build_request(p.state, questions.build_questions(p.state))
            it["req"] = req
            it["est"] = int(math.ceil(len(canonical_bytes(req)) / C.RESERVE_BYTES_PER_TOKEN))
        items.append(it)
    return items


def preflight(items, workdir, dec=None):
    """Dry run with live=False through the real client path; returns the summary used for the reservation."""
    dec = dec or e3lib.decision()
    workdir = pathlib.Path(workdir)
    dry_ledger = workdir / "offline" / "dryrun-budget.json"
    for p in (dry_ledger, pathlib.Path(str(dry_ledger) + ".lock")):
        if p.exists():
            p.unlink()
    big = Budget(dry_ledger, ceiling_usd=1e6, ceiling_input_tokens=10**12)       # a scratch ledger: the dry run never touches the real one
    client = JevClient(experiment=e3lib.EXPERIMENT, phase="dryrun", budget=big, journal=Journal(workdir / "journal/jev-dryrun.jsonl"), live=False)
    thr = e3lib.thresholds(dec)
    n_req = est = n_priv = 0
    for it in items:
        if it["req"] is None:
            continue
        r = client.ask(it["packet"].state, questions.build_questions(it["packet"].state), case_id=it["case"]["case_id"],
                       qset_version=questions.QSET_VERSION, data_classes=set(it["case"]["data_classes"]), purpose="E3 falsifier preflight")
        n_req += 1
        est += it["est"]
        if r.status == "refused" and r.error == "privacy":
            n_priv += 1
        elif not (r.status == "refused" and r.error == "dry_run"):
            raise RuntimeError(f"unexpected dry-run result {r.status}/{r.error} for {it['case']['case_id']}")
    reserve = int(est * 1.2) + 1
    return {"requests": n_req, "est_tokens": est, "reserve_tokens": reserve, "reserve_usd": usd(reserve), "privacy_refused": n_priv,
            "no_call_cases": sum(1 for it in items if it["req"] is None), "thresholds": thr}


def run_phase(items, client, out_dir, thr, resume=True):
    """Ask Jev once per OK packet.  Writes out_dir/<case_id>.json = {case_id, code_outcome, decision, result}.  Returns status counts."""
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    counts = {}
    for it in items:
        cid = it["case"]["case_id"]
        f = out_dir / f"{cid}.json"
        if resume and f.exists():
            prev = json.loads(f.read_text())
            if (prev.get("result") or {}).get("status") == "ok" or (prev.get("result") is None and prev.get("code_outcome") != "OK"):
                counts["ok" if prev.get("result") else "no_call"] = counts.get("ok" if prev.get("result") else "no_call", 0) + 1
                continue
        decision, r = screen.screen_packet(client, it["packet"], cid, it["case"]["data_classes"], thr, purpose="E3 falsifier")
        rec = {"case_id": cid, "code_outcome": it["packet"].code_outcome, "decision": decision, "result": screen.result_json(r),
               "qset_version": questions.QSET_VERSION}
        e3lib.write_json(f, rec)
        st = r.status if r is not None else "no_call"
        counts[st] = counts.get(st, 0) + 1
        if r is not None and r.status == "invalid" and str(r.error).startswith("http_4"):
            print(f"ERROR {cid}: {r.status} {r.error} (a request-builder bug, not an answer)")
    return counts


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--phase" not in argv or argv[argv.index("--phase") + 1] != "falsifier":
        print("usage: replay.py --phase falsifier [--live]")
        return 2
    live = "--live" in argv
    dec = e3lib.decision()
    cases = all_cases()
    if not [c for c in cases if c["split"] == "base"]:
        print("ERROR no base cases: run select_base.py (and perturb.py --real) first")
        return 2
    items = build_items(cases)
    s = preflight(items, e3lib.E3, dec)
    print(f"PREFLIGHT {len(cases)} cases, {s['requests']} Jev requests ({s['no_call_cases']} cases never reach Jev: EXCEPTION or QUOTE_FAIL), "
          f"{s['privacy_refused']} refused by the privacy guard")
    print(f"RESERVATION estimate {s['est_tokens']} tokens x 1.2 = {s['reserve_tokens']} tokens (${s['reserve_usd']:.6f}) of "
          f"${dec['jev']['offline_ceiling_usd']} / {dec['jev']['offline_ceiling_input_tokens']} tokens")
    ledger = e3lib.JEV / "budget/e3.json"
    if not live:
        spent_committed = 0
        if ledger.exists():                 # read-only peek: a dry run never creates or writes the real ledger
            led = json.loads(ledger.read_text())
            pending = sum(d["est"] for d in led["draws"].values() if d.get("actual") is None)
            undrawn = sum(max(r["tokens"] - r["drawn"], 0) for r in led["reserved"].values())
            spent_committed = led["spent_tokens"] + pending + undrawn
        tot = s["reserve_tokens"] + spent_committed
        fits = tot <= dec["jev"]["offline_ceiling_input_tokens"] and usd(tot) <= dec["jev"]["offline_ceiling_usd"]
        print(f"DRY RUN OK (reservation fits the ledger: {fits}); no network object created, no key needed, no ledger written")
        return 0
    budget = Budget(ledger, ceiling_usd=dec["jev"]["offline_ceiling_usd"], ceiling_input_tokens=dec["jev"]["offline_ceiling_input_tokens"])
    try:
        budget.reserve_phase(PHASE, s["reserve_tokens"])
    except BudgetExhausted as e:
        print(f"BLOCKED-BUDGET {e}")
        import analyze_offline
        analyze_offline.write_blocked_budget(s, str(e))
        return 4
    client = JevClient(experiment=e3lib.EXPERIMENT, phase=PHASE, budget=budget, journal=Journal(e3lib.E3 / "journal/jev-falsifier.jsonl"),
                       live=True, cache=ResponseCache(e3lib.OFF / "jev-cache"))
    try:
        counts = run_phase(items, client, e3lib.OFF / "jev", e3lib.thresholds(dec))
    except (KeyMissing, KeyRejected) as e:
        print(f"ERROR configuration: {e}")
        budget.release_phase(PHASE)
        return 3
    budget.release_phase(PHASE)
    manifest_update(e3lib.E3 / "journal/jev-falsifier.jsonl", e3lib.E3 / "manifest.json")
    print(f"REPLAY DONE status counts {counts}; spent ${budget.state()['spent_usd']:.6f}. Next: keyscan (contract J2), then analyze_offline.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
