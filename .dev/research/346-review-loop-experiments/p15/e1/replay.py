"""Jev replay of one offline phase (plan 3.1, 3.2; contract J2, J4, J5).  Dry run by default; only the coordinator passes --live.

  uv run --no-project python replay.py --phase smoke            # dry run: builds every request, checks privacy/size, prints the reservation
  bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $E1 && uv run --no-project python replay.py --phase smoke --live'

Live: first the pre-flight (every request built with live=False, reservation estimate x 1.2, reserve_phase BEFORE the first paid call);
a reservation that does not fit writes offline/BLOCKED-BUDGET-<phase>.json and makes no call.  A later failed draw is a recorded
refused/budget_exhausted fallback, never a stop (D6).  Exit codes: 0 ok, 2 key missing, 3 key rejected, 4 freeze missing (held-out), 5 blocked budget."""
import _boot  # noqa: F401
import argparse
import hashlib
import json
import math
import os
import pathlib
import sys
import time
import tomllib

from jevlib import config as C
from jevlib.budget import Budget, BudgetExhausted, usd
from jevlib.client import JevClient, KeyMissing, KeyRejected
from jevlib.journal import Journal
from jevlib import manifest as MANIFEST
from p15common.datasets import load_cases
import policy
from packets import build_packet, packet_state
from questions import QSET_VERSION, questions_for
import prep_offline as P

E1 = _boot.E1
OFFLINE = E1 / "offline"
JOURNAL = E1 / "journal"
DECISION = E1 / "decision.toml"
RESERVE_FACTOR = 1.2
PURPOSE = "e1-fix-closure-replay"


def load_decision(path=DECISION):
    with open(path, "rb") as f:
        return tomllib.load(f)


def thresholds_for(phase, dec, freeze_path=OFFLINE / "calibration-freeze.json"):
    """smoke and calibration use the starting values of decision.toml; held-out requires the frozen calibrated values (sha pinned)."""
    thr = {k: dec["thresholds"][k] for k in policy.DEFAULT_THR}
    if phase != "heldout":
        return thr, None
    want = dec["thresholds"].get("freeze_sha", "")
    p = pathlib.Path(freeze_path)
    if not want or not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != want:
        raise FreezeMissing("held-out replay needs offline/calibration-freeze.json with its sha256 in decision.toml [thresholds] freeze_sha")
    frozen = json.loads(p.read_text())
    return {k: frozen["thresholds"][k] for k in policy.DEFAULT_THR}, want


class FreezeMissing(Exception):
    pass


def rebuild(case):
    """Packet of a case from its inputs, with the recorded precheck verified (a drift between the case file and the code is an error row)."""
    i = case["packet"]["inputs"]
    pk = build_packet(i["before_text"], i["after_text"], i["finding"], i["history"])
    return pk


def prepare(cases):
    prepared = []
    for c in sorted(cases, key=lambda c: c["case_id"]):
        pk = rebuild(c)
        drift = pk.precheck != c["packet"]["precheck"]
        state = packet_state(pk) if pk.eligible else None
        if state is not None and c["packet"].get("state") is not None and state != c["packet"]["state"]:
            drift = True
        prepared.append((c, pk, state, drift))
    return prepared


def reservation_estimate(prepared) -> int:
    est = sum(pk.est_tokens for _, pk, st, _ in prepared if st is not None)
    return int(math.ceil(est * RESERVE_FACTOR))


def run_replay(phase, *, live, transport=None, dec=None, budget_path=None, journal_dir=JOURNAL, out_dir=OFFLINE, cases=None,
               thr=None, cache=None, sleep=time.sleep, clock=time.monotonic, out_name=None, announce=print):
    """-> summary dict.  Writes <out_dir>/replay-<phase>.jsonl (live) or replay-<phase>.dry.jsonl (dry run)."""
    dec = dec or load_decision()
    out_dir, journal_dir = pathlib.Path(out_dir), pathlib.Path(journal_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    journal_dir.mkdir(parents=True, exist_ok=True)
    if thr is None:
        thr, freeze = thresholds_for(phase, dec)
    cases = cases if cases is not None else load_cases(P.cases_dir(phase))
    prepared = prepare(cases)
    est = reservation_estimate(prepared)
    n_req = sum(1 for _, _, st, _ in prepared if st is not None)
    # ---- pre-flight: every request built with live=False (privacy, size, size accounting); journalled under phase "dryrun"
    jdir_budget = pathlib.Path(journal_dir) / "dryrun-budget.json"
    dry_budget = Budget(jdir_budget, ceiling_usd=dec["jev"]["offline_ceiling_usd"], ceiling_input_tokens=dec["jev"]["offline_ceiling_input_tokens"])
    dry = JevClient(experiment="E1", phase="dryrun", budget=dry_budget, journal=Journal(journal_dir / "jev-dryrun.jsonl"), live=False)
    dry_status = {}
    for c, pk, st, drift in prepared:
        if st is None:
            continue
        r = dry.ask(st, questions_for(pk.n_deps), case_id=c["case_id"], qset_version=QSET_VERSION,
                    data_classes=set(c["data_classes"]), purpose=PURPOSE)
        k = f"{r.status}/{r.error}"
        dry_status[k] = dry_status.get(k, 0) + 1
    summary = {"phase": phase, "cases": len(prepared), "requests": n_req, "reservation_input_tokens": est,
               "reservation_usd": round(usd(est), 6), "dry_status": dry_status, "drift": [c["case_id"] for c, _, _, d in prepared if d],
               "live": live}
    announce(f"PREFLIGHT phase={phase} cases={len(prepared)} requests={n_req} est. input tokens (x{RESERVE_FACTOR})={est} "
             f"reservation=${usd(est):.4f} (ceiling ${dec['jev']['offline_ceiling_usd']})")
    bad = {k: v for k, v in dry_status.items() if k != "refused/dry_run"}
    if bad:
        announce(f"ERROR pre-flight: requests that would not be sent: {bad}")
    if summary["drift"]:
        announce(f"ERROR case files differ from the code (rebuild the cases): {summary['drift']}")
    rows = []
    if live:
        if not os.environ.get(C.KEY_ENV):          # before any reservation: a missing key is a hard error, never a fallback
            raise KeyMissing(f"{C.KEY_ENV} is not set (live replay refused; run through the coordinator's bash -c 'set -a; . $SP/.jev.env ...')")
        bpath = budget_path or (_boot.JEV / "budget" / "E1.json")
        budget = Budget(bpath, ceiling_usd=dec["jev"]["offline_ceiling_usd"], ceiling_input_tokens=dec["jev"]["offline_ceiling_input_tokens"])
        try:
            budget.reserve_phase(phase, est)
        except BudgetExhausted as e:
            blk = {"status": "BLOCKED-BUDGET", "phase": phase, "estimate_input_tokens": est, "estimate_usd": usd(est), "detail": str(e)}
            (out_dir / f"BLOCKED-BUDGET-{phase}.json").write_text(json.dumps(blk, indent=1))
            announce(f"BLOCKED-BUDGET {phase}: {e} (no call made)")
            summary["blocked_budget"] = True
            return summary
        client = JevClient(experiment="E1", phase=phase, budget=budget, journal=Journal(journal_dir / f"jev-{phase}.jsonl"),
                           transport=transport, live=True, cache=cache, sleep=sleep, clock=clock)
    for c, pk, st, drift in prepared:
        row = {"case_id": c["case_id"], "group": c["group"], "family": c["family"], "category": c["category"], "variant": c["variant"],
               "split": c["split"], "stratum": c.get("stratum") or ("real" if "s1_spec" in c["data_classes"] or "stage2_artifact" in c["data_classes"] else "synthetic"),
               "precheck": pk.precheck, "n_deps": pk.n_deps, "qset_version": QSET_VERSION, "live": live,
               "status": "not_called", "error": None, "answers": None, "input_tokens": None, "model": None, "attempts": 0,
               "latency_ms": None, "request_sha256": None, "est_tokens": pk.est_tokens}
        res = None
        if st is not None and live:
            res = client.ask(st, questions_for(pk.n_deps), case_id=c["case_id"], qset_version=QSET_VERSION,
                             data_classes=set(c["data_classes"]), purpose=PURPOSE)
            row.update(status=res.status, error=res.error, model=res.model, attempts=res.attempts, latency_ms=res.latency_ms,
                       request_sha256=res.request_sha256,
                       input_tokens=(res.usage or {}).get("input_tokens"))
            if res.status == "ok":
                row["answers"] = {k: v.get("p") for k, v in res.answers.items()}
        row["decision"] = policy.decide(pk.precheck, res, thr, pk.n_deps)
        rows.append(row)
    if live:
        budget.release_phase(phase)
    name = out_name or (f"replay-{phase}.jsonl" if live else f"replay-{phase}.dry.jsonl")
    (out_dir / name).write_text("".join(json.dumps(r) + "\n" for r in rows))
    jp = journal_dir / f"jev-{phase}.jsonl"
    if live and jp.exists():
        MANIFEST.update(jp, out_dir / f"manifest-{phase}.json")
    summary["rows"] = len(rows)
    summary["decisions"] = {}
    for r in rows:
        summary["decisions"][r["decision"]] = summary["decisions"].get(r["decision"], 0) + 1
    if live:
        sc = {}
        for r in rows:
            sc[r["status"]] = sc.get(r["status"], 0) + 1
        summary["status_counts"] = sc
        summary["thresholds"] = thr
    announce(f"{'LIVE' if live else 'DRY RUN'} {phase}: {summary['decisions']}" + (f" status {summary['status_counts']}" if live else ""))
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=sorted(P.PHASE_DIRS))
    ap.add_argument("--live", action="store_true", help="make paid Jev calls (coordinator only; needs JEV_API_KEY in the environment)")
    a = ap.parse_args(argv)
    try:
        s = run_replay(a.phase, live=a.live)
    except FreezeMissing as e:
        print(f"ERROR {e}")
        return 4
    except KeyMissing as e:
        print(f"ERROR {e}")
        return 2
    except KeyRejected as e:
        print(f"ERROR key rejected: {e}")
        return 3
    if s.get("blocked_budget"):
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
