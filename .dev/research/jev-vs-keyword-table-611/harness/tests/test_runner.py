import json
import os
import pathlib
import subprocess
import sys

import pytest
from conftest import FAKE_KEY
from harness import events, gate, loader, runner, spend
from jevlib import config
from jevlib.budget import Budget, BudgetExhausted
from jevlib.transport import MockStep, MockTransport, TransportTimeout, fake_answer

KEYSCAN = loader.JEVLIB_DIR.parent / "keyscan.py"
PASSING = lambda cmd: (0, "12 passed in 0.1s")  # noqa: E731


def text(i):
    return f"synthetic problem text number {i}"


def mock(plan=None):
    """A mock transport that answers every request validly; ``plan`` maps a prompt text to steps (or callables of the request)
    returned first for that prompt."""
    plan = {k: list(v) for k, v in (plan or {}).items()}

    def script(req):
        queue = plan.get(req["state"]["prompt"])
        if queue:
            step = queue.pop(0)
            return step(req) if callable(step) else step
        return MockStep(200, fake_answer(req))
    return MockTransport(script)


@pytest.fixture
def exp(exp, monkeypatch):
    """The command line builds ``Paths`` from a root alone, so point its default jevlib folder at the fixture's stand-in."""
    monkeypatch.setattr(loader, "JEVLIB_DIR", exp.jevlib_dir)
    return exp


def go(exp, transport, run_id="r1", price=0.042):
    rule = loader.load_rule(exp.rule)
    return runner.execute(exp, rule, loader.load_corpus(exp.corpus), run_id, transport, price)


def rows_of(exp, run_id="r1"):
    return [json.loads(line) for line in (exp.runs / run_id / "jev-rows.jsonl").read_text().splitlines() if line.strip()]


def ledger_of(exp):
    return json.loads(exp.ledger.read_text())


def gated(exp):
    """Freeze everything and confirm the price and the go: the state in which ``runner.py run`` passes both gates."""
    s = exp.rule.read_text(encoding="utf-8")
    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
    exp.rule.write_text(s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3"), encoding="utf-8")
    gate.freeze_corpus(exp)
    gate.freeze_table(exp)
    gate.freeze_rule(exp)
    events.append_event(exp, "price_confirmed", usd_per_mtok=0.042, source="test")
    gate.record_tests(exp, runner=PASSING)
    events.append_event(exp, "lead_go", rule_sha256=loader.sha256_file(exp.rule), words="go")


# ---- one rerun per failed prompt (T-06)

def test_a_failed_first_attempt_gets_exactly_one_rerun(exp, fake_key):
    t = mock({text(0): [MockStep(500)]})
    out = go(exp, t)
    assert out["reason"] == "completed" and len(t.calls) == 9 and out["ok"] == 8
    p0 = rows_of(exp)[0]
    assert [a["status"] for a in p0["attempts"]] == ["unavailable", "ok"] and p0["final_status"] == "ok" and p0["model"] == config.MODEL
    journal = [json.loads(line) for line in (exp.runs / "r1" / "journal.jsonl").read_text().splitlines()]
    final_p0 = [j for j in journal if j["case_id"] == "p0" and j["final"]]
    assert len({j["logical_call_id"] for j in final_p0}) == 2
    assert len(ledger_of(exp)["draws"]) == 9


def test_a_prompt_that_fails_twice_is_an_error_with_exactly_two_posts(exp, fake_key):
    t = mock({text(0): [MockStep(500), MockStep(503)]})
    out = go(exp, t)
    assert out["reason"] == "completed" and out["ok"] == 7
    assert len([c for c in t.calls if text(0).encode() in c[2]]) == 2 and len(t.calls) == 9
    p0 = rows_of(exp)[0]
    assert p0["final_status"] == "error" and len(p0["attempts"]) == 2 and p0["choice"] is None and p0["noul"] is None


def test_a_timeout_is_rerun_and_is_not_a_stop(exp, fake_key):
    t = mock({text(0): [MockStep(exc=TransportTimeout("slow"))]})
    out = go(exp, t)
    p0 = rows_of(exp)[0]
    assert out["reason"] == "completed" and p0["attempts"][0]["timed_out"] is True and p0["attempts"][1]["status"] == "ok"
    assert all(isinstance(a["latency_s"], float) for a in p0["attempts"])


# ---- systemic signals end the run with no rerun (T-13, M-1)

def test_a_missing_key_ends_the_run_with_zero_posts(exp, monkeypatch):
    monkeypatch.delenv("JEV_API_KEY", raising=False)
    t = mock()
    out = go(exp, t)
    assert out["reason"] == "key_missing" and t.calls == [] and rows_of(exp) == []
    assert events.latest(exp, "run_end")["reason"] == "key_missing"


def test_a_rejected_key_ends_the_run_after_one_post(exp, fake_key):
    t = mock({text(0): [MockStep(401)]})
    out = go(exp, t)
    assert out["reason"] == "key_rejected" and len(t.calls) == 1
    assert [r["final_status"] for r in rows_of(exp)] == ["error"] and rows_of(exp)[0]["attempts"][0]["status"] == "key_rejected"


def test_a_returned_model_other_than_the_pin_ends_the_run_after_one_post(exp, fake_key):
    t = mock({text(0): [lambda req: MockStep(200, dict(fake_answer(req), model="jev-9.9.9"))]})
    out = go(exp, t)
    assert out["reason"] == "model_mismatch" and len(t.calls) == 1 and len(rows_of(exp)) == 1


def test_a_budget_exhausted_result_stops_the_run_with_no_rerun(exp, fake_key, monkeypatch):
    class Stingy(Budget):
        draws = 0

        def draw(self, phase, est_tokens):
            Stingy.draws += 1
            if Stingy.draws > 2:
                raise BudgetExhausted("stand-in ledger")
            return super().draw(phase, est_tokens)

    monkeypatch.setattr(runner, "Budget", Stingy)
    t = mock()
    out = go(exp, t)
    assert out["reason"] == "budget_exhausted" and len(t.calls) == 2
    last = rows_of(exp)[-1]
    assert len(rows_of(exp)) == 3 and last["final_status"] == "error" and len(last["attempts"]) == 1


# ---- the whole-run reservation (T-09)

def run_estimate(exp):
    import questions
    from jevlib.questions import build_request
    qs = questions.build_questions()
    reqs = [build_request({"prompt": r["text"]}, qs) for r in loader.load_corpus(exp.corpus)]
    return spend.estimate_run_tokens(reqs), max(spend.estimate_request_tokens(r) for r in reqs)


def test_a_ledger_where_every_request_fits_but_the_whole_run_does_not_gives_zero_posts(exp, fake_key):
    total, biggest = run_estimate(exp)
    cap = spend.ceiling_tokens(1.0, 0.042)
    left = total - 10
    assert left > biggest
    exp.ledger.parent.mkdir()
    exp.ledger.write_text(json.dumps({"experiment": "spend", "ceiling_usd": 1.0, "ceiling_input_tokens": cap, "spent_tokens": cap - left,
                                      "spent_usd": 0.0, "reserved": {}, "draws": {}}))
    t = mock()
    out = go(exp, t)
    assert out["reason"] == "spend_bound" and t.calls == [] and ledger_of(exp)["reserved"] == {}
    assert events.latest(exp, "run_end")["reason"] == "spend_bound" and events.latest(exp, "first_request") is None
    assert (exp.runs / "r1" / "run-record.md").is_file()


def test_a_completed_run_leaves_nothing_reserved_and_spend_carries_across_runs(exp, fake_key):
    go(exp, mock(), run_id="r1")
    one = ledger_of(exp)
    assert one["reserved"] == {} and one["spent_tokens"] > 0
    go(exp, mock(), run_id="r2")
    two = ledger_of(exp)
    assert two["reserved"] == {} and two["spent_tokens"] == 2 * one["spent_tokens"]


def test_a_higher_confirmed_price_lowers_the_token_ceiling(exp, fake_key, monkeypatch):
    seen = []

    class Spy(Budget):
        def __init__(self, path, **kw):
            seen.append(kw)
            super().__init__(path, **kw)

    monkeypatch.setattr(runner, "Budget", Spy)
    go(exp, mock(), price=0.084)
    assert seen[0]["ceiling_input_tokens"] == spend.ceiling_tokens(1.0, 0.084)
    assert seen[0]["ceiling_input_tokens"] < spend.ceiling_tokens(1.0, config.PRICE_USD_PER_MTOK_INPUT)


# ---- limits, rehearsal, the command line

def test_limits_set_and_restore_the_client_settings_also_after_an_exception():
    rule = {"attempt_timeout_s": 10.0}
    assert (config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S) == (1, 20.0)
    with runner.limits(rule):
        assert (config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S) == (0, 10.0)
    with pytest.raises(RuntimeError), runner.limits(rule):
        raise RuntimeError("boom")
    assert (config.MAX_RETRIES, config.ATTEMPT_TIMEOUT_S) == (1, 20.0)


class Recorder(dict):
    """A stand-in for ``os.environ`` that records which names are read."""

    def __init__(self, base):
        super().__init__(base)
        self.reads = []

    def get(self, key, default=None):
        self.reads.append(key)
        return super().get(key, default)

    def __getitem__(self, key):
        self.reads.append(key)
        return super().__getitem__(key)

    def __contains__(self, key):
        self.reads.append(key)
        return super().__contains__(key)


def test_a_failing_gate_leaves_the_key_and_url_variables_unread(exp, monkeypatch, capsys):
    rec = Recorder(os.environ)
    with monkeypatch.context() as m:
        m.setattr(os, "environ", rec)
        rc = runner.main(["run", "--run-id", "r1", "--live", "--root", str(exp.root)], transport=mock())
    assert rc == 1 and "GATE 1 FAILED" in capsys.readouterr().err
    assert not {"TYPESAFE_API_KEY", "JEV_API_KEY", "JEV_API_URL"} & set(rec.reads)
    assert not (exp.runs / "r1").exists()


def test_run_without_live_exits_two_before_any_gate(exp, capsys):
    assert runner.main(["run", "--run-id", "r1", "--root", str(exp.root)]) == 2
    assert "--live" in capsys.readouterr().err
    assert not exp.events.exists()                                  # a gate would have written its event


def test_run_refuses_an_existing_run_folder(exp, capsys):
    (exp.runs / "r1").mkdir(parents=True)
    assert runner.main(["run", "--run-id", "r1", "--live", "--root", str(exp.root)]) == 2
    assert not exp.events.exists()


def test_run_passes_the_gates_then_copies_the_key_and_never_prints_it(exp, monkeypatch, capsys):
    gated(exp)
    monkeypatch.setenv("JEV_API_KEY", "placeholder")               # so the test restores the variable afterwards
    monkeypatch.setenv("TYPESAFE_API_KEY", FAKE_KEY)
    t = mock()
    assert runner.main(["run", "--run-id", "r1", "--live", "--root", str(exp.root)], transport=t) == 0
    shown = capsys.readouterr()
    assert FAKE_KEY not in shown.out + shown.err and os.environ["JEV_API_KEY"] == FAKE_KEY
    assert [e["event"] for e in events.read_events(exp)][-4:] == ["gate1", "gate2", "first_request", "run_end"]
    assert len(t.calls) == 8 and events.latest(exp, "run_end")["reason"] == "completed"
    assert gate.gate2(exp) == ["prior_run"]                          # a second live run is refused
    for f in exp.root.rglob("*"):
        assert not f.is_file() or FAKE_KEY.encode() not in f.read_bytes(), f


def test_run_without_a_key_refuses_after_the_gates(exp, monkeypatch, capsys):
    gated(exp)
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    assert runner.main(["run", "--run-id", "r1", "--live", "--root", str(exp.root)], transport=mock()) == 1
    assert "TYPESAFE_API_KEY is not set" in capsys.readouterr().err and not (exp.runs / "r1").exists()


@pytest.mark.parametrize("bad", ["../escape", "/tmp/jev611-abs-run-id", "a/b", ".."])
def test_a_run_id_that_is_not_a_plain_name_is_refused_before_any_effect(exp, bad, capsys):
    assert runner.main(["run", "--run-id", bad, "--live", "--root", str(exp.root)]) == 2
    assert "run id may hold only" in capsys.readouterr().err
    assert not exp.events.exists() and not exp.runs.exists()           # no gate ran, nothing was created
    with pytest.raises(ValueError, match="run id may hold only"):
        go(exp, mock(), run_id=bad)
    assert not exp.runs.exists() and not (exp.root.parent / "escape").exists() and not pathlib.Path("/tmp/jev611-abs-run-id").exists()


class Boom:
    calls = 0

    def post(self, *a, **k):
        Boom.calls += 1
        raise AssertionError("a rehearsal posted")


def test_rehearse_never_posts_and_leaves_the_real_files_alone(exp, tmp_path):
    out = runner.rehearse(exp, tmp_path / "rh", transport=Boom())
    assert Boom.calls == 0 and out["prompts"] == 8 and out["dry_run_refusals"] == 8 and out["whole_run_estimate_tokens"] > 0
    assert not exp.events.exists() and not exp.ledger.exists() and not exp.runs.exists()
    assert (tmp_path / "rh" / "ledger.json").is_file()


def test_rehearse_refuses_a_folder_under_the_ledger_or_runs(exp, capsys):
    for bad in (exp.ledger.parent / "x", exp.runs, exp.runs / "y"):
        assert runner.main(["rehearse", "--out", str(bad), "--root", str(exp.root)]) == 2
        assert "must not be inside" in capsys.readouterr().err
    assert not exp.ledger.parent.exists() and not exp.runs.exists()


def test_rehearse_through_the_command_line_needs_no_gate_and_no_key(exp, tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("JEV_API_KEY", raising=False)
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    assert runner.main(["rehearse", "--out", str(tmp_path / "rh"), "--root", str(exp.root)]) == 0
    assert json.loads(capsys.readouterr().out)["prompts"] == 8


# ---- written files (T-10) and the run record

def test_no_written_file_holds_the_key_even_when_an_error_body_quotes_it(exp, fake_key):
    gated(exp)
    t = mock({text(0): [MockStep(500, body=f"upstream rejected {FAKE_KEY} twice"), MockStep(500, body=FAKE_KEY)]})
    out = go(exp, t)
    assert out["reason"] == "completed"
    paths = [str(exp.runs / "r1"), str(exp.events), str(exp.manifest), str(exp.ledger)]
    res = subprocess.run([sys.executable, str(KEYSCAN), "--fake", FAKE_KEY, *paths], capture_output=True, text=True)
    assert "KEYSCAN OK" in res.stdout and res.returncode == 0, res.stdout + res.stderr
    assert "[REDACTED]" in (exp.runs / "r1" / "journal.jsonl").read_text()
    assert FAKE_KEY not in res.stdout + res.stderr


def test_the_run_record_exists_after_a_completed_and_after_a_stopped_run(exp, fake_key):
    go(exp, mock(), run_id="done")
    go(exp, mock({text(1): [MockStep(401)]}), run_id="stopped")
    done = (exp.runs / "done" / "run-record.md").read_text(encoding="utf-8")
    stopped = (exp.runs / "stopped" / "run-record.md").read_text(encoding="utf-8")
    assert "Ended with: completed" in done and "Ended with: key_rejected" in stopped
    assert loader.sha256_file(exp.runs / "done" / "jev-rows.jsonl") in done and config.MODEL in done
    assert [e["reason"] for e in events.read_events(exp) if e["event"] == "run_end"] == ["completed", "key_rejected"]


def test_an_unexpected_error_still_writes_the_run_record_and_the_run_end_event(exp, fake_key, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("unexpected")
    monkeypatch.setattr(runner, "_ask", boom)
    out = go(exp, mock())
    assert out["reason"] == "crashed_RuntimeError" and (exp.runs / "r1" / "run-record.md").is_file()
    assert ledger_of(exp)["reserved"] == {}


def test_runner_holds_no_url_literal_and_posts_only_through_the_client():
    src = pathlib.Path(runner.__file__).read_text(encoding="utf-8")
    assert "http://" not in src and "https://" not in src
