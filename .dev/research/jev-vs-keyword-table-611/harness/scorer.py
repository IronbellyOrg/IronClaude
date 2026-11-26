"""Scorer: the pure functions of the decision rule, then the scoring pipeline, the verdict, the report and the command line.

Part 1 (``right`` to ``latency_stats``) is pure: nothing in it reads a file or the environment; every policy value comes in
through the ``rule`` argument that ``loader.load_rule`` returns.  Part 2 (``score``, ``verdict``, ``render_report``,
``render_decision_record``) is pure too.  Only ``build_run_meta`` and ``main`` read or write files.

Command line:
  scorer.py score --run-id ID [--root PATH]                      score a run: write report.md and decision-record.md at the root
  scorer.py score --run-id ID --rescore NAME --rule PATH [--root PATH]   non-decisional rescore under another rule file

``jev-rows.jsonl`` holds one row per prompt: ``prompt_id``, ``attempts`` (each ``status``, ``error``, ``latency_s``, ``timed_out``),
``final_status`` (``ok`` or ``error``), ``choice`` and ``probs`` (the answer to ``problem_type``), ``noul`` (the value of
``any_type_fits``) and ``model``.  ``run_meta`` keys: ``frozen_changed`` (names of frozen files that no longer match the manifest),
``gate1_event`` and ``gate2_event`` (a passing event exists), ``table_provenance_present``, ``stop_reason`` (``completed`` or the
systemic reason of the ``run_end`` event), ``live_runs`` (count of ``first_request`` events), ``model_pin`` and ``spent_usd``.
"""
import argparse
import json
import math
import pathlib
import sys

_EXP = pathlib.Path(__file__).resolve().parents[1]
_JEV = _EXP.parent / "346-review-loop-experiments" / "p15" / "jev"
for _p in (str(_EXP), str(_JEV)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from harness import events, gate, loader  # noqa: E402

TYPED = ("bug", "build", "performance", "deployment", "security", "test")
UNSET_LABELS = ("ambiguous", "none-fit")


def right(label, answer):
    """A typed label is right when the answer is that type; an ``ambiguous`` or ``none-fit`` label is right when the answer is
    unset (``None``).  The same rule serves both arms.  An unset answer on a typed label is not right."""
    if label in UNSET_LABELS:
        return answer is None
    if label in TYPED:
        return answer == label
    raise ValueError(f"unknown label {label!r}")


def sign_test_passes(b, c, alpha_inverse=20):
    """Exact one-sided sign test in integer arithmetic.  b = prompts only Jev gets right, c = prompts only the table gets right.
    Jev clearly beats the table when ``alpha_inverse * tail < 2 ** n``, where n = b + c and tail = the count of outcomes with at
    least b successes out of n fair coin tosses.  With b + c = 0 there is nothing to test: not clearly."""
    n = b + c
    if n == 0:
        return False
    tail = sum(math.comb(n, k) for k in range(b, n + 1))
    return alpha_inverse * tail < 2 ** n


def jev_answer(noul_p, choice, rule):
    """Map Jev's two answers to one answer or an unset answer.

    ``noul_p`` is the Noul value of ``any_type_fits`` (high means a type fits); ``choice`` is the validated answer of
    ``problem_type``.  Below the low edge (``lt``: strictly below ``noul_low``; ``le``: at or below) the answer is unset with
    reason ``none-fit``.  Above the high edge (``gt``: strictly above ``noul_high``; ``ge``: at or above) the answer is the
    choice.  In between it is unset with reason ``not-settled``.  Returns ``(answer, reason)``; the reason is ``None`` when the
    answer is the choice.  Refuses an operator that is ``UNSET`` or not valid for its edge."""
    low_op, high_op = rule["noul_low_operator"], rule["noul_high_operator"]
    if low_op not in ("lt", "le"):
        raise ValueError(f"noul_low_operator must be lt or le, not {low_op!r}")
    if high_op not in ("gt", "ge"):
        raise ValueError(f"noul_high_operator must be gt or ge, not {high_op!r}")
    low, high = rule["noul_low"], rule["noul_high"]
    if (noul_p < low) if low_op == "lt" else (noul_p <= low):
        return None, "none-fit"
    if (noul_p > high) if high_op == "gt" else (noul_p >= high):
        return choice, None
    return None, "not-settled"


def median(values):
    """The median; an even count gives the mean of the two middle values; an empty list gives ``None``."""
    v = sorted(values)
    if not v:
        return None
    mid = len(v) // 2
    return v[mid] if len(v) % 2 else (v[mid - 1] + v[mid]) / 2


def percentile_nearest_rank(values, q):
    """Nearest-rank percentile: ``sorted[ceil(q * n) - 1]``; an empty list gives ``None``."""
    v = sorted(values)
    if not v:
        return None
    return v[min(max(math.ceil(round(q * len(v), 9)) - 1, 0), len(v) - 1)]


def latency_stats(attempts, rule):
    """Latency statistics over the attempts of a run.

    Each attempt is a dict with ``prompt_id``, ``latency_s``, ``timed_out`` and ``answered`` (the response was a valid answer).
    The slowest is taken over all attempts, a timeout counted at ``attempt_timeout_s``.  The median and the 90th percentile are
    taken over one value per prompt, by ``median_population``: ``answered_only`` uses each prompt's last answered attempt;
    ``include_timeouts_at_cap`` uses each prompt's last attempt that answered or timed out, a timeout at ``attempt_timeout_s``.
    Every statistic is ``None`` when no value qualifies."""
    cap = rule["attempt_timeout_s"]

    def value(a):
        return cap if a["timed_out"] else a["latency_s"]

    mode = rule["median_population"]
    if mode not in ("answered_only", "include_timeouts_at_cap"):
        raise ValueError(f"unknown median_population {mode!r}")
    last = {}
    for a in attempts:
        if a["answered"] or (mode == "include_timeouts_at_cap" and a["timed_out"]):
            last[a["prompt_id"]] = value(a)
    pop = list(last.values())
    slowest = [value(a) for a in attempts]
    return {"median": median(pop), "slowest": max(slowest) if slowest else None,
            "p90": percentile_nearest_rank(pop, 0.9), "n": len(pop)}


# ---------------------------------------------------------------- part 2: the scoring pipeline, verdict and report

STATES = ("JEV_BEATS_TABLE", "NOT_CLEARLY", "RUN_INVALID")
INVALID_REASONS = ("gate_result_missing", "second_live_run", "table_answers_changed", "frozen_file_changed",
                   "table_provenance_missing", "key_rejected", "model_mismatch", "stopped_before_all_prompts",
                   "no_answered_prompts", "unresolved_failures_above_limit")


class ScoreRefused(Exception):
    """The scoring command refused: nothing was written."""


def _tally(items):
    both = sum(1 for i in items if i["jev_right"] and i["table_right"])
    only_jev = sum(1 for i in items if i["jev_right"] and not i["table_right"])
    only_table = sum(1 for i in items if i["table_right"] and not i["jev_right"])
    return {"n": len(items), "jev_right": both + only_jev, "table_right": both + only_table, "both": both,
            "only_jev": only_jev, "only_table": only_table, "neither": len(items) - both - only_jev - only_table}


def _table_answer(table_by_id, pid):
    if pid not in table_by_id:
        raise ValueError(f"no table answer for prompt {pid}")
    answer = table_by_id[pid].get("answer")
    if answer is not None and answer not in TYPED:
        raise ValueError(f"table answer for prompt {pid} is not a type or null")
    return answer


def score(corpus, table_answers, jev_rows, rule, run_meta):
    """Score one run.  An error or a missing row counts as not right and stays in the denominator.  Returns a plain dict."""
    table = {r["prompt_id"]: r for r in table_answers}
    rows = {r["prompt_id"]: r for r in jev_rows}
    per, attempts, models = [], [], set()
    for c in corpus:
        pid, label = c["id"], c["label"]
        t_ans = _table_answer(table, pid)
        row = rows.get(pid)
        probs = noul = None
        if row is not None and row["final_status"] == "ok":
            j_ans, j_reason = jev_answer(row["noul"], row["choice"], rule)
            status, probs, noul = "ok", row.get("probs"), row["noul"]
            models.add(row.get("model"))
        else:
            j_ans, j_reason = None, ("error" if row is not None else "missing")
            status = j_reason
        for a in (row or {}).get("attempts", []):
            attempts.append({"prompt_id": pid, "latency_s": a.get("latency_s") or 0.0, "timed_out": bool(a.get("timed_out")),
                             "answered": a.get("status") == "ok"})
        per.append({"id": pid, "label": label, "group": "unset" if label in UNSET_LABELS else "typed", "status": status,
                    "jev": j_ans, "jev_reason": j_reason, "table": t_ans, "jev_right": status == "ok" and right(label, j_ans),
                    "table_right": right(label, t_ans), "seen_by_table": bool(c.get("seen_by_table")), "probs": probs,
                    "noul": noul, "n_attempts": len((row or {}).get("attempts", []))})
    allt = _tally(per)
    typed = _tally([p for p in per if p["group"] == "typed"])
    unset = _tally([p for p in per if p["group"] == "unset"])
    alpha = rule["alpha_inverse"]
    passes = sign_test_passes(allt["only_jev"], allt["only_table"], alpha)
    answered = [p for p in per if p["status"] == "ok"]
    return {
        "n_prompts": len(per), "n_rows": sum(1 for c in corpus if c["id"] in rows), "answered": len(answered),
        "all": allt, "typed": typed, "unset_labels": unset,
        "seen_by_table": {"marked": sum(1 for p in per if p["seen_by_table"]), "unmarked": _tally([p for p in per if not p["seen_by_table"]])},
        "margin": {"b": allt["only_jev"], "c": allt["only_table"], "alpha_inverse": alpha, "passes": passes,
                   "rests_on_unset_group": passes and not sign_test_passes(typed["only_jev"], typed["only_table"], alpha)},
        "abstentions": {"jev": {r: sum(1 for p in answered if p["jev_reason"] == r) for r in ("none-fit", "not-settled")},
                        "table": sum(1 for p in per if p["table"] is None)},
        "errors": {"unresolved": sum(1 for p in per if p["status"] == "error"), "missing": sum(1 for p in per if p["status"] == "missing"),
                   "recovered_by_rerun": sum(1 for p in answered if p["n_attempts"] > 1)},
        "latency": latency_stats(attempts, rule), "attempts": len(attempts), "models": sorted(m for m in models if m),
        "cost": {"spent_usd": run_meta.get("spent_usd")},
        "disagreements": [{k: p[k] for k in ("id", "label", "jev", "jev_reason", "table", "status", "probs", "noul")}
                          for p in per if p["jev"] != p["table"]],
    }


def verdict(result, rule, run_meta):
    """``(state, reason)``.  ``RUN_INVALID`` reasons are checked in the order of ``INVALID_REASONS``; a valid run is
    ``JEV_BEATS_TABLE`` only when the margin test passes and both latency limits hold.  ``unresolved_failure_invalid_count`` is the
    count of unresolved failures that makes a run invalid, so a run with that many or more is invalid."""
    rm = run_meta
    if not (rm.get("gate1_event") and rm.get("gate2_event")):
        return "RUN_INVALID", "gate_result_missing"
    if rm.get("live_runs", 0) > 1:
        return "RUN_INVALID", "second_live_run"
    changed = list(rm.get("frozen_changed", []))
    if "table_answers" in changed:
        return "RUN_INVALID", "table_answers_changed"
    if changed:
        return "RUN_INVALID", "frozen_file_changed"
    if not rm.get("table_provenance_present"):
        return "RUN_INVALID", "table_provenance_missing"
    stop, pin = rm.get("stop_reason"), rm.get("model_pin")
    if stop == "key_rejected":
        return "RUN_INVALID", "key_rejected"
    if stop == "model_mismatch" or (pin and any(m != pin for m in result["models"])):
        return "RUN_INVALID", "model_mismatch"
    if stop != "completed" or result["n_rows"] < result["n_prompts"]:
        return "RUN_INVALID", "stopped_before_all_prompts"
    if result["answered"] == 0:
        return "RUN_INVALID", "no_answered_prompts"
    if result["errors"]["unresolved"] >= rule["unresolved_failure_invalid_count"]:
        return "RUN_INVALID", "unresolved_failures_above_limit"
    lat, fails = result["latency"], []
    if not result["margin"]["passes"]:
        fails.append("margin_not_passed")
    if lat["median"] is None or lat["median"] > rule["median_limit_s"]:
        fails.append("median_above_limit")
    if lat["slowest"] is None or lat["slowest"] > rule["slowest_limit_s"]:
        fails.append("slowest_above_limit")
    if fails:
        return "NOT_CLEARLY", ",".join(fails)
    return "JEV_BEATS_TABLE", "margin_test_passed_and_both_latency_limits_hold"


def _f(x, digits=3):
    return "n/a" if x is None else f"{x:.{digits}f}"


def _ratio(k, n):
    return f"{k}/{n} ({_f(k / n if n else None)})"


def _probs(p):
    if p is None:
        return ""
    return ";".join(f"{k}={_f(v)}" for k, v in sorted(p.items())) if isinstance(p, dict) else json.dumps(p, sort_keys=True)


def render_report(result):
    """The report as markdown.  Deterministic: the same result gives the same bytes (no time, no path, sorted keys)."""
    a, t, u, m, lat = result["all"], result["typed"], result["unset_labels"], result["margin"], result["latency"]
    v = result.get("verdict")
    out = ["# Jev versus the keyword table: report", ""]
    if result.get("rescore"):
        out += [f"**NON-DECISIONAL RESCORE `{result['rescore']['name']}` under rule file {result['rescore']['rule_sha256']}.** "
                "The root report and decision record are not changed by it.", ""]
    if v:
        out += [f"Verdict: **{v['state']}** ({v['reason']})", ""]
    out += ["## Accuracy over every frozen prompt", "", "| Arm | Right | Accuracy |", "|---|---|---|",
            f"| Jev | {a['jev_right']} of {a['n']} | {_ratio(a['jev_right'], a['n'])} |",
            f"| Table | {a['table_right']} of {a['n']} | {_ratio(a['table_right'], a['n'])} |", "",
            "## Paired breakdown", "", "| Both right | Only Jev (b) | Only table (c) | Neither |", "|---|---|---|---|",
            f"| {a['both']} | {a['only_jev']} | {a['only_table']} | {a['neither']} |", "",
            "## Margin test (exact one-sided sign test, integer arithmetic)", "",
            f"b = {m['b']}, c = {m['c']}, significance 1 in {m['alpha_inverse']}: **{'PASS' if m['passes'] else 'FAIL'}**"]
    if m["rests_on_unset_group"]:
        out += ["", "FLAG: the pass rests only on the `ambiguous` and `none-fit` prompts; the typed prompts alone do not pass."]
    out += ["", "## Typed prompts versus `ambiguous` and `none-fit` prompts", "",
            "| Group | Prompts | Jev right | Table right | Only Jev | Only table |", "|---|---|---|---|---|---|"]
    for name, g in (("typed", t), ("ambiguous or none-fit", u)):
        out.append(f"| {name} | {g['n']} | {_ratio(g['jev_right'], g['n'])} | {_ratio(g['table_right'], g['n'])} | "
                   f"{g['only_jev']} | {g['only_table']} |")
    un = result["seen_by_table"]["unmarked"]
    out += ["", "## Prompts marked `seen_by_table`", "", f"{result['seen_by_table']['marked']} prompts are marked. Without them:",
            f"Jev {_ratio(un['jev_right'], un['n'])}, table {_ratio(un['table_right'], un['n'])}, only Jev {un['only_jev']}, "
            f"only table {un['only_table']}.", "", "## Abstentions and errors", "",
            f"- Jev none-fit: {result['abstentions']['jev']['none-fit']}; Jev not-settled: {result['abstentions']['jev']['not-settled']}",
            f"- Table unset: {result['abstentions']['table']}",
            f"- Unresolved failures (error, not right): {result['errors']['unresolved']}; no row: {result['errors']['missing']}; "
            f"recovered by the one rerun: {result['errors']['recovered_by_rerun']}", "", "## Latency (client side)", "",
            f"- Median over each prompt's final answered attempt: {_f(lat['median'])} s",
            f"- Slowest over all attempts (a timeout counts at its cap): {_f(lat['slowest'])} s",
            f"- 90th percentile (nearest rank): {_f(lat['p90'])} s",
            f"- Prompts in the median: {lat['n']}; attempts: {result['attempts']}", "", "## Cost", "",
            f"- Spent: {_f(result['cost']['spent_usd'], 4)} USD", f"- Models returned: {', '.join(result['models']) or 'none'}", "",
            "## Disagreements (Jev answer differs from the table answer)", ""]
    if result["disagreements"]:
        out += ["| Prompt | Label | Jev | Jev reason | Table | Status | Jev probabilities | Noul |", "|---|---|---|---|---|---|---|---|"]
        for d in result["disagreements"]:
            out.append(f"| {d['id']} | {d['label']} | {d['jev'] or 'unset'} | {d['jev_reason'] or ''} | {d['table'] or 'unset'} | "
                       f"{d['status']} | {_probs(d['probs'])} | {_f(d['noul'])} |")
    else:
        out.append("None.")
    return "\n".join(out) + "\n"


def _rel(path):
    try:
        return pathlib.Path(path).resolve().relative_to(gate.REPO).as_posix()
    except ValueError:
        return str(path)


def render_decision_record(result, verdict_pair, paths):
    """The decision record: the verdict, the rule file's hash, the report path, the exact text to post on issues 611, 609 and 612,
    and an empty section for the coordinator to fill in once the text is posted."""
    state, reason = verdict_pair
    a, lat = result["all"], result["latency"]
    facts = (f"Jev right on {a['jev_right']} of {a['n']} prompts, table right on {a['table_right']} of {a['n']}; only Jev {a['only_jev']}, "
             f"only table {a['only_table']}; margin test {'passed' if result['margin']['passes'] else 'not passed'}; "
             f"median {_f(lat['median'])} s, slowest {_f(lat['slowest'])} s.")
    report = _rel(paths.report)
    if state == "RUN_INVALID":
        head = f"The comparison run is INVALID ({reason})."
        t611 = f"{head} No result is claimed. The harness, run record and report are in `{report}` and `{_rel(paths.decision_record)}`."
        t609 = f"Step 2 (Jev against the keyword table) produced no valid result: {reason}. The preflight is not decided by it."
        t612 = ("The run was invalid, so issue 612 stays undecided. The build and close decision on issue 612 is made only from a "
                "valid run.")
    else:
        head = f"Result: {state} ({reason})."
        t611 = f"{head} {facts} Full report: `{report}`."
        t609 = f"Step 2 (Jev against the keyword table) is done: {state}. {facts}"
        t612 = (f"A valid run says {state}. {facts} The build and close decision on issue 612 is made only from a valid run, and "
                "this is one.")
    return "\n".join([
        "# Decision record: Jev versus the keyword table (issue 611)", "", f"Verdict: **{state}**", f"Reason: {reason}",
        f"Rule file hash (SHA-256): {loader.sha256_file(paths.rule)}", f"Report: `{report}`", "",
        "The build and close decision on issue 612 is made only from a valid run.",
        *(["Issue 612 stays undecided: this run is invalid."] if state == "RUN_INVALID" else []), "",
        "## Text to post on issue 611", "", t611, "", "## Text to post on issue 609", "", t609, "", "## Text to post on issue 612", "", t612,
        "", "## Posted text and links", "", "(The coordinator fills this in after posting: where each text went, with its link.)", ""])


def build_run_meta(paths, run_id):
    """The facts about a run that the scorer cannot read from its rows: what still matches the manifest, which gate and run events
    exist, and how the run ended.  Built from the manifest, the events file and the files themselves."""
    m = gate.read_manifest(paths)
    changed = []
    frozen = dict(gate.CORPUS_SIDE, rule="rule", table_answers="table_answers", table_provenance="table_provenance")
    for key, attr in frozen.items():
        p = getattr(paths, attr)
        if key == "table_provenance" and not p.is_file():
            continue
        if key not in m or not p.is_file() or loader.sha256_file(p) != m[key]:
            changed.append(key)
    log = events.read_events(paths)
    # The code the tests passed on is the record made before the run's first request; a record-tests run after the run began
    # (an edit followed by new tests) never replaces it.
    first = next((i for i, e in enumerate(log) if e["event"] == "first_request"), len(log))
    tests = next((e for e in reversed(log[:first]) if e["event"] == "tests_passed"), None)
    if tests is None or tests.get("code_hashes") != gate._code_hashes(paths):
        changed.append("code")
    ends = [e for e in log if e["event"] == "run_end" and e.get("run_id") == run_id]
    return {"frozen_changed": changed,
            "gate1_event": any(e["event"] == "gate1" and e.get("passed") for e in log),
            "gate2_event": any(e["event"] == "gate2" and e.get("passed") for e in log),
            "table_provenance_present": paths.table_provenance.is_file(),
            "stop_reason": ends[-1].get("reason") if ends else "no_run_end",
            "live_runs": sum(1 for e in log if e["event"] == "first_request"),
            "model_pin": m.get("model_pin"), "spent_usd": ends[-1].get("spent_usd") if ends else None}


def _write_new(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "x", encoding="utf-8") as f:
            f.write(text)
    except FileExistsError:
        raise ScoreRefused(f"{path.name} already exists and is never overwritten") from None


def _score_command(paths, args):
    for label, value in (("run id", args.run_id), ("rescore name", args.rescore)):
        if value is not None and not loader.is_plain_name(value):
            raise ScoreRefused(f"the {label} may hold only letters, digits, dot, underscore and hyphen")
    loader.require_own_root(paths)
    if args.rescore:
        rule = loader.load_rule(args.rule, for_scoring=True)
        out = paths.rescores / args.rescore / "report.md"
        if out.exists():
            raise ScoreRefused(f"{out.name} already exists and is never overwritten")
    else:
        rule = loader.load_rule(paths.rule, for_scoring=True)
        if paths.report.exists() or paths.decision_record.exists():
            raise ScoreRefused("report.md or decision-record.md already exists and is never overwritten")
    corpus = loader.load_corpus(paths.corpus)
    table = loader.load_table_answers(paths.table_answers)
    rows = loader._jsonl(paths.runs / args.run_id / "jev-rows.jsonl", "jev rows")
    meta = build_run_meta(paths, args.run_id)
    if args.rescore:
        meta["frozen_changed"] = [k for k in meta["frozen_changed"] if k != "rule"]
    result = score(corpus, table, rows, rule, meta)
    state, reason = verdict(result, rule, meta)
    result["verdict"] = {"state": state, "reason": reason}
    if args.rescore:
        result["rescore"] = {"name": args.rescore, "rule_sha256": loader.sha256_file(args.rule)}
        _write_new(out, render_report(result))
        return state, reason
    _write_new(paths.report, render_report(result))
    _write_new(paths.decision_record, render_decision_record(result, (state, reason), paths))
    rule_sha = loader.sha256_file(paths.rule)
    events.append_event(paths, "scoring", evidence=paths.report, run_id=args.run_id, prompts=result["n_prompts"])
    events.append_event(paths, "verdict", evidence=paths.decision_record, run_id=args.run_id, state=state, reason=reason,
                        rule_sha256=rule_sha)
    return state, reason


def main(argv=None):
    ap = argparse.ArgumentParser(prog="scorer.py", description="score a finished run against the frozen decision rule")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score", help="write report.md and decision-record.md for a run, or a non-decisional rescore")
    s.add_argument("--run-id", required=True)
    s.add_argument("--root", default=None)
    s.add_argument("--rescore", default=None, help="NAME of a non-decisional rescore under another rule file")
    s.add_argument("--rule", default=None, help="the other rule file, with --rescore")
    args = ap.parse_args(argv)
    if bool(args.rescore) != bool(args.rule):
        ap.error("--rescore and --rule go together")
    try:
        state, reason = _score_command(loader.Paths(args.root), args)
    except (ScoreRefused, ValueError) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    print(f"{state}: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
