"""The runner: one live run of the Jev comparison on ``JevClient``, and a rehearsal that never posts.

Command line (each takes ``--root``, the experiment folder by default):
  runner.py run --run-id ID --live     check Gate 1 and Gate 2, then read TYPESAFE_API_KEY and run; refuses without --live
  runner.py rehearse --out DIR         build and budget every request against a throwaway ledger in DIR; no gate, no key, no post

``run`` reads no environment variable before both gates pass.  Only then is ``TYPESAFE_API_KEY`` copied into ``JEV_API_KEY`` inside
this process (``jevlib.config.KEY_ENV`` is ``JEV_API_KEY``); the key is never printed or written.  The live run is a coordinator
action, not part of the build.
"""
import argparse
import contextlib
import datetime
import json
import os
import pathlib
import sys
import time

_EXP = pathlib.Path(__file__).resolve().parents[1]
_JEV = _EXP.parent / "346-review-loop-experiments" / "p15" / "jev"
for _p in (str(_EXP), str(_JEV)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import questions  # noqa: E402
from jevlib import config  # noqa: E402
from jevlib.budget import Budget, BudgetExhausted  # noqa: E402
from jevlib.client import JevClient, KeyMissing, KeyRejected  # noqa: E402
from jevlib.journal import Journal  # noqa: E402
from jevlib.questions import build_request  # noqa: E402
from jevlib.transport import TransportTimeout, UrllibTransport  # noqa: E402

from harness import events, gate, loader, spend  # noqa: E402

# (result status, result error) -> the systemic reason that ends the run with no rerun
SYSTEMIC = {("refused", "budget_exhausted"): "budget_exhausted", ("invalid", "model_mismatch"): "model_mismatch",
            ("refused", "dry_run"): "dry_run"}
KEY_ENV_SOURCE = "TYPESAFE_API_KEY"


@contextlib.contextmanager
def limits(rule):
    """No retry inside the client and the rule's per-attempt timeout, restored afterwards whatever happens."""
    old = (config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S)
    config.MAX_RETRIES = 0
    config.ATTEMPT_TIMEOUT_S = float(rule["attempt_timeout_s"])
    try:
        yield
    finally:
        config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S = old


class TimedTransport:
    """Wraps a transport and times each ``post`` on the client side (``Result.latency_ms`` also counts local work)."""

    def __init__(self, inner, clock=time.monotonic):
        self.inner, self.clock, self.records = inner, clock, []

    def post(self, url, headers, body, timeout):
        t0, timed_out = self.clock(), False
        try:
            return self.inner.post(url, headers, body, timeout)
        except TransportTimeout:
            timed_out = True
            raise
        finally:
            self.records.append({"latency_s": self.clock() - t0, "timed_out": timed_out})


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _ask(client, timed, prompt):
    n0 = len(timed.records)
    res = client.ask({"prompt": prompt["text"]}, questions.build_questions(), case_id=prompt["id"],
                     qset_version=questions.QSET_VERSION, data_classes=["public"], purpose="issue611")
    return res, _attempt(timed, n0, res.status, res.error, res.latency_ms / 1000)


def _attempt(timed, n0, status, error, local_s):
    rec = timed.records[n0] if len(timed.records) > n0 else None
    return {"status": status, "error": error, "latency_s": rec["latency_s"] if rec else local_s,
            "timed_out": bool(rec and rec["timed_out"])}


def _row(prompt, attempts, res):
    ok = res is not None and res.status == "ok"
    pt = res.answers["problem_type"] if ok else None
    return {"prompt_id": prompt["id"], "attempts": attempts, "final_status": "ok" if ok else "error",
            "choice": pt["choice"] if ok else None, "probs": pt["probs"] if ok else None,
            "noul": res.answers["any_type_fits"]["p"] if ok else None, "model": res.model if ok else None}


def execute(paths, rule, corpus, run_id, transport, price, live=True):
    """One run, the gates already checked by the caller.  Returns the facts of the ``run_end`` event."""
    if not loader.is_plain_name(run_id):
        raise ValueError("the run id may hold only letters, digits, dot, underscore and hyphen")
    phase = f"issue611-{run_id}"
    run_dir = paths.runs / run_id
    run_dir.mkdir(parents=True)
    rows_path, journal_path = run_dir / "jev-rows.jsonl", run_dir / "journal.jsonl"
    rows_path.touch()
    journal_path.touch()
    qs = questions.build_questions()
    whole = spend.estimate_run_tokens([build_request({"prompt": r["text"]}, qs) for r in corpus])
    budget = Budget(paths.ledger, ceiling_usd=rule["spend_cap_usd"],
                    ceiling_input_tokens=spend.ceiling_tokens(rule["spend_cap_usd"], price))
    started, stop, rows = _utc(), None, []
    timed = TimedTransport(transport)
    try:
        try:
            budget.reserve_phase(phase, whole)
        except BudgetExhausted:
            stop = "spend_bound"
        if stop is None:
            events.append_event(paths, "first_request", run_id=run_id, prompts=len(corpus), whole_run_tokens=whole)
            with limits(rule):
                client = JevClient(experiment="issue611", phase=phase, budget=budget, journal=Journal(journal_path),
                                   transport=timed, live=live)
                for prompt in corpus:
                    attempts, res = [], None
                    for _ in range(2):                                   # the first attempt and at most one rerun
                        n0 = len(timed.records)
                        try:
                            res, att = _ask(client, timed, prompt)
                        except KeyMissing:
                            stop = "key_missing"
                            break
                        except KeyRejected:
                            res, stop = None, "key_rejected"
                            attempts.append(_attempt(timed, n0, "key_rejected", "http_401_or_403", 0.0))
                            break
                        attempts.append(att)
                        stop = SYSTEMIC.get((res.status, res.error))
                        if res.status == "ok" or stop:
                            break
                    if attempts:
                        row = _row(prompt, attempts, res)
                        rows.append(row)
                        with open(rows_path, "a", encoding="utf-8") as f:
                            f.write(json.dumps(row, sort_keys=True) + "\n")
                    if stop:
                        break
    except Exception as e:                                               # still write the run record and the run_end event
        stop = "crashed_" + type(e).__name__
    finally:
        budget.release_phase(phase)
    return _finish(paths, rule, run_id, price, started, stop or "completed", len(corpus), rows, budget, rows_path, journal_path)


def _finish(paths, rule, run_id, price, started, reason, n_prompts, rows, budget, rows_path, journal_path):
    state = budget.state()
    ok = [r for r in rows if r["final_status"] == "ok"]
    attempts = sum(len(r["attempts"]) for r in rows)
    spent_usd = spend.worst_case_usd(state["spent_tokens"], price)
    models = sorted({r["model"] for r in ok})
    record = paths.runs / run_id / "run-record.md"
    record.write_text("\n".join([
        f"# Run record: {run_id}", "", f"- Started (UTC): {started}", f"- Ended (UTC): {_utc()}", f"- Ended with: {reason}",
        f"- Prompts: {n_prompts}; with a row: {len(rows)}; attempts: {attempts}; ok: {len(ok)}; error: {len(rows) - len(ok)}",
        f"- Ledger: spent {state['spent_tokens']} input tokens, ceiling {state['ceiling_input_tokens']}, reserved {state['reserved']}",
        f"- Spent at the confirmed price: {spent_usd:.6f} USD (price {price} USD per million input tokens)",
        f"- Models returned: {', '.join(models) or 'none'}", f"- Rule file SHA-256: {loader.sha256_file(paths.rule)}",
        f"- jev-rows.jsonl SHA-256: {loader.sha256_file(rows_path)}", f"- journal.jsonl SHA-256: {loader.sha256_file(journal_path)}",
        f"- Per-call timeout: {rule['attempt_timeout_s']} s", ""]), encoding="utf-8")
    events.append_event(paths, "run_end", evidence=record, run_id=run_id, reason=reason, prompts=n_prompts, attempts=attempts,
                        ok=len(ok), error=len(rows) - len(ok), spent_tokens=state["spent_tokens"], spent_usd=spent_usd)
    return {"reason": reason, "prompts": n_prompts, "rows": len(rows), "ok": len(ok), "spent_usd": spent_usd}


def rehearse(paths, out_dir, transport=None):
    """Build, screen and budget every request with ``live=False`` against a throwaway ledger in ``out_dir``.  Nothing is posted."""
    out = pathlib.Path(out_dir).resolve()
    for guarded in (paths.ledger.parent, paths.runs):
        g = guarded.resolve()
        if out == g or g in out.parents:
            raise ValueError(f"--out must not be inside {guarded.name}/")
    rule = loader.load_rule(paths.rule)
    corpus = loader.load_corpus(paths.corpus)
    qs = questions.build_questions()
    estimate = spend.estimate_run_tokens([build_request({"prompt": r["text"]}, qs) for r in corpus])
    out.mkdir(parents=True, exist_ok=True)
    budget = Budget(out / "ledger.json", ceiling_usd=rule["spend_cap_usd"],
                    ceiling_input_tokens=spend.ceiling_tokens(rule["spend_cap_usd"], config.PRICE_USD_PER_MTOK_INPUT))
    client = JevClient(experiment="issue611", phase="issue611-rehearsal", budget=budget, journal=Journal(out / "journal.jsonl"),
                       transport=transport, live=False)
    refused = 0
    for prompt in corpus:
        res = client.ask({"prompt": prompt["text"]}, qs, case_id=prompt["id"], qset_version=questions.QSET_VERSION,
                         data_classes=["public"], purpose="issue611")
        refused += (res.status, res.error) == ("refused", "dry_run")
    return {"prompts": len(corpus), "dry_run_refusals": refused, "whole_run_estimate_tokens": estimate}


def _run_command(paths, args, transport):
    if not args.live:
        print("REFUSED: run needs --live", file=sys.stderr)
        return 2
    if not loader.is_plain_name(args.run_id):
        print("REFUSED: the run id may hold only letters, digits, dot, underscore and hyphen", file=sys.stderr)
        return 2
    if (paths.runs / args.run_id).exists():
        print(f"REFUSED: runs/{args.run_id} already exists", file=sys.stderr)
        return 2
    failed = gate.gate1(paths)
    if failed:
        print("GATE 1 FAILED: " + ",".join(failed), file=sys.stderr)
        return 1
    failed = gate.gate2(paths)
    if failed:
        print("GATE 2 FAILED: " + ",".join(failed), file=sys.stderr)
        return 1
    key = os.environ.get(KEY_ENV_SOURCE)
    if not key:
        print(f"REFUSED: {KEY_ENV_SOURCE} is not set", file=sys.stderr)
        return 1
    os.environ[config.KEY_ENV] = key
    rule = loader.load_rule(paths.rule, for_scoring=True)
    corpus = loader.load_corpus(paths.corpus)
    price = events.latest(paths, "price_confirmed")["usd_per_mtok"]
    out = execute(paths, rule, corpus, args.run_id, transport or UrllibTransport(), price)
    print(json.dumps(out, sort_keys=True))
    return 0 if out["reason"] == "completed" else 1


def main(argv=None, transport=None):
    ap = argparse.ArgumentParser(prog="runner.py", description="run the Jev comparison live, or rehearse it without posting")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run live: both gates, then the key, then the prompts")
    r.add_argument("--run-id", required=True)
    r.add_argument("--live", action="store_true")
    h = sub.add_parser("rehearse", help="dry run against a throwaway ledger; no gate, no key, no post")
    h.add_argument("--out", required=True)
    for p in (r, h):
        p.add_argument("--root", default=None)
    args = ap.parse_args(argv)
    paths = loader.Paths(args.root)
    try:
        if args.cmd == "run":
            return _run_command(paths, args, transport)
        print(json.dumps(rehearse(paths, args.out), sort_keys=True))
        return 0
    except (loader.LoadError, ValueError) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
