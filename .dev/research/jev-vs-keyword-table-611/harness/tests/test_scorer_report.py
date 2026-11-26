import json
import re

import pytest
from harness import events, gate, loader, scorer
from harness.scorer import (
    build_run_meta,
    render_decision_record,
    render_report,
    score,
    verdict,
)

PIN = "jev-1.14.0"
IDS = [f"p{i}" for i in range(8)]                  # labels: bug build performance deployment security test ambiguous none-fit
LABELS = dict(zip(IDS, ["bug", "build", "performance", "deployment", "security", "test", "ambiguous", "none-fit"]))
CORPUS = [{"id": i, "label": LABELS[i], "seen_by_table": False} for i in IDS]
# stand-in values: none of these may appear in the committed rule file
RULE = {"alpha_inverse": 20, "median_limit_s": 1.5, "slowest_limit_s": 4.5, "attempt_timeout_s": 10.0, "median_population": "answered_only",
        "noul_low": 0.3, "noul_high": 0.7, "noul_low_operator": "le", "noul_high_operator": "ge",
        "unresolved_failure_invalid_count": 77}
META = {"frozen_changed": [], "gate1_event": True, "gate2_event": True, "table_provenance_present": True, "stop_reason": "completed",
        "live_runs": 1, "model_pin": PIN, "spent_usd": 0.0123}
PASSING = lambda cmd: (0, "12 passed in 0.1s")  # noqa: E731


def jrow(pid, choice=None, noul=None, lat=1.0, attempts=None, final="ok", model=PIN):
    """A Jev row.  By default Jev is right: the label's own type for a typed prompt, an unset answer (low Noul) otherwise."""
    typed = LABELS[pid] not in ("ambiguous", "none-fit")
    choice = choice or (LABELS[pid] if typed else "bug")
    noul = noul if noul is not None else (0.9 if typed else 0.1)
    atts = attempts or [{"status": "ok", "error": None, "latency_s": lat, "timed_out": False}]
    ok = final == "ok"
    return {"prompt_id": pid, "attempts": atts, "final_status": final, "choice": choice if ok else None,
            "probs": {choice: 0.8, "test": 0.2} if ok else None, "noul": noul if ok else None, "model": model if ok else None}


def table_rows(right_ids):
    """Table answers: right on ``right_ids``, wrong on every other prompt."""
    out = []
    for i in IDS:
        typed = LABELS[i] not in ("ambiguous", "none-fit")
        right = LABELS[i] if typed else None
        wrong = ("test" if LABELS[i] == "bug" else "bug")
        out.append({"prompt_id": i, "answer": right if i in right_ids else wrong})
    return out


def run(rows, table_right=(), rule=RULE, meta=META, corpus=CORPUS):
    result = score(corpus, table_rows(set(table_right)), rows, rule, meta)
    return result, verdict(result, rule, meta)


def perfect(**kw):
    return [jrow(i, **kw) for i in IDS]


# ---- each verdict state, with the boundaries on both sides (T-12)

def test_jev_beats_the_table_when_margin_and_latency_hold():
    result, v = run(perfect(), table_right=IDS[:3])
    assert result["margin"]["b"] == 5 and result["margin"]["c"] == 0 and v[0] == "JEV_BEATS_TABLE"


def test_margin_boundary_five_nil_passes_and_four_nil_fails():
    assert run(perfect(), table_right=IDS[:3])[1][0] == "JEV_BEATS_TABLE"
    state, reason = run(perfect(), table_right=IDS[:4])[1]
    assert (state, reason) == ("NOT_CLEARLY", "margin_not_passed")


@pytest.mark.parametrize("lat,state", [(1.5, "JEV_BEATS_TABLE"), (1.6, "NOT_CLEARLY")])
def test_median_limit_boundary(lat, state):
    result, v = run(perfect(lat=lat), table_right=IDS[:3])
    assert v[0] == state and (state == "JEV_BEATS_TABLE" or v[1] == "median_above_limit")


@pytest.mark.parametrize("slow,state", [(4.5, "JEV_BEATS_TABLE"), (4.6, "NOT_CLEARLY")])
def test_slowest_limit_boundary_counts_every_attempt(slow, state):
    rows = perfect()
    rows[0] = jrow("p0", attempts=[{"status": "refused", "error": "http_500", "latency_s": slow, "timed_out": False},
                                   {"status": "ok", "error": None, "latency_s": 1.0, "timed_out": False}])
    result, v = run(rows, table_right=IDS[:3])
    assert v[0] == state and (state == "JEV_BEATS_TABLE" or v[1] == "slowest_above_limit")


def test_a_timeout_counts_at_its_cap_in_the_slowest():
    rows = perfect()
    rows[0] = jrow("p0", attempts=[{"status": "refused", "error": "timeout", "latency_s": 3.0, "timed_out": True},
                                   {"status": "ok", "error": None, "latency_s": 1.0, "timed_out": False}])
    result, v = run(rows, table_right=IDS[:3])
    assert result["latency"]["slowest"] == 10.0 and v == ("NOT_CLEARLY", "slowest_above_limit")


def test_not_clearly_names_every_failed_test():
    rows = perfect(lat=5.0)
    assert run(rows, table_right=IDS[:4])[1] == ("NOT_CLEARLY", "margin_not_passed,median_above_limit,slowest_above_limit")


# ---- RUN_INVALID, each reason (T-13)

@pytest.mark.parametrize("change,reason", [
    ({"gate1_event": False}, "gate_result_missing"),
    ({"gate2_event": False}, "gate_result_missing"),
    ({"live_runs": 2}, "second_live_run"),
    ({"frozen_changed": ["table_answers"]}, "table_answers_changed"),
    ({"frozen_changed": ["corpus"]}, "frozen_file_changed"),
    ({"frozen_changed": ["code"]}, "frozen_file_changed"),
    ({"table_provenance_present": False}, "table_provenance_missing"),
    ({"stop_reason": "key_rejected"}, "key_rejected"),
    ({"stop_reason": "model_mismatch"}, "model_mismatch"),
    ({"stop_reason": "spend_bound"}, "stopped_before_all_prompts"),
    ({"stop_reason": "no_run_end"}, "stopped_before_all_prompts"),
])
def test_each_meta_reason_makes_the_run_invalid(change, reason):
    assert run(perfect(), table_right=IDS[:3], meta=dict(META, **change))[1] == ("RUN_INVALID", reason)


def test_a_returned_model_other_than_the_pin_is_a_model_mismatch():
    rows = perfect()
    rows[3] = jrow("p3", model="jev-9.9.9")
    assert run(rows, table_right=IDS[:3])[1] == ("RUN_INVALID", "model_mismatch")


def test_fewer_rows_than_prompts_is_stopped_before_all_prompts():
    assert run(perfect()[:6], table_right=IDS[:3])[1] == ("RUN_INVALID", "stopped_before_all_prompts")


def test_a_run_with_no_answered_prompt_is_invalid():
    rows = [jrow(i, final="error", attempts=[{"status": "refused", "error": "http_500", "latency_s": 1.0, "timed_out": False}] * 2)
            for i in IDS]
    assert run(rows)[1] == ("RUN_INVALID", "no_answered_prompts")


def test_unresolved_failures_at_the_limit_make_the_run_invalid():
    bad = {"status": "refused", "error": "http_500", "latency_s": 1.0, "timed_out": False}
    rows = perfect()
    rows[0] = jrow("p0", final="error", attempts=[bad, bad])
    assert run(rows, table_right=IDS[:3], rule=dict(RULE, unresolved_failure_invalid_count=2))[1][0] != "RUN_INVALID"
    rows[1] = jrow("p1", final="error", attempts=[bad, bad])
    assert run(rows, table_right=IDS[:3], rule=dict(RULE, unresolved_failure_invalid_count=2))[1] == (
        "RUN_INVALID", "unresolved_failures_above_limit")


def test_the_first_failed_check_wins_and_every_reason_is_reachable():
    meta = dict(META, gate2_event=False, live_runs=2, frozen_changed=["corpus"])
    assert run(perfect(), meta=meta)[1] == ("RUN_INVALID", "gate_result_missing")
    assert set(scorer.INVALID_REASONS) == {"frozen_file_changed", "table_answers_changed", "stopped_before_all_prompts", "key_rejected",
                                           "model_mismatch", "unresolved_failures_above_limit", "gate_result_missing",
                                           "table_provenance_missing", "second_live_run", "no_answered_prompts"}


# ---- the paired breakdown, the disagreement list, the split and a twice-failed prompt (T-11, T-06)

def hand_built():
    rows = [jrow("p0"), jrow("p1"), jrow("p2", choice="bug"), jrow("p3", choice="bug"), jrow("p4", choice="bug"),
            jrow("p5", choice="bug"), jrow("p6"), jrow("p7", choice="bug", noul=0.9)]
    table = [{"prompt_id": p, "answer": a} for p, a in zip(IDS, ["test", "build", "performance", "bug", "test", "bug", "bug", None])]
    return rows, table


def test_paired_breakdown_and_disagreements_match_a_hand_count():
    rows, table = hand_built()
    r = score(CORPUS, table, rows, RULE, META)
    assert (r["all"]["both"], r["all"]["only_jev"], r["all"]["only_table"], r["all"]["neither"]) == (1, 2, 2, 3)
    assert (r["all"]["jev_right"], r["all"]["table_right"]) == (3, 3)
    assert [d["id"] for d in r["disagreements"]] == ["p0", "p2", "p4", "p6", "p7"]
    d = {x["id"]: x for x in r["disagreements"]}
    assert d["p6"]["jev"] is None and d["p6"]["jev_reason"] == "none-fit" and d["p6"]["table"] == "bug" and d["p6"]["noul"] == 0.1
    assert d["p0"]["probs"] == {"bug": 0.8, "test": 0.2}


def test_typed_and_unset_label_split():
    rows, table = hand_built()
    r = score(CORPUS, table, rows, RULE, META)
    assert (r["typed"]["n"], r["typed"]["only_jev"], r["typed"]["only_table"]) == (6, 1, 1)
    assert (r["unset_labels"]["n"], r["unset_labels"]["only_jev"], r["unset_labels"]["only_table"]) == (2, 1, 1)
    assert r["abstentions"]["jev"] == {"none-fit": 1, "not-settled": 0} and r["abstentions"]["table"] == 1


def test_a_pass_resting_only_on_the_unset_label_prompts_is_flagged():
    corpus = [{"id": "t0", "label": "bug", "seen_by_table": False}] + [
        {"id": f"u{i}", "label": "none-fit", "seen_by_table": False} for i in range(7)]
    rows = [dict(jrow("p0"), prompt_id="t0")] + [dict(jrow("p7"), prompt_id=f"u{i}") for i in range(7)]
    table = [{"prompt_id": "t0", "answer": "bug"}] + [{"prompt_id": f"u{i}", "answer": "bug"} for i in range(7)]
    r = score(corpus, table, rows, RULE, META)
    assert r["margin"]["passes"] and r["margin"]["rests_on_unset_group"]
    corpus2 = [{"id": f"t{i}", "label": "bug", "seen_by_table": False} for i in range(6)]
    rows2 = [dict(jrow("p0"), prompt_id=f"t{i}") for i in range(6)]
    table2 = [{"prompt_id": f"t{i}", "answer": "test"} for i in range(6)]
    r2 = score(corpus2, table2, rows2, RULE, META)
    assert r2["margin"]["passes"] and not r2["margin"]["rests_on_unset_group"]


def test_accuracy_with_and_without_the_prompts_the_table_saw():
    corpus = [dict(c, seen_by_table=(c["id"] == "p0")) for c in CORPUS]
    rows, table = hand_built()
    r = score(corpus, table, rows, RULE, META)
    assert r["seen_by_table"]["marked"] == 1 and r["seen_by_table"]["unmarked"]["n"] == 7
    assert r["seen_by_table"]["unmarked"]["jev_right"] == 2       # p0 was Jev's right answer outside p0: p1 and p6


def test_a_twice_failed_prompt_is_not_right_and_stays_in_the_denominator():
    bad = {"status": "refused", "error": "http_500", "latency_s": 1.0, "timed_out": False}
    rows = perfect()
    rows[6] = jrow("p6", final="error", attempts=[bad, bad])         # ambiguous label: an unset answer would be right, an error is not
    r = score(CORPUS, table_rows(set()), rows, RULE, META)
    assert r["all"]["jev_right"] == 7 and r["all"]["n"] == 8 and r["errors"]["unresolved"] == 1 and r["attempts"] == 9
    assert [d["status"] for d in r["disagreements"] if d["id"] == "p6"] == ["error"]
    assert "| Jev | 7 of 8 | 7/8 (0.875) |" in render_report(r)


def test_a_rerun_that_answers_is_counted_as_recovered():
    rows = perfect()
    rows[0] = jrow("p0", attempts=[{"status": "refused", "error": "http_500", "latency_s": 1.0, "timed_out": False},
                                   {"status": "ok", "error": None, "latency_s": 1.2, "timed_out": False}])
    r = score(CORPUS, table_rows(set()), rows, RULE, META)
    assert r["errors"]["recovered_by_rerun"] == 1 and r["errors"]["unresolved"] == 0 and r["all"]["jev_right"] == 8


def test_an_unset_operator_is_refused_by_the_scorer():
    with pytest.raises(ValueError):
        score(CORPUS, table_rows(set()), perfect(), dict(RULE, noul_low_operator="UNSET"), META)


# ---- the report and the decision record

def test_render_report_is_deterministic_and_names_the_verdict():
    result, v = run(perfect(), table_right=IDS[:3])
    result["verdict"] = {"state": v[0], "reason": v[1]}
    text = render_report(result)
    assert render_report(result) == text and "Verdict: **JEV_BEATS_TABLE**" in text and "**PASS**" in text
    assert "90th percentile (nearest rank): 1.000 s" in text and "Spent: 0.0123 USD" in text


def test_the_decision_record_names_the_issues_the_rule_hash_and_the_612_statement_for_each_verdict(exp):
    sha = loader.sha256_file(exp.rule)
    result, _ = run(perfect(), table_right=IDS[:3])
    for pair in (("JEV_BEATS_TABLE", "ok"), ("NOT_CLEARLY", "margin_not_passed"), ("RUN_INVALID", "key_rejected")):
        text = render_decision_record(result, pair, exp)
        assert pair[0] in text and sha in text and "## Posted text and links" in text
        for n in ("611", "609", "612"):
            assert f"## Text to post on issue {n}" in text
        assert "build and close decision on issue 612 is made only from a valid run" in text
        assert ("stays undecided" in text) == (pair[0] == "RUN_INVALID")
        assert text.split("## Posted text and links")[1].strip().startswith("(The coordinator fills this in")


def test_no_stand_in_value_of_these_tests_is_in_the_committed_rule_file():
    text = loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8")
    for key in ("median_limit_s", "slowest_limit_s", "unresolved_failure_invalid_count"):
        assert f"{key}: {RULE[key]}" not in text


# ---- the command (a temporary root for every file)

@pytest.fixture
def exp(exp, monkeypatch):
    """The command line builds ``Paths`` from a root alone, so point its default jevlib folder at the fixture's stand-in."""
    monkeypatch.setattr(loader, "JEVLIB_DIR", exp.jevlib_dir)
    return exp


def prepare(exp, rows=None, table_right=(), run_id="r1"):
    """Freeze everything, pass both gates, then write a finished run: the state of a root just before ``score`` is run."""
    s = exp.rule.read_text(encoding="utf-8")
    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
    exp.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3"), encoding="utf-8")
    gate.freeze_corpus(exp)
    gate.freeze_table(exp)
    gate.freeze_rule(exp)
    events.append_event(exp, "price_confirmed", usd_per_mtok=0.042, source="test")
    gate.record_tests(exp, runner=PASSING)
    events.append_event(exp, "lead_go", rule_sha256=loader.sha256_file(exp.rule), words="go")
    assert gate.gate1(exp) == [] and gate.gate2(exp) == []
    events.append_event(exp, "first_request")
    d = exp.runs / run_id
    d.mkdir(parents=True)
    d.joinpath("jev-rows.jsonl").write_text("\n".join(json.dumps(r) for r in (rows or perfect())) + "\n", encoding="utf-8")
    events.append_event(exp, "run_end", run_id=run_id, reason="completed", spent_usd=0.01)


def score_cmd(exp, *extra, run_id="r1"):
    return scorer.main(["score", "--run-id", run_id, "--root", str(exp.root), *extra])


def test_score_writes_the_report_and_the_decision_record_and_the_two_events(exp, capsys):
    prepare(exp)
    assert score_cmd(exp) == 0
    assert capsys.readouterr().out.startswith("JEV_BEATS_TABLE")
    assert exp.report.is_file() and "Verdict: **JEV_BEATS_TABLE**" in exp.report.read_text(encoding="utf-8")
    rec = exp.decision_record.read_text(encoding="utf-8")
    assert loader.sha256_file(exp.rule) in rec
    log = {e["event"]: e for e in events.read_events(exp)}
    assert log["scoring"]["evidence"] == "report.md" and log["verdict"]["state"] == "JEV_BEATS_TABLE"
    assert log["verdict"]["rule_sha256"] == loader.sha256_file(exp.rule)


def test_a_second_score_run_refuses_to_overwrite_the_root_report(exp, capsys):
    prepare(exp)
    assert score_cmd(exp) == 0
    before = (exp.report.read_bytes(), exp.decision_record.read_bytes(), exp.events.read_bytes())
    capsys.readouterr()
    assert score_cmd(exp) == 1
    assert "never overwritten" in capsys.readouterr().err
    assert (exp.report.read_bytes(), exp.decision_record.read_bytes(), exp.events.read_bytes()) == before


def test_score_refuses_and_writes_no_verdict_while_a_rule_value_is_unset(exp, capsys):
    (exp.runs / "r1").mkdir(parents=True)
    (exp.runs / "r1" / "jev-rows.jsonl").write_text(json.dumps(jrow("p0")) + "\n")
    assert score_cmd(exp) == 1
    assert "UNSET" in capsys.readouterr().err
    assert not exp.report.exists() and not exp.decision_record.exists() and events.latest(exp, "verdict") is None


def test_a_run_that_cannot_be_scored_is_refused_without_a_report(exp, capsys):
    prepare(exp)
    assert score_cmd(exp, run_id="nope") == 1
    assert "jev rows missing" in capsys.readouterr().err
    assert score_cmd(exp, run_id="../x") == 1
    assert not exp.report.exists()


def test_a_changed_table_answers_file_gives_a_report_with_run_invalid(exp, capsys):
    prepare(exp)
    exp.table_answers.write_text(exp.table_answers.read_text() + "\n")
    assert score_cmd(exp) == 0
    assert capsys.readouterr().out.strip() == "RUN_INVALID: table_answers_changed"
    assert "stays undecided" in exp.decision_record.read_text(encoding="utf-8")
    assert events.latest(exp, "verdict")["state"] == "RUN_INVALID"


def test_run_meta_reads_the_events_and_the_manifest(exp):
    prepare(exp)
    m = build_run_meta(exp, "r1")
    assert m["frozen_changed"] == [] and m["gate1_event"] and m["gate2_event"] and m["table_provenance_present"]
    assert (m["stop_reason"], m["live_runs"], m["model_pin"], m["spent_usd"]) == ("completed", 1, PIN, 0.01)
    assert build_run_meta(exp, "other")["stop_reason"] == "no_run_end"
    exp.questions_py.write_text("# changed\n")
    assert set(build_run_meta(exp, "r1")["frozen_changed"]) == {"questions", "code"}


def test_a_rescore_writes_only_under_rescores_and_changes_nothing_else(exp, tmp_path, capsys):
    prepare(exp)
    assert score_cmd(exp) == 0
    alt = tmp_path / "alt-rule.md"
    alt.write_text(exp.rule.read_text(encoding="utf-8").replace("slowest_limit_s: 5", "slowest_limit_s: 0.5"), encoding="utf-8")
    root_files = {p: p.read_bytes() for p in exp.root.rglob("*") if p.is_file()}
    capsys.readouterr()
    assert score_cmd(exp, "--rescore", "tight", "--rule", str(alt)) == 0
    assert capsys.readouterr().out.startswith("NOT_CLEARLY: slowest_above_limit")
    after = {p: p.read_bytes() for p in exp.root.rglob("*") if p.is_file()}
    new = set(after) - set(root_files)
    assert new == {exp.rescores / "tight" / "report.md"}
    assert all(after[p] == b for p, b in root_files.items())                       # report, record, events, manifest unchanged
    text = (exp.rescores / "tight" / "report.md").read_text(encoding="utf-8")
    assert "NON-DECISIONAL RESCORE `tight`" in text and loader.sha256_file(alt) in text
    assert score_cmd(exp, "--rescore", "tight", "--rule", str(alt)) == 1           # never overwritten


def test_rescore_needs_both_flags_and_a_plain_name(exp, tmp_path):
    prepare(exp)
    with pytest.raises(SystemExit):
        score_cmd(exp, "--rescore", "x")
    assert score_cmd(exp, "--rescore", "../x", "--rule", str(exp.rule)) == 1
    assert not exp.rescores.exists() or not list(exp.rescores.rglob("*"))


def test_the_report_text_for_the_real_paths_is_free_of_a_key_or_prompt_text(exp):
    result, _ = run(perfect(), table_right=IDS[:3])
    text = render_report(result)
    assert not re.search(r"https?://", text) and "synthetic problem text" not in text
