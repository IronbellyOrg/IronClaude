import json
import math
import re

import pytest
import questions
from harness import events, gate, loader, spend
from harness.gate import GateError
from jevlib.config import RESERVE_BYTES_PER_TOKEN
from jevlib.questions import build_request, canonical_bytes

PASSING = lambda cmd: (0, "12 passed in 0.1s")  # noqa: E731


def fill_rule(p, low="le", high="ge", count=3):
    s = p.rule.read_text(encoding="utf-8")
    s = s.replace("noul_low_operator: UNSET", f"noul_low_operator: {low}").replace("noul_high_operator: UNSET", f"noul_high_operator: {high}")
    p.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", f"unresolved_failure_invalid_count: {count}"), encoding="utf-8")


def ready(p, skip=(), price=0.042):
    """Every step the live run rests on, in order; ``skip`` leaves named steps out."""
    fill_rule(p)
    gate.freeze_corpus(p)
    if "table" not in skip:
        gate.freeze_table(p)
    if "rule" not in skip:
        gate.freeze_rule(p)
    if "price" not in skip:
        events.append_event(p, "price_confirmed", usd_per_mtok=price, source="test")
    if "tests" not in skip:
        gate.record_tests(p, runner=PASSING)
    if "go" not in skip:
        events.append_event(p, "lead_go", evidence=p.rule, rule_sha256=loader.sha256_file(p.rule), words="go")


def append_text(path, text="# edited\n"):
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def run_estimate(p):
    qs = questions.build_questions()
    rows = [json.loads(line) for line in p.corpus.read_text().splitlines() if line.strip()]
    reqs = [build_request({"prompt": r["text"]}, qs) for r in rows]
    return spend.estimate_run_tokens(reqs), max(spend.estimate_request_tokens(r) for r in reqs)


# ---- Gate 1 (T-01, T-02)

def test_gate1_passes_after_the_corpus_is_frozen_and_accepts_unset_values(exp):
    gate.freeze_corpus(exp)
    assert "UNSET" in exp.rule.read_text(encoding="utf-8")
    assert gate.gate1(exp) == []


def test_gate1_refuses_before_anything_is_frozen(exp):
    assert gate.gate1(exp) == ["manifest_missing"]


@pytest.mark.parametrize("edit,name", [
    (lambda s: s.replace("status: AGREED", "status: PROPOSED"), "rule_status"),
    (lambda s: s.replace("status: AGREED", "status: PENDING"), "rule_status"),
    (lambda s: s.replace("agreed_by: the IronFlow session and the build agent", "agreed_by:"), "rule_provenance_empty"),
    (lambda s: s.replace("agreed_at: 2026-11-26", "agreed_at:"), "rule_provenance_empty"),
    (lambda s: s.replace("relayed_owner_words: you and the agent debate whats correct way to handle this and do it",
                         "relayed_owner_words:"), "rule_provenance_empty"),
    (lambda s: s.replace("I agree with all five", "").split("## Agreement text (verbatim)")[0]
     + "## Agreement text (verbatim)\n\n## Rule in words\n", "rule_provenance_empty"),
])
def test_gate1_refuses_each_rule_file_defect(exp, edit, name):
    gate.freeze_corpus(exp)
    exp.rule.write_text(edit(exp.rule.read_text(encoding="utf-8")), encoding="utf-8")
    assert gate.gate1(exp) == [name]


def test_gate1_refuses_a_missing_rule_file(exp):
    gate.freeze_corpus(exp)
    exp.rule.unlink()
    assert gate.gate1(exp) == ["rule_missing"]


@pytest.mark.parametrize("attr,name", [("corpus", "hash_corpus"), ("selection_criteria", "hash_selection_criteria"),
                                       ("labelling_record", "hash_labelling_record"), ("questions_py", "hash_questions")])
def test_either_gate_refuses_a_changed_corpus_side_file(exp, attr, name):
    ready(exp)
    append_text(getattr(exp, attr), "\n")
    assert name in gate.gate1(exp)
    assert name in gate.gate2(exp)


# ---- Gate 2 (T-02, T-03, second-run refusal)

def test_gate2_passes_on_a_complete_synthetic_setup(exp):
    ready(exp)
    assert gate.gate2(exp) == []


@pytest.mark.parametrize("skip,name", [("go", "go_missing"), ("tests", "tests_not_recorded"), ("rule", "rule_not_frozen"),
                                       ("price", "price_not_confirmed"), ("table", "hash_table_answers")])
def test_gate2_refuses_a_missing_step(exp, skip, name):
    ready(exp, skip=(skip,))
    assert name in gate.gate2(exp)


def test_gate2_refuses_a_go_that_names_an_old_rule_hash(exp):
    ready(exp)
    events.append_event(exp, "lead_go", rule_sha256="0" * 64, words="old")
    assert gate.gate2(exp) == ["go_rule_hash"]


def test_gate2_refuses_an_unset_value(exp):
    ready(exp)
    exp.rule.write_text(exp.rule.read_text(encoding="utf-8").replace("noul_low_operator: le", "noul_low_operator: UNSET"), encoding="utf-8")
    assert "unset_value" in gate.gate2(exp)


def test_gate2_refuses_a_changed_rule_table_answers_provenance_code_or_jevlib_file(exp):
    ready(exp)
    for target, name in ((exp.rule, "hash_rule"), (exp.table_answers, "hash_table_answers"),
                         (exp.table_provenance, "hash_table_provenance"), (exp.root / "harness" / "scorer.py", "hash_code"),
                         (exp.root / "harness" / "runner.py", "hash_code"), (exp.jevlib_dir / "a.py", "hash_code")):
        original = target.read_bytes()
        append_text(target, "\n")
        assert name in gate.gate2(exp), name
        target.write_bytes(original)
    assert gate.gate2(exp) == []


@pytest.mark.parametrize("event", ["first_request", "run_end"])
def test_gate2_refuses_when_a_run_already_started_or_ended(exp, event):
    ready(exp)
    events.append_event(exp, event)
    assert gate.gate2(exp) == ["prior_run"]


def test_spend_bound_fails_when_each_request_fits_but_the_whole_run_does_not(exp):
    ready(exp)
    total, biggest = run_estimate(exp)
    cap = spend.ceiling_tokens(1.0, 0.042)
    left = total - 10
    assert left > biggest
    exp.ledger.parent.mkdir()
    exp.ledger.write_text(json.dumps({"ceiling_input_tokens": cap, "spent_tokens": cap - left, "draws": {}, "reserved": {}}))
    assert gate.gate2(exp) == ["spend_bound"]
    exp.ledger.write_text(json.dumps({"ceiling_input_tokens": cap, "spent_tokens": cap - total - 1, "draws": {}, "reserved": {}}))
    assert gate.gate2(exp) == []


def test_spend_bound_fails_when_the_worst_case_at_a_high_price_is_above_the_cap(exp):
    ready(exp, price=1000.0)
    assert gate.gate2(exp) == ["spend_bound"]


def test_gates_hash_files_only_and_never_call_the_corpus_loader(exp, monkeypatch):
    ready(exp)

    def boom(*a, **k):
        raise AssertionError("the corpus loader was called")
    monkeypatch.setattr(loader, "load_corpus", boom)
    assert gate.gate1(exp) == []
    assert gate.gate2(exp) == []


# ---- freezes and the manifest (write-once, gates only read)

def test_the_manifest_is_unchanged_by_either_gate(exp):
    ready(exp)
    before = exp.manifest.read_bytes()
    gate.gate1(exp)
    gate.gate2(exp)
    assert exp.manifest.read_bytes() == before


def test_a_second_freeze_of_each_kind_is_refused_and_keeps_the_frozen_value(exp):
    ready(exp)
    before = exp.manifest.read_bytes()
    for freeze in (gate.freeze_corpus, gate.freeze_table, gate.freeze_rule):
        with pytest.raises(GateError, match="already holds"):
            freeze(exp)
    assert exp.manifest.read_bytes() == before


def test_the_manifest_holds_the_hashes_and_the_model_pin(exp):
    ready(exp)
    m = gate.read_manifest(exp)
    assert m["model_pin"] == "jev-1.14.0" and m["rule"] == loader.sha256_file(exp.rule)
    assert set(m) == {"corpus", "selection_criteria", "labelling_record", "questions", "model_pin", "table_answers",
                      "table_provenance", "rule"}


def test_freeze_rule_refuses_an_unset_value(exp):
    gate.freeze_corpus(exp)
    with pytest.raises(loader.LoadError, match="UNSET"):
        gate.freeze_rule(exp)
    assert "rule" not in gate.read_manifest(exp)


def test_freeze_table_refuses_until_gate1_passes_and_when_a_file_is_missing(exp):
    with pytest.raises(GateError, match="Gate 1"):
        gate.freeze_table(exp)
    gate.freeze_corpus(exp)
    exp.table_provenance.unlink()
    with pytest.raises(GateError, match="missing"):
        gate.freeze_table(exp)


@pytest.mark.parametrize("rewrite,match", [
    (lambda rows: [{"prompt_id": r["prompt_id"]} for r in rows], "has no answer field"),
    (lambda rows: rows + [rows[0]], "more than once"),
    (lambda rows: [dict(rows[0], answer="urgent")] + rows[1:], "neither null nor one of the six"),
    (lambda rows: rows[:-1], "lack a row for corpus prompt"),
    (lambda rows: rows + [{"prompt_id": "zz", "answer": None}], "not in the corpus"),
])
def test_freeze_table_refuses_a_table_that_does_not_match_the_corpus_and_freezes_nothing(exp, rewrite, match):
    gate.freeze_corpus(exp)
    rows = [json.loads(line) for line in exp.table_answers.read_text().splitlines()]
    exp.table_answers.write_text("\n".join(json.dumps(r) for r in rewrite(rows)) + "\n")
    with pytest.raises(loader.LoadError, match=match):
        gate.freeze_table(exp)
    assert "table_answers" not in gate.read_manifest(exp) and events.latest(exp, "freeze")["what"] == "corpus"
    assert gate.main(["freeze-table", "--root", str(exp.root)]) == 1


def test_freeze_corpus_refuses_a_corpus_the_screen_refuses(exp):
    rows = [json.loads(line) for line in exp.corpus.read_text().splitlines()]
    rows[0]["text"] = "see https://github.com/example/project"
    exp.corpus.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    with pytest.raises(loader.LoadError, match="privacy"):
        gate.freeze_corpus(exp)
    assert gate.read_manifest(exp) == {}


@pytest.mark.parametrize("result,match", [((1, "1 failed, 3 passed"), "failed"), ((0, "no tests ran"), "no tests")])
def test_record_tests_refuses_a_failing_or_empty_run(exp, result, match):
    with pytest.raises(GateError, match=match):
        gate.record_tests(exp, runner=lambda cmd: result)
    assert events.latest(exp, "tests_passed") is None


def test_record_tests_records_the_command_count_and_hashes(exp):
    rec = gate.record_tests(exp, runner=PASSING)
    assert rec["count"] == 12 and rec["command"].startswith("uv run pytest ") and rec["command"].endswith(" -v")
    assert rec["code_hashes"]["code/questions.py"] == loader.sha256_file(exp.questions_py)
    assert rec["code_hashes"]["jevlib/a.py"] == loader.sha256_file(exp.jevlib_dir / "a.py")


def test_the_recorded_test_command_is_the_repo_relative_form_the_plan_names():
    # a read-only look at the real paths: nothing is run and nothing is written
    assert gate._tests_command(loader.Paths()) == ["uv", "run", "pytest", ".dev/research/jev-vs-keyword-table-611/harness/tests", "-v"]


def test_the_gate_command_line_returns_one_on_a_failure_and_zero_on_a_pass(exp, capsys):
    assert gate.main(["gate1", "--root", str(exp.root)]) == 1
    assert "FAILED: manifest_missing" in capsys.readouterr().out
    gate.freeze_corpus(exp)
    assert gate.main(["gate1", "--root", str(exp.root)]) == 0
    assert gate.main(["freeze-corpus", "--root", str(exp.root)]) == 1          # a second freeze is refused
    assert "already holds" in capsys.readouterr().err


# ---- events (append-only, evidence, the three commands)

def test_events_are_appended_never_rewritten_and_carry_time_path_and_hash(exp):
    first = events.append_event(exp, "freeze", evidence=exp.corpus, what="corpus")
    text1 = exp.events.read_text()
    events.append_event(exp, "gate1", passed=True, failed=[])
    assert exp.events.read_text().startswith(text1)
    assert exp.events.read_text().count("\n") == 2
    assert first["evidence"] == "corpus/corpus.jsonl" and first["evidence_sha256"] == loader.sha256_file(exp.corpus)
    assert first["ts"].endswith("+00:00")
    assert [e["event"] for e in events.read_events(exp)] == ["freeze", "gate1"]
    assert events.latest(exp, "freeze")["what"] == "corpus" and events.latest(exp, "verdict") is None


def test_every_event_kind_the_setup_writes_carries_a_time_a_path_and_a_hash(exp):
    ready(exp)
    gate.gate1(exp)
    gate.gate2(exp)
    events.append_event(exp, "first_request")
    log = events.read_events(exp)
    assert {e["event"] for e in log} >= {"freeze", "rule_freeze", "price_confirmed", "tests_passed", "lead_go", "gate1", "gate2",
                                         "first_request"}
    for e in log:
        assert e["ts"] and e["evidence"], e["event"]
        assert re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]), e["event"]
    assert events.latest(exp, "gate2")["evidence"] == "decision-rule.md"          # no evidence of its own: tied to the rule file


def test_an_evidence_path_that_is_not_a_file_is_refused(exp, tmp_path):
    with pytest.raises(ValueError, match="does not exist"):
        events.append_event(exp, "freeze", evidence=tmp_path / "nope.txt")
    with pytest.raises(SystemExit):
        events.main(["owner-input", "--evidence", str(tmp_path / "nope.txt"), "--note", "x", "--root", str(exp.root)])
    assert events.read_events(exp) == []


def test_events_refuse_an_unknown_name_and_a_reserved_field(exp):
    with pytest.raises(ValueError):
        events.append_event(exp, "made_up")
    with pytest.raises(ValueError):
        events.append_event(exp, "gate1", ts="now")


def test_the_three_event_commands_write_their_events(exp, tmp_path):
    note = tmp_path / "input.txt"
    note.write_text("owner answer\n")
    assert events.main(["owner-input", "--evidence", str(note), "--note", "owner set the operators", "--root", str(exp.root)]) == 0
    assert events.main(["price", "--usd-per-mtok", "0.05", "--source", "vendor page", "--root", str(exp.root)]) == 0
    assert events.main(["go", "--words", "go ahead", "--root", str(exp.root)]) == 0
    got = {e["event"]: e for e in events.read_events(exp)}
    assert set(got) == {"owner_input_received", "price_confirmed", "lead_go"}
    assert got["owner_input_received"]["evidence_sha256"] == loader.sha256_file(note)
    assert got["price_confirmed"]["usd_per_mtok"] == 0.05
    assert got["lead_go"]["rule_sha256"] == loader.sha256_file(exp.rule) and got["lead_go"]["words"] == "go ahead"
    assert all(e["evidence"] and re.fullmatch(r"[0-9a-f]{64}", e["evidence_sha256"]) for e in got.values())


def test_the_price_command_refuses_a_price_of_zero(exp):
    with pytest.raises(SystemExit):
        events.main(["price", "--usd-per-mtok", "0", "--source", "x", "--root", str(exp.root)])


# ---- spend

def test_spend_estimates_follow_the_client_formula():
    req = build_request({"prompt": "x"}, questions.build_questions())
    assert spend.estimate_request_tokens(req) == math.ceil(len(canonical_bytes(req)) / RESERVE_BYTES_PER_TOKEN)
    assert spend.estimate_run_tokens([req, req, req]) == 6 * spend.estimate_request_tokens(req)
    assert spend.estimate_run_tokens([]) == 0


def test_spend_ceiling_and_worst_case_follow_the_price():
    assert spend.ceiling_tokens(1.0, 0.042) == 23809523
    assert spend.ceiling_tokens(1.0, 0.084) == 11904761
    assert spend.worst_case_usd(1_000_000, 0.042) == pytest.approx(0.042)
