c44fc2899c2e2af9f55804273ad294cab0302ec6
Review one task for spec compliance.

Task brief: ## Task 6: Build the runner on `JevClient`

Depends on: Task 1, Task 2, Task 4

Create `.dev/research/jev-vs-keyword-table-611/harness/runner.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py`. The runner imports `JevClient`, `KeyMissing` and `KeyRejected` from `jevlib.client`, `Budget` and `BudgetExhausted` from `jevlib.budget`, `Journal` from `jevlib.journal`, `UrllibTransport`, `TransportTimeout` and `TransportError` from `jevlib.transport`, and `jevlib.config` as a module; the questions come from `questions.py`.

A context manager `limits(rule)` sets `config.MAX_RETRIES = 0` and `config.ATTEMPT_TIMEOUT_S` to the rule's `attempt_timeout_s` and restores both in a `finally`. A small timing class wraps the transport and records `time.monotonic()` around each `post` and whether it timed out, because `Result.latency_ms` also counts local work.

A core function `execute(paths, rule, corpus, run_id, transport, price)` runs one live run with the gates already checked by its caller, so tests can call it twice against one temporary ledger. Its steps are, in order:
- Compute the whole-run estimate with `spend.estimate_run_tokens` over the requests built from the frozen prompts, build the `Budget` at the ledger of `Paths` with `ceiling_usd` from the rule's `spend_cap_usd` and `ceiling_input_tokens` from `spend.ceiling_tokens` at the confirmed price, and call `budget.reserve_phase(phase, whole_run_tokens)` with `phase` equal to `issue611-<run_id>`, the same string given to `JevClient`. A `BudgetExhausted` there ends the run before any post with the reason `spend_bound`. The reservation is released with `budget.release_phase(phase)` in a `finally`.
- Append the `first_request` event, then handle prompts in corpus order, one at a time: build the state `{"prompt": text}` and call `client.ask(state, build_questions(), case_id=<prompt id>, qset_version=QSET_VERSION, data_classes=["public"], purpose="issue611")`.
- Stop the run with no rerun, and record the systemic reason, on the exceptions `KeyMissing` and `KeyRejected`, on a result with status `refused` and error `budget_exhausted`, on status `invalid` with error `model_mismatch`, and on status `refused` with error `dry_run`. On any other non-`ok` result make exactly one more `ask` for that prompt (a new logical call id). A second non-`ok` result makes the prompt an `error`. The model-pin check applies only to `ok` results, since every non-`ok` result has `model` of `None`.
- Every attempt is journaled to `runs/<run-id>/journal.jsonl` and drawn from the one cumulative ledger. Each prompt writes one row to `runs/<run-id>/jev-rows.jsonl` with the attempts (status, error, measured latency, timed-out flag), the final status, the choice and its probabilities, the Noul value and the returned model.
- At the end, also after a stop, write `runs/<run-id>/run-record.md` (run id, start and end in UTC, the stop reason or `completed`, the counts of prompts, attempts, `ok` and `error`, the ledger state, the models returned, the confirmed price, the rule's hash, and the SHA-256 of the rows and journal files) and append the `run_end` event. Neither file holds the key.

The command line has two subcommands, each taking `--root`:
- `run --run-id ID --live`: refuses to start (exit 2, nothing read) without `--live` or when `runs/<run-id>` exists. It then checks Gate 1 and Gate 2 and reads no environment variable before both pass. Only then does it read `TYPESAFE_API_KEY`, copy it into `JEV_API_KEY` in memory, load the corpus, read the latest `price_confirmed` event and call `execute`. It prints nothing about the key.
- `rehearse --out DIR`: never posts, needs no gate and no key, and refuses a `DIR` inside the experiment's `ledger/` or `runs/` folders. It runs the client with `live=False` against a throwaway ledger in `DIR`, so every request ends `refused`/`dry_run` before any transport call, and prints the prompt count and the whole-run estimate. It writes nothing to the events file, the real ledger or `runs/`.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py -v` passes using `MockTransport`, `fake_answer` and a temporary root only.
- Tests show a failed first attempt gets exactly one rerun, both attempts appear in the journal and the ledger, and a prompt that fails twice is recorded as `error` (T-06); the mock sees exactly two posts for a twice-failed prompt, so the client never retries by itself.
- Tests show each systemic signal ends the run with its reason and no rerun: zero posts for a missing key (`KeyMissing`); zero posts for the `spend_bound` refusal of a ledger too small for the whole-run estimate (the run ends before any post with reason `spend_bound`); one post for an HTTP 401 (`KeyRejected`) and one post for a returned model id other than `jev-1.14.0` (`invalid`/`model_mismatch`), both with no rerun; the result `refused`/`budget_exhausted`, injected through a stand-in ledger or client in a unit test, stops the run with no rerun; and a timeout is rerun and is not a stop (T-13) (finding M-1).
- Tests show a ledger where every request fits but the whole-run estimate does not gives zero posts, a `run_end` event with reason `spend_bound` and an empty `reserved` map afterwards; that a completed run also leaves `reserved` empty; and that spend carries across two run ids through the one ledger (T-09).
- Tests show a confirmed price higher than the jevlib constant lowers the token ceiling passed to `Budget`.
- Tests show that with an `os.environ` replaced by a recorder, a failing gate leaves `TYPESAFE_API_KEY`, `JEV_API_KEY` and `JEV_API_URL` unread (which also covers the direct read inside `privacy_violation`), and that `run` without `--live` exits 2 before checking any gate (T-03).
- A test shows `limits(rule)` restores `config.MAX_RETRIES` to 1 and `config.ATTEMPT_TIMEOUT_S` to 20.0 on exit, also after an exception.
- A test shows `rehearse` calls a transport that fails on any call zero times, leaves the real events file, ledger and `runs/` unchanged, and refuses a `DIR` under `ledger/`.
- A test sets a fake key, runs `execute` against a mock whose error text contains that key, then runs `keyscan.py --fake <value>` with explicit paths on the run folder, `events.jsonl`, `manifest.json` and the ledger and sees `KEYSCAN OK` and no occurrence of the value in any written file (T-10).
- `run-record.md` exists after a completed run and after a stopped run, and `runner.py` contains no `http://` or `https://` literal (the endpoint comes from `jevlib.config.api_url()`).
- No file under the `jevlib` folder is changed; its 31 importers (the experiments under `p15` and later folders) are untouched.

Acceptance criterion ids (in source order):
T6.AC1: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py -v` passes using `MockTransport`, `fake_answer` and a temporary root only.
T6.AC2: Tests show a failed first attempt gets exactly one rerun, both attempts appear in the journal and the ledger, and a prompt that fails twice is recorded as `error` (T-06); the mock sees exactly two posts for a twice-failed prompt, so the client never retries by itself.
T6.AC3: Tests show each systemic signal ends the run with its reason and no rerun: zero posts for a missing key (`KeyMissing`); zero posts for the `spend_bound` refusal of a ledger too small for the whole-run estimate (the run ends before any post with reason `spend_bound`); one post for an HTTP 401 (`KeyRejected`) and one post for a returned model id other than `jev-1.14.0` (`invalid`/`model_mismatch`), both with no rerun; the result `refused`/`budget_exhausted`, injected through a stand-in ledger or client in a unit test, stops the run with no rerun; and a timeout is rerun and is not a stop (T-13) (finding M-1).
T6.AC4: Tests show a ledger where every request fits but the whole-run estimate does not gives zero posts, a `run_end` event with reason `spend_bound` and an empty `reserved` map afterwards; that a completed run also leaves `reserved` empty; and that spend carries across two run ids through the one ledger (T-09).
T6.AC5: Tests show a confirmed price higher than the jevlib constant lowers the token ceiling passed to `Budget`.
T6.AC6: Tests show that with an `os.environ` replaced by a recorder, a failing gate leaves `TYPESAFE_API_KEY`, `JEV_API_KEY` and `JEV_API_URL` unread (which also covers the direct read inside `privacy_violation`), and that `run` without `--live` exits 2 before checking any gate (T-03).
T6.AC7: A test shows `limits(rule)` restores `config.MAX_RETRIES` to 1 and `config.ATTEMPT_TIMEOUT_S` to 20.0 on exit, also after an exception.
T6.AC8: A test shows `rehearse` calls a transport that fails on any call zero times, leaves the real events file, ledger and `runs/` unchanged, and refuses a `DIR` under `ledger/`.
T6.AC9: A test sets a fake key, runs `execute` against a mock whose error text contains that key, then runs `keyscan.py --fake <value>` with explicit paths on the run folder, `events.jsonl`, `manifest.json` and the ledger and sees `KEYSCAN OK` and no occurrence of the value in any written file (T-10).
T6.AC10: `run-record.md` exists after a completed run and after a stopped run, and `runner.py` contains no `http://` or `https://` literal (the endpoint comes from `jevlib.config.api_url()`).
T6.AC11: No file under the `jevlib` folder is changed; its 31 importers (the experiments under `p15` and later folders) are untouched.
Global constraints: ## Constraints

- Scope is build and test only. No task sends a prompt to TypeSafe, reads `TYPESAFE_API_KEY` or `JEV_API_KEY` from the real environment, or opens a network connection. Tests use `MockTransport` and a socket guard, set a fake key with `monkeypatch.setenv`, and use a temporary experiment root for every file the gates, events, runner and scorer write. The live run is a coordinator action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md` (lines 145 to 165).
- Left for a person or the coordinator, not in this plan: choosing and labelling about 30 public prompts (a named human labeller is required), applying the keyword table to them (a session or person who sees prompts only, after Gate 1), the live run with `keyscan.py`, scoring and the report, and the updates on issues 611, 609 and 612. Tasks 7 and 8 produce the procedures, templates and instructions those steps need. The pull request that delivers this plan says `Refs #611` and lists parts B to E of section 8 of the design as left (Task 8 puts that sentence in the README).
- Nothing under `src/`, `tests/`, `.claude/` or the existing `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` folder is changed. `jevlib` is imported read-only, and only from its submodules (`client`, `budget`, `journal`, `transport`, `questions`, `manifest`, `config`), because `jevlib/__init__.py` exports only `MODEL`, `API_URL` and `KEY_ENV`.
- Spend cap is 1 dollar in total; public prompts only; the key is never printed, logged, written to a file, put on a command line or put in a pull request. The runner copies `TYPESAFE_API_KEY` into `JEV_API_KEY` inside its own process only, because `jevlib.config.KEY_ENV` is `JEV_API_KEY`.
- Agreed decision rule (AGREED 2026-11-26 by the IronFlow session and the build agent, relayed by the lead; Clay's own words as quoted by the IronFlow session, not typed by Clay: "you and the agent debate whats correct way to handle this and do it").
- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. Per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
- Still open, so written as `UNSET` in the rule file: the operators at exactly 0.3 and 0.7 for the Noul band, and the count of unresolved failures that makes a run invalid. Gate 1 accepts `UNSET` and does not freeze the rule file's hash. The scorer, the `freeze-rule` command and Gate 2 refuse any `UNSET` value, and `freeze-rule` is the step that freezes the rule file's hash after the owner has filled the fields.
- The real client behaves differently from a mock-backed dry run: `JevClient` with `live=False` builds, screens and budgets the request, then returns `refused` with error `dry_run` before any transport call. So the runner has two subcommands: `run` needs `--live`, both gates and the key; `rehearse` never posts and needs no gate and no key. Tests that need the transport path use `live=True`, an injected `MockTransport` and a fake `JEV_API_KEY`.
- Test run command, recorded by `gate.py record-tests`: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`. The repository's `testpaths` is `tests`, so tests under `.dev/` are only collected when this path is given.
- Each of the four command-line modules (`gate.py`, `events.py`, `runner.py` and `scorer.py`) inserts the existing `jevlib` folder and the experiment folder into `sys.path` itself, as `.dev/research/346-review-loop-experiments/p15/jev/probe.py` does (read-only reference), because only `conftest.py` does so for tests (finding M-12).
Start sha: c44fc2899c2e2af9f55804273ad294cab0302ec6
Diff against the start snapshot: diff --git a/.dev/research/jev-vs-keyword-table-611/harness/runner.py b/.dev/research/jev-vs-keyword-table-611/harness/runner.py
new file mode 100644
index 000000000..2f2fef806
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/runner.py
@@ -0,0 +1,246 @@
+"""The runner: one live run of the Jev comparison on ``JevClient``, and a rehearsal that never posts.
+
+Command line (each takes ``--root``, the experiment folder by default):
+  runner.py run --run-id ID --live     check Gate 1 and Gate 2, then read TYPESAFE_API_KEY and run; refuses without --live
+  runner.py rehearse --out DIR         build and budget every request against a throwaway ledger in DIR; no gate, no key, no post
+
+``run`` reads no environment variable before both gates pass.  Only then is ``TYPESAFE_API_KEY`` copied into ``JEV_API_KEY`` inside
+this process (``jevlib.config.KEY_ENV`` is ``JEV_API_KEY``); the key is never printed or written.  The live run is a coordinator
+action, not part of the build.
+"""
+import argparse
+import contextlib
+import datetime
+import json
+import os
+import pathlib
+import sys
+import time
+
+_EXP = pathlib.Path(__file__).resolve().parents[1]
+_JEV = _EXP.parent / "346-review-loop-experiments" / "p15" / "jev"
+for _p in (str(_EXP), str(_JEV)):
+    if _p not in sys.path:
+        sys.path.insert(0, _p)
+
+import questions  # noqa: E402
+from jevlib import config  # noqa: E402
+from jevlib.budget import Budget, BudgetExhausted  # noqa: E402
+from jevlib.client import JevClient, KeyMissing, KeyRejected  # noqa: E402
+from jevlib.journal import Journal  # noqa: E402
+from jevlib.questions import build_request  # noqa: E402
+from jevlib.transport import TransportTimeout, UrllibTransport  # noqa: E402
+
+from harness import events, gate, loader, spend  # noqa: E402
+
+# (result status, result error) -> the systemic reason that ends the run with no rerun
+SYSTEMIC = {("refused", "budget_exhausted"): "budget_exhausted", ("invalid", "model_mismatch"): "model_mismatch",
+            ("refused", "dry_run"): "dry_run"}
+KEY_ENV_SOURCE = "TYPESAFE_API_KEY"
+
+
+@contextlib.contextmanager
+def limits(rule):
+    """No retry inside the client and the rule's per-attempt timeout, restored afterwards whatever happens."""
+    old = (config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S)
+    config.MAX_RETRIES = 0
+    config.ATTEMPT_TIMEOUT_S = float(rule["attempt_timeout_s"])
+    try:
+        yield
+    finally:
+        config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S = old
+
+
+class TimedTransport:
+    """Wraps a transport and times each ``post`` on the client side (``Result.latency_ms`` also counts local work)."""
+
+    def __init__(self, inner, clock=time.monotonic):
+        self.inner, self.clock, self.records = inner, clock, []
+
+    def post(self, url, headers, body, timeout):
+        t0, timed_out = self.clock(), False
+        try:
+            return self.inner.post(url, headers, body, timeout)
+        except TransportTimeout:
+            timed_out = True
+            raise
+        finally:
+            self.records.append({"latency_s": self.clock() - t0, "timed_out": timed_out})
+
+
+def _utc():
+    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
+
+
+def _ask(client, timed, prompt):
+    n0 = len(timed.records)
+    res = client.ask({"prompt": prompt["text"]}, questions.build_questions(), case_id=prompt["id"],
+                     qset_version=questions.QSET_VERSION, data_classes=["public"], purpose="issue611")
+    return res, _attempt(timed, n0, res.status, res.error, res.latency_ms / 1000)
+
+
+def _attempt(timed, n0, status, error, local_s):
+    rec = timed.records[n0] if len(timed.records) > n0 else None
+    return {"status": status, "error": error, "latency_s": rec["latency_s"] if rec else local_s,
+            "timed_out": bool(rec and rec["timed_out"])}
+
+
+def _row(prompt, attempts, res):
+    ok = res is not None and res.status == "ok"
+    pt = res.answers["problem_type"] if ok else None
+    return {"prompt_id": prompt["id"], "attempts": attempts, "final_status": "ok" if ok else "error",
+            "choice": pt["choice"] if ok else None, "probs": pt["probs"] if ok else None,
+            "noul": res.answers["any_type_fits"]["p"] if ok else None, "model": res.model if ok else None}
+
+
+def execute(paths, rule, corpus, run_id, transport, price, live=True):
+    """One run, the gates already checked by the caller.  Returns the facts of the ``run_end`` event."""
+    phase = f"issue611-{run_id}"
+    run_dir = paths.runs / run_id
+    run_dir.mkdir(parents=True)
+    rows_path, journal_path = run_dir / "jev-rows.jsonl", run_dir / "journal.jsonl"
+    rows_path.touch()
+    journal_path.touch()
+    qs = questions.build_questions()
+    whole = spend.estimate_run_tokens([build_request({"prompt": r["text"]}, qs) for r in corpus])
+    budget = Budget(paths.ledger, ceiling_usd=rule["spend_cap_usd"],
+                    ceiling_input_tokens=spend.ceiling_tokens(rule["spend_cap_usd"], price))
+    started, stop, rows = _utc(), None, []
+    timed = TimedTransport(transport)
+    try:
+        try:
+            budget.reserve_phase(phase, whole)
+        except BudgetExhausted:
+            stop = "spend_bound"
+        if stop is None:
+            events.append_event(paths, "first_request", run_id=run_id, prompts=len(corpus), whole_run_tokens=whole)
+            with limits(rule):
+                client = JevClient(experiment="issue611", phase=phase, budget=budget, journal=Journal(journal_path),
+                                   transport=timed, live=live)
+                for prompt in corpus:
+                    attempts, res = [], None
+                    for _ in range(2):                                   # the first attempt and at most one rerun
+                        n0 = len(timed.records)
+                        try:
+                            res, att = _ask(client, timed, prompt)
+                        except KeyMissing:
+                            stop = "key_missing"
+                            break
+                        except KeyRejected:
+                            res, stop = None, "key_rejected"
+                            attempts.append(_attempt(timed, n0, "key_rejected", "http_401_or_403", 0.0))
+                            break
+                        attempts.append(att)
+                        stop = SYSTEMIC.get((res.status, res.error))
+                        if res.status == "ok" or stop:
+                            break
+                    if attempts:
+                        row = _row(prompt, attempts, res)
+                        rows.append(row)
+                        with open(rows_path, "a", encoding="utf-8") as f:
+                            f.write(json.dumps(row, sort_keys=True) + "\n")
+                    if stop:
+                        break
+    except Exception as e:                                               # still write the run record and the run_end event
+        stop = "crashed_" + type(e).__name__
+    finally:
+        budget.release_phase(phase)
+    return _finish(paths, rule, run_id, price, started, stop or "completed", len(corpus), rows, budget, rows_path, journal_path)
+
+
+def _finish(paths, rule, run_id, price, started, reason, n_prompts, rows, budget, rows_path, journal_path):
+    state = budget.state()
+    ok = [r for r in rows if r["final_status"] == "ok"]
+    attempts = sum(len(r["attempts"]) for r in rows)
+    spent_usd = spend.worst_case_usd(state["spent_tokens"], price)
+    models = sorted({r["model"] for r in ok})
+    record = paths.runs / run_id / "run-record.md"
+    record.write_text("\n".join([
+        f"# Run record: {run_id}", "", f"- Started (UTC): {started}", f"- Ended (UTC): {_utc()}", f"- Ended with: {reason}",
+        f"- Prompts: {n_prompts}; with a row: {len(rows)}; attempts: {attempts}; ok: {len(ok)}; error: {len(rows) - len(ok)}",
+        f"- Ledger: spent {state['spent_tokens']} input tokens, ceiling {state['ceiling_input_tokens']}, reserved {state['reserved']}",
+        f"- Spent at the confirmed price: {spent_usd:.6f} USD (price {price} USD per million input tokens)",
+        f"- Models returned: {', '.join(models) or 'none'}", f"- Rule file SHA-256: {loader.sha256_file(paths.rule)}",
+        f"- jev-rows.jsonl SHA-256: {loader.sha256_file(rows_path)}", f"- journal.jsonl SHA-256: {loader.sha256_file(journal_path)}",
+        f"- Per-call timeout: {rule['attempt_timeout_s']} s", ""]), encoding="utf-8")
+    events.append_event(paths, "run_end", evidence=record, run_id=run_id, reason=reason, prompts=n_prompts, attempts=attempts,
+                        ok=len(ok), error=len(rows) - len(ok), spent_tokens=state["spent_tokens"], spent_usd=spent_usd)
+    return {"reason": reason, "prompts": n_prompts, "rows": len(rows), "ok": len(ok), "spent_usd": spent_usd}
+
+
+def rehearse(paths, out_dir, transport=None):
+    """Build, screen and budget every request with ``live=False`` against a throwaway ledger in ``out_dir``.  Nothing is posted."""
+    out = pathlib.Path(out_dir).resolve()
+    for guarded in (paths.ledger.parent, paths.runs):
+        g = guarded.resolve()
+        if out == g or g in out.parents:
+            raise ValueError(f"--out must not be inside {guarded.name}/")
+    rule = loader.load_rule(paths.rule)
+    corpus = loader.load_corpus(paths.corpus)
+    qs = questions.build_questions()
+    estimate = spend.estimate_run_tokens([build_request({"prompt": r["text"]}, qs) for r in corpus])
+    out.mkdir(parents=True, exist_ok=True)
+    budget = Budget(out / "ledger.json", ceiling_usd=rule["spend_cap_usd"],
+                    ceiling_input_tokens=spend.ceiling_tokens(rule["spend_cap_usd"], config.PRICE_USD_PER_MTOK_INPUT))
+    client = JevClient(experiment="issue611", phase="issue611-rehearsal", budget=budget, journal=Journal(out / "journal.jsonl"),
+                       transport=transport, live=False)
+    refused = 0
+    for prompt in corpus:
+        res = client.ask({"prompt": prompt["text"]}, qs, case_id=prompt["id"], qset_version=questions.QSET_VERSION,
+                         data_classes=["public"], purpose="issue611")
+        refused += (res.status, res.error) == ("refused", "dry_run")
+    return {"prompts": len(corpus), "dry_run_refusals": refused, "whole_run_estimate_tokens": estimate}
+
+
+def _run_command(paths, args, transport):
+    if not args.live:
+        print("REFUSED: run needs --live", file=sys.stderr)
+        return 2
+    if (paths.runs / args.run_id).exists():
+        print(f"REFUSED: runs/{args.run_id} already exists", file=sys.stderr)
+        return 2
+    failed = gate.gate1(paths)
+    if failed:
+        print("GATE 1 FAILED: " + ",".join(failed), file=sys.stderr)
+        return 1
+    failed = gate.gate2(paths)
+    if failed:
+        print("GATE 2 FAILED: " + ",".join(failed), file=sys.stderr)
+        return 1
+    key = os.environ.get(KEY_ENV_SOURCE)
+    if not key:
+        print(f"REFUSED: {KEY_ENV_SOURCE} is not set", file=sys.stderr)
+        return 1
+    os.environ[config.KEY_ENV] = key
+    rule = loader.load_rule(paths.rule, for_scoring=True)
+    corpus = loader.load_corpus(paths.corpus)
+    price = events.latest(paths, "price_confirmed")["usd_per_mtok"]
+    out = execute(paths, rule, corpus, args.run_id, transport or UrllibTransport(), price)
+    print(json.dumps(out, sort_keys=True))
+    return 0 if out["reason"] == "completed" else 1
+
+
+def main(argv=None, transport=None):
+    ap = argparse.ArgumentParser(prog="runner.py", description="run the Jev comparison live, or rehearse it without posting")
+    sub = ap.add_subparsers(dest="cmd", required=True)
+    r = sub.add_parser("run", help="run live: both gates, then the key, then the prompts")
+    r.add_argument("--run-id", required=True)
+    r.add_argument("--live", action="store_true")
+    h = sub.add_parser("rehearse", help="dry run against a throwaway ledger; no gate, no key, no post")
+    h.add_argument("--out", required=True)
+    for p in (r, h):
+        p.add_argument("--root", default=None)
+    args = ap.parse_args(argv)
+    paths = loader.Paths(args.root)
+    try:
+        if args.cmd == "run":
+            return _run_command(paths, args, transport)
+        print(json.dumps(rehearse(paths, args.out), sort_keys=True))
+        return 0
+    except (loader.LoadError, ValueError) as e:
+        print(f"REFUSED: {e}", file=sys.stderr)
+        return 2
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py
new file mode 100644
index 000000000..b09bb0662
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py
@@ -0,0 +1,329 @@
+import json
+import os
+import pathlib
+import subprocess
+import sys
+
+import pytest
+from conftest import FAKE_KEY
+from harness import events, gate, loader, runner, spend
+from jevlib import config
+from jevlib.budget import Budget, BudgetExhausted
+from jevlib.transport import MockStep, MockTransport, TransportTimeout, fake_answer
+
+KEYSCAN = loader.JEVLIB_DIR.parent / "keyscan.py"
+PASSING = lambda cmd: (0, "12 passed in 0.1s")  # noqa: E731
+
+
+def text(i):
+    return f"synthetic problem text number {i}"
+
+
+def mock(plan=None):
+    """A mock transport that answers every request validly; ``plan`` maps a prompt text to steps (or callables of the request)
+    returned first for that prompt."""
+    plan = {k: list(v) for k, v in (plan or {}).items()}
+
+    def script(req):
+        queue = plan.get(req["state"]["prompt"])
+        if queue:
+            step = queue.pop(0)
+            return step(req) if callable(step) else step
+        return MockStep(200, fake_answer(req))
+    return MockTransport(script)
+
+
+@pytest.fixture
+def exp(exp, monkeypatch):
+    """The command line builds ``Paths`` from a root alone, so point its default jevlib folder at the fixture's stand-in."""
+    monkeypatch.setattr(loader, "JEVLIB_DIR", exp.jevlib_dir)
+    return exp
+
+
+def go(exp, transport, run_id="r1", price=0.042):
+    rule = loader.load_rule(exp.rule)
+    return runner.execute(exp, rule, loader.load_corpus(exp.corpus), run_id, transport, price)
+
+
+def rows_of(exp, run_id="r1"):
+    return [json.loads(line) for line in (exp.runs / run_id / "jev-rows.jsonl").read_text().splitlines() if line.strip()]
+
+
+def ledger_of(exp):
+    return json.loads(exp.ledger.read_text())
+
+
+def gated(exp):
+    """Freeze everything and confirm the price and the go: the state in which ``runner.py run`` passes both gates."""
+    s = exp.rule.read_text(encoding="utf-8")
+    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
+    exp.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3"), encoding="utf-8")
+    gate.freeze_corpus(exp)
+    gate.freeze_table(exp)
+    gate.freeze_rule(exp)
+    events.append_event(exp, "price_confirmed", usd_per_mtok=0.042, source="test")
+    gate.record_tests(exp, runner=PASSING)
+    events.append_event(exp, "lead_go", rule_sha256=loader.sha256_file(exp.rule), words="go")
+
+
+# ---- one rerun per failed prompt (T-06)
+
+def test_a_failed_first_attempt_gets_exactly_one_rerun(exp, fake_key):
+    t = mock({text(0): [MockStep(500)]})
+    out = go(exp, t)
+    assert out["reason"] == "completed" and len(t.calls) == 9 and out["ok"] == 8
+    p0 = rows_of(exp)[0]
+    assert [a["status"] for a in p0["attempts"]] == ["unavailable", "ok"] and p0["final_status"] == "ok" and p0["model"] == config.MODEL
+    journal = [json.loads(line) for line in (exp.runs / "r1" / "journal.jsonl").read_text().splitlines()]
+    final_p0 = [j for j in journal if j["case_id"] == "p0" and j["final"]]
+    assert len({j["logical_call_id"] for j in final_p0}) == 2
+    assert len(ledger_of(exp)["draws"]) == 9
+
+
+def test_a_prompt_that_fails_twice_is_an_error_with_exactly_two_posts(exp, fake_key):
+    t = mock({text(0): [MockStep(500), MockStep(503)]})
+    out = go(exp, t)
+    assert out["reason"] == "completed" and out["ok"] == 7
+    assert len([c for c in t.calls if text(0).encode() in c[2]]) == 2 and len(t.calls) == 9
+    p0 = rows_of(exp)[0]
+    assert p0["final_status"] == "error" and len(p0["attempts"]) == 2 and p0["choice"] is None and p0["noul"] is None
+
+
+def test_a_timeout_is_rerun_and_is_not_a_stop(exp, fake_key):
+    t = mock({text(0): [MockStep(exc=TransportTimeout("slow"))]})
+    out = go(exp, t)
+    p0 = rows_of(exp)[0]
+    assert out["reason"] == "completed" and p0["attempts"][0]["timed_out"] is True and p0["attempts"][1]["status"] == "ok"
+    assert all(isinstance(a["latency_s"], float) for a in p0["attempts"])
+
+
+# ---- systemic signals end the run with no rerun (T-13, M-1)
+
+def test_a_missing_key_ends_the_run_with_zero_posts(exp, monkeypatch):
+    monkeypatch.delenv("JEV_API_KEY", raising=False)
+    t = mock()
+    out = go(exp, t)
+    assert out["reason"] == "key_missing" and t.calls == [] and rows_of(exp) == []
+    assert events.latest(exp, "run_end")["reason"] == "key_missing"
+
+
+def test_a_rejected_key_ends_the_run_after_one_post(exp, fake_key):
+    t = mock({text(0): [MockStep(401)]})
+    out = go(exp, t)
+    assert out["reason"] == "key_rejected" and len(t.calls) == 1
+    assert [r["final_status"] for r in rows_of(exp)] == ["error"] and rows_of(exp)[0]["attempts"][0]["status"] == "key_rejected"
+
+
+def test_a_returned_model_other_than_the_pin_ends_the_run_after_one_post(exp, fake_key):
+    t = mock({text(0): [lambda req: MockStep(200, dict(fake_answer(req), model="jev-9.9.9"))]})
+    out = go(exp, t)
+    assert out["reason"] == "model_mismatch" and len(t.calls) == 1 and len(rows_of(exp)) == 1
+
+
+def test_a_budget_exhausted_result_stops_the_run_with_no_rerun(exp, fake_key, monkeypatch):
+    class Stingy(Budget):
+        draws = 0
+
+        def draw(self, phase, est_tokens):
+            Stingy.draws += 1
+            if Stingy.draws > 2:
+                raise BudgetExhausted("stand-in ledger")
+            return super().draw(phase, est_tokens)
+
+    monkeypatch.setattr(runner, "Budget", Stingy)
+    t = mock()
+    out = go(exp, t)
+    assert out["reason"] == "budget_exhausted" and len(t.calls) == 2
+    last = rows_of(exp)[-1]
+    assert len(rows_of(exp)) == 3 and last["final_status"] == "error" and len(last["attempts"]) == 1
+
+
+# ---- the whole-run reservation (T-09)
+
+def run_estimate(exp):
+    import questions
+    from jevlib.questions import build_request
+    qs = questions.build_questions()
+    reqs = [build_request({"prompt": r["text"]}, qs) for r in loader.load_corpus(exp.corpus)]
+    return spend.estimate_run_tokens(reqs), max(spend.estimate_request_tokens(r) for r in reqs)
+
+
+def test_a_ledger_where_every_request_fits_but_the_whole_run_does_not_gives_zero_posts(exp, fake_key):
+    total, biggest = run_estimate(exp)
+    cap = spend.ceiling_tokens(1.0, 0.042)
+    left = total - 10
+    assert left > biggest
+    exp.ledger.parent.mkdir()
+    exp.ledger.write_text(json.dumps({"experiment": "spend", "ceiling_usd": 1.0, "ceiling_input_tokens": cap, "spent_tokens": cap - left,
+                                      "spent_usd": 0.0, "reserved": {}, "draws": {}}))
+    t = mock()
+    out = go(exp, t)
+    assert out["reason"] == "spend_bound" and t.calls == [] and ledger_of(exp)["reserved"] == {}
+    assert events.latest(exp, "run_end")["reason"] == "spend_bound" and events.latest(exp, "first_request") is None
+    assert (exp.runs / "r1" / "run-record.md").is_file()
+
+
+def test_a_completed_run_leaves_nothing_reserved_and_spend_carries_across_runs(exp, fake_key):
+    go(exp, mock(), run_id="r1")
+    one = ledger_of(exp)
+    assert one["reserved"] == {} and one["spent_tokens"] > 0
+    go(exp, mock(), run_id="r2")
+    two = ledger_of(exp)
+    assert two["reserved"] == {} and two["spent_tokens"] == 2 * one["spent_tokens"]
+
+
+def test_a_higher_confirmed_price_lowers_the_token_ceiling(exp, fake_key, monkeypatch):
+    seen = []
+
+    class Spy(Budget):
+        def __init__(self, path, **kw):
+            seen.append(kw)
+            super().__init__(path, **kw)
+
+    monkeypatch.setattr(runner, "Budget", Spy)
+    go(exp, mock(), price=0.084)
+    assert seen[0]["ceiling_input_tokens"] == spend.ceiling_tokens(1.0, 0.084)
+    assert seen[0]["ceiling_input_tokens"] < spend.ceiling_tokens(1.0, config.PRICE_USD_PER_MTOK_INPUT)
+
+
+# ---- limits, rehearsal, the command line
+
+def test_limits_set_and_restore_the_client_settings_also_after_an_exception():
+    rule = {"attempt_timeout_s": 10.0}
+    assert (config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S) == (1, 20.0)
+    with runner.limits(rule):
+        assert (config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S) == (0, 10.0)
+    with pytest.raises(RuntimeError), runner.limits(rule):
+        raise RuntimeError("boom")
+    assert (config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S) == (1, 20.0)
+
+
+class Recorder(dict):
+    """A stand-in for ``os.environ`` that records which names are read."""
+
+    def __init__(self, base):
+        super().__init__(base)
+        self.reads = []
+
+    def get(self, key, default=None):
+        self.reads.append(key)
+        return super().get(key, default)
+
+    def __getitem__(self, key):
+        self.reads.append(key)
+        return super().__getitem__(key)
+
+    def __contains__(self, key):
+        self.reads.append(key)
+        return super().__contains__(key)
+
+
+def test_a_failing_gate_leaves_the_key_and_url_variables_unread(exp, monkeypatch, capsys):
+    rec = Recorder(os.environ)
+    with monkeypatch.context() as m:
+        m.setattr(os, "environ", rec)
+        rc = runner.main(["run", "--run-id", "r1", "--live", "--root", str(exp.root)], transport=mock())
+    assert rc == 1 and "GATE 1 FAILED" in capsys.readouterr().err
+    assert not {"TYPESAFE_API_KEY", "JEV_API_KEY", "JEV_API_URL"} & set(rec.reads)
+    assert not (exp.runs / "r1").exists()
+
+
+def test_run_without_live_exits_two_before_any_gate(exp, capsys):
+    assert runner.main(["run", "--run-id", "r1", "--root", str(exp.root)]) == 2
+    assert "--live" in capsys.readouterr().err
+    assert not exp.events.exists()                                  # a gate would have written its event
+
+
+def test_run_refuses_an_existing_run_folder(exp, capsys):
+    (exp.runs / "r1").mkdir(parents=True)
+    assert runner.main(["run", "--run-id", "r1", "--live", "--root", str(exp.root)]) == 2
+    assert not exp.events.exists()
+
+
+def test_run_passes_the_gates_then_copies_the_key_and_never_prints_it(exp, monkeypatch, capsys):
+    gated(exp)
+    monkeypatch.setenv("JEV_API_KEY", "placeholder")               # so the test restores the variable afterwards
+    monkeypatch.setenv("TYPESAFE_API_KEY", FAKE_KEY)
+    t = mock()
+    assert runner.main(["run", "--run-id", "r1", "--live", "--root", str(exp.root)], transport=t) == 0
+    shown = capsys.readouterr()
+    assert FAKE_KEY not in shown.out + shown.err and os.environ["JEV_API_KEY"] == FAKE_KEY
+    assert [e["event"] for e in events.read_events(exp)][-4:] == ["gate1", "gate2", "first_request", "run_end"]
+    assert len(t.calls) == 8 and events.latest(exp, "run_end")["reason"] == "completed"
+    assert gate.gate2(exp) == ["prior_run"]                          # a second live run is refused
+    for f in exp.root.rglob("*"):
+        assert not f.is_file() or FAKE_KEY.encode() not in f.read_bytes(), f
+
+
+def test_run_without_a_key_refuses_after_the_gates(exp, monkeypatch, capsys):
+    gated(exp)
+    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
+    assert runner.main(["run", "--run-id", "r1", "--live", "--root", str(exp.root)], transport=mock()) == 1
+    assert "TYPESAFE_API_KEY is not set" in capsys.readouterr().err and not (exp.runs / "r1").exists()
+
+
+class Boom:
+    calls = 0
+
+    def post(self, *a, **k):
+        Boom.calls += 1
+        raise AssertionError("a rehearsal posted")
+
+
+def test_rehearse_never_posts_and_leaves_the_real_files_alone(exp, tmp_path):
+    out = runner.rehearse(exp, tmp_path / "rh", transport=Boom())
+    assert Boom.calls == 0 and out["prompts"] == 8 and out["dry_run_refusals"] == 8 and out["whole_run_estimate_tokens"] > 0
+    assert not exp.events.exists() and not exp.ledger.exists() and not exp.runs.exists()
+    assert (tmp_path / "rh" / "ledger.json").is_file()
+
+
+def test_rehearse_refuses_a_folder_under_the_ledger_or_runs(exp, capsys):
+    for bad in (exp.ledger.parent / "x", exp.runs, exp.runs / "y"):
+        assert runner.main(["rehearse", "--out", str(bad), "--root", str(exp.root)]) == 2
+        assert "must not be inside" in capsys.readouterr().err
+    assert not exp.ledger.parent.exists() and not exp.runs.exists()
+
+
+def test_rehearse_through_the_command_line_needs_no_gate_and_no_key(exp, tmp_path, monkeypatch, capsys):
+    monkeypatch.delenv("JEV_API_KEY", raising=False)
+    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
+    assert runner.main(["rehearse", "--out", str(tmp_path / "rh"), "--root", str(exp.root)]) == 0
+    assert json.loads(capsys.readouterr().out)["prompts"] == 8
+
+
+# ---- written files (T-10) and the run record
+
+def test_no_written_file_holds_the_key_even_when_an_error_body_quotes_it(exp, fake_key):
+    gated(exp)
+    t = mock({text(0): [MockStep(500, body=f"upstream rejected {FAKE_KEY} twice"), MockStep(500, body=FAKE_KEY)]})
+    out = go(exp, t)
+    assert out["reason"] == "completed"
+    paths = [str(exp.runs / "r1"), str(exp.events), str(exp.manifest), str(exp.ledger)]
+    res = subprocess.run([sys.executable, str(KEYSCAN), "--fake", FAKE_KEY, *paths], capture_output=True, text=True)
+    assert "KEYSCAN OK" in res.stdout and res.returncode == 0, res.stdout + res.stderr
+    assert "[REDACTED]" in (exp.runs / "r1" / "journal.jsonl").read_text()
+    assert FAKE_KEY not in res.stdout + res.stderr
+
+
+def test_the_run_record_exists_after_a_completed_and_after_a_stopped_run(exp, fake_key):
+    go(exp, mock(), run_id="done")
+    go(exp, mock({text(1): [MockStep(401)]}), run_id="stopped")
+    done = (exp.runs / "done" / "run-record.md").read_text(encoding="utf-8")
+    stopped = (exp.runs / "stopped" / "run-record.md").read_text(encoding="utf-8")
+    assert "Ended with: completed" in done and "Ended with: key_rejected" in stopped
+    assert loader.sha256_file(exp.runs / "done" / "jev-rows.jsonl") in done and config.MODEL in done
+    assert [e["reason"] for e in events.read_events(exp) if e["event"] == "run_end"] == ["completed", "key_rejected"]
+
+
+def test_an_unexpected_error_still_writes_the_run_record_and_the_run_end_event(exp, fake_key, monkeypatch):
+    def boom(*a, **k):
+        raise RuntimeError("unexpected")
+    monkeypatch.setattr(runner, "_ask", boom)
+    out = go(exp, mock())
+    assert out["reason"] == "crashed_RuntimeError" and (exp.runs / "r1" / "run-record.md").is_file()
+    assert ledger_of(exp)["reserved"] == {}
+
+
+def test_runner_holds_no_url_literal_and_posts_only_through_the_client():
+    src = pathlib.Path(runner.__file__).read_text(encoding="utf-8")
+    assert "http://" not in src and "https://" not in src


Codegraph context
index_state: fresh
checked_at: 2026-11-26T16:38:23Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the files of this task are new or only used by later tasks; no dependent outside the touched files.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
