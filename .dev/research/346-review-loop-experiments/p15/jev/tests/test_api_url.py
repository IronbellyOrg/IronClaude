"""JEV_API_URL override: the gateway route replaces the vendor URL, with strict validation (refs #346)."""
import pytest

from jevlib import config as C
from jevlib.budget import Budget
from jevlib.client import JevClient
from jevlib.journal import Journal
from jevlib.questions import build_request, noul
from jevlib.transport import MockStep, MockTransport, fake_answer

ST = {"m": "hello"}
Q = {"q": noul("Is it so?", "It is so.", "It is not so.")}


def test_default_is_the_vendor_url():
    assert C.api_url({}) == C.API_URL == "https://api.typesafe.ai/v1/systemone"
    assert C.api_url({"JEV_API_URL": ""}) == C.API_URL


def test_https_override_is_used_verbatim():
    u = "https://llm-gateway.example.internal/jev/v1/systemone"
    assert C.api_url({"JEV_API_URL": u}) == u


@pytest.mark.parametrize("bad", [
    "http://llm-gateway.example.internal/jev",      # plain http to a non-loopback host
    "ftp://x.example/v1",
    "https://user:pw@gw.example/v1",                 # credentials in the URL
    "https://gw.example/v1?key=abc",                 # query
    "https://gw.example/v1#frag",
    "https:///no-host",
    "not a url",
])
def test_bad_override_raises_and_never_falls_back(bad):
    with pytest.raises(ValueError, match="JEV_API_URL"):
        C.api_url({"JEV_API_URL": bad})


@pytest.mark.parametrize("ok", [
    "http://127.0.0.1:8099/v1/systemone",           # loopback mock
    "http://192.168.133.101:4000/cli/v1/systemone",  # the internal gateway: plain http on a private address
    "http://10.1.2.3/jev",
])
def test_http_is_allowed_for_loopback_and_private_ip_literals(ok):
    assert C.api_url({"JEV_API_URL": ok}) == ok


@pytest.mark.parametrize("bad", ["http://8.8.8.8/v1", "http://gateway.corp/v1", "http://[2606:4700:4700::1111]/v1"])
def test_http_is_refused_for_public_addresses_and_names(bad):
    with pytest.raises(ValueError, match="JEV_API_URL"):
        C.api_url({"JEV_API_URL": bad})


def _client(tmp_path, steps):
    b = Budget(tmp_path / "b.json", ceiling_usd=1.0, ceiling_input_tokens=10**7)
    t = MockTransport(steps)
    c = JevClient(experiment="T", phase="calibration", budget=b, journal=Journal(tmp_path / "j.jsonl"), transport=t,
                  live=True, sleep=lambda s: None)
    return c, t


def _ask(c):
    return c.ask(ST, Q, case_id="a", qset_version="v", data_classes={"synthetic"}, purpose="t")


def test_client_posts_to_the_override_and_still_checks_the_model(tmp_path, monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", "FAKEJEVKEY" + "7" * 30)
    monkeypatch.setenv("JEV_API_URL", "https://gw.example/jev/v1/systemone")
    c, t = _client(tmp_path, [MockStep(200, fake_answer(build_request(ST, Q), 1, 0.3))])
    r = _ask(c)
    assert r.status == "ok"
    assert t.calls[0][0] == "https://gw.example/jev/v1/systemone"
    assert "gw.example" not in str(t.calls[0][1])  # url is not echoed into headers


def test_gateway_that_rewrites_the_model_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", "FAKEJEVKEY" + "7" * 30)
    monkeypatch.setenv("JEV_API_URL", "https://gw.example/jev/v1/systemone")
    body = fake_answer(build_request(ST, Q), 1, 0.3)
    body["model"] = "jev-latest"
    c, t = _client(tmp_path, [MockStep(200, body)])
    r = _ask(c)
    assert r.status != "ok" and "model_mismatch" in str(r.error)


def test_bad_override_sends_nothing_and_releases_the_budget(tmp_path, monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", "FAKEJEVKEY" + "7" * 30)
    monkeypatch.setenv("JEV_API_URL", "http://not-loopback.example/v1")
    c, t = _client(tmp_path, [MockStep(200, fake_answer(build_request(ST, Q), 1, 0.3))])
    with pytest.raises(ValueError):
        _ask(c)
    assert t.calls == []
