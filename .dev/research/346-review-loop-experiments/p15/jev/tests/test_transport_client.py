import json
import os

import pytest

from jevlib.budget import Budget
from jevlib.client import JevClient, KeyMissing, KeyRejected
from jevlib.journal import Journal
from jevlib.questions import choice, noul
from jevlib.transport import MockStep, MockTransport, TransportError, TransportTimeout, fake_answer

QS = {"late": noul("Did it arrive late?", "It came after the date.", "It came on or before the date.")}
ST = {"message": "The parcel arrived two days after the promised date."}
KEY = "FAKEJEVKEY" + "Q" * 30


def mk(tmp_path, steps, live=True, phase="probe", **kw):
    b = Budget(tmp_path / "b.json", ceiling_usd=1.0, ceiling_input_tokens=10_000_000)
    j = Journal(tmp_path / "j.jsonl")
    t = MockTransport(steps)
    sleeps = []
    c = JevClient(experiment="T", phase=phase, budget=b, journal=j, transport=t, live=live,
                  sleep=sleeps.append, **kw)
    return c, t, b, j, sleeps


def ok_step():
    return MockStep(200, lambda_body())


def lambda_body():
    from jevlib.questions import build_request
    return fake_answer(build_request(ST, QS), 1, 0.9)


def ask(c, **kw):
    return c.ask(ST, QS, case_id="c1", qset_version="t-q1", data_classes={"synthetic"}, purpose="t", **kw)


@pytest.fixture(autouse=True)
def _key(monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", KEY)


def test_dry_run_makes_no_network_object(tmp_path):
    b = Budget(tmp_path / "b.json", ceiling_usd=1.0, ceiling_input_tokens=1_000_000)
    c = JevClient(experiment="T", phase="dryrun", budget=b, journal=Journal(tmp_path / "j.jsonl"), live=False)
    assert c.transport is None
    r = ask(c)
    assert (r.status, r.error) == ("refused", "dry_run")
    rec = [json.loads(x) for x in (tmp_path / "j.jsonl").read_text().splitlines()]
    assert rec[-1]["request"]["questions"]["late"]["type"] == "noul" and rec[-1]["final"] is True
    assert b.state()["spent_tokens"] == 0


def test_key_missing_raises_when_live(tmp_path, monkeypatch):
    monkeypatch.delenv("JEV_API_KEY")
    c, t, b, *_ = mk(tmp_path, [])
    with pytest.raises(KeyMissing):
        ask(c)
    assert t.calls == [] and b.state()["spent_tokens"] == 0


def test_401_raises_key_rejected_no_retry(tmp_path):
    c, t, *_ = mk(tmp_path, [MockStep(401, {"detail": "bad key"})])
    with pytest.raises(KeyRejected):
        ask(c)
    assert len(t.calls) == 1


def test_429_then_200_retries_once_and_honours_retry_after_cap(tmp_path):
    c, t, b, j, sleeps = mk(tmp_path, [MockStep(429, None, {"Retry-After": "100"}), ok_step()])
    r = ask(c)
    assert r.status == "ok" and r.attempts == 2 and sleeps == [20.0]
    assert r.answers["late"]["p"] == 0.9
    recs = [json.loads(x) for x in (tmp_path / "j.jsonl").read_text().splitlines()]
    assert [x["final"] for x in recs] == [False, False, True]
    assert b.state()["spent_tokens"] > 0


def test_529_twice_unavailable(tmp_path):
    c, t, b, j, sleeps = mk(tmp_path, [MockStep(529), MockStep(529)])
    r = ask(c)
    assert (r.status, r.error, r.attempts) == ("unavailable", "http_529", 2)
    assert sleeps == [2.0] and b.state()["spent_tokens"] == 0


def test_timeout_then_timeout_unavailable(tmp_path):
    c, t, *_ , sleeps = mk(tmp_path, [MockStep(exc=TransportTimeout("t")), MockStep(exc=TransportTimeout("t"))])
    r = ask(c)
    assert (r.status, r.error, r.attempts) == ("unavailable", "timeout", 2)
    c2, *_ = mk(tmp_path / "x", [MockStep(exc=TransportError("reset")), MockStep(exc=TransportError("reset"))])
    assert ask(c2).error == "transport"


def test_deadline_prevents_retry(tmp_path):
    b = Budget(tmp_path / "b.json", ceiling_usd=1.0, ceiling_input_tokens=10_000_000)
    t = MockTransport([MockStep(503), ok_step()])
    now = [0.0]
    def clock():
        now[0] += 30.0           # every look at the clock costs 30 s
        return now[0]
    sleeps = []
    c = JevClient(experiment="T", phase="probe", budget=b, journal=Journal(tmp_path / "j.jsonl"), transport=t, live=True,
                  clock=clock, sleep=sleeps.append)
    r = ask(c)
    assert (r.status, r.attempts) == ("unavailable", 1) and sleeps == [] and len(t.calls) == 1


def test_400_max_tokens_exceeded_refused_oversize_server(tmp_path):
    c, t, *_ = mk(tmp_path, [MockStep(400, {"detail": "max_tokens_exceeded"})])
    r = ask(c)
    assert (r.status, r.error, r.attempts) == ("refused", "oversize_server", 1)


def test_422_invalid_no_retry(tmp_path):
    c, t, *_ = mk(tmp_path, [MockStep(422, {"detail": "bad"})])
    r = ask(c)
    assert (r.status, r.error) == ("invalid", "http_422") and len(t.calls) == 1


def test_oversize_refused_locally_without_call(tmp_path):
    c, t, *_ = mk(tmp_path, [])
    r = c.ask({"text": "word " * 60_000}, QS, case_id="big", qset_version="t", data_classes={"synthetic"}, purpose="t")
    assert (r.status, r.error) == ("refused", "oversize") and t.calls == []
    r = c.ask({"text": "word " * 35_000}, QS, case_id="big2", qset_version="t", data_classes={"synthetic"}, purpose="t")
    assert r.error == "oversize"      # single-question limit (32k) is lower than the request limit


def test_privacy_refuses_email_path_and_unknown_class(tmp_path):
    c, t, *_ = mk(tmp_path, [])
    for text in ("mail me at someone@example.com", "see /home/user/x", "/tmp/claude-0/x", "IronbellyOrg", "github.com/x/y"):
        r = c.ask({"m": text}, QS, case_id="p", qset_version="t", data_classes={"synthetic"}, purpose="t")
        assert (r.status, r.error) == ("refused", "privacy"), text
    r = c.ask(ST, QS, case_id="p", qset_version="t", data_classes={"customer_data"}, purpose="t")
    assert r.error == "privacy"
    assert t.calls == []


def test_privacy_does_not_refuse_task_based_words(tmp_path):
    c, t, *_ = mk(tmp_path, [ok_step()])
    r = c.ask({"m": "task-based and risk-based review"}, QS, case_id="p", qset_version="t", data_classes={"synthetic"}, purpose="t")
    assert r.status == "ok"


def test_invalid_response_never_returns_answers(tmp_path):
    body = lambda_body(); body["model"] = "jev-latest"
    c, t, b, *_ = mk(tmp_path, [MockStep(200, body)])
    r = ask(c)
    assert (r.status, r.error, r.answers) == ("invalid", "model_mismatch", None)
    assert b.state()["spent_tokens"] > 0       # a served 200 is charged (usage or estimate)


def test_mock_transport_never_stores_authorization(tmp_path):
    c, t, *_ = mk(tmp_path, [ok_step()])
    ask(c)
    assert t.calls and all("authorization" not in {k.lower() for k in h} for _, h, _ in t.calls)
    assert KEY.encode() not in b"".join(x[2] for x in t.calls)


def test_cache_in_live_phase_rejected(tmp_path):
    from jevlib.cache import ResponseCache
    with pytest.raises(ValueError):
        mk(tmp_path, [], phase="live", cache=ResponseCache(tmp_path / "c"))


def test_unexpected_status_is_invalid(tmp_path):
    c, *_ = mk(tmp_path, [MockStep(404, "nope")])
    assert ask(c).error == "http_404"


def test_logical_call_id_counter(tmp_path):
    c, *_ = mk(tmp_path, [ok_step(), ok_step()])
    assert ask(c).logical_call_id == "T:probe:c1:t-q1:1"
    assert ask(c).logical_call_id == "T:probe:c1:t-q1:2"
