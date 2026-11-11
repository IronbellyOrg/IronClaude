#!/usr/bin/env python3
"""probe.py [--live] [--workdir DIR]   Live adapter probe (PLAN-0 section 6).  Coordinator-run; synthetic state only.

Three logical calls (experiment PLAN0, phase probe, budget $JEV/budget/plan0.json: ceiling $0.10 and 2,000,000 input tokens):
  1. a Noul `arrived_late`;  2. a Choice `delivery_timing` plus its companion Noul `timing_stated`;  3. call 2 with the Choice options in reverse order.
Without --live: a dry run (no network object is created); prints the three request payloads and the reservation estimate.
With --live: run through   bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $JEV && uv run --no-project python probe.py --live'
prints status, model_returned, answers, usage and latency per call (never the key), writes journal/jev-probe.jsonl and probe-result.json, then runs keyscan."""
import json
import math
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from jevlib import config as C  # noqa: E402
from jevlib.budget import Budget, usd  # noqa: E402
from jevlib.client import JevClient  # noqa: E402
from jevlib.journal import Journal  # noqa: E402
from jevlib.questions import build_request, canonical_bytes, choice, noul  # noqa: E402
from jevlib.transport import UrllibTransport  # noqa: E402

SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
QSET = "plan0-q1"
CEILING_USD, CEILING_TOKENS = 0.10, 2_000_000
STATE = {"message": "The parcel arrived two days after the promised date."}

ARRIVED_LATE = noul("Did the parcel arrive later than promised?",
                    "The message says the parcel came after the promised date.",
                    "The message says the parcel came on or before the promised date.")
TIMING_STATED = noul("Does `message` say when the parcel arrived relative to the promised date?",
                     "The message states whether the parcel came before, on or after the promised date.",
                     "The message says nothing about when the parcel arrived compared with the promised date.")
OPTIONS = {"early": "The message says the parcel came before the promised date, for example a day ahead of schedule.",
           "on_time": "The message says the parcel came on the promised date.",
           "late": "The message says the parcel came after the promised date, for example two days late."}


def timing_choice(options):
    return choice("When did the parcel arrive relative to the promised date, according to `message`?", options)


def calls():
    rev = dict(reversed(list(OPTIONS.items())))
    return [("arrived_late", {"arrived_late": ARRIVED_LATE}),
            ("timing", {"delivery_timing": timing_choice(OPTIONS), "timing_stated": TIMING_STATED}),
            ("timing_reversed", {"delivery_timing": timing_choice(rev), "timing_stated": TIMING_STATED})]


class Recording:
    """Wraps a transport and remembers each raw response body so the returned model id can be read even from an invalid response."""
    def __init__(self, inner):
        self.inner, self.bodies = inner, []

    def post(self, url, headers, body, timeout):
        status, h, raw = self.inner.post(url, headers, body, timeout)
        self.bodies.append(raw)
        return status, h, raw


def returned_model(raw):
    try:
        return json.loads(raw.decode("utf-8")).get("model")
    except Exception:
        return None


def order_consistent(a, b, tol=0.15):
    """Option-order check: same argmax choice and probabilities within tol for the Choice, companion Noul within tol."""
    if a is None or b is None:
        return False
    ca, cb = a["delivery_timing"], b["delivery_timing"]
    if ca["choice"] != cb["choice"]:
        return False
    if max(abs(ca["probs"][k] - cb["probs"][k]) for k in ca["probs"]) > tol:
        return False
    return abs(a["timing_stated"]["p"] - b["timing_stated"]["p"]) <= tol


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    live = "--live" in args
    work = pathlib.Path(args[args.index("--workdir") + 1]) if "--workdir" in args else HERE
    reqs = [(n, build_request(STATE, q)) for n, q in calls()]
    est = sum(math.ceil(len(canonical_bytes(r)) / C.RESERVE_BYTES_PER_TOKEN) for _, r in reqs)
    reserve = int(est * 1.2) + 1
    if not live:
        for n, r in reqs:
            print(f"--- request {n} ({len(canonical_bytes(r))} bytes)")
            print(json.dumps(r, indent=1, ensure_ascii=False))
        print(f"RESERVATION estimate {est} tokens x 1.2 = {reserve} tokens (${usd(reserve):.8f}); ceiling ${CEILING_USD} / {CEILING_TOKENS} tokens")
        print("DRY RUN OK: no network object created, no key needed")
        return 0
    budget = Budget(work / "budget/plan0.json", ceiling_usd=CEILING_USD, ceiling_input_tokens=CEILING_TOKENS)
    budget.reserve_phase("probe", reserve)
    rec = Recording(UrllibTransport())
    client = JevClient(experiment="PLAN0", phase="probe", budget=budget, journal=Journal(work / "journal/jev-probe.jsonl"),
                       transport=rec, live=True, allowed_classes={"synthetic"})
    results = []
    for n, q in calls():
        r = client.ask(STATE, q, case_id=n, qset_version=QSET, data_classes={"synthetic"}, purpose="plan0 adapter probe")
        mr = returned_model(rec.bodies[-1]) if rec.bodies else None
        print(f"{n}: status={r.status} error={r.error} model_returned={mr} attempts={r.attempts} latency_ms={r.latency_ms}")
        print(f"    answers={json.dumps(r.answers)} usage={r.usage}")
        results.append((r, mr))
    budget.release_phase("probe")
    ok = [r.status == "ok" for r, _ in results]
    out = {"model_ok": all(m == C.MODEL for _, m in results), "validator_ok": all(ok),
           "order_consistent": order_consistent(results[1][0].answers, results[2][0].answers) if ok[1] and ok[2] else False,
           "latency_ms": [r.latency_ms for r, _ in results], "usd": budget.state()["spent_usd"]}
    (work / "probe-result.json").write_text(json.dumps(out, indent=1))
    print("PROBE RESULT", json.dumps(out))
    if not out["model_ok"]:
        print("MODEL NOT CONFIRMED: the server answered with another model id; owner confirmation needed before any paid phase")
    kp = subprocess.run(["uv", "run", "--no-project", "python", str(HERE / "keyscan.py"), str(SP / "p15"), str(SP / "central")], capture_output=True, text=True)
    print(kp.stdout.strip())
    return 0 if out["model_ok"] and out["validator_ok"] and kp.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
