10ea9be71d8508604f2274c380e34f5901dbe417
Review one task for spec compliance.

Task brief: ## Task 5: Build the scoring pipeline, verdict, report and decision record

Depends on: Task 3, Task 4

Extend `.dev/research/jev-vs-keyword-table-611/harness/scorer.py` and create `.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py`. Add `score(corpus, table_answers, jev_rows, rule, run_meta) -> dict`, `verdict(result, rule, run_meta) -> (state, reason)`, `render_report(result) -> str` and `render_decision_record(result, verdict, paths) -> str`, plus a command line `score --run-id ID [--root PATH]` and `score --run-id ID --rescore NAME --rule PATH`.

The result holds: per-arm correct count, accuracy over every frozen prompt (an error counts as not right and stays in the denominator), abstentions by reason, error counts; the paired breakdown (both right, only Jev, only table, neither); accuracy split into typed prompts and `ambiguous` or `none-fit` prompts, with a flag when a margin-test pass rests only on the second group; accuracy with and without prompts marked `seen_by_table`; the full disagreement list (prompt id, label, both answers, Jev probabilities, Noul value); cost; and the latency statistics from Task 3.

`run_meta` is built by the command from the events, the manifest and the run record, through functions of `events.py` and `gate.py`: whether each frozen file still matches the manifest, whether the `gate1` and `gate2` events exist, whether the table provenance file exists, the systemic stop reason from the `run_end` event, the models returned by `ok` rows, the number of `first_request` events and the count of unresolved failures.

`verdict` returns `JEV_BEATS_TABLE`, `NOT_CLEARLY` or `RUN_INVALID` with a reason as the Constraints say. The `RUN_INVALID` reasons are `frozen_file_changed`, `table_answers_changed`, `stopped_before_all_prompts`, `key_rejected`, `model_mismatch`, `unresolved_failures_above_limit`, `gate_result_missing`, `table_provenance_missing`, `second_live_run` and `no_answered_prompts`.

The command loads the rule with `for_scoring=True` and exits with a refusal, and no verdict, while any value is `UNSET`. It writes `report.md` and `decision-record.md` at the experiment root, for every verdict, and appends `scoring` and `verdict` events; it refuses to overwrite either file. `render_decision_record` lists the verdict, the rule file's hash, the report path, the exact text to post on issues 611, 609 and 612, and an empty section "Posted text and links" for the coordinator to fill; for `RUN_INVALID` it states that issue 612 stays undecided, and it states that the build and close decision on issue 612 is made only from a valid run. `render_report` is deterministic: the same inputs give identical bytes. A rescore under another rule file writes `rescores/NAME/report.md`, labelled non-decisional, appends no event and never changes the root files.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py -v` passes, using a temporary root for every file it writes.
- Tests check each verdict state is reached from synthetic inputs, with boundary cases on both sides of the margin test and both latency limits using stand-in rule values (T-12), and each `RUN_INVALID` reason, including `no_answered_prompts` for a run with no answered prompt (T-13).
- Tests check the paired breakdown and disagreement list against hand-built rows (T-11), the typed versus `ambiguous` or `none-fit` split and its flag, and a twice-failed prompt scored not right and kept in the denominator (T-06).
- A test shows two calls to `render_report` give byte-identical output, a rescore writes only under `rescores/` and leaves the root report unchanged, and a second `score` run refuses to overwrite the root report (T-14).
- A test shows the command exits with a refusal and writes no verdict while the rule has an `UNSET` value, and that the decision record names the three issues, the rule hash and the 612 statement for each of the three verdicts.
- No stand-in value from a test appears in `decision-rule.md`.

Acceptance criterion ids (in source order):
T5.AC1: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py -v` passes, using a temporary root for every file it writes.
T5.AC2: Tests check each verdict state is reached from synthetic inputs, with boundary cases on both sides of the margin test and both latency limits using stand-in rule values (T-12), and each `RUN_INVALID` reason, including `no_answered_prompts` for a run with no answered prompt (T-13).
T5.AC3: Tests check the paired breakdown and disagreement list against hand-built rows (T-11), the typed versus `ambiguous` or `none-fit` split and its flag, and a twice-failed prompt scored not right and kept in the denominator (T-06).
T5.AC4: A test shows two calls to `render_report` give byte-identical output, a rescore writes only under `rescores/` and leaves the root report unchanged, and a second `score` run refuses to overwrite the root report (T-14).
T5.AC5: A test shows the command exits with a refusal and writes no verdict while the rule has an `UNSET` value, and that the decision record names the three issues, the rule hash and the 612 statement for each of the three verdicts.
T5.AC6: No stand-in value from a test appears in `decision-rule.md`.
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
Start sha: 10ea9be71d8508604f2274c380e34f5901dbe417
Diff against the start snapshot: diff --git a.dev/research/jev-vs-keyword-table-611/harness/scorer.py b/.dev/research/jev-vs-keyword-table-611/harness/scorer.py
index d03fd9b60..1b078bc9d 100644
--- a.dev/research/jev-vs-keyword-table-611/harness/scorer.py
+++ b/.dev/research/jev-vs-keyword-table-611/harness/scorer.py
@@ -1,9 +1,33 @@
-"""Scorer, part 1: the pure functions of the decision rule.
+"""Scorer: the pure functions of the decision rule, then the scoring pipeline, the verdict, the report and the command line.
 
-Stdlib only.  Nothing here reads a file or the environment; every policy value comes in through the ``rule`` argument that
-``loader.load_rule`` returns.  The pipeline, the verdict and the report are added further down in this module.
+Part 1 (``right`` to ``latency_stats``) is pure: nothing in it reads a file or the environment; every policy value comes in
+through the ``rule`` argument that ``loader.load_rule`` returns.  Part 2 (``score``, ``verdict``, ``render_report``,
+``render_decision_record``) is pure too.  Only ``build_run_meta`` and ``main`` read or write files.
+
+Command line:
+  scorer.py score --run-id ID [--root PATH]                      score a run: write report.md and decision-record.md at the root
+  scorer.py score --run-id ID --rescore NAME --rule PATH [--root PATH]   non-decisional rescore under another rule file
+
+``jev-rows.jsonl`` holds one row per prompt: ``prompt_id``, ``attempts`` (each ``status``, ``error``, ``latency_s``, ``timed_out``),
+``final_status`` (``ok`` or ``error``), ``choice`` and ``probs`` (the answer to ``problem_type``), ``noul`` (the value of
+``any_type_fits``) and ``model``.  ``run_meta`` keys: ``frozen_changed`` (names of frozen files that no longer match the manifest),
+``gate1_event`` and ``gate2_event`` (a passing event exists), ``table_provenance_present``, ``stop_reason`` (``completed`` or the
+systemic reason of the ``run_end`` event), ``live_runs`` (count of ``first_request`` events), ``model_pin`` and ``spent_usd``.
 """
+import argparse
+import json
 import math
+import pathlib
+import re
+import sys
+
+_EXP = pathlib.Path(__file__).resolve().parents[1]
+_JEV = _EXP.parent / "346-review-loop-experiments" / "p15" / "jev"
+for _p in (str(_EXP), str(_JEV)):
+    if _p not in sys.path:
+        sys.path.insert(0, _p)
+
+from harness import events, gate, loader  # noqa: E402
 
 TYPED = ("bug", "build", "performance", "deployment", "security", "test")
 UNSET_LABELS = ("ambiguous", "none-fit")
@@ -92,3 +116,312 @@ def latency_stats(attempts, rule):
     slowest = [value(a) for a in attempts]
     return {"median": median(pop), "slowest": max(slowest) if slowest else None,
             "p90": percentile_nearest_rank(pop, 0.9), "n": len(pop)}
+
+
+# ---------------------------------------------------------------- part 2: the scoring pipeline, verdict and report
+
+STATES = ("JEV_BEATS_TABLE", "NOT_CLEARLY", "RUN_INVALID")
+INVALID_REASONS = ("gate_result_missing", "second_live_run", "table_answers_changed", "frozen_file_changed",
+                   "table_provenance_missing", "key_rejected", "model_mismatch", "stopped_before_all_prompts",
+                   "no_answered_prompts", "unresolved_failures_above_limit")
+_NAME = re.compile(r"[A-Za-z0-9_.-]+")
+
+
+class ScoreRefused(Exception):
+    """The scoring command refused: nothing was written."""
+
+
+def _tally(items):
+    both = sum(1 for i in items if i["jev_right"] and i["table_right"])
+    only_jev = sum(1 for i in items if i["jev_right"] and not i["table_right"])
+    only_table = sum(1 for i in items if i["table_right"] and not i["jev_right"])
+    return {"n": len(items), "jev_right": both + only_jev, "table_right": both + only_table, "both": both,
+            "only_jev": only_jev, "only_table": only_table, "neither": len(items) - both - only_jev - only_table}
+
+
+def _table_answer(table_by_id, pid):
+    if pid not in table_by_id:
+        raise ValueError(f"no table answer for prompt {pid}")
+    answer = table_by_id[pid].get("answer")
+    if answer is not None and answer not in TYPED:
+        raise ValueError(f"table answer for prompt {pid} is not a type or null")
+    return answer
+
+
+def score(corpus, table_answers, jev_rows, rule, run_meta):
+    """Score one run.  An error or a missing row counts as not right and stays in the denominator.  Returns a plain dict."""
+    table = {r["prompt_id"]: r for r in table_answers}
+    rows = {r["prompt_id"]: r for r in jev_rows}
+    per, attempts, models = [], [], set()
+    for c in corpus:
+        pid, label = c["id"], c["label"]
+        t_ans = _table_answer(table, pid)
+        row = rows.get(pid)
+        probs = noul = None
+        if row is not None and row["final_status"] == "ok":
+            j_ans, j_reason = jev_answer(row["noul"], row["choice"], rule)
+            status, probs, noul = "ok", row.get("probs"), row["noul"]
+            models.add(row.get("model"))
+        else:
+            j_ans, j_reason = None, ("error" if row is not None else "missing")
+            status = j_reason
+        for a in (row or {}).get("attempts", []):
+            attempts.append({"prompt_id": pid, "latency_s": a.get("latency_s") or 0.0, "timed_out": bool(a.get("timed_out")),
+                             "answered": a.get("status") == "ok"})
+        per.append({"id": pid, "label": label, "group": "unset" if label in UNSET_LABELS else "typed", "status": status,
+                    "jev": j_ans, "jev_reason": j_reason, "table": t_ans, "jev_right": status == "ok" and right(label, j_ans),
+                    "table_right": right(label, t_ans), "seen_by_table": bool(c.get("seen_by_table")), "probs": probs,
+                    "noul": noul, "n_attempts": len((row or {}).get("attempts", []))})
+    allt = _tally(per)
+    typed = _tally([p for p in per if p["group"] == "typed"])
+    unset = _tally([p for p in per if p["group"] == "unset"])
+    alpha = rule["alpha_inverse"]
+    passes = sign_test_passes(allt["only_jev"], allt["only_table"], alpha)
+    answered = [p for p in per if p["status"] == "ok"]
+    return {
+        "n_prompts": len(per), "n_rows": sum(1 for c in corpus if c["id"] in rows), "answered": len(answered),
+        "all": allt, "typed": typed, "unset_labels": unset,
+        "seen_by_table": {"marked": sum(1 for p in per if p["seen_by_table"]), "unmarked": _tally([p for p in per if not p["seen_by_table"]])},
+        "margin": {"b": allt["only_jev"], "c": allt["only_table"], "alpha_inverse": alpha, "passes": passes,
+                   "rests_on_unset_group": passes and not sign_test_passes(typed["only_jev"], typed["only_table"], alpha)},
+        "abstentions": {"jev": {r: sum(1 for p in answered if p["jev_reason"] == r) for r in ("none-fit", "not-settled")},
+                        "table": sum(1 for p in per if p["table"] is None)},
+        "errors": {"unresolved": sum(1 for p in per if p["status"] == "error"), "missing": sum(1 for p in per if p["status"] == "missing"),
+                   "recovered_by_rerun": sum(1 for p in answered if p["n_attempts"] > 1)},
+        "latency": latency_stats(attempts, rule), "attempts": len(attempts), "models": sorted(m for m in models if m),
+        "cost": {"spent_usd": run_meta.get("spent_usd")},
+        "disagreements": [{k: p[k] for k in ("id", "label", "jev", "jev_reason", "table", "status", "probs", "noul")}
+                          for p in per if p["jev"] != p["table"]],
+    }
+
+
+def verdict(result, rule, run_meta):
+    """``(state, reason)``.  ``RUN_INVALID`` reasons are checked in the order of ``INVALID_REASONS``; a valid run is
+    ``JEV_BEATS_TABLE`` only when the margin test passes and both latency limits hold.  ``unresolved_failure_invalid_count`` is the
+    count of unresolved failures that makes a run invalid, so a run with that many or more is invalid."""
+    rm = run_meta
+    if not (rm.get("gate1_event") and rm.get("gate2_event")):
+        return "RUN_INVALID", "gate_result_missing"
+    if rm.get("live_runs", 0) > 1:
+        return "RUN_INVALID", "second_live_run"
+    changed = list(rm.get("frozen_changed", []))
+    if "table_answers" in changed:
+        return "RUN_INVALID", "table_answers_changed"
+    if changed:
+        return "RUN_INVALID", "frozen_file_changed"
+    if not rm.get("table_provenance_present"):
+        return "RUN_INVALID", "table_provenance_missing"
+    stop, pin = rm.get("stop_reason"), rm.get("model_pin")
+    if stop == "key_rejected":
+        return "RUN_INVALID", "key_rejected"
+    if stop == "model_mismatch" or (pin and any(m != pin for m in result["models"])):
+        return "RUN_INVALID", "model_mismatch"
+    if stop != "completed" or result["n_rows"] < result["n_prompts"]:
+        return "RUN_INVALID", "stopped_before_all_prompts"
+    if result["answered"] == 0:
+        return "RUN_INVALID", "no_answered_prompts"
+    if result["errors"]["unresolved"] >= rule["unresolved_failure_invalid_count"]:
+        return "RUN_INVALID", "unresolved_failures_above_limit"
+    lat, fails = result["latency"], []
+    if not result["margin"]["passes"]:
+        fails.append("margin_not_passed")
+    if lat["median"] is None or lat["median"] > rule["median_limit_s"]:
+        fails.append("median_above_limit")
+    if lat["slowest"] is None or lat["slowest"] > rule["slowest_limit_s"]:
+        fails.append("slowest_above_limit")
+    if fails:
+        return "NOT_CLEARLY", ",".join(fails)
+    return "JEV_BEATS_TABLE", "margin_test_passed_and_both_latency_limits_hold"
+
+
+def _f(x, digits=3):
+    return "n/a" if x is None else f"{x:.{digits}f}"
+
+
+def _ratio(k, n):
+    return f"{k}/{n} ({_f(k / n if n else None)})"
+
+
+def _probs(p):
+    if p is None:
+        return ""
+    return ";".join(f"{k}={_f(v)}" for k, v in sorted(p.items())) if isinstance(p, dict) else json.dumps(p, sort_keys=True)
+
+
+def render_report(result):
+    """The report as markdown.  Deterministic: the same result gives the same bytes (no time, no path, sorted keys)."""
+    a, t, u, m, lat = result["all"], result["typed"], result["unset_labels"], result["margin"], result["latency"]
+    v = result.get("verdict")
+    out = ["# Jev versus the keyword table: report", ""]
+    if result.get("rescore"):
+        out += [f"**NON-DECISIONAL RESCORE `{result['rescore']['name']}` under rule file {result['rescore']['rule_sha256']}.** "
+                "The root report and decision record are not changed by it.", ""]
+    if v:
+        out += [f"Verdict: **{v['state']}** ({v['reason']})", ""]
+    out += ["## Accuracy over every frozen prompt", "", "| Arm | Right | Accuracy |", "|---|---|---|",
+            f"| Jev | {a['jev_right']} of {a['n']} | {_ratio(a['jev_right'], a['n'])} |",
+            f"| Table | {a['table_right']} of {a['n']} | {_ratio(a['table_right'], a['n'])} |", "",
+            "## Paired breakdown", "", "| Both right | Only Jev (b) | Only table (c) | Neither |", "|---|---|---|---|",
+            f"| {a['both']} | {a['only_jev']} | {a['only_table']} | {a['neither']} |", "",
+            "## Margin test (exact one-sided sign test, integer arithmetic)", "",
+            f"b = {m['b']}, c = {m['c']}, significance 1 in {m['alpha_inverse']}: **{'PASS' if m['passes'] else 'FAIL'}**"]
+    if m["rests_on_unset_group"]:
+        out += ["", "FLAG: the pass rests only on the `ambiguous` and `none-fit` prompts; the typed prompts alone do not pass."]
+    out += ["", "## Typed prompts versus `ambiguous` and `none-fit` prompts", "",
+            "| Group | Prompts | Jev right | Table right | Only Jev | Only table |", "|---|---|---|---|---|---|"]
+    for name, g in (("typed", t), ("ambiguous or none-fit", u)):
+        out.append(f"| {name} | {g['n']} | {_ratio(g['jev_right'], g['n'])} | {_ratio(g['table_right'], g['n'])} | "
+                   f"{g['only_jev']} | {g['only_table']} |")
+    un = result["seen_by_table"]["unmarked"]
+    out += ["", "## Prompts marked `seen_by_table`", "", f"{result['seen_by_table']['marked']} prompts are marked. Without them:",
+            f"Jev {_ratio(un['jev_right'], un['n'])}, table {_ratio(un['table_right'], un['n'])}, only Jev {un['only_jev']}, "
+            f"only table {un['only_table']}.", "", "## Abstentions and errors", "",
+            f"- Jev none-fit: {result['abstentions']['jev']['none-fit']}; Jev not-settled: {result['abstentions']['jev']['not-settled']}",
+            f"- Table unset: {result['abstentions']['table']}",
+            f"- Unresolved failures (error, not right): {result['errors']['unresolved']}; no row: {result['errors']['missing']}; "
+            f"recovered by the one rerun: {result['errors']['recovered_by_rerun']}", "", "## Latency (client side)", "",
+            f"- Median over each prompt's final answered attempt: {_f(lat['median'])} s",
+            f"- Slowest over all attempts (a timeout counts at its cap): {_f(lat['slowest'])} s",
+            f"- 90th percentile (nearest rank): {_f(lat['p90'])} s",
+            f"- Prompts in the median: {lat['n']}; attempts: {result['attempts']}", "", "## Cost", "",
+            f"- Spent: {_f(result['cost']['spent_usd'], 4)} USD", f"- Models returned: {', '.join(result['models']) or 'none'}", "",
+            "## Disagreements (Jev answer differs from the table answer)", ""]
+    if result["disagreements"]:
+        out += ["| Prompt | Label | Jev | Jev reason | Table | Status | Jev probabilities | Noul |", "|---|---|---|---|---|---|---|---|"]
+        for d in result["disagreements"]:
+            out.append(f"| {d['id']} | {d['label']} | {d['jev'] or 'unset'} | {d['jev_reason'] or ''} | {d['table'] or 'unset'} | "
+                       f"{d['status']} | {_probs(d['probs'])} | {_f(d['noul'])} |")
+    else:
+        out.append("None.")
+    return "\n".join(out) + "\n"
+
+
+def _rel(path):
+    try:
+        return pathlib.Path(path).resolve().relative_to(gate.REPO).as_posix()
+    except ValueError:
+        return str(path)
+
+
+def render_decision_record(result, verdict_pair, paths):
+    """The decision record: the verdict, the rule file's hash, the report path, the exact text to post on issues 611, 609 and 612,
+    and an empty section for the coordinator to fill in once the text is posted."""
+    state, reason = verdict_pair
+    a, lat = result["all"], result["latency"]
+    facts = (f"Jev right on {a['jev_right']} of {a['n']} prompts, table right on {a['table_right']} of {a['n']}; only Jev {a['only_jev']}, "
+             f"only table {a['only_table']}; margin test {'passed' if result['margin']['passes'] else 'not passed'}; "
+             f"median {_f(lat['median'])} s, slowest {_f(lat['slowest'])} s.")
+    report = _rel(paths.report)
+    if state == "RUN_INVALID":
+        head = f"The comparison run is INVALID ({reason})."
+        t611 = f"{head} No result is claimed. The harness, run record and report are in `{report}` and `{_rel(paths.decision_record)}`."
+        t609 = f"Step 2 (Jev against the keyword table) produced no valid result: {reason}. The preflight is not decided by it."
+        t612 = ("The run was invalid, so issue 612 stays undecided. The build and close decision on issue 612 is made only from a "
+                "valid run.")
+    else:
+        head = f"Result: {state} ({reason})."
+        t611 = f"{head} {facts} Full report: `{report}`."
+        t609 = f"Step 2 (Jev against the keyword table) is done: {state}. {facts}"
+        t612 = (f"A valid run says {state}. {facts} The build and close decision on issue 612 is made only from a valid run, and "
+                "this is one.")
+    return "\n".join([
+        "# Decision record: Jev versus the keyword table (issue 611)", "", f"Verdict: **{state}**", f"Reason: {reason}",
+        f"Rule file hash (SHA-256): {loader.sha256_file(paths.rule)}", f"Report: `{report}`", "",
+        "The build and close decision on issue 612 is made only from a valid run.",
+        *(["Issue 612 stays undecided: this run is invalid."] if state == "RUN_INVALID" else []), "",
+        "## Text to post on issue 611", "", t611, "", "## Text to post on issue 609", "", t609, "", "## Text to post on issue 612", "", t612,
+        "", "## Posted text and links", "", "(The coordinator fills this in after posting: where each text went, with its link.)", ""])
+
+
+def build_run_meta(paths, run_id):
+    """The facts about a run that the scorer cannot read from its rows: what still matches the manifest, which gate and run events
+    exist, and how the run ended.  Built from the manifest, the events file and the files themselves."""
+    m = gate.read_manifest(paths)
+    changed = []
+    frozen = dict(gate.CORPUS_SIDE, rule="rule", table_answers="table_answers", table_provenance="table_provenance")
+    for key, attr in frozen.items():
+        p = getattr(paths, attr)
+        if key == "table_provenance" and not p.is_file():
+            continue
+        if key not in m or not p.is_file() or loader.sha256_file(p) != m[key]:
+            changed.append(key)
+    tests = events.latest(paths, "tests_passed")
+    if tests is None or tests.get("code_hashes") != gate._code_hashes(paths):
+        changed.append("code")
+    log = events.read_events(paths)
+    ends = [e for e in log if e["event"] == "run_end" and e.get("run_id") == run_id]
+    return {"frozen_changed": changed,
+            "gate1_event": any(e["event"] == "gate1" and e.get("passed") for e in log),
+            "gate2_event": any(e["event"] == "gate2" and e.get("passed") for e in log),
+            "table_provenance_present": paths.table_provenance.is_file(),
+            "stop_reason": ends[-1].get("reason") if ends else "no_run_end",
+            "live_runs": sum(1 for e in log if e["event"] == "first_request"),
+            "model_pin": m.get("model_pin"), "spent_usd": ends[-1].get("spent_usd") if ends else None}
+
+
+def _write_new(path, text):
+    path.parent.mkdir(parents=True, exist_ok=True)
+    try:
+        with open(path, "x", encoding="utf-8") as f:
+            f.write(text)
+    except FileExistsError:
+        raise ScoreRefused(f"{path.name} already exists and is never overwritten") from None
+
+
+def _score_command(paths, args):
+    for label, value in (("run id", args.run_id), ("rescore name", args.rescore)):
+        if value is not None and (not _NAME.fullmatch(value) or value in (".", "..")):
+            raise ScoreRefused(f"the {label} may hold only letters, digits, dot, underscore and hyphen")
+    if args.rescore:
+        rule = loader.load_rule(args.rule, for_scoring=True)
+        out = paths.rescores / args.rescore / "report.md"
+        if out.exists():
+            raise ScoreRefused(f"{out.name} already exists and is never overwritten")
+    else:
+        rule = loader.load_rule(paths.rule, for_scoring=True)
+        if paths.report.exists() or paths.decision_record.exists():
+            raise ScoreRefused("report.md or decision-record.md already exists and is never overwritten")
+    corpus = loader.load_corpus(paths.corpus)
+    table = loader.load_table_answers(paths.table_answers)
+    rows = loader._jsonl(paths.runs / args.run_id / "jev-rows.jsonl", "jev rows")
+    meta = build_run_meta(paths, args.run_id)
+    if args.rescore:
+        meta["frozen_changed"] = [k for k in meta["frozen_changed"] if k != "rule"]
+    result = score(corpus, table, rows, rule, meta)
+    state, reason = verdict(result, rule, meta)
+    result["verdict"] = {"state": state, "reason": reason}
+    if args.rescore:
+        result["rescore"] = {"name": args.rescore, "rule_sha256": loader.sha256_file(args.rule)}
+        _write_new(out, render_report(result))
+        return state, reason
+    _write_new(paths.report, render_report(result))
+    _write_new(paths.decision_record, render_decision_record(result, (state, reason), paths))
+    rule_sha = loader.sha256_file(paths.rule)
+    events.append_event(paths, "scoring", evidence=paths.report, run_id=args.run_id, prompts=result["n_prompts"])
+    events.append_event(paths, "verdict", evidence=paths.decision_record, run_id=args.run_id, state=state, reason=reason,
+                        rule_sha256=rule_sha)
+    return state, reason
+
+
+def main(argv=None):
+    ap = argparse.ArgumentParser(prog="scorer.py", description="score a finished run against the frozen decision rule")
+    sub = ap.add_subparsers(dest="cmd", required=True)
+    s = sub.add_parser("score", help="write report.md and decision-record.md for a run, or a non-decisional rescore")
+    s.add_argument("--run-id", required=True)
+    s.add_argument("--root", default=None)
+    s.add_argument("--rescore", default=None, help="NAME of a non-decisional rescore under another rule file")
+    s.add_argument("--rule", default=None, help="the other rule file, with --rescore")
+    args = ap.parse_args(argv)
+    if bool(args.rescore) != bool(args.rule):
+        ap.error("--rescore and --rule go together")
+    try:
+        state, reason = _score_command(loader.Paths(args.root), args)
+    except (ScoreRefused, ValueError) as e:
+        print(f"REFUSED: {e}", file=sys.stderr)
+        return 1
+    print(f"{state}: {reason}")
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py
new file mode 100644
index 000000000..9b2fec505
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py
@@ -0,0 +1,372 @@
+import json
+import re
+
+import pytest
+from harness import events, gate, loader, scorer
+from harness.scorer import (
+    build_run_meta,
+    render_decision_record,
+    render_report,
+    score,
+    verdict,
+)
+
+PIN = "jev-1.14.0"
+IDS = [f"p{i}" for i in range(8)]                  # labels: bug build performance deployment security test ambiguous none-fit
+LABELS = dict(zip(IDS, ["bug", "build", "performance", "deployment", "security", "test", "ambiguous", "none-fit"]))
+CORPUS = [{"id": i, "label": LABELS[i], "seen_by_table": False} for i in IDS]
+# stand-in values: none of these may appear in the committed rule file
+RULE = {"alpha_inverse": 20, "median_limit_s": 1.5, "slowest_limit_s": 4.5, "attempt_timeout_s": 10.0, "median_population": "answered_only",
+        "noul_low": 0.3, "noul_high": 0.7, "noul_low_operator": "le", "noul_high_operator": "ge",
+        "unresolved_failure_invalid_count": 77}
+META = {"frozen_changed": [], "gate1_event": True, "gate2_event": True, "table_provenance_present": True, "stop_reason": "completed",
+        "live_runs": 1, "model_pin": PIN, "spent_usd": 0.0123}
+PASSING = lambda cmd: (0, "12 passed in 0.1s")  # noqa: E731
+
+
+def jrow(pid, choice=None, noul=None, lat=1.0, attempts=None, final="ok", model=PIN):
+    """A Jev row.  By default Jev is right: the label's own type for a typed prompt, an unset answer (low Noul) otherwise."""
+    typed = LABELS[pid] not in ("ambiguous", "none-fit")
+    choice = choice or (LABELS[pid] if typed else "bug")
+    noul = noul if noul is not None else (0.9 if typed else 0.1)
+    atts = attempts or [{"status": "ok", "error": None, "latency_s": lat, "timed_out": False}]
+    ok = final == "ok"
+    return {"prompt_id": pid, "attempts": atts, "final_status": final, "choice": choice if ok else None,
+            "probs": {choice: 0.8, "test": 0.2} if ok else None, "noul": noul if ok else None, "model": model if ok else None}
+
+
+def table_rows(right_ids):
+    """Table answers: right on ``right_ids``, wrong on every other prompt."""
+    out = []
+    for i in IDS:
+        typed = LABELS[i] not in ("ambiguous", "none-fit")
+        right = LABELS[i] if typed else None
+        wrong = ("test" if LABELS[i] == "bug" else "bug")
+        out.append({"prompt_id": i, "answer": right if i in right_ids else wrong})
+    return out
+
+
+def run(rows, table_right=(), rule=RULE, meta=META, corpus=CORPUS):
+    result = score(corpus, table_rows(set(table_right)), rows, rule, meta)
+    return result, verdict(result, rule, meta)
+
+
+def perfect(**kw):
+    return [jrow(i, **kw) for i in IDS]
+
+
+# ---- each verdict state, with the boundaries on both sides (T-12)
+
+def test_jev_beats_the_table_when_margin_and_latency_hold():
+    result, v = run(perfect(), table_right=IDS[:3])
+    assert result["margin"]["b"] == 5 and result["margin"]["c"] == 0 and v[0] == "JEV_BEATS_TABLE"
+
+
+def test_margin_boundary_five_nil_passes_and_four_nil_fails():
+    assert run(perfect(), table_right=IDS[:3])[1][0] == "JEV_BEATS_TABLE"
+    state, reason = run(perfect(), table_right=IDS[:4])[1]
+    assert (state, reason) == ("NOT_CLEARLY", "margin_not_passed")
+
+
+@pytest.mark.parametrize("lat,state", [(1.5, "JEV_BEATS_TABLE"), (1.6, "NOT_CLEARLY")])
+def test_median_limit_boundary(lat, state):
+    result, v = run(perfect(lat=lat), table_right=IDS[:3])
+    assert v[0] == state and (state == "JEV_BEATS_TABLE" or v[1] == "median_above_limit")
+
+
+@pytest.mark.parametrize("slow,state", [(4.5, "JEV_BEATS_TABLE"), (4.6, "NOT_CLEARLY")])
+def test_slowest_limit_boundary_counts_every_attempt(slow, state):
+    rows = perfect()
+    rows[0] = jrow("p0", attempts=[{"status": "refused", "error": "http_500", "latency_s": slow, "timed_out": False},
+                                   {"status": "ok", "error": None, "latency_s": 1.0, "timed_out": False}])
+    result, v = run(rows, table_right=IDS[:3])
+    assert v[0] == state and (state == "JEV_BEATS_TABLE" or v[1] == "slowest_above_limit")
+
+
+def test_a_timeout_counts_at_its_cap_in_the_slowest():
+    rows = perfect()
+    rows[0] = jrow("p0", attempts=[{"status": "refused", "error": "timeout", "latency_s": 3.0, "timed_out": True},
+                                   {"status": "ok", "error": None, "latency_s": 1.0, "timed_out": False}])
+    result, v = run(rows, table_right=IDS[:3])
+    assert result["latency"]["slowest"] == 10.0 and v == ("NOT_CLEARLY", "slowest_above_limit")
+
+
+def test_not_clearly_names_every_failed_test():
+    rows = perfect(lat=5.0)
+    assert run(rows, table_right=IDS[:4])[1] == ("NOT_CLEARLY", "margin_not_passed,median_above_limit,slowest_above_limit")
+
+
+# ---- RUN_INVALID, each reason (T-13)
+
+@pytest.mark.parametrize("change,reason", [
+    ({"gate1_event": False}, "gate_result_missing"),
+    ({"gate2_event": False}, "gate_result_missing"),
+    ({"live_runs": 2}, "second_live_run"),
+    ({"frozen_changed": ["table_answers"]}, "table_answers_changed"),
+    ({"frozen_changed": ["corpus"]}, "frozen_file_changed"),
+    ({"frozen_changed": ["code"]}, "frozen_file_changed"),
+    ({"table_provenance_present": False}, "table_provenance_missing"),
+    ({"stop_reason": "key_rejected"}, "key_rejected"),
+    ({"stop_reason": "model_mismatch"}, "model_mismatch"),
+    ({"stop_reason": "spend_bound"}, "stopped_before_all_prompts"),
+    ({"stop_reason": "no_run_end"}, "stopped_before_all_prompts"),
+])
+def test_each_meta_reason_makes_the_run_invalid(change, reason):
+    assert run(perfect(), table_right=IDS[:3], meta=dict(META, **change))[1] == ("RUN_INVALID", reason)
+
+
+def test_a_returned_model_other_than_the_pin_is_a_model_mismatch():
+    rows = perfect()
+    rows[3] = jrow("p3", model="jev-9.9.9")
+    assert run(rows, table_right=IDS[:3])[1] == ("RUN_INVALID", "model_mismatch")
+
+
+def test_fewer_rows_than_prompts_is_stopped_before_all_prompts():
+    assert run(perfect()[:6], table_right=IDS[:3])[1] == ("RUN_INVALID", "stopped_before_all_prompts")
+
+
+def test_a_run_with_no_answered_prompt_is_invalid():
+    rows = [jrow(i, final="error", attempts=[{"status": "refused", "error": "http_500", "latency_s": 1.0, "timed_out": False}] * 2)
+            for i in IDS]
+    assert run(rows)[1] == ("RUN_INVALID", "no_answered_prompts")
+
+
+def test_unresolved_failures_at_the_limit_make_the_run_invalid():
+    bad = {"status": "refused", "error": "http_500", "latency_s": 1.0, "timed_out": False}
+    rows = perfect()
+    rows[0] = jrow("p0", final="error", attempts=[bad, bad])
+    assert run(rows, table_right=IDS[:3], rule=dict(RULE, unresolved_failure_invalid_count=2))[1][0] != "RUN_INVALID"
+    rows[1] = jrow("p1", final="error", attempts=[bad, bad])
+    assert run(rows, table_right=IDS[:3], rule=dict(RULE, unresolved_failure_invalid_count=2))[1] == (
+        "RUN_INVALID", "unresolved_failures_above_limit")
+
+
+def test_the_first_failed_check_wins_and_every_reason_is_reachable():
+    meta = dict(META, gate2_event=False, live_runs=2, frozen_changed=["corpus"])
+    assert run(perfect(), meta=meta)[1] == ("RUN_INVALID", "gate_result_missing")
+    assert set(scorer.INVALID_REASONS) == {"frozen_file_changed", "table_answers_changed", "stopped_before_all_prompts", "key_rejected",
+                                           "model_mismatch", "unresolved_failures_above_limit", "gate_result_missing",
+                                           "table_provenance_missing", "second_live_run", "no_answered_prompts"}
+
+
+# ---- the paired breakdown, the disagreement list, the split and a twice-failed prompt (T-11, T-06)
+
+def hand_built():
+    rows = [jrow("p0"), jrow("p1"), jrow("p2", choice="bug"), jrow("p3", choice="bug"), jrow("p4", choice="bug"),
+            jrow("p5", choice="bug"), jrow("p6"), jrow("p7", choice="bug", noul=0.9)]
+    table = [{"prompt_id": p, "answer": a} for p, a in zip(IDS, ["test", "build", "performance", "bug", "test", "bug", "bug", None])]
+    return rows, table
+
+
+def test_paired_breakdown_and_disagreements_match_a_hand_count():
+    rows, table = hand_built()
+    r = score(CORPUS, table, rows, RULE, META)
+    assert (r["all"]["both"], r["all"]["only_jev"], r["all"]["only_table"], r["all"]["neither"]) == (1, 2, 2, 3)
+    assert (r["all"]["jev_right"], r["all"]["table_right"]) == (3, 3)
+    assert [d["id"] for d in r["disagreements"]] == ["p0", "p2", "p4", "p6", "p7"]
+    d = {x["id"]: x for x in r["disagreements"]}
+    assert d["p6"]["jev"] is None and d["p6"]["jev_reason"] == "none-fit" and d["p6"]["table"] == "bug" and d["p6"]["noul"] == 0.1
+    assert d["p0"]["probs"] == {"bug": 0.8, "test": 0.2}
+
+
+def test_typed_and_unset_label_split():
+    rows, table = hand_built()
+    r = score(CORPUS, table, rows, RULE, META)
+    assert (r["typed"]["n"], r["typed"]["only_jev"], r["typed"]["only_table"]) == (6, 1, 1)
+    assert (r["unset_labels"]["n"], r["unset_labels"]["only_jev"], r["unset_labels"]["only_table"]) == (2, 1, 1)
+    assert r["abstentions"]["jev"] == {"none-fit": 1, "not-settled": 0} and r["abstentions"]["table"] == 1
+
+
+def test_a_pass_resting_only_on_the_unset_label_prompts_is_flagged():
+    corpus = [{"id": "t0", "label": "bug", "seen_by_table": False}] + [
+        {"id": f"u{i}", "label": "none-fit", "seen_by_table": False} for i in range(7)]
+    rows = [dict(jrow("p0"), prompt_id="t0")] + [dict(jrow("p7"), prompt_id=f"u{i}") for i in range(7)]
+    table = [{"prompt_id": "t0", "answer": "bug"}] + [{"prompt_id": f"u{i}", "answer": "bug"} for i in range(7)]
+    r = score(corpus, table, rows, RULE, META)
+    assert r["margin"]["passes"] and r["margin"]["rests_on_unset_group"]
+    corpus2 = [{"id": f"t{i}", "label": "bug", "seen_by_table": False} for i in range(6)]
+    rows2 = [dict(jrow("p0"), prompt_id=f"t{i}") for i in range(6)]
+    table2 = [{"prompt_id": f"t{i}", "answer": "test"} for i in range(6)]
+    r2 = score(corpus2, table2, rows2, RULE, META)
+    assert r2["margin"]["passes"] and not r2["margin"]["rests_on_unset_group"]
+
+
+def test_accuracy_with_and_without_the_prompts_the_table_saw():
+    corpus = [dict(c, seen_by_table=(c["id"] == "p0")) for c in CORPUS]
+    rows, table = hand_built()
+    r = score(corpus, table, rows, RULE, META)
+    assert r["seen_by_table"]["marked"] == 1 and r["seen_by_table"]["unmarked"]["n"] == 7
+    assert r["seen_by_table"]["unmarked"]["jev_right"] == 2       # p0 was Jev's right answer outside p0: p1 and p6
+
+
+def test_a_twice_failed_prompt_is_not_right_and_stays_in_the_denominator():
+    bad = {"status": "refused", "error": "http_500", "latency_s": 1.0, "timed_out": False}
+    rows = perfect()
+    rows[6] = jrow("p6", final="error", attempts=[bad, bad])         # ambiguous label: an unset answer would be right, an error is not
+    r = score(CORPUS, table_rows(set()), rows, RULE, META)
+    assert r["all"]["jev_right"] == 7 and r["all"]["n"] == 8 and r["errors"]["unresolved"] == 1 and r["attempts"] == 9
+    assert [d["status"] for d in r["disagreements"] if d["id"] == "p6"] == ["error"]
+    assert "| Jev | 7 of 8 | 7/8 (0.875) |" in render_report(r)
+
+
+def test_a_rerun_that_answers_is_counted_as_recovered():
+    rows = perfect()
+    rows[0] = jrow("p0", attempts=[{"status": "refused", "error": "http_500", "latency_s": 1.0, "timed_out": False},
+                                   {"status": "ok", "error": None, "latency_s": 1.2, "timed_out": False}])
+    r = score(CORPUS, table_rows(set()), rows, RULE, META)
+    assert r["errors"]["recovered_by_rerun"] == 1 and r["errors"]["unresolved"] == 0 and r["all"]["jev_right"] == 8
+
+
+def test_an_unset_operator_is_refused_by_the_scorer():
+    with pytest.raises(ValueError):
+        score(CORPUS, table_rows(set()), perfect(), dict(RULE, noul_low_operator="UNSET"), META)
+
+
+# ---- the report and the decision record
+
+def test_render_report_is_deterministic_and_names_the_verdict():
+    result, v = run(perfect(), table_right=IDS[:3])
+    result["verdict"] = {"state": v[0], "reason": v[1]}
+    text = render_report(result)
+    assert render_report(result) == text and "Verdict: **JEV_BEATS_TABLE**" in text and "**PASS**" in text
+    assert "90th percentile (nearest rank): 1.000 s" in text and "Spent: 0.0123 USD" in text
+
+
+def test_the_decision_record_names_the_issues_the_rule_hash_and_the_612_statement_for_each_verdict(exp):
+    sha = loader.sha256_file(exp.rule)
+    result, _ = run(perfect(), table_right=IDS[:3])
+    for pair in (("JEV_BEATS_TABLE", "ok"), ("NOT_CLEARLY", "margin_not_passed"), ("RUN_INVALID", "key_rejected")):
+        text = render_decision_record(result, pair, exp)
+        assert pair[0] in text and sha in text and "## Posted text and links" in text
+        for n in ("611", "609", "612"):
+            assert f"## Text to post on issue {n}" in text
+        assert "build and close decision on issue 612 is made only from a valid run" in text
+        assert ("stays undecided" in text) == (pair[0] == "RUN_INVALID")
+        assert text.split("## Posted text and links")[1].strip().startswith("(The coordinator fills this in")
+
+
+def test_no_stand_in_value_of_these_tests_is_in_the_committed_rule_file():
+    text = loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8")
+    for key in ("median_limit_s", "slowest_limit_s", "unresolved_failure_invalid_count"):
+        assert f"{key}: {RULE[key]}" not in text
+
+
+# ---- the command (a temporary root for every file)
+
+@pytest.fixture
+def exp(exp, monkeypatch):
+    """The command line builds ``Paths`` from a root alone, so point its default jevlib folder at the fixture's stand-in."""
+    monkeypatch.setattr(loader, "JEVLIB_DIR", exp.jevlib_dir)
+    return exp
+
+
+def prepare(exp, rows=None, table_right=(), run_id="r1"):
+    """Freeze everything, pass both gates, then write a finished run: the state of a root just before ``score`` is run."""
+    s = exp.rule.read_text(encoding="utf-8")
+    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
+    exp.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3"), encoding="utf-8")
+    gate.freeze_corpus(exp)
+    gate.freeze_table(exp)
+    gate.freeze_rule(exp)
+    events.append_event(exp, "price_confirmed", usd_per_mtok=0.042, source="test")
+    gate.record_tests(exp, runner=PASSING)
+    events.append_event(exp, "lead_go", rule_sha256=loader.sha256_file(exp.rule), words="go")
+    assert gate.gate1(exp) == [] and gate.gate2(exp) == []
+    events.append_event(exp, "first_request")
+    d = exp.runs / run_id
+    d.mkdir(parents=True)
+    d.joinpath("jev-rows.jsonl").write_text("\n".join(json.dumps(r) for r in (rows or perfect())) + "\n", encoding="utf-8")
+    events.append_event(exp, "run_end", run_id=run_id, reason="completed", spent_usd=0.01)
+
+
+def score_cmd(exp, *extra, run_id="r1"):
+    return scorer.main(["score", "--run-id", run_id, "--root", str(exp.root), *extra])
+
+
+def test_score_writes_the_report_and_the_decision_record_and_the_two_events(exp, capsys):
+    prepare(exp)
+    assert score_cmd(exp) == 0
+    assert capsys.readouterr().out.startswith("JEV_BEATS_TABLE")
+    assert exp.report.is_file() and "Verdict: **JEV_BEATS_TABLE**" in exp.report.read_text(encoding="utf-8")
+    rec = exp.decision_record.read_text(encoding="utf-8")
+    assert loader.sha256_file(exp.rule) in rec
+    log = {e["event"]: e for e in events.read_events(exp)}
+    assert log["scoring"]["evidence"] == "report.md" and log["verdict"]["state"] == "JEV_BEATS_TABLE"
+    assert log["verdict"]["rule_sha256"] == loader.sha256_file(exp.rule)
+
+
+def test_a_second_score_run_refuses_to_overwrite_the_root_report(exp, capsys):
+    prepare(exp)
+    assert score_cmd(exp) == 0
+    before = (exp.report.read_bytes(), exp.decision_record.read_bytes(), exp.events.read_bytes())
+    capsys.readouterr()
+    assert score_cmd(exp) == 1
+    assert "never overwritten" in capsys.readouterr().err
+    assert (exp.report.read_bytes(), exp.decision_record.read_bytes(), exp.events.read_bytes()) == before
+
+
+def test_score_refuses_and_writes_no_verdict_while_a_rule_value_is_unset(exp, capsys):
+    (exp.runs / "r1").mkdir(parents=True)
+    (exp.runs / "r1" / "jev-rows.jsonl").write_text(json.dumps(jrow("p0")) + "\n")
+    assert score_cmd(exp) == 1
+    assert "UNSET" in capsys.readouterr().err
+    assert not exp.report.exists() and not exp.decision_record.exists() and events.latest(exp, "verdict") is None
+
+
+def test_a_run_that_cannot_be_scored_is_refused_without_a_report(exp, capsys):
+    prepare(exp)
+    assert score_cmd(exp, run_id="nope") == 1
+    assert "jev rows missing" in capsys.readouterr().err
+    assert score_cmd(exp, run_id="../x") == 1
+    assert not exp.report.exists()
+
+
+def test_a_changed_table_answers_file_gives_a_report_with_run_invalid(exp, capsys):
+    prepare(exp)
+    exp.table_answers.write_text(exp.table_answers.read_text() + "\n")
+    assert score_cmd(exp) == 0
+    assert capsys.readouterr().out.strip() == "RUN_INVALID: table_answers_changed"
+    assert "stays undecided" in exp.decision_record.read_text(encoding="utf-8")
+    assert events.latest(exp, "verdict")["state"] == "RUN_INVALID"
+
+
+def test_run_meta_reads_the_events_and_the_manifest(exp):
+    prepare(exp)
+    m = build_run_meta(exp, "r1")
+    assert m["frozen_changed"] == [] and m["gate1_event"] and m["gate2_event"] and m["table_provenance_present"]
+    assert (m["stop_reason"], m["live_runs"], m["model_pin"], m["spent_usd"]) == ("completed", 1, PIN, 0.01)
+    assert build_run_meta(exp, "other")["stop_reason"] == "no_run_end"
+    exp.questions_py.write_text("# changed\n")
+    assert set(build_run_meta(exp, "r1")["frozen_changed"]) == {"questions", "code"}
+
+
+def test_a_rescore_writes_only_under_rescores_and_changes_nothing_else(exp, tmp_path, capsys):
+    prepare(exp)
+    assert score_cmd(exp) == 0
+    alt = tmp_path / "alt-rule.md"
+    alt.write_text(exp.rule.read_text(encoding="utf-8").replace("slowest_limit_s: 5", "slowest_limit_s: 0.5"), encoding="utf-8")
+    root_files = {p: p.read_bytes() for p in exp.root.rglob("*") if p.is_file()}
+    capsys.readouterr()
+    assert score_cmd(exp, "--rescore", "tight", "--rule", str(alt)) == 0
+    assert capsys.readouterr().out.startswith("NOT_CLEARLY: slowest_above_limit")
+    after = {p: p.read_bytes() for p in exp.root.rglob("*") if p.is_file()}
+    new = set(after) - set(root_files)
+    assert new == {exp.rescores / "tight" / "report.md"}
+    assert all(after[p] == b for p, b in root_files.items())                       # report, record, events, manifest unchanged
+    text = (exp.rescores / "tight" / "report.md").read_text(encoding="utf-8")
+    assert "NON-DECISIONAL RESCORE `tight`" in text and loader.sha256_file(alt) in text
+    assert score_cmd(exp, "--rescore", "tight", "--rule", str(alt)) == 1           # never overwritten
+
+
+def test_rescore_needs_both_flags_and_a_plain_name(exp, tmp_path):
+    prepare(exp)
+    with pytest.raises(SystemExit):
+        score_cmd(exp, "--rescore", "x")
+    assert score_cmd(exp, "--rescore", "../x", "--rule", str(exp.rule)) == 1
+    assert not exp.rescores.exists() or not list(exp.rescores.rglob("*"))
+
+
+def test_the_report_text_for_the_real_paths_is_free_of_a_key_or_prompt_text(exp):
+    result, _ = run(perfect(), table_right=IDS[:3])
+    text = render_report(result)
+    assert not re.search(r"https?://", text) and "synthetic problem text" not in text


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
