223bda41860ac06ef72c4795b2dbcd2f457b9e3e
Review one task for spec compliance.

Task brief: ## Task 4: Build the spend estimates, the event log and the gates

Depends on: Task 2

Create `.dev/research/jev-vs-keyword-table-611/harness/spend.py`, `.dev/research/jev-vs-keyword-table-611/harness/events.py`, `.dev/research/jev-vs-keyword-table-611/harness/gate.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py`, and add to `conftest.py` a fixture `exp(tmp_path)` that builds a `loader.Paths` on a temporary root populated with small synthetic frozen files and a copy of the rule file.

`spend.py` (pure; the only code that estimates spend): `estimate_request_tokens(req)` is `ceil(len(canonical_bytes(req)) / RESERVE_BYTES_PER_TOKEN)`, the formula `JevClient.ask` uses (from `jevlib.questions` and `jevlib.config`); `estimate_run_tokens(requests)` is the sum over every request times 2 for the one allowed rerun; `ceiling_tokens(cap_usd, price_usd_per_mtok)` is `int(cap_usd / price * 1e6)`; `worst_case_usd(tokens, price)`.

`events.py` appends one JSON line per event to the events file of `Paths` (sorted keys, a UTC timestamp, the event name, an evidence path and the evidence file's SHA-256 through `loader.sha256_file`, plus event-specific fields). It never rewrites or deletes a line. Events: `owner_input_received`, `freeze`, `rule_freeze`, `gate1`, `gate2`, `tests_passed`, `price_confirmed`, `lead_go`, `first_request`, `run_end`, `scoring`, `verdict`. It provides `append_event`, `read_events` and `latest`. Its command line has `owner-input --evidence PATH --note TEXT`, `price --usd-per-mtok VALUE --source TEXT` and `go --words TEXT`; `go` records the rule file's current SHA-256 in the `lead_go` event. Every command takes `--root`.

`gate.py` owns the manifest and the gates. Its command line has six subcommands, each taking `--root`:
- `freeze-corpus`: runs `loader.load_corpus` (so the privacy screen runs), refuses on any failure, and writes the manifest keys `corpus`, `selection_criteria`, `labelling_record`, `questions` and `model_pin` (the hashes and `jev-1.14.0`), then a `freeze` event. It refuses when the manifest already holds these keys.
- `gate1`: reads the manifest and checks, returning the failed checks by name: `rule_missing`, `rule_status`, `rule_provenance_empty` (who, when or words empty), `manifest_missing`, `hash_corpus`, `hash_selection_criteria`, `hash_labelling_record`, `hash_questions`. It accepts `UNSET` values and never writes the manifest. It writes a `gate1` event and exits non-zero on a failure.
- `freeze-table`: refuses unless every Gate 1 check passes now and the table answers file and the provenance file exist; writes the manifest keys `table_answers` and `table_provenance` and a `freeze` event. It refuses when the manifest already holds these keys. (finding M-3)
- `freeze-rule`: loads the rule with `for_scoring=True` (refusing any `UNSET`), writes the manifest key `rule` and a `rule_freeze` event. It refuses when the manifest already holds this key. (finding M-3)
- `record-tests`: runs `uv run pytest <harness tests folder> -q` itself, refuses a non-zero exit or a count of zero, and writes a `tests_passed` event holding the command, the count and the SHA-256 of every file in `Paths.code_files()` and `Paths.jevlib_files()`. The function takes the runner of the command as a parameter so tests inject a fake.
- `gate2`: all Gate 1 checks plus `unset_value`, `rule_not_frozen`, `hash_rule`, `table_missing`, `table_provenance_missing`, `hash_table_answers`, `hash_table_provenance`, `tests_not_recorded`, `hash_code` (any code or `jevlib` file differs from the `tests_passed` event), `price_not_confirmed`, `spend_bound`, `go_missing`, `go_rule_hash` (the `lead_go` names a different rule hash than the current one) and `prior_run` (a `first_request` or `run_end` event already exists). `spend_bound` fails when `worst_case_usd` of the whole-run estimate at the confirmed price exceeds the rule's `spend_cap_usd`, or when the whole-run tokens exceed the ledger's remaining allowance. It writes a `gate2` event.

`gate1` and `gate2` hash files only and never call the corpus loader.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py -v` passes, using only the `exp` fixture's temporary root.
- Tests show Gate 1 refuses on `PROPOSED`, `PENDING`, an empty who, when or words, and a missing rule file, accepts a rule file with `UNSET` values, and either gate refuses on a hash mismatch for the corpus, questions, rule, table answers or any `jevlib` or code file (T-01 and T-02).
- Tests show Gate 2 refuses with no `lead_go` event, a `lead_go` naming an old rule hash, no `tests_passed` event, an `UNSET` value, no `rule_freeze`, no `price_confirmed`, and a `first_request` or `run_end` event already in the log (the second-run refusal), and passes on a complete synthetic setup (T-03).
- Tests show `spend_bound` fails when each request fits the ledger but the whole-run total does not, and when the worst-case dollars at a high confirmed price exceed the cap.
- Tests show the manifest bytes are unchanged after `gate1` and `gate2`, a second `freeze-corpus`, a second `freeze-table` and a second `freeze-rule` are each refused (finding M-3), `freeze-rule` refuses an `UNSET` value, `record-tests` refuses a failing or empty run (injected), and a test patches `loader.load_corpus` to raise and shows both gates still run.
- A test shows event lines are append-only and each carries a timestamp, an evidence path and a hash, that `go` writes the rule's current hash, and that the three `events.py` subcommands write their events.
- The real `events.jsonl`, `manifest.json` and ledger are unchanged by the test run (the autouse fixture of Task 1).

Acceptance criterion ids (in source order):
T4.AC1: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py -v` passes, using only the `exp` fixture's temporary root.
T4.AC2: Tests show Gate 1 refuses on `PROPOSED`, `PENDING`, an empty who, when or words, and a missing rule file, accepts a rule file with `UNSET` values, and either gate refuses on a hash mismatch for the corpus, questions, rule, table answers or any `jevlib` or code file (T-01 and T-02).
T4.AC3: Tests show Gate 2 refuses with no `lead_go` event, a `lead_go` naming an old rule hash, no `tests_passed` event, an `UNSET` value, no `rule_freeze`, no `price_confirmed`, and a `first_request` or `run_end` event already in the log (the second-run refusal), and passes on a complete synthetic setup (T-03).
T4.AC4: Tests show `spend_bound` fails when each request fits the ledger but the whole-run total does not, and when the worst-case dollars at a high confirmed price exceed the cap.
T4.AC5: Tests show the manifest bytes are unchanged after `gate1` and `gate2`, a second `freeze-corpus`, a second `freeze-table` and a second `freeze-rule` are each refused (finding M-3), `freeze-rule` refuses an `UNSET` value, `record-tests` refuses a failing or empty run (injected), and a test patches `loader.load_corpus` to raise and shows both gates still run.
T4.AC6: A test shows event lines are append-only and each carries a timestamp, an evidence path and a hash, that `go` writes the rule's current hash, and that the three `events.py` subcommands write their events.
T4.AC7: The real `events.jsonl`, `manifest.json` and ledger are unchanged by the test run (the autouse fixture of Task 1).
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
Start sha: 223bda41860ac06ef72c4795b2dbcd2f457b9e3e
Diff against the start snapshot: diff --git a/.dev/research/jev-vs-keyword-table-611/harness/spend.py b/.dev/research/jev-vs-keyword-table-611/harness/spend.py
new file mode 100644
index 000000000..a3b2d71de
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/spend.py
@@ -0,0 +1,28 @@
+"""Spend estimates: the only code that estimates tokens or turns a price and a cap into a ceiling.
+
+Pure.  The per-request estimate is the formula ``JevClient.ask`` uses to size a draw, so a whole-run reservation made from these
+numbers covers exactly what the client will draw.
+"""
+import math
+
+from jevlib.config import RESERVE_BYTES_PER_TOKEN
+from jevlib.questions import canonical_bytes
+
+
+def estimate_request_tokens(req):
+    """Input tokens reserved for one request: ``ceil(len(canonical request bytes) / RESERVE_BYTES_PER_TOKEN)``."""
+    return int(math.ceil(len(canonical_bytes(req)) / RESERVE_BYTES_PER_TOKEN))
+
+
+def estimate_run_tokens(requests):
+    """Worst case for a whole run: every request, times two for the one allowed rerun of a failed prompt."""
+    return 2 * sum(estimate_request_tokens(r) for r in requests)
+
+
+def ceiling_tokens(cap_usd, price_usd_per_mtok):
+    """The token ceiling that keeps spend at or below ``cap_usd`` at the given price per million input tokens."""
+    return int(cap_usd / price_usd_per_mtok * 1e6)
+
+
+def worst_case_usd(tokens, price_usd_per_mtok):
+    return tokens * price_usd_per_mtok / 1e6
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/events.py b/.dev/research/jev-vs-keyword-table-611/harness/events.py
new file mode 100644
index 000000000..380025d87
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/events.py
@@ -0,0 +1,115 @@
+"""Event log: one JSON line per event, append-only, plus the commands that record the owner's input, the price and the go.
+
+Command line (each takes ``--root``, the experiment folder by default):
+  events.py owner-input --evidence PATH --note TEXT
+  events.py price --usd-per-mtok VALUE --source TEXT
+  events.py go --words TEXT
+The other events (freeze, rule_freeze, gate1, gate2, tests_passed, first_request, run_end, scoring, verdict) are written by the
+module that does the work, through ``append_event``.  This module never rewrites or deletes a line.
+"""
+import argparse
+import datetime
+import json
+import os
+import pathlib
+import sys
+
+_EXP = pathlib.Path(__file__).resolve().parents[1]
+_JEV = _EXP.parent / "346-review-loop-experiments" / "p15" / "jev"
+for _p in (str(_EXP), str(_JEV)):
+    if _p not in sys.path:
+        sys.path.insert(0, _p)
+
+from harness import loader  # noqa: E402
+
+EVENTS = ("owner_input_received", "freeze", "rule_freeze", "gate1", "gate2", "tests_passed", "price_confirmed", "lead_go",
+          "first_request", "run_end", "scoring", "verdict")
+_CORE = ("ts", "event", "evidence", "evidence_sha256")
+
+
+def _evidence_path(paths, evidence):
+    p = pathlib.Path(evidence)
+    try:
+        return str(p.resolve().relative_to(paths.root.resolve()))
+    except ValueError:
+        return str(p)
+
+
+def append_event(paths, event, evidence=None, **fields):
+    """Append one event line (sorted keys, UTC timestamp, the evidence path and the evidence file's SHA-256) and return it.
+
+    An event with no evidence of its own is tied to the rule file in force when it was written, so the line still carries a path
+    and a hash.  An evidence path that is not a file is refused.  Only a log with no rule file yet leaves both null.
+    """
+    if event not in EVENTS:
+        raise ValueError(f"unknown event {event!r}")
+    clash = [k for k in fields if k in _CORE]
+    if clash:
+        raise ValueError(f"event field names reserved: {clash}")
+    if evidence is None and paths.rule.is_file():
+        evidence = paths.rule
+    ev_path, ev_sha = None, None
+    if evidence is not None:
+        if not pathlib.Path(evidence).is_file():
+            raise ValueError(f"evidence file does not exist: {evidence}")
+        ev_path = _evidence_path(paths, evidence)
+        ev_sha = loader.sha256_file(evidence)
+    rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "event": event,
+           "evidence": ev_path, "evidence_sha256": ev_sha, **fields}
+    paths.events.parent.mkdir(parents=True, exist_ok=True)
+    with open(paths.events, "a", encoding="utf-8") as f:
+        f.write(json.dumps(rec, sort_keys=True) + "\n")
+        f.flush()
+        os.fsync(f.fileno())
+    return rec
+
+
+def read_events(paths):
+    """Every event in the log, oldest first; an empty list when there is no log."""
+    if not paths.events.is_file():
+        return []
+    return [json.loads(line) for line in paths.events.read_text(encoding="utf-8").splitlines() if line.strip()]
+
+
+def latest(paths, name):
+    """The newest event with this name, or ``None``."""
+    found = [e for e in read_events(paths) if e["event"] == name]
+    return found[-1] if found else None
+
+
+def main(argv=None):
+    ap = argparse.ArgumentParser(prog="events.py", description="record owner input, the confirmed price and the lead's go")
+    sub = ap.add_subparsers(dest="cmd", required=True)
+    a = sub.add_parser("owner-input", help="record that the owner gave input, with the file that holds it")
+    a.add_argument("--evidence", required=True)
+    a.add_argument("--note", required=True)
+    b = sub.add_parser("price", help="record the re-confirmed price per million input tokens")
+    b.add_argument("--usd-per-mtok", type=float, required=True)
+    b.add_argument("--source", required=True)
+    c = sub.add_parser("go", help="record the lead's go, naming the rule file's current hash")
+    c.add_argument("--words", required=True)
+    for p in (a, b, c):
+        p.add_argument("--root", default=None)
+    args = ap.parse_args(argv)
+    paths = loader.Paths(args.root)
+    if args.cmd == "owner-input":
+        ev = pathlib.Path(args.evidence)
+        if not ev.is_file() and (paths.root / ev).is_file():
+            ev = paths.root / ev
+        if not ev.is_file():
+            ap.error(f"--evidence {args.evidence} is not a file")
+        rec = append_event(paths, "owner_input_received", evidence=ev, note=args.note)
+    elif args.cmd == "price":
+        if not args.usd_per_mtok > 0:
+            ap.error("--usd-per-mtok must be above zero")
+        rec = append_event(paths, "price_confirmed", usd_per_mtok=args.usd_per_mtok, source=args.source)
+    else:
+        if not paths.rule.is_file():
+            ap.error("no rule file to name in the go")
+        rec = append_event(paths, "lead_go", evidence=paths.rule, rule_sha256=loader.sha256_file(paths.rule), words=args.words)
+    print(json.dumps(rec, sort_keys=True))
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/gate.py b/.dev/research/jev-vs-keyword-table-611/harness/gate.py
new file mode 100644
index 000000000..9a03cd27b
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/gate.py
@@ -0,0 +1,265 @@
+"""The manifest and the two gates that keep every live call closed.
+
+Command line (each takes ``--root``, the experiment folder by default):
+  gate.py freeze-corpus   screen and freeze the corpus, its two records, ``questions.py`` and the model pin
+  gate.py gate1           check the rule file and the corpus-side hashes; accepts UNSET values
+  gate.py freeze-table    freeze the table answers and their provenance (after Gate 1 passes)
+  gate.py freeze-rule     freeze the rule file's hash (refuses any UNSET value)
+  gate.py record-tests    run the harness tests and record the result with the hash of every code file
+  gate.py gate2           everything Gate 1 checks, plus the rest; a pass is what the live run rests on (a lead_go that names the
+                          current rule hash must already be recorded, or it fails)
+Only the three ``freeze-*`` commands write the manifest, each its own keys and never an existing key.  The gates only read it, and
+they hash files only: they never call the corpus loader.
+"""
+import argparse
+import json
+import os
+import pathlib
+import re
+import subprocess
+import sys
+
+_EXP = pathlib.Path(__file__).resolve().parents[1]
+_JEV = _EXP.parent / "346-review-loop-experiments" / "p15" / "jev"
+for _p in (str(_EXP), str(_JEV)):
+    if _p not in sys.path:
+        sys.path.insert(0, _p)
+
+from harness import events, loader, spend  # noqa: E402
+
+REPO = loader.EXPERIMENT.parents[2]
+# manifest key -> the Paths attribute of the file it hashes (the corpus side, frozen by freeze-corpus)
+CORPUS_SIDE = {"corpus": "corpus", "selection_criteria": "selection_criteria", "labelling_record": "labelling_record",
+               "questions": "questions_py"}
+
+
+class GateError(Exception):
+    """A freeze or a recording step was refused."""
+
+
+def read_manifest(paths):
+    if not paths.manifest.is_file():
+        return {}
+    try:
+        return json.loads(paths.manifest.read_text(encoding="utf-8"))
+    except ValueError:
+        raise GateError("manifest.json is not valid JSON") from None
+
+
+def _write_manifest_keys(paths, new):
+    m = read_manifest(paths)
+    held = sorted(k for k in new if k in m)
+    if held:
+        raise GateError("the manifest already holds " + ", ".join(held) + "; a frozen value is never replaced")
+    m.update(new)
+    tmp = paths.manifest.with_suffix(".json.tmp")
+    tmp.write_text(json.dumps(m, indent=1, sort_keys=True) + "\n", encoding="utf-8")
+    os.replace(tmp, paths.manifest)
+
+
+def _code_hashes(paths):
+    """SHA-256 of every code file of the experiment and every top-level jevlib file, by a stable name."""
+    h = {}
+    for p in paths.code_files():
+        if p.is_file():
+            h["code/" + p.relative_to(paths.root).as_posix()] = loader.sha256_file(p)
+    for p in paths.jevlib_files():
+        h["jevlib/" + p.name] = loader.sha256_file(p)
+    return h
+
+
+def _remaining_tokens(paths, cap_tokens):
+    """Tokens still free under the cap: the ledger read as plain JSON (never through Budget, which rewrites it)."""
+    if not paths.ledger.is_file():
+        return cap_tokens
+    led = json.loads(paths.ledger.read_text(encoding="utf-8"))
+    pending = sum(d["est"] for d in led.get("draws", {}).values() if d.get("actual") is None)
+    undrawn = sum(max(r["tokens"] - r["drawn"], 0) for r in led.get("reserved", {}).values())
+    committed = led.get("spent_tokens", 0) + pending + undrawn
+    return min(led.get("ceiling_input_tokens", cap_tokens), cap_tokens) - committed
+
+
+def _spend_bound_reason(paths, price):
+    """Why the whole-run worst case does not fit, or ``None``.  The prompts are read as JSON lines, not through the loader."""
+    try:
+        rule = loader.load_rule(paths.rule)
+        rows = [json.loads(line) for line in paths.corpus.read_text(encoding="utf-8").splitlines() if line.strip()]
+    except (loader.LoadError, OSError, ValueError):
+        return "the rule file or the corpus cannot be read"
+    import questions
+    from jevlib.questions import build_request
+    qs = questions.build_questions()
+    est = spend.estimate_run_tokens([build_request({"prompt": r["text"]}, qs) for r in rows])
+    cap = rule["spend_cap_usd"]
+    if spend.worst_case_usd(est, price) > cap:
+        return "the whole-run worst case costs more than the cap"
+    if est > _remaining_tokens(paths, spend.ceiling_tokens(cap, price)):
+        return "the whole-run estimate is above the allowance left in the ledger"
+    return None
+
+
+def _gate1_checks(paths):
+    failed = []
+    if not paths.rule.is_file():
+        failed.append("rule_missing")
+    else:
+        try:
+            loader.load_rule(paths.rule)
+        except loader.LoadError as e:
+            msg = str(e)
+            if "not AGREED" in msg:
+                failed.append("rule_status")
+            elif "is empty" in msg or "agreement text" in msg:
+                failed.append("rule_provenance_empty")
+            else:
+                failed.append("rule_invalid")
+    m = read_manifest(paths)
+    if any(k not in m for k in CORPUS_SIDE):
+        failed.append("manifest_missing")
+    else:
+        for key, attr in CORPUS_SIDE.items():
+            p = getattr(paths, attr)
+            if not p.is_file() or loader.sha256_file(p) != m[key]:
+                failed.append("hash_" + key)
+    return failed
+
+
+def _gate2_checks(paths):
+    failed = _gate1_checks(paths)
+    m = read_manifest(paths)
+    rule_sha = loader.sha256_file(paths.rule) if paths.rule.is_file() else None
+    try:
+        loader.load_rule(paths.rule, for_scoring=True)
+    except loader.LoadError as e:
+        if "UNSET" in str(e):
+            failed.append("unset_value")
+    if events.latest(paths, "rule_freeze") is None or "rule" not in m:
+        failed.append("rule_not_frozen")
+    if "rule" in m and m["rule"] != rule_sha:
+        failed.append("hash_rule")
+    for key, missing, mismatch in (("table_answers", "table_missing", "hash_table_answers"),
+                                   ("table_provenance", "table_provenance_missing", "hash_table_provenance")):
+        p = getattr(paths, key)
+        if not p.is_file():
+            failed.append(missing)
+        elif m.get(key) != loader.sha256_file(p):
+            failed.append(mismatch)
+    tests = events.latest(paths, "tests_passed")
+    if tests is None:
+        failed.append("tests_not_recorded")
+    elif tests.get("code_hashes") != _code_hashes(paths):
+        failed.append("hash_code")
+    price = events.latest(paths, "price_confirmed")
+    if price is None:
+        failed.append("price_not_confirmed")
+    elif _spend_bound_reason(paths, price["usd_per_mtok"]):
+        failed.append("spend_bound")
+    go = events.latest(paths, "lead_go")
+    if go is None:
+        failed.append("go_missing")
+    elif go.get("rule_sha256") != rule_sha:
+        failed.append("go_rule_hash")
+    if events.latest(paths, "first_request") or events.latest(paths, "run_end"):
+        failed.append("prior_run")
+    return failed
+
+
+def gate1(paths):
+    """Run Gate 1, write its result as an event and return the failed checks by name (an empty list is a pass)."""
+    failed = _gate1_checks(paths)
+    events.append_event(paths, "gate1", passed=not failed, failed=failed)
+    return failed
+
+
+def gate2(paths):
+    """Run Gate 2, write its result as an event and return the failed checks by name (an empty list is a pass)."""
+    failed = _gate2_checks(paths)
+    events.append_event(paths, "gate2", passed=not failed, failed=failed)
+    return failed
+
+
+def freeze_corpus(paths):
+    rows = loader.load_corpus(paths.corpus)
+    for p in (paths.selection_criteria, paths.labelling_record, paths.questions_py):
+        if not p.is_file():
+            raise GateError(f"{p.name} is missing")
+    from jevlib.config import MODEL
+    keys = {k: loader.sha256_file(getattr(paths, attr)) for k, attr in CORPUS_SIDE.items()}
+    keys["model_pin"] = MODEL
+    _write_manifest_keys(paths, keys)
+    events.append_event(paths, "freeze", evidence=paths.corpus, what="corpus", prompts=len(rows))
+    return keys
+
+
+def freeze_table(paths):
+    failed = _gate1_checks(paths)
+    if failed:
+        raise GateError("Gate 1 checks fail: " + ", ".join(failed))
+    for p in (paths.table_answers, paths.table_provenance):
+        if not p.is_file():
+            raise GateError(f"{p.name} is missing")
+    keys = {"table_answers": loader.sha256_file(paths.table_answers),
+            "table_provenance": loader.sha256_file(paths.table_provenance)}
+    _write_manifest_keys(paths, keys)
+    events.append_event(paths, "freeze", evidence=paths.table_answers, what="table")
+    return keys
+
+
+def freeze_rule(paths):
+    loader.load_rule(paths.rule, for_scoring=True)
+    keys = {"rule": loader.sha256_file(paths.rule)}
+    _write_manifest_keys(paths, keys)
+    events.append_event(paths, "rule_freeze", evidence=paths.rule)
+    return keys
+
+
+def _run(cmd):
+    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
+    return r.returncode, r.stdout + r.stderr
+
+
+def _tests_command(paths):
+    """``uv run pytest <tests folder> -v``, the folder relative to the repository root when it is under it."""
+    try:
+        folder = paths.tests_dir.relative_to(REPO).as_posix()
+    except ValueError:
+        folder = str(paths.tests_dir)
+    return ["uv", "run", "pytest", folder, "-v"]
+
+
+def record_tests(paths, runner=None):
+    """Run the harness tests (``runner`` is injected in tests) and record the result with the hash of every code file."""
+    cmd = _tests_command(paths)
+    code, out = (runner or _run)(cmd)
+    if code != 0:
+        raise GateError("the test run failed")
+    m = re.search(r"(\d+) passed", out)
+    count = int(m.group(1)) if m else 0
+    if count == 0:
+        raise GateError("the test run passed no tests")
+    return events.append_event(paths, "tests_passed", command=" ".join(cmd), count=count, code_hashes=_code_hashes(paths))
+
+
+def main(argv=None):
+    ap = argparse.ArgumentParser(prog="gate.py", description="freeze the experiment's inputs and check the two gates")
+    sub = ap.add_subparsers(dest="cmd", required=True)
+    for name in ("freeze-corpus", "gate1", "freeze-table", "freeze-rule", "record-tests", "gate2"):
+        sub.add_parser(name).add_argument("--root", default=None)
+    args = ap.parse_args(argv)
+    paths = loader.Paths(args.root)
+    try:
+        if args.cmd in ("gate1", "gate2"):
+            failed = (gate1 if args.cmd == "gate1" else gate2)(paths)
+            print("PASS" if not failed else "FAILED: " + ",".join(failed))
+            return 1 if failed else 0
+        result = {"freeze-corpus": freeze_corpus, "freeze-table": freeze_table, "freeze-rule": freeze_rule,
+                  "record-tests": record_tests}[args.cmd](paths)
+        print(json.dumps(result, sort_keys=True))
+        return 0
+    except (GateError, loader.LoadError) as e:
+        print(f"REFUSED: {e}", file=sys.stderr)
+        return 1
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py
index cf4b70646..d47c992bb 100644
--- a.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py
@@ -57,3 +57,49 @@ def fake_key(monkeypatch):
 @pytest.fixture
 def snapshot_fn():
     return real_state_snapshot
+
+
+def normalised_rule_text():
+    """The committed rule file with its three open fields forced back to ``UNSET``, so a test never depends on whether the owner
+    has filled them in yet."""
+    import re
+
+    from harness import loader
+    text = loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8")
+    return re.sub(r"^(noul_low_operator|noul_high_operator|unresolved_failure_invalid_count): .*$", r"\1: UNSET", text,
+                  flags=re.MULTILINE)
+
+
+def synthetic_corpus_rows():
+    """Eight valid corpus rows: one per type, one ambiguous, one none-fit."""
+    labels = ["bug", "build", "performance", "deployment", "security", "test", "ambiguous", "none-fit"]
+    return [{"id": f"p{i}", "text": f"synthetic problem text number {i}", "source": f"https://example.org/post/{i}",
+             "retrieved_on": "2026-11-26", "selection_reason": "synthetic", "label": lab, "label_basis": "synthetic",
+             "labeller": "a test", "labelled_on": "2026-11-26", "seen_by_table": False} for i, lab in enumerate(labels)]
+
+
+@pytest.fixture
+def exp(tmp_path):
+    """A loader.Paths on a temporary root, filled with small synthetic frozen files, code stand-ins, a jevlib stand-in folder and
+    a copy of the committed rule file with its open fields set to UNSET.  Nothing here touches the real experiment folder."""
+    import json
+
+    from harness import loader
+    jevlib = tmp_path / "jevlib"
+    jevlib.mkdir()
+    for name in ("a.py", "b.py"):
+        (jevlib / name).write_text(f"# stand-in {name}\n")
+    p = loader.Paths(tmp_path, jevlib_dir=jevlib)
+    for f in p.code_files():
+        f.parent.mkdir(parents=True, exist_ok=True)
+        f.write_text(f"# stand-in {f.name}\n")
+    p.corpus.parent.mkdir(parents=True)
+    p.corpus.write_text("\n".join(json.dumps(r) for r in synthetic_corpus_rows()) + "\n")
+    p.selection_criteria.write_text("selection criteria\n")
+    p.labelling_record.write_text("labelling record\n")
+    p.table_answers.parent.mkdir(parents=True)
+    p.table_answers.write_text("\n".join(json.dumps({"prompt_id": f"p{i}", "answer": None}) for i in range(8)) + "\n")
+    p.table_provenance.write_text("table provenance\n")
+    p.tests_dir.mkdir(parents=True, exist_ok=True)
+    p.rule.write_text(normalised_rule_text(), encoding="utf-8")
+    return p
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py
new file mode 100644
index 000000000..4b2d22516
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py
@@ -0,0 +1,318 @@
+import json
+import math
+import re
+
+import pytest
+import questions
+from harness import events, gate, loader, spend
+from harness.gate import GateError
+from jevlib.config import RESERVE_BYTES_PER_TOKEN
+from jevlib.questions import build_request, canonical_bytes
+
+PASSING = lambda cmd: (0, "12 passed in 0.1s")  # noqa: E731
+
+
+def fill_rule(p, low="le", high="ge", count=3):
+    s = p.rule.read_text(encoding="utf-8")
+    s = s.replace("noul_low_operator: UNSET", f"noul_low_operator: {low}").replace("noul_high_operator: UNSET", f"noul_high_operator: {high}")
+    p.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", f"unresolved_failure_invalid_count: {count}"), encoding="utf-8")
+
+
+def ready(p, skip=(), price=0.042):
+    """Every step the live run rests on, in order; ``skip`` leaves named steps out."""
+    fill_rule(p)
+    gate.freeze_corpus(p)
+    if "table" not in skip:
+        gate.freeze_table(p)
+    if "rule" not in skip:
+        gate.freeze_rule(p)
+    if "price" not in skip:
+        events.append_event(p, "price_confirmed", usd_per_mtok=price, source="test")
+    if "tests" not in skip:
+        gate.record_tests(p, runner=PASSING)
+    if "go" not in skip:
+        events.append_event(p, "lead_go", evidence=p.rule, rule_sha256=loader.sha256_file(p.rule), words="go")
+
+
+def append_text(path, text="# edited\n"):
+    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")
+
+
+def run_estimate(p):
+    qs = questions.build_questions()
+    rows = [json.loads(line) for line in p.corpus.read_text().splitlines() if line.strip()]
+    reqs = [build_request({"prompt": r["text"]}, qs) for r in rows]
+    return spend.estimate_run_tokens(reqs), max(spend.estimate_request_tokens(r) for r in reqs)
+
+
+# ---- Gate 1 (T-01, T-02)
+
+def test_gate1_passes_after_the_corpus_is_frozen_and_accepts_unset_values(exp):
+    gate.freeze_corpus(exp)
+    assert "UNSET" in exp.rule.read_text(encoding="utf-8")
+    assert gate.gate1(exp) == []
+
+
+def test_gate1_refuses_before_anything_is_frozen(exp):
+    assert gate.gate1(exp) == ["manifest_missing"]
+
+
+@pytest.mark.parametrize("edit,name", [
+    (lambda s: s.replace("status: AGREED", "status: PROPOSED"), "rule_status"),
+    (lambda s: s.replace("status: AGREED", "status: PENDING"), "rule_status"),
+    (lambda s: s.replace("agreed_by: the IronFlow session and the build agent", "agreed_by:"), "rule_provenance_empty"),
+    (lambda s: s.replace("agreed_at: 2026-11-26", "agreed_at:"), "rule_provenance_empty"),
+    (lambda s: s.replace("relayed_owner_words: you and the agent debate whats correct way to handle this and do it",
+                         "relayed_owner_words:"), "rule_provenance_empty"),
+    (lambda s: s.replace("I agree with all five", "").split("## Agreement text (verbatim)")[0]
+     + "## Agreement text (verbatim)\n\n## Rule in words\n", "rule_provenance_empty"),
+])
+def test_gate1_refuses_each_rule_file_defect(exp, edit, name):
+    gate.freeze_corpus(exp)
+    exp.rule.write_text(edit(exp.rule.read_text(encoding="utf-8")), encoding="utf-8")
+    assert gate.gate1(exp) == [name]
+
+
+def test_gate1_refuses_a_missing_rule_file(exp):
+    gate.freeze_corpus(exp)
+    exp.rule.unlink()
+    assert gate.gate1(exp) == ["rule_missing"]
+
+
+@pytest.mark.parametrize("attr,name", [("corpus", "hash_corpus"), ("selection_criteria", "hash_selection_criteria"),
+                                       ("labelling_record", "hash_labelling_record"), ("questions_py", "hash_questions")])
+def test_either_gate_refuses_a_changed_corpus_side_file(exp, attr, name):
+    ready(exp)
+    append_text(getattr(exp, attr), "\n")
+    assert name in gate.gate1(exp)
+    assert name in gate.gate2(exp)
+
+
+# ---- Gate 2 (T-02, T-03, second-run refusal)
+
+def test_gate2_passes_on_a_complete_synthetic_setup(exp):
+    ready(exp)
+    assert gate.gate2(exp) == []
+
+
+@pytest.mark.parametrize("skip,name", [("go", "go_missing"), ("tests", "tests_not_recorded"), ("rule", "rule_not_frozen"),
+                                       ("price", "price_not_confirmed"), ("table", "hash_table_answers")])
+def test_gate2_refuses_a_missing_step(exp, skip, name):
+    ready(exp, skip=(skip,))
+    assert name in gate.gate2(exp)
+
+
+def test_gate2_refuses_a_go_that_names_an_old_rule_hash(exp):
+    ready(exp)
+    events.append_event(exp, "lead_go", rule_sha256="0" * 64, words="old")
+    assert gate.gate2(exp) == ["go_rule_hash"]
+
+
+def test_gate2_refuses_an_unset_value(exp):
+    ready(exp)
+    exp.rule.write_text(exp.rule.read_text(encoding="utf-8").replace("noul_low_operator: le", "noul_low_operator: UNSET"), encoding="utf-8")
+    assert "unset_value" in gate.gate2(exp)
+
+
+def test_gate2_refuses_a_changed_rule_table_answers_provenance_code_or_jevlib_file(exp):
+    ready(exp)
+    for target, name in ((exp.rule, "hash_rule"), (exp.table_answers, "hash_table_answers"),
+                         (exp.table_provenance, "hash_table_provenance"), (exp.root / "harness" / "scorer.py", "hash_code"),
+                         (exp.root / "harness" / "runner.py", "hash_code"), (exp.jevlib_dir / "a.py", "hash_code")):
+        original = target.read_bytes()
+        append_text(target, "\n")
+        assert name in gate.gate2(exp), name
+        target.write_bytes(original)
+    assert gate.gate2(exp) == []
+
+
+@pytest.mark.parametrize("event", ["first_request", "run_end"])
+def test_gate2_refuses_when_a_run_already_started_or_ended(exp, event):
+    ready(exp)
+    events.append_event(exp, event)
+    assert gate.gate2(exp) == ["prior_run"]
+
+
+def test_spend_bound_fails_when_each_request_fits_but_the_whole_run_does_not(exp):
+    ready(exp)
+    total, biggest = run_estimate(exp)
+    cap = spend.ceiling_tokens(1.0, 0.042)
+    left = total - 10
+    assert left > biggest
+    exp.ledger.parent.mkdir()
+    exp.ledger.write_text(json.dumps({"ceiling_input_tokens": cap, "spent_tokens": cap - left, "draws": {}, "reserved": {}}))
+    assert gate.gate2(exp) == ["spend_bound"]
+    exp.ledger.write_text(json.dumps({"ceiling_input_tokens": cap, "spent_tokens": cap - total - 1, "draws": {}, "reserved": {}}))
+    assert gate.gate2(exp) == []
+
+
+def test_spend_bound_fails_when_the_worst_case_at_a_high_price_is_above_the_cap(exp):
+    ready(exp, price=1000.0)
+    assert gate.gate2(exp) == ["spend_bound"]
+
+
+def test_gates_hash_files_only_and_never_call_the_corpus_loader(exp, monkeypatch):
+    ready(exp)
+
+    def boom(*a, **k):
+        raise AssertionError("the corpus loader was called")
+    monkeypatch.setattr(loader, "load_corpus", boom)
+    assert gate.gate1(exp) == []
+    assert gate.gate2(exp) == []
+
+
+# ---- freezes and the manifest (write-once, gates only read)
+
+def test_the_manifest_is_unchanged_by_either_gate(exp):
+    ready(exp)
+    before = exp.manifest.read_bytes()
+    gate.gate1(exp)
+    gate.gate2(exp)
+    assert exp.manifest.read_bytes() == before
+
+
+def test_a_second_freeze_of_each_kind_is_refused_and_keeps_the_frozen_value(exp):
+    ready(exp)
+    before = exp.manifest.read_bytes()
+    for freeze in (gate.freeze_corpus, gate.freeze_table, gate.freeze_rule):
+        with pytest.raises(GateError, match="already holds"):
+            freeze(exp)
+    assert exp.manifest.read_bytes() == before
+
+
+def test_the_manifest_holds_the_hashes_and_the_model_pin(exp):
+    ready(exp)
+    m = gate.read_manifest(exp)
+    assert m["model_pin"] == "jev-1.14.0" and m["rule"] == loader.sha256_file(exp.rule)
+    assert set(m) == {"corpus", "selection_criteria", "labelling_record", "questions", "model_pin", "table_answers",
+                      "table_provenance", "rule"}
+
+
+def test_freeze_rule_refuses_an_unset_value(exp):
+    gate.freeze_corpus(exp)
+    with pytest.raises(loader.LoadError, match="UNSET"):
+        gate.freeze_rule(exp)
+    assert "rule" not in gate.read_manifest(exp)
+
+
+def test_freeze_table_refuses_until_gate1_passes_and_when_a_file_is_missing(exp):
+    with pytest.raises(GateError, match="Gate 1"):
+        gate.freeze_table(exp)
+    gate.freeze_corpus(exp)
+    exp.table_provenance.unlink()
+    with pytest.raises(GateError, match="missing"):
+        gate.freeze_table(exp)
+
+
+def test_freeze_corpus_refuses_a_corpus_the_screen_refuses(exp):
+    rows = [json.loads(line) for line in exp.corpus.read_text().splitlines()]
+    rows[0]["text"] = "see https://github.com/example/project"
+    exp.corpus.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
+    with pytest.raises(loader.LoadError, match="privacy"):
+        gate.freeze_corpus(exp)
+    assert gate.read_manifest(exp) == {}
+
+
+@pytest.mark.parametrize("result,match", [((1, "1 failed, 3 passed"), "failed"), ((0, "no tests ran"), "no tests")])
+def test_record_tests_refuses_a_failing_or_empty_run(exp, result, match):
+    with pytest.raises(GateError, match=match):
+        gate.record_tests(exp, runner=lambda cmd: result)
+    assert events.latest(exp, "tests_passed") is None
+
+
+def test_record_tests_records_the_command_count_and_hashes(exp):
+    rec = gate.record_tests(exp, runner=PASSING)
+    assert rec["count"] == 12 and rec["command"].startswith("uv run pytest ") and rec["command"].endswith(" -v")
+    assert rec["code_hashes"]["code/questions.py"] == loader.sha256_file(exp.questions_py)
+    assert rec["code_hashes"]["jevlib/a.py"] == loader.sha256_file(exp.jevlib_dir / "a.py")
+
+
+def test_the_recorded_test_command_is_the_repo_relative_form_the_plan_names():
+    # a read-only look at the real paths: nothing is run and nothing is written
+    assert gate._tests_command(loader.Paths()) == ["uv", "run", "pytest", ".dev/research/jev-vs-keyword-table-611/harness/tests", "-v"]
+
+
+def test_the_gate_command_line_returns_one_on_a_failure_and_zero_on_a_pass(exp, capsys):
+    assert gate.main(["gate1", "--root", str(exp.root)]) == 1
+    assert "FAILED: manifest_missing" in capsys.readouterr().out
+    gate.freeze_corpus(exp)
+    assert gate.main(["gate1", "--root", str(exp.root)]) == 0
+    assert gate.main(["freeze-corpus", "--root", str(exp.root)]) == 1          # a second freeze is refused
+    assert "already holds" in capsys.readouterr().err
+
+
+# ---- events (append-only, evidence, the three commands)
+
+def test_events_are_appended_never_rewritten_and_carry_time_path_and_hash(exp):
+    first = events.append_event(exp, "freeze", evidence=exp.corpus, what="corpus")
+    text1 = exp.events.read_text()
+    events.append_event(exp, "gate1", passed=True, failed=[])
+    assert exp.events.read_text().startswith(text1)
+    assert exp.events.read_text().count("\n") == 2
+    assert first["evidence"] == "corpus/corpus.jsonl" and first["evidence_sha256"] == loader.sha256_file(exp.corpus)
+    assert first["ts"].endswith("+00:00")
+    assert [e["event"] for e in events.read_events(exp)] == ["freeze", "gate1"]
+    assert events.latest(exp, "freeze")["what"] == "corpus" and events.latest(exp, "verdict") is None
+
+
+def test_every_event_kind_the_setup_writes_carries_a_time_a_path_and_a_hash(exp):
+    ready(exp)
+    gate.gate1(exp)
+    gate.gate2(exp)
+    events.append_event(exp, "first_request")
+    log = events.read_events(exp)
+    assert {e["event"] for e in log} >= {"freeze", "rule_freeze", "price_confirmed", "tests_passed", "lead_go", "gate1", "gate2",
+                                         "first_request"}
+    for e in log:
+        assert e["ts"] and e["evidence"], e["event"]
+        assert re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]), e["event"]
+    assert events.latest(exp, "gate2")["evidence"] == "decision-rule.md"          # no evidence of its own: tied to the rule file
+
+
+def test_an_evidence_path_that_is_not_a_file_is_refused(exp, tmp_path):
+    with pytest.raises(ValueError, match="does not exist"):
+        events.append_event(exp, "freeze", evidence=tmp_path / "nope.txt")
+    with pytest.raises(SystemExit):
+        events.main(["owner-input", "--evidence", str(tmp_path / "nope.txt"), "--note", "x", "--root", str(exp.root)])
+    assert events.read_events(exp) == []
+
+
+def test_events_refuse_an_unknown_name_and_a_reserved_field(exp):
+    with pytest.raises(ValueError):
+        events.append_event(exp, "made_up")
+    with pytest.raises(ValueError):
+        events.append_event(exp, "gate1", ts="now")
+
+
+def test_the_three_event_commands_write_their_events(exp, tmp_path):
+    note = tmp_path / "input.txt"
+    note.write_text("owner answer\n")
+    assert events.main(["owner-input", "--evidence", str(note), "--note", "owner set the operators", "--root", str(exp.root)]) == 0
+    assert events.main(["price", "--usd-per-mtok", "0.05", "--source", "vendor page", "--root", str(exp.root)]) == 0
+    assert events.main(["go", "--words", "go ahead", "--root", str(exp.root)]) == 0
+    got = {e["event"]: e for e in events.read_events(exp)}
+    assert set(got) == {"owner_input_received", "price_confirmed", "lead_go"}
+    assert got["owner_input_received"]["evidence_sha256"] == loader.sha256_file(note)
+    assert got["price_confirmed"]["usd_per_mtok"] == 0.05
+    assert got["lead_go"]["rule_sha256"] == loader.sha256_file(exp.rule) and got["lead_go"]["words"] == "go ahead"
+    assert all(e["evidence"] and re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]) for e in got.values())
+
+
+def test_the_price_command_refuses_a_price_of_zero(exp):
+    with pytest.raises(SystemExit):
+        events.main(["price", "--usd-per-mtok", "0", "--source", "x", "--root", str(exp.root)])
+
+
+# ---- spend
+
+def test_spend_estimates_follow_the_client_formula():
+    req = build_request({"prompt": "x"}, questions.build_questions())
+    assert spend.estimate_request_tokens(req) == math.ceil(len(canonical_bytes(req)) / RESERVE_BYTES_PER_TOKEN)
+    assert spend.estimate_run_tokens([req, req, req]) == 6 * spend.estimate_request_tokens(req)
+    assert spend.estimate_run_tokens([]) == 0
+
+
+def test_spend_ceiling_and_worst_case_follow_the_price():
+    assert spend.ceiling_tokens(1.0, 0.042) == 23809523
+    assert spend.ceiling_tokens(1.0, 0.084) == 11904761
+    assert spend.worst_case_usd(1_000_000, 0.042) == pytest.approx(0.042)
diff --git a.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py
index d4deb2fcf..53cb225cc 100644
--- a.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py
@@ -2,6 +2,7 @@ import json
 import pathlib
 
 import pytest
+from conftest import normalised_rule_text
 from harness import loader
 from harness.loader import LoadError, Paths
 
@@ -10,7 +11,8 @@ OPEN_FIELDS = {"noul_low_operator", "noul_high_operator", "unresolved_failure_in
 
 
 def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
-    s = RULE.read_text(encoding="utf-8") if text is None else text
+    """A copy of the rule file with its open fields UNSET (unless ``text`` is given), whatever the live file holds now."""
+    s = normalised_rule_text() if text is None else text
     if old is not None:
         assert old in s
         s = s.replace(old, new, 1)
@@ -23,9 +25,11 @@ def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
 
 # ---- rule file (T-01 refusals, T-04)
 
-def test_committed_rule_loads_with_exactly_the_three_open_fields_unset():
+def test_committed_rule_loads_and_only_the_three_open_fields_may_be_unset(tmp_path):
     rule = loader.load_rule(RULE)
-    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} == OPEN_FIELDS
+    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} <= OPEN_FIELDS
+    normal = loader.load_rule(_rule_copy(tmp_path))
+    assert {k for k in loader.RULE_KEYS if normal[k] == "UNSET"} == OPEN_FIELDS
     assert rule["status"] == "AGREED" and rule["alpha_inverse"] == 20 and rule["attempt_timeout_s"] == 10.0
     assert rule["median_limit_s"] == 2.0 and rule["slowest_limit_s"] == 5.0 and rule["spend_cap_usd"] == 1.0
 
@@ -69,8 +73,8 @@ def test_rule_refuses_a_missing_key_and_a_missing_file(tmp_path):
 
 def test_rule_refuses_scoring_while_a_value_is_unset_and_accepts_it_when_all_are_set(tmp_path):
     with pytest.raises(LoadError, match="UNSET"):
-        loader.load_rule(RULE, for_scoring=True)
-    s = RULE.read_text(encoding="utf-8")
+        loader.load_rule(_rule_copy(tmp_path), for_scoring=True)
+    s = normalised_rule_text()
     s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
     s = s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3")
     rule = loader.load_rule(_rule_copy(tmp_path, text=s), for_scoring=True)


Codegraph context
index_state: fresh
checked_at: 2026-11-26T16:38:23Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the files of this task are new or only used by later tasks; no dependent outside the touched files.
Delta diff from the previous reviewed tree (empty on the first review): diff --git a.dev/research/jev-vs-keyword-table-611/harness/events.py b/.dev/research/jev-vs-keyword-table-611/harness/events.py
index 04f360e81..380025d87 100644
--- a.dev/research/jev-vs-keyword-table-611/harness/events.py
+++ b/.dev/research/jev-vs-keyword-table-611/harness/events.py
@@ -36,17 +36,24 @@ def _evidence_path(paths, evidence):
 
 
 def append_event(paths, event, evidence=None, **fields):
-    """Append one event line (sorted keys, UTC timestamp, the evidence path and the evidence file's SHA-256) and return it."""
+    """Append one event line (sorted keys, UTC timestamp, the evidence path and the evidence file's SHA-256) and return it.
+
+    An event with no evidence of its own is tied to the rule file in force when it was written, so the line still carries a path
+    and a hash.  An evidence path that is not a file is refused.  Only a log with no rule file yet leaves both null.
+    """
     if event not in EVENTS:
         raise ValueError(f"unknown event {event!r}")
     clash = [k for k in fields if k in _CORE]
     if clash:
         raise ValueError(f"event field names reserved: {clash}")
+    if evidence is None and paths.rule.is_file():
+        evidence = paths.rule
     ev_path, ev_sha = None, None
     if evidence is not None:
+        if not pathlib.Path(evidence).is_file():
+            raise ValueError(f"evidence file does not exist: {evidence}")
         ev_path = _evidence_path(paths, evidence)
-        if pathlib.Path(evidence).is_file():
-            ev_sha = loader.sha256_file(evidence)
+        ev_sha = loader.sha256_file(evidence)
     rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "event": event,
            "evidence": ev_path, "evidence_sha256": ev_sha, **fields}
     paths.events.parent.mkdir(parents=True, exist_ok=True)
@@ -89,6 +96,8 @@ def main(argv=None):
         ev = pathlib.Path(args.evidence)
         if not ev.is_file() and (paths.root / ev).is_file():
             ev = paths.root / ev
+        if not ev.is_file():
+            ap.error(f"--evidence {args.evidence} is not a file")
         rec = append_event(paths, "owner_input_received", evidence=ev, note=args.note)
     elif args.cmd == "price":
         if not args.usd_per_mtok > 0:
diff --git a.dev/research/jev-vs-keyword-table-611/harness/gate.py b/.dev/research/jev-vs-keyword-table-611/harness/gate.py
index c8bfd2ca8..9a03cd27b 100644
--- a.dev/research/jev-vs-keyword-table-611/harness/gate.py
+++ b/.dev/research/jev-vs-keyword-table-611/harness/gate.py
@@ -6,7 +6,8 @@ Command line (each takes ``--root``, the experiment folder by default):
   gate.py freeze-table    freeze the table answers and their provenance (after Gate 1 passes)
   gate.py freeze-rule     freeze the rule file's hash (refuses any UNSET value)
   gate.py record-tests    run the harness tests and record the result with the hash of every code file
-  gate.py gate2           everything Gate 1 checks, plus the rest; its pass is what the lead's go rests on
+  gate.py gate2           everything Gate 1 checks, plus the rest; a pass is what the live run rests on (a lead_go that names the
+                          current rule hash must already be recorded, or it fails)
 Only the three ``freeze-*`` commands write the manifest, each its own keys and never an existing key.  The gates only read it, and
 they hash files only: they never call the corpus loader.
 """
@@ -217,9 +218,18 @@ def _run(cmd):
     return r.returncode, r.stdout + r.stderr
 
 
+def _tests_command(paths):
+    """``uv run pytest <tests folder> -v``, the folder relative to the repository root when it is under it."""
+    try:
+        folder = paths.tests_dir.relative_to(REPO).as_posix()
+    except ValueError:
+        folder = str(paths.tests_dir)
+    return ["uv", "run", "pytest", folder, "-v"]
+
+
 def record_tests(paths, runner=None):
     """Run the harness tests (``runner`` is injected in tests) and record the result with the hash of every code file."""
-    cmd = ["uv", "run", "pytest", str(paths.tests_dir), "-q"]
+    cmd = _tests_command(paths)
     code, out = (runner or _run)(cmd)
     if code != 0:
         raise GateError("the test run failed")
diff --git a.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py
index ea467f116..d47c992bb 100644
--- a.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py
@@ -59,6 +59,17 @@ def snapshot_fn():
     return real_state_snapshot
 
 
+def normalised_rule_text():
+    """The committed rule file with its three open fields forced back to ``UNSET``, so a test never depends on whether the owner
+    has filled them in yet."""
+    import re
+
+    from harness import loader
+    text = loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8")
+    return re.sub(r"^(noul_low_operator|noul_high_operator|unresolved_failure_invalid_count): .*$", r"\1: UNSET", text,
+                  flags=re.MULTILINE)
+
+
 def synthetic_corpus_rows():
     """Eight valid corpus rows: one per type, one ambiguous, one none-fit."""
     labels = ["bug", "build", "performance", "deployment", "security", "test", "ambiguous", "none-fit"]
@@ -70,7 +81,7 @@ def synthetic_corpus_rows():
 @pytest.fixture
 def exp(tmp_path):
     """A loader.Paths on a temporary root, filled with small synthetic frozen files, code stand-ins, a jevlib stand-in folder and
-    a copy of the committed rule file.  Nothing here touches the real experiment folder."""
+    a copy of the committed rule file with its open fields set to UNSET.  Nothing here touches the real experiment folder."""
     import json
 
     from harness import loader
@@ -90,5 +101,5 @@ def exp(tmp_path):
     p.table_answers.write_text("\n".join(json.dumps({"prompt_id": f"p{i}", "answer": None}) for i in range(8)) + "\n")
     p.table_provenance.write_text("table provenance\n")
     p.tests_dir.mkdir(parents=True, exist_ok=True)
-    p.rule.write_text(loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8"), encoding="utf-8")
+    p.rule.write_text(normalised_rule_text(), encoding="utf-8")
     return p
diff --git a.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py
index cca67f1b5..4b2d22516 100644
--- a.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py
@@ -1,5 +1,6 @@
 import json
 import math
+import re
 
 import pytest
 import questions
@@ -221,11 +222,16 @@ def test_record_tests_refuses_a_failing_or_empty_run(exp, result, match):
 
 def test_record_tests_records_the_command_count_and_hashes(exp):
     rec = gate.record_tests(exp, runner=PASSING)
-    assert rec["count"] == 12 and rec["command"].startswith("uv run pytest ") and rec["command"].endswith(" -q")
+    assert rec["count"] == 12 and rec["command"].startswith("uv run pytest ") and rec["command"].endswith(" -v")
     assert rec["code_hashes"]["code/questions.py"] == loader.sha256_file(exp.questions_py)
     assert rec["code_hashes"]["jevlib/a.py"] == loader.sha256_file(exp.jevlib_dir / "a.py")
 
 
+def test_the_recorded_test_command_is_the_repo_relative_form_the_plan_names():
+    # a read-only look at the real paths: nothing is run and nothing is written
+    assert gate._tests_command(loader.Paths()) == ["uv", "run", "pytest", ".dev/research/jev-vs-keyword-table-611/harness/tests", "-v"]
+
+
 def test_the_gate_command_line_returns_one_on_a_failure_and_zero_on_a_pass(exp, capsys):
     assert gate.main(["gate1", "--root", str(exp.root)]) == 1
     assert "FAILED: manifest_missing" in capsys.readouterr().out
@@ -249,6 +255,28 @@ def test_events_are_appended_never_rewritten_and_carry_time_path_and_hash(exp):
     assert events.latest(exp, "freeze")["what"] == "corpus" and events.latest(exp, "verdict") is None
 
 
+def test_every_event_kind_the_setup_writes_carries_a_time_a_path_and_a_hash(exp):
+    ready(exp)
+    gate.gate1(exp)
+    gate.gate2(exp)
+    events.append_event(exp, "first_request")
+    log = events.read_events(exp)
+    assert {e["event"] for e in log} >= {"freeze", "rule_freeze", "price_confirmed", "tests_passed", "lead_go", "gate1", "gate2",
+                                         "first_request"}
+    for e in log:
+        assert e["ts"] and e["evidence"], e["event"]
+        assert re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]), e["event"]
+    assert events.latest(exp, "gate2")["evidence"] == "decision-rule.md"          # no evidence of its own: tied to the rule file
+
+
+def test_an_evidence_path_that_is_not_a_file_is_refused(exp, tmp_path):
+    with pytest.raises(ValueError, match="does not exist"):
+        events.append_event(exp, "freeze", evidence=tmp_path / "nope.txt")
+    with pytest.raises(SystemExit):
+        events.main(["owner-input", "--evidence", str(tmp_path / "nope.txt"), "--note", "x", "--root", str(exp.root)])
+    assert events.read_events(exp) == []
+
+
 def test_events_refuse_an_unknown_name_and_a_reserved_field(exp):
     with pytest.raises(ValueError):
         events.append_event(exp, "made_up")
@@ -267,6 +295,7 @@ def test_the_three_event_commands_write_their_events(exp, tmp_path):
     assert got["owner_input_received"]["evidence_sha256"] == loader.sha256_file(note)
     assert got["price_confirmed"]["usd_per_mtok"] == 0.05
     assert got["lead_go"]["rule_sha256"] == loader.sha256_file(exp.rule) and got["lead_go"]["words"] == "go ahead"
+    assert all(e["evidence"] and re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]) for e in got.values())
 
 
 def test_the_price_command_refuses_a_price_of_zero(exp):
diff --git a.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py
index d4deb2fcf..53cb225cc 100644
--- a.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py
@@ -2,6 +2,7 @@ import json
 import pathlib
 
 import pytest
+from conftest import normalised_rule_text
 from harness import loader
 from harness.loader import LoadError, Paths
 
@@ -10,7 +11,8 @@ OPEN_FIELDS = {"noul_low_operator", "noul_high_operator", "unresolved_failure_in
 
 
 def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
-    s = RULE.read_text(encoding="utf-8") if text is None else text
+    """A copy of the rule file with its open fields UNSET (unless ``text`` is given), whatever the live file holds now."""
+    s = normalised_rule_text() if text is None else text
     if old is not None:
         assert old in s
         s = s.replace(old, new, 1)
@@ -23,9 +25,11 @@ def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
 
 # ---- rule file (T-01 refusals, T-04)
 
-def test_committed_rule_loads_with_exactly_the_three_open_fields_unset():
+def test_committed_rule_loads_and_only_the_three_open_fields_may_be_unset(tmp_path):
     rule = loader.load_rule(RULE)
-    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} == OPEN_FIELDS
+    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} <= OPEN_FIELDS
+    normal = loader.load_rule(_rule_copy(tmp_path))
+    assert {k for k in loader.RULE_KEYS if normal[k] == "UNSET"} == OPEN_FIELDS
     assert rule["status"] == "AGREED" and rule["alpha_inverse"] == 20 and rule["attempt_timeout_s"] == 10.0
     assert rule["median_limit_s"] == 2.0 and rule["slowest_limit_s"] == 5.0 and rule["spend_cap_usd"] == 1.0
 
@@ -69,8 +73,8 @@ def test_rule_refuses_a_missing_key_and_a_missing_file(tmp_path):
 
 def test_rule_refuses_scoring_while_a_value_is_unset_and_accepts_it_when_all_are_set(tmp_path):
     with pytest.raises(LoadError, match="UNSET"):
-        loader.load_rule(RULE, for_scoring=True)
-    s = RULE.read_text(encoding="utf-8")
+        loader.load_rule(_rule_copy(tmp_path), for_scoring=True)
+    s = normalised_rule_text()
     s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
     s = s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3")
     rule = loader.load_rule(_rule_copy(tmp_path, text=s), for_scoring=True)

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T4.AC6 at=.dev/research/jev-vs-keyword-table-611/harness/gate.py:169 anchor="each carries a timestamp, an evidence path and a hash" chk=amiss:y,false:n,harm:n,constraint:n family=evidence-hash fix=pass an evidence file to the gate1, gate2 and tests_passed events (for example the rule file or the manifest), and have the AC6 test check every event kind it can write covered by the AC [covers="event lines ... each carries a timestamp, an evidence path and a hash"] first=A1 origin=new: `gate1`, `gate2` (`gate.py:176`), `tests_passed` (`gate.py:230`) and `price_confirmed` (`events.py:96`) are written with `evidence=None`, so their `evidence` and `evidence_sha256` are null. The test checks only the `freeze` event (`tests/test_gate_events.py:241-247`).
F1.2 sev=blocking trigger=B1 ac=T4.AC6 at=.dev/research/jev-vs-keyword-table-611/harness/events.py:88 anchor="each carries a timestamp, an evidence path and a hash" chk=amiss:y,false:n,harm:n,constraint:n family=evidence-hash fix=make `owner-input` refuse a `--evidence` path that is not a file, and add a test first=A1 origin=new: `owner-input` with a nonexistent `--evidence` path still writes `owner_input_received` with `evidence_sha256` null (`events.py:88-92` with `events.py:48-49`). The test only uses an existing file (`tests/test_gate_events.py:259-269`).
F1.4 sev=blocking trigger=B1 ac=T4.AC1 at=.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:93 anchor="passes, using only the `exp` fixture's temporary root" chk=amiss:y,false:n,harm:n,constraint:n family=rule-copy fix=have the `exp` fixture normalise its copy (force the three open fields to `UNSET` and the rest to the committed values) so the tests do not depend on the live rule file's current state [covers="a copy of the rule file"] first=A1 origin=new: the fixture copies the live `decision-rule.md`, which still holds `UNSET` today. The tests assert that state: `tests/test_gate_events.py:51` asserts `"UNSET"` is present, and `:190-193` expects `freeze_rule` to raise on `UNSET`. `:112` only works if the owner chooses `le` for the low operator. The plan has the owner fill those fields before `freeze-rule`. After that, `uv run pytest .../test_gate_events.py` and the `record-tests` run fail (the `uv run pytest <tests folder>` command in `gate.py:222`). The same dependence exists at `tests/test_loader.py:28`. This is a plan-check fragility: it can make AC1 fail as written.
F1.5 sev=blocking trigger=B4 ac=scope at=.dev/research/jev-vs-keyword-table-611/harness/gate.py:222 anchor="Test run command, recorded by `gate.py record-tests`: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`" chk=amiss:n,false:n,harm:n,constraint:y family=record-command fix=reconcile the plan (the task text at brief line 18 says `-q`) and make the code, the test at `tests/test_gate_events.py:224` and the constraint say the same thing [covers="Test run command, recorded by `gate.py record-tests`"] first=A1 origin=new: the recorded command is `uv run pytest <absolute tests dir> -q`. The constraint says a repo-relative path and `-v`. The code follows the Task 4 brief text, so this is a plan conflict, but the constraint's recorded form is not what is written.
F1.6 sev=blocking trigger=B2 ac=scope at=.dev/research/jev-vs-keyword-table-611/harness/gate.py:9 anchor=.dev/research/jev-vs-keyword-table-611/harness/gate.py:156-158 chk=amiss:n,false:y,harm:n,constraint:n family=docstring fix=reword to say Gate 2 requires a `lead_go` that names the current rule hash, so the go is recorded before Gate 2 passes first=A1 origin=new: the module docstring says Gate 2's "pass is what the lead's go rests on". The code requires the `lead_go` event to exist before Gate 2 can pass (`go_missing`, `go_rule_hash`). Wording only.

Saved-probe re-check hit locations (may be empty): probe family evidence-hash, hit locations after the fix:
  .dev/research/jev-vs-keyword-table-611/harness/events.py:4:  events.py owner-input --evidence PATH --note TEXT
  .dev/research/jev-vs-keyword-table-611/harness/events.py:27:_CORE = ("ts", "event", "evidence", "evidence_sha256")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:30:def _evidence_path(paths, evidence):
  .dev/research/jev-vs-keyword-table-611/harness/events.py:31:    p = pathlib.Path(evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:38:def append_event(paths, event, evidence=None, **fields):
  .dev/research/jev-vs-keyword-table-611/harness/events.py:39:    """Append one event line (sorted keys, UTC timestamp, the evidence path and the evidence file's SHA-256) and return it.
  .dev/research/jev-vs-keyword-table-611/harness/events.py:41:    An event with no evidence of its own is tied to the rule file in force when it was written, so the line still carries a path
  .dev/research/jev-vs-keyword-table-611/harness/events.py:42:    and a hash.  An evidence path that is not a file is refused.  Only a log with no rule file yet leaves both null.
  .dev/research/jev-vs-keyword-table-611/harness/events.py:49:    if evidence is None and paths.rule.is_file():
  .dev/research/jev-vs-keyword-table-611/harness/events.py:50:        evidence = paths.rule
  .dev/research/jev-vs-keyword-table-611/harness/events.py:52:    if evidence is not None:
  .dev/research/jev-vs-keyword-table-611/harness/events.py:53:        if not pathlib.Path(evidence).is_file():
  .dev/research/jev-vs-keyword-table-611/harness/events.py:54:            raise ValueError(f"evidence file does not exist: {evidence}")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:55:        ev_path = _evidence_path(paths, evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:56:        ev_sha = loader.sha256_file(evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:58:           "evidence": ev_path, "evidence_sha256": ev_sha, **fields}
  .dev/research/jev-vs-keyword-table-611/harness/events.py:84:    a.add_argument("--evidence", required=True)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:96:        ev = pathlib.Path(args.evidence)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:100:            ap.error(f"--evidence {args.evidence} is not a file")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:101:        rec = append_event(paths, "owner_input_received", evidence=ev, note=args.note)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:105:        rec = append_event(paths, "price_confirmed", usd_per_mtok=args.usd_per_mtok, source=args.source)
  .dev/research/jev-vs-keyword-table-611/harness/events.py:109:        rec = append_event(paths, "lead_go", evidence=paths.rule, rule_sha256=loader.sha256_file(paths.rule), words=args.words)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:170:    events.append_event(paths, "gate1", passed=not failed, failed=failed)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:177:    events.append_event(paths, "gate2", passed=not failed, failed=failed)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:190:    events.append_event(paths, "freeze", evidence=paths.corpus, what="corpus", prompts=len(rows))
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:204:    events.append_event(paths, "freeze", evidence=paths.table_answers, what="table")
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:212:    events.append_event(paths, "rule_freeze", evidence=paths.rule)
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:240:    return events.append_event(paths, "tests_passed", command=" ".join(cmd), count=count, code_hashes=_code_hashes(paths))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:30:        events.append_event(p, "price_confirmed", usd_per_mtok=price, source="test")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:34:        events.append_event(p, "lead_go", evidence=p.rule, rule_sha256=loader.sha256_file(p.rule), words="go")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:107:    events.append_event(exp, "lead_go", rule_sha256="0" * 64, words="old")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:132:    events.append_event(exp, event)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:244:# ---- events (append-only, evidence, the three commands)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:247:    first = events.append_event(exp, "freeze", evidence=exp.corpus, what="corpus")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:249:    events.append_event(exp, "gate1", passed=True, failed=[])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:252:    assert first["evidence"] == "corpus/corpus.jsonl" and first["evidence_sha256"] == loader.sha256_file(exp.corpus)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:262:    events.append_event(exp, "first_request")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:267:        assert e["ts"] and e["evidence"], e["event"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:268:        assert re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]), e["event"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:269:    assert events.latest(exp, "gate2")["evidence"] == "decision-rule.md"          # no evidence of its own: tied to the rule file
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:272:def test_an_evidence_path_that_is_not_a_file_is_refused(exp, tmp_path):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:274:        events.append_event(exp, "freeze", evidence=tmp_path / "nope.txt")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:276:        events.main(["owner-input", "--evidence", str(tmp_path / "nope.txt"), "--note", "x", "--root", str(exp.root)])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:282:        events.append_event(exp, "made_up")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:284:        events.append_event(exp, "gate1", ts="now")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:290:    assert events.main(["owner-input", "--evidence", str(note), "--note", "owner set the operators", "--root", str(exp.root)]) == 0
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:295:    assert got["owner_input_received"]["evidence_sha256"] == loader.sha256_file(note)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:298:    assert all(e["evidence"] and re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]) for e in got.values())
probe family rule-copy, hit locations after the fix:
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:63:    """The committed rule file with its three open fields forced back to ``UNSET``, so a test never depends on whether the owner
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:68:    text = loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:69:    return re.sub(r"^(noul_low_operator|noul_high_operator|unresolved_failure_invalid_count): .*$", r"\1: UNSET", text,
  .dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py:84:    a copy of the committed rule file with its open fields set to UNSET.  Nothing here touches the real experiment folder."""
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:17:    s = s.replace("noul_low_operator: UNSET", f"noul_low_operator: {low}").replace("noul_high_operator: UNSET", f"noul_high_operator: {high}")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:18:    p.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", f"unresolved_failure_invalid_count: {count}"), encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:52:    assert "UNSET" in exp.rule.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:113:    exp.rule.write_text(exp.rule.read_text(encoding="utf-8").replace("noul_low_operator: le", "noul_low_operator: UNSET"), encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:193:    with pytest.raises(loader.LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:269:    assert events.latest(exp, "gate2")["evidence"] == "decision-rule.md"          # no evidence of its own: tied to the rule file
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:9:RULE = loader.EXPERIMENT / "decision-rule.md"
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:13:def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:14:    """A copy of the rule file with its open fields UNSET (unless ``text`` is given), whatever the live file holds now."""
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:21:    p = tmp_path / "decision-rule.md"
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:29:    rule = loader.load_rule(RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:30:    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} <= OPEN_FIELDS
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:31:    normal = loader.load_rule(_rule_copy(tmp_path))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:32:    assert {k for k in loader.RULE_KEYS if normal[k] == "UNSET"} == OPEN_FIELDS
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:38:    text = RULE.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:47:        loader.load_rule(_rule_copy(tmp_path, "status: AGREED", f"status: {status}"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:51:    s = RULE.read_text(encoding="utf-8")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:54:    p = _rule_copy(tmp_path, text=head + "## Agreement text (verbatim)\n\n## Relayed owner words" + tail)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:56:        loader.load_rule(p)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:61:    lines = [(f"{key}:" if line.startswith(key + ":") else line) for line in RULE.read_text(encoding="utf-8").splitlines()]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:62:    p = _rule_copy(tmp_path, text="\n".join(lines) + "\n")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:64:        loader.load_rule(p)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:69:        loader.load_rule(_rule_copy(tmp_path, drop_line="alpha_inverse:"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:71:        loader.load_rule(tmp_path / "nope.md")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:75:    with pytest.raises(LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:76:        loader.load_rule(_rule_copy(tmp_path), for_scoring=True)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:78:    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:79:    s = s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:80:    rule = loader.load_rule(_rule_copy(tmp_path, text=s), for_scoring=True)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:86:        loader.load_rule(_rule_copy(tmp_path, "noul_low_operator: UNSET", "noul_low_operator: gt"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py:88:        loader.load_rule(_rule_copy(tmp_path, "noul_high_operator: UNSET", "noul_high_operator: lt"))
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:83:@pytest.mark.parametrize("low_op,high_op", [("UNSET", "ge"), ("le", "UNSET"), ("gt", "ge"), ("le", "lt")])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:109:RULE = {"attempt_timeout_s": 10.0, "median_population": "answered_only"}
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:114:    s = latency_stats(attempts, RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:119:    s = latency_stats([_a("p1", 0.5), _a("p2", 2.0, answered=False)], RULE)
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:124:    rule = dict(RULE, median_population="include_timeouts_at_cap")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:130:    assert latency_stats([], RULE) == {"median": None, "slowest": None, "p90": None, "n": 0}
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py:132:        latency_stats([_a("p1", 1.0)], dict(RULE, median_population="all"))
probe family record-command, hit locations after the fix:
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:222:    """``uv run pytest <tests folder> -v``, the folder relative to the repository root when it is under it."""
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:227:    return ["uv", "run", "pytest", folder, "-v"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:5:import pytest
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:60:@pytest.mark.parametrize("edit,name", [
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:82:@pytest.mark.parametrize("attr,name", [("corpus", "hash_corpus"), ("selection_criteria", "hash_selection_criteria"),
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:98:@pytest.mark.parametrize("skip,name", [("go", "go_missing"), ("tests", "tests_not_recorded"), ("rule", "rule_not_frozen"),
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:129:@pytest.mark.parametrize("event", ["first_request", "run_end"])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:178:        with pytest.raises(GateError, match="already holds"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:193:    with pytest.raises(loader.LoadError, match="UNSET"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:199:    with pytest.raises(GateError, match="Gate 1"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:203:    with pytest.raises(GateError, match="missing"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:211:    with pytest.raises(loader.LoadError, match="privacy"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:216:@pytest.mark.parametrize("result,match", [((1, "1 failed, 3 passed"), "failed"), ((0, "no tests ran"), "no tests")])
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:218:    with pytest.raises(GateError, match=match):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:225:    assert rec["count"] == 12 and rec["command"].startswith("uv run pytest ") and rec["command"].endswith(" -v")
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:232:    assert gate._tests_command(loader.Paths()) == ["uv", "run", "pytest", ".dev/research/jev-vs-keyword-table-611/harness/tests", "-v"]
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:273:    with pytest.raises(ValueError, match="does not exist"):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:275:    with pytest.raises(SystemExit):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:281:    with pytest.raises(ValueError):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:283:    with pytest.raises(ValueError):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:302:    with pytest.raises(SystemExit):
  .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py:318:    assert spend.worst_case_usd(1_000_000, 0.042) == pytest.approx(0.042)
probe family docstring, hit locations after the fix:
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:9:  gate.py gate2           everything Gate 1 checks, plus the rest; a pass is what the live run rests on (a lead_go that names the
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:157:    go = events.latest(paths, "lead_go")
  .dev/research/jev-vs-keyword-table-611/harness/gate.py:159:        failed.append("go_missing")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:25:EVENTS = ("owner_input_received", "freeze", "rule_freeze", "gate1", "gate2", "tests_passed", "price_confirmed", "lead_go",
  .dev/research/jev-vs-keyword-table-611/harness/events.py:81:    ap = argparse.ArgumentParser(prog="events.py", description="record owner input, the confirmed price and the lead's go")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:89:    c = sub.add_parser("go", help="record the lead's go, naming the rule file's current hash")
  .dev/research/jev-vs-keyword-table-611/harness/events.py:109:        rec = append_event(paths, "lead_go", evidence=paths.rule, rule_sha256=loader.sha256_file(paths.rule), words=args.words)


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
